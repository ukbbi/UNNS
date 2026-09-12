#!/usr/bin/env python3
"""
generate_shuffle_ladder.py

R4 adversarial generator:
Shuffled real-gap ladders.

ALIGNED WITH ACTUAL ARCHIVE STRUCTURE
====================================

Handles the REAL corpus layout:

CLE_PILOT_I/
    helium/
        helium_levels_raw.csv
        helium_II_levels_raw.csv

    neutrino/
        raw/
            *.txt

    cosmology/
        raw/
            *.json

The script recursively scans:
    - helium
    - neutrino/raw
    - cosmology/raw

and automatically extracts numeric ladders.

------------------------------------------------------------
PURPOSE
------------------------------------------------------------

Preserve:
    - exact gap distribution
    - marginal statistics
    - scale structure

Destroy:
    - sequential ordering
    - local continuity
    - admissible organization

This is the MOST IMPORTANT adversarial test.

------------------------------------------------------------
OUTPUT
------------------------------------------------------------

CLE_PILOT_I/adversarial/raw/shuffle/

------------------------------------------------------------
USAGE
------------------------------------------------------------

python generate_shuffle_ladder.py

No arguments required.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path("CLE_PILOT_I")

OUTPUT_DIR = (
    ROOT /
    "adversarial" /
    "raw" /
    "shuffle"
)

COPIES_PER_FILE = 5
MIN_VALUES = 10
MASTER_SEED = 42


# ============================================================
# FILE DISCOVERY
# ============================================================

def collect_files():

    files = []

    # --------------------------------------------------------
    # HELIUM
    # --------------------------------------------------------

    helium_dir = ROOT / "helium"

    if helium_dir.exists():

        files.extend(
            helium_dir.glob("*.csv")
        )

    # --------------------------------------------------------
    # NEUTRINO
    # --------------------------------------------------------

    neutrino_dir = ROOT / "neutrino" / "raw"

    if neutrino_dir.exists():

        files.extend(
            neutrino_dir.glob("*.txt")
        )

    # --------------------------------------------------------
    # COSMOLOGY
    # --------------------------------------------------------

    cosmology_dir = ROOT / "cosmology" / "raw"

    if cosmology_dir.exists():

        files.extend(
            cosmology_dir.glob("*.json")
        )

    return sorted(files)


# ============================================================
# NUMERIC EXTRACTION
# ============================================================

def extract_csv(path):

    df = pd.read_csv(path)

    numeric_cols = [
        c for c in df.columns
        if pd.api.types.is_numeric_dtype(df[c])
    ]

    values = []

    for col in numeric_cols:

        values.extend(
            df[col]
            .dropna()
            .astype(float)
            .tolist()
        )

    return np.array(values, dtype=float)


def extract_txt(path):

    values = []

    with open(
        path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:

        for line in f:

            parts = (
                line.strip()
                .replace(",", " ")
                .split()
            )

            for p in parts:

                try:
                    values.append(float(p))
                except:
                    pass

    return np.array(values, dtype=float)


def extract_json(path):

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    values = []

    def walk(obj):

        if isinstance(obj, dict):

            for v in obj.values():
                walk(v)

        elif isinstance(obj, list):

            for v in obj:
                walk(v)

        else:

            try:
                values.append(float(obj))
            except:
                pass

    walk(data)

    return np.array(values, dtype=float)


def extract_values(path):

    suffix = path.suffix.lower()

    try:

        if suffix == ".csv":
            return extract_csv(path)

        elif suffix == ".txt":
            return extract_txt(path)

        elif suffix == ".json":
            return extract_json(path)

    except Exception as e:

        print(f"[FAILED] {path.name}: {e}")

    return np.array([])


# ============================================================
# CLEANING
# ============================================================

def clean_values(values):

    values = np.asarray(values, dtype=float)

    values = values[np.isfinite(values)]

    if len(values) < MIN_VALUES:
        return np.array([])

    values = np.unique(np.sort(values))

    if len(values) < MIN_VALUES:
        return np.array([])

    return values


# ============================================================
# SHUFFLE
# ============================================================

def shuffle_ladder(values, seed):

    rng = np.random.default_rng(seed)

    gaps = np.diff(values)

    if len(gaps) < 2:
        return np.array([])

    shuffled = np.array(gaps, copy=True)

    rng.shuffle(shuffled)

    shuffled[shuffled <= 1e-12] = 1e-12

    new_values = np.concatenate([
        [0.0],
        np.cumsum(shuffled)
    ])

    return new_values


# ============================================================
# MAIN
# ============================================================

def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    rng = np.random.default_rng(MASTER_SEED)

    manifest = []

    files = collect_files()

    if not files:

        raise RuntimeError(
            "No valid corpus files found."
        )

    print()
    print("========================================")
    print("R4 SHUFFLE GENERATION")
    print("========================================")
    print()

    counter = 0

    for file in files:

        print(f"[PROCESSING] {file}")

        raw_values = extract_values(file)

        if len(raw_values) < MIN_VALUES:

            print(
                f"  -> skipped "
                f"(only {len(raw_values)} values)"
            )

            continue

        values = clean_values(raw_values)

        if len(values) < MIN_VALUES:

            print(
                f"  -> skipped after cleaning "
                f"(only {len(values)} values)"
            )

            continue

        print(
            f"  -> extracted "
            f"{len(values)} values"
        )

        for j in range(COPIES_PER_FILE):

            seed = int(
                rng.integers(
                    0,
                    2**32 - 1
                )
            )

            shuffled_values = shuffle_ladder(
                values,
                seed
            )

            if len(shuffled_values) < MIN_VALUES:
                continue

            name = (
                f"shuffle_{counter:04d}_"
                f"{file.stem}_"
                f"s{j:02d}.csv"
            )

            out_path = OUTPUT_DIR / name

            df = pd.DataFrame({
                "n": np.arange(
                    1,
                    len(shuffled_values) + 1
                ),
                "value": shuffled_values
            })

            df.to_csv(
                out_path,
                index=False
            )

            manifest.append({
                "file": name,
                "source": str(file),
                "length": len(shuffled_values),
                "seed": seed,
                "path": str(out_path)
            })

            counter += 1

    manifest_path = (
        OUTPUT_DIR /
        "shuffle_manifest.csv"
    )

    pd.DataFrame(manifest).to_csv(
        manifest_path,
        index=False
    )

    print()
    print("========================================")
    print("DONE")
    print("========================================")
    print()

    print(f"Generated: {counter}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Manifest: {manifest_path}")
    print()


if __name__ == "__main__":
    main()