import csv
import os
from collections import defaultdict

# ============================================================
# UNNS Spectral Trajectory Extraction Engine
# Revised: Global oxide trajectories
# ============================================================

INPUT_FILE = "spectralparam_full.TXT"
OUTPUT_DIR = "ladders"

# Candidate coordinate columns
COORD_CANDIDATES = [
    "ColorantWtPct",
    "ColorantMW",
    "WtPercent",
    "Concentration",
]

# Spectral value candidates
SPECTRAL_CANDIDATES = [
    "Nd",
    "Density",
    "RI",
    "nD",
]

# ============================================================
# Helpers
# ============================================================

def to_float(x):
    try:
        x = str(x).strip().replace(",", ".")
        return float(x)
    except:
        return None


def detect_separator(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        sample = f.readline()

    if "\t" in sample:
        return "\t"

    if ";" in sample:
        return ";"

    return ","


def sanitize_filename(name):
    invalid = '<>:"/\\|?*'
    for c in invalid:
        name = name.replace(c, "_")
    return name.strip()


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 50)
    print("UNNS Spectral Trajectory Extraction Engine")
    print("=" * 50)

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Missing input file: {INPUT_FILE}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    separator = detect_separator(INPUT_FILE)

    print(f"[OK] Using separator: '{separator}'")

    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:

        reader = csv.DictReader(f, delimiter=separator)

        headers = reader.fieldnames

        if headers is None:
            raise RuntimeError("No headers detected.")

        print(f"[OK] Headers detected: {len(headers)}")

        # ----------------------------------------------------
        # Detect coordinate column
        # ----------------------------------------------------

        coord_col = None

        for c in COORD_CANDIDATES:
            if c in headers:
                coord_col = c
                break

        if coord_col is None:
            raise RuntimeError(
                f"No coordinate column found.\nAvailable headers:\n{headers}"
            )

        print(f"[OK] Coordinate column: {coord_col}")

        # ----------------------------------------------------
        # Detect spectral column
        # ----------------------------------------------------

        spectral_col = None

        for s in SPECTRAL_CANDIDATES:
            if s in headers:
                spectral_col = s
                break

        if spectral_col is None:
            raise RuntimeError(
                f"No spectral column found.\nAvailable headers:\n{headers}"
            )

        print(f"[OK] Spectral column: {spectral_col}")

        # ----------------------------------------------------
        # Detect oxide/material column
        # ----------------------------------------------------

        oxide_col = None

        possible_oxide_cols = [
            "Colorant",
            "Oxide",
            "Material",
            "NAME",
        ]

        for c in possible_oxide_cols:
            if c in headers:
                oxide_col = c
                break

        if oxide_col is None:
            raise RuntimeError(
                f"No oxide/material column found.\nAvailable headers:\n{headers}"
            )

        print(f"[OK] Oxide column: {oxide_col}")

        # ----------------------------------------------------
        # Build global trajectories
        # ----------------------------------------------------

        groups = defaultdict(list)

        row_count = 0

        for row in reader:

            row_count += 1

            oxide = str(row.get(oxide_col, "")).strip()

            coord = to_float(row.get(coord_col))
            spectral = to_float(row.get(spectral_col))

            if not oxide:
                continue

            if coord is None:
                continue

            if spectral is None:
                continue

            groups[oxide].append((coord, spectral))

        print(f"[OK] Rows parsed: {row_count}")
        print(f"[OK] Oxide groups detected: {len(groups)}")

    # ========================================================
    # Emit ladders
    # ========================================================

    emitted = 0

    for oxide, points in groups.items():

        # remove duplicates
        points = list(set(points))

        # sort by coordinate
        points.sort(key=lambda x: x[0])

        # skip trivial ladders
        if len(points) < 5:
            continue

        filename = sanitize_filename(oxide)

        outpath = os.path.join(
            OUTPUT_DIR,
            f"{filename}.txt"
        )

        with open(outpath, "w", encoding="utf-8") as out:

            out.write("# UNNS Spectral Trajectory Ladder\n")
            out.write(f"# Oxide: {oxide}\n")
            out.write("\n")
            out.write("# index wt_pct spectral\n")

            for i, (coord, spectral) in enumerate(points):

                out.write(
                    f"{i} "
                    f"{coord:.12f} "
                    f"{spectral:.12f}\n"
                )

        emitted += 1

        print(
            f"[WRITE] {outpath} "
            f"({len(points)} points)"
        )

    print("=" * 50)
    print(f"[DONE] Ladders emitted: {emitted}")
    print("=" * 50)


# ============================================================
# Entry
# ============================================================

if __name__ == "__main__":
    main()