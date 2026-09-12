"""ELM risk scaffold based on boundary overload."""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_boundary_overload(
    df: pd.DataFrame,
    load_col: str = "pedestal_load",
    margin_col: str = "m_edge",
    eps: float = 1e-9,
) -> pd.Series:
    """
    Boundary overload proxy: positive pedestal load divided by positive margin.

    This is a placeholder. A useful version must be tested against ELM timing.
    """
    load = pd.to_numeric(df.get(load_col, pd.Series(index=df.index, dtype=float)), errors="coerce").abs()
    margin = pd.to_numeric(df.get(margin_col, pd.Series(index=df.index, dtype=float)), errors="coerce")
    denom = np.maximum(eps, margin.clip(lower=0) + eps)
    return load / denom
