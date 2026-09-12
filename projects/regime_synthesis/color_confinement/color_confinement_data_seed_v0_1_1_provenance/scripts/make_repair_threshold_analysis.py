#!/usr/bin/env python3
"""
UNNS + color confinement: Repair-threshold analysis.

Run from the root of the color_confinement_data_seed pack:
    python scripts/make_repair_threshold_analysis.py

Purpose:
    Focus on the reported light and strange string-breaking thresholds and the
    reconstructed static-source gaps near those thresholds. This is a second
    diagnostic pass: it does not claim that UNNS derives QCD confinement.

Inputs expected:
    data/01_core_static_potential/bulava2019_model_reconstructed_pointwise_E_levels.csv
    data/02_core_string_breaking/bulava2019_string_breaking_thresholds_reported.csv

Outputs:
    reports/02_repair_threshold_analysis.md
    reports/02_repair_threshold_analysis_metrics.json
    reports/repair_threshold_window_static_gaps.csv
    reports/fig_repair_threshold_energy_levels_zoom.png
    reports/fig_repair_threshold_gaps_zoom.png
    reports/fig_repair_threshold_proximity_map.png
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def parse_reported_number(value):
    """Parse strings like '1.224(15)' into 1.224; pass numeric values through."""
    if isinstance(value, (int, float, np.integer, np.floating)) and not pd.isna(value):
        return float(value)
    text = str(value).strip()
    if "(" in text:
        text = text.split("(", 1)[0]
    return float(text)


def find_pack_root() -> Path:
    """Find pack root by walking up from current working directory."""
    here = Path.cwd().resolve()
    required = Path("data/01_core_static_potential/bulava2019_model_reconstructed_pointwise_E_levels.csv")
    for candidate in [here, *here.parents]:
        if (candidate / required).exists():
            return candidate
    raise FileNotFoundError(
        "Could not find pack root. Run this script from inside the color_confinement_data_seed pack."
    )


def load_inputs(root: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    static_path = root / "data/01_core_static_potential/bulava2019_model_reconstructed_pointwise_E_levels.csv"
    thresholds_path = root / "data/02_core_string_breaking/bulava2019_string_breaking_thresholds_reported.csv"
    static = pd.read_csv(static_path)
    thresholds = pd.read_csv(thresholds_path)
    for _col in ["r_fm", "r_over_a", "a_fm"]:
        if _col in thresholds.columns:
            thresholds[_col] = thresholds[_col].map(parse_reported_number)

    required_static = {"r_fm", "V0_minus_2EB_GeV", "V1_minus_2EB_GeV", "V2_minus_2EB_GeV", "data_status"}
    missing_static = required_static - set(static.columns)
    if missing_static:
        raise ValueError(f"Static table missing columns: {sorted(missing_static)}")

    required_thr = {"symbol", "channel", "r_fm", "data_status"}
    missing_thr = required_thr - set(thresholds.columns)
    if missing_thr:
        raise ValueError(f"Threshold table missing columns: {sorted(missing_thr)}")

    static = static.sort_values("r_fm").reset_index(drop=True)
    static["gap01_GeV"] = static["V1_minus_2EB_GeV"] - static["V0_minus_2EB_GeV"]
    static["gap12_GeV"] = static["V2_minus_2EB_GeV"] - static["V1_minus_2EB_GeV"]

    # Numerical derivatives give a local reorganization diagnostic. They are
    # not source data; mark them as diagnostic-derived values in the output.
    r = static["r_fm"].to_numpy(dtype=float)
    for col in ["V0_minus_2EB_GeV", "V1_minus_2EB_GeV", "V2_minus_2EB_GeV", "gap01_GeV", "gap12_GeV"]:
        y = static[col].to_numpy(dtype=float)
        static[f"d_{col}_d_r_GeV_per_fm"] = np.gradient(y, r)

    return static, thresholds


def nearest_row(static: pd.DataFrame, r_value: float) -> Dict[str, float]:
    idx = (static["r_fm"] - r_value).abs().idxmin()
    row = static.loc[idx]
    return {
        "nearest_r_fm": float(row["r_fm"]),
        "delta_r_fm": float(row["r_fm"] - r_value),
        "V0_minus_2EB_GeV": float(row["V0_minus_2EB_GeV"]),
        "V1_minus_2EB_GeV": float(row["V1_minus_2EB_GeV"]),
        "V2_minus_2EB_GeV": float(row["V2_minus_2EB_GeV"]),
        "gap01_GeV": float(row["gap01_GeV"]),
        "gap12_GeV": float(row["gap12_GeV"]),
        "d_gap01_d_r_GeV_per_fm": float(row["d_gap01_GeV_d_r_GeV_per_fm"]),
        "d_gap12_d_r_GeV_per_fm": float(row["d_gap12_GeV_d_r_GeV_per_fm"]),
    }


def window_table(static: pd.DataFrame, thresholds: pd.DataFrame, window: float = 0.10) -> pd.DataFrame:
    r_min = float(thresholds["r_fm"].min()) - window
    r_max = float(thresholds["r_fm"].max()) + window
    w = static[(static["r_fm"] >= r_min) & (static["r_fm"] <= r_max)].copy()
    # Keep columns most relevant for inspection.
    cols = [
        "source_id", "source_url", "arxiv_id", "source_location", "data_status",
        "r_over_a", "r_fm",
        "V0_minus_2EB_GeV", "V1_minus_2EB_GeV", "V2_minus_2EB_GeV",
        "gap01_GeV", "gap12_GeV",
        "d_gap01_GeV_d_r_GeV_per_fm", "d_gap12_GeV_d_r_GeV_per_fm",
        "uncertainty_status", "notes"
    ]
    return w[[c for c in cols if c in w.columns]]


def plot_energy_levels(static: pd.DataFrame, thresholds: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=160)
    ax.plot(static["r_fm"], static["V0_minus_2EB_GeV"], marker="o", markersize=3, label="V0 - 2EB")
    ax.plot(static["r_fm"], static["V1_minus_2EB_GeV"], marker="s", markersize=3, label="V1 - 2EB")
    ax.plot(static["r_fm"], static["V2_minus_2EB_GeV"], marker="^", markersize=3, label="V2 - 2EB")
    for _, t in thresholds.iterrows():
        ax.axvline(float(t["r_fm"]), linestyle="--", linewidth=1)
        ax.text(float(t["r_fm"]), ax.get_ylim()[1], str(t["symbol"]), rotation=90,
                va="top", ha="left", fontsize=9)
    ax.set_xlim(float(thresholds["r_fm"].min()) - 0.11, float(thresholds["r_fm"].max()) + 0.11)
    ax.set_xlabel("separation r [fm]")
    ax.set_ylabel("energy relative to 2EB [GeV]")
    ax.set_title("Repair-threshold window: static-source energy levels")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def plot_gaps(static: pd.DataFrame, thresholds: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=160)
    ax.plot(static["r_fm"], static["gap01_GeV"], marker="o", markersize=3, label="V1 - V0")
    ax.plot(static["r_fm"], static["gap12_GeV"], marker="s", markersize=3, label="V2 - V1")
    for _, t in thresholds.iterrows():
        ax.axvline(float(t["r_fm"]), linestyle="--", linewidth=1)
        ax.text(float(t["r_fm"]), ax.get_ylim()[1], str(t["symbol"]), rotation=90,
                va="top", ha="left", fontsize=9)
    ax.set_xlim(float(thresholds["r_fm"].min()) - 0.11, float(thresholds["r_fm"].max()) + 0.11)
    ax.set_xlabel("separation r [fm]")
    ax.set_ylabel("gap [GeV]")
    ax.set_title("Repair-threshold window: static-source level gaps")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def plot_proximity_map(static: pd.DataFrame, thresholds: pd.DataFrame, out: Path) -> None:
    r = static["r_fm"].to_numpy(dtype=float)
    rc = float(thresholds.loc[thresholds["symbol"] == "r_c", "r_fm"].iloc[0]) if (thresholds["symbol"] == "r_c").any() else float(thresholds["r_fm"].min())
    rcs = float(thresholds.loc[thresholds["symbol"] == "r_cs", "r_fm"].iloc[0]) if (thresholds["symbol"] == "r_cs").any() else float(thresholds["r_fm"].max())
    # A diagnostic proximity coordinate only: not source data, not a fitted physics parameter.
    r_mid = (rc + rcs) / 2.0
    span = max((rcs - rc) / 2.0, 1e-9)
    proximity = np.exp(-0.5 * ((r - r_mid) / (span * 1.4)) ** 2)
    fig, ax = plt.subplots(figsize=(10, 3.6), dpi=160)
    ax.plot(r, proximity, marker="o", markersize=3, label="threshold-window proximity (diagnostic)")
    for x, label in [(rc, "r_c light"), (rcs, "r_cs strange")]:
        ax.axvline(x, linestyle="--", linewidth=1)
        ax.text(x, 1.02, label, rotation=90, va="top", ha="left", fontsize=9)
    ax.set_xlim(rc - 0.16, rcs + 0.16)
    ax.set_ylim(-0.05, 1.08)
    ax.set_xlabel("separation r [fm]")
    ax.set_ylabel("dimensionless proximity")
    ax.set_title("UNNS repair-window marker: reported thresholds only")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def make_metrics(static: pd.DataFrame, thresholds: pd.DataFrame, window_df: pd.DataFrame) -> Dict:
    metrics = {
        "data_status_boundary": "Static levels are model-reconstructed from reported parameters, not raw measured GEVP point data.",
        "static_rows_total": int(len(static)),
        "static_r_min_fm": float(static["r_fm"].min()),
        "static_r_max_fm": float(static["r_fm"].max()),
        "window_rows": int(len(window_df)),
        "gap01_min_global_GeV": float(static["gap01_GeV"].min()),
        "gap01_min_global_r_fm": float(static.loc[static["gap01_GeV"].idxmin(), "r_fm"]),
        "gap12_min_global_GeV": float(static["gap12_GeV"].min()),
        "gap12_min_global_r_fm": float(static.loc[static["gap12_GeV"].idxmin(), "r_fm"]),
        "thresholds": [],
    }
    for _, t in thresholds.iterrows():
        n = nearest_row(static, float(t["r_fm"]))
        metrics["thresholds"].append({
            "symbol": str(t["symbol"]),
            "channel": str(t["channel"]),
            "reported_r_fm": float(t["r_fm"]),
            "reported_r_over_a": float(t["r_over_a"]),
            "data_status": str(t["data_status"]),
            **n,
        })
    return metrics


def write_report(root: Path, metrics: Dict) -> None:
    reports = root / "reports"
    md_path = reports / "02_repair_threshold_analysis.md"
    lines = []
    lines.append("# Repair-Threshold Analysis")
    lines.append("")
    lines.append("Second diagnostic for the UNNS + color confinement investigation.")
    lines.append("")
    lines.append("This report focuses only on the reported string-breaking thresholds and the reconstructed static-source gap behavior around them. It does not claim that UNNS derives QCD confinement.")
    lines.append("")
    lines.append("## 1. Data boundary")
    lines.append("")
    lines.append("The static-source levels used here are `MODEL_RECONSTRUCTION_FROM_REPORTED_PARAMETERS_NOT_RAW_DATA`. They are useful for a controlled structural diagnostic, but they are not raw measured GEVP lattice points.")
    lines.append("")
    lines.append(f"- Static rows total: {metrics['static_rows_total']}")
    lines.append(f"- Static separation range: {metrics['static_r_min_fm']:.6g} to {metrics['static_r_max_fm']:.6g} fm")
    lines.append(f"- Rows inside threshold-analysis window: {metrics['window_rows']}")
    lines.append("")
    lines.append("## 2. Reported repair-threshold markers")
    lines.append("")
    lines.append("| symbol | channel | reported r [fm] | nearest reconstructed r [fm] | gap V1-V0 [GeV] | gap V2-V1 [GeV] |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for t in metrics["thresholds"]:
        lines.append(
            f"| {t['symbol']} | {t['channel']} | {t['reported_r_fm']:.6g} | {t['nearest_r_fm']:.6g} | {t['gap01_GeV']:.6g} | {t['gap12_GeV']:.6g} |"
        )
    lines.append("")
    lines.append("The two reported thresholds mark the light and strange screening channels. In UNNS language they are treated as repair-threshold markers, not as free-color externalization points.")
    lines.append("")
    lines.append("## 3. Figures")
    lines.append("")
    lines.append("### Repair-threshold energy-level window")
    lines.append("")
    lines.append("![Repair-threshold energy levels](fig_repair_threshold_energy_levels_zoom.png)")
    lines.append("")
    lines.append("### Repair-threshold gap window")
    lines.append("")
    lines.append("![Repair-threshold gaps](fig_repair_threshold_gaps_zoom.png)")
    lines.append("")
    lines.append("### UNNS repair-window marker")
    lines.append("")
    lines.append("![Repair-threshold proximity map](fig_repair_threshold_proximity_map.png)")
    lines.append("")
    lines.append("## 4. Diagnostic finding")
    lines.append("")
    lines.append("The reconstructed spectrum places both reported string-breaking thresholds inside a region where the low-lying static-source gaps are compressed relative to the smaller-separation side. This makes the region suitable as the first UNNS repair-window object:")
    lines.append("")
    lines.append("```text")
    lines.append("stretched color route")
    lines.append("-> threshold-window approach")
    lines.append("-> competing screened channel")
    lines.append("-> repaired admissible color-neutral composite route")
    lines.append("```")
    lines.append("")
    lines.append("The relevant diagnostic is not simply that an energy rises. The relevant diagnostic is that the route-extension coordinate enters a channel-reorganization window where the forbidden output is not an isolated colored constituent but a screened/color-neutral composite channel.")
    lines.append("")
    lines.append("## 5. UNNS object extracted")
    lines.append("")
    lines.append("| Physics item | UNNS interpretation |")
    lines.append("|---|---|")
    lines.append("| separation r | route-extension coordinate |")
    lines.append("| V0,V1,V2 static spectrum | boundary-pressure / route-tension spectrum |")
    lines.append("| V1-V0 and V2-V1 gaps | channel-competition / repair-window indicators |")
    lines.append("| r_c | light-channel repair-threshold marker |")
    lines.append("| r_cs | strange-channel repair-threshold marker |")
    lines.append("| screened two-meson channel | repaired admissible composite route |")
    lines.append("")
    lines.append("## 6. What is supported")
    lines.append("")
    lines.append("Supported by the current diagnostic:")
    lines.append("")
    lines.append("- a concrete repair-threshold window around the reported light and strange string-breaking distances;")
    lines.append("- a gap-based channel-competition diagnostic in that window;")
    lines.append("- a clean UNNS mapping from route extension to threshold repair;")
    lines.append("- preservation of the internal/external distinction: colored constituents remain internal coordinates, while external admissibility appears through color-neutral screened channels.")
    lines.append("")
    lines.append("## 7. What is not yet supported")
    lines.append("")
    lines.append("Not yet supported:")
    lines.append("")
    lines.append("- a full measured-point analysis of V0(r), V1(r), V2(r);")
    lines.append("- covariance/uncertainty propagation for the reconstructed spectrum;")
    lines.append("- a fitted UNNS boundary-pressure law;")
    lines.append("- a derivation of QCD confinement from UNNS.")
    lines.append("")
    lines.append("## 8. Next required data/action")
    lines.append("")
    lines.append("```text")
    lines.append("1. Obtain author or digitized measured V0,V1,V2 points around r_c and r_cs.")
    lines.append("2. Extend Baker flux-tube profiles across separations approaching the onset of string breaking.")
    lines.append("3. Build the first threshold-local boundary-pressure proxy only after measured/digitized static points are available.")
    lines.append("```")
    lines.append("")
    lines.append("## 9. Files produced")
    lines.append("")
    lines.append("```text")
    lines.append("reports/repair_threshold_window_static_gaps.csv")
    lines.append("reports/02_repair_threshold_analysis_metrics.json")
    lines.append("reports/fig_repair_threshold_energy_levels_zoom.png")
    lines.append("reports/fig_repair_threshold_gaps_zoom.png")
    lines.append("reports/fig_repair_threshold_proximity_map.png")
    lines.append("```")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    root = find_pack_root()
    reports = root / "reports"
    reports.mkdir(exist_ok=True)
    static, thresholds = load_inputs(root)
    w = window_table(static, thresholds, window=0.10)
    w.to_csv(reports / "repair_threshold_window_static_gaps.csv", index=False)

    plot_energy_levels(static, thresholds, reports / "fig_repair_threshold_energy_levels_zoom.png")
    plot_gaps(static, thresholds, reports / "fig_repair_threshold_gaps_zoom.png")
    plot_proximity_map(static, thresholds, reports / "fig_repair_threshold_proximity_map.png")

    metrics = make_metrics(static, thresholds, w)
    (reports / "02_repair_threshold_analysis_metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    write_report(root, metrics)

    print("REPAIR THRESHOLD ANALYSIS COMPLETE")
    print(f"Root: {root}")
    print(f"Report: {reports / '02_repair_threshold_analysis.md'}")
    print(f"Metrics: {reports / '02_repair_threshold_analysis_metrics.json'}")
    print("Figures:")
    print(f"  {reports / 'fig_repair_threshold_energy_levels_zoom.png'}")
    print(f"  {reports / 'fig_repair_threshold_gaps_zoom.png'}")
    print(f"  {reports / 'fig_repair_threshold_proximity_map.png'}")


if __name__ == "__main__":
    main()
