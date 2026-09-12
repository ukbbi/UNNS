#!/usr/bin/env python3
"""
tokamark_cross_shot_m_edge_comparator.py

UNNS-H Mode Project
Cross-shot comparison for two TokaMark/MAST m_edge(t) traces.

Purpose
-------
Compare reference shot 12063 against a weaker / comparison TokaMark shot after
the same pipeline has been run on both shots.

Required prior outputs for each shot:
    outputs/reports/tokamark_shot_<SHOT>_m_edge_t_probe.csv
    outputs/reports/tokamark_shot_<SHOT>_m_edge_trace_inspection_summary.json

Run after the comparison shot pipeline:
    python components\\tokamark_cross_shot_m_edge_comparator.py ^
      --reference-shot 12063 ^
      --comparison-shot 11830 ^
      --out-dir outputs\\reports

Outputs:
    outputs/reports/tokamark_cross_shot_m_edge_comparison.csv
    outputs/reports/tokamark_cross_shot_m_edge_comparison.json
    outputs/reports/tokamark_cross_shot_m_edge_comparison.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd


STATE_COLUMNS = [
    "positive_boundary_margin",
    "boundary_ambiguous_margin",
    "negative_leakage_margin",
    "insufficient_data",
]

FEATURE_COLUMNS = [
    "m_edge",
    "C_edge_capacity",
    "F_route_fragmentation",
    "S_edge_response",
    "S_power_balance",
    "S_transport",
    "density_support",
    "geometry_stability",
    "missingness_pressure",
]


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


def load_metadata_row(path: Path, shot_id: int) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        df = pd.read_csv(path)
        if "shot_id" not in df.columns:
            return {}
        df["shot_id"] = pd.to_numeric(df["shot_id"], errors="coerce").fillna(-1).astype(int)
        row = df[df["shot_id"].eq(int(shot_id))]
        if row.empty:
            return {}
        return row.iloc[0].to_dict()
    except Exception:
        return {}


def load_inspection(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {
            "missing": True,
            "error": f"missing inspection file: {path}",
            "summary": {},
            "windows": [],
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        "missing": False,
        "summary": payload.get("summary", {}),
        "windows": payload.get("windows", []),
    }


def summarize_shot(
    shot_id: int,
    probe_csv: Path,
    inspection_json: Path,
    metadata_row: Dict[str, Any],
) -> Dict[str, Any]:
    if not probe_csv.exists():
        raise FileNotFoundError(f"Missing probe CSV for shot {shot_id}: {probe_csv}")

    df = pd.read_csv(probe_csv)
    if "m_edge_state" not in df.columns:
        raise ValueError(f"Probe CSV has no m_edge_state column: {probe_csv}")

    n = len(df)
    state_counts = df["m_edge_state"].astype(str).value_counts(dropna=False).to_dict()

    out: Dict[str, Any] = {
        "shot_id": shot_id,
        "probe_csv": str(probe_csv),
        "inspection_json": str(inspection_json),
        "rows": int(n),
        "time_min": float(pd.to_numeric(df["time_s"], errors="coerce").min()) if "time_s" in df.columns else None,
        "time_max": float(pd.to_numeric(df["time_s"], errors="coerce").max()) if "time_s" in df.columns else None,
        "candidate_class": metadata_row.get("candidate_class", ""),
        "candidate_score": metadata_row.get("candidate_score", ""),
        "campaign": metadata_row.get("campaign", ""),
        "split_membership": metadata_row.get("split_membership", ""),
        "core_required_present": metadata_row.get("core_required_present", ""),
        "profile_preferred_present": metadata_row.get("profile_preferred_present", ""),
        "edge_activity_present": metadata_row.get("edge_activity_present", ""),
        "supporting_present": metadata_row.get("supporting_present", ""),
    }

    for state in STATE_COLUMNS:
        count = int(state_counts.get(state, 0))
        out[f"{state}_count"] = count
        out[f"{state}_fraction"] = float(count / max(n, 1))

    for col in FEATURE_COLUMNS:
        if col in df.columns:
            stats = finite_stats(df[col])
            for k, v in stats.items():
                out[f"{col}_{k}"] = v

    inspection = load_inspection(inspection_json)
    out["inspection_missing"] = inspection.get("missing", False)
    if inspection.get("missing"):
        out["inspection_error"] = inspection.get("error", "")

    windows = inspection.get("windows", [])
    interp_counts: Dict[str, int] = {}
    for w in windows:
        flag = str(w.get("interpretability_flag", "unknown"))
        interp_counts[flag] = interp_counts.get(flag, 0) + 1

    out["inspection_window_count"] = len(windows)
    out["interpretable_positive_count"] = int(interp_counts.get("interpretable_positive_candidate", 0))
    out["interpretable_negative_count"] = int(interp_counts.get("interpretable_negative_candidate", 0))
    out["fragile_positive_count"] = int(interp_counts.get("fragile_positive_candidate", 0))
    out["fragile_negative_count"] = int(interp_counts.get("fragile_negative_candidate", 0))
    out["weak_positive_count"] = int(interp_counts.get("weak_positive_candidate", 0))
    out["weak_negative_count"] = int(interp_counts.get("weak_negative_candidate", 0))
    out["interpretability_counts"] = json.dumps(interp_counts, sort_keys=True)

    # Aggregate inspected-window durations.
    pos_durations = [
        float(w.get("duration", 0.0))
        for w in windows
        if w.get("interpretability_flag") == "interpretable_positive_candidate"
    ]
    neg_durations = [
        float(w.get("duration", 0.0))
        for w in windows
        if w.get("interpretability_flag") == "interpretable_negative_candidate"
    ]
    out["interpretable_positive_total_duration"] = float(np.nansum(pos_durations)) if pos_durations else 0.0
    out["interpretable_negative_total_duration"] = float(np.nansum(neg_durations)) if neg_durations else 0.0

    return out


def md_table(rows: List[Dict[str, Any]], columns: List[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = []
    lines.append("| " + " | ".join(columns) + " |")
    lines.append("| " + " | ".join(["---"] * len(columns)) + " |")
    for row in rows:
        vals = []
        for c in columns:
            v = row.get(c, "")
            if isinstance(v, float):
                vals.append(f"{v:.6g}")
            else:
                vals.append(str(v))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def comparison_decision(ref: Dict[str, Any], comp: Dict[str, Any]) -> Dict[str, Any]:
    ref_pos = float(ref.get("positive_boundary_margin_fraction", 0) or 0)
    comp_pos = float(comp.get("positive_boundary_margin_fraction", 0) or 0)
    ref_interp = int(ref.get("interpretable_positive_count", 0) or 0)
    comp_interp = int(comp.get("interpretable_positive_count", 0) or 0)
    ref_mmax = ref.get("m_edge_max")
    comp_mmax = comp.get("m_edge_max")
    ref_missing = float(ref.get("missingness_pressure_median", 0) or 0)
    comp_missing = float(comp.get("missingness_pressure_median", 0) or 0)

    decision = "inconclusive"
    reasons: List[str] = []

    if ref_interp > comp_interp:
        reasons.append("reference_has_more_interpretable_positive_windows")
    elif ref_interp < comp_interp:
        reasons.append("comparison_has_more_interpretable_positive_windows")
    else:
        reasons.append("interpretable_positive_counts_equal")

    if ref_pos > comp_pos:
        reasons.append("reference_has_higher_positive_fraction")
    elif ref_pos < comp_pos:
        reasons.append("comparison_has_higher_positive_fraction")
    else:
        reasons.append("positive_fractions_equal")

    if ref_mmax is not None and comp_mmax is not None:
        try:
            if float(ref_mmax) > float(comp_mmax):
                reasons.append("reference_has_higher_peak_m_edge")
            elif float(ref_mmax) < float(comp_mmax):
                reasons.append("comparison_has_higher_peak_m_edge")
        except Exception:
            pass

    if comp_missing > ref_missing + 0.10:
        reasons.append("comparison_more_missingness_sensitive")

    if ref_interp > comp_interp and ref_pos >= comp_pos:
        decision = "reference_structurally_stronger"
    elif comp_interp >= ref_interp and comp_pos >= ref_pos:
        decision = "v0_1_may_be_overbroad_or_comparison_not_weaker"
    elif comp_missing > ref_missing + 0.20:
        decision = "comparison_limited_by_missingness"
    else:
        decision = "mixed_result_requires_trace_review"

    return {
        "decision": decision,
        "reasons": reasons,
        "delta_positive_fraction_comparison_minus_reference": comp_pos - ref_pos,
        "delta_interpretable_positive_count_comparison_minus_reference": comp_interp - ref_interp,
        "delta_missingness_median_comparison_minus_reference": comp_missing - ref_missing,
    }


def write_report(path: Path, ref: Dict[str, Any], comp: Dict[str, Any], decision: Dict[str, Any]) -> None:
    key_cols = [
        "shot_id", "candidate_class", "candidate_score",
        "positive_boundary_margin_fraction", "negative_leakage_margin_fraction",
        "boundary_ambiguous_margin_fraction", "insufficient_data_fraction",
        "m_edge_median", "m_edge_mean", "m_edge_min", "m_edge_max",
        "C_edge_capacity_median", "F_route_fragmentation_median",
        "S_edge_response_median", "S_power_balance_median", "S_transport_median",
        "missingness_pressure_median",
        "interpretable_positive_count", "interpretable_negative_count",
        "interpretable_positive_total_duration", "interpretable_negative_total_duration",
    ]
    rows = [ref, comp]
    md = []
    md.append("# TokaMark Cross-Shot m_edge(t) Comparison")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Compare the reference public TokaMark shot against a weaker / comparison candidate after both have been run through the same `m_edge(t)` and trace-inspection pipeline.")
    md.append("")
    md.append("This is the next step after `docs/20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md`.")
    md.append("")
    md.append("## Compared shots")
    md.append("")
    md.append(md_table(rows, [c for c in key_cols if c in ref or c in comp]))
    md.append("")
    md.append("## Decision")
    md.append("")
    md.append("```text")
    md.append(f"decision: {decision['decision']}")
    for reason in decision["reasons"]:
        md.append(f"- {reason}")
    md.append(f"delta positive fraction: {decision['delta_positive_fraction_comparison_minus_reference']}")
    md.append(f"delta interpretable positive count: {decision['delta_interpretable_positive_count_comparison_minus_reference']}")
    md.append(f"delta missingness median: {decision['delta_missingness_median_comparison_minus_reference']}")
    md.append("```")
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append("If the reference shot has more coherent positive windows and a stronger positive-margin distribution, shot 12063 becomes structurally more meaningful. If the comparison shot reproduces the same pattern, v0.1 may be overbroad and should be revised before further claims.")
    md.append("")
    md.append("## Bounded claim")
    md.append("")
    md.append("This comparison is still not physical H-mode validation. It tests whether the structural margin distinguishes two public TokaMark shots under the same pipeline.")
    path.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two TokaMark m_edge(t) traces.")
    parser.add_argument("--reference-shot", type=int, default=12063)
    parser.add_argument("--comparison-shot", type=int, required=True)
    parser.add_argument("--out-dir", default="outputs/reports")
    parser.add_argument("--probe-dir", default="outputs/reports")
    parser.add_argument(
        "--metadata-candidates",
        default="outputs/reports/tokamark_positive_corridor_metadata_candidates.csv",
    )
    parser.add_argument("--prefix", default="tokamark_cross_shot_m_edge_comparison")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    probe_dir = Path(args.probe_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    meta_path = Path(args.metadata_candidates)
    ref_meta = load_metadata_row(meta_path, args.reference_shot)
    comp_meta = load_metadata_row(meta_path, args.comparison_shot)

    def probe_csv(shot: int) -> Path:
        return probe_dir / f"tokamark_shot_{shot}_m_edge_t_probe.csv"

    def inspect_json(shot: int) -> Path:
        return probe_dir / f"tokamark_shot_{shot}_m_edge_trace_inspection_summary.json"

    missing = []
    for p in [probe_csv(args.reference_shot), inspect_json(args.reference_shot), probe_csv(args.comparison_shot), inspect_json(args.comparison_shot)]:
        if not p.exists():
            missing.append(str(p))

    if missing:
        msg = [
            "Missing required inputs for cross-shot comparison:",
            *[f"  {m}" for m in missing],
            "",
            "Run the same pipeline for the comparison shot first, for example:",
            f"  python components\\tokamark_one_shot_array_probe.py --shot-id {args.comparison_shot} --out-dir outputs\\reports",
            f"  python components\\tokamark_m_edge_t_probe.py --shot-id {args.comparison_shot} --out-dir outputs\\reports",
            f"  python components\\tokamark_m_edge_trace_inspector.py --input outputs\\reports\\tokamark_shot_{args.comparison_shot}_m_edge_t_probe.csv --shot-id {args.comparison_shot} --out-dir outputs\\reports",
        ]
        raise SystemExit("\n".join(msg))

    ref = summarize_shot(args.reference_shot, probe_csv(args.reference_shot), inspect_json(args.reference_shot), ref_meta)
    comp = summarize_shot(args.comparison_shot, probe_csv(args.comparison_shot), inspect_json(args.comparison_shot), comp_meta)
    decision = comparison_decision(ref, comp)

    csv_path = out_dir / f"{args.prefix}.csv"
    json_path = out_dir / f"{args.prefix}.json"
    md_path = out_dir / f"{args.prefix}.md"

    pd.DataFrame([ref, comp]).to_csv(csv_path, index=False)
    json_path.write_text(json.dumps({
        "component": "tokamark_cross_shot_m_edge_comparator.py",
        "reference": ref,
        "comparison": comp,
        "decision": decision,
    }, indent=2, default=str), encoding="utf-8")
    write_report(md_path, ref, comp, decision)

    print("Cross-shot comparison complete.")
    print(f"Reference shot:  {args.reference_shot}")
    print(f"Comparison shot: {args.comparison_shot}")
    print(f"Decision:        {decision['decision']}")
    print(f"CSV:             {csv_path}")
    print(f"JSON:            {json_path}")
    print(f"Report:          {md_path}")


if __name__ == "__main__":
    main()
