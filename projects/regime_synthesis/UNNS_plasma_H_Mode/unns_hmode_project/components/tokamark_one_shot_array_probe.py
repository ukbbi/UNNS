#!/usr/bin/env python3
"""
tokamark_one_shot_array_probe.py

UNNS-H Mode Project
TokaMark / MAST one-shot array probe.

Purpose
-------
Fetch selected diagnostic arrays for one public TokaMark/MAST shot and produce
compact signal summaries for a future UNNS-H Mode time-resolved positive-corridor
probe.

This component is intentionally narrow.

It does:
    1. Fetch `.zmetadata` by HTTPS.
    2. Read only selected arrays by direct HTTP chunk requests.
    3. Save compact summaries.
    4. Compute first raw diagnostic proxies:
       - NBI power trace summary
       - line-density trace summary
       - D-alpha trace summary
       - soft-X activity trace summary
       - Thomson edge Te/ne profile summaries
       - equilibrium geometry summaries

It does NOT:
    - compute final m_edge(t)
    - decide H-mode / L-H transition timing
    - classify the shot as positive corridor
    - download the whole Zarr store

Default target
--------------
    shot_id = 12063

This was ranked first in the metadata candidate scan as a FULL_PROFILE_EDGE_CANDIDATE.

Run from project root
---------------------
PowerShell:

    python components\\tokamark_one_shot_array_probe.py --shot-id 12063 --out-dir outputs\\reports

Dependencies
------------
    python -m pip install requests numpy pandas numcodecs

Outputs
-------
    outputs/reports/tokamark_shot_12063_signal_probe.csv
    outputs/reports/tokamark_shot_12063_signal_probe.json
    outputs/reports/tokamark_shot_12063_signal_probe.md
    outputs/reports/tokamark_shot_12063_proxy_timeseries_preview.csv
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd
import requests
from numcodecs import get_codec


# ---------------------------------------------------------------------------
# Target arrays
# ---------------------------------------------------------------------------

# The format is:
#   output_label: zarr array path without ".zarray"
#
# Time arrays are source-level time arrays, usually:
#   source/time
#
TARGET_ARRAYS: Dict[str, str] = {
    # Power / current / density
    "summary_power_nbi": "summary/power_nbi",
    "summary_ip": "summary/ip",
    "interferometer_n_e_line": "interferometer/n_e_line",

    # Edge response
    "dalpha_voltage": "spectrometer_visible/filter_spectrometer_dalpha_voltage",
    "soft_x_lower": "soft_x_rays/horizontal_cam_lower",
    "soft_x_upper": "soft_x_rays/horizontal_cam_upper",

    # Profiles
    "thomson_t_e": "thomson_scattering/t_e",
    "thomson_n_e": "thomson_scattering/n_e",

    # Geometry / equilibrium
    "equilibrium_q95": "equilibrium/q95",
    "equilibrium_elongation": "equilibrium/elongation",
    "equilibrium_triangularity_upper": "equilibrium/triangularity_upper",
    "equilibrium_triangularity_lower": "equilibrium/triangularity_lower",
    "equilibrium_minor_radius": "equilibrium/minor_radius",
    "equilibrium_beta_normal": "equilibrium/beta_normal",
    "equilibrium_beta_pol": "equilibrium/beta_pol",
    "equilibrium_whmd": "equilibrium/whmd",
}

TIME_ARRAYS: Dict[str, str] = {
    "summary": "summary/time",
    "interferometer": "interferometer/time",
    "spectrometer_visible": "spectrometer_visible/time",
    "soft_x_rays": "soft_x_rays/time",
    "thomson_scattering": "thomson_scattering/time",
    "equilibrium": "equilibrium/time",
}


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def request_bytes(url: str, timeout: float, retries: int, delay: float) -> bytes:
    last_error: Optional[Exception] = None
    for attempt in range(retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 404:
                raise FileNotFoundError(url)
            response.raise_for_status()
            return response.content
        except Exception as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(delay)
    raise RuntimeError(f"Could not fetch {url}: {last_error!r}")


def request_json(url: str, timeout: float, retries: int, delay: float) -> Dict[str, Any]:
    return json.loads(request_bytes(url, timeout=timeout, retries=retries, delay=delay).decode("utf-8"))


def normalize_zmetadata(zmetadata: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(zmetadata.get("metadata"), dict):
        return zmetadata["metadata"]
    return zmetadata


# ---------------------------------------------------------------------------
# Zarr v2 direct HTTP array reader
# ---------------------------------------------------------------------------

def parse_fill_value(fill_value: Any, dtype: np.dtype) -> Any:
    if fill_value is None:
        if np.issubdtype(dtype, np.floating):
            return np.nan
        return 0
    if isinstance(fill_value, str) and fill_value.lower() in {"nan", "na"}:
        return np.nan
    try:
        return dtype.type(fill_value)
    except Exception:
        return fill_value


def chunk_grid(shape: Tuple[int, ...], chunks: Tuple[int, ...]) -> Iterable[Tuple[int, ...]]:
    ranges = [range(math.ceil(s / c)) for s, c in zip(shape, chunks)]
    return itertools.product(*ranges)


def chunk_slices(idx: Tuple[int, ...], shape: Tuple[int, ...], chunks: Tuple[int, ...]) -> Tuple[Tuple[slice, ...], Tuple[slice, ...]]:
    out_slices = []
    in_slices = []
    for i, dim, chunk in zip(idx, shape, chunks):
        start = i * chunk
        stop = min(start + chunk, dim)
        valid = stop - start
        out_slices.append(slice(start, stop))
        in_slices.append(slice(0, valid))
    return tuple(out_slices), tuple(in_slices)


def decode_chunk(raw: bytes, zarray: Dict[str, Any], dtype: np.dtype) -> bytes:
    data = raw

    compressor = zarray.get("compressor")
    if compressor:
        data = get_codec(compressor).decode(data)

    filters = zarray.get("filters") or []
    # On read, filters decode after decompression. Reverse order is safest for
    # chained filters.
    for filter_spec in reversed(filters):
        data = get_codec(filter_spec).decode(data)

    return data


def zarr_chunk_key(array_path: str, idx: Tuple[int, ...], zarray: Dict[str, Any]) -> str:
    separator = zarray.get("dimension_separator", ".")
    if len(idx) == 1:
        chunk_name = str(idx[0])
    elif separator == "/":
        chunk_name = "/".join(str(i) for i in idx)
    else:
        chunk_name = ".".join(str(i) for i in idx)
    return f"{array_path}/{chunk_name}"


def read_zarr_array_http(
    *,
    base_url: str,
    metadata: Dict[str, Any],
    array_path: str,
    timeout: float,
    retries: int,
    delay: float,
    max_chunk_downloads: int = 5000,
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Read one Zarr v2 array directly over HTTP using consolidated metadata.

    Returns:
        array, read_info
    """
    zarray_key = f"{array_path}/.zarray"
    if zarray_key not in metadata:
        raise KeyError(f"Missing array metadata: {zarray_key}")

    zarray = metadata[zarray_key]
    shape = tuple(int(x) for x in zarray["shape"])
    chunks = tuple(int(x) for x in zarray["chunks"])
    dtype = np.dtype(zarray["dtype"])
    order = zarray.get("order", "C")
    fill_value = parse_fill_value(zarray.get("fill_value"), dtype)

    total_chunks = int(np.prod([math.ceil(s / c) for s, c in zip(shape, chunks)]))
    if total_chunks > max_chunk_downloads:
        raise RuntimeError(
            f"Array {array_path} requires {total_chunks} chunk downloads, above limit {max_chunk_downloads}."
        )

    out = np.empty(shape, dtype=dtype)
    try:
        out[...] = fill_value
    except Exception:
        out[...] = 0

    downloaded = 0
    missing_chunks = 0
    errors: List[str] = []

    for idx in chunk_grid(shape, chunks):
        key = zarr_chunk_key(array_path, idx, zarray)
        url = f"{base_url.rstrip('/')}/{key}"

        try:
            raw = request_bytes(url, timeout=timeout, retries=retries, delay=delay)
            decoded = decode_chunk(raw, zarray, dtype)
            chunk_arr = np.frombuffer(decoded, dtype=dtype)

            expected_full_size = int(np.prod(chunks))
            if chunk_arr.size < expected_full_size:
                # Rare but possible if stored chunk is already boundary-shaped.
                # We will reshape with inferred boundary shape below.
                pass

            # Zarr stores full chunks in most cases. Boundary chunks are clipped
            # when copied into the output array.
            full_chunk_shape = chunks
            try:
                chunk_arr = chunk_arr.reshape(full_chunk_shape, order=order)
            except Exception:
                # Fallback: boundary-shaped chunk.
                out_slices, in_slices = chunk_slices(idx, shape, chunks)
                boundary_shape = tuple(s.stop - s.start for s in out_slices)
                chunk_arr = chunk_arr.reshape(boundary_shape, order=order)

            out_slices, in_slices = chunk_slices(idx, shape, chunks)
            if chunk_arr.shape == chunks:
                out[out_slices] = chunk_arr[in_slices]
            else:
                out[out_slices] = chunk_arr

            downloaded += 1

        except FileNotFoundError:
            missing_chunks += 1
        except Exception as exc:
            missing_chunks += 1
            errors.append(f"{key}: {exc!r}")

    read_info = {
        "array_path": array_path,
        "shape": list(shape),
        "chunks": list(chunks),
        "dtype": str(dtype),
        "order": order,
        "total_chunks": total_chunks,
        "downloaded_chunks": downloaded,
        "missing_chunks": missing_chunks,
        "errors": errors[:10],
    }

    return out, read_info


