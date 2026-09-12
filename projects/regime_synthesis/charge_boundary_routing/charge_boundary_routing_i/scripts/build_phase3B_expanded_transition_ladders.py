#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phase3B_expanded_transition_ladders.py

Charge Boundary Routing I
Phase 3B — Expanded Allowed Transition Corpus

Purpose
-------
Read the Phase 3B expanded allowed-transition corpus and build numeric,
chamber-ready ladders for STRUC-PERC-I and STRUC-I.

Input:

    data/canonical/phase3B_expanded_allowed_transition_corpus.csv

Outputs:

    ladders/phase3B_expanded_transitions/
    ladders/phase3B_expanded_transitions/one_column/
    ladders/phase3B_expanded_transitions/diagnostics/

Run from project root:

    python scripts/build_phase3B_expanded_transition_ladders.py

Important
---------
This script is the Phase 3B counterpart of:

    scripts/build_phase3_transition_ladders.py

It does not rebuild the corpus. Run this first:

    python scripts/build_phase3B_expanded_transition_corpus.py
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


ENCODINGS = [
    "charge_balance_error",
    "initial_total_charge",
    "final_total_charge",
    "charged_multiplicity_delta",
    "neutral_multiplicity_delta",
    "layer_transition_code",
    "route_transition_code",
    "closure_transition_code",
    "category_transition_code",
    "boundary_preservation_code",
    "externalization_delta",
    "composite_count_delta",
    "transition_class_code",
    "transition_family_code",
    "initial_multiplicity",
    "final_multiplicity",
    "charged_initial_count",
    "charged_final_count",
    "neutral_initial_count",
    "neutral_final_count",
    "composite_initial_count",
    "composite_final_count",
    "external_initial_count",
    "external_final_count",
]


FULL_FIELDNAMES = [
    "value",
    "transition_id",
    "transition_name",
    "phase",
    "batch",
    "transition_family",
    "encoding",
    "initial_objects",
    "final_objects",
    "initial_symbols",
    "final_symbols",
    "initial_Q_sum",
    "final_Q_sum",
    "charge_balance_error",
    "charge_conserved",
    "initial_layers",
    "final_layers",
    "layer_transition",
    "route_transition",
    "closure_transition",
    "category_transition",
    "transition_class",
    "source_file",
    "source_note",
    "notes",
]


def project_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing input file: {path}\n"
            "Run scripts/build_phase3B_expanded_transition_corpus.py first."
        )
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def safe_float(value: object) -> float:
    if value is None or str(value).strip() == "":
        return 0.0
    return float(value)


def stable_code(values: Sequence[str]) -> Dict[str, int]:
    """
    Assign deterministic 1-based integer codes to sorted unique values.

    These codes are categorical IDs, not physical magnitudes.
    """
    unique = sorted(set(values))
    return {value: idx + 1 for idx, value in enumerate(unique)}


def unique_count(values: Sequence[float]) -> int:
    return len(set(values))


