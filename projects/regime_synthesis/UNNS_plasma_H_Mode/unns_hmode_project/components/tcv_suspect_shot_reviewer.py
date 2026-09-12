#!/usr/bin/env python3
"""
TCV suspect-shot reviewer for the UNNS-H Mode Project.

Purpose
-------
Create a focused one-row-per-shot review table for recurrent shots identified by
fragment/isolate mapping. The script joins:

1. data/processed/tcv_lh_events_canonical.csv
2. outputs/reports/tcv_suspect_transition_families.csv

and exports a compact physical/UNNS review table suitable for the next analysis
step before running any additional chambers.

This script does not run STRUC-I or STRUC-PERC-I. It only maps already-detected
fragmentation back to TCV shot-level physical variables.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Iterable, List, Dict, Any

import numpy as np
import pandas as pd

DEFAULT_SHOTS = [69807, 68001, 69668, 69892, 66445, 68719, 69913, 67992, 68206]

REQUESTED_COLUMNS = [
    "SHOT",
    "TIME",
    "ILH",
    "P_LH_candidate_MW",
    "P_total_candidate_MW",
    "P_total_aux_candidate_MW",
    "P_loss_candidate_MW",
    "dWmhd_dt_candidate_MW",
    "Wmhd_J",
    "n_e_1e20_m3",
    "I_p_MA",
    "B_t_T",
    "q95",
    "kappa",
    "delta",
    "hydrogen_fraction_candidate",
    "helium_fraction_candidate",
    "Z_eff",
    "n_Ryter",
    "P_Ryter",
    "chi_eff_candidate",
    "divertor_signal_candidate",
    "divertor_signal_150_candidate",
    "fragment_variables",
    "fragment_count",
]

CANONICAL_MAP = {
    "SHOT": "shot_id",
    "TIME": "event_time",
    "ILH": "src_ILH",
}

NUMERIC_REVIEW_COLUMNS = [
    "P_LH_candidate_MW",
    "P_total_candidate_MW",
    "P_total_aux_candidate_MW",
    "P_loss_candidate_MW",
    "dWmhd_dt_candidate_MW",
    "Wmhd_J",
    "n_e_1e20_m3",
    "I_p_MA",
    "B_t_T",
    "q95",
    "kappa",
    "delta",
    "hydrogen_fraction_candidate",
    "helium_fraction_candidate",
    "Z_eff",
    "n_Ryter",
    "P_Ryter",
    "chi_eff_candidate",
    "divertor_signal_candidate",
    "divertor_signal_150_candidate",
]

FRAGMENT_TAG_RULES = [
    ("power_balance_branch", {"P_total_candidate_MW", "P_total_aux_candidate_MW", "P_loss_candidate_MW"}),
    ("transport_branch", {"chi_eff_candidate"}),
    ("edge_divertor_response_branch", {"divertor_signal_candidate", "divertor_signal_150_candidate"}),
    ("timing_branch", {"event_time", "TIME"}),
    ("density_threshold_branch", {"n_Ryter", "P_Ryter", "n_e_1e20_m3"}),
    ("species_branch", {"hydrogen_fraction_candidate", "helium_fraction_candidate"}),
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Create focused TCV suspect-shot review table.")
    p.add_argument(
        "--canonical",
        default="data/processed/tcv_lh_events_canonical.csv",
        help="Path to canonical TCV event table CSV.",
    )
    p.add_argument(
        "--families",
        default="outputs/reports/tcv_suspect_transition_families.csv",
        help="Path to fragment/isolate mapped transition families CSV.",
    )
    p.add_argument(
        "--out-dir",
        default="outputs/reports",
        help="Directory for review outputs.",
    )
    p.add_argument(
        "--shots",
        nargs="*",
        type=int,
        default=DEFAULT_SHOTS,
        help="Shot IDs to include. Defaults to the recurrent shots from the fragment mapping stage.",
    )
    return p.parse_args()


def ensure_file(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing {label}: {path}")


def clean_shot(x: Any) -> int | None:
    if pd.isna(x):
        return None
    try:
        return int(round(float(x)))
    except Exception:
        return None


def fmt_float(x: Any, digits: int = 6) -> str:
    if x is None or pd.isna(x):
        return ""
    try:
        v = float(x)
        if not math.isfinite(v):
            return ""
        return f"{v:.{digits}g}"
    except Exception:
        return str(x)


def semicolon_unique(values: Iterable[Any], digits: int | None = None) -> str:
    out: list[str] = []
    seen = set()
    for v in values:
        if pd.isna(v):
            continue
        if digits is not None:
            try:
                s = f"{float(v):.{digits}f}"
            except Exception:
                s = str(v)
        else:
            s = str(v)
        if s not in seen:
            seen.add(s)
            out.append(s)
    return ";".join(out)


def split_shots(s: Any) -> list[int]:
    if pd.isna(s):
        return []
    out = []
    for part in str(s).replace(",", ";").split(";"):
        part = part.strip()
        if not part:
            continue
        try:
            out.append(int(round(float(part))))
        except Exception:
            pass
    return out


def load_inputs(canonical_path: Path, families_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    ensure_file(canonical_path, "canonical CSV")
    ensure_file(families_path, "suspect transition families CSV")
    canonical = pd.read_csv(canonical_path)
    families = pd.read_csv(families_path)

    if "shot_id" not in canonical.columns:
        raise ValueError("Canonical CSV must contain 'shot_id'.")
    if "variable" not in families.columns or "involved_shots" not in families.columns:
        raise ValueError("Families CSV must contain 'variable' and 'involved_shots'.")

    canonical["SHOT_INT"] = canonical["shot_id"].map(clean_shot)
    families["INVOLVED_SHOT_LIST"] = families["involved_shots"].map(split_shots)
    return canonical, families


def collect_fragments_for_shot(families: pd.DataFrame, shot: int) -> pd.DataFrame:
    mask = families["INVOLVED_SHOT_LIST"].map(lambda xs: shot in xs)
    return families.loc[mask].copy()


def infer_fragment_tags(fragment_variables: list[str]) -> list[str]:
    var_set = set(fragment_variables)
    tags = []
    for tag, keys in FRAGMENT_TAG_RULES:
        if var_set.intersection(keys):
            tags.append(tag)
    return tags


def level_tag(value: float | None, series: pd.Series) -> str:
    if value is None or pd.isna(value):
        return "unknown"
    s = pd.to_numeric(series, errors="coerce").dropna()
    if len(s) < 4:
        return "unknown"
    q25, q75 = s.quantile([0.25, 0.75])
    if value < q25:
        return "low"
    if value > q75:
        return "high"
    return "mid"


def aggregate_shot_rows(canonical: pd.DataFrame, shot: int) -> dict[str, Any]:
    rows = canonical.loc[canonical["SHOT_INT"] == shot].copy()
    base: dict[str, Any] = {"SHOT": shot}
    if rows.empty:
        base["TIME"] = ""
        base["ILH"] = ""
        for c in NUMERIC_REVIEW_COLUMNS:
            base[c] = np.nan
        base["canonical_event_rows"] = 0
        return base

    base["TIME"] = semicolon_unique(rows["event_time"], digits=3) if "event_time" in rows.columns else ""
    base["ILH"] = semicolon_unique(rows["src_ILH"], digits=0) if "src_ILH" in rows.columns else ""
    base["canonical_event_rows"] = len(rows)
    base["event_time_min"] = pd.to_numeric(rows.get("event_time"), errors="coerce").min()
    base["event_time_max"] = pd.to_numeric(rows.get("event_time"), errors="coerce").max()

    for c in NUMERIC_REVIEW_COLUMNS:
        if c in rows.columns:
            base[c] = pd.to_numeric(rows[c], errors="coerce").mean()
        else:
            base[c] = np.nan
    return base


def build_review(canonical: pd.DataFrame, families: pd.DataFrame, shots: list[int]) -> pd.DataFrame:
    review_rows = []
    for shot in shots:
        row = aggregate_shot_rows(canonical, shot)
        frag = collect_fragments_for_shot(families, shot)
        frag_vars = sorted(set(frag["variable"].dropna().astype(str)))
        row["fragment_variables"] = ";".join(frag_vars)
        row["fragment_count"] = int(len(frag))
        row["fragment_subsets"] = semicolon_unique(frag.get("subset", pd.Series(dtype=object)))
        row["fragment_roles"] = semicolon_unique(frag.get("component_role", pd.Series(dtype=object)))
        row["fragment_component_ids"] = semicolon_unique(frag.get("component_id", pd.Series(dtype=object)))
        row["fragment_tags"] = ";".join(infer_fragment_tags(frag_vars))

        # Relative position tags, useful for quick physical review.
        row["P_total_level"] = level_tag(row.get("P_total_candidate_MW"), canonical.get("P_total_candidate_MW", pd.Series(dtype=float)))
        row["P_loss_level"] = level_tag(row.get("P_loss_candidate_MW"), canonical.get("P_loss_candidate_MW", pd.Series(dtype=float)))
        row["n_e_level"] = level_tag(row.get("n_e_1e20_m3"), canonical.get("n_e_1e20_m3", pd.Series(dtype=float)))
        row["helium_fraction_level"] = level_tag(row.get("helium_fraction_candidate"), canonical.get("helium_fraction_candidate", pd.Series(dtype=float)))
        row["chi_eff_level"] = level_tag(row.get("chi_eff_candidate"), canonical.get("chi_eff_candidate", pd.Series(dtype=float)))
        row["divertor_signal_level"] = level_tag(row.get("divertor_signal_candidate"), canonical.get("divertor_signal_candidate", pd.Series(dtype=float)))

        review_rows.append(row)

    df = pd.DataFrame(review_rows)

    # Stable order: requested columns first, then helper columns.
    helper_cols = [
        "canonical_event_rows",
        "event_time_min",
        "event_time_max",
        "fragment_subsets",
        "fragment_roles",
        "fragment_component_ids",
        "fragment_tags",
        "P_total_level",
        "P_loss_level",
        "n_e_level",
        "helium_fraction_level",
        "chi_eff_level",
        "divertor_signal_level",
    ]
    cols = [c for c in REQUESTED_COLUMNS if c in df.columns] + [c for c in helper_cols if c in df.columns]
    return df[cols]


def summarize_review(review: pd.DataFrame) -> dict[str, Any]:
    var_counts: Dict[str, int] = {}
    tag_counts: Dict[str, int] = {}
    for _, r in review.iterrows():
        for v in str(r.get("fragment_variables", "")).split(";"):
            v = v.strip()
            if v:
                var_counts[v] = var_counts.get(v, 0) + 1
        for t in str(r.get("fragment_tags", "")).split(";"):
            t = t.strip()
            if t:
                tag_counts[t] = tag_counts.get(t, 0) + 1
    top_shots = review.sort_values(["fragment_count", "SHOT"], ascending=[False, True])[["SHOT", "fragment_count", "fragment_variables", "fragment_tags"]]
    return {
        "shot_count": int(len(review)),
        "shots": [int(x) for x in review["SHOT"].tolist()],
        "fragment_variable_counts": dict(sorted(var_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "fragment_tag_counts": dict(sorted(tag_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "top_shots": top_shots.to_dict(orient="records"),
    }


def write_markdown(review: pd.DataFrame, summary: dict[str, Any], out_path: Path) -> None:
    lines: list[str] = []
    lines.append("# TCV Suspect Shot Review")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append("This report creates a focused one-row-per-shot review table for the recurrent TCV shots identified by the fragment/isolate mapping stage. It does not run another chamber. It maps previously detected fragmentation back to physical shot variables.")
    lines.append("")
    lines.append("## Reviewed shots")
    lines.append("")
    lines.append(", ".join(str(s) for s in summary["shots"]))
    lines.append("")
    lines.append("## Fragment-variable recurrence")
    lines.append("")
    lines.append("| Fragment variable | Shot count |")
    lines.append("|---|---:|")
    for var, count in summary["fragment_variable_counts"].items():
        lines.append(f"| `{var}` | {count} |")
    lines.append("")
    lines.append("## Preliminary branch tags")
    lines.append("")
    lines.append("| Branch tag | Shot count |")
    lines.append("|---|---:|")
    for tag, count in summary["fragment_tag_counts"].items():
        lines.append(f"| `{tag}` | {count} |")
    lines.append("")
    lines.append("## Focused shot table")
    lines.append("")
    display_cols = [
        "SHOT", "TIME", "canonical_event_rows", "fragment_count", "fragment_variables", "fragment_tags",
        "P_LH_candidate_MW", "P_total_candidate_MW", "P_loss_candidate_MW", "n_e_1e20_m3",
        "helium_fraction_candidate", "chi_eff_candidate", "divertor_signal_candidate",
    ]
    md = review[display_cols].copy()
    for c in NUMERIC_REVIEW_COLUMNS:
        if c in md.columns:
            md[c] = md[c].map(lambda x: fmt_float(x, 6))
    lines.append(md.to_markdown(index=False))
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The reviewed shots form a concentrated candidate set. Most are not isolated through geometry alone; they are recurrently linked to power-balance, transport, timing, and edge/divertor-response variables. This is consistent with the working UNNS-H Mode hypothesis that H-mode access is a boundary-route organization problem rather than a single total-power threshold problem.")
    lines.append("")
    lines.append("## Caution")
    lines.append("")
    lines.append("This table identifies candidate transition families. It does not prove that these shots are faulty, anomalous, or physically causal. The next step is manual physical review of the rows and, if needed, dataset-specific diagnostics from the source notebook/README.")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    canonical_path = Path(args.canonical)
    families_path = Path(args.families)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    canonical, families = load_inputs(canonical_path, families_path)
    review = build_review(canonical, families, args.shots)
    summary = summarize_review(review)

    csv_path = out_dir / "tcv_suspect_shot_review.csv"
    json_path = out_dir / "tcv_suspect_shot_review_summary.json"
    md_path = out_dir / "tcv_suspect_shot_review.md"

    review.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_markdown(review, summary, md_path)

    print("Suspect shot review complete.")
    print(f"  CSV:     {csv_path}")
    print(f"  Report:  {md_path}")
    print(f"  Summary: {json_path}")


if __name__ == "__main__":
    main()
