#!/usr/bin/env python3
"""
c_line_ladder_to_struc_perc_i.py

STELLAR_BOUNDARY_DYNAMICS_I
Phase C — Spectral line ladder to STRUC-PERC-I converter.

Reads:
  ladders/C1_SN1993J_spectral_line_ladder.csv
  ladders/C2_SN2012aw_spectral_line_ladder.csv

Writes:
  struc_perc_i/canonical_inputs/C1_SN1993J_struc_perc_input.csv
  struc_perc_i/canonical_inputs/C2_SN2012aw_struc_perc_input.csv

  struc_perc_i/numeric_ladders/C1_SN1993J_numeric_ladder.txt
  struc_perc_i/numeric_ladders/C2_SN2012aw_numeric_ladder.txt

  struc_perc_i/summaries/C_STRUC_PERC_I_INPUT_SUMMARY.csv

Usage from C_spectral_time_series/:

  python tools/c_line_ladder_to_struc_perc_i.py --batch ladders struc_perc_i

Single object:

  python tools/c_line_ladder_to_struc_perc_i.py ladders/C1_SN1993J_spectral_line_ladder.csv struc_perc_i/canonical_inputs/C1_SN1993J_struc_perc_input.csv struc_perc_i/numeric_ladders/C1_SN1993J_numeric_ladder.txt

This script builds real Phase C spectral structural ladders from line-window
proxies. It does not infer abundances and does not perform radiative-transfer
modeling.
"""

import argparse
import csv
import math
import statistics
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path


CANONICAL_COLUMNS = [
    "struc_perc_id",
    "source_ladder_id",
    "object_id",
    "object_name",
    "spectrum_index",
    "spectrum_id",
    "spectrum_file",
    "spectrum_date",
    "phase_days",
    "spectral_phase_role",
    "line_id",
    "line_name",
    "element_group",
    "rest_wavelength",
    "n_points_window",
    "continuum_level",
    "line_flux_proxy",
    "line_depth_proxy",
    "equivalent_width_proxy",
    "velocity_proxy_km_s",
    "width_proxy_angstrom",
    "signal_quality_proxy",
    "delta_line_flux",
    "delta_line_depth",
    "delta_equivalent_width",
    "delta_velocity",
    "delta_width",
    "delta_signal_quality",
    "line_transition_flag",
    "element_transition_flag",
    "gap",
    "gap_source",
    "boundary_role",
    "struc_perc_role",
    "alpha_ready",
    "unns_interpretation",
    "raw_reference",
]

SUMMARY_COLUMNS = [
    "input_file",
    "canonical_output",
    "numeric_ladder_output",
    "object_id",
    "object_name",
    "ladder_rows_in",
    "canonical_rows_out",
    "numeric_points_out",
    "unique_spectra",
    "unique_lines",
    "date_min",
    "date_max",
    "gap_min",
    "gap_max",
    "gap_sum",
    "status",
]


FEATURES = [
    "line_flux_proxy",
    "line_depth_proxy",
    "equivalent_width_proxy",
    "velocity_proxy_km_s",
    "width_proxy_angstrom",
    "signal_quality_proxy",
]


def to_float(value, default=0.0):
    try:
        if value is None or str(value).strip() == "":
            return default
        x = float(str(value).strip())
        if math.isnan(x) or math.isinf(x):
            return default
        return x
    except Exception:
        return default


def fmt(value):
    if isinstance(value, float):
        return f"{value:.12g}"
    if value is None:
        return ""
    return str(value)


def read_csv(path):
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, columns):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def parse_date(value):
    text = str(value or "").strip()
    if not text:
        return None

    candidates = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
    ]
    for fmt_str in candidates:
        try:
            return datetime.strptime(text[:19], fmt_str)
        except Exception:
            pass

    # Fallback for ISO-like strings.
    try:
        return datetime.fromisoformat(text.replace("Z", ""))
    except Exception:
        return None


def object_id_from_path(path):
    stem = Path(path).stem
    if stem.endswith("_spectral_line_ladder"):
        return stem.replace("_spectral_line_ladder", "")
    return stem


def sort_key(row):
    dt = parse_date(row.get("spectrum_date"))
    date_key = dt.timestamp() if dt else 0.0
    spectrum_id = row.get("spectrum_id", "")
    line_id = row.get("line_id", "")
    rest = to_float(row.get("rest_wavelength"))
    return (date_key, spectrum_id, rest, line_id)


