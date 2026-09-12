#!/usr/bin/env python3
"""
edge_event_model_validator.py

UNNS-H Mode Project
Event-level edge-admissibility model validator.

Purpose
-------
Validate the first event-level UNNS-H Mode model:

    m_edge_event = C_edge_capacity - F_route_fragmentation

This validator does not run STRUC-I or STRUC-PERC-I. It reads the model
scores already produced by edge_admissibility_event_model.py and checks whether
the resulting event-level margin separates the reviewed TCV shots into coherent
corridors.

Expected inputs
---------------
Required:
    outputs/reports/tcv_edge_event_model_scores.csv

Optional:
    data/processed/tcv_lh_events_canonical.csv
    outputs/reports/tcv_suspect_shot_review.csv

Expected outputs
----------------
    outputs/reports/tcv_edge_event_model_validation.csv
    outputs/reports/tcv_edge_event_model_validation.md
    outputs/reports/tcv_edge_event_model_validation_summary.json

Typical use from project root
-----------------------------
PowerShell:

    python components\\edge_event_model_validator.py ^
      --scores outputs\\reports\\tcv_edge_event_model_scores.csv ^
      --canonical data\\processed\\tcv_lh_events_canonical.csv ^
      --shot-review outputs\\reports\\tcv_suspect_shot_review.csv ^
      --out-dir outputs\\reports

Unix/macOS:

    python components/edge_event_model_validator.py \\
      --scores outputs/reports/tcv_edge_event_model_scores.csv \\
      --canonical data/processed/tcv_lh_events_canonical.csv \\
      --shot-review outputs/reports/tcv_suspect_shot_review.csv \\
      --out-dir outputs/reports
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import pandas as pd


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PRESSURE_TERMS = ["S_power_balance", "S_transport", "S_timing"]
CAPACITY_TERMS = [
    "S_edge_response",
    "density_support_percentile",
    "species_position_percentile",
    "geometry_stability",
]

EXPECTED_SCORE_COLUMNS = [
    "SHOT",
    "ILH",
    "fragment_tags",
    "formal_corridor",
    "m_edge_state",
    "m_edge_event",
    "C_edge_capacity",
    "F_route_fragmentation",
    "S_power_balance",
    "S_transport",
    "S_edge_response",
    "S_timing",
]

STATE_ORDER = {
    "negative_leakage_margin": 0,
    "boundary_ambiguous_margin": 1,
    "positive_boundary_margin": 2,
}


def split_semicolon(value: Any) -> List[str]:
    """Split a semicolon-separated field into clean tokens."""
    if value is None:
        return []
    if isinstance(value, float) and math.isnan(value):
        return []
    text = str(value).strip()
    if not text:
        return []
    return [item.strip() for item in text.split(";") if item.strip()]


def safe_float(value: Any, default: float = float("nan")) -> float:
    try:
        if value is None:
            return default
        if isinstance(value, str) and not value.strip():
            return default
        return float(value)
    except Exception:
        return default


def classify_ilh(value: Any) -> str:
    """Normalize ILH state. Handles values like 1, 0, '1;0'."""
    tokens = split_semicolon(value)
    if not tokens:
        tokens = [str(value).strip()] if str(value).strip() else []
    cleaned = set()
    for tok in tokens:
        try:
            cleaned.add(str(int(float(tok))))
        except Exception:
            cleaned.add(tok)
    if cleaned == {"1"}:
        return "ILH_1"
    if cleaned == {"0"}:
        return "ILH_0"
    if cleaned == {"0", "1"} or cleaned == {"1", "0"}:
        return "ILH_mixed"
    if not cleaned:
        return "ILH_unknown"
    return "ILH_other"


def dominant_term(row: pd.Series, terms: Iterable[str]) -> Tuple[str, float]:
    """Return the highest-valued term name and value."""
    best_name = ""
    best_val = float("-inf")
    for term in terms:
        val = safe_float(row.get(term))
        if math.isnan(val):
            continue
        if val > best_val:
            best_name, best_val = term, val
    if best_name == "":
        return "", float("nan")
    return best_name, best_val


def margin_support_level(margin: float) -> str:
    """Human-readable confidence band for event-level margin."""
    if math.isnan(margin):
        return "missing"
    if margin <= -0.50:
        return "strong_negative"
    if margin < -0.10:
        return "moderate_negative"
    if margin <= 0.10:
        return "ambiguous_boundary"
    if margin < 0.50:
        return "moderate_positive"
    return "strong_positive"


def validation_note(row: pd.Series) -> str:
    """Create a compact per-shot validation note."""
    shot = row.get("SHOT")
    margin = safe_float(row.get("m_edge_event"))
    state = str(row.get("m_edge_state", ""))
    dominant_pressure = row.get("dominant_fragmentation_term", "")
    dominant_capacity = row.get("dominant_capacity_term", "")
    tags = split_semicolon(row.get("fragment_tags"))

    if state == "negative_leakage_margin":
        return (
            f"SHOT {shot}: leakage-like event; route-fragmentation exceeds "
            f"edge capacity. Dominant pressure: {dominant_pressure}; "
            f"dominant capacity term: {dominant_capacity}; m={margin:.3f}."
        )
    if state == "positive_boundary_margin":
        return (
            f"SHOT {shot}: positive boundary-response event; edge capacity exceeds "
            f"fragmentation pressure. Dominant capacity: {dominant_capacity}; "
            f"m={margin:.3f}."
        )
    if state == "boundary_ambiguous_margin":
        return (
            f"SHOT {shot}: boundary-ambiguous event; margin is close to zero. "
            f"Dominant pressure: {dominant_pressure}; dominant capacity: "
            f"{dominant_capacity}; m={margin:.3f}."
        )
    return f"SHOT {shot}: unclassified model state; tags={';'.join(tags)}; m={margin:.3f}."


def require_columns(df: pd.DataFrame, columns: List[str], label: str) -> List[str]:
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(
            f"{label} is missing required columns: {missing}\n"
            f"Available columns: {list(df.columns)}"
        )
    return missing


def summarize_numeric_group(df: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
    if group_col not in df.columns or value_col not in df.columns:
        return pd.DataFrame()
    out = (
        df.groupby(group_col, dropna=False)[value_col]
        .agg(["count", "mean", "median", "min", "max", "std"])
        .reset_index()
    )
    return out


def compact_records(df: pd.DataFrame, max_rows: Optional[int] = None) -> List[Dict[str, Any]]:
    if df is None or df.empty:
        return []
    if max_rows is not None:
        df = df.head(max_rows)
    return json.loads(df.to_json(orient="records"))


def state_separation_test(df: pd.DataFrame) -> Dict[str, Any]:
    """Check whether state margins are strictly ordered."""
    result: Dict[str, Any] = {"status": "INSUFFICIENT", "details": {}}
    if "m_edge_state" not in df.columns or "m_edge_event" not in df.columns:
        result["details"]["reason"] = "required columns missing"
        return result

    ranges: Dict[str, Dict[str, float]] = {}
    for state, part in df.groupby("m_edge_state"):
        vals = pd.to_numeric(part["m_edge_event"], errors="coerce").dropna()
        if vals.empty:
            continue
        ranges[str(state)] = {
            "count": int(vals.shape[0]),
            "min": float(vals.min()),
            "max": float(vals.max()),
            "mean": float(vals.mean()),
        }

    result["details"]["ranges"] = ranges

    required = [
        "negative_leakage_margin",
        "boundary_ambiguous_margin",
        "positive_boundary_margin",
    ]
    if not all(s in ranges for s in required):
        result["status"] = "PARTIAL"
        result["details"]["reason"] = "not all three model states are present"
        return result

    neg_max = ranges["negative_leakage_margin"]["max"]
    amb_min = ranges["boundary_ambiguous_margin"]["min"]
    amb_max = ranges["boundary_ambiguous_margin"]["max"]
    pos_min = ranges["positive_boundary_margin"]["min"]

    if neg_max < amb_min and amb_max < pos_min:
        result["status"] = "PASS_STRICT_ORDERING"
    elif neg_max < pos_min:
        result["status"] = "PASS_COARSE_ORDERING"
    else:
        result["status"] = "FAIL_OVERLAP"

    result["details"]["ordering_check"] = {
        "negative_max": neg_max,
        "ambiguous_min": amb_min,
        "ambiguous_max": amb_max,
        "positive_min": pos_min,
    }
    return result


def branch_pattern_table(df: pd.DataFrame) -> pd.DataFrame:
    """Explode fragment_tags and summarize m_edge_event + scores by branch."""
    rows: List[Dict[str, Any]] = []
    for _, row in df.iterrows():
        tags = split_semicolon(row.get("fragment_tags"))
        if not tags:
            tags = ["untagged"]
        for tag in tags:
            rec = {
                "branch_tag": tag,
                "SHOT": row.get("SHOT"),
                "m_edge_event": safe_float(row.get("m_edge_event")),
                "C_edge_capacity": safe_float(row.get("C_edge_capacity")),
                "F_route_fragmentation": safe_float(row.get("F_route_fragmentation")),
                "S_power_balance": safe_float(row.get("S_power_balance")),
                "S_transport": safe_float(row.get("S_transport")),
                "S_edge_response": safe_float(row.get("S_edge_response")),
                "S_timing": safe_float(row.get("S_timing")),
            }
            rows.append(rec)
    exploded = pd.DataFrame(rows)
    if exploded.empty:
        return pd.DataFrame()

    agg = (
        exploded.groupby("branch_tag")
        .agg(
            shot_count=("SHOT", "nunique"),
            mean_m_edge_event=("m_edge_event", "mean"),
            min_m_edge_event=("m_edge_event", "min"),
            max_m_edge_event=("m_edge_event", "max"),
            mean_C_edge_capacity=("C_edge_capacity", "mean"),
            mean_F_route_fragmentation=("F_route_fragmentation", "mean"),
            mean_S_power_balance=("S_power_balance", "mean"),
            mean_S_transport=("S_transport", "mean"),
            mean_S_edge_response=("S_edge_response", "mean"),
            mean_S_timing=("S_timing", "mean"),
        )
        .reset_index()
        .sort_values(["mean_m_edge_event", "branch_tag"])
    )
    return agg


def make_validation_table(scores: pd.DataFrame) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []

    for _, row in scores.iterrows():
        dominant_pressure, dominant_pressure_val = dominant_term(row, PRESSURE_TERMS)
        dominant_capacity, dominant_capacity_val = dominant_term(row, CAPACITY_TERMS)

        tags = split_semicolon(row.get("fragment_tags"))
        fragment_count = safe_float(row.get("fragment_count"), default=0)

        out = dict(row)
        out["ILH_category"] = classify_ilh(row.get("ILH"))
        out["branch_tag_count"] = len(tags)
        out["dominant_fragmentation_term"] = dominant_pressure
        out["dominant_fragmentation_value"] = dominant_pressure_val
        out["dominant_capacity_term"] = dominant_capacity
        out["dominant_capacity_value"] = dominant_capacity_val
        out["margin_support_level"] = margin_support_level(safe_float(row.get("m_edge_event")))
        out["abs_margin"] = abs(safe_float(row.get("m_edge_event")))
        out["is_boundary_ambiguous"] = out["margin_support_level"] == "ambiguous_boundary"
        out["is_mixed_ilh"] = out["ILH_category"] == "ILH_mixed"
        out["validation_note"] = validation_note(pd.Series(out))
        rows.append(out)

    validation = pd.DataFrame(rows)

    preferred_order = [
        "SHOT",
        "TIME",
        "ILH",
        "ILH_category",
        "fragment_tags",
        "formal_corridor",
        "m_edge_state",
        "m_edge_event",
        "C_edge_capacity",
        "F_route_fragmentation",
        "S_power_balance",
        "S_transport",
        "S_edge_response",
        "S_timing",
        "density_support_percentile",
        "species_position_percentile",
        "geometry_stability",
        "dominant_fragmentation_term",
        "dominant_fragmentation_value",
        "dominant_capacity_term",
        "dominant_capacity_value",
        "margin_support_level",
        "abs_margin",
        "is_boundary_ambiguous",
        "is_mixed_ilh",
        "validation_note",
    ]
    ordered = [c for c in preferred_order if c in validation.columns]
    rest = [c for c in validation.columns if c not in ordered]
    return validation[ordered + rest]


def markdown_table(df: pd.DataFrame, columns: Optional[List[str]] = None, max_rows: Optional[int] = None) -> str:
    if df is None or df.empty:
        return "_No rows._"
    view = df.copy()
    if columns:
        view = view[[c for c in columns if c in view.columns]]
    if max_rows:
        view = view.head(max_rows)
    return view.to_markdown(index=False)


def build_markdown_report(
    validation: pd.DataFrame,
    state_summary: pd.DataFrame,
    branch_summary: pd.DataFrame,
    ilh_summary: pd.DataFrame,
    summary: Dict[str, Any],
) -> str:
    sep_status = summary.get("state_separation", {}).get("status", "UNKNOWN")
    ambiguous = validation[validation.get("is_boundary_ambiguous", False) == True]
    mixed_ilh = validation[validation.get("is_mixed_ilh", False) == True]

    top_cols = [
        "SHOT",
        "ILH",
        "m_edge_event",
        "m_edge_state",
        "formal_corridor",
        "dominant_fragmentation_term",
        "dominant_capacity_term",
        "margin_support_level",
    ]

    text = f"""# TCV Edge-Event Model Validation

