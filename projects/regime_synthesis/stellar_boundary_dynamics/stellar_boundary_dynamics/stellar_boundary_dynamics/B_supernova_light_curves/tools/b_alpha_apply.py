#!/usr/bin/env python3
"""
b_alpha_apply.py

Phase B alpha-application / deformation-grid constructor for
STELLAR_BOUNDARY_DYNAMICS_I.

Reads compact Phase B STRUC_PERC_I canonical input CSV files and writes:

  alpha_application/grids/<OBJECT>_alpha_grid.csv
  alpha_application/vectors/<OBJECT>_5d_vector.csv
  alpha_application/summaries/B_ALPHA_APPLICATION_SUMMARY.csv
  alpha_application/summaries/B_5D_VECTOR_SUMMARY.csv

Input layer:
  struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv

This script does NOT re-run raw photometry and does NOT re-run STRUC-PERC-I.
It operates on the compact object × band × phase structural rows that already
passed STRUC-PERC-I numeric ladder evaluation.

Usage from B_supernova_light_curves/:

  python tools/b_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application

Single object:

  python tools/b_alpha_apply.py struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv alpha_application/grids/B_SN1987A_alpha_grid.csv alpha_application/vectors/B_SN1987A_5d_vector.csv

Optional alpha grid:

  python tools/b_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application --alpha-min 0.5 --alpha-max 1.5 --alpha-points 21
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
    "supernova_type",
    "band",
    "phase_name",
    "stage_index",
    "alpha",
    "alpha_radius",
    "gap_base",
    "duration_base",
    "slope_base",
    "curvature_base",
    "gap_alpha",
    "duration_alpha",
    "slope_alpha",
    "curvature_alpha",
    "gap_response_norm",
    "duration_response_norm",
    "slope_response_norm",
    "curvature_response_norm",
    "structural_response",
    "phase_persistence_score",
    "boundary_role",
    "support_regime_proxy",
    "alpha_status",
    "instability_flag",
]

VECTOR_COLUMNS = [
    "object_id",
    "object_name",
    "supernova_type",
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

PHASE_ORDER = {
    "pre_discovery_or_baseline": 0,
    "rise": 1,
    "peak": 2,
    "early_decline": 3,
    "plateau_or_shoulder": 4,
    "break": 5,
    "tail_decay": 6,
    "late_relaxation": 7,
    "unclassified": 8,
}

# References from the STRUC-PERC-I batch result already obtained.
# These values are used only as context in the 5D vector file.
REFERENCE_RESULTS = {
    "B_SN1987A": {"kappa_connect": 0.4216965034285822, "tail_dominance": 0.0},
    "B_SN1993J": {"kappa_connect": 0.4216965034285822, "tail_dominance": 0.0},
    "B_SN1999em": {"kappa_connect": 0.1778279410038923, "tail_dominance": 0.0},
    "B_SN2011dh": {"kappa_connect": 1.0, "tail_dominance": 0.0},
    "B_SN2012aw": {"kappa_connect": 4.399999999999965, "tail_dominance": 0.3290154711673699},
    "B_SN2013ej": {"kappa_connect": 0.31622776601683805, "tail_dominance": 0.0},
}


def to_float(value, default=0.0):
    if value is None:
        return default
    text = str(value).strip()
    if text == "":
        return default
    try:
        x = float(text)
    except ValueError:
        return default
    if math.isnan(x) or math.isinf(x):
        return default
    return x


def fmt(value):
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10g}"
    return str(value)


def safe_mean(values):
    values = [v for v in values if v is not None and math.isfinite(v)]
    return statistics.fmean(values) if values else 0.0


def safe_variance(values):
    values = [v for v in values if v is not None and math.isfinite(v)]
    if len(values) < 2:
        return 0.0
    return statistics.pvariance(values)


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


def object_name_from_rows(rows, object_id):
    for row in rows:
        name = row.get("object_name", "").strip()
        if name:
            return name
    return object_id.replace("B_", "").replace("_", " ")


def supernova_type_from_rows(rows):
    for row in rows:
        typ = row.get("supernova_type", "").strip()
        if typ:
            return typ
    return "unknown"


def make_alpha_values(alpha_min, alpha_max, alpha_points):
    if alpha_points <= 1:
        return [1.0]
    step = (alpha_max - alpha_min) / (alpha_points - 1)
    return [alpha_min + i * step for i in range(alpha_points)]


def robust_scale(values):
    values = sorted(abs(v) for v in values if math.isfinite(v))
    if not values:
        return 1.0
    mid = len(values) // 2
    if len(values) % 2:
        med = values[mid]
    else:
        med = (values[mid - 1] + values[mid]) / 2.0
    return med if med > 0 else max(values) if max(values) > 0 else 1.0


def normalized_response(base, alpha_value, scale):
    """
    Response is measured as absolute deformation displacement relative to a
    robust dataset scale. This makes gap, duration, slope, and curvature
    comparable without claiming physical equivalence.
    """
    return abs(base * (alpha_value - 1.0)) / scale if scale > 0 else 0.0


def phase_persistence_score(structural_response):
    """
    First-pass persistence score. A score near 1 means the phase row remains
    close to alpha = 1 behavior. The score decreases smoothly under deformation.
    """
    return 1.0 / (1.0 + structural_response)


def instability_from_response(structural_response, phase_persistence, alpha_radius):
    """
    Conservative first-pass instability criterion.

    Instability is marked only if the structural response is high and the
    persistence score is low. This avoids labeling normal alpha displacement
    as collapse.
    """
    if structural_response >= 2.0 and phase_persistence <= 0.333:
        return "yes"
    if alpha_radius >= 0.45 and structural_response >= 1.5 and phase_persistence <= 0.4:
        return "yes"
    return "no"


def phase_sort_key(row):
    try:
        stage = int(float(row.get("stage_index", PHASE_ORDER.get(row.get("phase_name", ""), 999))))
    except ValueError:
        stage = PHASE_ORDER.get(row.get("phase_name", ""), 999)
    return (
        row.get("object_name", ""),
        row.get("band", ""),
        stage,
        PHASE_ORDER.get(row.get("phase_name", ""), 999),
        row.get("phase_name", ""),
    )


def build_grid_rows(input_rows, object_id, alphas):
    object_name = object_name_from_rows(input_rows, object_id)
    supernova_type = supernova_type_from_rows(input_rows)

    gap_values = [to_float(r.get("gap"), to_float(r.get("mag_range"), 0.0)) for r in input_rows]
    duration_values = [to_float(r.get("duration_days"), 0.0) for r in input_rows]
    slope_values = [to_float(r.get("mean_slope"), 0.0) for r in input_rows]
    curvature_values = [to_float(r.get("mean_curvature"), 0.0) for r in input_rows]

    gap_scale = robust_scale(gap_values)
    duration_scale = robust_scale(duration_values)
    slope_scale = robust_scale(slope_values)
    curvature_scale = robust_scale(curvature_values)

    grid_rows = []

    for row in sorted(input_rows, key=phase_sort_key):
        gap_base = abs(to_float(row.get("gap"), to_float(row.get("mag_range"), 0.0)))
        duration_base = abs(to_float(row.get("duration_days"), 0.0))
        slope_base = to_float(row.get("mean_slope"), 0.0)
        curvature_base = to_float(row.get("mean_curvature"), 0.0)

        for alpha in alphas:
            alpha_radius = abs(alpha - 1.0)

            gap_alpha = gap_base * alpha
            duration_alpha = duration_base * alpha
            slope_alpha = slope_base * alpha
            curvature_alpha = curvature_base * alpha

            gap_r = normalized_response(gap_base, alpha, gap_scale)
            duration_r = normalized_response(duration_base, alpha, duration_scale)
            slope_r = normalized_response(slope_base, alpha, slope_scale)
            curvature_r = normalized_response(curvature_base, alpha, curvature_scale)

            # Weighted first-pass structural response. Gap and duration dominate
            # because they are more stable than finite-difference curvature.
            structural_response = (
                0.40 * gap_r +
                0.30 * duration_r +
                0.15 * slope_r +
                0.15 * curvature_r
            )

            persistence = phase_persistence_score(structural_response)
            instability = instability_from_response(structural_response, persistence, alpha_radius)
            status = "valid" if instability == "no" else "unstable"

            grid_rows.append({
                "object_id": object_id,
                "object_name": object_name,
                "supernova_type": supernova_type,
                "band": row.get("band", ""),
                "phase_name": row.get("phase_name", ""),
                "stage_index": row.get("stage_index", ""),
                "alpha": fmt(alpha),
                "alpha_radius": fmt(alpha_radius),
                "gap_base": fmt(gap_base),
                "duration_base": fmt(duration_base),
                "slope_base": fmt(slope_base),
                "curvature_base": fmt(curvature_base),
                "gap_alpha": fmt(gap_alpha),
                "duration_alpha": fmt(duration_alpha),
                "slope_alpha": fmt(slope_alpha),
                "curvature_alpha": fmt(curvature_alpha),
                "gap_response_norm": fmt(gap_r),
                "duration_response_norm": fmt(duration_r),
                "slope_response_norm": fmt(slope_r),
                "curvature_response_norm": fmt(curvature_r),
                "structural_response": fmt(structural_response),
                "phase_persistence_score": fmt(persistence),
                "boundary_role": row.get("boundary_role", ""),
                "support_regime_proxy": row.get("support_regime_proxy", ""),
                "alpha_status": status,
                "instability_flag": instability,
            })

    return grid_rows


def compute_vector(grid_rows, object_id, object_name, supernova_type):
    gap_responses = [to_float(r.get("gap_response_norm"), 0.0) for r in grid_rows]
    structural_responses = [to_float(r.get("structural_response"), 0.0) for r in grid_rows]
    persistence_scores = [to_float(r.get("phase_persistence_score"), 0.0) for r in grid_rows]

    valid_rows = [r for r in grid_rows if r.get("alpha_status") == "valid"]
    instability_rows = [r for r in grid_rows if r.get("instability_flag") == "yes"]

    # mean_GR and var_GR use normalized gap response specifically.
    mean_gr = safe_mean(gap_responses)
    var_gr = safe_variance(gap_responses)

    # Anisotropic persistence: variance of mean structural response across band-phase groups.
    grouped = defaultdict(list)
    for r in grid_rows:
        key = (r.get("band", ""), r.get("phase_name", ""))
        grouped[key].append(to_float(r.get("structural_response"), 0.0))
    group_means = [safe_mean(vals) for vals in grouped.values()]
    anisotropic_persistence = safe_variance(group_means)

    admissibility_persistence = len(valid_rows) / len(grid_rows) if grid_rows else 0.0

    if instability_rows:
        collapse_onset_radius = min(to_float(r.get("alpha_radius"), 0.0) for r in instability_rows)
        collapse_observed = "yes"
    else:
        collapse_onset_radius = max((to_float(r.get("alpha_radius"), 0.0) for r in grid_rows), default=0.0)
        collapse_observed = "no"

    ref = REFERENCE_RESULTS.get(object_id, {})
    kappa_ref = ref.get("kappa_connect", "")
    tail_ref = ref.get("tail_dominance", "")

    notes = (
        "first-pass Phase B alpha vector; "
        "gap response is phase-local magnitude-range deformation; "
        "collapse_onset_radius records max tested radius when collapse_observed=no"
    )
    if object_id == "B_SN2012aw":
        notes += "; attention: SN2012aw had high STRUC-PERC-I kappa_connect and tail dominance"

    return {
        "object_id": object_id,
        "object_name": object_name,
        "supernova_type": supernova_type,
        "mean_GR": fmt(mean_gr),
        "var_GR": fmt(var_gr),
        "anisotropic_persistence": fmt(anisotropic_persistence),
        "admissibility_persistence": fmt(admissibility_persistence),
        "collapse_onset_radius": fmt(collapse_onset_radius),
        "collapse_observed": collapse_observed,
        "kappa_connect_reference": fmt(kappa_ref) if kappa_ref != "" else "",
        "tail_dominance_reference": fmt(tail_ref) if tail_ref != "" else "",
        "n_grid_rows": len(grid_rows),
        "n_valid_rows": len(valid_rows),
        "n_instability_rows": len(instability_rows),
        "notes": notes,
    }


def convert_one(input_csv, grid_csv, vector_csv, alphas):
    input_csv = Path(input_csv)
    object_id = object_id_from_path(input_csv)
    input_rows = read_csv(input_csv)

    if not input_rows:
        raise ValueError(f"No rows in {input_csv}")

    object_name = object_name_from_rows(input_rows, object_id)
    supernova_type = supernova_type_from_rows(input_rows)

    grid_rows = build_grid_rows(input_rows, object_id, alphas)
    vector_row = compute_vector(grid_rows, object_id, object_name, supernova_type)

    write_csv(grid_csv, grid_rows, GRID_COLUMNS)
    write_csv(vector_csv, [vector_row], VECTOR_COLUMNS)

    alpha_min = min(alphas) if alphas else ""
    alpha_max = max(alphas) if alphas else ""

    return {
        "object_id": object_id,
        "object_name": object_name,
        "input_file": str(input_csv),
        "grid_file": str(grid_csv),
        "vector_file": str(vector_csv),
        "canonical_rows": len(input_rows),
        "grid_rows": len(grid_rows),
        "alpha_min": alpha_min,
        "alpha_max": alpha_max,
        "alpha_points": len(alphas),
        "valid_fraction": vector_row["admissibility_persistence"],
        "collapse_observed": vector_row["collapse_observed"],
        "collapse_onset_radius": vector_row["collapse_onset_radius"],
        "status": "converted",
    }, vector_row


def output_stem_for(input_file):
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

    input_files = sorted(input_dir.glob("B_*_struc_perc_input.csv"))
    if not input_files:
        raise FileNotFoundError(f"No B_*_struc_perc_input.csv files found in {input_dir}")

    alphas = make_alpha_values(alpha_min, alpha_max, alpha_points)
    summaries = []
    vectors = []

    for input_file in input_files:
        stem = output_stem_for(input_file)
        grid_file = grids_dir / f"{stem}_alpha_grid.csv"
        vector_file = vectors_dir / f"{stem}_5d_vector.csv"

        summary, vector = convert_one(input_file, grid_file, vector_file, alphas)
        summaries.append(summary)
        vectors.append(vector)

        print(f"Converted: {input_file}")
        print(f"  grid:   {grid_file}")
        print(f"  vector: {vector_file}")
        print(f"  rows: canonical={summary['canonical_rows']} grid={summary['grid_rows']} valid_fraction={summary['valid_fraction']} collapse={summary['collapse_observed']}")

    alpha_summary = summaries_dir / "B_ALPHA_APPLICATION_SUMMARY.csv"
    vector_summary = summaries_dir / "B_5D_VECTOR_SUMMARY.csv"

    write_csv(alpha_summary, summaries, ALPHA_SUMMARY_COLUMNS)
    write_csv(vector_summary, vectors, VECTOR_COLUMNS)

    print(f"Summary written: {alpha_summary}")
    print(f"5D vector summary written: {vector_summary}")


def parse_args():
    parser = argparse.ArgumentParser(description="Apply alpha deformation to Phase B canonical inputs.")
    parser.add_argument("paths", nargs="*", help="Single mode: input_csv grid_csv vector_csv")
    parser.add_argument("--batch", action="store_true", help="Batch mode: input_dir alpha_application_dir")
    parser.add_argument("--alpha-min", type=float, default=0.5)
    parser.add_argument("--alpha-max", type=float, default=1.5)
    parser.add_argument("--alpha-points", type=int, default=21)
    return parser.parse_args()


def main():
    args = parse_args()
    alphas = make_alpha_values(args.alpha_min, args.alpha_max, args.alpha_points)

    if args.batch:
        if len(args.paths) != 2:
            raise SystemExit("Batch usage: python tools/b_alpha_apply.py --batch struc_perc_i/canonical_inputs alpha_application")
        input_dir, alpha_dir = args.paths
        batch_convert(input_dir, alpha_dir, args.alpha_min, args.alpha_max, args.alpha_points)
        return

    if len(args.paths) != 3:
        raise SystemExit(__doc__)

    input_csv, grid_csv, vector_csv = args.paths
    summary, vector = convert_one(input_csv, grid_csv, vector_csv, alphas)

    print(f"Object: {summary['object_name']}")
    print(f"Canonical rows: {summary['canonical_rows']}")
    print(f"Grid rows: {summary['grid_rows']}")
    print(f"Valid fraction: {summary['valid_fraction']}")
    print(f"Collapse observed: {summary['collapse_observed']}")
    print(f"Grid output: {summary['grid_file']}")
    print(f"Vector output: {summary['vector_file']}")


if __name__ == "__main__":
    main()
