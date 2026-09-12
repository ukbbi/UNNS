#!/usr/bin/env python3
"""
Build Dataset A preliminary scalar representations for structural analysis.

Input:
    ../../generated_trajectory/validated/
    classical_friedmann_approach_validated.csv

Outputs:
    classical_friedmann_response_ladder_preliminary.csv
    classical_friedmann_response_path_preliminary.csv
    classical_friedmann_response_ladder_preliminary_struc_i.csv
    classical_friedmann_response_ladder_preliminary_manifest.txt

Definitions:
    q_A(a) = ln(E(a))
    E(a) = |H(a)| / H0

The sorted ladder is intended for STRUC-PERC-I.
The direction-preserving path retains contraction order from a = 1 to a = 1e-8.
The STRUC-I file contains the same sorted ladder with a single header row.

No third-party packages are required.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path
from typing import Dict, List


HERE = Path(__file__).resolve().parent

DEFAULT_INPUT = (
    HERE
    / ".."
    / ".."
    / "generated_trajectory"
    / "validated"
    / "classical_friedmann_approach_validated.csv"
)

DEFAULT_LADDER = (
    HERE
    / "classical_friedmann_response_ladder_preliminary.csv"
)

DEFAULT_PATH = (
    HERE
    / "classical_friedmann_response_path_preliminary.csv"
)

DEFAULT_STRUC_I = (
    HERE
    / "classical_friedmann_response_ladder_preliminary_struc_i.csv"
)

DEFAULT_MANIFEST = (
    HERE
    / "classical_friedmann_response_ladder_preliminary_manifest.txt"
)


def load_validated_trajectory(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = set(reader.fieldnames or [])

    required = {
        "sample_index",
        "scale_factor",
        "redshift",
        "E_of_a",
        "H_signed_km_s_Mpc",
        "H_magnitude_km_s_Mpc",
        "boundary_margin_candidate",
        "contraction_elapsed_time_Gyr",
    }
    missing = sorted(required - fields)
    if missing:
        raise ValueError(
            "Validated trajectory is missing required column(s): "
            + ", ".join(missing)
        )

    if len(rows) < 3:
        raise ValueError("At least three trajectory rows are required.")

    return rows


def parse_finite_positive(
    row: Dict[str, str],
    field: str,
    line_number: int,
) -> float:
    raw = (row.get(field) or "").strip()
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(
            f"Invalid {field} at CSV line {line_number}: {raw!r}"
        ) from exc

    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(
            f"{field} must be finite and positive at CSV line {line_number}"
        )
    return value


def parse_finite(
    row: Dict[str, str],
    field: str,
    line_number: int,
) -> float:
    raw = (row.get(field) or "").strip()
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(
            f"Invalid {field} at CSV line {line_number}: {raw!r}"
        ) from exc

    if not math.isfinite(value):
        raise ValueError(
            f"{field} must be finite at CSV line {line_number}"
        )
    return value


def build_path_rows(
    trajectory_rows: List[Dict[str, str]],
) -> List[Dict[str, object]]:
    path_rows: List[Dict[str, object]] = []

    for index, row in enumerate(trajectory_rows, start=2):
        e_value = parse_finite_positive(row, "E_of_a", index)
        scale_factor = parse_finite_positive(
            row, "scale_factor", index
        )
        redshift = parse_finite(row, "redshift", index)
        h_signed = parse_finite(
            row, "H_signed_km_s_Mpc", index
        )
        h_magnitude = parse_finite_positive(
            row, "H_magnitude_km_s_Mpc", index
        )
        margin = parse_finite(
            row, "boundary_margin_candidate", index
        )
        elapsed = parse_finite(
            row, "contraction_elapsed_time_Gyr", index
        )

        path_rows.append(
            {
                "path_index": len(path_rows),
                "source_sample_index": row["sample_index"],
                "scale_factor": scale_factor,
                "redshift": redshift,
                "contraction_elapsed_time_Gyr": elapsed,
                "H_signed_km_s_Mpc": h_signed,
                "H_magnitude_km_s_Mpc": h_magnitude,
                "E_of_a": e_value,
                "q_A_ln_E": math.log(e_value),
                "boundary_margin_candidate": margin,
                "trajectory_direction": "contraction",
            }
        )

    return path_rows


def write_sorted_ladder(
    path: Path,
    q_values: List[float],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(q_values)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        for value in ordered:
            writer.writerow([f"{value:.17g}"])


def write_path(
    path: Path,
    rows: List[Dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "path_index",
        "source_sample_index",
        "scale_factor",
        "redshift",
        "contraction_elapsed_time_Gyr",
        "H_signed_km_s_Mpc",
        "H_magnitude_km_s_Mpc",
        "E_of_a",
        "q_A_ln_E",
        "boundary_margin_candidate",
        "trajectory_direction",
    ]

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            serial = dict(row)
            for field in (
                "scale_factor",
                "redshift",
                "contraction_elapsed_time_Gyr",
                "H_signed_km_s_Mpc",
                "H_magnitude_km_s_Mpc",
                "E_of_a",
                "q_A_ln_E",
                "boundary_margin_candidate",
            ):
                serial[field] = f"{float(serial[field]):.17g}"
            writer.writerow(serial)


def write_struc_i(
    path: Path,
    q_values: List[float],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(q_values)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["value"])
        for value in ordered:
            writer.writerow([f"{value:.17g}"])


def write_manifest(
    path: Path,
    input_path: Path,
    ladder_path: Path,
    path_output: Path,
    struc_i_path: Path,
    path_rows: List[Dict[str, object]],
) -> None:
    q_values = [float(row["q_A_ln_E"]) for row in path_rows]
    ordered = sorted(q_values)
    gaps = [
        ordered[index + 1] - ordered[index]
        for index in range(len(ordered) - 1)
    ]

    scale_values = [
        float(row["scale_factor"]) for row in path_rows
    ]
    h_signed_values = [
        float(row["H_signed_km_s_Mpc"]) for row in path_rows
    ]

    same_direction = all(
        scale_values[index + 1] < scale_values[index]
        for index in range(len(scale_values) - 1)
    )
    h_negative = all(value < 0.0 for value in h_signed_values)

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        handle.write(
            "DATASET A PRELIMINARY STRUCTURAL REPRESENTATION MANIFEST\n"
        )
        handle.write("=" * 72 + "\n\n")

        handle.write(f"Input trajectory: {input_path}\n")
        handle.write(f"Sorted ladder: {ladder_path}\n")
        handle.write(f"Direction-preserving path: {path_output}\n")
        handle.write(f"STRUC-I input: {struc_i_path}\n\n")

        handle.write("DATASET\n")
        handle.write(
            "Dataset A — matched classical Friedmann contraction\n\n"
        )

        handle.write("SCALAR RESPONSE COORDINATE\n")
        handle.write("q_A(a) = ln(E(a))\n")
        handle.write("E(a) = |H(a)| / H0\n\n")

        handle.write("REPRESENTATIONS\n")
        handle.write(
            "1. Sorted ladder: values ordered numerically for "
            "STRUC-PERC-I.\n"
        )
        handle.write(
            "2. Direction-preserving path: values retained in contraction "
            "order from a = 1 toward a = 1e-8.\n"
        )
        handle.write(
            "3. STRUC-I ladder: sorted ladder with a single 'value' "
            "header.\n\n"
        )

        handle.write("COUNTS\n")
        handle.write(f"trajectory rows = {len(path_rows)}\n")
        handle.write(f"ladder elements = {len(ordered)}\n")
        handle.write(
            f"unique ladder elements = {len(set(ordered))}\n"
        )
        handle.write(f"gap count = {len(gaps)}\n\n")

        handle.write("RANGE\n")
        handle.write(
            f"minimum q_A = {ordered[0]:.17g}\n"
        )
        handle.write(
            f"maximum q_A = {ordered[-1]:.17g}\n"
        )
        handle.write(
            f"minimum gap = {min(gaps):.17g}\n"
        )
        handle.write(
            f"maximum gap = {max(gaps):.17g}\n\n"
        )

        handle.write("PATH CHECKS\n")
        handle.write(
            f"scale factor strictly decreasing = "
            f"{'yes' if same_direction else 'no'}\n"
        )
        handle.write(
            f"H_signed negative throughout = "
            f"{'yes' if h_negative else 'no'}\n"
        )
        handle.write(
            f"path start scale factor = {scale_values[0]:.17g}\n"
        )
        handle.write(
            f"path end scale factor = {scale_values[-1]:.17g}\n\n"
        )

        handle.write("STRUC-PERC-I SETTINGS\n")
        handle.write("domain adapter = Generic\n")
        handle.write("kappa points = 17\n")
        handle.write("kappa minimum = 0.01\n")
        handle.write("kappa maximum = 1.0\n\n")

        handle.write("STRUC-I SETTINGS\n")
        handle.write("maximum ladder size = 5000\n")
        handle.write("Monte Carlo runs = 2000\n")
        handle.write("kappa steps = 40\n")
        handle.write("kappa minimum = 0.01\n")
        handle.write("kappa maximum = 1.0\n\n")

        handle.write("EXPECTED RELATION TO DATASET C\n")
        handle.write(
            "Dataset A and Dataset C use the same E(a) magnitude, "
            "Planck anchor, scale-factor samples, and scalar mapping.\n"
        )
        handle.write(
            "Therefore their sorted q = ln(E) ladders are expected to be "
            "identical, while their path orientation and signed-H "
            "representations differ.\n\n"
        )

        handle.write("STATUS\n")
        handle.write("PRELIMINARY\n\n")

        handle.write("INTERPRETIVE LIMITS\n")
        handle.write(
            "- The sorted ladder removes trajectory direction.\n"
        )
        handle.write(
            "- Direct STRUC-PERC-I and STRUC-I results cannot by themselves "
            "distinguish expansion from contraction when the scalar sets "
            "are identical.\n"
        )
        handle.write(
            "- The direction-preserving path must be retained for alpha "
            "analysis and later A/B/C bridge metrics.\n"
        )
        handle.write(
            "- boundary_margin_candidate remains provisional.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build Dataset A sorted ln(E) ladder, contraction-order path, "
            "and STRUC-I-compatible ladder."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
    )
    parser.add_argument(
        "--ladder-output",
        type=Path,
        default=DEFAULT_LADDER,
    )
    parser.add_argument(
        "--path-output",
        type=Path,
        default=DEFAULT_PATH,
    )
    parser.add_argument(
        "--struc-i-output",
        type=Path,
        default=DEFAULT_STRUC_I,
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        default=DEFAULT_MANIFEST,
    )
    args = parser.parse_args()

    input_path = args.input.resolve()
    ladder_path = args.ladder_output.resolve()
    path_output = args.path_output.resolve()
    struc_i_path = args.struc_i_output.resolve()
    manifest_path = args.manifest_output.resolve()

    if not input_path.is_file():
        raise FileNotFoundError(
            f"Validated Dataset A trajectory not found: {input_path}"
        )

    trajectory_rows = load_validated_trajectory(input_path)
    path_rows = build_path_rows(trajectory_rows)
    q_values = [
        float(row["q_A_ln_E"]) for row in path_rows
    ]

    write_sorted_ladder(ladder_path, q_values)
    write_path(path_output, path_rows)
    write_struc_i(struc_i_path, q_values)
    write_manifest(
        manifest_path,
        input_path,
        ladder_path,
        path_output,
        struc_i_path,
        path_rows,
    )

    print(f"Created sorted ladder: {ladder_path}")
    print(f"Created direction-preserving path: {path_output}")
    print(f"Created STRUC-I input: {struc_i_path}")
    print(f"Created manifest: {manifest_path}")
    print(f"Elements: {len(q_values)}")
    print(
        f"Range: [{min(q_values):.12g}, {max(q_values):.12g}]"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
