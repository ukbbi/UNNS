#!/usr/bin/env python3

"""
compute_similarity_matrices.py

========================================================
STEP 5 — ADVERSARIAL SIMILARITY / FALSIFICATION ENGINE
========================================================
"""

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


# ======================================================
# PATHS
# ======================================================

ROOT = Path(".")

ADVERSARIAL_FILE = ROOT / "adversarial_STRUC_5D_proxy_vectors.csv"

REAL_FILE = ROOT / "real_STRUC_5D_vectors.csv"

OUTPUT_DIR = ROOT / "similarity_outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ======================================================
# VECTOR SCHEMA
# ======================================================

VECTOR_COLUMNS = [
    "P_depth",
    "sigma2_GR",
    "frag_rate",
    "adm_persist",
    "aniso_persist",
]


# ======================================================
# THRESHOLDS
# ======================================================

FALSIFICATION_THRESHOLD = 0.85

TARGET_REAL_REAL_MIN = 0.88


# ======================================================
# HELPERS
# ======================================================

def load_vectors(path):

    df = pd.read_csv(path)

    missing = [
        c for c in VECTOR_COLUMNS
        if c not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing vector columns in {path}: {missing}"
        )

    return df


def normalize_vectors(df):

    scaler = StandardScaler()

    X = scaler.fit_transform(
        df[VECTOR_COLUMNS].values
    )

    return X


def compute_similarity_matrix(df_a, df_b):

    Xa = normalize_vectors(df_a)
    Xb = normalize_vectors(df_b)

    sim = cosine_similarity(Xa, Xb)

    return sim


def safe_class(row_dict):

    if "class" in row_dict:
        return row_dict["class"]

    if "class_label" in row_dict:
        return row_dict["class_label"]

    return "unknown"


def safe_name(row_dict):

    if "name" in row_dict:
        return row_dict["name"]

    if "filename" in row_dict:
        return row_dict["filename"]

    return "unknown"


def pairwise_table(df_a, df_b, sim_matrix, label):

    rows = []

    for i, a in enumerate(df_a.itertuples(index=False)):

        a_dict = a._asdict()

        for j, b in enumerate(df_b.itertuples(index=False)):

            b_dict = b._asdict()

            rows.append({

                "type": label,

                "A_name":
                    safe_name(a_dict),

                "A_class":
                    safe_class(a_dict),

                "B_name":
                    safe_name(b_dict),

                "B_class":
                    safe_class(b_dict),

                "R_sim":
                    float(sim_matrix[i, j])

            })

    return pd.DataFrame(rows)


def summarize_distribution(values):

    return {

        "median":
            float(np.median(values)),

        "mean":
            float(np.mean(values)),

        "std":
            float(np.std(values)),

        "min":
            float(np.min(values)),

        "max":
            float(np.max(values))
    }


# ======================================================
# LOAD DATA
# ======================================================

print("=" * 60)
print("LOADING VECTORS")
print("=" * 60)

adv_df = load_vectors(ADVERSARIAL_FILE)

real_df = load_vectors(REAL_FILE)

print(f"Adversarial vectors : {len(adv_df)}")
print(f"Real vectors        : {len(real_df)}")


# ======================================================
# ADVERSARIAL vs REAL
# ======================================================

print()
print("=" * 60)
print("ADVERSARIAL vs REAL")
print("=" * 60)

adv_real_sim = compute_similarity_matrix(
    adv_df,
    real_df
)

adv_real_table = pairwise_table(
    adv_df,
    real_df,
    adv_real_sim,
    "adversarial_vs_real"
)

adv_real_path = (
    OUTPUT_DIR /
    "adversarial_vs_real_similarity.csv"
)

adv_real_table.to_csv(
    adv_real_path,
    index=False
)

print(f"Saved: {adv_real_path}")


# ======================================================
# WITHIN RANDOM
# ======================================================

print()
print("=" * 60)
print("WITHIN RANDOM")
print("=" * 60)

within_random_sim = compute_similarity_matrix(
    adv_df,
    adv_df
)

