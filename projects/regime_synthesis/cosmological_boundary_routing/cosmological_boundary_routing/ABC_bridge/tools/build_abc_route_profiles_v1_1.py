#!/usr/bin/env python3
"""
build_abc_route_profiles_v1_1.py

Reproduce the two derived Bridge v1.1 datasets from:

    ABC_orientation_sensitive_bridge_v1_1.csv

Outputs
-------
ABC_orientation_sensitive_route_profile_v1_1.csv
ABC_orientation_sensitive_phase_summary_v1_1.csv

Method
------
1. Map bridge rows into five interpretation phases:
   - A_terminal_approach
   - B_pre_bounce_approach
   - B_turning_surface
   - B_post_bounce_recession
   - C_boundary_recession

2. Build a branch-resolved phase summary so Dataset B is not reduced to
   cancelling full-path means.

3. Build a route-profile dataset:
   - ordinary phases are binned into up to 50 equal-width bins in the shared
     route coordinate;
   - the B turning-surface rows are preserved as one dedicated profile rather
     than merged into neighboring bins.

No third-party packages beyond pandas and numpy are required.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


SCRIPT_VERSION = "1.0.0"

HERE = Path(__file__).resolve().parent
BRIDGE_ROOT = HERE.parent

DEFAULT_INPUT = (
    BRIDGE_ROOT
    / "outputs"
    / "ABC_orientation_sensitive_bridge_v1_1.csv"
)

DEFAULT_PROFILE_OUTPUT = (
    BRIDGE_ROOT
    / "outputs"
    / "ABC_orientation_sensitive_route_profile_v1_1.csv"
)

DEFAULT_PHASE_SUMMARY_OUTPUT = (
    BRIDGE_ROOT
    / "outputs"
    / "ABC_orientation_sensitive_phase_summary_v1_1.csv"
)


PHASE_MAP = {
    ("A", "terminal_approach"): "A_terminal_approach",
    ("B", "pre_bounce_approach"): "B_pre_bounce_approach",
    ("B", "turning_surface"): "B_turning_surface",
    ("B", "post_bounce_recession"): "B_post_bounce_recession",
    ("C", "boundary_recession"): "C_boundary_recession",
}


PROFILE_NUMERIC_COLUMNS = [
    "signed_route_step",
    "signed_delta_ln_a",
    "normalized_signed_delta_ln_a",
    "signed_H_flow",
    "normalized_signed_H_flow",
    "signed_density_flow",
    "normalized_signed_density_flow",
    "signed_curvature_flow",
    "normalized_signed_curvature_flow",
    "signed_margin_flow",
    "normalized_signed_margin_flow",
    "rho_over_rho_c_mid",
    "x_bounce_distance_mid",
]


def validate_columns(frame: pd.DataFrame) -> None:
    required = {
        "dataset_id",
        "dataset_name",
        "route_phase",
        "route_coordinate_left",
        "route_coordinate_right",
        "route_coordinate_mid",
        "margin_flow_direction",
        "crosses_turning_surface",
        *PROFILE_NUMERIC_COLUMNS,
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(
            "Input bridge file is missing required column(s): "
            + ", ".join(missing)
        )


def add_profile_phase(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["profile_phase"] = [
        PHASE_MAP.get(
            (str(dataset), str(phase)),
            f"{dataset}_{phase}",
        )
        for dataset, phase in zip(
            result["dataset_id"],
            result["route_phase"],
        )
    ]
    return result


def build_route_profile(
    frame: pd.DataFrame,
    bin_count: int,
) -> pd.DataFrame:
    profile_rows: list[dict[str, object]] = []

    for phase, group in frame.groupby(
        "profile_phase",
        sort=False,
    ):
        group = group.sort_values("route_coordinate_mid").copy()

        if phase == "B_turning_surface":
            grouped_chunks = [("turning_surface", group)]
        else:
            route_min = float(group["route_coordinate_mid"].min())
            route_max = float(group["route_coordinate_mid"].max())

            if np.isclose(route_min, route_max):
                grouped_chunks = [("single_bin", group)]
            else:
                bins = np.linspace(
                    route_min,
                    route_max,
                    bin_count + 1,
                )
                group["route_bin"] = pd.cut(
                    group["route_coordinate_mid"],
                    bins=bins,
                    include_lowest=True,
                    duplicates="drop",
                )
                grouped_chunks = list(
                    group.groupby(
                        "route_bin",
                        observed=True,
                    )
                )

        for bin_index, (bin_label, chunk) in enumerate(grouped_chunks):
            row: dict[str, object] = {
                "profile_phase": phase,
                "dataset_id": str(chunk["dataset_id"].iloc[0]),
                "dataset_name": str(chunk["dataset_name"].iloc[0]),
                "route_phase": str(chunk["route_phase"].iloc[0]),
                "profile_bin_index": bin_index,
                "profile_bin_label": str(bin_label),
                "n_intervals": len(chunk),
                "route_coordinate_min": float(
                    chunk["route_coordinate_left"].min()
                ),
                "route_coordinate_max": float(
                    chunk["route_coordinate_right"].max()
                ),
                "route_coordinate_mid_mean": float(
                    chunk["route_coordinate_mid"].mean()
                ),
                "fraction_margin_decreasing": float(
                    (
                        chunk["margin_flow_direction"]
                        == "margin_decreasing"
                    ).mean()
                ),
                "fraction_margin_increasing": float(
                    (
                        chunk["margin_flow_direction"]
                        == "margin_increasing"
                    ).mean()
                ),
                "fraction_crossing_surface": float(
                    (
                        chunk["crosses_turning_surface"]
                        == "yes"
                    ).mean()
                ),
                "script_version": SCRIPT_VERSION,
            }

            for column in PROFILE_NUMERIC_COLUMNS:
                row[f"mean_{column}"] = float(chunk[column].mean())
                row[f"mean_abs_{column}"] = float(
                    chunk[column].abs().mean()
                )

            profile_rows.append(row)

    return pd.DataFrame(profile_rows)


def build_phase_summary(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for phase, group in frame.groupby(
        "profile_phase",
        sort=False,
    ):
        rows.append(
            {
                "profile_phase": phase,
                "dataset_id": str(group["dataset_id"].iloc[0]),
                "dataset_name": str(group["dataset_name"].iloc[0]),
                "route_phase": str(group["route_phase"].iloc[0]),
                "n_intervals": len(group),
                "route_coordinate_min": float(
                    group["route_coordinate_left"].min()
                ),
                "route_coordinate_max": float(
                    group["route_coordinate_right"].max()
                ),
                "mean_normalized_signed_delta_ln_a": float(
                    group["normalized_signed_delta_ln_a"].mean()
                ),
                "mean_normalized_signed_H_flow": float(
                    group["normalized_signed_H_flow"].mean()
                ),
                "mean_normalized_signed_density_flow": float(
                    group["normalized_signed_density_flow"].mean()
                ),
                "mean_normalized_signed_curvature_flow": float(
                    group["normalized_signed_curvature_flow"].mean()
                ),
                "mean_normalized_signed_margin_flow": float(
                    group["normalized_signed_margin_flow"].mean()
                ),
                "mean_abs_normalized_signed_delta_ln_a": float(
                    group["normalized_signed_delta_ln_a"].abs().mean()
                ),
                "mean_abs_normalized_signed_H_flow": float(
                    group["normalized_signed_H_flow"].abs().mean()
                ),
                "mean_abs_normalized_signed_density_flow": float(
                    group["normalized_signed_density_flow"].abs().mean()
                ),
                "mean_abs_normalized_signed_curvature_flow": float(
                    group["normalized_signed_curvature_flow"].abs().mean()
                ),
                "mean_abs_normalized_signed_margin_flow": float(
                    group["normalized_signed_margin_flow"].abs().mean()
                ),
                "fraction_margin_decreasing": float(
                    (
                        group["margin_flow_direction"]
                        == "margin_decreasing"
                    ).mean()
                ),
                "fraction_margin_increasing": float(
                    (
                        group["margin_flow_direction"]
                        == "margin_increasing"
                    ).mean()
                ),
                "turning_crossing_intervals": int(
                    (
                        group["crosses_turning_surface"]
                        == "yes"
                    ).sum()
                ),
                "script_version": SCRIPT_VERSION,
            }
        )

    return pd.DataFrame(rows)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Reproduce Bridge v1.1 route-profile and phase-summary datasets."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
    )
    parser.add_argument(
        "--profile-output",
        type=Path,
        default=DEFAULT_PROFILE_OUTPUT,
    )
    parser.add_argument(
        "--phase-summary-output",
        type=Path,
        default=DEFAULT_PHASE_SUMMARY_OUTPUT,
    )
    parser.add_argument(
        "--bins",
        type=int,
        default=50,
        help="Equal-width route-coordinate bins for ordinary phases.",
    )
    args = parser.parse_args()

    input_path = args.input.resolve()
    profile_output = args.profile_output.resolve()
    phase_summary_output = args.phase_summary_output.resolve()

    if not input_path.is_file():
        raise FileNotFoundError(
            f"Bridge v1.1 input not found: {input_path}"
        )
    if args.bins < 1:
        raise ValueError("--bins must be at least 1.")

    frame = pd.read_csv(input_path)
    validate_columns(frame)
    frame = add_profile_phase(frame)

    profile = build_route_profile(frame, args.bins)
    phase_summary = build_phase_summary(frame)

    profile_output.parent.mkdir(parents=True, exist_ok=True)
    phase_summary_output.parent.mkdir(parents=True, exist_ok=True)

    profile.to_csv(profile_output, index=False)
    phase_summary.to_csv(phase_summary_output, index=False)

    print(f"Script version: {SCRIPT_VERSION}")
    print(f"Input: {input_path}")
    print(f"Created route profile: {profile_output}")
    print(f"Created phase summary: {phase_summary_output}")
    print(f"Route-profile rows: {len(profile)}")
    print(f"Phase-summary rows: {len(phase_summary)}")
    print("Profile phases:")
    for phase in phase_summary["profile_phase"]:
        print(f"  {phase}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
