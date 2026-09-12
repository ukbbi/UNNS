# neutrino_rigidity_generator.py
#
# CLE v2 — Neutrino Rigidity Generator
#
# Purpose:
#   Build α–μ rigidity grids directly from neutrino ladder TXT files.
#
# Features:
#   - auto-detects ladder family from filename
#   - scans raw/ recursively
#   - computes admissibility rigidity field
#   - exports JSON rigidity grids
#   - preserves original archive structure
#
# Output:
#   CLE_PILOT_I/neutrino/rigidity/
#
# Usage:
#   python neutrino_rigidity_generator.py
#

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean, pstdev

# ============================================================
# PATHS
# ============================================================

ROOT = Path("CLE_PILOT_I/neutrino")
RAW_DIR = ROOT / "raw"
OUT_DIR = ROOT / "rigidity"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# PARAMETERS
# ============================================================

ALPHA_VALUES = [
    0.80,
    0.85,
    0.90,
    0.95,
    1.00,
    1.05,
    1.10,
    1.15,
    1.20,
]

MU_VALUES = [
    0.80,
    0.85,
    0.90,
    0.95,
    1.00,
    1.05,
    1.10,
    1.15,
    1.20,
]

# ============================================================
# FAMILY DETECTION
# ============================================================

def detect_family(filename: str) -> str:

    name = filename.lower()

    if "tmva" in name:
        return "tmva"

    if "deepl" in name:
        return "deepl"

    if "sig" in name:
        return "raw_sig"

    if "bkg" in name:
        return "raw_bkg"

    if "fib" in name:
        return "fib"

    return "misc"


# ============================================================
# LOADING
# ============================================================

def load_numeric_values(path: Path):

    values = []

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                parts = (
                    line.replace(",", " ")
                        .replace(";", " ")
                        .split()
                )

                for p in parts:

                    try:
                        v = float(p)

                        if math.isfinite(v):
                            values.append(v)

                    except:
                        pass

    except Exception as e:
        print(f"FAILED: {path}")
        print(e)

    return values


# ============================================================
# RIGIDITY FIELD
# ============================================================

def compute_gr(
    values,
    alpha,
    mu,
):

    if not values:
        return 0.0

    m = mean(values)

    if len(values) > 1:
        s = pstdev(values)
    else:
        s = 0.0

    drift = abs(m) * alpha
    variance_penalty = s * mu

    gr = math.exp(-(drift + variance_penalty))

    return max(0.0, min(1.0, gr))


# ============================================================
# GRID GENERATION
# ============================================================

def generate_grid(values):

    grid = []

    total = len(ALPHA_VALUES) * len(MU_VALUES)
    idx = 0

    for alpha in ALPHA_VALUES:

        for mu in MU_VALUES:

            idx += 1

            print(
                f"[{idx:02d}/{total}] "
                f"alpha={alpha:.2f} "
                f"mu={mu:.2f}"
            )

            gr = compute_gr(
                values=values,
                alpha=alpha,
                mu=mu,
            )

            cell = {
                "alpha": alpha,
                "mu": mu,
                "GR": gr,
                "admissible": gr >= 0.50,
            }

            grid.append(cell)

    return grid


# ============================================================
# EXPORT
# ============================================================

def export_grid(
    path: Path,
    payload,
):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("======================================")
    print("NEUTRINO RIGIDITY GENERATOR")
    print("======================================")
    print()

    txt_files = sorted(RAW_DIR.rglob("*.txt"))

    if not txt_files:
        print("No TXT ladders found.")
        return

    print(f"Found {len(txt_files)} ladder files")
    print()

    for txt_file in txt_files:

        family = detect_family(txt_file.name)

        print("------------------------------------------------")
        print(txt_file.name)
        print(f"family: {family}")

        values = load_numeric_values(txt_file)

        print(f"values loaded: {len(values)}")

        if len(values) < 10:
            print("SKIPPED (too few numeric values)")
            print()
            continue

        print("generating rigidity grid...")

        grid = generate_grid(values)

        payload = {
            "source_file": txt_file.name,
            "family": family,
            "points": len(values),
            "grid": grid,
        }

        out_name = (
            txt_file.stem
            + "_grid.json"
        )

        out_path = OUT_DIR / out_name

        export_grid(
            out_path,
            payload,
        )

        print(f"saved: {out_path}")
        print()

    print("Done.")
    print()


if __name__ == "__main__":
    main()