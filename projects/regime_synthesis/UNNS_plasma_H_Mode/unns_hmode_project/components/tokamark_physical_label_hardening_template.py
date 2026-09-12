#!/usr/bin/env python3
"""
tokamark_physical_label_hardening_template.py

UNNS-H Mode Project
Physical-window label hardening review-template generator.

Purpose
-------
Create a hardening review CSV and markdown review sheet from the current edited
physical-window labels and the first physical-window label analysis.

This follows:

    docs/30_PHYSICAL_WINDOW_LABEL_HARDENING_PLAN.md

The script does NOT harden labels automatically.
The script does NOT validate H-mode.
The script prepares a structured review artifact so the provisional labels can
be accepted, downgraded, rejected, kept ambiguous, or marked as needing an
external reference.

Default inputs
--------------

    outputs/reports/tokamark_physical_window_label_template_EDITED.csv
    outputs/reports/tokamark_physical_window_label_analysis.csv
    outputs/reports/tokamark_physical_window_label_candidate_markers.csv

Default outputs
---------------

    outputs/reports/tokamark_physical_window_labels_HARDENING_REVIEW.csv
    outputs/reports/tokamark_physical_window_labels_HARDENING_REVIEW.md
    outputs/reports/tokamark_physical_window_labels_HARDENING_REVIEW_summary.json

Reviewer workflow
-----------------

1. Open the review CSV.
2. Inspect each row using the preview files and physical diagnostics.
3. Edit:
       hardened_label_type
       hardening_level
       review_decision
       evidence columns
       reviewer_notes
       excluded_from_validation
       exclusion_reason
4. Save the reviewed copy as:

       outputs/reports/tokamark_physical_window_labels_HARDENED_v0_1.csv

5. Then rerun the label analyzer using the hardened file.

Scientific caution
------------------
The UNNS margin is included only as an audit/comparison field. It must not be
used to decide the physical label.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


REVIEW_COLUMNS = [
    "shot_id",
    "window_id",
    "original_label_type",
    "hardened_label_type",
    "t_start",
    "t_end",
    "window_duration",
    "hardening_level",
    "label_confidence",
    "dalpha_evidence",
    "profile_evidence",
    "softx_evidence",
    "power_density_context",
    "geometry_context",
    "external_reference",
    "review_decision",
    "reviewer_notes",
    "excluded_from_validation",
    "exclusion_reason",
    "original_excluded_from_validation",
    "original_primary_evidence",
    "original_secondary_evidence",
    "analysis_status",
    "n_samples",
    "Q_diag_median",
    "P_missing_critical_median",
    "m_edge_conf_median_AUDIT_ONLY",
    "conf_positive_fraction_AUDIT_ONLY",
    "conf_negative_fraction_AUDIT_ONLY",
    "physical_marker_overlap_count",
    "overlapping_physical_markers",
    "preview_file",
]

ALLOWED_HARDENED_LABEL_TYPES = [
    "L_MODE",
    "LH_TRANSITION",
    "H_MODE_STABLE",
    "PRE_ELM",
    "POST_ELM",
    "HL_BACK_TRANSITION",
    "AMBIGUOUS",
    "UNLABELABLE",
    "REJECTED",
]

ALLOWED_HARDENING_LEVELS = [
    "0_PROVISIONAL",
    "1_PLAUSIBLE",
    "2_SUPPORTED",
    "3_EXTERNALLY_ANCHORED",
]

ALLOWED_REVIEW_DECISIONS = [
    "ACCEPT",
    "DOWNGRADE",
    "REJECT",
    "KEEP_AMBIGUOUS",
    "KEEP_UNLABELABLE",
    "NEEDS_EXTERNAL_REFERENCE",
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
        out.extend(line(row) for row in rows)
        return "\n".join(out)


def read_csv(path: Path, required: bool = True) -> pd.DataFrame:
    if not path.exists():
        if required:
            raise FileNotFoundError(f"Missing CSV: {path}")
        return pd.DataFrame()
    return pd.read_csv(path)


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
    return str(value).strip().lower() in {"true", "1", "yes", "y", "excluded"}


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


def fmt_float(value: Any, digits: int = 6) -> str:
    v = fnum(value)
    if v is None:
        return ""
    return f"{v:.{digits}g}"


def overlap_fraction(a_start: float, a_end: float, b_start: float, b_end: float) -> float:
    lo = max(a_start, b_start)
    hi = min(a_end, b_end)
    if hi <= lo:
        return 0.0
    denom = max(a_end - a_start, 1e-12)
    return float((hi - lo) / denom)


def norm_label(value: Any) -> str:
    if value is None:
        return "AMBIGUOUS"
    text = str(value).strip().upper()
    return text if text else "AMBIGUOUS"


# ---------------------------------------------------------------------------
# Load and merge
# ---------------------------------------------------------------------------

def load_labels(path: Path) -> pd.DataFrame:
    df = read_csv(path, required=True)
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

    out = df.copy()
    out["shot_id"] = pd.to_numeric(out["shot_id"], errors="coerce")
    out = out.dropna(subset=["shot_id"]).copy()
    out["shot_id"] = out["shot_id"].astype(int)
    out["window_id"] = out["window_id"].astype(str)
    out["label_type"] = out["label_type"].apply(norm_label)
    out["t_start"] = pd.to_numeric(out["t_start"], errors="coerce")
    out["t_end"] = pd.to_numeric(out["t_end"], errors="coerce")
    out["window_duration"] = out["t_end"] - out["t_start"]
    out["excluded_from_validation_bool"] = out["excluded_from_validation"].apply(as_bool)
    return out


def load_analysis(path: Path) -> pd.DataFrame:
    df = read_csv(path, required=True)
    if "window_id" not in df.columns:
        raise ValueError("Analysis file must contain window_id.")
    out = df.copy()
    out["window_id"] = out["window_id"].astype(str)
    if "shot_id" in out.columns:
        out["shot_id"] = pd.to_numeric(out["shot_id"], errors="coerce").astype("Int64")
    return out


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


def overlapping_physical_markers(markers: pd.DataFrame, shot_id: int, start: float, end: float) -> Tuple[int, str]:
    if markers.empty:
        return 0, ""
    if not {"shot_id", "marker_family", "t_start", "t_end"}.issubset(set(markers.columns)):
        return 0, ""

    m = markers[
        (markers["shot_id"].astype("Int64") == int(shot_id))
        & (markers["marker_family"].astype(str).eq("PHYSICAL"))
    ].copy()
    if m.empty:
        return 0, ""

    overlaps: List[str] = []
    for _, row in m.iterrows():
        ms = fnum(row.get("t_start"))
        me = fnum(row.get("t_end"))
        if ms is None or me is None:
            continue
        frac = overlap_fraction(start, end, ms, me)
        if frac > 0 or overlap_fraction(ms, me, start, end) > 0:
            marker_type = str(row.get("marker_type", "PHYSICAL_MARKER"))
            src = str(row.get("source_column", ""))
            score = fmt_float(row.get("score_max"))
            overlaps.append(f"{marker_type}@[{ms:.6g},{me:.6g}] src={src} score={score}")

    return len(overlaps), "; ".join(overlaps)


# ---------------------------------------------------------------------------
# Suggested hardening values
# ---------------------------------------------------------------------------

def suggest_hardened_label(label: str) -> str:
    label = norm_label(label)
    if label in ALLOWED_HARDENED_LABEL_TYPES:
        return label
    return "AMBIGUOUS"


def suggest_review_decision(row: pd.Series) -> str:
    label = norm_label(row.get("label_type"))
    excluded = as_bool(row.get("excluded_from_validation"))
    confidence = str(row.get("label_confidence", "")).strip().lower()

    if label == "UNLABELABLE":
        return "KEEP_UNLABELABLE"
    if label == "AMBIGUOUS" or excluded:
        return "KEEP_AMBIGUOUS"
    if label == "H_MODE_STABLE":
        # H-mode-stable labels in the first draft were intentionally low-confidence.
        return "NEEDS_EXTERNAL_REFERENCE" if confidence in {"low", ""} else "ACCEPT"
    if label in {"L_MODE", "LH_TRANSITION"}:
        return "ACCEPT" if confidence in {"moderate", "high"} else "NEEDS_EXTERNAL_REFERENCE"
    return "NEEDS_EXTERNAL_REFERENCE"


def suggest_hardening_level(row: pd.Series, marker_count: int) -> str:
    label = norm_label(row.get("label_type"))
    excluded = as_bool(row.get("excluded_from_validation"))
    confidence = str(row.get("label_confidence", "")).strip().lower()

    if label in {"AMBIGUOUS", "UNLABELABLE"} or excluded:
        return "0_PROVISIONAL"

    if confidence == "high" and marker_count >= 2:
        return "2_SUPPORTED"
    if confidence in {"moderate", "high"} and marker_count >= 1:
        return "1_PLAUSIBLE"
    return "0_PROVISIONAL"


def evidence_from_label(row: pd.Series, analysis: Optional[pd.Series], overlapping_markers: str) -> Dict[str, str]:
    primary = str(row.get("primary_evidence", "") or "")
    secondary = str(row.get("secondary_evidence", "") or "")
    label = norm_label(row.get("label_type"))

    # These are deliberately phrased as review prompts, not final truth.
    dalpha = ""
    profile = ""
    softx = ""
    power_density = ""
    geometry = ""

    if "D_ALPHA" in primary.upper() or "D-ALPHA" in primary.upper() or "D-alpha" in primary:
        dalpha = primary
    elif "D_ALPHA" in overlapping_markers or "dalpha" in overlapping_markers.lower():
        dalpha = "overlapping physical D-alpha marker: " + overlapping_markers
    else:
        dalpha = "REVIEW_REQUIRED: confirm D-alpha morphology manually"

    if "PROFILE" in primary.upper() or "profile" in secondary.lower():
        profile = primary if "PROFILE" in primary.upper() else secondary
    elif "PROFILE_GRADIENT" in overlapping_markers:
        profile = "overlapping profile-gradient marker: " + overlapping_markers
    else:
        profile = "REVIEW_REQUIRED: confirm profile-gradient / pedestal proxy"

    if "SOFTX" in overlapping_markers or "SOFTX" in primary.upper() or "soft-X" in secondary:
        softx = "review overlapping soft-X/edge activity evidence: " + (overlapping_markers or primary or secondary)
    else:
        softx = "REVIEW_REQUIRED: confirm soft-X / edge activity consistency"

    if label == "L_MODE":
        power_density = "REVIEW_REQUIRED: confirm pre-transition power/density context"
    elif label == "LH_TRANSITION":
        power_density = "REVIEW_REQUIRED: confirm transition occurs in plausible power/density context"
    elif label == "H_MODE_STABLE":
        power_density = "REVIEW_REQUIRED: confirm sustained post-transition context, not only positive UNNS margin"
    elif label == "UNLABELABLE":
        power_density = "missing critical independent diagnostics; keep excluded unless external evidence exists"
    else:
        power_density = "REVIEW_REQUIRED"

    geometry = "optional support only; do not assign label from geometry alone"

    return {
        "dalpha_evidence": dalpha,
        "profile_evidence": profile,
        "softx_evidence": softx,
        "power_density_context": power_density,
        "geometry_context": geometry,
    }


# ---------------------------------------------------------------------------
# Build review table
# ---------------------------------------------------------------------------

def build_review(labels: pd.DataFrame, analysis: pd.DataFrame, markers: pd.DataFrame, out_dir: Path) -> pd.DataFrame:
    analysis_by_window: Dict[str, pd.Series] = {}
    if not analysis.empty and "window_id" in analysis.columns:
        for _, row in analysis.iterrows():
            analysis_by_window[str(row["window_id"])] = row

    rows: List[Dict[str, Any]] = []

    for _, label_row in labels.iterrows():
        window_id = str(label_row["window_id"])
        shot_id = int(label_row["shot_id"])
        t_start = fnum(label_row.get("t_start"))
        t_end = fnum(label_row.get("t_end"))
        analysis_row = analysis_by_window.get(window_id)

        marker_count, marker_text = (0, "")
        if t_start is not None and t_end is not None:
            marker_count, marker_text = overlapping_physical_markers(markers, shot_id, t_start, t_end)

        evidence = evidence_from_label(label_row, analysis_row, marker_text)
        review_decision = suggest_review_decision(label_row)
        hardening_level = suggest_hardening_level(label_row, marker_count)

        excluded_original = as_bool(label_row.get("excluded_from_validation"))
        label_type = norm_label(label_row.get("label_type"))

        if review_decision in {"KEEP_AMBIGUOUS", "KEEP_UNLABELABLE"}:
            excluded = True
        else:
            excluded = excluded_original

        if label_type == "UNLABELABLE":
            exclusion_reason = str(label_row.get("exclusion_reason", "") or "unlabelable due to insufficient independent diagnostics")
        elif label_type == "AMBIGUOUS":
            exclusion_reason = str(label_row.get("exclusion_reason", "") or "ambiguous pending hardening review")
        else:
            exclusion_reason = str(label_row.get("exclusion_reason", "") or "")

        analysis_status = analysis_row.get("analysis_status", "") if analysis_row is not None else "missing_analysis"
        n_samples = analysis_row.get("n_samples", "") if analysis_row is not None else ""

        q_diag = analysis_row.get("Q_diag_median", "") if analysis_row is not None else ""
        p_miss = analysis_row.get("P_missing_critical_median", "") if analysis_row is not None else ""
        m_conf = analysis_row.get("m_edge_conf_median", "") if analysis_row is not None else ""
        conf_pos = analysis_row.get("conf_positive_fraction", "") if analysis_row is not None else ""
        conf_neg = analysis_row.get("conf_negative_fraction", "") if analysis_row is not None else ""

        notes = str(label_row.get("notes", "") or "")
        reviewer_notes = (
            "HARDENING_REVIEW_REQUIRED. "
            "Assign label using physical diagnostics first; inspect UNNS audit columns only after label decision. "
            + notes
        )

        rows.append({
            "shot_id": shot_id,
            "window_id": window_id,
            "original_label_type": label_type,
            "hardened_label_type": suggest_hardened_label(label_type),
            "t_start": t_start,
            "t_end": t_end,
            "window_duration": fnum(label_row.get("window_duration")),
            "hardening_level": hardening_level,
            "label_confidence": label_row.get("label_confidence", ""),
            "dalpha_evidence": evidence["dalpha_evidence"],
            "profile_evidence": evidence["profile_evidence"],
            "softx_evidence": evidence["softx_evidence"],
            "power_density_context": evidence["power_density_context"],
            "geometry_context": evidence["geometry_context"],
            "external_reference": "",
            "review_decision": review_decision,
            "reviewer_notes": reviewer_notes,
            "excluded_from_validation": excluded,
            "exclusion_reason": exclusion_reason,
            "original_excluded_from_validation": excluded_original,
            "original_primary_evidence": label_row.get("primary_evidence", ""),
            "original_secondary_evidence": label_row.get("secondary_evidence", ""),
            "analysis_status": analysis_status,
            "n_samples": n_samples,
            "Q_diag_median": q_diag,
            "P_missing_critical_median": p_miss,
            "m_edge_conf_median_AUDIT_ONLY": m_conf,
            "conf_positive_fraction_AUDIT_ONLY": conf_pos,
            "conf_negative_fraction_AUDIT_ONLY": conf_neg,
            "physical_marker_overlap_count": marker_count,
            "overlapping_physical_markers": marker_text,
            "preview_file": str(out_dir / f"tokamark_physical_window_label_preview_shot_{shot_id}.csv"),
        })

    review = pd.DataFrame(rows)
    for col in REVIEW_COLUMNS:
        if col not in review.columns:
            review[col] = ""
    return review[REVIEW_COLUMNS]


def summarize_review(review: pd.DataFrame) -> Dict[str, Any]:
    def value_counts(col: str) -> Dict[str, int]:
        if col not in review.columns:
            return {}
        return {str(k): int(v) for k, v in review[col].astype(str).value_counts(dropna=False).to_dict().items()}

    return {
        "row_count": int(len(review)),
        "shot_count": int(review["shot_id"].nunique()) if "shot_id" in review.columns else 0,
        "original_label_counts": value_counts("original_label_type"),
        "hardened_label_counts_initial": value_counts("hardened_label_type"),
        "review_decision_counts_initial": value_counts("review_decision"),
        "hardening_level_counts_initial": value_counts("hardening_level"),
        "excluded_from_validation_counts_initial": value_counts("excluded_from_validation"),
    }


def write_review_markdown(path: Path, review: pd.DataFrame, summary: Dict[str, Any]) -> None:
    md: List[str] = []
    md.append("# TokaMark Physical-Window Label Hardening Review")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("This file supports hardening provisional physical-window labels before stronger validation claims.")
    md.append("")
    md.append("The reviewer should edit:")
    md.append("")
    md.append("```text")
    md.append("outputs/reports/tokamark_physical_window_labels_HARDENING_REVIEW.csv")
    md.append("```")
    md.append("")
    md.append("and save the accepted hardened version as:")
    md.append("")
    md.append("```text")
    md.append("outputs/reports/tokamark_physical_window_labels_HARDENED_v0_1.csv")
    md.append("```")
    md.append("")
    md.append("## Review rules")
    md.append("")
    md.append("- Do not assign a physical label from `m_edge_conf(t)`.")
    md.append("- Use D-alpha, profile-gradient, soft-X, power/density context, and external references where available.")
    md.append("- Keep uncertain windows as `AMBIGUOUS` or `UNLABELABLE`.")
    md.append("- Reject labels that cannot be justified without UNNS columns.")
    md.append("- Treat `m_edge_conf_median_AUDIT_ONLY` as comparison data only.")
    md.append("")
    md.append("## Allowed hardened labels")
    md.append("")
    md.append("```text")
    for item in ALLOWED_HARDENED_LABEL_TYPES:
        md.append(item)
    md.append("```")
    md.append("")
    md.append("## Allowed hardening levels")
    md.append("")
    md.append("```text")
    for item in ALLOWED_HARDENING_LEVELS:
        md.append(item)
    md.append("```")
    md.append("")
    md.append("## Allowed review decisions")
    md.append("")
    md.append("```text")
    for item in ALLOWED_REVIEW_DECISIONS:
        md.append(item)
    md.append("```")
    md.append("")
    md.append("## Initial summary")
    md.append("")
    for key, value in summary.items():
        md.append(f"- **{key}**: `{value}`")
    md.append("")
    md.append("## Rows requiring external reference or decision")
    md.append("")
    focus = review[review["review_decision"].astype(str).isin(["NEEDS_EXTERNAL_REFERENCE", "KEEP_AMBIGUOUS", "KEEP_UNLABELABLE"])].copy()
    focus_cols = [
        "shot_id",
        "window_id",
        "original_label_type",
        "hardened_label_type",
        "t_start",
        "t_end",
        "hardening_level",
        "review_decision",
        "dalpha_evidence",
        "profile_evidence",
        "softx_evidence",
        "Q_diag_median",
        "P_missing_critical_median",
        "m_edge_conf_median_AUDIT_ONLY",
    ]
    focus_cols = [c for c in focus_cols if c in focus.columns]
    md.append(df_to_markdown(focus[focus_cols], index=False) if not focus.empty else "_No focus rows._")
    md.append("")
    md.append("## Candidate accepted rows needing confirmation")
    md.append("")
    accepted = review[review["review_decision"].astype(str).eq("ACCEPT")].copy()
    acc_cols = [
        "shot_id",
        "window_id",
        "original_label_type",
        "hardened_label_type",
        "t_start",
        "t_end",
        "hardening_level",
        "dalpha_evidence",
        "profile_evidence",
        "softx_evidence",
        "power_density_context",
    ]
    acc_cols = [c for c in acc_cols if c in accepted.columns]
    md.append(df_to_markdown(accepted[acc_cols], index=False) if not accepted.empty else "_No initially accepted rows._")
    md.append("")
    md.append("## Next command after hardened CSV is saved")
    md.append("")
    md.append("```powershell")
    md.append("python components\\tokamark_physical_window_label_analyzer.py ^")
    md.append("  --labels outputs\\reports\\tokamark_physical_window_labels_HARDENED_v0_1.csv ^")
    md.append("  --out-dir outputs\\reports ^")
    md.append("  --prefix tokamark_physical_window_label_analysis_HARDENED_v0_1")
    md.append("```")
    md.append("")
    md.append("## Next report")
    md.append("")
    md.append("```text")
    md.append("docs/")
    md.append("  31_PHYSICAL_WINDOW_LABEL_HARDENING_RESULTS.md")
    md.append("```")
    md.append("")
    path.write_text("\n".join(md), encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Create a physical-window label hardening review template.")
    parser.add_argument("--labels", default="outputs/reports/tokamark_physical_window_label_template_EDITED.csv", help="Edited label CSV.")
    parser.add_argument("--analysis", default="outputs/reports/tokamark_physical_window_label_analysis.csv", help="Window analysis CSV.")
    parser.add_argument("--markers", default="outputs/reports/tokamark_physical_window_label_candidate_markers.csv", help="Candidate markers CSV.")
    parser.add_argument("--out-dir", default="outputs/reports", help="Output/report directory.")
    parser.add_argument("--prefix", default="tokamark_physical_window_labels_HARDENING_REVIEW", help="Output prefix.")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    labels_path = Path(args.labels)
    analysis_path = Path(args.analysis)
    markers_path = Path(args.markers)

    labels = load_labels(labels_path)
    analysis = load_analysis(analysis_path)
    markers = load_markers(markers_path)

    review = build_review(labels, analysis, markers, out_dir)
    summary = summarize_review(review)

    csv_out = out_dir / f"{args.prefix}.csv"
    md_out = out_dir / f"{args.prefix}.md"
    json_out = out_dir / f"{args.prefix}_summary.json"

    review.to_csv(csv_out, index=False)
    write_review_markdown(md_out, review, summary)
    write_json(json_out, {
        "component": "tokamark_physical_label_hardening_template.py",
        "labels_input": str(labels_path),
        "analysis_input": str(analysis_path),
        "markers_input": str(markers_path),
        "review_csv": str(csv_out),
        "review_md": str(md_out),
        "summary": summary,
        "allowed_hardened_label_types": ALLOWED_HARDENED_LABEL_TYPES,
        "allowed_hardening_levels": ALLOWED_HARDENING_LEVELS,
        "allowed_review_decisions": ALLOWED_REVIEW_DECISIONS,
        "next_hardened_file": str(out_dir / "tokamark_physical_window_labels_HARDENED_v0_1.csv"),
    })

    print("Physical label hardening review template complete.")
    print(f"Rows: {len(review)}")
    print(f"Shots: {review['shot_id'].nunique() if 'shot_id' in review.columns else 0}")
    print(f"Review CSV: {csv_out}")
    print(f"Review MD: {md_out}")
    print(f"Summary JSON: {json_out}")
    print()
    print("Edit the review CSV, then save the hardened version as:")
    print(f"  {out_dir / 'tokamark_physical_window_labels_HARDENED_v0_1.csv'}")
    print()
    print("Next report after hardened analysis:")
    print("  docs/31_PHYSICAL_WINDOW_LABEL_HARDENING_RESULTS.md")


if __name__ == "__main__":
    main()