## Purpose

This report validates the first event-level UNNS-H Mode model:

```text
m_edge_event = C_edge_capacity - F_route_fragmentation
```

The validator does not run another chamber. It tests whether the already computed
edge-event scores separate the reviewed TCV suspect shots into meaningful
corridors.

## Validation status

```text
state_separation: {sep_status}
reviewed_shots: {int(validation.shape[0])}
ambiguous_shots: {int(ambiguous.shape[0])}
mixed_ILH_shots: {int(mixed_ilh.shape[0])}
```

## Main validation table

{markdown_table(validation, top_cols)}

## State-level margin summary

{markdown_table(state_summary)}

## Branch-family score patterns

{markdown_table(branch_summary)}

## ILH-category summary

{markdown_table(ilh_summary)}

## Ambiguous shots

{markdown_table(ambiguous, top_cols)}

## Mixed-ILH shots

{markdown_table(mixed_ilh, top_cols)}

## Interpretation

The key validation question is whether the formal event margin separates the
shot families into coherent corridors instead of merely restating the raw branch
labels.

A strict ordering pass means:

```text
max(negative leakage margin) < min(boundary ambiguous margin)
and
max(boundary ambiguous margin) < min(positive boundary margin)
```

A coarse ordering pass means the negative and positive corridors separate, but
the boundary-ambiguous zone may overlap with one side.

