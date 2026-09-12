"""Turbulence fragmentation scaffold."""

from __future__ import annotations

import pandas as pd


def compute_turbulence_fragmentation(df: pd.DataFrame, turbulence_col: str = "turbulence_level") -> pd.Series:
    """Return turbulence/route-fragmentation proxy."""
    if turbulence_col not in df.columns:
        return pd.Series([None] * len(df), index=df.index)
    return pd.to_numeric(df[turbulence_col], errors="coerce")
