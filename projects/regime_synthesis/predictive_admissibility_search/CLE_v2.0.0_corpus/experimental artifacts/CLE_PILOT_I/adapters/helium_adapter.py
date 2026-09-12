"""
helium_adapter.py
FULLY PATCHED VERSION

Fixes:
- dirty NIST numeric fields
- unicode minus signs
- bracketed uncertainties
- annotated energy values
- duplicate levels
- malformed rows
- sparse coercion collapse

Purpose
-------
Convert helium spectral datasets into canonical
realizability ladders for:

    STRUC-PERC-I
    CLE v2.0
    PAS falsification pipeline
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

RAW_DIR = ROOT / "raw" / "helium"
OUT_DIR = ROOT / "canonical" / "helium"

OUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# HELPERS
# ============================================================

def clean_name(name: str) -> str:

    name = name.replace(";", "_")
    name = name.replace(":", "_")
    name = name.replace(" ", "_")

    return re.sub(r"[^A-Za-z0-9_\-]", "_", name)


def parse_energy(value):
    """
    Robust extraction of numeric energy values
    from messy NIST strings.
    """

    if pd.isna(value):
        return None

    text = str(value)

    # normalize unicode minus
    text = text.replace("−", "-")

    # extract first numeric substring
    match = re.search(
        r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?",
        text
    )

    if not match:
        return None

    try:
        return float(match.group())
    except Exception:
        return None


def detect_energy_column(df: pd.DataFrame) -> str:
    """
    Detect likely energy column automatically.
    """

    candidates = []

    for col in df.columns:

        lower = str(col).lower()

        if (
            "level" in lower
            or "energy" in lower
            or "cm" in lower
        ):
            candidates.append(col)

    if candidates:
        return candidates[0]

    raise RuntimeError(
        f"Could not locate energy column.\n"
        f"Columns found:\n{list(df.columns)}"
    )


# ============================================================
# CORE
# ============================================================

def canonicalize_helium_levels(
    csv_path: Path,
    label: str,
) -> pd.DataFrame:

    print(f"\n[INFO] Processing: {csv_path.name}")

    df = pd.read_csv(csv_path)

    col = detect_energy_column(df)

    print(f"[INFO] Using energy column: {col}")

    # --------------------------------------------------------
    # ROBUST NUMERIC EXTRACTION
    # --------------------------------------------------------

    levels = df[col].apply(parse_energy)

    levels = levels.dropna()

    levels = np.asarray(levels, dtype=float)

    # --------------------------------------------------------
    # CLEAN
    # --------------------------------------------------------

    levels = levels[np.isfinite(levels)]

    levels = np.unique(levels)

    levels = np.sort(levels)

    if len(levels) < 3:
        raise RuntimeError(
            f"Insufficient usable energy levels in {csv_path.name}"
        )

    # --------------------------------------------------------
    # GAPS
    # --------------------------------------------------------

    gaps = np.diff(levels)

    gaps = gaps[gaps != 0]

    if len(gaps) == 0:
        raise RuntimeError(
            f"No nonzero gaps in {csv_path.name}"
        )

    # --------------------------------------------------------
    # NORMALIZATION
    # --------------------------------------------------------

    max_gap = np.max(np.abs(gaps))

    if max_gap == 0:
        norm = np.zeros_like(gaps)
    else:
        norm = gaps / max_gap

    # --------------------------------------------------------
    # BUILD CANONICAL TABLE
    # --------------------------------------------------------

    canonical = pd.DataFrame({
        "index": np.arange(1, len(gaps) + 1),
        "coordinate": levels[:-1][:len(gaps)],
        "gap": gaps,
        "normalized_gap": norm,
        "domain": "helium",
        "observable": label,
        "source": csv_path.stem,
    })

    return canonical


# ============================================================
# SAVE
# ============================================================

def save_canonical(df: pd.DataFrame, stem: str):

    out_path = OUT_DIR / f"{stem}_canonical.csv"

    df.to_csv(out_path, index=False)

    print(f"[OK] Saved:")
    print(f"     {out_path}")


# ============================================================
# MAIN
# ============================================================

def main():

    files = sorted(RAW_DIR.glob("*.csv"))

    if not files:
        print("[WARN] No helium CSV files found.")
        return

    processed = 0
    failed = 0

    for csv_path in files:

        try:

            label = csv_path.stem

            canonical = canonicalize_helium_levels(
                csv_path=csv_path,
                label=label,
            )

            stem = clean_name(csv_path.stem)

            save_canonical(canonical, stem)

            processed += 1

        except Exception as e:

            print(f"[FAIL] {csv_path.name}")
            print(f"       {e}")

            failed += 1

    print("\n================================================")
    print("HELIUM CANONICALIZATION COMPLETE")
    print("================================================")
    print(f"Processed : {processed}")
    print(f"Failed    : {failed}")
    print(f"Output    : {OUT_DIR}")
    print("================================================")


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":
    main()