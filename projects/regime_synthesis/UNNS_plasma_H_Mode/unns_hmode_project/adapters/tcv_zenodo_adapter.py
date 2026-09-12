"""
TCV Zenodo 14996664 adapter for the UNNS-H Mode project.

Purpose
-------
Read the event-level `lhdatabase.h5` file from the public TCV L-H transition
Zenodo dataset and export two derived tables:

1. a raw flat CSV with all HDF5 top-level datasets as columns;
2. a first canonical transition-event CSV for UNNS-H Mode analysis.

Rule
----
This adapter does not edit raw files. Keep downloaded `.h5` files in
`data/raw/tcv_zenodo_14996664/` and write all derived files to
`data/processed/` and `outputs/reports/`.

Notes
-----
Some semantic mappings must be confirmed against the dataset README/notebook.
Until then, fields such as TIME, THL, ILH, PLH, PLMW, and PTOTMW_A are treated
as candidate event/threshold variables.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import h5py
import numpy as np
import pandas as pd


SOURCE_NAME = "TCV L-H transition database — Zenodo 14996664"
DEVICE = "TCV"


def _to_1d(array: np.ndarray) -> np.ndarray:
    """Convert an HDF5 dataset array to a 1D numpy array."""
    arr = np.asarray(array).squeeze()
    if arr.ndim == 0:
        return np.asarray([arr.item()])
    if arr.ndim != 1:
        raise ValueError(f"Expected scalar/vector dataset after squeeze; got shape {arr.shape}")
    return arr


def load_lhdatabase_h5(path: str | Path) -> pd.DataFrame:
    """Load flat top-level datasets from `lhdatabase.h5` into a DataFrame."""
    path = Path(path)
    data: dict[str, np.ndarray] = {}
    with h5py.File(path, "r") as h5:
        for key in h5.keys():
            if not isinstance(h5[key], h5py.Dataset):
                continue
            data[key] = _to_1d(h5[key][()])

    lengths = {k: len(v) for k, v in data.items()}
    unique_lengths = sorted(set(lengths.values()))
    if len(unique_lengths) != 1:
        raise ValueError(f"Datasets have inconsistent lengths: {lengths}")

    return pd.DataFrame(data)


def make_canonical_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a first canonical transition-event table.

    This is deliberately conservative: all source columns are retained with a
    `src_` prefix where useful, while the minimum schema fields are made explicit.
    """
    out = pd.DataFrame()
    out["device"] = DEVICE
    out["dataset"] = SOURCE_NAME
    out["shot_id"] = df.get("SHOT")
    out["event_time"] = df.get("TIME")
    out["event_type"] = np.where(df.get("ILH", pd.Series(np.nan, index=df.index)) == 1, "LH", "UNKNOWN")
    out["confidence"] = np.where(df.get("COND", pd.Series(np.nan, index=df.index)) == 1, 1.0, np.nan)
    out["source"] = "lhdatabase.h5"
    out["notes"] = "Initial adapter mapping; confirm TIME/THL/ILH semantics against README/notebook."

    # Physics / threshold candidate fields.
    mappings = {
        "src_TIME": "TIME",
        "src_THL": "THL",
        "src_ILH": "ILH",
        "src_COND": "COND",
        "P_LH_candidate_MW": "PLH",
        "P_loss_candidate_MW": "PLMW",
        "P_total_candidate_MW": "PTOTMW",
        "P_total_aux_candidate_MW": "PTOTMW_A",
        "P_NBI_W": "PNBI",
        "P_ECH_W": "PECH",
        "P_ohmic_W": "POHMSMOOTH",
        "P_rad_W": "PRAD",
        "P_rad_core_W": "PRADCORE",
        "dWmhd_dt_candidate_MW": "DWMHDMW",
        "Wmhd_J": "WMHD",
        "n_e_m3": "NEL",
        "n_e_1e20_m3": "NEL20",
        "I_p_MA": "IP",
        "B_t_T": "BT",
        "q95": "Q95",
        "kappa": "KAPPA",
        "delta": "DELTA",
        "aspect_or_species_A": "A",
        "minor_radius_m": "AMIN",
        "R_geo_m": "RGEO",
        "volume_m3": "VOL",
        "hydrogen_fraction_candidate": "cH",
        "helium_fraction_candidate": "cHe",
        "Z_eff": "ZEFF",
        "n_Ryter": "nRyter",
        "P_Ryter": "PRyter",
        "chi_eff_candidate": "CHIEFF",
        "divertor_signal_candidate": "PDIV",
        "divertor_signal_150_candidate": "PDIV150",
    }
    for canonical, source_col in mappings.items():
        out[canonical] = df[source_col] if source_col in df.columns else np.nan

    return out


