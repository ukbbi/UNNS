#!/usr/bin/env python3
"""
a_inlists_to_stage_ladder.py

Phase A scaffold converter for STELLAR_BOUNDARY_DYNAMICS_I.

Reads the archived MESA test-suite source folders:

  A1_12M_pre_ms_to_core_collapse/
  A2_20M_pre_ms_to_core_collapse/

and writes first-pass structural-stage scaffold ladders:

  ladders/A1_12M_stage_ladder.csv
  ladders/A2_20M_stage_ladder.csv

This script does NOT parse MESA history.data or profile*.data.
It creates a scaffold ladder from the known MESA inlist stage chain.

Usage from A_mesa_precollapse_tracks/:

  python tools/a_inlists_to_stage_ladder.py --batch .

Single folder example:

  python tools/a_inlists_to_stage_ladder.py A1_12M_pre_ms_to_core_collapse ladders/A1_12M_stage_ladder.csv
"""

import argparse
import csv
from pathlib import Path


OUTPUT_COLUMNS = [
    "ladder_id",
    "source_id",
    "source_name",
    "object_name",
    "mass_class",
    "stage_index",
    "phase_name",
    "inlist_name",
    "inlist_present",
    "stage_role",
    "stage_weight",
    "expected_physical_state",
    "boundary_role",
    "struc_perc_role",
    "unns_interpretation",
    "raw_reference",
]


STAGE_CHAIN = [
    {
        "stage_index": 1,
        "phase_name": "late_pre_zams",
        "inlist_name": "inlist_make_late_pre_zams",
        "stage_role": "initial_relaxation",
        "stage_weight": 1.0,
        "expected_physical_state": "pre-main-sequence stellar relaxation before zero-age main sequence",
        "boundary_role": "baseline_initialization",
        "struc_perc_role": "scaffold_ladder_state",
        "unns_interpretation": "initial structural placement before main-sequence evolution",
    },
    {
        "stage_index": 2,
        "phase_name": "zams",
        "inlist_name": "inlist_to_zams",
        "stage_role": "main_sequence_entry",
        "stage_weight": 1.2,
        "expected_physical_state": "zero-age main sequence entry",
        "boundary_role": "stable_burning_entry",
        "struc_perc_role": "scaffold_ladder_state",
        "unns_interpretation": "entry into sustained hydrogen-burning structural regime",
    },
    {
        "stage_index": 3,
        "phase_name": "end_core_he_burn",
        "inlist_name": "inlist_to_end_core_he_burn",
        "stage_role": "helium_depletion_boundary",
        "stage_weight": 1.6,
        "expected_physical_state": "core helium depletion",
        "boundary_role": "composition_transition",
        "struc_perc_role": "scaffold_transition_state",
        "unns_interpretation": "composition-space transition after helium-burning exhaustion",
    },
    {
        "stage_index": 4,
        "phase_name": "end_core_c_burn",
        "inlist_name": "inlist_to_end_core_c_burn",
        "stage_role": "carbon_depletion_boundary",
        "stage_weight": 2.1,
        "expected_physical_state": "core carbon depletion",
        "boundary_role": "advanced_burning_transition",
        "struc_perc_role": "scaffold_transition_state",
        "unns_interpretation": "advanced burning transition approaching late stellar instability",
    },
    {
        "stage_index": 5,
        "phase_name": "lgTmax_silicon_approach",
        "inlist_name": "inlist_to_lgTmax",
        "stage_role": "silicon_burning_approach",
        "stage_weight": 2.8,
        "expected_physical_state": "central temperature approaches logT threshold near silicon-burning regime",
        "boundary_role": "precollapse_boundary_approach",
        "struc_perc_role": "scaffold_transition_state",
        "unns_interpretation": "approach to high-temperature pre-collapse boundary regime",
    },
    {
        "stage_index": 6,
        "phase_name": "core_collapse",
        "inlist_name": "inlist_to_cc",
        "stage_role": "collapse_endpoint",
        "stage_weight": 3.7,
        "expected_physical_state": "core-collapse endpoint in MESA test-suite stage chain",
        "boundary_role": "collapse_boundary",
        "struc_perc_role": "scaffold_endpoint_state",
        "unns_interpretation": "terminal pre-collapse scaffold state before post-boundary response",
    },
]


