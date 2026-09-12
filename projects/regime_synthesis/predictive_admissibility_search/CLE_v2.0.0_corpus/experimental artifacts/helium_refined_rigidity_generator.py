# helium_refined_rigidity_generator.py
#
# CLE v2 — Helium Refined Rigidity Generator
#
# Purpose:
#   Rebuild helium rigidity grids using the FULL helium representation family,
#   weaker perturbation ranges, and finer sampling near the collapse boundary.
#
# Input:
#   CLE_PILOT_I/helium/
#       qmi/*.csv
#       zeeman/*.csv
#       delta/*.csv
#
# Output:
#   CLE_PILOT_I/helium/rigidity_refined/*.json
#
# Usage:
#   python helium_refined_rigidity_generator.py

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean, pstdev


ROOT = Path("CLE_PILOT_I/helium")
OUT_DIR = ROOT / "rigidity_refined"
OUT_DIR.mkdir(parents=True, exist_ok=True)


INPUT_FILES = {
    "qmi_spectrum": ROOT / "qmi" / "helium_spectrum_QM1.csv",
    "qmi_gap": ROOT / "qmi" / "helium_gap_structure_QM1.csv",
    "qmi_preprocessed": ROOT / "qmi" / "helium_QM1_preprocessed.csv",

    "zeeman_full": ROOT / "zeeman" / "helium_zeeman_ladder.csv",
    "zeeman_singlet": ROOT / "zeeman" / "helium_singlet_zeeman_ladder.csv",
    "zeeman_triplet": ROOT / "zeeman" / "helium_triplet_zeeman_ladder.csv",

    "delta_qmi_spectrum": ROOT / "delta" / "delta_qmi_spectrum.csv",
    "delta_qmi_gap": ROOT / "delta" / "delta_qmi_gap.csv",
    "delta_qmi_preprocessed": ROOT / "delta" / "delta_qmi_preprocessed.csv",
    "delta_zeeman_full": ROOT / "delta" / "delta_zeeman.csv",
    "delta_zeeman_singlet": ROOT / "delta" / "delta_zeeman_singlet.csv",
    "delta_zeeman_triplet": ROOT / "delta" / "delta_zeeman_triplet.csv",
}


# Coarse field: weak perturbation around identity
ALPHA_COARSE = [
    0.90, 0.925, 0.95, 0.975,
    1.00,
    1.025, 1.05, 1.075, 1.10,
]

MU_COARSE = [
    0.90, 0.925, 0.95, 0.975,
    1.00,
    1.025, 1.05, 1.075, 1.10,
]

# Fine boundary probe: very close to identity
ALPHA_FINE = [
    0.975, 0.985, 0.995,
    1.000,
    1.005, 1.015, 1.025,
]

MU_FINE = [
    0.975, 0.985, 0.995,
    1.000,
    1.005, 1.015, 1.025,
]


def load_numeric_csv(path: Path):
    values = []

    with open(path, "r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.reader(f)

        for row in reader:
            for cell in row:
                try:
                    v = float(str(cell).strip())
                    if math.isfinite(v):
                        values.append(v)
                except Exception:
                    pass

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


def local_connectivity_score(values):
    if len(values) < 2:
        return 0.0

    diffs = [
        abs(values[i + 1] - values[i])
        for i in range(len(values) - 1)
    ]

    avg_gap = mean(diffs)

    if len(diffs) > 1:
        gap_var = pstdev(diffs)
    else:
        gap_var = 0.0

    return math.exp(-(avg_gap + gap_var))


def global_dispersion_score(values):
    if not values:
        return 0.0

    s = pstdev(values) if len(values) > 1 else 0.0
    m = abs(mean(values))

    return math.exp(-(0.35 * s + 0.15 * m))


def tail_stability_score(values):
    if not values:
        return 0.0

    k = max(1, len(values) // 10)
    tail = values[-k:]

    tmean = abs(mean(tail))
    tstd = pstdev(tail) if len(tail) > 1 else 0.0

    return math.exp(-(0.25 * tmean + 0.25 * tstd))


def compute_gr(values):
    if len(values) < 2:
        return 0.0

    local = local_connectivity_score(values)
    global_s = global_dispersion_score(values)
    tail = tail_stability_score(values)

    gr = (
        0.45 * local
        + 0.40 * global_s
        + 0.15 * tail
    )

    return max(0.0, min(1.0, gr))


def verdict(gr):
    if gr >= 0.75:
        return "FULL"
    if gr >= 0.50:
        return "GIANT"
    return "FRAGMENTED"


def generate_grid(values, alpha_values, mu_values, grid_type):
    grid = []

    total = len(alpha_values) * len(mu_values)
    counter = 0

    for alpha in alpha_values:
        for mu in mu_values:
            counter += 1

            deformed = deform_values(values, alpha, mu)
            gr = compute_gr(deformed)

            cell = {
                "grid_type": grid_type,
                "alpha": alpha,
                "mu": mu,
                "GR": gr,
                "giantRatio": gr,
                "verdict": verdict(gr),
                "admissible": gr >= 0.50,
            }

            grid.append(cell)

            print(
                f"[{counter:03d}/{total}] "
                f"{grid_type:<6} "
                f"alpha={alpha:.3f} "
                f"mu={mu:.3f} "
                f"GR={gr:.5f} "
                f"{cell['verdict']}"
            )

    return grid


def export_payload(name, source_path, raw_values, values, coarse_grid, fine_grid):
    payload = {
        "meta": {
            "experiment": "helium_refined_rigidity",
            "encoding_id": name,
            "source_file": str(source_path),
            "raw_values": len(raw_values),
            "normalized_values": len(values),
            "coarse_points": len(coarse_grid),
            "fine_points": len(fine_grid),
            "total_points": len(coarse_grid) + len(fine_grid),
            "purpose": (
                "Resolve helium rigidity manifold using weaker "
                "perturbation and local identity-neighborhood sampling."
            ),
        },
        "source_file": str(source_path),
        "family": "helium_refined",
        "encoding_id": name,
        "points": len(values),
        "grid": coarse_grid + fine_grid,
    }

    out_path = OUT_DIR / f"{name}_refined_grid.json"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"saved: {out_path}")


def main():
    print()
    print("=" * 72)
    print("HELIUM REFINED RIGIDITY GENERATOR")
    print("=" * 72)
    print()

    for name, path in INPUT_FILES.items():
        print("-" * 72)
        print(f"encoding: {name}")
        print(f"source:   {path}")

        if not path.exists():
            print("SKIPPED: missing file")
            print()
            continue

        raw_values = load_numeric_csv(path)
        values = normalize_values(raw_values)

        print(f"raw values:        {len(raw_values)}")
        print(f"normalized values: {len(values)}")

        if len(values) < 2:
            print("SKIPPED: too few numeric values")
            print()
            continue

        print("generating coarse weak-perturbation grid...")
        coarse_grid = generate_grid(
            values,
            ALPHA_COARSE,
            MU_COARSE,
            "coarse",
        )

        print("generating fine identity-neighborhood grid...")
        fine_grid = generate_grid(
            values,
            ALPHA_FINE,
            MU_FINE,
            "fine",
        )

        export_payload(
            name=name,
            source_path=path,
            raw_values=raw_values,
            values=values,
            coarse_grid=coarse_grid,
            fine_grid=fine_grid,
        )

        print()

    print("=" * 72)
    print("Done.")
    print("=" * 72)


if __name__ == "__main__":
    main()