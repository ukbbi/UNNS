#!/usr/bin/env python3
"""
tcv_fragment_isolate_mapper.py

UNNS-H Mode Project — TCV fragment isolate mapper.

Purpose
-------
Map STRUC-PERC-I hard-fragmenting scalar variables back to the actual TCV
rows/shots that sit adjacent to isolated or non-giant gap components.

This script does not rerun STRUC-I or STRUC-PERC-I. It reconstructs the final
STRUC-PERC-I full pairwise gap graph at kappa_max, identifies non-giant gap
components, and maps those gap vertices back to the source transition rows.

Default target variables:
    chi_eff_candidate
    P_total_candidate_MW
    P_total_aux_candidate_MW
    P_loss_candidate_MW
    event_time
    divertor_signal_candidate

Inputs expected in a normal project checkout:
    data/processed/tcv_lh_events_canonical.csv
    outputs/reports/struc_perc_batch_results.json
    outputs/reports/struc_perc_batch_results_lh_only.json

Outputs:
    outputs/reports/tcv_fragment_component_summary.csv
    outputs/reports/tcv_fragment_gap_map.csv
    outputs/reports/tcv_suspect_transition_families.csv
    outputs/reports/tcv_fragment_isolate_mapping_report.md
    outputs/reports/tcv_fragment_isolate_mapping_summary.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd

DEFAULT_TARGETS = [
    "chi_eff_candidate",
    "P_total_candidate_MW",
    "P_total_aux_candidate_MW",
    "P_loss_candidate_MW",
    "event_time",
    "divertor_signal_candidate",
]

CONTEXT_COLUMNS = [
    "shot_id", "event_time", "event_type", "src_ILH", "src_COND",
    "P_LH_candidate_MW", "P_loss_candidate_MW", "P_total_candidate_MW",
    "P_total_aux_candidate_MW", "dWmhd_dt_candidate_MW", "Wmhd_J",
    "n_e_1e20_m3", "I_p_MA", "B_t_T", "q95", "kappa", "delta",
    "minor_radius_m", "R_geo_m", "volume_m3",
    "hydrogen_fraction_candidate", "helium_fraction_candidate", "Z_eff",
    "n_Ryter", "P_Ryter", "chi_eff_candidate",
    "divertor_signal_candidate", "divertor_signal_150_candidate",
]


def _safe_read_json(path: Path) -> list:
    if path and path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []


def load_struc_perc_results(all_path: Path | None, lh_path: Path | None) -> Dict[Tuple[str, str], dict]:
    """Return mapping keyed by (subset, variable)."""
    out: Dict[Tuple[str, str], dict] = {}
    for subset, path in [("all_events", all_path), ("lh_only", lh_path)]:
        for item in _safe_read_json(path) if path else []:
            name = str(item.get("name", ""))
            var = name
            if var.endswith(".csv"):
                var = var[:-4]
            if "__" in var:
                var = var.split("__", 1)[1]
            elif var.startswith("tcv_lh__"):
                var = var[len("tcv_lh__"):]
            out[(subset, var)] = item
    return out


def js_quantile_iqr(values: np.ndarray) -> float:
    """Replicate the STRUC-PERC-I v2.5 style IQR index rule from the JS code."""
    if len(values) == 0:
        return 0.0
    s = np.sort(values.astype(float))
    q1 = s[int(np.floor(0.25 * (len(s) - 1)))]
    q3 = s[int(np.floor(0.75 * (len(s) - 1)))]
    return float(q3 - q1)


def median(values: np.ndarray) -> float:
    if len(values) == 0:
        return 0.0
    return float(np.median(values.astype(float)))


def deduplicate_exact(sorted_values: np.ndarray) -> np.ndarray:
    """STRUC-PERC batch/generic ingestion effectively works on sorted unique values."""
    if len(sorted_values) == 0:
        return sorted_values
    return np.array(sorted(set(map(float, sorted_values))), dtype=float)


def build_gap_components(gaps: np.ndarray, eps: float) -> List[List[int]]:
    """Full pairwise gap graph: edge(i,j) iff |gap_i-gap_j| <= eps."""
    n = len(gaps)
    if n == 0:
        return []

    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    order = np.argsort(gaps)
    left = 0
    for pos, idx in enumerate(order):
        while gaps[idx] - gaps[order[left]] > eps:
            left += 1
        for jpos in range(left, pos):
            union(int(order[jpos]), int(idx))

    groups: Dict[int, List[int]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def rows_for_value(dfv: pd.DataFrame, variable: str, value: float) -> pd.DataFrame:
    # Exact values are preserved from the CSV; use allclose for floating-string roundtrip safety.
    col = pd.to_numeric(dfv[variable], errors="coerce")
    mask = np.isclose(col.astype(float), float(value), rtol=1e-10, atol=1e-12)
    return dfv.loc[mask].copy()


def summarize_rows(rows: pd.DataFrame) -> dict:
    out = {}
    if rows.empty:
        return {
            "involved_row_count": 0,
            "involved_shot_count": 0,
            "involved_shots": "",
            "event_time_min": np.nan,
            "event_time_max": np.nan,
        }

    shots = sorted(set(pd.to_numeric(rows.get("shot_id"), errors="coerce").dropna().astype(int).tolist())) if "shot_id" in rows else []
    out["involved_row_count"] = int(len(rows))
    out["involved_shot_count"] = int(len(shots))
    out["involved_shots"] = ";".join(map(str, shots[:40])) + (";..." if len(shots) > 40 else "")
    if "event_time" in rows:
        et = pd.to_numeric(rows["event_time"], errors="coerce")
        out["event_time_min"] = float(et.min()) if et.notna().any() else np.nan
        out["event_time_max"] = float(et.max()) if et.notna().any() else np.nan
    else:
        out["event_time_min"] = np.nan
        out["event_time_max"] = np.nan

    for c in [
        "P_LH_candidate_MW", "P_loss_candidate_MW", "P_total_candidate_MW",
        "P_total_aux_candidate_MW", "dWmhd_dt_candidate_MW", "Wmhd_J",
        "n_e_1e20_m3", "I_p_MA", "B_t_T", "q95", "kappa", "delta",
        "hydrogen_fraction_candidate", "helium_fraction_candidate", "Z_eff",
        "n_Ryter", "P_Ryter", "chi_eff_candidate",
        "divertor_signal_candidate", "divertor_signal_150_candidate",
    ]:
        if c in rows:
            vals = pd.to_numeric(rows[c], errors="coerce")
            out[f"mean_{c}"] = float(vals.mean()) if vals.notna().any() else np.nan
    return out


def analyze_variable(
    df_subset: pd.DataFrame,
    subset_name: str,
    variable: str,
    chamber_result: dict | None,
    kappa_max: float,
) -> tuple[list[dict], list[dict], list[dict]]:
    if variable not in df_subset.columns:
        return [], [], []

    vals = pd.to_numeric(df_subset[variable], errors="coerce")
    valid_df = df_subset.loc[vals.notna()].copy()
    if len(valid_df) < 4:
        return [], [], []

    raw_values = pd.to_numeric(valid_df[variable], errors="coerce").astype(float).values
    unique_values = deduplicate_exact(np.sort(raw_values))
    if len(unique_values) < 4:
        return [], [], []

    gaps = np.diff(unique_values)
    if len(gaps) < 3:
        return [], [], []

    iqr = js_quantile_iqr(gaps)
    med = median(gaps)
    scale = iqr if iqr > 0 else med
    eps = float(kappa_max * scale)
    comps = build_gap_components(gaps, eps)
    comps_sorted = sorted(comps, key=len, reverse=True)
    giant = comps_sorted[0] if comps_sorted else []
    giant_set = set(giant)
    giant_fraction = len(giant) / len(gaps) if len(gaps) else np.nan

    verdict = (chamber_result or {}).get("verdict", "NOT_PROVIDED")
    chamber_giant = (chamber_result or {}).get("giantRatio", np.nan)
    chamber_iso = (chamber_result or {}).get("isolated", np.nan)
    chamber_iso_fraction = (chamber_result or {}).get("isolatedFraction", np.nan)
    chamber_kconn = (chamber_result or {}).get("kappa_connect", np.nan)
    tail_dom = (chamber_result or {}).get("tailDominance", np.nan)

    component_rows = []
    gap_rows = []
    family_rows = []

    for comp_id, comp in enumerate(comps_sorted):
        comp = sorted(comp)
        role = "giant" if set(comp) == giant_set else ("singleton_isolate" if len(comp) == 1 else "minor_component")
        comp_gaps = gaps[comp]
        comp_lower_values = unique_values[comp]
        comp_upper_values = unique_values[np.array(comp) + 1]

        # Collect adjacent source rows for the whole component.
        adj_frames = []
        for gi in comp:
            lval = unique_values[gi]
            uval = unique_values[gi + 1]
            adj_frames.append(rows_for_value(valid_df, variable, lval))
            adj_frames.append(rows_for_value(valid_df, variable, uval))
        adj_rows = pd.concat(adj_frames, ignore_index=False).drop_duplicates() if adj_frames else pd.DataFrame()
        row_summary = summarize_rows(adj_rows)

        comp_record = {
            "subset": subset_name,
            "variable": variable,
            "chamber_verdict": verdict,
            "component_id": comp_id,
            "component_role": role,
            "component_size_gaps": int(len(comp)),
            "component_fraction_gaps": float(len(comp) / len(gaps)),
            "n_valid_rows": int(len(valid_df)),
            "n_unique_values": int(len(unique_values)),
            "n_gaps": int(len(gaps)),
            "computed_giant_fraction_gaps": float(giant_fraction),
            "chamber_giantRatio": chamber_giant,
            "chamber_isolated": chamber_iso,
            "chamber_isolatedFraction": chamber_iso_fraction,
            "chamber_kappa_connect": chamber_kconn,
            "tailDominance": tail_dom,
            "scale_IQR_or_median": float(scale),
            "epsilon_at_kappa_max": float(eps),
            "gap_min": float(np.min(comp_gaps)),
            "gap_max": float(np.max(comp_gaps)),
            "gap_mean": float(np.mean(comp_gaps)),
            "lower_value_min": float(np.min(comp_lower_values)),
            "upper_value_max": float(np.max(comp_upper_values)),
        }
        comp_record.update(row_summary)
        component_rows.append(comp_record)

        # Family rows focus on non-giant components from hard variables.
        if role != "giant" or verdict == "HARD_FRAGMENTATION":
            fam = dict(comp_record)
            fam["mapping_priority"] = (
                "HIGH" if verdict == "HARD_FRAGMENTATION" and role != "giant"
                else "MEDIUM" if verdict == "HARD_FRAGMENTATION"
                else "LOW"
            )
            family_rows.append(fam)

        for local_rank, gi in enumerate(comp):
            lval = unique_values[gi]
            uval = unique_values[gi + 1]
            lower_rows = rows_for_value(valid_df, variable, lval)
            upper_rows = rows_for_value(valid_df, variable, uval)
            adj_rows = pd.concat([lower_rows, upper_rows], ignore_index=False).drop_duplicates()
            adj_summary = summarize_rows(adj_rows)
            gap_ratio_to_median = float(gaps[gi] / med) if med > 0 else np.nan
            gap_record = {
                "subset": subset_name,
                "variable": variable,
                "chamber_verdict": verdict,
                "component_id": comp_id,
                "component_role": role,
                "gap_local_rank_in_component": int(local_rank),
                "gap_index_in_sorted_unique_ladder": int(gi),
                "gap_value": float(gaps[gi]),
                "gap_ratio_to_median": gap_ratio_to_median,
                "lower_value": float(lval),
                "upper_value": float(uval),
                "lower_row_indices": ";".join(map(str, lower_rows.index.tolist()[:20])),
                "upper_row_indices": ";".join(map(str, upper_rows.index.tolist()[:20])),
                "lower_shots": ";".join(map(str, sorted(set(pd.to_numeric(lower_rows.get("shot_id"), errors="coerce").dropna().astype(int).tolist()))[:20])) if not lower_rows.empty else "",
                "upper_shots": ";".join(map(str, sorted(set(pd.to_numeric(upper_rows.get("shot_id"), errors="coerce").dropna().astype(int).tolist()))[:20])) if not upper_rows.empty else "",
            }
            gap_record.update(adj_summary)
            gap_rows.append(gap_record)

    return component_rows, gap_rows, family_rows


def make_markdown_report(component_df: pd.DataFrame, family_df: pd.DataFrame, out_path: Path) -> None:
    hard = component_df[component_df["chamber_verdict"].eq("HARD_FRAGMENTATION")]
    nongiant = family_df[family_df["component_role"].ne("giant")].copy() if not family_df.empty else family_df

    lines = []
    lines.append("# TCV Fragment-Isolate Mapping Report")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append("This report maps STRUC-PERC-I hard-fragmenting scalar variables back to the TCV event rows and shots adjacent to isolated or non-giant gap components.")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append("For each target variable and each subset (`all_events`, `lh_only`), the script sorts unique scalar values, constructs the gap vector Δ, rebuilds the full pairwise gap graph at κ = 1 using ε = IQR(Δ), identifies giant and non-giant components, and maps each gap back to the lower/upper source rows.")
    lines.append("")
    lines.append("## Hard-fragmenting target variables")
    lines.append("")
    if hard.empty:
        lines.append("No hard-fragmenting target variables were found in the supplied STRUC-PERC-I result files.")
    else:
        for subset, subdf in hard.groupby("subset"):
            vars_ = sorted(set(subdf["variable"]))
            lines.append(f"- **{subset}**: " + ", ".join(f"`{v}`" for v in vars_))
    lines.append("")
    lines.append("## Non-giant components requiring inspection")
    lines.append("")
    if nongiant.empty:
        lines.append("No non-giant components were reconstructed for the target variables at κ = 1.")
    else:
        cols = ["subset", "variable", "component_id", "component_role", "component_size_gaps", "involved_row_count", "involved_shot_count", "involved_shots", "event_time_min", "event_time_max"]
        table = nongiant[cols].sort_values(["subset", "variable", "component_role", "component_id"]).head(60)
        lines.append(table.to_markdown(index=False))
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("Rows adjacent to non-giant components are the first candidates for transition-family inspection. They are not automatically errors or outliers; in UNNS terms they are candidate branch points or isolated admissibility corridors in the transition corpus.")
    lines.append("")
    lines.append("## Generated outputs")
    lines.append("")
    lines.append("- `tcv_fragment_component_summary.csv`")
    lines.append("- `tcv_fragment_gap_map.csv`")
    lines.append("- `tcv_suspect_transition_families.csv`")
    lines.append("- `tcv_fragment_isolate_mapping_summary.json`")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Map TCV STRUC-PERC fragment branches back to source rows/shots.")
    ap.add_argument("--canonical", default="data/processed/tcv_lh_events_canonical.csv", help="Canonical TCV CSV")
    ap.add_argument("--all-perc-json", default="outputs/reports/struc_perc_batch_results.json", help="STRUC-PERC all-events JSON")
    ap.add_argument("--lh-perc-json", default="outputs/reports/struc_perc_batch_results_lh_only.json", help="STRUC-PERC L-H-only JSON")
    ap.add_argument("--out-dir", default="outputs/reports", help="Output report directory")
    ap.add_argument("--kappa-max", type=float, default=1.0, help="κ used for final isolate mapping")
    ap.add_argument("--targets", nargs="*", default=DEFAULT_TARGETS, help="Variables to inspect")
    args = ap.parse_args()

    canonical = Path(args.canonical)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not canonical.exists():
        raise FileNotFoundError(f"Canonical CSV not found: {canonical}")

    df = pd.read_csv(canonical)
    # Preserve source row index for mapping.
    df = df.reset_index().rename(columns={"index": "source_row_index"})

    result_map = load_struc_perc_results(Path(args.all_perc_json), Path(args.lh_perc_json))

    subsets = {
        "all_events": df.copy(),
        "lh_only": df[(df.get("event_type").astype(str).str.upper() == "LH") | (pd.to_numeric(df.get("src_ILH"), errors="coerce") == 1)].copy(),
    }

    all_components: list[dict] = []
    all_gaps: list[dict] = []
    all_families: list[dict] = []

    for subset_name, sdf in subsets.items():
        for variable in args.targets:
            chamber_result = result_map.get((subset_name, variable), {})
            comp, gaps, fam = analyze_variable(sdf, subset_name, variable, chamber_result, args.kappa_max)
            all_components.extend(comp)
            all_gaps.extend(gaps)
            all_families.extend(fam)

    component_df = pd.DataFrame(all_components)
    gap_df = pd.DataFrame(all_gaps)
    family_df = pd.DataFrame(all_families)

    # Sort outputs for readability.
    if not component_df.empty:
        component_df = component_df.sort_values(["subset", "variable", "component_id"])
    if not gap_df.empty:
        gap_df = gap_df.sort_values(["subset", "variable", "component_id", "gap_index_in_sorted_unique_ladder"])
    if not family_df.empty:
        family_df = family_df.sort_values(["mapping_priority", "subset", "variable", "component_role", "component_id"], ascending=[True, True, True, True, True])

    component_path = out_dir / "tcv_fragment_component_summary.csv"
    gap_path = out_dir / "tcv_fragment_gap_map.csv"
    family_path = out_dir / "tcv_suspect_transition_families.csv"
    report_path = out_dir / "tcv_fragment_isolate_mapping_report.md"
    summary_path = out_dir / "tcv_fragment_isolate_mapping_summary.json"

    component_df.to_csv(component_path, index=False)
    gap_df.to_csv(gap_path, index=False)
    family_df.to_csv(family_path, index=False)
    make_markdown_report(component_df, family_df, report_path)

    summary = {
        "source": str(canonical),
        "rows": int(len(df)),
        "targets": args.targets,
        "subsets": {k: int(len(v)) for k, v in subsets.items()},
        "component_rows": int(len(component_df)),
        "gap_rows": int(len(gap_df)),
        "suspect_family_rows": int(len(family_df)),
        "outputs": {
            "component_summary_csv": str(component_path),
            "gap_map_csv": str(gap_path),
            "suspect_transition_families_csv": str(family_path),
            "markdown_report": str(report_path),
        },
    }
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("Fragment isolate mapping complete.")
    print(f"  components: {component_path}")
    print(f"  gaps:       {gap_path}")
    print(f"  families:   {family_path}")
    print(f"  report:     {report_path}")
    print(f"  summary:    {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
