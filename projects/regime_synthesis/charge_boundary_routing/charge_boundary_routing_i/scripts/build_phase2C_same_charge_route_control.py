#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phase2C_same_charge_route_control.py

Charge Boundary Routing I
Phase 2C — Same-Charge Different-Route Control

Purpose
-------
Build the reserved +1 same-charge route-control corpus.

Phase 2C is not a transition corpus. It is a static control test.

Question:
    Do objects with the same external charge Q = +1 occupy the same structural
    route, or do they separate by route / closure / category coordinates?

Expected UNNS result:
    Same Q = +1 does not imply same structural route.

Control objects:
    positron
    proton
    pi+
    K+
    W+

This script writes:

    data/canonical/phase2C_same_charge_route_control.csv
    data/derived/phase2C_same_charge_route_control_summary.json

It also prepares:

    ladders/phase2C_same_charge_control/
    ladders/phase2C_same_charge_control/one_column/
    ladders/phase2C_same_charge_control/diagnostics/
    results/struc_perc_i/phase2C_same_charge_control/
    results/struc_i/phase2C_same_charge_control/
    outputs/reports/phase2C_same_charge_control/

Run from project root:

    python scripts/build_phase2C_same_charge_route_control.py
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


# ---------------------------------------------------------------------------
# Layer codes inherited from Charge Boundary Routing I
# ---------------------------------------------------------------------------

LAYER_A = "A"  # primitive external closures
LAYER_C = "C"  # composite closures


# ---------------------------------------------------------------------------
# Phase 2C object corpus
# ---------------------------------------------------------------------------
# All objects have external charge Q/e = +1.
# They differ by category, compositeness, route class, closure class, and source layer.

OBJECTS: List[Dict[str, object]] = [
    {
        "object_id": "positron",
        "pdg_name": "positron",
        "symbol": "e+",
        "category": "lepton",
        "sub_category": "charged_lepton_antiparticle",
        "Q_over_e": 1.0,
        "layer": LAYER_A,
        "layer_label": "primitive_external_closure",
        "composite": 0,
        "external": 1,
        "boson": 0,
        "fermion": 1,
        "hadron": 0,
        "meson": 0,
        "baryon": 0,
        "lepton": 1,
        "gauge_boson": 0,
        "route_class": "FREE_INTEGER_ROUTE",
        "closure_class": "FREE_INTEGER_CLOSURE",
        "structural_route_label": "external_leptonic_integer_closure",
        "source_file": "rpp2026-sum-leptons.pdf",
        "source_note": "Stable external charged lepton antiparticle with Q/e = +1.",
        "notes": "Primitive external closure; same charge as proton, pi+, K+, and W+ but different route.",
    },
    {
        "object_id": "proton",
        "pdg_name": "proton",
        "symbol": "p",
        "category": "baryon",
        "sub_category": "charged_baryon",
        "Q_over_e": 1.0,
        "layer": LAYER_C,
        "layer_label": "composite_closure",
        "composite": 1,
        "external": 0,
        "boson": 0,
        "fermion": 1,
        "hadron": 1,
        "meson": 0,
        "baryon": 1,
        "lepton": 0,
        "gauge_boson": 0,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "structural_route_label": "composite_baryonic_integer_closure",
        "source_file": "rpp2026-sum-baryons.pdf",
        "source_note": "Composite baryon closure with Q/e = +1.",
        "notes": "Composite baryonic closure; same external charge as positron but not the same route.",
    },
    {
        "object_id": "pi_plus",
        "pdg_name": "positive pion",
        "symbol": "pi+",
        "category": "meson",
        "sub_category": "charged_light_meson",
        "Q_over_e": 1.0,
        "layer": LAYER_C,
        "layer_label": "composite_closure",
        "composite": 1,
        "external": 0,
        "boson": 1,
        "fermion": 0,
        "hadron": 1,
        "meson": 1,
        "baryon": 0,
        "lepton": 0,
        "gauge_boson": 0,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "structural_route_label": "composite_mesonic_integer_closure",
        "source_file": "rpp2026-sum-mesons.pdf",
        "source_note": "Composite meson closure with Q/e = +1.",
        "notes": "Composite mesonic closure; same charge as proton but different category and route subtype.",
    },
    {
        "object_id": "k_plus",
        "pdg_name": "positive kaon",
        "symbol": "K+",
        "category": "meson",
        "sub_category": "charged_strange_meson",
        "Q_over_e": 1.0,
        "layer": LAYER_C,
        "layer_label": "composite_closure",
        "composite": 1,
        "external": 0,
        "boson": 1,
        "fermion": 0,
        "hadron": 1,
        "meson": 1,
        "baryon": 0,
        "lepton": 0,
        "gauge_boson": 0,
        "route_class": "COMPOSITE_INTEGER_ROUTE",
        "closure_class": "COMPOSITE_INTEGER_CLOSURE",
        "structural_route_label": "composite_strange_mesonic_integer_closure",
        "source_file": "rpp2026-sum-mesons.pdf",
        "source_note": "Composite strange meson closure with Q/e = +1.",
        "notes": "Composite strange mesonic closure; same charge as pi+ but distinct subtype.",
    },
    {
        "object_id": "w_plus",
        "pdg_name": "W plus boson",
        "symbol": "W+",
        "category": "gauge_boson",
        "sub_category": "charged_weak_gauge_boson",
        "Q_over_e": 1.0,
        "layer": LAYER_A,
        "layer_label": "primitive_external_closure",
        "composite": 0,
        "external": 1,
        "boson": 1,
        "fermion": 0,
        "hadron": 0,
        "meson": 0,
        "baryon": 0,
        "lepton": 0,
        "gauge_boson": 1,
        "route_class": "FREE_INTEGER_ROUTE",
        "closure_class": "FREE_INTEGER_CLOSURE",
        "structural_route_label": "external_gauge_integer_closure",
        "source_file": "rpp2026-sum-gauge-higgs-bosons.pdf",
        "source_note": "External charged weak gauge boson with Q/e = +1.",
        "notes": "External gauge closure; same charge as positron but different spin/category/route subtype.",
    },
]


