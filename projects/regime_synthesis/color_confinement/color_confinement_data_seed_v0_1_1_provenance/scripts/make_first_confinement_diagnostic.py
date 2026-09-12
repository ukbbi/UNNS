#!/usr/bin/env python3
"""
make_first_confinement_diagnostic.py

First diagnostic script for the UNNS + color confinement data seed.

Run from the pack root, or pass --root explicitly:

    python scripts/make_first_confinement_diagnostic.py
    python scripts/make_first_confinement_diagnostic.py --root "C:/path/to/color_confinement_data_seed_v0_1_1_provenance"

Outputs, by default:

    reports/fig_static_energy_levels.png
    reports/fig_static_energy_gaps.png
    reports/fig_flux_tube_profile.png
    reports/fig_unns_confinement_sequence.png
    reports/01_first_confinement_diagnostic.md
    reports/01_first_confinement_diagnostic_metrics.json

Data-status discipline:
- Static-source V0,V1,V2 values may be model-reconstructed from reported parameters.
- Flux-tube Ex profiles may be author-ancillary pointwise data.
- The report preserves these statuses instead of treating everything as raw lattice data.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd

# Use a non-interactive backend so the script works from PowerShell/CI.
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


@dataclass
class InputPaths:
    static_levels: Path
    string_breaking: Optional[Path]
    flux_profile: Path


def find_project_root(start: Path) -> Path:
    """Find a pack root containing data/. Works when run from root or scripts/."""
    start = start.resolve()
    candidates = [start]
    candidates.extend(start.parents)
    for candidate in candidates[:8]:
        if (candidate / "data").is_dir():
            return candidate
    raise FileNotFoundError(
        "Could not find project root. Run from the pack root or pass --root."
    )


def first_glob(root: Path, patterns: Iterable[str], required: bool = True) -> Optional[Path]:
    for pattern in patterns:
        matches = sorted(root.glob(pattern))
        if matches:
            return matches[0]
    if required:
        raise FileNotFoundError(
            "Missing required file. Tried patterns:\n  " + "\n  ".join(patterns)
        )
    return None


def discover_inputs(root: Path) -> InputPaths:
    static_levels = first_glob(
        root,
        [
            "data/01_core_static_potential/*reconstructed*E_levels*.csv",
            "data/01_core_static_potential/*pointwise*E_levels*.csv",
            "data/01_core_static_potential/*V*levels*.csv",
        ],
    )
    string_breaking = first_glob(
        root,
        [
            "data/02_core_string_breaking/*threshold*.csv",
            "data/02_core_string_breaking/*string_breaking*.csv",
            "*string_breaking_thresholds*.csv",
        ],
        required=False,
    )
    flux_profile = first_glob(
        root,
        [
            "data/03_core_flux_tube_profiles/*pointwise*Ex*FULL*NP*.csv",
            "data/03_core_flux_tube_profiles/*pointwise*flux*.csv",
            "data/03_core_flux_tube_profiles/*Ex*.csv",
        ],
    )
    return InputPaths(static_levels=static_levels, string_breaking=string_breaking, flux_profile=flux_profile)


def require_columns(df: pd.DataFrame, required: Iterable[str], label: str) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{label} is missing required columns: {missing}")


def parse_value_with_parenthetical_error(value) -> tuple[float, Optional[float]]:
    """
    Parse physics notation such as 1.224(15) -> (1.224, 0.015).
    Returns (nan, None) if parsing fails.
    """
    if pd.isna(value):
        return math.nan, None
    text = str(value).strip()
    match = re.fullmatch(r"([+-]?\d+(?:\.\d+)?)(?:\((\d+)\))?", text)
    if not match:
        try:
            return float(text), None
        except ValueError:
            return math.nan, None
    base_text, err_digits = match.groups()
    base = float(base_text)
    if not err_digits:
        return base, None
    decimals = len(base_text.split(".", 1)[1]) if "." in base_text else 0
    err = int(err_digits) * (10 ** (-decimals))
    return base, err


def load_static_levels(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    require_columns(
        df,
        ["r_fm", "V0_minus_2EB_GeV", "V1_minus_2EB_GeV", "V2_minus_2EB_GeV"],
        path.name,
    )
    df = df.copy()
    for col in ["r_fm", "V0_minus_2EB_GeV", "V1_minus_2EB_GeV", "V2_minus_2EB_GeV"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["r_fm", "V0_minus_2EB_GeV", "V1_minus_2EB_GeV", "V2_minus_2EB_GeV"])
    df = df.sort_values("r_fm").reset_index(drop=True)
    df["gap01_GeV"] = df["V1_minus_2EB_GeV"] - df["V0_minus_2EB_GeV"]
    df["gap12_GeV"] = df["V2_minus_2EB_GeV"] - df["V1_minus_2EB_GeV"]
    return df


def load_string_breaking(path: Optional[Path]) -> pd.DataFrame:
    if path is None:
        return pd.DataFrame()
    df = pd.read_csv(path)
    if "r_fm" in df.columns:
        parsed = df["r_fm"].apply(parse_value_with_parenthetical_error)
        df = df.copy()
        df["r_fm_value"] = [v for v, _ in parsed]
        df["r_fm_error"] = [e for _, e in parsed]
    return df


def load_flux_profile(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    require_columns(pathlib_df := df, ["x_t_fm", "Ex_FULL_GeV2", "Ex_NP_GeV2"], path.name)
    df = df.copy()
    for col in ["x_t_fm", "Ex_FULL_GeV2", "Ex_NP_GeV2", "Ex_FULL_error_GeV2", "Ex_NP_error_GeV2"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["x_t_fm", "Ex_FULL_GeV2", "Ex_NP_GeV2"])
    df = df.sort_values("x_t_fm").reset_index(drop=True)
    return df


def nearest_row(df: pd.DataFrame, xcol: str, target: float) -> dict:
    idx = (df[xcol] - target).abs().idxmin()
    return df.loc[idx].to_dict()


def estimate_fwhm_symmetric(df: pd.DataFrame, x_col: str, y_col: str) -> Optional[float]:
    """Estimate FWHM from a roughly symmetric profile by using |x| and interpolation."""
    small = df[[x_col, y_col]].dropna().copy()
    if small.empty:
        return None
    small["abs_x"] = small[x_col].abs()
    # Average +/- points with the same |x| after rounding to stabilize duplicates.
    small["abs_x_round"] = small["abs_x"].round(9)
    radial = small.groupby("abs_x_round", as_index=False)[y_col].mean().rename(columns={"abs_x_round": "abs_x"})
    radial = radial.sort_values("abs_x")
    y_peak = radial[y_col].max()
    if not np.isfinite(y_peak) or y_peak <= 0:
        return None
    half = 0.5 * y_peak
    above = radial[radial[y_col] >= half]
    below = radial[radial[y_col] < half]
    if above.empty or below.empty:
        return None
    last_above = above.iloc[-1]
    candidates = below[below["abs_x"] > last_above["abs_x"]]
    if candidates.empty:
        radius = float(last_above["abs_x"])
    else:
        first_below = candidates.iloc[0]
        x1, y1 = float(last_above["abs_x"]), float(last_above[y_col])
        x2, y2 = float(first_below["abs_x"]), float(first_below[y_col])
        if y2 == y1:
            radius = x1
        else:
            radius = x1 + (half - y1) * (x2 - x1) / (y2 - y1)
    return 2.0 * radius


def plot_static_energy_levels(static_df: pd.DataFrame, thresholds_df: pd.DataFrame, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(static_df["r_fm"], static_df["V0_minus_2EB_GeV"], marker="o", markersize=3, label="V0 - 2EB")
    ax.plot(static_df["r_fm"], static_df["V1_minus_2EB_GeV"], marker="s", markersize=3, label="V1 - 2EB")
    ax.plot(static_df["r_fm"], static_df["V2_minus_2EB_GeV"], marker="^", markersize=3, label="V2 - 2EB")
    add_threshold_lines(ax, thresholds_df)
    ax.set_title("Static Q-Qbar model-reconstructed energy levels")
    ax.set_xlabel("separation r [fm]")
    ax.set_ylabel("energy relative to 2EB [GeV]")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def plot_static_energy_gaps(static_df: pd.DataFrame, thresholds_df: pd.DataFrame, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(static_df["r_fm"], static_df["gap01_GeV"], marker="o", markersize=3, label="V1 - V0")
    ax.plot(static_df["r_fm"], static_df["gap12_GeV"], marker="s", markersize=3, label="V2 - V1")
    add_threshold_lines(ax, thresholds_df)
    ax.set_title("Static-source level gaps")
    ax.set_xlabel("separation r [fm]")
    ax.set_ylabel("gap [GeV]")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def add_threshold_lines(ax, thresholds_df: pd.DataFrame) -> None:
    if thresholds_df.empty or "r_fm_value" not in thresholds_df.columns:
        return
    y_min, y_max = ax.get_ylim()
    for _, row in thresholds_df.dropna(subset=["r_fm_value"]).iterrows():
        r = float(row["r_fm_value"])
        symbol = str(row.get("symbol", "threshold"))
        ax.axvline(r, linestyle="--", linewidth=1)
        ax.text(r, y_max, f" {symbol}", rotation=90, va="top", ha="left", fontsize=8)


def plot_flux_profile(flux_df: pd.DataFrame, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    if "Ex_FULL_error_GeV2" in flux_df.columns:
        ax.errorbar(
            flux_df["x_t_fm"],
            flux_df["Ex_FULL_GeV2"],
            yerr=flux_df["Ex_FULL_error_GeV2"],
            marker="o",
            markersize=3,
            linestyle="-",
            capsize=2,
            label="Ex FULL",
        )
    else:
        ax.plot(flux_df["x_t_fm"], flux_df["Ex_FULL_GeV2"], marker="o", markersize=3, label="Ex FULL")
    if "Ex_NP_error_GeV2" in flux_df.columns:
        ax.errorbar(
            flux_df["x_t_fm"],
            flux_df["Ex_NP_GeV2"],
            yerr=flux_df["Ex_NP_error_GeV2"],
            marker="s",
            markersize=3,
            linestyle="-",
            capsize=2,
            label="Ex nonperturbative",
        )
    else:
        ax.plot(flux_df["x_t_fm"], flux_df["Ex_NP_GeV2"], marker="s", markersize=3, label="Ex nonperturbative")
    ax.set_title("Flux-tube transverse longitudinal chromoelectric profile")
    ax.set_xlabel("transverse distance xt [fm]")
    ax.set_ylabel("Ex [GeV^2]")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def plot_unns_sequence(out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.axis("off")
    labels = [
        "internal colored\nconstituent",
        "attempted\nseparation",
        "localized route\ntension",
        "threshold /\nrepair region",
        "admissible\ncolor-neutral\ncomposite",
    ]
    xs = np.linspace(0.08, 0.92, len(labels))
    y = 0.55
    for i, (x, label) in enumerate(zip(xs, labels)):
        ax.text(
            x,
            y,
            label,
            ha="center",
            va="center",
            fontsize=10,
            bbox={"boxstyle": "round,pad=0.4", "facecolor": "none", "edgecolor": "black"},
            transform=ax.transAxes,
        )
        if i < len(labels) - 1:
            ax.annotate(
                "",
                xy=(xs[i + 1] - 0.075, y),
                xytext=(x + 0.075, y),
                xycoords=ax.transAxes,
                arrowprops={"arrowstyle": "->", "linewidth": 1.2},
            )
    ax.text(
        0.5,
        0.12,
        "UNNS working map: route extension -> boundary pressure -> repair into closed admissible state",
        ha="center",
        va="center",
        fontsize=10,
        transform=ax.transAxes,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def summarize(static_df: pd.DataFrame, thresholds_df: pd.DataFrame, flux_df: pd.DataFrame, inputs: InputPaths) -> dict:
    metrics: dict = {
        "inputs": {
            "static_levels": str(inputs.static_levels),
            "string_breaking": str(inputs.string_breaking) if inputs.string_breaking else None,
            "flux_profile": str(inputs.flux_profile),
        },
        "static_levels": {
            "rows": int(len(static_df)),
            "r_min_fm": float(static_df["r_fm"].min()),
            "r_max_fm": float(static_df["r_fm"].max()),
            "data_status": sorted(static_df.get("data_status", pd.Series(dtype=str)).dropna().astype(str).unique().tolist()),
            "gap01_min_GeV": float(static_df["gap01_GeV"].min()),
            "gap12_min_GeV": float(static_df["gap12_GeV"].min()),
        },
        "thresholds": [],
        "flux_profile": {
            "rows": int(len(flux_df)),
            "x_t_min_fm": float(flux_df["x_t_fm"].min()),
            "x_t_max_fm": float(flux_df["x_t_fm"].max()),
            "source_separation_fm": float(flux_df["source_separation_fm"].dropna().iloc[0]) if "source_separation_fm" in flux_df.columns and not flux_df["source_separation_fm"].dropna().empty else None,
            "data_status": sorted(flux_df.get("data_status", pd.Series(dtype=str)).dropna().astype(str).unique().tolist()),
            "Ex_FULL_peak_GeV2": float(flux_df["Ex_FULL_GeV2"].max()),
            "Ex_NP_peak_GeV2": float(flux_df["Ex_NP_GeV2"].max()),
            "Ex_NP_fwhm_fm_estimate": estimate_fwhm_symmetric(flux_df, "x_t_fm", "Ex_NP_GeV2"),
        },
    }
    if not thresholds_df.empty and "r_fm_value" in thresholds_df.columns:
        for _, row in thresholds_df.iterrows():
            item = {
                "symbol": str(row.get("symbol", "")),
                "channel": str(row.get("channel", "")),
                "r_fm": None if pd.isna(row.get("r_fm_value")) else float(row.get("r_fm_value")),
                "r_fm_error": None if pd.isna(row.get("r_fm_error")) else float(row.get("r_fm_error")),
                "data_status": str(row.get("data_status", "")),
            }
            if item["r_fm"] is not None:
                near = nearest_row(static_df, "r_fm", item["r_fm"])
                item["nearest_static_r_fm"] = float(near["r_fm"])
                item["nearest_gap01_GeV"] = float(near["gap01_GeV"])
                item["nearest_gap12_GeV"] = float(near["gap12_GeV"])
            metrics["thresholds"].append(item)
    return metrics


def write_report(root: Path, reports_dir: Path, metrics: dict) -> Path:
    report_path = reports_dir / "01_first_confinement_diagnostic.md"
    figures = {
        "Static energy levels": "fig_static_energy_levels.png",
        "Static energy gaps": "fig_static_energy_gaps.png",
        "Flux-tube profile": "fig_flux_tube_profile.png",
        "UNNS confinement sequence": "fig_unns_confinement_sequence.png",
    }

    static_status = ", ".join(metrics["static_levels"].get("data_status") or ["not recorded"])
    flux_status = ", ".join(metrics["flux_profile"].get("data_status") or ["not recorded"])

    threshold_lines = []
    for item in metrics.get("thresholds", []):
        err = item.get("r_fm_error")
        err_text = f" +/- {err:.3g} fm" if err is not None else ""
        threshold_lines.append(
            f"- {item.get('symbol')} ({item.get('channel')}): r = {item.get('r_fm'):.6g} fm{err_text}; "
            f"nearest reconstructed r = {item.get('nearest_static_r_fm'):.6g} fm; "
            f"gap01 = {item.get('nearest_gap01_GeV'):.6g} GeV; "
            f"gap12 = {item.get('nearest_gap12_GeV'):.6g} GeV."
        )
    if not threshold_lines:
        threshold_lines = ["- No string-breaking threshold table was found."]

    fwhm = metrics["flux_profile"].get("Ex_NP_fwhm_fm_estimate")
    fwhm_text = "not estimated" if fwhm is None else f"{fwhm:.6g} fm"

    text = f"""# First Confinement Diagnostic

