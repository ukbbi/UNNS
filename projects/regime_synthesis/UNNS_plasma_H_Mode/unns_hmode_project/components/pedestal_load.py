"""Pedestal / edge-gradient load scaffold."""

from __future__ import annotations

import pandas as pd


def compute_pedestal_load(df: pd.DataFrame, gradient_col: str = "edge_gradient") -> pd.Series:
    """Return nonnegative edge-gradient load proxy."""
    if gradient_col not in df.columns:
        return pd.Series([None] * len(df), index=df.index)
    return pd.to_numeric(df[gradient_col], errors="coerce").abs()
