"""E2-P2 builder.  Writes data/*.json and results/P2_*.json (deterministic, exact).  Usage: python build_p2.py [--out DIR]"""
import json
import math
import os
import sys
import time
from collections import Counter
from fractions import Fraction as Fr
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lattice_transport as lt  # noqa: E402
import fibre_transport as ft  # noqa: E402
import graver_transport as gt  # noqa: E402
import cell_transport as ct  # noqa: E402

ct0 = ct.ct0


def dump(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)
        fh.write("\n")


def tl(v):
    return [list(t) if isinstance(t, tuple) else t for t in v]


def squarefree(r):
    if r == 1:
        return True
    if r >= 10 ** 12:
        return None
    p = 2
    while p <= 10 ** 4:
        if r % p == 0:
            if r % (p * p) == 0:
                return False
            r //= p
        if r == 1:
            return True
        p += 1 if p == 2 else 2
    return math.isqrt(r) ** 2 != r


def same_coords(x2, P, q):
    """True / False / None(unresolved): active primes and box of x2 equal (P,q)?"""
    a = x2.numerator
    for p, m in zip(P, q):
        v = 0
        while a % p == 0:
            a //= p
            v += 1
        if v // 2 != m:
            return False
    return squarefree(a)


def spans(F, P, b):
    """Does the finite fibre generate the full relation lattice Lambda_b (same index)?"""
    if not F:
        return False
    B = lt.hnf_basis(list(F), len(P))
    return len(B) == len(P) and lt.index_from_basis(B) == lt.describe(P, b)["index"]


def fibre_of(P, b, q):
    return tuple(sorted(a for a in product(*[range(m + 1) for m in q]) if any(a) and lt.in_lambda(a, P, b)))