This diagnostic is generated from the current UNNS + color confinement data pack.
It is a first analysis pass, not a claim that UNNS derives QCD confinement.

## 1. Data status

### Static-source energy levels

- Input: `{metrics['inputs']['static_levels']}`
- Rows: {metrics['static_levels']['rows']}
- Separation range: {metrics['static_levels']['r_min_fm']:.6g} to {metrics['static_levels']['r_max_fm']:.6g} fm
- Data status: {static_status}

### String-breaking thresholds

""" + "\n".join(threshold_lines) + f"""

### Flux-tube pointwise profile

- Input: `{metrics['inputs']['flux_profile']}`
- Rows: {metrics['flux_profile']['rows']}
- Transverse range: {metrics['flux_profile']['x_t_min_fm']:.6g} to {metrics['flux_profile']['x_t_max_fm']:.6g} fm
- Source separation: {metrics['flux_profile'].get('source_separation_fm')} fm
- Data status: {flux_status}
- Peak Ex FULL: {metrics['flux_profile']['Ex_FULL_peak_GeV2']:.6g} GeV^2
- Peak Ex NP: {metrics['flux_profile']['Ex_NP_peak_GeV2']:.6g} GeV^2
- Estimated NP FWHM: {fwhm_text}

## 2. Diagnostic figures

