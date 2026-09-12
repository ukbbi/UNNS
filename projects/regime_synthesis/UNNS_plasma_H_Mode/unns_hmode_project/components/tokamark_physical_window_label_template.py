#!/usr/bin/env python3
"""
tokamark_physical_window_label_template.py

UNNS-H Mode Project
Physical-window labeling template generator.

Purpose
-------
Create the first independent physical-window labeling template after the v0.2
diagnostic-confidence method passed the moderate TokaMark panel.

This follows:

    docs/28_PHYSICAL_WINDOW_LABELING_REQUIREMENTS.md

Important
---------
This script DOES NOT validate H-mode.
This script DOES NOT assign final physical labels.
This script DOES NOT use m_edge_conf(t) to create physical labels.

It generates a manual-review template and diagnostic marker sheets so that
physical windows can be labeled independently of the UNNS score.

Default initial shot set
------------------------
The default first labeling set is:

    12046  top-ranked full-profile-edge candidate
    11941  top-ranked full-profile-edge candidate
    12055  top-ranked full-profile-edge candidate
    12007  top-ranked full-profile-edge candidate
    12017  top-ranked full-profile-edge candidate
    12063  original reference anchor
    11768  partial raw-positive but confidence-suppressed control
    11776  low-priority raw-positive but confidence-suppressed control

Run from project root
---------------------

    python components\tokamark_physical_window_label_template.py --out-dir outputs\reports

Custom shots:

    python components\tokamark_physical_window_label_template.py ^
      --shots 12046 11941 12055 12007 12017 12063 11768 11776 ^
      --out-dir outputs\reports

Outputs
-------

    outputs/reports/tokamark_physical_window_label_template.csv
    outputs/reports/tokamark_physical_window_label_candidate_markers.csv
    outputs/reports/tokamark_physical_window_label_review.md
    outputs/reports/tokamark_physical_window_label_summary.json
    outputs/reports/tokamark_physical_window_preview_shot_<SHOT>.csv

Next document after manual labeling
-----------------------------------

    docs/29_PHYSICAL_WINDOW_LABELING_RESULTS.md

Scientific caution
------------------
Physical labels must be assigned from physical diagnostics such as D-alpha,
profile-gradient behavior, soft-X behavior, power/density context, and published
or manual plasma notes if available. UNNS columns are included only for later
comparison and should not be used to create the labels.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


DEFAULT_SHOTS = [12046, 11941, 12055, 12007, 12017, 12063, 11768, 11776]

ALLOWED_LABEL_TYPES = [
    "L_MODE",
    "LH_TRANSITION",
    "H_MODE_STABLE",
    "PRE_ELM",
    "POST_ELM",
    "HL_BACK_TRANSITION",
    "AMBIGUOUS",
    "UNLABELABLE",
]

LABEL_TEMPLATE_COLUMNS = [
    "shot_id",
    "window_id",
    "label_type",
    "t_start",
    "t_end",
    "label_confidence",
    "primary_evidence",
    "secondary_evidence",
    "excluded_from_validation",
    "exclusion_reason",
    "notes",
]

REVIEW_COLUMNS = [
    "time_s",
    "dalpha_proxy",
    "softx_lower_proxy",
    "softx_upper_proxy",
    "softx_combined_proxy",
    "te_profile_gradient_proxy",
    "ne_profile_gradient_proxy",
    "profile_gradient_proxy",
    "nbi_proxy",
    "density_proxy",
    "m_edge_raw",
    "m_edge_conf",
    "Q_diag",
    "P_missing_critical",
    "m_edge_conf_state",
]


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
        out.extend(line(r) for r in rows)
        return "\n".join(out)


def parse_shots(values: Optional[Sequence[str | int]]) -> List[int]:
    if not values:
        return DEFAULT_SHOTS[:]
    out: List[int] = []
    for value in values:
        try:
            out.append(int(value))
        except Exception:
            pass
    return out or DEFAULT_SHOTS[:]


def read_csv_if_exists(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def numeric(df: pd.DataFrame, col: str) -> pd.Series:
    if col not in df.columns:
        return pd.Series([np.nan] * len(df), index=df.index, dtype=float)
    return pd.to_numeric(df[col], errors="coerce")


def first_existing_column(df: pd.DataFrame, candidates: Sequence[str]) -> Optional[str]:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def finite_fraction(series: pd.Series) -> float:
    arr = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)
    return float(np.isfinite(arr).mean()) if arr.size else 0.0


def safe_minmax_time(df: pd.DataFrame) -> Tuple[Optional[float], Optional[float]]:
    if "time_s" not in df.columns or df.empty:
        return None, None
    t = numeric(df, "time_s")
    finite = t[np.isfinite(t)]
    if finite.empty:
        return None, None
    return float(finite.min()), float(finite.max())


def finite_stats(series: pd.Series) -> Dict[str, Any]:
    arr = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return {"count": 0, "fraction": 0.0, "min": None, "median": None, "mean": None, "max": None}
    return {
        "count": int(finite.size),
        "fraction": float(finite.size / max(arr.size, 1)),
        "min": float(np.nanmin(finite)),
        "median": float(np.nanmedian(finite)),
        "mean": float(np.nanmean(finite)),
        "max": float(np.nanmax(finite)),
    }


# ---------------------------------------------------------------------------
# Data loading and harmonization
# ---------------------------------------------------------------------------

def load_shot_frame(out_dir: Path, shot_id: int) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Prefer confidence-revision CSV, then m_edge_t_probe CSV.
    """
    confidence_csv = out_dir / f"tokamark_shot_{shot_id}_m_edge_confidence_revision.csv"
    medge_csv = out_dir / f"tokamark_shot_{shot_id}_m_edge_t_probe.csv"
    signal_json = out_dir / f"tokamark_shot_{shot_id}_signal_probe.json"

    source = None
    df = pd.DataFrame()

    if confidence_csv.exists():
        df = read_csv_if_exists(confidence_csv)
        source = str(confidence_csv)
    elif medge_csv.exists():
        df = read_csv_if_exists(medge_csv)
        source = str(medge_csv)

    metadata = {
        "shot_id": shot_id,
        "source_csv": source,
        "confidence_csv_exists": confidence_csv.exists(),
        "m_edge_csv_exists": medge_csv.exists(),
        "signal_json_exists": signal_json.exists(),
    }

    if signal_json.exists():
        try:
            signal_payload = json.loads(signal_json.read_text(encoding="utf-8"))
            metadata["loaded_signal_arrays"] = len(signal_payload.get("loaded_labels", []) or [])
            metadata["failed_signal_arrays"] = len(signal_payload.get("failed_labels", {}) or {})
            metadata["loaded_labels"] = signal_payload.get("loaded_labels", [])
        except Exception:
            metadata["loaded_signal_arrays"] = None
            metadata["failed_signal_arrays"] = None

    if df.empty:
        return df, metadata

    df = harmonize_frame(df)
    return df, metadata


