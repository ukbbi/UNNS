#!/usr/bin/env python3
"""
a_alpha_apply.py

Phase A alpha-application / deformation-grid constructor for
STELLAR_BOUNDARY_DYNAMICS_I.

Reads compact Phase A STRUC-PERC-I canonical input CSV files and writes:

  alpha_application/grids/<OBJECT>_alpha_grid.csv
  alpha_application/vectors/<OBJECT>_5d_vector.csv
  alpha_application/summaries/A_ALPHA_APPLICATION_SUMMARY.csv
  alpha_application/summaries/A_5D_VECTOR_SUMMARY.csv

Input layer:
  struc_perc_i/canonical_inputs/A1_12M_struc_perc_input.csv
  struc_perc_i/canonical_inputs/A2_20M_struc_perc_input.csv

This script operates on real pre-supernova radial-profile canonical inputs,
not on MESA inlist scaffolds.

Usage from A_mesa_precollapse_tracks/:

  python tools/a_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application

Optional alpha grid:

  python tools/a_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application --alpha-min 0.5 --alpha-max 1.5 --alpha-points 21

Single object:

  python tools/a_alpha_apply.py struc_perc_i/canonical_inputs/A1_12M_struc_perc_input.csv alpha_application/grids/A1_12M_alpha_grid.csv alpha_application/vectors/A1_12M_5d_vector.csv
"""

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path


GRID_COLUMNS = [
    "object_id",
    "object_name",
    "target_mass_class",
    "selected_model_mass",
    "progenitor_type",
    "network",
    "phase_name",
    "stage_index",
    "alpha",
    "alpha_radius",
    "gap_base",
    "delta_logT_base",
    "delta_logRho_base",
    "delta_ye_base",
    "delta_support_base",
    "delta_energy_loss_base",
    "composition_transition_count",
    "gap_alpha",
    "delta_logT_alpha",
    "delta_logRho_alpha",
    "delta_ye_alpha",
    "delta_support_alpha",
    "delta_energy_loss_alpha",
    "gap_response_norm",
    "thermal_response_norm",
    "density_response_norm",
    "composition_response_norm",
    "support_response_norm",
    "loss_response_norm",
    "structural_response",
    "phase_persistence_score",
    "boundary_role_mode",
    "composition_stage_mode",
    "dominant_species_mode",
    "alpha_status",
    "instability_flag",
]

VECTOR_COLUMNS = [
    "object_id",
    "object_name",
    "target_mass_class",
    "selected_model_mass",
    "progenitor_type",
    "network",
    "mean_GR",
    "var_GR",
    "anisotropic_persistence",
    "admissibility_persistence",
    "collapse_onset_radius",
    "collapse_observed",
    "kappa_connect_reference",
    "tail_dominance_reference",
    "n_grid_rows",
    "n_valid_rows",
    "n_instability_rows",
    "notes",
]

ALPHA_SUMMARY_COLUMNS = [
    "object_id",
    "object_name",
    "input_file",
    "grid_file",
    "vector_file",
    "canonical_rows",
    "grid_rows",
    "alpha_min",
    "alpha_max",
    "alpha_points",
    "valid_fraction",
    "collapse_observed",
    "collapse_onset_radius",
    "status",
]

REFERENCE_RESULTS = {
    "A1_12M": {"kappa_connect": 2.0, "tail_dominance": 0.0},
    "A2_20M": {"kappa_connect": 1.0, "tail_dominance": 0.0},
}


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
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def safe_mean(values):
    values = [v for v in values if math.isfinite(v)]
    return statistics.fmean(values) if values else 0.0


def safe_variance(values):
    values = [v for v in values if math.isfinite(v)]
    return statistics.pvariance(values) if len(values) >= 2 else 0.0


def robust_scale(values):
    values = sorted(abs(v) for v in values if math.isfinite(v))
    if not values:
        return 1.0
    med = statistics.median(values)
    if med > 0:
        return med
    mx = max(values)
    return mx if mx > 0 else 1.0


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


def object_id_from_path(path):
    stem = Path(path).stem
    if stem.endswith("_struc_perc_input"):
        return stem.replace("_struc_perc_input", "")
    return stem


def make_alpha_values(alpha_min, alpha_max, alpha_points):
    if alpha_points <= 1:
        return [1.0]
    step = (alpha_max - alpha_min) / (alpha_points - 1)
    return [alpha_min + i * step for i in range(alpha_points)]


