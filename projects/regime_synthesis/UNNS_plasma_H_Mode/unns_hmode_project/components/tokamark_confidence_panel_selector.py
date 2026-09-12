#!/usr/bin/env python3
"""
tokamark_confidence_panel_selector.py

UNNS-H Mode Project
Moderate balanced TokaMark confidence-panel selector.

Purpose
-------
Select a controlled, balanced 20-50 shot panel for the v0.2 diagnostic-confidence
UNNS-H Mode test.

This follows:

    docs/26_TOKAMARK_MODERATE_CONFIDENCE_PANEL_PLAN.md

The selector does NOT run the physics pipeline. It only selects the panel to be
processed next.

Default target
--------------
Select 6 shots from each class:

    FULL_PROFILE_EDGE_CANDIDATE
    PROFILE_DALPHA_CANDIDATE
    CORE_DALPHA_GEOMETRY_CANDIDATE
    PARTIAL_DALPHA_CANDIDATE
    LOW_PRIORITY

Always include calibration anchors when available:

    12063
    11830
    11876
    11768
    11776

Run from project root
---------------------

    python components\tokamark_confidence_panel_selector.py ^
      --metadata outputs\reports\tokamark_positive_corridor_metadata_candidates.csv ^
      --per-class 6 ^
      --out-dir outputs\reports

Outputs
-------

    outputs/reports/tokamark_moderate_confidence_panel_selection.csv
    outputs/reports/tokamark_moderate_confidence_panel_selection.json
    outputs/reports/tokamark_moderate_confidence_panel_selection.md

Scientific caution
------------------
This selector creates a balanced test panel. It does not validate H-mode and does
not rank physical success. It is a controlled sampling step before v0.2 is run.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


DEFAULT_CLASSES = [
    "FULL_PROFILE_EDGE_CANDIDATE",
    "PROFILE_DALPHA_CANDIDATE",
    "CORE_DALPHA_GEOMETRY_CANDIDATE",
    "PARTIAL_DALPHA_CANDIDATE",
    "LOW_PRIORITY",
]

DEFAULT_ANCHORS = [12063, 11830, 11876, 11768, 11776]

ANCHOR_ROLES = {
    12063: "reference_anchor",
    11830: "profile_no_softx_anchor",
    11876: "core_dalpha_geometry_anchor",
    11768: "partial_dalpha_anchor",
    11776: "low_priority_anchor",
}


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


def ensure_columns(df: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col not in out.columns:
            out[col] = np.nan
    return out


def norm_class(value: Any) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "UNKNOWN"
    return str(value).strip()


def as_int_list(values: Optional[Sequence[str | int]], default: List[int]) -> List[int]:
    if not values:
        return default[:]
    out: List[int] = []
    for value in values:
        try:
            out.append(int(value))
        except Exception:
            pass
    return out


def score_numeric(series: pd.Series, default: float = 0.0) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(default)


# ---------------------------------------------------------------------------
# Loading and candidate preparation
# ---------------------------------------------------------------------------

def load_metadata(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Metadata candidate CSV not found: {path}")

    df = pd.read_csv(path)

    if "shot_id" not in df.columns:
        # Common fallback names.
        for candidate in ["SHOT", "shot", "shot_number"]:
            if candidate in df.columns:
                df = df.rename(columns={candidate: "shot_id"})
                break

    if "shot_id" not in df.columns:
        raise ValueError("Metadata CSV must contain a shot_id column.")

    if "candidate_class" not in df.columns:
        raise ValueError("Metadata CSV must contain a candidate_class column.")

    df["shot_id"] = pd.to_numeric(df["shot_id"], errors="coerce")
    df = df.dropna(subset=["shot_id"]).copy()
    df["shot_id"] = df["shot_id"].astype(int)

    df["candidate_class"] = df["candidate_class"].apply(norm_class)

    if "candidate_score" not in df.columns:
        df["candidate_score"] = 0.0
    df["candidate_score"] = score_numeric(df["candidate_score"], default=0.0)

    # Deduplicate by shot id, preserving highest candidate score.
    df = df.sort_values(["shot_id", "candidate_score"], ascending=[True, False])
    df = df.drop_duplicates(subset=["shot_id"], keep="first").reset_index(drop=True)

    required = [
        "campaign",
        "split_membership",
        "core_required_present",
        "profile_preferred_present",
        "edge_activity_present",
        "supporting_present",
        "missing_core_required",
        "missing_profile_preferred",
        "missing_edge_activity",
    ]
    df = ensure_columns(df, required)

    # Numeric helper columns.
    for col in [
        "core_required_present",
        "profile_preferred_present",
        "edge_activity_present",
        "supporting_present",
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def class_target(per_class: int, panel_size: Optional[int], classes: List[str]) -> Dict[str, int]:
    if panel_size is None:
        return {cls: int(per_class) for cls in classes}

    base = max(1, int(panel_size) // max(len(classes), 1))
    remainder = max(0, int(panel_size) - base * len(classes))
    targets = {cls: base for cls in classes}

    # Put extra capacity into stronger/more complete classes first.
    for cls in classes[:remainder]:
        targets[cls] += 1

    return targets


def shot_distance_score(shot_id: int, selected_ids: Sequence[int]) -> float:
    if not selected_ids:
        return 1.0
    distances = [abs(int(shot_id) - int(s)) for s in selected_ids]
    dmin = min(distances)
    # Cap because enormous shot gaps should not dominate candidate quality.
    return min(dmin / 250.0, 1.0)


def diversity_penalty(row: pd.Series, selected_rows: pd.DataFrame) -> float:
    if selected_rows.empty:
        return 0.0

    penalty = 0.0

    # Penalize overconcentration in campaign/split when fields exist.
    for col, weight in [("campaign", 0.10), ("split_membership", 0.05)]:
        val = row.get(col, np.nan)
        if pd.notna(val) and col in selected_rows.columns:
            same = selected_rows[col].astype(str).eq(str(val)).sum()
            penalty += weight * min(same, 3)

    # Penalize adjacent shots already selected.
    shot_id = int(row["shot_id"])
    close = sum(abs(shot_id - int(s)) <= 3 for s in selected_rows["shot_id"].astype(int).tolist())
    penalty += 0.15 * close

    return penalty


def candidate_quality(row: pd.Series, selected_ids: Sequence[int], selected_rows: pd.DataFrame) -> float:
    score = float(row.get("candidate_score", 0.0) or 0.0) / 100.0

    core = row.get("core_required_present", 0.0)
    profile = row.get("profile_preferred_present", 0.0)
    edge = row.get("edge_activity_present", 0.0)
    supporting = row.get("supporting_present", 0.0)

    core_q = min(float(core) / 8.0, 1.0) if pd.notna(core) else 0.0
    profile_q = min(float(profile) / 2.0, 1.0) if pd.notna(profile) else 0.0
    edge_q = min(float(edge) / 2.0, 1.0) if pd.notna(edge) else 0.0
    support_q = min(float(supporting) / 10.0, 1.0) if pd.notna(supporting) else 0.0

    distance_q = shot_distance_score(int(row["shot_id"]), selected_ids)
    penalty = diversity_penalty(row, selected_rows)

    # Quality values favor usable data, but distance prevents selecting only a tiny cluster.
    quality = (
        0.45 * score
        + 0.20 * core_q
        + 0.12 * profile_q
        + 0.12 * edge_q
        + 0.06 * support_q
        + 0.05 * distance_q
        - penalty
    )
    return float(quality)


def select_greedy_diverse(
    pool: pd.DataFrame,
    n: int,
    selected_ids: List[int],
    selected_rows: pd.DataFrame,
) -> pd.DataFrame:
    if n <= 0 or pool.empty:
        return pool.iloc[0:0].copy()

    chosen: List[pd.Series] = []

    remaining = pool[~pool["shot_id"].astype(int).isin(set(selected_ids))].copy()
    while len(chosen) < n and not remaining.empty:
        scores = []
        current_rows = pd.concat([selected_rows, pd.DataFrame(chosen)], ignore_index=True) if chosen else selected_rows
        current_ids = selected_ids + [int(r["shot_id"]) for r in chosen]
        for idx, row in remaining.iterrows():
            scores.append((candidate_quality(row, current_ids, current_rows), idx))

        scores.sort(reverse=True, key=lambda x: x[0])
        _, best_idx = scores[0]
        best = remaining.loc[best_idx].copy()
        chosen.append(best)
        remaining = remaining.drop(index=best_idx)

    if not chosen:
        return pool.iloc[0:0].copy()

    return pd.DataFrame(chosen).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Selection logic
# ---------------------------------------------------------------------------

def select_panel(
    df: pd.DataFrame,
    *,
    classes: List[str],
    targets: Dict[str, int],
    anchors: List[int],
    include_anchors: bool = True,
    seed: int = 17,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    rng = random.Random(seed)

    selected_parts: List[pd.DataFrame] = []
    selected_ids: List[int] = []
    warnings: List[str] = []

    # Include available anchors first.
    if include_anchors:
        anchor_rows = df[df["shot_id"].astype(int).isin(anchors)].copy()
        if not anchor_rows.empty:
            anchor_rows["selection_role"] = anchor_rows["shot_id"].astype(int).map(ANCHOR_ROLES).fillna("anchor")
            anchor_rows["selection_reason"] = "predefined calibration anchor from five-shot confidence panel"
            anchor_rows["selection_class_bucket"] = anchor_rows["candidate_class"]
            selected_parts.append(anchor_rows)
            selected_ids.extend(anchor_rows["shot_id"].astype(int).tolist())

        missing_anchors = [s for s in anchors if s not in set(selected_ids)]
        if missing_anchors:
            warnings.append(f"Missing anchors not present in metadata: {missing_anchors}")

    selected_df = pd.concat(selected_parts, ignore_index=True) if selected_parts else df.iloc[0:0].copy()

    # Fill each requested class to target, counting anchors already in that class.
    for cls in classes:
        target = int(targets.get(cls, 0))
        already = selected_df[selected_df["candidate_class"].eq(cls)] if not selected_df.empty else pd.DataFrame()
        need = max(0, target - len(already))

        pool = df[df["candidate_class"].eq(cls)].copy()
        chosen = select_greedy_diverse(pool, need, selected_ids, selected_df)

        if len(chosen) < need:
            warnings.append(f"Class {cls} shortage: needed {need}, selected {len(chosen)} additional shots.")

        if not chosen.empty:
            chosen["selection_role"] = f"class_balanced_{cls}"
            chosen["selection_reason"] = f"selected to fill target bucket for {cls}"
            chosen["selection_class_bucket"] = cls
            selected_parts.append(chosen)
            selected_ids.extend(chosen["shot_id"].astype(int).tolist())
            selected_df = pd.concat(selected_parts, ignore_index=True)

    # If panel is still smaller than requested total because of class shortage,
    # fill from any remaining candidate, favoring diverse and readable.
    requested_total = sum(targets.values())
    if include_anchors:
        # Anchors count toward class targets. requested_total remains the intended panel size.
        pass

    selected_df = pd.concat(selected_parts, ignore_index=True).drop_duplicates(subset=["shot_id"], keep="first") if selected_parts else df.iloc[0:0].copy()
    selected_ids = selected_df["shot_id"].astype(int).tolist()

    if len(selected_df) < requested_total:
        need = requested_total - len(selected_df)
        remainder = df[~df["shot_id"].astype(int).isin(set(selected_ids))].copy()
        # Avoid making the panel dominated by the strongest class; fill by global quality.
        filler = select_greedy_diverse(remainder, need, selected_ids, selected_df)
        if not filler.empty:
            filler["selection_role"] = "shortage_filler"
            filler["selection_reason"] = "selected because one or more target classes had insufficient candidates"
            filler["selection_class_bucket"] = filler["candidate_class"]
            selected_df = pd.concat([selected_df, filler], ignore_index=True)
        if len(filler) < need:
            warnings.append(f"Could not fill requested panel size. Needed {requested_total}, selected {len(selected_df)}.")

    # Final ordering: anchors first in anchor order, then by class order, then score.
    anchor_order = {shot: i for i, shot in enumerate(anchors)}
    class_order = {cls: i for i, cls in enumerate(classes)}

    def sort_key(row: pd.Series) -> Tuple[int, int, float, int]:
        shot = int(row["shot_id"])
        is_anchor_sort = 0 if shot in anchor_order else 1
        anchor_idx = anchor_order.get(shot, 9999)
        cls_idx = class_order.get(str(row.get("candidate_class")), 999)
        score = -float(row.get("candidate_score", 0.0) or 0.0)
        return (is_anchor_sort, anchor_idx if is_anchor_sort == 0 else cls_idx, score, shot)

    selected_df = selected_df.copy()
    selected_df["_sort_tuple"] = selected_df.apply(sort_key, axis=1)
    selected_df = selected_df.sort_values("_sort_tuple").drop(columns=["_sort_tuple"]).reset_index(drop=True)
    selected_df["selection_order"] = np.arange(1, len(selected_df) + 1)

    # Compute class summary.
    class_summary = []
    for cls in classes:
        bucket = selected_df[selected_df["candidate_class"].eq(cls)]
        available = df[df["candidate_class"].eq(cls)]
        class_summary.append({
            "candidate_class": cls,
            "target": int(targets.get(cls, 0)),
            "available": int(len(available)),
            "selected": int(len(bucket)),
            "shortage": int(max(0, targets.get(cls, 0) - len(bucket))),
        })

    metadata = {
        "requested_targets": targets,
        "requested_total": int(requested_total),
        "selected_total": int(len(selected_df)),
        "classes": classes,
        "anchors": anchors if include_anchors else [],
        "warnings": warnings,
        "class_summary": class_summary,
    }
    return selected_df, metadata


def write_selection_report(path: Path, selected: pd.DataFrame, metadata: Dict[str, Any]) -> None:
    cols = [
        "selection_order",
        "shot_id",
        "candidate_class",
        "candidate_score",
        "selection_role",
        "selection_reason",
        "core_required_present",
        "profile_preferred_present",
        "edge_activity_present",
        "supporting_present",
        "missing_core_required",
        "missing_profile_preferred",
        "missing_edge_activity",
        "campaign",
        "split_membership",
    ]
    cols = [c for c in cols if c in selected.columns]

    class_summary = pd.DataFrame(metadata.get("class_summary", []))

    md = []
    md.append("# TokaMark Moderate Confidence Panel Selection")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Select a balanced moderate panel for the v0.2 diagnostic-confidence UNNS-H Mode test.")
    md.append("")
    md.append("## Selection summary")
    md.append("")
    md.append("```text")
    md.append(f"requested total: {metadata.get('requested_total')}")
    md.append(f"selected total: {metadata.get('selected_total')}")
    md.append(f"anchors included: {metadata.get('anchors')}")
    md.append("```")
    md.append("")
    md.append("## Class balance")
    md.append("")
    md.append(df_to_markdown(class_summary, index=False) if not class_summary.empty else "_No class summary._")
    md.append("")
    if metadata.get("warnings"):
        md.append("## Warnings")
        md.append("")
        for warning in metadata.get("warnings", []):
            md.append(f"- {warning}")
        md.append("")
    md.append("## Selected panel")
    md.append("")
    md.append(df_to_markdown(selected[cols], index=False))
    md.append("")
    md.append("## Next step")
    md.append("")
    md.append("Run the existing TokaMark array/probe/confidence pipeline on these selected shots, then report results as:")
    md.append("")
    md.append("```text")
    md.append("docs/")
    md.append("  27_TOKAMARK_MODERATE_CONFIDENCE_PANEL_RESULTS.md")
    md.append("```")
    md.append("")
    md.append("## Bounded interpretation")
    md.append("")
    md.append("This file is only a panel-selection artifact. It does not validate H-mode physically.")
    md.append("")
    path.write_text("\n".join(md), encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_class_list(raw: Optional[str]) -> List[str]:
    if not raw:
        return DEFAULT_CLASSES[:]
    classes = [x.strip() for x in raw.split(",") if x.strip()]
    return classes if classes else DEFAULT_CLASSES[:]


def main() -> None:
    parser = argparse.ArgumentParser(description="Select a balanced moderate TokaMark confidence panel.")
    parser.add_argument(
        "--metadata",
        default="outputs/reports/tokamark_positive_corridor_metadata_candidates.csv",
        help="Metadata candidate CSV from tokamark_metadata_candidate_scanner.py.",
    )
    parser.add_argument("--out-dir", default="outputs/reports", help="Output directory.")
    parser.add_argument("--per-class", type=int, default=6, help="Target shots per class.")
    parser.add_argument("--panel-size", type=int, default=None, help="Optional total panel size. Overrides per-class distribution.")
    parser.add_argument("--classes", default=None, help="Comma-separated class list. Defaults to five canonical buckets.")
    parser.add_argument("--anchors", nargs="*", default=None, help="Anchor shot IDs to force-include when available.")
    parser.add_argument("--no-anchors", action="store_true", help="Do not force include anchors.")
    parser.add_argument("--seed", type=int, default=17, help="Deterministic selection seed.")
    parser.add_argument("--prefix", default="tokamark_moderate_confidence_panel_selection", help="Output file prefix.")
    args = parser.parse_args()

    metadata_path = Path(args.metadata)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    classes = parse_class_list(args.classes)
    anchors = as_int_list(args.anchors, DEFAULT_ANCHORS)
    targets = class_target(args.per_class, args.panel_size, classes)

    df = load_metadata(metadata_path)

    selected, meta = select_panel(
        df,
        classes=classes,
        targets=targets,
        anchors=anchors,
        include_anchors=not args.no_anchors,
        seed=args.seed,
    )

    output_cols = [
        "selection_order",
        "shot_id",
        "candidate_class",
        "candidate_score",
        "selection_role",
        "selection_reason",
        "selection_class_bucket",
        "campaign",
        "split_membership",
        "core_required_present",
        "profile_preferred_present",
        "edge_activity_present",
        "supporting_present",
        "missing_core_required",
        "missing_profile_preferred",
        "missing_edge_activity",
    ]
    output_cols = [c for c in output_cols if c in selected.columns]
    selected_out = selected[output_cols].copy()

    csv_path = out_dir / f"{args.prefix}.csv"
    json_path = out_dir / f"{args.prefix}.json"
    md_path = out_dir / f"{args.prefix}.md"

    selected_out.to_csv(csv_path, index=False)
    write_json(json_path, {
        "component": "tokamark_confidence_panel_selector.py",
        "metadata_input": str(metadata_path),
        "selection_metadata": meta,
        "selected_shots": selected_out.to_dict(orient="records"),
    })
    write_selection_report(md_path, selected_out, meta)

    print("Moderate confidence panel selection complete.")
    print(f"Metadata: {metadata_path}")
    print(f"Selected total: {len(selected_out)}")
    print(f"CSV:  {csv_path}")
    print(f"JSON: {json_path}")
    print(f"MD:   {md_path}")
    print()
    print("Selected shots:")
    print(" ".join(str(int(x)) for x in selected_out["shot_id"].tolist()))
    print()
    print("Class counts:")
    for cls, count in selected_out["candidate_class"].value_counts().sort_index().items():
        print(f"  {cls}: {count}")

    if meta.get("warnings"):
        print()
        print("Warnings:")
        for warning in meta["warnings"]:
            print(f"  - {warning}")


if __name__ == "__main__":
    main()
