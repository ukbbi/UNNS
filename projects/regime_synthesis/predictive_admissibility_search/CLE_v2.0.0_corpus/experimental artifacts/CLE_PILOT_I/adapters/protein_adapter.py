"""
protein_adapter.py
────────────────────────────────────────────────────────────
Canonical adapter for protein MSM / trajectory ladders.

Purpose
-------
Transforms protein-state trajectory outputs into
canonical realizability ladders suitable for:

    STRUC-PERC-I
    CLE v2.0
    Predictive Admissibility Search
    Cross-domain rigidity comparison

Supported Inputs
----------------
protein/

    populations.npy
    tprobs.npy
    protein_ladders/*.csv
    protein_ladders/*.txt

Observed Protein Structure
--------------------------
The protein corpus contains:

    MSM state populations
    transition probabilities
    trajectory ladders
    metastable state dynamics

The adapter converts these into:

    transition-gap ladders
    persistence trajectories
    admissibility structures

Output
------
canonical/protein/
    protein_population_canonical.csv
    protein_transition_canonical.csv
    protein_ladder_*.csv

Canonical Schema
----------------
index,coordinate,gap,normalized_gap,domain,observable,source

Interpretation
--------------
The adapter converts:

    protein folding dynamics
→ metastable transition ladders
→ admissibility trajectories

This places protein dynamics into the same
structural regime space as:

    helium spectra
    Planck cosmology
    neutrino detector traces
    adversarial manifolds

This is NOT a biochemistry-specific parser.

It is a universal structural canonicalization layer.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

PROTEIN_DIR = ROOT / "protein"

OUT_DIR = ROOT / "canonical" / "protein"

OUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# HELPERS
# ============================================================

def clean_name(name: str) -> str:

    name = name.replace(";", "_")
    name = name.replace(":", "_")
    name = name.replace(" ", "_")

    return re.sub(r"[^A-Za-z0-9_\-]", "_", name)


def build_canonical_from_signal(
    signal: np.ndarray,
    source: str,
    observable: str,
) -> pd.DataFrame:
    """
    Convert arbitrary signal trajectory
    into canonical ladder representation.
    """

    signal = np.asarray(signal, dtype=float)

    signal = signal[np.isfinite(signal)]

    if len(signal) < 3:
        raise RuntimeError(
            f"Insufficient usable values in {source}"
        )

    coord = np.arange(len(signal), dtype=float)

    gaps = np.diff(signal)

    max_gap = np.max(np.abs(gaps))

    if max_gap == 0:
        norm = np.zeros_like(gaps)
    else:
        norm = gaps / max_gap

    canonical = pd.DataFrame({
        "index": np.arange(1, len(gaps) + 1),
        "coordinate": coord[:-1],
        "gap": gaps,
        "normalized_gap": norm,
        "domain": "protein",
        "observable": observable,
        "source": source,
    })

    return canonical


def save_canonical(df: pd.DataFrame, name: str) -> None:

    out_path = OUT_DIR / name

    df.to_csv(out_path, index=False)

    print(f"[OK] Saved:")
    print(f"     {out_path}")


# ============================================================
# POPULATIONS
# ============================================================

def process_populations() -> None:

    path = PROTEIN_DIR / "populations.npy"

    if not path.exists():
        print("[WARN] populations.npy missing")
        return

    print(f"\n[INFO] Processing populations.npy")

    arr = np.load(path)

    arr = np.ravel(arr)

    canonical = build_canonical_from_signal(
        signal=arr,
        source="populations",
        observable="protein_population",
    )

    save_canonical(
        canonical,
        "protein_population_canonical.csv",
    )


# ============================================================
# TRANSITION PROBABILITIES
# ============================================================

def process_transition_probabilities() -> None:

    path = PROTEIN_DIR / "tprobs.npy"

    if not path.exists():
        print("[WARN] tprobs.npy missing")
        return

    print(f"\n[INFO] Processing tprobs.npy")

    arr = np.load(path)

    # flatten matrix into transition stream
    arr = np.ravel(arr)

    canonical = build_canonical_from_signal(
        signal=arr,
        source="transition_probabilities",
        observable="protein_transition_probability",
    )

    save_canonical(
        canonical,
        "protein_transition_canonical.csv",
    )


# ============================================================
# LADDER FILES
# ============================================================

def process_ladder_files() -> None:

    ladder_dir = PROTEIN_DIR / "protein_ladders"

    if not ladder_dir.exists():
        print("[WARN] protein_ladders directory missing")
        return

    files = []

    files.extend(sorted(ladder_dir.glob("*.csv")))
    files.extend(sorted(ladder_dir.glob("*.txt")))

    if not files:
        print("[WARN] No ladder files found")
        return

    for path in files:

        try:

            print(f"\n[INFO] Processing: {path.name}")

            # ------------------------------------------------
            # LOAD
            # ------------------------------------------------

            try:
                df = pd.read_csv(path)
            except Exception:
                df = pd.read_csv(
                    path,
                    delim_whitespace=True,
                    header=None,
                )

            numeric = df.select_dtypes(include=[np.number])

            if numeric.empty:
                raise RuntimeError(
                    "No numeric columns detected."
                )

            # highest variance column
            variances = numeric.var(axis=0)

            signal_col = variances.idxmax()

            signal = numeric[signal_col].to_numpy()

            canonical = build_canonical_from_signal(
                signal=signal,
                source=path.stem,
                observable="protein_ladder",
            )

            stem = clean_name(path.stem)

            save_canonical(
                canonical,
                f"{stem}_canonical.csv",
            )

        except Exception as e:

            print(f"[FAIL] {path.name}")
            print(f"       {e}")


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print("================================================")
    print("PROTEIN CANONICALIZATION")
    print("================================================")

    process_populations()

    process_transition_probabilities()

    process_ladder_files()

    print("\n================================================")
    print("PROTEIN CANONICALIZATION COMPLETE")
    print("================================================")
    print(f"Output: {OUT_DIR}")
    print("================================================")


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":
    main()