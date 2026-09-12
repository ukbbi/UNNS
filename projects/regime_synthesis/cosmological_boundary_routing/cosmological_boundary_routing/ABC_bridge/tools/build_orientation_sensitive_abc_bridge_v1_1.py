#!/usr/bin/env python3
"""
build_orientation_sensitive_abc_bridge_v1_1.py

Construct Bridge v1.1 for the Cosmological Boundary Routing project.

Version 1.1 replaces heterogeneous surface-distance fields with one shared,
dimensionless route coordinate based on cumulative |Delta ln(a)|.

Coordinate convention
---------------------
A: classical contraction
    route_coordinate runs from -1 at the outer starting point to 0 at the
    terminal small-a endpoint.

B: LQC bounce
    contraction branch runs from -1 to 0 at the exact bounce;
    expansion branch runs from 0 to +1.

C: classical expansion
    route_coordinate runs from 0 at the early small-a endpoint to +1 at the
    late outer endpoint.

The bridge also adds normalized signed-flow summaries. Each raw signed flow is
scaled by its dataset-specific Q90 absolute magnitude and mapped to [-1,1]:

    normalized_flow = raw_flow / (Q90(|raw_flow|) + |raw_flow|)

This preserves sign, limits outlier dominance, and supports cross-dataset
comparison without mixing dimensional endpoint scales.

Outputs
-------
../outputs/ABC_orientation_sensitive_bridge_v1_1.csv
../outputs/ABC_orientation_sensitive_bridge_summary_v1_1.csv
../outputs/ABC_orientation_sensitive_bridge_manifest_v1_1.txt

No third-party packages are required.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


SCRIPT_VERSION = "1.1.0"
FLOW_SCALE_QUANTILE = 0.90

HERE = Path(__file__).resolve().parent
BRIDGE_ROOT = HERE.parent

DEFAULT_A_INPUT = (
    BRIDGE_ROOT.parent
    / "A_classical_friedmann"
    / "generated_trajectory"
    / "validated"
    / "classical_friedmann_approach_validated.csv"
)

DEFAULT_B_INPUT = (
    BRIDGE_ROOT.parent
    / "B_lqc_bounce"
    / "canonical"
    / "ladder"
    / "lqc_bounce_response_path_preliminary.csv"
)

DEFAULT_C_INPUT = (
    BRIDGE_ROOT.parent
    / "C_planck_lcdm"
    / "generated_trajectory"
    / "validated"
    / "planck_lcdm_trajectory_validated.csv"
)

DEFAULT_BRIDGE_OUTPUT = (
    BRIDGE_ROOT / "outputs" / "ABC_orientation_sensitive_bridge_v1_1.csv"
)
DEFAULT_SUMMARY_OUTPUT = (
    BRIDGE_ROOT
    / "outputs"
    / "ABC_orientation_sensitive_bridge_summary_v1_1.csv"
)
DEFAULT_MANIFEST_OUTPUT = (
    BRIDGE_ROOT
    / "outputs"
    / "ABC_orientation_sensitive_bridge_manifest_v1_1.txt"
)


BRIDGE_COLUMNS = [
    "dataset_id",
    "dataset_name",
    "interval_index",
    "sample_index_left",
    "sample_index_right",
    "branch_left",
    "branch_right",
    "route_phase",
    "crosses_turning_surface",
    "route_coordinate_left",
    "route_coordinate_right",
    "route_coordinate_mid",
    "signed_route_step",
    "route_direction",
    "time_left",
    "time_right",
    "time_mid",
    "scale_factor_left",
    "scale_factor_right",
    "scale_factor_mid",
    "signed_delta_ln_a",
    "normalized_signed_delta_ln_a",
    "H_signed_left",
    "H_signed_right",
    "signed_H_flow",
    "normalized_signed_H_flow",
    "density_left",
    "density_right",
    "signed_density_flow",
    "normalized_signed_density_flow",
    "curvature_left",
    "curvature_right",
    "signed_curvature_flow",
    "normalized_signed_curvature_flow",
    "margin_left",
    "margin_right",
    "signed_margin_flow",
    "normalized_signed_margin_flow",
    "margin_flow_direction",
    "rho_over_rho_c_left",
    "rho_over_rho_c_right",
    "rho_over_rho_c_mid",
    "x_bounce_distance_left",
    "x_bounce_distance_right",
    "x_bounce_distance_mid",
    "is_exact_bounce_left",
    "is_exact_bounce_right",
]


SUMMARY_COLUMNS = [
    "dataset_id",
    "dataset_name",
    "n_rows",
    "n_intervals",
    "n_turning_crossings",
    "route_coordinate_min",
    "route_coordinate_max",
    "mean_signed_route_step",
    "mean_normalized_signed_delta_ln_a",
    "mean_normalized_signed_H_flow",
    "mean_normalized_signed_density_flow",
    "mean_normalized_signed_curvature_flow",
    "mean_normalized_signed_margin_flow",
    "mean_abs_normalized_delta_ln_a",
    "mean_abs_normalized_H_flow",
    "mean_abs_normalized_density_flow",
    "mean_abs_normalized_curvature_flow",
    "mean_abs_normalized_margin_flow",
    "fraction_margin_decreasing",
    "fraction_margin_increasing",
    "fraction_route_negative",
    "fraction_route_positive",
    "fraction_route_crossing_zero",
    "delta_ln_a_q90_scale",
    "H_flow_q90_scale",
    "density_flow_q90_scale",
    "curvature_flow_q90_scale",
    "margin_flow_q90_scale",
    "route_class",
    "script_version",
]


def to_float(value: object, default: float = 0.0) -> float:
    try:
        if value is None or str(value).strip() == "":
            return default
        result = float(str(value).strip())
        return result if math.isfinite(result) else default
    except (TypeError, ValueError):
        return default


def safe_log(value: float) -> float:
    return math.log(max(value, 1.0e-300))


def safe_mean(values: Iterable[float]) -> float:
    data = [v for v in values if math.isfinite(v)]
    return statistics.fmean(data) if data else 0.0


def fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def quantile(values: Iterable[float], q: float) -> float:
    data = sorted(abs(v) for v in values if math.isfinite(v))
    if not data:
        return 1.0
    if len(data) == 1:
        return data[0] if data[0] > 0 else 1.0

    position = q * (len(data) - 1)
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        result = data[lower]
    else:
        fraction = position - lower
        result = data[lower] * (1.0 - fraction) + data[upper] * fraction

    if result > 0.0:
        return result
    maximum = max(data)
    return maximum if maximum > 0.0 else 1.0


def bounded_signed(value: float, scale: float) -> float:
    denominator = max(scale, 1.0e-300) + abs(value)
    return value / denominator


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


def first_existing(row: Dict[str, str], *names: str) -> str:
    for name in names:
        value = row.get(name)
        if value is not None and str(value).strip() != "":
            return str(value)
    return ""


def normalize_a(rows: Sequence[Dict[str, str]]) -> List[Dict[str, object]]:
    result: List[Dict[str, object]] = []
    for index, row in enumerate(rows):
        result.append(
            {
                "sample_index": first_existing(row, "sample_index") or index,
                "branch": "contraction",
                "time": to_float(
                    first_existing(
                        row,
                        "contraction_elapsed_time_Gyr",
                        "time_relative_to_bounce_Gyr",
                    )
                ),
                "scale_factor": to_float(row.get("scale_factor")),
                "H_signed": to_float(row.get("H_signed_km_s_Mpc")),
                "density": to_float(
                    row.get("rho_total_relative_to_rho_crit0")
                ),
                "curvature": to_float(
                    first_existing(
                        row,
                        "ricci_scalar_over_6H0sq",
                        "effective_ricci_over_6H0sq",
                    )
                ),
                "margin": to_float(row.get("boundary_margin_candidate")),
                "rho_over_rho_c": 0.0,
                "x_bounce_distance": 0.0,
                "is_exact_bounce": "no",
            }
        )
    return result


def normalize_b(rows: Sequence[Dict[str, str]]) -> List[Dict[str, object]]:
    result: List[Dict[str, object]] = []
    for index, row in enumerate(rows):
        result.append(
            {
                "sample_index": first_existing(
                    row, "source_sample_index", "sample_index"
                ) or index,
                "branch": (row.get("branch") or "").strip(),
                "time": to_float(row.get("time_relative_to_bounce_Gyr")),
                "scale_factor": to_float(row.get("scale_factor")),
                "H_signed": to_float(row.get("H_signed_km_s_Mpc")),
                "density": to_float(
                    row.get("rho_total_relative_to_rho_crit0")
                ),
                "curvature": to_float(
                    row.get("effective_ricci_over_6H0sq")
                ),
                "margin": to_float(row.get("boundary_margin_candidate")),
                "rho_over_rho_c": to_float(row.get("rho_over_rho_c")),
                "x_bounce_distance": to_float(
                    row.get("x_bounce_distance")
                ),
                "is_exact_bounce": (
                    row.get("is_exact_bounce") or "no"
                ).strip().lower(),
            }
        )
    return result


def normalize_c(rows: Sequence[Dict[str, str]]) -> List[Dict[str, object]]:
    result: List[Dict[str, object]] = []
    for index, row in enumerate(rows):
        result.append(
            {
                "sample_index": first_existing(row, "sample_index") or index,
                "branch": "expansion",
                "time": to_float(
                    first_existing(
                        row,
                        "cosmic_time_Gyr",
                        "elapsed_time_Gyr",
                        "time_from_start_Gyr",
                    )
                ),
                "scale_factor": to_float(row.get("scale_factor")),
                "H_signed": to_float(
                    first_existing(
                        row,
                        "H_signed_km_s_Mpc",
                        "H_km_s_Mpc",
                        "H_magnitude_km_s_Mpc",
                    )
                ),
                "density": to_float(
                    row.get("rho_total_relative_to_rho_crit0")
                ),
                "curvature": to_float(
                    first_existing(
                        row,
                        "ricci_scalar_over_6H0sq",
                        "effective_ricci_over_6H0sq",
                    )
                ),
                "margin": to_float(row.get("boundary_margin_candidate")),
                "rho_over_rho_c": 0.0,
                "x_bounce_distance": 0.0,
                "is_exact_bounce": "no",
            }
        )
    return result


def cumulative_log_a_arc(rows: Sequence[Dict[str, object]]) -> List[float]:
    cumulative = [0.0]
    for index in range(1, len(rows)):
        left = max(to_float(rows[index - 1]["scale_factor"]), 1.0e-300)
        right = max(to_float(rows[index]["scale_factor"]), 1.0e-300)
        cumulative.append(
            cumulative[-1] + abs(safe_log(right) - safe_log(left))
        )
    return cumulative


def assign_route_coordinate(
    dataset_id: str,
    rows: Sequence[Dict[str, object]],
) -> List[float]:
    if len(rows) < 2:
        raise ValueError(f"Dataset {dataset_id} has fewer than two rows.")

    if dataset_id == "A":
        arc = cumulative_log_a_arc(rows)
        total = arc[-1] or 1.0
        return [-1.0 + value / total for value in arc]

    if dataset_id == "C":
        arc = cumulative_log_a_arc(rows)
        total = arc[-1] or 1.0
        return [value / total for value in arc]

    bounce_indices = [
        i for i, row in enumerate(rows)
        if str(row["is_exact_bounce"]) == "yes"
    ]
    if len(bounce_indices) != 1:
        raise ValueError(
            f"Dataset B requires one exact bounce row, found {len(bounce_indices)}."
        )

    bounce_index = bounce_indices[0]
    contraction_rows = rows[: bounce_index + 1]
    expansion_rows = rows[bounce_index:]

    contraction_arc = cumulative_log_a_arc(contraction_rows)
    contraction_total = contraction_arc[-1] or 1.0
    contraction_coordinates = [
        -1.0 + value / contraction_total
        for value in contraction_arc
    ]

    expansion_arc = cumulative_log_a_arc(expansion_rows)
    expansion_total = expansion_arc[-1] or 1.0
    expansion_coordinates = [
        value / expansion_total
        for value in expansion_arc
    ]

    return contraction_coordinates[:-1] + expansion_coordinates


def infer_route_phase(
    dataset_id: str,
    left: Dict[str, object],
    right: Dict[str, object],
) -> str:
    if dataset_id == "A":
        return "terminal_approach"
    if dataset_id == "C":
        return "boundary_recession"

    if (
        left["is_exact_bounce"] == "yes"
        or right["is_exact_bounce"] == "yes"
        or left["branch"] != right["branch"]
    ):
        return "turning_surface"
    if left["branch"] == "contraction":
        return "pre_bounce_approach"
    return "post_bounce_recession"


def margin_direction(delta: float) -> str:
    tolerance = 1.0e-15
    if delta < -tolerance:
        return "margin_decreasing"
    if delta > tolerance:
        return "margin_increasing"
    return "margin_stationary"


def route_direction(delta: float) -> str:
    tolerance = 1.0e-15
    if delta < -tolerance:
        return "toward_negative_route"
    if delta > tolerance:
        return "toward_positive_route"
    return "route_stationary"


def compute_raw_intervals(
    dataset_id: str,
    dataset_name: str,
    rows: Sequence[Dict[str, object]],
    coordinates: Sequence[float],
) -> List[Dict[str, object]]:
    intervals: List[Dict[str, object]] = []

    for index in range(len(rows) - 1):
        left = rows[index]
        right = rows[index + 1]

        a_left = max(to_float(left["scale_factor"]), 1.0e-300)
        a_right = max(to_float(right["scale_factor"]), 1.0e-300)
        density_left = max(to_float(left["density"]), 1.0e-300)
        density_right = max(to_float(right["density"]), 1.0e-300)
        curvature_left = to_float(left["curvature"])
        curvature_right = to_float(right["curvature"])
        margin_left = to_float(left["margin"])
        margin_right = to_float(right["margin"])

        route_left = coordinates[index]
        route_right = coordinates[index + 1]

        crosses = (
            left["is_exact_bounce"] == "yes"
            or right["is_exact_bounce"] == "yes"
            or left["branch"] != right["branch"]
            or (route_left < 0.0 < route_right)
        )

        intervals.append(
            {
                "dataset_id": dataset_id,
                "dataset_name": dataset_name,
                "interval_index": index,
                "sample_index_left": left["sample_index"],
                "sample_index_right": right["sample_index"],
                "branch_left": left["branch"],
                "branch_right": right["branch"],
                "route_phase": infer_route_phase(
                    dataset_id, left, right
                ),
                "crosses_turning_surface": "yes" if crosses else "no",
                "route_coordinate_left": route_left,
                "route_coordinate_right": route_right,
                "route_coordinate_mid": 0.5 * (route_left + route_right),
                "signed_route_step": route_right - route_left,
                "route_direction": route_direction(route_right - route_left),
                "time_left": to_float(left["time"]),
                "time_right": to_float(right["time"]),
                "time_mid": 0.5 * (
                    to_float(left["time"]) + to_float(right["time"])
                ),
                "scale_factor_left": a_left,
                "scale_factor_right": a_right,
                "scale_factor_mid": math.sqrt(a_left * a_right),
                "signed_delta_ln_a": safe_log(a_right) - safe_log(a_left),
                "H_signed_left": to_float(left["H_signed"]),
                "H_signed_right": to_float(right["H_signed"]),
                "signed_H_flow": (
                    to_float(right["H_signed"])
                    - to_float(left["H_signed"])
                ),
                "density_left": density_left,
                "density_right": density_right,
                "signed_density_flow": (
                    safe_log(density_right) - safe_log(density_left)
                ),
                "curvature_left": curvature_left,
                "curvature_right": curvature_right,
                "signed_curvature_flow": (
                    math.copysign(
                        math.log1p(abs(curvature_right)),
                        curvature_right,
                    )
                    - math.copysign(
                        math.log1p(abs(curvature_left)),
                        curvature_left,
                    )
                ),
                "margin_left": margin_left,
                "margin_right": margin_right,
                "signed_margin_flow": margin_right - margin_left,
                "margin_flow_direction": margin_direction(
                    margin_right - margin_left
                ),
                "rho_over_rho_c_left": to_float(
                    left["rho_over_rho_c"]
                ),
                "rho_over_rho_c_right": to_float(
                    right["rho_over_rho_c"]
                ),
                "rho_over_rho_c_mid": 0.5 * (
                    to_float(left["rho_over_rho_c"])
                    + to_float(right["rho_over_rho_c"])
                ),
                "x_bounce_distance_left": to_float(
                    left["x_bounce_distance"]
                ),
                "x_bounce_distance_right": to_float(
                    right["x_bounce_distance"]
                ),
                "x_bounce_distance_mid": 0.5 * (
                    to_float(left["x_bounce_distance"])
                    + to_float(right["x_bounce_distance"])
                ),
                "is_exact_bounce_left": left["is_exact_bounce"],
                "is_exact_bounce_right": right["is_exact_bounce"],
            }
        )

    return intervals


def flow_scales(
    intervals: Sequence[Dict[str, object]],
) -> Dict[str, float]:
    return {
        "delta_ln_a": quantile(
            (to_float(r["signed_delta_ln_a"]) for r in intervals),
            FLOW_SCALE_QUANTILE,
        ),
        "H": quantile(
            (to_float(r["signed_H_flow"]) for r in intervals),
            FLOW_SCALE_QUANTILE,
        ),
        "density": quantile(
            (to_float(r["signed_density_flow"]) for r in intervals),
            FLOW_SCALE_QUANTILE,
        ),
        "curvature": quantile(
            (to_float(r["signed_curvature_flow"]) for r in intervals),
            FLOW_SCALE_QUANTILE,
        ),
        "margin": quantile(
            (to_float(r["signed_margin_flow"]) for r in intervals),
            FLOW_SCALE_QUANTILE,
        ),
    }


def apply_normalized_flows(
    intervals: Sequence[Dict[str, object]],
    scales: Dict[str, float],
) -> List[Dict[str, object]]:
    output: List[Dict[str, object]] = []

    for row in intervals:
        serial = dict(row)
        serial["normalized_signed_delta_ln_a"] = bounded_signed(
            to_float(row["signed_delta_ln_a"]),
            scales["delta_ln_a"],
        )
        serial["normalized_signed_H_flow"] = bounded_signed(
            to_float(row["signed_H_flow"]),
            scales["H"],
        )
        serial["normalized_signed_density_flow"] = bounded_signed(
            to_float(row["signed_density_flow"]),
            scales["density"],
        )
        serial["normalized_signed_curvature_flow"] = bounded_signed(
            to_float(row["signed_curvature_flow"]),
            scales["curvature"],
        )
        serial["normalized_signed_margin_flow"] = bounded_signed(
            to_float(row["signed_margin_flow"]),
            scales["margin"],
        )

        output.append(
            {
                key: fmt(serial.get(key, ""))
                for key in BRIDGE_COLUMNS
            }
        )

    return output


def classify_route(dataset_id: str) -> str:
    return {
        "A": "terminal_boundary_approach",
        "B": "finite_turning_surface_route",
        "C": "boundary_recession_expansion",
    }[dataset_id]


def summarize(
    dataset_id: str,
    dataset_name: str,
    row_count: int,
    raw_intervals: Sequence[Dict[str, object]],
    normalized_intervals: Sequence[Dict[str, object]],
    scales: Dict[str, float],
) -> Dict[str, object]:
    n = len(raw_intervals)

    margin_directions = [
        str(r["margin_flow_direction"]) for r in raw_intervals
    ]
    route_left = [
        to_float(r["route_coordinate_left"]) for r in raw_intervals
    ]
    route_right = [
        to_float(r["route_coordinate_right"]) for r in raw_intervals
    ]

    def mean_norm(name: str) -> float:
        return safe_mean(
            to_float(r[name]) for r in normalized_intervals
        )

    def mean_abs_norm(name: str) -> float:
        return safe_mean(
            abs(to_float(r[name])) for r in normalized_intervals
        )

    return {
        "dataset_id": dataset_id,
        "dataset_name": dataset_name,
        "n_rows": row_count,
        "n_intervals": n,
        "n_turning_crossings": sum(
            r["crosses_turning_surface"] == "yes"
            for r in raw_intervals
        ),
        "route_coordinate_min": fmt(min(route_left + route_right)),
        "route_coordinate_max": fmt(max(route_left + route_right)),
        "mean_signed_route_step": fmt(
            safe_mean(
                to_float(r["signed_route_step"])
                for r in raw_intervals
            )
        ),
        "mean_normalized_signed_delta_ln_a": fmt(
            mean_norm("normalized_signed_delta_ln_a")
        ),
        "mean_normalized_signed_H_flow": fmt(
            mean_norm("normalized_signed_H_flow")
        ),
        "mean_normalized_signed_density_flow": fmt(
            mean_norm("normalized_signed_density_flow")
        ),
        "mean_normalized_signed_curvature_flow": fmt(
            mean_norm("normalized_signed_curvature_flow")
        ),
        "mean_normalized_signed_margin_flow": fmt(
            mean_norm("normalized_signed_margin_flow")
        ),
        "mean_abs_normalized_delta_ln_a": fmt(
            mean_abs_norm("normalized_signed_delta_ln_a")
        ),
        "mean_abs_normalized_H_flow": fmt(
            mean_abs_norm("normalized_signed_H_flow")
        ),
        "mean_abs_normalized_density_flow": fmt(
            mean_abs_norm("normalized_signed_density_flow")
        ),
        "mean_abs_normalized_curvature_flow": fmt(
            mean_abs_norm("normalized_signed_curvature_flow")
        ),
        "mean_abs_normalized_margin_flow": fmt(
            mean_abs_norm("normalized_signed_margin_flow")
        ),
        "fraction_margin_decreasing": fmt(
            margin_directions.count("margin_decreasing") / n
        ),
        "fraction_margin_increasing": fmt(
            margin_directions.count("margin_increasing") / n
        ),
        "fraction_route_negative": fmt(
            sum(
                0.5 * (l + r) < 0.0
                for l, r in zip(route_left, route_right)
            )
            / n
        ),
        "fraction_route_positive": fmt(
            sum(
                0.5 * (l + r) > 0.0
                for l, r in zip(route_left, route_right)
            )
            / n
        ),
        "fraction_route_crossing_zero": fmt(
            sum(
                l <= 0.0 <= r or r <= 0.0 <= l
                for l, r in zip(route_left, route_right)
            )
            / n
        ),
        "delta_ln_a_q90_scale": fmt(scales["delta_ln_a"]),
        "H_flow_q90_scale": fmt(scales["H"]),
        "density_flow_q90_scale": fmt(scales["density"]),
        "curvature_flow_q90_scale": fmt(scales["curvature"]),
        "margin_flow_q90_scale": fmt(scales["margin"]),
        "route_class": classify_route(dataset_id),
        "script_version": SCRIPT_VERSION,
    }


def write_manifest(
    path: Path,
    inputs: Dict[str, Path],
    bridge_output: Path,
    summary_output: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        handle.write(
            "A–B–C ORIENTATION-SENSITIVE BRIDGE MANIFEST V1.1\n"
        )
        handle.write("=" * 72 + "\n\n")

        handle.write(f"Script version: {SCRIPT_VERSION}\n")
        handle.write(
            f"Flow normalization quantile: Q{int(FLOW_SCALE_QUANTILE * 100)}\n\n"
        )

        handle.write("INPUTS\n")
        for key in ("A", "B", "C"):
            handle.write(f"Dataset {key}: {inputs[key]}\n")
        handle.write("\n")

        handle.write("OUTPUTS\n")
        handle.write(f"Bridge intervals: {bridge_output}\n")
        handle.write(f"Bridge summary: {summary_output}\n\n")

        handle.write("SHARED DIMENSIONLESS ROUTE COORDINATE\n")
        handle.write(
            "The coordinate is constructed from cumulative |Delta ln(a)|.\n"
        )
        handle.write(
            "A: -1 at the outer contraction endpoint to 0 at termination.\n"
        )
        handle.write(
            "B: -1 on the outer contraction branch, 0 at the exact bounce, "
            "+1 on the outer expansion branch.\n"
        )
        handle.write(
            "C: 0 at the early small-a endpoint to +1 at the late endpoint.\n\n"
        )

        handle.write("NORMALIZED SIGNED FLOWS\n")
        handle.write(
            "Each raw signed flow uses its dataset-specific Q90 absolute scale:\n"
        )
        handle.write(
            "normalized = raw / (Q90(|raw|) + |raw|)\n"
        )
        handle.write(
            "The result is dimensionless, sign-preserving, and bounded "
            "within [-1,1].\n\n"
        )

        handle.write("ROUTE INTERPRETATION\n")
        handle.write("A: terminal boundary approach\n")
        handle.write("B: finite turning-surface routing\n")
        handle.write("C: boundary-recession expansion\n\n")

        handle.write("LIMITS\n")
        handle.write(
            "- The route coordinate is path intrinsic, not a final physical "
            "metric distance.\n"
        )
        handle.write(
            "- boundary_margin_candidate remains provisional.\n"
        )
        handle.write(
            "- Q90 normalization must remain fixed for matched reruns.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build orientation-sensitive ABC Bridge v1.1."
    )
    parser.add_argument("--a-input", type=Path, default=DEFAULT_A_INPUT)
    parser.add_argument("--b-input", type=Path, default=DEFAULT_B_INPUT)
    parser.add_argument("--c-input", type=Path, default=DEFAULT_C_INPUT)
    parser.add_argument(
        "--bridge-output", type=Path, default=DEFAULT_BRIDGE_OUTPUT
    )
    parser.add_argument(
        "--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT
    )
    parser.add_argument(
        "--manifest-output", type=Path, default=DEFAULT_MANIFEST_OUTPUT
    )
    args = parser.parse_args()

    inputs = {
        "A": args.a_input.resolve(),
        "B": args.b_input.resolve(),
        "C": args.c_input.resolve(),
    }
    for path in inputs.values():
        if not path.is_file():
            raise FileNotFoundError(f"Required input not found: {path}")

    datasets = {
        "A": (
            "Classical Friedmann contraction",
            normalize_a(read_csv(inputs["A"])),
        ),
        "B": (
            "Effective LQC bounce",
            normalize_b(read_csv(inputs["B"])),
        ),
        "C": (
            "Planck-anchored Lambda-CDM expansion",
            normalize_c(read_csv(inputs["C"])),
        ),
    }

    all_bridge_rows: List[Dict[str, object]] = []
    summaries: List[Dict[str, object]] = []

    for dataset_id in ("A", "B", "C"):
        dataset_name, rows = datasets[dataset_id]
        coordinates = assign_route_coordinate(dataset_id, rows)
        raw_intervals = compute_raw_intervals(
            dataset_id,
            dataset_name,
            rows,
            coordinates,
        )
        scales = flow_scales(raw_intervals)
        normalized_intervals = apply_normalized_flows(
            raw_intervals,
            scales,
        )
        all_bridge_rows.extend(normalized_intervals)
        summaries.append(
            summarize(
                dataset_id,
                dataset_name,
                len(rows),
                raw_intervals,
                normalized_intervals,
                scales,
            )
        )

    bridge_output = args.bridge_output.resolve()
    summary_output = args.summary_output.resolve()
    manifest_output = args.manifest_output.resolve()

    write_csv(bridge_output, all_bridge_rows, BRIDGE_COLUMNS)
    write_csv(summary_output, summaries, SUMMARY_COLUMNS)
    write_manifest(
        manifest_output,
        inputs,
        bridge_output,
        summary_output,
    )

    print(f"Script version: {SCRIPT_VERSION}")
    print(f"Created bridge: {bridge_output}")
    print(f"Created summary: {summary_output}")
    print(f"Created manifest: {manifest_output}")
    print(f"Total bridge rows: {len(all_bridge_rows)}")

    for row in summaries:
        print(
            f"{row['dataset_id']}: {row['route_class']}, "
            f"route=[{row['route_coordinate_min']}, "
            f"{row['route_coordinate_max']}], "
            f"norm dln(a)={row['mean_normalized_signed_delta_ln_a']}, "
            f"norm density={row['mean_normalized_signed_density_flow']}"
        )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
