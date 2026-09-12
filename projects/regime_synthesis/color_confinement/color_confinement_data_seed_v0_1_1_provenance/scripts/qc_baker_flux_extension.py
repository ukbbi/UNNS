#!/usr/bin/env python3
"""
QC Baker flux-tube separation extension for the UNNS + color confinement project.

Run from the pack root:
    python scripts/qc_baker_flux_extension.py

Inputs searched, in order:
    data/03_core_flux_tube_profiles/baker2024_flux_profile_separation_summary.csv
    reports/03_flux_tube_separation_extension.md
    data/03_core_flux_tube_profiles/baker2024_extended_flux_profiles_long.csv

Outputs:
    reports/04_baker_flux_extension_qc.md
    reports/04_baker_flux_extension_qc_metrics.json
    reports/baker_flux_profile_qc_table.csv
    reports/baker_flux_profile_trusted_summary.csv
    reports/fig_baker_qc_peak_trusted.png
    reports/fig_baker_qc_width_trusted.png
    reports/fig_baker_qc_profiles_trusted_full.png
    reports/fig_baker_qc_profiles_trusted_np.png

This script is intentionally conservative. It does not claim a physical trend unless
profiles pass minimal status, component, and outlier checks.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@dataclass
class Paths:
    root: Path
    reports: Path
    data_flux: Path
    summary_csv: Path
    long_csv: Path
    extension_report: Path


def get_paths(root: Path) -> Paths:
    reports = root / "reports"
    data_flux = root / "data" / "03_core_flux_tube_profiles"
    return Paths(
        root=root,
        reports=reports,
        data_flux=data_flux,
        summary_csv=data_flux / "baker2024_flux_profile_separation_summary.csv",
        long_csv=data_flux / "baker2024_extended_flux_profiles_long.csv",
        extension_report=reports / "03_flux_tube_separation_extension.md",
    )


def _to_float(value) -> float:
    if value is None:
        return np.nan
    if isinstance(value, (int, float, np.number)):
        return float(value)
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "null"}:
        return np.nan
    # Remove markdown backticks or surrounding spaces.
    text = text.strip(" `")
    try:
        return float(text)
    except ValueError:
        match = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", text)
        return float(match.group(0)) if match else np.nan


def parse_extension_report_table(path: Path) -> pd.DataFrame:
    """Parse the Markdown separation-summary table from the extension report."""
    if not path.exists():
        return pd.DataFrame()
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    rows = []
    in_table = False
    headers: list[str] | None = None
    for line in lines:
        if line.strip().startswith("| source file | component |"):
            in_table = True
            headers = [h.strip() for h in line.strip().strip("|").split("|")]
            continue
        if in_table:
            if not line.strip().startswith("|"):
                break
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if parts and all(set(p) <= {"-", ":"} for p in parts):
                continue
            if headers and len(parts) == len(headers):
                rows.append(dict(zip(headers, parts)))
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    rename = {
        "source file": "source_file",
        "d [fm]": "source_separation_fm",
        "group": "nominal_separation_group",
        "n": "n_points",
        "peak [GeV^2]": "peak_field_GeV2",
        "FWHM [fm]": "fwhm_estimate_fm",
        "area": "area_trapz_GeV2_fm",
    }
    df = df.rename(columns=rename)
    for col in ["source_separation_fm", "n_points", "peak_field_GeV2", "fwhm_estimate_fm", "area_trapz_GeV2_fm"]:
        if col in df.columns:
            df[col] = df[col].map(_to_float)
    if "n_points" in df.columns:
        df["n_points"] = df["n_points"].fillna(0).astype(int)
    df["data_status"] = "parsed_from_extension_report_summary_table"
    return df


def estimate_fwhm(group: pd.DataFrame) -> float:
    """Estimate FWHM using linear interpolation of the half-maximum crossings."""
    if group.empty or "x_t_fm" not in group or "field_value_GeV2" not in group:
        return np.nan
    g = group[["x_t_fm", "field_value_GeV2"]].dropna().sort_values("x_t_fm")
    if len(g) < 5:
        return np.nan
    x = g["x_t_fm"].to_numpy(float)
    y = g["field_value_GeV2"].to_numpy(float)
    ymax = np.nanmax(y)
    if not np.isfinite(ymax) or ymax <= 0:
        return np.nan
    half = ymax / 2.0
    above = y >= half
    if above.sum() < 2:
        return np.nan
    indices = np.where(above)[0]
    left_idx = indices[0]
    right_idx = indices[-1]

    def cross_between(i1: int, i2: int) -> float:
        x1, y1 = x[i1], y[i1]
        x2, y2 = x[i2], y[i2]
        if y2 == y1:
            return float(x1)
        return float(x1 + (half - y1) * (x2 - x1) / (y2 - y1))

    left = x[left_idx]
    if left_idx > 0:
        left = cross_between(left_idx - 1, left_idx)
    right = x[right_idx]
    if right_idx < len(x) - 1:
        right = cross_between(right_idx, right_idx + 1)
    width = right - left
    return float(width) if width >= 0 else np.nan


def summarize_long_profiles(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    if df.empty:
        return pd.DataFrame()
    required = {"source_file", "component", "source_separation_fm", "x_t_fm", "field_value_GeV2"}
    if not required.issubset(df.columns):
        return pd.DataFrame()
    if "target" not in df.columns:
        df["target"] = ""
    if "nominal_separation_group" not in df.columns:
        df["nominal_separation_group"] = df["source_separation_fm"].map(lambda v: f"{v:g} fm")
    if "data_status" not in df.columns:
        df["data_status"] = "computed_from_long_pointwise_table"
    keys = ["source_file", "target", "component", "source_separation_fm", "nominal_separation_group"]
    rows = []
    for keys_vals, g in df.groupby(keys, dropna=False):
        row = dict(zip(keys, keys_vals))
        gg = g.dropna(subset=["x_t_fm", "field_value_GeV2"])
        row["n_points"] = int(len(gg))
        row["x_min_fm"] = float(gg["x_t_fm"].min()) if len(gg) else np.nan
        row["x_max_fm"] = float(gg["x_t_fm"].max()) if len(gg) else np.nan
        row["peak_field_GeV2"] = float(gg["field_value_GeV2"].max()) if len(gg) else np.nan
        if len(gg):
            center_idx = (gg["x_t_fm"].abs()).idxmin()
            row["center_field_GeV2"] = float(gg.loc[center_idx, "field_value_GeV2"])
        else:
            row["center_field_GeV2"] = np.nan
        row["fwhm_estimate_fm"] = estimate_fwhm(gg)
        row["area_trapz_GeV2_fm"] = float(np.trapz(gg.sort_values("x_t_fm")["field_value_GeV2"], gg.sort_values("x_t_fm")["x_t_fm"])) if len(gg) >= 2 else np.nan
        row["data_status"] = ";".join(sorted(map(str, g.get("data_status", pd.Series(["computed_from_long_pointwise_table"])).dropna().unique())))
        rows.append(row)
    return pd.DataFrame(rows)


def load_summary(paths: Paths) -> tuple[pd.DataFrame, str]:
    # Prefer an already-complete summary CSV.
    if paths.summary_csv.exists():
        df = pd.read_csv(paths.summary_csv)
        if len(df) >= 5:
            return normalize_summary(df), f"summary_csv:{paths.summary_csv}"
    # If summary CSV is incomplete, parse the full extension report table if present.
    md_df = parse_extension_report_table(paths.extension_report)
    if len(md_df) >= 5:
        return normalize_summary(md_df), f"extension_report_table:{paths.extension_report}"
    # Fall back to long pointwise table.
    long_df = summarize_long_profiles(paths.long_csv)
    if len(long_df):
        return normalize_summary(long_df), f"long_pointwise_csv:{paths.long_csv}"
    # Last fallback: small summary CSV.
    if paths.summary_csv.exists():
        return normalize_summary(pd.read_csv(paths.summary_csv)), f"summary_csv_incomplete:{paths.summary_csv}"
    return pd.DataFrame(), "none"


def normalize_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    ren = {
        "d [fm]": "source_separation_fm",
        "peak [GeV^2]": "peak_field_GeV2",
        "FWHM [fm]": "fwhm_estimate_fm",
        "area": "area_trapz_GeV2_fm",
        "n": "n_points",
        "source file": "source_file",
        "group": "nominal_separation_group",
    }
    df = df.rename(columns=ren)
    for col in ["source_file", "component", "nominal_separation_group", "target", "data_status"]:
        if col not in df.columns:
            df[col] = ""
    for col in ["source_separation_fm", "n_points", "peak_field_GeV2", "center_field_GeV2", "fwhm_estimate_fm", "area_trapz_GeV2_fm"]:
        if col in df.columns:
            df[col] = df[col].map(_to_float)
        else:
            df[col] = np.nan
    df["n_points"] = df["n_points"].fillna(0).astype(int)
    df["component"] = df["component"].astype(str).str.strip().replace({"": "UNKNOWN"})
    df["source_file"] = df["source_file"].astype(str).str.strip()
    return df


def qc_decision_table(df: pd.DataFrame, fwhm_max: float = 1.5, min_points: int = 5, peak_ratio_hi: float = 1.75, peak_ratio_lo: float = 0.45) -> pd.DataFrame:
    df = df.copy()
    reasons = []
    decisions = []

    # Build medians within component and nominal group for outlier checks.
    med = (
        df[df["component"].isin(["FULL", "NP"])]
        .groupby(["component", "nominal_separation_group"], dropna=False)["peak_field_GeV2"]
        .median()
        .rename("group_peak_median")
        .reset_index()
    )
    df = df.merge(med, on=["component", "nominal_separation_group"], how="left")
    df["peak_to_group_median"] = df["peak_field_GeV2"] / df["group_peak_median"]

    for _, row in df.iterrows():
        r = []
        component = str(row["component"])
        n = int(row["n_points"]) if pd.notna(row["n_points"]) else 0
        fwhm = row["fwhm_estimate_fm"]
        peak = row["peak_field_GeV2"]
        ratio = row.get("peak_to_group_median", np.nan)

        if n <= 1:
            r.append("summary_or_single_point_row")
        elif n < min_points:
            r.append(f"too_few_points_n<{min_points}")
        if component == "PAPER_DEFINED":
            r.append("paper_defined_profile_class_keep_separate")
        elif component not in {"FULL", "NP"}:
            r.append("unknown_component")
        if not np.isfinite(peak) or peak <= 0:
            r.append("invalid_peak")
        if not np.isfinite(fwhm):
            r.append("missing_fwhm")
        elif fwhm <= 0:
            r.append("invalid_fwhm")
        elif fwhm > fwhm_max:
            r.append(f"wide_fwhm>{fwhm_max:g}fm")
        if np.isfinite(ratio) and (ratio > peak_ratio_hi or ratio < peak_ratio_lo):
            r.append("peak_outlier_vs_group_median")

        if "summary_or_single_point_row" in r or "invalid_peak" in r or "invalid_fwhm" in r or "unknown_component" in r:
            decision = "EXCLUDE_FROM_TREND"
        elif component == "PAPER_DEFINED" or any(x.startswith("wide_fwhm") for x in r) or "peak_outlier_vs_group_median" in r or "missing_fwhm" in r:
            decision = "REVIEW_SEPARATELY"
        else:
            decision = "ACCEPT_FOR_TREND"
        decisions.append(decision)
        reasons.append("; ".join(r) if r else "passes_basic_qc")
    df["qc_decision"] = decisions
    df["qc_reason"] = reasons
    return df


def maybe_load_long(paths: Paths) -> pd.DataFrame:
    if paths.long_csv.exists():
        try:
            return pd.read_csv(paths.long_csv)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()


def plot_trusted_trends(qc: pd.DataFrame, reports: Path) -> list[str]:
    reports.mkdir(parents=True, exist_ok=True)
    figs = []
    trusted = qc[(qc["qc_decision"] == "ACCEPT_FOR_TREND") & qc["component"].isin(["FULL", "NP"])].copy()
    if trusted.empty:
        return figs
    for ycol, ylabel, filename, title in [
        ("peak_field_GeV2", "peak field [GeV^2]", "fig_baker_qc_peak_trusted.png", "QC trusted Baker flux-tube peak vs separation"),
        ("fwhm_estimate_fm", "FWHM estimate [fm]", "fig_baker_qc_width_trusted.png", "QC trusted Baker flux-tube width vs separation"),
    ]:
        fig, ax = plt.subplots(figsize=(10, 5.5), dpi=160)
        for component, group in trusted.groupby("component"):
            g = group.dropna(subset=["source_separation_fm", ycol]).sort_values("source_separation_fm")
            if len(g):
                ax.plot(g["source_separation_fm"], g[ycol], marker="o", label=component)
        ax.set_title(title)
        ax.set_xlabel("source separation d [fm]")
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        out = reports / filename
        fig.savefig(out)
        plt.close(fig)
        figs.append(str(out))
    return figs


def plot_trusted_profiles(long_df: pd.DataFrame, qc: pd.DataFrame, reports: Path) -> list[str]:
    if long_df.empty:
        return []
    if not {"source_file", "component", "source_separation_fm", "x_t_fm", "field_value_GeV2"}.issubset(long_df.columns):
        return []
    figs = []
    trusted_keys = qc[qc["qc_decision"] == "ACCEPT_FOR_TREND"][["source_file", "component", "source_separation_fm"]].copy()
    if trusted_keys.empty:
        return figs
    # merge approximate by rounding distance because text parse can differ very slightly.
    long = long_df.copy()
    long["_d_round"] = long["source_separation_fm"].map(lambda v: round(float(v), 6) if pd.notna(v) else np.nan)
    trusted_keys["_d_round"] = trusted_keys["source_separation_fm"].map(lambda v: round(float(v), 6) if pd.notna(v) else np.nan)
    selected = long.merge(trusted_keys[["source_file", "component", "_d_round"]].drop_duplicates(), on=["source_file", "component", "_d_round"], how="inner")
    if selected.empty:
        return figs
    for component, filename in [("FULL", "fig_baker_qc_profiles_trusted_full.png"), ("NP", "fig_baker_qc_profiles_trusted_np.png")]:
        data = selected[selected["component"] == component]
        if data.empty:
            continue
        fig, ax = plt.subplots(figsize=(11, 6), dpi=160)
        for (source_file, d), g in data.groupby(["source_file", "source_separation_fm"]):
            gg = g.dropna(subset=["x_t_fm", "field_value_GeV2"]).sort_values("x_t_fm")
            if len(gg) >= 5:
                ax.plot(gg["x_t_fm"], gg["field_value_GeV2"], marker="o", markersize=2.5, linewidth=1, label=f"d={d:.3f} {source_file[:16]}")
        ax.set_title(f"QC trusted Baker flux-tube profiles: {component}")
        ax.set_xlabel("transverse distance x_t [fm]")
        ax.set_ylabel("longitudinal chromoelectric field [GeV^2]")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=7, ncols=1)
        fig.tight_layout()
        out = reports / filename
        fig.savefig(out)
        plt.close(fig)
        figs.append(str(out))
    return figs


def markdown_table(df: pd.DataFrame, columns: list[str], max_rows: int = 60) -> str:
    if df.empty:
        return "_No rows._"
    small = df[columns].copy().head(max_rows)
    # format numeric values.
    for col in small.columns:
        if pd.api.types.is_numeric_dtype(small[col]):
            small[col] = small[col].map(lambda v: "" if pd.isna(v) else f"{v:.6g}")
    headers = "| " + " | ".join(columns) + " |"
    sep = "|" + "|".join(["---" for _ in columns]) + "|"
    rows = [headers, sep]
    for _, row in small.iterrows():
        rows.append("| " + " | ".join(str(row[c]) for c in columns) + " |")
    if len(df) > max_rows:
        rows.append(f"\n_Only first {max_rows} of {len(df)} rows shown._")
    return "\n".join(rows)


def write_report(paths: Paths, qc: pd.DataFrame, source_used: str, figs: list[str], long_rows: int) -> Path:
    reports = paths.reports
    metrics_counts = qc["qc_decision"].value_counts().to_dict() if not qc.empty else {}
    component_counts = qc["component"].value_counts().to_dict() if not qc.empty else {}
    trusted = qc[qc["qc_decision"] == "ACCEPT_FOR_TREND"].copy()
    review = qc[qc["qc_decision"].isin(["REVIEW_SEPARATELY", "EXCLUDE_FROM_TREND"])].copy()
    trend_range = "not available"
    if not trusted.empty:
        trend_range = f"{trusted['source_separation_fm'].min():.3f}–{trusted['source_separation_fm'].max():.3f} fm"
    report = f"""# Baker Flux-Tube Extension QC

