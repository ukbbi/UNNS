# cosmology_rigidity_generator.py
#
# CLE v2 — Cosmology Rigidity Generator
#
# Purpose:
#   Build α–μ rigidity grids from Planck cosmology JSON ladders.
#
# First cosmology experiment:
#   planck_EE_full.json
#   planck_TE_full.json
#   planck_TT_full.json
#
# Input:
#   CLE_PILOT_I/cosmology/raw/*.json
#
# Output:
#   CLE_PILOT_I/cosmology/rigidity/
#
# Usage:
#   python cosmology_rigidity_generator.py

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean, pstdev


ROOT = Path("CLE_PILOT_I/cosmology")
RAW_DIR = ROOT / "raw"
OUT_DIR = ROOT / "rigidity"
OUT_DIR.mkdir(parents=True, exist_ok=True)


ALPHA_VALUES = [0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20]
MU_VALUES = [0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20]


TARGET_FILES = {
    "planck_EE": "planck_EE_full.json",
    "planck_TE": "planck_TE_full.json",
    "planck_TT": "planck_TT_full.json",
}


def flatten_numeric(obj):
    values = []

    if isinstance(obj, dict):
        for value in obj.values():
            values.extend(flatten_numeric(value))

    elif isinstance(obj, list):
        for value in obj:
            values.extend(flatten_numeric(value))

    else:
        try:
            v = float(obj)
            if math.isfinite(v):
                values.append(v)
        except Exception:
            pass

    return values


def load_json_values(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    values = flatten_numeric(payload)

    return values


def normalize_values(values):
    if not values:
        return []

    m = mean(values)
    centered = [v - m for v in values]

    scale = max(abs(v) for v in centered)

    if scale == 0:
        return [0.0 for _ in centered]

    return [v / scale for v in centered]


def deform_values(values, alpha, mu):
    out = []

    for v in values:
        sign = -1.0 if v < 0 else 1.0
        mag = abs(v)

        y = sign * mu * (mag ** alpha)

        if math.isfinite(y):
            out.append(y)

    return out


def compute_gr(values):
    if not values:
        return 0.0

    m = abs(mean(values))
    s = pstdev(values) if len(values) > 1 else 0.0

    tail = mean(abs(v) for v in values[-max(1, len(values) // 10):])

    penalty = (
        0.60 * m
        + 0.35 * s
        + 0.05 * tail
    )

    gr = math.exp(-penalty)

    return max(0.0, min(1.0, gr))


def verdict_from_gr(gr):
    if gr >= 0.75:
        return "FULL"
    if gr >= 0.50:
        return "GIANT"
    return "FRAGMENTED"


def generate_grid(values):
    grid = []

    total = len(ALPHA_VALUES) * len(MU_VALUES)
    counter = 0

    for alpha in ALPHA_VALUES:
        for mu in MU_VALUES:
            counter += 1

            deformed = deform_values(values, alpha, mu)
            gr = compute_gr(deformed)

            cell = {
                "alpha": alpha,
                "mu": mu,
                "GR": gr,
                "giantRatio": gr,
                "verdict": verdict_from_gr(gr),
                "admissible": gr >= 0.50,
            }

            grid.append(cell)

            print(
                f"[{counter:02d}/{total}] "
                f"alpha={alpha:.2f} "
                f"mu={mu:.2f} "
                f"GR={gr:.5f} "
                f"{cell['verdict']}"
            )

    return grid


def export_grid(name, source_path, values, grid):
    payload = {
        "meta": {
            "experiment": "cosmology_planck_rigidity",
            "encoding_id": name,
            "source_file": source_path.name,
            "n_values": len(values),
            "alpha_range": [min(ALPHA_VALUES), max(ALPHA_VALUES)],
            "mu_range": [min(MU_VALUES), max(MU_VALUES)],
            "n_points": len(grid),
        },
        "source_file": source_path.name,
        "family": "planck",
        "encoding_id": name,
        "points": len(values),
        "grid": grid,
    }

    out_path = OUT_DIR / f"{name}_grid.json"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"saved: {out_path}")


def main():
    print()
    print("========================================")
    print("COSMOLOGY RIGIDITY GENERATOR")
    print("========================================")
    print()

    for name, filename in TARGET_FILES.items():
        path = RAW_DIR / filename

        print("----------------------------------------")
        print(f"encoding: {name}")
        print(f"source:   {path}")

        if not path.exists():
            print("SKIPPED: missing file")
            continue

        raw_values = load_json_values(path)
        values = normalize_values(raw_values)

        print(f"raw values:        {len(raw_values)}")
        print(f"normalized values: {len(values)}")
        print("generating grid...")

        if len(values) < 10:
            print("SKIPPED: too few numeric values")
            continue

        grid = generate_grid(values)

        export_grid(
            name=name,
            source_path=path,
            values=values,
            grid=grid,
        )

        print()

    print("Done.")
    print()


if __name__ == "__main__":
    main()