# ------------------------------------------------------------------ one transition, complete record
def transition_record(x, geometry=True, full_geometry=False, graver_fn=gt.graver_fast):
    x = Fr(x)
    r = ft.C_step(x)
    x2 = r["next"]
    cd = ft.coordinate_data(x)
    P, q, b = cd["primes"], cd["box"], cd["b"]
    cd2 = ft.coordinate_data(x2)
    assert cd2["primes"] == P and cd2["box"] == q
    b2 = cd2["b"]
    rec = {"x": str(x), "x_next": str(x2), "a": x.numerator, "b": b, "b_next": b2, "L": r["L"], "G": r["G"],
           "increment": str(r["increment"]), "primes": list(P), "box": list(q),
           "n_D_source": len(ft.D(x)), "n_D_target": len(ft.D(x2))}
    rec["lattice"] = {"source": lt.describe(P, b), "target": lt.describe(P, b2), "relation": lt.relation(P, b, b2)}
    F, F2 = fibre_of(P, b, q), fibre_of(P, b2, q)
    assert set(F) == set(ft.fibre(x)) and set(F2) == set(ft.fibre(x2))
    G, G2 = graver_fn(P, b, q), graver_fn(P, b2, q)
    rec["fibre"] = {"source": tl(F), "target": tl(F2), "source_subset_target": set(F) <= set(F2)}
    rec["graver"] = {"source": tl(G), "target": tl(G2), "common": tl(sorted(set(G) & set(G2)))}
    Go, G2o = ft.oriented(G), ft.oriented(G2)
    pred = gt.predict(Go, P, b2)
    rec["graver_prediction"] = {"survive": tl(pred["survive"]), "lost": tl(pred["lost"]),
                                "matches_direct_target_graver": sorted(pred["survive"]) == sorted(set(Go) & set(G2o)),
                                "order_rule_blocked": tl([g for g in Go if gt.order_rule_blocks(g, P, b2)]),
                                "order_rule_exact": sorted(g for g in Go if gt.order_rule_blocks(g, P, b2))
                                == sorted(pred["lost"])}
    cx, cx2 = ct0.build_complex(F, Go, len(q)), ct0.build_complex(F2, G2o, len(q))
    surv = ct0.abstract_survival(cx, cx2)
    rec["cells"] = {"f_source": ct0.f_vector(cx), "f_target": ct0.f_vector(cx2),
                    "survival": {str(j): v for j, v in surv.items()},
                    "betti_abs_source": ct0.betti_complex(cx), "betti_abs_target": ct0.betti_complex(cx2)}
    # cell-level prediction from generator survival (Correction B form: vertices in F' and generators in G')
    Fs2, surv_g = set(F2), set(pred["survive"])
    ok = True
    for j in sorted(cx):
        predicted = {key for key, c in cx[j].items() if all(v in Fs2 for v in c.verts) and all(g in surv_g for g in c.gens)}
        direct = set(cx[j]) & set(cx2.get(j, {}))
        ok = ok and predicted == direct
    rec["cell_prediction_exact"] = ok
    lost_edges = sorted(k for k in cx[1] if k not in cx2[1]) if 1 in cx else []
    kept_edges = sorted(k for k in cx[1] if k in cx2[1]) if 1 in cx else []
    rec["edges"] = {"kept": tl([list(map(list, e)) for e in kept_edges]) if len(F) <= 80 else len(kept_edges),
                    "lost": tl([list(map(list, e)) for e in lost_edges]) if len(F) <= 80 else len(lost_edges),
                    "n_kept": len(kept_edges), "n_lost": len(lost_edges)}
    if geometry and len(q) == 2:
        res = ct.planar_transport(cx, cx2, q[0])
        cs, ct_, ms, mt, S = res.pop("_masks")
        if full_geometry:
            ns, nt = ct.nerve_of_union(cs, ms), ct.nerve_of_union(ct_, mt)
            emb_s, wit_s = ct.planar_embedded(cx, cs, ms)
            emb_t, wit_t = ct.planar_embedded(cx2, ct_, mt)
            res["union_topology"] = {"source": {"betti": ns["betti_b0_b1_b2"], "maximal_cells": ns["maximal_cells"],
                                                 "nerve_simplex_counts": ns["nerve_simplex_counts"], "embedded": emb_s,
                                                 "non_embedded_witness": None if wit_s is None else [str(k) for k in wit_s["cells"]]},
                                     "target": {"betti": nt["betti_b0_b1_b2"], "maximal_cells": nt["maximal_cells"],
                                                 "nerve_simplex_counts": nt["nerve_simplex_counts"], "embedded": emb_t,
                                                 "non_embedded_witness": None if wit_t is None else [str(k) for k in wit_t["cells"]]}}
            res["maximal_cells_source"] = ns["maximal_cell_list"]
            res["maximal_cells_target"] = nt["maximal_cell_list"]
        rec["geometry"] = res
    return rec


def specimen(a, b):
    return transition_record(Fr(a, b), geometry=True, full_geometry=True)


