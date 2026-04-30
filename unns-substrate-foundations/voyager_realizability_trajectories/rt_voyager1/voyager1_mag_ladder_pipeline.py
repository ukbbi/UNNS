#!/usr/bin/env python3

"""
Voyager 1 MAG (48s) → DLCP Ladder Generator

✔ No directory assumptions
✔ Windows-safe paths
✔ STRUC-PERC-I .txt output
✔ Sliding-window DLCP
✔ Computes |B| from B1/B2/B3 vector components (NOT norm48)
✔ Zero-plateau filter in clean() — critical for MAG fill artifacts
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

# anchor output to script location (NOT working dir)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# ── PATCH: use vector components, not norm48 ──────────────────────────────────
# norm48 in Voyager 1 MAG CDFs is often a flag/placeholder (zeros or scaled
# integers) rather than a valid physical field magnitude.  The correct approach
# is to reconstruct |B| from the three orthogonal components.
#
# Adjust these names if your CDF uses different variable identifiers.
# Common alternatives: "B_RTN" (3-element vector), "BR"/"BT"/"BN",
# "Bx"/"By"/"Bz".  Run `cdf.cdf_info()` to list all variables in your file.
B_COMPONENTS = ["B1", "B2", "B3"]    # RTN or spacecraft-frame components

# =========================
# UTILS
# =========================

def ensure_output_root():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def safe_base_name(path):
    base = os.path.basename(path)
    base = re.sub(r"\.cdf$", "", base, flags=re.IGNORECASE)
    base = re.sub(r"[^A-Za-z0-9_\-]+", "_", base)
    return base


def get_fill_values(cdf, var):
    """Extract FILLVAL and any *FILL* attribute from the variable metadata."""
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


# ── PATCH: zero-plateau filter added ─────────────────────────────────────────
def clean(arr, fill_vals):
    """
    Clean a raw array for DLCP ladder construction:
      1. Cast to float64 and flatten
      2. Remove non-finite values (NaN, ±Inf)
      3. Remove declared fill values (from CDF metadata)
      4. Remove zero-valued samples — Voyager MAG zeros are invalid:
         real |B| in the heliosheath / ISM is always > 0.
         Zero entries are quantisation artifacts, fill encodings, or
         instrument dropouts that escaped the metadata fill declaration.
    """
    arr = np.array(arr, dtype=np.float64).flatten()

    mask = np.isfinite(arr)

    for fv in fill_vals:
        try:
            mask &= arr != float(fv)
        except Exception:
            pass

    # ── PATCH: reject zero plateau ────────────────────────────────────────────
    mask &= arr > 0.0

    # ── PATCH: reject extreme fill/overflow artifacts ─────────────────────────
    # Voyager 1 MAG expected physical range: ~0.01 – 10 nT.
    # Values like 1730 nT are instrument overflow codes or scaling artifacts
    # that survive fill-value removal.  They go to the top of the sorted
    # ladder and catastrophically distort κ and percolation thresholds.
    mask &= arr < 10.0

    return arr[mask]


def build_ladder(segment):
    """DLCP ladder: strictly ordered (ascending sort). Not a time series."""
    return np.sort(segment)


def write_ladder_safe(filename, ladder):
    """
    Write a STRUC-PERC-I–compatible .txt ladder directly into OUTPUT_DIR.
    One floating-point value per line, 12 significant figures.
    """
    full_path = os.path.join(OUTPUT_DIR, filename)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        for val in ladder:
            f.write(f"{val:.12g}\n")

    return full_path


# =========================
# CORE
# =========================

def load_bmag(cdf, path):
    """
    Reconstruct |B| = sqrt(B1² + B2² + B3²) from vector components.

    Returns (Bmag_array, fill_values_from_B1) or (None, []) on failure.
    Fill values are read from B1; the same fill sentinel applies to all
    three components in standard Voyager MAG CDFs.
    """
    components = {}
    for var in B_COMPONENTS:
        try:
            data = cdf.varget(var)
            components[var] = np.array(data, dtype=np.float64).flatten()
        except Exception as e:
            print(f"  ERROR loading component {var}: {e}")
            return None, []

    # All three components must have the same length
    lengths = [len(v) for v in components.values()]
    if len(set(lengths)) != 1:
        print(f"  ERROR: component length mismatch — {dict(zip(B_COMPONENTS, lengths))}")
        return None, []

    b1 = components[B_COMPONENTS[0]]
    b2 = components[B_COMPONENTS[1]]
    b3 = components[B_COMPONENTS[2]]

    # Compute magnitude
    bmag = np.sqrt(b1**2 + b2**2 + b3**2)

    # Collect fill values from B1 (representative)
    fills = get_fill_values(cdf, B_COMPONENTS[0])

    return bmag, fills


def process_file(path):
    print(f"\nProcessing: {path}")

    try:
        cdf = cdflib.CDF(path)
    except Exception as e:
        print(f"  ERROR opening CDF: {e}")
        return

    # ── PATCH: load |B| from vector components ────────────────────────────────
    bmag, fills = load_bmag(cdf, path)
    if bmag is None:
        print("  Skipped: could not reconstruct |B|")
        return

    print(f"  Loaded |B| from {B_COMPONENTS}: {len(bmag)} samples")

    # ── PATCH: sanity check — print before any windowing ─────────────────────
    finite_mask = np.isfinite(bmag) & (bmag > 0)
    if finite_mask.sum() == 0:
        print("  ABORT: all values are zero or non-finite after magnitude "
              "calculation. Check B_COMPONENTS variable names in this CDF.")
        return

    bmag_valid = bmag[finite_mask]
    print(f"  |B| sanity — min: {bmag_valid.min():.4f}  "
          f"max: {bmag_valid.max():.4f}  "
          f"mean: {bmag_valid.mean():.4f}  "
          f"(valid samples: {len(bmag_valid)}/{len(bmag)})")

    # ── PATCH: extreme-value safeguard ────────────────────────────────────────
    if bmag_valid.max() > 100:
        n_extreme = (bmag_valid > 10).sum()
        print(f"  WARNING: extreme values detected before cleaning — "
              f"max={bmag_valid.max():.1f} nT, "
              f"n_above_10={n_extreme} ({100*n_extreme/len(bmag_valid):.1f}%). "
              f"These will be rejected by the physical range filter (< 10 nT).")

    # Values near zero after cleaning indicate the zero-plateau problem.
    # Expected heliosheath / ISM |B|: ~0.05 – 5 nT.
    if bmag_valid.max() < 0.01:
        print("  WARNING: |B| max < 0.01 — field magnitude suspiciously small. "
              "Verify B_COMPONENTS names match your CDF variable inventory.")

    if len(bmag) < WINDOW_SIZE:
        print("  Skipped: too short")
        return

    # ── Sliding-window DLCP ────────────────────────────────────────────────────
    base    = safe_base_name(path)
    win_idx = 0

    for start in range(0, len(bmag) - WINDOW_SIZE + 1, STEP_SIZE):
        end = start + WINDOW_SIZE

        seg       = bmag[start:end]
        seg_clean = clean(seg, fills)

        if len(seg_clean) < WINDOW_SIZE * MIN_VALID_RATIO:
            continue

        ladder = build_ladder(seg_clean)

        # Bundle name includes CDF base for traceability
        bundle_name = f"v1_{base}_win_{win_idx:04d}_{start}_{end}"

        # Flat output — one .txt file per window directly in OUTPUT_DIR.
        # No subdirectory per ladder (previously each window had its own folder).
        filename = f"{bundle_name}_L_B.txt"

        out_path = write_ladder_safe(filename, ladder)
        print(f"  win {win_idx:04d}  [{start}:{end}]  "
              f"n_clean={len(seg_clean)}  "
              f"|B| [{seg_clean.min():.3f}, {seg_clean.max():.3f}]  "
              f"→ {os.path.basename(out_path)}")

        win_idx += 1

    print(f"  Generated {win_idx} windows")


# =========================
# MAIN
# =========================

def main():
    ensure_output_root()

    files = sorted(
        f for f in os.listdir(".")
        if f.lower().endswith(".cdf")
    )

    if not files:
        print("No CDF files found in current directory.")
        print("Tip: run this script from the folder containing your .cdf files,")
        print("     or place the .cdf files alongside the script.")
        return

    print(f"Found {len(files)} CDF file(s)")
    print(f"B_COMPONENTS : {B_COMPONENTS}")
    print(f"WINDOW_SIZE  : {WINDOW_SIZE}")
    print(f"STEP_SIZE    : {STEP_SIZE}")
    print(f"OUTPUT_DIR   : {OUTPUT_DIR}")

    for file in files:
        process_file(file)

    print("\nDONE.")


if __name__ == "__main__":
    main()