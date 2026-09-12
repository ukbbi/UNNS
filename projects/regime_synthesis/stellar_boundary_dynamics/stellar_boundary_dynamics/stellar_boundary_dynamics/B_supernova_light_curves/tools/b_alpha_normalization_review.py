#!/usr/bin/env python3
"""
b_alpha_normalization_review.py

Phase B alpha normalization review for STELLAR_BOUNDARY_DYNAMICS_I.

Reads:
  alpha_application/grids/*.csv
  alpha_application/summaries/B_5D_VECTOR_SUMMARY.csv

Writes:
  alpha_application/normalization_review/B_ALPHA_NORMALIZATION_REVIEW.csv
  alpha_application/normalization_review/B_5D_VECTOR_SUMMARY_v2.csv
  alpha_application/normalization_review/B_NORMALIZATION_REVIEW_INTERPRETATION.txt

Purpose:
  detect slope/curvature domination
  bound anisotropic_persistence
  recompute comparable v2 vectors
  preserve original v1 outputs

Usage from B_supernova_light_curves/:
  python tools/b_alpha_normalization_review.py alpha_application/grids alpha_application/summaries/B_5D_VECTOR_SUMMARY.csv alpha_application/normalization_review
"""

import csv
import math
import statistics
import sys
from pathlib import Path


REVIEW_COLUMNS = [
    "object_id",
    "object_name",
    "grid_file",
    "n_rows",
    "mean_gap_response",
    "mean_duration_response",
    "mean_slope_response",
    "mean_curvature_response",
    "max_channel",
    "slope_to_gap_ratio",
    "curvature_to_gap_ratio",
    "max_channel_to_gap_ratio",
    "original_anisotropic_persistence",
    "bounded_anisotropic_persistence",
    "admissibility_persistence",
    "collapse_onset_radius",
    "collapse_observed",
    "kappa_connect_reference",
    "tail_dominance_reference",
    "slope_dominant",
    "curvature_dominant",
    "scale_review_needed",
    "high_tail_attention",
    "review_status",
]

V2_COLUMNS = [
    "object_id",
    "object_name",
    "supernova_type",
    "mean_GR",
    "var_GR",
    "anisotropic_persistence_v1",
    "anisotropic_persistence_bounded",
    "admissibility_persistence",
    "collapse_onset_radius",
    "collapse_observed",
    "kappa_connect_reference",
    "tail_dominance_reference",
    "slope_to_gap_ratio",
    "curvature_to_gap_ratio",
    "scale_review_needed",
    "notes",
]


def read_csv(path):
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, columns):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def to_float(value, default=0.0):
    try:
        if value is None or str(value).strip() == "":
            return default
        x = float(value)
        if math.isnan(x) or math.isinf(x):
            return default
        return x
    except Exception:
        return default


def fmt(x):
    if isinstance(x, float):
        return f"{x:.10g}"
    return str(x)


def mean(values):
    values = [v for v in values if math.isfinite(v)]
    return statistics.fmean(values) if values else 0.0


def variance(values):
    values = [v for v in values if math.isfinite(v)]
    return statistics.pvariance(values) if len(values) >= 2 else 0.0


def bounded(x):
    x = max(0.0, x)
    return x / (1.0 + x)


def object_id_from_grid(path):
    stem = Path(path).stem
    if stem.endswith("_alpha_grid"):
        return stem.replace("_alpha_grid", "")
    return stem


