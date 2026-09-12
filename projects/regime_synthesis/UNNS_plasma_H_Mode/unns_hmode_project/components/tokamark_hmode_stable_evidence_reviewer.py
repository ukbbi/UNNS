#!/usr/bin/env python3
"""
tokamark_hmode_stable_evidence_reviewer.py

UNNS-H Mode Project
Focused evidence-review template for excluded H_MODE_STABLE candidate windows.

Follows:
    docs/32_H_MODE_STABLE_EVIDENCE_RECOVERY_PLAN.md

This script does not auto-accept H_MODE_STABLE labels and does not validate H-mode.
It summarizes independent physical evidence fields and keeps UNNS values as audit-only.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

OUTPUT_PREFIX = "tokamark_hmode_stable_evidence_review"

REVIEW_COLUMNS = [
    "shot_id", "window_id", "t_start", "t_end", "window_duration",
    "source_label_file", "preview_file", "trace_file", "has_preview", "has_trace",
    "dalpha_evidence_score", "profile_evidence_score", "softx_evidence_score",
    "power_density_context_score", "external_reference_score", "H_evidence_score",
    "dalpha_notes", "profile_notes", "softx_notes", "power_density_notes", "external_reference_notes",
    "physical_review_decision", "accepted_as_hmode_stable", "hardening_level",
    "excluded_from_validation", "exclusion_reason", "reviewer_notes",
    "dalpha_window_median", "dalpha_pre_median", "dalpha_post_median",
    "dalpha_pre_to_window_delta", "dalpha_window_std",
    "profile_window_median", "profile_pre_median", "profile_post_median", "profile_pre_to_window_delta",
    "softx_window_median", "softx_pre_median", "softx_post_median", "softx_pre_to_window_delta",
    "nbi_window_median", "density_window_median",
    "physical_marker_overlap_count", "overlapping_physical_markers",
    "UNNS_AUDIT_m_edge_conf_median", "UNNS_AUDIT_conf_positive_fraction",
    "UNNS_AUDIT_conf_negative_fraction", "UNNS_AUDIT_Q_diag_median", "UNNS_AUDIT_P_missing_critical_median",
]

ALLOWED_DECISIONS = [
    "ACCEPT_H_MODE_STABLE", "DOWNGRADE_TO_AMBIGUOUS", "REJECT",
    "NEEDS_EXTERNAL_REFERENCE", "KEEP_EXCLUDED",
]

ALLOWED_HARDENING_LEVELS = [
    "0_PROVISIONAL", "1_PLAUSIBLE", "2_SUPPORTED", "3_EXTERNALLY_ANCHORED",
]


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
        return None if not np.isfinite(obj) else float(obj)
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
        out.extend(line(r) for r in rows)
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
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def fnum(value: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if value is None or value == "":
            return default
        v = float(value)
        return v if np.isfinite(v) else default
    except Exception:
        return default


def numeric(df: pd.DataFrame, col: str) -> pd.Series:
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    return pd.Series([np.nan] * len(df), index=df.index, dtype=float)


def read_csv(path: Path, required: bool = False) -> pd.DataFrame:
    if not path.exists():
        if required:
            raise FileNotFoundError(f"Missing CSV: {path}")
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        if required:
            raise
        return pd.DataFrame()


def finite_stats(values: pd.Series) -> Dict[str, Any]:
    arr = pd.to_numeric(values, errors="coerce").to_numpy(dtype=float)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return {"count": 0, "median": None, "mean": None, "std": None, "min": None, "max": None}
    return {
        "count": int(finite.size),
        "median": float(np.nanmedian(finite)),
        "mean": float(np.nanmean(finite)),
        "std": float(np.nanstd(finite)),
        "min": float(np.nanmin(finite)),
        "max": float(np.nanmax(finite)),
    }


def robust_scale(values: pd.Series) -> float:
    x = pd.to_numeric(values, errors="coerce").to_numpy(dtype=float)
    x = x[np.isfinite(x)]
    if x.size == 0:
        return 1.0
    med = float(np.nanmedian(x))
    mad = float(np.nanmedian(np.abs(x - med)))
    if np.isfinite(mad) and mad > 1e-12:
        return float(1.4826 * mad)
    std = float(np.nanstd(x))
    return std if np.isfinite(std) and std > 1e-12 else 1.0


def window_slice(df: pd.DataFrame, start: float, end: float) -> pd.DataFrame:
    if df.empty or "time_s" not in df.columns:
        return pd.DataFrame()
    t = pd.to_numeric(df["time_s"], errors="coerce")
    return df[(t >= start) & (t <= end)].copy()


def interval_context(df: pd.DataFrame, start: float, end: float, flank: float) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return window_slice(df, start - flank, start), window_slice(df, start, end), window_slice(df, end, end + flank)


def choose_col(df: pd.DataFrame, candidates: Sequence[str]) -> Optional[str]:
    for col in candidates:
        if col in df.columns and pd.to_numeric(df[col], errors="coerce").notna().any():
            return col
    return None


def median_or_none(df: pd.DataFrame, col: Optional[str]) -> Optional[float]:
    if col is None or df.empty:
        return None
    return finite_stats(df[col])["median"]


def std_or_none(df: pd.DataFrame, col: Optional[str]) -> Optional[float]:
    if col is None or df.empty:
        return None
    return finite_stats(df[col])["std"]


def pre_window_delta(pre: pd.DataFrame, win: pd.DataFrame, col: Optional[str]) -> Optional[float]:
    if col is None or pre.empty or win.empty:
        return None
    pre_med = median_or_none(pre, col)
    win_med = median_or_none(win, col)
    if pre_med is None or win_med is None:
        return None
    return float(win_med - pre_med)


def overlap_fraction(a_start: float, a_end: float, b_start: float, b_end: float) -> float:
    lo = max(a_start, b_start)
    hi = min(a_end, b_end)
    if hi <= lo:
        return 0.0
    return float((hi - lo) / max(a_end - a_start, 1e-12))


def load_labels(path: Path) -> pd.DataFrame:
    df = read_csv(path, required=True)
    required = ["shot_id", "window_id", "label_type", "t_start", "t_end", "excluded_from_validation"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Hardened label file missing required columns: {missing}")
    out = df.copy()
    out["shot_id"] = pd.to_numeric(out["shot_id"], errors="coerce")
    out = out.dropna(subset=["shot_id"]).copy()
    out["shot_id"] = out["shot_id"].astype(int)
    out["window_id"] = out["window_id"].astype(str)
    out["label_type"] = out["label_type"].astype(str).str.upper()
    out["t_start"] = pd.to_numeric(out["t_start"], errors="coerce")
    out["t_end"] = pd.to_numeric(out["t_end"], errors="coerce")
    out["window_duration"] = out["t_end"] - out["t_start"]
    out["excluded_from_validation_bool"] = out["excluded_from_validation"].apply(as_bool)
    return out


def select_hmode_candidates(labels: pd.DataFrame, include_accepted: bool = False) -> pd.DataFrame:
    label_cols = [c for c in ["label_type", "hardened_label_type", "original_label_type"] if c in labels.columns]
    mask = pd.Series(False, index=labels.index)
    for col in label_cols:
        mask |= labels[col].astype(str).str.upper().eq("H_MODE_STABLE")
    if not include_accepted:
        mask &= labels["excluded_from_validation_bool"].astype(bool)
    return labels[mask].copy().sort_values(["shot_id", "t_start", "window_id"]).reset_index(drop=True)


def load_preview(out_dir: Path, shot_id: int) -> pd.DataFrame:
    p1 = out_dir / f"tokamark_physical_window_label_preview_shot_{shot_id}.csv"
    p2 = out_dir / f"tokamark_physical_window_preview_shot_{shot_id}.csv"
    df = read_csv(p1, required=False)
    if df.empty:
        df = read_csv(p2, required=False)
    if df.empty:
        return df
    if "time_s" not in df.columns:
        df["time_s"] = pd.to_numeric(df["time"], errors="coerce") if "time" in df.columns else np.arange(len(df), dtype=float)
    if "softx_combined_proxy" not in df.columns:
        lower = numeric(df, "softx_lower_proxy")
        upper = numeric(df, "softx_upper_proxy")
        if lower.notna().any() or upper.notna().any():
            df["softx_combined_proxy"] = np.nanmean(np.vstack([lower.to_numpy(float), upper.to_numpy(float)]), axis=0)
    if "profile_gradient_proxy" not in df.columns:
        te = numeric(df, "te_profile_gradient_proxy")
        ne = numeric(df, "ne_profile_gradient_proxy")
        if te.notna().any() or ne.notna().any():
            df["profile_gradient_proxy"] = np.nanmean(np.vstack([te.to_numpy(float), ne.to_numpy(float)]), axis=0)
    return df


def load_trace(out_dir: Path, shot_id: int) -> pd.DataFrame:
    path = out_dir / f"tokamark_shot_{shot_id}_m_edge_confidence_revision.csv"
    df = read_csv(path, required=False)
    if df.empty:
        return df
    if "time_s" not in df.columns:
        df["time_s"] = pd.to_numeric(df["time"], errors="coerce") if "time" in df.columns else np.arange(len(df), dtype=float)
    return df


def load_markers(path: Path) -> pd.DataFrame:
    df = read_csv(path, required=False)
    if df.empty:
        return df
    out = df.copy()
    if "shot_id" in out.columns:
        out["shot_id"] = pd.to_numeric(out["shot_id"], errors="coerce").astype("Int64")
    for col in ["t_start", "t_end", "center_time", "score_max"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def overlapping_markers(markers: pd.DataFrame, shot_id: int, start: float, end: float) -> Tuple[int, str]:
    if markers.empty:
        return 0, ""
    required = {"shot_id", "marker_family", "marker_type", "t_start", "t_end"}
    if not required.issubset(set(markers.columns)):
        return 0, ""
    m = markers[(markers["shot_id"].astype("Int64") == int(shot_id)) & (markers["marker_family"].astype(str).eq("PHYSICAL"))]
    texts: List[str] = []
    for _, row in m.iterrows():
        ms = fnum(row.get("t_start"))
        me = fnum(row.get("t_end"))
        if ms is None or me is None:
            continue
        if overlap_fraction(start, end, ms, me) > 0 or overlap_fraction(ms, me, start, end) > 0:
            score = fnum(row.get("score_max"), None)
            score_txt = "" if score is None else f"{score:.6g}"
            texts.append(f"{row.get('marker_type')}@[{ms:.6g},{me:.6g}] src={row.get('source_column','')} score={score_txt}")
    return len(texts), "; ".join(texts)


def score_delta(delta: Optional[float], scale: float, positive_is_support: bool = True) -> int:
    if delta is None or not np.isfinite(delta):
        return 0
    signed = delta if positive_is_support else -delta
    if signed > 1.0 * scale:
        return 2
    if signed > 0.25 * scale:
        return 1
    return 0


def score_stability(std_value: Optional[float], scale: float) -> int:
    if std_value is None or not np.isfinite(std_value):
        return 0
    if std_value <= 0.5 * scale:
        return 2
    if std_value <= 1.0 * scale:
        return 1
    return 0


def summarize_physical_evidence(preview: pd.DataFrame, trace: pd.DataFrame, shot_id: int, start: float, end: float, markers: pd.DataFrame, flank: float) -> Dict[str, Any]:
    df = preview.copy() if not preview.empty else trace.copy()
    if df.empty:
        return {
            "dalpha_evidence_score": 0, "profile_evidence_score": 0, "softx_evidence_score": 0,
            "power_density_context_score": 0, "external_reference_score": 0, "H_evidence_score": 0,
            "dalpha_notes": "No preview/trace data available for physical diagnostic review.",
            "profile_notes": "No preview/trace data available.",
            "softx_notes": "No preview/trace data available.",
            "power_density_notes": "No preview/trace data available.",
            "external_reference_notes": "No external reference supplied.",
        }
    pre, win, post = interval_context(df, start, end, flank=flank)
    dalpha_col = choose_col(df, ["dalpha_proxy", "spectrometer_visible-filter_spectrometer_dalpha_voltage", "D_alpha"])
    profile_col = choose_col(df, ["profile_gradient_proxy", "te_profile_gradient_proxy", "ne_profile_gradient_proxy"])
    softx_col = choose_col(df, ["softx_combined_proxy", "softx_lower_proxy", "softx_upper_proxy"])
    nbi_col = choose_col(df, ["nbi_proxy", "summary_power_nbi", "power_nbi"])
    density_col = choose_col(df, ["density_proxy", "interferometer_n_e_line", "n_e_line"])

    dalpha_delta = pre_window_delta(pre, win, dalpha_col)
    dalpha_std = std_or_none(win, dalpha_col)
    dalpha_scale = robust_scale(df[dalpha_col]) if dalpha_col else 1.0
    dalpha_score = max(score_delta(dalpha_delta, dalpha_scale, False), score_delta(dalpha_delta, dalpha_scale, True), score_stability(dalpha_std, dalpha_scale)) if dalpha_col else 0

    profile_delta = pre_window_delta(pre, win, profile_col)
    profile_scale = robust_scale(df[profile_col]) if profile_col else 1.0
    profile_score = score_delta(profile_delta, profile_scale, True) if profile_col else 0

    softx_delta = pre_window_delta(pre, win, softx_col)
    softx_std = std_or_none(win, softx_col)
    softx_scale = robust_scale(df[softx_col]) if softx_col else 1.0
    softx_score = max(score_delta(softx_delta, softx_scale, True), score_stability(softx_std, softx_scale)) if softx_col else 0

    nbi_med = median_or_none(win, nbi_col)
    density_med = median_or_none(win, density_col)
    power_density_score = 2 if (nbi_med is not None and density_med is not None) else (1 if (nbi_med is not None or density_med is not None) else 0)
    external_score = 0
    marker_count, marker_text = overlapping_markers(markers, shot_id, start, end)

    audit_df = trace if not trace.empty else df
    audit_win = window_slice(audit_df, start, end)
    if not audit_win.empty:
        state = audit_win["m_edge_conf_state"].astype(str) if "m_edge_conf_state" in audit_win.columns else pd.Series([""] * len(audit_win))
        audit = {
            "UNNS_AUDIT_m_edge_conf_median": median_or_none(audit_win, "m_edge_conf"),
            "UNNS_AUDIT_conf_positive_fraction": float(state.eq("confidence_positive_boundary_margin").mean()),
            "UNNS_AUDIT_conf_negative_fraction": float(state.eq("confidence_negative_leakage_margin").mean()),
            "UNNS_AUDIT_Q_diag_median": median_or_none(audit_win, "Q_diag"),
            "UNNS_AUDIT_P_missing_critical_median": median_or_none(audit_win, "P_missing_critical"),
        }
    else:
        audit = {k: None for k in [
            "UNNS_AUDIT_m_edge_conf_median", "UNNS_AUDIT_conf_positive_fraction", "UNNS_AUDIT_conf_negative_fraction",
            "UNNS_AUDIT_Q_diag_median", "UNNS_AUDIT_P_missing_critical_median"]}

    return {
        "dalpha_evidence_score": int(dalpha_score),
        "profile_evidence_score": int(profile_score),
        "softx_evidence_score": int(softx_score),
        "power_density_context_score": int(power_density_score),
        "external_reference_score": int(external_score),
        "H_evidence_score": int(dalpha_score + profile_score + softx_score + power_density_score + external_score),
        "dalpha_notes": f"column={dalpha_col or 'MISSING'}; pre_median={median_or_none(pre, dalpha_col)}; window_median={median_or_none(win, dalpha_col)}; post_median={median_or_none(post, dalpha_col)}; pre_to_window_delta={dalpha_delta}; window_std={dalpha_std}. Reviewer must decide whether morphology supports post-transition stable H-mode behavior.",
        "profile_notes": f"column={profile_col or 'MISSING'}; pre_median={median_or_none(pre, profile_col)}; window_median={median_or_none(win, profile_col)}; post_median={median_or_none(post, profile_col)}; pre_to_window_delta={profile_delta}. Reviewer must confirm edge-gradient/pedestal-like support.",
        "softx_notes": f"column={softx_col or 'MISSING'}; pre_median={median_or_none(pre, softx_col)}; window_median={median_or_none(win, softx_col)}; post_median={median_or_none(post, softx_col)}; pre_to_window_delta={softx_delta}; window_std={softx_std}. Reviewer must confirm edge-activity consistency and absence of disruptive behavior.",
        "power_density_notes": f"nbi_column={nbi_col or 'MISSING'}; nbi_window_median={nbi_med}; density_column={density_col or 'MISSING'}; density_window_median={density_med}. Reviewer must decide whether power/density context is physically plausible.",
        "external_reference_notes": "No external L-H/H-mode timing supplied. Fill if published timing, shot log, or expert annotation is available.",
        "dalpha_window_median": median_or_none(win, dalpha_col), "dalpha_pre_median": median_or_none(pre, dalpha_col), "dalpha_post_median": median_or_none(post, dalpha_col), "dalpha_pre_to_window_delta": dalpha_delta, "dalpha_window_std": dalpha_std,
        "profile_window_median": median_or_none(win, profile_col), "profile_pre_median": median_or_none(pre, profile_col), "profile_post_median": median_or_none(post, profile_col), "profile_pre_to_window_delta": profile_delta,
        "softx_window_median": median_or_none(win, softx_col), "softx_pre_median": median_or_none(pre, softx_col), "softx_post_median": median_or_none(post, softx_col), "softx_pre_to_window_delta": softx_delta,
        "nbi_window_median": nbi_med, "density_window_median": density_med,
        "physical_marker_overlap_count": int(marker_count), "overlapping_physical_markers": marker_text,
        **audit,
    }


def suggested_decision(evidence_score: int) -> Tuple[str, bool, str, bool, str]:
    if evidence_score >= 6:
        return ("NEEDS_EXTERNAL_REFERENCE", False, "1_PLAUSIBLE", True, "Evidence score is suggestive, but external/manual confirmation is still required before validation inclusion.")
    if evidence_score >= 5:
        return ("NEEDS_EXTERNAL_REFERENCE", False, "1_PLAUSIBLE", True, "Minimum evidence score reached, but reviewer must confirm at least two independent physical families before inclusion.")
    return ("KEEP_EXCLUDED", False, "0_PROVISIONAL", True, "Insufficient independent physical evidence for H_MODE_STABLE acceptance in automatic review template.")


def build_review(candidates: pd.DataFrame, labels_path: Path, out_dir: Path, markers: pd.DataFrame, flank: float) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for _, cand in candidates.iterrows():
        shot_id = int(cand["shot_id"])
        window_id = str(cand["window_id"])
        start = fnum(cand.get("t_start"))
        end = fnum(cand.get("t_end"))
        preview_path = out_dir / f"tokamark_physical_window_label_preview_shot_{shot_id}.csv"
        if not preview_path.exists():
            preview_path = out_dir / f"tokamark_physical_window_preview_shot_{shot_id}.csv"
        trace_path = out_dir / f"tokamark_shot_{shot_id}_m_edge_confidence_revision.csv"
        preview = load_preview(out_dir, shot_id)
        trace = load_trace(out_dir, shot_id)
        if start is None or end is None or end <= start:
            evidence = {"dalpha_evidence_score": 0, "profile_evidence_score": 0, "softx_evidence_score": 0, "power_density_context_score": 0, "external_reference_score": 0, "H_evidence_score": 0, "dalpha_notes": "Invalid candidate time window.", "profile_notes": "Invalid candidate time window.", "softx_notes": "Invalid candidate time window.", "power_density_notes": "Invalid candidate time window.", "external_reference_notes": "No external reference supplied."}
        else:
            evidence = summarize_physical_evidence(preview, trace, shot_id, start, end, markers, flank)
        decision, accepted, hardening_level, excluded, exclusion_reason = suggested_decision(int(evidence.get("H_evidence_score", 0)))
        row: Dict[str, Any] = {
            "shot_id": shot_id, "window_id": window_id, "t_start": start, "t_end": end,
            "window_duration": fnum(cand.get("window_duration"), (end - start if start is not None and end is not None else None)),
            "source_label_file": str(labels_path), "preview_file": str(preview_path), "trace_file": str(trace_path),
            "has_preview": bool(not preview.empty), "has_trace": bool(not trace.empty),
            "physical_review_decision": decision, "accepted_as_hmode_stable": bool(accepted), "hardening_level": hardening_level,
            "excluded_from_validation": bool(excluded), "exclusion_reason": exclusion_reason,
            "reviewer_notes": "Manual review required. Do not accept this H_MODE_STABLE window from UNNS audit values. Inspect D-alpha, profile-gradient, soft-X, power/density context, and external timing if available.",
        }
        row.update(evidence)
        rows.append(row)
    review = pd.DataFrame(rows)
    for col in REVIEW_COLUMNS:
        if col not in review.columns:
            review[col] = ""
    return review[REVIEW_COLUMNS]


def summarize_review(review: pd.DataFrame) -> Dict[str, Any]:
    if review.empty:
        return {"candidate_count": 0, "shot_count": 0, "decision_counts": {}, "hardening_level_counts": {}, "accepted_count_initial": 0}
    return {
        "candidate_count": int(len(review)),
        "shot_count": int(review["shot_id"].nunique()),
        "decision_counts": {str(k): int(v) for k, v in review["physical_review_decision"].value_counts(dropna=False).to_dict().items()},
        "hardening_level_counts": {str(k): int(v) for k, v in review["hardening_level"].value_counts(dropna=False).to_dict().items()},
        "accepted_count_initial": int(review["accepted_as_hmode_stable"].astype(bool).sum()),
        "score_summary": {
            "min": float(pd.to_numeric(review["H_evidence_score"], errors="coerce").min()),
            "median": float(pd.to_numeric(review["H_evidence_score"], errors="coerce").median()),
            "max": float(pd.to_numeric(review["H_evidence_score"], errors="coerce").max()),
        },
    }


def write_review_md(path: Path, review: pd.DataFrame, summary: Dict[str, Any]) -> None:
    md: List[str] = []
    md.append("# TokaMark H-Mode-Stable Evidence Review")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Focused review of excluded `H_MODE_STABLE` candidate windows from the conservative hardened-label pass.")
    md.append("")
    md.append("This review supports:")
    md.append("")
    md.append("```text")
    md.append("docs/")
    md.append("  33_H_MODE_STABLE_EVIDENCE_RECOVERY_RESULTS.md")
    md.append("```")
    md.append("")
    md.append("## Non-circularity rule")
    md.append("")
    md.append("Do not accept an H-mode-stable label from `m_edge_conf(t)`. UNNS audit columns are shown only after the physical evidence fields.")
    md.append("")
    md.append("## Summary")
    md.append("")
    for key, value in summary.items():
        md.append(f"- **{key}**: `{value}`")
    md.append("")
    md.append("## Candidate review table")
    md.append("")
    cols = ["shot_id", "window_id", "t_start", "t_end", "dalpha_evidence_score", "profile_evidence_score", "softx_evidence_score", "power_density_context_score", "external_reference_score", "H_evidence_score", "physical_review_decision", "accepted_as_hmode_stable", "hardening_level", "excluded_from_validation", "UNNS_AUDIT_m_edge_conf_median", "UNNS_AUDIT_conf_positive_fraction", "UNNS_AUDIT_Q_diag_median"]
    cols = [c for c in cols if c in review.columns]
    md.append(df_to_markdown(review[cols], index=False) if not review.empty else "_No H_MODE_STABLE candidates found._")
    md.append("")
    md.append("## Per-window physical notes")
    md.append("")
    for _, row in review.iterrows():
        md.append(f"### {row['window_id']}")
        md.append("")
        md.append(f"- Shot: `{row['shot_id']}`")
        md.append(f"- Interval: `{row['t_start']}` to `{row['t_end']}`")
        md.append(f"- D-alpha: {row['dalpha_notes']}")
        md.append(f"- Profile: {row['profile_notes']}")
        md.append(f"- Soft-X: {row['softx_notes']}")
        md.append(f"- Power/density: {row['power_density_notes']}")
        md.append(f"- External reference: {row['external_reference_notes']}")
        md.append("")
        md.append("UNNS audit only — not used for physical label assignment:")
        md.append("")
        md.append("```text")
        md.append(f"m_edge_conf median: {row['UNNS_AUDIT_m_edge_conf_median']}")
        md.append(f"confidence-positive fraction: {row['UNNS_AUDIT_conf_positive_fraction']}")
        md.append(f"confidence-negative fraction: {row['UNNS_AUDIT_conf_negative_fraction']}")
        md.append(f"Q_diag median: {row['UNNS_AUDIT_Q_diag_median']}")
        md.append(f"P_missing_critical median: {row['UNNS_AUDIT_P_missing_critical_median']}")
        md.append("```")
        md.append("")
    md.append("## Manual next step")
    md.append("")
    md.append("Edit:")
    md.append("")
    md.append("```text")
    md.append("outputs/reports/tokamark_hmode_stable_evidence_review.csv")
    md.append("```")
    md.append("")
    md.append("Then create:")
    md.append("")
    md.append("```text")
    md.append("outputs/reports/tokamark_physical_window_labels_HARDENED_v0_2.csv")
    md.append("```")
    md.append("")
    path.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create focused review artifacts for excluded H_MODE_STABLE windows.")
    parser.add_argument("--labels", default="outputs/reports/tokamark_physical_window_labels_HARDENED_v0_1.csv", help="Hardened v0.1 label CSV.")
    parser.add_argument("--markers", default="outputs/reports/tokamark_physical_window_label_candidate_markers.csv", help="Candidate marker CSV.")
    parser.add_argument("--out-dir", default="outputs/reports", help="Output directory.")
    parser.add_argument("--flank", type=float, default=0.035, help="Seconds before/after H window for context summaries.")
    parser.add_argument("--include-accepted", action="store_true", help="Include already validation-eligible H_MODE_STABLE rows if any exist.")
    parser.add_argument("--prefix", default=OUTPUT_PREFIX, help="Output prefix.")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    labels_path = Path(args.labels)
    markers_path = Path(args.markers)
    labels = load_labels(labels_path)
    candidates = select_hmode_candidates(labels, include_accepted=args.include_accepted)
    markers = load_markers(markers_path)
    review = build_review(candidates, labels_path, out_dir, markers, flank=args.flank)
    summary = summarize_review(review)
    csv_out = out_dir / f"{args.prefix}.csv"
    md_out = out_dir / f"{args.prefix}.md"
    json_out = out_dir / f"{args.prefix}_summary.json"
    review.to_csv(csv_out, index=False)
    write_review_md(md_out, review, summary)
    write_json(json_out, {
        "component": "tokamark_hmode_stable_evidence_reviewer.py",
        "labels_input": str(labels_path),
        "markers_input": str(markers_path),
        "review_csv": str(csv_out),
        "review_md": str(md_out),
        "summary": summary,
        "allowed_decisions": ALLOWED_DECISIONS,
        "allowed_hardening_levels": ALLOWED_HARDENING_LEVELS,
        "next_hardened_file": str(out_dir / "tokamark_physical_window_labels_HARDENED_v0_2.csv"),
    })
    print("H_MODE_STABLE evidence review template complete.")
    print(f"Candidates: {len(review)}")
    print(f"Shots: {review['shot_id'].nunique() if not review.empty else 0}")
    print(f"Review CSV: {csv_out}")
    print(f"Review MD: {md_out}")
    print(f"Summary JSON: {json_out}")
    print()
    print("Manual next step:")
    print(f"  Edit {csv_out}")
    print()
    print("Then create:")
    print(f"  {out_dir / 'tokamark_physical_window_labels_HARDENED_v0_2.csv'}")
    print()
    print("Next report:")
    print("  docs/33_H_MODE_STABLE_EVIDENCE_RECOVERY_RESULTS.md")


if __name__ == "__main__":
    main()