def normalized_response(base, alpha_value, scale):
    return abs(base * (alpha_value - 1.0)) / scale if scale > 0 else 0.0


def phase_persistence_score(structural_response):
    return 1.0 / (1.0 + structural_response)


def instability_from_response(structural_response, phase_persistence, alpha_radius):
    """
    First-pass Phase A instability rule.

    Because Phase A is a radial pre-supernova profile rather than a light curve,
    this threshold is intentionally conservative. It marks instability only
    when deformation produces a high normalized structural response and low
    persistence.
    """
    if structural_response >= 2.0 and phase_persistence <= 0.333:
        return "yes"
    if alpha_radius >= 0.45 and structural_response >= 1.5 and phase_persistence <= 0.4:
        return "yes"
    return "no"


def phase_sort_key(row):
    return (
        int(to_float(row.get("stage_index"), 999)),
        to_float(row.get("q_mid"), 0.0),
        row.get("phase_name", ""),
    )


def build_grid_rows(rows, object_id, alphas):
    if not rows:
        raise ValueError("No canonical rows supplied")

    first = rows[0]
    object_name = first.get("object_name", object_id)
    target_mass = first.get("target_mass_class", "")
    selected_mass = first.get("selected_model_mass", "")
    progenitor_type = first.get("progenitor_type", "")
    network = first.get("network", "")

    gap_vals = [to_float(r.get("gap")) for r in rows]
    logT_vals = [to_float(r.get("delta_logT")) for r in rows]
    logRho_vals = [to_float(r.get("delta_logRho")) for r in rows]
    ye_vals = [to_float(r.get("delta_ye")) for r in rows]
    support_vals = [to_float(r.get("delta_support_margin")) for r in rows]
    loss_vals = [to_float(r.get("delta_energy_loss")) for r in rows]

    scales = {
        "gap": robust_scale(gap_vals),
        "logT": robust_scale(logT_vals),
        "logRho": robust_scale(logRho_vals),
        "ye": robust_scale(ye_vals),
        "support": robust_scale(support_vals),
        "loss": robust_scale(loss_vals),
    }

    grid_rows = []

    for row in sorted(rows, key=phase_sort_key):
        gap_base = abs(to_float(row.get("gap")))
        d_logT = abs(to_float(row.get("delta_logT")))
        d_logRho = abs(to_float(row.get("delta_logRho")))
        d_ye = abs(to_float(row.get("delta_ye")))
        d_support = abs(to_float(row.get("delta_support_margin")))
        d_loss = abs(to_float(row.get("delta_energy_loss")))
        comp_count = to_float(row.get("composition_transition_count"))

        for alpha in alphas:
            alpha_radius = abs(alpha - 1.0)

            gap_alpha = gap_base * alpha
            logT_alpha = d_logT * alpha
            logRho_alpha = d_logRho * alpha
            ye_alpha = d_ye * alpha
            support_alpha = d_support * alpha
            loss_alpha = d_loss * alpha

            gap_r = normalized_response(gap_base, alpha, scales["gap"])
            thermal_r = normalized_response(d_logT, alpha, scales["logT"])
            density_r = normalized_response(d_logRho, alpha, scales["logRho"])
            composition_r = normalized_response(d_ye, alpha, scales["ye"])
            support_r = normalized_response(d_support, alpha, scales["support"])
            loss_r = normalized_response(d_loss, alpha, scales["loss"])

            structural_response = (
                0.25 * gap_r +
                0.20 * thermal_r +
                0.20 * density_r +
                0.15 * composition_r +
                0.10 * support_r +
                0.10 * loss_r
            )

            persistence = phase_persistence_score(structural_response)
            instability = instability_from_response(structural_response, persistence, alpha_radius)
            status = "valid" if instability == "no" else "unstable"

            grid_rows.append({
                "object_id": object_id,
                "object_name": object_name,
                "target_mass_class": target_mass,
                "selected_model_mass": selected_mass,
                "progenitor_type": progenitor_type,
                "network": network,
                "phase_name": row.get("phase_name", ""),
                "stage_index": row.get("stage_index", ""),
                "alpha": fmt(alpha),
                "alpha_radius": fmt(alpha_radius),
                "gap_base": fmt(gap_base),
                "delta_logT_base": fmt(d_logT),
                "delta_logRho_base": fmt(d_logRho),
                "delta_ye_base": fmt(d_ye),
                "delta_support_base": fmt(d_support),
                "delta_energy_loss_base": fmt(d_loss),
                "composition_transition_count": fmt(comp_count),
                "gap_alpha": fmt(gap_alpha),
                "delta_logT_alpha": fmt(logT_alpha),
                "delta_logRho_alpha": fmt(logRho_alpha),
                "delta_ye_alpha": fmt(ye_alpha),
                "delta_support_alpha": fmt(support_alpha),
                "delta_energy_loss_alpha": fmt(loss_alpha),
                "gap_response_norm": fmt(gap_r),
                "thermal_response_norm": fmt(thermal_r),
                "density_response_norm": fmt(density_r),
                "composition_response_norm": fmt(composition_r),
                "support_response_norm": fmt(support_r),
                "loss_response_norm": fmt(loss_r),
                "structural_response": fmt(structural_response),
                "phase_persistence_score": fmt(persistence),
                "boundary_role_mode": row.get("boundary_role_mode", ""),
                "composition_stage_mode": row.get("composition_stage_mode", ""),
                "dominant_species_mode": row.get("dominant_species_mode", ""),
                "alpha_status": status,
                "instability_flag": instability,
            })

    return grid_rows


