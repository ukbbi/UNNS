#!/usr/bin/env python3
"""
tokamark_metadata_candidate_scanner.py

UNNS-H Mode Project
TokaMark / MAST metadata candidate scanner.

Purpose
-------
Scan public TokaMark MAST shot metadata through plain HTTPS `.zmetadata` requests
and rank candidate shots for a future UNNS-H Mode time-resolved positive-corridor
probe.

This script does NOT download full diagnostic arrays.
It only downloads consolidated Zarr metadata files:

    https://s3.echo.stfc.ac.uk/mast/tokamark/v1/<shot_id>.zarr/.zmetadata

Why metadata first?
-------------------
The direct zarr/s3fs route may hang on some Windows Python environments. Metadata
HTTP probing is fast, safer, and sufficient for identifying which shots contain
the required signal families.

Default input
-------------
    src/tokamark/metadata/TokaMark_temporal_data_splits.csv

But in this project, use the copy you already have if needed:

    TokaMark_temporal_data_splits.csv

Outputs
-------
    outputs/reports/tokamark_positive_corridor_metadata_candidates.csv
    outputs/reports/tokamark_positive_corridor_metadata_candidates.md
    outputs/reports/tokamark_positive_corridor_metadata_candidates_summary.json

Basic run
---------
From project root:

    python components\\tokamark_metadata_candidate_scanner.py ^
      --splits TokaMark_temporal_data_splits.csv ^
      --out-dir outputs\\reports ^
      --max-shots 200

Full scan:

    python components\\tokamark_metadata_candidate_scanner.py ^
      --splits TokaMark_temporal_data_splits.csv ^
      --out-dir outputs\\reports ^
      --max-shots 0

Campaign-specific scan:

    python components\\tokamark_metadata_candidate_scanner.py ^
      --splits TokaMark_temporal_data_splits.csv ^
      --out-dir outputs\\reports ^
      --campaign M9 ^
      --max-shots 0

Split-specific scan:

    python components\\tokamark_metadata_candidate_scanner.py ^
      --splits TokaMark_temporal_data_splits.csv ^
      --out-dir outputs\\reports ^
      --split test ^
      --max-shots 0
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests


# ---------------------------------------------------------------------------
# Signal definitions
# ---------------------------------------------------------------------------

# Minimal signals needed for an event-level / time-resolved edge-admissibility
# prototype without full Thomson profile support.
CORE_REQUIRED = [
    "summary-power_nbi",
    "interferometer-n_e_line",
    "spectrometer_visible-filter_spectrometer_dalpha_voltage",
    "equilibrium-q95",
    "equilibrium-elongation",
    "equilibrium-triangularity_upper",
    "equilibrium-triangularity_lower",
    "equilibrium-minor_radius",
]

# Strongly preferred signals for real m_edge(t) development.
PROFILE_PREFERRED = [
    "thomson_scattering-t_e",
    "thomson_scattering-n_e",
]

EDGE_ACTIVITY_PREFERRED = [
    "soft_x_rays-horizontal_cam_lower",
    "soft_x_rays-horizontal_cam_upper",
]

# Helpful substitutes or supporting signals.
SUPPORTING_SIGNALS = [
    "summary-ip",
    "magnetics-ip",
    "gas_injection-total_injected",
    "equilibrium-whmd",
    "equilibrium-beta_normal",
    "equilibrium-beta_pol",
    "equilibrium-psi",
    "equilibrium-q",
    "pf_active-coil_current",
    "pf_active-solenoid_current",
    "magnetics-b_field_pol_probe_obr_field",
    "magnetics-b_field_tor_probe_omaha_voltage",
    "charge_exchange-t_i",
    "charge_exchange-v_i",
]

ALL_TARGET_SIGNALS = (
    CORE_REQUIRED
    + PROFILE_PREFERRED
    + EDGE_ACTIVITY_PREFERRED
    + SUPPORTING_SIGNALS
)


@dataclass
class ScanConfig:
    base_url: str
    timeout: float
    retries: int
    delay: float


# ---------------------------------------------------------------------------
# Metadata parsing
# ---------------------------------------------------------------------------

def fetch_zmetadata(shot_id: int, cfg: ScanConfig) -> Dict[str, Any]:
    url = f"{cfg.base_url.rstrip('/')}/{shot_id}.zarr/.zmetadata"
    last_error: Optional[Exception] = None

    for attempt in range(cfg.retries + 1):
        try:
            response = requests.get(url, timeout=cfg.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            last_error = exc
            if attempt < cfg.retries:
                time.sleep(cfg.delay)

    raise RuntimeError(f"Could not fetch metadata for shot {shot_id}: {last_error!r}")


def normalize_metadata(zmetadata: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(zmetadata.get("metadata"), dict):
        return zmetadata["metadata"]
    return zmetadata


def signal_to_source_signal(signal_key: str) -> tuple[str, str]:
    source, signal = signal_key.split("-", 1)
    return source, signal


def inspect_signal(metadata: Dict[str, Any], signal_key: str) -> Dict[str, Any]:
    """
    Check a source-signal in consolidated Zarr metadata.

    Looks for common layouts:
      source/signal/.zarray
      source/signal/values/.zarray
      source/signal/time/.zarray
      source/time/.zarray
    """
    source, signal = signal_to_source_signal(signal_key)
    base = f"{source}/{signal}"

    candidate_value_keys = [
        f"{base}/.zarray",
        f"{base}/values/.zarray",
        f"{base}/value/.zarray",
        f"{base}/data/.zarray",
    ]

    candidate_time_keys = [
        f"{base}/time/.zarray",
        f"{base}/times/.zarray",
        f"{source}/time/.zarray",
    ]

    value_key = next((k for k in candidate_value_keys if k in metadata), "")
    time_key = next((k for k in candidate_time_keys if k in metadata), "")

    prefix_matches = [k for k in metadata.keys() if str(k).startswith(base + "/")]
    present = bool(value_key or prefix_matches)

    values_shape = ""
    time_shape = ""

    if value_key:
        try:
            values_shape = str(metadata[value_key].get("shape", ""))
        except Exception:
            values_shape = ""

    if time_key:
        try:
            time_shape = str(metadata[time_key].get("shape", ""))
        except Exception:
            time_shape = ""

    return {
        "signal": signal_key,
        "present": present,
        "values_present": bool(value_key),
        "time_present": bool(time_key),
        "values_shape": values_shape,
        "time_shape": time_shape,
        "value_key": value_key,
        "time_key": time_key,
        "prefix_match_count": len(prefix_matches),
    }


def inspect_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    keys = [str(k) for k in metadata.keys()]
    source_counts: Dict[str, int] = {}
    signal_like: set[str] = set()

    for key in keys:
        parts = key.split("/")
        if parts:
            source_counts[parts[0]] = source_counts.get(parts[0], 0) + 1
        if len(parts) >= 3 and parts[-1] == ".zarray":
            signal_like.add(f"{parts[0]}-{parts[1]}")

    return {
        "metadata_key_count": len(keys),
        "source_count": len(source_counts),
        "sources": ";".join(sorted(source_counts.keys())),
        "signal_like_count": len(signal_like),
        "signal_like_sample": ";".join(sorted(signal_like)[:50]),
    }


def count_present(signal_rows: Iterable[Dict[str, Any]], signals: List[str]) -> int:
    present = {row["signal"]: bool(row["present"]) for row in signal_rows}
    return sum(1 for sig in signals if present.get(sig, False))


def classify_candidate(
    signal_rows: List[Dict[str, Any]],
    metadata_info: Dict[str, Any],
) -> Dict[str, Any]:
    present = {row["signal"]: bool(row["present"]) for row in signal_rows}

    core_count = count_present(signal_rows, CORE_REQUIRED)
    profile_count = count_present(signal_rows, PROFILE_PREFERRED)
    edge_activity_count = count_present(signal_rows, EDGE_ACTIVITY_PREFERRED)
    support_count = count_present(signal_rows, SUPPORTING_SIGNALS)

    has_core = core_count == len(CORE_REQUIRED)
    has_profile = profile_count == len(PROFILE_PREFERRED)
    has_edge_activity = edge_activity_count >= 1
    has_full_edge_activity = edge_activity_count == len(EDGE_ACTIVITY_PREFERRED)

    # Main score intentionally weights complete core + profiles + D-alpha/soft-X.
    score = (
        50.0 * (core_count / max(len(CORE_REQUIRED), 1))
        + 25.0 * (profile_count / max(len(PROFILE_PREFERRED), 1))
        + 15.0 * (edge_activity_count / max(len(EDGE_ACTIVITY_PREFERRED), 1))
        + 10.0 * (support_count / max(len(SUPPORTING_SIGNALS), 1))
    )

    if has_core and has_profile and has_full_edge_activity:
        candidate_class = "FULL_PROFILE_EDGE_CANDIDATE"
    elif has_core and has_profile and has_edge_activity:
        candidate_class = "PROFILE_DALPHA_SOFTX_PARTIAL_CANDIDATE"
    elif has_core and has_profile:
        candidate_class = "PROFILE_DALPHA_CANDIDATE"
    elif has_core:
        candidate_class = "CORE_DALPHA_GEOMETRY_CANDIDATE"
    elif present.get("spectrometer_visible-filter_spectrometer_dalpha_voltage", False):
        candidate_class = "PARTIAL_DALPHA_CANDIDATE"
    else:
        candidate_class = "LOW_PRIORITY"

    return {
        "candidate_score": round(score, 3),
        "candidate_class": candidate_class,
        "core_required_present": core_count,
        "core_required_total": len(CORE_REQUIRED),
        "profile_preferred_present": profile_count,
        "profile_preferred_total": len(PROFILE_PREFERRED),
        "edge_activity_present": edge_activity_count,
        "edge_activity_total": len(EDGE_ACTIVITY_PREFERRED),
        "supporting_present": support_count,
        "supporting_total": len(SUPPORTING_SIGNALS),
        "has_core_required": has_core,
        "has_thomson_profiles": has_profile,
        "has_soft_xray": has_edge_activity,
        "metadata_key_count": metadata_info.get("metadata_key_count"),
        "signal_like_count": metadata_info.get("signal_like_count"),
        "sources": metadata_info.get("sources", ""),
    }


# ---------------------------------------------------------------------------
# Split loading / filtering
# ---------------------------------------------------------------------------

def read_split_rows(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        raise ValueError(f"No rows found in split file: {path}")
    if "shot_id" not in rows[0]:
        raise ValueError(f"Split file has no 'shot_id' column: {path}")
    return rows


def normalize_bool(value: Any) -> bool:
    text = str(value).strip().lower()
    return text in {"true", "1", "yes", "y", "t"}


def filter_split_rows(
    rows: List[Dict[str, Any]],
    campaign: str = "",
    split: str = "",
    max_shots: int = 0,
    start_at: int = 0,
) -> List[Dict[str, Any]]:
    filtered = []

    for row in rows:
        if campaign and str(row.get("campaign", "")).strip() != campaign:
            continue

        if split:
            if split not in row:
                raise ValueError(f"Requested split '{split}' not found. Available columns: {list(row.keys())}")
            if not normalize_bool(row.get(split)):
                continue

        filtered.append(row)

    if start_at > 0:
        filtered = filtered[start_at:]

    if max_shots and max_shots > 0:
        filtered = filtered[:max_shots]

    return filtered


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    preferred = [
        "rank",
        "shot_id",
        "campaign",
        "split_membership",
        "status",
        "candidate_score",
        "candidate_class",
        "core_required_present",
        "core_required_total",
        "profile_preferred_present",
        "profile_preferred_total",
        "edge_activity_present",
        "edge_activity_total",
        "supporting_present",
        "supporting_total",
        "has_core_required",
        "has_thomson_profiles",
        "has_soft_xray",
        "metadata_key_count",
        "signal_like_count",
        "sources",
        "missing_core_required",
        "missing_profile_preferred",
        "missing_edge_activity",
        "error",
    ]

    all_keys = set()
    for row in rows:
        all_keys.update(row.keys())

    fieldnames = [k for k in preferred if k in all_keys] + sorted(k for k in all_keys if k not in preferred)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def write_md(path: Path, rows: List[Dict[str, Any]], summary: Dict[str, Any]) -> None:
    top = rows[:25]

    md = []
    md.append("# TokaMark Positive-Corridor Metadata Candidate Scanner")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("This report ranks public TokaMark/MAST shots by metadata-level suitability for a future UNNS-H Mode positive-corridor time-resolved probe.")
    md.append("")
    md.append("The scanner only inspects `.zmetadata`; it does not download full arrays.")
    md.append("")
    md.append("## Scan summary")
    md.append("")
    md.append(f"- split file: `{summary.get('split_file')}`")
    md.append(f"- scanned shots: `{summary.get('scanned_shots')}`")
    md.append(f"- successful metadata fetches: `{summary.get('successful_fetches')}`")
    md.append(f"- failed metadata fetches: `{summary.get('failed_fetches')}`")
    md.append(f"- campaign filter: `{summary.get('campaign_filter') or 'none'}`")
    md.append(f"- split filter: `{summary.get('split_filter') or 'none'}`")
    md.append(f"- max shots: `{summary.get('max_shots')}`")
    md.append("")
    md.append("## Candidate classes")
    md.append("")
    for klass, count in summary.get("candidate_class_counts", {}).items():
        md.append(f"- `{klass}`: {count}")
    md.append("")
    md.append("## Top candidates")
    md.append("")
    md.append("| rank | shot_id | campaign | score | class | core | profile | soft-X | support |")
    md.append("|---:|---:|---|---:|---|---:|---:|---:|---:|")
    for row in top:
        md.append(
            f"| {row.get('rank')} | {row.get('shot_id')} | {row.get('campaign', '')} | "
            f"{row.get('candidate_score')} | `{row.get('candidate_class')}` | "
            f"{row.get('core_required_present')}/{row.get('core_required_total')} | "
            f"{row.get('profile_preferred_present')}/{row.get('profile_preferred_total')} | "
            f"{row.get('edge_activity_present')}/{row.get('edge_activity_total')} | "
            f"{row.get('supporting_present')}/{row.get('supporting_total')} |"
        )
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append("Preferred targets are `FULL_PROFILE_EDGE_CANDIDATE` or `PROFILE_DALPHA_SOFTX_PARTIAL_CANDIDATE` shots.")
    md.append("")
    md.append("If no full candidate is found, `PROFILE_DALPHA_CANDIDATE` is still useful for a Thomson+D-alpha edge-response probe.")
    md.append("")
    md.append("If only `CORE_DALPHA_GEOMETRY_CANDIDATE` shots are found, the source can support an event-level edge-response probe but not full profile-resolved `m_edge(t)`.")
    md.append("")
    md.append("## Next step")
    md.append("")
    md.append("After identifying a top candidate, build a small HTTP chunk/array reader or a controlled zarr loader for that one shot only.")
    path.write_text("\n".join(md), encoding="utf-8")


def summarize(rows: List[Dict[str, Any]], args: argparse.Namespace, split_file: Path) -> Dict[str, Any]:
    class_counts: Dict[str, int] = {}
    status_counts: Dict[str, int] = {}

    for row in rows:
        class_counts[row.get("candidate_class", "UNKNOWN")] = class_counts.get(row.get("candidate_class", "UNKNOWN"), 0) + 1
        status_counts[row.get("status", "UNKNOWN")] = status_counts.get(row.get("status", "UNKNOWN"), 0) + 1

    return {
        "scanner": "tokamark_metadata_candidate_scanner.py",
        "split_file": str(split_file),
        "base_url": args.base_url,
        "campaign_filter": args.campaign,
        "split_filter": args.split,
        "max_shots": args.max_shots,
        "start_at": args.start_at,
        "scanned_shots": len(rows),
        "successful_fetches": status_counts.get("OK", 0),
        "failed_fetches": sum(v for k, v in status_counts.items() if k != "OK"),
        "status_counts": status_counts,
        "candidate_class_counts": dict(sorted(class_counts.items(), key=lambda item: item[0])),
        "core_required": CORE_REQUIRED,
        "profile_preferred": PROFILE_PREFERRED,
        "edge_activity_preferred": EDGE_ACTIVITY_PREFERRED,
        "supporting_signals": SUPPORTING_SIGNALS,
        "top_10": rows[:10],
    }


# ---------------------------------------------------------------------------
# Main scan
# ---------------------------------------------------------------------------

def scan_one_shot(row: Dict[str, Any], cfg: ScanConfig) -> Dict[str, Any]:
    shot_id = int(float(row["shot_id"]))
    campaign = str(row.get("campaign", ""))

    split_membership = []
    for col in ["train", "val", "test"]:
        if col in row and normalize_bool(row.get(col)):
            split_membership.append(col)

    base_out: Dict[str, Any] = {
        "shot_id": shot_id,
        "campaign": campaign,
        "split_membership": ";".join(split_membership),
        "status": "FAIL",
        "error": "",
    }

    try:
        zmetadata = fetch_zmetadata(shot_id, cfg)
        metadata = normalize_metadata(zmetadata)
        metadata_info = inspect_metadata(metadata)

        signal_rows = [inspect_signal(metadata, sig) for sig in ALL_TARGET_SIGNALS]
        class_info = classify_candidate(signal_rows, metadata_info)

        present = {s["signal"]: bool(s["present"]) for s in signal_rows}
        missing_core = [sig for sig in CORE_REQUIRED if not present.get(sig, False)]
        missing_profile = [sig for sig in PROFILE_PREFERRED if not present.get(sig, False)]
        missing_edge = [sig for sig in EDGE_ACTIVITY_PREFERRED if not present.get(sig, False)]

        out = dict(base_out)
        out.update(class_info)
        out.update({
            "status": "OK",
            "missing_core_required": ";".join(missing_core),
            "missing_profile_preferred": ";".join(missing_profile),
            "missing_edge_activity": ";".join(missing_edge),
        })

        # Add one boolean column per major signal for quick spreadsheet filtering.
        for sig in ALL_TARGET_SIGNALS:
            out[f"has__{sig}"] = present.get(sig, False)

        # Add shape columns for key signals.
        for sigrow in signal_rows:
            sig = sigrow["signal"]
            if sig in CORE_REQUIRED + PROFILE_PREFERRED + EDGE_ACTIVITY_PREFERRED:
                out[f"shape__{sig}"] = sigrow.get("values_shape", "")

        return out

    except Exception as exc:
        out = dict(base_out)
        out.update({
            "candidate_score": 0.0,
            "candidate_class": "FETCH_FAILED",
            "core_required_present": 0,
            "core_required_total": len(CORE_REQUIRED),
            "profile_preferred_present": 0,
            "profile_preferred_total": len(PROFILE_PREFERRED),
            "edge_activity_present": 0,
            "edge_activity_total": len(EDGE_ACTIVITY_PREFERRED),
            "supporting_present": 0,
            "supporting_total": len(SUPPORTING_SIGNALS),
            "has_core_required": False,
            "has_thomson_profiles": False,
            "has_soft_xray": False,
            "metadata_key_count": "",
            "signal_like_count": "",
            "sources": "",
            "missing_core_required": ";".join(CORE_REQUIRED),
            "missing_profile_preferred": ";".join(PROFILE_PREFERRED),
            "missing_edge_activity": ";".join(EDGE_ACTIVITY_PREFERRED),
            "error": repr(exc),
        })
        return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan public TokaMark metadata for UNNS-H Mode candidate shots.")
    parser.add_argument(
        "--splits",
        default="TokaMark_temporal_data_splits.csv",
        help="Path to TokaMark temporal or random data split CSV.",
    )
    parser.add_argument("--out-dir", default="outputs/reports", help="Output directory.")
    parser.add_argument(
        "--base-url",
        default="https://s3.echo.stfc.ac.uk/mast/tokamark/v1",
        help="Base HTTPS URL for public TokaMark Zarr stores.",
    )
    parser.add_argument("--campaign", default="", help="Optional campaign filter, e.g. M8 or M9.")
    parser.add_argument("--split", default="", help="Optional split filter: train, val, or test.")
    parser.add_argument(
        "--max-shots",
        type=int,
        default=200,
        help="Maximum shots to scan. Use 0 for all filtered shots.",
    )
    parser.add_argument(
        "--start-at",
        type=int,
        default=0,
        help="Skip this many filtered rows before scanning. Useful for batch continuation.",
    )
    parser.add_argument("--timeout", type=float, default=12.0, help="HTTP timeout per metadata request.")
    parser.add_argument("--retries", type=int, default=1, help="Retry count per shot after first failure.")
    parser.add_argument("--delay", type=float, default=0.05, help="Delay between retries and between shots.")
    parser.add_argument(
        "--prefix",
        default="tokamark_positive_corridor_metadata_candidates",
        help="Output filename prefix.",
    )

    args = parser.parse_args()

    split_file = Path(args.splits)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = read_split_rows(split_file)
    filtered = filter_split_rows(
        rows,
        campaign=args.campaign,
        split=args.split,
        max_shots=args.max_shots,
        start_at=args.start_at,
    )

    if not filtered:
        raise SystemExit("No shots matched the requested filters.")

    cfg = ScanConfig(
        base_url=args.base_url,
        timeout=args.timeout,
        retries=args.retries,
        delay=args.delay,
    )

    print(f"Scanning {len(filtered)} shots from {split_file}...")
    print(f"Base URL: {args.base_url}")
    if args.campaign:
        print(f"Campaign filter: {args.campaign}")
    if args.split:
        print(f"Split filter: {args.split}")

    out_rows: List[Dict[str, Any]] = []

    for idx, row in enumerate(filtered, start=1):
        shot_id = row.get("shot_id")
        print(f"[{idx}/{len(filtered)}] shot {shot_id}", flush=True)
        out_rows.append(scan_one_shot(row, cfg))
        if args.delay > 0:
            time.sleep(args.delay)

    # Sort best first:
    #  1. score descending
    #  2. profile present
    #  3. soft-X present
    #  4. core present
    #  5. shot_id
    out_rows.sort(
        key=lambda r: (
            float(r.get("candidate_score") or 0.0),
            bool(r.get("has_thomson_profiles")),
            bool(r.get("has_soft_xray")),
            bool(r.get("has_core_required")),
            -int(r.get("shot_id", 0)),
        ),
        reverse=True,
    )

    for rank, row in enumerate(out_rows, start=1):
        row["rank"] = rank

    summary = summarize(out_rows, args, split_file)

    csv_path = out_dir / f"{args.prefix}.csv"
    md_path = out_dir / f"{args.prefix}.md"
    json_path = out_dir / f"{args.prefix}_summary.json"

    write_csv(csv_path, out_rows)
    write_md(md_path, out_rows, summary)
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("Candidate scan complete.")
    print(f"CSV:     {csv_path}")
    print(f"Report:  {md_path}")
    print(f"Summary: {json_path}")

    print("\nTop candidates:")
    for row in out_rows[:10]:
        print(
            f"  rank {row['rank']:>3} | shot {row['shot_id']} | score {row['candidate_score']} | "
            f"{row['candidate_class']} | campaign {row.get('campaign', '')}"
        )


if __name__ == "__main__":
    main()
