#!/usr/bin/env python3
"""
build_lqc_bounce_preliminary_ladder.py

Build Dataset B preliminary structural representations from the validated
effective LQC bounce trajectory.

Input:
    ../../generated_trajectory/validated/
    lqc_bounce_trajectory_validated_v2_2.csv

Outputs:
    lqc_bounce_response_path_preliminary.csv
    lqc_bounce_expansion_ladder_preliminary.csv
    lqc_bounce_expansion_ladder_preliminary_struc_i.csv
    lqc_bounce_ladder_preliminary_manifest.txt

Representation policy:
1. Preserve the full 4001-row contraction -> bounce -> expansion path.
2. Build the direct scalar ladder from the finite post-bounce expansion branch
   only, excluding the exact bounce row where E_lqc = 0.
3. Do not duplicate the contraction branch in the sorted scalar ladder because
   contraction and expansion have the same |H| values in reverse order.
4. Do not replace the exact bounce with an arbitrary epsilon.

Scalar coordinate:
    q_B(a) = ln(E_lqc(a))

No third-party packages are required.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path
from typing import Dict, List, Sequence


HERE = Path(__file__).resolve().parent

DEFAULT_INPUT = (
    HERE
    / ".."
    / ".."
    / "generated_trajectory"
    / "validated"
    / "lqc_bounce_trajectory_validated_v2_2.csv"
)

DEFAULT_PATH_OUTPUT = (
    HERE
    / "lqc_bounce_response_path_preliminary.csv"
)

DEFAULT_LADDER_OUTPUT = (
    HERE
    / "lqc_bounce_expansion_ladder_preliminary.csv"
)

DEFAULT_STRUC_I_OUTPUT = (
    HERE
    / "lqc_bounce_expansion_ladder_preliminary_struc_i.csv"
)

DEFAULT_MANIFEST_OUTPUT = (
    HERE
    / "lqc_bounce_ladder_preliminary_manifest.txt"
)


PATH_COLUMNS = [
    "path_index",
    "source_sample_index",
    "branch_local_index",
    "branch",
    "time_relative_to_bounce_Gyr",
    "distance_to_bounce_Gyr",
    "sampling_region",
    "x_bounce_distance",
    "scale_factor",
    "ln_scale_factor",
    "redshift_equivalent",
    "H_signed_km_s_Mpc",
    "H_magnitude_km_s_Mpc",
    "E_classical_of_a",
    "E_lqc_of_a",
    "E2_lqc_of_a",
    "q_B_ln_E_lqc",
    "rho_total_relative_to_rho_crit0",
    "rho_over_rho_c",
    "lqc_correction_factor",
    "fraction_matter_at_a",
    "fraction_radiation_at_a",
    "fraction_lambda_at_a",
    "effective_ricci_over_6H0sq",
    "boundary_margin_candidate",
    "distance_from_bounce_log_a",
    "is_exact_bounce",
]


def parse_float(
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


def load_validated_trajectory(
    path: Path,
) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = set(reader.fieldnames or [])

    required = {
        "sample_index",
        "branch_local_index",
        "branch",
        "time_relative_to_bounce_Gyr",
        "distance_to_bounce_Gyr",
        "sampling_region",
        "x_bounce_distance",
        "scale_factor",
        "ln_scale_factor",
        "redshift_equivalent",
        "H_signed_km_s_Mpc",
        "H_magnitude_km_s_Mpc",
        "E_classical_of_a",
        "E_lqc_of_a",
        "E2_lqc_of_a",
        "rho_total_relative_to_rho_crit0",
        "rho_over_rho_c",
        "lqc_correction_factor",
        "fraction_matter_at_a",
        "fraction_radiation_at_a",
        "fraction_lambda_at_a",
        "effective_ricci_over_6H0sq",
        "boundary_margin_candidate",
        "distance_from_bounce_log_a",
        "is_exact_bounce",
    }

    missing = sorted(required - fields)
    if missing:
        raise ValueError(
            "Validated trajectory is missing required column(s): "
            + ", ".join(missing)
        )

    if len(rows) < 3:
        raise ValueError("Validated trajectory is too short.")

    return rows


def build_path_rows(
    rows: Sequence[Dict[str, str]],
) -> List[Dict[str, object]]:
    output: List[Dict[str, object]] = []
    bounce_count = 0

    for path_index, row in enumerate(rows):
        line_number = path_index + 2

        branch = (row.get("branch") or "").strip()
        is_bounce = (
            (row.get("is_exact_bounce") or "").strip().lower()
            == "yes"
        )

        e_lqc = parse_float(row, "E_lqc_of_a", line_number)
        if e_lqc < 0.0:
            raise ValueError(
                f"E_lqc_of_a must be non-negative at line {line_number}"
            )

        if is_bounce:
            bounce_count += 1
            q_value: object = ""
            if e_lqc != 0.0:
                raise ValueError(
                    "Exact bounce row must have E_lqc_of_a = 0."
                )
        else:
            if e_lqc <= 0.0:
                raise ValueError(
                    f"Non-bounce row must have E_lqc_of_a > 0 "
                    f"at line {line_number}"
                )
            q_value = math.log(e_lqc)

        output.append(
            {
                "path_index": path_index,
                "source_sample_index": row["sample_index"],
                "branch_local_index": row["branch_local_index"],
                "branch": branch,
                "time_relative_to_bounce_Gyr": parse_float(
                    row,
                    "time_relative_to_bounce_Gyr",
                    line_number,
                ),
                "distance_to_bounce_Gyr": parse_float(
                    row,
                    "distance_to_bounce_Gyr",
                    line_number,
                ),
                "sampling_region": row["sampling_region"],
                "x_bounce_distance": parse_float(
                    row,
                    "x_bounce_distance",
                    line_number,
                ),
                "scale_factor": parse_float(
                    row,
                    "scale_factor",
                    line_number,
                ),
                "ln_scale_factor": parse_float(
                    row,
                    "ln_scale_factor",
                    line_number,
                ),
                "redshift_equivalent": parse_float(
                    row,
                    "redshift_equivalent",
                    line_number,
                ),
                "H_signed_km_s_Mpc": parse_float(
                    row,
                    "H_signed_km_s_Mpc",
                    line_number,
                ),
                "H_magnitude_km_s_Mpc": parse_float(
                    row,
                    "H_magnitude_km_s_Mpc",
                    line_number,
                ),
                "E_classical_of_a": parse_float(
                    row,
                    "E_classical_of_a",
                    line_number,
                ),
                "E_lqc_of_a": e_lqc,
                "E2_lqc_of_a": parse_float(
                    row,
                    "E2_lqc_of_a",
                    line_number,
                ),
                "q_B_ln_E_lqc": q_value,
                "rho_total_relative_to_rho_crit0": parse_float(
                    row,
                    "rho_total_relative_to_rho_crit0",
                    line_number,
                ),
                "rho_over_rho_c": parse_float(
                    row,
                    "rho_over_rho_c",
                    line_number,
                ),
                "lqc_correction_factor": parse_float(
                    row,
                    "lqc_correction_factor",
                    line_number,
                ),
                "fraction_matter_at_a": parse_float(
                    row,
                    "fraction_matter_at_a",
                    line_number,
                ),
                "fraction_radiation_at_a": parse_float(
                    row,
                    "fraction_radiation_at_a",
                    line_number,
                ),
                "fraction_lambda_at_a": parse_float(
                    row,
                    "fraction_lambda_at_a",
                    line_number,
                ),
                "effective_ricci_over_6H0sq": parse_float(
                    row,
                    "effective_ricci_over_6H0sq",
                    line_number,
                ),
                "boundary_margin_candidate": parse_float(
                    row,
                    "boundary_margin_candidate",
                    line_number,
                ),
                "distance_from_bounce_log_a": parse_float(
                    row,
                    "distance_from_bounce_log_a",
                    line_number,
                ),
                "is_exact_bounce": "yes" if is_bounce else "no",
            }
        )

    if bounce_count != 1:
        raise ValueError(
            f"Expected exactly one exact bounce row, found {bounce_count}."
        )

    return output


def select_expansion_ladder(
    path_rows: Sequence[Dict[str, object]],
) -> List[float]:
    values: List[float] = []

    for row in path_rows:
        if row["branch"] != "expansion":
            continue
        if row["is_exact_bounce"] == "yes":
            continue

        q_raw = row["q_B_ln_E_lqc"]
        if q_raw == "":
            continue

        value = float(q_raw)
        if not math.isfinite(value):
            raise ValueError("Non-finite q_B value in expansion branch.")
        values.append(value)

    if len(values) < 3:
        raise ValueError(
            "Expansion ladder contains too few finite values."
        )

    return values


def write_path(
    path: Path,
    rows: Sequence[Dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=PATH_COLUMNS,
        )
        writer.writeheader()

        for row in rows:
            serial: Dict[str, object] = {}
            for field in PATH_COLUMNS:
                value = row[field]
                if isinstance(value, float):
                    serial[field] = f"{value:.17g}"
                else:
                    serial[field] = value
            writer.writerow(serial)


def write_headerless_ladder(
    path: Path,
    values: Sequence[float],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    ordered = sorted(values)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        for value in ordered:
            writer.writerow([f"{value:.17g}"])


def write_struc_i_ladder(
    path: Path,
    values: Sequence[float],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    ordered = sorted(values)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["value"])
        for value in ordered:
            writer.writerow([f"{value:.17g}"])


def is_strictly_increasing(values: Sequence[float]) -> bool:
    return all(
        values[index + 1] > values[index]
        for index in range(len(values) - 1)
    )


def is_strictly_decreasing(values: Sequence[float]) -> bool:
    return all(
        values[index + 1] < values[index]
        for index in range(len(values) - 1)
    )


def write_manifest(
    path: Path,
    input_path: Path,
    path_output: Path,
    ladder_output: Path,
    struc_i_output: Path,
    path_rows: Sequence[Dict[str, object]],
    ladder_values: Sequence[float],
) -> None:
    ordered = sorted(ladder_values)
    gaps = [
        ordered[index + 1] - ordered[index]
        for index in range(len(ordered) - 1)
    ]

    bounce_indices = [
        int(row["path_index"])
        for row in path_rows
        if row["is_exact_bounce"] == "yes"
    ]
    bounce_index = bounce_indices[0]

    contraction = [
        row for row in path_rows
        if row["branch"] == "contraction"
    ]
    expansion = [
        row for row in path_rows
        if row["branch"] == "expansion"
    ]

    contraction_a = [
        float(row["scale_factor"]) for row in contraction
    ]
    expansion_a = [
        float(row["scale_factor"]) for row in expansion
    ]
    contraction_h = [
        float(row["H_signed_km_s_Mpc"]) for row in contraction
    ]
    expansion_h = [
        float(row["H_signed_km_s_Mpc"]) for row in expansion
        if row["is_exact_bounce"] != "yes"
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        handle.write(
            "DATASET B PRELIMINARY STRUCTURAL REPRESENTATION MANIFEST\n"
        )
        handle.write("=" * 72 + "\n\n")

        handle.write(f"Input trajectory: {input_path}\n")
        handle.write(f"Full path output: {path_output}\n")
        handle.write(f"Expansion ladder: {ladder_output}\n")
        handle.write(f"STRUC-I ladder: {struc_i_output}\n\n")

        handle.write("DATASET\n")
        handle.write(
            "Dataset B — effective LQC contraction-bounce-expansion\n\n"
        )

        handle.write("SCALAR COORDINATE\n")
        handle.write("q_B(a) = ln(E_lqc(a))\n\n")

        handle.write("REPRESENTATION POLICY\n")
        handle.write(
            "1. Full direction-preserving path retains all trajectory rows.\n"
        )
        handle.write(
            "2. Exact bounce remains in the path with q_B left blank because "
            "ln(0) is undefined.\n"
        )
        handle.write(
            "3. Direct scalar ladder uses only finite post-bounce expansion "
            "rows.\n"
        )
        handle.write(
            "4. Contraction rows are excluded from the scalar ladder to avoid "
            "duplicating the same |H| values and creating artificial zero gaps.\n"
        )
        handle.write(
            "5. No epsilon replacement is used at the bounce.\n\n"
        )

        handle.write("COUNTS\n")
        handle.write(f"full path rows = {len(path_rows)}\n")
        handle.write(f"contraction rows = {len(contraction)}\n")
        handle.write(f"expansion rows = {len(expansion)}\n")
        handle.write(f"exact bounce rows = {len(bounce_indices)}\n")
        handle.write(f"bounce path index = {bounce_index}\n")
        handle.write(
            f"finite expansion ladder elements = {len(ordered)}\n"
        )
        handle.write(f"ladder gaps = {len(gaps)}\n")
        handle.write(
            f"unique ladder elements = {len(set(ordered))}\n\n"
        )

        handle.write("LADDER RANGE\n")
        handle.write(
            f"minimum q_B = {ordered[0]:.17g}\n"
        )
        handle.write(
            f"maximum q_B = {ordered[-1]:.17g}\n"
        )
        handle.write(
            f"minimum gap = {min(gaps):.17g}\n"
        )
        handle.write(
            f"maximum gap = {max(gaps):.17g}\n\n"
        )

        handle.write("PATH CHECKS\n")
        handle.write(
            "contraction scale factor decreasing = "
            f"{'yes' if is_strictly_decreasing(contraction_a) else 'no'}\n"
        )
        handle.write(
            "expansion scale factor increasing = "
            f"{'yes' if is_strictly_increasing(expansion_a) else 'no'}\n"
        )
        handle.write(
            "contraction H negative = "
            f"{'yes' if all(value < 0 for value in contraction_h) else 'no'}\n"
        )
        handle.write(
            "post-bounce expansion H positive = "
            f"{'yes' if all(value > 0 for value in expansion_h) else 'no'}\n\n"
        )

        handle.write("STRUC-PERC-I SETTINGS\n")
        handle.write("input = lqc_bounce_expansion_ladder_preliminary.csv\n")
        handle.write("domain adapter = Generic\n")
        handle.write("kappa points = 17\n")
        handle.write("kappa minimum = 0.01\n")
        handle.write("kappa maximum = 1.0\n\n")

        handle.write("STRUC-I SETTINGS\n")
        handle.write(
            "input = "
            "lqc_bounce_expansion_ladder_preliminary_struc_i.csv\n"
        )
        handle.write("maximum ladder size = 5000\n")
        handle.write("Monte Carlo runs = 2000\n")
        handle.write("kappa steps = 40\n")
        handle.write("kappa minimum = 0.01\n")
        handle.write("kappa maximum = 1.0\n\n")

        handle.write("INTERPRETIVE LIMITS\n")
        handle.write(
            "- The direct scalar ladder describes only the finite expansion "
            "branch.\n"
        )
        handle.write(
            "- The bounce cannot be represented by ln(E_lqc) because E_lqc=0.\n"
        )
        handle.write(
            "- The full path is mandatory for alpha analysis and the final "
            "orientation-sensitive A/B/C bridge.\n"
        )
        handle.write(
            "- boundary_margin_candidate remains provisional.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build Dataset B direction-preserving bounce path and finite "
            "post-bounce expansion ladder."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
    )
    parser.add_argument(
        "--path-output",
        type=Path,
        default=DEFAULT_PATH_OUTPUT,
    )
    parser.add_argument(
        "--ladder-output",
        type=Path,
        default=DEFAULT_LADDER_OUTPUT,
    )
    parser.add_argument(
        "--struc-i-output",
        type=Path,
        default=DEFAULT_STRUC_I_OUTPUT,
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        default=DEFAULT_MANIFEST_OUTPUT,
    )
    args = parser.parse_args()

    input_path = args.input.resolve()
    path_output = args.path_output.resolve()
    ladder_output = args.ladder_output.resolve()
    struc_i_output = args.struc_i_output.resolve()
    manifest_output = args.manifest_output.resolve()

    if not input_path.is_file():
        raise FileNotFoundError(
            f"Validated Dataset B trajectory not found: {input_path}"
        )

    source_rows = load_validated_trajectory(input_path)
    path_rows = build_path_rows(source_rows)
    ladder_values = select_expansion_ladder(path_rows)

    write_path(path_output, path_rows)
    write_headerless_ladder(ladder_output, ladder_values)
    write_struc_i_ladder(struc_i_output, ladder_values)
    write_manifest(
        manifest_output,
        input_path,
        path_output,
        ladder_output,
        struc_i_output,
        path_rows,
        ladder_values,
    )

    print(f"Created full bounce path: {path_output}")
    print(f"Created expansion ladder: {ladder_output}")
    print(f"Created STRUC-I input: {struc_i_output}")
    print(f"Created manifest: {manifest_output}")
    print(f"Full path rows: {len(path_rows)}")
    print(f"Finite expansion ladder elements: {len(ladder_values)}")
    print(
        f"Ladder range: "
        f"[{min(ladder_values):.12g}, {max(ladder_values):.12g}]"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
