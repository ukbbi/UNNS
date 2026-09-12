#!/usr/bin/env python3
"""
b_lqc_bounce_alpha_apply_v2_2.py

Dataset B alpha-application / deformation-grid constructor for the validated
effective LQC contraction-bounce-expansion trajectory.

This script uses the full direction-preserving bounce path, not the
expansion-only scalar ladder.

Input:
    ../../ladder/lqc_bounce_response_path_preliminary.csv

Outputs:
    ../grids/B_LQC_BOUNCE_alpha_grid_v2_2.csv
    ../vectors/B_LQC_BOUNCE_5d_vector_v2_2.csv
    ../summaries/B_ALPHA_APPLICATION_SUMMARY_v2_2.csv
    ../normalization_review/B_ALPHA_NORMALIZATION_REVIEW_v2_2.csv

Active-channel convention:
    bounce-safe signed-flow gap response   0.35
    total-density response                 0.30
    curvature response                     0.20
    composition response                   0.15

The provisional margin channel is diagnostic-only.

Bounce-safe response coordinate:
    q_B = asinh(H_signed / H0)

This coordinate is finite and continuous through H = 0, preserves contraction
versus expansion sign, and avoids replacing the exact bounce with an arbitrary
epsilon.

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


SCRIPT_VERSION = "2.2.0"
OBJECT_ID = "B_LQC_BOUNCE_V2"
OBJECT_NAME = "Effective LQC contraction-bounce-expansion"
DOMAIN = "lqc-bounce-full-path"
SCALE_QUANTILE = 0.90
RESPONSE_CAP = 5.0

HERE = Path(__file__).resolve().parent
ALPHA_ROOT = HERE.parent

DEFAULT_INPUT = (
    HERE
    / ".."
    / ".."
    / "ladder"
    / "lqc_bounce_response_path_preliminary.csv"
)

DEFAULT_GRID = (
    ALPHA_ROOT / "grids" / "B_LQC_BOUNCE_alpha_grid_v2_2.csv"
)
DEFAULT_VECTOR = (
    ALPHA_ROOT / "vectors" / "B_LQC_BOUNCE_5d_vector_v2_2.csv"
)
DEFAULT_SUMMARY = (
    ALPHA_ROOT / "summaries" / "B_ALPHA_APPLICATION_SUMMARY_v2_2.csv"
)
DEFAULT_REVIEW = (
    ALPHA_ROOT
    / "normalization_review"
    / "B_ALPHA_NORMALIZATION_REVIEW_v2_2.csv"
)

GRID_COLUMNS = [
    "object_id",
    "object_name",
    "domain",
    "interval_index",
    "sample_index_left",
    "sample_index_right",
    "branch_left",
    "branch_right",
    "crosses_bounce",
    "normalization_region",
    "time_mid_Gyr",
    "scale_factor_mid",
    "rho_over_rho_c_mid",
    "alpha",
    "alpha_radius",
    "signed_flow_gap_base",
    "density_logchange_base",
    "curvature_logchange_base",
    "composition_shift_base",
    "margin_change_base",
    "signed_flow_gap_alpha",
    "density_logchange_alpha",
    "curvature_logchange_alpha",
    "composition_shift_alpha",
    "margin_change_alpha",
    "signed_flow_response_norm",
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
    "n_base_intervals",
    "n_grid_rows",
    "n_valid_rows",
    "n_instability_rows",
    "n_bounce_crossing_rows",
    "alpha_min",
    "alpha_max",
    "alpha_points",
    "scale_quantile",
    "response_cap",
    "script_version",
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
    "bounce_crossing_intervals",
    "alpha_min",
    "alpha_max",
    "alpha_points",
    "valid_fraction",
    "collapse_observed",
    "collapse_onset_radius",
    "scale_quantile",
    "response_cap",
    "script_version",
    "status",
]

REVIEW_COLUMNS = [
    "object_id",
    "object_name",
    "n_grid_rows",
    "mean_signed_flow_response",
    "mean_density_response",
    "mean_curvature_response",
    "mean_composition_response",
    "mean_margin_response",
    "max_active_channel",
    "density_to_flow_ratio",
    "curvature_to_flow_ratio",
    "composition_to_flow_ratio",
    "margin_to_flow_ratio",
    "contraction_outer_flow_scale",
    "contraction_outer_density_scale",
    "contraction_outer_curvature_scale",
    "contraction_outer_composition_scale",
    "contraction_outer_margin_scale",
    "contraction_near_bounce_flow_scale",
    "contraction_near_bounce_density_scale",
    "contraction_near_bounce_curvature_scale",
    "contraction_near_bounce_composition_scale",
    "contraction_near_bounce_margin_scale",
    "bounce_crossing_flow_scale",
    "bounce_crossing_density_scale",
    "bounce_crossing_curvature_scale",
    "bounce_crossing_composition_scale",
    "bounce_crossing_margin_scale",
    "expansion_near_bounce_flow_scale",
    "expansion_near_bounce_density_scale",
    "expansion_near_bounce_curvature_scale",
    "expansion_near_bounce_composition_scale",
    "expansion_near_bounce_margin_scale",
    "expansion_outer_flow_scale",
    "expansion_outer_density_scale",
    "expansion_outer_curvature_scale",
    "expansion_outer_composition_scale",
    "expansion_outer_margin_scale",
    "anisotropic_persistence_v1",
    "anisotropic_persistence_bounded",
    "admissibility_persistence",
    "collapse_onset_radius",
    "collapse_observed",
    "active_scale_review_needed",
    "margin_diagnostic_warning",
    "review_status",
    "scale_quantile",
    "response_cap",
    "script_version",
    "notes",
]


def to_float(value: object, default: float = 0.0) -> float:
    try:
        if value is None or str(value).strip() == "":
            return default
        result = float(str(value).strip())
        return result if math.isfinite(result) else default
    except (TypeError, ValueError):
        return default


def fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def safe_mean(values: Iterable[float]) -> float:
    valid = [v for v in values if math.isfinite(v)]
    return statistics.fmean(valid) if valid else 0.0


def safe_variance(values: Iterable[float]) -> float:
    valid = [v for v in values if math.isfinite(v)]
    return statistics.pvariance(valid) if len(valid) >= 2 else 0.0


def quantile_scale(
    values: Iterable[float],
    quantile: float = SCALE_QUANTILE,
) -> float:
    valid = sorted(abs(v) for v in values if math.isfinite(v))
    if not valid:
        return 1.0

    if not (0.0 <= quantile <= 1.0):
        raise ValueError("quantile must lie in [0,1].")

    if len(valid) == 1:
        value = valid[0]
    else:
        position = quantile * (len(valid) - 1)
        lower = int(math.floor(position))
        upper = int(math.ceil(position))
        if lower == upper:
            value = valid[lower]
        else:
            fraction = position - lower
            value = (
                valid[lower] * (1.0 - fraction)
                + valid[upper] * fraction
            )

    if value > 0.0:
        return value

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
        raise ValueError("alpha_max must be >= alpha_min.")
    step = (alpha_max - alpha_min) / (alpha_points - 1)
    return [alpha_min + i * step for i in range(alpha_points)]


def normalized_response(
    base: float,
    alpha: float,
    scale: float,
    response_cap: float = RESPONSE_CAP,
) -> float:
    if scale <= 0.0:
        return 0.0
    raw = abs(base * (alpha - 1.0)) / scale
    return min(raw, response_cap)


def phase_persistence_score(response: float) -> float:
    return 1.0 / (1.0 + response)


def instability_from_response(
    response: float,
    persistence: float,
    alpha_radius: float,
) -> str:
    if response >= 2.0 and persistence <= 0.333:
        return "yes"
    if (
        alpha_radius >= 0.45
        and response >= 1.5
        and persistence <= 0.4
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
        raise ValueError(f"No path rows found in {path}")

    required = {
        "path_index",
        "source_sample_index",
        "branch",
        "time_relative_to_bounce_Gyr",
        "scale_factor",
        "H_signed_km_s_Mpc",
        "rho_total_relative_to_rho_crit0",
        "rho_over_rho_c",
        "fraction_matter_at_a",
        "fraction_radiation_at_a",
        "fraction_lambda_at_a",
        "effective_ricci_over_6H0sq",
        "boundary_margin_candidate",
        "is_exact_bounce",
    }
    missing = sorted(required - set(rows[0].keys()))
    if missing:
        raise ValueError(
            "Bounce path is missing required column(s): "
            + ", ".join(missing)
        )


def infer_h0(rows: Sequence[Dict[str, str]]) -> float:
    """
    Infer H0 from the outermost expansion endpoint where a is largest.
    For the validated trajectory at a=1, E_lqc is effectively 1.
    """
    candidates = [
        row for row in rows
        if row.get("branch") == "expansion"
    ]
    if not candidates:
        raise ValueError("No expansion branch rows found.")

    outer = max(candidates, key=lambda r: to_float(r.get("scale_factor")))
    h0 = abs(to_float(outer.get("H_signed_km_s_Mpc")))
    if h0 <= 0.0:
        raise ValueError("Could not infer positive H0 from outer endpoint.")
    return h0



def classify_region(
    left: Dict[str, str],
    right: Dict[str, str],
    crosses_bounce: bool,
    near_bounce_threshold: float = 0.01,
) -> str:
    if crosses_bounce:
        return "bounce_crossing"

    branch = (left.get("branch") or "").strip()
    rho_mid = 0.5 * (
        to_float(left.get("rho_over_rho_c"))
        + to_float(right.get("rho_over_rho_c"))
    )
    near = rho_mid >= near_bounce_threshold

    if branch == "contraction":
        return "contraction_near_bounce" if near else "contraction_outer"
    if branch == "expansion":
        return "expansion_near_bounce" if near else "expansion_outer"
    return "bounce_crossing"


def build_base_intervals(
    rows: Sequence[Dict[str, str]],
    h0: float,
) -> List[Dict[str, object]]:
    intervals: List[Dict[str, object]] = []

    for index in range(len(rows) - 1):
        left = rows[index]
        right = rows[index + 1]

        h_left = to_float(left.get("H_signed_km_s_Mpc"))
        h_right = to_float(right.get("H_signed_km_s_Mpc"))

        q_left = math.asinh(h_left / h0)
        q_right = math.asinh(h_right / h0)

        rho_left = max(
            to_float(left.get("rho_total_relative_to_rho_crit0")),
            1.0e-300,
        )
        rho_right = max(
            to_float(right.get("rho_total_relative_to_rho_crit0")),
            1.0e-300,
        )

        curvature_left = to_float(
            left.get("effective_ricci_over_6H0sq")
        )
        curvature_right = to_float(
            right.get("effective_ricci_over_6H0sq")
        )

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
                (r - l) ** 2
                for l, r in zip(fractions_left, fractions_right)
            )
        )

        margin_left = to_float(left.get("boundary_margin_candidate"))
        margin_right = to_float(right.get("boundary_margin_candidate"))

        branch_left = (left.get("branch") or "").strip()
        branch_right = (right.get("branch") or "").strip()
        crosses_bounce = (
            (left.get("is_exact_bounce") or "").strip().lower() == "yes"
            or (right.get("is_exact_bounce") or "").strip().lower() == "yes"
            or branch_left != branch_right
        )

        normalization_region = classify_region(left, right, crosses_bounce)

        intervals.append(
            {
                "interval_index": index,
                "sample_index_left": left.get("source_sample_index", index),
                "sample_index_right": right.get(
                    "source_sample_index", index + 1
                ),
                "branch_left": branch_left,
                "branch_right": branch_right,
                "crosses_bounce": "yes" if crosses_bounce else "no",
                "normalization_region": normalization_region,
                "time_mid_Gyr": 0.5 * (
                    to_float(left.get("time_relative_to_bounce_Gyr"))
                    + to_float(right.get("time_relative_to_bounce_Gyr"))
                ),
                "scale_factor_mid": math.sqrt(
                    max(
                        to_float(left.get("scale_factor"))
                        * to_float(right.get("scale_factor")),
                        0.0,
                    )
                ),
                "rho_over_rho_c_mid": 0.5 * (
                    to_float(left.get("rho_over_rho_c"))
                    + to_float(right.get("rho_over_rho_c"))
                ),
                "signed_flow_gap_base": abs(q_right - q_left),
                "density_logchange_base": abs(
                    math.log(rho_right) - math.log(rho_left)
                ),
                "curvature_logchange_base": abs(
                    math.log1p(abs(curvature_right))
                    - math.log1p(abs(curvature_left))
                ),
                "composition_shift_base": composition_shift,
                "margin_change_base": abs(margin_right - margin_left),
            }
        )

    if not intervals:
        raise ValueError("At least two path rows are required.")
    return intervals



def build_region_scales(
    intervals: Sequence[Dict[str, object]],
) -> Dict[str, Dict[str, float]]:
    regions = (
        "contraction_outer",
        "contraction_near_bounce",
        "bounce_crossing",
        "expansion_near_bounce",
        "expansion_outer",
    )
    scales: Dict[str, Dict[str, float]] = {}

    for region in regions:
        rows = [
            r for r in intervals
            if r["normalization_region"] == region
        ]
        if not rows:
            raise ValueError(
                f"No intervals for normalization region: {region}"
            )

        # Version 2.2:
        # - ordinary regions use Q90 empirical scales;
        # - the two bounce-crossing intervals use their own local scales.
        # This preserves the turning-point event without measuring it in
        # thousands of near-bounce interval units.
        scales[region] = {
            "flow": quantile_scale(
                to_float(r["signed_flow_gap_base"]) for r in rows
            ),
            "density": quantile_scale(
                to_float(r["density_logchange_base"]) for r in rows
            ),
            "curvature": quantile_scale(
                to_float(r["curvature_logchange_base"]) for r in rows
            ),
            "composition": quantile_scale(
                to_float(r["composition_shift_base"]) for r in rows
            ),
            "margin": quantile_scale(
                to_float(r["margin_change_base"]) for r in rows
            ),
        }

    return scales


def build_grid_rows(
    intervals: Sequence[Dict[str, object]],
    alphas: Sequence[float],
) -> tuple[List[Dict[str, object]], Dict[str, Dict[str, float]]]:
    region_scales = build_region_scales(intervals)
    grid: List[Dict[str, object]] = []

    for interval in intervals:
        region = str(interval["normalization_region"])
        scales = region_scales[region]

        flow_base = to_float(interval["signed_flow_gap_base"])
        density_base = to_float(interval["density_logchange_base"])
        curvature_base = to_float(interval["curvature_logchange_base"])
        composition_base = to_float(interval["composition_shift_base"])
        margin_base = to_float(interval["margin_change_base"])

        for alpha in alphas:
            radius = abs(alpha - 1.0)
            flow_response = normalized_response(flow_base, alpha, scales["flow"])
            density_response = normalized_response(density_base, alpha, scales["density"])
            curvature_response = normalized_response(curvature_base, alpha, scales["curvature"])
            composition_response = normalized_response(composition_base, alpha, scales["composition"])
            margin_response = normalized_response(margin_base, alpha, scales["margin"])

            response = (
                0.35 * flow_response
                + 0.30 * density_response
                + 0.20 * curvature_response
                + 0.15 * composition_response
            )
            persistence = phase_persistence_score(response)
            instability = instability_from_response(response, persistence, radius)

            grid.append({
                "object_id": OBJECT_ID,
                "object_name": OBJECT_NAME,
                "domain": DOMAIN,
                "interval_index": interval["interval_index"],
                "sample_index_left": interval["sample_index_left"],
                "sample_index_right": interval["sample_index_right"],
                "branch_left": interval["branch_left"],
                "branch_right": interval["branch_right"],
                "crosses_bounce": interval["crosses_bounce"],
                "normalization_region": region,
                "time_mid_Gyr": fmt(to_float(interval["time_mid_Gyr"])),
                "scale_factor_mid": fmt(to_float(interval["scale_factor_mid"])),
                "rho_over_rho_c_mid": fmt(to_float(interval["rho_over_rho_c_mid"])),
                "alpha": fmt(alpha),
                "alpha_radius": fmt(radius),
                "signed_flow_gap_base": fmt(flow_base),
                "density_logchange_base": fmt(density_base),
                "curvature_logchange_base": fmt(curvature_base),
                "composition_shift_base": fmt(composition_base),
                "margin_change_base": fmt(margin_base),
                "signed_flow_gap_alpha": fmt(flow_base * alpha),
                "density_logchange_alpha": fmt(density_base * alpha),
                "curvature_logchange_alpha": fmt(curvature_base * alpha),
                "composition_shift_alpha": fmt(composition_base * alpha),
                "margin_change_alpha": fmt(margin_base * alpha),
                "signed_flow_response_norm": fmt(flow_response),
                "density_response_norm": fmt(density_response),
                "curvature_response_norm": fmt(curvature_response),
                "composition_response_norm": fmt(composition_response),
                "margin_response_norm": fmt(margin_response),
                "structural_response": fmt(response),
                "phase_persistence_score": fmt(persistence),
                "alpha_status": "valid" if instability == "no" else "unstable",
                "instability_flag": instability,
            })
    return grid, region_scales


def compute_vector(
    grid_rows: Sequence[Dict[str, object]],
    intervals: Sequence[Dict[str, object]],
    alphas: Sequence[float],
) -> Dict[str, object]:
    flow_responses = [
        to_float(r.get("signed_flow_response_norm"))
        for r in grid_rows
    ]
    valid = [r for r in grid_rows if r["alpha_status"] == "valid"]
    unstable = [
        r for r in grid_rows if r["instability_flag"] == "yes"
    ]
    bounce_rows = [
        r for r in grid_rows if r["crosses_bounce"] == "yes"
    ]

    grouped: Dict[str, List[float]] = defaultdict(list)
    for row in grid_rows:
        left = str(row.get("branch_left", ""))
        right = str(row.get("branch_right", ""))
        key = "bounce" if row["crosses_bounce"] == "yes" else left or right
        grouped[key].append(to_float(row.get("structural_response")))

    group_means = [safe_mean(v) for v in grouped.values()]
    anisotropy = safe_variance(group_means)

    admissibility = len(valid) / len(grid_rows) if grid_rows else 0.0

    if unstable:
        onset = min(
            to_float(r.get("alpha_radius")) for r in unstable
        )
        collapse_observed = "yes"
    else:
        onset = max(
            (to_float(r.get("alpha_radius")) for r in grid_rows),
            default=0.0,
        )
        collapse_observed = "no"

    notes = (
        "Dataset B full-path alpha vector with five-region Q90 normalization, dedicated bounce-crossing scales, and response cap 5; bounce-safe signed-flow coordinate "
        "q_B=asinh(H_signed/H0); active weights flow=0.35, density=0.30, "
        "curvature=0.20, composition=0.15; margin diagnostic-only; "
        "anisotropic_persistence is variance across contraction, bounce, "
        "and expansion response groups"
    )

    return {
        "object_id": OBJECT_ID,
        "object_name": OBJECT_NAME,
        "domain": DOMAIN,
        "mean_GR": fmt(safe_mean(flow_responses)),
        "var_GR": fmt(safe_variance(flow_responses)),
        "anisotropic_persistence": fmt(anisotropy),
        "admissibility_persistence": fmt(admissibility),
        "collapse_onset_radius": fmt(onset),
        "collapse_observed": collapse_observed,
        "n_base_intervals": len(intervals),
        "n_grid_rows": len(grid_rows),
        "n_valid_rows": len(valid),
        "n_instability_rows": len(unstable),
        "n_bounce_crossing_rows": len(bounce_rows),
        "alpha_min": fmt(min(alphas)),
        "alpha_max": fmt(max(alphas)),
        "alpha_points": len(alphas),
        "scale_quantile": fmt(SCALE_QUANTILE),
        "response_cap": fmt(RESPONSE_CAP),
        "script_version": SCRIPT_VERSION,
        "notes": notes,
    }


def compute_review(
    grid_rows: Sequence[Dict[str, object]],
    vector: Dict[str, object],
    region_scales: Dict[str, Dict[str, float]],
) -> Dict[str, object]:
    means = {
        "flow": safe_mean(
            to_float(r.get("signed_flow_response_norm"))
            for r in grid_rows
        ),
        "density": safe_mean(
            to_float(r.get("density_response_norm")) for r in grid_rows
        ),
        "curvature": safe_mean(
            to_float(r.get("curvature_response_norm")) for r in grid_rows
        ),
        "composition": safe_mean(
            to_float(r.get("composition_response_norm")) for r in grid_rows
        ),
        "margin": safe_mean(
            to_float(r.get("margin_response_norm")) for r in grid_rows
        ),
    }

    flow = max(means["flow"], 1.0e-12)
    ratios = {
        "density": means["density"] / flow,
        "curvature": means["curvature"] / flow,
        "composition": means["composition"] / flow,
        "margin": means["margin"] / flow,
    }

    active_ratios = {
        k: ratios[k] for k in ("density", "curvature", "composition")
    }
    anisotropy = to_float(vector["anisotropic_persistence"])

    active_review = (
        max(active_ratios.values(), default=0.0) >= 10.0
        or anisotropy >= 100.0
    )
    margin_warning = ratios["margin"] >= 10.0

    return {
        "object_id": OBJECT_ID,
        "object_name": OBJECT_NAME,
        "n_grid_rows": len(grid_rows),
        "mean_signed_flow_response": fmt(means["flow"]),
        "mean_density_response": fmt(means["density"]),
        "mean_curvature_response": fmt(means["curvature"]),
        "mean_composition_response": fmt(means["composition"]),
        "mean_margin_response": fmt(means["margin"]),
        "max_active_channel": max(
            ("flow", "density", "curvature", "composition"),
            key=lambda k: means[k],
        ),
        "density_to_flow_ratio": fmt(ratios["density"]),
        "curvature_to_flow_ratio": fmt(ratios["curvature"]),
        "composition_to_flow_ratio": fmt(ratios["composition"]),
        "margin_to_flow_ratio": fmt(ratios["margin"]),

        "contraction_outer_flow_scale": fmt(region_scales["contraction_outer"]["flow"]),
        "contraction_outer_density_scale": fmt(region_scales["contraction_outer"]["density"]),
        "contraction_outer_curvature_scale": fmt(region_scales["contraction_outer"]["curvature"]),
        "contraction_outer_composition_scale": fmt(region_scales["contraction_outer"]["composition"]),
        "contraction_outer_margin_scale": fmt(region_scales["contraction_outer"]["margin"]),
        "contraction_near_bounce_flow_scale": fmt(region_scales["contraction_near_bounce"]["flow"]),
        "contraction_near_bounce_density_scale": fmt(region_scales["contraction_near_bounce"]["density"]),
        "contraction_near_bounce_curvature_scale": fmt(region_scales["contraction_near_bounce"]["curvature"]),
        "contraction_near_bounce_composition_scale": fmt(region_scales["contraction_near_bounce"]["composition"]),
        "contraction_near_bounce_margin_scale": fmt(region_scales["contraction_near_bounce"]["margin"]),
        "bounce_crossing_flow_scale": fmt(region_scales["bounce_crossing"]["flow"]),
        "bounce_crossing_density_scale": fmt(region_scales["bounce_crossing"]["density"]),
        "bounce_crossing_curvature_scale": fmt(region_scales["bounce_crossing"]["curvature"]),
        "bounce_crossing_composition_scale": fmt(region_scales["bounce_crossing"]["composition"]),
        "bounce_crossing_margin_scale": fmt(region_scales["bounce_crossing"]["margin"]),
        "expansion_near_bounce_flow_scale": fmt(region_scales["expansion_near_bounce"]["flow"]),
        "expansion_near_bounce_density_scale": fmt(region_scales["expansion_near_bounce"]["density"]),
        "expansion_near_bounce_curvature_scale": fmt(region_scales["expansion_near_bounce"]["curvature"]),
        "expansion_near_bounce_composition_scale": fmt(region_scales["expansion_near_bounce"]["composition"]),
        "expansion_near_bounce_margin_scale": fmt(region_scales["expansion_near_bounce"]["margin"]),
        "expansion_outer_flow_scale": fmt(region_scales["expansion_outer"]["flow"]),
        "expansion_outer_density_scale": fmt(region_scales["expansion_outer"]["density"]),
        "expansion_outer_curvature_scale": fmt(region_scales["expansion_outer"]["curvature"]),
        "expansion_outer_composition_scale": fmt(region_scales["expansion_outer"]["composition"]),
        "expansion_outer_margin_scale": fmt(region_scales["expansion_outer"]["margin"]),
        "anisotropic_persistence_v1": fmt(anisotropy),
        "anisotropic_persistence_bounded": fmt(bounded(anisotropy)),
        "admissibility_persistence": vector[
            "admissibility_persistence"
        ],
        "collapse_onset_radius": vector["collapse_onset_radius"],
        "collapse_observed": vector["collapse_observed"],
        "active_scale_review_needed": "yes" if active_review else "no",
        "margin_diagnostic_warning": "yes" if margin_warning else "no",
        "review_status": (
            "review_required"
            if active_review
            else "comparable_active_channels"
        ),
        "scale_quantile": fmt(SCALE_QUANTILE),
        "response_cap": fmt(RESPONSE_CAP),
        "script_version": SCRIPT_VERSION,
        "notes": (
            "Version 2 Dataset B review; active channels only can reject the "
            "vector; margin remains diagnostic-only."
        ),
    }


def build_summary(
    input_path: Path,
    grid_path: Path,
    vector_path: Path,
    review_path: Path,
    trajectory_rows: Sequence[Dict[str, str]],
    intervals: Sequence[Dict[str, object]],
    grid_rows: Sequence[Dict[str, object]],
    alphas: Sequence[float],
    vector: Dict[str, object],
) -> Dict[str, object]:
    bounce_intervals = sum(
        1 for r in intervals if r["crosses_bounce"] == "yes"
    )
    valid_fraction = (
        sum(1 for r in grid_rows if r["alpha_status"] == "valid")
        / len(grid_rows)
        if grid_rows
        else 0.0
    )

    return {
        "object_id": OBJECT_ID,
        "object_name": OBJECT_NAME,
        "input_file": str(input_path),
        "grid_file": str(grid_path),
        "vector_file": str(vector_path),
        "review_file": str(review_path),
        "trajectory_rows": len(trajectory_rows),
        "base_intervals": len(intervals),
        "grid_rows": len(grid_rows),
        "bounce_crossing_intervals": bounce_intervals,
        "alpha_min": fmt(min(alphas)),
        "alpha_max": fmt(max(alphas)),
        "alpha_points": len(alphas),
        "valid_fraction": fmt(valid_fraction),
        "collapse_observed": vector["collapse_observed"],
        "collapse_onset_radius": vector["collapse_onset_radius"],
        "scale_quantile": fmt(SCALE_QUANTILE),
        "response_cap": fmt(RESPONSE_CAP),
        "script_version": SCRIPT_VERSION,
        "status": "complete_full_bounce_path_bounded_q90",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Apply the v2.2 bounded-Q90 alpha workflow to the full Dataset B LQC bounce path."
        )
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument(
        "--grid-output", type=Path, default=DEFAULT_GRID
    )
    parser.add_argument(
        "--vector-output", type=Path, default=DEFAULT_VECTOR
    )
    parser.add_argument(
        "--summary-output", type=Path, default=DEFAULT_SUMMARY
    )
    parser.add_argument(
        "--review-output", type=Path, default=DEFAULT_REVIEW
    )
    parser.add_argument("--alpha-min", type=float, default=0.5)
    parser.add_argument("--alpha-max", type=float, default=1.5)
    parser.add_argument("--alpha-points", type=int, default=21)
    args = parser.parse_args()

    input_path = args.input.resolve()
    grid_path = args.grid_output.resolve()
    vector_path = args.vector_output.resolve()
    summary_path = args.summary_output.resolve()
    review_path = args.review_output.resolve()

    if not input_path.is_file():
        raise FileNotFoundError(
            f"Dataset B full bounce path not found: {input_path}"
        )

    trajectory_rows = read_csv(input_path)
    require_columns(trajectory_rows, input_path)
    h0 = infer_h0(trajectory_rows)

    alphas = make_alpha_values(
        args.alpha_min,
        args.alpha_max,
        args.alpha_points,
    )
    intervals = build_base_intervals(trajectory_rows, h0)
    grid_rows, region_scales = build_grid_rows(intervals, alphas)
    vector = compute_vector(grid_rows, intervals, alphas)
    review = compute_review(grid_rows, vector, region_scales)
    summary = build_summary(
        input_path,
        grid_path,
        vector_path,
        review_path,
        trajectory_rows,
        intervals,
        grid_rows,
        alphas,
        vector,
    )

    write_csv(grid_path, grid_rows, GRID_COLUMNS)
    write_csv(vector_path, [vector], VECTOR_COLUMNS)
    write_csv(summary_path, [summary], SUMMARY_COLUMNS)
    write_csv(review_path, [review], REVIEW_COLUMNS)

    print(f"Script version: {SCRIPT_VERSION}")
    print(f"Created alpha grid: {grid_path}")
    print(f"Created 5D vector: {vector_path}")
    print(f"Created summary: {summary_path}")
    print(f"Created normalization review: {review_path}")
    print(f"Trajectory rows: {len(trajectory_rows)}")
    print(f"Base intervals: {len(intervals)}")
    print(f"Alpha points: {len(alphas)}")
    print(f"Grid rows: {len(grid_rows)}")
    print(f"Inferred H0: {h0:.12g}")
    print(f"Scale quantile: Q{int(SCALE_QUANTILE * 100)}")
    print(f"Response cap: {RESPONSE_CAP:.12g}")
    print("Region-conditioned scales:")
    for region_name in (
        "contraction_outer",
        "contraction_near_bounce",
        "bounce_crossing",
        "expansion_near_bounce",
        "expansion_outer",
    ):
        s = region_scales[region_name]
        print(
            f"  {region_name}: flow={s['flow']:.12g}, "
            f"density={s['density']:.12g}, "
            f"curvature={s['curvature']:.12g}, "
            f"composition={s['composition']:.12g}, "
            f"margin={s['margin']:.12g}"
        )
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
