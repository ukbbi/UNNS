import json
import csv
import math
from pathlib import Path


# ===================================================
# EXTRACT RIGIDITY METRICS
# ===================================================
# Purpose:
#   Read helium rigidity grid JSON files and compute
#   second-order rigidity metrics for CLT analysis.
#
# Input:
#   CLE_PILOT_I/helium/rigidity/*.json
#
# Output:
#   CLE_OUTPUT/helium/rigidity_metrics.json
#   CLE_OUTPUT/helium/rigidity_metrics.csv
#
# Run from:
#   cle_v1_0_2/
#
# Command:
#   python extract_rigidity_metrics.py
# ===================================================


# ---------------------------------------------------
# PATHS
# ---------------------------------------------------

INPUT_DIR = Path("CLE_PILOT_I/helium/rigidity")
OUTPUT_DIR = Path("CLE_OUTPUT/helium")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUTPUT = OUTPUT_DIR / "rigidity_metrics.json"
CSV_OUTPUT = OUTPUT_DIR / "rigidity_metrics.csv"


# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------

def load_grid(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def euclidean_radius(alpha, mu):
    return math.sqrt((alpha - 1.0) ** 2 + (mu - 1.0) ** 2)


def safe_mean(values):
    if not values:
        return 0.0
    return sum(values) / len(values)


def safe_variance(values):
    if len(values) < 2:
        return 0.0

    m = safe_mean(values)

    return sum((x - m) ** 2 for x in values) / (len(values) - 1)


def verdict_is_full(point):
    return point.get("verdict") == "FULL"


def verdict_is_nonfull(point):
    return point.get("verdict") != "FULL"


def compute_full_region_volume(grid):
    if not grid:
        return 0.0

    full_count = sum(1 for p in grid if verdict_is_full(p))

    return full_count / len(grid)


def compute_admissibility_persistence(grid):
    """
    Fraction of grid preserving at least GIANT-level admissibility.

    FULL and GIANT count as admissible persistence.
    TAIL and HARD count as loss.
    """

    if not grid:
        return 0.0

    admissible = {
        "FULL",
        "GIANT",
    }

    count = sum(
        1 for p in grid
        if p.get("verdict") in admissible
    )

    return count / len(grid)


def compute_fragmentation_rate(grid):
    """
    Fraction of grid not FULL.
    """

    if not grid:
        return 0.0

    nonfull = sum(1 for p in grid if verdict_is_nonfull(p))

    return nonfull / len(grid)


def compute_collapse_onset_radius(grid):
    """
    Smallest distance from the physical point (1,1)
    where verdict stops being FULL.

    If no collapse found, return None.
    """

    radii = []

    for p in grid:
        if verdict_is_nonfull(p):
            radii.append(
                euclidean_radius(
                    float(p.get("alpha")),
                    float(p.get("mu")),
                )
            )

    if not radii:
        return None

    return min(radii)


def compute_kappa_variance(grid):
    vals = [
        float(p.get("kappaConn"))
        for p in grid
        if p.get("kappaConn") is not None
    ]

    return safe_variance(vals)


def compute_gr_variance(grid):
    vals = [
        float(p.get("giantRatio"))
        for p in grid
        if p.get("giantRatio") is not None
    ]

    return safe_variance(vals)


def compute_mean_tail_dominance(grid):
    vals = [
        float(p.get("tailDominance"))
        for p in grid
        if p.get("tailDominance") is not None
    ]

    return safe_mean(vals)


def compute_mean_n_iso(grid):
    vals = [
        float(p.get("nIso"))
        for p in grid
        if p.get("nIso") is not None
    ]

    return safe_mean(vals)


def compute_bifurcation_sharpness(grid):
    """
    Measures how abruptly FULL changes to non-FULL
    near the reference point.

    Operational proxy:
      max absolute jump in giantRatio between neighboring
      alpha/mu grid cells.

    Higher = sharper phase boundary.
    """

    if not grid:
        return 0.0

    # index points by (alpha, mu)
    points = {}

    for p in grid:
        a = round(float(p.get("alpha")), 6)
        m = round(float(p.get("mu")), 6)

        points[(a, m)] = p

    alphas = sorted(set(a for a, _ in points.keys()))
    mus = sorted(set(m for _, m in points.keys()))

    max_jump = 0.0

    for a in alphas:
        for m in mus:

            current = points.get((a, m))

            if current is None:
                continue

            current_gr = float(current.get("giantRatio"))

            # neighbor in alpha direction
            ai = alphas.index(a)
            mi = mus.index(m)

            neighbors = []

            if ai + 1 < len(alphas):
                neighbors.append((alphas[ai + 1], m))

            if mi + 1 < len(mus):
                neighbors.append((a, mus[mi + 1]))

            for nb in neighbors:
                q = points.get(nb)

                if q is None:
                    continue

                q_gr = float(q.get("giantRatio"))

                jump = abs(current_gr - q_gr)

                if jump > max_jump:
                    max_jump = jump

    return max_jump


def summarize_grid(path):
    data = load_grid(path)

    meta = data.get("meta", {})
    reference = data.get("reference", {})
    grid = data.get("grid", [])

    encoding_id = (
        meta.get("encoding_id")
        or path.stem.replace("_grid", "")
    )

    metrics = {
        "encoding_id": encoding_id,
        "source_file": str(path),
        "n_points": len(grid),

        "reference_verdict": reference.get("verdict"),
        "reference_giant_ratio": reference.get("giantRatio"),
        "reference_kappa_conn": reference.get("kappaConn"),
        "reference_tail_dominance": reference.get("tailDominance"),
        "reference_n_iso": reference.get("nIso"),
        "reference_n": reference.get("n"),

        "full_region_volume": compute_full_region_volume(grid),
        "collapse_onset_radius": compute_collapse_onset_radius(grid),
        "kappa_conn_variance": compute_kappa_variance(grid),
        "giant_ratio_variance": compute_gr_variance(grid),
        "admissibility_persistence": compute_admissibility_persistence(grid),
        "fragmentation_rate": compute_fragmentation_rate(grid),
        "mean_tail_dominance": compute_mean_tail_dominance(grid),
        "mean_n_iso": compute_mean_n_iso(grid),
        "bifurcation_sharpness": compute_bifurcation_sharpness(grid),
    }

    return metrics


def write_json(results):
    with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


def write_csv(results):
    if not results:
        return

    fieldnames = list(results[0].keys())

    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for row in results:
            writer.writerow(row)


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

def main():
    print("\n====================================")
    print("EXTRACT RIGIDITY METRICS")
    print("====================================\n")

    grid_files = sorted(INPUT_DIR.glob("*_grid.json"))

    if not grid_files:
        raise FileNotFoundError(
            f"No *_grid.json files found in {INPUT_DIR}"
        )

    results = []

    for path in grid_files:

        print(f"Processing: {path}")

        metrics = summarize_grid(path)

        results.append(metrics)

        print(
            f"  encoding={metrics['encoding_id']} | "
            f"FULL volume={metrics['full_region_volume']:.4f} | "
            f"collapse radius={metrics['collapse_onset_radius']} | "
            f"κ var={metrics['kappa_conn_variance']:.6f} | "
            f"GR var={metrics['giant_ratio_variance']:.6f} | "
            f"bifurcation={metrics['bifurcation_sharpness']:.6f}"
        )

    write_json(results)
    write_csv(results)

    print("\nExports written:")
    print(JSON_OUTPUT)
    print(CSV_OUTPUT)

    print("\nDone.")


if __name__ == "__main__":
    main()