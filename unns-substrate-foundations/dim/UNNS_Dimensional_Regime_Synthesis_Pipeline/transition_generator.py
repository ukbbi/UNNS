#!/usr/bin/env python3

import numpy as np
import pandas as pd
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------

B_VALUES = np.linspace(0.0, 1.0, 101)
OUTPUT_DIR = Path("generated_transition_data")
OUTPUT_DIR.mkdir(exist_ok=True)

# -----------------------------
# BASE ENERGY MODELS
# -----------------------------

def hydrogen_like(n_levels=20):
    n = np.arange(1, n_levels + 1)
    return -1.0 / (n ** 2) * 100000  # scaled

def metallic_like(n_levels=20):
    return np.linspace(0, 20000, n_levels)

def irregular_like(n_levels=20):
    base = np.linspace(0, 20000, n_levels)
    noise = np.random.normal(0, 200, size=n_levels)
    return base + noise

# -----------------------------
# ZEEMAN m-values
# -----------------------------

def m_quantum_numbers(n_levels):
    # simple symmetric distribution
    m = np.linspace(-1, 1, n_levels)
    return m

# -----------------------------
# NONLINEAR STRUCTURE
# -----------------------------

def apply_mixing(E, B, strength=0.02):
    E = E.copy()

    for i in range(len(E) - 1):
        delta = E[i+1] - E[i]
        V = strength * B

        shift = np.sqrt(delta**2 + V**2) - abs(delta)

        E[i]   -= shift / 2
        E[i+1] += shift / 2

    return E


def cluster_interaction(E, B):
    E = E.copy()
    n = len(E)

    for i in range(0, n, 3):
        cluster = E[i:i+3]
        if len(cluster) < 3:
            continue

        center = np.mean(cluster)
        spread = (cluster - center) * (1 + B)

        E[i:i+3] = center + spread

    return E


def nonlinear_field(E0, m_vals, B):
    return E0 + m_vals * (B + 0.5 * B**2)

# -----------------------------
# FULL MODEL
# -----------------------------

def generate_levels(E0, m_vals, B):
    E = nonlinear_field(E0, m_vals, B)
    E = apply_mixing(E, B)
    E = cluster_interaction(E, B)
    return np.sort(E)

# -----------------------------
# GENERATION PIPELINE
# -----------------------------

def generate_dataset(name, base_func):
    E0 = base_func()
    m_vals = m_quantum_numbers(len(E0))

    rows = []

    for B in B_VALUES:
        E = generate_levels(E0, m_vals, B)

        for i, e in enumerate(E):
            rows.append({
                "B_T": B,
                "Level0_cm1": E0[i],
                "LevelB_cm1": e
            })

    df = pd.DataFrame(rows)
    out_path = OUTPUT_DIR / f"{name}_zeeman_transition.csv"
    df.to_csv(out_path, index=False)

    print(f"[OK] Generated: {out_path}")


# -----------------------------
# MAIN
# -----------------------------

def main():
    generate_dataset("hydrogen_like", hydrogen_like)
    generate_dataset("metallic_like", metallic_like)
    generate_dataset("irregular_like", irregular_like)


if __name__ == "__main__":
    main()