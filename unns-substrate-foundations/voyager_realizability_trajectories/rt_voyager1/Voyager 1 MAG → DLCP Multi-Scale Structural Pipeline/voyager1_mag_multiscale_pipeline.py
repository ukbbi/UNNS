#!/usr/bin/env python3

"""
Voyager 1 MAG (48s) → DLCP Multi-Scale Window Robustness Test

Controlled parameter sweep: WINDOW_SIZE ∈ {512, 1024, 2048}
Everything except window size and step size is held constant.

Purpose: verify that t* = 2012 (structural boundary estimator,
         identified as the κ_conn minimum) is not an artifact of
         the 1024-sample baseline window.

Output structure:
    outputs_multi_scale/
        W512_S128/
            run_config.txt          ← audit record
            <ladder files>.txt      ← flat, STRUC-PERC-I–ready
        W1024_S256/
            run_config.txt
            <ladder files>.txt
        W2048_S512/
            run_config.txt
            <ladder files>.txt

Invariant across all three runs:
  ✔ B_COMPONENTS = ["B1", "B2", "B3"]
  ✔ MIN_VALID_RATIO = 0.95
  ✔ Physical range filter: 0 < |B| < 10 nT
  ✔ Zero-plateau rejection
  ✔ Extreme-value rejection (> 100 nT warning; > 10 nT filtered)
  ✔ sort+unique+finite adapter
  ✔ Flat .txt output (no subdirectory per window)

Usage:
    Place .cdf files in the same directory as this script (or set CDF_DIR).
    Run: python3 voyager1_mag_multiscale_pipeline.py
"""

import os
import re
import time
import numpy as np
import cdflib

# ── Multi-scale sweep config ──────────────────────────────────────────────────
WINDOW_CONFIGS = [
    (512,  128),   # half-baseline: ~6.8 h per window at 48 s cadence
    (1024, 256),   # baseline (existing analysis)
    (2048, 512),   # double-baseline: ~27.3 h per window
]

# Output root — all three runs land here as subdirectories
SCRIPT_DIR      = os.path.dirname(os.path.abspath(__file__))
BASE_OUTPUT_DIR = os.path.join(SCRIPT_DIR, "outputs_multi_scale")

# ── Invariant parameters (DO NOT modify between scales) ──────────────────────
B_COMPONENTS    = ["B1", "B2", "B3"]   # RTN or spacecraft-frame components
MIN_VALID_RATIO = 0.95                  # ≥ 95% clean samples required per window
B_MAX_NT        = 10.0                  # physical upper bound (nT)
B_MIN_NT        = 0.0                   # zero-plateau rejection threshold


# ═══════════════════════════════════════════════════════════════════════════════
# UTILS  (identical to baseline pipeline — no changes)
# ═══════════════════════════════════════════════════════════════════════════════

def safe_base_name(path: str) -> str:
    """Sanitise a CDF path to a filesystem-safe identifier."""
    base = os.path.basename(path)
    base = re.sub(r"\.cdf$", "", base, flags=re.IGNORECASE)
    base = re.sub(r"[^A-Za-z0-9_\-]+", "_", base)
    return base


def get_fill_values(cdf, var: str) -> list:
    """Extract FILLVAL and any *FILL* attribute from CDF variable metadata."""
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


def clean(arr: np.ndarray, fill_vals: list) -> np.ndarray:
    """
    Clean raw |B| array for DLCP ladder construction.
    Identical filter chain across all window scales:
      1. float64 + flatten
      2. Remove non-finite (NaN, ±Inf)
      3. Remove declared fill values
      4. Reject zero plateau (B_MIN_NT = 0)
      5. Reject extreme overflow artifacts (B_MAX_NT = 10 nT)
    """
    arr  = np.array(arr, dtype=np.float64).flatten()
    mask = np.isfinite(arr)

    for fv in fill_vals:
        try:
            mask &= arr != float(fv)
        except Exception:
            pass

    mask &= arr > B_MIN_NT   # zero-plateau rejection
    mask &= arr < B_MAX_NT   # overflow/artifact rejection

    return arr[mask]


def build_ladder(segment: np.ndarray) -> np.ndarray:
    """DLCP ladder: strictly ascending sort. Not a time series."""
    return np.sort(segment)


