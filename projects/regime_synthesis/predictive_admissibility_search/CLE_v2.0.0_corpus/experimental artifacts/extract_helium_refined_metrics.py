# extract_helium_refined_metrics.py
#
# CLE v2 — Helium Refined Metrics Extractor
#
# Input:
#   CLE_PILOT_I/helium/rigidity_refined/*_refined_grid.json
#
# Output:
#   CLE_OUTPUT/helium_refined/
#       helium_refined_metrics.json
#       helium_refined_metrics.csv
#
# Usage:
#   python extract_helium_refined_metrics.py

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean, pstdev


GRID_DIR = Path("CLE_PILOT_I/helium/rigidity_refined")

OUT_DIR = Path("CLE_OUTPUT/helium_refined")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "helium_refined_metrics.json"
CSV_OUT = OUT_DIR / "helium_refined_metrics.csv"

ADMISSIBILITY_THRESHOLD = 0.50
FULL_THRESHOLD = 0.75


def safe_mean(values):
    return mean(values) if values else 0.0


def safe_std(values):
    return pstdev(values) if len(values) > 1 else 0.0


def load_grid(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_grs(grid, grid_type=None):
    values = []

    for cell in grid:
        if grid_type is not None and cell.get("grid_type") != grid_type:
            continue

        try:
            g = float(cell.get("GR", 0.0))
            if math.isfinite(g):
                values.append(g)
        except Exception:
            pass

    return values


def full_region_volume(grs):
    if not grs:
        return 0.0

    return sum(g >= ADMISSIBILITY_THRESHOLD for g in grs) / len(grs)


def full_phase_fraction(grs):
    if not grs:
        return 0.0

    return sum(g >= FULL_THRESHOLD for g in grs) / len(grs)


def giant_phase_fraction(grs):
    if not grs:
        return 0.0

    return sum(
        ADMISSIBILITY_THRESHOLD <= g < FULL_THRESHOLD
        for g in grs
    ) / len(grs)


def fragmentation_rate(grs):
    if not grs:
        return 1.0

    return sum(g < ADMISSIBILITY_THRESHOLD for g in grs) / len(grs)


def collapse_onset_radius(grs):
    if not grs:
        return 0.0

    sorted_grs = sorted(grs)

    for idx, g in enumerate(sorted_grs):
        if g < ADMISSIBILITY_THRESHOLD:
            return idx / len(sorted_grs)

    return 1.0


def bifurcation_sharpness(grs):
    if len(grs) < 2:
        return 0.0

    ordered = sorted(grs)
    diffs = [
        abs(ordered[i + 1] - ordered[i])
        for i in range(len(ordered) - 1)
    ]

    return max(diffs) if diffs else 0.0


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

    return math.exp(-safe_std(grs))


def rigidity_gradient(grid):
    """
    Approximate α and μ response using cells nearest identity lines.
    """

    alpha_line = []
    mu_line = []

    for cell in grid:
        alpha = float(cell.get("alpha", 0.0))
        mu = float(cell.get("mu", 0.0))
        gr = float(cell.get("GR", 0.0))

        if abs(mu - 1.0) < 1e-9:
            alpha_line.append((alpha, gr))

        if abs(alpha - 1.0) < 1e-9:
            mu_line.append((mu, gr))

    alpha_line.sort()
    mu_line.sort()

    def slope(line):
        if len(line) < 2:
            return 0.0

        x0, y0 = line[0]
        x1, y1 = line[-1]

        if x1 == x0:
            return 0.0

        return (y1 - y0) / (x1 - x0)

    return slope(alpha_line), slope(mu_line)


def curvature_proxy(grs):
    if len(grs) < 3:
        return 0.0

    ordered = sorted(grs)

    second_diffs = []

    for i in range(1, len(ordered) - 1):
        second_diffs.append(
            abs(ordered[i + 1] - 2 * ordered[i] + ordered[i - 1])
        )

    return safe_mean(second_diffs)


def classify_refined_regime(metrics):
    gr = metrics["mean_gr"]
    frag = metrics["fragmentation_rate"]
    full = metrics["full_phase_fraction"]
    giant = metrics["giant_phase_fraction"]
    elasticity = metrics["recovery_elasticity"]

    if frag == 0.0 and full >= 0.95 and gr >= 0.80:
        return "REFINED_STABLE_FULL"

    if frag == 0.0 and full >= 0.70:
        return "REFINED_FULL_DOMINANT"

    if frag == 0.0 and giant > 0.20:
        return "REFINED_FULL_GIANT_BOUNDARY"

    if frag > 0.0 and elasticity > 0.20:
        return "REFINED_TRANSITIONAL"

    return "REFINED_INDETERMINATE"


def process_file(path: Path):
    payload = load_grid(path)

    grid = payload.get("grid", [])

    all_grs = extract_grs(grid)
    coarse_grs = extract_grs(grid, "coarse")
    fine_grs = extract_grs(grid, "fine")

    alpha_slope, mu_slope = rigidity_gradient(grid)

    metrics = {
        "source_file": payload.get("source_file", path.name),
        "encoding_id": payload.get("encoding_id", path.stem),
        "family": payload.get("family", "helium_refined"),
        "points": payload.get("points", 0),

        "grid_points": len(all_grs),
        "coarse_points": len(coarse_grs),
        "fine_points": len(fine_grs),

        "mean_gr": safe_mean(all_grs),
        "mean_gr_coarse": safe_mean(coarse_grs),
        "mean_gr_fine": safe_mean(fine_grs),

        "gr_variance": safe_std(all_grs),
        "gr_min": min(all_grs) if all_grs else 0.0,
        "gr_max": max(all_grs) if all_grs else 0.0,

        "full_region_volume": full_region_volume(all_grs),
        "collapse_onset_radius": collapse_onset_radius(all_grs),
        "fragmentation_rate": fragmentation_rate(all_grs),

        "full_phase_fraction": full_phase_fraction(all_grs),
        "giant_phase_fraction": giant_phase_fraction(all_grs),

        "admissibility_persistence": full_phase_fraction(all_grs),

        "bifurcation_sharpness": bifurcation_sharpness(all_grs),
        "recovery_elasticity": recovery_elasticity(all_grs),
        "anisotropic_persistence": anisotropic_persistence(all_grs),

        "alpha_rigidity_slope": alpha_slope,
        "mu_rigidity_slope": mu_slope,
        "curvature_proxy": curvature_proxy(all_grs),
    }

    metrics["refined_regime"] = classify_refined_regime(metrics)

    return metrics


def export_json(rows):
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)


def export_csv(rows):
    if not rows:
        return

    keys = list(rows[0].keys())

    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()

        for row in rows:
            writer.writerow(row)


def main():
    print()
    print("=" * 72)
    print("EXTRACT HELIUM REFINED METRICS")
    print("=" * 72)
    print()

    files = sorted(GRID_DIR.glob("*_refined_grid.json"))

    if not files:
        print(f"No refined helium grids found in: {GRID_DIR}")
        return

    results = []

    for path in files:
        metrics = process_file(path)
        results.append(metrics)

        print(
            f"{metrics['encoding_id']:<24} | "
            f"GR={metrics['mean_gr']:.5f} | "
            f"FULL={metrics['full_phase_fraction']:.3f} | "
            f"GIANT={metrics['giant_phase_fraction']:.3f} | "
            f"frag={metrics['fragmentation_rate']:.3f} | "
            f"{metrics['refined_regime']}"
        )

    export_json(results)
    export_csv(results)

    print()
    print("Exports written:")
    print(JSON_OUT)
    print(CSV_OUT)
    print()
    print("Done.")


if __name__ == "__main__":
    main()