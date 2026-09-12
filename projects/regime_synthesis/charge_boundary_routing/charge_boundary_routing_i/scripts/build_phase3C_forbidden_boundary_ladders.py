#!/usr/bin/env python3
"""
build_phase3C_forbidden_boundary_ladders.py

Charge Boundary Routing I
Phase 3C — Constrained and Forbidden Transition Boundary Tests

Purpose
-------
Reads:

    data/canonical/phase3C_forbidden_constrained_transition_corpus.csv

Writes:

    data/derived/phase3C_forbidden_constrained_transition_summary.json

    ladders/phase3C_forbidden_boundary/
        phase3C_ladder_<encoding>.csv

    ladders/phase3C_forbidden_boundary/one_column/
        phase3C_ladder_<encoding>.csv

    ladders/phase3C_forbidden_boundary/diagnostics/
        phase3C_encoding_manifest.csv
        phase3C_category_codebook.json
        phase3C_transition_audit.csv
        phase3C_balance_check.csv
        phase3C_group_counts.json
        phase3C_expected_behavior_summary.json

Also prepares:

    results/struc_perc_i/phase3C_forbidden_boundary/
    results/struc_i/phase3C_forbidden_boundary/
    outputs/reports/phase3C_forbidden_boundary/

Run from project root:

    python scripts/build_phase3C_forbidden_boundary_ladders.py
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_CSV = PROJECT_ROOT / "data" / "canonical" / "phase3C_forbidden_constrained_transition_corpus.csv"
DERIVED_DIR = PROJECT_ROOT / "data" / "derived"
LADDER_DIR = PROJECT_ROOT / "ladders" / "phase3C_forbidden_boundary"
ONE_COLUMN_DIR = LADDER_DIR / "one_column"
DIAGNOSTICS_DIR = LADDER_DIR / "diagnostics"
STRUC_PERC_RESULTS_DIR = PROJECT_ROOT / "results" / "struc_perc_i" / "phase3C_forbidden_boundary"
STRUC_I_RESULTS_DIR = PROJECT_ROOT / "results" / "struc_i" / "phase3C_forbidden_boundary"
REPORT_DIR = PROJECT_ROOT / "outputs" / "reports" / "phase3C_forbidden_boundary"


# These are the primary encodings recommended for first chamber pass.
PRIMARY_ENCODINGS = [
    "route_charge_consistency_code",
    "closure_charge_consistency_code",
    "allowed_vs_forbidden_code",
    "boundary_pressure_index",
    "boundary_response_code",
    "route_transition_code",
    "closure_transition_code",
    "transition_class_code",
    "transition_status_code",
    "charge_balance_abs_error",
    "electric_charge_violation_flag",
    "free_fractional_externalization_flag",
    "selection_violation_flag",
    "route_incoherence_flag",
    "forbidden_flag",
]

# Secondary encodings are useful once primary contrast is checked.
SECONDARY_ENCODINGS = [
    "initial_total_charge",
    "final_total_charge",
    "charge_balance_error",
    "charge_balance_code",
    "layer_transition_code",
    "category_transition_code",
    "transition_family_code",
    "initial_multiplicity",
    "final_multiplicity",
    "multiplicity_delta",
    "initial_charged_multiplicity",
    "final_charged_multiplicity",
    "charged_multiplicity_delta",
    "initial_neutral_multiplicity",
    "final_neutral_multiplicity",
    "neutral_multiplicity_delta",
    "initial_composite_count",
    "final_composite_count",
    "composite_count_delta",
    "initial_external_count",
    "final_external_count",
    "external_count_delta",
    "initial_fractional_external_count",
    "final_fractional_external_count",
    "fractional_external_count_delta",
    "constrained_flag",
    "boundary_candidate_flag",
    "allowed_control_flag",
]

ALL_ENCODINGS = PRIMARY_ENCODINGS + [x for x in SECONDARY_ENCODINGS if x not in PRIMARY_ENCODINGS]

CODEBOOK_COLUMNS = [
    "phase3C_group",
    "group_name",
    "transition_status",
    "transition_family",
    "transition_class",
    "charge_balance_code",
    "layer_transition_label",
    "route_transition_label",
    "closure_transition_label",
    "category_transition_label",
    "expected_boundary_response",
    "expected_chamber_behavior",
    "source_basis",
]


def ensure_dirs() -> None:
    for path in [
        DERIVED_DIR,
        LADDER_DIR,
        ONE_COLUMN_DIR,
        DIAGNOSTICS_DIR,
        STRUC_PERC_RESULTS_DIR,
        STRUC_I_RESULTS_DIR,
        REPORT_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required corpus file not found:\n  {path}\n\n"
            "Place phase3C_forbidden_constrained_transition_corpus.csv at:\n"
            "  data/canonical/phase3C_forbidden_constrained_transition_corpus.csv\n"
            "then rerun this script."
        )

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError(f"Input CSV has no rows: {path}")

    return rows


def is_number(value: Any) -> bool:
    try:
        float(str(value).strip())
        return True
    except (TypeError, ValueError):
        return False


def to_float(value: Any) -> float:
    return float(str(value).strip())


def numeric_stats(values: List[float]) -> Dict[str, Any]:
    n = len(values)
    n_unique = len(set(values))
    if n == 0:
        return {
            "n_rows": 0,
            "n_unique": 0,
            "min": "",
            "max": "",
            "mean": "",
            "is_constant": True,
        }
    return {
        "n_rows": n,
        "n_unique": n_unique,
        "min": min(values),
        "max": max(values),
        "mean": sum(values) / n,
        "is_constant": n_unique <= 1,
    }


def write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_ladders(rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    manifest: List[Dict[str, Any]] = []

    for encoding in ALL_ENCODINGS:
        if encoding not in rows[0]:
            manifest.append({
                "encoding_name": encoding,
                "source_column": encoding,
                "value_type": "missing",
                "n_rows": 0,
                "n_unique": 0,
                "min": "",
                "max": "",
                "mean": "",
                "is_constant": True,
                "recommended_for_struc_perc": 0,
                "recommended_for_struc_i": 0,
                "notes": "missing from source corpus",
            })
            continue

        raw_values = [r.get(encoding, "") for r in rows]
        numeric_ok = all(is_number(v) for v in raw_values)

        if not numeric_ok:
            manifest.append({
                "encoding_name": encoding,
                "source_column": encoding,
                "value_type": "non_numeric",
                "n_rows": len(raw_values),
                "n_unique": len(set(raw_values)),
                "min": "",
                "max": "",
                "mean": "",
                "is_constant": len(set(raw_values)) <= 1,
                "recommended_for_struc_perc": 0,
                "recommended_for_struc_i": 0,
                "notes": "non-numeric; not exported as chamber ladder",
            })
            continue

        values = [to_float(v) for v in raw_values]
        stats = numeric_stats(values)
        is_constant = bool(stats["is_constant"])

        full_rows = []
        one_col_rows = []

        for idx, (row, value) in enumerate(zip(rows, values), start=1):
            full_rows.append({
                "row_index": idx,
                "transition_id": row.get("transition_id", ""),
                "transition_label": row.get("transition_label", ""),
                "phase3C_group": row.get("phase3C_group", ""),
                "group_name": row.get("group_name", ""),
                "transition_status": row.get("transition_status", ""),
                "expected_boundary_response": row.get("expected_boundary_response", ""),
                encoding: value,
            })
            one_col_rows.append({encoding: value})

        full_path = LADDER_DIR / f"phase3C_ladder_{encoding}.csv"
        one_path = ONE_COLUMN_DIR / f"phase3C_ladder_{encoding}.csv"

        write_csv(
            full_path,
            full_rows,
            [
                "row_index",
                "transition_id",
                "transition_label",
                "phase3C_group",
                "group_name",
                "transition_status",
                "expected_boundary_response",
                encoding,
            ],
        )
        write_csv(one_path, one_col_rows, [encoding])

        notes = []
        if encoding in PRIMARY_ENCODINGS:
            notes.append("primary")
        else:
            notes.append("secondary")
        if is_constant:
            notes.append("constant_or_single_value; avoid first-pass chamber upload")
        elif stats["n_unique"] < 2:
            notes.append("n_unique<2; avoid first-pass chamber upload")

        manifest.append({
            "encoding_name": encoding,
            "source_column": encoding,
            "value_type": "numeric",
            "n_rows": stats["n_rows"],
            "n_unique": stats["n_unique"],
            "min": stats["min"],
            "max": stats["max"],
            "mean": stats["mean"],
            "is_constant": int(is_constant),
            "recommended_for_struc_perc": int((not is_constant) and encoding in PRIMARY_ENCODINGS),
            "recommended_for_struc_i": int((not is_constant) and encoding in PRIMARY_ENCODINGS),
            "notes": "; ".join(notes),
        })

    return manifest


def build_codebook(rows: List[Dict[str, str]]) -> Dict[str, Dict[str, int]]:
    codebook: Dict[str, Dict[str, int]] = {}
    for col in CODEBOOK_COLUMNS:
        if col not in rows[0]:
            continue
        values = sorted(set(r.get(col, "") for r in rows))
        codebook[col] = {value: idx for idx, value in enumerate(values)}
    return codebook


def build_transition_audit(rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    audit_rows: List[Dict[str, Any]] = []
    for row in rows:
        error = to_float(row.get("charge_balance_error", "nan"))
        expected_balanced = 0 if int(float(row.get("electric_charge_violation_flag", "0"))) else 1
        balance_status = "balanced" if abs(error) < 1e-12 else "charge_violating"

        audit_rows.append({
            "transition_id": row.get("transition_id", ""),
            "transition_label": row.get("transition_label", ""),
            "phase3C_group": row.get("phase3C_group", ""),
            "group_name": row.get("group_name", ""),
            "transition_status": row.get("transition_status", ""),
            "initial_state": row.get("initial_state", ""),
            "final_state": row.get("final_state", ""),
            "Qi": row.get("initial_total_charge", ""),
            "Qf": row.get("final_total_charge", ""),
            "charge_balance_error": row.get("charge_balance_error", ""),
            "electric_charge_violation_flag": row.get("electric_charge_violation_flag", ""),
            "free_fractional_externalization_flag": row.get("free_fractional_externalization_flag", ""),
            "selection_violation_flag": row.get("selection_violation_flag", ""),
            "route_incoherence_flag": row.get("route_incoherence_flag", ""),
            "constrained_flag": row.get("constrained_flag", ""),
            "boundary_candidate_flag": row.get("boundary_candidate_flag", ""),
            "forbidden_flag": row.get("forbidden_flag", ""),
            "allowed_control_flag": row.get("allowed_control_flag", ""),
            "expected_boundary_response": row.get("expected_boundary_response", ""),
            "expected_chamber_behavior": row.get("expected_chamber_behavior", ""),
            "audit_status": balance_status,
            "notes": row.get("notes", ""),
        })

    return audit_rows


def build_balance_check(rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        err = to_float(row.get("charge_balance_error", "nan"))
        expected_balanced = 0 if int(float(row.get("electric_charge_violation_flag", "0"))) else 1
        balance_status = "PASS_BALANCED" if abs(err) < 1e-12 else "FAIL_CHARGE_VIOLATION"
        if expected_balanced == 0 and abs(err) >= 1e-12:
            expectation_status = "EXPECTED_VIOLATION"
        elif expected_balanced == 1 and abs(err) < 1e-12:
            expectation_status = "EXPECTED_BALANCED"
        else:
            expectation_status = "CHECK_CLASSIFICATION"

        out.append({
            "transition_id": row.get("transition_id", ""),
            "initial_state": row.get("initial_state", ""),
            "final_state": row.get("final_state", ""),
            "Qi": row.get("initial_total_charge", ""),
            "Qf": row.get("final_total_charge", ""),
            "error": row.get("charge_balance_error", ""),
            "abs_error": row.get("charge_balance_abs_error", ""),
            "expected_balanced": expected_balanced,
            "balance_status": balance_status,
            "expectation_status": expectation_status,
        })
    return out


def counts_by(rows: List[Dict[str, str]], col: str) -> Dict[str, int]:
    return dict(Counter(r.get(col, "") for r in rows))


def build_summary(rows: List[Dict[str, str]], manifest: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(rows)
    charge_balanced = sum(1 for r in rows if abs(to_float(r.get("charge_balance_error", "0"))) < 1e-12)
    charge_violating = total - charge_balanced

    return {
        "project": "Charge Boundary Routing I",
        "phase": "Phase 3C — Constrained and Forbidden Transition Boundary Tests",
        "input_csv": str(INPUT_CSV.relative_to(PROJECT_ROOT)),
        "rows": total,
        "columns": len(rows[0]) if rows else 0,
        "charge_balanced_rows": charge_balanced,
        "charge_violating_rows": charge_violating,
        "group_counts": counts_by(rows, "phase3C_group"),
        "group_name_counts": counts_by(rows, "group_name"),
        "transition_status_counts": counts_by(rows, "transition_status"),
        "transition_family_counts": counts_by(rows, "transition_family"),
        "transition_class_counts": counts_by(rows, "transition_class"),
        "expected_boundary_response_counts": counts_by(rows, "expected_boundary_response"),
        "expected_chamber_behavior_counts": counts_by(rows, "expected_chamber_behavior"),
        "flag_counts": {
            flag: sum(int(float(r.get(flag, 0))) for r in rows)
            for flag in [
                "electric_charge_violation_flag",
                "free_fractional_externalization_flag",
                "selection_violation_flag",
                "route_incoherence_flag",
                "constrained_flag",
                "boundary_candidate_flag",
                "forbidden_flag",
                "allowed_control_flag",
            ]
        },
        "ladders_written": len([m for m in manifest if m.get("value_type") == "numeric"]),
        "primary_ladders_recommended": [
            m["encoding_name"] for m in manifest
            if int(m.get("recommended_for_struc_perc", 0)) == 1
        ],
        "constant_or_avoid_first_pass": [
            m["encoding_name"] for m in manifest
            if int(m.get("is_constant", 0)) == 1
        ],
        "output_directories": {
            "derived": str(DERIVED_DIR.relative_to(PROJECT_ROOT)),
            "ladders": str(LADDER_DIR.relative_to(PROJECT_ROOT)),
            "one_column": str(ONE_COLUMN_DIR.relative_to(PROJECT_ROOT)),
            "diagnostics": str(DIAGNOSTICS_DIR.relative_to(PROJECT_ROOT)),
            "struc_perc_results": str(STRUC_PERC_RESULTS_DIR.relative_to(PROJECT_ROOT)),
            "struc_i_results": str(STRUC_I_RESULTS_DIR.relative_to(PROJECT_ROOT)),
            "reports": str(REPORT_DIR.relative_to(PROJECT_ROOT)),
        },
    }


def main() -> None:
    ensure_dirs()
    rows = read_csv(INPUT_CSV)

    manifest = write_ladders(rows)

    write_csv(
        DIAGNOSTICS_DIR / "phase3C_encoding_manifest.csv",
        manifest,
        [
            "encoding_name",
            "source_column",
            "value_type",
            "n_rows",
            "n_unique",
            "min",
            "max",
            "mean",
            "is_constant",
            "recommended_for_struc_perc",
            "recommended_for_struc_i",
            "notes",
        ],
    )

    codebook = build_codebook(rows)
    with (DIAGNOSTICS_DIR / "phase3C_category_codebook.json").open("w", encoding="utf-8") as f:
        json.dump(codebook, f, indent=2, ensure_ascii=False)

    transition_audit = build_transition_audit(rows)
    write_csv(
        DIAGNOSTICS_DIR / "phase3C_transition_audit.csv",
        transition_audit,
        list(transition_audit[0].keys()),
    )

    balance_check = build_balance_check(rows)
    write_csv(
        DIAGNOSTICS_DIR / "phase3C_balance_check.csv",
        balance_check,
        list(balance_check[0].keys()),
    )

    group_counts = {
        "phase3C_group": counts_by(rows, "phase3C_group"),
        "group_name": counts_by(rows, "group_name"),
        "transition_status": counts_by(rows, "transition_status"),
        "transition_family": counts_by(rows, "transition_family"),
        "transition_class": counts_by(rows, "transition_class"),
        "expected_boundary_response": counts_by(rows, "expected_boundary_response"),
    }
    with (DIAGNOSTICS_DIR / "phase3C_group_counts.json").open("w", encoding="utf-8") as f:
        json.dump(group_counts, f, indent=2, ensure_ascii=False)

    expected_behavior = counts_by(rows, "expected_chamber_behavior")
    with (DIAGNOSTICS_DIR / "phase3C_expected_behavior_summary.json").open("w", encoding="utf-8") as f:
        json.dump(expected_behavior, f, indent=2, ensure_ascii=False)

    summary = build_summary(rows, manifest)
    with (DERIVED_DIR / "phase3C_forbidden_constrained_transition_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("Phase 3C ladder generation complete.")
    print(f"Input rows: {summary['rows']}")
    print(f"Ladders written: {summary['ladders_written']}")
    print(f"One-column directory: {ONE_COLUMN_DIR.relative_to(PROJECT_ROOT)}")
    print(f"Diagnostics directory: {DIAGNOSTICS_DIR.relative_to(PROJECT_ROOT)}")
    print(f"Derived summary: {(DERIVED_DIR / 'phase3C_forbidden_constrained_transition_summary.json').relative_to(PROJECT_ROOT)}")
    print()
    print("Primary first-pass chamber files:")
    for enc in summary["primary_ladders_recommended"]:
        print(f"  ladders/phase3C_forbidden_boundary/one_column/phase3C_ladder_{enc}.csv")


if __name__ == "__main__":
    main()
