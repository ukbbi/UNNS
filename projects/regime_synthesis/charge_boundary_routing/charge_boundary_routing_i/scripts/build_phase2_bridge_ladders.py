#!/usr/bin/env python3
"""
build_phase2_bridge_ladders.py

Charge Boundary Routing I
Phase 2 — Bridge Tests

Generate bridge-ladder CSV files from the verified Phase 1 canonical corpus.

Input:
    data/derived/charge_boundary_phase1_combined.csv

Outputs:
    ladders/phase2_bridges/
        AB_bridge_external_to_fractional_ladder_<encoding>.csv
        BC_bridge_fractional_to_composite_ladder_<encoding>.csv
        CD_bridge_composite_to_boundary_ladder_<encoding>.csv
        ABC_bridge_external_fractional_composite_ladder_<encoding>.csv
        BCD_bridge_fractional_composite_boundary_ladder_<encoding>.csv

    ladders/phase2_bridges/one_column/
        chamber-ready one-column CSV files with only a "value" column

    ladders/phase2_bridges/diagnostics/
        phase2_bridge_ladder_generation_summary.json
        phase2_bridge_ladder_generation_report.txt

Purpose:
    Phase 1 tested isolated layers:
        A — Primitive External Charge Closures
        B — Confined Fractional Coordinates
        C — Composite Closures
        D — Boundary Absences and Non-observed Cases

    Phase 2 tests bridges between layers:
        A <-> B
        B <-> C
        C <-> D
        A <-> B <-> C
        B <-> C <-> D

Important Layer D rule:
    Layer D is a boundary-absence / constraint layer, not an ordinary
    charge-state ladder. Therefore, when a bridge includes D, this script
    does NOT generate signed_charge or absolute_charge bridge ladders.
    D participates only through boundary / closure / route encodings.

    This prevents the same error seen in isolated Layer D STRUC-I testing:
        "No valid numeric ladder found in csv."

Run from the project root:
    python scripts/build_phase2_bridge_ladders.py

or from the scripts folder:
    python build_phase2_bridge_ladders.py
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from datetime import date
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


# ---------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------

def find_project_root() -> Path:
    """
    Resolve project root whether the script is launched from:
        charge_boundary_routing_i/scripts/
    or copied/run directly from:
        charge_boundary_routing_i/
    """
    here = Path(__file__).resolve()

    candidates = [
        here.parent.parent,  # normal: project/scripts/script.py
        here.parent,         # fallback: project/script.py
        Path.cwd(),          # fallback: current working directory
    ]

    for candidate in candidates:
        expected = candidate / "data" / "derived" / "charge_boundary_phase1_combined.csv"
        if expected.exists():
            return candidate

    raise FileNotFoundError(
        "Could not find project root. Expected file:\n"
        "    data/derived/charge_boundary_phase1_combined.csv\n\n"
        "Place this script in charge_boundary_routing_i/scripts/ and run:\n"
        "    python scripts/build_phase2_bridge_ladders.py"
    )


ROOT = find_project_root()

INPUT_FILE = ROOT / "data" / "derived" / "charge_boundary_phase1_combined.csv"

OUT_DIR = ROOT / "ladders" / "phase2_bridges"
ONE_COLUMN_DIR = OUT_DIR / "one_column"
DIAGNOSTICS_DIR = OUT_DIR / "diagnostics"

OUT_DIR.mkdir(parents=True, exist_ok=True)
ONE_COLUMN_DIR.mkdir(parents=True, exist_ok=True)
DIAGNOSTICS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# Numeric coding maps
# ---------------------------------------------------------------------

# Keep these maps aligned with build_charge_ladders.py, with one correction:
# EXTERNAL_NEUTRALITY_CONSTRAINT appears in Layer D and must be treated as a
# constrained boundary class.
CLOSURE_CLASS_CODE = {
    "FREE_NEUTRAL_CLOSURE": 0.0,
    "FREE_INTEGER_CLOSURE": 1.0,
    "INTERNAL_FRACTIONAL_COORDINATE": 2.0,
    "COMPOSITE_NEUTRAL_CLOSURE": 3.0,
    "COMPOSITE_INTEGER_CLOSURE": 4.0,
    "TERMINAL_FREE_FRACTIONAL": 5.0,
    "UNRESOLVED_DUAL_BOUNDARY": 6.0,
    "CONSTRAINED_NEUTRALITY_BOUNDARY": 7.0,
    "EXTERNAL_NEUTRALITY_CONSTRAINT": 7.0,
    "CONSTRAINED_CHARGE_VIOLATION_BOUNDARY": 8.0,
}

ROUTE_CLASS_CODE = {
    "EXTERNAL_CLOSURE": 0.0,
    "CONFINED_ROUTE": 1.0,
    "COMPOSITE_CLOSURE": 2.0,
    "BOUNDARY_ABSENCE": 3.0,
    "DUAL_BOUNDARY_CANDIDATE": 4.0,
    "BOUNDARY_CONSTRAINT": 5.0,
}

# Ordered UNNS route coordinate for boundary-routing tests.
BOUNDARY_ROUTE_COORDINATE = {
    "FREE_NEUTRAL_CLOSURE": 0.00,
    "FREE_INTEGER_CLOSURE": 0.25,
    "INTERNAL_FRACTIONAL_COORDINATE": 0.50,
    "COMPOSITE_NEUTRAL_CLOSURE": 0.75,
    "COMPOSITE_INTEGER_CLOSURE": 1.00,
    "TERMINAL_FREE_FRACTIONAL": 1.25,
    "UNRESOLVED_DUAL_BOUNDARY": 1.50,
    "CONSTRAINED_NEUTRALITY_BOUNDARY": 1.75,
    "EXTERNAL_NEUTRALITY_CONSTRAINT": 1.75,
    "CONSTRAINED_CHARGE_VIOLATION_BOUNDARY": 2.00,
}

# Closure-state code emphasizes whether a row is externally closed,
# internally fractional, not closed, constrained, or unresolved.
CLOSURE_STATE_CODE = {
    "closed": 0.0,
    "internal_fractional": 1.0,
    "not_closed": 2.0,
    "constrained": 3.0,
    "unresolved": 4.0,
}


ENCODINGS = [
    "signed_charge",
    "absolute_charge",
    "boundary_route_coordinate",
    "closure_class_code",
    "closure_state_code",
    "route_class_code",
]


BRIDGES = {
    "AB": {
        "label": "A <-> B",
        "layers": ["A", "B"],
        "stem": "AB_bridge_external_to_fractional_ladder",
        "description": "External primitive closures to confined fractional coordinates.",
    },
    "BC": {
        "label": "B <-> C",
        "layers": ["B", "C"],
        "stem": "BC_bridge_fractional_to_composite_ladder",
        "description": "Confined fractional coordinates to composite closures.",
    },
    "CD": {
        "label": "C <-> D",
        "layers": ["C", "D"],
        "stem": "CD_bridge_composite_to_boundary_ladder",
        "description": "Composite closures to boundary absences / constraints.",
    },
    "ABC": {
        "label": "A <-> B <-> C",
        "layers": ["A", "B", "C"],
        "stem": "ABC_bridge_external_fractional_composite_ladder",
        "description": "External primitive, confined fractional, and composite closure route.",
    },
    "BCD": {
        "label": "B <-> C <-> D",
        "layers": ["B", "C", "D"],
        "stem": "BCD_bridge_fractional_composite_boundary_ladder",
        "description": "Fractional, composite, and boundary-marker route.",
    },
}


PROVENANCE_FIELDS = [
    "value",
    "bridge_id",
    "bridge_label",
    "bridge_layers",
    "object_id",
    "phase",
    "layer",
    "pdg_section",
    "pdg_name",
    "symbol",
    "category",
    "components",
    "component_charges",
    "Q_over_e",
    "closure_class",
    "route_class",
    "encoding",
    "source_file",
    "source_note",
    "notes",
]


# ---------------------------------------------------------------------
# Basic IO helpers
# ---------------------------------------------------------------------

def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing input file: {path}\n"
            "Run scripts/build_phase1_verified_corpus.py first."
        )

    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: List[Dict[str, str]], fields: List[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_one_column(path: Path, values: List[float]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["value"])
        writer.writeheader()
        for value in values:
            writer.writerow({"value": f"{value:.12g}"})


# ---------------------------------------------------------------------
# Parsing and classification helpers
# ---------------------------------------------------------------------

def parse_charge_to_float(raw: str) -> Optional[float]:
    """
    Parse Q_over_e values such as:
        -1, +1, 0, +2/3, -1/3, <1e-21

    Returns None for non-numeric boundary labels such as:
        not observed
        not observed within listed bound

    For strict provenance, bounds such as <1e-21 are also returned as None
    because they are constraints, not ordinary charge values.
    """
    if raw is None:
        return None

    s = str(raw).strip()
    if not s:
        return None

    lowered = s.lower()

    if lowered in {
        "fractional",
        "not_electric_charge",
        "forbidden_transition",
        "constraint",
        "not_applicable",
        "not observed",
        "not observed within listed bound",
        "magnetic charge",
    }:
        return None

    if lowered.startswith("<"):
        return None

    s = s.replace("+", "")
    try:
        if "/" in s:
            return float(Fraction(s))
        return float(s)
    except Exception:
        return None


def layer_key(row: Dict[str, str]) -> str:
    object_id = row.get("object_id", "")

    if object_id.startswith("L_A_"):
        return "A"
    if object_id.startswith("L_B_"):
        return "B"
    if object_id.startswith("L_C_"):
        return "C"
    if object_id.startswith("L_D_"):
        return "D"

    layer = row.get("layer", "")
    if layer.startswith("A_"):
        return "A"
    if layer.startswith("B_"):
        return "B"
    if layer.startswith("C_"):
        return "C"
    if layer.startswith("D_"):
        return "D"

    return "UNKNOWN"


def closure_state(row: Dict[str, str]) -> str:
    closure_class = row.get("closure_class", "")

    if closure_class in {
        "FREE_INTEGER_CLOSURE",
        "FREE_NEUTRAL_CLOSURE",
        "COMPOSITE_INTEGER_CLOSURE",
        "COMPOSITE_NEUTRAL_CLOSURE",
    }:
        return "closed"

    if closure_class == "INTERNAL_FRACTIONAL_COORDINATE":
        return "internal_fractional"

    if closure_class == "TERMINAL_FREE_FRACTIONAL":
        return "not_closed"

    if closure_class in {
        "CONSTRAINED_NEUTRALITY_BOUNDARY",
        "EXTERNAL_NEUTRALITY_CONSTRAINT",
        "CONSTRAINED_CHARGE_VIOLATION_BOUNDARY",
    }:
        return "constrained"

    if closure_class == "UNRESOLVED_DUAL_BOUNDARY":
        return "unresolved"

    return "unresolved"


def make_bridge_row(
    source: Dict[str, str],
    value: float,
    encoding: str,
    bridge_id: str,
    bridge_label: str,
    bridge_layers: List[str],
) -> Dict[str, str]:
    return {
        "value": f"{value:.12g}",
        "bridge_id": bridge_id,
        "bridge_label": bridge_label,
        "bridge_layers": "".join(bridge_layers),
        "object_id": source.get("object_id", ""),
        "phase": source.get("phase", ""),
        "layer": source.get("layer", ""),
        "pdg_section": source.get("pdg_section", ""),
        "pdg_name": source.get("pdg_name", ""),
        "symbol": source.get("symbol", ""),
        "category": source.get("category", ""),
        "components": source.get("components", ""),
        "component_charges": source.get("component_charges", ""),
        "Q_over_e": source.get("Q_over_e", ""),
        "closure_class": source.get("closure_class", ""),
        "route_class": source.get("route_class", ""),
        "encoding": encoding,
        "source_file": source.get("source_file", ""),
        "source_note": source.get("source_note", ""),
        "notes": source.get("notes", ""),
    }


# ---------------------------------------------------------------------
# Encoding builders
# ---------------------------------------------------------------------

def value_for_encoding(row: Dict[str, str], encoding: str) -> Optional[float]:
    if encoding == "signed_charge":
        return parse_charge_to_float(row.get("Q_over_e", ""))

    if encoding == "absolute_charge":
        q = parse_charge_to_float(row.get("Q_over_e", ""))
        return None if q is None else abs(q)

    if encoding == "boundary_route_coordinate":
        closure_class = row.get("closure_class", "")
        return BOUNDARY_ROUTE_COORDINATE.get(closure_class)

    if encoding == "closure_class_code":
        closure_class = row.get("closure_class", "")
        return CLOSURE_CLASS_CODE.get(closure_class)

    if encoding == "closure_state_code":
        state = closure_state(row)
        return CLOSURE_STATE_CODE.get(state)

    if encoding == "route_class_code":
        route_class = row.get("route_class", "")
        return ROUTE_CLASS_CODE.get(route_class)

    raise ValueError(f"Unknown encoding: {encoding}")


def should_skip_bridge_encoding(bridge_id: str, bridge_layers: List[str], encoding: str) -> Tuple[bool, str]:
    """
    Layer D is a boundary marker. Do not generate charge-value encodings for
    bridges that include D, because D does not supply ordinary Q_over_e values.
    """
    if "D" in bridge_layers and encoding in {"signed_charge", "absolute_charge"}:
        return True, (
            "N/A: bridge includes Layer D; Layer D is a boundary-absence / "
            "constraint layer and should not be forced into signed/absolute charge ladders."
        )

    return False, ""


def build_bridge_ladder(
    rows: List[Dict[str, str]],
    bridge_id: str,
    bridge_info: Dict[str, object],
    encoding: str,
) -> Tuple[List[Dict[str, str]], Dict[str, object]]:
    bridge_layers = list(bridge_info["layers"])
    bridge_label = str(bridge_info["label"])

    skip, reason = should_skip_bridge_encoding(bridge_id, bridge_layers, encoding)
    if skip:
        return [], {
            "bridge_id": bridge_id,
            "bridge_label": bridge_label,
            "encoding": encoding,
            "status": "SKIPPED",
            "reason": reason,
            "row_count": 0,
            "unique_value_count": 0,
            "layer_counts": {},
            "values": [],
        }

    selected = [r for r in rows if layer_key(r) in bridge_layers]

    out: List[Dict[str, str]] = []
    skipped_rows = 0

    for r in selected:
        value = value_for_encoding(r, encoding)
        if value is None or not math.isfinite(value):
            skipped_rows += 1
            continue

        out.append(
            make_bridge_row(
                source=r,
                value=value,
                encoding=encoding,
                bridge_id=bridge_id,
                bridge_label=bridge_label,
                bridge_layers=bridge_layers,
            )
        )

    # Sort by numeric value, then layer route order, then object id. This keeps the
    # ladder numeric but preserves deterministic bridge provenance.
    layer_order = {layer: i for i, layer in enumerate(["A", "B", "C", "D"])}
    out.sort(
        key=lambda r: (
            float(r["value"]),
            layer_order.get(layer_key(r), 99),
            r["object_id"],
        )
    )

    values = [float(r["value"]) for r in out]
    layers_present = Counter(layer_key(r) for r in out)

    status = "OK" if out else "EMPTY"
    if out and len(layers_present) < len(bridge_layers):
        status = "PARTIAL"
    if out and len(set(values)) < 2:
        status = "LOW_VARIATION"

    diag = {
        "bridge_id": bridge_id,
        "bridge_label": bridge_label,
        "encoding": encoding,
        "status": status,
        "reason": "",
        "row_count": len(out),
        "source_rows_selected": len(selected),
        "source_rows_skipped_for_non_numeric_value": skipped_rows,
        "unique_value_count": len(set(values)),
        "min_value": min(values) if values else None,
        "max_value": max(values) if values else None,
        "layer_counts": dict(layers_present),
        "values": sorted(set(values)),
    }

    return out, diag


# ---------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------

def main() -> None:
    rows = read_csv(INPUT_FILE)

    layer_counts = Counter(layer_key(r) for r in rows)

    all_diags: List[Dict[str, object]] = []
    written_files: List[str] = []
    skipped_files: List[Dict[str, str]] = []

    for bridge_id, bridge_info in BRIDGES.items():
        stem = str(bridge_info["stem"])
        bridge_layers = list(bridge_info["layers"])

        for encoding in ENCODINGS:
            ladder_rows, diag = build_bridge_ladder(rows, bridge_id, bridge_info, encoding)
            all_diags.append(diag)

            if diag["status"] == "SKIPPED":
                skipped_files.append(
                    {
                        "bridge_id": bridge_id,
                        "encoding": encoding,
                        "reason": str(diag["reason"]),
                    }
                )
                continue

            if not ladder_rows:
                skipped_files.append(
                    {
                        "bridge_id": bridge_id,
                        "encoding": encoding,
                        "reason": "No numeric values generated.",
                    }
                )
                continue

            filename = f"{stem}_{encoding}.csv"

            provenance_path = OUT_DIR / filename
            write_csv(provenance_path, ladder_rows, PROVENANCE_FIELDS)
            written_files.append(str(provenance_path.relative_to(ROOT)))

            values = [float(r["value"]) for r in ladder_rows]
            one_column_path = ONE_COLUMN_DIR / filename
            write_one_column(one_column_path, values)
            written_files.append(str(one_column_path.relative_to(ROOT)))

    summary = {
        "project": "Charge Boundary Routing I",
        "phase": "Phase 2 — Bridge Tests",
        "generated": date.today().isoformat(),
        "input_file": str(INPUT_FILE.relative_to(ROOT)),
        "output_dir": str(OUT_DIR.relative_to(ROOT)),
        "one_column_dir": str(ONE_COLUMN_DIR.relative_to(ROOT)),
        "diagnostics_dir": str(DIAGNOSTICS_DIR.relative_to(ROOT)),
        "source_layer_counts": dict(layer_counts),
        "bridges": {
            bridge_id: {
                "label": info["label"],
                "layers": info["layers"],
                "description": info["description"],
                "stem": info["stem"],
            }
            for bridge_id, info in BRIDGES.items()
        },
        "encodings": ENCODINGS,
        "layer_D_rule": (
            "Bridges containing Layer D skip signed_charge and absolute_charge. "
            "Layer D participates only through boundary_route_coordinate, "
            "closure_class_code, closure_state_code, and route_class_code."
        ),
        "diagnostics": all_diags,
        "written_files": written_files,
        "skipped": skipped_files,
    }

    summary_path = DIAGNOSTICS_DIR / "phase2_bridge_ladder_generation_summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    report_path = DIAGNOSTICS_DIR / "phase2_bridge_ladder_generation_report.txt"
    write_report(report_path, summary)

    print("Phase 2 bridge ladders generated.")
    print(f"Project root: {ROOT}")
    print(f"Input:        {INPUT_FILE.relative_to(ROOT)}")
    print(f"Output:       {OUT_DIR.relative_to(ROOT)}")
    print(f"One-column:   {ONE_COLUMN_DIR.relative_to(ROOT)}")
    print(f"Diagnostics:  {DIAGNOSTICS_DIR.relative_to(ROOT)}")
    print()
    print(f"Files written: {len(written_files)}")
    print(f"Skipped cases: {len(skipped_files)}")
    print()
    print("Next:")
    print("    Start with B <-> C bridge.")
    print("    Upload one-column BC files to STRUC-PERC-I first, then STRUC-I.")


def write_report(path: Path, summary: Dict[str, object]) -> None:
    lines: List[str] = []

    lines.append("Charge Boundary Routing I")
    lines.append("Phase 2 — Bridge Ladder Generation Report")
    lines.append("phase2_bridge_ladder_generation_report.txt")
    lines.append("")
    lines.append(f"Generated: {summary['generated']}")
    lines.append("")
    lines.append("Purpose")
    lines.append("-------")
    lines.append("Generate bridge ladders for Phase 2 cross-layer tests:")
    lines.append("")
    lines.append("    A <-> B")
    lines.append("    B <-> C")
    lines.append("    C <-> D")
    lines.append("    A <-> B <-> C")
    lines.append("    B <-> C <-> D")
    lines.append("")
    lines.append("These ladders test where charge-route coherence first appears.")
    lines.append("")
    lines.append("Input")
    lines.append("-----")
    lines.append(f"    {summary['input_file']}")
    lines.append("")
    lines.append("Outputs")
    lines.append("-------")
    lines.append(f"    {summary['output_dir']}")
    lines.append(f"    {summary['one_column_dir']}")
    lines.append(f"    {summary['diagnostics_dir']}")
    lines.append("")
    lines.append("Layer D Rule")
    lines.append("------------")
    lines.append(str(summary["layer_D_rule"]))
    lines.append("")
    lines.append("Source Layer Counts")
    lines.append("-------------------")
    for layer, count in sorted(summary["source_layer_counts"].items()):
        lines.append(f"    {layer}: {count}")
    lines.append("")
    lines.append("Bridge Diagnostics")
    lines.append("------------------")

    for diag in summary["diagnostics"]:
        lines.append("")
        lines.append(f"{diag['bridge_id']} | {diag['bridge_label']} | {diag['encoding']}")
        lines.append(f"    status: {diag['status']}")
        if diag.get("reason"):
            lines.append(f"    reason: {diag['reason']}")
        lines.append(f"    row_count: {diag['row_count']}")
        lines.append(f"    unique_value_count: {diag['unique_value_count']}")
        lines.append(f"    layer_counts: {diag['layer_counts']}")
        lines.append(f"    values: {diag['values']}")

    lines.append("")
    lines.append("Recommended First Run")
    lines.append("---------------------")
    lines.append("Start with the B <-> C bridge because it tests the central physical route:")
    lines.append("")
    lines.append("    confined fractional coordinates -> composite closures")
    lines.append("")
    lines.append("Upload the one-column BC files first to STRUC-PERC-I, then STRUC-I.")
    lines.append("")
    lines.append("Do not begin with C <-> D until B <-> C is checked, because Layer D is")
    lines.append("a boundary-marker layer and only becomes meaningful through a bridge.")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
