#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
protein_msm_ladder_generator.py

UNNS Protein MSM Ladder Generator
=================================

Purpose
-------
Convert a protein Markov State Model into STRUC_PERC_I-ready ladders.

Input files expected in the same folder:

    tprobs.npy
    populations.npy

Source context:
    Folding@home / OSF COVID-19 protein MSM data.

Interpretation
--------------
tprobs.npy:
    transition probability matrix between metastable protein states

populations.npy:
    equilibrium population / basin occupancy of each state

Output:
    protein_ladders/

Generated ladders:
    1. msm_out_strength.txt
       state index -> outgoing transition strength

    2. msm_in_strength.txt
       state index -> incoming transition strength

    3. msm_population.txt
       state index -> basin population

    4. msm_stitching_strength.txt
       state index -> combined local admissibility stitching score

    5. msm_bottleneck_risk.txt
       state index -> local rupture / bottleneck risk proxy

Format:
    One numeric value per line after comments.

Important:
    STRUC_PERC_I batch mode currently extracts all numeric tokens from files.
    Therefore each output file keeps comments minimal and writes a clean
    one-column numeric ladder after the header.
"""

from pathlib import Path
import numpy as np


TPROBS_FILE = "tprobs.npy"
POPS_FILE = "populations.npy"
OUTPUT_DIR = "protein_ladders"

EPS = 1e-15


def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def load_array(path: str) -> np.ndarray:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return np.load(p, allow_pickle=False)


def normalize(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    values = np.nan_to_num(values, nan=0.0, posinf=0.0, neginf=0.0)

    vmin = float(np.min(values))
    vmax = float(np.max(values))

    if vmax - vmin < EPS:
        return np.zeros_like(values, dtype=float)

    return (values - vmin) / (vmax - vmin)


def safe_row_normalize(matrix: np.ndarray) -> np.ndarray:
    m = np.asarray(matrix, dtype=float)
    m = np.nan_to_num(m, nan=0.0, posinf=0.0, neginf=0.0)
    m[m < 0] = 0.0

    row_sums = m.sum(axis=1, keepdims=True)
    return np.divide(m, row_sums, out=np.zeros_like(m), where=row_sums > EPS)


def write_ladder(path: Path, title: str, values: np.ndarray) -> None:
    values = np.asarray(values, dtype=float)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n")
        f.write("# one numeric value per line\n")
        for v in values:
            f.write(f"{float(v):.12f}\n")


def main() -> None:
    print("=" * 60)
    print("UNNS Protein MSM Ladder Generator")
    print("=" * 60)

    ensure_dir(OUTPUT_DIR)

    tprobs = load_array(TPROBS_FILE)
    populations = load_array(POPS_FILE)

    print(f"[OK] Loaded {TPROBS_FILE}: shape={tprobs.shape}")
    print(f"[OK] Loaded {POPS_FILE}: shape={populations.shape}")

    if tprobs.ndim != 2 or tprobs.shape[0] != tprobs.shape[1]:
        raise ValueError("tprobs.npy must be a square transition matrix")

    n = tprobs.shape[0]

    populations = np.asarray(populations, dtype=float).reshape(-1)

    if populations.shape[0] != n:
        raise ValueError(
            f"populations.npy length {populations.shape[0]} does not match "
            f"tprobs matrix size {n}"
        )

    # Clean and normalize transition matrix.
    P = safe_row_normalize(tprobs)

    # Remove self-loops for connectivity/stitching diagnostics.
    Q = P.copy()
    np.fill_diagonal(Q, 0.0)

    # Basic MSM-derived local geometry.
    out_strength = Q.sum(axis=1)
    in_strength = Q.sum(axis=0)

    # Number of nonzero outgoing corridors per state.
    out_degree = (Q > EPS).sum(axis=1).astype(float)
    in_degree = (Q > EPS).sum(axis=0).astype(float)

    # Population basin strength.
    pop = np.nan_to_num(populations, nan=0.0, posinf=0.0, neginf=0.0)
    pop[pop < 0] = 0.0

    # Local stitching proxy:
    # high when a state is both populated and well transition-connected.
    stitching = (
        normalize(out_strength)
        + normalize(in_strength)
        + normalize(out_degree)
        + normalize(in_degree)
        + normalize(pop)
    ) / 5.0

    # Bottleneck risk proxy:
    # high when population exists but transition stitching is weak.
    bottleneck_risk = normalize(pop) * (1.0 - normalize(out_strength + in_strength))

    # Write ladders.
    out = Path(OUTPUT_DIR)

    write_ladder(
        out / "msm_out_strength.txt",
        "MSM outgoing transition strength ladder",
        normalize(out_strength),
    )

    write_ladder(
        out / "msm_in_strength.txt",
        "MSM incoming transition strength ladder",
        normalize(in_strength),
    )

    write_ladder(
        out / "msm_population.txt",
        "MSM basin population ladder",
        normalize(pop),
    )

    write_ladder(
        out / "msm_stitching_strength.txt",
        "MSM local admissibility stitching strength ladder",
        stitching,
    )

    write_ladder(
        out / "msm_bottleneck_risk.txt",
        "MSM local bottleneck / rupture risk ladder",
        bottleneck_risk,
    )

    # Also write a compact report.
    report_path = out / "MSM_LADDER_REPORT.txt"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("UNNS Protein MSM Ladder Report\n")
        f.write("==============================\n\n")
        f.write(f"states: {n}\n")
        f.write(f"matrix_shape: {tprobs.shape}\n")
        f.write(f"population_entries: {len(populations)}\n\n")
        f.write("Generated ladders:\n")
        f.write("  msm_out_strength.txt\n")
        f.write("  msm_in_strength.txt\n")
        f.write("  msm_population.txt\n")
        f.write("  msm_stitching_strength.txt\n")
        f.write("  msm_bottleneck_risk.txt\n\n")
        f.write("Interpretation:\n")
        f.write("  out_strength = outgoing transition continuity\n")
        f.write("  in_strength = incoming transition accessibility\n")
        f.write("  population = basin occupancy / stability\n")
        f.write("  stitching_strength = local admissibility-gluing proxy\n")
        f.write("  bottleneck_risk = populated but weakly stitched states\n")

    print("=" * 60)
    print("[DONE] Protein ladders written")
    print(f"[OUT]  {OUTPUT_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    main()