#!/usr/bin/env python3

"""
voyager_ladder_pipeline.py

FULL DLCP IMPLEMENTATION — WINDOWS-SAFE FIXED VERSION

- Batch processes all .cdf files in the same directory
- Extracts V, dens, T, w
- Builds synchronized sliding-window ladders
- Preserves raw-file identity in shortened safe form
- Outputs STRUC-PERC-I-ready .txt ladders
- Writes into output/

Output example:

output/
  voyager_v2_20070827_v01_WIN_0000_0_1024/
      voyager_v2_20070827_v01_WIN_0000_0_1024_L_V.txt
      voyager_v2_20070827_v01_WIN_0000_0_1024_L_dens.txt
      voyager_v2_20070827_v01_WIN_0000_0_1024_L_T.txt
      voyager_v2_20070827_v01_WIN_0000_0_1024_L_w.txt
"""

import os
import re
import numpy as np
import cdflib

# =========================
# CONFIG
# =========================

WINDOW_SIZE = 1024
STEP_SIZE = 256
MIN_VALID_RATIO = 0.95

NORMALIZE = False

OUTPUT_DIR = "output"

VARIABLES = {
    "V": "V",
    "dens": "dens",
    "T": "T",
    "w": "w",
}

# =========================
# UTILS
# =========================

def ensure_output():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def safe_base_name(path):
    """
    Preserve source identity while avoiding overlong Windows paths.
    """
    base = os.path.basename(path)
    base = re.sub(r"\.cdf$", "", base, flags=re.IGNORECASE)

    base = base.replace(
        "voyager2_pls_hires_plasma_data_hsh_",
        "v2_"
    )

    base = re.sub(r"[^A-Za-z0-9_\-]+", "_", base)

    return base


def get_fill_values(cdf, var):
    try:
        attrs = cdf.varattsget(var)
        fill_vals = []

        for k, v in attrs.items():
            if "FILL" in k.upper():
                if isinstance(v, (list, tuple, np.ndarray)):
                    fill_vals.extend(np.array(v).flatten().tolist())
                else:
                    fill_vals.append(v)

        return fill_vals
    except Exception:
        return []


def clean(arr, fill_vals):
    arr = np.array(arr, dtype=np.float64).flatten()

    mask = np.isfinite(arr)

    for fv in fill_vals:
        try:
            mask &= arr != float(fv)
        except Exception:
            pass

    return arr[mask]


def normalize(arr):
    std = np.std(arr)
    if std == 0:
        return arr
    return (arr - np.mean(arr)) / std


def build_ladder(segment):
    if NORMALIZE:
        segment = normalize(segment)
    return np.sort(segment)


def write_ladder(path, ladder):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for val in ladder:
            f.write(f"{val:.12g}\n")


# =========================
# CORE
# =========================

def process_file(path):
    print(f"\nProcessing: {path}")

    try:
        cdf = cdflib.CDF(path)
    except Exception as e:
        print(f"  ERROR: could not open CDF: {e}")
        return

    data = {}
    fills = {}

    for key, var in VARIABLES.items():
        try:
            raw = cdf.varget(var)
            raw = np.array(raw).flatten()

            fills[var] = get_fill_values(cdf, var)
            data[var] = raw

            print(f"  Loaded {var}: {len(raw)}")

        except Exception as e:
            print(f"  Missing variable {var}: {e}")
            return

    min_len = min(len(v) for v in data.values())

    if min_len < WINDOW_SIZE:
        print(f"  Skipped: aligned length {min_len} < WINDOW_SIZE {WINDOW_SIZE}")
        return

    for var in data:
        data[var] = data[var][:min_len]

    print(f"  Aligned length: {min_len}")

    base = safe_base_name(path)
    win_idx = 0

    for start in range(0, min_len - WINDOW_SIZE + 1, STEP_SIZE):
        end = start + WINDOW_SIZE

        window_data = {}
        valid = True

        for key, var in VARIABLES.items():
            seg = data[var][start:end]
            seg_clean = clean(seg, fills[var])

            if len(seg_clean) < WINDOW_SIZE * MIN_VALID_RATIO:
                valid = False
                break

            window_data[key] = seg_clean

        if not valid:
            continue

        bundle_name = f"voyager_{base}_WIN_{win_idx:04d}_{start}_{end}"
        bundle_dir = os.path.join(OUTPUT_DIR, bundle_name)
        os.makedirs(bundle_dir, exist_ok=True)

        for key in VARIABLES:
            ladder = build_ladder(window_data[key])

            out_name = f"{bundle_name}_L_{key}.txt"
            out_path = os.path.join(bundle_dir, out_name)

            write_ladder(out_path, ladder)

        win_idx += 1

    print(f"  Generated {win_idx} windows")


# =========================
# MAIN
# =========================

def main():
    ensure_output()

    files = sorted(
        f for f in os.listdir(".")
        if f.lower().endswith(".cdf")
    )

    if not files:
        print("No CDF files found.")
        return

    print(f"Found {len(files)} files")

    for file in files:
        process_file(file)

    print("\nDONE.")


if __name__ == "__main__":
    main()