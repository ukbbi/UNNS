"""
cosmology_adapter.py
────────────────────────────────────────────────────────────
Canonical adapter for Planck cosmology power-spectrum ladders.

Purpose
-------
Transforms raw Planck angular power-spectrum datasets into
canonical realizability ladders suitable for:

    STRUC-PERC-I
    CLE v2.0
    Predictive Admissibility Search
    Cross-domain rigidity comparison

Supported Inputs
----------------
raw/cosmology/
    planck_TT_full.json
    planck_TE_full.json
    planck_EE_full.json

Observed JSON Structure
-----------------------
{
    "channel": "TT",
    "ell": [...],
    "Dl": [...]
}

Output
------
canonical/cosmology/
    planck_TT_canonical.csv
    planck_TE_canonical.csv
    planck_EE_canonical.csv

Canonical Schema
----------------
index,ell,gap,normalized_gap,domain,observable,source

Interpretation
--------------
The adapter converts:

    cosmological fluctuation spectra
→ spectral transition ladders
→ admissibility trajectories

This places cosmology into the same structural regime space as:

    helium spectra
    neutrino oscillations
    protein folding
    adversarial manifolds

This is a structural canonicalization layer,
NOT merely a parser.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT / "raw" / "cosmology"
OUT_DIR = ROOT / "canonical" / "cosmology"

OUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CORE PROCESSING
# ============================================================

def load_planck_json(path: Path) -> dict:
    """
    Load Planck JSON dataset.
    """

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def canonicalize_planck_spectrum(
    json_path: Path,
    label: str,
) -> pd.DataFrame:
    """
    Convert Planck angular power spectrum
    into canonical ladder representation.
    """

    print(f"\n[INFO] Processing: {json_path.name}")

    data = load_planck_json(json_path)

    if "ell" not in data:
        raise RuntimeError(
            f"'ell' field missing in {json_path.name}"
        )

    if "Dl" not in data:
        raise RuntimeError(
            f"'Dl' field missing in {json_path.name}"
        )

    ell = np.asarray(data["ell"], dtype=float)
    Dl = np.asarray(data["Dl"], dtype=float)

    if len(ell) != len(Dl):
        raise RuntimeError(
            f"Length mismatch in {json_path.name}: "
            f"len(ell)={len(ell)} "
            f"len(Dl)={len(Dl)}"
        )

    # --------------------------------------------------------
    # CLEAN
    # --------------------------------------------------------

    mask = np.isfinite(ell) & np.isfinite(Dl)

    ell = ell[mask]
    Dl = Dl[mask]

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    order = np.argsort(ell)

    ell = ell[order]
    Dl = Dl[order]

    # --------------------------------------------------------
    # GAP EXTRACTION
    # --------------------------------------------------------

    gaps = np.diff(Dl)

    canonical = pd.DataFrame({
        "index": np.arange(1, len(gaps) + 1),
        "ell": ell[:-1],
        "gap": gaps,
    })

    # --------------------------------------------------------
    # NORMALIZATION
    # --------------------------------------------------------

    max_gap = np.max(np.abs(gaps))

    if max_gap == 0:
        canonical["normalized_gap"] = 0.0
    else:
        canonical["normalized_gap"] = gaps / max_gap

    # --------------------------------------------------------
    # METADATA
    # --------------------------------------------------------

    canonical["domain"] = "cosmology"
    canonical["observable"] = "cmb_power_spectrum_transition"
    canonical["source"] = label

    # --------------------------------------------------------
    # COLUMN ORDER
    # --------------------------------------------------------

    canonical = canonical[
        [
            "index",
            "ell",
            "gap",
            "normalized_gap",
            "domain",
            "observable",
            "source",
        ]
    ]

    return canonical


# ============================================================
# SAVE
# ============================================================

def save_canonical(
    df: pd.DataFrame,
    output_name: str,
) -> None:
    """
    Save canonical ladder.
    """

    out_path = OUT_DIR / output_name

    df.to_csv(out_path, index=False)

    print(f"[OK] Saved:")
    print(f"     {out_path}")


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    targets = [
        (
            RAW_DIR / "planck_TT_full.json",
            "planck_TT",
            "planck_TT_canonical.csv",
        ),
        (
            RAW_DIR / "planck_TE_full.json",
            "planck_TE",
            "planck_TE_canonical.csv",
        ),
        (
            RAW_DIR / "planck_EE_full.json",
            "planck_EE",
            "planck_EE_canonical.csv",
        ),
    ]

    for json_path, label, output_name in targets:

        if not json_path.exists():
            print(f"[WARN] Missing file: {json_path.name}")
            continue

        canonical = canonicalize_planck_spectrum(
            json_path=json_path,
            label=label,
        )

        save_canonical(
            canonical,
            output_name,
        )

    print("\n[COMPLETE] Cosmology canonicalization finished.")


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":
    main()