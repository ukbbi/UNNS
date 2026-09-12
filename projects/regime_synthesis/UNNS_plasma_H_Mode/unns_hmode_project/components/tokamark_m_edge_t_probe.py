#!/usr/bin/env python3
"""
tokamark_m_edge_t_probe.py

UNNS-H Mode Project
TokaMark / MAST first normalized m_edge(t) probe.

Purpose
-------
Build a first time-resolved UNNS-H Mode edge-admissibility margin for one public
TokaMark/MAST shot.

Default target:
    shot_id = 12063

This script follows:
    components/tokamark_one_shot_array_probe.py

It uses the same safe direct-HTTPS Zarr v2 array-reading approach:
    - fetch .zmetadata
    - fetch selected Zarr chunks by HTTPS
    - decode with numcodecs
    - avoid zarr/s3fs entirely

It computes first cautious, normalized versions of:

    S_power_balance(t)
    S_transport(t)
    S_edge_response(t)
    C_edge_capacity(t)
    F_route_fragmentation(t)
    m_edge(t)

Run from project root
---------------------

    python components\\tokamark_m_edge_t_probe.py --shot-id 12063 --out-dir outputs\\reports

Dependencies
------------

    python -m pip install requests numpy pandas numcodecs

Outputs
-------

    outputs/reports/tokamark_shot_12063_m_edge_t_probe.csv
    outputs/reports/tokamark_shot_12063_m_edge_t_probe.json
    outputs/reports/tokamark_shot_12063_m_edge_t_probe.md

Important scientific caution
----------------------------

This is a first normalized structural probe, not a final plasma-physics
classification.

The TokaMark arrays may be normalized/preprocessed rather than raw engineering
units. Therefore this script uses robust feature normalization and does not use
absolute physical thresholds.

The Thomson edge proxy assumes the outer edge corresponds to the last 20 percent
of profile indices. This is a raw first-pass approximation until explicit radial
or flux-coordinate mapping is added.
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
# Zarr target arrays
# ---------------------------------------------------------------------------

TARGET_ARRAYS: Dict[str, str] = {
    "summary_power_nbi": "summary/power_nbi",
    "summary_ip": "summary/ip",
    "interferometer_n_e_line": "interferometer/n_e_line",
    "dalpha_voltage": "spectrometer_visible/filter_spectrometer_dalpha_voltage",
    "soft_x_lower": "soft_x_rays/horizontal_cam_lower",
    "soft_x_upper": "soft_x_rays/horizontal_cam_upper",
    "thomson_t_e": "thomson_scattering/t_e",
    "thomson_n_e": "thomson_scattering/n_e",
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

            try:
                chunk_arr = chunk_arr.reshape(chunks, order=order)
            except Exception:
                out_slices, _ = chunk_slices(idx, shape, chunks)
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
# Signal processing helpers
# ---------------------------------------------------------------------------

def finite_array(values: Any) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    return arr[np.isfinite(arr)]


def robust_unit(values: Any, *, invert: bool = False, center_abs: bool = False) -> np.ndarray:
    """
    Map an array to [0, 1] using robust percentiles.

    invert=True:
        high raw values become low normalized values.

    center_abs=True:
        use absolute deviation around median before scaling.
    """
    arr = np.asarray(values, dtype=float)
    out = np.full(arr.shape, np.nan, dtype=float)
    finite = arr[np.isfinite(arr)]

    if finite.size < 3:
        return out

    if center_abs:
        med = np.nanmedian(finite)
        arr2 = np.abs(arr - med)
        finite2 = arr2[np.isfinite(arr2)]
    else:
        arr2 = arr
        finite2 = finite

    if finite2.size < 3:
        return out

    lo = float(np.nanpercentile(finite2, 5))
    hi = float(np.nanpercentile(finite2, 95))

    if not np.isfinite(lo) or not np.isfinite(hi) or abs(hi - lo) < 1e-12:
        return out

    out = (arr2 - lo) / (hi - lo)
    out = np.clip(out, 0.0, 1.0)

    if invert:
        out = 1.0 - out

    return out


def reduce_channels(values: np.ndarray) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim == 1:
        return arr
    if arr.ndim == 2:
        with np.errstate(all="ignore"):
            return np.nanmedian(arr, axis=0)
    with np.errstate(all="ignore"):
        return np.nanmedian(arr.reshape((-1, arr.shape[-1])), axis=0)


def profile_proxies(values: np.ndarray, edge_fraction: float = 0.20) -> Dict[str, np.ndarray]:
    """
    Crude Thomson profile proxies.

    Assumption:
        first axis = profile/radial index
        second axis = time

    Edge approximation:
        last edge_fraction of profile indices
    """
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 2 or arr.shape[0] < 5:
        return {}

    n_profile = arr.shape[0]
    n_edge = max(1, int(round(n_profile * edge_fraction)))
    n_core = max(1, int(round(n_profile * edge_fraction)))

    core = arr[:n_core, :]
    edge = arr[-n_edge:, :]

    with np.errstate(all="ignore"):
        edge_median = np.nanmedian(edge, axis=0)
        core_median = np.nanmedian(core, axis=0)

    ratio = edge_median / np.where(np.abs(core_median) > 1e-12, core_median, np.nan)

    try:
        with np.errstate(all="ignore"):
            grad = np.nanmedian(np.abs(np.gradient(arr, axis=0)), axis=0)
    except Exception:
        grad = np.full(arr.shape[1], np.nan)

    return {
        "edge_median": edge_median,
        "core_median": core_median,
        "edge_core_ratio": ratio,
        "profile_gradient": grad,
    }


def interp_to_grid(source_time: np.ndarray, source_values: np.ndarray, grid: np.ndarray) -> np.ndarray:
    """
    Linear interpolation to common grid.

    Does not extrapolate beyond finite source time range.
    """
    t = np.asarray(source_time, dtype=float).ravel()
    v = np.asarray(source_values, dtype=float).ravel()

    mask = np.isfinite(t) & np.isfinite(v)
    if mask.sum() < 2:
        return np.full(grid.shape, np.nan)

    t = t[mask]
    v = v[mask]

    order = np.argsort(t)
    t = t[order]
    v = v[order]

    # Remove duplicate time values.
    unique_t, unique_idx = np.unique(t, return_index=True)
    t = unique_t
    v = v[unique_idx]

    if t.size < 2:
        return np.full(grid.shape, np.nan)

    out = np.interp(grid, t, v)
    out[(grid < t.min()) | (grid > t.max())] = np.nan
    return out


def safe_weighted_mean(items: List[Tuple[np.ndarray, float]]) -> np.ndarray:
    """
    Weighted row-wise mean that ignores NaNs and renormalizes weights.
    """
    if not items:
        raise ValueError("No items for weighted mean.")

    shape = items[0][0].shape
    num = np.zeros(shape, dtype=float)
    den = np.zeros(shape, dtype=float)

    for arr, w in items:
        arr = np.asarray(arr, dtype=float)
        mask = np.isfinite(arr)
        num[mask] += arr[mask] * w
        den[mask] += w

    out = np.full(shape, np.nan, dtype=float)
    mask = den > 0
    out[mask] = num[mask] / den[mask]
    return out


def classify_margin(m: float) -> str:
    if not np.isfinite(m):
        return "insufficient_data"
    if m >= 0.20:
        return "positive_boundary_margin"
    if m <= -0.20:
        return "negative_leakage_margin"
    return "boundary_ambiguous_margin"


def contiguous_intervals(time_grid: np.ndarray, mask: np.ndarray, min_duration: float = 0.003) -> List[Dict[str, Any]]:
    """
    Return contiguous true-mask intervals.
    """
    intervals: List[Dict[str, Any]] = []
    t = np.asarray(time_grid, dtype=float)
    m = np.asarray(mask, dtype=bool)

    if t.size == 0 or m.size == 0:
        return intervals

    start_idx: Optional[int] = None

    for i, flag in enumerate(m):
        if flag and start_idx is None:
            start_idx = i
        if (not flag or i == len(m) - 1) and start_idx is not None:
            end_idx = i if flag and i == len(m) - 1 else i - 1
            t0 = float(t[start_idx])
            t1 = float(t[end_idx])
            duration = t1 - t0
            if duration >= min_duration:
                intervals.append({
                    "start_time": t0,
                    "end_time": t1,
                    "duration": duration,
                    "start_index": int(start_idx),
                    "end_index": int(end_idx),
                })
            start_idx = None

    return intervals


def finite_stats(values: Any) -> Dict[str, Any]:
    arr = np.asarray(values, dtype=float)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return {
            "finite_count": 0,
            "total_count": int(arr.size),
            "finite_fraction": 0.0,
            "min": None,
            "median": None,
            "mean": None,
            "max": None,
            "std": None,
        }

    return {
        "finite_count": int(finite.size),
        "total_count": int(arr.size),
        "finite_fraction": float(finite.size / max(arr.size, 1)),
        "min": float(np.nanmin(finite)),
        "median": float(np.nanmedian(finite)),
        "mean": float(np.nanmean(finite)),
        "max": float(np.nanmax(finite)),
        "std": float(np.nanstd(finite)),
    }


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def source_from_path(array_path: str) -> str:
    return array_path.split("/", 1)[0]


def load_selected_arrays(args: argparse.Namespace) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, str], Dict[str, Any]]:
    base_store_url = f"{args.base_url.rstrip('/')}/{args.shot_id}.zarr"
    zmetadata_url = f"{base_store_url}/.zmetadata"

    print(f"Fetching metadata: {zmetadata_url}")
    zmetadata = request_json(zmetadata_url, timeout=args.timeout, retries=args.retries, delay=args.delay)
    metadata = normalize_zmetadata(zmetadata)

    source_times: Dict[str, np.ndarray] = {}
    read_infos: Dict[str, Any] = {}
    failed: Dict[str, str] = {}

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
            failed[f"time::{source}"] = repr(exc)

    loaded: Dict[str, Any] = {}

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
            loaded[label] = {
                "array_path": array_path,
                "values": values,
                "time": source_times.get(source),
                "read_info": info,
            }
            read_infos[label] = info
        except Exception as exc:
            failed[label] = repr(exc)
            print(f"  FAILED: {label}: {exc!r}", flush=True)

    meta = {
        "zmetadata_url": zmetadata_url,
        "base_store_url": base_store_url,
        "metadata_key_count": len(metadata),
    }

    return loaded, read_infos, failed, meta


# ---------------------------------------------------------------------------
# m_edge(t) construction
# ---------------------------------------------------------------------------

def compute_m_edge_t(loaded: Dict[str, Any], dt: float, edge_fraction: float) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Construct first normalized m_edge(t).

    Formula v0.1:

        S_power_balance(t)
          = 0.70 * normalized NBI pressure
          + 0.30 * density deviation pressure

        S_transport(t)
          = 0.40 * Te profile-gradient pressure
          + 0.40 * ne profile-gradient pressure
          + 0.20 * profile asymmetry pressure

        S_edge_response(t)
          = 0.40 * D-alpha suppression/quiescence feature
          + 0.30 * soft-X activity feature
          + 0.30 * Thomson profile sharpening feature

        C_edge_capacity(t)
          = 0.50 * S_edge_response(t)
          + 0.25 * density_support(t)
          + 0.25 * geometry_stability(t)

        F_route_fragmentation(t)
          = 0.45 * S_power_balance(t)
          + 0.45 * S_transport(t)
          + 0.10 * missingness_pressure(t)

        m_edge(t)
          = C_edge_capacity(t) - F_route_fragmentation(t)

    All terms are normalized to [0, 1] where possible.
    """
    # Choose time domain from high-resolution D-alpha or soft-X time arrays.
    candidate_times = []
    for label in ["dalpha_voltage", "soft_x_lower", "soft_x_upper", "summary_power_nbi", "thomson_t_e"]:
        if label in loaded and loaded[label].get("time") is not None:
            t = np.asarray(loaded[label]["time"], dtype=float)
            finite = t[np.isfinite(t)]
            if finite.size >= 2:
                candidate_times.append((finite.min(), finite.max()))

    if not candidate_times:
        raise RuntimeError("No usable time arrays found.")

    t_min = max(x[0] for x in candidate_times)
    t_max = min(x[1] for x in candidate_times)

    if not np.isfinite(t_min) or not np.isfinite(t_max) or t_max <= t_min:
        # fallback to widest range if strict overlap fails
        t_min = min(x[0] for x in candidate_times)
        t_max = max(x[1] for x in candidate_times)

    time_grid = np.arange(t_min, t_max + dt * 0.5, dt)

    raw: Dict[str, np.ndarray] = {}

    def add_interp(name: str, label: str, reducer=None):
        if label not in loaded:
            raw[name] = np.full(time_grid.shape, np.nan)
            return
        time_values = loaded[label].get("time")
        if time_values is None:
            raw[name] = np.full(time_grid.shape, np.nan)
            return
        values = loaded[label]["values"]
        if reducer is not None:
            values = reducer(values)
        raw[name] = interp_to_grid(time_values, values, time_grid)

    add_interp("nbi", "summary_power_nbi")
    add_interp("ip", "summary_ip")
    add_interp("density", "interferometer_n_e_line")
    add_interp("dalpha", "dalpha_voltage", reduce_channels)
    add_interp("softx_lower", "soft_x_lower", reduce_channels)
    add_interp("softx_upper", "soft_x_upper", reduce_channels)

    # Thomson proxies.
    for label, prefix in [("thomson_t_e", "te"), ("thomson_n_e", "ne")]:
        if label in loaded and loaded[label].get("time") is not None:
            p = profile_proxies(loaded[label]["values"], edge_fraction=edge_fraction)
            t = loaded[label]["time"]
            for key, arr in p.items():
                raw[f"{prefix}_{key}"] = interp_to_grid(t, arr, time_grid)
        else:
            for key in ["edge_median", "core_median", "edge_core_ratio", "profile_gradient"]:
                raw[f"{prefix}_{key}"] = np.full(time_grid.shape, np.nan)

    # Equilibrium / geometry.
    geometry_labels = [
        ("q95", "equilibrium_q95"),
        ("elongation", "equilibrium_elongation"),
        ("triangularity_upper", "equilibrium_triangularity_upper"),
        ("triangularity_lower", "equilibrium_triangularity_lower"),
        ("minor_radius", "equilibrium_minor_radius"),
        ("beta_normal", "equilibrium_beta_normal"),
        ("beta_pol", "equilibrium_beta_pol"),
        ("whmd", "equilibrium_whmd"),
    ]

    for name, label in geometry_labels:
        add_interp(name, label)

    # Normalize raw features.
    nbi_pressure = robust_unit(raw["nbi"])
    density_pressure = robust_unit(raw["density"], center_abs=True)
    density_support = robust_unit(raw["density"])

    te_grad_pressure = robust_unit(raw["te_profile_gradient"])
    ne_grad_pressure = robust_unit(raw["ne_profile_gradient"])
    te_ratio_pressure = robust_unit(raw["te_edge_core_ratio"], center_abs=True)
    ne_ratio_pressure = robust_unit(raw["ne_edge_core_ratio"], center_abs=True)

    # D-alpha: for H-mode-like access, D-alpha suppression/quiescence after a turbulent edge response
    # is often useful. In this first normalized probe, lower D-alpha relative to its own distribution
    # increases edge-response capacity.
    dalpha_suppression = robust_unit(raw["dalpha"], invert=True)

    softx_activity = safe_weighted_mean([
        (robust_unit(raw["softx_lower"]), 0.5),
        (robust_unit(raw["softx_upper"]), 0.5),
    ])

    profile_sharpening = safe_weighted_mean([
        (robust_unit(raw["te_profile_gradient"]), 0.5),
        (robust_unit(raw["ne_profile_gradient"]), 0.5),
    ])

    # Geometry stability = inverse robust deviation from each signal's own median.
    geometry_stability_terms = []
    for name, _label in geometry_labels[:5]:
        geometry_stability_terms.append((robust_unit(raw[name], center_abs=True, invert=True), 1.0))
    geometry_stability = safe_weighted_mean(geometry_stability_terms)

    # Missingness pressure: high when key diagnostic evidence is missing at a grid time.
    key_raw = [
        raw["nbi"],
        raw["density"],
        raw["dalpha"],
        raw["softx_lower"],
        raw["softx_upper"],
        raw["te_profile_gradient"],
        raw["ne_profile_gradient"],
        raw["q95"],
        raw["elongation"],
    ]
    valid_counts = np.zeros(time_grid.shape, dtype=float)
    for arr in key_raw:
        valid_counts += np.isfinite(arr).astype(float)
    missingness_pressure = 1.0 - (valid_counts / len(key_raw))

    S_power_balance = safe_weighted_mean([
        (nbi_pressure, 0.70),
        (density_pressure, 0.30),
    ])

    S_transport = safe_weighted_mean([
        (te_grad_pressure, 0.40),
        (ne_grad_pressure, 0.40),
        (te_ratio_pressure, 0.10),
        (ne_ratio_pressure, 0.10),
    ])

    S_edge_response = safe_weighted_mean([
        (dalpha_suppression, 0.40),
        (softx_activity, 0.30),
        (profile_sharpening, 0.30),
    ])

    C_edge_capacity = safe_weighted_mean([
        (S_edge_response, 0.50),
        (density_support, 0.25),
        (geometry_stability, 0.25),
    ])

    F_route_fragmentation = safe_weighted_mean([
        (S_power_balance, 0.45),
        (S_transport, 0.45),
        (missingness_pressure, 0.10),
    ])

    m_edge = C_edge_capacity - F_route_fragmentation

    out = pd.DataFrame({
        "time_s": time_grid,
        "S_power_balance": S_power_balance,
        "S_transport": S_transport,
        "S_edge_response": S_edge_response,
        "density_support": density_support,
        "geometry_stability": geometry_stability,
        "missingness_pressure": missingness_pressure,
        "C_edge_capacity": C_edge_capacity,
        "F_route_fragmentation": F_route_fragmentation,
        "m_edge": m_edge,
        "nbi_proxy": raw["nbi"],
        "density_proxy": raw["density"],
        "dalpha_proxy": raw["dalpha"],
        "softx_lower_proxy": raw["softx_lower"],
        "softx_upper_proxy": raw["softx_upper"],
        "te_edge_median_proxy": raw["te_edge_median"],
        "te_core_median_proxy": raw["te_core_median"],
        "te_profile_gradient_proxy": raw["te_profile_gradient"],
        "ne_edge_median_proxy": raw["ne_edge_median"],
        "ne_core_median_proxy": raw["ne_core_median"],
        "ne_profile_gradient_proxy": raw["ne_profile_gradient"],
        "q95_proxy": raw["q95"],
        "elongation_proxy": raw["elongation"],
        "triangularity_upper_proxy": raw["triangularity_upper"],
        "triangularity_lower_proxy": raw["triangularity_lower"],
        "minor_radius_proxy": raw["minor_radius"],
        "beta_normal_proxy": raw["beta_normal"],
        "beta_pol_proxy": raw["beta_pol"],
        "whmd_proxy": raw["whmd"],
    })

    out["m_edge_state"] = out["m_edge"].apply(classify_margin)

    summary = {
        "time_grid": {
            "dt": dt,
            "count": int(len(time_grid)),
            "time_min": float(np.nanmin(time_grid)),
            "time_max": float(np.nanmax(time_grid)),
        },
        "formula_version": "tokamark_m_edge_t_probe_v0.1_normalized",
        "formula": {
            "S_power_balance": "0.70*nbi_pressure + 0.30*density_deviation_pressure",
            "S_transport": "0.40*Te_gradient + 0.40*ne_gradient + 0.10*Te_edge_core_deviation + 0.10*ne_edge_core_deviation",
            "S_edge_response": "0.40*Dalpha_suppression + 0.30*softX_activity + 0.30*profile_sharpening",
            "C_edge_capacity": "0.50*S_edge_response + 0.25*density_support + 0.25*geometry_stability",
            "F_route_fragmentation": "0.45*S_power_balance + 0.45*S_transport + 0.10*missingness_pressure",
            "m_edge": "C_edge_capacity - F_route_fragmentation",
        },
        "feature_stats": {
            "S_power_balance": finite_stats(S_power_balance),
            "S_transport": finite_stats(S_transport),
            "S_edge_response": finite_stats(S_edge_response),
            "C_edge_capacity": finite_stats(C_edge_capacity),
            "F_route_fragmentation": finite_stats(F_route_fragmentation),
            "m_edge": finite_stats(m_edge),
            "missingness_pressure": finite_stats(missingness_pressure),
        },
        "state_counts": out["m_edge_state"].value_counts(dropna=False).to_dict(),
        "positive_intervals": contiguous_intervals(
            out["time_s"].to_numpy(),
            out["m_edge_state"].eq("positive_boundary_margin").to_numpy(),
        ),
        "negative_intervals": contiguous_intervals(
            out["time_s"].to_numpy(),
            out["m_edge_state"].eq("negative_leakage_margin").to_numpy(),
        ),
        "notes": [
            "First normalized structural probe only.",
            "Uses robust percentile normalization within the shot.",
            "Does not establish physical positive-corridor status by itself.",
            "TokaMark signals may be preprocessed/normalized; absolute-unit thresholds are avoided.",
            "Thomson edge proxy uses last 20 percent of profile indices as raw edge approximation.",
        ],
    }

    return out, summary


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def write_report(path: Path, shot_id: int, result: pd.DataFrame, summary: Dict[str, Any], failed: Dict[str, str], meta: Dict[str, Any]) -> None:
    stats = summary["feature_stats"]
    state_counts = summary["state_counts"]
    pos_intervals = summary["positive_intervals"][:10]
    neg_intervals = summary["negative_intervals"][:10]

    key_stats_rows = []
    for key in ["S_power_balance", "S_transport", "S_edge_response", "C_edge_capacity", "F_route_fragmentation", "m_edge", "missingness_pressure"]:
        row = {"quantity": key}
        row.update(stats.get(key, {}))
        key_stats_rows.append(row)
    stats_df = pd.DataFrame(key_stats_rows)

    # Peak rows
    m = result["m_edge"].to_numpy(dtype=float)
    if np.isfinite(m).any():
        peak_pos_idx = int(np.nanargmax(m))
        peak_neg_idx = int(np.nanargmin(m))
        peak_pos = result.iloc[peak_pos_idx].to_dict()
        peak_neg = result.iloc[peak_neg_idx].to_dict()
    else:
        peak_pos = {}
        peak_neg = {}

    md: List[str] = []
    md.append(f"# TokaMark First m_edge(t) Probe — Shot {shot_id}")
    md.append("")
    md.append("## 1. Purpose")
    md.append("")
    md.append("This report records the first normalized time-resolved UNNS-H Mode edge-admissibility probe for a public MAST/TokaMark shot.")
    md.append("")
    md.append("It computes first versions of:")
    md.append("")
    md.append("```text")
    md.append("S_power_balance(t)")
    md.append("S_transport(t)")
    md.append("S_edge_response(t)")
    md.append("C_edge_capacity(t)")
    md.append("F_route_fragmentation(t)")
    md.append("m_edge(t)")
    md.append("```")
    md.append("")
    md.append("This is a first structural probe, not a final physical validation.")
    md.append("")
    md.append("## 2. Source")
    md.append("")
    md.append(f"- shot_id: `{shot_id}`")
    md.append(f"- source: `{meta.get('base_store_url')}`")
    md.append(f"- metadata: `{meta.get('zmetadata_url')}`")
    md.append("")
    md.append("## 3. Load status")
    md.append("")
    md.append(f"- failed arrays/time arrays: `{len(failed)}`")
    if failed:
        for label, err in failed.items():
            md.append(f"  - `{label}`: `{err}`")
    md.append("")
    md.append("## 4. Time grid")
    md.append("")
    tg = summary["time_grid"]
    md.append("```text")
    md.append(f"dt:       {tg['dt']}")
    md.append(f"count:    {tg['count']}")
    md.append(f"time_min: {tg['time_min']}")
    md.append(f"time_max: {tg['time_max']}")
    md.append("```")
    md.append("")
    md.append("## 5. Formula version")
    md.append("")
    md.append(f"`{summary['formula_version']}`")
    md.append("")
    md.append("```text")
    for k, v in summary["formula"].items():
        md.append(f"{k} = {v}")
    md.append("```")
    md.append("")
    md.append("## 6. Summary statistics")
    md.append("")
    md.append(stats_df.to_markdown(index=False, floatfmt=".6g"))
    md.append("")
    md.append("## 7. Margin-state counts")
    md.append("")
    md.append("```text")
    for k, v in state_counts.items():
        md.append(f"{k}: {v}")
    md.append("```")
    md.append("")
    md.append("## 8. Peak margin points")
    md.append("")
    md.append("### Peak positive m_edge")
    md.append("")
    if peak_pos:
        md.append("```text")
        for k in ["time_s", "m_edge", "C_edge_capacity", "F_route_fragmentation", "S_edge_response", "S_power_balance", "S_transport", "density_support", "geometry_stability", "missingness_pressure", "m_edge_state"]:
            md.append(f"{k}: {peak_pos.get(k)}")
        md.append("```")
    else:
        md.append("_No finite m_edge values._")
    md.append("")
    md.append("### Peak negative m_edge")
    md.append("")
    if peak_neg:
        md.append("```text")
        for k in ["time_s", "m_edge", "C_edge_capacity", "F_route_fragmentation", "S_edge_response", "S_power_balance", "S_transport", "density_support", "geometry_stability", "missingness_pressure", "m_edge_state"]:
            md.append(f"{k}: {peak_neg.get(k)}")
        md.append("```")
    else:
        md.append("_No finite m_edge values._")
    md.append("")
    md.append("## 9. Candidate positive intervals")
    md.append("")
    if pos_intervals:
        md.append(pd.DataFrame(pos_intervals).to_markdown(index=False, floatfmt=".6g"))
    else:
        md.append("_No positive-boundary intervals found under the v0.1 threshold._")
    md.append("")
    md.append("## 10. Candidate negative intervals")
    md.append("")
    if neg_intervals:
        md.append(pd.DataFrame(neg_intervals).to_markdown(index=False, floatfmt=".6g"))
    else:
        md.append("_No negative-leakage intervals found under the v0.1 threshold._")
    md.append("")
    md.append("## 11. Interpretation")
    md.append("")
    md.append("This output is the first computable `m_edge(t)` trace for the public TokaMark candidate shot.")
    md.append("")
    md.append("It should be interpreted as a normalized structural diagnostic, because TokaMark signals may be preprocessed and not in raw physical engineering units.")
    md.append("")
    md.append("A positive interval means that, under this v0.1 normalized formula, edge-capacity proxies exceed route-fragmentation proxies. It does not by itself prove H-mode, L-H transition timing, or positive-corridor status.")
    md.append("")
    md.append("A negative interval means that route-fragmentation proxies exceed edge-capacity proxies under the same exploratory formula.")
    md.append("")
    md.append("## 12. Limitations")
    md.append("")
    md.append("```text")
    md.append("1. Uses robust within-shot normalization, not absolute physical thresholds.")
    md.append("2. Uses a crude Thomson edge approximation: last 20 percent of profile indices.")
    md.append("3. Does not yet use explicit radial or flux-coordinate mapping.")
    md.append("4. Does not identify L-H transition time.")
    md.append("5. Does not compare against negative or ambiguous MAST shots.")
    md.append("6. Does not validate the positive corridor physically.")
    md.append("```")
    md.append("")
    md.append("## 13. Next step")
    md.append("")
    md.append("The next step is to inspect the generated CSV and decide whether the v0.1 margin intervals align with recognizable edge-response structure.")
    md.append("")
    md.append("Then create a validation note:")
    md.append("")
    md.append("```text")
    md.append("docs/")
    md.append("  19_TOKAMARK_M_EDGE_T_PROBE_REPORT.md")
    md.append("```")
    md.append("")
    md.append("Only after that should the formula be revised or extended.")
    path.write_text("\n".join(md), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Compute first normalized m_edge(t) for one public TokaMark/MAST shot.")
    parser.add_argument("--shot-id", type=int, default=12063, help="MAST shot ID.")
    parser.add_argument("--out-dir", default="outputs/reports", help="Output directory.")
    parser.add_argument("--base-url", default="https://s3.echo.stfc.ac.uk/mast/tokamark/v1", help="Base HTTPS URL.")
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout.")
    parser.add_argument("--retries", type=int, default=1, help="Retries per HTTP request.")
    parser.add_argument("--delay", type=float, default=0.05, help="Retry delay.")
    parser.add_argument("--max-chunk-downloads", type=int, default=5000, help="Safety limit per array.")
    parser.add_argument("--dt", type=float, default=0.001, help="Common time-grid spacing in seconds.")
    parser.add_argument("--edge-fraction", type=float, default=0.20, help="Outer profile fraction used as crude edge proxy.")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    loaded, read_infos, failed, meta = load_selected_arrays(args)

    print("Computing normalized m_edge(t)...")
    result, summary = compute_m_edge_t(
        loaded,
        dt=args.dt,
        edge_fraction=args.edge_fraction,
    )

    prefix = f"tokamark_shot_{args.shot_id}_m_edge_t_probe"
    csv_path = out_dir / f"{prefix}.csv"
    json_path = out_dir / f"{prefix}.json"
    md_path = out_dir / f"{prefix}.md"

    result.to_csv(csv_path, index=False)

    json_payload = {
        "component": "tokamark_m_edge_t_probe.py",
        "shot_id": args.shot_id,
        "base_url": args.base_url,
        "meta": meta,
        "failed": failed,
        "loaded_labels": sorted(loaded.keys()),
        "read_infos": read_infos,
        "summary": summary,
    }
    json_path.write_text(json.dumps(json_payload, indent=2, default=str), encoding="utf-8")

    write_report(
        md_path,
        shot_id=args.shot_id,
        result=result,
        summary=summary,
        failed=failed,
        meta=meta,
    )

    print("m_edge(t) probe complete.")
    print(f"CSV:    {csv_path}")
    print(f"JSON:   {json_path}")
    print(f"Report: {md_path}")
    print("State counts:")
    for k, v in summary["state_counts"].items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