"""
    for label, filename in figures.items():
        text += f"### {label}\n\n![{label}]({filename})\n\n"

    text += """## 3. UNNS working map

The current evidence supports the following provisional mapping:

```text
quark separation r
-> route-extension coordinate

static spectrum V0(r), V1(r), V2(r)
-> boundary-pressure / route-tension spectrum

string-breaking threshold
-> repair-threshold marker

two-meson threshold / screened channel
-> repaired admissible composite channel

flux-tube transverse profile Ex(xt)
-> localized route geometry

absence of free color in the ordinary external spectrum
-> non-externalizable internal coordinate
```

## 4. Interpretation

The static-source diagnostic supplies a controlled route-extension axis: increasing separation r probes how the static-source spectrum reorganizes near reported string-breaking thresholds. The flux-tube profile supplies a direct geometry of route localization: the chromoelectric field is concentrated around the line connecting the static sources rather than dispersing freely.

For the UNNS investigation, this supports a structural reading of color confinement as admissibility-by-closure: internal colored constituents are not externally admissible as isolated objects; attempted separation is carried by a tensioned route and repaired into color-neutral composite channels.

## 5. What is not yet proven

- The Bulava V0,V1,V2 table used here is model-reconstructed from reported Hamiltonian parameters, not raw measured GEVP point data.
- Only one Baker flux-tube profile is included in this first pointwise pass.
- This diagnostic does not derive QCD confinement from UNNS.
- This diagnostic does not replace lattice-QCD analysis.

