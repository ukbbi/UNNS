#!/usr/bin/env python3
"""
tokamark_comparison_candidate_selector.py

UNNS-H Mode Project
Select a weaker / comparison TokaMark shot from the existing metadata candidate scan.

Purpose
-------
Use the already-produced metadata candidate scan to select a comparison shot
against reference shot 12063.

This is the correct next step after:
    docs/20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md

Default input:
    outputs/reports/tokamark_positive_corridor_metadata_candidates.csv

Outputs:
    outputs/reports/tokamark_comparison_candidate_selection.csv
    outputs/reports/tokamark_comparison_candidate_selection.json
    outputs/reports/tokamark_comparison_candidate_selection.md

Run:
    python components\\tokamark_comparison_candidate_selector.py --out-dir outputs\\reports

Recommended default result on the first 200-shot scan:
    shot 11830
    PROFILE_DALPHA_CANDIDATE
    core 8/8, profiles 2/2, soft-X 0/2

This is a useful weaker comparison because it keeps core + Thomson coverage
but lacks soft-X edge-activity support.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "t"}


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(float(value))
    except Exception:
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def classify_role(row: pd.Series) -> str:
    klass = str(row.get("candidate_class", ""))
    core = safe_int(row.get("core_required_present"))
    profile = safe_int(row.get("profile_preferred_present"))
    edge = safe_int(row.get("edge_activity_present"))

    if klass == "FULL_PROFILE_EDGE_CANDIDATE":
        return "full_profile_edge_nearby_control"
    if klass == "PROFILE_DALPHA_CANDIDATE":
        return "profile_no_softx_weaker_control"
    if klass == "CORE_DALPHA_GEOMETRY_CANDIDATE":
        if core >= 8 and edge >= 2 and profile == 0:
            return "core_softx_no_profile_weaker_control"
        return "core_dalpha_geometry_weaker_control"
    if klass == "PARTIAL_DALPHA_CANDIDATE":
        return "partial_dalpha_weak_control"
    if klass == "LOW_PRIORITY":
        return "low_priority_reject_or_stress_test"
    return "unclassified"


def recommendation_priority(row: pd.Series, mode: str) -> int:
    """
    Lower number is better.
    """
    role = row["comparison_role"]
    core = safe_int(row.get("core_required_present"))
    profile = safe_int(row.get("profile_preferred_present"))
    edge = safe_int(row.get("edge_activity_present"))

    if mode == "balanced":
        # Best first weaker candidate: full core + Thomson but no soft-X.
        if role == "profile_no_softx_weaker_control":
            return 1
        if role == "core_softx_no_profile_weaker_control":
            return 2
        if role == "full_profile_edge_nearby_control":
            return 3
        if role == "partial_dalpha_weak_control":
            return 4
        return 9

    if mode == "diagnostic_complete_control":
        if role == "full_profile_edge_nearby_control":
            return 1
        if role == "profile_no_softx_weaker_control":
            return 2
        if role == "core_softx_no_profile_weaker_control":
            return 3
        return 9

    if mode == "weakest_usable":
        if core >= 7 and edge >= 1:
            if role == "partial_dalpha_weak_control":
                return 1
            if role == "core_softx_no_profile_weaker_control":
                return 2
            if role == "profile_no_softx_weaker_control":
                return 3
        return 9

    return 9


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Select a TokaMark comparison candidate from metadata scan results.")
    parser.add_argument(
        "--candidates",
        default="outputs/reports/tokamark_positive_corridor_metadata_candidates.csv",
        help="Metadata candidate scan CSV.",
    )
    parser.add_argument("--reference-shot", type=int, default=12063, help="Reference shot to exclude.")
    parser.add_argument("--out-dir", default="outputs/reports", help="Output directory.")
    parser.add_argument(
        "--mode",
        default="balanced",
        choices=["balanced", "diagnostic_complete_control", "weakest_usable"],
        help="Candidate-selection mode.",
    )
    parser.add_argument("--top-n", type=int, default=20, help="Number of candidate rows to report.")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.candidates)
    if "shot_id" not in df.columns:
        raise ValueError("Candidate CSV must contain shot_id.")

    df = df.copy()
    df["shot_id"] = df["shot_id"].apply(lambda x: safe_int(x))
    df = df[df["shot_id"] != args.reference_shot].copy()

    df["comparison_role"] = df.apply(classify_role, axis=1)
    df["selection_priority"] = df.apply(lambda r: recommendation_priority(r, args.mode), axis=1)

    # Prefer usable candidates, then lower priority number, then lower score for weaker mode,
    # then original rank.
    if args.mode == "diagnostic_complete_control":
        df = df.sort_values(["selection_priority", "rank"], ascending=[True, True])
    else:
        df = df.sort_values(["selection_priority", "candidate_score", "rank"], ascending=[True, True, True])

    recommended = df.iloc[0].to_dict()
    shortlist = df.head(args.top_n).copy()

    prefix = "tokamark_comparison_candidate_selection"
    csv_path = out_dir / f"{prefix}.csv"
    json_path = out_dir / f"{prefix}.json"
    md_path = out_dir / f"{prefix}.md"

    shortlist.to_csv(csv_path, index=False)

    payload = {
        "component": "tokamark_comparison_candidate_selector.py",
        "mode": args.mode,
        "reference_shot": args.reference_shot,
        "recommended": recommended,
        "top_n": args.top_n,
        "shortlist": shortlist.to_dict(orient="records"),
    }
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    rec_shot = int(recommended["shot_id"])
    rec_class = recommended.get("candidate_class", "")
    rec_role = recommended.get("comparison_role", "")

    columns = [
        "rank", "shot_id", "campaign", "split_membership", "candidate_score",
        "candidate_class", "comparison_role", "core_required_present",
        "profile_preferred_present", "edge_activity_present", "supporting_present",
        "missing_core_required", "missing_profile_preferred", "missing_edge_activity",
    ]

    md = []
    md.append("# TokaMark Comparison Candidate Selection")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Select the next weaker / comparison TokaMark shot to run through the same pipeline as reference shot 12063.")
    md.append("")
    md.append("This follows `docs/20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md`.")
    md.append("")
    md.append("## Recommended candidate")
    md.append("")
    md.append("```text")
    md.append(f"reference shot:      {args.reference_shot}")
    md.append(f"recommended shot:    {rec_shot}")
    md.append(f"candidate class:     {rec_class}")
    md.append(f"comparison role:     {rec_role}")
    md.append(f"candidate score:     {recommended.get('candidate_score')}")
    md.append(f"core required:       {recommended.get('core_required_present')}/{recommended.get('core_required_total')}")
    md.append(f"profile preferred:   {recommended.get('profile_preferred_present')}/{recommended.get('profile_preferred_total')}")
    md.append(f"edge activity:       {recommended.get('edge_activity_present')}/{recommended.get('edge_activity_total')}")
    md.append(f"supporting:          {recommended.get('supporting_present')}/{recommended.get('supporting_total')}")
    md.append("```")
    md.append("")
    md.append("## Why this candidate")
    md.append("")
    if rec_role == "profile_no_softx_weaker_control":
        md.append("This is the preferred first comparison because it preserves core + Thomson profile coverage but lacks soft-X edge-activity support. It is weaker than shot 12063 without being diagnostically unusable.")
    elif rec_role == "core_softx_no_profile_weaker_control":
        md.append("This is a useful weaker comparison because it preserves core + soft-X edge support but lacks Thomson profile coverage.")
    elif rec_role == "full_profile_edge_nearby_control":
        md.append("This is a diagnostic-complete nearby control. It tests whether v0.1 labels any full-profile shot as strongly positive.")
    else:
        md.append("This is a weaker or stress-test candidate. Interpret missingness carefully.")
    md.append("")
    md.append("## Run this pipeline")
    md.append("")
    md.append("```powershell")
    md.append(f"python components\\tokamark_one_shot_array_probe.py --shot-id {rec_shot} --out-dir outputs\\reports")
    md.append(f"python components\\tokamark_m_edge_t_probe.py --shot-id {rec_shot} --out-dir outputs\\reports")
    md.append(f"python components\\tokamark_m_edge_trace_inspector.py --input outputs\\reports\\tokamark_shot_{rec_shot}_m_edge_t_probe.csv --shot-id {rec_shot} --out-dir outputs\\reports")
    md.append(f"python components\\tokamark_cross_shot_m_edge_comparator.py --reference-shot {args.reference_shot} --comparison-shot {rec_shot} --out-dir outputs\\reports")
    md.append("```")
    md.append("")
    md.append("## Shortlist")
    md.append("")
    md.append(md_table(shortlist.to_dict(orient="records"), [c for c in columns if c in shortlist.columns]))
    md.append("")
    md.append("## Decision rule")
    md.append("")
    md.append("If the comparison shot reproduces the same coherent positive-window pattern as shot 12063, v0.1 is probably overbroad. If it lacks coherent positive windows or shows higher missingness/fragmentation dominance, shot 12063 becomes structurally more meaningful.")
    md_path.write_text("\n".join(md), encoding="utf-8")

    print("Comparison candidate selection complete.")
    print(f"Recommended shot: {rec_shot}")
    print(f"Candidate class:  {rec_class}")
    print(f"Role:             {rec_role}")
    print(f"CSV:              {csv_path}")
    print(f"JSON:             {json_path}")
    print(f"Report:           {md_path}")


if __name__ == "__main__":
    main()
