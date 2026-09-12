#!/usr/bin/env python3
"""
tokamark_m_edge_confidence_revision.py

UNNS-H Mode Project
Diagnostic-confidence revision for the TokaMark/MAST m_edge(t) pipeline.

Purpose
-------
Preserve the raw v0.1 margin:

    m_edge_raw(t) = C_edge_capacity(t) - F_route_fragmentation(t)

and add a diagnostic-confidence layer:

    Q_diag(t)
    P_missing_critical(t)
    m_edge_conf(t)

This is the required correction after:

    docs/24_DIAGNOSTIC_CONFIDENCE_REVISION_PLAN.md

The component is deliberately conservative. Missing diagnostics may reduce
confidence, but missing diagnostics may not create positive evidence.

Default panel
-------------
If no shot is provided, the script runs the current five-shot panel:

    12063  reference / full profile + edge candidate
    11830  profile/no-softX comparison
    11876  core+softX/no-Thomson comparison
    11768  partial candidate
    11776  low-priority stress-test candidate

Run from project root
---------------------

    python components\tokamark_m_edge_confidence_revision.py --out-dir outputs\reports

Run one shot:

    python components\tokamark_m_edge_confidence_revision.py --shot-id 12063 --out-dir outputs\reports

Run custom shots:

    python components\tokamark_m_edge_confidence_revision.py --shots 12063 11830 11876 --out-dir outputs\reports

Inputs
------
For each shot, the script expects:

    outputs/reports/tokamark_shot_<SHOT>_m_edge_t_probe.csv
    outputs/reports/tokamark_shot_<SHOT>_signal_probe.json       optional but recommended

and optionally:

    outputs/reports/tokamark_positive_corridor_metadata_candidates.csv

Outputs
-------
Per shot:

    outputs/reports/tokamark_shot_<SHOT>_m_edge_confidence_revision.csv
    outputs/reports/tokamark_shot_<SHOT>_m_edge_confidence_revision.json
    outputs/reports/tokamark_shot_<SHOT>_m_edge_confidence_revision.md

Panel:

    outputs/reports/tokamark_confidence_panel_comparison.csv
    outputs/reports/tokamark_confidence_panel_comparison.json
    outputs/reports/tokamark_confidence_panel_comparison.md

Scientific caution
------------------
This is not physical H-mode validation. It is a correction to the structural
exploratory margin so incomplete diagnostic cases cannot be over-read.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


DEFAULT_PANEL = [12063, 11830, 11876, 11768, 11776]


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(make_json_safe(payload), indent=2, ensure_ascii=False), encoding="utf-8")


def make_json_safe(obj: Any) -> Any:
    """Recursively convert numpy/pandas values to JSON-safe Python values."""
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


def numeric_series(df: pd.DataFrame, col: str, default: float = np.nan) -> pd.Series:
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    return pd.Series([default] * len(df), index=df.index, dtype=float)


def finite_mask(df: pd.DataFrame, col: str) -> pd.Series:
    return np.isfinite(numeric_series(df, col))


def finite_score(df: pd.DataFrame, col: str) -> pd.Series:
    return finite_mask(df, col).astype(float)


def clip01(x: pd.Series | np.ndarray | float) -> pd.Series | np.ndarray | float:
    return np.clip(x, 0.0, 1.0)


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
        "min": float(np.min(finite)),
        "median": float(np.median(finite)),
        "mean": float(np.mean(finite)),
        "max": float(np.max(finite)),
        "std": float(np.std(finite)),
    }


def fraction(count: int, total: int) -> float:
    return float(count / total) if total else 0.0


def df_to_markdown(df: pd.DataFrame, index: bool = False, floatfmt: str = ".6g") -> str:
    try:
        return df.to_markdown(index=index, floatfmt=floatfmt)
    except Exception:
        # Fallback if tabulate is not installed.
        if df.empty:
            return "_No rows._"
        headers = list(df.columns)
        rows = []
        for _, row in df.iterrows():
            rows.append([row.get(c, "") for c in headers])
        widths = [len(str(h)) for h in headers]
        for r in rows:
            for i, cell in enumerate(r):
                widths[i] = max(widths[i], len(str(cell)))
        def fmt_row(values: Iterable[Any]) -> str:
            return "| " + " | ".join(str(v).ljust(widths[i]) for i, v in enumerate(values)) + " |"
        out = [fmt_row(headers), "| " + " | ".join("-" * w for w in widths) + " |"]
        out += [fmt_row(r) for r in rows]
        return "\n".join(out)


def safe_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if value is None:
        return False
    if isinstance(value, float) and np.isnan(value):
        return False
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y", "ok"}
    return bool(value)


def load_metadata(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        df = pd.read_csv(path)
        if "shot_id" in df.columns:
            df["shot_id"] = pd.to_numeric(df["shot_id"], errors="coerce").fillna(-1).astype(int)
        return df
    except Exception:
        return pd.DataFrame()


def metadata_row(metadata: pd.DataFrame, shot_id: int) -> Dict[str, Any]:
    if metadata.empty or "shot_id" not in metadata.columns:
        return {}
    rows = metadata[metadata["shot_id"].astype(int).eq(int(shot_id))]
    if rows.empty:
        return {}
    return rows.iloc[0].to_dict()


def has_loaded_label(signal_json: Dict[str, Any], *labels: str) -> bool:
    loaded = set(signal_json.get("loaded_labels", []) or [])
    for label in labels:
        if label in loaded:
            return True
    return False


def metadata_has(meta: Dict[str, Any], key: str) -> Optional[bool]:
    """Return metadata availability if present; otherwise None."""
    if key in meta:
        return safe_bool(meta.get(key))
    return None


def any_metadata_or_signal(
    meta: Dict[str, Any],
    signal_json: Dict[str, Any],
    meta_key: str,
    labels: Iterable[str],
    fallback: Optional[bool] = None,
) -> bool:
    m = metadata_has(meta, meta_key)
    if m is not None:
        return bool(m)
    if signal_json:
        return any(has_loaded_label(signal_json, label) for label in labels)
    return bool(fallback) if fallback is not None else False


# ---------------------------------------------------------------------------
# Diagnostic confidence model
# ---------------------------------------------------------------------------

def compute_confidence_revision(
    df: pd.DataFrame,
    *,
    shot_id: int,
    signal_json: Dict[str, Any],
    meta: Dict[str, Any],
    positive_threshold: float,
    negative_threshold: float,
    low_confidence_threshold: float,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    out = df.copy()

    # Preserve raw margin and raw state.
    out["m_edge_raw"] = numeric_series(out, "m_edge")
    if "m_edge_state" in out.columns:
        out["m_edge_raw_state"] = out["m_edge_state"].astype(str)
    else:
        out["m_edge_raw_state"] = np.where(
            out["m_edge_raw"] >= positive_threshold,
            "positive_boundary_margin",
            np.where(out["m_edge_raw"] <= negative_threshold, "negative_leakage_margin", "boundary_ambiguous_margin"),
        )

    # Determine whole-shot diagnostic availability using metadata / signal JSON.
    has_nbi_global = any_metadata_or_signal(
        meta, signal_json,
        "has__summary-power_nbi",
        ["summary_power_nbi", "summary-power_nbi"],
        fallback="nbi_proxy" in out.columns,
    )
    has_ip_global = any_metadata_or_signal(
        meta, signal_json,
        "has__summary-ip",
        ["summary_ip", "summary-ip"],
        fallback=True,
    )
    has_density_global = any_metadata_or_signal(
        meta, signal_json,
        "has__interferometer-n_e_line",
        ["interferometer_n_e_line", "interferometer-n_e_line"],
        fallback="density_proxy" in out.columns,
    )
    has_dalpha_global = any_metadata_or_signal(
        meta, signal_json,
        "has__spectrometer_visible-filter_spectrometer_dalpha_voltage",
        ["dalpha_voltage", "spectrometer_visible-filter_spectrometer_dalpha_voltage"],
        fallback="dalpha_proxy" in out.columns,
    )
    has_softx_lower_global = any_metadata_or_signal(
        meta, signal_json,
        "has__soft_x_rays-horizontal_cam_lower",
        ["soft_x_lower", "soft_x_rays-horizontal_cam_lower"],
        fallback="softx_lower_proxy" in out.columns,
    )
    has_softx_upper_global = any_metadata_or_signal(
        meta, signal_json,
        "has__soft_x_rays-horizontal_cam_upper",
        ["soft_x_upper", "soft_x_rays-horizontal_cam_upper"],
        fallback="softx_upper_proxy" in out.columns,
    )
    has_te_global = any_metadata_or_signal(
        meta, signal_json,
        "has__thomson_scattering-t_e",
        ["thomson_t_e", "thomson_scattering-t_e"],
        fallback="te_profile_gradient_proxy" in out.columns,
    )
    has_ne_global = any_metadata_or_signal(
        meta, signal_json,
        "has__thomson_scattering-n_e",
        ["thomson_n_e", "thomson_scattering-n_e"],
        fallback="ne_profile_gradient_proxy" in out.columns,
    )

    # Time-dependent finite masks.
    nbi_finite = finite_score(out, "nbi_proxy") if has_nbi_global else pd.Series(0.0, index=out.index)
    ip_finite = pd.Series(1.0 if has_ip_global else 0.0, index=out.index)
    density_finite = finite_score(out, "density_proxy") if has_density_global else pd.Series(0.0, index=out.index)
    density_support_finite = finite_score(out, "density_support")

    dalpha_finite = finite_score(out, "dalpha_proxy") if has_dalpha_global else pd.Series(0.0, index=out.index)
    softx_lower_finite = finite_score(out, "softx_lower_proxy") if has_softx_lower_global else pd.Series(0.0, index=out.index)
    softx_upper_finite = finite_score(out, "softx_upper_proxy") if has_softx_upper_global else pd.Series(0.0, index=out.index)

    te_grad_finite = finite_score(out, "te_profile_gradient_proxy") if has_te_global else pd.Series(0.0, index=out.index)
    ne_grad_finite = finite_score(out, "ne_profile_gradient_proxy") if has_ne_global else pd.Series(0.0, index=out.index)
    s_transport_finite = finite_score(out, "S_transport")

    geometry_cols = [
        "q95_proxy",
        "elongation_proxy",
        "triangularity_upper_proxy",
        "triangularity_lower_proxy",
        "minor_radius_proxy",
        "geometry_stability",
    ]
    geometry_scores = [finite_score(out, c) for c in geometry_cols if c in out.columns]
    if geometry_scores:
        geometry_stack = np.vstack([s.to_numpy(dtype=float) for s in geometry_scores])
        q_geometry = pd.Series(np.nanmean(geometry_stack, axis=0), index=out.index)
    else:
        q_geometry = pd.Series(0.0, index=out.index)

    missingness = numeric_series(out, "missingness_pressure", default=1.0).fillna(1.0).clip(0.0, 1.0)
    q_missing = 1.0 - missingness

    # Confidence groups from the plan.
    out["Q_power"] = clip01(0.70 * nbi_finite + 0.30 * ip_finite)
    out["Q_density"] = clip01(0.60 * density_finite + 0.40 * density_support_finite)
    out["Q_edge"] = clip01(0.50 * dalpha_finite + 0.25 * softx_lower_finite + 0.25 * softx_upper_finite)
    out["Q_profile"] = clip01(0.35 * te_grad_finite + 0.35 * ne_grad_finite + 0.30 * s_transport_finite)
    out["Q_geometry"] = clip01(q_geometry.fillna(0.0))
    out["Q_missing"] = clip01(q_missing)

    out["Q_diag"] = clip01(
        0.20 * out["Q_power"]
        + 0.15 * out["Q_density"]
        + 0.25 * out["Q_edge"]
        + 0.25 * out["Q_profile"]
        + 0.10 * out["Q_geometry"]
        + 0.05 * out["Q_missing"]
    )

    # Critical missing terms. These are row-level because a signal may be globally present
    # but unavailable at a given time point after interpolation/alignment.
    missing_nbi = (1.0 - nbi_finite).clip(0.0, 1.0)
    missing_dalpha = (1.0 - dalpha_finite).clip(0.0, 1.0)
    missing_te = (1.0 - te_grad_finite).clip(0.0, 1.0)
    missing_ne = (1.0 - ne_grad_finite).clip(0.0, 1.0)
    missing_softx_pair = (1.0 - ((softx_lower_finite + softx_upper_finite) >= 2.0).astype(float)).clip(0.0, 1.0)
    missing_transport = (1.0 - s_transport_finite).clip(0.0, 1.0)

    out["P_missing_critical"] = clip01(
        0.20 * missing_nbi
        + 0.25 * missing_dalpha
        + 0.15 * missing_te
        + 0.15 * missing_ne
        + 0.10 * missing_softx_pair
        + 0.10 * missing_transport
        + 0.05 * missingness
    )

    out["Q_capacity"] = clip01(
        0.40 * out["Q_edge"]
        + 0.25 * out["Q_density"]
        + 0.20 * out["Q_geometry"]
        + 0.15 * out["Q_profile"]
    )
    out["Q_fragmentation"] = clip01(
        0.40 * out["Q_power"]
        + 0.40 * out["Q_profile"]
        + 0.20 * out["Q_missing"]
    )

    capacity = numeric_series(out, "C_edge_capacity", default=0.0).fillna(0.0)
    fragmentation = numeric_series(out, "F_route_fragmentation", default=0.0).fillna(0.0)

    out["m_edge_conf_simple"] = out["m_edge_raw"].fillna(0.0) * out["Q_diag"]
    out["m_edge_conf"] = (
        capacity * out["Q_capacity"]
        - fragmentation * out["Q_fragmentation"]
        - out["P_missing_critical"]
    )
    out["delta_conf_minus_raw"] = out["m_edge_conf"] - out["m_edge_raw"]

    # Missing critical flags for auditability.
    flag_names = [
        ("missing_NBI", missing_nbi),
        ("missing_Dalpha", missing_dalpha),
        ("missing_Te", missing_te),
        ("missing_ne", missing_ne),
        ("missing_softX_pair", missing_softx_pair),
        ("missing_transport", missing_transport),
    ]
    flags: List[str] = []
    for i in range(len(out)):
        row_flags = [name for name, arr in flag_names if float(arr.iloc[i]) >= 0.5]
        if float(missingness.iloc[i]) >= 0.5:
            row_flags.append("high_missingness_pressure")
        flags.append(";".join(row_flags) if row_flags else "none")
    out["missing_critical_flags"] = flags

    # Confidence flags.
    out["is_low_confidence"] = out["Q_diag"] < low_confidence_threshold
    out["confidence_flag"] = np.select(
        [
            out["Q_diag"] >= 0.70,
            out["Q_diag"] >= 0.50,
            out["Q_diag"] >= low_confidence_threshold,
            out["Q_diag"] < low_confidence_threshold,
        ],
        [
            "high_confidence",
            "moderate_confidence",
            "low_confidence",
            "low_confidence_uninterpretable",
        ],
        default="low_confidence_uninterpretable",
    )

    # Confidence-adjusted states. Low confidence overrides margin states.
    out["m_edge_conf_state"] = np.select(
        [
            out["Q_diag"] < low_confidence_threshold,
            out["m_edge_conf"] >= positive_threshold,
            out["m_edge_conf"] <= negative_threshold,
        ],
        [
            "low_confidence_uninterpretable",
            "confidence_positive_boundary_margin",
            "confidence_negative_leakage_margin",
        ],
        default="confidence_boundary_ambiguous_margin",
    )

    out["is_confidence_positive"] = out["m_edge_conf_state"].eq("confidence_positive_boundary_margin")
    out["is_confidence_negative"] = out["m_edge_conf_state"].eq("confidence_negative_leakage_margin")

    summary = summarize_revision(out, shot_id=shot_id, meta=meta, signal_json=signal_json)
    summary["global_diagnostic_availability"] = {
        "has_nbi_global": has_nbi_global,
        "has_ip_global": has_ip_global,
        "has_density_global": has_density_global,
        "has_dalpha_global": has_dalpha_global,
        "has_softx_lower_global": has_softx_lower_global,
        "has_softx_upper_global": has_softx_upper_global,
        "has_te_global": has_te_global,
        "has_ne_global": has_ne_global,
    }
    return out, summary


def summarize_revision(
    df: pd.DataFrame,
    *,
    shot_id: int,
    meta: Dict[str, Any],
    signal_json: Dict[str, Any],
) -> Dict[str, Any]:
    total = len(df)
    raw_state = df.get("m_edge_raw_state", pd.Series([""] * total)).astype(str)
    conf_state = df.get("m_edge_conf_state", pd.Series([""] * total)).astype(str)

    raw_pos = int(raw_state.eq("positive_boundary_margin").sum())
    raw_neg = int(raw_state.eq("negative_leakage_margin").sum())
    raw_amb = int(raw_state.eq("boundary_ambiguous_margin").sum())
    raw_insuf = int(raw_state.eq("insufficient_data").sum())

    conf_pos = int(conf_state.eq("confidence_positive_boundary_margin").sum())
    conf_neg = int(conf_state.eq("confidence_negative_leakage_margin").sum())
    conf_amb = int(conf_state.eq("confidence_boundary_ambiguous_margin").sum())
    conf_low = int(conf_state.eq("low_confidence_uninterpretable").sum())

    summary: Dict[str, Any] = {
        "shot_id": int(shot_id),
        "rows": int(total),
        "candidate_class": meta.get("candidate_class", ""),
        "candidate_score": meta.get("candidate_score", ""),
        "campaign": meta.get("campaign", ""),
        "split_membership": meta.get("split_membership", ""),
        "core_required_present": meta.get("core_required_present", ""),
        "profile_preferred_present": meta.get("profile_preferred_present", ""),
        "edge_activity_present": meta.get("edge_activity_present", ""),
        "supporting_present": meta.get("supporting_present", ""),
        "missing_core_required": meta.get("missing_core_required", ""),
        "missing_profile_preferred": meta.get("missing_profile_preferred", ""),
        "missing_edge_activity": meta.get("missing_edge_activity", ""),
        "loaded_signal_arrays": len(signal_json.get("loaded_labels", []) or []),
        "failed_signal_arrays": len(signal_json.get("failed_labels", {}) or {}),
        "raw_positive_count": raw_pos,
        "raw_negative_count": raw_neg,
        "raw_ambiguous_count": raw_amb,
        "raw_insufficient_count": raw_insuf,
        "raw_positive_fraction": fraction(raw_pos, total),
        "raw_negative_fraction": fraction(raw_neg, total),
        "raw_ambiguous_fraction": fraction(raw_amb, total),
        "raw_insufficient_fraction": fraction(raw_insuf, total),
        "conf_positive_count": conf_pos,
        "conf_negative_count": conf_neg,
        "conf_ambiguous_count": conf_amb,
        "conf_low_confidence_count": conf_low,
        "conf_positive_fraction": fraction(conf_pos, total),
        "conf_negative_fraction": fraction(conf_neg, total),
        "conf_ambiguous_fraction": fraction(conf_amb, total),
        "conf_low_confidence_fraction": fraction(conf_low, total),
    }

    for col in [
        "m_edge_raw",
        "m_edge_conf",
        "m_edge_conf_simple",
        "delta_conf_minus_raw",
        "Q_power",
        "Q_density",
        "Q_edge",
        "Q_profile",
        "Q_geometry",
        "Q_missing",
        "Q_diag",
        "Q_capacity",
        "Q_fragmentation",
        "P_missing_critical",
    ]:
        if col in df.columns:
            stats = finite_stats(df[col])
            for k, v in stats.items():
                summary[f"{col}_{k}"] = v

    # Confidence structural score for panel ranking.
    conf_pos_frac = float(summary.get("conf_positive_fraction", 0.0) or 0.0)
    conf_neg_frac = float(summary.get("conf_negative_fraction", 0.0) or 0.0)
    low_frac = float(summary.get("conf_low_confidence_fraction", 0.0) or 0.0)
    q_med = float(summary.get("Q_diag_median", 0.0) or 0.0)
    pcrit_med = float(summary.get("P_missing_critical_median", 0.0) or 0.0)
    m_med = max(float(summary.get("m_edge_conf_median", 0.0) or 0.0), 0.0)
    m_max = max(float(summary.get("m_edge_conf_max", 0.0) or 0.0), 0.0)

    summary["confidence_structural_score"] = (
        20.0 * conf_pos_frac
        + 5.0 * m_med
        + 2.0 * m_max
        + 3.0 * q_med
        - 15.0 * conf_neg_frac
        - 10.0 * low_frac
        - 2.0 * pcrit_med
    )

    return summary


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def write_shot_report(path: Path, summary: Dict[str, Any]) -> None:
    keys = [
        "shot_id",
        "candidate_class",
        "candidate_score",
        "rows",
        "raw_positive_fraction",
        "conf_positive_fraction",
        "raw_negative_fraction",
        "conf_negative_fraction",
        "conf_low_confidence_fraction",
        "m_edge_raw_median",
        "m_edge_conf_median",
        "m_edge_raw_max",
        "m_edge_conf_max",
        "Q_diag_median",
        "P_missing_critical_median",
        "confidence_structural_score",
    ]

    summary_df = pd.DataFrame([{k: summary.get(k, "") for k in keys}])

    availability = summary.get("global_diagnostic_availability", {})
    availability_df = pd.DataFrame([availability]) if availability else pd.DataFrame()

    md = []
    md.append(f"# TokaMark m_edge Diagnostic-Confidence Revision — Shot {summary.get('shot_id')}")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Preserve raw `m_edge(t)` while adding diagnostic confidence and a conservative confidence-weighted margin.")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append(df_to_markdown(summary_df, index=False))
    md.append("")
    md.append("## Global diagnostic availability")
    md.append("")
    md.append(df_to_markdown(availability_df, index=False) if not availability_df.empty else "_No diagnostic availability metadata._")
    md.append("")
    md.append("## Bounded interpretation")
    md.append("")
    md.append("This output is not physical H-mode validation. It tests whether the raw structural margin remains interpretable after missing and incomplete diagnostics are penalized.")
    md.append("")
    path.write_text("\n".join(md), encoding="utf-8")


def write_panel_report(path: Path, panel_df: pd.DataFrame, decision: Dict[str, Any], shots: List[int]) -> None:
    display_cols = [
        "confidence_panel_rank",
        "shot_id",
        "candidate_class",
        "confidence_structural_score",
        "raw_positive_fraction",
        "conf_positive_fraction",
        "raw_negative_fraction",
        "conf_negative_fraction",
        "conf_low_confidence_fraction",
        "m_edge_raw_median",
        "m_edge_conf_median",
        "Q_diag_median",
        "P_missing_critical_median",
        "missing_core_required",
        "missing_profile_preferred",
        "missing_edge_activity",
    ]
    display_cols = [c for c in display_cols if c in panel_df.columns]

    md = []
    md.append("# TokaMark Diagnostic-Confidence Panel Comparison")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Retest the same five-shot panel after adding diagnostic confidence to the raw v0.1 `m_edge(t)` margin.")
    md.append("")
    md.append("## Panel")
    md.append("")
    md.append("```text")
    for shot in shots:
        md.append(str(shot))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("")
    md.append("```text")
    md.append(f"decision: {decision.get('decision')}")
    for reason in decision.get("reasons", []):
        md.append(f"- {reason}")
    md.append("```")
    md.append("")
    md.append("## Confidence-adjusted ranking")
    md.append("")
    md.append(df_to_markdown(panel_df[display_cols], index=False))
    md.append("")
    md.append("## Bounded interpretation")
    md.append("")
    md.append("This panel does not validate H-mode physically. It tests whether the confidence correction preserves the stronger structure of shot 12063 while suppressing incomplete inflated cases such as 11776 and 11768.")
    md.append("")
    md.append("## Next document")
    md.append("")
    md.append("```text")
    md.append("docs/")
    md.append("  25_TOKAMARK_M_EDGE_CONFIDENCE_REVISION_RESULTS.md")
    md.append("```")
    md.append("")
    path.write_text("\n".join(md), encoding="utf-8")


def decide_panel(panel_df: pd.DataFrame, reference_shot: int = 12063) -> Dict[str, Any]:
    if panel_df.empty:
        return {"decision": "inconclusive_empty_panel", "reasons": []}

    if reference_shot not in set(panel_df["shot_id"].astype(int)):
        return {"decision": "inconclusive_missing_reference", "reasons": []}

    ref = panel_df[panel_df["shot_id"].astype(int).eq(int(reference_shot))].iloc[0]
    comps = panel_df[~panel_df["shot_id"].astype(int).eq(int(reference_shot))]

    reasons: List[str] = []
    ref_rank = int(ref.get("confidence_panel_rank", 999))
    ref_conf_pos = float(ref.get("conf_positive_fraction", 0.0) or 0.0)
    ref_q = float(ref.get("Q_diag_median", 0.0) or 0.0)
    ref_score = float(ref.get("confidence_structural_score", 0.0) or 0.0)

    max_comp_pos = float(comps["conf_positive_fraction"].fillna(0).max()) if not comps.empty else 0.0
    max_comp_score = float(comps["confidence_structural_score"].fillna(-999).max()) if not comps.empty else -999.0

    # Specific incomplete-shot checks.
    incomplete = panel_df[panel_df["shot_id"].astype(int).isin([11776, 11768])]
    incomplete_suppressed = True
    if not incomplete.empty:
        # Require incomplete shots to have either low confidence or reduced confidence-positive fraction.
        incomplete_suppressed = bool(
            ((incomplete["conf_low_confidence_fraction"].fillna(0) >= 0.25)
             | (incomplete["conf_positive_fraction"].fillna(0) < incomplete["raw_positive_fraction"].fillna(0))).all()
        )

    if ref_rank == 1:
        reasons.append("reference_has_top_confidence_adjusted_rank")
    if ref_conf_pos >= max_comp_pos:
        reasons.append("reference_has_highest_or_tied_confidence_positive_fraction")
    if ref_score >= max_comp_score:
        reasons.append("reference_has_highest_confidence_structural_score")
    if ref_q >= 0.40:
        reasons.append("reference_remains_interpretable_after_confidence_correction")
    if incomplete_suppressed:
        reasons.append("incomplete_inflated_cases_are_confidence_limited_or_suppressed")
    else:
        reasons.append("incomplete_inflated_cases_not_sufficiently_suppressed")

    if ref_rank == 1 and incomplete_suppressed and ref_q >= 0.40:
        decision = "confidence_revision_passes_initial_panel"
    elif ref_rank <= 2 and incomplete_suppressed:
        decision = "confidence_revision_partially_passes_initial_panel"
    elif not incomplete_suppressed:
        decision = "confidence_revision_fails_to_suppress_incomplete_cases"
    else:
        decision = "confidence_revision_inconclusive"

    return {
        "decision": decision,
        "reasons": reasons,
        "reference_shot": int(reference_shot),
        "reference_confidence_rank": ref_rank,
        "reference_confidence_positive_fraction": ref_conf_pos,
        "max_comparison_confidence_positive_fraction": max_comp_pos,
        "reference_confidence_structural_score": ref_score,
        "max_comparison_confidence_structural_score": max_comp_score,
        "reference_Q_diag_median": ref_q,
        "incomplete_cases_suppressed": incomplete_suppressed,
    }


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def process_shot(
    *,
    shot_id: int,
    out_dir: Path,
    metadata: pd.DataFrame,
    positive_threshold: float,
    negative_threshold: float,
    low_confidence_threshold: float,
) -> Dict[str, Any]:
    input_csv = out_dir / f"tokamark_shot_{shot_id}_m_edge_t_probe.csv"
    signal_json_path = out_dir / f"tokamark_shot_{shot_id}_signal_probe.json"

    if not input_csv.exists():
        raise FileNotFoundError(f"Missing m_edge input CSV for shot {shot_id}: {input_csv}")

    df = pd.read_csv(input_csv)
    signal_json = read_json(signal_json_path)
    meta = metadata_row(metadata, shot_id)

    revised, summary = compute_confidence_revision(
        df,
        shot_id=shot_id,
        signal_json=signal_json,
        meta=meta,
        positive_threshold=positive_threshold,
        negative_threshold=negative_threshold,
        low_confidence_threshold=low_confidence_threshold,
    )

    csv_out = out_dir / f"tokamark_shot_{shot_id}_m_edge_confidence_revision.csv"
    json_out = out_dir / f"tokamark_shot_{shot_id}_m_edge_confidence_revision.json"
    md_out = out_dir / f"tokamark_shot_{shot_id}_m_edge_confidence_revision.md"

    revised.to_csv(csv_out, index=False)
    write_json(json_out, {
        "component": "tokamark_m_edge_confidence_revision.py",
        "shot_id": int(shot_id),
        "input_csv": str(input_csv),
        "signal_json": str(signal_json_path),
        "summary": summary,
    })
    write_shot_report(md_out, summary)

    summary["output_csv"] = str(csv_out)
    summary["output_json"] = str(json_out)
    summary["output_md"] = str(md_out)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply diagnostic-confidence correction to TokaMark m_edge(t) outputs.")
    parser.add_argument("--shot-id", type=int, default=None, help="Single shot ID.")
    parser.add_argument("--shots", nargs="*", type=int, default=None, help="Shot IDs for panel mode.")
    parser.add_argument("--reference-shot", type=int, default=12063, help="Reference shot for panel decision.")
    parser.add_argument("--out-dir", default="outputs/reports", help="Output/report directory.")
    parser.add_argument("--metadata-candidates", default="outputs/reports/tokamark_positive_corridor_metadata_candidates.csv", help="Metadata candidate CSV.")
    parser.add_argument("--positive-threshold", type=float, default=0.20, help="Confidence-positive threshold.")
    parser.add_argument("--negative-threshold", type=float, default=-0.20, help="Confidence-negative threshold.")
    parser.add_argument("--low-confidence-threshold", type=float, default=0.40, help="Low-confidence threshold.")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.shot_id is not None:
        shots = [int(args.shot_id)]
    elif args.shots:
        shots = [int(s) for s in args.shots]
    else:
        shots = DEFAULT_PANEL[:]

    # Preserve reference first in default/custom panel when present.
    if args.reference_shot in shots:
        shots = [args.reference_shot] + [s for s in shots if s != args.reference_shot]

    metadata = load_metadata(Path(args.metadata_candidates))

    summaries: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []

    for shot in shots:
        print(f"[shot {shot}] confidence revision...", flush=True)
        try:
            summaries.append(process_shot(
                shot_id=shot,
                out_dir=out_dir,
                metadata=metadata,
                positive_threshold=args.positive_threshold,
                negative_threshold=args.negative_threshold,
                low_confidence_threshold=args.low_confidence_threshold,
            ))
        except Exception as exc:
            failures.append({"shot_id": int(shot), "error": repr(exc)})
            print(f"[shot {shot}] FAILED: {exc}", flush=True)

    if not summaries:
        raise SystemExit(f"No shots processed. Failures: {failures}")

    panel_df = pd.DataFrame(summaries)
    panel_df["confidence_panel_rank"] = panel_df["confidence_structural_score"].rank(ascending=False, method="min").astype(int)
    panel_df = panel_df.sort_values(["confidence_panel_rank", "shot_id"])

    panel_csv = out_dir / "tokamark_confidence_panel_comparison.csv"
    panel_json = out_dir / "tokamark_confidence_panel_comparison.json"
    panel_md = out_dir / "tokamark_confidence_panel_comparison.md"

    decision = decide_panel(panel_df, reference_shot=args.reference_shot)

    panel_df.to_csv(panel_csv, index=False)
    write_json(panel_json, {
        "component": "tokamark_m_edge_confidence_revision.py",
        "shots": shots,
        "reference_shot": int(args.reference_shot),
        "decision": decision,
        "failures": failures,
        "panel": panel_df.to_dict(orient="records"),
    })
    write_panel_report(panel_md, panel_df, decision, shots)

    print()
    print("Diagnostic-confidence revision complete.")
    print(f"Shots requested: {shots}")
    print(f"Processed: {len(summaries)}")
    print(f"Failures: {len(failures)}")
    print(f"Decision: {decision.get('decision')}")
    print(f"Panel CSV:  {panel_csv}")
    print(f"Panel JSON: {panel_json}")
    print(f"Panel MD:   {panel_md}")
    print()
    print("Confidence-adjusted ranking:")
    for _, row in panel_df.iterrows():
        print(
            f"  rank {int(row['confidence_panel_rank'])} | "
            f"shot {int(row['shot_id'])} | "
            f"score {float(row['confidence_structural_score']):.4f} | "
            f"conf+ {float(row['conf_positive_fraction']):.3f} | "
            f"low_conf {float(row['conf_low_confidence_fraction']):.3f} | "
            f"Q_diag_med {float(row['Q_diag_median']) if pd.notna(row['Q_diag_median']) else float('nan'):.3f} | "
            f"{row.get('candidate_class', '')}"
        )

    if failures:
        print()
        print("Failures:")
        for f in failures:
            print(f"  shot {f['shot_id']}: {f['error']}")


if __name__ == "__main__":
    main()