def write_ladder(output_dir: str, filename: str, ladder: np.ndarray) -> str:
    """Write a STRUC-PERC-I–compatible .txt ladder (one value per line)."""
    full_path = os.path.join(output_dir, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        for val in ladder:
            f.write(f"{val:.12g}\n")
    return full_path


def write_run_config(output_dir: str, window_size: int, step_size: int,
                     cdf_files: list, n_ladders: int, elapsed_s: float) -> None:
    """Write an audit-proof run configuration record."""
    config_path = os.path.join(output_dir, "run_config.txt")
    with open(config_path, "w", encoding="utf-8") as f:
        f.write("# DLCP Multi-Scale Robustness Test — Run Configuration\n")
        f.write("# This file is auto-generated. Do not edit.\n\n")
        f.write(f"WINDOW_SIZE     = {window_size}\n")
        f.write(f"STEP_SIZE       = {step_size}\n")
        f.write(f"MIN_VALID_RATIO = {MIN_VALID_RATIO}\n")
        f.write(f"B_COMPONENTS    = {B_COMPONENTS}\n")
        f.write(f"B_MIN_NT        = {B_MIN_NT}\n")
        f.write(f"B_MAX_NT        = {B_MAX_NT}\n")
        f.write(f"OUTPUT_DIR      = {output_dir}\n\n")
        f.write(f"CDF_FILES_FOUND = {len(cdf_files)}\n")
        for cf in cdf_files:
            f.write(f"  {cf}\n")
        f.write(f"\nLADDERS_GENERATED = {n_ladders}\n")
        f.write(f"ELAPSED_SECONDS   = {elapsed_s:.1f}\n")
        f.write(f"\n# Invariant note:\n")
        f.write("# All parameters except WINDOW_SIZE and STEP_SIZE are identical\n")
        f.write("# across all scales. This is a controlled robustness test.\n")


# ═══════════════════════════════════════════════════════════════════════════════
# CORE — file loader and window processor
# ═══════════════════════════════════════════════════════════════════════════════

def load_bmag(cdf, path: str):
    """
    Reconstruct |B| = sqrt(B1² + B2² + B3²) from vector components.
    Returns (bmag_array, fill_values) or (None, []) on failure.
    """
    components = {}
    for var in B_COMPONENTS:
        try:
            data = cdf.varget(var)
            components[var] = np.array(data, dtype=np.float64).flatten()
        except Exception as e:
            print(f"  ERROR loading component {var}: {e}")
            return None, []

    lengths = [len(v) for v in components.values()]
    if len(set(lengths)) != 1:
        print(f"  ERROR: component length mismatch — {dict(zip(B_COMPONENTS, lengths))}")
        return None, []

    b1, b2, b3 = (components[v] for v in B_COMPONENTS)
    bmag = np.sqrt(b1**2 + b2**2 + b3**2)
    fills = get_fill_values(cdf, B_COMPONENTS[0])
    return bmag, fills


def process_file(path: str, window_size: int, step_size: int,
                 output_dir: str) -> int:
    """
    Process one CDF file at the given window scale.
    Returns the number of ladders generated.
    """
    print(f"\n  File: {os.path.basename(path)}")

    try:
        cdf = cdflib.CDF(path)
    except Exception as e:
        print(f"    ERROR opening CDF: {e}")
        return 0

    bmag, fills = load_bmag(cdf, path)
    if bmag is None:
        print("    Skipped: could not reconstruct |B|")
        return 0

    # Sanity check (printed once per file, before windowing)
    finite_mask = np.isfinite(bmag) & (bmag > 0)
    if finite_mask.sum() == 0:
        print("    ABORT: all values zero or non-finite. "
              "Check B_COMPONENTS names.")
        return 0

    bmag_valid = bmag[finite_mask]
    print(f"    |B| raw — min:{bmag_valid.min():.4f}  "
          f"max:{bmag_valid.max():.4f}  "
          f"mean:{bmag_valid.mean():.4f}  "
          f"valid:{len(bmag_valid)}/{len(bmag)}")

    if bmag_valid.max() > 100:
        n_ext = (bmag_valid > B_MAX_NT).sum()
        print(f"    WARNING: {n_ext} samples above {B_MAX_NT} nT "
              f"(overflow artifacts — will be filtered)")

    if len(bmag) < window_size:
        print(f"    Skipped: file too short for W={window_size}")
        return 0

    base    = safe_base_name(path)
    win_idx = 0

    for start in range(0, len(bmag) - window_size + 1, step_size):
        end       = start + window_size
        seg       = bmag[start:end]
        seg_clean = clean(seg, fills)

        if len(seg_clean) < window_size * MIN_VALID_RATIO:
            continue   # window fails quality gate

        ladder    = build_ladder(seg_clean)
        filename  = f"v1_{base}_W{window_size}_win_{win_idx:04d}_{start}_{end}_L_B.txt"
        write_ladder(output_dir, filename, ladder)

        win_idx += 1

    print(f"    → {win_idx} ladders  "
          f"(W={window_size}, step={step_size}, "
          f"~{window_size*48/3600:.1f} h/window)")
    return win_idx


# ═══════════════════════════════════════════════════════════════════════════════
# PIPELINE RUNNER — one call per scale
# ═══════════════════════════════════════════════════════════════════════════════

def run_pipeline(window_size: int, step_size: int) -> None:
    """
    Run the full DLCP pipeline for a single (window_size, step_size) pair.
    Output lands in BASE_OUTPUT_DIR/W{window_size}_S{step_size}/.
    """
    output_dir = os.path.join(BASE_OUTPUT_DIR, f"W{window_size}_S{step_size}")
    os.makedirs(output_dir, exist_ok=True)

    # Discover CDF files from current working directory
    cdf_files = sorted(
        f for f in os.listdir(".")
        if f.lower().endswith(".cdf")
    )

    if not cdf_files:
        print(f"  [W={window_size}] No CDF files found — skipping this scale.")
        return

    print(f"\n{'═'*60}")
    print(f"  SCALE: WINDOW_SIZE={window_size}  STEP_SIZE={step_size}")
    print(f"  Window duration: ~{window_size*48/3600:.1f} h at 48 s cadence")
    print(f"  Output: {output_dir}")
    print(f"  CDF files: {len(cdf_files)}")
    print(f"{'═'*60}")

    t0 = time.time()
    total_ladders = 0

    for cdf_file in cdf_files:
        n = process_file(cdf_file, window_size, step_size, output_dir)
        total_ladders += n

    elapsed = time.time() - t0

    write_run_config(output_dir, window_size, step_size,
                     cdf_files, total_ladders, elapsed)

    print(f"\n  SCALE COMPLETE: {total_ladders} ladders in {elapsed:.1f} s")
    print(f"  Config written: {os.path.join(output_dir, 'run_config.txt')}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN — execute the three-scale controlled sweep
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

    # Print the invariant experiment header once
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  DLCP MULTI-SCALE WINDOW ROBUSTNESS TEST                    ║")
    print("║  Voyager 1 MAG 48 s — controlled parameter sweep            ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Scales:  {[f'W{w}_S{s}' for w,s in WINDOW_CONFIGS]}")
    print(f"║  Invariant: B_COMPONENTS={B_COMPONENTS}")
    print(f"║  Invariant: MIN_VALID_RATIO={MIN_VALID_RATIO}")
    print(f"║  Invariant: physical filter 0 < |B| < {B_MAX_NT} nT")
    print(f"║  Output root: {BASE_OUTPUT_DIR}")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("Scientific objective:")
    print("  Verify that t* = 2012 (κ_conn minimum) is not an artifact")
    print("  of the 1024-sample baseline window size.")
    print()

    sweep_t0 = time.time()

    for window_size, step_size in WINDOW_CONFIGS:
        run_pipeline(window_size, step_size)

    sweep_elapsed = time.time() - sweep_t0

    print(f"\n{'═'*60}")
    print(f"  ALL SCALES COMPLETE  ({sweep_elapsed:.1f} s total)")
    print(f"  Output: {BASE_OUTPUT_DIR}/")
    for w, s in WINDOW_CONFIGS:
        print(f"    W{w}_S{s}/")
    print()
    print("  Next step:")
    print("    Run each W*/  batch through STRUC-PERC-I (batch mode).")
    print("    Compute annual mean κ_conn for each scale.")
    print("    Confirm that argmin_t κ_conn(t) = 2012 at all three scales.")
    print("    If t* is stable, the result is window-size–independent.")
    print(f"{'═'*60}")


if __name__ == "__main__":
    main()