def harmonize_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Time column.
    if "time_s" not in out.columns:
        tcol = first_existing_column(out, ["time", "t", "time_sec", "seconds"])
        if tcol:
            out["time_s"] = numeric(out, tcol)
        else:
            out["time_s"] = np.arange(len(out), dtype=float)

    # UNNS raw/conf columns.
    if "m_edge_raw" not in out.columns and "m_edge" in out.columns:
        out["m_edge_raw"] = numeric(out, "m_edge")
    if "m_edge_conf" not in out.columns:
        out["m_edge_conf"] = np.nan
    if "Q_diag" not in out.columns:
        out["Q_diag"] = np.nan
    if "P_missing_critical" not in out.columns:
        out["P_missing_critical"] = np.nan

    # Derived physical proxies if missing.
    if "softx_combined_proxy" not in out.columns:
        lower = numeric(out, "softx_lower_proxy")
        upper = numeric(out, "softx_upper_proxy")
        if np.isfinite(lower).any() or np.isfinite(upper).any():
            out["softx_combined_proxy"] = np.nanmean(np.vstack([lower.to_numpy(float), upper.to_numpy(float)]), axis=0)
        else:
            out["softx_combined_proxy"] = np.nan

    if "profile_gradient_proxy" not in out.columns:
        te = numeric(out, "te_profile_gradient_proxy")
        ne = numeric(out, "ne_profile_gradient_proxy")
        if np.isfinite(te).any() or np.isfinite(ne).any():
            out["profile_gradient_proxy"] = np.nanmean(np.vstack([te.to_numpy(float), ne.to_numpy(float)]), axis=0)
        else:
            out["profile_gradient_proxy"] = np.nan

    return out


# ---------------------------------------------------------------------------
# Candidate marker detection
# ---------------------------------------------------------------------------