# ------------------------------------------------------------------ family P2-F21
def family(hmax_direct=12, hmax_geom=8, hmax_formula=80):
    rows, forms = [], []
    for h in range(1, hmax_direct + 1):
        x = Fr(21 ** (2 * h), 5)
        rec = transition_record(x, geometry=(h <= hmax_geom), full_geometry=(h <= 6))
        fc = gt.family_counts(h)
        c = rec["cells"]["survival"]
        rec["formula"] = fc
        rec["formula_matches_direct"] = (fc["V_src"] == c["0"]["source"] and fc["V_tgt"] == c["0"]["target"]
                                          and fc["E_src"] == c["1"]["source"] and fc["E_tgt"] == c["1"]["target"]
                                          and fc["E_kept"] == c["1"]["preserved"] and fc["E_lost"] == c["1"]["lost"])
        rec["arith"] = {"L_is_21_pow_h": rec["L"] == 21 ** h, "G_is_20": rec["G"] == 20,
                        "next_is_21_2h_over_4": rec["x_next"] == str(Fr(21 ** (2 * h), 4))}
        rec["common_graver"] = rec["graver"]["common"]
        # keep family rows compact
        for k in ("fibre", "edges"):
            if len(rec["fibre"]["source"]) > 60:
                rec[k] = {kk: (vv if kk in ("n_kept", "n_lost", "source_subset_target") else None)
                          for kk, vv in rec[k].items() if kk in ("n_kept", "n_lost", "source_subset_target")}
        rows.append(rec)
    for h in range(1, hmax_formula + 1):
        forms.append(gt.family_counts(h))
    # quasi-polynomials in h (period 4): E(h) = c2 h^2 + c1 h + c0 for h = r mod 4 (h >= 4); exact fit from 3 points
    qp = {}
    for key in ("V_src", "V_tgt", "E_src", "E_tgt", "E_kept", "E_lost", "E_new"):
        qp[key] = {}
        for r in range(4):
            hs = [h for h in range(4, 40) if h % 4 == r][:3]
            ys = [Fr(gt.family_counts(h)[key]) for h in hs]
            # Lagrange -> coefficients
            x0, x1, x2 = map(Fr, hs)
            y0, y1, y2 = ys
            c2 = (y0 / ((x0 - x1) * (x0 - x2)) + y1 / ((x1 - x0) * (x1 - x2)) + y2 / ((x2 - x0) * (x2 - x1)))
            c1 = (-y0 * (x1 + x2) / ((x0 - x1) * (x0 - x2)) - y1 * (x0 + x2) / ((x1 - x0) * (x1 - x2))
                  - y2 * (x0 + x1) / ((x2 - x0) * (x2 - x1)))
            c0 = (y0 * x1 * x2 / ((x0 - x1) * (x0 - x2)) + y1 * x0 * x2 / ((x1 - x0) * (x1 - x2))
                  + y2 * x0 * x1 / ((x2 - x0) * (x2 - x1)))
            good = all(c2 * h * h + c1 * h + c0 == gt.family_counts(h)[key] for h in range(4, 200) if h % 4 == r)
            qp[key][str(r)] = {"c2": str(c2), "c1": str(c1), "c0": str(c0), "verified_h_4_to_199": good}
    return {"direct": rows, "formula_table_h1_to_80": forms, "quasi_polynomials_mod4": qp}


# ------------------------------------------------------------------ corpus search
def corpus(prime_pool, qmax, bmax, k, geometry_cap):
    rows, skip = [], Counter()
    t0 = time.time()
    for P in combinations(prime_pool, k):
        for q in product(range(1, qmax + 1), repeat=k):
            a = 1
            for p, m in zip(P, q):
                a *= p ** (2 * m)
            for b in range(2, bmax + 1):
                if math.gcd(a, b) != 1:
                    continue
                x = Fr(a, b)
                ds = ft.D(x)
                if not ds:
                    skip["empty_fibre"] += 1
                    continue
                r = ft.C_step(x)
                x2 = r["next"]
                sc = same_coords(x2, P, q)
                if sc is not True:
                    skip["coordinates_change" if sc is False else "UNAVAILABLE_coordinates_undecided"] += 1
                    continue
                b2 = x2.denominator
                if math.prod(lt.orders(P, b)) > 20000 or math.prod(lt.orders(P, b2)) > 20000:
                    skip["UNAVAILABLE_order_product_large"] += 1
                    continue
                if lt.describe(P, b)["index"] == 1 or lt.describe(P, b2)["index"] == 1:
                    skip["trivial_lattice"] += 1
                    continue
                rel = lt.relation(P, b, b2)
                if rel == "EQUAL":
                    skip["equal_lattices"] += 1
                    continue
                rows.append({"primes": list(P), "box": list(q), "x": str(x), "x_next": str(x2), "b": b, "b_next": b2,
                             "L": r["L"], "G": r["G"], "relation": rel})
    return rows, dict(skip), time.time() - t0


