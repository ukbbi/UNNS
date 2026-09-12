"""Transition detector scaffold."""

from __future__ import annotations

import pandas as pd


def label_transition_windows(df: pd.DataFrame, mode_col: str = "mode_label") -> pd.DataFrame:
    """
    Placeholder for future labeling logic.

    In Phase 1, labels should come from source datasets or manual curation.
    In Phase 2, we can infer candidate LH/HL windows from D_alpha, W_plasma,
    density, and turbulence signals.
    """
    out = df.copy()
    if mode_col not in out.columns:
        out[mode_col] = "unknown"
    return out
