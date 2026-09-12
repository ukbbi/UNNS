"""
UNNS edge admissibility margin component.

This is intentionally conservative: it provides a normalized scaffold, not
a final physics claim. Final coefficients must be fitted and stress-tested.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _zsafe(series: pd.Series) -> pd.Series:
    x = pd.to_numeric(series, errors="coerce")
    mu = x.mean(skipna=True)
    sig = x.std(skipna=True)
    if not np.isfinite(sig) or sig == 0:
        return x * 0
    return (x - mu) / sig


def compute_edge_margin(
    df: pd.DataFrame,
    stabilizer_col: str = "ExB_shear",
    coherence_col: str = "H98",
    fragmentation_col: str = "turbulence_level",
    load_col: str = "edge_gradient",
    load_weight: float = 0.5,
) -> pd.Series:
    """
    Compute a first-pass m_edge(t).

    m_edge = z(stabilizer) + z(coherence) - z(fragmentation) - load_weight*z(load)

    Interpretation:
        negative -> leakage / L-like
        near zero -> transition / dithering
        positive -> H-like boundary preservation
    """
    stabilizer = _zsafe(df.get(stabilizer_col, pd.Series(index=df.index, dtype=float)))
    coherence = _zsafe(df.get(coherence_col, pd.Series(index=df.index, dtype=float)))
    fragmentation = _zsafe(df.get(fragmentation_col, pd.Series(index=df.index, dtype=float)))
    load = _zsafe(df.get(load_col, pd.Series(index=df.index, dtype=float)))
    return stabilizer + coherence - fragmentation - load_weight * load
