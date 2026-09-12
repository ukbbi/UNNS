#!/usr/bin/env python3
"""
ab_bridge_compare.py

STELLAR_BOUNDARY_DYNAMICS_I
A–B Bridge comparator.

Compares normalization-reviewed v2 structural vectors:

  AB_bridge/inputs/A_5D_VECTOR_SUMMARY_v2.csv
  AB_bridge/inputs/B_5D_VECTOR_SUMMARY_v2.csv

and writes:

  AB_bridge/comparisons/AB_VECTOR_PAIRWISE_COMPARISON.csv
  AB_bridge/comparisons/AB_DOMAIN_CENTROID_COMPARISON.csv
  AB_bridge/comparisons/AB_OBJECT_RANKING.csv

  AB_bridge/summaries/AB_BRIDGE_SUMMARY.csv
  AB_bridge/summaries/AB_BRIDGE_INTERPRETATION.txt

Usage from stellar_boundary_dynamics/:

  python tools/ab_bridge_compare.py AB_bridge/inputs/A_5D_VECTOR_SUMMARY_v2.csv AB_bridge/inputs/B_5D_VECTOR_SUMMARY_v2.csv AB_bridge

Usage from inside AB_bridge/:

  python ../tools/ab_bridge_compare.py inputs/A_5D_VECTOR_SUMMARY_v2.csv inputs/B_5D_VECTOR_SUMMARY_v2.csv .
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
    "a_object_id",
    "a_object_name",
    "b_object_id",
    "b_object_name",
    "euclidean_distance",
    "manhattan_distance",
    "cosine_similarity",
    "mean_GR_delta",
    "var_GR_delta",
    "anisotropic_bounded_delta",
    "admissibility_persistence_delta",
    "collapse_onset_radius_delta",
    "kappa_connect_delta",
    "tail_dominance_delta",
    "closest_rank_for_b",
    "interpretation",
]

CENTROID_COLUMNS = [
    "domain_a_count",
    "domain_b_count",
    "feature",
    "a_centroid",
    "b_centroid",
    "delta_b_minus_a",
    "abs_delta",
]

RANKING_COLUMNS = [
    "b_object_id",
    "b_object_name",
    "nearest_a_object_id",
    "nearest_a_object_name",
    "nearest_distance",
    "mean_distance_to_a",
    "rank",
    "bridge_note",
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


def get_object_id(row):
    return row.get("object_id") or row.get("id") or row.get("name") or row.get("object_name", "")


def get_object_name(row):
    return row.get("object_name") or row.get("object_id") or row.get("name") or ""


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


def pair_interpretation(distance, cos):
    if distance < 0.35:
        return "close structural contact in reviewed v2 feature space"
    if distance < 0.75:
        return "weakly separated structural relation"
    if distance < 1.25:
        return "moderately separated structural relation"
    return "strongly separated structural relation"


def compare(a_path, b_path, out_root):
    a_rows = read_csv(a_path)
    b_rows = read_csv(b_path)

    if not a_rows:
        raise ValueError(f"No rows in {a_path}")
    if not b_rows:
        raise ValueError(f"No rows in {b_path}")

    out_root = Path(out_root)
    comparisons_dir = out_root / "comparisons"
    summaries_dir = out_root / "summaries"
    comparisons_dir.mkdir(parents=True, exist_ok=True)
    summaries_dir.mkdir(parents=True, exist_ok=True)

    all_rows = a_rows + b_rows
    normalized, raw = min_max_normalize(all_rows)

    pair_rows = []
    b_to_distances = {get_object_id(b): [] for b in b_rows}

    for a in a_rows:
        a_id = get_object_id(a)
        a_name = get_object_name(a)
        av = normalized[a_id]
        for b in b_rows:
            b_id = get_object_id(b)
            b_name = get_object_name(b)
            bv = normalized[b_id]

            ed = euclidean(av, bv)
            md = manhattan(av, bv)
            cs = cosine(av, bv)
            b_to_distances[b_id].append((ed, a_id, a_name))

            pair_rows.append({
                "a_object_id": a_id,
                "a_object_name": a_name,
                "b_object_id": b_id,
                "b_object_name": b_name,
                "euclidean_distance": fmt(ed),
                "manhattan_distance": fmt(md),
                "cosine_similarity": fmt(cs),
                "mean_GR_delta": fmt(to_float(b.get("mean_GR")) - to_float(a.get("mean_GR"))),
                "var_GR_delta": fmt(to_float(b.get("var_GR")) - to_float(a.get("var_GR"))),
                "anisotropic_bounded_delta": fmt(to_float(b.get("anisotropic_persistence_bounded")) - to_float(a.get("anisotropic_persistence_bounded"))),
                "admissibility_persistence_delta": fmt(to_float(b.get("admissibility_persistence")) - to_float(a.get("admissibility_persistence"))),
                "collapse_onset_radius_delta": fmt(to_float(b.get("collapse_onset_radius")) - to_float(a.get("collapse_onset_radius"))),
                "kappa_connect_delta": fmt(to_float(b.get("kappa_connect_reference")) - to_float(a.get("kappa_connect_reference"))),
                "tail_dominance_delta": fmt(to_float(b.get("tail_dominance_reference")) - to_float(a.get("tail_dominance_reference"))),
                "closest_rank_for_b": "",
                "interpretation": pair_interpretation(ed, cs),
            })

    # Rank A-pairs for each B object.
    rank_lookup = {}
    for b_id, dist_list in b_to_distances.items():
        for rank, (distance, a_id, a_name) in enumerate(sorted(dist_list), start=1):
            rank_lookup[(a_id, b_id)] = rank

    for row in pair_rows:
        row["closest_rank_for_b"] = rank_lookup.get((row["a_object_id"], row["b_object_id"]), "")

    ranking_rows = []
    for b in b_rows:
        b_id = get_object_id(b)
        b_name = get_object_name(b)
        dist_list = sorted(b_to_distances[b_id])
        nearest_distance, nearest_a_id, nearest_a_name = dist_list[0]
        mean_distance = statistics.fmean(d[0] for d in dist_list)

        note = "nearest Phase A pre-supernova profile in reviewed v2 feature space"
        if "SN2012aw" in b_name or "SN2012aw" in b_id:
            note += "; SN2012aw remains high-tail/high-kappa attention object"

        ranking_rows.append({
            "b_object_id": b_id,
            "b_object_name": b_name,
            "nearest_a_object_id": nearest_a_id,
            "nearest_a_object_name": nearest_a_name,
            "nearest_distance": fmt(nearest_distance),
            "mean_distance_to_a": fmt(mean_distance),
            "rank": "",
            "bridge_note": note,
        })

    ranking_rows.sort(key=lambda r: to_float(r["nearest_distance"]))
    for i, row in enumerate(ranking_rows, start=1):
        row["rank"] = i

    a_centroid = centroid(a_rows, normalized)
    b_centroid = centroid(b_rows, normalized)
    centroid_distance = euclidean(a_centroid, b_centroid)
    centroid_label = separation_label(centroid_distance)

    centroid_rows = []
    for f, av, bv in zip(FEATURES, a_centroid, b_centroid):
        centroid_rows.append({
            "domain_a_count": len(a_rows),
            "domain_b_count": len(b_rows),
            "feature": f,
            "a_centroid": fmt(av),
            "b_centroid": fmt(bv),
            "delta_b_minus_a": fmt(bv - av),
            "abs_delta": fmt(abs(bv - av)),
        })

    all_distances = [to_float(r["euclidean_distance"]) for r in pair_rows]
    min_pair = min(pair_rows, key=lambda r: to_float(r["euclidean_distance"]))
    max_pair = max(pair_rows, key=lambda r: to_float(r["euclidean_distance"]))

    summary_rows = [
        {
            "metric": "domain_a_count",
            "value": len(a_rows),
            "interpretation": "number of Phase A pre-collapse profile vectors",
        },
        {
            "metric": "domain_b_count",
            "value": len(b_rows),
            "interpretation": "number of Phase B post-collapse light-curve vectors",
        },
        {
            "metric": "pairwise_min_distance",
            "value": fmt(min(all_distances)),
            "interpretation": f"closest A-B pair: {min_pair['a_object_id']} ↔ {min_pair['b_object_id']}",
        },
        {
            "metric": "pairwise_mean_distance",
            "value": fmt(statistics.fmean(all_distances)),
            "interpretation": "mean normalized Euclidean distance over all A-B pairs",
        },
        {
            "metric": "pairwise_max_distance",
            "value": fmt(max(all_distances)),
            "interpretation": f"most separated A-B pair: {max_pair['a_object_id']} ↔ {max_pair['b_object_id']}",
        },
        {
            "metric": "centroid_distance",
            "value": fmt(centroid_distance),
            "interpretation": centroid_label,
        },
        {
            "metric": "nearest_b_object_to_a_domain",
            "value": ranking_rows[0]["b_object_id"],
            "interpretation": f"nearest distance {ranking_rows[0]['nearest_distance']}",
        },
    ]

    write_csv(comparisons_dir / "AB_VECTOR_PAIRWISE_COMPARISON.csv", pair_rows, PAIRWISE_COLUMNS)
    write_csv(comparisons_dir / "AB_DOMAIN_CENTROID_COMPARISON.csv", centroid_rows, CENTROID_COLUMNS)
    write_csv(comparisons_dir / "AB_OBJECT_RANKING.csv", ranking_rows, RANKING_COLUMNS)
    write_csv(summaries_dir / "AB_BRIDGE_SUMMARY.csv", summary_rows, SUMMARY_COLUMNS)

    write_interpretation(
        summaries_dir / "AB_BRIDGE_INTERPRETATION.txt",
        summary_rows,
        ranking_rows,
        centroid_distance,
        centroid_label,
        min_pair,
        max_pair,
    )

    print(f"Pairwise comparison written: {comparisons_dir / 'AB_VECTOR_PAIRWISE_COMPARISON.csv'}")
    print(f"Centroid comparison written: {comparisons_dir / 'AB_DOMAIN_CENTROID_COMPARISON.csv'}")
    print(f"Object ranking written: {comparisons_dir / 'AB_OBJECT_RANKING.csv'}")
    print(f"Bridge summary written: {summaries_dir / 'AB_BRIDGE_SUMMARY.csv'}")
    print(f"Bridge interpretation written: {summaries_dir / 'AB_BRIDGE_INTERPRETATION.txt'}")
    print(f"Centroid distance: {centroid_distance:.6g} ({centroid_label})")
    print(f"Closest pair: {min_pair['a_object_id']} ↔ {min_pair['b_object_id']} distance={min_pair['euclidean_distance']}")


def write_interpretation(path, summary_rows, ranking_rows, centroid_distance, centroid_label, min_pair, max_pair):
    lines = []
    lines.append("# AB_BRIDGE_INTERPRETATION.txt")
    lines.append("# STELLAR_BOUNDARY_DYNAMICS_I")
    lines.append("# A–B Bridge Interpretation")
    lines.append("")
    lines.append("PURPOSE:")
    lines.append("Interpret the first bridge comparison between Phase A pre-collapse")
    lines.append("pre-supernova radial-profile vectors and Phase B post-collapse light-curve")
    lines.append("response vectors.")
    lines.append("")
    lines.append("DATA LAYERS:")
    lines.append("Phase A uses real processed pre-supernova profile structures.")
    lines.append("Phase B uses observed supernova light-curve response structures.")
    lines.append("Both domains are compared only after normalization-reviewed v2 vector construction.")
    lines.append("")
    lines.append("PRIMARY DOMAIN RESULT:")
    lines.append(f"Centroid distance = {centroid_distance:.12g}")
    lines.append(f"Centroid separation label = {centroid_label}")
    lines.append("")
    lines.append("CLOSEST A–B PAIR:")
    lines.append(f"{min_pair['a_object_id']} ↔ {min_pair['b_object_id']}")
    lines.append(f"distance = {min_pair['euclidean_distance']}")
    lines.append(f"interpretation = {min_pair['interpretation']}")
    lines.append("")
    lines.append("MOST SEPARATED A–B PAIR:")
    lines.append(f"{max_pair['a_object_id']} ↔ {max_pair['b_object_id']}")
    lines.append(f"distance = {max_pair['euclidean_distance']}")
    lines.append(f"interpretation = {max_pair['interpretation']}")
    lines.append("")
    lines.append("PHASE B OBJECT RANKING BY NEAREST PHASE A PROFILE:")
    for r in ranking_rows:
        lines.append(
            f"{r['rank']}. {r['b_object_id']} nearest to {r['nearest_a_object_id']} "
            f"at distance {r['nearest_distance']}"
        )
    lines.append("")
    lines.append("INTERPRETATION RULE:")
    lines.append("This bridge is structural and comparative. It does not claim that a specific")
    lines.append("pre-supernova profile predicts a specific observed light curve.")
    lines.append("")
    lines.append("VALID CLAIM:")
    lines.append("The current processed dataset permits a first structural comparison between")
    lines.append("pre-boundary radial profiles and post-boundary brightness-response ladders.")
    lines.append("")
    lines.append("INVALID CLAIM:")
    lines.append("Do not claim direct explosion modeling or object-by-object astrophysical")
    lines.append("prediction from this bridge alone.")
    lines.append("")
    lines.append("NEXT STEP:")
    lines.append("Inspect AB_VECTOR_PAIRWISE_COMPARISON.csv and AB_OBJECT_RANKING.csv, then")
    lines.append("decide whether to expand Phase A with more pre-supernova models or Phase B")
    lines.append("with spectra/remnant/neutrino layers.")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)

    compare(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