# ---------------------------------------------------------------------------
# Summaries and derived proxies
# ---------------------------------------------------------------------------

def finite_stats(arr: np.ndarray) -> Dict[str, Any]:
    a = np.asarray(arr)
    numeric = pd.to_numeric(pd.Series(a.ravel()), errors="coerce").to_numpy(dtype=float)
    numeric = numeric[np.isfinite(numeric)]

    total = int(a.size)
    finite = int(numeric.size)

    if finite == 0:
        return {
            "finite_count": 0,
            "total_count": total,
            "finite_fraction": 0.0,
            "min": np.nan,
            "p05": np.nan,
            "median": np.nan,
            "mean": np.nan,
            "p95": np.nan,
            "max": np.nan,
            "std": np.nan,
        }

    return {
        "finite_count": finite,
        "total_count": total,
        "finite_fraction": float(finite / max(total, 1)),
        "min": float(np.nanmin(numeric)),
        "p05": float(np.nanpercentile(numeric, 5)),
        "median": float(np.nanmedian(numeric)),
        "mean": float(np.nanmean(numeric)),
        "p95": float(np.nanpercentile(numeric, 95)),
        "max": float(np.nanmax(numeric)),
        "std": float(np.nanstd(numeric)),
    }


def source_from_path(array_path: str) -> str:
    return array_path.split("/", 1)[0]


