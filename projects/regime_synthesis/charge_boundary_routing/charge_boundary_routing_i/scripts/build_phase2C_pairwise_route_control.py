#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phase2C_pairwise_route_control.py

Charge Boundary Routing I
Phase 2C-P — Pairwise Same-Charge Route Control

This v2 script is deliberately defensive: it creates every output folder before
every write operation, so OneDrive / missing empty folders cannot trigger a
diagnostics FileNotFoundError.

Run from project root:

    python scripts\build_phase2C_pairwise_route_control.py
"""

from __future__ import annotations

import csv
import itertools
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


OBJECT_INPUT = Path("data/canonical/phase2C_same_charge_route_control.csv")

PAIRWISE_FIELDS = [
    "pair_id", "phase", "control_name",
    "object_a", "object_b", "symbol_a", "symbol_b",
    "Q_a", "Q_b", "charge_difference", "same_charge_pair",
    "layer_a", "layer_b", "layer_pair", "layer_difference",
    "category_a", "category_b", "category_pair", "category_difference",
    "sub_category_a", "sub_category_b", "sub_category_pair", "sub_category_difference",
    "route_class_a", "route_class_b", "route_class_pair", "route_class_difference",
    "closure_class_a", "closure_class_b", "closure_class_pair", "closure_class_difference",
    "structural_route_a", "structural_route_b", "structural_route_pair", "structural_route_difference",
    "composite_difference", "external_difference", "boson_difference", "fermion_difference",
    "hadron_difference", "meson_difference", "baryon_difference", "lepton_difference", "gauge_boson_difference",
    "type_distance", "route_distance", "structural_distance", "pair_class", "source_note", "notes"
]

ENCODINGS = [
    "charge_difference", "same_charge_pair",
    "layer_pair_code", "layer_difference",
    "category_pair_code", "category_difference",
    "sub_category_pair_code", "sub_category_difference",
    "route_class_pair_code", "route_class_difference",
    "closure_class_pair_code", "closure_class_difference",
    "structural_route_pair_code", "structural_route_difference",
    "composite_difference", "external_difference", "boson_difference", "fermion_difference",
    "hadron_difference", "meson_difference", "baryon_difference", "lepton_difference", "gauge_boson_difference",
    "type_distance", "route_distance", "structural_distance", "pair_class_code"
]

FULL_LADDER_FIELDS = [
    "value", "pair_id", "phase", "control_name", "encoding",
    "object_a", "object_b", "symbol_a", "symbol_b",
    "Q_a", "Q_b", "charge_difference", "same_charge_pair",
    "layer_pair", "category_pair", "sub_category_pair", "route_class_pair",
    "closure_class_pair", "structural_route_pair",
    "type_distance", "route_distance", "structural_distance",
    "pair_class", "source_note", "notes"
]


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path):
    if not path.exists():
        raise FileNotFoundError(
            f"Missing input: {path}\n"
            "Run scripts\\build_phase2C_same_charge_route_control.py first."
        )
    with path.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) < 2:
        raise ValueError("Pairwise control requires at least two object rows.")
    return rows


def write_csv(path: Path, fields, rows) -> None:
    ensure_parent(path)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_one_column(path: Path, values) -> None:
    ensure_parent(path)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["value"])
        for value in values:
            writer.writerow([value])


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, obj) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def fnum(row, key) -> float:
    value = row.get(key, "")
    if value is None or str(value).strip() == "":
        return 0.0
    return float(value)


def difference(a, b) -> int:
    return 0 if str(a) == str(b) else 1


def ndiff(a, b) -> float:
    return abs(float(a) - float(b))


def pair_label(a, b) -> str:
    return "|".join(sorted([str(a), str(b)]))


def stable_code(values):
    return {value: idx + 1 for idx, value in enumerate(sorted(set(values)))}


def classify_pair(a, b) -> str:
    if a["layer"] != b["layer"]:
        return "CROSS_LAYER_SAME_CHARGE_PAIR"
    if a["category"] != b["category"]:
        return "SAME_LAYER_DIFFERENT_CATEGORY_PAIR"
    if a["sub_category"] != b["sub_category"]:
        return "SAME_CATEGORY_DIFFERENT_SUBTYPE_PAIR"
    return "SAME_ROUTE_FAMILY_PAIR"


def build_pairs(object_rows):
    flags = ["composite", "external", "boson", "fermion", "hadron", "meson", "baryon", "lepton", "gauge_boson"]
    pair_rows = []

    for idx, (a, b) in enumerate(itertools.combinations(object_rows, 2), start=1):
        q_a = fnum(a, "Q_over_e")
        q_b = fnum(b, "Q_over_e")

        layer_difference = difference(a["layer"], b["layer"])
        category_difference = difference(a["category"], b["category"])
        sub_category_difference = difference(a["sub_category"], b["sub_category"])
        route_class_difference = difference(a["route_class"], b["route_class"])
        closure_class_difference = difference(a["closure_class"], b["closure_class"])
        structural_route_difference = difference(a["structural_route_label"], b["structural_route_label"])

        flag_diffs = {
            f"{flag}_difference": ndiff(fnum(a, flag), fnum(b, flag))
            for flag in flags
        }

        type_distance = sum(flag_diffs.values())
        route_distance = (
            layer_difference
            + category_difference
            + sub_category_difference
            + route_class_difference
            + closure_class_difference
            + structural_route_difference
        )
        structural_distance = type_distance + route_distance

        row = {
            "pair_id": f"P{idx:03d}",
            "phase": "Phase 2C-P",
            "control_name": "pairwise_same_charge_route_control",
            "object_a": a["object_id"],
            "object_b": b["object_id"],
            "symbol_a": a["symbol"],
            "symbol_b": b["symbol"],
            "Q_a": q_a,
            "Q_b": q_b,
            "charge_difference": ndiff(q_a, q_b),
            "same_charge_pair": str(ndiff(q_a, q_b) == 0.0).upper(),
            "layer_a": a["layer"],
            "layer_b": b["layer"],
            "layer_pair": pair_label(a["layer"], b["layer"]),
            "layer_difference": layer_difference,
            "category_a": a["category"],
            "category_b": b["category"],
            "category_pair": pair_label(a["category"], b["category"]),
            "category_difference": category_difference,
            "sub_category_a": a["sub_category"],
            "sub_category_b": b["sub_category"],
            "sub_category_pair": pair_label(a["sub_category"], b["sub_category"]),
            "sub_category_difference": sub_category_difference,
            "route_class_a": a["route_class"],
            "route_class_b": b["route_class"],
            "route_class_pair": pair_label(a["route_class"], b["route_class"]),
            "route_class_difference": route_class_difference,
            "closure_class_a": a["closure_class"],
            "closure_class_b": b["closure_class"],
            "closure_class_pair": pair_label(a["closure_class"], b["closure_class"]),
            "closure_class_difference": closure_class_difference,
            "structural_route_a": a["structural_route_label"],
            "structural_route_b": b["structural_route_label"],
            "structural_route_pair": pair_label(a["structural_route_label"], b["structural_route_label"]),
            "structural_route_difference": structural_route_difference,
            **flag_diffs,
            "type_distance": type_distance,
            "route_distance": route_distance,
            "structural_distance": structural_distance,
            "pair_class": classify_pair(a, b),
            "source_note": f"{a['symbol']} compared with {b['symbol']}; both have Q/e = +1.",
            "notes": "Pairwise same-charge control. Charge difference is zero; structural differences are measured separately.",
        }
        pair_rows.append(row)

    return pair_rows


def build_values(pair_rows):
    codebooks = {
        "layer_pair_code": stable_code([row["layer_pair"] for row in pair_rows]),
        "category_pair_code": stable_code([row["category_pair"] for row in pair_rows]),
        "sub_category_pair_code": stable_code([row["sub_category_pair"] for row in pair_rows]),
        "route_class_pair_code": stable_code([row["route_class_pair"] for row in pair_rows]),
        "closure_class_pair_code": stable_code([row["closure_class_pair"] for row in pair_rows]),
        "structural_route_pair_code": stable_code([row["structural_route_pair"] for row in pair_rows]),
        "pair_class_code": stable_code([row["pair_class"] for row in pair_rows]),
    }

    values = {encoding: [] for encoding in ENCODINGS}

    for row in pair_rows:
        values["charge_difference"].append(float(row["charge_difference"]))
        values["same_charge_pair"].append(1.0 if row["same_charge_pair"] == "TRUE" else 0.0)

        for code_encoding in [
            "layer_pair_code",
            "category_pair_code",
            "sub_category_pair_code",
            "route_class_pair_code",
            "closure_class_pair_code",
            "structural_route_pair_code",
            "pair_class_code",
        ]:
            source_key = code_encoding.replace("_code", "")
            values[code_encoding].append(float(codebooks[code_encoding][row[source_key]]))

        for numeric_encoding in [
            "layer_difference",
            "category_difference",
            "sub_category_difference",
            "route_class_difference",
            "closure_class_difference",
            "structural_route_difference",
            "composite_difference",
            "external_difference",
            "boson_difference",
            "fermion_difference",
            "hadron_difference",
            "meson_difference",
            "baryon_difference",
            "lepton_difference",
            "gauge_boson_difference",
            "type_distance",
            "route_distance",
            "structural_distance",
        ]:
            values[numeric_encoding].append(float(row[numeric_encoding]))

    return values, codebooks


def full_ladder_rows(pair_rows, encoding, values):
    out = []
    for row, value in zip(pair_rows, values):
        out.append({
            "value": value,
            "pair_id": row["pair_id"],
            "phase": row["phase"],
            "control_name": row["control_name"],
            "encoding": encoding,
            "object_a": row["object_a"],
            "object_b": row["object_b"],
            "symbol_a": row["symbol_a"],
            "symbol_b": row["symbol_b"],
            "Q_a": row["Q_a"],
            "Q_b": row["Q_b"],
            "charge_difference": row["charge_difference"],
            "same_charge_pair": row["same_charge_pair"],
            "layer_pair": row["layer_pair"],
            "category_pair": row["category_pair"],
            "sub_category_pair": row["sub_category_pair"],
            "route_class_pair": row["route_class_pair"],
            "closure_class_pair": row["closure_class_pair"],
            "structural_route_pair": row["structural_route_pair"],
            "type_distance": row["type_distance"],
            "route_distance": row["route_distance"],
            "structural_distance": row["structural_distance"],
            "pair_class": row["pair_class"],
            "source_note": row["source_note"],
            "notes": row["notes"],
        })
    return out


def unique_count(values) -> int:
    return len(set(values))


def main() -> int:
    r = project_root()

    input_csv = r / OBJECT_INPUT
    pairwise_csv = r / "data" / "derived" / "phase2C_pairwise_same_charge_route_control.csv"
    summary_json = r / "data" / "derived" / "phase2C_pairwise_same_charge_route_control_summary.json"

    ladder_dir = r / "ladders" / "phase2C_pairwise_same_charge_control"
    one_col_dir = ladder_dir / "one_column"
    diagnostics_dir = ladder_dir / "diagnostics"

    result_dirs = [
        r / "results" / "struc_perc_i" / "phase2C_pairwise_same_charge_control",
        r / "results" / "struc_i" / "phase2C_pairwise_same_charge_control",
        r / "outputs" / "reports" / "phase2C_pairwise_same_charge_control",
    ]

    for directory in [pairwise_csv.parent, ladder_dir, one_col_dir, diagnostics_dir, *result_dirs]:
        ensure_dir(directory)

    object_rows = read_csv(input_csv)
    pair_rows = build_pairs(object_rows)

    write_csv(pairwise_csv, PAIRWISE_FIELDS, pair_rows)

    values, codebooks = build_values(pair_rows)

    written_files = []
    for encoding, vals in values.items():
        full_path = ladder_dir / f"phase2C_pairwise_ladder_{encoding}.csv"
        one_col_path = one_col_dir / f"phase2C_pairwise_ladder_{encoding}.csv"

        write_csv(full_path, FULL_LADDER_FIELDS, full_ladder_rows(pair_rows, encoding, vals))
        write_one_column(one_col_path, vals)

        written_files.append(str(full_path.relative_to(r)))
        written_files.append(str(one_col_path.relative_to(r)))

    flagged = [
        {
            "encoding": encoding,
            "reason": "constant_pairwise_control_encoding",
            "unique_values": unique_count(vals),
            "values": sorted(set(vals)),
        }
        for encoding, vals in values.items()
        if unique_count(vals) < 2
    ]

    summary = {
        "program": "UNNS Substrate Program",
        "project": "Charge Boundary Routing I",
        "phase": "Phase 2C-P — Pairwise Same-Charge Route Control",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "source_object_rows": len(object_rows),
        "pair_rows": len(pair_rows),
        "object_ids": [row["object_id"] for row in object_rows],
        "pair_ids": [row["pair_id"] for row in pair_rows],
        "all_charge_differences": sorted(set(float(row["charge_difference"]) for row in pair_rows)),
        "pair_class_counts": dict(sorted(Counter(row["pair_class"] for row in pair_rows).items())),
        "encodings": ENCODINGS,
        "flagged_constant_or_low_diversity_encodings": flagged,
        "codebooks": codebooks,
        "encoding_stats": {
            encoding: {
                "row_count": len(vals),
                "unique_values": unique_count(vals),
                "min": min(vals),
                "max": max(vals),
                "values": vals,
            }
            for encoding, vals in values.items()
        },
        "files_written": len(written_files),
        "written_files": written_files,
        "interpretation": {
            "control_question": "When charge_difference = 0 for every pair, do structural route differences remain nonzero?",
            "expected_result": "Same Q = +1 does not imply same structural route.",
            "canonical_statement": "Charge equality is not structural-route equivalence.",
        },
    }

    write_json(summary_json, summary)
    write_json(diagnostics_dir / "phase2C_pairwise_same_charge_route_control_summary.json", summary)

    diagnostics_readme = "\n".join([
        "Charge Boundary Routing I",
        "Phase 2C-P — Pairwise Same-Charge Route Control Diagnostics",
        "",
        f"Generated UTC: {summary['generated_utc']}",
        f"Source object rows: {summary['source_object_rows']}",
        f"Pair rows: {summary['pair_rows']}",
        "",
        "Why this exists:",
        "  The original Phase 2C object-level control has only 5 rows.",
        "  STRUC-I may reject those tiny ladders.",
        "  Pairwise conversion creates 10 rows while preserving the same control question.",
        "",
        "Control question:",
        "  When charge_difference = 0 for every pair, do structural route differences remain nonzero?",
        "",
        "Expected result:",
        "  Same Q = +1 does not imply same structural route.",
        "",
        "Do not upload first:",
        "  phase2C_pairwise_ladder_charge_difference.csv",
        "  phase2C_pairwise_ladder_same_charge_pair.csv",
        "",
        "Primary chamber files:",
        "  phase2C_pairwise_ladder_structural_distance.csv",
        "  phase2C_pairwise_ladder_route_distance.csv",
        "  phase2C_pairwise_ladder_type_distance.csv",
        "  phase2C_pairwise_ladder_structural_route_pair_code.csv",
        "  phase2C_pairwise_ladder_category_pair_code.csv",
        "  phase2C_pairwise_ladder_sub_category_pair_code.csv",
        "  phase2C_pairwise_ladder_pair_class_code.csv",
        "  phase2C_pairwise_ladder_layer_pair_code.csv",
    ])
    write_text(diagnostics_dir / "README_phase2C_pairwise_same_charge_route_control_diagnostics.txt", diagnostics_readme)

    print("Phase 2C-P pairwise same-charge route-control corpus and ladders built.")
    print(f"Project root: {r}")
    print(f"Source objects: {len(object_rows)}")
    print(f"Pair rows: {len(pair_rows)}")
    print(f"Pairwise corpus: {pairwise_csv.relative_to(r)}")
    print(f"Summary: {summary_json.relative_to(r)}")
    print(f"Ladders: {ladder_dir.relative_to(r)}")
    print(f"One-column: {one_col_dir.relative_to(r)}")
    print(f"Diagnostics: {diagnostics_dir.relative_to(r)}")
    print(f"Files written: {len(written_files)}")
    print("")
    print("Flagged constant encodings:")
    for item in flagged:
        print(f"  - {item['encoding']}: {item['reason']}")
    print("")
    print("Primary chamber files:")
    print("  phase2C_pairwise_ladder_structural_distance.csv")
    print("  phase2C_pairwise_ladder_route_distance.csv")
    print("  phase2C_pairwise_ladder_type_distance.csv")
    print("  phase2C_pairwise_ladder_structural_route_pair_code.csv")
    print("  phase2C_pairwise_ladder_category_pair_code.csv")
    print("  phase2C_pairwise_ladder_sub_category_pair_code.csv")
    print("  phase2C_pairwise_ladder_pair_class_code.csv")
    print("  phase2C_pairwise_ladder_layer_pair_code.csv")
    print("")
    print("Do not upload first:")
    print("  phase2C_pairwise_ladder_charge_difference.csv")
    print("  phase2C_pairwise_ladder_same_charge_pair.csv")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