def review_grid(grid_file, v1_lookup):
    rows = read_csv(grid_file)
    object_id = object_id_from_grid(grid_file)
    v1 = v1_lookup.get(object_id, {})

    object_name = rows[0].get("object_name", object_id) if rows else object_id

    gap_vals = [to_float(r.get("gap_response_norm")) for r in rows]
    duration_vals = [to_float(r.get("duration_response_norm")) for r in rows]
    slope_vals = [to_float(r.get("slope_response_norm")) for r in rows]
    curvature_vals = [to_float(r.get("curvature_response_norm")) for r in rows]

    mg = mean(gap_vals)
    md = mean(duration_vals)
    ms = mean(slope_vals)
    mc = mean(curvature_vals)

    channels = {
        "gap": mg,
        "duration": md,
        "slope": ms,
        "curvature": mc,
    }
    max_channel = max(channels, key=channels.get)
    eps = 1e-12
    slope_to_gap = ms / max(mg, eps)
    curvature_to_gap = mc / max(mg, eps)
    max_to_gap = channels[max_channel] / max(mg, eps)

    anis_v1 = to_float(v1.get("anisotropic_persistence"))
    anis_bounded = bounded(anis_v1)

    tail = to_float(v1.get("tail_dominance_reference"))
    kappa = to_float(v1.get("kappa_connect_reference"))
    adm = to_float(v1.get("admissibility_persistence"))
    collapse_radius = to_float(v1.get("collapse_onset_radius"))
    collapse_observed = v1.get("collapse_observed", "")

    slope_dominant = "yes" if slope_to_gap >= 10.0 and ms == channels[max_channel] else "no"
    curvature_dominant = "yes" if curvature_to_gap >= 10.0 and mc == channels[max_channel] else "no"
    scale_review_needed = "yes" if slope_to_gap >= 10.0 or curvature_to_gap >= 10.0 or anis_v1 >= 100.0 else "no"
    high_tail_attention = "yes" if tail >= 0.10 or kappa >= 2.0 else "no"

    if scale_review_needed == "yes":
        status = "review_required"
    else:
        status = "comparable"

    return {
        "object_id": object_id,
        "object_name": object_name,
        "grid_file": str(grid_file),
        "n_rows": len(rows),
        "mean_gap_response": fmt(mg),
        "mean_duration_response": fmt(md),
        "mean_slope_response": fmt(ms),
        "mean_curvature_response": fmt(mc),
        "max_channel": max_channel,
        "slope_to_gap_ratio": fmt(slope_to_gap),
        "curvature_to_gap_ratio": fmt(curvature_to_gap),
        "max_channel_to_gap_ratio": fmt(max_to_gap),
        "original_anisotropic_persistence": fmt(anis_v1),
        "bounded_anisotropic_persistence": fmt(anis_bounded),
        "admissibility_persistence": fmt(adm),
        "collapse_onset_radius": fmt(collapse_radius),
        "collapse_observed": collapse_observed,
        "kappa_connect_reference": fmt(kappa),
        "tail_dominance_reference": fmt(tail),
        "slope_dominant": slope_dominant,
        "curvature_dominant": curvature_dominant,
        "scale_review_needed": scale_review_needed,
        "high_tail_attention": high_tail_attention,
        "review_status": status,
    }


def make_v2_vector(v1_row, review_row):
    object_id = v1_row.get("object_id", review_row["object_id"])
    object_name = v1_row.get("object_name", review_row["object_name"])
    notes = [
        "v2 normalization-review vector",
        "anisotropic_persistence is bounded as x/(1+x)",
        "v1 outputs preserved separately",
    ]
    if review_row["scale_review_needed"] == "yes":
        notes.append("scale review needed before final physical interpretation")
    if review_row["high_tail_attention"] == "yes":
        notes.append("high tail/kappa attention")
    if object_id == "B_SN2012aw":
        notes.append("SN2012aw remains special sensitivity candidate")

    return {
        "object_id": object_id,
        "object_name": object_name,
        "supernova_type": v1_row.get("supernova_type", ""),
        "mean_GR": v1_row.get("mean_GR", ""),
        "var_GR": v1_row.get("var_GR", ""),
        "anisotropic_persistence_v1": v1_row.get("anisotropic_persistence", ""),
        "anisotropic_persistence_bounded": review_row["bounded_anisotropic_persistence"],
        "admissibility_persistence": v1_row.get("admissibility_persistence", ""),
        "collapse_onset_radius": v1_row.get("collapse_onset_radius", ""),
        "collapse_observed": v1_row.get("collapse_observed", ""),
        "kappa_connect_reference": v1_row.get("kappa_connect_reference", ""),
        "tail_dominance_reference": v1_row.get("tail_dominance_reference", ""),
        "slope_to_gap_ratio": review_row["slope_to_gap_ratio"],
        "curvature_to_gap_ratio": review_row["curvature_to_gap_ratio"],
        "scale_review_needed": review_row["scale_review_needed"],
        "notes": "; ".join(notes),
    }


