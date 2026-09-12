#!/usr/bin/env python3
"""
abc_bridge_compare.py

STELLAR_BOUNDARY_DYNAMICS_I
A-B-C tri-domain bridge comparator.

Compares normalization-reviewed v2 structural vectors:

  ABC_bridge/inputs/A_5D_VECTOR_SUMMARY_v2.csv
  ABC_bridge/inputs/B_5D_VECTOR_SUMMARY_v2.csv
  ABC_bridge/inputs/C_5D_VECTOR_SUMMARY_v2.csv

and writes:

  ABC_bridge/comparisons/ABC_DOMAIN_CENTROID_COMPARISON.csv
  ABC_bridge/comparisons/ABC_PAIRWISE_DOMAIN_DISTANCE.csv
  ABC_bridge/comparisons/ABC_OBJECT_CHAIN_ALIGNMENT.csv
  ABC_bridge/comparisons/ABC_TRANSITION_CHAIN_TEST.csv

  ABC_bridge/summaries/ABC_BRIDGE_SUMMARY.csv
  ABC_bridge/summaries/ABC_BRIDGE_INTERPRETATION.txt

Usage from stellar_boundary_dynamics/:

  python tools/abc_bridge_compare.py ABC_bridge/inputs/A_5D_VECTOR_SUMMARY_v2.csv ABC_bridge/inputs/B_5D_VECTOR_SUMMARY_v2.csv ABC_bridge/inputs/C_5D_VECTOR_SUMMARY_v2.csv ABC_bridge

Usage from inside ABC_bridge/:

  python ../tools/abc_bridge_compare.py inputs/A_5D_VECTOR_SUMMARY_v2.csv inputs/B_5D_VECTOR_SUMMARY_v2.csv inputs/C_5D_VECTOR_SUMMARY_v2.csv .
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

DOMAIN_CENTROID_COLUMNS = [
    "domain",
    "object_count",
    "feature",
    "centroid_value_normalized",
    "raw_mean",
    "raw_min",
    "raw_max",
]

PAIRWISE_DOMAIN_COLUMNS = [
    "domain_pair",
    "domain_left",
    "domain_right",
    "left_count",
    "right_count",
    "centroid_distance",
    "separation_label",
    "mean_pairwise_distance",
    "min_pairwise_distance",
    "min_pair",
    "max_pairwise_distance",
    "max_pair",
    "interpretation",
]

CHAIN_ALIGNMENT_COLUMNS = [
    "chain_id",
    "chain_role",
    "a_object_id",
    "a_object_name",
    "b_object_id",
    "b_object_name",
    "c_object_id",
    "c_object_name",
    "distance_ab",
    "distance_bc",
    "distance_ac",
    "ab_separation",
    "bc_separation",
    "ac_separation",
    "chain_score",
    "branching_index",
    "a_to_b_nearest",
    "b_to_c_nearest",
    "interpretation",
]

CHAIN_TEST_COLUMNS = [
    "test",
    "value",
    "classification",
    "interpretation",
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


def object_id(row):
    return row.get("object_id") or row.get("id") or row.get("name") or row.get("object_name", "")


def object_name(row):
    return row.get("object_name") or object_id(row)


def vec(row):
    return [to_float(row.get(f), 0.0) for f in FEATURES]


def norm_all(domain_rows):
    all_rows = []
    for domain, rows in domain_rows.items():
        for row in rows:
            rr = dict(row)
            rr["_domain"] = domain
            all_rows.append(rr)

    raw = {object_id(r): vec(r) for r in all_rows}
    cols = list(zip(*raw.values()))
    mins = [min(c) for c in cols]
    maxs = [max(c) for c in cols]

    norm = {}
    for oid, values in raw.items():
        out = []
        for x, mn, mx in zip(values, mins, maxs):
            if mx == mn:
                out.append(0.0)
            else:
                out.append((x - mn) / (mx - mn))
        norm[oid] = out
    return norm, raw, mins, maxs


def euclidean(a, b):
    return math.sqrt(sum((x-y)**2 for x, y in zip(a, b)))


def manhattan(a, b):
    return sum(abs(x-y) for x, y in zip(a, b))


def cosine(a, b):
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x*y for x, y in zip(a, b)) / (na * nb)


def centroid(rows, norm_lookup):
    if not rows:
        return [0.0] * len(FEATURES)
    vectors = [norm_lookup[object_id(r)] for r in rows]
    return [statistics.fmean(col) for col in zip(*vectors)]


def raw_feature_stats(rows, feature):
    vals = [to_float(r.get(feature)) for r in rows]
    if not vals:
        return 0.0, 0.0, 0.0
    return statistics.fmean(vals), min(vals), max(vals)


def separation_label(d):
    if d >= 1.25:
        return "strong_separation"
    if d >= 0.75:
        return "moderate_separation"
    if d >= 0.35:
        return "weak_separation"
    return "overlap_or_close_contact"


def pair_interp(pair_name, centroid_distance):
    label = separation_label(centroid_distance)
    if pair_name == "A-B":
        if label in {"overlap_or_close_contact", "weak_separation"}:
            return "pre-boundary profiles and light curves are related but shifted"
        return "pre-boundary profiles and light curves are strongly separated"
    if pair_name == "B-C":
        if label == "strong_separation":
            return "light curves and spectra form distinct post-boundary observable regimes"
        return "light curves and spectra show partial post-boundary overlap"
    if pair_name == "A-C":
        if label == "strong_separation":
            return "pre-boundary profiles and spectra are separated across the full boundary route"
        return "pre-boundary profiles and spectra retain some direct structural contact"
    return label


def domain_pair_summary(name, left_name, right_name, left_rows, right_rows, norm_lookup, centroids):
    lv = centroids[left_name]
    rv = centroids[right_name]
    centroid_dist = euclidean(lv, rv)

    pair_dists = []
    for l in left_rows:
        for r in right_rows:
            d = euclidean(norm_lookup[object_id(l)], norm_lookup[object_id(r)])
            pair_dists.append((d, object_id(l), object_id(r)))

    pair_dists = sorted(pair_dists)
    min_d, min_l, min_r = pair_dists[0]
    max_d, max_l, max_r = pair_dists[-1]
    mean_d = statistics.fmean(d for d, _, _ in pair_dists)

    return {
        "domain_pair": name,
        "domain_left": left_name,
        "domain_right": right_name,
        "left_count": len(left_rows),
        "right_count": len(right_rows),
        "centroid_distance": fmt(centroid_dist),
        "separation_label": separation_label(centroid_dist),
        "mean_pairwise_distance": fmt(mean_d),
        "min_pairwise_distance": fmt(min_d),
        "min_pair": f"{min_l} <-> {min_r}",
        "max_pairwise_distance": fmt(max_d),
        "max_pair": f"{max_l} <-> {max_r}",
        "interpretation": pair_interp(name, centroid_dist),
    }


def nearest(target, candidates, norm_lookup):
    tv = norm_lookup[object_id(target)]
    ordered = sorted((euclidean(tv, norm_lookup[object_id(c)]), c) for c in candidates)
    return ordered[0]


def get_by_id_contains(rows, token):
    token = token.upper()
    for r in rows:
        if token in object_id(r).upper() or token in object_name(r).upper():
            return r
    return None


def make_chain(chain_id, role, a, b, c, a_rows, b_rows, c_rows, norm_lookup):
    av = norm_lookup[object_id(a)]
    bv = norm_lookup[object_id(b)]
    cv = norm_lookup[object_id(c)]

    dab = euclidean(av, bv)
    dbc = euclidean(bv, cv)
    dac = euclidean(av, cv)

    # A -> B -> C chain score: smaller if A-C is approximately explained by A-B plus B-C,
    # while also penalizing large B-C branch separation.
    triangle_excess = abs((dab + dbc) - dac)
    chain_score = 1.0 / (1.0 + triangle_excess + 0.5 * dbc)

    # Branching index: how much C separates from the A-B bridge.
    # Positive large values mean C is farther from B than B is from A.
    branching_index = dbc - dab

    n_ab_d, n_ab = nearest(a, b_rows, norm_lookup)
    n_bc_d, n_bc = nearest(b, c_rows, norm_lookup)

    if dbc > dab and dbc >= 1.25:
        interpretation = "C branches away from the A-B contact path"
    elif dab < 0.35 and dbc < 0.75:
        interpretation = "compact transition chain with C still near B"
    elif dab < dbc:
        interpretation = "transition chain with increasing post-boundary separation"
    else:
        interpretation = "non-monotone chain; B-C is not the dominant separation"

    return {
        "chain_id": chain_id,
        "chain_role": role,
        "a_object_id": object_id(a),
        "a_object_name": object_name(a),
        "b_object_id": object_id(b),
        "b_object_name": object_name(b),
        "c_object_id": object_id(c),
        "c_object_name": object_name(c),
        "distance_ab": fmt(dab),
        "distance_bc": fmt(dbc),
        "distance_ac": fmt(dac),
        "ab_separation": separation_label(dab),
        "bc_separation": separation_label(dbc),
        "ac_separation": separation_label(dac),
        "chain_score": fmt(chain_score),
        "branching_index": fmt(branching_index),
        "a_to_b_nearest": object_id(n_ab),
        "b_to_c_nearest": object_id(n_bc),
        "interpretation": interpretation,
    }


def classify_global(ab, bc, ac):
    if ab < bc and bc >= 1.25 and ac >= 1.25:
        return "A_to_B_contact_with_C_branching"
    if ab < bc < ac:
        return "monotone_A_to_B_to_C_chain"
    if ab < 0.75 and bc < 0.75:
        return "compact_three_layer_chain"
    if ab >= 1.25 and bc >= 1.25 and ac >= 1.25:
        return "three_strongly_separated_clusters"
    return "mixed_cluster_routing"


def compare(a_path, b_path, c_path, out_root):
    a_rows = read_csv(a_path)
    b_rows = read_csv(b_path)
    c_rows = read_csv(c_path)

    if not a_rows or not b_rows or not c_rows:
        raise ValueError("A, B, and C input files must all contain at least one row.")

    domains = {"A": a_rows, "B": b_rows, "C": c_rows}
    norm_lookup, raw_lookup, mins, maxs = norm_all(domains)

    out_root = Path(out_root)
    comparisons_dir = out_root / "comparisons"
    summaries_dir = out_root / "summaries"
    comparisons_dir.mkdir(parents=True, exist_ok=True)
    summaries_dir.mkdir(parents=True, exist_ok=True)

    centroids = {d: centroid(rows, norm_lookup) for d, rows in domains.items()}

    centroid_rows = []
    for d, rows in domains.items():
        for idx, f in enumerate(FEATURES):
            raw_mean, raw_min, raw_max = raw_feature_stats(rows, f)
            centroid_rows.append({
                "domain": d,
                "object_count": len(rows),
                "feature": f,
                "centroid_value_normalized": fmt(centroids[d][idx]),
                "raw_mean": fmt(raw_mean),
                "raw_min": fmt(raw_min),
                "raw_max": fmt(raw_max),
            })

    pair_rows = [
        domain_pair_summary("A-B", "A", "B", a_rows, b_rows, norm_lookup, centroids),
        domain_pair_summary("B-C", "B", "C", b_rows, c_rows, norm_lookup, centroids),
        domain_pair_summary("A-C", "A", "C", a_rows, c_rows, norm_lookup, centroids),
    ]

    dist = {r["domain_pair"]: to_float(r["centroid_distance"]) for r in pair_rows}
    global_class = classify_global(dist["A-B"], dist["B-C"], dist["A-C"])

    # Object chains.
    a2 = get_by_id_contains(a_rows, "A2") or a_rows[-1]
    a1 = get_by_id_contains(a_rows, "A1") or a_rows[0]
    b1993 = get_by_id_contains(b_rows, "SN1993J")
    c1993 = get_by_id_contains(c_rows, "SN1993J")
    b2012 = get_by_id_contains(b_rows, "SN2012AW")
    c2012 = get_by_id_contains(c_rows, "SN2012AW")

    chain_rows = []
    if b1993 and c1993:
        chain_rows.append(make_chain(
            "SN1993J_contact_chain",
            "contact_coherence_test",
            a2, b1993, c1993,
            a_rows, b_rows, c_rows, norm_lookup
        ))
    if b2012 and c2012:
        # choose nearest A to B2012aw
        _, nearest_a_for_2012 = nearest(b2012, a_rows, norm_lookup)
        chain_rows.append(make_chain(
            "SN2012aw_anomaly_chain",
            "persistent_anomaly_test",
            nearest_a_for_2012, b2012, c2012,
            a_rows, b_rows, c_rows, norm_lookup
        ))

    chain_test_rows = [
        {
            "test": "centroid_AB_distance",
            "value": fmt(dist["A-B"]),
            "classification": separation_label(dist["A-B"]),
            "interpretation": "pre-boundary to light-curve bridge",
        },
        {
            "test": "centroid_BC_distance",
            "value": fmt(dist["B-C"]),
            "classification": separation_label(dist["B-C"]),
            "interpretation": "light-curve to spectral bridge",
        },
        {
            "test": "centroid_AC_distance",
            "value": fmt(dist["A-C"]),
            "classification": separation_label(dist["A-C"]),
            "interpretation": "direct pre-boundary to spectral bridge",
        },
        {
            "test": "BC_minus_AB",
            "value": fmt(dist["B-C"] - dist["A-B"]),
            "classification": "C_branching" if dist["B-C"] > dist["A-B"] else "no_C_branching",
            "interpretation": "positive value means spectra separate more strongly from light curves than light curves from profiles",
        },
        {
            "test": "AC_minus_AB",
            "value": fmt(dist["A-C"] - dist["A-B"]),
            "classification": "spectral_farther_than_lightcurve" if dist["A-C"] > dist["A-B"] else "spectral_not_farther",
            "interpretation": "positive value means spectra are farther from pre-boundary profiles than light curves are",
        },
        {
            "test": "global_ABC_classification",
            "value": global_class,
            "classification": global_class,
            "interpretation": "tri-domain structural routing class",
        },
    ]

    summary_rows = [
        {"metric": "A_count", "value": len(a_rows), "interpretation": "Phase A v2 vectors"},
        {"metric": "B_count", "value": len(b_rows), "interpretation": "Phase B v2 vectors"},
        {"metric": "C_count", "value": len(c_rows), "interpretation": "Phase C v2 vectors"},
        {"metric": "AB_centroid_distance", "value": fmt(dist["A-B"]), "interpretation": separation_label(dist["A-B"])},
        {"metric": "BC_centroid_distance", "value": fmt(dist["B-C"]), "interpretation": separation_label(dist["B-C"])},
        {"metric": "AC_centroid_distance", "value": fmt(dist["A-C"]), "interpretation": separation_label(dist["A-C"])},
        {"metric": "BC_minus_AB", "value": fmt(dist["B-C"] - dist["A-B"]), "interpretation": "C branching strength relative to A-B"},
        {"metric": "global_ABC_classification", "value": global_class, "interpretation": "tri-domain routing class"},
    ]

    for chain in chain_rows:
        summary_rows.append({
            "metric": chain["chain_id"],
            "value": chain["chain_score"],
            "interpretation": chain["interpretation"],
        })

    write_csv(comparisons_dir / "ABC_DOMAIN_CENTROID_COMPARISON.csv", centroid_rows, DOMAIN_CENTROID_COLUMNS)
    write_csv(comparisons_dir / "ABC_PAIRWISE_DOMAIN_DISTANCE.csv", pair_rows, PAIRWISE_DOMAIN_COLUMNS)
    write_csv(comparisons_dir / "ABC_OBJECT_CHAIN_ALIGNMENT.csv", chain_rows, CHAIN_ALIGNMENT_COLUMNS)
    write_csv(comparisons_dir / "ABC_TRANSITION_CHAIN_TEST.csv", chain_test_rows, CHAIN_TEST_COLUMNS)
    write_csv(summaries_dir / "ABC_BRIDGE_SUMMARY.csv", summary_rows, SUMMARY_COLUMNS)

    write_interpretation(
        summaries_dir / "ABC_BRIDGE_INTERPRETATION.txt",
        pair_rows,
        chain_rows,
        chain_test_rows,
        global_class
    )

    print(f"Domain centroid comparison written: {comparisons_dir / 'ABC_DOMAIN_CENTROID_COMPARISON.csv'}")
    print(f"Pairwise domain distance written: {comparisons_dir / 'ABC_PAIRWISE_DOMAIN_DISTANCE.csv'}")
    print(f"Object chain alignment written: {comparisons_dir / 'ABC_OBJECT_CHAIN_ALIGNMENT.csv'}")
    print(f"Transition chain test written: {comparisons_dir / 'ABC_TRANSITION_CHAIN_TEST.csv'}")
    print(f"Bridge summary written: {summaries_dir / 'ABC_BRIDGE_SUMMARY.csv'}")
    print(f"Bridge interpretation written: {summaries_dir / 'ABC_BRIDGE_INTERPRETATION.txt'}")
    print(f"Classification: {global_class}")
    print(f"A-B = {dist['A-B']:.6g}, B-C = {dist['B-C']:.6g}, A-C = {dist['A-C']:.6g}")


def write_interpretation(path, pair_rows, chain_rows, chain_test_rows, global_class):
    lookup = {r["domain_pair"]: r for r in pair_rows}
    ab = lookup["A-B"]
    bc = lookup["B-C"]
    ac = lookup["A-C"]

    lines = []
    lines.append("# ABC_BRIDGE_INTERPRETATION.txt")
    lines.append("# STELLAR_BOUNDARY_DYNAMICS_I")
    lines.append("# A-B-C Tri-Domain Bridge Interpretation")
    lines.append("")
    lines.append("PURPOSE:")
    lines.append("Interpret the tri-domain bridge across pre-boundary profiles, post-boundary")
    lines.append("light curves, and post-boundary spectral line evolution.")
    lines.append("")
    lines.append("DATA LAYERS:")
    lines.append("A = pre-supernova radial support/composition profiles")
    lines.append("B = post-collapse light-curve response trajectories")
    lines.append("C = post-collapse spectral line-evolution trajectories")
    lines.append("")
    lines.append("PRIMARY DOMAIN DISTANCES:")
    lines.append(f"A-B centroid distance = {ab['centroid_distance']} ({ab['separation_label']})")
    lines.append(f"B-C centroid distance = {bc['centroid_distance']} ({bc['separation_label']})")
    lines.append(f"A-C centroid distance = {ac['centroid_distance']} ({ac['separation_label']})")
    lines.append("")
    lines.append("GLOBAL ABC CLASSIFICATION:")
    lines.append(global_class)
    lines.append("")
    if global_class == "A_to_B_contact_with_C_branching":
        lines.append("INTERPRETATION:")
        lines.append("The tri-domain structure is best read as A-to-B contact or weak transition,")
        lines.append("with C branching away as an independent post-collapse observable regime.")
    elif global_class == "monotone_A_to_B_to_C_chain":
        lines.append("INTERPRETATION:")
        lines.append("The tri-domain structure is consistent with a monotone A -> B -> C transition")
        lines.append("chain in reviewed v2 structural-vector space.")
    elif global_class == "compact_three_layer_chain":
        lines.append("INTERPRETATION:")
        lines.append("All three domains remain close enough to form a compact chain.")
    else:
        lines.append("INTERPRETATION:")
        lines.append("The tri-domain structure is mixed and should be interpreted as a linked")
        lines.append("admissible cluster rather than a single simple trajectory.")
    lines.append("")
    lines.append("DOMAIN-PAIR DETAILS:")
    for r in pair_rows:
        lines.append(
            f"{r['domain_pair']}: centroid={r['centroid_distance']} "
            f"label={r['separation_label']}; min_pair={r['min_pair']} "
            f"min_distance={r['min_pairwise_distance']}; max_pair={r['max_pair']} "
            f"max_distance={r['max_pairwise_distance']}; {r['interpretation']}"
        )
    lines.append("")
    lines.append("OBJECT CHAIN ALIGNMENT:")
    for r in chain_rows:
        lines.append(
            f"{r['chain_id']}: A={r['a_object_id']} B={r['b_object_id']} C={r['c_object_id']}; "
            f"dAB={r['distance_ab']}; dBC={r['distance_bc']}; dAC={r['distance_ac']}; "
            f"branching_index={r['branching_index']}; {r['interpretation']}"
        )
    lines.append("")
    lines.append("VALID CLAIM:")
    lines.append("The ABC bridge evaluates whether a catastrophic stellar boundary is better")
    lines.append("described as a simple chain or as routing between linked admissible regimes.")
    lines.append("")
    lines.append("INVALID CLAIMS:")
    lines.append("Do not claim direct supernova prediction, hydrodynamic explosion modeling,")
    lines.append("radiative-transfer modeling, or nucleosynthesis yield recovery.")
    lines.append("")
    lines.append("NEXT STEP:")
    lines.append("Create ABC_BRIDGE_RESULT_RECORD.txt and update the manuscript synthesis.")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def main():
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    compare(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == "__main__":
    main()