def robust_scale(values):
    vals = [abs(v) for v in values if math.isfinite(v)]
    if not vals:
        return 1.0
    med = statistics.median(vals)
    if med > 0:
        return med
    mx = max(vals)
    return mx if mx > 0 else 1.0


def compute_scales(rows):
    scales = {}
    for f in FEATURES:
        vals = [to_float(r.get(f)) for r in rows]
        if f == "velocity_proxy_km_s":
            # Velocities can be large; use adjacent-change scale below as well.
            pass
        scales[f] = robust_scale(vals)

    # Adjacent differences are better for gaps.
    deltas = defaultdict(list)
    prev_by_line = {}
    for row in sorted(rows, key=sort_key):
        lid = row.get("line_id", "")
        prev = prev_by_line.get(lid)
        if prev is not None:
            for f in FEATURES:
                deltas[f].append(to_float(row.get(f)) - to_float(prev.get(f)))
        prev_by_line[lid] = row

    for f in FEATURES:
        dscale = robust_scale(deltas[f])
        if dscale > 0:
            scales[f] = dscale

    return scales


def spectral_phase_role_from_order(index, total):
    if total <= 1:
        return "single_spectrum"
    x = index / max(1, total - 1)
    if x <= 0.15:
        return "early_spectral_state"
    if x <= 0.35:
        return "rising_or_near_peak_spectral_state"
    if x <= 0.65:
        return "decline_spectral_state"
    if x <= 0.85:
        return "late_decline_spectral_state"
    return "late_nebular_or_tail_spectral_state"


def boundary_role(row, spectrum_index, total_spectra):
    role = row.get("spectral_phase_role", "") or spectral_phase_role_from_order(spectrum_index, total_spectra)
    if role != "unknown_phase":
        return role
    return spectral_phase_role_from_order(spectrum_index, total_spectra)


def struc_perc_role(boundary, element):
    if "early" in boundary:
        return "early_post_boundary_spectral_state"
    if "peak" in boundary:
        return "peak_response_spectral_state"
    if "decline" in boundary:
        return "relaxation_spectral_state"
    if "nebular" in boundary or "tail" in boundary:
        return "late_element_redistribution_state"
    if element in ("Fe", "NiCo", "Ca"):
        return "heavy_element_spectral_state"
    return "spectral_line_state"


def line_transition(prev, row):
    if prev is None:
        return 0
    return 1 if prev.get("line_id") != row.get("line_id") else 0


def element_transition(prev, row):
    if prev is None:
        return 0
    return 1 if prev.get("element_group") != row.get("element_group") else 0


def compute_gap(prev_same_line, row, scales):
    """
    Date-ordered line-specific spectral gap.

    Uses changes in:
      line_flux_proxy
      line_depth_proxy
      equivalent_width_proxy
      velocity_proxy_km_s
      width_proxy_angstrom
      signal_quality_proxy

    If a line has no previous observation, use a small baseline gap derived from
    current normalized feature magnitude so that the numeric ladder remains
    cumulative and positive.
    """
    if prev_same_line is None:
        components = {
            "line_flux_proxy": abs(to_float(row.get("line_flux_proxy"))) / scales["line_flux_proxy"],
            "line_depth_proxy": abs(to_float(row.get("line_depth_proxy"))) / scales["line_depth_proxy"],
            "equivalent_width_proxy": abs(to_float(row.get("equivalent_width_proxy"))) / scales["equivalent_width_proxy"],
            "velocity_proxy_km_s": abs(to_float(row.get("velocity_proxy_km_s"))) / scales["velocity_proxy_km_s"],
            "width_proxy_angstrom": abs(to_float(row.get("width_proxy_angstrom"))) / scales["width_proxy_angstrom"],
            "signal_quality_proxy": abs(to_float(row.get("signal_quality_proxy"))) / scales["signal_quality_proxy"],
        }
        gap = 0.02 + 0.01 * statistics.fmean(components.values())
        deltas = {k: 0.0 for k in FEATURES}
        return max(gap, 1e-12), deltas

    deltas = {
        "line_flux_proxy": to_float(row.get("line_flux_proxy")) - to_float(prev_same_line.get("line_flux_proxy")),
        "line_depth_proxy": to_float(row.get("line_depth_proxy")) - to_float(prev_same_line.get("line_depth_proxy")),
        "equivalent_width_proxy": to_float(row.get("equivalent_width_proxy")) - to_float(prev_same_line.get("equivalent_width_proxy")),
        "velocity_proxy_km_s": to_float(row.get("velocity_proxy_km_s")) - to_float(prev_same_line.get("velocity_proxy_km_s")),
        "width_proxy_angstrom": to_float(row.get("width_proxy_angstrom")) - to_float(prev_same_line.get("width_proxy_angstrom")),
        "signal_quality_proxy": to_float(row.get("signal_quality_proxy")) - to_float(prev_same_line.get("signal_quality_proxy")),
    }

    gap = (
        0.22 * abs(deltas["line_flux_proxy"]) / scales["line_flux_proxy"] +
        0.18 * abs(deltas["line_depth_proxy"]) / scales["line_depth_proxy"] +
        0.18 * abs(deltas["equivalent_width_proxy"]) / scales["equivalent_width_proxy"] +
        0.18 * abs(deltas["velocity_proxy_km_s"]) / scales["velocity_proxy_km_s"] +
        0.14 * abs(deltas["width_proxy_angstrom"]) / scales["width_proxy_angstrom"] +
        0.10 * abs(deltas["signal_quality_proxy"]) / scales["signal_quality_proxy"]
    )

    return max(gap, 1e-12), deltas