def enrich(rows, geometry_cap):
    out, ngeo = [], 0
    for row in rows:
        P, q, b, b2 = tuple(row["primes"]), tuple(row["box"]), row["b"], row["b_next"]
        F, F2 = fibre_of(P, b, q), fibre_of(P, b2, q)
        G, G2 = gt.graver_fast(P, b, q), gt.graver_fast(P, b2, q)
        Go, G2o = ft.oriented(G), ft.oriented(G2)
        cx, cx2 = ct0.build_complex(F, Go, len(q)), ct0.build_complex(F2, G2o, len(q))
        surv = ct0.abstract_survival(cx, cx2)
        pred = gt.predict(Go, P, b2)
        surv_g, Fs2 = set(pred["survive"]), set(F2)
        exact = True
        for j in sorted(cx):
            predicted = {key for key, c in cx[j].items() if all(v in Fs2 for v in c.verts) and all(g in surv_g for g in c.gens)}
            exact = exact and predicted == (set(cx[j]) & set(cx2.get(j, {})))
        blocked = sorted(g for g in Go if gt.order_rule_blocks(g, P, b2))
        r = dict(row)
        r.update({"index_source": lt.describe(P, b)["index"], "index_target": lt.describe(P, b2)["index"],
                  "coupled_source": lt.coupled(P, b) if len(P) > 1 else False,
                  "n_F": len(F), "n_F_target": len(F2), "F_subset_F_target": set(F) <= set(F2),
                  "fibre_spans_source_lattice": spans(F, P, b),
                  "rank_common_graver": ct0.int_rank(tuple(sorted(set(Go) & set(G2o)))) if set(Go) & set(G2o) else 0,
                  "max_surviving_dim": max([j for j, v in surv.items() if v["preserved"] > 0] or [-1]),
                  "f_source": ct0.f_vector(cx), "f_target": ct0.f_vector(cx2),
                  "survival": {str(j): [v["source"], v["preserved"], v["lost"]] for j, v in surv.items()},
                  "n_graver_source": len(G), "n_graver_surviving": len(pred["survive"]),
                  "cell_prediction_exact": exact,
                  "order_rule_exact": blocked == sorted(pred["lost"]),
                  "order_rule_sound": set(blocked) <= set(pred["lost"])})
        if len(q) == 2 and (row["relation"] == "ENLARGE" or ngeo < geometry_cap) and len(F) > 0:
            res = ct.planar_transport(cx, cx2, q[0])
            res.pop("_masks")
            r["geometry"] = {"union_relation": res["union_relation"],
                             "source_cells_vs_target_union": res["source_cells_vs_target_union"]}
            if row["relation"] != "ENLARGE":
                ngeo += 1
        out.append(r)
    return out


