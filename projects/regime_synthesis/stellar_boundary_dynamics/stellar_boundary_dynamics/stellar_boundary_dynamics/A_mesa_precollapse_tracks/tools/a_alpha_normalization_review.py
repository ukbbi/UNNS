#!/usr/bin/env python3
"""
a_alpha_normalization_review.py

Phase A alpha normalization review for STELLAR_BOUNDARY_DYNAMICS_I.

Reads:
  alpha_application/grids/*.csv
  alpha_application/summaries/A_5D_VECTOR_SUMMARY.csv

Writes:
  alpha_application/normalization_review/A_ALPHA_NORMALIZATION_REVIEW.csv
  alpha_application/normalization_review/A_5D_VECTOR_SUMMARY_v2.csv
  alpha_application/normalization_review/A_NORMALIZATION_REVIEW_INTERPRETATION.txt

Purpose:
  detect response-channel domination
  bound anisotropic_persistence
  recompute comparable v2 vectors
  preserve original v1 outputs

Usage from A_mesa_precollapse_tracks/:

  python tools/a_alpha_normalization_review.py alpha_application/grids alpha_application/summaries/A_5D_VECTOR_SUMMARY.csv alpha_application/normalization_review
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
    "mean_thermal_response",
    "mean_density_response",
    "mean_composition_response",
    "mean_support_response",
    "mean_loss_response",
    "max_channel",
    "thermal_to_gap_ratio",
    "density_to_gap_ratio",
    "composition_to_gap_ratio",
    "support_to_gap_ratio",
    "loss_to_gap_ratio",
    "max_channel_to_gap_ratio",
    "original_anisotropic_persistence",
    "bounded_anisotropic_persistence",
    "admissibility_persistence",
    "collapse_onset_radius",
    "collapse_observed",
    "kappa_connect_reference",
    "tail_dominance_reference",
    "thermal_dominant",
    "density_dominant",
    "composition_dominant",
    "support_dominant",
    "loss_dominant",
    "scale_review_needed",
    "high_kappa_attention",
    "review_status",
]

V2_COLUMNS = [
    "object_id",
    "object_name",
    "target_mass_class",
    "selected_model_mass",
    "progenitor_type",
    "network",
    "mean_GR",
    "var_GR",
    "anisotropic_persistence_v1",
    "anisotropic_persistence_bounded",
    "admissibility_persistence",
    "collapse_onset_radius",
    "collapse_observed",
    "kappa_connect_reference",
    "tail_dominance_reference",
    "thermal_to_gap_ratio",
    "density_to_gap_ratio",
    "composition_to_gap_ratio",
    "support_to_gap_ratio",
    "loss_to_gap_ratio",
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


def fmt(value):
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def mean(values):
    values = [v for v in values if math.isfinite(v)]
    return statistics.fmean(values) if values else 0.0


def bounded(x):
    x = max(0.0, x)
    return x / (1.0 + x)


def object_id_from_grid(path):
    stem = Path(path).stem
    if stem.endswith("_alpha_grid"):
        return stem.replace("_alpha_grid", "")
    return stem


def ratio(channel_mean, gap_mean):
    eps = 1e-12
    return channel_mean / max(gap_mean, eps)


def dominance_flag(channel_name, max_channel, channel_to_gap_ratio, threshold=10.0):
    return "yes" if channel_name == max_channel and channel_to_gap_ratio >= threshold else "no"


def review_grid(grid_file, v1_lookup):
    rows = read_csv(grid_file)
    object_id = object_id_from_grid(grid_file)
    v1 = v1_lookup.get(object_id, {})

    object_name = rows[0].get("object_name", object_id) if rows else object_id

    gap_vals = [to_float(r.get("gap_response_norm")) for r in rows]
    thermal_vals = [to_float(r.get("thermal_response_norm")) for r in rows]
    density_vals = [to_float(r.get("density_response_norm")) for r in rows]
    composition_vals = [to_float(r.get("composition_response_norm")) for r in rows]
    support_vals = [to_float(r.get("support_response_norm")) for r in rows]
    loss_vals = [to_float(r.get("loss_response_norm")) for r in rows]

    mg = mean(gap_vals)
    mt = mean(thermal_vals)
    md = mean(density_vals)
    mc = mean(composition_vals)
    ms = mean(support_vals)
    ml = mean(loss_vals)

    channels = {
        "gap": mg,
        "thermal": mt,
        "density": md,
        "composition": mc,
        "support": ms,
        "loss": ml,
    }
    max_channel = max(channels, key=channels.get)

    thermal_to_gap = ratio(mt, mg)
    density_to_gap = ratio(md, mg)
    composition_to_gap = ratio(mc, mg)
    support_to_gap = ratio(ms, mg)
    loss_to_gap = ratio(ml, mg)
    max_to_gap = ratio(channels[max_channel], mg)

    anis_v1 = to_float(v1.get("anisotropic_persistence"))
    anis_bounded = bounded(anis_v1)

    adm = to_float(v1.get("admissibility_persistence"))
    collapse_radius = to_float(v1.get("collapse_onset_radius"))
    collapse_observed = v1.get("collapse_observed", "")

    kappa = to_float(v1.get("kappa_connect_reference"))
    tail = to_float(v1.get("tail_dominance_reference"))

    thermal_dominant = dominance_flag("thermal", max_channel, thermal_to_gap)
    density_dominant = dominance_flag("density", max_channel, density_to_gap)
    composition_dominant = dominance_flag("composition", max_channel, composition_to_gap)
    support_dominant = dominance_flag("support", max_channel, support_to_gap)
    loss_dominant = dominance_flag("loss", max_channel, loss_to_gap)

    any_ratio_high = max(
        thermal_to_gap,
        density_to_gap,
        composition_to_gap,
        support_to_gap,
        loss_to_gap,
    ) >= 10.0

    scale_review_needed = "yes" if any_ratio_high or anis_v1 >= 100.0 else "no"
    high_kappa_attention = "yes" if kappa >= 2.0 else "no"

    review_status = "review_required" if scale_review_needed == "yes" else "comparable"

    return {
        "object_id": object_id,
        "object_name": object_name,
        "grid_file": str(grid_file),
        "n_rows": len(rows),
        "mean_gap_response": fmt(mg),
        "mean_thermal_response": fmt(mt),
        "mean_density_response": fmt(md),
        "mean_composition_response": fmt(mc),
        "mean_support_response": fmt(ms),
        "mean_loss_response": fmt(ml),
        "max_channel": max_channel,
        "thermal_to_gap_ratio": fmt(thermal_to_gap),
        "density_to_gap_ratio": fmt(density_to_gap),
        "composition_to_gap_ratio": fmt(composition_to_gap),
        "support_to_gap_ratio": fmt(support_to_gap),
        "loss_to_gap_ratio": fmt(loss_to_gap),
        "max_channel_to_gap_ratio": fmt(max_to_gap),
        "original_anisotropic_persistence": fmt(anis_v1),
        "bounded_anisotropic_persistence": fmt(anis_bounded),
        "admissibility_persistence": fmt(adm),
        "collapse_onset_radius": fmt(collapse_radius),
        "collapse_observed": collapse_observed,
        "kappa_connect_reference": fmt(kappa),
        "tail_dominance_reference": fmt(tail),
        "thermal_dominant": thermal_dominant,
        "density_dominant": density_dominant,
        "composition_dominant": composition_dominant,
        "support_dominant": support_dominant,
        "loss_dominant": loss_dominant,
        "scale_review_needed": scale_review_needed,
        "high_kappa_attention": high_kappa_attention,
        "review_status": review_status,
    }


def make_v2_vector(v1_row, review_row):
    notes = [
        "v2 normalization-review vector",
        "anisotropic_persistence bounded as x/(1+x)",
        "v1 outputs preserved separately",
        "Phase A is real pre-supernova radial-profile data",
    ]

    if review_row["scale_review_needed"] == "yes":
        notes.append("scale review needed before final physical interpretation")
    if review_row["high_kappa_attention"] == "yes":
        notes.append("high kappa attention")
    if review_row["object_id"] == "A1_12M":
        notes.append("A1 required higher STRUC-PERC-I kappa_connect than A2")
    if review_row["object_id"] == "A2_20M":
        notes.append("A2 was more compact at STRUC-PERC-I kappa_connect layer")

    return {
        "object_id": v1_row.get("object_id", review_row["object_id"]),
        "object_name": v1_row.get("object_name", review_row["object_name"]),
        "target_mass_class": v1_row.get("target_mass_class", ""),
        "selected_model_mass": v1_row.get("selected_model_mass", ""),
        "progenitor_type": v1_row.get("progenitor_type", ""),
        "network": v1_row.get("network", ""),
        "mean_GR": v1_row.get("mean_GR", ""),
        "var_GR": v1_row.get("var_GR", ""),
        "anisotropic_persistence_v1": v1_row.get("anisotropic_persistence", ""),
        "anisotropic_persistence_bounded": review_row["bounded_anisotropic_persistence"],
        "admissibility_persistence": v1_row.get("admissibility_persistence", ""),
        "collapse_onset_radius": v1_row.get("collapse_onset_radius", ""),
        "collapse_observed": v1_row.get("collapse_observed", ""),
        "kappa_connect_reference": v1_row.get("kappa_connect_reference", ""),
        "tail_dominance_reference": v1_row.get("tail_dominance_reference", ""),
        "thermal_to_gap_ratio": review_row["thermal_to_gap_ratio"],
        "density_to_gap_ratio": review_row["density_to_gap_ratio"],
        "composition_to_gap_ratio": review_row["composition_to_gap_ratio"],
        "support_to_gap_ratio": review_row["support_to_gap_ratio"],
        "loss_to_gap_ratio": review_row["loss_to_gap_ratio"],
        "scale_review_needed": review_row["scale_review_needed"],
        "notes": "; ".join(notes),
    }


def write_interpretation(path, review_rows, v2_rows):
    comparable = [r for r in review_rows if r["review_status"] == "comparable"]
    review_needed = [r for r in review_rows if r["review_status"] == "review_required"]
    high_kappa = [r for r in review_rows if r["high_kappa_attention"] == "yes"]

    lines = []
    lines.append("# A_NORMALIZATION_REVIEW_INTERPRETATION.txt")
    lines.append("# STELLAR_BOUNDARY_DYNAMICS_I")
    lines.append("# Phase A — Alpha Normalization Review Interpretation")
    lines.append("")
    lines.append("PURPOSE:")
    lines.append("Interpret the normalization review performed on Phase A alpha grids and")
    lines.append("first-pass 5D vectors.")
    lines.append("")
    lines.append("DATA STATUS:")
    lines.append("Phase A is now based on real processed pre-supernova radial profile data,")
    lines.append("not inlist scaffolds.")
    lines.append("")
    lines.append("REVIEW STATUS COUNTS:")
    lines.append(f"Comparable objects: {len(comparable)}")
    lines.append(f"Scale-review-needed objects: {len(review_needed)}")
    lines.append(f"High-kappa-attention objects: {len(high_kappa)}")
    lines.append("")
    lines.append("PRIMARY FINDING:")
    if review_needed:
        lines.append("At least one Phase A object shows response-channel dominance or very large")
        lines.append("raw anisotropic persistence. Use the v2 vector summary for A–B comparison.")
    else:
        lines.append("No major response-channel domination was detected. Phase A v2 vectors are")
        lines.append("ready for A–B comparison.")
    lines.append("")
    lines.append("OBJECT FLAGS:")
    for r in review_rows:
        lines.append(
            f"{r['object_id']}: "
            f"status={r['review_status']}; "
            f"scale_review_needed={r['scale_review_needed']}; "
            f"high_kappa_attention={r['high_kappa_attention']}; "
            f"max_channel={r['max_channel']}; "
            f"thermal/gap={r['thermal_to_gap_ratio']}; "
            f"density/gap={r['density_to_gap_ratio']}; "
            f"composition/gap={r['composition_to_gap_ratio']}; "
            f"support/gap={r['support_to_gap_ratio']}; "
            f"loss/gap={r['loss_to_gap_ratio']}; "
            f"bounded_anis={r['bounded_anisotropic_persistence']}"
        )
    lines.append("")
    lines.append("V2 VECTOR USE:")
    lines.append("Use A_5D_VECTOR_SUMMARY_v2.csv for A–B bridge work. It preserves the v1")
    lines.append("values while adding bounded anisotropic persistence and review flags.")
    lines.append("")
    lines.append("INTERPRETATION RULE:")
    lines.append("A scale-review flag is not a failure. It means the object should not be")
    lines.append("compared using raw anisotropic_persistence or a dominated response channel")
    lines.append("alone.")
    lines.append("")
    lines.append("A–B BRIDGE REQUIREMENT:")
    lines.append("Compare this file:")
    lines.append("A_mesa_precollapse_tracks/alpha_application/normalization_review/A_5D_VECTOR_SUMMARY_v2.csv")
    lines.append("")
    lines.append("against:")
    lines.append("B_supernova_light_curves/alpha_application/normalization_review/B_5D_VECTOR_SUMMARY_v2.csv")
    lines.append("")
    lines.append("NEXT STEP:")
    lines.append("Proceed to A–B bridge construction only after verifying that both A and B")
    lines.append("normalization-reviewed v2 summaries are present.")
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
    for grid_file in sorted(grids_dir.glob("A*_alpha_grid.csv")):
        review_rows.append(review_grid(grid_file, v1_lookup))

    review_lookup = {row["object_id"]: row for row in review_rows}

    v2_rows = []
    for v1_row in v1_rows:
        oid = v1_row.get("object_id", "")
        if oid in review_lookup:
            v2_rows.append(make_v2_vector(v1_row, review_lookup[oid]))

    review_csv = out_dir / "A_ALPHA_NORMALIZATION_REVIEW.csv"
    v2_csv = out_dir / "A_5D_VECTOR_SUMMARY_v2.csv"
    interpretation_txt = out_dir / "A_NORMALIZATION_REVIEW_INTERPRETATION.txt"

    write_csv(review_csv, review_rows, REVIEW_COLUMNS)
    write_csv(v2_csv, v2_rows, V2_COLUMNS)
    write_interpretation(interpretation_txt, review_rows, v2_rows)

    print(f"Review written: {review_csv}")
    print(f"V2 vectors written: {v2_csv}")
    print(f"Interpretation written: {interpretation_txt}")
    print(f"Objects reviewed: {len(review_rows)}")
    print(f"Scale-review-needed: {sum(1 for r in review_rows if r['scale_review_needed'] == 'yes')}")
    print(f"High-kappa-attention: {sum(1 for r in review_rows if r['high_kappa_attention'] == 'yes')}")


if __name__ == "__main__":
    main()