def summarize_signal(label: str, array_path: str, values: np.ndarray, times: Optional[np.ndarray], read_info: Dict[str, Any]) -> Dict[str, Any]:
    stats = finite_stats(values)
    row: Dict[str, Any] = {
        "label": label,
        "array_path": array_path,
        "source": source_from_path(array_path),
        "values_shape": str(tuple(values.shape)),
        "values_dtype": str(values.dtype),
        "time_shape": str(tuple(times.shape)) if times is not None else "",
        "time_min": float(np.nanmin(times)) if times is not None and np.asarray(times).size else np.nan,
        "time_max": float(np.nanmax(times)) if times is not None and np.asarray(times).size else np.nan,
        "time_count": int(np.asarray(times).size) if times is not None else 0,
    }
    row.update(stats)
    row.update({
        "chunks": str(read_info.get("chunks")),
        "total_chunks": read_info.get("total_chunks"),
        "downloaded_chunks": read_info.get("downloaded_chunks"),
        "missing_chunks": read_info.get("missing_chunks"),
    })
    return row


def reduce_channels(values: np.ndarray) -> np.ndarray:
    """
    Convert a signal to a 1D time proxy.

    If values is [channels, time], median over channels.
    If values is [time], return as-is.
    If values is [profile, time], median over profile axis.
    """
    arr = np.asarray(values, dtype=float)
    if arr.ndim == 1:
        return arr
    if arr.ndim == 2:
        return np.nanmedian(arr, axis=0)
    return np.nanmedian(arr.reshape((-1, arr.shape[-1])), axis=0)