within_random_table = pairwise_table(
    adv_df,
    adv_df,
    within_random_sim,
    "within_random"
)

within_random_path = (
    OUTPUT_DIR /
    "within_random_similarity.csv"
)

within_random_table.to_csv(
    within_random_path,
    index=False
)

print(f"Saved: {within_random_path}")


# ======================================================
# REAL vs REAL
# ======================================================

print()
print("=" * 60)
print("REAL vs REAL")
print("=" * 60)

real_real_sim = compute_similarity_matrix(
    real_df,
    real_df
)

real_real_table = pairwise_table(
    real_df,
    real_df,
    real_real_sim,
    "real_vs_real"
)

real_real_path = (
    OUTPUT_DIR /
    "real_vs_real_similarity.csv"
)

real_real_table.to_csv(
    real_real_path,
    index=False
)

print(f"Saved: {real_real_path}")


# ======================================================
# STATISTICS
# ======================================================

print()
print("=" * 60)
print("STATISTICS")
print("=" * 60)

adv_real_vals = (
    adv_real_table["R_sim"].values
)

within_random_vals = (
    within_random_table["R_sim"].values
)

real_real_vals = (
    real_real_table["R_sim"].values
)

stats_rows = [

    {
        "comparison":
            "adversarial_vs_real",

        **summarize_distribution(
            adv_real_vals
        )
    },

    {
        "comparison":
            "within_random",

        **summarize_distribution(
            within_random_vals
        )
    },

    {
        "comparison":
            "real_vs_real",

        **summarize_distribution(
            real_real_vals
        )
    }
]

stats_df = pd.DataFrame(stats_rows)

stats_path = (
    OUTPUT_DIR /
    "similarity_statistics.csv"
)

stats_df.to_csv(
    stats_path,
    index=False
)

print(f"Saved: {stats_path}")


# ======================================================
# FALSIFICATION ANALYSIS
# ======================================================

print()
print("=" * 60)
print("FALSIFICATION ANALYSIS")
print("=" * 60)

median_adv_real = float(
    np.median(adv_real_vals)
)

median_real_real = float(
    np.median(real_real_vals)
)

max_adv_real = float(
    np.max(adv_real_vals)
)

min_real_real = float(
    np.min(real_real_vals)
)

delta = (
    min_real_real -
    max_adv_real
)

passed = True

reasons = []


if median_adv_real > FALSIFICATION_THRESHOLD:

    passed = False

    reasons.append(
        "Median adversarial-real similarity exceeded threshold."
    )


if delta <= 0:

    passed = False

    reasons.append(
        "No structural separation boundary detected."
    )


if median_real_real < TARGET_REAL_REAL_MIN:

    passed = False

    reasons.append(
        "Real-real similarity unexpectedly weak."
    )


report_lines = []

report_lines.append("=" * 60)
report_lines.append("FALSIFICATION REPORT")
report_lines.append("=" * 60)
report_lines.append("")

report_lines.append(
    f"Median(adversarial ↔ real) : {median_adv_real:.6f}"
)

report_lines.append(
    f"Median(real ↔ real)        : {median_real_real:.6f}"
)

report_lines.append(
    f"Max(adversarial ↔ real)    : {max_adv_real:.6f}"
)

report_lines.append(
    f"Min(real ↔ real)           : {min_real_real:.6f}"
)

report_lines.append(
    f"Separation margin Δ        : {delta:.6f}"
)

report_lines.append("")

if passed:

    report_lines.append(
        "RESULT: H1 survives falsification."
    )

else:

    report_lines.append(
        "RESULT: H1 weakened / falsified."
    )

    report_lines.append("")

    report_lines.append("Reasons:")

    for r in reasons:

        report_lines.append(
            f" - {r}"
        )


report_text = "\n".join(
    report_lines
)

report_path = (
    OUTPUT_DIR /
    "falsification_report.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as f:

    f.write(report_text)


print(report_text)

print()
print(f"Saved: {report_path}")


# ======================================================
# DONE
# ======================================================

print()
print("=" * 60)
print("DONE")
print("=" * 60)

print(
    f"Output directory: {OUTPUT_DIR}"
)