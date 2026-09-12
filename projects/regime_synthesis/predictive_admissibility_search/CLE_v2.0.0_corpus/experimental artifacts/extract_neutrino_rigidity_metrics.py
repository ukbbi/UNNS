# extract_neutrino_rigidity_metrics.py
#
# CLE v2 — Neutrino Rigidity Metrics Extractor
#
# Purpose:
#   Compute second-order rigidity observables
#   from neutrino α–μ rigidity grids.
#
# Input:
#   CLE_PILOT_I/neutrino/rigidity/*.json
#
# Output:
#   CLE_OUTPUT/neutrino/
#       neutrino_rigidity_metrics.json
#       neutrino_rigidity_metrics.csv
#
# Usage:
#   python extract_neutrino_rigidity_metrics.py
#

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean, pstdev

# ============================================================
# PATHS
# ============================================================

GRID_DIR = Path("CLE_PILOT_I/neutrino/rigidity")

OUT_DIR = Path("CLE_OUTPUT/neutrino")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "neutrino_rigidity_metrics.json"
CSV_OUT = OUT_DIR / "neutrino_rigidity_metrics.csv"

# ============================================================
# THRESHOLDS
# ============================================================

ADMISSIBILITY_THRESHOLD = 0.50

# ============================================================
# HELPERS
# ============================================================

def safe_mean(values):

    if not values:
        return 0.0

    return mean(values)


def safe_std(values):

    if len(values) < 2:
        return 0.0

    return pstdev(values)


# ============================================================
# METRIC COMPUTATIONS
# ============================================================

def full_region_volume(grs):

    if not grs:
        return 0.0

    admissible = [
        g for g in grs
        if g >= ADMISSIBILITY_THRESHOLD
    ]

    return len(admissible) / len(grs)


def collapse_onset_radius(grs):

    sorted_grs = sorted(grs)

    for idx, g in enumerate(sorted_grs):

        if g < ADMISSIBILITY_THRESHOLD:
            return idx / len(sorted_grs)

    return 1.0


def fragmentation_rate(grs):

    if not grs:
        return 1.0

    collapsed = [
        g for g in grs
        if g < ADMISSIBILITY_THRESHOLD
    ]

    return len(collapsed) / len(grs)


def admissibility_persistence(grs):

    if not grs:
        return 0.0

    stable = [
        g for g in grs
        if g >= 0.75
    ]

    return len(stable) / len(grs)


def bifurcation_sharpness(grs):

    if len(grs) < 2:
        return 0.0

    ordered = sorted(grs)

    diffs = []

    for i in range(len(ordered) - 1):
        diffs.append(abs(ordered[i + 1] - ordered[i]))

    return max(diffs)


def recovery_elasticity(grs):

    if not grs:
        return 0.0

    peak = max(grs)
    trough = min(grs)

    if peak == 0:
        return 0.0

    return (peak - trough) / peak


def anisotropic_persistence(grs):

    if not grs:
        return 0.0

    directional_spread = safe_std(grs)

    return math.exp(-directional_spread)


# ============================================================
# FAMILY DETECTION
# ============================================================

def detect_family(name):

    n = name.lower()

    if "tmva" in n:
        return "tmva"

    if "deepl" in n:
        return "deepl"

    if "sig" in n:
        return "raw_sig"

    if "bkg" in n:
        return "raw_bkg"

    if "fib" in n:
        return "fib"

    return "misc"


# ============================================================
# LOAD GRID
# ============================================================

def load_grid(path):

    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    return payload


# ============================================================
# PROCESS GRID
# ============================================================

def process_grid(path):

    payload = load_grid(path)

    grid = payload["grid"]

    grs = [
        cell["GR"]
        for cell in grid
    ]

    metrics = {

        "source_file":
            payload["source_file"],

        "family":
            detect_family(payload["source_file"]),

        "mean_gr":
            safe_mean(grs),

        "gr_variance":
            safe_std(grs),

        "full_region_volume":
            full_region_volume(grs),

        "collapse_onset_radius":
            collapse_onset_radius(grs),

        "fragmentation_rate":
            fragmentation_rate(grs),

        "admissibility_persistence":
            admissibility_persistence(grs),

        "bifurcation_sharpness":
            bifurcation_sharpness(grs),

        "recovery_elasticity":
            recovery_elasticity(grs),

        "anisotropic_persistence":
            anisotropic_persistence(grs),
    }

    return metrics


# ============================================================
# EXPORT
# ============================================================

def export_json(results):

    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


def export_csv(results):

    if not results:
        return

    keys = list(results[0].keys())

    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=keys,
        )

        writer.writeheader()

        for row in results:
            writer.writerow(row)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("========================================")
    print("EXTRACT NEUTRINO RIGIDITY METRICS")
    print("========================================")
    print()

    grid_files = sorted(
        GRID_DIR.glob("*_grid.json")
    )

    if not grid_files:
        print("No rigidity grids found.")
        return

    print(f"Found {len(grid_files)} grids")
    print()

    results = []

    for path in grid_files:

        print("----------------------------------------")
        print(path.name)

        metrics = process_grid(path)

        print(
            f"family={metrics['family']} | "
            f"GR={metrics['mean_gr']:.5f} | "
            f"persist={metrics['admissibility_persistence']:.5f} | "
            f"frag={metrics['fragmentation_rate']:.5f}"
        )

        results.append(metrics)

    export_json(results)
    export_csv(results)

    print()
    print("Exports written:")
    print(JSON_OUT)
    print(CSV_OUT)
    print()
    print("Done.")
    print()


if __name__ == "__main__":
    main()