Fourth diagnostic for the UNNS + color confinement investigation.

This is a quality-control report, not a final physics interpretation. Its purpose is to separate usable separation-dependent flux-tube profiles from summary rows, paper-defined aggregate rows, and outlier-like profiles before a formal flux-tube extension report is written.

## 1. Input status

- Summary source used: `{source_used}`
- Profile-summary rows inspected: {len(qc)}
- Long pointwise rows available locally: {long_rows}
- Components represented: `{json.dumps(component_counts, ensure_ascii=False)}`
- QC decision counts: `{json.dumps(metrics_counts, ensure_ascii=False)}`

## 2. QC rules

The QC pass applies conservative rules:

```text
ACCEPT_FOR_TREND:
  FULL or NP component; n_points >= 5; valid peak; finite FWHM <= 1.5 fm; no strong local peak outlier.

REVIEW_SEPARATELY:
  PAPER_DEFINED component, unusually wide FWHM, missing FWHM, or peak outlier versus same component/group.

EXCLUDE_FROM_TREND:
  single-point summary row, invalid field/width values, unknown component, or too few data points.
```

The review threshold `FWHM > 1.5 fm` is deliberately permissive: it flags extreme width estimates without removing ordinary broadened profiles.

## 3. QC summary

Trusted trend separation range: **{trend_range}**.