def compute_vector(grid_rows, object_id):
    if not grid_rows:
        raise ValueError("No grid rows supplied")

    first = grid_rows[0]
    gap_responses = [to_float(r.get("gap_response_norm")) for r in grid_rows]
    structural_responses = [to_float(r.get("structural_response")) for r in grid_rows]

    valid_rows = [r for r in grid_rows if r.get("alpha_status") == "valid"]
    instability_rows = [r for r in grid_rows if r.get("instability_flag") == "yes"]

    mean_gr = safe_mean(gap_responses)
    var_gr = safe_variance(gap_responses)

    grouped = defaultdict(list)
    for r in grid_rows:
        key = (r.get("stage_index", ""), r.get("phase_name", ""))
        grouped[key].append(to_float(r.get("structural_response")))
    group_means = [safe_mean(vals) for vals in grouped.values()]
    anisotropic_persistence = safe_variance(group_means)

    admissibility_persistence = len(valid_rows) / len(grid_rows) if grid_rows else 0.0

    if instability_rows:
        collapse_onset_radius = min(to_float(r.get("alpha_radius")) for r in instability_rows)
        collapse_observed = "yes"
    else:
        collapse_onset_radius = max(to_float(r.get("alpha_radius")) for r in grid_rows)
        collapse_observed = "no"

    ref = REFERENCE_RESULTS.get(object_id, {})
    kappa = ref.get("kappa_connect", "")
    tail = ref.get("tail_dominance", "")

    notes = (
        "first-pass Phase A alpha vector from real pre-supernova radial profile; "
        "collapse_onset_radius records max tested radius when collapse_observed=no"
    )

    return {
        "object_id": object_id,
        "object_name": first.get("object_name", object_id),
        "target_mass_class": first.get("target_mass_class", ""),
        "selected_model_mass": first.get("selected_model_mass", ""),
        "progenitor_type": first.get("progenitor_type", ""),
        "network": first.get("network", ""),
        "mean_GR": fmt(mean_gr),
        "var_GR": fmt(var_gr),
        "anisotropic_persistence": fmt(anisotropic_persistence),
        "admissibility_persistence": fmt(admissibility_persistence),
        "collapse_onset_radius": fmt(collapse_onset_radius),
        "collapse_observed": collapse_observed,
        "kappa_connect_reference": fmt(kappa) if kappa != "" else "",
        "tail_dominance_reference": fmt(tail) if tail != "" else "",
        "n_grid_rows": len(grid_rows),
        "n_valid_rows": len(valid_rows),
        "n_instability_rows": len(instability_rows),
        "notes": notes,
    }