def robust_z_score(values: pd.Series) -> pd.Series:
    x = pd.to_numeric(values, errors="coerce").astype(float)
    finite = x[np.isfinite(x)]
    if finite.empty:
        return pd.Series([np.nan] * len(x), index=x.index, dtype=float)
    median = float(np.nanmedian(finite))
    mad = float(np.nanmedian(np.abs(finite - median)))
    if not np.isfinite(mad) or mad <= 1e-12:
        std = float(np.nanstd(finite))
        scale = std if std > 1e-12 else 1.0
    else:
        scale = 1.4826 * mad
    return (x - median) / scale


def derivative_strength(df: pd.DataFrame, col: str) -> pd.Series:
    if col not in df.columns:
        return pd.Series([np.nan] * len(df), index=df.index, dtype=float)
    y = pd.to_numeric(df[col], errors="coerce").astype(float)
    t = pd.to_numeric(df["time_s"], errors="coerce").astype(float)
    dy = y.diff()
    dt = t.diff().replace(0, np.nan)
    d = (dy / dt).replace([np.inf, -np.inf], np.nan)
    return robust_z_score(d.abs())


def level_strength(df: pd.DataFrame, col: str) -> pd.Series:
    if col not in df.columns:
        return pd.Series([np.nan] * len(df), index=df.index, dtype=float)
    return robust_z_score(pd.to_numeric(df[col], errors="coerce").abs())


def indices_to_windows(
    df: pd.DataFrame,
    indices: Sequence[int],
    *,
    half_width_seconds: float,
    min_duration_seconds: float,
) -> List[Tuple[float, float, List[int]]]:
    if "time_s" not in df.columns or df.empty:
        return []

    t = pd.to_numeric(df["time_s"], errors="coerce")
    windows: List[Tuple[float, float, List[int]]] = []

    for idx in sorted(set(int(i) for i in indices if 0 <= int(i) < len(df))):
        center = t.iloc[idx]
        if not np.isfinite(center):
            continue
        start = float(center - half_width_seconds)
        end = float(center + half_width_seconds)
        if end - start < min_duration_seconds:
            end = start + min_duration_seconds
        windows.append((start, end, [idx]))

    # Merge overlapping windows.
    if not windows:
        return []

    windows.sort(key=lambda x: x[0])
    merged: List[Tuple[float, float, List[int]]] = [windows[0]]
    for start, end, ids in windows[1:]:
        last_start, last_end, last_ids = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end), last_ids + ids)
        else:
            merged.append((start, end, ids))

    return merged


def top_event_indices(score: pd.Series, max_events: int, min_separation: int) -> List[int]:
    s = pd.to_numeric(score, errors="coerce")
    finite = s[np.isfinite(s)]
    if finite.empty:
        return []

    # Use both quantile and absolute z threshold to avoid too many weak markers.
    q = float(np.nanquantile(finite, 0.95)) if len(finite) >= 20 else float(np.nanmax(finite))
    threshold = max(2.0, q)

    candidates = [(float(v), int(i)) for i, v in s.items() if np.isfinite(v) and float(v) >= threshold]
    candidates.sort(reverse=True)

    selected: List[int] = []
    for _, idx in candidates:
        if all(abs(idx - j) >= min_separation for j in selected):
            selected.append(idx)
        if len(selected) >= max_events:
            break
    return sorted(selected)


def marker_evidence_at(df: pd.DataFrame, indices: Sequence[int], cols: Sequence[str]) -> Dict[str, Any]:
    evidence: Dict[str, Any] = {}
    for col in cols:
        if col not in df.columns:
            continue
        vals = pd.to_numeric(df[col], errors="coerce").iloc[list(indices)] if indices else pd.Series(dtype=float)
        vals = vals[np.isfinite(vals)]
        if vals.empty:
            continue
        evidence[f"{col}_median"] = float(vals.median())
        evidence[f"{col}_min"] = float(vals.min())
        evidence[f"{col}_max"] = float(vals.max())
    return evidence