def write_interpretation(path, review_rows, v2_rows):
    scale_needed = [r for r in review_rows if r["scale_review_needed"] == "yes"]
    tail_attention = [r for r in review_rows if r["high_tail_attention"] == "yes"]
    comparable = [r for r in review_rows if r["review_status"] == "comparable"]

    lines = []
    lines.append("# B_NORMALIZATION_REVIEW_INTERPRETATION.txt")
    lines.append("# STELLAR_BOUNDARY_DYNAMICS_I")
    lines.append("# Phase B — Alpha Normalization Review Interpretation")
    lines.append("")
    lines.append("PURPOSE:")
    lines.append("Interpret the normalization review performed on Phase B alpha grids and")
    lines.append("first-pass 5D vectors.")
    lines.append("")
    lines.append("PRIMARY FINDING:")
    if scale_needed:
        lines.append("Some objects show scale domination in slope/curvature or very large original")
        lines.append("anisotropic_persistence. The v1 vectors remain useful diagnostics, but the")
        lines.append("bounded v2 vector summary should be used for cross-object comparison.")
    else:
        lines.append("No major slope/curvature dominance was detected. The v1 and v2 summaries are")
        lines.append("consistent for comparison.")
    lines.append("")
    lines.append("REVIEW STATUS COUNTS:")
    lines.append(f"Comparable objects: {len(comparable)}")
    lines.append(f"Scale-review-needed objects: {len(scale_needed)}")
    lines.append(f"High-tail/kappa-attention objects: {len(tail_attention)}")
    lines.append("")
    lines.append("OBJECT FLAGS:")
    for r in review_rows:
        lines.append(
            f"{r['object_name']}: "
            f"status={r['review_status']}; "
            f"scale_review_needed={r['scale_review_needed']}; "
            f"high_tail_attention={r['high_tail_attention']}; "
            f"max_channel={r['max_channel']}; "
            f"slope/gap={r['slope_to_gap_ratio']}; "
            f"curvature/gap={r['curvature_to_gap_ratio']}; "
            f"bounded_anis={r['bounded_anisotropic_persistence']}"
        )
    lines.append("")
    lines.append("V2 VECTOR USE:")
    lines.append("Use B_5D_VECTOR_SUMMARY_v2.csv for A–B comparison because it preserves the")
    lines.append("original v1 values while adding bounded anisotropic persistence and review")
    lines.append("flags.")
    lines.append("")
    lines.append("INTERPRETATION RULE:")
    lines.append("A scale-review flag is not a failure. It means the object should not be")
    lines.append("compared using raw anisotropic_persistence alone.")
    lines.append("")
    lines.append("SN2012aw NOTE:")
    lines.append("SN2012aw remains the main special case because it combines high κ_connect,")
    lines.append("high tail dominance, and strong deformation sensitivity. It should be kept as")
    lines.append("a named candidate for deeper inspection.")
    lines.append("")
    lines.append("NEXT STEP:")
    lines.append("Proceed to the A–B bridge only using the normalization-reviewed v2 vector")
    lines.append("summary, not the raw v1 vector summary alone.")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)

    grids_dir = Path(sys.argv[1])
    v1_path = Path(sys.argv[2])
    out_dir = Path(sys.argv[3])
    out_dir.mkdir(parents=True, exist_ok=True)

    v1_rows = read_csv(v1_path)
    v1_lookup = {row.get("object_id", ""): row for row in v1_rows}

    review_rows = []
    for grid_file in sorted(grids_dir.glob("B_*_alpha_grid.csv")):
        review_rows.append(review_grid(grid_file, v1_lookup))

    review_lookup = {row["object_id"]: row for row in review_rows}
    v2_rows = []
    for v1 in v1_rows:
        oid = v1.get("object_id", "")
        if oid in review_lookup:
            v2_rows.append(make_v2_vector(v1, review_lookup[oid]))

    review_csv = out_dir / "B_ALPHA_NORMALIZATION_REVIEW.csv"
    v2_csv = out_dir / "B_5D_VECTOR_SUMMARY_v2.csv"
    interpretation_txt = out_dir / "B_NORMALIZATION_REVIEW_INTERPRETATION.txt"

    write_csv(review_csv, review_rows, REVIEW_COLUMNS)
    write_csv(v2_csv, v2_rows, V2_COLUMNS)
    write_interpretation(interpretation_txt, review_rows, v2_rows)

    print(f"Review written: {review_csv}")
    print(f"V2 vectors written: {v2_csv}")
    print(f"Interpretation written: {interpretation_txt}")
    print(f"Objects reviewed: {len(review_rows)}")
    print(f"Scale-review-needed: {sum(1 for r in review_rows if r['scale_review_needed'] == 'yes')}")
    print(f"High-tail-attention: {sum(1 for r in review_rows if r['high_tail_attention'] == 'yes')}")


if __name__ == "__main__":
    main()