def build_column_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create a compact per-column summary."""
    rows: list[dict[str, Any]] = []
    for col in df.columns:
        s = df[col]
        row: dict[str, Any] = {
            "column": col,
            "dtype": str(s.dtype),
            "count": int(s.count()),
            "missing": int(s.isna().sum()),
            "unique": int(s.nunique(dropna=True)),
        }
        if pd.api.types.is_numeric_dtype(s):
            row.update({
                "min": float(np.nanmin(s)) if s.count() else None,
                "max": float(np.nanmax(s)) if s.count() else None,
                "mean": float(np.nanmean(s)) if s.count() else None,
            })
        rows.append(row)
    return pd.DataFrame(rows)


def inspect_lh_data_h5(path: str | Path) -> dict[str, Any]:
    """Return a shallow structural summary of `LH_DATA.h5`."""
    path = Path(path)
    summary: dict[str, Any] = {"file": str(path), "groups": {}}
    with h5py.File(path, "r") as h5:
        for group_name in ["data/fig1", "data/fig2", "data/fig5", "data/fig6", "data/fig8"]:
            if group_name not in h5:
                continue
            group = h5[group_name]
            entries = []
            for key in group.keys():
                obj = group[key]
                if isinstance(obj, h5py.Dataset):
                    entries.append({"name": key, "type": "dataset", "shape": list(obj.shape), "dtype": str(obj.dtype)})
                else:
                    entries.append({"name": key, "type": "group", "children": len(obj.keys())})
            summary["groups"][group_name] = entries
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest TCV Zenodo L-H transition HDF5 files for UNNS-H Mode.")
    parser.add_argument("--raw-dir", default="data/raw/tcv_zenodo_14996664", help="Directory containing lhdatabase.h5 and LH_DATA.h5")
    parser.add_argument("--processed-dir", default="data/processed", help="Output directory for derived CSV files")
    parser.add_argument("--reports-dir", default="outputs/reports", help="Output directory for JSON/summary reports")
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    processed_dir = Path(args.processed_dir)
    reports_dir = Path(args.reports_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    lhdatabase_path = raw_dir / "lhdatabase.h5"
    lh_data_path = raw_dir / "LH_DATA.h5"

    df = load_lhdatabase_h5(lhdatabase_path)
    canonical = make_canonical_events(df)
    col_summary = build_column_summary(df)

    raw_flat_csv = processed_dir / "tcv_lh_events_raw_flat.csv"
    canonical_csv = processed_dir / "tcv_lh_events_canonical.csv"
    columns_csv = reports_dir / "tcv_lh_columns_summary.csv"
    inspection_json = reports_dir / "tcv_lh_h5_inspection_summary.json"

    df.to_csv(raw_flat_csv, index=False)
    canonical.to_csv(canonical_csv, index=False)
    col_summary.to_csv(columns_csv, index=False)

    summary = {
        "source": SOURCE_NAME,
        "lhdatabase_h5": {
            "rows": int(len(df)),
            "column_count": int(len(df.columns)),
            "unique_shots": int(df["SHOT"].nunique()) if "SHOT" in df else None,
            "shot_min": float(df["SHOT"].min()) if "SHOT" in df else None,
            "shot_max": float(df["SHOT"].max()) if "SHOT" in df else None,
            "ilh_counts": {str(k): int(v) for k, v in df["ILH"].value_counts(dropna=False).items()} if "ILH" in df else {},
            "cond_counts": {str(k): int(v) for k, v in df["COND"].value_counts(dropna=False).items()} if "COND" in df else {},
            "years": sorted([int(x) for x in df["SHOTYEAR"].dropna().unique()]) if "SHOTYEAR" in df else [],
            "columns": list(df.columns),
            "outputs": {
                "raw_flat_csv": str(raw_flat_csv),
                "canonical_csv": str(canonical_csv),
                "columns_csv": str(columns_csv),
            },
        },
    }
    if lh_data_path.exists():
        summary["LH_DATA_h5"] = inspect_lh_data_h5(lh_data_path)

    inspection_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["lhdatabase_h5"], indent=2))


if __name__ == "__main__":
    main()