def detect_candidate_markers(
    df: pd.DataFrame,
    shot_id: int,
    *,
    max_markers_per_signal: int,
    half_width_seconds: float,
    min_duration_seconds: float,
) -> pd.DataFrame:
    """
    Detect review markers. Physical diagnostic markers are intended as labeling aids.
    UNNS markers are included only for comparison and should not create labels.
    """
    if df.empty:
        return pd.DataFrame()

    marker_specs = [
        ("PHYSICAL", "D_ALPHA_SHARP_CHANGE", "dalpha_proxy", "derivative", "D-alpha proxy sharp change"),
        ("PHYSICAL", "SOFTX_SHARP_CHANGE", "softx_combined_proxy", "derivative", "soft-X combined proxy sharp change"),
        ("PHYSICAL", "PROFILE_GRADIENT_CHANGE", "profile_gradient_proxy", "derivative", "profile-gradient proxy sharp change"),
        ("PHYSICAL", "POWER_CONTEXT_CHANGE", "nbi_proxy", "derivative", "NBI / power proxy sharp change"),
        ("PHYSICAL", "DENSITY_CONTEXT_CHANGE", "density_proxy", "derivative", "density proxy sharp change"),
        ("UNNS_AUDIT", "M_EDGE_CONF_POSITIVE_REGION", "m_edge_conf", "positive_level", "m_edge_conf positive region"),
        ("UNNS_AUDIT", "M_EDGE_CONF_NEGATIVE_REGION", "m_edge_conf", "negative_level", "m_edge_conf negative region"),
        ("UNNS_AUDIT", "Q_DIAG_DROP", "Q_diag", "negative_derivative", "diagnostic-confidence drop"),
        ("UNNS_AUDIT", "P_MISSING_CRITICAL_SPIKE", "P_missing_critical", "positive_level", "critical-missing penalty spike"),
    ]

    rows: List[Dict[str, Any]] = []

    for marker_family, marker_type, col, mode, description in marker_specs:
        if col not in df.columns:
            continue

        if mode == "derivative":
            score = derivative_strength(df, col)
        elif mode == "negative_derivative":
            vals = -pd.to_numeric(df[col], errors="coerce")
            tmp = df.copy()
            tmp[f"__neg_{col}"] = vals
            score = derivative_strength(tmp, f"__neg_{col}")
        elif mode == "positive_level":
            score = robust_z_score(pd.to_numeric(df[col], errors="coerce"))
        elif mode == "negative_level":
            score = robust_z_score(-pd.to_numeric(df[col], errors="coerce"))
        else:
            continue

        indices = top_event_indices(score, max_events=max_markers_per_signal, min_separation=8)
        windows = indices_to_windows(
            df,
            indices,
            half_width_seconds=half_width_seconds,
            min_duration_seconds=min_duration_seconds,
        )

        for n, (start, end, ids) in enumerate(windows, start=1):
            evidence = marker_evidence_at(
                df,
                ids,
                [
                    col,
                    "dalpha_proxy",
                    "softx_combined_proxy",
                    "profile_gradient_proxy",
                    "nbi_proxy",
                    "density_proxy",
                    "m_edge_raw",
                    "m_edge_conf",
                    "Q_diag",
                    "P_missing_critical",
                ],
            )

            rows.append({
                "shot_id": int(shot_id),
                "marker_id": f"{shot_id}_{marker_type}_{n:02d}",
                "marker_family": marker_family,
                "marker_type": marker_type,
                "marker_description": description,
                "source_column": col,
                "t_start": float(start),
                "t_end": float(end),
                "center_time": float((start + end) / 2.0),
                "n_peak_indices": int(len(ids)),
                "score_max": float(pd.to_numeric(score, errors="coerce").iloc[ids].max()) if ids else None,
                "evidence_json": json.dumps(make_json_safe(evidence), sort_keys=True),
            })

    if not rows:
        return pd.DataFrame()

    markers = pd.DataFrame(rows)

    # Sort physical markers before audit markers, then by shot/time.
    family_order = {"PHYSICAL": 0, "UNNS_AUDIT": 1}
    markers["_family_order"] = markers["marker_family"].map(family_order).fillna(9)
    markers = markers.sort_values(["shot_id", "_family_order", "t_start", "marker_type"]).drop(columns=["_family_order"])
    return markers.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Label template and previews
# ---------------------------------------------------------------------------

