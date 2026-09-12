from __future__ import annotations

import io
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd


FIG2D_LEFT = "DTC_Data/fig_2d_left.csv"
FIG2D_RIGHT = "DTC_Data/fig_2d_right.csv"
FIG3A = "DTC_Data/fig_3a.csv"


def _read_csv(zf: zipfile.ZipFile, member: str) -> pd.DataFrame:
    raw = zf.read(member).decode("utf-8-sig")
    return pd.read_csv(io.StringIO(raw))


def _leading_finite_rows(x: np.ndarray) -> np.ndarray:
    finite = np.all(np.isfinite(x), axis=1)
    if finite.all():
        return x
    bad = np.flatnonzero(~finite)
    if len(bad):
        return x[:bad[0]]
    return x


def load_fig2d_state_trajectories(data_zip: str | Path) -> dict[str, np.ndarray]:
    """
    Fig. 2d CSVs are stored as:
        rows    = qubit location (20 qubits)
        columns = Floquet cycle / time sample

    The adapter only transposes this representation to the frozen metric's
    state convention:
        X_t = vector over qubit locations at time t.

    No rescaling, smoothing, sign alignment, or phase labeling enters the
    closure metric.
    """
    with zipfile.ZipFile(data_zip, "r") as zf:
        thermal_qt = _read_csv(zf, FIG2D_LEFT).to_numpy(dtype=float)
        mbl_qt = _read_csv(zf, FIG2D_RIGHT).to_numpy(dtype=float)

    thermal_tq = _leading_finite_rows(thermal_qt.T)
    mbl_tq = _leading_finite_rows(mbl_qt.T)
    return {
        "fig2d_g060": thermal_tq,
        "fig2d_g097": mbl_tq,
    }


def load_fig3a_initial_state_trajectories(data_zip: str | Path) -> dict[str, np.ndarray]:
    """
    Fig. 3a contains three experimental autocorrelator traces for each regime:
    Neel, polarized/ground, and random initial states.

    The three traces are treated as three coordinates of X_t. This tests
    recurrence together with consistency across initial-state classes.
    """
    with zipfile.ZipFile(data_zip, "r") as zf:
        df = _read_csv(zf, FIG3A)

    mbl_cols = ["mbl_neel", "mbl_ground", "mbl_random"]
    pre_cols = ["prethermal_neel", "prethermal_ground", "prethermal_random"]

    return {
        "fig3a_mbl": df[mbl_cols].to_numpy(dtype=float),
        "fig3a_prethermal": df[pre_cols].to_numpy(dtype=float),
    }


def load_fig3a_pairwise_trajectories(data_zip: str | Path) -> dict[str, np.ndarray]:
    """
    Fixed exhaustive pairwise decomposition of the three Fig. 3a initial-state
    channels. All 3 choose 2 pairs are used; none are selected or discarded.
    """
    with zipfile.ZipFile(data_zip, "r") as zf:
        df = _read_csv(zf, FIG3A)

    groups = {
        "mbl": ["mbl_neel", "mbl_ground", "mbl_random"],
        "prethermal": ["prethermal_neel", "prethermal_ground", "prethermal_random"],
    }

    out = {}
    for regime, cols in groups.items():
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                a, b = cols[i], cols[j]
                key = f"fig3a_{regime}__{a.split('_')[-1]}__{b.split('_')[-1]}"
                out[key] = df[[a, b]].to_numpy(dtype=float)
    return out