The trusted rows are suitable for cautious trend plotting only. They are not yet a fitted UNNS law.

## 4. Accepted trend rows

{markdown_table(trusted.sort_values(['component', 'source_separation_fm', 'source_file']), ['source_file', 'component', 'source_separation_fm', 'n_points', 'peak_field_GeV2', 'fwhm_estimate_fm', 'area_trapz_GeV2_fm', 'qc_decision'], max_rows=80)}

## 5. Rows requiring review or exclusion

{markdown_table(review.sort_values(['qc_decision', 'component', 'source_separation_fm', 'source_file']), ['source_file', 'component', 'source_separation_fm', 'n_points', 'peak_field_GeV2', 'fwhm_estimate_fm', 'qc_decision', 'qc_reason'], max_rows=80)}

## 6. Figures produced

"""
    if figs:
        for fig in figs:
            name = Path(fig).name
            report += f"- `{name}`\n"
    else:
        report += "No figures produced because no trusted rows or pointwise profile table was available.\n"
    report += """
## 7. UNNS interpretation boundary

This QC pass does not yet establish route broadening, route weakening, or threshold approach. It only establishes which Baker profiles may be used in the next formal interpretation.

The provisional UNNS reading after QC is:

```text
trusted FULL / NP profiles
-> usable localized-route geometry samples

PAPER_DEFINED and wide/outlier profiles
-> keep separate until source conventions and normalization are inspected

single-point summary rows
-> exclude from shape/width/peak trend plots
```