def convert_one(input_csv, grid_csv, vector_csv, alphas):
    input_csv = Path(input_csv)
    object_id = object_id_from_path(input_csv)
    rows = read_csv(input_csv)
    grid_rows = build_grid_rows(rows, object_id, alphas)
    vector = compute_vector(grid_rows, object_id)

    write_csv(grid_csv, grid_rows, GRID_COLUMNS)
    write_csv(vector_csv, [vector], VECTOR_COLUMNS)

    return {
        "object_id": object_id,
        "object_name": vector["object_name"],
        "input_file": str(input_csv),
        "grid_file": str(grid_csv),
        "vector_file": str(vector_csv),
        "canonical_rows": len(rows),
        "grid_rows": len(grid_rows),
        "alpha_min": min(alphas),
        "alpha_max": max(alphas),
        "alpha_points": len(alphas),
        "valid_fraction": vector["admissibility_persistence"],
        "collapse_observed": vector["collapse_observed"],
        "collapse_onset_radius": vector["collapse_onset_radius"],
        "status": "converted",
    }, vector


def stem_for(input_file):
    stem = Path(input_file).stem
    if stem.endswith("_struc_perc_input"):
        return stem.replace("_struc_perc_input", "")
    return stem


def batch_convert(input_dir, alpha_dir, alpha_min, alpha_max, alpha_points):
    input_dir = Path(input_dir)
    alpha_dir = Path(alpha_dir)
    grids_dir = alpha_dir / "grids"
    vectors_dir = alpha_dir / "vectors"
    summaries_dir = alpha_dir / "summaries"

    grids_dir.mkdir(parents=True, exist_ok=True)
    vectors_dir.mkdir(parents=True, exist_ok=True)
    summaries_dir.mkdir(parents=True, exist_ok=True)

    input_files = sorted(input_dir.glob("A*_struc_perc_input.csv"))
    if not input_files:
        raise FileNotFoundError(f"No A*_struc_perc_input.csv files found in {input_dir}")

    alphas = make_alpha_values(alpha_min, alpha_max, alpha_points)

    summaries = []
    vectors = []
    for input_file in input_files:
        stem = stem_for(input_file)
        grid_file = grids_dir / f"{stem}_alpha_grid.csv"
        vector_file = vectors_dir / f"{stem}_5d_vector.csv"
        summary, vector = convert_one(input_file, grid_file, vector_file, alphas)
        summaries.append(summary)
        vectors.append(vector)

        print(f"Converted: {input_file}")
        print(f"  grid: {grid_file}")
        print(f"  vector: {vector_file}")
        print(f"  rows: canonical={summary['canonical_rows']} grid={summary['grid_rows']} valid_fraction={summary['valid_fraction']} collapse={summary['collapse_observed']}")

    write_csv(summaries_dir / "A_ALPHA_APPLICATION_SUMMARY.csv", summaries, ALPHA_SUMMARY_COLUMNS)
    write_csv(summaries_dir / "A_5D_VECTOR_SUMMARY.csv", vectors, VECTOR_COLUMNS)

    print(f"Summary written: {summaries_dir / 'A_ALPHA_APPLICATION_SUMMARY.csv'}")
    print(f"5D vector summary written: {summaries_dir / 'A_5D_VECTOR_SUMMARY.csv'}")


def main():
    parser = argparse.ArgumentParser(description="Apply alpha deformation to Phase A canonical inputs.")
    parser.add_argument("paths", nargs="*", help="Single mode: input_csv grid_csv vector_csv")
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--alpha-min", type=float, default=0.5)
    parser.add_argument("--alpha-max", type=float, default=1.5)
    parser.add_argument("--alpha-points", type=int, default=21)
    args = parser.parse_args()

    alphas = make_alpha_values(args.alpha_min, args.alpha_max, args.alpha_points)

    if args.batch:
        if len(args.paths) != 2:
            raise SystemExit("Batch usage: python tools/a_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application")
        batch_convert(args.paths[0], args.paths[1], args.alpha_min, args.alpha_max, args.alpha_points)
        return

    if len(args.paths) != 3:
        raise SystemExit(__doc__)

    summary, vector = convert_one(args.paths[0], args.paths[1], args.paths[2], alphas)
    print(f"Object: {summary['object_name']}")
    print(f"Canonical rows: {summary['canonical_rows']}")
    print(f"Grid rows: {summary['grid_rows']}")
    print(f"Valid fraction: {summary['valid_fraction']}")
    print(f"Collapse observed: {summary['collapse_observed']}")
    print(f"Grid output: {summary['grid_file']}")
    print(f"Vector output: {summary['vector_file']}")


if __name__ == "__main__":
    main()
