#!/usr/bin/env python3
"""
tokamark_http_metadata_smoke_test.py

UNNS-H Mode Project
TokaMark public HTTP metadata smoke test.

Purpose
-------
Avoid Windows/s3fs/zarr hangs by testing the public TokaMark Zarr store through
plain HTTPS metadata requests only.

This script does NOT download full arrays.
It only tries to fetch:

    https://s3.echo.stfc.ac.uk/mast/tokamark/v1/<shot_id>.zarr/.zmetadata

and uses that consolidated metadata to check whether required UNNS-H Mode signals
appear in the shot store.

Why this exists
---------------
The s3fs/zarr route can hang or leave aiohttp tasks pending on some Windows Python
installations. A direct HTTP metadata check is much safer as a first public-source
test.

Run from project root:

    python components\\tokamark_http_metadata_smoke_test.py --shot-id 30471 --out-dir outputs\\reports

Install dependency if needed:

    python -m pip install requests

Outputs:

    outputs/reports/tokamark_http_metadata_smoke_test_30471.json
    outputs/reports/tokamark_http_metadata_smoke_test_30471.csv
    outputs/reports/tokamark_http_metadata_smoke_test_30471.md
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests


REQUIRED_SIGNALS = [
    "summary-power_nbi",
    "summary-ip",
    "pulse_schedule-i_plasma",
    "pulse_schedule-n_e_line",
    "interferometer-n_e_line",
    "spectrometer_visible-filter_spectrometer_dalpha_voltage",
    "thomson_scattering-t_e",
    "thomson_scattering-n_e",
    "soft_x_rays-horizontal_cam_lower",
    "soft_x_rays-horizontal_cam_upper",
    "equilibrium-q95",
    "equilibrium-elongation",
    "equilibrium-triangularity_upper",
    "equilibrium-triangularity_lower",
    "equilibrium-minor_radius",
]


def source_signal_to_path(signal_key: str) -> Tuple[str, str]:
    source, signal = signal_key.split("-", 1)
    return source, signal


def fetch_json(url: str, timeout: float) -> Dict[str, Any]:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()


def normalize_metadata(zmetadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return the metadata dict from a consolidated Zarr metadata object.

    Handles both:
      { "metadata": {...} }
    and direct metadata-like dicts.
    """
    if "metadata" in zmetadata and isinstance(zmetadata["metadata"], dict):
        return zmetadata["metadata"]
    return zmetadata


def find_signal_metadata(metadata: Dict[str, Any], signal_key: str) -> Dict[str, Any]:
    """
    Check a source-signal path in consolidated Zarr metadata.

    Zarr layouts vary, so this checks common keys:
      source/signal/.zarray
      source/signal/values/.zarray
      source/signal/time/.zarray
      source/signal
      source/signal/values
      source/signal/time
    """
    source, signal = source_signal_to_path(signal_key)
    base = f"{source}/{signal}"

    candidate_value_keys = [
        f"{base}/values/.zarray",
        f"{base}/.zarray",
        f"{base}/data/.zarray",
        f"{base}/value/.zarray",
    ]

    candidate_time_keys = [
        f"{base}/time/.zarray",
        f"{base}/times/.zarray",
        f"{source}/time/.zarray",
    ]

    candidate_group_keys = [
        f"{base}/.zgroup",
        base,
    ]

    values_key = next((k for k in candidate_value_keys if k in metadata), "")
    time_key = next((k for k in candidate_time_keys if k in metadata), "")
    group_key = next((k for k in candidate_group_keys if k in metadata), "")

    present = bool(values_key or group_key)

    values_shape = ""
    time_shape = ""

    if values_key:
        try:
            values_shape = str(metadata[values_key].get("shape", ""))
        except Exception:
            values_shape = ""

    if time_key:
        try:
            time_shape = str(metadata[time_key].get("shape", ""))
        except Exception:
            time_shape = ""

    # Wider fallback: any metadata key beginning with source/signal/
    prefix_matches = [k for k in metadata.keys() if str(k).startswith(base + "/")]
    if not present and prefix_matches:
        present = True
        group_key = prefix_matches[0]

    return {
        "signal": signal_key,
        "present": present,
        "values_present": bool(values_key),
        "time_present": bool(time_key),
        "values_shape": values_shape,
        "time_shape": time_shape,
        "values_key": values_key,
        "time_key": time_key,
        "group_key_or_first_match": group_key,
        "prefix_match_count": len(prefix_matches),
    }


