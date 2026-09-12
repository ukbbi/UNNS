#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
============================================================
UNNS Grid Sweep Runner
============================================================

Purpose
-------
Prepare normalized ladders for multiple STRUC-PERC-I
κ-grid validation runs.

This version DOES NOT automate STRUC-PERC-I.

Instead it creates:

    grid_runs/
        GRID_A/
        GRID_B/
        GRID_C/
        ...

Each folder contains:
    • copied normalized ladders
    • κ-grid metadata
    • run instructions

Scientific Goal
----------------
Validate that:

    • regime classes survive grid refinement
    • κ thresholds remain stable
    • discretization is not a numerical artifact

============================================================
"""

import shutil
from pathlib import Path

# ==========================================================
# CONFIG
# ==========================================================

INPUT_DIR = "normalized_ladders"
OUTPUT_DIR = "grid_runs"

GRID_CONFIGS = {

    "GRID_A": {
        "k_min": 0.01,
        "k_max": 1.0,
        "k_points": 17,
        "description": "Baseline"
    },

    "GRID_B": {
        "k_min": 0.01,
        "k_max": 1.0,
        "k_points": 33,
        "description": "Refined grid"
    },

    "GRID_C": {
        "k_min": 0.01,
        "k_max": 1.0,
        "k_points": 65,
        "description": "High-resolution grid"
    },

    "GRID_D": {
        "k_min": 0.01,
        "k_max": 1.0,
        "k_points": 129,
        "description": "Ultra-refined grid"
    },

    "GRID_E": {
        "k_min": 0.005,
        "k_max": 1.0,
        "k_points": 65,
        "description": "Lower κ perturbation"
    },

    "GRID_F": {
        "k_min": 0.01,
        "k_max": 1.25,
        "k_points": 65,
        "description": "Upper κ extension"
    },

    "GRID_G": {
        "k_min": 0.001,
        "k_max": 2.0,
        "k_points": 65,
        "description": "Extreme perturbation"
    }
}

# ==========================================================
# HELPERS
# ==========================================================

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def list_ladders():
    return sorted(Path(INPUT_DIR).glob("*.txt"))


def write_metadata(grid_dir, grid_name, cfg):

    meta_path = grid_dir / "GRID_METADATA.txt"

    with open(meta_path, "w", encoding="utf-8") as f:

        f.write("====================================================\n")
        f.write("UNNS STRUC-PERC-I GRID SWEEP CONFIGURATION\n")
        f.write("====================================================\n\n")

        f.write(f"GRID NAME: {grid_name}\n")
        f.write(f"DESCRIPTION: {cfg['description']}\n\n")

        f.write("κ PARAMETERS\n")
        f.write("------------------------------\n")
        f.write(f"k_min    = {cfg['k_min']}\n")
        f.write(f"k_max    = {cfg['k_max']}\n")
        f.write(f"k_points = {cfg['k_points']}\n\n")

        f.write("MANUAL STRUC-PERC-I PROCEDURE\n")
        f.write("-----------------------------------------\n")
        f.write("1. Open STRUC-PERC-I_v2_5_0.html\n")
        f.write("2. Set κ_min\n")
        f.write("3. Set κ_max\n")
        f.write("4. Set κ_points\n")
        f.write("5. Load ladders from this folder\n")
        f.write("6. Run phase mapping\n")
        f.write("7. Export regime map\n")
        f.write("8. Compare against other grids\n\n")

        f.write("TARGET VALIDATION\n")
        f.write("-----------------------------------------\n")
        f.write("Check whether:\n")
        f.write("• κ_connect survives refinement\n")
        f.write("• regime classes remain stable\n")
        f.write("• discretization persists\n")
        f.write("• thresholds remain continuous\n")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)
    print("UNNS GRID SWEEP PREPARATION")
    print("=" * 60)

    ladders = list_ladders()

    print(f"[OK] Normalized ladders found: {len(ladders)}")

    if not ladders:

        print("[ERROR] No ladders found.")
        print(f"Expected folder: {INPUT_DIR}")
        return

    ensure_dir(OUTPUT_DIR)

    # ------------------------------------------------------
    # CREATE GRID RUN DIRECTORIES
    # ------------------------------------------------------

    for grid_name, cfg in GRID_CONFIGS.items():

        print("\n" + "=" * 60)
        print(f"[GRID] {grid_name}")
        print("=" * 60)

        grid_dir = Path(OUTPUT_DIR) / grid_name

        ensure_dir(grid_dir)

        # ----------------------------------------------
        # WRITE METADATA
        # ----------------------------------------------

        write_metadata(grid_dir, grid_name, cfg)

        print("[OK] Metadata written")

        # ----------------------------------------------
        # COPY LADDERS
        # ----------------------------------------------

        copied = 0

        for ladder in ladders:

            dst = grid_dir / ladder.name

            shutil.copy2(ladder, dst)

            copied += 1

        print(f"[OK] Ladders copied: {copied}")

    print("\n" + "=" * 60)
    print("[DONE] Grid sweep preparation complete")
    print("=" * 60)

    print("\nGenerated:")
    print(f"    {OUTPUT_DIR}/")
    print("        GRID_A/")
    print("        GRID_B/")
    print("        GRID_C/")
    print("        GRID_D/")
    print("        GRID_E/")
    print("        GRID_F/")
    print("        GRID_G/")


# ==========================================================
# ENTRY
# ==========================================================

if __name__ == "__main__":
    main()