def write_full_ladder(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FULL_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_one_column(path: Path, values: Sequence[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["value"])
        for value in values:
            writer.writerow([value])


def base_output_row(source: Dict[str, str], encoding: str, value: float) -> Dict[str, object]:
    return {
        "value": value,
        "transition_id": source.get("transition_id", ""),
        "transition_name": source.get("transition_name", ""),
        "phase": source.get("phase", ""),
        "batch": source.get("batch", ""),
        "transition_family": source.get("transition_family", ""),
        "encoding": encoding,
        "initial_objects": source.get("initial_objects", ""),
        "final_objects": source.get("final_objects", ""),
        "initial_symbols": source.get("initial_symbols", ""),
        "final_symbols": source.get("final_symbols", ""),
        "initial_Q_sum": source.get("initial_Q_sum", ""),
        "final_Q_sum": source.get("final_Q_sum", ""),
        "charge_balance_error": source.get("charge_balance_error", ""),
        "charge_conserved": source.get("charge_conserved", ""),
        "initial_layers": source.get("initial_layers", ""),
        "final_layers": source.get("final_layers", ""),
        "layer_transition": source.get("layer_transition", ""),
        "route_transition": source.get("route_transition", ""),
        "closure_transition": source.get("closure_transition", ""),
        "category_transition": source.get("category_transition", ""),
        "transition_class": source.get("transition_class", ""),
        "source_file": source.get("source_file", ""),
        "source_note": source.get("source_note", ""),
        "notes": source.get("notes", ""),
    }


def build_encoding_values(
    rows: Sequence[Dict[str, str]]
) -> Tuple[Dict[str, List[float]], Dict[str, Dict[str, int]]]:
    codebooks: Dict[str, Dict[str, int]] = {}

    codebooks["layer_transition_code"] = stable_code([row["layer_transition"] for row in rows])
    codebooks["route_transition_code"] = stable_code([row["route_transition"] for row in rows])
    codebooks["closure_transition_code"] = stable_code([row["closure_transition"] for row in rows])
    codebooks["category_transition_code"] = stable_code([row["category_transition"] for row in rows])
    codebooks["transition_class_code"] = stable_code([row["transition_class"] for row in rows])
    codebooks["transition_family_code"] = stable_code([row["transition_family"] for row in rows])

    values: Dict[str, List[float]] = {encoding: [] for encoding in ENCODINGS}

    for row in rows:
        values["charge_balance_error"].append(abs(safe_float(row["charge_balance_error"])))
        values["initial_total_charge"].append(safe_float(row["initial_Q_sum"]))
        values["final_total_charge"].append(safe_float(row["final_Q_sum"]))

        values["charged_multiplicity_delta"].append(safe_float(row["charged_multiplicity_delta"]))
        values["neutral_multiplicity_delta"].append(safe_float(row["neutral_multiplicity_delta"]))

        values["layer_transition_code"].append(float(codebooks["layer_transition_code"][row["layer_transition"]]))
        values["route_transition_code"].append(float(codebooks["route_transition_code"][row["route_transition"]]))
        values["closure_transition_code"].append(float(codebooks["closure_transition_code"][row["closure_transition"]]))
        values["category_transition_code"].append(float(codebooks["category_transition_code"][row["category_transition"]]))

        values["boundary_preservation_code"].append(safe_float(row["boundary_preservation_code"]))
        values["externalization_delta"].append(safe_float(row["externalization_delta"]))
        values["composite_count_delta"].append(safe_float(row["composite_count_delta"]))

        values["transition_class_code"].append(float(codebooks["transition_class_code"][row["transition_class"]]))
        values["transition_family_code"].append(float(codebooks["transition_family_code"][row["transition_family"]]))

        values["initial_multiplicity"].append(safe_float(row["initial_multiplicity"]))
        values["final_multiplicity"].append(safe_float(row["final_multiplicity"]))
        values["charged_initial_count"].append(safe_float(row["charged_initial_count"]))
        values["charged_final_count"].append(safe_float(row["charged_final_count"]))
        values["neutral_initial_count"].append(safe_float(row["neutral_initial_count"]))
        values["neutral_final_count"].append(safe_float(row["neutral_final_count"]))
        values["composite_initial_count"].append(safe_float(row["composite_initial_count"]))
        values["composite_final_count"].append(safe_float(row["composite_final_count"]))
        values["external_initial_count"].append(safe_float(row["external_initial_count"]))
        values["external_final_count"].append(safe_float(row["external_final_count"]))

    return values, codebooks


def write_diagnostics(
    diagnostics_dir: Path,
    source_rows: Sequence[Dict[str, str]],
    values_by_encoding: Dict[str, List[float]],
    codebooks: Dict[str, Dict[str, int]],
    written_files: Sequence[str],
    flagged: Sequence[Dict[str, object]],
) -> None:
    diagnostics_dir.mkdir(parents=True, exist_ok=True)

    stats = {}
    for encoding, values in values_by_encoding.items():
        stats[encoding] = {
            "row_count": len(values),
            "unique_values": unique_count(values),
            "min": min(values) if values else None,
            "max": max(values) if values else None,
            "values": values,
        }

    summary = {
        "program": "UNNS Substrate Program",
        "project": "Charge Boundary Routing I",
        "phase": "Phase 3B — Expanded Allowed Transition Corpus",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "input_rows": len(source_rows),
        "encodings_requested": ENCODINGS,
        "files_written": len(written_files),
        "written_files": list(written_files),
        "flagged_constant_or_low_diversity_encodings": list(flagged),
        "codebooks": codebooks,
        "encoding_stats": stats,
        "notes": [
            "Full provenance ladder files preserve transition metadata.",
            "One-column files contain only the numeric value column for chamber upload.",
            "Categorical code values are deterministic IDs, not physical magnitudes.",
            "Constant encodings are retained as diagnostics but should normally be skipped in first chamber runs.",
            "Phase 3B tests robustness of Phase 3 route/closure persistence beyond the 7-transition seed.",
        ],
    }

    (diagnostics_dir / "phase3B_expanded_transition_ladder_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    note_lines = []
    note_lines.append("Charge Boundary Routing I")
    note_lines.append("Phase 3B — Expanded Allowed Transition Corpus")
    note_lines.append("README_phase3B_expanded_transition_ladder_diagnostics.txt")
    note_lines.append("")
    note_lines.append(f"Generated UTC: {summary['generated_utc']}")
    note_lines.append(f"Input rows: {len(source_rows)}")
    note_lines.append(f"Files written: {len(written_files)}")
    note_lines.append("")
    note_lines.append("Purpose:")
    note_lines.append("  Diagnose Phase 3B expanded transition ladder encodings before chamber upload.")
    note_lines.append("")
    note_lines.append("Encoding stats:")
    for encoding in ENCODINGS:
        s = stats[encoding]
        note_lines.append(
            f"- {encoding}: rows={s['row_count']}, unique={s['unique_values']}, "
            f"min={s['min']}, max={s['max']}"
        )

    note_lines.append("")
    note_lines.append("Flagged constant / low-diversity encodings:")
    if flagged:
        for item in flagged:
            note_lines.append(
                f"- {item['encoding']}: {item['reason']}; "
                f"unique={item['unique_values']}; values={item['values']}"
            )
    else:
        note_lines.append("- none")

    note_lines.append("")
    note_lines.append("Codebooks:")
    for codebook_name, codebook in codebooks.items():
        note_lines.append("")
        note_lines.append(codebook_name + ":")
        for label, code in codebook.items():
            note_lines.append(f"  {code}: {label}")

    note_lines.append("")
    note_lines.append("Recommended first chamber inputs:")
    note_lines.append("  Use non-constant one-column ladders from:")
    note_lines.append("    ladders/phase3B_expanded_transitions/one_column/")
    note_lines.append("")
    note_lines.append("Usually skip first if constant:")
    note_lines.append("  charge_balance_error")
    note_lines.append("  boundary_preservation_code")
    note_lines.append("")
    note_lines.append("Primary Phase 3B robustness targets:")
    note_lines.append("  route_transition_code")
    note_lines.append("  closure_transition_code")
    note_lines.append("  transition_class_code")
    note_lines.append("  transition_family_code")
    note_lines.append("  category_transition_code")

    (diagnostics_dir / "README_phase3B_expanded_transition_ladder_diagnostics.txt").write_text(
        "\n".join(note_lines),
        encoding="utf-8",
    )


def main() -> int:
    root = project_root_from_script()

    input_csv = root / "data" / "canonical" / "phase3B_expanded_allowed_transition_corpus.csv"
    out_dir = root / "ladders" / "phase3B_expanded_transitions"
    one_col_dir = out_dir / "one_column"
    diagnostics_dir = out_dir / "diagnostics"

    source_rows = read_csv(input_csv)
    if not source_rows:
        raise ValueError(f"Input corpus is empty: {input_csv}")

    values_by_encoding, codebooks = build_encoding_values(source_rows)

    written_files: List[str] = []
    flagged: List[Dict[str, object]] = []

    for encoding in ENCODINGS:
        values = values_by_encoding[encoding]
        u_count = unique_count(values)

        if u_count < 2:
            flagged.append({
                "encoding": encoding,
                "reason": "constant_seed_or_invariant_encoding",
                "unique_values": u_count,
                "values": sorted(set(values)),
            })

        full_rows = [
            base_output_row(source, encoding, value)
            for source, value in zip(source_rows, values)
        ]

        full_path = out_dir / f"phase3B_expanded_transition_ladder_{encoding}.csv"
        one_col_path = one_col_dir / f"phase3B_expanded_transition_ladder_{encoding}.csv"

        write_full_ladder(full_path, full_rows)
        write_one_column(one_col_path, values)

        written_files.append(str(full_path.relative_to(root)))
        written_files.append(str(one_col_path.relative_to(root)))

    write_diagnostics(
        diagnostics_dir=diagnostics_dir,
        source_rows=source_rows,
        values_by_encoding=values_by_encoding,
        codebooks=codebooks,
        written_files=written_files,
        flagged=flagged,
    )

    print("Phase 3B expanded transition ladders generated.")
    print(f"Project root: {root}")
    print(f"Input: {input_csv.relative_to(root)}")
    print(f"Output: {out_dir.relative_to(root)}")
    print(f"One-column: {one_col_dir.relative_to(root)}")
    print(f"Diagnostics: {diagnostics_dir.relative_to(root)}")
    print("")
    print(f"Input rows: {len(source_rows)}")
    print(f"Encodings: {len(ENCODINGS)}")
    print(f"Files written: {len(written_files)}")
    print(f"Flagged constant/low-diversity encodings: {len(flagged)}")

    if flagged:
        print("")
        print("Flagged encodings:")
        for item in flagged:
            print(f"  - {item['encoding']}: {item['reason']}")

    print("")
    print("Next:")
    print("  Upload selected non-constant one-column Phase 3B files to STRUC-PERC-I first, then STRUC-I.")
    print("")
    print("Primary robustness targets:")
    print("  phase3B_expanded_transition_ladder_route_transition_code.csv")
    print("  phase3B_expanded_transition_ladder_closure_transition_code.csv")
    print("  phase3B_expanded_transition_ladder_transition_class_code.csv")
    print("  phase3B_expanded_transition_ladder_transition_family_code.csv")
    print("  phase3B_expanded_transition_ladder_category_transition_code.csv")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