def build_label_template_for_shot(
    shot_id: int,
    df: pd.DataFrame,
    markers: pd.DataFrame,
    *,
    max_template_windows: int,
) -> pd.DataFrame:
    """
    Create placeholder rows for manual labeling.

    Physical markers are used as candidate review windows, but the label remains
    AMBIGUOUS with low confidence until a human reviewer assigns a physical label.
    """
    t_min, t_max = safe_minmax_time(df)

    rows: List[Dict[str, Any]] = []

    if df.empty or t_min is None or t_max is None:
        rows.append({
            "shot_id": int(shot_id),
            "window_id": f"{shot_id}_UNLABELABLE_001",
            "label_type": "UNLABELABLE",
            "t_start": "",
            "t_end": "",
            "label_confidence": "unlabelable",
            "primary_evidence": "no readable time-resolved input",
            "secondary_evidence": "",
            "excluded_from_validation": True,
            "exclusion_reason": "missing confidence-revision or m_edge time-series CSV",
            "notes": "Manual review cannot proceed until time-resolved data exists.",
        })
        return pd.DataFrame(rows, columns=LABEL_TEMPLATE_COLUMNS)

    physical = markers[
        (markers["shot_id"].astype(int).eq(int(shot_id)))
        & (markers["marker_family"].astype(str).eq("PHYSICAL"))
    ].copy() if not markers.empty else pd.DataFrame()

    if physical.empty:
        rows.append({
            "shot_id": int(shot_id),
            "window_id": f"{shot_id}_REVIEW_FULL_001",
            "label_type": "AMBIGUOUS",
            "t_start": float(t_min),
            "t_end": float(t_max),
            "label_confidence": "low",
            "primary_evidence": "no strong physical diagnostic marker auto-detected",
            "secondary_evidence": "review full available trace manually",
            "excluded_from_validation": True,
            "exclusion_reason": "requires manual physical label",
            "notes": "Fill label_type only after independent physical review.",
        })
        return pd.DataFrame(rows, columns=LABEL_TEMPLATE_COLUMNS)

    # Limit to most useful physical markers by marker quality and variety.
    physical = physical.copy()
    physical["score_max_numeric"] = pd.to_numeric(physical["score_max"], errors="coerce").fillna(0.0)
    physical = physical.sort_values(["score_max_numeric", "t_start"], ascending=[False, True]).head(max_template_windows)
    physical = physical.sort_values("t_start")

    for i, marker in enumerate(physical.itertuples(index=False), start=1):
        rows.append({
            "shot_id": int(shot_id),
            "window_id": f"{shot_id}_CANDIDATE_{i:03d}",
            "label_type": "AMBIGUOUS",
            "t_start": float(getattr(marker, "t_start")),
            "t_end": float(getattr(marker, "t_end")),
            "label_confidence": "low",
            "primary_evidence": f"{getattr(marker, 'marker_type')} from {getattr(marker, 'source_column')}",
            "secondary_evidence": getattr(marker, "marker_description"),
            "excluded_from_validation": True,
            "exclusion_reason": "manual physical label not yet assigned",
            "notes": (
                "Candidate review window only. Replace label_type with L_MODE, LH_TRANSITION, "
                "H_MODE_STABLE, PRE_ELM, POST_ELM, HL_BACK_TRANSITION, AMBIGUOUS, or UNLABELABLE "
                "after independent physical review."
            ),
        })

    return pd.DataFrame(rows, columns=LABEL_TEMPLATE_COLUMNS)


def downsample_preview(df: pd.DataFrame, max_rows: int) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=REVIEW_COLUMNS)

    cols = [c for c in REVIEW_COLUMNS if c in df.columns]
    preview = df[cols].copy()

    if len(preview) <= max_rows:
        return preview

    idx = np.linspace(0, len(preview) - 1, max_rows).round().astype(int)
    idx = np.unique(idx)
    return preview.iloc[idx].reset_index(drop=True)


def shot_summary(shot_id: int, df: pd.DataFrame, metadata: Dict[str, Any], markers: pd.DataFrame) -> Dict[str, Any]:
    t_min, t_max = safe_minmax_time(df)

    row: Dict[str, Any] = {
        "shot_id": int(shot_id),
        "source_csv": metadata.get("source_csv"),
        "rows": int(len(df)),
        "time_min": t_min,
        "time_max": t_max,
        "confidence_csv_exists": metadata.get("confidence_csv_exists"),
        "m_edge_csv_exists": metadata.get("m_edge_csv_exists"),
        "signal_json_exists": metadata.get("signal_json_exists"),
        "loaded_signal_arrays": metadata.get("loaded_signal_arrays"),
        "failed_signal_arrays": metadata.get("failed_signal_arrays"),
    }

    for col in [
        "dalpha_proxy",
        "softx_combined_proxy",
        "profile_gradient_proxy",
        "nbi_proxy",
        "density_proxy",
        "m_edge_raw",
        "m_edge_conf",
        "Q_diag",
        "P_missing_critical",
    ]:
        if col in df.columns:
            stats = finite_stats(df[col])
            row[f"{col}_finite_fraction"] = stats["fraction"]
            row[f"{col}_median"] = stats["median"]

    if not markers.empty:
        m = markers[markers["shot_id"].astype(int).eq(int(shot_id))]
        row["physical_marker_count"] = int(m["marker_family"].astype(str).eq("PHYSICAL").sum()) if not m.empty else 0
        row["unns_audit_marker_count"] = int(m["marker_family"].astype(str).eq("UNNS_AUDIT").sum()) if not m.empty else 0
    else:
        row["physical_marker_count"] = 0
        row["unns_audit_marker_count"] = 0

    return row


