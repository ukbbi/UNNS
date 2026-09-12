#!/usr/bin/env python3
"""
bc_bridge_compare.py

STELLAR_BOUNDARY_DYNAMICS_I
B–C Bridge comparator.

Compares normalization-reviewed v2 structural vectors:

  BC_bridge/inputs/B_5D_VECTOR_SUMMARY_v2.csv
  BC_bridge/inputs/C_5D_VECTOR_SUMMARY_v2.csv

and writes:

  BC_bridge/comparisons/BC_VECTOR_PAIRWISE_COMPARISON.csv
  BC_bridge/comparisons/BC_DOMAIN_CENTROID_COMPARISON.csv
  BC_bridge/comparisons/BC_OBJECT_ALIGNMENT.csv

  BC_bridge/summaries/BC_BRIDGE_SUMMARY.csv
  BC_bridge/summaries/BC_BRIDGE_INTERPRETATION.txt

Usage from stellar_boundary_dynamics/:

  python tools/bc_bridge_compare.py BC_bridge/inputs/B_5D_VECTOR_SUMMARY_v2.csv BC_bridge/inputs/C_5D_VECTOR_SUMMARY_v2.csv BC_bridge

Usage from inside BC_bridge/:

  python ../tools/bc_bridge_compare.py inputs/B_5D_VECTOR_SUMMARY_v2.csv inputs/C_5D_VECTOR_SUMMARY_v2.csv .
"""

import csv
import math
import statistics
import sys
from pathlib import Path


FEATURES = [
    "mean_GR",
    "var_GR",
    "anisotropic_persistence_bounded",
    "admissibility_persistence",
    "collapse_onset_radius",
    "kappa_connect_reference",
    "tail_dominance_reference",
]

PAIRWISE_COLUMNS = [
    "b_object_id",
    "b_object_name",
    "c_object_id",
    "c_object_name",
    "matched_object_family",
    "is_object_matched_pair",
    "euclidean_distance",
    "manhattan_distance",
    "cosine_similarity",
    "mean_GR_delta_c_minus_b",
    "var_GR_delta_c_minus_b",
    "anisotropic_bounded_delta_c_minus_b",
    "admissibility_persistence_delta_c_minus_b",
    "collapse_onset_radius_delta_c_minus_b",
    "kappa_connect_delta_c_minus_b",
    "tail_dominance_delta_c_minus_b",
    "nearest_c_rank_for_b",
    "interpretation",
]

CENTROID_COLUMNS = [
    "domain_b_count",
    "domain_c_count",
    "feature",
    "b_centroid",
    "c_centroid",
    "delta_c_minus_b",
    "abs_delta",
]

ALIGNMENT_COLUMNS = [
    "object_family",
    "b_object_id",
    "b_object_name",
    "c_object_id",
    "c_object_name",
    "matched_pair_distance",
    "matched_pair_cosine_similarity",
    "nearest_c_for_b",
    "nearest_c_distance",
    "is_matched_pair_nearest",
    "b_high_tail_attention",
    "c_high_tail_attention",
    "b_high_kappa_attention",
    "c_high_kappa_attention",
    "alignment_note",
]

