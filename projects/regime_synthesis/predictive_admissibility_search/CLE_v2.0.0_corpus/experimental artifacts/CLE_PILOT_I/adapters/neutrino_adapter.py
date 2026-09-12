"""
neutrino_adapter.py
FULLY FIXED VERSION
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

RAW_DIR = ROOT / "raw" / "neutrino"
OUT_DIR = ROOT / "canonical" / "neutrino"

OUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# HELPERS
# ============================================================

def clean_name(name: str) -> str:

    name = name.replace(";", "_")
    name = name.replace(":", "_")
    name = name.replace(" ", "_")

    return re.sub(r"[^A-Za-z0-9_\-]", "_", name)


# ============================================================
# SIMPLE 1D LADDER EXTRACTION
# ============================================================

def extract_numeric_series(path: Path) -> np.ndarray:
    """
    Extract a 1D floating-point ladder from CERN txt exports.

    The actual neutrino files are NOT tables.
    They are mostly:

        scalar
        scalar
        scalar
        ...

    with occasional metadata/comment rows.

    This extractor robustly pulls all valid floats.
    """

    values = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            # skip comments / ROOT metadata
            if line.startswith("#"):
                continue

            if line.startswith("//"):
                continue

            # split whitespace
            tokens = re.split(r"\s+", line)

            for token in tokens:

                token = token.strip()

                if not token:
                    continue

                try:
                    val = float(token)

                    if np.isfinite(val):
                        values.append(val)

                except Exception:
                    pass

    if len(values) < 3:
        raise RuntimeError(
            f"Could not extract sufficient numeric values from {path.name}"
        )

    return np.asarray(values, dtype=float)


# ============================================================
# CANONICALIZATION
# ============================================================

def canonicalize_trace(path: Path) -> pd.DataFrame:

    print(f"\n[INFO] Processing: {path.name}")

    values = extract_numeric_series(path)

    # --------------------------------------------------------
    # CLEAN
    # --------------------------------------------------------

    values = values[np.isfinite(values)]

    values = np.unique(values)

    values = np.sort(values)

    if len(values) < 3:
        raise RuntimeError(
            f"Insufficient usable ladder points in {path.name}"
        )

    # --------------------------------------------------------
    # GAPS
    # --------------------------------------------------------

    gaps = np.diff(values)

    # remove zero gaps
    gaps = gaps[gaps != 0]

    if len(gaps) == 0:
        raise RuntimeError(
            f"No nonzero gaps extracted from {path.name}"
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
        "coordinate": values[:-1][:len(gaps)],
        "gap": gaps,
        "normalized_gap": norm,
        "domain": "neutrino",
        "observable": "detector_transition",
        "source": path.stem,
    })

    return canonical


# ============================================================
# SAVE
# ============================================================

def save_canonical(df: pd.DataFrame, stem: str) -> None:

    out_path = OUT_DIR / f"{stem}_canonical.csv"

    df.to_csv(out_path, index=False)

    print(f"[OK] Saved:")
    print(f"     {out_path}")


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    files = sorted(RAW_DIR.glob("*.txt"))

    if not files:
        print("[WARN] No neutrino txt files found.")
        return

    processed = 0
    failed = 0

    for path in files:

        try:

            canonical = canonicalize_trace(path)

            stem = clean_name(path.stem)

            save_canonical(canonical, stem)

            processed += 1

        except Exception as e:

            print(f"[FAIL] {path.name}")
            print(f"       {e}")

            failed += 1

    print("\n================================================")
    print("NEUTRINO CANONICALIZATION COMPLETE")
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