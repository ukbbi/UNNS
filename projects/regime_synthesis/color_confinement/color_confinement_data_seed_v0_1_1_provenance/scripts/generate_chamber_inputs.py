#!/usr/bin/env python3
"""
Generate chamber-ready single-column ladder CSV files for the
UNNS + color confinement investigation.

Run from the project root:

    python scripts/generate_chamber_inputs.py

Expected inputs, preferably in reports/:
    reports/baker_flux_profile_trusted_summary.csv
    reports/repair_threshold_window_static_gaps.csv

The script writes:
    chamber_inputs/*.csv

These outputs are deliberately single-column CSV files with header `value`,
because STRUC-I and STRUC-PERC-I ingest ordered numeric ladders rather than
multi-column physics tables.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

ROOT = Path.cwd()
OUT_DIR = ROOT / "chamber_inputs"
REPORTS = ROOT / "reports"


def find_file(name: str) -> Path:
    """Find an input file in likely project locations."""
    candidates = [
        REPORTS / name,
        ROOT / name,
        ROOT / "data" / name,
        ROOT / "data" / "03_core_flux_tube_profiles" / name,
        ROOT / "data" / "01_core_static_potential" / name,
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(
        f"Could not find {name}. Expected it in reports/ or the project root."
    )


def read_table(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def as_float(value: str) -> Optional[float]:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(x) or math.isinf(x):
        return None
    return x


def write_ladder(path: Path, values: Iterable[float]) -> int:
    vals = [v for v in values if v is not None and math.isfinite(v)]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["value"])
        for v in vals:
            w.writerow([f"{v:.12g}"])
    return len(vals)


def write_manifest(rows: List[Dict[str, str]]) -> None:
    path = OUT_DIR / "chamber_input_manifest.csv"
    fieldnames = [
        "file",
        "source_table",
        "source_filter",
        "source_column",
        "rows",
        "units",
        "intended_chamber_use",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def write_boundary_pressure_schema() -> None:
    path = OUT_DIR / "boundary_pressure_proxy_ladder_SCHEMA.csv"
    rows = [
        {
            "field": "value",
            "meaning": "future scalar boundary-pressure proxy value per ordered sample",
            "formula_or_source": "to be defined after measured or digitized V0(r), V1(r), V2(r) points near r_c and r_cs are available",
            "status": "SCHEMA_ONLY_NOT_A_CHAMBER_INPUT_YET",
        },
        {
            "field": "candidate_formula_1",
            "meaning": "gap-compression proxy",
            "formula_or_source": "B_gap(r) = 1 / min(gap01(r), gap12(r)) after uncertainty propagation",
            "status": "candidate_only",
        },
        {
            "field": "candidate_formula_2",
            "meaning": "threshold-proximity weighted pressure proxy",
            "formula_or_source": "B_thr(r) = B_gap(r) * exp(-min(|r-r_c|, |r-r_cs|)/lambda_r)",
            "status": "candidate_only",
        },
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["field", "meaning", "formula_or_source", "status"])
        w.writeheader()
        w.writerows(rows)


def write_readme(manifest_rows: List[Dict[str, str]], trusted_source: Path, repair_source: Path) -> None:
    lines = []
    lines.append("# Chamber Inputs — UNNS + Color Confinement\n")
    lines.append("These files are chamber-ready ordered numeric ladders generated from QC-clean confinement diagnostics.\n")
    lines.append("## Source inputs\n")
    lines.append(f"- Trusted Baker flux profile summary: `{trusted_source}`\n")
    lines.append(f"- Repair-window static gaps: `{repair_source}`\n")
    lines.append("\n## Rule\n")
    lines.append("Each chamber input CSV is deliberately single-column with header `value`. Do not add metadata columns to these ladder files, because STRUC-I and STRUC-PERC-I ingest numeric ladders. Provenance is kept in `chamber_input_manifest.csv`.\n")
    lines.append("\n## Generated ladder files\n")
    for row in manifest_rows:
        lines.append(f"- `{row['file']}` — {row['intended_chamber_use']} ({row['rows']} values; {row['units']})\n")
    lines.append("\n## How to run\n")
    lines.append("1. Upload up to six flux ladders into STRUC-I first.\n")
    lines.append("2. Export STRUC-I JSON/CSV.\n")
    lines.append("3. Run STRUC-PERC-I on the same ladder CSV files.\n")
    lines.append("4. Compare STRUC-I admissibility class with STRUC-PERC-I realizability/connectivity class.\n")
    lines.append("\n## Boundary\n")
    lines.append("These files are derived chamber inputs, not raw QCD data. They use the QC-accepted FULL/NP rows only. REVIEW_SEPARATELY rows are not mixed into these ladders.\n")
    (OUT_DIR / "README.md").write_text("".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    trusted_path = find_file("baker_flux_profile_trusted_summary.csv")
    repair_path = find_file("repair_threshold_window_static_gaps.csv")

    trusted_rows = read_table(trusted_path)
    repair_rows = read_table(repair_path)

    # Only accepted FULL / NP rows enter chamber trend ladders.
    accepted = [
        r for r in trusted_rows
        if r.get("qc_decision", "").strip() == "ACCEPT_FOR_TREND"
        and r.get("component", "").strip() in {"FULL", "NP"}
    ]

    manifest_rows: List[Dict[str, str]] = []

    flux_specs: List[Tuple[str, str, str, str, str]] = [
        ("FULL", "peak_field_GeV2", "flux_FULL_peak_trusted_ladder.csv", "GeV^2", "FULL flux-tube central/peak route-intensity ladder"),
        ("NP", "peak_field_GeV2", "flux_NP_peak_trusted_ladder.csv", "GeV^2", "nonperturbative peak route-intensity ladder"),
        ("FULL", "fwhm_estimate_fm", "flux_FULL_width_trusted_ladder.csv", "fm", "FULL flux-tube transverse-width ladder"),
        ("NP", "fwhm_estimate_fm", "flux_NP_width_trusted_ladder.csv", "fm", "nonperturbative transverse-width ladder"),
        ("FULL", "area_trapz_GeV2_fm", "flux_FULL_area_trusted_ladder.csv", "GeV^2 fm", "FULL integrated transverse route-strength ladder"),
        ("NP", "area_trapz_GeV2_fm", "flux_NP_area_trusted_ladder.csv", "GeV^2 fm", "nonperturbative integrated transverse route-strength ladder"),
    ]

    for component, col, fname, units, use in flux_specs:
        rows = [r for r in accepted if r.get("component", "").strip() == component]
        # Keep physical separation order for provenance/reproducibility. The chambers will sort internally as ladders.
        rows.sort(key=lambda r: (as_float(r.get("source_separation_fm", "")) or 0.0, as_float(r.get(col, "")) or 0.0))
        n = write_ladder(OUT_DIR / fname, (as_float(r.get(col, "")) for r in rows))
        manifest_rows.append({
            "file": fname,
            "source_table": str(trusted_path),
            "source_filter": f"component={component}; qc_decision=ACCEPT_FOR_TREND",
            "source_column": col,
            "rows": str(n),
            "units": units,
            "intended_chamber_use": use,
        })

    static_specs = [
        ("gap01_GeV", "static_gap01_repair_window_ladder.csv", "GeV", "repair-window V1-V0 channel-competition ladder"),
        ("gap12_GeV", "static_gap12_repair_window_ladder.csv", "GeV", "repair-window V2-V1 channel-competition ladder"),
    ]

    # Repair-window rows are already local-window rows; keep by r_fm.
    repair_rows.sort(key=lambda r: as_float(r.get("r_fm", "")) or 0.0)
    for col, fname, units, use in static_specs:
        n = write_ladder(OUT_DIR / fname, (as_float(r.get(col, "")) for r in repair_rows))
        manifest_rows.append({
            "file": fname,
            "source_table": str(repair_path),
            "source_filter": "threshold-window rows",
            "source_column": col,
            "rows": str(n),
            "units": units,
            "intended_chamber_use": use,
        })

    write_boundary_pressure_schema()
    manifest_rows.append({
        "file": "boundary_pressure_proxy_ladder_SCHEMA.csv",
        "source_table": "not generated yet",
        "source_filter": "schema only",
        "source_column": "future proxy value",
        "rows": "0",
        "units": "dimension depends on proxy",
        "intended_chamber_use": "placeholder for future boundary-pressure proxy ladder; not used as chamber input yet",
    })

    write_manifest(manifest_rows)
    write_readme(manifest_rows, trusted_path, repair_path)

    print("CHAMBER INPUT GENERATION COMPLETE")
    print(f"Output folder: {OUT_DIR}")
    for row in manifest_rows:
        print(f"- {row['file']}: {row['rows']} rows")


if __name__ == "__main__":
    main()