FIELDNAMES = [
    "object_id",
    "phase",
    "control_name",
    "pdg_name",
    "symbol",
    "category",
    "sub_category",
    "Q_over_e",
    "same_charge_class",
    "layer",
    "layer_label",
    "composite",
    "external",
    "boson",
    "fermion",
    "hadron",
    "meson",
    "baryon",
    "lepton",
    "gauge_boson",
    "route_class",
    "closure_class",
    "structural_route_label",
    "source_file",
    "source_note",
    "notes",
]


ENCODINGS = [
    "Q_over_e",
    "same_charge_constant",
    "layer_code",
    "route_class_code",
    "closure_class_code",
    "category_code",
    "sub_category_code",
    "structural_route_code",
    "composite",
    "external",
    "boson",
    "fermion",
    "hadron",
    "meson",
    "baryon",
    "lepton",
    "gauge_boson",
]


FULL_LADDER_FIELDNAMES = [
    "value",
    "object_id",
    "phase",
    "control_name",
    "encoding",
    "pdg_name",
    "symbol",
    "category",
    "sub_category",
    "Q_over_e",
    "same_charge_class",
    "layer",
    "route_class",
    "closure_class",
    "structural_route_label",
    "source_file",
    "source_note",
    "notes",
]


def project_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def stable_code(values: Sequence[str]) -> Dict[str, int]:
    unique = sorted(set(values))
    return {value: idx + 1 for idx, value in enumerate(unique)}


