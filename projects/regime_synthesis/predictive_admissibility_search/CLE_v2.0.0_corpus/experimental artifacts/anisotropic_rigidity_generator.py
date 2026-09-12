#!/usr/bin/env python3
"""
anisotropic_rigidity_generator.py

UNNS Substrate
Rigidity Universality Breaking Experiment

Purpose
-------
This generator intentionally BREAKS the global symmetry preserved by:

- zeeman
- singlet
- triplet
- Δ-singlet
- Δ-triplet

by introducing:

    • anisotropic coupling
    • directional topology
    • local rigidity defects
    • asymmetric transition penalties
    • nonuniform admissibility weighting

This is the first true universality-splitting experiment.

Output
------
Produces:
    anisotropic_<encoding>_grid.json

for every encoding.

Expected Result
---------------
If universality is real:

    small perturbations
    -> preserve topology

while sufficiently strong perturbations:

    -> split rigidity classes
    -> distort κ fields
    -> shift collapse surfaces
    -> generate disconnected admissibility islands
"""

import json
import math
import numpy as np
from pathlib import Path
from collections import defaultdict

# ============================================================
# CONFIG
# ============================================================

N_POINTS = 101

ALPHA_VALUES = np.round(np.arange(0.8, 1.201, 0.05), 2)
MU_VALUES = np.round(np.arange(0.8, 1.201, 0.05), 2)

ENCODINGS = [
    "zeeman",
    "zeeman_singlet",
    "zeeman_triplet",
    "delta_zeeman_singlet",
    "delta_zeeman_triplet"
]

OUTPUT_DIR = Path("anisotropic_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# BASE STATE GENERATOR
# ============================================================

def generate_base_signal(n=101):

    x = np.linspace(-1.0, 1.0, n)

    signal = np.exp(-5 * x**2)

    return signal


# ============================================================
# ANISOTROPIC PERTURBATION FIELD
# ============================================================

def anisotropic_field(x, alpha, mu):

    directional_bias = 1.0 + 0.4 * x

    angular_modulation = (
        1
        + 0.25 * np.sin(8 * np.pi * x * alpha)
        + 0.15 * np.cos(5 * np.pi * x * mu)
    )

    asymmetry = np.where(
        x < 0,
        1.0 - 0.3 * abs(x),
        1.0 + 0.5 * abs(x)
    )

    return directional_bias * angular_modulation * asymmetry


# ============================================================
# LOCAL RIGIDITY DEFECTS
# ============================================================

def inject_defects(signal, x):

    defect_centers = [-0.45, 0.18, 0.63]

    modified = signal.copy()

    for c in defect_centers:

        defect = np.exp(-((x - c) ** 2) / 0.002)

        modified *= (1 - 0.55 * defect)

    return modified


# ============================================================
# NONUNIFORM ADMISSIBILITY WEIGHTING
# ============================================================

def admissibility_weight(x):

    return (
        1.0
        - 0.25 * np.abs(x)
        + 0.12 * np.sin(3 * np.pi * x)
    )


# ============================================================
# STRUCTURAL METRICS
# ============================================================

def compute_metrics(signal):

    threshold = 0.18

    connected = signal > threshold

    giant_ratio = np.sum(connected) / len(signal)

    transitions = np.sum(np.abs(np.diff(connected.astype(int))))

    kappa_conn = transitions / len(signal)

    tail_left = np.mean(signal[:15])
    tail_right = np.mean(signal[-15:])

    tail_dominance = abs(tail_left - tail_right)

    isolated = np.sum(signal < 0.05)

    kappa_star = np.std(signal)

    if giant_ratio > 0.95:
        verdict = "FULL"
    elif giant_ratio > 0.55:
        verdict = "GIANT"
    else:
        verdict = "FRAGMENTED"

    return {
        "verdict": verdict,
        "giantRatio": round(float(giant_ratio), 5),
        "kappaConn": round(float(kappa_conn), 5),
        "kappaStar": round(float(kappa_star), 5),
        "tailDominance": round(float(tail_dominance), 5),
        "nIso": int(isolated),
        "n": len(signal)
    }


# ============================================================
# ENCODING-SPECIFIC DEFORMATION
# ============================================================

def encoding_deformation(signal, encoding, x):

    s = signal.copy()

    if encoding == "zeeman":

        s *= 1 + 0.12 * np.sin(6 * np.pi * x)

    elif encoding == "zeeman_singlet":

        s *= 1 - 0.18 * np.exp(-((x + 0.25) ** 2) / 0.015)

    elif encoding == "zeeman_triplet":

        s *= 1 + 0.22 * np.exp(-((x - 0.4) ** 2) / 0.01)

    elif encoding == "delta_zeeman_singlet":

        s *= 1 + 0.35 * np.sin(10 * np.pi * x) * (x > 0)

    elif encoding == "delta_zeeman_triplet":

        s *= 1 - 0.4 * np.cos(7 * np.pi * x) * (x < 0)

    return s


# ============================================================
# GRID GENERATION
# ============================================================

def run_encoding(encoding):

    print(f"Running {encoding}")

    x = np.linspace(-1.0, 1.0, N_POINTS)

    grid = []

    for alpha in ALPHA_VALUES:

        for mu in MU_VALUES:

            base = generate_base_signal(N_POINTS)

            field = anisotropic_field(x, alpha, mu)

            weighted = base * field

            weighted *= admissibility_weight(x)

            weighted = inject_defects(weighted, x)

            weighted = encoding_deformation(
                weighted,
                encoding,
                x
            )

            # α and μ scaling
            weighted *= (
                np.exp(-abs(alpha - 1.0) * 2.0)
                * np.exp(-abs(mu - 1.0) * 0.8)
            )

            metrics = compute_metrics(weighted)

            grid.append({
                "alpha": float(alpha),
                "mu": float(mu),
                **metrics
            })

    reference = next(
        g for g in grid
        if g["alpha"] == 1.0 and g["mu"] == 1.0
    )

    output = {
        "meta": {
            "experiment": "anisotropic_rigidity_breaking",
            "encoding_id": encoding,
            "alpha_range": [0.8, 1.2],
            "mu_range": [0.8, 1.2],
            "step": 0.05,
            "n_points": len(grid)
        },
        "reference": reference,
        "grid": grid
    }

    outpath = OUTPUT_DIR / f"anisotropic_{encoding}_grid.json"

    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Saved: {outpath}")


# ============================================================
# MAIN
# ============================================================

def main():

    for encoding in ENCODINGS:

        run_encoding(encoding)

    print("\nUniversality-breaking experiment complete.")


if __name__ == "__main__":

    main()