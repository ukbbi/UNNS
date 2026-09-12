#!/usr/bin/env python3
"""
a_profile_ladder_to_struc_perc_i.py

Convert real Phase A pre-supernova radial profile ladders into
STRUC-PERC-I canonical inputs and numeric ladders.

Input:
  ladders/A1_12M_presupernova_profile_ladder.csv
  ladders/A2_20M_presupernova_profile_ladder.csv

Output:
  struc_perc_i/canonical_inputs/A1_12M_struc_perc_input.csv
  struc_perc_i/canonical_inputs/A2_20M_struc_perc_input.csv

  struc_perc_i/numeric_ladders/A1_12M_numeric_ladder.txt
  struc_perc_i/numeric_ladders/A2_20M_numeric_ladder.txt

  struc_perc_i/summaries/A_STRUC_PERC_I_INPUT_SUMMARY.csv

This script uses real radial-profile structure. It does not use inlist scaffold
weights.

Usage from A_mesa_precollapse_tracks/:

  python tools/a_profile_ladder_to_struc_perc_i.py --batch ladders struc_perc_i

Single file:

  python tools/a_profile_ladder_to_struc_perc_i.py ladders/A1_12M_presupernova_profile_ladder.csv struc_perc_i/canonical_inputs/A1_12M_struc_perc_input.csv struc_perc_i/numeric_ladders/A1_12M_numeric_ladder.txt
"""

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path


CANONICAL_COLUMNS = [
    "struc_perc_id",
    "source_ladder_id",
    "object_name",
    "target_mass_class",
    "selected_model_mass",
    "progenitor_type",
    "network",
    "stage_index",
    "phase_name",
    "zone_start",
    "zone_end",
    "n_zones",
    "q_start",
    "q_end",
    "q_mid",
    "mass_start",
    "mass_end",
    "radius_start",
    "radius_end",
    "mean_logT",
    "mean_logRho",
    "mean_logP",
    "mean_ye",
    "mean_support_margin_proxy",
    "mean_energy_loss_proxy",
    "dominant_species_mode",
    "composition_stage_mode",
    "boundary_role_mode",
    "struc_perc_role_mode",
    "delta_logT",
    "delta_logRho",
    "delta_ye",
    "delta_support_margin",
    "delta_energy_loss",
    "composition_transition_count",
    "gap",
    "gap_source",
    "alpha_ready",
    "unns_interpretation",
    "raw_reference",
]

SUMMARY_COLUMNS = [
    "input_file",
    "canonical_output",
    "numeric_ladder_output",
    "object_name",
    "target_mass_class",
    "selected_model_mass",
    "profile_rows_in",
    "canonical_rows_out",
    "numeric_points_out",
    "gap_min",
    "gap_max",
    "gap_sum",
    "status",
]


def to_float(value, default=0.0):
    try:
        if value is None or str(value).strip() == "":
            return default
        x = float(value)
        if math.isnan(x) or math.isinf(x):
            return default
        return x
    except Exception:
        return default


def fmt(value):
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.12g}"
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


def safe_mean(values):
    values = [v for v in values if math.isfinite(v)]
    return statistics.fmean(values) if values else 0.0


def mode(values):
    counts = defaultdict(int)
    for v in values:
        if v is not None and str(v).strip() != "":
            counts[str(v)] += 1
    if not counts:
        return ""
    return max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0]


def robust_range(rows, key):
    vals = [to_float(r.get(key)) for r in rows]
    vals = [v for v in vals if math.isfinite(v)]
    if not vals:
        return 1.0
    r = max(vals) - min(vals)
    return r if r > 0 else 1.0


def phase_from_q(q_mid, boundary_mode, comp_mode):
    """
    Radial structural phases from exterior to core.
    q ≈ M_r/M_total in MESA profile coordinates.
    """
    if q_mid >= 0.95:
        return 1, "surface_envelope"
    if q_mid >= 0.75:
        return 2, "outer_envelope"
    if q_mid >= 0.50:
        return 3, "outer_shell"
    if q_mid >= 0.20:
        return 4, "intermediate_shell"
    if q_mid >= 0.05:
        return 5, "inner_shell"
    if q_mid >= 0.01:
        return 6, "core_boundary"
    if q_mid >= 0.001:
        return 7, "inner_core"
    return 8, "central_core"


def chunk_rows_by_radial_quantile(rows, n_bins=64):
    """
    Build compact radial bins from full profile rows. The MESA profile is ordered
    surface → center, so each bin preserves radial order.
    """
    n = len(rows)
    if n == 0:
        return []
    chunks = []
    for i in range(n_bins):
        start = int(round(i * n / n_bins))
        end = int(round((i + 1) * n / n_bins))
        if end <= start:
            continue
        chunks.append(rows[start:end])
    return chunks


