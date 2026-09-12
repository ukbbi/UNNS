#!/usr/bin/env python3
"""
edge_admissibility_event_model.py

UNNS-H Mode event-level edge admissibility model v0.1.

Purpose
-------
Convert the four empirically observed branch families from the TCV L-H pilot
(power-balance, transport, edge/divertor response, timing) into a first
formal event-level UNNS model: m_edge_event.

This is NOT the full time-dependent m_edge(t). It is an event-table precursor
built for the limited TCV Zenodo event-level dataset.

Inputs
------
--canonical    data/processed/tcv_lh_events_canonical.csv
--shot-review  outputs/reports/tcv_suspect_shot_review.csv
--out-dir      outputs/reports

Outputs
-------
- tcv_edge_event_model_scores.csv
- tcv_edge_event_model_summary.md
- tcv_edge_event_model_summary.json

Run
---
python components/edge_admissibility_event_model.py \
  --canonical data/processed/tcv_lh_events_canonical.csv \
  --shot-review outputs/reports/tcv_suspect_shot_review.csv \
  --out-dir outputs/reports
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

EPS = 1e-12

POWER_COLS = ["P_loss_candidate_MW", "P_total_candidate_MW", "P_total_aux_candidate_MW"]
TRANSPORT_COLS = ["chi_eff_candidate"]
EDGE_COLS = ["divertor_signal_candidate", "divertor_signal_150_candidate"]
DENSITY_COL = "n_e_1e20_m3"
GEOMETRY_COLS = ["q95", "kappa", "delta", "B_t_T"]
SPECIES_COLS = ["hydrogen_fraction_candidate", "helium_fraction_candidate"]

TARGET_SHOTS = [69807, 68001, 69668, 69892, 66445, 68719, 69913, 67992, 68206]


def coerce_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def percentile_rank(value: float, reference: pd.Series) -> float:
    """Return [0, 1] percentile rank for value against finite reference."""
    ref = coerce_numeric(reference).dropna().to_numpy(dtype=float)
    if not np.isfinite(value) or len(ref) == 0:
        return np.nan
    return float(np.mean(ref <= value))


def robust_geometry_stability(row: pd.Series, reference: pd.DataFrame) -> float:
    """1 means geometrically ordinary/stable; 0 means highly geometry-displaced."""
    deviations = []
    for col in GEOMETRY_COLS:
        if col not in reference.columns or col not in row.index:
            continue
        ref = coerce_numeric(reference[col]).dropna().to_numpy(dtype=float)
        x = pd.to_numeric(row[col], errors="coerce")
        if not np.isfinite(x) or len(ref) < 3:
            continue
        med = float(np.nanmedian(ref))
        mad = float(np.nanmedian(np.abs(ref - med)))
        scale = 1.4826 * mad if mad > EPS else float(np.nanstd(ref))
        if not np.isfinite(scale) or scale <= EPS:
            continue
        z = abs((float(x) - med) / scale)
        deviations.append(min(z / 3.0, 1.0))
    if not deviations:
        return 0.5
    return float(1.0 - np.mean(deviations))


def contains_tag(tags: str, tag: str) -> int:
    return int(tag in str(tags).split(";"))


def max_percentile(row: pd.Series, reference: pd.DataFrame, cols: Iterable[str]) -> float:
    vals = []
    for col in cols:
        if col in row.index and col in reference.columns:
            x = pd.to_numeric(row[col], errors="coerce")
            vals.append(percentile_rank(float(x), reference[col]) if np.isfinite(x) else np.nan)
    vals = [v for v in vals if np.isfinite(v)]
    return float(max(vals)) if vals else np.nan


def mean_percentile(row: pd.Series, reference: pd.DataFrame, cols: Iterable[str]) -> float:
    vals = []
    for col in cols:
        if col in row.index and col in reference.columns:
            x = pd.to_numeric(row[col], errors="coerce")
            vals.append(percentile_rank(float(x), reference[col]) if np.isfinite(x) else np.nan)
    vals = [v for v in vals if np.isfinite(v)]
    return float(np.mean(vals)) if vals else np.nan


def event_span_score(row: pd.Series, reference_review: pd.DataFrame) -> float:
    """Normalize event-time span among reviewed shots. Larger span -> timing pressure."""
    span = pd.to_numeric(row.get("event_time_max", np.nan), errors="coerce") - pd.to_numeric(row.get("event_time_min", np.nan), errors="coerce")
    spans = (coerce_numeric(reference_review.get("event_time_max", pd.Series(dtype=float))) -
             coerce_numeric(reference_review.get("event_time_min", pd.Series(dtype=float)))).dropna()
    if not np.isfinite(span) or spans.empty:
        return 0.0
    max_span = float(spans.max())
    if max_span <= EPS:
        return 0.0
    return float(np.clip(span / max_span, 0.0, 1.0))


def classify_corridor(row: pd.Series) -> str:
    m = row["m_edge_event"]
    sp = row["S_power_balance"]
    st = row["S_transport"]
    se = row["S_edge_response"]
    sx = row["S_timing"]

    if se >= 0.65 and m >= 0.05:
        return "edge_divertor_response_corridor"
    if sx >= 0.65 and sp < 0.55 and st < 0.65:
        return "timing_only_or_timing_dominant_corridor"
    if sp >= 0.65 and st >= 0.65 and sx >= 0.65:
        return "mixed_power_transport_timing_leakage_corridor"
    if sp >= 0.65 and st >= 0.65:
        return "power_transport_corridor"
    if st >= 0.65 and sx >= 0.65:
        return "transport_timing_corridor"
    if sp >= 0.65:
        return "power_balance_corridor"
    if st >= 0.65:
        return "transport_corridor"
    return "weak_or_unclassified_corridor"


def margin_state(m: float) -> str:
    if m >= 0.20:
        return "positive_boundary_margin"
    if m <= -0.20:
        return "negative_leakage_margin"
    return "boundary_ambiguous_margin"


def build_model_scores(canonical: pd.DataFrame, review: pd.DataFrame) -> pd.DataFrame:
    # Use canonical event rows as the reference distribution for percentiles.
    ref = canonical.copy()

    rows = []
    for _, row in review.iterrows():
        tags = str(row.get("fragment_tags", ""))
        B_power = contains_tag(tags, "power_balance_branch")
        B_transport = contains_tag(tags, "transport_branch")
        B_edge = contains_tag(tags, "edge_divertor_response_branch")
        B_timing = contains_tag(tags, "timing_branch")

        power_level = max_percentile(row, ref, POWER_COLS)
        transport_level = mean_percentile(row, ref, TRANSPORT_COLS)
        edge_level = mean_percentile(row, ref, EDGE_COLS)
        density_support = percentile_rank(float(pd.to_numeric(row.get(DENSITY_COL, np.nan), errors="coerce")), ref[DENSITY_COL]) if DENSITY_COL in ref.columns else np.nan
        species_position = mean_percentile(row, ref, SPECIES_COLS)
        geom_stability = robust_geometry_stability(row, ref)
        timing_span = event_span_score(row, review)

        # Branch evidence scores. Tag evidence gets priority; scalar rank refines intensity.
        S_power = 0.65 * B_power + 0.35 * (0.0 if not np.isfinite(power_level) else power_level)
        S_transport = 0.70 * B_transport + 0.30 * (0.0 if not np.isfinite(transport_level) else transport_level)
        S_edge = 0.65 * B_edge + 0.35 * (0.0 if not np.isfinite(edge_level) else edge_level)
        S_timing = 0.70 * B_timing + 0.30 * timing_span

        # Event-level decomposition. Route pressure penalizes fragmented power/transport/timing.
        # Boundary capacity rewards observable edge response, density support, and geometry stability.
        F_route = 0.35 * S_power + 0.35 * S_transport + 0.30 * S_timing
        C_edge = 0.45 * S_edge + 0.25 * (0.5 if not np.isfinite(density_support) else density_support) + 0.15 * geom_stability + 0.15 * (0.5 if not np.isfinite(species_position) else species_position)
        m_edge = C_edge - F_route

        out = row.to_dict()
        out.update({
            "B_power_balance": B_power,
            "B_transport": B_transport,
            "B_edge_divertor_response": B_edge,
            "B_timing": B_timing,
            "power_level_percentile": power_level,
            "transport_level_percentile": transport_level,
            "edge_response_percentile": edge_level,
            "density_support_percentile": density_support,
            "species_position_percentile": species_position,
            "geometry_stability": geom_stability,
            "timing_span_score": timing_span,
            "S_power_balance": S_power,
            "S_transport": S_transport,
            "S_edge_response": S_edge,
            "S_timing": S_timing,
            "F_route_fragmentation": F_route,
            "C_edge_capacity": C_edge,
            "m_edge_event": m_edge,
        })
        rows.append(out)

    scores = pd.DataFrame(rows)
    scores["m_edge_state"] = scores["m_edge_event"].apply(margin_state)
    scores["formal_corridor"] = scores.apply(classify_corridor, axis=1)
    # Rank: strongest negative leakage first, then strongest edge response.
    scores["review_order"] = scores["m_edge_event"].rank(method="first", ascending=True).astype(int)
    return scores.sort_values(["m_edge_event", "fragment_count"], ascending=[True, False])


def write_summary(scores: pd.DataFrame, out_path: Path) -> None:
    corridor_counts = scores["formal_corridor"].value_counts().to_dict()
    state_counts = scores["m_edge_state"].value_counts().to_dict()

    lines = []
    lines.append("# TCV Event-Level Edge-Admissibility Model v0.1")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append("This report converts the four observed TCV branch families into a first formal UNNS-H Mode event-level model. It does not run another chamber and does not claim a full time-dependent edge margin. It defines and evaluates `m_edge_event`, an event-table precursor to `m_edge(t)`.")
    lines.append("")
    lines.append("## Model definition")
    lines.append("")
    lines.append("The observed branch vector is:")
    lines.append("")
    lines.append("```text")
    lines.append("β_event = (B_power_balance, B_transport, B_edge_divertor_response, B_timing)")
    lines.append("```")
    lines.append("")
    lines.append("The event-level margin is:")
    lines.append("")
    lines.append("```text")
    lines.append("m_edge_event = C_edge_capacity - F_route_fragmentation")
    lines.append("```")
    lines.append("")
    lines.append("where route fragmentation is driven by power-balance, transport, and timing branch evidence, while edge capacity is driven by edge/divertor response, density support, geometry stability, and species position.")
    lines.append("")
    lines.append("## Margin states")
    lines.append("")
    for k, v in state_counts.items():
        lines.append(f"- `{k}`: {v} shots")
    lines.append("")
    lines.append("## Formal corridor counts")
    lines.append("")
    for k, v in corridor_counts.items():
        lines.append(f"- `{k}`: {v} shots")
    lines.append("")
    lines.append("## Scored shot table")
    lines.append("")
    view_cols = ["SHOT", "ILH", "fragment_count", "fragment_tags", "S_power_balance", "S_transport", "S_edge_response", "S_timing", "F_route_fragmentation", "C_edge_capacity", "m_edge_event", "m_edge_state", "formal_corridor"]
    lines.append(scores[view_cols].to_markdown(index=False, floatfmt=".3f"))
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The most negative margins represent route-fragmentation-dominated events: power-balance, transport, and/or timing pressure exceed event-level boundary response capacity. The positive or less negative margins represent candidate edge-response corridors where divertor/edge response and density support partly offset route fragmentation.")
    lines.append("")
    lines.append("In this first v0.1 model, `69807` is the strongest mixed leakage case because it combines power-balance, transport, and timing branch evidence with weak edge/divertor response. The edge-divertor trio is separated because it has strong boundary-response evidence rather than mixed route-fragmentation evidence.")
    lines.append("")
    lines.append("## What this model is not")
    lines.append("")
    lines.append("This is not a proof of H-mode origin, not a reactor confinement model, and not a replacement for plasma physics. It is a formal UNNS event-level bridge from observed branch families to a computable edge-admissibility precursor.")
    lines.append("")
    lines.append("## Next use")
    lines.append("")
    lines.append("Use this model to test whether branch families occupy separable regions in feature space. Once richer time-series data are available, replace `m_edge_event` with `m_edge(t)` and test whether the margin rises before L-H transition and weakens before ELM or H-L relaxation.")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--canonical", required=True)
    ap.add_argument("--shot-review", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    canonical = pd.read_csv(args.canonical)
    review = pd.read_csv(args.shot_review)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    scores = build_model_scores(canonical, review)

    csv_path = out_dir / "tcv_edge_event_model_scores.csv"
    md_path = out_dir / "tcv_edge_event_model_summary.md"
    json_path = out_dir / "tcv_edge_event_model_summary.json"

    scores.to_csv(csv_path, index=False)
    write_summary(scores, md_path)

    summary = {
        "model": "UNNS-H Mode event-level edge-admissibility model",
        "version": "0.1",
        "shot_count": int(len(scores)),
        "margin_state_counts": scores["m_edge_state"].value_counts().to_dict(),
        "formal_corridor_counts": scores["formal_corridor"].value_counts().to_dict(),
        "lowest_margin_shots": scores[["SHOT", "m_edge_event", "formal_corridor", "fragment_tags"]].head(5).to_dict(orient="records"),
        "highest_margin_shots": scores[["SHOT", "m_edge_event", "formal_corridor", "fragment_tags"]].tail(5).to_dict(orient="records"),
        "outputs": {
            "scores_csv": str(csv_path),
            "summary_md": str(md_path),
        },
    }
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("Event-level edge admissibility model complete.")
    print(f"Scores:  {csv_path}")
    print(f"Report:  {md_path}")
    print(f"Summary: {json_path}")


if __name__ == "__main__":
    main()
