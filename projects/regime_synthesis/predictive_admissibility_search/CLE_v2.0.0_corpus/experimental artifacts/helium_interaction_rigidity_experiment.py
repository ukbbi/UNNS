import json
import math
from pathlib import Path

import pandas as pd

from cle.pipeline import CLEPipeline


# ===================================================
# HELIUM INTERACTION RIGIDITY EXPERIMENT
# ===================================================
#
# PURPOSE
# -------
# Dedicated CLT rigidity experiment for:
#
#   - Zeeman
#   - Zeeman singlet
#   - Zeeman triplet
#   - Δ-Zeeman singlet
#   - Δ-Zeeman triplet
#
# This is intentionally SEPARATE from:
#
#   helium_rigidity_generator.py
#
# to preserve:
#
#   - experiment provenance,
#   - reproducibility,
#   - interpretational clarity,
#   - CLT protocol separation.
#
#
# OUTPUT
# ------
#
# CLE_PILOT_I/helium/rigidity_interaction/
#
#   zeeman_grid.json
#   zeeman_singlet_grid.json
#   zeeman_triplet_grid.json
#   delta_zeeman_singlet_grid.json
#   delta_zeeman_triplet_grid.json
#
#
# RUN
# ---
#
# python helium_interaction_rigidity_experiment.py
#
# ===================================================


# ---------------------------------------------------
# INPUTS
# ---------------------------------------------------

INPUTS = {

    "zeeman":
        "CLE_PILOT_I/helium/zeeman/helium_zeeman_ladder.csv",

    "zeeman_singlet":
        "CLE_PILOT_I/helium/zeeman/helium_singlet_zeeman_ladder.csv",

    "zeeman_triplet":
        "CLE_PILOT_I/helium/zeeman/helium_triplet_zeeman_ladder.csv",

    "delta_zeeman_singlet":
        "CLE_PILOT_I/helium/delta/delta_zeeman_singlet.csv",

    "delta_zeeman_triplet":
        "CLE_PILOT_I/helium/delta/delta_zeeman_triplet.csv",
}


# ---------------------------------------------------
# OUTPUT
# ---------------------------------------------------

OUTPUT_DIR = Path(
    "CLE_PILOT_I/helium/rigidity_interaction"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------
# GRID CONFIG
# ---------------------------------------------------

ALPHA_MIN = 0.80
ALPHA_MAX = 1.20

MU_MIN = 0.80
MU_MAX = 1.20

STEP = 0.05


# ---------------------------------------------------
# GLOBAL CLE PIPELINE
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
            f"No numeric columns in {path}"
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

    deformed = []

    for x in values:

        if x >= 0:
            y = mu_scale * (x ** alpha_scale)

        else:
            y = -mu_scale * ((abs(x)) ** alpha_scale)

        if math.isfinite(y):
            deformed.append(y)

    return deformed


def analyze(values, domain="atomic"):

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

    reference = analyze(values)

    grid = []

    total = len(alpha_values) * len(mu_values)

    counter = 0

    for alpha in alpha_values:

        for mu in mu_values:

            counter += 1

            print(
                f"[{counter}/{total}] "
                f"{encoding_id} "
                f"alpha={alpha:.2f} "
                f"mu={mu:.2f}"
            )

            deformed = deform_ladder(
                values,
                alpha,
                mu
            )

            result = analyze(deformed)

            grid.append({

                "alpha": alpha,
                "mu": mu,

                "verdict":
                    result["verdict"],

                "giantRatio":
                    result["giantRatio"],

                "kappaConn":
                    result["kappaConn"],

                "kappaStar":
                    result["kappaStar"],

                "tailDominance":
                    result["tailDominance"],

                "nIso":
                    result["nIso"],

                "n":
                    result["n"],
            })

    return {

        "meta": {

            "experiment":
                "helium_interaction_rigidity",

            "encoding_id":
                encoding_id,

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

            "verdict":
                reference["verdict"],

            "giantRatio":
                reference["giantRatio"],

            "kappaConn":
                reference["kappaConn"],

            "kappaStar":
                reference["kappaStar"],

            "tailDominance":
                reference["tailDominance"],

            "nIso":
                reference["nIso"],

            "n":
                reference["n"],
        },

        "grid": grid,
    }


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

def main():

    print("\n====================================")
    print("HELIUM INTERACTION RIGIDITY TEST")
    print("====================================\n")

    for encoding_id, source_path in INPUTS.items():

        print(f"\nLoading: {encoding_id}")
        print(f"Source : {source_path}")

        values = read_first_numeric_column(
            source_path
        )

        print(f"Values : {len(values)}")
        print("Generating grid...\n")

        result = build_grid(
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
                result,
                f,
                indent=2
            )

        print(f"\nSaved: {output_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()