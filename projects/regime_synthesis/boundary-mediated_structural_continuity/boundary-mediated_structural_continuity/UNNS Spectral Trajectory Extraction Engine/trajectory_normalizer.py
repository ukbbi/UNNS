import os
import glob
import statistics

# ============================================================
# UNNS Trajectory Normalizer
# ============================================================

INPUT_DIR = "ladders"
OUTPUT_DIR = "normalized_ladders"

MIN_POINTS = 5

# jump threshold multiplier
JUMP_SIGMA = 6.0

# ============================================================
# Helpers
# ============================================================

def parse_ladder(path):

    points = []

    with open(path, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) < 3:
                continue

            try:
                idx = int(parts[0])
                coord = float(parts[1])
                spectral = float(parts[2])

                points.append((coord, spectral))

            except:
                continue

    return points


def deduplicate(points):

    merged = {}

    for coord, spectral in points:

        if coord not in merged:
            merged[coord] = []

        merged[coord].append(spectral)

    out = []

    for coord in sorted(merged.keys()):

        avg = sum(merged[coord]) / len(merged[coord])

        out.append((coord, avg))

    return out


def remove_outliers(points):

    if len(points) < 5:
        return points

    spectral_values = [p[1] for p in points]

    median = statistics.median(spectral_values)

    absdev = [abs(x - median) for x in spectral_values]

    mad = statistics.median(absdev)

    if mad == 0:
        return points

    cleaned = []

    for coord, spectral in points:

        z = abs(spectral - median) / mad

        if z < JUMP_SIGMA:
            cleaned.append((coord, spectral))

    return cleaned


def smooth(points):

    if len(points) < 3:
        return points

    smoothed = []

    for i in range(len(points)):

        coord = points[i][0]

        neighbors = []

        for j in range(max(0, i - 1), min(len(points), i + 2)):
            neighbors.append(points[j][1])

        avg = sum(neighbors) / len(neighbors)

        smoothed.append((coord, avg))

    return smoothed


def normalize(points):

    coords = [p[0] for p in points]
    vals = [p[1] for p in points]

    cmin = min(coords)
    cmax = max(coords)

    vmin = min(vals)
    vmax = max(vals)

    out = []

    for coord, spectral in points:

        if cmax != cmin:
            c = (coord - cmin) / (cmax - cmin)
        else:
            c = 0.0

        if vmax != vmin:
            s = (spectral - vmin) / (vmax - vmin)
        else:
            s = 0.0

        out.append((c, s))

    return out


def write_ladder(path, points):

    with open(path, "w", encoding="utf-8") as f:

        f.write("# UNNS Normalized Spectral Ladder\n")
        f.write("\n")
        f.write("# index coord spectral\n")

        for i, (coord, spectral) in enumerate(points):

            f.write(
                f"{i} "
                f"{coord:.12f} "
                f"{spectral:.12f}\n"
            )


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 50)
    print("UNNS Trajectory Normalizer")
    print("=" * 50)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = glob.glob(os.path.join(INPUT_DIR, "*.txt"))

    print(f"[OK] Input ladders: {len(files)}")

    emitted = 0

    for path in files:

        name = os.path.basename(path)

        print(f"\n[PROCESS] {name}")

        points = parse_ladder(path)

        if len(points) < MIN_POINTS:
            print("[SKIP] Too few points")
            continue

        print(f"[OK] Raw points: {len(points)}")

        # ----------------------------------------------------
        # deduplicate
        # ----------------------------------------------------

        points = deduplicate(points)

        print(f"[OK] After deduplication: {len(points)}")

        # ----------------------------------------------------
        # remove outliers
        # ----------------------------------------------------

        before = len(points)

        points = remove_outliers(points)

        removed = before - len(points)

        print(f"[OK] Outliers removed: {removed}")

        # ----------------------------------------------------
        # smoothing
        # ----------------------------------------------------

        points = smooth(points)

        print("[OK] Smoothed")

        # ----------------------------------------------------
        # normalization
        # ----------------------------------------------------

        points = normalize(points)

        print("[OK] Normalized to [0,1]")

        # ----------------------------------------------------
        # final validation
        # ----------------------------------------------------

        if len(points) < MIN_POINTS:
            print("[SKIP] Too few points after cleaning")
            continue

        outpath = os.path.join(OUTPUT_DIR, name)

        write_ladder(outpath, points)

        emitted += 1

        print(f"[WRITE] {outpath}")

    print("\n" + "=" * 50)
    print(f"[DONE] Normalized ladders emitted: {emitted}")
    print("=" * 50)


# ============================================================
# Entry
# ============================================================

if __name__ == "__main__":
    main()