def infer_source(folder: Path):
    name = folder.name
    if name.startswith("A1_12M"):
        return {
            "source_id": "A1",
            "object_name": "12M_pre_ms_to_core_collapse",
            "mass_class": "12M",
            "ladder_id": "A1_12M",
        }
    if name.startswith("A2_20M"):
        return {
            "source_id": "A2",
            "object_name": "20M_pre_ms_to_core_collapse",
            "mass_class": "20M",
            "ladder_id": "A2_20M",
        }

    # Fallback for custom names.
    mass = "unknown"
    if "12M" in name:
        mass = "12M"
    elif "20M" in name:
        mass = "20M"

    source_id = name.split("_")[0] if "_" in name else name
    return {
        "source_id": source_id,
        "object_name": name,
        "mass_class": mass,
        "ladder_id": source_id,
    }


def find_inlist(folder: Path, inlist_name: str):
    """
    Check top level first, then one-level recursive search.
    MESA test-suite folders usually keep the inlists in the top directory.
    """
    direct = folder / inlist_name
    if direct.exists():
        return direct

    matches = list(folder.glob(f"**/{inlist_name}"))
    if matches:
        return matches[0]

    return None


def build_rows(folder: Path):
    meta = infer_source(folder)
    rows = []

    for stage in STAGE_CHAIN:
        inlist_path = find_inlist(folder, stage["inlist_name"])
        present = "yes" if inlist_path else "no"
        raw_ref = str(inlist_path) if inlist_path else str(folder / stage["inlist_name"])

        rows.append({
            "ladder_id": meta["ladder_id"],
            "source_id": meta["source_id"],
            "source_name": "MESA test-suite pre-MS to core-collapse source folder",
            "object_name": meta["object_name"],
            "mass_class": meta["mass_class"],
            "stage_index": stage["stage_index"],
            "phase_name": stage["phase_name"],
            "inlist_name": stage["inlist_name"],
            "inlist_present": present,
            "stage_role": stage["stage_role"],
            "stage_weight": stage["stage_weight"],
            "expected_physical_state": stage["expected_physical_state"],
            "boundary_role": stage["boundary_role"],
            "struc_perc_role": stage["struc_perc_role"],
            "unns_interpretation": stage["unns_interpretation"],
            "raw_reference": raw_ref,
        })

    return rows


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def convert_one(input_folder, output_csv):
    folder = Path(input_folder)
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Input folder not found: {folder}")

    rows = build_rows(folder)
    write_csv(Path(output_csv), rows)

    present = sum(1 for r in rows if r["inlist_present"] == "yes")
    missing = len(rows) - present

    print(f"Converted: {folder}")
    print(f"Output: {output_csv}")
    print(f"Stages: {len(rows)}")
    print(f"Inlists present: {present}")
    print(f"Inlists missing: {missing}")


def batch_convert(root):
    root = Path(root)
    ladders_dir = root / "ladders"
    targets = [
        (root / "A1_12M_pre_ms_to_core_collapse", ladders_dir / "A1_12M_stage_ladder.csv"),
        (root / "A2_20M_pre_ms_to_core_collapse", ladders_dir / "A2_20M_stage_ladder.csv"),
    ]

    for folder, output in targets:
        convert_one(folder, output)


def parse_args():
    parser = argparse.ArgumentParser(description="Create Phase A stage scaffold ladders from MESA inlist folders.")
    parser.add_argument("paths", nargs="*", help="Single mode: input_folder output_csv. Batch mode: root folder.")
    parser.add_argument("--batch", action="store_true", help="Batch mode over A1/A2 folders.")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.batch:
        root = args.paths[0] if args.paths else "."
        batch_convert(root)
        return

    if len(args.paths) != 2:
        raise SystemExit(__doc__)

    convert_one(args.paths[0], args.paths[1])


if __name__ == "__main__":
    main()
