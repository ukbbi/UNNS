#!/usr/bin/env python3
"""
tokamark_moderate_confidence_panel_runner.py

UNNS-H Mode Project
Moderate TokaMark confidence-panel runner.

Purpose
-------
Run the existing v0.2 diagnostic-confidence pipeline on the moderate panel
selected by:

    components/tokamark_confidence_panel_selector.py

This follows:

    docs/26_TOKAMARK_MODERATE_CONFIDENCE_PANEL_PLAN.md

The runner reads:

    outputs/reports/tokamark_moderate_confidence_panel_selection.csv

Then, for each selected shot, it runs:

    1. tokamark_one_shot_array_probe.py
    2. tokamark_m_edge_t_probe.py
    3. tokamark_m_edge_trace_inspector.py

After per-shot products exist, it runs:

    4. tokamark_m_edge_confidence_revision.py --shots <selected shots>

Finally it copies/aggregates the confidence panel outputs as:

    outputs/reports/tokamark_moderate_confidence_panel_results.csv
    outputs/reports/tokamark_moderate_confidence_panel_results.json
    outputs/reports/tokamark_moderate_confidence_panel_results.md

Run from project root
---------------------

    python components\tokamark_moderate_confidence_panel_runner.py ^
      --selection outputs\reports\tokamark_moderate_confidence_panel_selection.csv ^
      --out-dir outputs\reports

Recompute all per-shot stages:

    python components\tokamark_moderate_confidence_panel_runner.py ^
      --selection outputs\reports\tokamark_moderate_confidence_panel_selection.csv ^
      --out-dir outputs\reports ^
      --force

Only aggregate existing outputs without running per-shot stages:

    python components\tokamark_moderate_confidence_panel_runner.py ^
      --selection outputs\reports\tokamark_moderate_confidence_panel_selection.csv ^
      --out-dir outputs\reports ^
      --skip-run

Scientific caution
------------------
This runner does not validate H-mode physically. It tests whether the v0.2
diagnostic-confidence correction remains stable and meaningful on a moderate
controlled panel.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

import numpy as np
import pandas as pd


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


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


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


def run_command(cmd: List[str], log_path: Path) -> int:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as log:
        log.write("\n\n" + "=" * 100 + "\n")
        log.write("COMMAND: " + " ".join(cmd) + "\n")
        log.write("=" * 100 + "\n")
        log.flush()

        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        log.write(proc.stdout)
        log.write(f"\nRETURN_CODE: {proc.returncode}\n")
    return int(proc.returncode)


def load_selection(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Selection CSV not found: {path}")

    df = pd.read_csv(path)

    if "shot_id" not in df.columns:
        raise ValueError("Selection CSV must contain shot_id column.")

    df["shot_id"] = pd.to_numeric(df["shot_id"], errors="coerce")
    df = df.dropna(subset=["shot_id"]).copy()
    df["shot_id"] = df["shot_id"].astype(int)

    if "selection_order" not in df.columns:
        df["selection_order"] = range(1, len(df) + 1)

    df = df.sort_values("selection_order").drop_duplicates(subset=["shot_id"], keep="first")
    return df.reset_index(drop=True)


def expected_files_for_stage(out_dir: Path, shot: int, stage: str) -> List[Path]:
    if stage == "one_shot_array_probe":
        return [
            out_dir / f"tokamark_shot_{shot}_signal_probe.csv",
            out_dir / f"tokamark_shot_{shot}_signal_probe.json",
            out_dir / f"tokamark_shot_{shot}_signal_probe.md",
        ]
    if stage == "m_edge_t_probe":
        return [
            out_dir / f"tokamark_shot_{shot}_m_edge_t_probe.csv",
            out_dir / f"tokamark_shot_{shot}_m_edge_t_probe.json",
            out_dir / f"tokamark_shot_{shot}_m_edge_t_probe.md",
        ]
    if stage == "trace_inspection":
        return [
            out_dir / f"tokamark_shot_{shot}_m_edge_trace_inspection_windows.csv",
            out_dir / f"tokamark_shot_{shot}_m_edge_trace_inspection_summary.json",
            out_dir / f"tokamark_shot_{shot}_m_edge_trace_inspection.md",
        ]
    if stage == "confidence_revision":
        return [
            out_dir / f"tokamark_shot_{shot}_m_edge_confidence_revision.csv",
            out_dir / f"tokamark_shot_{shot}_m_edge_confidence_revision.json",
            out_dir / f"tokamark_shot_{shot}_m_edge_confidence_revision.md",
        ]
    raise ValueError(f"Unknown stage: {stage}")


def stage_status(
    *,
    shot: int,
    stage: str,
    command: List[str],
    expected_files: List[Path],
    log_path: Path,
    force: bool,
    skip_run: bool,
) -> Dict[str, Any]:
    existing = all(path.exists() for path in expected_files)

    if skip_run:
        return {
            "shot_id": int(shot),
            "stage": stage,
            "status": "skip_run_existing" if existing else "skip_run_missing",
            "return_code": 0 if existing else None,
            "outputs": [str(p) for p in expected_files],
        }

    if existing and not force:
        return {
            "shot_id": int(shot),
            "stage": stage,
            "status": "skipped_existing",
            "return_code": 0,
            "outputs": [str(p) for p in expected_files],
        }

    print(f"[shot {shot}] running {stage}...", flush=True)
    rc = run_command(command, log_path)
    ok = rc == 0 and all(path.exists() for path in expected_files)

    return {
        "shot_id": int(shot),
        "stage": stage,
        "status": "ok" if ok else "failed",
        "return_code": rc,
        "outputs": [str(p) for p in expected_files],
    }


def finite_stats(series: pd.Series) -> Dict[str, Any]:
    arr = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return {"median": None, "mean": None, "min": None, "max": None}
    return {
        "median": float(np.median(finite)),
        "mean": float(np.mean(finite)),
        "min": float(np.min(finite)),
        "max": float(np.max(finite)),
    }


# ---------------------------------------------------------------------------
# Result aggregation
# ---------------------------------------------------------------------------

def merge_selection_and_panel(selection: pd.DataFrame, panel: pd.DataFrame) -> pd.DataFrame:
    if panel.empty:
        out = selection.copy()
        out["result_status"] = "missing_panel_result"
        return out

    merged = selection.merge(panel, on="shot_id", how="left", suffixes=("_selected", ""))

    if "confidence_panel_rank" in merged.columns:
        merged = merged.sort_values(["confidence_panel_rank", "selection_order"], na_position="last")
    else:
        merged = merged.sort_values("selection_order")

    # Add per-shot result status.
    if "confidence_structural_score" in merged.columns:
        merged["result_status"] = np.where(merged["confidence_structural_score"].notna(), "ok", "missing_confidence_result")
    else:
        merged["result_status"] = "missing_confidence_result"

    return merged.reset_index(drop=True)


def class_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "candidate_class" not in df.columns:
        return pd.DataFrame()

    rows = []
    for cls, group in df.groupby("candidate_class", dropna=False):
        row: Dict[str, Any] = {
            "candidate_class": cls,
            "count": int(len(group)),
        }
        for col in [
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
        ]:
            if col in group.columns:
                stats = finite_stats(group[col])
                row[f"{col}_median"] = stats["median"]
                row[f"{col}_mean"] = stats["mean"]

        if "conf_positive_fraction" in group.columns:
            vals = pd.to_numeric(group["conf_positive_fraction"], errors="coerce").fillna(0)
            row["fraction_with_conf_positive_gt_0"] = float((vals > 0).mean()) if len(vals) else 0.0

        if "conf_low_confidence_fraction" in group.columns:
            vals = pd.to_numeric(group["conf_low_confidence_fraction"], errors="coerce").fillna(0)
            row["fraction_with_low_conf_gt_0_25"] = float((vals > 0.25).mean()) if len(vals) else 0.0

        rows.append(row)

    return pd.DataFrame(rows).sort_values("candidate_class").reset_index(drop=True)


def stage_summary(stage_records: List[Dict[str, Any]]) -> pd.DataFrame:
    if not stage_records:
        return pd.DataFrame()

    df = pd.DataFrame(stage_records)
    rows = []
    for stage, group in df.groupby("stage", dropna=False):
        rows.append({
            "stage": stage,
            "total": int(len(group)),
            "ok": int(group["status"].astype(str).isin(["ok", "skipped_existing", "skip_run_existing"]).sum()),
            "failed": int(group["status"].astype(str).eq("failed").sum()),
            "missing_after_skip": int(group["status"].astype(str).eq("skip_run_missing").sum()),
        })
    return pd.DataFrame(rows)


def decide_moderate_panel(merged: pd.DataFrame, class_df: pd.DataFrame) -> Dict[str, Any]:
    reasons: List[str] = []
    warnings: List[str] = []
    decision = "moderate_panel_inconclusive"

    if merged.empty:
        return {"decision": "moderate_panel_empty", "reasons": [], "warnings": ["No merged panel rows."]}

    # Basic quantities.
    ok_rows = merged[merged.get("result_status", "").astype(str).eq("ok")] if "result_status" in merged.columns else merged
    total = len(merged)
    ok_count = len(ok_rows)

    if ok_count < max(5, total * 0.70):
        warnings.append("Too many missing confidence results for a stable panel decision.")

    top_n = min(10, len(ok_rows))
    top = ok_rows.sort_values("confidence_panel_rank").head(top_n) if "confidence_panel_rank" in ok_rows.columns else ok_rows.head(top_n)

    full_top_count = int(top["candidate_class"].astype(str).eq("FULL_PROFILE_EDGE_CANDIDATE").sum()) if "candidate_class" in top.columns else 0
    low_top_count = int(top["candidate_class"].astype(str).eq("LOW_PRIORITY").sum()) if "candidate_class" in top.columns else 0

    if full_top_count >= max(2, top_n // 3):
        reasons.append("FULL_PROFILE_EDGE_CANDIDATE shots are enriched among top-ranked cases.")
    else:
        warnings.append("FULL_PROFILE_EDGE_CANDIDATE shots are not clearly enriched among top-ranked cases.")

    if low_top_count == 0:
        reasons.append("LOW_PRIORITY shots are absent from top-ranked cases.")
    else:
        warnings.append("LOW_PRIORITY shots appear among top-ranked cases.")

    # Low-priority suppression.
    low = ok_rows[ok_rows["candidate_class"].astype(str).eq("LOW_PRIORITY")] if "candidate_class" in ok_rows.columns else pd.DataFrame()
    if not low.empty and "conf_positive_fraction" in low.columns:
        low_conf_pos = pd.to_numeric(low["conf_positive_fraction"], errors="coerce").fillna(0)
        if float((low_conf_pos > 0).mean()) == 0.0:
            reasons.append("LOW_PRIORITY shots have zero confidence-positive fraction.")
        else:
            warnings.append("Some LOW_PRIORITY shots have nonzero confidence-positive fraction.")

    # Partial suppression.
    partial = ok_rows[ok_rows["candidate_class"].astype(str).eq("PARTIAL_DALPHA_CANDIDATE")] if "candidate_class" in ok_rows.columns else pd.DataFrame()
    if not partial.empty and "conf_positive_fraction" in partial.columns:
        p_conf_pos = pd.to_numeric(partial["conf_positive_fraction"], errors="coerce").fillna(0)
        if float((p_conf_pos > 0).mean()) <= 0.25:
            reasons.append("PARTIAL_DALPHA_CANDIDATE shots are mostly suppressed.")
        else:
            warnings.append("PARTIAL_DALPHA_CANDIDATE shots often remain confidence-positive.")

    # Confidence-positive must occur at decent Q.
    conf_pos_cases = ok_rows[pd.to_numeric(ok_rows.get("conf_positive_fraction", 0), errors="coerce").fillna(0) > 0]
    if not conf_pos_cases.empty and "Q_diag_median" in conf_pos_cases.columns:
        q_med = pd.to_numeric(conf_pos_cases["Q_diag_median"], errors="coerce").median()
        if pd.notna(q_med) and q_med >= 0.60:
            reasons.append("Confidence-positive cases have moderate/high median Q_diag.")
        else:
            warnings.append("Confidence-positive cases do not have sufficiently high Q_diag.")
    elif conf_pos_cases.empty:
        warnings.append("No confidence-positive cases found in moderate panel.")

    # Missingness penalties should suppress low-priority/partial.
    if not class_df.empty and "candidate_class" in class_df.columns:
        try:
            full_row = class_df[class_df["candidate_class"].eq("FULL_PROFILE_EDGE_CANDIDATE")]
            low_row = class_df[class_df["candidate_class"].eq("LOW_PRIORITY")]
            if not full_row.empty and not low_row.empty:
                full_p = float(full_row["P_missing_critical_median_median"].iloc[0])
                low_p = float(low_row["P_missing_critical_median_median"].iloc[0])
                if low_p > full_p:
                    reasons.append("Critical-missing penalties are higher in LOW_PRIORITY cases than in FULL_PROFILE_EDGE_CANDIDATE cases.")
                else:
                    warnings.append("Critical-missing penalties do not separate LOW_PRIORITY from FULL_PROFILE_EDGE_CANDIDATE cases.")
        except Exception:
            pass

    # Final decision.
    if ok_count >= max(5, total * 0.70) and len(reasons) >= 4 and not any("LOW_PRIORITY shots appear" in w for w in warnings):
        decision = "moderate_confidence_panel_passes_initial_stability_test"
    elif ok_count >= max(5, total * 0.70) and len(reasons) >= 2:
        decision = "moderate_confidence_panel_mixed_but_usable"
    else:
        decision = "moderate_confidence_panel_fails_or_inconclusive"

    return {
        "decision": decision,
        "reasons": reasons,
        "warnings": warnings,
        "selected_total": int(total),
        "processed_ok": int(ok_count),
        "top_n_reviewed": int(top_n),
        "top_n_full_profile_edge_count": int(full_top_count),
        "top_n_low_priority_count": int(low_top_count),
        "confidence_positive_case_count": int(len(conf_pos_cases)),
    }


def write_results_report(
    path: Path,
    *,
    selection: pd.DataFrame,
    merged: pd.DataFrame,
    class_df: pd.DataFrame,
    stage_df: pd.DataFrame,
    decision: Dict[str, Any],
    confidence_json: Dict[str, Any],
) -> None:
    ranking_cols = [
        "confidence_panel_rank",
        "selection_order",
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
        "selection_role",
    ]
    ranking_cols = [c for c in ranking_cols if c in merged.columns]

    class_cols = [
        "candidate_class",
        "count",
        "confidence_structural_score_median",
        "conf_positive_fraction_median",
        "conf_negative_fraction_median",
        "conf_low_confidence_fraction_median",
        "Q_diag_median_median",
        "P_missing_critical_median_median",
        "fraction_with_conf_positive_gt_0",
        "fraction_with_low_conf_gt_0_25",
    ]
    class_cols = [c for c in class_cols if c in class_df.columns]

    top5 = merged.sort_values("confidence_panel_rank").head(5) if "confidence_panel_rank" in merged.columns else merged.head(5)
    bottom5 = merged.sort_values("confidence_panel_rank").tail(5) if "confidence_panel_rank" in merged.columns else merged.tail(5)

    conf_pos = merged[pd.to_numeric(merged.get("conf_positive_fraction", 0), errors="coerce").fillna(0) > 0].copy()
    raw_inflated_suppressed = merged[
        (pd.to_numeric(merged.get("raw_positive_fraction", 0), errors="coerce").fillna(0) > 0.5)
        & (pd.to_numeric(merged.get("conf_positive_fraction", 0), errors="coerce").fillna(0) == 0)
    ].copy()

    md = []
    md.append("# TokaMark Moderate Confidence Panel Results")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Report the moderate controlled panel run for the v0.2 diagnostic-confidence UNNS-H Mode pipeline.")
    md.append("")
    md.append("This report is the intended content source for:")
    md.append("")
    md.append("```text")
    md.append("docs/")
    md.append("  27_TOKAMARK_MODERATE_CONFIDENCE_PANEL_RESULTS.md")
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("")
    md.append("```text")
    md.append(f"decision: {decision.get('decision')}")
    md.append(f"selected total: {decision.get('selected_total')}")
    md.append(f"processed ok: {decision.get('processed_ok')}")
    md.append(f"confidence-positive case count: {decision.get('confidence_positive_case_count')}")
    md.append("```")
    md.append("")
    if decision.get("reasons"):
        md.append("### Reasons")
        md.append("")
        for r in decision.get("reasons", []):
            md.append(f"- {r}")
        md.append("")
    if decision.get("warnings"):
        md.append("### Warnings")
        md.append("")
        for w in decision.get("warnings", []):
            md.append(f"- {w}")
        md.append("")
    md.append("## Confidence-adjusted ranking")
    md.append("")
    md.append(df_to_markdown(merged[ranking_cols], index=False) if ranking_cols else "_No ranking columns._")
    md.append("")
    md.append("## Class-level summary")
    md.append("")
    md.append(df_to_markdown(class_df[class_cols], index=False) if class_cols else "_No class summary._")
    md.append("")
    md.append("## Stage summary")
    md.append("")
    md.append(df_to_markdown(stage_df, index=False) if not stage_df.empty else "_No stage summary._")
    md.append("")
    md.append("## Manual review queues")
    md.append("")
    md.append("### Top 5 confidence-ranked shots")
    md.append("")
    md.append(df_to_markdown(top5[ranking_cols], index=False) if ranking_cols else "_No rows._")
    md.append("")
    md.append("### Bottom 5 confidence-ranked shots")
    md.append("")
    md.append(df_to_markdown(bottom5[ranking_cols], index=False) if ranking_cols else "_No rows._")
    md.append("")
    md.append("### Confidence-positive shots")
    md.append("")
    md.append(df_to_markdown(conf_pos[ranking_cols], index=False) if not conf_pos.empty and ranking_cols else "_No confidence-positive shots._")
    md.append("")
    md.append("### Raw-positive inflated but confidence-suppressed shots")
    md.append("")
    md.append(df_to_markdown(raw_inflated_suppressed[ranking_cols], index=False) if not raw_inflated_suppressed.empty and ranking_cols else "_No raw-positive > 0.5 cases suppressed to zero confidence-positive._")
    md.append("")
    md.append("## Bounded interpretation")
    md.append("")
    md.append("This moderate panel does not validate H-mode physically. It tests whether the v0.2 diagnostic-confidence correction remains methodologically stable across a controlled panel.")
    md.append("")
    md.append("## Next document")
    md.append("")
    md.append("If this panel passes, the next planning document should be:")
    md.append("")
    md.append("```text")
    md.append("docs/")
    md.append("  28_PHYSICAL_WINDOW_LABELING_REQUIREMENTS.md")
    md.append("```")
    md.append("")
    path.write_text("\n".join(md), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Run the moderate TokaMark confidence panel.")
    parser.add_argument("--selection", default="outputs/reports/tokamark_moderate_confidence_panel_selection.csv", help="Moderate panel selection CSV.")
    parser.add_argument("--out-dir", default="outputs/reports", help="Output/report directory.")
    parser.add_argument("--components-dir", default="components", help="Components directory.")
    parser.add_argument("--metadata-candidates", default="outputs/reports/tokamark_positive_corridor_metadata_candidates.csv")
    parser.add_argument("--force", action="store_true", help="Re-run per-shot stages even if outputs exist.")
    parser.add_argument("--skip-run", action="store_true", help="Only aggregate existing outputs; do not run per-shot stages.")
    parser.add_argument("--skip-inspection", action="store_true", help="Skip trace-inspection stage.")
    parser.add_argument("--prefix", default="tokamark_moderate_confidence_panel_results", help="Output prefix.")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    comp_dir = Path(args.components_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    selection_path = Path(args.selection)
    selection = load_selection(selection_path)
    shots = selection["shot_id"].astype(int).tolist()

    one_shot = comp_dir / "tokamark_one_shot_array_probe.py"
    medge = comp_dir / "tokamark_m_edge_t_probe.py"
    inspector = comp_dir / "tokamark_m_edge_trace_inspector.py"
    confidence = comp_dir / "tokamark_m_edge_confidence_revision.py"

    required = [one_shot, medge, confidence]
    if not args.skip_inspection:
        required.append(inspector)

    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise SystemExit("Missing required components:\n" + "\n".join(missing))

    py = sys.executable
    log_path = out_dir / "tokamark_moderate_confidence_panel_runner.log"
    stage_records: List[Dict[str, Any]] = []

    print("Moderate confidence panel runner")
    print(f"Selection: {selection_path}")
    print(f"Shots: {shots}")
    print(f"Count: {len(shots)}")
    print()

    # Per-shot stages.
    for shot in shots:
        stage_records.append(stage_status(
            shot=shot,
            stage="one_shot_array_probe",
            command=[py, str(one_shot), "--shot-id", str(shot), "--out-dir", str(out_dir)],
            expected_files=expected_files_for_stage(out_dir, shot, "one_shot_array_probe"),
            log_path=log_path,
            force=args.force,
            skip_run=args.skip_run,
        ))

        stage_records.append(stage_status(
            shot=shot,
            stage="m_edge_t_probe",
            command=[py, str(medge), "--shot-id", str(shot), "--out-dir", str(out_dir)],
            expected_files=expected_files_for_stage(out_dir, shot, "m_edge_t_probe"),
            log_path=log_path,
            force=args.force,
            skip_run=args.skip_run,
        ))

        if not args.skip_inspection:
            stage_records.append(stage_status(
                shot=shot,
                stage="trace_inspection",
                command=[
                    py, str(inspector),
                    "--input", str(out_dir / f"tokamark_shot_{shot}_m_edge_t_probe.csv"),
                    "--shot-id", str(shot),
                    "--out-dir", str(out_dir),
                ],
                expected_files=expected_files_for_stage(out_dir, shot, "trace_inspection"),
                log_path=log_path,
                force=args.force,
                skip_run=args.skip_run,
            ))

    # Confidence revision stage over whole panel.
    confidence_cmd = [
        py, str(confidence),
        "--shots", *[str(s) for s in shots],
        "--out-dir", str(out_dir),
        "--metadata-candidates", str(args.metadata_candidates),
    ]

    if args.skip_run:
        conf_existing = all((out_dir / f"tokamark_shot_{shot}_m_edge_confidence_revision.csv").exists() for shot in shots)
        stage_records.append({
            "shot_id": "panel",
            "stage": "confidence_revision_panel",
            "status": "skip_run_existing" if conf_existing else "skip_run_missing",
            "return_code": 0 if conf_existing else None,
            "outputs": [
                str(out_dir / "tokamark_confidence_panel_comparison.csv"),
                str(out_dir / "tokamark_confidence_panel_comparison.json"),
                str(out_dir / "tokamark_confidence_panel_comparison.md"),
            ],
        })
    else:
        print("[panel] running confidence_revision...", flush=True)
        rc = run_command(confidence_cmd, log_path)
        ok = rc == 0 and (out_dir / "tokamark_confidence_panel_comparison.csv").exists()
        stage_records.append({
            "shot_id": "panel",
            "stage": "confidence_revision_panel",
            "status": "ok" if ok else "failed",
            "return_code": rc,
            "outputs": [
                str(out_dir / "tokamark_confidence_panel_comparison.csv"),
                str(out_dir / "tokamark_confidence_panel_comparison.json"),
                str(out_dir / "tokamark_confidence_panel_comparison.md"),
            ],
        })

    # Read confidence revision outputs.
    conf_csv = out_dir / "tokamark_confidence_panel_comparison.csv"
    conf_json = out_dir / "tokamark_confidence_panel_comparison.json"
    conf_md = out_dir / "tokamark_confidence_panel_comparison.md"

    if conf_csv.exists():
        panel = pd.read_csv(conf_csv)
    else:
        panel = pd.DataFrame()

    confidence_payload = read_json(conf_json)

    merged = merge_selection_and_panel(selection, panel)
    class_df = class_summary(merged)
    stage_df = stage_summary(stage_records)
    decision = decide_moderate_panel(merged, class_df)

    # Write moderate outputs.
    results_csv = out_dir / f"{args.prefix}.csv"
    results_json = out_dir / f"{args.prefix}.json"
    results_md = out_dir / f"{args.prefix}.md"

    merged.to_csv(results_csv, index=False)
    write_json(results_json, {
        "component": "tokamark_moderate_confidence_panel_runner.py",
        "selection_input": str(selection_path),
        "shots": shots,
        "decision": decision,
        "stage_records": stage_records,
        "stage_summary": stage_df.to_dict(orient="records") if not stage_df.empty else [],
        "class_summary": class_df.to_dict(orient="records") if not class_df.empty else [],
        "confidence_revision_payload": confidence_payload,
        "panel": merged.to_dict(orient="records"),
    })
    write_results_report(
        results_md,
        selection=selection,
        merged=merged,
        class_df=class_df,
        stage_df=stage_df,
        decision=decision,
        confidence_json=confidence_payload,
    )

    # Also snapshot confidence panel generic outputs to moderate-specific names for audit.
    snapshot_map = [
        (conf_csv, out_dir / f"{args.prefix}__raw_confidence_panel.csv"),
        (conf_json, out_dir / f"{args.prefix}__raw_confidence_panel.json"),
        (conf_md, out_dir / f"{args.prefix}__raw_confidence_panel.md"),
    ]
    for src, dst in snapshot_map:
        if src.exists():
            try:
                shutil.copy2(src, dst)
            except Exception:
                pass

    print()
    print("Moderate confidence panel run complete.")
    print(f"Selected shots: {len(shots)}")
    print(f"Decision: {decision.get('decision')}")
    print(f"Results CSV:  {results_csv}")
    print(f"Results JSON: {results_json}")
    print(f"Results MD:   {results_md}")
    print(f"Log:          {log_path}")
    print()
    if decision.get("reasons"):
        print("Reasons:")
        for r in decision["reasons"]:
            print(f"  - {r}")
    if decision.get("warnings"):
        print()
        print("Warnings:")
        for w in decision["warnings"]:
            print(f"  - {w}")
    print()
    print("Next report:")
    print("  docs/27_TOKAMARK_MODERATE_CONFIDENCE_PANEL_RESULTS.md")


if __name__ == "__main__":
    main()
