import json
import math
from pathlib import Path

import pandas as pd

from cle.pipeline import CLEPipeline


# ===================================================
# HELIUM RIGIDITY GENERATOR
# ===================================================
# Purpose:
#   Generate alpha-mu deformation grids for selected
#   helium ladder encodings and export FieldGenerator-
#   compatible JSON files for CLE v1.0.2.
#
# Run from:
#   cle_v1_0_2/
#
# Command:
#   python helium_rigidity_generator.py
# ===================================================


# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

INPUTS = {
    "qmi_spectrum":
        "CLE_PILOT_I/helium/qmi/helium_spectrum_QM1.csv",

    "zeeman":
        "CLE_PILOT_I/helium/zeeman/helium_zeeman_ladder.csv",
}

OUTPUT_DIR = Path("CLE_PILOT_I/helium/rigidity")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ALPHA_MIN = 0.80
ALPHA_MAX = 1.20

MU_MIN = 0.80
MU_MAX = 1.20

# ---------------------------------------------------
# FIRST TEST GRID
# ---------------------------------------------------
# 0.05 => 81 points
# instead of 441
# ---------------------------------------------------

STEP = 0.05


# ---------------------------------------------------
# GLOBAL PIPELINE
# ---------------------------------------------------
# IMPORTANT:
# Avoid rebuilding CLEPipeline
# at every grid point.
# ---------------------------------------------------

pipeline = CLEPipeline()


# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------

def read_first_numeric_column(path):

    df = pd.read_csv(path)

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        raise ValueError(
            f"No numeric columns found in {path}"
        )

    values = (
        numeric.iloc[:, 0]
        .dropna()
        .astype(float)
        .tolist()
    )

    if len(values) < 2:
        raise ValueError(
            f"Need at least 2 numeric values in {path}"
        )

    return values


def frange(start, stop, step):

    values = []

    x = start

    while x <= stop + 1e-12:

        values.append(round(x, 6))

        x += step

    return values


def deform_ladder(values, alpha_scale, mu_scale):

    """
    Conservative CLT deformation model.

    alpha_scale:
        nonlinear spectral deformation

    mu_scale:
        global scaling deformation

    This is NOT a physical Zeeman solver.
    It is a structural admissibility probe.
    """

    deformed = []

    for x in values:

        if x >= 0:
            y = mu_scale * (x ** alpha_scale)

        else:
            y = -mu_scale * ((abs(x)) ** alpha_scale)

        if math.isfinite(y):
            deformed.append(y)

    return deformed


def analyze_ladder(values, domain="atomic"):

    # ------------------------------------------------
    # REUSE GLOBAL PIPELINE
    # ------------------------------------------------

    cst = pipeline.analyze(
        values,
        domain=domain
    )

    return {
        "verdict": cst.verdict,
        "giantRatio": cst.giant_ratio,
        "kappaConn": cst.kappa_conn,
        "kappaStar": cst.kappa_star,
        "tailDominance": cst.tail_dominance,
        "nIso": cst.n_iso,
        "n": cst.n_ladder,
    }


def build_grid(encoding_id, values):

    alpha_values = frange(
        ALPHA_MIN,
        ALPHA_MAX,
        STEP
    )

    mu_values = frange(
        MU_MIN,
        MU_MAX,
        STEP
    )

    reference = analyze_ladder(values)

    grid = []

    total_points = len(alpha_values) * len(mu_values)

    counter = 0

    for alpha in alpha_values:

        for mu in mu_values:

            counter += 1

            print(
                f"  [{counter}/{total_points}] "
                f"alpha={alpha:.2f} "
                f"mu={mu:.2f}"
            )

            deformed = deform_ladder(
                values,
                alpha,
                mu
            )

            result = analyze_ladder(deformed)

            grid.append({
                "alpha": alpha,
                "mu": mu,
                "verdict": result["verdict"],
                "giantRatio": result["giantRatio"],
                "kappaConn": result["kappaConn"],
                "kappaStar": result["kappaStar"],
                "tailDominance": result["tailDominance"],
                "nIso": result["nIso"],
                "n": result["n"],
            })

    return {
        "meta": {
            "instrument":
                "helium_rigidity_generator",

            "encoding_id":
                encoding_id,

            "grid_type":
                "alpha_mu",

            "alpha_range":
                [ALPHA_MIN, ALPHA_MAX],

            "mu_range":
                [MU_MIN, MU_MAX],

            "step":
                STEP,

            "n_points":
                len(grid),
        },

        "reference": {
            "alpha": 1.0,
            "mu": 1.0,
            "verdict": reference["verdict"],
            "giantRatio": reference["giantRatio"],
            "kappaConn": reference["kappaConn"],
            "kappaStar": reference["kappaStar"],
            "tailDominance": reference["tailDominance"],
            "nIso": reference["nIso"],
            "n": reference["n"],
        },

        "grid": grid,
    }


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

def main():

    print("\n====================================")
    print("HELIUM RIGIDITY GENERATOR")
    print("====================================\n")

    for encoding_id, source_path in INPUTS.items():

        print(
            f"\nLoading {encoding_id}: "
            f"{source_path}"
        )

        values = read_first_numeric_column(
            source_path
        )

        print(f"  values: {len(values)}")
        print("  generating alpha-mu grid...\n")

        grid_result = build_grid(
            encoding_id,
            values
        )

        output_path = (
            OUTPUT_DIR /
            f"{encoding_id}_grid.json"
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                grid_result,
                f,
                indent=2
            )

        print(f"\n  saved: {output_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()