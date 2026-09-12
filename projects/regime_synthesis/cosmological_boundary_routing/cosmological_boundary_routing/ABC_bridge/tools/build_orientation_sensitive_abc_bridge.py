#!/usr/bin/env python3
"""
build_orientation_sensitive_abc_bridge.py

Construct the orientation-sensitive A–B–C bridge for the Cosmological
Boundary Routing project.

Datasets
--------
A — classical Friedmann contraction toward the small-a boundary
B — effective LQC contraction -> exact bounce -> expansion
C — Planck-anchored Lambda-CDM expansion

The bridge preserves path orientation and signed flow information that is
discarded by sorted scalar ladders and magnitude-only deformation metrics.

Default inputs
--------------
../../A_classical_friedmann/generated_trajectory/validated/
    classical_friedmann_approach_validated.csv

../../B_lqc_bounce/canonical/ladder/
    lqc_bounce_response_path_preliminary.csv

../../C_planck_lcdm/generated_trajectory/validated/
    planck_lcdm_trajectory_validated.csv

Outputs
-------
../outputs/ABC_orientation_sensitive_bridge.csv
../outputs/ABC_orientation_sensitive_bridge_summary.csv
../outputs/ABC_orientation_sensitive_bridge_manifest.txt

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


SCRIPT_VERSION = "1.0.0"

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
    BRIDGE_ROOT
    / "outputs"
    / "ABC_orientation_sensitive_bridge.csv"
)

DEFAULT_SUMMARY_OUTPUT = (
    BRIDGE_ROOT
    / "outputs"
    / "ABC_orientation_sensitive_bridge_summary.csv"
)

DEFAULT_MANIFEST_OUTPUT = (
    BRIDGE_ROOT
    / "outputs"
    / "ABC_orientation_sensitive_bridge_manifest.txt"
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
    "time_left",
    "time_right",
    "time_mid",
    "scale_factor_left",
    "scale_factor_right",
    "scale_factor_mid",
    "signed_delta_ln_a",
    "H_signed_left",
    "H_signed_right",
    "signed_H_flow",
    "density_left",
    "density_right",
    "signed_density_flow",
    "curvature_left",
    "curvature_right",
    "signed_curvature_flow",
    "margin_left",
    "margin_right",
    "signed_margin_flow",
    "margin_flow_direction",
    "distance_to_surface_left",
    "distance_to_surface_right",
    "distance_to_surface_mid",
    "signed_surface_approach",
    "surface_relation",
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
    "mean_signed_delta_ln_a",
    "mean_signed_H_flow",
    "mean_signed_density_flow",
    "mean_signed_curvature_flow",
    "mean_signed_margin_flow",
    "fraction_margin_decreasing",
    "fraction_margin_increasing",
    "fraction_approaching_surface",
    "fraction_receding_from_surface",
    "minimum_margin",
    "maximum_margin",
    "minimum_distance_to_surface",
    "maximum_distance_to_surface",
    "route_class",
    "script_version",
]


def to_float(value: object, default: float = 0.0) -> float:
    try:
        if value is None or str(value).strip() == "":
            return default
        number = float(str(value).strip())
        return number if math.isfinite(number) else default
    except (TypeError, ValueError):
        return default


def safe_log(value: float) -> float:
    return math.log(max(value, 1.0e-300))


def safe_mean(values: Iterable[float]) -> float:
    data = [value for value in values if math.isfinite(value)]
    return statistics.fmean(data) if data else 0.0


def fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


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
    normalized: List[Dict[str, object]] = []

    for index, row in enumerate(rows):
        normalized.append(
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
                "distance_to_surface": max(
                    to_float(
                        first_existing(
                            row,
                            "distance_to_cutoff_log_a",
                            "distance_from_bounce_log_a",
                        )
                    ),
                    0.0,
                ),
                "rho_over_rho_c": 0.0,
                "x_bounce_distance": 0.0,
                "is_exact_bounce": "no",
            }
        )

    return normalized


def normalize_b(rows: Sequence[Dict[str, str]]) -> List[Dict[str, object]]:
    normalized: List[Dict[str, object]] = []

    for index, row in enumerate(rows):
        normalized.append(
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
                "distance_to_surface": abs(
                    to_float(row.get("x_bounce_distance"))
                ),
                "rho_over_rho_c": to_float(row.get("rho_over_rho_c")),
                "x_bounce_distance": to_float(
                    row.get("x_bounce_distance")
                ),
                "is_exact_bounce": (
                    row.get("is_exact_bounce") or "no"
                ).strip().lower(),
            }
        )

    return normalized


def normalize_c(rows: Sequence[Dict[str, str]]) -> List[Dict[str, object]]:
    normalized: List[Dict[str, object]] = []

    for index, row in enumerate(rows):
        normalized.append(
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
                "distance_to_surface": max(
                    to_float(
                        first_existing(
                            row,
                            "distance_to_cutoff_log_a",
                            "distance_from_boundary_log_a",
                            "distance_from_bounce_log_a",
                        )
                    ),
                    0.0,
                ),
                "rho_over_rho_c": 0.0,
                "x_bounce_distance": 0.0,
                "is_exact_bounce": "no",
            }
        )

    return normalized


def infer_route_phase(
    dataset_id: str,
    left: Dict[str, object],
    right: Dict[str, object],
) -> str:
    if dataset_id == "A":
        return "terminal_approach"

    if dataset_id == "C":
        return "boundary_recession"

    left_branch = str(left["branch"])
    right_branch = str(right["branch"])

    if (
        left["is_exact_bounce"] == "yes"
        or right["is_exact_bounce"] == "yes"
        or left_branch != right_branch
    ):
        return "turning_surface"

    if left_branch == "contraction":
        return "pre_bounce_approach"

    if left_branch == "expansion":
        return "post_bounce_recession"

    return "undetermined"


def surface_relation(
    distance_left: float,
    distance_right: float,
) -> str:
    delta = distance_right - distance_left
    tolerance = 1.0e-15

    if delta < -tolerance:
        return "approaching_surface"
    if delta > tolerance:
        return "receding_from_surface"
    return "surface_stationary"


def margin_direction(delta_margin: float) -> str:
    tolerance = 1.0e-15
    if delta_margin < -tolerance:
        return "margin_decreasing"
    if delta_margin > tolerance:
        return "margin_increasing"
    return "margin_stationary"


def build_intervals(
    dataset_id: str,
    dataset_name: str,
    rows: Sequence[Dict[str, object]],
) -> List[Dict[str, object]]:
    if len(rows) < 2:
        raise ValueError(f"Dataset {dataset_id} has fewer than two rows.")

    intervals: List[Dict[str, object]] = []

    for index in range(len(rows) - 1):
        left = rows[index]
        right = rows[index + 1]

        a_left = max(to_float(left["scale_factor"]), 1.0e-300)
        a_right = max(to_float(right["scale_factor"]), 1.0e-300)

        h_left = to_float(left["H_signed"])
        h_right = to_float(right["H_signed"])

        density_left = max(to_float(left["density"]), 1.0e-300)
        density_right = max(to_float(right["density"]), 1.0e-300)

        curvature_left = to_float(left["curvature"])
        curvature_right = to_float(right["curvature"])

        margin_left = to_float(left["margin"])
        margin_right = to_float(right["margin"])

        distance_left = max(to_float(left["distance_to_surface"]), 0.0)
        distance_right = max(to_float(right["distance_to_surface"]), 0.0)

        crosses = (
            str(left["is_exact_bounce"]) == "yes"
            or str(right["is_exact_bounce"]) == "yes"
            or str(left["branch"]) != str(right["branch"])
        )

        signed_delta_ln_a = safe_log(a_right) - safe_log(a_left)
        signed_h_flow = h_right - h_left
        signed_density_flow = (
            safe_log(density_right) - safe_log(density_left)
        )
        signed_curvature_flow = (
            math.copysign(math.log1p(abs(curvature_right)), curvature_right)
            - math.copysign(math.log1p(abs(curvature_left)), curvature_left)
        )
        signed_margin_flow = margin_right - margin_left
        signed_surface_approach = distance_right - distance_left

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
                "time_left": fmt(to_float(left["time"])),
                "time_right": fmt(to_float(right["time"])),
                "time_mid": fmt(
                    0.5
                    * (
                        to_float(left["time"])
                        + to_float(right["time"])
                    )
                ),
                "scale_factor_left": fmt(a_left),
                "scale_factor_right": fmt(a_right),
                "scale_factor_mid": fmt(math.sqrt(a_left * a_right)),
                "signed_delta_ln_a": fmt(signed_delta_ln_a),
                "H_signed_left": fmt(h_left),
                "H_signed_right": fmt(h_right),
                "signed_H_flow": fmt(signed_h_flow),
                "density_left": fmt(density_left),
                "density_right": fmt(density_right),
                "signed_density_flow": fmt(signed_density_flow),
                "curvature_left": fmt(curvature_left),
                "curvature_right": fmt(curvature_right),
                "signed_curvature_flow": fmt(
                    signed_curvature_flow
                ),
                "margin_left": fmt(margin_left),
                "margin_right": fmt(margin_right),
                "signed_margin_flow": fmt(signed_margin_flow),
                "margin_flow_direction": margin_direction(
                    signed_margin_flow
                ),
                "distance_to_surface_left": fmt(distance_left),
                "distance_to_surface_right": fmt(distance_right),
                "distance_to_surface_mid": fmt(
                    0.5 * (distance_left + distance_right)
                ),
                "signed_surface_approach": fmt(
                    signed_surface_approach
                ),
                "surface_relation": surface_relation(
                    distance_left, distance_right
                ),
                "rho_over_rho_c_left": fmt(
                    to_float(left["rho_over_rho_c"])
                ),
                "rho_over_rho_c_right": fmt(
                    to_float(right["rho_over_rho_c"])
                ),
                "rho_over_rho_c_mid": fmt(
                    0.5
                    * (
                        to_float(left["rho_over_rho_c"])
                        + to_float(right["rho_over_rho_c"])
                    )
                ),
                "x_bounce_distance_left": fmt(
                    to_float(left["x_bounce_distance"])
                ),
                "x_bounce_distance_right": fmt(
                    to_float(right["x_bounce_distance"])
                ),
                "x_bounce_distance_mid": fmt(
                    0.5
                    * (
                        to_float(left["x_bounce_distance"])
                        + to_float(right["x_bounce_distance"])
                    )
                ),
                "is_exact_bounce_left": left["is_exact_bounce"],
                "is_exact_bounce_right": right["is_exact_bounce"],
            }
        )

    return intervals


def classify_route(
    dataset_id: str,
    intervals: Sequence[Dict[str, object]],
) -> str:
    if dataset_id == "A":
        return "terminal_boundary_approach"
    if dataset_id == "B":
        has_turn = any(
            row["crosses_turning_surface"] == "yes"
            for row in intervals
        )
        return (
            "finite_turning_surface_route"
            if has_turn
            else "bounce_route_not_detected"
        )
    if dataset_id == "C":
        return "boundary_recession_expansion"
    return "unclassified"


def summarize_dataset(
    dataset_id: str,
    dataset_name: str,
    row_count: int,
    intervals: Sequence[Dict[str, object]],
) -> Dict[str, object]:
    n = len(intervals)
    if n == 0:
        raise ValueError(f"No intervals for Dataset {dataset_id}.")

    margin_directions = [
        str(row["margin_flow_direction"]) for row in intervals
    ]
    surface_relations = [
        str(row["surface_relation"]) for row in intervals
    ]

    minimum_margin = min(
        min(
            to_float(row["margin_left"]),
            to_float(row["margin_right"]),
        )
        for row in intervals
    )
    maximum_margin = max(
        max(
            to_float(row["margin_left"]),
            to_float(row["margin_right"]),
        )
        for row in intervals
    )
    minimum_distance = min(
        min(
            to_float(row["distance_to_surface_left"]),
            to_float(row["distance_to_surface_right"]),
        )
        for row in intervals
    )
    maximum_distance = max(
        max(
            to_float(row["distance_to_surface_left"]),
            to_float(row["distance_to_surface_right"]),
        )
        for row in intervals
    )

    return {
        "dataset_id": dataset_id,
        "dataset_name": dataset_name,
        "n_rows": row_count,
        "n_intervals": n,
        "n_turning_crossings": sum(
            row["crosses_turning_surface"] == "yes"
            for row in intervals
        ),
        "mean_signed_delta_ln_a": fmt(
            safe_mean(
                to_float(row["signed_delta_ln_a"])
                for row in intervals
            )
        ),
        "mean_signed_H_flow": fmt(
            safe_mean(
                to_float(row["signed_H_flow"])
                for row in intervals
            )
        ),
        "mean_signed_density_flow": fmt(
            safe_mean(
                to_float(row["signed_density_flow"])
                for row in intervals
            )
        ),
        "mean_signed_curvature_flow": fmt(
            safe_mean(
                to_float(row["signed_curvature_flow"])
                for row in intervals
            )
        ),
        "mean_signed_margin_flow": fmt(
            safe_mean(
                to_float(row["signed_margin_flow"])
                for row in intervals
            )
        ),
        "fraction_margin_decreasing": fmt(
            margin_directions.count("margin_decreasing") / n
        ),
        "fraction_margin_increasing": fmt(
            margin_directions.count("margin_increasing") / n
        ),
        "fraction_approaching_surface": fmt(
            surface_relations.count("approaching_surface") / n
        ),
        "fraction_receding_from_surface": fmt(
            surface_relations.count("receding_from_surface") / n
        ),
        "minimum_margin": fmt(minimum_margin),
        "maximum_margin": fmt(maximum_margin),
        "minimum_distance_to_surface": fmt(minimum_distance),
        "maximum_distance_to_surface": fmt(maximum_distance),
        "route_class": classify_route(dataset_id, intervals),
        "script_version": SCRIPT_VERSION,
    }


def write_manifest(
    path: Path,
    a_input: Path,
    b_input: Path,
    c_input: Path,
    bridge_output: Path,
    summary_output: Path,
    summaries: Sequence[Dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    by_id = {str(row["dataset_id"]): row for row in summaries}

    with path.open("w", encoding="utf-8") as handle:
        handle.write(
            "A–B–C ORIENTATION-SENSITIVE BRIDGE MANIFEST\n"
        )
        handle.write("=" * 72 + "\n\n")

        handle.write(f"Script version: {SCRIPT_VERSION}\n\n")

        handle.write("INPUTS\n")
        handle.write(f"Dataset A: {a_input}\n")
        handle.write(f"Dataset B: {b_input}\n")
        handle.write(f"Dataset C: {c_input}\n\n")

        handle.write("OUTPUTS\n")
        handle.write(f"Bridge intervals: {bridge_output}\n")
        handle.write(f"Bridge summary: {summary_output}\n\n")

        handle.write("PURPOSE\n")
        handle.write(
            "The bridge restores orientation information discarded by "
            "sorted scalar ladders and magnitude-only alpha metrics.\n\n"
        )

        handle.write("PRIMARY SIGNED QUANTITIES\n")
        handle.write("- signed Delta ln(a)\n")
        handle.write("- signed H flow\n")
        handle.write("- signed density flow\n")
        handle.write("- signed curvature flow\n")
        handle.write("- signed provisional-margin flow\n")
        handle.write("- signed approach to or recession from the surface\n\n")

        handle.write("ROUTE CLASSES\n")
        for dataset_id in ("A", "B", "C"):
            row = by_id.get(dataset_id)
            if row:
                handle.write(
                    f"{dataset_id}: {row['route_class']}\n"
                )
        handle.write("\n")

        handle.write("CORE TEST\n")
        handle.write(
            "A should approach a terminal boundary with decreasing margin.\n"
        )
        handle.write(
            "B should approach a finite turning surface, cross it, and "
            "recede after reversal.\n"
        )
        handle.write(
            "C should expand away from the early boundary regime.\n\n"
        )

        handle.write("INTERPRETIVE LIMITS\n")
        handle.write(
            "- boundary_margin_candidate remains provisional.\n"
        )
        handle.write(
            "- Dataset A and C surface-distance fields depend on available "
            "trajectory columns and are not yet a final common metric.\n"
        )
        handle.write(
            "- Dataset B uses x_bounce_distance as its turning-surface "
            "coordinate.\n"
        )
        handle.write(
            "- The bridge is an orientation-sensitive comparison layer, "
            "not yet the final canonical boundary-routing proof.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build the orientation-sensitive A–B–C cosmological bridge."
        )
    )
    parser.add_argument(
        "--a-input",
        type=Path,
        default=DEFAULT_A_INPUT,
    )
    parser.add_argument(
        "--b-input",
        type=Path,
        default=DEFAULT_B_INPUT,
    )
    parser.add_argument(
        "--c-input",
        type=Path,
        default=DEFAULT_C_INPUT,
    )
    parser.add_argument(
        "--bridge-output",
        type=Path,
        default=DEFAULT_BRIDGE_OUTPUT,
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=DEFAULT_SUMMARY_OUTPUT,
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        default=DEFAULT_MANIFEST_OUTPUT,
    )
    args = parser.parse_args()

    a_input = args.a_input.resolve()
    b_input = args.b_input.resolve()
    c_input = args.c_input.resolve()
    bridge_output = args.bridge_output.resolve()
    summary_output = args.summary_output.resolve()
    manifest_output = args.manifest_output.resolve()

    for path in (a_input, b_input, c_input):
        if not path.is_file():
            raise FileNotFoundError(f"Required input not found: {path}")

    a_rows = normalize_a(read_csv(a_input))
    b_rows = normalize_b(read_csv(b_input))
    c_rows = normalize_c(read_csv(c_input))

    a_intervals = build_intervals(
        "A",
        "Classical Friedmann contraction",
        a_rows,
    )
    b_intervals = build_intervals(
        "B",
        "Effective LQC bounce",
        b_rows,
    )
    c_intervals = build_intervals(
        "C",
        "Planck-anchored Lambda-CDM expansion",
        c_rows,
    )

    bridge_rows = a_intervals + b_intervals + c_intervals

    summaries = [
        summarize_dataset(
            "A",
            "Classical Friedmann contraction",
            len(a_rows),
            a_intervals,
        ),
        summarize_dataset(
            "B",
            "Effective LQC bounce",
            len(b_rows),
            b_intervals,
        ),
        summarize_dataset(
            "C",
            "Planck-anchored Lambda-CDM expansion",
            len(c_rows),
            c_intervals,
        ),
    ]

    write_csv(bridge_output, bridge_rows, BRIDGE_COLUMNS)
    write_csv(summary_output, summaries, SUMMARY_COLUMNS)
    write_manifest(
        manifest_output,
        a_input,
        b_input,
        c_input,
        bridge_output,
        summary_output,
        summaries,
    )

    print(f"Script version: {SCRIPT_VERSION}")
    print(f"Created bridge: {bridge_output}")
    print(f"Created summary: {summary_output}")
    print(f"Created manifest: {manifest_output}")
    print(f"Dataset A intervals: {len(a_intervals)}")
    print(f"Dataset B intervals: {len(b_intervals)}")
    print(f"Dataset C intervals: {len(c_intervals)}")
    print(f"Total bridge rows: {len(bridge_rows)}")
    for row in summaries:
        print(
            f"{row['dataset_id']}: "
            f"{row['route_class']}, "
            f"margin decreasing={row['fraction_margin_decreasing']}, "
            f"margin increasing={row['fraction_margin_increasing']}"
        )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
