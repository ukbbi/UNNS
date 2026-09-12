#!/usr/bin/env python3
"""
tokamark_small_panel_runner.py

UNNS-H Mode Project
Small multi-shot TokaMark/MAST m_edge(t) panel runner.

Purpose
-------
Run the same pipeline used for shot 12063 across a small comparison panel:

  1. tokamark_one_shot_array_probe.py
  2. tokamark_m_edge_t_probe.py
  3. tokamark_m_edge_trace_inspector.py
  4. small-panel summary aggregation

This is the next step after:

  docs/21_TOKAMARK_CROSS_SHOT_M_EDGE_COMPARISON.md

Default panel
-------------
If no --shots are provided, the runner uses a deliberately small and diverse
panel from the first 200-shot metadata scan:

  12063  FULL_PROFILE_EDGE_CANDIDATE        reference
  11830  PROFILE_DALPHA_CANDIDATE          profile/no-softX weaker control
  11876  CORE_DALPHA_GEOMETRY_CANDIDATE    core+softX/no-Thomson control
  11768  PARTIAL_DALPHA_CANDIDATE          partial candidate
  11776  LOW_PRIORITY                      stress-test / weak candidate

Run from project root
---------------------

  python components\\tokamark_small_panel_runner.py --out-dir outputs\\reports

To skip already existing per-shot outputs:

  python components\\tokamark_small_panel_runner.py --out-dir outputs\\reports

To recompute everything:

  python components\\tokamark_small_panel_runner.py --out-dir outputs\\reports --force

To run a custom panel:

  python components\\tokamark_small_panel_runner.py --shots 12063 11830 11876 11768 --out-dir outputs\\reports

Outputs
-------

  outputs/reports/tokamark_small_panel_m_edge_comparison.csv
  outputs/reports/tokamark_small_panel_m_edge_comparison.json
  outputs/reports/tokamark_small_panel_m_edge_comparison.md

Scientific caution
------------------
This is still structural comparison, not physical H-mode validation.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd


DEFAULT_PANEL = [12063, 11830, 11876, 11768, 11776]


def run_command(cmd: List[str], log_path: Path) -> int:
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a", encoding="utf-8") as log:
        log.write("\n\n" + "=" * 80 + "\n")
        log.write("COMMAND: " + " ".join(cmd) + "\n")
        log.write("=" * 80 + "\n")
        log.flush()

        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        log.write(process.stdout)
        log.write(f"\nRETURN_CODE: {process.returncode}\n")

    return process.returncode


def ensure_stage(
    *,
    stage_name: str,
    shot: int,
    output_files: List[Path],
    command: List[str],
    log_path: Path,
    force: bool,
) -> Dict[str, Any]:
    if not force and all(p.exists() for p in output_files):
        return {
            "shot_id": shot,
            "stage": stage_name,
            "status": "skipped_existing",
            "return_code": 0,
            "outputs": [str(p) for p in output_files],
        }

    print(f"[shot {shot}] running {stage_name}...", flush=True)
    rc = run_command(command, log_path)
    status = "ok" if rc == 0 and all(p.exists() for p in output_files) else "failed"

    return {
        "shot_id": shot,
        "stage": stage_name,
        "status": status,
        "return_code": rc,
        "outputs": [str(p) for p in output_files],
    }


def load_candidate_metadata(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        df = pd.read_csv(path)
        if "shot_id" in df.columns:
            df["shot_id"] = pd.to_numeric(df["shot_id"], errors="coerce").fillna(-1).astype(int)
        return df
    except Exception:
        return pd.DataFrame()


def metadata_for_shot(df: pd.DataFrame, shot: int) -> Dict[str, Any]:
    if df.empty or "shot_id" not in df.columns:
        return {}
    row = df[df["shot_id"].eq(int(shot))]
    if row.empty:
        return {}
    return row.iloc[0].to_dict()


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


def load_inspection_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"summary": {}, "windows": [], "missing": True}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return {
            "summary": data.get("summary", {}),
            "windows": data.get("windows", []),
            "missing": False,
        }
    except Exception as exc:
        return {"summary": {}, "windows": [], "missing": True, "error": repr(exc)}


def summarize_shot(out_dir: Path, shot: int, metadata: Dict[str, Any]) -> Dict[str, Any]:
    probe_csv = out_dir / f"tokamark_shot_{shot}_m_edge_t_probe.csv"
    inspect_json = out_dir / f"tokamark_shot_{shot}_m_edge_trace_inspection_summary.json"
    signal_json = out_dir / f"tokamark_shot_{shot}_signal_probe.json"

    row: Dict[str, Any] = {
        "shot_id": shot,
        "probe_csv": str(probe_csv),
        "inspection_json": str(inspect_json),
        "signal_probe_json": str(signal_json),
        "has_probe_csv": probe_csv.exists(),
        "has_inspection_json": inspect_json.exists(),
        "has_signal_probe_json": signal_json.exists(),
        "candidate_class": metadata.get("candidate_class", ""),
        "candidate_score": metadata.get("candidate_score", ""),
        "campaign": metadata.get("campaign", ""),
        "split_membership": metadata.get("split_membership", ""),
        "core_required_present": metadata.get("core_required_present", ""),
        "profile_preferred_present": metadata.get("profile_preferred_present", ""),
        "edge_activity_present": metadata.get("edge_activity_present", ""),
        "supporting_present": metadata.get("supporting_present", ""),
        "missing_core_required": metadata.get("missing_core_required", ""),
        "missing_profile_preferred": metadata.get("missing_profile_preferred", ""),
        "missing_edge_activity": metadata.get("missing_edge_activity", ""),
    }

    if signal_json.exists():
        try:
            signal_payload = json.loads(signal_json.read_text(encoding="utf-8"))
            row["loaded_signal_arrays"] = len(signal_payload.get("loaded_labels", []))
            row["failed_signal_arrays"] = len(signal_payload.get("failed_labels", {}))
        except Exception:
            row["loaded_signal_arrays"] = ""
            row["failed_signal_arrays"] = ""

    if not probe_csv.exists():
        row["summary_status"] = "missing_probe_csv"
        return row

    df = pd.read_csv(probe_csv)
    row["summary_status"] = "ok"
    row["rows"] = int(len(df))
    if "time_s" in df.columns:
        row["time_min"] = float(pd.to_numeric(df["time_s"], errors="coerce").min())
        row["time_max"] = float(pd.to_numeric(df["time_s"], errors="coerce").max())

    if "m_edge_state" in df.columns:
        counts = df["m_edge_state"].astype(str).value_counts(dropna=False).to_dict()
        total = max(len(df), 1)
        for state in [
            "positive_boundary_margin",
            "boundary_ambiguous_margin",
            "negative_leakage_margin",
            "insufficient_data",
        ]:
            c = int(counts.get(state, 0))
            row[f"{state}_count"] = c
            row[f"{state}_fraction"] = float(c / total)

    for col in [
        "m_edge",
        "C_edge_capacity",
        "F_route_fragmentation",
        "S_edge_response",
        "S_power_balance",
        "S_transport",
        "missingness_pressure",
        "density_support",
        "geometry_stability",
    ]:
        if col in df.columns:
            stats = finite_stats(df[col])
            for k, v in stats.items():
                row[f"{col}_{k}"] = v

    inspection = load_inspection_json(inspect_json)
    windows = inspection.get("windows", [])
    interp_counts: Dict[str, int] = {}
    for w in windows:
        flag = str(w.get("interpretability_flag", "unknown"))
        interp_counts[flag] = interp_counts.get(flag, 0) + 1

    row["inspection_missing"] = inspection.get("missing", True)
    row["inspection_window_count"] = len(windows)
    row["interpretable_positive_count"] = int(interp_counts.get("interpretable_positive_candidate", 0))
    row["interpretable_negative_count"] = int(interp_counts.get("interpretable_negative_candidate", 0))
    row["fragile_positive_count"] = int(interp_counts.get("fragile_positive_candidate", 0))
    row["fragile_negative_count"] = int(interp_counts.get("fragile_negative_candidate", 0))
    row["weak_positive_count"] = int(interp_counts.get("weak_positive_candidate", 0))
    row["weak_negative_count"] = int(interp_counts.get("weak_negative_candidate", 0))
    row["interpretability_counts"] = json.dumps(interp_counts, sort_keys=True)

    row["interpretable_positive_total_duration"] = float(np.nansum([
        float(w.get("duration", 0.0))
        for w in windows
        if w.get("interpretability_flag") == "interpretable_positive_candidate"
    ])) if windows else 0.0

    row["interpretable_negative_total_duration"] = float(np.nansum([
        float(w.get("duration", 0.0))
        for w in windows
        if w.get("interpretability_flag") == "interpretable_negative_candidate"
    ])) if windows else 0.0

    return row


def rank_panel(df: pd.DataFrame, reference_shot: int) -> pd.DataFrame:
    df = df.copy()

    def val(row: pd.Series, key: str, default: float = 0.0) -> float:
        try:
            x = row.get(key, default)
            if pd.isna(x):
                return default
            return float(x)
        except Exception:
            return default

    scores = []
    for _, r in df.iterrows():
        score = (
            2.5 * val(r, "interpretable_positive_count")
            + 2.0 * val(r, "positive_boundary_margin_fraction")
            + 1.5 * max(val(r, "m_edge_median"), 0.0)
            + 1.0 * max(val(r, "m_edge_max"), 0.0)
            - 1.5 * val(r, "negative_leakage_margin_fraction")
            - 1.0 * val(r, "fragile_positive_count")
            - 0.8 * val(r, "fragile_negative_count")
            - 0.5 * val(r, "missingness_pressure_median")
        )
        scores.append(score)

    df["panel_structural_score"] = scores
    df["panel_rank"] = df["panel_structural_score"].rank(ascending=False, method="min").astype(int)
    df["panel_role"] = df["shot_id"].apply(lambda s: "reference" if int(s) == int(reference_shot) else "comparison")
    return df.sort_values(["panel_rank", "shot_id"])


def panel_decision(df: pd.DataFrame, reference_shot: int) -> Dict[str, Any]:
    if df.empty or reference_shot not in set(df["shot_id"].astype(int)):
        return {"decision": "inconclusive_missing_reference", "reasons": []}

    ref = df[df["shot_id"].astype(int).eq(int(reference_shot))].iloc[0]
    comps = df[~df["shot_id"].astype(int).eq(int(reference_shot))]

    reasons: List[str] = []
    decision = "inconclusive"

    ref_rank = int(ref.get("panel_rank", 9999))
    ref_interp = float(ref.get("interpretable_positive_count", 0) or 0)
    ref_pos_frac = float(ref.get("positive_boundary_margin_fraction", 0) or 0)
    ref_median = float(ref.get("m_edge_median", 0) or 0)
    ref_missing = float(ref.get("missingness_pressure_median", 0) or 0)

    max_comp_interp = float(comps["interpretable_positive_count"].fillna(0).max()) if not comps.empty else 0
    max_comp_pos_frac = float(comps["positive_boundary_margin_fraction"].fillna(0).max()) if not comps.empty else 0
    max_comp_median = float(comps["m_edge_median"].fillna(-999).max()) if not comps.empty else -999
    median_comp_missing = float(comps["missingness_pressure_median"].fillna(0).median()) if not comps.empty else 0

    if ref_rank == 1:
        reasons.append("reference_has_top_panel_structural_score")
    if ref_interp >= max_comp_interp:
        reasons.append("reference_has_highest_or_tied_interpretable_positive_count")
    if ref_pos_frac >= max_comp_pos_frac:
        reasons.append("reference_has_highest_or_tied_positive_fraction")
    if ref_median >= max_comp_median:
        reasons.append("reference_has_highest_or_tied_median_m_edge")
    if abs(ref_missing - median_comp_missing) <= 0.15:
        reasons.append("reference_result_not_explained_by_lower_missingness")

    if ref_rank == 1 and ref_interp >= max_comp_interp and ref_pos_frac >= max_comp_pos_frac:
        decision = "reference_structurally_strongest_in_panel"
    elif ref_rank <= 2 and ref_interp >= max_comp_interp:
        decision = "reference_structurally_strong_but_not_unique"
    elif ref_rank > 2:
        decision = "reference_not_structurally_strongest_v0_1_needs_review"
    else:
        decision = "mixed_panel_result_requires_review"

    return {
        "decision": decision,
        "reasons": reasons,
        "reference_shot": int(reference_shot),
        "panel_size": int(len(df)),
        "reference_panel_rank": ref_rank,
        "reference_interpretable_positive_count": ref_interp,
        "max_comparison_interpretable_positive_count": max_comp_interp,
        "reference_positive_fraction": ref_pos_frac,
        "max_comparison_positive_fraction": max_comp_pos_frac,
        "reference_m_edge_median": ref_median,
        "max_comparison_m_edge_median": max_comp_median,
        "reference_missingness_median": ref_missing,
        "comparison_missingness_median": median_comp_missing,
    }


def md_table(df: pd.DataFrame, columns: List[str]) -> str:
    if df.empty:
        return "_No rows._"
    use = [c for c in columns if c in df.columns]
    return df[use].to_markdown(index=False, floatfmt=".6g")


def write_report(path: Path, panel_df: pd.DataFrame, decision: Dict[str, Any], stages: List[Dict[str, Any]]) -> None:
    key_cols = [
        "panel_rank",
        "panel_role",
        "shot_id",
        "candidate_class",
        "candidate_score",
        "panel_structural_score",
        "positive_boundary_margin_fraction",
        "negative_leakage_margin_fraction",
        "m_edge_median",
        "m_edge_max",
        "interpretable_positive_count",
        "interpretable_negative_count",
        "fragile_positive_count",
        "fragile_negative_count",
        "missingness_pressure_median",
    ]

    meta_cols = [
        "shot_id",
        "candidate_class",
        "core_required_present",
        "profile_preferred_present",
        "edge_activity_present",
        "supporting_present",
        "missing_core_required",
        "missing_profile_preferred",
        "missing_edge_activity",
    ]

    md = []
    md.append("# TokaMark Small-Panel m_edge(t) Comparison")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Run and summarize a small multi-shot TokaMark/MAST panel using the same pipeline as the reference shot 12063.")
    md.append("")
    md.append("This is the next step after `docs/21_TOKAMARK_CROSS_SHOT_M_EDGE_COMPARISON.md`.")
    md.append("")
    md.append("## Panel decision")
    md.append("")
    md.append("```text")
    md.append(f"decision: {decision.get('decision')}")
    for reason in decision.get("reasons", []):
        md.append(f"- {reason}")
    md.append(f"reference shot: {decision.get('reference_shot')}")
    md.append(f"panel size: {decision.get('panel_size')}")
    md.append(f"reference panel rank: {decision.get('reference_panel_rank')}")
    md.append("```")
    md.append("")
    md.append("## Panel summary")
    md.append("")
    md.append(md_table(panel_df, key_cols))
    md.append("")
    md.append("## Metadata roles")
    md.append("")
    md.append(md_table(panel_df.sort_values('shot_id'), meta_cols))
    md.append("")
    md.append("## Pipeline stage status")
    md.append("")
    stage_df = pd.DataFrame(stages)
    if not stage_df.empty:
        md.append(stage_df[["shot_id", "stage", "status", "return_code"]].to_markdown(index=False))
    else:
        md.append("_No stage records._")
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append("If the reference shot remains top-ranked or structurally stronger across this small panel, v0.1 passes a stronger specificity test. If weaker shots reproduce the same coherent positive-window structure, v0.1 is probably overbroad and should be revised.")
    md.append("")
    md.append("## Bounded claim")
    md.append("")
    md.append("This panel comparison is still not physical H-mode validation. It tests whether the normalized UNNS-H Mode margin distinguishes the reference shot from several weaker public TokaMark candidates.")
    md.append("")
    md.append("## Next document")
    md.append("")
    md.append("```text")
    md.append("docs/")
    md.append("  22_TOKAMARK_SMALL_PANEL_M_EDGE_COMPARISON.md")
    md.append("```")
    path.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a small TokaMark m_edge(t) comparison panel.")
    parser.add_argument("--shots", nargs="*", type=int, default=None, help="Panel shot IDs. Defaults to a diverse 5-shot panel.")
    parser.add_argument("--reference-shot", type=int, default=12063, help="Reference shot.")
    parser.add_argument("--out-dir", default="outputs/reports", help="Output/report directory.")
    parser.add_argument("--components-dir", default="components", help="Components directory.")
    parser.add_argument("--metadata-candidates", default="outputs/reports/tokamark_positive_corridor_metadata_candidates.csv")
    parser.add_argument("--force", action="store_true", help="Recompute stages even when outputs already exist.")
    parser.add_argument("--skip-run", action="store_true", help="Only aggregate existing outputs; do not run stages.")
    parser.add_argument("--prefix", default="tokamark_small_panel_m_edge_comparison", help="Output filename prefix.")
    args = parser.parse_args()

    shots = args.shots if args.shots else DEFAULT_PANEL
    # Ensure reference first.
    shots = [args.reference_shot] + [s for s in shots if s != args.reference_shot]

    out_dir = Path(args.out_dir)
    comp_dir = Path(args.components_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    py = sys.executable

    one_shot = comp_dir / "tokamark_one_shot_array_probe.py"
    medge = comp_dir / "tokamark_m_edge_t_probe.py"
    inspector = comp_dir / "tokamark_m_edge_trace_inspector.py"

    for script in [one_shot, medge, inspector]:
        if not script.exists():
            raise SystemExit(f"Missing required component: {script}")

    log_path = out_dir / "tokamark_small_panel_runner.log"
    stages: List[Dict[str, Any]] = []

    if not args.skip_run:
        for shot in shots:
            stages.append(ensure_stage(
                stage_name="one_shot_array_probe",
                shot=shot,
                output_files=[
                    out_dir / f"tokamark_shot_{shot}_signal_probe.csv",
                    out_dir / f"tokamark_shot_{shot}_signal_probe.json",
                    out_dir / f"tokamark_shot_{shot}_signal_probe.md",
                ],
                command=[py, str(one_shot), "--shot-id", str(shot), "--out-dir", str(out_dir)],
                log_path=log_path,
                force=args.force,
            ))

            stages.append(ensure_stage(
                stage_name="m_edge_t_probe",
                shot=shot,
                output_files=[
                    out_dir / f"tokamark_shot_{shot}_m_edge_t_probe.csv",
                    out_dir / f"tokamark_shot_{shot}_m_edge_t_probe.json",
                    out_dir / f"tokamark_shot_{shot}_m_edge_t_probe.md",
                ],
                command=[py, str(medge), "--shot-id", str(shot), "--out-dir", str(out_dir)],
                log_path=log_path,
                force=args.force,
            ))

            stages.append(ensure_stage(
                stage_name="trace_inspection",
                shot=shot,
                output_files=[
                    out_dir / f"tokamark_shot_{shot}_m_edge_trace_inspection_windows.csv",
                    out_dir / f"tokamark_shot_{shot}_m_edge_trace_inspection_summary.json",
                    out_dir / f"tokamark_shot_{shot}_m_edge_trace_inspection.md",
                ],
                command=[
                    py, str(inspector),
                    "--input", str(out_dir / f"tokamark_shot_{shot}_m_edge_t_probe.csv"),
                    "--shot-id", str(shot),
                    "--out-dir", str(out_dir),
                ],
                log_path=log_path,
                force=args.force,
            ))
    else:
        stages.append({"shot_id": "", "stage": "all", "status": "skip_run_requested", "return_code": 0})

    metadata_df = load_candidate_metadata(Path(args.metadata_candidates))
    rows = []
    for shot in shots:
        rows.append(summarize_shot(out_dir, shot, metadata_for_shot(metadata_df, shot)))

    panel_df = pd.DataFrame(rows)
    panel_df = rank_panel(panel_df, args.reference_shot)
    decision = panel_decision(panel_df, args.reference_shot)

    csv_path = out_dir / f"{args.prefix}.csv"
    json_path = out_dir / f"{args.prefix}.json"
    md_path = out_dir / f"{args.prefix}.md"

    panel_df.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps({
        "component": "tokamark_small_panel_runner.py",
        "shots": shots,
        "reference_shot": args.reference_shot,
        "decision": decision,
        "stage_records": stages,
        "panel": panel_df.to_dict(orient="records"),
    }, indent=2, default=str), encoding="utf-8")
    write_report(md_path, panel_df, decision, stages)

    print("Small panel comparison complete.")
    print(f"Shots:    {shots}")
    print(f"Decision: {decision.get('decision')}")
    print(f"CSV:      {csv_path}")
    print(f"JSON:     {json_path}")
    print(f"Report:   {md_path}")
    print(f"Log:      {log_path}")
    print()
    print("Panel ranking:")
    for _, r in panel_df.sort_values("panel_rank").iterrows():
        print(
            f"  rank {int(r['panel_rank'])} | shot {int(r['shot_id'])} | "
            f"score {float(r['panel_structural_score']):.4f} | "
            f"interp+ {r.get('interpretable_positive_count', '')} | "
            f"class {r.get('candidate_class', '')}"
        )


if __name__ == "__main__":
    main()
