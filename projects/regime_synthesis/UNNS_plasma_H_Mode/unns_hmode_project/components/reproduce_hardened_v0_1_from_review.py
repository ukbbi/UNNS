#!/usr/bin/env python3
"""
reproduce_hardened_v0_1_from_review.py

UNNS-H Mode Project
Deterministic reproduction script for the conservative hardened-label file.

Purpose
-------
Reproduce:

    outputs/reports/tokamark_physical_window_labels_HARDENED_v0_1.csv

from:

    outputs/reports/tokamark_physical_window_labels_HARDENING_REVIEW.csv

using the exact conservative v0.1 hardening rule documented in:

    docs/31A_REPRODUCIBILITY_PROTOCOL_HARDENED_LABELS.md

This script reproduces the HARDENED v0.1 label file.
It does not independently validate H-mode.
It does not replace expert/manual plasma-regime labeling.

Conservative v0.1 hardening rule
--------------------------------
1. Accept only rows where:
       original_label_type in {L_MODE, LH_TRANSITION}
       review_decision == ACCEPT

2. Keep all H_MODE_STABLE rows excluded as:
       review_decision = NEEDS_EXTERNAL_REFERENCE
       hardening_level = 0_PROVISIONAL

3. Keep all AMBIGUOUS rows excluded.

4. Keep all UNLABELABLE rows excluded.

5. Do not use any UNNS audit-only column to accept or reject physical labels:
       m_edge_conf_median_AUDIT_ONLY
       conf_positive_fraction_AUDIT_ONLY
       conf_negative_fraction_AUDIT_ONLY

Run from project root
---------------------

    python components\\reproduce_hardened_v0_1_from_review.py ^
      --review outputs\\reports\\tokamark_physical_window_labels_HARDENING_REVIEW.csv ^
      --out-dir outputs\\reports

Outputs
-------

    outputs/reports/tokamark_physical_window_labels_HARDENED_v0_1.csv
    outputs/reports/tokamark_physical_window_labels_HARDENED_v0_1_summary.json
    outputs/reports/tokamark_physical_window_labels_HARDENED_v0_1_SUMMARY.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pandas as pd
import numpy as np


OUTPUT_BASENAME = "tokamark_physical_window_labels_HARDENED_v0_1"


FRONT_COLUMNS = [
    "shot_id",
    "window_id",
    "label_type",
    "hardened_label_type",
    "original_label_type",
    "t_start",
    "t_end",
    "label_confidence",
    "hardening_level",
    "review_decision",
    "excluded_from_validation",
    "exclusion_reason",
    "dalpha_evidence",
    "profile_evidence",
    "softx_evidence",
    "power_density_context",
    "external_reference",
    "reviewer_notes",
    "hardening_pass",
    "hardening_basis",
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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_bool_string(value: Any) -> str:
    """Normalize validation flags to literal True/False strings for reproducibility."""
    if isinstance(value, bool):
        return "True" if value else "False"
    if value is None:
        return "False"
    try:
        if pd.isna(value):
            return "False"
    except Exception:
        pass
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return "True"
    if text in {"false", "0", "no", "n", ""}:
        return "False"
    return "True" if bool(value) else "False"


def ensure_required_columns(df: pd.DataFrame) -> None:
    required = [
        "shot_id",
        "window_id",
        "original_label_type",
        "hardened_label_type",
        "t_start",
        "t_end",
        "label_confidence",
        "hardening_level",
        "review_decision",
        "excluded_from_validation",
        "exclusion_reason",
    ]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Review CSV is missing required columns: {missing}")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def reproduce_hardened(review: pd.DataFrame) -> pd.DataFrame:
    ensure_required_columns(review)

    out = review.copy()

    for col in [
        "original_label_type",
        "hardened_label_type",
        "review_decision",
        "hardening_level",
        "label_confidence",
        "exclusion_reason",
    ]:
        if col in out.columns:
            out[col] = out[col].apply(normalize_text)

    out["original_label_type"] = out["original_label_type"].str.upper()
    out["hardened_label_type"] = out["hardened_label_type"].str.upper()
    out["review_decision"] = out["review_decision"].str.upper()
    out["hardening_level"] = out["hardening_level"].str.upper()

    # Analyzer compatibility: label_type column must exist.
    out["label_type"] = out["hardened_label_type"].astype(str)

    for idx, row in out.iterrows():
        original_label = str(row.get("original_label_type", "")).strip().upper()
        review_decision = str(row.get("review_decision", "")).strip().upper()

        if original_label == "UNLABELABLE" or review_decision == "KEEP_UNLABELABLE":
            out.at[idx, "hardened_label_type"] = "UNLABELABLE"
            out.at[idx, "label_type"] = "UNLABELABLE"
            out.at[idx, "hardening_level"] = "0_PROVISIONAL"
            out.at[idx, "review_decision"] = "KEEP_UNLABELABLE"
            out.at[idx, "excluded_from_validation"] = "True"
            if not normalize_text(row.get("exclusion_reason")):
                out.at[idx, "exclusion_reason"] = "unlabelable due to insufficient independent diagnostics"

        elif original_label == "AMBIGUOUS" or review_decision == "KEEP_AMBIGUOUS":
            out.at[idx, "hardened_label_type"] = "AMBIGUOUS"
            out.at[idx, "label_type"] = "AMBIGUOUS"
            out.at[idx, "hardening_level"] = "0_PROVISIONAL"
            out.at[idx, "review_decision"] = "KEEP_AMBIGUOUS"
            out.at[idx, "excluded_from_validation"] = "True"
            if not normalize_text(row.get("exclusion_reason")):
                out.at[idx, "exclusion_reason"] = "ambiguous pending stronger physical review"

        elif original_label == "H_MODE_STABLE":
            out.at[idx, "hardened_label_type"] = "H_MODE_STABLE"
            out.at[idx, "label_type"] = "H_MODE_STABLE"
            out.at[idx, "hardening_level"] = "0_PROVISIONAL"
            out.at[idx, "review_decision"] = "NEEDS_EXTERNAL_REFERENCE"
            out.at[idx, "excluded_from_validation"] = "True"
            out.at[idx, "exclusion_reason"] = (
                "H_MODE_STABLE not hardened: requires independent confirmation from D-alpha/profile/soft-X "
                "or external timing; not accepted from post-transition quiet interval alone"
            )
            out.at[idx, "label_confidence"] = "low"

        elif original_label in {"L_MODE", "LH_TRANSITION"} and review_decision == "ACCEPT":
            out.at[idx, "hardened_label_type"] = original_label
            out.at[idx, "label_type"] = original_label
            out.at[idx, "review_decision"] = "ACCEPT"
            out.at[idx, "hardening_level"] = "1_PLAUSIBLE" if original_label == "LH_TRANSITION" else (
                "1_PLAUSIBLE" if str(row.get("hardening_level", "")).strip().upper() == "1_PLAUSIBLE" else "0_PROVISIONAL"
            )
            out.at[idx, "excluded_from_validation"] = "False"
            out.at[idx, "exclusion_reason"] = ""
            if not normalize_text(row.get("label_confidence")):
                out.at[idx, "label_confidence"] = "moderate"

        else:
            # Fail-closed behavior: unexpected rows remain excluded.
            label = original_label if original_label else "AMBIGUOUS"
            if label not in {"L_MODE", "LH_TRANSITION", "H_MODE_STABLE", "AMBIGUOUS", "UNLABELABLE", "REJECTED"}:
                label = "AMBIGUOUS"
            out.at[idx, "hardened_label_type"] = label
            out.at[idx, "label_type"] = label
            out.at[idx, "review_decision"] = review_decision if review_decision else "KEEP_AMBIGUOUS"
            out.at[idx, "hardening_level"] = "0_PROVISIONAL"
            out.at[idx, "excluded_from_validation"] = "True"
            if not normalize_text(row.get("exclusion_reason")):
                out.at[idx, "exclusion_reason"] = "not accepted in conservative hardened pass"

    out["excluded_from_validation"] = out["excluded_from_validation"].apply(stable_bool_string)

    out["hardening_pass"] = "v0_1_conservative"
    out["hardening_basis"] = (
        "Accepted only L_MODE/LH_TRANSITION rows initially marked ACCEPT; "
        "kept H_MODE_STABLE excluded pending external or stronger physical support; "
        "kept AMBIGUOUS/UNLABELABLE excluded; UNNS audit columns not used for label acceptance."
    )

    # Stable column order: required front columns first, then all remaining original columns.
    for col in FRONT_COLUMNS:
        if col not in out.columns:
            out[col] = ""
    out = out[FRONT_COLUMNS + [col for col in out.columns if col not in FRONT_COLUMNS]]

    # Stable row order.
    out["__shot_sort"] = pd.to_numeric(out["shot_id"], errors="coerce")
    out["__t_sort"] = pd.to_numeric(out["t_start"], errors="coerce")
    out = out.sort_values(["__shot_sort", "__t_sort", "window_id"], na_position="last")
    out = out.drop(columns=["__shot_sort", "__t_sort"]).reset_index(drop=True)

    return out


def summarize(hardened: pd.DataFrame, review_path: Path, output_path: Path) -> Dict[str, Any]:
    eligible_mask = hardened["excluded_from_validation"].astype(str).str.lower().isin({"false", "0", "no"})
    eligible = hardened[eligible_mask]

    return {
        "component": "reproduce_hardened_v0_1_from_review.py",
        "input": str(review_path),
        "output": str(output_path),
        "rows": int(len(hardened)),
        "shots": int(hardened["shot_id"].nunique()) if "shot_id" in hardened.columns else 0,
        "label_counts": {str(k): int(v) for k, v in hardened["label_type"].value_counts(dropna=False).to_dict().items()},
        "review_decision_counts": {str(k): int(v) for k, v in hardened["review_decision"].value_counts(dropna=False).to_dict().items()},
        "hardening_level_counts": {str(k): int(v) for k, v in hardened["hardening_level"].value_counts(dropna=False).to_dict().items()},
        "excluded_from_validation_counts": {
            str(k): int(v) for k, v in hardened["excluded_from_validation"].astype(str).value_counts(dropna=False).to_dict().items()
        },
        "eligible_rows": int(len(eligible)),
        "eligible_label_counts": {str(k): int(v) for k, v in eligible["label_type"].value_counts(dropna=False).to_dict().items()},
        "rule": (
            "Conservative v0.1 hardening: accept L_MODE/LH_TRANSITION rows initially marked ACCEPT; "
            "exclude all H_MODE_STABLE rows pending external or stronger physical evidence; keep AMBIGUOUS "
            "and UNLABELABLE excluded; do not use UNNS audit-only columns for physical-label acceptance."
        ),
    }


def write_summary_md(path: Path, summary: Dict[str, Any], output_csv: Path, summary_json: Path) -> None:
    lines: List[str] = []
    lines.append("# Hardened Labels v0.1 Reproduction Summary")
    lines.append("")
    lines.append("This file was generated by `reproduce_hardened_v0_1_from_review.py`.")
    lines.append("")
    lines.append("## Rule")
    lines.append("")
    lines.append(summary["rule"])
    lines.append("")
    lines.append("## Outputs")
    lines.append("")
    lines.append("```text")
    lines.append(str(output_csv))
    lines.append(str(summary_json))
    lines.append(str(path))
    lines.append("```")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append(f"- Rows: `{summary['rows']}`")
    lines.append(f"- Shots: `{summary['shots']}`")
    lines.append(f"- Eligible rows: `{summary['eligible_rows']}`")
    lines.append("")
    lines.append("### Label counts")
    lines.append("")
    lines.append("| label_type | count |")
    lines.append("|---|---:|")
    for label, count in summary["label_counts"].items():
        lines.append(f"| {label} | {count} |")
    lines.append("")
    lines.append("### Eligible label counts")
    lines.append("")
    lines.append("| label_type | count |")
    lines.append("|---|---:|")
    for label, count in summary["eligible_label_counts"].items():
        lines.append(f"| {label} | {count} |")
    lines.append("")
    lines.append("## Important interpretation")
    lines.append("")
    lines.append("This reproduces the conservative hardened label file exactly by rule. It does not independently validate H-mode. Independent physical reproduction still requires a reviewer to assign labels from D-alpha/profile/soft-X/power/density evidence without using the UNNS audit columns.")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce the conservative HARDENED v0.1 physical-window labels from the hardening review CSV.")
    parser.add_argument(
        "--review",
        default="outputs/reports/tokamark_physical_window_labels_HARDENING_REVIEW.csv",
        help="Input hardening review CSV.",
    )
    parser.add_argument("--out-dir", default="outputs/reports", help="Output directory.")
    parser.add_argument("--basename", default=OUTPUT_BASENAME, help="Output basename.")
    args = parser.parse_args()

    review_path = Path(args.review)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    output_csv = out_dir / f"{args.basename}.csv"
    summary_json = out_dir / f"{args.basename}_summary.json"
    summary_md = out_dir / f"{args.basename}_SUMMARY.md"

    review = pd.read_csv(review_path)
    hardened = reproduce_hardened(review)
    hardened.to_csv(output_csv, index=False)

    summary = summarize(hardened, review_path, output_csv)
    summary["input_sha256"] = sha256_file(review_path)
    summary["output_sha256"] = sha256_file(output_csv)

    summary_json.write_text(json.dumps(make_json_safe(summary), indent=2), encoding="utf-8")
    write_summary_md(summary_md, summary, output_csv, summary_json)

    print("HARDENED v0.1 reproduction complete.")
    print(f"Input review CSV: {review_path}")
    print(f"Output CSV:       {output_csv}")
    print(f"Summary JSON:     {summary_json}")
    print(f"Summary MD:       {summary_md}")
    print()
    print(f"Rows:          {summary['rows']}")
    print(f"Shots:         {summary['shots']}")
    print(f"Eligible rows: {summary['eligible_rows']}")
    print(f"Input SHA256:  {summary['input_sha256']}")
    print(f"Output SHA256: {summary['output_sha256']}")
    print()
    print("Eligible label counts:")
    for label, count in summary["eligible_label_counts"].items():
        print(f"  {label}: {count}")


if __name__ == "__main__":
    main()
