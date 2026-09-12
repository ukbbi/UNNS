#!/usr/bin/env python3
"""
c_alpha_apply.py

STELLAR_BOUNDARY_DYNAMICS_I
Phase C — alpha-application / deformation-grid constructor.

Reads Phase C STRUC-PERC-I canonical inputs:

  struc_perc_i/canonical_inputs/C1_SN1993J_struc_perc_input.csv
  struc_perc_i/canonical_inputs/C2_SN2012aw_struc_perc_input.csv

Writes:

  alpha_application/grids/C1_SN1993J_alpha_grid.csv
  alpha_application/grids/C2_SN2012aw_alpha_grid.csv

  alpha_application/vectors/C1_SN1993J_5d_vector.csv
  alpha_application/vectors/C2_SN2012aw_5d_vector.csv

  alpha_application/summaries/C_ALPHA_APPLICATION_SUMMARY.csv
  alpha_application/summaries/C_5D_VECTOR_SUMMARY.csv

Usage from C_spectral_time_series/:

  python tools/c_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application

Optional alpha grid:

  python tools/c_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application --alpha-min 0.5 --alpha-max 1.5 --alpha-points 21

Single object:

  python tools/c_alpha_apply.py struc_perc_i/canonical_inputs/C1_SN1993J_struc_perc_input.csv alpha_application/grids/C1_SN1993J_alpha_grid.csv alpha_application/vectors/C1_SN1993J_5d_vector.csv

This is a structural spectral deformation layer. It does not claim abundance
measurement, radiative-transfer modeling, or nucleosynthesis yield recovery.
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
    "line_id",
    "line_name",
    "element_group",
    "spectral_phase_role",
    "spectrum_index",
    "alpha",
    "alpha_radius",
    "gap_base",
    "delta_line_flux_base",
    "delta_line_depth_base",
    "delta_equivalent_width_base",
    "delta_velocity_base",
    "delta_width_base",
    "delta_signal_quality_base",
    "line_transition_flag",
    "element_transition_flag",
    "gap_alpha",
    "delta_line_flux_alpha",
    "delta_line_depth_alpha",
    "delta_equivalent_width_alpha",
    "delta_velocity_alpha",
    "delta_width_alpha",
    "delta_signal_quality_alpha",
    "gap_response_norm",
    "flux_response_norm",
    "depth_response_norm",
    "equivalent_width_response_norm",
    "velocity_response_norm",
    "width_response_norm",
    "quality_response_norm",
    "transition_response_norm",
    "structural_response",
    "phase_persistence_score",
    "tail_pressure_proxy",
    "boundary_role",
    "struc_perc_role",
    "alpha_status",
    "instability_flag",
]

VECTOR_COLUMNS = [
    "object_id",
    "object_name",
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
    "C1_SN1993J": {
        "kappa_connect": 201.4048389456797,
        "tail_dominance": 0.5700456253569127,
    },
    "C2_SN2012aw": {
        "kappa_connect": 3992.353936889229,
        "tail_dominance": 0.9594287169370818,
    },
}


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


def persistence_score(structural_response, tail_pressure):
    return 1.0 / (1.0 + structural_response + 0.25 * tail_pressure)


def instability_from_response(structural_response, persistence, alpha_radius, tail_pressure):
    """
    Conservative spectral instability flag.

    Spectral ladders can be tail-dominated without failing percolation. We flag
    instability only when response and tail pressure are both high.
    """
    if structural_response >= 2.5 and persistence <= 0.30:
        return "yes"
    if tail_pressure >= 1.0 and structural_response >= 1.75 and alpha_radius >= 0.35:
        return "yes"
    if tail_pressure >= 2.0 and alpha_radius >= 0.25:
        return "yes"
    return "no"


def phase_sort_key(row):
    return (
        int(to_float(row.get("spectrum_index"), 0)),
        row.get("line_id", ""),
        to_float(row.get("rest_wavelength"), 0.0),
    )


def build_grid_rows(rows, object_id, alphas):
    if not rows:
        raise ValueError("No canonical rows supplied")

    first = rows[0]
    object_name = first.get("object_name", object_id)

    gap_vals = [to_float(r.get("gap")) for r in rows]
    flux_vals = [to_float(r.get("delta_line_flux")) for r in rows]
    depth_vals = [to_float(r.get("delta_line_depth")) for r in rows]
    ew_vals = [to_float(r.get("delta_equivalent_width")) for r in rows]
    vel_vals = [to_float(r.get("delta_velocity")) for r in rows]
    width_vals = [to_float(r.get("delta_width")) for r in rows]
    qual_vals = [to_float(r.get("delta_signal_quality")) for r in rows]
    trans_vals = [
        to_float(r.get("line_transition_flag")) + to_float(r.get("element_transition_flag"))
        for r in rows
    ]

    scales = {
        "gap": robust_scale(gap_vals),
        "flux": robust_scale(flux_vals),
        "depth": robust_scale(depth_vals),
        "ew": robust_scale(ew_vals),
        "velocity": robust_scale(vel_vals),
        "width": robust_scale(width_vals),
        "quality": robust_scale(qual_vals),
        "transition": robust_scale(trans_vals),
    }

    ref = REFERENCE_RESULTS.get(object_id, {})
    tail_ref = to_float(ref.get("tail_dominance", 0.0))
    kappa_ref = to_float(ref.get("kappa_connect", 0.0))

    # Tail pressure carries STRUC-PERC-I tail/kappa geometry into alpha layer.
    kappa_scale = 500.0
    base_tail_pressure = tail_ref * math.log1p(max(kappa_ref, 0.0)) / math.log1p(kappa_scale)

    grid_rows = []

    for row in sorted(rows, key=phase_sort_key):
        gap_base = abs(to_float(row.get("gap")))
        d_flux = abs(to_float(row.get("delta_line_flux")))
        d_depth = abs(to_float(row.get("delta_line_depth")))
        d_ew = abs(to_float(row.get("delta_equivalent_width")))
        d_vel = abs(to_float(row.get("delta_velocity")))
        d_width = abs(to_float(row.get("delta_width")))
        d_quality = abs(to_float(row.get("delta_signal_quality")))
        transition = abs(to_float(row.get("line_transition_flag")) + to_float(row.get("element_transition_flag")))

        for alpha in alphas:
            alpha_radius = abs(alpha - 1.0)

            gap_alpha = gap_base * alpha
            flux_alpha = d_flux * alpha
            depth_alpha = d_depth * alpha
            ew_alpha = d_ew * alpha
            vel_alpha = d_vel * alpha
            width_alpha = d_width * alpha
            quality_alpha = d_quality * alpha

            gap_r = normalized_response(gap_base, alpha, scales["gap"])
            flux_r = normalized_response(d_flux, alpha, scales["flux"])
            depth_r = normalized_response(d_depth, alpha, scales["depth"])
            ew_r = normalized_response(d_ew, alpha, scales["ew"])
            vel_r = normalized_response(d_vel, alpha, scales["velocity"])
            width_r = normalized_response(d_width, alpha, scales["width"])
            qual_r = normalized_response(d_quality, alpha, scales["quality"])
            trans_r = normalized_response(transition, alpha, scales["transition"])

            structural_response = (
                0.20 * gap_r +
                0.16 * flux_r +
                0.14 * depth_r +
                0.14 * ew_r +
                0.16 * vel_r +
                0.10 * width_r +
                0.06 * qual_r +
                0.04 * trans_r
            )

            tail_pressure = base_tail_pressure * (1.0 + alpha_radius)
            persistence = persistence_score(structural_response, tail_pressure)
            instability = instability_from_response(structural_response, persistence, alpha_radius, tail_pressure)
            status = "valid" if instability == "no" else "unstable"

            grid_rows.append({
                "object_id": object_id,
                "object_name": object_name,
                "line_id": row.get("line_id", ""),
                "line_name": row.get("line_name", ""),
                "element_group": row.get("element_group", ""),
                "spectral_phase_role": row.get("spectral_phase_role", ""),
                "spectrum_index": row.get("spectrum_index", ""),
                "alpha": fmt(alpha),
                "alpha_radius": fmt(alpha_radius),
                "gap_base": fmt(gap_base),
                "delta_line_flux_base": fmt(d_flux),
                "delta_line_depth_base": fmt(d_depth),
                "delta_equivalent_width_base": fmt(d_ew),
                "delta_velocity_base": fmt(d_vel),
                "delta_width_base": fmt(d_width),
                "delta_signal_quality_base": fmt(d_quality),
                "line_transition_flag": row.get("line_transition_flag", ""),
                "element_transition_flag": row.get("element_transition_flag", ""),
                "gap_alpha": fmt(gap_alpha),
                "delta_line_flux_alpha": fmt(flux_alpha),
                "delta_line_depth_alpha": fmt(depth_alpha),
                "delta_equivalent_width_alpha": fmt(ew_alpha),
                "delta_velocity_alpha": fmt(vel_alpha),
                "delta_width_alpha": fmt(width_alpha),
                "delta_signal_quality_alpha": fmt(quality_alpha),
                "gap_response_norm": fmt(gap_r),
                "flux_response_norm": fmt(flux_r),
                "depth_response_norm": fmt(depth_r),
                "equivalent_width_response_norm": fmt(ew_r),
                "velocity_response_norm": fmt(vel_r),
                "width_response_norm": fmt(width_r),
                "quality_response_norm": fmt(qual_r),
                "transition_response_norm": fmt(trans_r),
                "structural_response": fmt(structural_response),
                "phase_persistence_score": fmt(persistence),
                "tail_pressure_proxy": fmt(tail_pressure),
                "boundary_role": row.get("boundary_role", ""),
                "struc_perc_role": row.get("struc_perc_role", ""),
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
        key = (r.get("element_group", ""), r.get("line_id", ""))
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
        "first-pass Phase C alpha vector from real WISeREP spectral line ladders; "
        "line-window proxies are structural features, not abundances"
    )

    return {
        "object_id": object_id,
        "object_name": first.get("object_name", object_id),
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

    input_files = sorted(input_dir.glob("C*_struc_perc_input.csv"))
    if not input_files:
        raise FileNotFoundError(f"No C*_struc_perc_input.csv files found in {input_dir}")

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

    write_csv(summaries_dir / "C_ALPHA_APPLICATION_SUMMARY.csv", summaries, ALPHA_SUMMARY_COLUMNS)
    write_csv(summaries_dir / "C_5D_VECTOR_SUMMARY.csv", vectors, VECTOR_COLUMNS)

    print(f"Summary written: {summaries_dir / 'C_ALPHA_APPLICATION_SUMMARY.csv'}")
    print(f"5D vector summary written: {summaries_dir / 'C_5D_VECTOR_SUMMARY.csv'}")


def main():
    parser = argparse.ArgumentParser(description="Apply alpha deformation to Phase C spectral canonical inputs.")
    parser.add_argument("paths", nargs="*", help="Single mode: input_csv grid_csv vector_csv")
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--alpha-min", type=float, default=0.5)
    parser.add_argument("--alpha-max", type=float, default=1.5)
    parser.add_argument("--alpha-points", type=int, default=21)
    args = parser.parse_args()

    alphas = make_alpha_values(args.alpha_min, args.alpha_max, args.alpha_points)

    if args.batch:
        if len(args.paths) != 2:
            raise SystemExit("Batch usage: python tools/c_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application")
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