## Caution

This validation is still internal to the first TCV event-level pilot. It does
not yet prove the physical origin of H-mode, and it does not replace
time-series validation using edge turbulence, radial electric field, E×B shear,
pedestal evolution, confinement time, or ELM timing.

The result should be treated as validation of the first event-level
edge-admissibility model only.
"""
    return text


def validate(
    scores_path: Path,
    canonical_path: Optional[Path],
    shot_review_path: Optional[Path],
    out_dir: Path,
    prefix: str,
) -> Dict[str, Path]:
    if not scores_path.exists():
        raise FileNotFoundError(f"Scores file not found: {scores_path}")

    out_dir.mkdir(parents=True, exist_ok=True)

    scores = pd.read_csv(scores_path)
    require_columns(scores, EXPECTED_SCORE_COLUMNS, "edge-event scores")

    # Optional sources are loaded for metadata/warnings, not for core validation.
    source_notes: List[str] = []
    if canonical_path is not None:
        if canonical_path.exists():
            canonical = pd.read_csv(canonical_path)
            source_notes.append(f"Loaded canonical table: {canonical_path} ({canonical.shape[0]} rows)")
        else:
            source_notes.append(f"Canonical table not found: {canonical_path}")
    if shot_review_path is not None:
        if shot_review_path.exists():
            shot_review = pd.read_csv(shot_review_path)
            source_notes.append(f"Loaded shot-review table: {shot_review_path} ({shot_review.shape[0]} rows)")
        else:
            source_notes.append(f"Shot-review table not found: {shot_review_path}")

    validation = make_validation_table(scores)

    # Sort by margin so the corridor separation is visible.
    validation = validation.sort_values(["m_edge_event", "SHOT"], ascending=[True, True])

    state_summary = summarize_numeric_group(validation, "m_edge_state", "m_edge_event")
    if not state_summary.empty:
        state_summary["state_order"] = state_summary["m_edge_state"].map(STATE_ORDER).fillna(99)
        state_summary = state_summary.sort_values(["state_order", "m_edge_state"]).drop(columns=["state_order"])

    corridor_summary = summarize_numeric_group(validation, "formal_corridor", "m_edge_event")
    branch_summary = branch_pattern_table(validation)
    ilh_summary = summarize_numeric_group(validation, "ILH_category", "m_edge_event")

    state_sep = state_separation_test(validation)

    dominance_counts = {
        "dominant_fragmentation_term": validation["dominant_fragmentation_term"].value_counts(dropna=False).to_dict()
        if "dominant_fragmentation_term" in validation.columns else {},
        "dominant_capacity_term": validation["dominant_capacity_term"].value_counts(dropna=False).to_dict()
        if "dominant_capacity_term" in validation.columns else {},
        "m_edge_state": validation["m_edge_state"].value_counts(dropna=False).to_dict()
        if "m_edge_state" in validation.columns else {},
        "ILH_category": validation["ILH_category"].value_counts(dropna=False).to_dict()
        if "ILH_category" in validation.columns else {},
    }

    summary = {
        "validator": "edge_event_model_validator.py",
        "model": "m_edge_event = C_edge_capacity - F_route_fragmentation",
        "scores_file": str(scores_path),
        "source_notes": source_notes,
        "shot_count": int(validation.shape[0]),
        "state_separation": state_sep,
        "dominance_counts": dominance_counts,
        "state_summary": compact_records(state_summary),
        "corridor_summary": compact_records(corridor_summary),
        "branch_summary": compact_records(branch_summary),
        "ILH_summary": compact_records(ilh_summary),
        "ambiguous_shots": compact_records(
            validation[validation["is_boundary_ambiguous"] == True][
                [c for c in ["SHOT", "ILH", "m_edge_event", "m_edge_state", "formal_corridor"] if c in validation.columns]
            ]
        ),
        "mixed_ILH_shots": compact_records(
            validation[validation["is_mixed_ilh"] == True][
                [c for c in ["SHOT", "ILH", "m_edge_event", "m_edge_state", "formal_corridor"] if c in validation.columns]
            ]
        ),
    }

    csv_out = out_dir / f"{prefix}.csv"
    md_out = out_dir / f"{prefix}.md"
    json_out = out_dir / f"{prefix}_summary.json"

    validation.to_csv(csv_out, index=False)
    md_out.write_text(
        build_markdown_report(validation, state_summary, branch_summary, ilh_summary, summary),
        encoding="utf-8",
    )
    json_out.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    return {"csv": csv_out, "markdown": md_out, "json": json_out}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate the UNNS-H Mode event-level edge-admissibility model."
    )
    parser.add_argument(
        "--scores",
        default="outputs/reports/tcv_edge_event_model_scores.csv",
        help="Path to tcv_edge_event_model_scores.csv.",
    )
    parser.add_argument(
        "--canonical",
        default="data/processed/tcv_lh_events_canonical.csv",
        help="Optional path to canonical TCV event table.",
    )
    parser.add_argument(
        "--shot-review",
        default="outputs/reports/tcv_suspect_shot_review.csv",
        help="Optional path to suspect-shot review table.",
    )
    parser.add_argument(
        "--out-dir",
        default="outputs/reports",
        help="Directory for validation outputs.",
    )
    parser.add_argument(
        "--prefix",
        default="tcv_edge_event_model_validation",
        help="Output filename prefix.",
    )

    args = parser.parse_args()

    outputs = validate(
        scores_path=Path(args.scores),
        canonical_path=Path(args.canonical) if args.canonical else None,
        shot_review_path=Path(args.shot_review) if args.shot_review else None,
        out_dir=Path(args.out_dir),
        prefix=args.prefix,
    )

    print("Edge-event model validation complete.")
    print(f"CSV:     {outputs['csv']}")
    print(f"Report:  {outputs['markdown']}")
    print(f"Summary: {outputs['json']}")


if __name__ == "__main__":
    main()
