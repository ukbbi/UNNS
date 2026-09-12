#!/usr/bin/env python3
"""
tokamark_physical_window_label_analyzer.py

UNNS-H Mode Project
Physical-window label analyzer.

Purpose
-------
Compare independently edited physical-window labels against the v0.2
diagnostic-confidence UNNS-H Mode time traces.

This follows:

    docs/28_PHYSICAL_WINDOW_LABELING_REQUIREMENTS.md

and is intended to produce the evidence for:

    docs/29_PHYSICAL_WINDOW_LABELING_RESULTS.md

Important
---------
This script does NOT create physical labels.
It reads a manually edited label file and tests those labels against
m_edge_raw(t), m_edge_conf(t), Q_diag(t), and P_missing_critical(t).

Default label input
-------------------
    outputs/reports/tokamark_physical_window_label_template_EDITED.csv

Required per-shot input
-----------------------
    outputs/reports/tokamark_shot_<SHOT>_m_edge_confidence_revision.csv

Run from project root
---------------------

    python components\tokamark_physical_window_label_analyzer.py --out-dir outputs\reports

Custom label file:

    python components\tokamark_physical_window_label_analyzer.py ^
      --labels outputs\reports\tokamark_physical_window_label_template_EDITED.csv ^
      --out-dir outputs\reports

Outputs
-------
    outputs/reports/tokamark_physical_window_label_analysis.csv
    outputs/reports/tokamark_physical_window_label_analysis_by_label.csv
    outputs/reports/tokamark_physical_window_label_transition_pairs.csv
    outputs/reports/tokamark_physical_window_label_analysis.json
    outputs/reports/tokamark_physical_window_label_analysis.md

Scientific caution
------------------
This is the first physical-window comparison. It is not yet broad physical
validation. It tests whether manually labeled windows show the expected
relationship to the confidence-corrected structural margin.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


VALIDATION_LABELS = [
    "L_MODE",
    "LH_TRANSITION",
    "H_MODE_STABLE",
    "PRE_ELM",
    "POST_ELM",
    "HL_BACK_TRANSITION",
]

ALL_LABELS = VALIDATION_LABELS + ["AMBIGUOUS", "UNLABELABLE"]


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def make_json_safe(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    if isinstance(obj, tuple):
        return [make_json_safe(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        if not np.isfinite(obj):
            return None
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    try:
        if pd.isna(obj):
            return None
    except Exception:
        pass
    return obj


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(make_json_safe(payload), indent=2, ensure_ascii=False), encoding="utf-8")


def df_to_markdown(df: pd.DataFrame, index: bool = False, floatfmt: str = ".6g") -> str:
    try:
        return df.to_markdown(index=index, floatfmt=floatfmt)
    except Exception:
        if df.empty:
            return "_No rows._"
        cols = list(df.columns)
        rows = [[row.get(c, "") for c in cols] for _, row in df.iterrows()]
        widths = [len(str(c)) for c in cols]
        for row in rows:
            for i, val in enumerate(row):
                widths[i] = max(widths[i], len(str(val)))
        def line(vals: Iterable[Any]) -> str:
            return "| " + " | ".join(str(v).ljust(widths[i]) for i, v in enumerate(vals)) + " |"
        out = [line(cols), "| " + " | ".join("-" * w for w in widths) + " |"]
        out.extend(line(row) for row in rows)
        return "\n".join(out)


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except Exception:
        pass
    text = str(value).strip().lower()
    return text in {"true", "1", "yes", "y", "excluded"}


def fnum(value: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if value is None or value == "":
            return default
        v = float(value)
        if not np.isfinite(v):
            return default
        return v
    except Exception:
        return default


def numeric(df: pd.DataFrame, col: str, default: float = np.nan) -> pd.Series:
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    return pd.Series([default] * len(df), index=df.index, dtype=float)


def finite_stats(series: pd.Series) -> Dict[str, Any]:
    arr = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return {
            "finite_count": 0,
            "finite_fraction": 0.0,
            "min": None,
            "median": None,
            "mean": None,
            "max": None,
            "std": None,
        }
    return {
        "finite_count": int(finite.size),
        "finite_fraction": float(finite.size / max(arr.size, 1)),
        "min": float(np.nanmin(finite)),
        "median": float(np.nanmedian(finite)),
        "mean": float(np.nanmean(finite)),
        "max": float(np.nanmax(finite)),
        "std": float(np.nanstd(finite)),
    }


def fraction_true(series: pd.Series) -> Optional[float]:
    if len(series) == 0:
        return None
    return float(series.fillna(False).astype(bool).mean())


def safe_diff(a: Any, b: Any) -> Optional[float]:
    av = fnum(a)
    bv = fnum(b)
    if av is None or bv is None:
        return None
    return float(av - bv)


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_labels(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Label file not found: {path}")

    df = pd.read_csv(path)

    required = [
        "shot_id",
        "window_id",
        "label_type",
        "t_start",
        "t_end",
        "label_confidence",
        "excluded_from_validation",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Label file missing required columns: {missing}")

    df = df.copy()
    df["shot_id"] = pd.to_numeric(df["shot_id"], errors="coerce")
    df = df.dropna(subset=["shot_id"]).copy()
    df["shot_id"] = df["shot_id"].astype(int)
    df["label_type"] = df["label_type"].astype(str).str.strip().str.upper()
    df["excluded_from_validation_bool"] = df["excluded_from_validation"].apply(as_bool)
    df["t_start_numeric"] = pd.to_numeric(df["t_start"], errors="coerce")
    df["t_end_numeric"] = pd.to_numeric(df["t_end"], errors="coerce")
    df["window_duration"] = df["t_end_numeric"] - df["t_start_numeric"]
    return df


def load_trace(out_dir: Path, shot_id: int) -> pd.DataFrame:
    path = out_dir / f"tokamark_shot_{shot_id}_m_edge_confidence_revision.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)

    # Ensure essential columns exist.
    if "time_s" not in df.columns:
        if "time" in df.columns:
            df["time_s"] = pd.to_numeric(df["time"], errors="coerce")
        else:
            df["time_s"] = np.arange(len(df), dtype=float)

    if "m_edge_raw" not in df.columns:
        if "m_edge" in df.columns:
            df["m_edge_raw"] = pd.to_numeric(df["m_edge"], errors="coerce")
        else:
            df["m_edge_raw"] = np.nan

    for col in ["m_edge_conf", "Q_diag", "P_missing_critical"]:
        if col not in df.columns:
            df[col] = np.nan

    if "m_edge_conf_state" not in df.columns:
        df["m_edge_conf_state"] = "unknown"

    return df


# ---------------------------------------------------------------------------
# Window analysis
# ---------------------------------------------------------------------------

def trace_window(df: pd.DataFrame, start: float, end: float) -> pd.DataFrame:
    if df.empty or "time_s" not in df.columns:
        return pd.DataFrame()
    t = pd.to_numeric(df["time_s"], errors="coerce")
    return df[(t >= start) & (t <= end)].copy()


def analyze_window(label_row: pd.Series, trace: pd.DataFrame) -> Dict[str, Any]:
    shot_id = int(label_row["shot_id"])
    window_id = str(label_row["window_id"])
    label_type = str(label_row["label_type"])
    t_start = fnum(label_row["t_start_numeric"])
    t_end = fnum(label_row["t_end_numeric"])
    duration = safe_diff(t_end, t_start)

    out: Dict[str, Any] = {
        "shot_id": shot_id,
        "window_id": window_id,
        "label_type": label_type,
        "label_confidence": label_row.get("label_confidence", ""),
        "excluded_from_validation": bool(label_row.get("excluded_from_validation_bool", False)),
        "exclusion_reason": label_row.get("exclusion_reason", ""),
        "notes": label_row.get("notes", ""),
        "t_start": t_start,
        "t_end": t_end,
        "window_duration": duration,
        "analysis_status": "ok",
    }

    if t_start is None or t_end is None or duration is None or duration <= 0:
        out["analysis_status"] = "invalid_window_time"
        return out

    if trace.empty:
        out["analysis_status"] = "missing_trace"
        return out

    w = trace_window(trace, t_start, t_end)
    out["n_samples"] = int(len(w))

    if w.empty:
        out["analysis_status"] = "no_trace_samples_in_window"
        return out

    # Core metrics.
    for col in [
        "m_edge_raw",
        "m_edge_conf",
        "m_edge_conf_simple",
        "Q_diag",
        "P_missing_critical",
        "Q_power",
        "Q_density",
        "Q_edge",
        "Q_profile",
        "Q_geometry",
        "Q_missing",
        "Q_capacity",
        "Q_fragmentation",
        "C_edge_capacity",
        "F_route_fragmentation",
        "S_edge_response",
        "S_power_balance",
        "S_transport",
        "missingness_pressure",
        "dalpha_proxy",
        "softx_combined_proxy",
        "profile_gradient_proxy",
        "nbi_proxy",
        "density_proxy",
    ]:
        if col in w.columns:
            stats = finite_stats(w[col])
            for k, v in stats.items():
                out[f"{col}_{k}"] = v

    state = w.get("m_edge_conf_state", pd.Series(["unknown"] * len(w))).astype(str)
    raw_state = w.get("m_edge_raw_state", pd.Series(["unknown"] * len(w))).astype(str)

    out["conf_positive_fraction"] = float(state.eq("confidence_positive_boundary_margin").mean())
    out["conf_negative_fraction"] = float(state.eq("confidence_negative_leakage_margin").mean())
    out["conf_ambiguous_fraction"] = float(state.eq("confidence_boundary_ambiguous_margin").mean())
    out["conf_low_confidence_fraction"] = float(state.eq("low_confidence_uninterpretable").mean())

    out["raw_positive_fraction"] = float(raw_state.eq("positive_boundary_margin").mean())
    out["raw_negative_fraction"] = float(raw_state.eq("negative_leakage_margin").mean())
    out["raw_ambiguous_fraction"] = float(raw_state.eq("boundary_ambiguous_margin").mean())

    out["validation_eligible"] = (
        (label_type in VALIDATION_LABELS)
        and not bool(label_row.get("excluded_from_validation_bool", False))
        and out["analysis_status"] == "ok"
    )

    return out


def analyze_labels(labels: pd.DataFrame, out_dir: Path) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []

    traces: Dict[int, pd.DataFrame] = {}
    for shot in sorted(labels["shot_id"].astype(int).unique()):
        traces[shot] = load_trace(out_dir, shot)

    for _, label in labels.iterrows():
        shot = int(label["shot_id"])
        rows.append(analyze_window(label, traces.get(shot, pd.DataFrame())))

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Aggregation and decision
# ---------------------------------------------------------------------------

def aggregate_by_label(analysis: pd.DataFrame) -> pd.DataFrame:
    if analysis.empty:
        return pd.DataFrame()

    eligible = analysis[analysis.get("validation_eligible", False).astype(bool)].copy()
    if eligible.empty:
        return pd.DataFrame()

    rows: List[Dict[str, Any]] = []
    for label_type, group in eligible.groupby("label_type", dropna=False):
        row: Dict[str, Any] = {
            "label_type": label_type,
            "window_count": int(len(group)),
            "shot_count": int(group["shot_id"].nunique()),
            "total_duration": float(pd.to_numeric(group["window_duration"], errors="coerce").fillna(0).sum()),
        }
        for col in [
            "m_edge_raw_median",
            "m_edge_conf_median",
            "conf_positive_fraction",
            "conf_negative_fraction",
            "conf_low_confidence_fraction",
            "Q_diag_median",
            "P_missing_critical_median",
            "C_edge_capacity_median",
            "F_route_fragmentation_median",
            "S_edge_response_median",
            "S_power_balance_median",
            "S_transport_median",
        ]:
            if col in group.columns:
                stats = finite_stats(group[col])
                row[f"{col}_median"] = stats["median"]
                row[f"{col}_mean"] = stats["mean"]
                row[f"{col}_min"] = stats["min"]
                row[f"{col}_max"] = stats["max"]
        rows.append(row)

    return pd.DataFrame(rows).sort_values("label_type").reset_index(drop=True)


def transition_pairs(analysis: pd.DataFrame) -> pd.DataFrame:
    """
    Compare L_MODE and H_MODE_STABLE windows within the same shot where available,
    and record transition window metrics if present.
    """
    if analysis.empty:
        return pd.DataFrame()

    eligible = analysis[analysis.get("validation_eligible", False).astype(bool)].copy()
    if eligible.empty:
        return pd.DataFrame()

    rows: List[Dict[str, Any]] = []

    for shot, group in eligible.groupby("shot_id"):
        lmode = group[group["label_type"].eq("L_MODE")]
        hmode = group[group["label_type"].eq("H_MODE_STABLE")]
        trans = group[group["label_type"].eq("LH_TRANSITION")]

        if lmode.empty and hmode.empty and trans.empty:
            continue

        # Use first/median if multiple windows exist.
        def med(label_df: pd.DataFrame, col: str) -> Optional[float]:
            if label_df.empty or col not in label_df.columns:
                return None
            vals = pd.to_numeric(label_df[col], errors="coerce")
            vals = vals[np.isfinite(vals)]
            if vals.empty:
                return None
            return float(vals.median())

        row: Dict[str, Any] = {
            "shot_id": int(shot),
            "has_L_MODE": not lmode.empty,
            "has_LH_TRANSITION": not trans.empty,
            "has_H_MODE_STABLE": not hmode.empty,
            "L_MODE_m_edge_conf_median": med(lmode, "m_edge_conf_median"),
            "LH_TRANSITION_m_edge_conf_median": med(trans, "m_edge_conf_median"),
            "H_MODE_STABLE_m_edge_conf_median": med(hmode, "m_edge_conf_median"),
            "L_MODE_conf_positive_fraction": med(lmode, "conf_positive_fraction"),
            "LH_TRANSITION_conf_positive_fraction": med(trans, "conf_positive_fraction"),
            "H_MODE_STABLE_conf_positive_fraction": med(hmode, "conf_positive_fraction"),
            "L_MODE_Q_diag_median": med(lmode, "Q_diag_median"),
            "H_MODE_STABLE_Q_diag_median": med(hmode, "Q_diag_median"),
            "L_MODE_P_missing_critical_median": med(lmode, "P_missing_critical_median"),
            "H_MODE_STABLE_P_missing_critical_median": med(hmode, "P_missing_critical_median"),
        }
        row["delta_H_minus_L_m_edge_conf_median"] = safe_diff(
            row["H_MODE_STABLE_m_edge_conf_median"],
            row["L_MODE_m_edge_conf_median"],
        )
        row["delta_H_minus_L_conf_positive_fraction"] = safe_diff(
            row["H_MODE_STABLE_conf_positive_fraction"],
            row["L_MODE_conf_positive_fraction"],
        )
        rows.append(row)

    return pd.DataFrame(rows).sort_values("shot_id").reset_index(drop=True)


def decide(analysis: pd.DataFrame, by_label: pd.DataFrame, pairs: pd.DataFrame) -> Dict[str, Any]:
    reasons: List[str] = []
    warnings: List[str] = []
    decision = "physical_window_analysis_inconclusive"

    eligible = analysis[analysis.get("validation_eligible", False).astype(bool)].copy() if not analysis.empty else pd.DataFrame()
    excluded = analysis[~analysis.get("validation_eligible", False).astype(bool)].copy() if not analysis.empty else pd.DataFrame()

    if eligible.empty:
        return {
            "decision": "physical_window_analysis_no_eligible_windows",
            "reasons": [],
            "warnings": ["No validation-eligible physical windows were found."],
            "eligible_window_count": 0,
            "excluded_window_count": int(len(excluded)),
        }

    label_counts = eligible["label_type"].value_counts().to_dict()
    if "L_MODE" in label_counts and "H_MODE_STABLE" in label_counts:
        reasons.append("Both L_MODE and H_MODE_STABLE labels are present.")
    else:
        warnings.append("L_MODE and H_MODE_STABLE are not both present; direct comparison is limited.")

    if "LH_TRANSITION" in label_counts:
        reasons.append("LH_TRANSITION labels are present for transition-local comparison.")
    else:
        warnings.append("No LH_TRANSITION labels are present.")

    # Label-level directional test.
    def label_metric(label: str, metric: str) -> Optional[float]:
        if by_label.empty or metric not in by_label.columns:
            return None
        row = by_label[by_label["label_type"].eq(label)]
        if row.empty:
            return None
        return fnum(row.iloc[0][metric])

    h_conf = label_metric("H_MODE_STABLE", "m_edge_conf_median_median")
    l_conf = label_metric("L_MODE", "m_edge_conf_median_median")
    h_pos = label_metric("H_MODE_STABLE", "conf_positive_fraction_median")
    l_pos = label_metric("L_MODE", "conf_positive_fraction_median")

    if h_conf is not None and l_conf is not None:
        if h_conf > l_conf:
            reasons.append("H_MODE_STABLE windows have higher median m_edge_conf than L_MODE windows.")
        else:
            warnings.append("H_MODE_STABLE windows do not have higher median m_edge_conf than L_MODE windows.")

    if h_pos is not None and l_pos is not None:
        if h_pos >= l_pos:
            reasons.append("H_MODE_STABLE windows have equal or higher confidence-positive fraction than L_MODE windows.")
        else:
            warnings.append("H_MODE_STABLE windows have lower confidence-positive fraction than L_MODE windows.")

    # Within-shot pair test.
    if not pairs.empty and "delta_H_minus_L_m_edge_conf_median" in pairs.columns:
        deltas = pd.to_numeric(pairs["delta_H_minus_L_m_edge_conf_median"], errors="coerce")
        deltas = deltas[np.isfinite(deltas)]
        if not deltas.empty:
            positive_rate = float((deltas > 0).mean())
            if positive_rate >= 0.60:
                reasons.append("Most within-shot H_MODE_STABLE windows have higher m_edge_conf than L_MODE windows.")
            else:
                warnings.append("Within-shot H-vs-L m_edge_conf improvement is weak or mixed.")
        else:
            warnings.append("No finite within-shot H-vs-L m_edge_conf deltas.")

    # Excluded controls should not contribute validation evidence.
    if "UNLABELABLE" in analysis["label_type"].values:
        unlab = analysis[analysis["label_type"].eq("UNLABELABLE")]
        if bool(unlab.get("validation_eligible", pd.Series([False] * len(unlab))).any()):
            warnings.append("Some UNLABELABLE rows are validation-eligible; this should not happen.")
        else:
            reasons.append("UNLABELABLE control windows are excluded from validation.")

    if len(reasons) >= 5 and len(warnings) <= 2:
        decision = "physical_window_analysis_passes_first_gate"
    elif len(reasons) >= 3:
        decision = "physical_window_analysis_mixed_but_usable"
    else:
        decision = "physical_window_analysis_inconclusive_or_weak"

    return {
        "decision": decision,
        "reasons": reasons,
        "warnings": warnings,
        "eligible_window_count": int(len(eligible)),
        "excluded_window_count": int(len(excluded)),
        "label_counts": {str(k): int(v) for k, v in label_counts.items()},
    }


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def write_report(
    path: Path,
    *,
    labels_path: Path,
    analysis: pd.DataFrame,
    by_label: pd.DataFrame,
    pairs: pd.DataFrame,
    decision: Dict[str, Any],
) -> None:
    md: List[str] = []
    md.append("# TokaMark Physical-Window Label Analysis")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Compare manually edited physical-window labels against the v0.2 UNNS-H Mode diagnostic-confidence traces.")
    md.append("")
    md.append("This report is the source artifact for:")
    md.append("")
    md.append("```text")
    md.append("docs/")
    md.append("  29_PHYSICAL_WINDOW_LABELING_RESULTS.md")
    md.append("```")
    md.append("")
    md.append("## Input labels")
    md.append("")
    md.append("```text")
    md.append(str(labels_path))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("")
    md.append("```text")
    md.append(f"decision: {decision.get('decision')}")
    md.append(f"eligible windows: {decision.get('eligible_window_count')}")
    md.append(f"excluded windows: {decision.get('excluded_window_count')}")
    md.append(f"label counts: {decision.get('label_counts')}")
    md.append("```")
    md.append("")
    if decision.get("reasons"):
        md.append("### Reasons")
        md.append("")
        for reason in decision["reasons"]:
            md.append(f"- {reason}")
        md.append("")
    if decision.get("warnings"):
        md.append("### Warnings")
        md.append("")
        for warning in decision["warnings"]:
            md.append(f"- {warning}")
        md.append("")
    md.append("## By-label summary")
    md.append("")
    label_cols = [
        "label_type",
        "window_count",
        "shot_count",
        "total_duration",
        "m_edge_conf_median_median",
        "m_edge_raw_median_median",
        "conf_positive_fraction_median",
        "conf_negative_fraction_median",
        "Q_diag_median_median",
        "P_missing_critical_median_median",
        "C_edge_capacity_median_median",
        "F_route_fragmentation_median_median",
    ]
    label_cols = [c for c in label_cols if c in by_label.columns]
    md.append(df_to_markdown(by_label[label_cols], index=False) if not by_label.empty else "_No eligible label summary._")
    md.append("")
    md.append("## Within-shot L/H transition pairs")
    md.append("")
    pair_cols = [
        "shot_id",
        "has_L_MODE",
        "has_LH_TRANSITION",
        "has_H_MODE_STABLE",
        "L_MODE_m_edge_conf_median",
        "LH_TRANSITION_m_edge_conf_median",
        "H_MODE_STABLE_m_edge_conf_median",
        "delta_H_minus_L_m_edge_conf_median",
        "L_MODE_conf_positive_fraction",
        "H_MODE_STABLE_conf_positive_fraction",
        "delta_H_minus_L_conf_positive_fraction",
    ]
    pair_cols = [c for c in pair_cols if c in pairs.columns]
    md.append(df_to_markdown(pairs[pair_cols], index=False) if not pairs.empty else "_No within-shot pairs._")
    md.append("")
    md.append("## Window-level analysis")
    md.append("")
    window_cols = [
        "shot_id",
        "window_id",
        "label_type",
        "label_confidence",
        "validation_eligible",
        "t_start",
        "t_end",
        "window_duration",
        "n_samples",
        "m_edge_conf_median",
        "m_edge_raw_median",
        "conf_positive_fraction",
        "conf_negative_fraction",
        "Q_diag_median",
        "P_missing_critical_median",
        "analysis_status",
    ]
    window_cols = [c for c in window_cols if c in analysis.columns]
    md.append(df_to_markdown(analysis[window_cols], index=False) if not analysis.empty else "_No windows._")
    md.append("")
    md.append("## Bounded interpretation")
    md.append("")
    md.append("This analysis tests alignment between independently edited physical windows and the v0.2 UNNS-H Mode margin. It is not broad H-mode validation and depends on the quality of the manual labels.")
    md.append("")
    md.append("## Next document")
    md.append("")
    md.append("Use these outputs to write:")
    md.append("")
    md.append("```text")
    md.append("docs/")
    md.append("  29_PHYSICAL_WINDOW_LABELING_RESULTS.md")
    md.append("```")
    md.append("")
    path.write_text("\n".join(md), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze edited physical-window labels against m_edge confidence traces.")
    parser.add_argument("--labels", default="outputs/reports/tokamark_physical_window_label_template_EDITED.csv", help="Edited physical-window labels CSV.")
    parser.add_argument("--out-dir", default="outputs/reports", help="Output/report directory.")
    parser.add_argument("--prefix", default="tokamark_physical_window_label_analysis", help="Output prefix.")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    labels_path = Path(args.labels)
    labels = load_labels(labels_path)
    analysis = analyze_labels(labels, out_dir)
    by_label = aggregate_by_label(analysis)
    pairs = transition_pairs(analysis)
    decision = decide(analysis, by_label, pairs)

    analysis_csv = out_dir / f"{args.prefix}.csv"
    by_label_csv = out_dir / f"{args.prefix}_by_label.csv"
    pairs_csv = out_dir / f"{args.prefix}_transition_pairs.csv"
    json_path = out_dir / f"{args.prefix}.json"
    md_path = out_dir / f"{args.prefix}.md"

    analysis.to_csv(analysis_csv, index=False)
    by_label.to_csv(by_label_csv, index=False)
    pairs.to_csv(pairs_csv, index=False)
    write_json(json_path, {
        "component": "tokamark_physical_window_label_analyzer.py",
        "labels_input": str(labels_path),
        "decision": decision,
        "analysis_csv": str(analysis_csv),
        "by_label_csv": str(by_label_csv),
        "transition_pairs_csv": str(pairs_csv),
        "analysis": analysis.to_dict(orient="records"),
        "by_label": by_label.to_dict(orient="records"),
        "transition_pairs": pairs.to_dict(orient="records"),
    })
    write_report(
        md_path,
        labels_path=labels_path,
        analysis=analysis,
        by_label=by_label,
        pairs=pairs,
        decision=decision,
    )

    print("Physical-window label analysis complete.")
    print(f"Labels: {labels_path}")
    print(f"Decision: {decision.get('decision')}")
    print(f"Eligible windows: {decision.get('eligible_window_count')}")
    print(f"Excluded windows: {decision.get('excluded_window_count')}")
    print(f"Analysis CSV: {analysis_csv}")
    print(f"By-label CSV: {by_label_csv}")
    print(f"Transition pairs CSV: {pairs_csv}")
    print(f"JSON: {json_path}")
    print(f"Report: {md_path}")
    print()
    if decision.get("reasons"):
        print("Reasons:")
        for r in decision["reasons"]:
            print(f"  - {r}")
    if decision.get("warnings"):
        print()
        print("Warnings:")
        for w in decision["warnings"]:
            print(f"  - {w}")
    print()
    print("Next report:")
    print("  docs/29_PHYSICAL_WINDOW_LABELING_RESULTS.md")


if __name__ == "__main__":
    main()