def thomson_edge_proxy(values: np.ndarray, edge_fraction: float = 0.20) -> Dict[str, Any]:
    """
    Compute profile-level proxies from Thomson profile arrays.

    Assumption:
        The first axis is profile/radial coordinate and the second axis is time.
        Without an explicit radial coordinate in this probe, the outer edge is
        approximated as the last `edge_fraction` of profile indices.

    This is a raw probe, not final physics classification.
    """
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 2 or arr.shape[0] < 5:
        return {}

    n_profile = arr.shape[0]
    n_edge = max(1, int(round(n_profile * edge_fraction)))
    n_core = max(1, int(round(n_profile * edge_fraction)))

    core = arr[:n_core, :]
    edge = arr[-n_edge:, :]

    edge_median = np.nanmedian(edge, axis=0)
    core_median = np.nanmedian(core, axis=0)

    # Raw profile-gradient proxy along index axis.
    try:
        grad = np.nanmedian(np.abs(np.gradient(arr, axis=0)), axis=0)
    except Exception:
        grad = np.full(arr.shape[1], np.nan)

    ratio = edge_median / np.where(np.abs(core_median) > 1e-12, core_median, np.nan)

    return {
        "edge_median": edge_median,
        "core_median": core_median,
        "edge_core_ratio": ratio,
        "profile_gradient_proxy": grad,
    }


def build_proxy_preview(loaded: Dict[str, Dict[str, Any]], max_points: int = 250) -> pd.DataFrame:
    """
    Build a compact preview table from selected 1D proxies.

    This is not a common-timebase interpolation. Each proxy keeps its own native
    first `max_points` samples to avoid distorting diagnostics.
    """
    columns: Dict[str, List[Any]] = {}

    def add_series(name: str, arr: np.ndarray) -> None:
        flat = np.asarray(arr).ravel()
        n = min(max_points, flat.size)
        columns[name] = list(flat[:n]) + [np.nan] * (max_points - n)

    # Time/value previews from key sources
    for label in ["summary_power_nbi", "summary_ip", "interferometer_n_e_line"]:
        if label in loaded:
            add_series(f"{label}_value", loaded[label]["values"])
            if loaded[label].get("time") is not None:
                add_series(f"{label}_time", loaded[label]["time"])

    for label in ["dalpha_voltage", "soft_x_lower", "soft_x_upper"]:
        if label in loaded:
            add_series(f"{label}_proxy", reduce_channels(loaded[label]["values"]))
            if loaded[label].get("time") is not None:
                add_series(f"{label}_time", loaded[label]["time"])

    for label in ["thomson_t_e", "thomson_n_e"]:
        if label in loaded:
            proxies = thomson_edge_proxy(loaded[label]["values"])
            if proxies:
                add_series(f"{label}_edge_median", proxies["edge_median"])
                add_series(f"{label}_profile_gradient_proxy", proxies["profile_gradient_proxy"])
                if loaded[label].get("time") is not None:
                    add_series(f"{label}_time", loaded[label]["time"])

    if not columns:
        return pd.DataFrame()

    return pd.DataFrame(columns)