def compute_gap(chunk, scales):
    """
    Real-profile structural gap based on local radial variation.

    Uses weighted normalized changes in:
      logT
      logRho
      Ye
      support_margin_proxy
      energy_loss_proxy
      composition transition count

    The output is positive and cumulative-ready for STRUC-PERC-I.
    """
    first = chunk[0]
    last = chunk[-1]

    d_logT = abs(to_float(last.get("logT")) - to_float(first.get("logT")))
    d_logRho = abs(to_float(last.get("logRho")) - to_float(first.get("logRho")))
    d_ye = abs(to_float(last.get("ye")) - to_float(first.get("ye")))
    d_support = abs(to_float(last.get("support_margin_proxy")) - to_float(first.get("support_margin_proxy")))
    d_loss = abs(to_float(last.get("energy_loss_proxy")) - to_float(first.get("energy_loss_proxy")))

    comps = [r.get("composition_stage", "") for r in chunk]
    transitions = sum(1 for a, b in zip(comps, comps[1:]) if a != b)

    norm_logT = d_logT / scales["logT"]
    norm_logRho = d_logRho / scales["logRho"]
    norm_ye = d_ye / scales["ye"]
    norm_support = d_support / scales["support_margin_proxy"]
    norm_loss = d_loss / scales["energy_loss_proxy"]
    norm_comp = transitions / max(1, len(chunk) - 1)

    gap = (
        0.25 * norm_logT +
        0.25 * norm_logRho +
        0.15 * norm_ye +
        0.15 * norm_support +
        0.10 * norm_loss +
        0.10 * norm_comp
    )

    return max(gap, 1e-12), {
        "delta_logT": d_logT,
        "delta_logRho": d_logRho,
        "delta_ye": d_ye,
        "delta_support_margin": d_support,
        "delta_energy_loss": d_loss,
        "composition_transition_count": transitions,
    }


def convert_one(input_csv, canonical_csv, numeric_txt, n_bins=64):
    input_csv = Path(input_csv)
    canonical_csv = Path(canonical_csv)
    numeric_txt = Path(numeric_txt)

    rows = read_csv(input_csv)
    if not rows:
        raise ValueError(f"No rows found in {input_csv}")

    object_name = rows[0].get("object_name", "")
    target_mass = rows[0].get("target_mass_class", "")
    selected_mass = rows[0].get("selected_model_mass", "")
    progenitor_type = rows[0].get("progenitor_type", "")
    network = rows[0].get("network", "")
    ladder_id = rows[0].get("ladder_id", input_csv.stem)

    scales = {
        "logT": robust_range(rows, "logT"),
        "logRho": robust_range(rows, "logRho"),
        "ye": robust_range(rows, "ye"),
        "support_margin_proxy": robust_range(rows, "support_margin_proxy"),
        "energy_loss_proxy": robust_range(rows, "energy_loss_proxy"),
    }

    chunks = chunk_rows_by_radial_quantile(rows, n_bins=n_bins)
    canonical_rows = []
    gaps = []

    for idx, chunk in enumerate(chunks, start=1):
        q_vals = [to_float(r.get("q")) for r in chunk]
        q_mid = safe_mean(q_vals)
        boundary_mode = mode([r.get("boundary_role") for r in chunk])
        comp_mode = mode([r.get("composition_stage") for r in chunk])
        stage_index, phase_name = phase_from_q(q_mid, boundary_mode, comp_mode)

        gap, deltas = compute_gap(chunk, scales)
        gaps.append(gap)

        first = chunk[0]
        last = chunk[-1]
        sid = f"{ladder_id}_radial_bin_{idx:03d}"

        canonical_rows.append({
            "struc_perc_id": sid,
            "source_ladder_id": ladder_id,
            "object_name": object_name,
            "target_mass_class": target_mass,
            "selected_model_mass": selected_mass,
            "progenitor_type": progenitor_type,
            "network": network,
            "stage_index": stage_index,
            "phase_name": phase_name,
            "zone_start": first.get("zone_index", ""),
            "zone_end": last.get("zone_index", ""),
            "n_zones": len(chunk),
            "q_start": first.get("q", ""),
            "q_end": last.get("q", ""),
            "q_mid": fmt(q_mid),
            "mass_start": first.get("mass_coordinate", ""),
            "mass_end": last.get("mass_coordinate", ""),
            "radius_start": first.get("radius", ""),
            "radius_end": last.get("radius", ""),
            "mean_logT": fmt(safe_mean([to_float(r.get("logT")) for r in chunk])),
            "mean_logRho": fmt(safe_mean([to_float(r.get("logRho")) for r in chunk])),
            "mean_logP": fmt(safe_mean([to_float(r.get("logP")) for r in chunk])),
            "mean_ye": fmt(safe_mean([to_float(r.get("ye")) for r in chunk])),
            "mean_support_margin_proxy": fmt(safe_mean([to_float(r.get("support_margin_proxy")) for r in chunk])),
            "mean_energy_loss_proxy": fmt(safe_mean([to_float(r.get("energy_loss_proxy")) for r in chunk])),
            "dominant_species_mode": mode([r.get("dominant_species") for r in chunk]),
            "composition_stage_mode": comp_mode,
            "boundary_role_mode": boundary_mode,
            "struc_perc_role_mode": mode([r.get("struc_perc_role") for r in chunk]),
            "delta_logT": fmt(deltas["delta_logT"]),
            "delta_logRho": fmt(deltas["delta_logRho"]),
            "delta_ye": fmt(deltas["delta_ye"]),
            "delta_support_margin": fmt(deltas["delta_support_margin"]),
            "delta_energy_loss": fmt(deltas["delta_energy_loss"]),
            "composition_transition_count": deltas["composition_transition_count"],
            "gap": fmt(gap),
            "gap_source": "weighted_radial_profile_change_logT_logRho_ye_support_loss_composition",
            "alpha_ready": "yes" if len(chunk) >= 2 else "partial",
            "unns_interpretation": "compact radial pre-supernova structural state derived from real profile ladder",
            "raw_reference": f"{input_csv.name}::{first.get('raw_reference', '')}--{last.get('raw_reference', '')}",
        })

    write_csv(canonical_csv, canonical_rows, CANONICAL_COLUMNS)

    # Numeric ladder for STRUC-PERC-I: cumulative positive radial gaps.
    numeric_txt.parent.mkdir(parents=True, exist_ok=True)
    total = 0.0
    numeric = [0.0]
    for g in gaps:
        total += g
        numeric.append(total)

    with numeric_txt.open("w", encoding="utf-8") as f:
        for x in numeric:
            f.write(f"{x:.12g}\n")

    return {
        "input_file": str(input_csv),
        "canonical_output": str(canonical_csv),
        "numeric_ladder_output": str(numeric_txt),
        "object_name": object_name,
        "target_mass_class": target_mass,
        "selected_model_mass": selected_mass,
        "profile_rows_in": len(rows),
        "canonical_rows_out": len(canonical_rows),
        "numeric_points_out": len(numeric),
        "gap_min": min(gaps) if gaps else "",
        "gap_max": max(gaps) if gaps else "",
        "gap_sum": sum(gaps) if gaps else "",
        "status": "converted",
    }


