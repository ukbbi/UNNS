#!/usr/bin/env python3
"""
build_charge_ladders.py

Charge Boundary Routing I
Generate chamber-ready numeric CSV ladder files from the verified Phase 1
canonical corpus.

Input:
    data/derived/charge_boundary_phase1_combined.csv

Outputs:
    ladders/layerA_external_charge_ladder.csv
    ladders/layerB_fractional_charge_ladder.csv
    ladders/layerC_composite_closure_ladder.csv
    ladders/layerD_boundary_absence_ladder.csv
    ladders/ABCD_charge_boundary_ladder.csv

    ladders/diagnostics/charge_ladder_generation_summary.json
    ladders/diagnostics/charge_ladder_generation_report.txt

These ladder files are intended for later upload into STRUC-PERC-I and STRUC-I.

Important:
    These are numeric encodings derived from a curated corpus.
    They are not new physics data.
    They are structural ladders for testing charge-boundary routing behavior.
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


ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "derived" / "charge_boundary_phase1_combined.csv"
LADDERS_DIR = ROOT / "ladders"
DIAGNOSTICS_DIR = LADDERS_DIR / "diagnostics"

LADDERS_DIR.mkdir(parents=True, exist_ok=True)
DIAGNOSTICS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# Numeric coding maps
# ---------------------------------------------------------------------

CLOSURE_CLASS_CODE = {
    "FREE_NEUTRAL_CLOSURE": 0.0,
    "FREE_INTEGER_CLOSURE": 1.0,
    "INTERNAL_FRACTIONAL_COORDINATE": 2.0,
    "COMPOSITE_NEUTRAL_CLOSURE": 3.0,
    "COMPOSITE_INTEGER_CLOSURE": 4.0,
    "TERMINAL_FREE_FRACTIONAL": 5.0,
    "UNRESOLVED_DUAL_BOUNDARY": 6.0,
    "CONSTRAINED_NEUTRALITY_BOUNDARY": 7.0,
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

# This coordinate is not a physical observable. It is an ordered UNNS route
# coordinate for boundary-routing tests.
BOUNDARY_ROUTE_COORDINATE = {
    "FREE_NEUTRAL_CLOSURE": 0.00,
    "FREE_INTEGER_CLOSURE": 0.25,
    "INTERNAL_FRACTIONAL_COORDINATE": 0.50,
    "COMPOSITE_NEUTRAL_CLOSURE": 0.75,
    "COMPOSITE_INTEGER_CLOSURE": 1.00,
    "TERMINAL_FREE_FRACTIONAL": 1.25,
    "UNRESOLVED_DUAL_BOUNDARY": 1.50,
    "CONSTRAINED_NEUTRALITY_BOUNDARY": 1.75,
    "CONSTRAINED_CHARGE_VIOLATION_BOUNDARY": 2.00,
}

# Closure-state code is designed to emphasize whether a row is closed,
# open/not-closed, constrained, or unresolved.
CLOSURE_STATE_CODE = {
    "closed": 0.0,
    "internal_fractional": 1.0,
    "not_closed": 2.0,
    "constrained": 3.0,
    "unresolved": 4.0,
}


LADDER_FIELDS = [
    "value",
    "object_id",
    "layer",
    "pdg_name",
    "symbol",
    "category",
    "Q_over_e",
    "closure_class",
    "route_class",
    "encoding",
    "source_file",
    "notes",
]


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing input file: {path}\n"
            "Run scripts/build_phase1_verified_corpus.py first."
        )

    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_ladder(path: Path, rows: List[Dict[str, str]]) -> None:
    rows_sorted = sorted(rows, key=lambda r: (float(r["value"]), r["object_id"]))

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LADDER_FIELDS)
        writer.writeheader()
        writer.writerows(rows_sorted)


def parse_charge_to_float(raw: str) -> Optional[float]:
    """
    Parse Q_over_e values such as:
        -1, +1, 0, +2/3, -1/3, fractional

    Returns None for non-numeric boundary labels.
    """
    if raw is None:
        return None

    s = raw.strip()
    if not s:
        return None

    # Known non-numeric or constraint values
    lowered = s.lower()
    if lowered in {
        "fractional",
        "not_electric_charge",
        "forbidden_transition",
        "constraint",
        "not_applicable",
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
        "CONSTRAINED_CHARGE_VIOLATION_BOUNDARY",
    }:
        return "constrained"

    if closure_class == "UNRESOLVED_DUAL_BOUNDARY":
        return "unresolved"

    return "unresolved"


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
    return "UNKNOWN"


def make_ladder_row(row: Dict[str, str], value: float, encoding: str) -> Dict[str, str]:
    return {
        "value": f"{value:.12g}",
        "object_id": row.get("object_id", ""),
        "layer": row.get("layer", ""),
        "pdg_name": row.get("pdg_name", ""),
        "symbol": row.get("symbol", ""),
        "category": row.get("category", ""),
        "Q_over_e": row.get("Q_over_e", ""),
        "closure_class": row.get("closure_class", ""),
        "route_class": row.get("route_class", ""),
        "encoding": encoding,
        "source_file": row.get("source_file", ""),
        "notes": row.get("notes", ""),
    }


def build_signed_charge_ladder(rows: Iterable[Dict[str, str]], encoding: str) -> List[Dict[str, str]]:
    out = []
    for r in rows:
        value = parse_charge_to_float(r.get("Q_over_e", ""))
        if value is not None and math.isfinite(value):
            out.append(make_ladder_row(r, value, encoding))
    return out


def build_absolute_charge_ladder(rows: Iterable[Dict[str, str]], encoding: str) -> List[Dict[str, str]]:
    out = []
    for r in rows:
        value = parse_charge_to_float(r.get("Q_over_e", ""))
        if value is not None and math.isfinite(value):
            out.append(make_ladder_row(r, abs(value), encoding))
    return out


def build_closure_class_ladder(rows: Iterable[Dict[str, str]], encoding: str) -> List[Dict[str, str]]:
    out = []
    for r in rows:
        closure_class = r.get("closure_class", "")
        if closure_class in CLOSURE_CLASS_CODE:
            out.append(make_ladder_row(r, CLOSURE_CLASS_CODE[closure_class], encoding))
    return out


def build_route_class_ladder(rows: Iterable[Dict[str, str]], encoding: str) -> List[Dict[str, str]]:
    out = []
    for r in rows:
        route_class = r.get("route_class", "")
        if route_class in ROUTE_CLASS_CODE:
            out.append(make_ladder_row(r, ROUTE_CLASS_CODE[route_class], encoding))
    return out


def build_boundary_route_ladder(rows: Iterable[Dict[str, str]], encoding: str) -> List[Dict[str, str]]:
    out = []
    for r in rows:
        closure_class = r.get("closure_class", "")
        if closure_class in BOUNDARY_ROUTE_COORDINATE:
            out.append(make_ladder_row(r, BOUNDARY_ROUTE_COORDINATE[closure_class], encoding))
    return out


def build_closure_state_ladder(rows: Iterable[Dict[str, str]], encoding: str) -> List[Dict[str, str]]:
    out = []
    for r in rows:
        state = closure_state(r)
        out.append(make_ladder_row(r, CLOSURE_STATE_CODE[state], encoding))
    return out


def write_encoding_set(prefix: str, rows: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Write multiple numeric encodings for the given row subset.

    STRUC-PERC-I and STRUC-I can use any one of these CSV files. The
    'signed_charge' and 'absolute_charge' encodings are closest to charge data.
    The class-coded encodings are route-topology encodings.
    """
    encoders = {
        "signed_charge": build_signed_charge_ladder,
        "absolute_charge": build_absolute_charge_ladder,
        "closure_class_code": build_closure_class_ladder,
        "route_class_code": build_route_class_ladder,
        "boundary_route_coordinate": build_boundary_route_ladder,
        "closure_state_code": build_closure_state_ladder,
    }

    counts = {}
    for encoding, fn in encoders.items():
        ladder_rows = fn(rows, encoding)
        filename = f"{prefix}_{encoding}.csv"
        write_ladder(LADDERS_DIR / filename, ladder_rows)
        counts[filename] = len(ladder_rows)

    return counts