SUMMARY_COLUMNS = [
    "metric",
    "value",
    "interpretation",
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


def get_object_id(row):
    return row.get("object_id") or row.get("id") or row.get("name") or row.get("object_name", "")


def get_object_name(row):
    return row.get("object_name") or row.get("object_id") or row.get("name") or ""


def canonical_family(row):
    """
    Map B_SN1993J and C1_SN1993J to SN1993J, etc.
    """
    text = (get_object_id(row) + " " + get_object_name(row)).upper()
    for fam in ["SN1987A", "SN1993J", "SN1999EM", "SN2011DH", "SN2012AW", "SN2013EJ"]:
        if fam in text:
            # Preserve usual case.
            return {
                "SN1987A": "SN1987A",
                "SN1993J": "SN1993J",
                "SN1999EM": "SN1999em",
                "SN2011DH": "SN2011dh",
                "SN2012AW": "SN2012aw",
                "SN2013EJ": "SN2013ej",
            }[fam]
    return ""


def feature_vector(row):
    return [to_float(row.get(f), 0.0) for f in FEATURES]


def min_max_normalize(all_rows):
    raw = {get_object_id(r): feature_vector(r) for r in all_rows}
    cols = list(zip(*raw.values()))
    mins = [min(c) for c in cols]
    maxs = [max(c) for c in cols]

    norm = {}
    for oid, vec in raw.items():
        nv = []
        for value, mn, mx in zip(vec, mins, maxs):
            if mx == mn:
                nv.append(0.0)
            else:
                nv.append((value - mn) / (mx - mn))
        norm[oid] = nv

    return norm, raw


def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def manhattan(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def cosine(a, b):
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def centroid(rows, normalized_lookup):
    if not rows:
        return [0.0] * len(FEATURES)
    vectors = [normalized_lookup[get_object_id(r)] for r in rows]
    return [statistics.fmean(col) for col in zip(*vectors)]


def separation_label(distance):
    if distance >= 1.25:
        return "strong_separation"
    if distance >= 0.75:
        return "moderate_separation"
    if distance >= 0.35:
        return "weak_separation"
    return "overlap_or_close_contact"


def pair_interpretation(distance, cos, matched):
    if matched and distance < 0.35:
        return "object-matched close contact across light-curve and spectral layers"
    if matched and distance < 0.75:
        return "object-matched weak separation across B-C layers"
    if matched:
        return "object-matched separation across B-C layers"
    if distance < 0.35:
        return "cross-object close contact in reviewed v2 feature space"
    if distance < 0.75:
        return "cross-object weak separation"
    if distance < 1.25:
        return "cross-object moderate separation"
    return "cross-object strong separation"


def truthy(row, key):
    return str(row.get(key, "")).strip().lower() in {"yes", "true", "1"}


def compare(b_path, c_path, out_root):
    b_rows = read_csv(b_path)
    c_rows = read_csv(c_path)

    if not b_rows:
        raise ValueError(f"No rows in {b_path}")
    if not c_rows:
        raise ValueError(f"No rows in {c_path}")

    out_root = Path(out_root)
    comparisons_dir = out_root / "comparisons"
    summaries_dir = out_root / "summaries"
    comparisons_dir.mkdir(parents=True, exist_ok=True)
    summaries_dir.mkdir(parents=True, exist_ok=True)

    normalized, raw = min_max_normalize(b_rows + c_rows)

    pair_rows = []
    b_to_distances = {get_object_id(b): [] for b in b_rows}

    for b in b_rows:
        b_id = get_object_id(b)
        b_name = get_object_name(b)
        b_fam = canonical_family(b)
        bv = normalized[b_id]

        for c in c_rows:
            c_id = get_object_id(c)
            c_name = get_object_name(c)
            c_fam = canonical_family(c)
            cv = normalized[c_id]

            matched = bool(b_fam and c_fam and b_fam == c_fam)
            ed = euclidean(bv, cv)
            md = manhattan(bv, cv)
            cs = cosine(bv, cv)

            b_to_distances[b_id].append((ed, c_id, c_name))

            pair_rows.append({
                "b_object_id": b_id,
                "b_object_name": b_name,
                "c_object_id": c_id,
                "c_object_name": c_name,
                "matched_object_family": b_fam if matched else "",
                "is_object_matched_pair": "yes" if matched else "no",
                "euclidean_distance": fmt(ed),
                "manhattan_distance": fmt(md),
                "cosine_similarity": fmt(cs),
                "mean_GR_delta_c_minus_b": fmt(to_float(c.get("mean_GR")) - to_float(b.get("mean_GR"))),
                "var_GR_delta_c_minus_b": fmt(to_float(c.get("var_GR")) - to_float(b.get("var_GR"))),
                "anisotropic_bounded_delta_c_minus_b": fmt(to_float(c.get("anisotropic_persistence_bounded")) - to_float(b.get("anisotropic_persistence_bounded"))),
                "admissibility_persistence_delta_c_minus_b": fmt(to_float(c.get("admissibility_persistence")) - to_float(b.get("admissibility_persistence"))),
                "collapse_onset_radius_delta_c_minus_b": fmt(to_float(c.get("collapse_onset_radius")) - to_float(b.get("collapse_onset_radius"))),
                "kappa_connect_delta_c_minus_b": fmt(to_float(c.get("kappa_connect_reference")) - to_float(b.get("kappa_connect_reference"))),
                "tail_dominance_delta_c_minus_b": fmt(to_float(c.get("tail_dominance_reference")) - to_float(b.get("tail_dominance_reference"))),
                "nearest_c_rank_for_b": "",
                "interpretation": pair_interpretation(ed, cs, matched),
            })

    # Rank C-pairs for each B object.
    rank_lookup = {}
    nearest_lookup = {}
    for b_id, dist_list in b_to_distances.items():
        ordered = sorted(dist_list)
        nearest_lookup[b_id] = ordered[0]
        for rank, (distance, c_id, c_name) in enumerate(ordered, start=1):
            rank_lookup[(b_id, c_id)] = rank

    for row in pair_rows:
        row["nearest_c_rank_for_b"] = rank_lookup.get((row["b_object_id"], row["c_object_id"]), "")

    c_by_family = {canonical_family(c): c for c in c_rows if canonical_family(c)}
    b_by_family = {canonical_family(b): b for b in b_rows if canonical_family(b)}

    alignment_rows = []
    for fam in sorted(set(c_by_family) & set(b_by_family)):
        b = b_by_family[fam]
        c = c_by_family[fam]
        b_id = get_object_id(b)
        c_id = get_object_id(c)
        bv = normalized[b_id]
        cv = normalized[c_id]

        matched_distance = euclidean(bv, cv)
        matched_cos = cosine(bv, cv)
        nearest_distance, nearest_c_id, nearest_c_name = nearest_lookup[b_id]
        is_nearest = "yes" if nearest_c_id == c_id else "no"

        b_high_tail = "yes" if truthy(b, "high_tail_attention") or to_float(b.get("tail_dominance_reference")) >= 0.75 else "no"
        c_high_tail = "yes" if truthy(c, "high_tail_attention") or to_float(c.get("tail_dominance_reference")) >= 0.75 else "no"
        b_high_kappa = "yes" if truthy(b, "high_kappa_attention") or to_float(b.get("kappa_connect_reference")) >= 1000 else "no"
        c_high_kappa = "yes" if truthy(c, "high_kappa_attention") or to_float(c.get("kappa_connect_reference")) >= 1000 else "no"

        note = []
        if is_nearest == "yes":
            note.append("matched C object is nearest spectral counterpart")
        else:
            note.append("matched C object is not nearest spectral counterpart")
        if fam == "SN2012aw":
            note.append("SN2012aw special-case persistence test")
        if b_high_tail == "yes" and c_high_tail == "yes":
            note.append("high-tail persists across B and C")
        if b_high_kappa == "yes" and c_high_kappa == "yes":
            note.append("high-kappa persists across B and C")
        if fam == "SN1993J":
            note.append("contact-case pilot test")

        alignment_rows.append({
            "object_family": fam,
            "b_object_id": b_id,
            "b_object_name": get_object_name(b),
            "c_object_id": c_id,
            "c_object_name": get_object_name(c),
            "matched_pair_distance": fmt(matched_distance),
            "matched_pair_cosine_similarity": fmt(matched_cos),
            "nearest_c_for_b": nearest_c_id,
            "nearest_c_distance": fmt(nearest_distance),
            "is_matched_pair_nearest": is_nearest,
            "b_high_tail_attention": b_high_tail,
            "c_high_tail_attention": c_high_tail,
            "b_high_kappa_attention": b_high_kappa,
            "c_high_kappa_attention": c_high_kappa,
            "alignment_note": "; ".join(note),
        })

    b_centroid = centroid(b_rows, normalized)
    c_centroid = centroid(c_rows, normalized)
    centroid_distance = euclidean(b_centroid, c_centroid)
    centroid_label = separation_label(centroid_distance)

    centroid_rows = []
    for f, bv, cv in zip(FEATURES, b_centroid, c_centroid):
        centroid_rows.append({
            "domain_b_count": len(b_rows),
            "domain_c_count": len(c_rows),
            "feature": f,
            "b_centroid": fmt(bv),
            "c_centroid": fmt(cv),
            "delta_c_minus_b": fmt(cv - bv),
            "abs_delta": fmt(abs(cv - bv)),
        })

    all_distances = [to_float(r["euclidean_distance"]) for r in pair_rows]
    min_pair = min(pair_rows, key=lambda r: to_float(r["euclidean_distance"]))
    max_pair = max(pair_rows, key=lambda r: to_float(r["euclidean_distance"]))
    matched_pairs = [r for r in pair_rows if r["is_object_matched_pair"] == "yes"]

    matched_mean = statistics.fmean([to_float(r["euclidean_distance"]) for r in matched_pairs]) if matched_pairs else 0.0
    cross_mean = statistics.fmean(all_distances)

    sn2012_alignment = next((r for r in alignment_rows if r["object_family"] == "SN2012aw"), None)
    sn1993j_alignment = next((r for r in alignment_rows if r["object_family"] == "SN1993J"), None)

    summary_rows = [
        {
            "metric": "domain_b_count",
            "value": len(b_rows),
            "interpretation": "number of Phase B light-curve vectors",
        },
        {
            "metric": "domain_c_count",
            "value": len(c_rows),
            "interpretation": "number of Phase C spectral vectors",
        },
        {
            "metric": "pairwise_min_distance",
            "value": fmt(min(all_distances)),
            "interpretation": f"closest B-C pair: {min_pair['b_object_id']} ↔ {min_pair['c_object_id']}",
        },
        {
            "metric": "pairwise_mean_distance",
            "value": fmt(cross_mean),
            "interpretation": "mean normalized Euclidean distance over all B-C pairs",
        },
        {
            "metric": "pairwise_max_distance",
            "value": fmt(max(all_distances)),
            "interpretation": f"most separated B-C pair: {max_pair['b_object_id']} ↔ {max_pair['c_object_id']}",
        },
        {
            "metric": "object_matched_mean_distance",
            "value": fmt(matched_mean),
            "interpretation": "mean distance for object-matched B-C pairs only",
        },
        {
            "metric": "centroid_distance",
            "value": fmt(centroid_distance),
            "interpretation": centroid_label,
        },
    ]

    if sn1993j_alignment:
        summary_rows.append({
            "metric": "SN1993J_matched_distance",
            "value": sn1993j_alignment["matched_pair_distance"],
            "interpretation": sn1993j_alignment["alignment_note"],
        })

    if sn2012_alignment:
        summary_rows.append({
            "metric": "SN2012aw_matched_distance",
            "value": sn2012_alignment["matched_pair_distance"],
            "interpretation": sn2012_alignment["alignment_note"],
        })

    write_csv(comparisons_dir / "BC_VECTOR_PAIRWISE_COMPARISON.csv", pair_rows, PAIRWISE_COLUMNS)
    write_csv(comparisons_dir / "BC_DOMAIN_CENTROID_COMPARISON.csv", centroid_rows, CENTROID_COLUMNS)
    write_csv(comparisons_dir / "BC_OBJECT_ALIGNMENT.csv", alignment_rows, ALIGNMENT_COLUMNS)
    write_csv(summaries_dir / "BC_BRIDGE_SUMMARY.csv", summary_rows, SUMMARY_COLUMNS)

    write_interpretation(
        summaries_dir / "BC_BRIDGE_INTERPRETATION.txt",
        summary_rows,
        alignment_rows,
        centroid_distance,
        centroid_label,
        min_pair,
        max_pair,
        matched_mean,
        cross_mean,
    )

    print(f"Pairwise comparison written: {comparisons_dir / 'BC_VECTOR_PAIRWISE_COMPARISON.csv'}")
    print(f"Centroid comparison written: {comparisons_dir / 'BC_DOMAIN_CENTROID_COMPARISON.csv'}")
    print(f"Object alignment written: {comparisons_dir / 'BC_OBJECT_ALIGNMENT.csv'}")
    print(f"Bridge summary written: {summaries_dir / 'BC_BRIDGE_SUMMARY.csv'}")
    print(f"Bridge interpretation written: {summaries_dir / 'BC_BRIDGE_INTERPRETATION.txt'}")
    print(f"Centroid distance: {centroid_distance:.6g} ({centroid_label})")
    print(f"Closest pair: {min_pair['b_object_id']} ↔ {min_pair['c_object_id']} distance={min_pair['euclidean_distance']}")


def write_interpretation(path, summary_rows, alignment_rows, centroid_distance, centroid_label, min_pair, max_pair, matched_mean, cross_mean):
    lines = []
    lines.append("# BC_BRIDGE_INTERPRETATION.txt")
    lines.append("# STELLAR_BOUNDARY_DYNAMICS_I")
    lines.append("# B–C Bridge Interpretation")
    lines.append("")
    lines.append("PURPOSE:")
    lines.append("Interpret the first bridge comparison between Phase B post-collapse")
    lines.append("light-curve response vectors and Phase C post-collapse spectral line-evolution")
    lines.append("vectors.")
    lines.append("")
    lines.append("DATA LAYERS:")
    lines.append("Phase B uses observed light-curve response ladders.")
    lines.append("Phase C uses WISeREP spectral line-window ladders.")
    lines.append("Both domains are compared only after normalization-reviewed v2 vector construction.")
    lines.append("")
    lines.append("PRIMARY DOMAIN RESULT:")
    lines.append(f"Centroid distance = {centroid_distance:.12g}")
    lines.append(f"Centroid separation label = {centroid_label}")
    lines.append("")
    lines.append("CLOSEST B–C PAIR:")
    lines.append(f"{min_pair['b_object_id']} ↔ {min_pair['c_object_id']}")
    lines.append(f"distance = {min_pair['euclidean_distance']}")
    lines.append(f"interpretation = {min_pair['interpretation']}")
    lines.append("")
    lines.append("MOST SEPARATED B–C PAIR:")
    lines.append(f"{max_pair['b_object_id']} ↔ {max_pair['c_object_id']}")
    lines.append(f"distance = {max_pair['euclidean_distance']}")
    lines.append(f"interpretation = {max_pair['interpretation']}")
    lines.append("")
    lines.append("OBJECT-MATCHED ALIGNMENT:")
    lines.append(f"Mean object-matched distance = {matched_mean:.12g}")
    lines.append(f"Mean all-pair B-C distance = {cross_mean:.12g}")
    for r in alignment_rows:
        lines.append(
            f"{r['object_family']}: {r['b_object_id']} ↔ {r['c_object_id']} "
            f"distance={r['matched_pair_distance']}; "
            f"matched_is_nearest={r['is_matched_pair_nearest']}; "
            f"{r['alignment_note']}"
        )
    lines.append("")
    lines.append("INTERPRETATION RULE:")
    lines.append("This bridge compares two post-collapse observable channels. It does not")
    lines.append("claim that spectral line-window proxies are direct abundances or that vector")
    lines.append("proximity alone proves physical causation.")
    lines.append("")
    lines.append("VALID CLAIM:")
    lines.append("The B–C bridge tests whether brightness-response and spectral-line evolution")
    lines.append("preserve the same contact/outlier pattern.")
    lines.append("")
    lines.append("INVALID CLAIM:")
    lines.append("Do not claim radiative-transfer modeling, direct nucleosynthesis yields, or")
    lines.append("object-by-object progenitor reconstruction from this bridge alone.")
    lines.append("")
    lines.append("NEXT STEP:")
    lines.append("Create BC_BRIDGE_RESULT_RECORD.txt, then proceed to A–B–C tri-domain bridge.")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)

    compare(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