# ------------------------------------------------------------------ result files
def write_results(out, A, B, fam, k2, k3, skip2, skip3):
    rows = k2["rows"] + k3["rows"]
    cls = Counter(r["relation"] for r in rows)
    lo = {"definition": "relation classes computed on the infinite lattices (P2-T1); EQUAL rows are counted in 'skipped'",
          "specimens": {"P2-A": {"b": A["b"], "b_next": A["b_next"], **A["lattice"]},
                        "P2-B": {"b": B["b"], "b_next": B["b_next"], **B["lattice"]}},
          "corpus": {"k2": {"parameters": k2["parameters"], "skipped": skip2, "classes": dict(Counter(r["relation"] for r in k2["rows"]))},
                     "k3": {"parameters": k3["parameters"], "skipped": skip3, "classes": dict(Counter(r["relation"] for r in k3["rows"]))}}}
    lo["fibre_inclusion_vs_lattice_order"] = dict(Counter((r["relation"], r["F_subset_F_target"]) .__repr__() for r in rows))
    lo["by_fibre_spanning"] = dict(Counter("%s|spans=%s" % (r["relation"], r["fibre_spans_source_lattice"]) for r in rows))
    lo["denominator_divisibility"] = {
        "b_next_divides_b": dict(Counter(r["relation"] for r in rows if r["b"] % r["b_next"] == 0)),
        "b_next_does_not_divide_b": dict(Counter(r["relation"] for r in rows if r["b"] % r["b_next"] != 0)),
        "b_divides_b_next": dict(Counter(r["relation"] for r in rows if r["b_next"] % r["b"] == 0))}
    dump(lo, os.path.join(out, "results", "P2_LATTICE_ORDER.json"))

    def stat(rs):
        return {"rows": len(rs), "cell_prediction_exact": sum(r["cell_prediction_exact"] for r in rs),
                "order_rule_sound": sum(r["order_rule_sound"] for r in rs), "order_rule_exact": sum(r["order_rule_exact"] for r in rs),
                "max_surviving_dim_le_rank_common": sum(r["max_surviving_dim"] <= max(r["rank_common_graver"], 0) for r in rs),
                "edges_all_kept_and_source_has_edges": sum(1 for r in rs if r["survival"].get("1", [0, 0, 0])[0] > 0 and r["survival"]["1"][2] == 0),
                "edges_all_lost": sum(1 for r in rs if r["survival"].get("1", [0, 0, 0])[0] > 0 and r["survival"]["1"][1] == 0)}
    cs = {"specimens": {"P2-A": {"survival": A["cells"]["survival"], "edges_kept": A["edges"]["kept"], "edges_lost": A["edges"]["lost"],
                                  "graver_common": A["graver"]["common"]},
                        "P2-B": {"survival": B["cells"]["survival"], "edges_kept": B["edges"]["kept"], "edges_lost": B["edges"]["lost"],
                                  "graver_common": B["graver"]["common"]}},
          "family_P2_F21": {"theorem": "P2-TF1", "rows": [{"h": r["formula"]["h"], "formula": r["formula"], "matches_direct": r["formula_matches_direct"],
                                                         "common_graver": r["common_graver"], "two_cells_source": r["cells"]["survival"]["2"]["source"],
                                                         "two_cells_preserved": r["cells"]["survival"]["2"]["preserved"]} for r in fam["direct"]],
                            "quasi_polynomials_mod4": fam["quasi_polynomials_mod4"]},
          "corpus": {"k2": stat(k2["rows"]), "k3": stat(k3["rows"]),
                     "by_relation_k2": {c: stat([r for r in k2["rows"] if r["relation"] == c]) for c in ("ENLARGE", "SHRINK", "INCOMPARABLE")}}}
    dump(cs, os.path.join(out, "results", "P2_CELL_SURVIVAL.json"))

    def gstat(rs):
        g = [r for r in rs if "geometry" in r]
        return {"rows_with_geometry": len(g), "union_relation": dict(Counter(r["geometry"]["union_relation"] for r in g)),
                "rows_with_partial_cells": sum(1 for r in g if any(v["PARTIAL"] for v in r["geometry"]["source_cells_vs_target_union"].values())),
                "abstract_edge_loss_with_full_geometric_containment": sum(1 for r in g if r["survival"].get("1", [0, 0, 0])[2] > 0 and r["geometry"]["union_relation"] in ("U_SUBSET_U2", "EQUAL"))}
    ge = {"specimens": {n: {"union_relation": X["geometry"]["union_relation"], "source_cells_vs_target_union": X["geometry"]["source_cells_vs_target_union"],
                             "partial_cells": X["geometry"]["partial_cells"], "witness_target_not_in_source": X["geometry"]["witness_target_not_in_source"],
                             "union_topology": X["geometry"]["union_topology"], "abstract_betti_source": X["cells"]["betti_abs_source"],
                             "abstract_betti_target": X["cells"]["betti_abs_target"], "maximal_cells_source": X["geometry"]["maximal_cells_source"],
                             "maximal_cells_target": X["geometry"]["maximal_cells_target"]} for n, X in (("P2-A", A), ("P2-B", B))},
          "family_P2_F21": [{"h": r["formula"]["h"], "union_relation": r["geometry"]["union_relation"],
                             "per_dim": r["geometry"]["source_cells_vs_target_union"],
                             "betti_union": [r["geometry"]["union_topology"]["source"]["betti"], r["geometry"]["union_topology"]["target"]["betti"]]
                             if "union_topology" in r["geometry"] else None} for r in fam["direct"] if "geometry" in r],
          "corpus_k2": gstat(k2["rows"]),
          "corpus_k2_ENLARGE": gstat([r for r in k2["rows"] if r["relation"] == "ENLARGE"]),
          "conjecture_CP2": "k=2, Lambda < Lambda' (same primes and box)  =>  U(x) subset U(C(x)).  Supported, NOT proved.",
          "three_coordinate_contrast": {"source": "E2-P1 x1=2*110^4/3 -> x2=110^4 (even-sum lattice, coupled, -> Z^3)",
                                         "witness_cell": {"base": [0, 0, 2], "gens": [[0, 1, -1], [1, 0, -1]]},
                                         "witness_point": ["2/3", "2/3", "2/3"],
                                         "statement": "ENLARGE in k=3 with a coupled source lattice: 6 source cells are PARTIAL; planar containment pattern fails"}}
    dump(ge, os.path.join(out, "results", "P2_GEOMETRY.json"))

    ce = []
    enl = [r for r in rows if r["relation"] == "ENLARGE"]
    kept = [r for r in k2["rows"] if r["relation"] == "ENLARGE" and r["survival"]["1"][0] > 0 and r["survival"]["1"][2] == 0]
    ce.append({"id": "CE-P2-F1", "proposed_law": "Strict lattice enlargement necessarily destroys existing Graver edges", "verdict": "FALSE",
               "witness": {"transition": "55^12/27 -> 55^12/18", "edges_source": 5, "edges_lost": 0}, "corpus_rows_with_all_edges_kept": len(kept),
               "of_enlarge_rows_with_edges": sum(1 for r in k2["rows"] if r["relation"] == "ENLARGE" and r["survival"]["1"][0] > 0)})
    bad = [r for r in rows if r["relation"] in ("SHRINK", "INCOMPARABLE") and r["F_subset_F_target"]]
    wit = lambda c: sorted([r for r in rows if r["relation"] == c], key=lambda r: (-r["n_F"], r["b"], r["x"]))[0]
    ce.append({"id": "CE-P2-F2", "proposed_law": "Occurrence-fibre inclusion implies full lattice inclusion", "verdict": "FALSE",
               "n_FIELD_I_transitions_with_F_subset_F_next_and_non_ordered_lattices": len(bad),
               "witness_SHRINK": {k: wit("SHRINK")[k] for k in ("x", "x_next", "primes", "box", "b", "b_next", "n_F", "n_F_target")},
               "witness_INCOMPARABLE": {k: wit("INCOMPARABLE")[k] for k in ("x", "x_next", "primes", "box", "b", "b_next", "n_F", "n_F_target")},
               "non_FIELD_I_pair": {"x": "484/3", "x_prime": "484/7", "primes": [2, 11], "box": [1, 1], "fibre": [[1, 1]], "relation": "INCOMPARABLE"}})
    nd = [r for r in enl if r["b"] % r["b_next"] != 0]
    ce.append({"id": "CE-P2-F3", "proposed_law": "Denominator divisibility b' | b is necessary for Lambda_b <= Lambda_b'", "verdict": "FALSE",
               "witness": {"transition": "21^8/5 -> 21^8/4", "b": 5, "b_next": 4, "relation": "ENLARGE"}, "corpus_ENLARGE_rows_with_b_next_not_dividing_b": len(nd), "of": len(enl)})
    ce.append({"id": "CE-P2-F4", "proposed_law": "Abstract edge loss implies geometric segment loss", "verdict": "FALSE",
               "witness": {"transition": "21^8/5 -> 21^8/4", "edges_lost": A["edges"]["n_lost"], "source_cells_partial": 0},
               "corpus": gstat(k2["rows"])["abstract_edge_loss_with_full_geometric_containment"]})
    ce.append({"id": "CE-P2-F5", "proposed_law": "The planar containment pattern (ENLARGE => U subset U') extends to genuine three-coordinate coupling", "verdict": "FALSE",
               "witness": ge["three_coordinate_contrast"]})
    pair = None
    cand = [r for r in k2["rows"] if r["relation"] == "ENLARGE" and r["survival"]["1"][0] > 0]
    seen = {}
    for r in sorted(cand, key=lambda r: (r["b"], r["x"])):
        key = (tuple(r["primes"]), r["index_source"], r["index_target"], tuple(r["box"]))
        seen.setdefault(key, []).append(r)
    for key, rs in sorted(seen.items(), key=lambda kv: str(kv[0])):
        lost0 = [r for r in rs if r["survival"]["1"][2] == 0]
        lost1 = [r for r in rs if r["survival"]["1"][2] > 0]
        if lost0 and lost1:
            pair = (lost0[0], lost1[0])
            break
    if pair is None:
        key2 = {}
        for r in cand:
            key2.setdefault((r["index_source"], r["index_target"], r["survival"]["1"][2] == 0), []).append(r)
        for (i, j, z), rs in sorted(key2.items(), key=lambda kv: str(kv[0])):
            if (i, j, not z) in key2:
                pair = (key2[(i, j, True)][0], key2[(i, j, False)][0])
                break
    ce.append({"id": "CE-P2-F6", "proposed_law": "Lattice-order data (class, indices) alone determine geometric transport", "verdict": "FALSE",
               "witness_pair": [{k: r[k] for k in ("x", "x_next", "primes", "box", "relation", "index_source", "index_target", "survival")} for r in pair]})
    sh = sorted([r for r in rows if r["relation"] == "SHRINK" and r["n_F"] >= 2], key=lambda r: (-r["n_F"], r["b"]))[:1]
    ce.append({"id": "CE-P2-L6", "proposed_law": "Along a FIELD-I step with unchanged primes and box the relation lattice never shrinks (observed in all 405 E2-P1 sample transitions)",
               "verdict": "FALSE", "n_SHRINK_rows": cls["SHRINK"], "witness": [{k: r[k] for k in ("x", "x_next", "primes", "box", "b", "b_next", "n_F", "n_F_target", "fibre_spans_source_lattice")} for r in sh],
               "note": "no SHRINK or INCOMPARABLE row has a source fibre spanning its lattice: " + str(
                   sum(1 for r in rows if r["relation"] in ("SHRINK", "INCOMPARABLE") and r["fibre_spans_source_lattice"]) == 0)})
    dump({"counterexamples": ce}, os.path.join(out, "results", "P2_COUNTEREXAMPLES.json"))