def main() -> None:
    rows = read_csv(INPUT_FILE)

    layers: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for r in rows:
        layers[layer_key(r)].append(r)

    generated_counts: Dict[str, int] = {}

    layer_prefixes = {
        "A": "layerA_external_charge_ladder",
        "B": "layerB_fractional_charge_ladder",
        "C": "layerC_composite_closure_ladder",
        "D": "layerD_boundary_absence_ladder",
    }

    for key, prefix in layer_prefixes.items():
        generated_counts.update(write_encoding_set(prefix, layers.get(key, [])))

    generated_counts.update(write_encoding_set("ABCD_charge_boundary_ladder", rows))

    # Minimal one-column files for easy manual chamber upload.
    # These contain only a single 'value' column.
    one_col_dir = LADDERS_DIR / "one_column"
    one_col_dir.mkdir(parents=True, exist_ok=True)

    for ladder_file in sorted(LADDERS_DIR.glob("*.csv")):
        with ladder_file.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            values = [r["value"] for r in reader]

        one_col_path = one_col_dir / ladder_file.name
        with one_col_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["value"])
            for v in values:
                writer.writerow([v])

    closure_counts = Counter(r.get("closure_class", "") for r in rows)
    route_counts = Counter(r.get("route_class", "") for r in rows)
    layer_counts = Counter(layer_key(r) for r in rows)

    summary = {
        "project": "Charge Boundary Routing I",
        "generated_on": str(date.today()),
        "input_file": str(INPUT_FILE.relative_to(ROOT)),
        "output_folder": str(LADDERS_DIR.relative_to(ROOT)),
        "total_input_rows": len(rows),
        "layer_counts": dict(sorted(layer_counts.items())),
        "closure_class_counts": dict(sorted(closure_counts.items())),
        "route_class_counts": dict(sorted(route_counts.items())),
        "generated_ladder_files": dict(sorted(generated_counts.items())),
        "one_column_folder": str(one_col_dir.relative_to(ROOT)),
        "note": (
            "Full CSV files preserve provenance columns. Files in ladders/one_column/ "
            "contain only the numeric value column for chamber upload."
        ),
    }

    with (DIAGNOSTICS_DIR / "charge_ladder_generation_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    report_lines = [
        "Charge Boundary Routing I",
        "Charge Ladder Generation Report",
        "",
        f"Generated: {summary['generated_on']}",
        f"Input:     {summary['input_file']}",
        f"Rows:      {summary['total_input_rows']}",
        "",
        "Generated ladder files:",
    ]

    for name, count in sorted(generated_counts.items()):
        report_lines.append(f"  - {name}: {count} rows")

    report_lines.extend([
        "",
        "One-column chamber-upload copies:",
        f"  - {summary['one_column_folder']}/",
        "",
        "Recommended first chamber tests:",
        "  1. ladders/one_column/ABCD_charge_boundary_ladder_signed_charge.csv",
        "  2. ladders/one_column/ABCD_charge_boundary_ladder_absolute_charge.csv",
        "  3. ladders/one_column/ABCD_charge_boundary_ladder_boundary_route_coordinate.csv",
        "  4. ladders/one_column/layerC_composite_closure_ladder_signed_charge.csv",
        "",
        "Interpretation caution:",
        "  These files are numeric structural encodings of the canonical corpus.",
        "  They are intended for STRUC-PERC-I / STRUC-I exploratory testing.",
        "  They are not a final physical law and not a replacement for the source corpus.",
        "",
    ])

    (DIAGNOSTICS_DIR / "charge_ladder_generation_report.txt").write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    print("WROTE CHARGE LADDER FILES")
    print(f"Input rows:       {len(rows)}")
    print(f"Ladders folder:   {LADDERS_DIR}")
    print(f"One-column files: {one_col_dir}")
    print(f"Diagnostics:      {DIAGNOSTICS_DIR}")


if __name__ == "__main__":
    main()