def convert_one(input_csv, canonical_csv, numeric_txt):
    input_csv = Path(input_csv)
    object_id = object_id_from_path(input_csv)
    rows = sorted(read_csv(input_csv), key=sort_key)

    if not rows:
        raise ValueError(f"No ladder rows found in {input_csv}")

    object_name = rows[0].get("object_name", object_id)

    spectrum_order = []
    seen_spectra = set()
    for r in rows:
        sid = r.get("spectrum_id", "")
        if sid not in seen_spectra:
            seen_spectra.add(sid)
            spectrum_order.append(sid)
    spectrum_index_lookup = {sid: i for i, sid in enumerate(spectrum_order)}
    total_spectra = len(spectrum_order)

    scales = compute_scales(rows)

    canonical_rows = []
    prev_by_line = {}
    prev_global = None
    gaps = []

    for idx, row in enumerate(rows, start=1):
        sid = row.get("spectrum_id", "")
        spectrum_index = spectrum_index_lookup.get(sid, 0)
        prev_line = prev_by_line.get(row.get("line_id", ""))

        gap, deltas = compute_gap(prev_line, row, scales)
        gap += 0.03 * line_transition(prev_global, row)
        gap += 0.02 * element_transition(prev_global, row)

        gaps.append(gap)

        boundary = boundary_role(row, spectrum_index, total_spectra)
        role = struc_perc_role(boundary, row.get("element_group", ""))

        canonical_rows.append({
            "struc_perc_id": f"{object_id}_spectral_state_{idx:05d}",
            "source_ladder_id": object_id,
            "object_id": object_id,
            "object_name": object_name,
            "spectrum_index": spectrum_index + 1,
            "spectrum_id": sid,
            "spectrum_file": row.get("spectrum_file", ""),
            "spectrum_date": row.get("spectrum_date", ""),
            "phase_days": row.get("phase_days", ""),
            "spectral_phase_role": boundary,
            "line_id": row.get("line_id", ""),
            "line_name": row.get("line_name", ""),
            "element_group": row.get("element_group", ""),
            "rest_wavelength": row.get("rest_wavelength", ""),
            "n_points_window": row.get("n_points_window", ""),
            "continuum_level": row.get("continuum_level", ""),
            "line_flux_proxy": row.get("line_flux_proxy", ""),
            "line_depth_proxy": row.get("line_depth_proxy", ""),
            "equivalent_width_proxy": row.get("equivalent_width_proxy", ""),
            "velocity_proxy_km_s": row.get("velocity_proxy_km_s", ""),
            "width_proxy_angstrom": row.get("width_proxy_angstrom", ""),
            "signal_quality_proxy": row.get("signal_quality_proxy", ""),
            "delta_line_flux": fmt(deltas["line_flux_proxy"]),
            "delta_line_depth": fmt(deltas["line_depth_proxy"]),
            "delta_equivalent_width": fmt(deltas["equivalent_width_proxy"]),
            "delta_velocity": fmt(deltas["velocity_proxy_km_s"]),
            "delta_width": fmt(deltas["width_proxy_angstrom"]),
            "delta_signal_quality": fmt(deltas["signal_quality_proxy"]),
            "line_transition_flag": line_transition(prev_global, row),
            "element_transition_flag": element_transition(prev_global, row),
            "gap": fmt(gap),
            "gap_source": "date_ordered_line_window_proxy_change",
            "boundary_role": boundary,
            "struc_perc_role": role,
            "alpha_ready": "yes",
            "unns_interpretation": "post-collapse spectral element-line structural state",
            "raw_reference": row.get("raw_reference", ""),
        })

        prev_by_line[row.get("line_id", "")] = row
        prev_global = row

    write_csv(canonical_csv, canonical_rows, CANONICAL_COLUMNS)

    numeric_txt = Path(numeric_txt)
    numeric_txt.parent.mkdir(parents=True, exist_ok=True)
    total = 0.0
    numeric = [0.0]
    for g in gaps:
        total += g
        numeric.append(total)

    with numeric_txt.open("w", encoding="utf-8") as f:
        for value in numeric:
            f.write(f"{value:.12g}\n")

    dates = [r.get("spectrum_date", "") for r in rows if r.get("spectrum_date", "")]
    unique_lines = sorted({r.get("line_id", "") for r in rows if r.get("line_id", "")})

    return {
        "input_file": str(input_csv),
        "canonical_output": str(canonical_csv),
        "numeric_ladder_output": str(numeric_txt),
        "object_id": object_id,
        "object_name": object_name,
        "ladder_rows_in": len(rows),
        "canonical_rows_out": len(canonical_rows),
        "numeric_points_out": len(numeric),
        "unique_spectra": total_spectra,
        "unique_lines": len(unique_lines),
        "date_min": min(dates) if dates else "",
        "date_max": max(dates) if dates else "",
        "gap_min": min(gaps) if gaps else "",
        "gap_max": max(gaps) if gaps else "",
        "gap_sum": sum(gaps) if gaps else "",
        "status": "converted",
    }