def inspect_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    keys = [str(k) for k in metadata.keys()]
    source_counts: Dict[str, int] = {}
    for k in keys:
        if "/" in k:
            source = k.split("/", 1)[0]
            source_counts[source] = source_counts.get(source, 0) + 1

    signal_like = []
    for k in keys:
        parts = k.split("/")
        if len(parts) >= 3 and parts[-1] == ".zarray":
            signal_like.append("/".join(parts[:2]).replace("/", "-"))

    return {
        "metadata_key_count": len(keys),
        "source_counts": dict(sorted(source_counts.items())),
        "signal_like_count": len(set(signal_like)),
        "signal_like_sample": sorted(set(signal_like))[:80],
    }


def write_outputs(out_dir: Path, shot_id: int, result: Dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / f"tokamark_http_metadata_smoke_test_{shot_id}.json"
    csv_path = out_dir / f"tokamark_http_metadata_smoke_test_{shot_id}.csv"
    md_path = out_dir / f"tokamark_http_metadata_smoke_test_{shot_id}.md"

    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    rows = result.get("required_signal_check", [])
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        fields = [
            "signal",
            "present",
            "values_present",
            "time_present",
            "values_shape",
            "time_shape",
            "values_key",
            "time_key",
            "group_key_or_first_match",
            "prefix_match_count",
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})

    present = sum(1 for r in rows if r.get("present"))
    values = sum(1 for r in rows if r.get("values_present"))
    times = sum(1 for r in rows if r.get("time_present"))

    md = []
    md.append(f"# TokaMark HTTP Metadata Smoke Test — Shot {shot_id}")
    md.append("")
    md.append(f"Status: `{result.get('status')}`")
    md.append("")
    md.append("## Metadata URL")
    md.append("")
    md.append(f"`{result.get('zmetadata_url')}`")
    md.append("")
    md.append("## Required signal availability")
    md.append("")
    md.append(f"- signals present: `{present}/{len(rows)}`")
    md.append(f"- signals with values metadata: `{values}/{len(rows)}`")
    md.append(f"- signals with time metadata: `{times}/{len(rows)}`")
    md.append("")
    md.append("| signal | present | values | time | values_shape | time_shape |")
    md.append("|---|---:|---:|---:|---|---|")
    for r in rows:
        md.append(
            f"| `{r.get('signal')}` | {r.get('present')} | {r.get('values_present')} | "
            f"{r.get('time_present')} | `{r.get('values_shape')}` | `{r.get('time_shape')}` |"
        )
    md.append("")
    md.append("## Interpretation")
    md.append("")
    if result.get("status") == "FULL_PASS":
        md.append("The public metadata is reachable and all required UNNS-H Mode candidate signals are present in metadata.")
    elif result.get("status") == "PASS":
        md.append("The public metadata is reachable, but some required candidate signals are absent in this shot.")
    else:
        md.append("The public metadata request failed. Inspect the JSON error field.")
    md_path.write_text("\n".join(md), encoding="utf-8")

    print("HTTP metadata smoke-test outputs:")
    print(f"  {json_path}")
    print(f"  {csv_path}")
    print(f"  {md_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="HTTP metadata smoke test for TokaMark public Zarr shot store.")
    parser.add_argument("--shot-id", type=int, default=30471, help="MAST shot ID.")
    parser.add_argument("--out-dir", default="outputs/reports", help="Output directory.")
    parser.add_argument("--base-url", default="https://s3.echo.stfc.ac.uk/mast/tokamark/v1", help="Base HTTPS URL.")
    parser.add_argument("--timeout", type=float, default=20.0, help="HTTP timeout in seconds.")
    args = parser.parse_args()

    zmetadata_url = f"{args.base_url.rstrip('/')}/{args.shot_id}.zarr/.zmetadata"

    result: Dict[str, Any] = {
        "shot_id": args.shot_id,
        "base_url": args.base_url,
        "zmetadata_url": zmetadata_url,
        "timeout": args.timeout,
        "status": "FAIL",
        "error": "",
        "metadata_inspection": {},
        "required_signals": REQUIRED_SIGNALS,
        "required_signal_check": [],
    }

    try:
        zmetadata = fetch_json(zmetadata_url, timeout=args.timeout)
        metadata = normalize_metadata(zmetadata)
        result["metadata_inspection"] = inspect_metadata(metadata)
        rows = [find_signal_metadata(metadata, sig) for sig in REQUIRED_SIGNALS]
        result["required_signal_check"] = rows
        result["status"] = "FULL_PASS" if all(r["present"] for r in rows) else "PASS"
    except Exception as e:
        result["error"] = repr(e)

    write_outputs(Path(args.out_dir), args.shot_id, result)

    print(f"Status: {result['status']}")
    if result["error"]:
        print(f"Error: {result['error']}")
    else:
        rows = result["required_signal_check"]
        print(f"Signals present: {sum(1 for r in rows if r.get('present'))}/{len(rows)}")


if __name__ == "__main__":
    main()
