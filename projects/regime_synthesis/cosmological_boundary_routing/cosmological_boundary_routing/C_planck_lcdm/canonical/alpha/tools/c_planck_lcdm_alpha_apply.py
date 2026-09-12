#!/usr/bin/env python3
"""
c_planck_lcdm_alpha_apply.py

Dataset C alpha-application / deformation-grid constructor for
COSMOLOGICAL BOUNDARY ROUTING.

This script adapts the alpha-grid method used in the recent Stellar Boundary
Dynamics workflow to the validated Planck-anchored Lambda-CDM trajectory.

It does NOT multiply the complete ln(E) ladder and call that a new ladder.
Instead, it:

1. reads the validated cosmological trajectory;
2. constructs interval-level structural features;
3. applies alpha over a controlled deformation grid;
4. robustly normalizes each feature response;
5. computes structural response and persistence;
6. exports the established 5D rigidity vector;
7. writes a normalization-review record and run summary.

Default input, resolved from canonical/alpha/tools/:

    ../../../generated_trajectory/validated/
    planck_lcdm_trajectory_validated.csv

Default outputs:

    ../grids/C_PLANCK_LCDM_alpha_grid.csv
    ../vectors/C_PLANCK_LCDM_5d_vector.csv
    ../summaries/C_ALPHA_APPLICATION_SUMMARY.csv
    ../normalization_review/C_ALPHA_NORMALIZATION_REVIEW.csv

Methodological status:
    This is the Dataset C cosmological adaptation of the established alpha-grid
    procedure. The direct STRUC-PERC-I and STRUC-I results remain separate.

No third-party packages are required.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


OBJECT_ID = "C_PLANCK_LCDM"
OBJECT_NAME = "Planck-anchored Lambda-CDM expansion"
DOMAIN = "cosmological-background-trajectory"

KAPPA_CONNECT_REFERENCE = 0.0133352143
TAIL_DOMINANCE_REFERENCE = 0.0

DEFAULT_INPUT = (
    Path(__file__).resolve().parent
    / ".."
    / ".."
    / ".."
    / "generated_trajectory"
    / "validated"
    / "planck_lcdm_trajectory_validated.csv"
)

DEFAULT_ALPHA_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GRID = DEFAULT_ALPHA_ROOT / "grids" / f"{OBJECT_ID}_alpha_grid.csv"
DEFAULT_VECTOR = DEFAULT_ALPHA_ROOT / "vectors" / f"{OBJECT_ID}_5d_vector.csv"
DEFAULT_SUMMARY = (
    DEFAULT_ALPHA_ROOT
    / "summaries"
    / "C_ALPHA_APPLICATION_SUMMARY.csv"
)
DEFAULT_REVIEW = (
    DEFAULT_ALPHA_ROOT
    / "normalization_review"
    / "C_ALPHA_NORMALIZATION_REVIEW.csv"
)


GRID_COLUMNS = [
    "object_id",
    "object_name",
    "domain",
    "interval_index",
    "sample_index_left",
    "sample_index_right",
    "scale_factor_mid",
    "redshift_mid",
    "cosmological_era",
    "alpha",
    "alpha_radius",
    "gap_lnE_base",
    "density_logchange_base",
    "curvature_logchange_base",
    "composition_shift_base",
    "margin_change_base",
    "gap_lnE_alpha",
    "density_logchange_alpha",
    "curvature_logchange_alpha",
    "composition_shift_alpha",
    "margin_change_alpha",
    "gap_response_norm",
    "density_response_norm",
    "curvature_response_norm",
    "composition_response_norm",
    "margin_response_norm",
    "structural_response",
    "phase_persistence_score",
    "alpha_status",
    "instability_flag",
]

VECTOR_COLUMNS = [
    "object_id",
    "object_name",
    "domain",
    "mean_GR",
    "var_GR",
    "anisotropic_persistence",
    "admissibility_persistence",
    "collapse_onset_radius",
    "collapse_observed",
    "kappa_connect_reference",
    "tail_dominance_reference",
    "n_base_intervals",
    "n_grid_rows",
    "n_valid_rows",
    "n_instability_rows",
    "alpha_min",
    "alpha_max",
    "alpha_points",
    "notes",
]

SUMMARY_COLUMNS = [
    "object_id",
    "object_name",
    "input_file",
    "grid_file",
    "vector_file",
    "review_file",
    "trajectory_rows",
    "base_intervals",
    "grid_rows",
    "alpha_min",
    "alpha_max",
    "alpha_points",
    "valid_fraction",
    "collapse_observed",
    "collapse_onset_radius",
    "status",
]

REVIEW_COLUMNS = [
    "object_id",
    "object_name",
    "n_grid_rows",
    "mean_gap_response",
    "mean_density_response",
    "mean_curvature_response",
    "mean_composition_response",
    "mean_margin_response",
    "max_channel",
    "density_to_gap_ratio",
    "curvature_to_gap_ratio",
    "composition_to_gap_ratio",
    "margin_to_gap_ratio",
    "anisotropic_persistence_v1",
    "anisotropic_persistence_bounded",
    "admissibility_persistence",
    "collapse_onset_radius",
    "collapse_observed",
    "scale_review_needed",
    "review_status",
    "notes",
]


def to_float(value: object, default: float = 0.0) -> float:
    try:
        if value is None or str(value).strip() == "":
            return default
        result = float(str(value).strip())
        if not math.isfinite(result):
            return default
        return result
    except (TypeError, ValueError):
        return default


def fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def safe_mean(values: Iterable[float]) -> float:
    valid = [value for value in values if math.isfinite(value)]
    return statistics.fmean(valid) if valid else 0.0


def safe_variance(values: Iterable[float]) -> float:
    valid = [value for value in values if math.isfinite(value)]
    return statistics.pvariance(valid) if len(valid) >= 2 else 0.0


def robust_scale(values: Iterable[float]) -> float:
    """
    Stellar-workflow-compatible scale rule:
    median absolute value, then maximum absolute value, then 1.
    """
    valid = sorted(abs(value) for value in values if math.isfinite(value))
    if not valid:
        return 1.0
    median_value = statistics.median(valid)
    if median_value > 0.0:
        return median_value
    maximum = max(valid)
    return maximum if maximum > 0.0 else 1.0


def bounded(value: float) -> float:
    value = max(0.0, value)
    return value / (1.0 + value)


def make_alpha_values(
    alpha_min: float,
    alpha_max: float,
    alpha_points: int,
) -> List[float]:
    if alpha_points <= 1:
        return [1.0]
    if alpha_max < alpha_min:
        raise ValueError("alpha_max must be greater than or equal to alpha_min.")
    step = (alpha_max - alpha_min) / (alpha_points - 1)
    return [alpha_min + index * step for index in range(alpha_points)]


def normalized_response(
    base: float,
    alpha_value: float,
    scale: float,
) -> float:
    if scale <= 0.0:
        return 0.0
    return abs(base * (alpha_value - 1.0)) / scale


def phase_persistence_score(structural_response: float) -> float:
    return 1.0 / (1.0 + structural_response)


def instability_from_response(
    structural_response: float,
    phase_persistence: float,
    alpha_radius: float,
) -> str:
    """
    Established conservative first-pass rule used by the stellar alpha scripts.
    """
    if structural_response >= 2.0 and phase_persistence <= 0.333:
        return "yes"
    if (
        alpha_radius >= 0.45
        and structural_response >= 1.5
        and phase_persistence <= 0.4
    ):
        return "yes"
    return "no"


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(
    path: Path,
    rows: Sequence[Dict[str, object]],
    columns: Sequence[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns))
        writer.writeheader()
        writer.writerows(rows)


def require_columns(rows: Sequence[Dict[str, str]], path: Path) -> None:
    if not rows:
        raise ValueError(f"No trajectory rows found in {path}")

    required = {
        "sample_index",
        "redshift",
        "scale_factor",
        "E_of_a",
        "rho_total_relative_to_rho_crit0",
        "fraction_matter_at_a",
        "fraction_radiation_at_a",
        "fraction_lambda_at_a",
        "ricci_scalar_over_6H0sq",
        "boundary_margin_candidate",
    }
    missing = sorted(required - set(rows[0].keys()))
    if missing:
        raise ValueError(
            "Validated trajectory is missing required column(s): "
            + ", ".join(missing)
        )


def positive_log(value: float, floor: float = 1e-300) -> float:
    return math.log(max(abs(value), floor))


def cosmological_era(row: Dict[str, str]) -> str:
    fractions = {
        "radiation": to_float(row.get("fraction_radiation_at_a")),
        "matter": to_float(row.get("fraction_matter_at_a")),
        "lambda": to_float(row.get("fraction_lambda_at_a")),
    }
    return max(fractions, key=fractions.get)


def build_base_intervals(
    trajectory_rows: Sequence[Dict[str, str]],
) -> List[Dict[str, object]]:
    """
    Convert the trajectory into interval-level structural features.

    The feature definitions are shared across every alpha value:

    gap_lnE:
        |Delta ln(E)|

    density_logchange:
        |Delta ln(rho_total / rho_crit0)|

    curvature_logchange:
        |Delta ln(1 + |R / 6H0^2|)|

    composition_shift:
        Euclidean change in the radiation/matter/lambda fraction vector

    margin_change:
        |Delta boundary_margin_candidate|

    The existing boundary margin remains provisional. It receives the smallest
    response weight and is retained explicitly rather than silently promoted to
    a canonical margin.
    """
    intervals: List[Dict[str, object]] = []

    for index in range(len(trajectory_rows) - 1):
        left = trajectory_rows[index]
        right = trajectory_rows[index + 1]

        e_left = to_float(left.get("E_of_a"))
        e_right = to_float(right.get("E_of_a"))
        rho_left = to_float(left.get("rho_total_relative_to_rho_crit0"))
        rho_right = to_float(right.get("rho_total_relative_to_rho_crit0"))
        ricci_left = to_float(left.get("ricci_scalar_over_6H0sq"))
        ricci_right = to_float(right.get("ricci_scalar_over_6H0sq"))
        margin_left = to_float(left.get("boundary_margin_candidate"))
        margin_right = to_float(right.get("boundary_margin_candidate"))

        fractions_left = (
            to_float(left.get("fraction_radiation_at_a")),
            to_float(left.get("fraction_matter_at_a")),
            to_float(left.get("fraction_lambda_at_a")),
        )
        fractions_right = (
            to_float(right.get("fraction_radiation_at_a")),
            to_float(right.get("fraction_matter_at_a")),
            to_float(right.get("fraction_lambda_at_a")),
        )

        composition_shift = math.sqrt(
            sum(
                (right_value - left_value) ** 2
                for left_value, right_value
                in zip(fractions_left, fractions_right)
            )
        )

        a_left = to_float(left.get("scale_factor"))
        a_right = to_float(right.get("scale_factor"))
        z_left = to_float(left.get("redshift"))
        z_right = to_float(right.get("redshift"))

        interval = {
            "interval_index": index,
            "sample_index_left": left.get("sample_index", index),
            "sample_index_right": right.get("sample_index", index + 1),
            "scale_factor_mid": math.sqrt(max(a_left * a_right, 0.0)),
            "redshift_mid": 0.5 * (z_left + z_right),
            "cosmological_era": cosmological_era(
                {
                    "fraction_radiation_at_a": fmt(
                        0.5 * (fractions_left[0] + fractions_right[0])
                    ),
                    "fraction_matter_at_a": fmt(
                        0.5 * (fractions_left[1] + fractions_right[1])
                    ),
                    "fraction_lambda_at_a": fmt(
                        0.5 * (fractions_left[2] + fractions_right[2])
                    ),
                }
            ),
            "gap_lnE_base": abs(
                positive_log(e_right) - positive_log(e_left)
            ),
            "density_logchange_base": abs(
                positive_log(rho_right) - positive_log(rho_left)
            ),
            "curvature_logchange_base": abs(
                math.log1p(abs(ricci_right))
                - math.log1p(abs(ricci_left))
            ),
            "composition_shift_base": composition_shift,
            "margin_change_base": abs(margin_right - margin_left),
        }
        intervals.append(interval)

    if not intervals:
        raise ValueError("At least two trajectory rows are required.")

    return intervals


def build_grid_rows(
    base_intervals: Sequence[Dict[str, object]],
    alphas: Sequence[float],
) -> List[Dict[str, object]]:
    scales = {
        "gap": robust_scale(
            to_float(row["gap_lnE_base"]) for row in base_intervals
        ),
        "density": robust_scale(
            to_float(row["density_logchange_base"]) for row in base_intervals
        ),
        "curvature": robust_scale(
            to_float(row["curvature_logchange_base"]) for row in base_intervals
        ),
        "composition": robust_scale(
            to_float(row["composition_shift_base"]) for row in base_intervals
        ),
        "margin": robust_scale(
            to_float(row["margin_change_base"]) for row in base_intervals
        ),
    }

    grid_rows: List[Dict[str, object]] = []

    for interval in base_intervals:
        gap_base = to_float(interval["gap_lnE_base"])
        density_base = to_float(interval["density_logchange_base"])
        curvature_base = to_float(interval["curvature_logchange_base"])
        composition_base = to_float(interval["composition_shift_base"])
        margin_base = to_float(interval["margin_change_base"])

        for alpha in alphas:
            alpha_radius = abs(alpha - 1.0)

            gap_response = normalized_response(
                gap_base, alpha, scales["gap"]
            )
            density_response = normalized_response(
                density_base, alpha, scales["density"]
            )
            curvature_response = normalized_response(
                curvature_base, alpha, scales["curvature"]
            )
            composition_response = normalized_response(
                composition_base, alpha, scales["composition"]
            )
            margin_response = normalized_response(
                margin_base, alpha, scales["margin"]
            )

            # Cosmological first-pass weighting.
            # Expansion-gap and density response dominate; curvature and
            # composition encode regime change; the provisional margin is
            # deliberately assigned the smallest weight.
            structural_response = (
                0.30 * gap_response
                + 0.25 * density_response
                + 0.20 * curvature_response
                + 0.15 * composition_response
                + 0.10 * margin_response
            )

            persistence = phase_persistence_score(structural_response)
            instability = instability_from_response(
                structural_response,
                persistence,
                alpha_radius,
            )
            status = "valid" if instability == "no" else "unstable"

            grid_rows.append(
                {
                    "object_id": OBJECT_ID,
                    "object_name": OBJECT_NAME,
                    "domain": DOMAIN,
                    "interval_index": interval["interval_index"],
                    "sample_index_left": interval["sample_index_left"],
                    "sample_index_right": interval["sample_index_right"],
                    "scale_factor_mid": fmt(
                        to_float(interval["scale_factor_mid"])
                    ),
                    "redshift_mid": fmt(
                        to_float(interval["redshift_mid"])
                    ),
                    "cosmological_era": interval["cosmological_era"],
                    "alpha": fmt(alpha),
                    "alpha_radius": fmt(alpha_radius),
                    "gap_lnE_base": fmt(gap_base),
                    "density_logchange_base": fmt(density_base),
                    "curvature_logchange_base": fmt(curvature_base),
                    "composition_shift_base": fmt(composition_base),
                    "margin_change_base": fmt(margin_base),
                    "gap_lnE_alpha": fmt(gap_base * alpha),
                    "density_logchange_alpha": fmt(
                        density_base * alpha
                    ),
                    "curvature_logchange_alpha": fmt(
                        curvature_base * alpha
                    ),
                    "composition_shift_alpha": fmt(
                        composition_base * alpha
                    ),
                    "margin_change_alpha": fmt(margin_base * alpha),
                    "gap_response_norm": fmt(gap_response),
                    "density_response_norm": fmt(density_response),
                    "curvature_response_norm": fmt(
                        curvature_response
                    ),
                    "composition_response_norm": fmt(
                        composition_response
                    ),
                    "margin_response_norm": fmt(margin_response),
                    "structural_response": fmt(structural_response),
                    "phase_persistence_score": fmt(persistence),
                    "alpha_status": status,
                    "instability_flag": instability,
                }
            )

    return grid_rows


def compute_vector(
    grid_rows: Sequence[Dict[str, object]],
    base_intervals: Sequence[Dict[str, object]],
    alphas: Sequence[float],
) -> Dict[str, object]:
    gap_responses = [
        to_float(row.get("gap_response_norm")) for row in grid_rows
    ]
    valid_rows = [
        row for row in grid_rows if row.get("alpha_status") == "valid"
    ]
    instability_rows = [
        row
        for row in grid_rows
        if row.get("instability_flag") == "yes"
    ]

    mean_gr = safe_mean(gap_responses)
    var_gr = safe_variance(gap_responses)

    # Cosmological anisotropy: variance of mean structural response across
    # radiation-, matter-, and lambda-dominated interval groups.
    grouped: Dict[str, List[float]] = defaultdict(list)
    for row in grid_rows:
        grouped[str(row.get("cosmological_era", "unknown"))].append(
            to_float(row.get("structural_response"))
        )
    era_means = [safe_mean(values) for values in grouped.values()]
    anisotropic_persistence = safe_variance(era_means)

    admissibility_persistence = (
        len(valid_rows) / len(grid_rows) if grid_rows else 0.0
    )

    if instability_rows:
        collapse_onset_radius = min(
            to_float(row.get("alpha_radius"))
            for row in instability_rows
        )
        collapse_observed = "yes"
    else:
        collapse_onset_radius = max(
            (
                to_float(row.get("alpha_radius"))
                for row in grid_rows
            ),
            default=0.0,
        )
        collapse_observed = "no"

    notes = (
        "first-pass Dataset C cosmological alpha vector; "
        "mean_GR and var_GR use normalized ln(E)-gap response; "
        "anisotropic_persistence is variance of mean structural response "
        "across radiation-, matter-, and lambda-dominated intervals; "
        "boundary-margin channel is provisional and has weight 0.10; "
        "collapse_onset_radius records maximum tested radius when "
        "collapse_observed=no"
    )

    return {
        "object_id": OBJECT_ID,
        "object_name": OBJECT_NAME,
        "domain": DOMAIN,
        "mean_GR": fmt(mean_gr),
        "var_GR": fmt(var_gr),
        "anisotropic_persistence": fmt(anisotropic_persistence),
        "admissibility_persistence": fmt(admissibility_persistence),
        "collapse_onset_radius": fmt(collapse_onset_radius),
        "collapse_observed": collapse_observed,
        "kappa_connect_reference": fmt(KAPPA_CONNECT_REFERENCE),
        "tail_dominance_reference": fmt(TAIL_DOMINANCE_REFERENCE),
        "n_base_intervals": len(base_intervals),
        "n_grid_rows": len(grid_rows),
        "n_valid_rows": len(valid_rows),
        "n_instability_rows": len(instability_rows),
        "alpha_min": fmt(min(alphas)),
        "alpha_max": fmt(max(alphas)),
        "alpha_points": len(alphas),
        "notes": notes,
    }


def compute_normalization_review(
    grid_rows: Sequence[Dict[str, object]],
    vector: Dict[str, object],
) -> Dict[str, object]:
    channel_means = {
        "gap": safe_mean(
            to_float(row.get("gap_response_norm")) for row in grid_rows
        ),
        "density": safe_mean(
            to_float(row.get("density_response_norm"))
            for row in grid_rows
        ),
        "curvature": safe_mean(
            to_float(row.get("curvature_response_norm"))
            for row in grid_rows
        ),
        "composition": safe_mean(
            to_float(row.get("composition_response_norm"))
            for row in grid_rows
        ),
        "margin": safe_mean(
            to_float(row.get("margin_response_norm"))
            for row in grid_rows
        ),
    }

    gap_mean = max(channel_means["gap"], 1e-12)
    ratios = {
        "density": channel_means["density"] / gap_mean,
        "curvature": channel_means["curvature"] / gap_mean,
        "composition": channel_means["composition"] / gap_mean,
        "margin": channel_means["margin"] / gap_mean,
    }
    max_channel = max(channel_means, key=channel_means.get)
    maximum_ratio = max(ratios.values(), default=0.0)

    anisotropy = to_float(vector["anisotropic_persistence"])
    scale_review_needed = (
        maximum_ratio >= 10.0 or anisotropy >= 100.0
    )
    review_status = (
        "review_required" if scale_review_needed else "comparable"
    )

    notes = (
        "channel-to-gap ratios are diagnostic only; "
        "bounded anisotropy uses x/(1+x); "
        "margin response remains provisional"
    )

    return {
        "object_id": OBJECT_ID,
        "object_name": OBJECT_NAME,
        "n_grid_rows": len(grid_rows),
        "mean_gap_response": fmt(channel_means["gap"]),
        "mean_density_response": fmt(channel_means["density"]),
        "mean_curvature_response": fmt(channel_means["curvature"]),
        "mean_composition_response": fmt(
            channel_means["composition"]
        ),
        "mean_margin_response": fmt(channel_means["margin"]),
        "max_channel": max_channel,
        "density_to_gap_ratio": fmt(ratios["density"]),
        "curvature_to_gap_ratio": fmt(ratios["curvature"]),
        "composition_to_gap_ratio": fmt(ratios["composition"]),
        "margin_to_gap_ratio": fmt(ratios["margin"]),
        "anisotropic_persistence_v1": fmt(anisotropy),
        "anisotropic_persistence_bounded": fmt(
            bounded(anisotropy)
        ),
        "admissibility_persistence": vector[
            "admissibility_persistence"
        ],
        "collapse_onset_radius": vector["collapse_onset_radius"],
        "collapse_observed": vector["collapse_observed"],
        "scale_review_needed": "yes" if scale_review_needed else "no",
        "review_status": review_status,
        "notes": notes,
    }


def build_summary(
    input_path: Path,
    grid_path: Path,
    vector_path: Path,
    review_path: Path,
    trajectory_rows: Sequence[Dict[str, str]],
    base_intervals: Sequence[Dict[str, object]],
    grid_rows: Sequence[Dict[str, object]],
    alphas: Sequence[float],
    vector: Dict[str, object],
) -> Dict[str, object]:
    valid_rows = [
        row for row in grid_rows if row.get("alpha_status") == "valid"
    ]
    valid_fraction = (
        len(valid_rows) / len(grid_rows) if grid_rows else 0.0
    )

    return {
        "object_id": OBJECT_ID,
        "object_name": OBJECT_NAME,
        "input_file": str(input_path),
        "grid_file": str(grid_path),
        "vector_file": str(vector_path),
        "review_file": str(review_path),
        "trajectory_rows": len(trajectory_rows),
        "base_intervals": len(base_intervals),
        "grid_rows": len(grid_rows),
        "alpha_min": fmt(min(alphas)),
        "alpha_max": fmt(max(alphas)),
        "alpha_points": len(alphas),
        "valid_fraction": fmt(valid_fraction),
        "collapse_observed": vector["collapse_observed"],
        "collapse_onset_radius": vector[
            "collapse_onset_radius"
        ],
        "status": "complete",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Apply the established alpha-grid workflow to the validated "
            "Dataset C Planck-Lambda-CDM trajectory."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Validated Planck-Lambda-CDM trajectory CSV.",
    )
    parser.add_argument(
        "--grid-output",
        type=Path,
        default=DEFAULT_GRID,
        help="Alpha-grid CSV output.",
    )
    parser.add_argument(
        "--vector-output",
        type=Path,
        default=DEFAULT_VECTOR,
        help="5D vector CSV output.",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=DEFAULT_SUMMARY,
        help="Run-summary CSV output.",
    )
    parser.add_argument(
        "--review-output",
        type=Path,
        default=DEFAULT_REVIEW,
        help="Normalization-review CSV output.",
    )
    parser.add_argument(
        "--alpha-min",
        type=float,
        default=0.5,
    )
    parser.add_argument(
        "--alpha-max",
        type=float,
        default=1.5,
    )
    parser.add_argument(
        "--alpha-points",
        type=int,
        default=21,
    )
    args = parser.parse_args()

    input_path = args.input.resolve()
    grid_path = args.grid_output.resolve()
    vector_path = args.vector_output.resolve()
    summary_path = args.summary_output.resolve()
    review_path = args.review_output.resolve()

    if not input_path.is_file():
        raise FileNotFoundError(
            f"Validated trajectory not found: {input_path}"
        )

    trajectory_rows = read_csv(input_path)
    require_columns(trajectory_rows, input_path)

    alphas = make_alpha_values(
        args.alpha_min,
        args.alpha_max,
        args.alpha_points,
    )
    base_intervals = build_base_intervals(trajectory_rows)
    grid_rows = build_grid_rows(base_intervals, alphas)
    vector = compute_vector(grid_rows, base_intervals, alphas)
    review = compute_normalization_review(grid_rows, vector)
    summary = build_summary(
        input_path,
        grid_path,
        vector_path,
        review_path,
        trajectory_rows,
        base_intervals,
        grid_rows,
        alphas,
        vector,
    )

    write_csv(grid_path, grid_rows, GRID_COLUMNS)
    write_csv(vector_path, [vector], VECTOR_COLUMNS)
    write_csv(summary_path, [summary], SUMMARY_COLUMNS)
    write_csv(review_path, [review], REVIEW_COLUMNS)

    print(f"Created alpha grid: {grid_path}")
    print(f"Created 5D vector: {vector_path}")
    print(f"Created summary: {summary_path}")
    print(f"Created normalization review: {review_path}")
    print(f"Trajectory rows: {len(trajectory_rows)}")
    print(f"Base intervals: {len(base_intervals)}")
    print(f"Alpha points: {len(alphas)}")
    print(f"Grid rows: {len(grid_rows)}")
    print(
        "Admissibility persistence: "
        f"{vector['admissibility_persistence']}"
    )
    print(f"Collapse observed: {vector['collapse_observed']}")
    print(
        "Collapse onset radius: "
        f"{vector['collapse_onset_radius']}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