## 8. Next action

Use the accepted FULL and NP rows to write the formal flux-tube extension report only after inspecting the rows marked `REVIEW_SEPARATELY`, especially large-distance and paper-defined profiles.
"""
    out = reports / "04_baker_flux_extension_qc.md"
    out.write_text(report, encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="QC Baker flux-tube extension profiles.")
    parser.add_argument("--root", default=".", help="Project pack root. Defaults to current working directory.")
    parser.add_argument("--fwhm-max", type=float, default=1.5, help="FWHM review threshold in fm.")
    parser.add_argument("--min-points", type=int, default=5, help="Minimum points for trend acceptance.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    paths = get_paths(root)
    paths.reports.mkdir(parents=True, exist_ok=True)

    summary, source_used = load_summary(paths)
    if summary.empty:
        raise SystemExit("No Baker flux summary data found. Run extend_baker_flux_profiles_across_separations.py first.")

    qc = qc_decision_table(summary, fwhm_max=args.fwhm_max, min_points=args.min_points)
    qc_out = paths.reports / "baker_flux_profile_qc_table.csv"
    qc.to_csv(qc_out, index=False)

    trusted = qc[qc["qc_decision"] == "ACCEPT_FOR_TREND"].copy()
    trusted_out = paths.reports / "baker_flux_profile_trusted_summary.csv"
    trusted.to_csv(trusted_out, index=False)

    long_df = maybe_load_long(paths)
    figs = []
    figs += plot_trusted_trends(qc, paths.reports)
    figs += plot_trusted_profiles(long_df, qc, paths.reports)

    metrics = {
        "source_used": source_used,
        "summary_rows_inspected": int(len(qc)),
        "long_pointwise_rows_available": int(len(long_df)),
        "decision_counts": qc["qc_decision"].value_counts().to_dict(),
        "component_counts": qc["component"].value_counts().to_dict(),
        "accepted_rows": int((qc["qc_decision"] == "ACCEPT_FOR_TREND").sum()),
        "review_rows": int((qc["qc_decision"] == "REVIEW_SEPARATELY").sum()),
        "excluded_rows": int((qc["qc_decision"] == "EXCLUDE_FROM_TREND").sum()),
        "fwhm_review_threshold_fm": args.fwhm_max,
        "min_points": args.min_points,
        "figures": [str(Path(f).relative_to(root)) if Path(f).is_absolute() and root in Path(f).parents else str(f) for f in figs],
        "outputs": {
            "qc_table": str(qc_out.relative_to(root)),
            "trusted_summary": str(trusted_out.relative_to(root)),
            "report": "reports/04_baker_flux_extension_qc.md",
        },
    }
    metrics_out = paths.reports / "04_baker_flux_extension_qc_metrics.json"
    metrics_out.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    report_out = write_report(paths, qc, source_used, figs, long_rows=len(long_df))

    print("BAKER FLUX EXTENSION QC COMPLETE")
    print(f"summary rows inspected: {len(qc)}")
    print(f"accepted: {metrics['accepted_rows']}  review: {metrics['review_rows']}  excluded: {metrics['excluded_rows']}")
    print(f"report: {report_out}")
    print(f"metrics: {metrics_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