def output_names(input_file, struc_dir):
    oid = object_id_from_path(input_file)
    return (
        Path(struc_dir) / "canonical_inputs" / f"{oid}_struc_perc_input.csv",
        Path(struc_dir) / "numeric_ladders" / f"{oid}_numeric_ladder.txt",
    )


def batch_convert(ladders_dir, struc_dir):
    ladders_dir = Path(ladders_dir)
    struc_dir = Path(struc_dir)

    input_files = sorted(ladders_dir.glob("C*_spectral_line_ladder.csv"))
    if not input_files:
        raise FileNotFoundError(f"No C*_spectral_line_ladder.csv files found in {ladders_dir}")

    summaries = []
    for input_file in input_files:
        canonical, numeric = output_names(input_file, struc_dir)
        summary = convert_one(input_file, canonical, numeric)
        summaries.append(summary)

        print(f"Converted: {input_file}")
        print(f"  canonical: {canonical}")
        print(f"  numeric:   {numeric}")
        print(f"  rows: ladder={summary['ladder_rows_in']} canonical={summary['canonical_rows_out']} numeric={summary['numeric_points_out']}")
        print(f"  gap sum: {summary['gap_sum']}")

    summary_path = struc_dir / "summaries" / "C_STRUC_PERC_I_INPUT_SUMMARY.csv"
    write_csv(summary_path, summaries, SUMMARY_COLUMNS)
    print(f"Summary written: {summary_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert Phase C spectral line ladders to STRUC-PERC-I inputs.")
    parser.add_argument("paths", nargs="*", help="Batch: ladders_dir struc_perc_i_dir. Single: input_csv canonical_csv numeric_txt.")
    parser.add_argument("--batch", action="store_true")
    args = parser.parse_args()

    if args.batch:
        if len(args.paths) != 2:
            raise SystemExit("Batch usage: python tools/c_line_ladder_to_struc_perc_i.py --batch ladders struc_perc_i")
        batch_convert(args.paths[0], args.paths[1])
        return

    if len(args.paths) != 3:
        raise SystemExit(__doc__)

    summary = convert_one(args.paths[0], args.paths[1], args.paths[2])
    print(f"Converted: {summary['object_id']}")
    print(f"Canonical output: {summary['canonical_output']}")
    print(f"Numeric output: {summary['numeric_ladder_output']}")


if __name__ == "__main__":
    main()