def main():
    out = os.path.join(os.path.dirname(HERE))
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    t0 = time.time()
    A = specimen(21 ** 8, 5)
    B = specimen(55 ** 12, 27)
    dump({"specimen": "P2-A", "transition": "21^8/5 -> 21^8/4", **A}, os.path.join(out, "data", "P2_A.json"))
    dump({"specimen": "P2-B", "transition": "55^12/27 -> 55^12/18", **B}, os.path.join(out, "data", "P2_B.json"))
    fam = family()
    dump(fam, os.path.join(out, "data", "P2_F21.json"))
    rows2, skip2, t2 = corpus([2, 3, 5, 7, 11, 13, 17], 4, 130, 2, 0)
    rows3, skip3, t3 = corpus([2, 3, 5, 7], 2, 60, 3, 0)
    e2, e3 = enrich(rows2, 60), enrich(rows3, 0)
    k2d = {"parameters": {"primes": [2, 3, 5, 7, 11, 13, 17], "q_max": 4, "b_max": 130, "states": "x = prod p_i^(2 q_i) / b"}, "skipped": skip2, "rows": e2}
    k3d = {"parameters": {"primes": [2, 3, 5, 7], "q_max": 2, "b_max": 60, "states": "x = prod p_i^(2 q_i) / b"}, "skipped": skip3, "rows": e3}
    write_results(out, A, B, fam, k2d, k3d, skip2, skip3)
    dump({"k2": {"parameters": {"primes": [2, 3, 5, 7, 11, 13, 17], "q_max": 4, "b_max": 130,
                                "states": "x = prod p_i^(2 q_i) / b"},
                 "skipped": skip2, "rows": e2},
          "k3": {"parameters": {"primes": [2, 3, 5, 7], "q_max": 2, "b_max": 60, "states": "x = prod p_i^(2 q_i) / b"},
                 "skipped": skip3, "rows": e3}}, os.path.join(out, "data", "SEARCH_CORPUS.json"))
    print("built in %.1fs; corpus k2 %d rows, k3 %d rows" % (time.time() - t0, len(e2), len(e3)))


if __name__ == "__main__":
    main()
