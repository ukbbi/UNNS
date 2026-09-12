#!/usr/bin/env python3
"""
c_alpha_normalization_review.py

STELLAR_BOUNDARY_DYNAMICS_I
Phase C — Alpha normalization review.

Reads:
  alpha_application/grids/*.csv
  alpha_application/summaries/C_5D_VECTOR_SUMMARY.csv

Writes:
  alpha_application/normalization_review/C_ALPHA_NORMALIZATION_REVIEW.csv
  alpha_application/normalization_review/C_5D_VECTOR_SUMMARY_v2.csv
  alpha_application/normalization_review/C_NORMALIZATION_REVIEW_INTERPRETATION.txt

Purpose:
  detect response-channel domination
  bound raw anisotropic_persistence
  preserve high-tail / high-kappa spectral warnings
  create a safer v2 vector summary for B–C and A–B–C bridge work

Usage from C_spectral_time_series/:

  python tools/c_alpha_normalization_review.py alpha_application/grids alpha_application/summaries/C_5D_VECTOR_SUMMARY.csv alpha_application/normalization_review
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
    "mean_flux_response",
    "mean_depth_response",
    "mean_equivalent_width_response",
    "mean_velocity_response",
    "mean_width_response",
    "mean_quality_response",
    "mean_transition_response",
    "mean_tail_pressure",
    "max_tail_pressure",
    "max_channel",
    "flux_to_gap_ratio",
    "depth_to_gap_ratio",
    "equivalent_width_to_gap_ratio",
    "velocity_to_gap_ratio",
    "width_to_gap_ratio",
    "quality_to_gap_ratio",
    "transition_to_gap_ratio",
    "tail_pressure_to_gap_ratio",
    "max_channel_to_gap_ratio",
    "original_anisotropic_persistence",
    "bounded_anisotropic_persistence",
    "admissibility_persistence",
    "collapse_onset_radius",
    "collapse_observed",
    "kappa_connect_reference",
    "tail_dominance_reference",
    "flux_dominant",
    "depth_dominant",
    "equivalent_width_dominant",
    "velocity_dominant",
    "width_dominant",
    "quality_dominant",
    "transition_dominant",
    "tail_pressure_dominant",
    "scale_review_needed",
    "high_tail_attention",
    "high_kappa_attention",
    "review_status",
]

V2_COLUMNS = [
    "object_id",
    "object_name",
    "mean_GR",
    "var_GR",
    "anisotropic_persistence_v1",
    "anisotropic_persistence_bounded",
    "admissibility_persistence",
    "collapse_onset_radius",
    "collapse_observed",
    "kappa_connect_reference",
    "tail_dominance_reference",
    "flux_to_gap_ratio",
    "depth_to_gap_ratio",
    "equivalent_width_to_gap_ratio",
    "velocity_to_gap_ratio",
    "width_to_gap_ratio",
    "quality_to_gap_ratio",
    "transition_to_gap_ratio",
    "tail_pressure_to_gap_ratio",
    "scale_review_needed",
    "high_tail_attention",
    "high_kappa_attention",
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
        x = float(str(value).strip())
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


def ratio(channel_mean, gap_mean):
    return channel_mean / max(gap_mean, 1e-12)


def object_id_from_grid(path):
    stem = Path(path).stem
    if stem.endswith("_alpha_grid"):
        return stem.replace("_alpha_grid", "")
    return stem


def dominance_flag(channel_name, max_channel, channel_to_gap_ratio, threshold=10.0):
    return "yes" if channel_name == max_channel and channel_to_gap_ratio >= threshold else "no"


def review_grid(grid_file, v1_lookup):
    rows = read_csv(grid_file)
    object_id = object_id_from_grid(grid_file)
    v1 = v1_lookup.get(object_id, {})
    object_name = rows[0].get("object_name", object_id) if rows else object_id

    mg = mean([to_float(r.get("gap_response_norm")) for r in rows])
    mf = mean([to_float(r.get("flux_response_norm")) for r in rows])
    md = mean([to_float(r.get("depth_response_norm")) for r in rows])
    mew = mean([to_float(r.get("equivalent_width_response_norm")) for r in rows])
    mv = mean([to_float(r.get("velocity_response_norm")) for r in rows])
    mw = mean([to_float(r.get("width_response_norm")) for r in rows])
    mq = mean([to_float(r.get("quality_response_norm")) for r in rows])
    mt = mean([to_float(r.get("transition_response_norm")) for r in rows])
    mtail = mean([to_float(r.get("tail_pressure_proxy")) for r in rows])
    max_tail = max([to_float(r.get("tail_pressure_proxy")) for r in rows], default=0.0)

    channels = {
        "gap": mg,
        "flux": mf,
        "depth": md,
        "equivalent_width": mew,
        "velocity": mv,
        "width": mw,
        "quality": mq,
        "transition": mt,
        "tail_pressure": mtail,
    }
    max_channel = max(channels, key=channels.get)

    flux_to_gap = ratio(mf, mg)
    depth_to_gap = ratio(md, mg)
    ew_to_gap = ratio(mew, mg)
    vel_to_gap = ratio(mv, mg)
    width_to_gap = ratio(mw, mg)
    quality_to_gap = ratio(mq, mg)
    transition_to_gap = ratio(mt, mg)
    tail_to_gap = ratio(mtail, mg)
    max_to_gap = ratio(channels[max_channel], mg)

    anis_v1 = to_float(v1.get("anisotropic_persistence"))
    anis_bounded = bounded(anis_v1)

    adm = to_float(v1.get("admissibility_persistence"))
    collapse_radius = to_float(v1.get("collapse_onset_radius"))
    collapse_observed = v1.get("collapse_observed", "")

    kappa = to_float(v1.get("kappa_connect_reference"))
    tail_ref = to_float(v1.get("tail_dominance_reference"))

    high_tail = "yes" if tail_ref >= 0.75 or mtail >= 1.0 else "no"
    high_kappa = "yes" if kappa >= 1000.0 else "no"

    flux_dom = dominance_flag("flux", max_channel, flux_to_gap)
    depth_dom = dominance_flag("depth", max_channel, depth_to_gap)
    ew_dom = dominance_flag("equivalent_width", max_channel, ew_to_gap)
    vel_dom = dominance_flag("velocity", max_channel, vel_to_gap)
    width_dom = dominance_flag("width", max_channel, width_to_gap)
    quality_dom = dominance_flag("quality", max_channel, quality_to_gap)
    transition_dom = dominance_flag("transition", max_channel, transition_to_gap)
    tail_dom = dominance_flag("tail_pressure", max_channel, tail_to_gap)

    any_ratio_high = max(
        flux_to_gap,
        depth_to_gap,
        ew_to_gap,
        vel_to_gap,
        width_to_gap,
        quality_to_gap,
        transition_to_gap,
        tail_to_gap,
    ) >= 10.0

    scale_review_needed = "yes" if any_ratio_high or anis_v1 >= 100.0 or high_tail == "yes" or high_kappa == "yes" else "no"
    review_status = "review_required" if scale_review_needed == "yes" else "comparable"

    return {
        "object_id": object_id,
        "object_name": object_name,
        "grid_file": str(grid_file),
        "n_rows": len(rows),
        "mean_gap_response": fmt(mg),
        "mean_flux_response": fmt(mf),
        "mean_depth_response": fmt(md),
        "mean_equivalent_width_response": fmt(mew),
        "mean_velocity_response": fmt(mv),
        "mean_width_response": fmt(mw),
        "mean_quality_response": fmt(mq),
        "mean_transition_response": fmt(mt),
        "mean_tail_pressure": fmt(mtail),
        "max_tail_pressure": fmt(max_tail),
        "max_channel": max_channel,
        "flux_to_gap_ratio": fmt(flux_to_gap),
        "depth_to_gap_ratio": fmt(depth_to_gap),
        "equivalent_width_to_gap_ratio": fmt(ew_to_gap),
        "velocity_to_gap_ratio": fmt(vel_to_gap),
        "width_to_gap_ratio": fmt(width_to_gap),
        "quality_to_gap_ratio": fmt(quality_to_gap),
        "transition_to_gap_ratio": fmt(transition_to_gap),
        "tail_pressure_to_gap_ratio": fmt(tail_to_gap),
        "max_channel_to_gap_ratio": fmt(max_to_gap),
        "original_anisotropic_persistence": fmt(anis_v1),
        "bounded_anisotropic_persistence": fmt(anis_bounded),
        "admissibility_persistence": fmt(adm),
        "collapse_onset_radius": fmt(collapse_radius),
        "collapse_observed": collapse_observed,
        "kappa_connect_reference": fmt(kappa),
        "tail_dominance_reference": fmt(tail_ref),
        "flux_dominant": flux_dom,
        "depth_dominant": depth_dom,
        "equivalent_width_dominant": ew_dom,
        "velocity_dominant": vel_dom,
        "width_dominant": width_dom,
        "quality_dominant": quality_dom,
        "transition_dominant": transition_dom,
        "tail_pressure_dominant": tail_dom,
        "scale_review_needed": scale_review_needed,
        "high_tail_attention": high_tail,
        "high_kappa_attention": high_kappa,
        "review_status": review_status,
    }


def make_v2_vector(v1_row, review_row):
    notes = [
        "v2 normalization-review vector",
        "anisotropic_persistence bounded as x/(1+x)",
        "v1 outputs preserved separately",
        "Phase C is real WISeREP spectral line-window ladder data",
        "line-window proxies are structural spectral features, not abundances",
    ]

    if review_row["scale_review_needed"] == "yes":
        notes.append("scale review needed before bridge interpretation")
    if review_row["high_tail_attention"] == "yes":
        notes.append("high tail attention")
    if review_row["high_kappa_attention"] == "yes":
        notes.append("high kappa attention")
    if review_row["object_id"] == "C1_SN1993J":
        notes.append("contact-case pilot object")
    if review_row["object_id"] == "C2_SN2012aw":
        notes.append("outlier-case pilot object")

    return {
        "object_id": v1_row.get("object_id", review_row["object_id"]),
        "object_name": v1_row.get("object_name", review_row["object_name"]),
        "mean_GR": v1_row.get("mean_GR", ""),
        "var_GR": v1_row.get("var_GR", ""),
        "anisotropic_persistence_v1": v1_row.get("anisotropic_persistence", ""),
        "anisotropic_persistence_bounded": review_row["bounded_anisotropic_persistence"],
        "admissibility_persistence": v1_row.get("admissibility_persistence", ""),
        "collapse_onset_radius": v1_row.get("collapse_onset_radius", ""),
        "collapse_observed": v1_row.get("collapse_observed", ""),
        "kappa_connect_reference": v1_row.get("kappa_connect_reference", ""),
        "tail_dominance_reference": v1_row.get("tail_dominance_reference", ""),
        "flux_to_gap_ratio": review_row["flux_to_gap_ratio"],
        "depth_to_gap_ratio": review_row["depth_to_gap_ratio"],
        "equivalent_width_to_gap_ratio": review_row["equivalent_width_to_gap_ratio"],
        "velocity_to_gap_ratio": review_row["velocity_to_gap_ratio"],
        "width_to_gap_ratio": review_row["width_to_gap_ratio"],
        "quality_to_gap_ratio": review_row["quality_to_gap_ratio"],
        "transition_to_gap_ratio": review_row["transition_to_gap_ratio"],
        "tail_pressure_to_gap_ratio": review_row["tail_pressure_to_gap_ratio"],
        "scale_review_needed": review_row["scale_review_needed"],
        "high_tail_attention": review_row["high_tail_attention"],
        "high_kappa_attention": review_row["high_kappa_attention"],
        "notes": "; ".join(notes),
    }


def write_interpretation(path, review_rows, v2_rows):
    comparable = [r for r in review_rows if r["review_status"] == "comparable"]
    review_needed = [r for r in review_rows if r["review_status"] == "review_required"]
    high_tail = [r for r in review_rows if r["high_tail_attention"] == "yes"]
    high_kappa = [r for r in review_rows if r["high_kappa_attention"] == "yes"]

    lines = []
    lines.append("# C_NORMALIZATION_REVIEW_INTERPRETATION.txt")
    lines.append("# STELLAR_BOUNDARY_DYNAMICS_I")
    lines.append("# Phase C — Alpha Normalization Review Interpretation")
    lines.append("")
    lines.append("PURPOSE:")
    lines.append("Interpret the normalization review performed on Phase C spectral alpha grids")
    lines.append("and first-pass 5D vectors.")
    lines.append("")
    lines.append("DATA STATUS:")
    lines.append("Phase C is based on real WISeREP public spectra converted to spectral")
    lines.append("line-window ladders. These line-window proxies are structural spectral")
    lines.append("features, not direct abundances.")
    lines.append("")
    lines.append("REVIEW STATUS COUNTS:")
    lines.append(f"Comparable objects: {len(comparable)}")
    lines.append(f"Scale-review-needed objects: {len(review_needed)}")
    lines.append(f"High-tail-attention objects: {len(high_tail)}")
    lines.append(f"High-kappa-attention objects: {len(high_kappa)}")
    lines.append("")
    lines.append("PRIMARY FINDING:")
    if review_needed:
        lines.append("At least one Phase C object shows scale domination, high tail pressure, or")
        lines.append("high kappa. Use the v2 vector summary for B–C and A–B–C comparisons.")
    else:
        lines.append("No major scale domination was detected. Phase C v2 vectors are ready for")
        lines.append("bridge comparisons.")
    lines.append("")
    lines.append("OBJECT FLAGS:")
    for r in review_rows:
        lines.append(
            f"{r['object_id']}: "
            f"status={r['review_status']}; "
            f"scale_review_needed={r['scale_review_needed']}; "
            f"high_tail_attention={r['high_tail_attention']}; "
            f"high_kappa_attention={r['high_kappa_attention']}; "
            f"max_channel={r['max_channel']}; "
            f"flux/gap={r['flux_to_gap_ratio']}; "
            f"depth/gap={r['depth_to_gap_ratio']}; "
            f"EW/gap={r['equivalent_width_to_gap_ratio']}; "
            f"velocity/gap={r['velocity_to_gap_ratio']}; "
            f"width/gap={r['width_to_gap_ratio']}; "
            f"quality/gap={r['quality_to_gap_ratio']}; "
            f"transition/gap={r['transition_to_gap_ratio']}; "
            f"tail/gap={r['tail_pressure_to_gap_ratio']}; "
            f"bounded_anis={r['bounded_anisotropic_persistence']}"
        )
    lines.append("")
    lines.append("V2 VECTOR USE:")
    lines.append("Use C_5D_VECTOR_SUMMARY_v2.csv for B–C, A–C, and A–B–C bridge work.")
    lines.append("The v2 summary preserves raw v1 values while adding bounded anisotropy and")
    lines.append("tail/kappa review flags.")
    lines.append("")
    lines.append("INTERPRETATION RULE:")
    lines.append("A scale-review flag is not a failure. It means the object should not be")
    lines.append("compared using raw anisotropic_persistence or an unbounded dominated response")
    lines.append("channel alone.")
    lines.append("")
    lines.append("EXPECTED SPECIAL CASE:")
    lines.append("C2_SN2012aw is expected to remain a high-tail/high-kappa attention object if")
    lines.append("the spectral layer supports the A–B outlier pattern.")
    lines.append("")
    lines.append("NEXT STEP:")
    lines.append("Proceed to B–C bridge construction only after verifying:")
    lines.append("C_spectral_time_series/alpha_application/normalization_review/C_5D_VECTOR_SUMMARY_v2.csv")
    lines.append("")
    lines.append("Do not use raw C_5D_VECTOR_SUMMARY.csv for bridge claims.")
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
    for grid_file in sorted(grids_dir.glob("C*_alpha_grid.csv")):
        review_rows.append(review_grid(grid_file, v1_lookup))

    review_lookup = {row["object_id"]: row for row in review_rows}

    v2_rows = []
    for v1_row in v1_rows:
        oid = v1_row.get("object_id", "")
        if oid in review_lookup:
            v2_rows.append(make_v2_vector(v1_row, review_lookup[oid]))

    review_csv = out_dir / "C_ALPHA_NORMALIZATION_REVIEW.csv"
    v2_csv = out_dir / "C_5D_VECTOR_SUMMARY_v2.csv"
    interpretation_txt = out_dir / "C_NORMALIZATION_REVIEW_INTERPRETATION.txt"

    write_csv(review_csv, review_rows, REVIEW_COLUMNS)
    write_csv(v2_csv, v2_rows, V2_COLUMNS)
    write_interpretation(interpretation_txt, review_rows, v2_rows)

    print(f"Review written: {review_csv}")
    print(f"V2 vectors written: {v2_csv}")
    print(f"Interpretation written: {interpretation_txt}")
    print(f"Objects reviewed: {len(review_rows)}")
    print(f"Scale-review-needed: {sum(1 for r in review_rows if r['scale_review_needed'] == 'yes')}")
    print(f"High-tail-attention: {sum(1 for r in review_rows if r['high_tail_attention'] == 'yes')}")
    print(f"High-kappa-attention: {sum(1 for r in review_rows if r['high_kappa_attention'] == 'yes')}")


if __name__ == "__main__":
    main()
