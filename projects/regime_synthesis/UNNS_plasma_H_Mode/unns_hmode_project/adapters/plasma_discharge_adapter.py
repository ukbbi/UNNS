"""
Plasma discharge adapter for UNNS-H Mode.

Purpose:
    Convert device-specific plasma data into the canonical UNNS plasma
    time-series schema.

Rule:
    New devices/datasets get adapter methods here or sibling adapter files.
    Do not create one-off generator scripts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any
import pandas as pd


CANONICAL_COLUMNS = [
    "device", "shot_id", "time", "mode_label",
    "P_heat", "P_loss", "n_e", "T_e", "T_e_edge",
    "I_p", "B_t", "R", "a", "kappa", "q95",
    "D_alpha", "W_plasma", "edge_gradient", "turbulence_level",
    "E_radial", "ExB_shear", "tau_E", "H98", "ELM_flag",
]


@dataclass
class PlasmaDischargeAdapter:
    """Minimal adapter scaffold."""

    device: str

    def from_dataframe(
        self,
        df: pd.DataFrame,
        column_map: Mapping[str, str],
        shot_id: str | int,
    ) -> pd.DataFrame:
        """
        Convert an arbitrary dataframe to canonical UNNS plasma columns.

        Parameters
        ----------
        df:
            Source dataframe.
        column_map:
            Mapping from canonical column name -> source dataframe column name.
        shot_id:
            Shot/discharge identifier.
        """
        out = pd.DataFrame()
        out["device"] = self.device
        out["shot_id"] = shot_id

        for canonical in CANONICAL_COLUMNS:
            if canonical in ("device", "shot_id"):
                continue
            src = column_map.get(canonical)
            out[canonical] = df[src] if src in df.columns else None

        if "time" not in out.columns or out["time"].isna().all():
            raise ValueError("Canonical output requires a valid time column.")

        return out[CANONICAL_COLUMNS]

    def validate_minimal(self, df: pd.DataFrame) -> None:
        required = {"device", "shot_id", "time"}
        missing = required.difference(df.columns)
        if missing:
            raise ValueError(f"Missing required canonical columns: {sorted(missing)}")