def write_review_markdown(
    path: Path,
    *,
    shots: List[int],
    summaries: pd.DataFrame,
    labels: pd.DataFrame,
    markers: pd.DataFrame,
    out_dir: Path,
) -> None:
    md: List[str] = []
    md.append("# TokaMark Physical-Window Label Review Template")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("This review sheet supports independent manual physical-window labeling.")
    md.append("")
    md.append("Do not assign physical labels from `m_edge_conf(t)`. Use physical diagnostics first, then compare UNNS columns afterward.")
    md.append("")
    md.append("## Shots")
    md.append("")
    md.append("```text")
    for shot in shots:
        md.append(str(shot))
    md.append("```")
    md.append("")
    md.append("## Output files")
    md.append("")
    md.append("```text")
    md.append("outputs/reports/tokamark_physical_window_label_template.csv")
    md.append("outputs/reports/tokamark_physical_window_label_candidate_markers.csv")
    md.append("outputs/reports/tokamark_physical_window_label_summary.json")
    md.append("outputs/reports/tokamark_physical_window_preview_shot_<SHOT>.csv")
    md.append("```")
    md.append("")
    md.append("## Allowed label types")
    md.append("")
    md.append("```text")
    for label in ALLOWED_LABEL_TYPES:
        md.append(label)
    md.append("```")
    md.append("")
    md.append("## Shot summary")
    md.append("")
    summary_cols = [
        "shot_id", "rows", "time_min", "time_max",
        "dalpha_proxy_finite_fraction",
        "softx_combined_proxy_finite_fraction",
        "profile_gradient_proxy_finite_fraction",
        "m_edge_conf_finite_fraction",
        "Q_diag_median",
        "P_missing_critical_median",
        "physical_marker_count",
        "unns_audit_marker_count",
    ]
    summary_cols = [c for c in summary_cols if c in summaries.columns]
    md.append(df_to_markdown(summaries[summary_cols], index=False))
    md.append("")
    md.append("## Manual labeling instructions")
    md.append("")
    md.append("1. Open each preview CSV and inspect physical diagnostics first: D-alpha, soft-X, profile gradients, power, and density.")
    md.append("2. Assign labels in `tokamark_physical_window_label_template.csv` only after physical review.")
    md.append("3. Keep `excluded_from_validation = true` until the label is physically justified.")
    md.append("4. Use `AMBIGUOUS` instead of forcing a label.")
    md.append("5. Use `UNLABELABLE` when the physical evidence is insufficient.")
    md.append("6. Only after labels are assigned, compare them against `m_edge_conf(t)`.")
    md.append("")
    md.append("## Candidate label rows")
    md.append("")
    label_cols = LABEL_TEMPLATE_COLUMNS
    md.append(df_to_markdown(labels[label_cols], index=False))
    md.append("")
    md.append("## Candidate physical markers")
    md.append("")
    physical = markers[markers["marker_family"].astype(str).eq("PHYSICAL")] if not markers.empty else pd.DataFrame()
    marker_cols = [
        "shot_id", "marker_id", "marker_type", "source_column",
        "t_start", "t_end", "score_max", "marker_description"
    ]
    marker_cols = [c for c in marker_cols if c in physical.columns]
    md.append(df_to_markdown(physical[marker_cols], index=False) if not physical.empty else "_No physical markers detected._")
    md.append("")
    md.append("## UNNS audit markers")
    md.append("")
    audit = markers[markers["marker_family"].astype(str).eq("UNNS_AUDIT")] if not markers.empty else pd.DataFrame()
    marker_cols = [c for c in marker_cols if c in audit.columns]
    md.append(df_to_markdown(audit[marker_cols], index=False) if not audit.empty else "_No UNNS audit markers detected._")
    md.append("")
    md.append("## Next document after manual labels")
    md.append("")
    md.append("```text")
    md.append("docs/")
    md.append("  29_PHYSICAL_WINDOW_LABELING_RESULTS.md")
    md.append("```")
    md.append("")
    md.append("## Bounded interpretation")
    md.append("")
    md.append("This template does not validate H-mode. It prepares independent physical labels so that validation can be attempted without circularity.")
    md.append("")

    path.write_text("\n".join(md), encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate physical-window label template and review sheets.")
    parser.add_argument("--shots", nargs="*", default=None, help="Shot IDs. Defaults to initial physical-window labeling set.")
    parser.add_argument("--out-dir", default="outputs/reports", help="Output/report directory.")
    parser.add_argument("--max-preview-rows", type=int, default=500, help="Maximum rows per preview CSV.")
    parser.add_argument("--max-markers-per-signal", type=int, default=4, help="Maximum detected markers per signal per shot.")
    parser.add_argument("--max-template-windows", type=int, default=10, help="Maximum candidate template windows per shot.")
    parser.add_argument("--half-width-seconds", type=float, default=0.006, help="Half-width around detected markers.")
    parser.add_argument("--min-duration-seconds", type=float, default=0.004, help="Minimum candidate window duration.")
    parser.add_argument("--prefix", default="tokamark_physical_window_label", help="Output filename prefix.")
    args = parser.parse_args()

    shots = parse_shots(args.shots)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    all_markers: List[pd.DataFrame] = []
    all_labels: List[pd.DataFrame] = []
    summaries: List[Dict[str, Any]] = []

    for shot in shots:
        print(f"[shot {shot}] building physical-window review template...", flush=True)
        df, metadata = load_shot_frame(out_dir, shot)

        markers = detect_candidate_markers(
            df,
            shot,
            max_markers_per_signal=args.max_markers_per_signal,
            half_width_seconds=args.half_width_seconds,
            min_duration_seconds=args.min_duration_seconds,
        )

        labels = build_label_template_for_shot(
            shot,
            df,
            markers,
            max_template_windows=args.max_template_windows,
        )

        preview = downsample_preview(df, args.max_preview_rows)
        preview_path = out_dir / f"{args.prefix}_preview_shot_{shot}.csv"
        preview.to_csv(preview_path, index=False)

        summaries.append(shot_summary(shot, df, metadata, markers))
        if not markers.empty:
            all_markers.append(markers)
        all_labels.append(labels)

    markers_df = pd.concat(all_markers, ignore_index=True) if all_markers else pd.DataFrame()
    labels_df = pd.concat(all_labels, ignore_index=True) if all_labels else pd.DataFrame(columns=LABEL_TEMPLATE_COLUMNS)
    summaries_df = pd.DataFrame(summaries)

    template_csv = out_dir / f"{args.prefix}_template.csv"
    markers_csv = out_dir / f"{args.prefix}_candidate_markers.csv"
    review_md = out_dir / f"{args.prefix}_review.md"
    summary_json = out_dir / f"{args.prefix}_summary.json"

    labels_df.to_csv(template_csv, index=False)
    markers_df.to_csv(markers_csv, index=False)
    write_json(summary_json, {
        "component": "tokamark_physical_window_label_template.py",
        "shots": shots,
        "label_template": str(template_csv),
        "candidate_markers": str(markers_csv),
        "review_markdown": str(review_md),
        "summary": summaries,
        "allowed_label_types": ALLOWED_LABEL_TYPES,
        "warning": "Labels are placeholders. Manual physical labeling is still required.",
    })
    write_review_markdown(
        review_md,
        shots=shots,
        summaries=summaries_df,
        labels=labels_df,
        markers=markers_df,
        out_dir=out_dir,
    )

    print()
    print("Physical-window label template complete.")
    print(f"Shots: {shots}")
    print(f"Template CSV: {template_csv}")
    print(f"Candidate markers CSV: {markers_csv}")
    print(f"Review MD: {review_md}")
    print(f"Summary JSON: {summary_json}")
    print()
    print("Next manual file to edit:")
    print(f"  {template_csv}")
    print()
    print("Next report after manual labeling:")
    print("  docs/29_PHYSICAL_WINDOW_LABELING_RESULTS.md")


if __name__ == "__main__":
    main()