def proxy_summary(loaded: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}

    def add_proxy_stats(name: str, arr: np.ndarray) -> None:
        out[name] = finite_stats(arr)

    if "dalpha_voltage" in loaded:
        add_proxy_stats("dalpha_median_across_channels", reduce_channels(loaded["dalpha_voltage"]["values"]))

    if "soft_x_lower" in loaded:
        add_proxy_stats("soft_x_lower_median_across_channels", reduce_channels(loaded["soft_x_lower"]["values"]))

    if "soft_x_upper" in loaded:
        add_proxy_stats("soft_x_upper_median_across_channels", reduce_channels(loaded["soft_x_upper"]["values"]))

    if "thomson_t_e" in loaded:
        p = thomson_edge_proxy(loaded["thomson_t_e"]["values"])
        for key, val in p.items():
            add_proxy_stats(f"thomson_t_e_{key}", val)

    if "thomson_n_e" in loaded:
        p = thomson_edge_proxy(loaded["thomson_n_e"]["values"])
        for key, val in p.items():
            add_proxy_stats(f"thomson_n_e_{key}", val)

    return out


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def write_markdown_report(
    path: Path,
    *,
    shot_id: int,
    base_url: str,
    summary_rows: List[Dict[str, Any]],
    loaded_labels: List[str],
    failed_labels: Dict[str, str],
    proxy_stats: Dict[str, Any],
) -> None:
    df = pd.DataFrame(summary_rows)

    md: List[str] = []
    md.append(f"# TokaMark One-Shot Array Probe — Shot {shot_id}")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("This report records a controlled one-shot array probe for a candidate MAST/TokaMark discharge.")
    md.append("")
    md.append("It fetches selected arrays only and produces compact summaries. It does not compute final `m_edge(t)`.")
    md.append("")
    md.append("## Source")
    md.append("")
    md.append(f"- base URL: `{base_url}`")
    md.append(f"- shot store: `{base_url.rstrip('/')}/{shot_id}.zarr/`")
    md.append("")
    md.append("## Load status")
    md.append("")
    md.append(f"- loaded arrays: `{len(loaded_labels)}`")
    md.append(f"- failed arrays: `{len(failed_labels)}`")
    md.append("")
    if failed_labels:
        md.append("### Failed arrays")
        md.append("")
        for label, err in failed_labels.items():
            md.append(f"- `{label}`: `{err}`")
        md.append("")
    md.append("## Signal summaries")
    md.append("")
    if not df.empty:
        show_cols = [
            "label", "values_shape", "time_shape", "finite_fraction",
            "min", "median", "mean", "max", "time_min", "time_max",
            "downloaded_chunks", "missing_chunks",
        ]
        show_cols = [c for c in show_cols if c in df.columns]
        md.append(df[show_cols].to_markdown(index=False))
    else:
        md.append("_No signals loaded._")
    md.append("")
    md.append("## Raw proxy summaries")
    md.append("")
    if proxy_stats:
        proxy_table = []
        for key, stats in proxy_stats.items():
            proxy_table.append({
                "proxy": key,
                "finite_fraction": stats.get("finite_fraction"),
                "min": stats.get("min"),
                "median": stats.get("median"),
                "mean": stats.get("mean"),
                "max": stats.get("max"),
                "std": stats.get("std"),
            })
        md.append(pd.DataFrame(proxy_table).to_markdown(index=False))
    else:
        md.append("_No proxy summaries computed._")
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append("This probe confirms whether the selected candidate shot can be read at array level by direct HTTP chunk requests.")
    md.append("")
    md.append("If the key arrays load successfully, the next component should construct a first time-resolved diagnostic margin prototype:")
    md.append("")
    md.append("```text")
    md.append("components/")
    md.append("  tokamark_m_edge_t_probe.py")
    md.append("```")
    md.append("")
    md.append("This one-shot probe does not yet establish that the shot is a positive-corridor discharge. It only verifies that the data needed to test that claim can be extracted.")
    path.write_text("\n".join(md), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Probe selected arrays from one public TokaMark/MAST shot.")
    parser.add_argument("--shot-id", type=int, default=12063, help="MAST shot ID to probe.")
    parser.add_argument("--out-dir", default="outputs/reports", help="Output directory.")
    parser.add_argument(
        "--base-url",
        default="https://s3.echo.stfc.ac.uk/mast/tokamark/v1",
        help="Base HTTPS URL for TokaMark Zarr stores.",
    )
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout per request.")
    parser.add_argument("--retries", type=int, default=1, help="Retries per request.")
    parser.add_argument("--delay", type=float, default=0.05, help="Delay between retries.")
    parser.add_argument(
        "--max-chunk-downloads",
        type=int,
        default=5000,
        help="Safety limit per array.",
    )
    parser.add_argument(
        "--skip-preview",
        action="store_true",
        help="Do not write the proxy time-series preview CSV.",
    )

    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    base_store_url = f"{args.base_url.rstrip('/')}/{args.shot_id}.zarr"
    zmetadata_url = f"{base_store_url}/.zmetadata"

    print(f"Fetching metadata: {zmetadata_url}")
    zmetadata = request_json(zmetadata_url, timeout=args.timeout, retries=args.retries, delay=args.delay)
    metadata = normalize_zmetadata(zmetadata)

    loaded: Dict[str, Dict[str, Any]] = {}
    failed: Dict[str, str] = {}
    summary_rows: List[Dict[str, Any]] = []
    read_infos: Dict[str, Any] = {}

    # Read time arrays first, keyed by source.
    source_times: Dict[str, np.ndarray] = {}
    for source, time_path in TIME_ARRAYS.items():
        try:
            if f"{time_path}/.zarray" in metadata:
                arr, info = read_zarr_array_http(
                    base_url=base_store_url,
                    metadata=metadata,
                    array_path=time_path,
                    timeout=args.timeout,
                    retries=args.retries,
                    delay=args.delay,
                    max_chunk_downloads=args.max_chunk_downloads,
                )
                source_times[source] = arr
                read_infos[f"time::{source}"] = info
        except Exception as exc:
            # Time arrays are useful but not fatal.
            read_infos[f"time::{source}"] = {"error": repr(exc)}

    # Read target signal arrays.
    for label, array_path in TARGET_ARRAYS.items():
        print(f"Reading {label}: {array_path}", flush=True)
        try:
            values, info = read_zarr_array_http(
                base_url=base_store_url,
                metadata=metadata,
                array_path=array_path,
                timeout=args.timeout,
                retries=args.retries,
                delay=args.delay,
                max_chunk_downloads=args.max_chunk_downloads,
            )
            source = source_from_path(array_path)
            time_values = source_times.get(source)

            loaded[label] = {
                "array_path": array_path,
                "values": values,
                "time": time_values,
                "read_info": info,
            }
            read_infos[label] = info
            summary_rows.append(summarize_signal(label, array_path, values, time_values, info))

        except Exception as exc:
            failed[label] = repr(exc)
            print(f"  FAILED: {label}: {exc!r}", flush=True)

    proxy_stats = proxy_summary(loaded)

    prefix = f"tokamark_shot_{args.shot_id}_signal_probe"
    csv_path = out_dir / f"{prefix}.csv"
    json_path = out_dir / f"{prefix}.json"
    md_path = out_dir / f"{prefix}.md"
    preview_path = out_dir / f"tokamark_shot_{args.shot_id}_proxy_timeseries_preview.csv"

    pd.DataFrame(summary_rows).to_csv(csv_path, index=False)

    json_payload = {
        "component": "tokamark_one_shot_array_probe.py",
        "shot_id": args.shot_id,
        "base_url": args.base_url,
        "zmetadata_url": zmetadata_url,
        "loaded_labels": list(loaded.keys()),
        "failed_labels": failed,
        "summary_rows": summary_rows,
        "read_infos": read_infos,
        "proxy_summary": proxy_stats,
        "notes": [
            "This probe reads selected arrays only.",
            "Thomson edge proxy assumes the outer edge is represented by the last 20% of profile indices.",
            "This is not final m_edge(t) and does not classify the shot physically.",
        ],
    }
    json_path.write_text(json.dumps(json_payload, indent=2, default=str), encoding="utf-8")

    write_markdown_report(
        md_path,
        shot_id=args.shot_id,
        base_url=args.base_url,
        summary_rows=summary_rows,
        loaded_labels=list(loaded.keys()),
        failed_labels=failed,
        proxy_stats=proxy_stats,
    )

    if not args.skip_preview:
        preview = build_proxy_preview(loaded, max_points=250)
        preview.to_csv(preview_path, index=False)

    print("One-shot array probe complete.")
    print(f"CSV:     {csv_path}")
    print(f"JSON:    {json_path}")
    print(f"Report:  {md_path}")
    if not args.skip_preview:
        print(f"Preview: {preview_path}")
    print(f"Loaded arrays: {len(loaded)}")
    print(f"Failed arrays: {len(failed)}")


if __name__ == "__main__":
    main()