def output_names_for(input_file, struc_dir):
    name = Path(input_file).name
    if "A1_12M" in name:
        stem = "A1_12M"
    elif "A2_20M" in name:
        stem = "A2_20M"
    else:
        stem = Path(input_file).stem.replace("_presupernova_profile_ladder", "")

    canonical = Path(struc_dir) / "canonical_inputs" / f"{stem}_struc_perc_input.csv"
    numeric = Path(struc_dir) / "numeric_ladders" / f"{stem}_numeric_ladder.txt"
    return canonical, numeric


def batch_convert(ladders_dir, struc_dir, n_bins=64):
    ladders_dir = Path(ladders_dir)
    struc_dir = Path(struc_dir)

    input_files = sorted(ladders_dir.glob("A*_presupernova_profile_ladder.csv"))
    if not input_files:
        raise FileNotFoundError(f"No A*_presupernova_profile_ladder.csv files found in {ladders_dir}")

    summaries = []
    for input_file in input_files:
        canonical, numeric = output_names_for(input_file, struc_dir)
        summary = convert_one(input_file, canonical, numeric, n_bins=n_bins)
        summaries.append(summary)
        print(f"Converted: {input_file}")
        print(f"  canonical: {canonical}")
        print(f"  numeric:   {numeric}")
        print(f"  rows: profile={summary['profile_rows_in']} compact={summary['canonical_rows_out']} numeric={summary['numeric_points_out']}")

    summary_path = struc_dir / "summaries" / "A_STRUC_PERC_I_INPUT_SUMMARY.csv"
    write_csv(summary_path, summaries, SUMMARY_COLUMNS)
    print(f"Summary written: {summary_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert Phase A profile ladders to STRUC-PERC-I inputs.")
    parser.add_argument("paths", nargs="*", help="Batch: ladders_dir struc_perc_i_dir. Single: input_csv canonical_csv numeric_txt.")
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--bins", type=int, default=64, help="Number of compact radial bins for canonical input.")
    args = parser.parse_args()

    if args.batch:
        if len(args.paths) != 2:
            raise SystemExit("Batch usage: python tools/a_profile_ladder_to_struc_perc_i.py --batch ladders struc_perc_i")
        batch_convert(args.paths[0], args.paths[1], n_bins=args.bins)
        return

    if len(args.paths) != 3:
        raise SystemExit(__doc__)

    summary = convert_one(args.paths[0], args.paths[1], args.paths[2], n_bins=args.bins)
    print(f"Object: {summary['object_name']}")
    print(f"Canonical rows: {summary['canonical_rows_out']}")
    print(f"Numeric points: {summary['numeric_points_out']}")
    print(f"Canonical output: {summary['canonical_output']}")
    print(f"Numeric output: {summary['numeric_ladder_output']}")


if __name__ == "__main__":
    main()
