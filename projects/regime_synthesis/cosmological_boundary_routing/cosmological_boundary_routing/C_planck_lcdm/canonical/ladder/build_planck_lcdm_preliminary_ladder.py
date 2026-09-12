#!/usr/bin/env python3
"""
Convert the validated Dataset C Planck-Lambda-CDM trajectory into a
single-column preliminary scalar ladder for STRUC-PERC-I v2.5.0.

Scalar response coordinate:
    q_C(a) = ln(E(a))
    E(a) = H(a) / H0

Input:
    ../../generated_trajectory/validated/planck_lcdm_trajectory_validated.csv

Outputs:
    ../../canonical/ladder/planck_lcdm_response_ladder_preliminary.csv
    ../../canonical/ladder/planck_lcdm_response_ladder_preliminary_manifest.txt

The CSV output has no header and contains exactly one finite number per row,
which is the safest input format for STRUC-PERC-I.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path


DEFAULT_INPUT = (
    Path(__file__).resolve().parent
    / ".."
    / ".."
    / "generated_trajectory"
    / "validated"
    / "planck_lcdm_trajectory_validated.csv"
)

DEFAULT_OUTPUT = (
    Path(__file__).resolve().parent
    / "planck_lcdm_response_ladder_preliminary.csv"
)

DEFAULT_MANIFEST = (
    Path(__file__).resolve().parent
    / "planck_lcdm_response_ladder_preliminary_manifest.txt"
)


def load_response_coordinate(path: Path) -> list[float]:
    values: list[float] = []

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        required = {"E_of_a", "scale_factor", "sample_index"}
        missing = sorted(required - fields)
        if missing:
            raise ValueError(
                "Validated trajectory is missing required column(s): "
                + ", ".join(missing)
            )

        for line_number, row in enumerate(reader, start=2):
            try:
                e_value = float(row["E_of_a"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid E_of_a at CSV line {line_number}"
                ) from exc

            if not math.isfinite(e_value) or e_value <= 0.0:
                raise ValueError(
                    f"E_of_a must be finite and positive at line {line_number}"
                )

            values.append(math.log(e_value))

    if len(values) < 3:
        raise ValueError("At least three trajectory samples are required.")

    return values


def write_ladder(path: Path, values: list[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    # STRUC-PERC-I sorts values internally. Exporting sorted values makes
    # the canonical ladder explicit and independently inspectable.
    ordered = sorted(values)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        for value in ordered:
            writer.writerow([f"{value:.17g}"])


def write_manifest(
    path: Path,
    input_path: Path,
    output_path: Path,
    values: list[float],
) -> None:
    ordered = sorted(values)
    unique_count = len(set(ordered))

    gaps = [
        ordered[i + 1] - ordered[i]
        for i in range(len(ordered) - 1)
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        handle.write("PLANCK LCDM PRELIMINARY STRUC-PERC LADDER MANIFEST\n")
        handle.write("=" * 72 + "\n\n")
        handle.write(f"Input trajectory: {input_path}\n")
        handle.write(f"Output ladder: {output_path}\n\n")
        handle.write("DATASET\n")
        handle.write("Dataset C — Planck-anchored Lambda-CDM expansion\n\n")
        handle.write("SCALAR RESPONSE COORDINATE\n")
        handle.write("q_C(a) = ln(E(a))\n")
        handle.write("E(a) = H(a) / H0\n\n")
        handle.write("STATUS\n")
        handle.write("PRELIMINARY\n")
        handle.write(
            "This is a controlled one-column conversion for an initial "
            "STRUC-PERC-I evaluation.\n"
        )
        handle.write(
            "It is not yet the frozen shared A/B/C canonical ladder definition.\n\n"
        )
        handle.write("COUNTS\n")
        handle.write(f"trajectory samples = {len(values)}\n")
        handle.write(f"ladder elements = {len(ordered)}\n")
        handle.write(f"unique ladder elements = {unique_count}\n")
        handle.write(f"gap count = {len(gaps)}\n\n")
        handle.write("RANGE\n")
        handle.write(f"minimum q_C = {ordered[0]:.17g}\n")
        handle.write(f"maximum q_C = {ordered[-1]:.17g}\n")
        handle.write(
            f"minimum gap = {min(gaps):.17g}\n"
            if gaps else "minimum gap = not available\n"
        )
        handle.write(
            f"maximum gap = {max(gaps):.17g}\n"
            if gaps else "maximum gap = not available\n"
        )
        handle.write("\n")
        handle.write("STRUC-PERC-I SETTINGS\n")
        handle.write("domain adapter = Generic\n")
        handle.write("kappa points = 17\n")
        handle.write("kappa minimum = 0.01\n")
        handle.write("kappa maximum = 1.0\n\n")
        handle.write("IMPORTANT LIMITS\n")
        handle.write(
            "- Do not load the full multi-column trajectory CSV directly "
            "into STRUC-PERC-I.\n"
        )
        handle.write(
            "- This ladder measures the gap geometry of ln(E), not the final "
            "UNNS cosmological margin.\n"
        )
        handle.write(
            "- The result remains sampling-dependent until Datasets A and B "
            "use the same grid and scalar mapping.\n"
        )
        handle.write(
            "- Alpha application must be performed as a separate recorded step.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Convert the validated Planck LCDM trajectory into a preliminary "
            "one-column ln(E) ladder for STRUC-PERC-I."
        )
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    input_path = args.input.resolve()
    output_path = args.output.resolve()
    manifest_path = args.manifest.resolve()

    if not input_path.is_file():
        raise FileNotFoundError(f"Validated trajectory not found: {input_path}")

    values = load_response_coordinate(input_path)
    write_ladder(output_path, values)
    write_manifest(
        manifest_path,
        input_path,
        output_path,
        values,
    )

    print(f"Created ladder: {output_path}")
    print(f"Created manifest: {manifest_path}")
    print(f"Elements: {len(values)}")
    print(f"Range: [{min(values):.12g}, {max(values):.12g}]")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