def write_csv(path: Path, fieldnames: Sequence[str], rows: Sequence[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
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


def build_corpus_rows() -> List[Dict[str, object]]:
    rows = []
    for obj in OBJECTS:
        row = {
            **obj,
            "phase": "Phase 2C",
            "control_name": "same_charge_different_route_control",
            "same_charge_class": "Q_PLUS_1",
        }
        rows.append(row)
    return rows


def build_ladders(rows: Sequence[Dict[str, object]]) -> Tuple[Dict[str, List[float]], Dict[str, Dict[str, int]]]:
    codebooks = {
        "layer_code": stable_code([str(r["layer"]) for r in rows]),
        "route_class_code": stable_code([str(r["route_class"]) for r in rows]),
        "closure_class_code": stable_code([str(r["closure_class"]) for r in rows]),
        "category_code": stable_code([str(r["category"]) for r in rows]),
        "sub_category_code": stable_code([str(r["sub_category"]) for r in rows]),
        "structural_route_code": stable_code([str(r["structural_route_label"]) for r in rows]),
    }

    values = {encoding: [] for encoding in ENCODINGS}
    for row in rows:
        values["Q_over_e"].append(float(row["Q_over_e"]))
        values["same_charge_constant"].append(1.0)
        values["layer_code"].append(float(codebooks["layer_code"][str(row["layer"])]))
        values["route_class_code"].append(float(codebooks["route_class_code"][str(row["route_class"])]))
        values["closure_class_code"].append(float(codebooks["closure_class_code"][str(row["closure_class"])]))
        values["category_code"].append(float(codebooks["category_code"][str(row["category"])]))
        values["sub_category_code"].append(float(codebooks["sub_category_code"][str(row["sub_category"])]))
        values["structural_route_code"].append(float(codebooks["structural_route_code"][str(row["structural_route_label"])]))

        for flag in ["composite", "external", "boson", "fermion", "hadron", "meson", "baryon", "lepton", "gauge_boson"]:
            values[flag].append(float(row[flag]))

    return values, codebooks


def full_ladder_rows(rows: Sequence[Dict[str, object]], encoding: str, values: Sequence[float]) -> List[Dict[str, object]]:
    out = []
    for row, value in zip(rows, values):
        out.append({
            "value": value,
            "object_id": row["object_id"],
            "phase": row["phase"],
            "control_name": row["control_name"],
            "encoding": encoding,
            "pdg_name": row["pdg_name"],
            "symbol": row["symbol"],
            "category": row["category"],
            "sub_category": row["sub_category"],
            "Q_over_e": row["Q_over_e"],
            "same_charge_class": row["same_charge_class"],
            "layer": row["layer"],
            "route_class": row["route_class"],
            "closure_class": row["closure_class"],
            "structural_route_label": row["structural_route_label"],
            "source_file": row["source_file"],
            "source_note": row["source_note"],
            "notes": row["notes"],
        })
    return out


def unique_count(values: Sequence[float]) -> int:
    return len(set(values))


def build_summary(rows: Sequence[Dict[str, object]], values: Dict[str, List[float]], codebooks: Dict[str, Dict[str, int]]) -> Dict[str, object]:
    flagged = []
    for encoding, vals in values.items():
        if unique_count(vals) < 2:
            flagged.append({
                "encoding": encoding,
                "reason": "constant_control_encoding",
                "unique_values": unique_count(vals),
                "values": sorted(set(vals)),
            })

    return {
        "program": "UNNS Substrate Program",
        "project": "Charge Boundary Routing I",
        "phase": "Phase 2C — Same-Charge Different-Route Control",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "row_count": len(rows),
        "object_ids": [str(r["object_id"]) for r in rows],
        "same_charge_class": "Q_PLUS_1",
        "all_Q_over_e": sorted(set(float(r["Q_over_e"]) for r in rows)),
        "category_counts": dict(sorted(Counter(str(r["category"]) for r in rows).items())),
        "layer_counts": dict(sorted(Counter(str(r["layer"]) for r in rows).items())),
        "route_class_counts": dict(sorted(Counter(str(r["route_class"]) for r in rows).items())),
        "closure_class_counts": dict(sorted(Counter(str(r["closure_class"]) for r in rows).items())),
        "structural_route_count": len(set(str(r["structural_route_label"]) for r in rows)),
        "encodings": ENCODINGS,
        "flagged_constant_or_low_diversity_encodings": flagged,
        "codebooks": codebooks,
        "encoding_stats": {
            encoding: {
                "row_count": len(vals),
                "unique_values": unique_count(vals),
                "min": min(vals) if vals else None,
                "max": max(vals) if vals else None,
                "values": vals,
            }
            for encoding, vals in values.items()
        },
        "output_files": {
            "canonical_csv": "data/canonical/phase2C_same_charge_route_control.csv",
            "summary_json": "data/derived/phase2C_same_charge_route_control_summary.json",
            "ladders": "ladders/phase2C_same_charge_control/",
            "one_column_ladders": "ladders/phase2C_same_charge_control/one_column/",
            "diagnostics": "ladders/phase2C_same_charge_control/diagnostics/",
        },
        "interpretation": {
            "control_question": "Does same external charge Q = +1 imply same structural route?",
            "expected_result": "Same Q = +1 does not imply same structural route.",
            "canonical_statement": "Charge value is a projection; structural route is a separate coordinate.",
        },
        "notes": [
            "Phase 2C is a static control, not a transition corpus.",
            "Q_over_e and same_charge_constant are intentionally constant and should not be uploaded first.",
            "Primary chamber inputs are structural_route_code, category_code, sub_category_code, layer_code, and object flags.",
        ],
    }


def write_diagnostics(path: Path, summary: Dict[str, object]) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "phase2C_same_charge_route_control_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = []
    lines.append("Charge Boundary Routing I")
    lines.append("Phase 2C — Same-Charge Different-Route Control")
    lines.append("README_phase2C_same_charge_route_control_diagnostics.txt")
    lines.append("")
    lines.append(f"Generated UTC: {summary['generated_utc']}")
    lines.append(f"Rows: {summary['row_count']}")
    lines.append("")
    lines.append("Control question:")
    lines.append("  Does same external charge Q = +1 imply same structural route?")
    lines.append("")
    lines.append("Expected result:")
    lines.append("  Same Q = +1 does not imply same structural route.")
    lines.append("")
    lines.append("Objects:")
    for oid in summary["object_ids"]:
        lines.append(f"  - {oid}")
    lines.append("")
    lines.append("Flagged constant encodings:")
    for item in summary["flagged_constant_or_low_diversity_encodings"]:
        lines.append(f"  - {item['encoding']}: {item['reason']}; values={item['values']}")
    lines.append("")
    lines.append("Primary chamber inputs:")
    lines.append("  phase2C_same_charge_ladder_structural_route_code.csv")
    lines.append("  phase2C_same_charge_ladder_category_code.csv")
    lines.append("  phase2C_same_charge_ladder_sub_category_code.csv")
    lines.append("  phase2C_same_charge_ladder_layer_code.csv")
    lines.append("  phase2C_same_charge_ladder_composite.csv")
    lines.append("  phase2C_same_charge_ladder_external.csv")
    lines.append("  phase2C_same_charge_ladder_boson.csv")
    lines.append("  phase2C_same_charge_ladder_fermion.csv")
    lines.append("  phase2C_same_charge_ladder_hadron.csv")
    lines.append("")
    lines.append("Do not upload first:")
    lines.append("  phase2C_same_charge_ladder_Q_over_e.csv")
    lines.append("  phase2C_same_charge_ladder_same_charge_constant.csv")
    lines.append("")
    lines.append("Codebooks:")
    for name, cb in summary["codebooks"].items():
        lines.append("")
        lines.append(name + ":")
        for key, val in cb.items():
            lines.append(f"  {val}: {key}")

    (path / "README_phase2C_same_charge_route_control_diagnostics.txt").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> int:
    root = project_root_from_script()

    canonical_csv = root / "data" / "canonical" / "phase2C_same_charge_route_control.csv"
    summary_json = root / "data" / "derived" / "phase2C_same_charge_route_control_summary.json"

    ladder_dir = root / "ladders" / "phase2C_same_charge_control"
    one_col_dir = ladder_dir / "one_column"
    diagnostics_dir = ladder_dir / "diagnostics"

    dirs = [
        canonical_csv.parent,
        summary_json.parent,
        ladder_dir,
        one_col_dir,
        diagnostics_dir,
        root / "results" / "struc_perc_i" / "phase2C_same_charge_control",
        root / "results" / "struc_i" / "phase2C_same_charge_control",
        root / "outputs" / "reports" / "phase2C_same_charge_control",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    rows = build_corpus_rows()
    write_csv(canonical_csv, FIELDNAMES, rows)

    values, codebooks = build_ladders(rows)

    written_files = []
    for encoding, vals in values.items():
        full_path = ladder_dir / f"phase2C_same_charge_ladder_{encoding}.csv"
        one_col_path = one_col_dir / f"phase2C_same_charge_ladder_{encoding}.csv"

        write_csv(full_path, FULL_LADDER_FIELDNAMES, full_ladder_rows(rows, encoding, vals))
        write_one_column(one_col_path, vals)

        written_files.append(str(full_path.relative_to(root)))
        written_files.append(str(one_col_path.relative_to(root)))

    summary = build_summary(rows, values, codebooks)
    summary["files_written"] = len(written_files)
    summary["written_files"] = written_files
    summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    write_diagnostics(diagnostics_dir, summary)

    print("Phase 2C same-charge route-control corpus and ladders built.")
    print(f"Project root: {root}")
    print(f"Rows: {len(rows)}")
    print(f"Corpus: {canonical_csv.relative_to(root)}")
    print(f"Summary: {summary_json.relative_to(root)}")
    print(f"Ladders: {ladder_dir.relative_to(root)}")
    print(f"One-column: {one_col_dir.relative_to(root)}")
    print(f"Diagnostics: {diagnostics_dir.relative_to(root)}")
    print(f"Files written: {len(written_files)}")
    print("")
    print("Flagged constant encodings:")
    for item in summary["flagged_constant_or_low_diversity_encodings"]:
        print(f"  - {item['encoding']}: {item['reason']}")
    print("")
    print("Primary chamber files:")
    print("  phase2C_same_charge_ladder_structural_route_code.csv")
    print("  phase2C_same_charge_ladder_category_code.csv")
    print("  phase2C_same_charge_ladder_sub_category_code.csv")
    print("  phase2C_same_charge_ladder_layer_code.csv")
    print("  phase2C_same_charge_ladder_composite.csv")
    print("  phase2C_same_charge_ladder_external.csv")
    print("  phase2C_same_charge_ladder_boson.csv")
    print("  phase2C_same_charge_ladder_fermion.csv")
    print("  phase2C_same_charge_ladder_hadron.csv")
    print("")
    print("Do not upload first:")
    print("  phase2C_same_charge_ladder_Q_over_e.csv")
    print("  phase2C_same_charge_ladder_same_charge_constant.csv")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