## 6. Next missing data

```text
1. Author or digitized measured V0(r), V1(r), V2(r) points from Bulava figures/tables.
2. All Baker ancillary flux-tube profiles across separations and beta values.
3. A small comparison table linking threshold positions to gap structure and flux-tube width.
4. Only then: a UNNS boundary-pressure proxy fitted across the acquired pointwise data.
```
"""
    report_path.write_text(text, encoding="utf-8")
    return report_path


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Create the first UNNS color-confinement diagnostic plots and report.")
    parser.add_argument("--root", type=Path, default=None, help="Pack root. Defaults to current directory or parent containing data/.")
    parser.add_argument("--reports", type=Path, default=None, help="Reports output directory. Defaults to <root>/reports.")
    args = parser.parse_args(argv)

    root = find_project_root(args.root or Path.cwd())
    reports_dir = (args.reports or (root / "reports")).resolve()
    reports_dir.mkdir(parents=True, exist_ok=True)

    inputs = discover_inputs(root)
    static_df = load_static_levels(inputs.static_levels)
    thresholds_df = load_string_breaking(inputs.string_breaking)
    flux_df = load_flux_profile(inputs.flux_profile)

    plot_static_energy_levels(static_df, thresholds_df, reports_dir / "fig_static_energy_levels.png")
    plot_static_energy_gaps(static_df, thresholds_df, reports_dir / "fig_static_energy_gaps.png")
    plot_flux_profile(flux_df, reports_dir / "fig_flux_tube_profile.png")
    plot_unns_sequence(reports_dir / "fig_unns_confinement_sequence.png")

    metrics = summarize(static_df, thresholds_df, flux_df, inputs)
    metrics_path = reports_dir / "01_first_confinement_diagnostic_metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    report_path = write_report(root, reports_dir, metrics)

    print("FIRST CONFINEMENT DIAGNOSTIC COMPLETE")
    print(f"Root: {root}")
    print(f"Report: {report_path}")
    print(f"Metrics: {metrics_path}")
    print("Figures:")
    for name in [
        "fig_static_energy_levels.png",
        "fig_static_energy_gaps.png",
        "fig_flux_tube_profile.png",
        "fig_unns_confinement_sequence.png",
    ]:
        print(f"  {reports_dir / name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
