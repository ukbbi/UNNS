"""GEO-HD-1B / E2-P1 -- builder.  Writes data/*.json and results/E2_TRANSPORT.json,
results/E2_COUNTEREXAMPLES.json (the independent certificates are written by RUN_VERIFY.py).
Usage: python src/build_e2.py [--out DIR]   (default: package root)  Standard library only."""
import json
import os
import sys
from fractions import Fraction
from itertools import combinations
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fibre_transport as ft  # noqa: E402
import cell_transport as ct  # noqa: E402

X0 = Fraction(110 ** 4, 3)
SPEC = "GEO_HD_1_SPEC_v003"


def j(o):
    return json.dumps(o, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def stage_states():
    x1 = X0 + Fraction(110 ** 4, 3)
    x2 = Fraction(110 ** 4)
    return [X0, x1, x2]


def complex_for(x):
    cd = ft.coordinate_data(x)
    F = ft.fibre(x)
    G = ft.region_graver(cd["primes"], cd["b"], cd["box"])
    cx = ct.build_complex(F, ft.oriented(G), len(cd["primes"]))
    return cd, F, G, cx


def cell_json(cx):
    return {str(d): [{"base": list(c.base), "gens": [list(g) for g in c.gens], "verts": [list(v) for v in c.verts]}
                     for _, c in sorted(cx[d].items())] for d in sorted(cx)}


def geometric_block(cx, geo, name):
    allc = [c for d in cx for c in cx[d].values()]
    gm = ct.geometric_maximal(allc, geo)
    nb = ct.nerve_betti([geo.mask(c) for c in gm], 4)
    import hashlib
    nh = [hashlib.sha256(json.dumps(sd).encode()).hexdigest() for sd in nb["simplices"]]
    fm = ct.face_maximal(cx)
    emb, wit = ct.is_embedded(fm, geo, True)
    return {"stage": name, "geometric_maximal": [{"dim": c.dim, "base": list(c.base), "gens": [list(g) for g in c.gens]} for c in gm],
            "nerve_simplex_counts": nb["simplex_counts"], "nerve_simplices_sha256_by_dim": nh, "U_betti_b0_b1_b2_b3": nb["betti"],
            "face_maximal_count": len(fm), "embedded": emb,
            "nonembedded_witness": None if emb else [[list(v) for v in wit[0]], [list(v) for v in wit[1]]]}


def euler_union_from_betti(b):
    return sum((-1) ** i * x for i, x in enumerate(b))


def lattice_relation(primes, b, b2, q):
    """Exact comparison of Lambda_b and Lambda_b2 on [-q,q]^k by enumeration."""
    from itertools import product
    box = [range(-m, m + 1) for m in q]
    A = {v for v in product(*box) if ft.in_lattice(v, primes, b)}
    B = {v for v in product(*box) if ft.in_lattice(v, primes, b2)}
    return "EQUAL" if A == B else "ENLARGE" if A < B else "SHRINK" if B < A else "INCOMPARABLE"


def group_order(primes, b):
    """|<p_i mod b>| in (Z/b)^x  (= index of Lambda_b in Z^k)."""
    if b == 1:
        return 1
    seen = {1}
    frontier = [1]
    gens = [p % b for p in primes]
    while frontier:
        nxt = []
        for h in frontier:
            for g in gens:
                y = h * g % b
                if y not in seen:
                    seen.add(y)
                    nxt.append(y)
        frontier = nxt
    return len(seen)


def predicted_relation(primes, b, b2):
    """Criterion: Lambda_b <= Lambda_b2  <=>  |H_lcm(b,b2)| = |H_b|   (index formula)."""
    l = b * b2 // gcd(b, b2)
    hb, hb2, hl = group_order(primes, b), group_order(primes, b2), group_order(primes, l)
    sub, sup = hl == hb, hl == hb2  # Lambda_b <= Lambda_b2 ; Lambda_b2 <= Lambda_b
    return "EQUAL" if sub and sup else "ENLARGE" if sub else "SHRINK" if sup else "INCOMPARABLE"


def sweep(primes_pool, ks, steps=3):
    rows = []
    for k in ks:
        for P in combinations(primes_pool, k):
            n = 1
            for p in P:
                n *= p
            x = Fraction(n ** 4, 3)
            orb = ft.orbit(x, steps)
            seq = []
            for r in orb:
                cd = ft.coordinate_data(r["x"])
                Fn = ft.fibre(r["x"])
                idx = ct.hnf_index(Fn, len(cd["primes"]))
                seq.append({"n": r["n"], "b": cd["b"], "primes": list(cd["primes"]), "box": list(cd["box"]), "fibre": len(Fn),
                            "F_generates_lattice": idx is not None and idx == group_order(tuple(cd["primes"]), cd["b"])})
            trans = []
            for s0, s1 in zip(seq, seq[1:]):
                if s0["primes"] == s1["primes"] and s0["box"] == s1["box"]:
                    act = lattice_relation(tuple(s0["primes"]), s0["b"], s1["b"], tuple(s0["box"]))
                    pre = predicted_relation(tuple(s0["primes"]), s0["b"], s1["b"])
                    trans.append({"from": s0["n"], "relation_actual": act, "relation_predicted": pre, "match": act == pre,
                                  "F_generates_source_lattice": s0["F_generates_lattice"],
                                  "fibre_from": s0["fibre"], "fibre_to": s1["fibre"]})
                else:
                    trans.append({"from": s0["n"], "relation_actual": "COORDINATES_CHANGE", "relation_predicted": None, "match": None,
                                  "F_generates_source_lattice": s0["F_generates_lattice"],
                                  "fibre_from": s0["fibre"], "fibre_to": s1["fibre"]})
            G0 = orb[0]["G"]
            rows.append({"k": k, "primes": list(P), "contains_2": 2 in P, "G0": G0, "stages": seq, "transitions": trans,
                         "denominators_divide_G0": all(G0 % st["b"] == 0 for st in seq)})
    return rows


def main():
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.dirname(HERE)
    os.makedirs(os.path.join(out, "data"), exist_ok=True)
    os.makedirs(os.path.join(out, "results"), exist_ok=True)
    xs = stage_states()

    # ---------------- orbit
    orb = ft.orbit(X0, 7)
    orbit_json = {"spec": SPEC, "scope": "FIELD-I collective map C(x)=x+L^2/G (not SELECT-II)", "x0": str(X0),
                  "a0": 110 ** 4, "steps": []}
    for r in orb:
        orbit_json["steps"].append({"n": r["n"], "x": str(r["x"]), "numerator": r["a"], "denominator": r["b"],
                                    "num_indices": len(r["D"]), "L": r.get("L"), "G": r.get("G"),
                                    "increment": str(r["increment"]) if "increment" in r else None})
    orbit_json["stage_map"] = {"stage0": "n=0", "stage1": "n=1", "stage2": "n=2"}
    orbit_json["facts"] = {
        "x1_equals_2x0": orb[1]["x"] == 2 * orb[0]["x"], "x2_equals_110^4": orb[2]["x"] == 110 ** 4,
        "index_sets_equal_0_1": orb[0]["D"] == orb[1]["D"], "index_set_0_subset_2": set(orb[0]["D"]) < set(orb[2]["D"]),
        "regime_I_x_n+3_eq_4x_n_from_n=2": all(orb[n + 3]["x"] == 4 * orb[n]["x"] for n in range(2, 5))}
    open(os.path.join(out, "data", "E2_ORBIT.json"), "w", newline="\n").write(j(orbit_json))

    # ---------------- fibres, complexes
    recs, cxs, Gs, Fs, cds = [], [], [], [], []
    for n, x in enumerate(xs):
        cd, F, G, cx = complex_for(x)
        recs.append(ft.stage_record(n, x))
        cxs.append(cx), Gs.append(G), Fs.append(F), cds.append(cd)
    fib = {"spec": SPEC, "stages": recs,
           "vertex_transport": {"0->1": ft.vertex_transport(Fs[0], Fs[1]), "1->2": ft.vertex_transport(Fs[1], Fs[2]),
                                "0->2": ft.vertex_transport(Fs[0], Fs[2])},
           "move_transport": {"0->1": ft.move_transport(Gs[0], Gs[1]), "1->2": ft.move_transport(Gs[1], Gs[2]),
                              "0->2": ft.move_transport(Gs[0], Gs[2])}}
    fib["vertex_transport_summary"] = {k: {kk: len(vv) for kk, vv in v.items()} for k, v in fib["vertex_transport"].items()}
    open(os.path.join(out, "data", "E2_FIBRES.json"), "w", newline="\n").write(j(fib))

    cells_json = {"spec": SPEC, "grammar": "GEO-I v002 sec.1: parallelotopes P(u;g_1..g_j), lex-positive independent region-Graver generators, all corners in F; K_abs face-closed",
                  "stage0": {"f_vector": ct.f_vector(cxs[0]), "cells": cell_json(cxs[0])},
                  "stage1": {"identical_to_stage0": True, "f_vector": ct.f_vector(cxs[1])},
                  "stage2": {"f_vector": ct.f_vector(cxs[2]), "cells": cell_json(cxs[2])}}
    assert [sorted(cxs[0][d]) for d in cxs[0]] == [sorted(cxs[1][d]) for d in cxs[1]]
    open(os.path.join(out, "data", "E2_CELLS.json"), "w", newline="\n").write(j(cells_json))

    # ---------------- transport
    geo = ct.Geometry((2, 2, 2), list(ft.oriented(Gs[0])) + list(ft.oriented(Gs[2])))
    ok_boundary = [ct.check_boundary_squared(c) for c in cxs]
    abstract = {"0->1": ct.abstract_survival(cxs[0], cxs[1]), "1->2": ct.abstract_survival(cxs[1], cxs[2]),
                "0->2": ct.abstract_survival(cxs[0], cxs[2])}
    topo = {}
    for n in (0, 2):
        topo["K_abs_stage%d" % n] = {"f_vector": ct.f_vector(cxs[n]), "euler": ct.euler(ct.f_vector(cxs[n])),
                                     "betti_Q": ct.betti_complex(cxs[n]), "boundary_squared_zero": ok_boundary[n]}
    geom0, geom2 = geometric_block(cxs[0], geo, "stage0"), geometric_block(cxs[2], geo, "stage2")
    # U2 = Y at all candidate points (Prop 2 of GEO-I v002) -------------------------------------
    um = 0
    for d in cxs[2]:
        for c in cxs[2][d].values():
            um |= geo.mask(c)
    Ym = geo.mask_where(lambda x: max(x) >= 1)
    # geometric survival of source cells inside U2 = Y
    le1 = geo.mask_where(lambda x: all(t <= 1 for t in x))
    ones = [geo.mask_where(lambda x, i=i: x[i] == 1) for i in range(3)]
    status = {}
    partial = []
    for d in sorted(cxs[0]):
        cnt = {"CONTAINED": 0, "PARTIAL": 0}
        for key, c in sorted(cxs[0][d].items()):
            s = ct.corner_region_status(c, geo, ones, le1)
            cnt[s] += 1
            if s == "PARTIAL":
                S = geo.mask(c) & le1
                pts = [geo.cand[i] for i in range(len(geo.cand)) if (S >> i) & 1]
                opn = [p for p in pts if max(p) < 1]
                if opn:
                    cen = min(opn, key=lambda p: (max(Fraction(t).denominator for t in p), p))
                else:
                    cen = tuple(sum(p[t] for p in pts) / len(pts) for t in range(3))
                partial.append({"dim": c.dim, "base": list(c.base), "gens": [list(g) for g in c.gens],
                                "witness_point_in_cell_with_all_coordinates_lt_1": [str(t) for t in cen]})
        status[str(d)] = cnt
    # sufficient+necessary pattern for this lattice/box: partial <=> corner set contains T={(0,1,1),(1,0,1),(1,1,0)}
    T = {(0, 1, 1), (1, 0, 1), (1, 1, 0)}
    tcrit = all((T <= set(c.verts)) == (ct.corner_region_status(c, geo, ones, le1) == "PARTIAL")
                for d in cxs[0] for c in cxs[0][d].values())
    # inclusion tests of whole unions
    u0 = 0
    for d in cxs[0]:
        for c in cxs[0][d].values():
            u0 |= geo.mask(c)
    union_rel = {"U0_subset_U2_at_candidates": (u0 & ~um) == 0, "U2_subset_U0_at_candidates": (um & ~u0) == 0,
                 "U2_equals_Y_at_candidates": um == Ym}
    transport = {"spec": SPEC, "scope": "FIELD-I step; K_abs / U / K_emb kept distinct (K_emb not constructed in 3D)",
                 "abstract_survival": abstract, "topology": topo,
                 "geometry": {"stage0": geom0, "stage2": geom2, "union_relations": union_rel,
                              "source_cells_vs_U2": status, "partial_cells": partial,
                              "partial_iff_corners_contain_T": tcrit, "T": [list(t) for t in sorted(T)],
                              "candidate_points": len(geo.cand), "plane_family_size": len(geo.planes), "denominator": geo.den},
                 "stage1_vs_stage0": "identical lattice, box, fibre, Graver set, K_abs, U (state depends only on (Lambda,q))",
                 "move_transport_summary": {k: {kk: len(vv) for kk, vv in v.items()} for k, v in fib["move_transport"].items()}}

    # frozen-baseline reproductions ------------------------------------------------------------
    base = {}
    # k=2: pure model Gamma_{2,1} (v004 S2 hand computation: V=4,E=5,beta1=2)
    cx2d = ct.build_complex(((0, 2), (1, 1), (2, 0), (2, 2)), ft.oriented(ft.region_graver((2, 5), 3, (2, 2))), 2)
    base["k2_parity_hollow_box"] = {"f_vector": ct.f_vector(cx2d), "betti_K_abs": ct.betti_complex(cx2d), "expected_v004_S2": {"V": 4, "E": 5, "beta1": 2}}
    # parity k=3: smallest non-embedded box (2,1,1) and embeddedness of smaller boxes
    emb = {}
    for q in [(1, 1, 1), (2, 1, 1), (2, 2, 1), (2, 2, 2)]:
        from itertools import product as _p
        F = tuple(sorted(a for a in _p(*[range(m + 1) for m in q]) if any(a) and sum(a) % 2 == 0))
        G = ft.oriented(ft.region_graver((2, 5, 11), 3, q))
        cx = ct.build_complex(F, G, 3)
        g3 = ct.Geometry(q, G)
        emb[str(q)] = {"fibre": len(F), "embedded": ct.is_embedded(ct.face_maximal(cx), g3), "f_vector": ct.f_vector(cx)}
    base["parity_k3_embedding_by_box"] = emb
    base["target_b1_k3_box222"] = {"f_vector": ct.f_vector(cxs[2]), "maximal_cubes": 7, "betti": ct.betti_complex(cxs[2]),
                                   "expected": "v002 Prop 1: d_cell=k (max q_i>=2); Prop 2: contractible"}
    transport["frozen_baseline_reproduction"] = base

    # k=4 abstract transport (no 4-D geometry) -------------------------------------------------
    k4 = {}
    for name, b in (("stage0", 3), ("stage2", 1)):
        P = (2, 5, 11, 17)
        q = (2, 2, 2, 2)
        from itertools import product as _p
        F = tuple(sorted(a for a in _p(*[range(m + 1) for m in q]) if any(a) and ft.in_lattice(a, P, b)))
        G = ft.oriented(ft.region_graver(P, b, q))
        cx = ct.build_complex(F, G, 4)
        k4[name] = {"x": "1870^4/3" if b == 3 else "1870^4", "fibre": len(F), "f_vector": ct.f_vector(cx),
                    "betti_K_abs": ct.betti_complex(cx), "cx": cx}
    k4["abstract_survival_0_to_2"] = ct.abstract_survival(k4["stage0"].pop("cx"), k4["stage2"].pop("cx"))
    transport["k4_PARITY_TERNARY_K4_abstract"] = k4

    # family sweeps -------------------------------------------------------------------------------
    pool = [2, 5, 11, 17, 23, 29, 41, 47, 53]
    sw = sweep(pool, (2, 3))
    sw4 = sweep([2, 5, 11, 17, 23, 29], (4,))
    pat = {}
    for r in sw + sw4:
        key = (r["k"], tuple((s["fibre"], s["b"]) for s in r["stages"]))
        pat.setdefault(str(key), []).append(r["primes"])
    transport["family_sweep"] = {"pool": pool, "rows": sw + sw4,
                                 "patterns": {k: {"count": len(v), "example": v[0], "all_contain_2": all(2 in P for P in v)} for k, v in pat.items()}}
    # theorem 1 prediction for every row containing 2
    t1 = []
    for r in sw + sw4:
        if r["contains_2"]:
            k = r["k"]
            exp = [((3 ** k - 1) // 2, 3), ((3 ** k - 1) // 2, 3), (3 ** k - 1, 1), (3 ** k - 1, 1)]
            t1.append({"primes": r["primes"], "match": [(s["fibre"], s["b"]) for s in r["stages"]] == exp})
    transport["theorem1_check_rows_containing_2"] = {"rows": len(t1), "all_match": all(x["match"] for x in t1)}
    crit = [t for r in sw + sw4 for t in r["transitions"] if t["match"] is not None]
    transport["lattice_relation_criterion_check"] = {"transitions_tested": len(crit), "all_match": all(t["match"] for t in crit),
                                                     "relations_seen": sorted({t["relation_actual"] for t in crit})}
    transport["orbit_lattice_floor_check"] = {"rows": len(sw + sw4), "all_denominators_divide_G0": all(r["denominators_divide_G0"] for r in sw + sw4),
                                              "basis": "Vol.II ch.1: b | G(x), G(C(x)) | G(x), reduced denominator of C(x) divides G(x)"}
    hyp = [t for t in crit if t["F_generates_source_lattice"]]
    transport["no_shrink_lemma_check"] = {"transitions_with_hypothesis": len(hyp), "of_tested": len(crit),
                                          "none_is_SHRINK_or_INCOMPARABLE": all(t["relation_actual"] in ("EQUAL", "ENLARGE") for t in hyp),
                                          "note": "hypothesis: F_n generates Lambda_{b_n}; conclusion uses inherited Vol.II Thm 1.3 (D(x)<=D(C(x)))"}
    transport["lattice_relation_counts"] = {rel: sum(1 for r in sw + sw4 for t in r["transitions"] if t["relation_actual"] == rel)
                                            for rel in ("EQUAL", "ENLARGE", "SHRINK", "INCOMPARABLE", "COORDINATES_CHANGE")}
    open(os.path.join(out, "results", "E2_TRANSPORT.json"), "w", newline="\n").write(j(transport))

    # ---------------- counterexamples
    src_edge = cxs[0][1]
    e0 = sorted(src_edge)[0]
    ce = {"spec": SPEC, "counterexamples": [
        {"id": "CE-1", "proposed_law": "L1: if D(x) <= D(C(x)) (occurrence indices persist) then Graver edges of K_abs(x) persist as edges of K_abs(C(x)).",
         "verdict": "FALSE", "witness": {"x": "2*110^4/3", "C(x)": "110^4",
                                          "edge": [list(e0[0]), list(e0[1])], "move": [e0[1][i] - e0[0][i] for i in range(3)],
                                          "reason": "all 45 source edges have even coordinate-sum change; every target edge changes the coordinate sum by 1"},
         "exact_data": {"vertices_preserved": 13, "edges_preserved": abstract["0->2"][1]["preserved"], "edges_source": abstract["0->2"][1]["source"]}},
        {"id": "CE-2", "proposed_law": "L2: if every vertex of a source cell persists then the realized geometry U(x) is contained in U(C(x)).",
         "verdict": "FALSE", "witness": {"partial_cells": partial[:3], "n_partial_total": len(partial)},
         "exact_data": union_rel},
        {"id": "CE-3", "proposed_law": "L3: abstract loss of a cell implies loss of its geometric image.",
         "verdict": "FALSE", "witness": {"statement": "all 45 source edges are abstractly lost (not target edges) yet every source edge segment lies inside U2 = Y",
                                          "source_cells_vs_U2": status}},
        {"id": "CE-4", "proposed_law": "L4: topology is monotone under occurrence-index inclusion (Betti numbers of K_abs or of U can only grow, or only shrink).",
         "verdict": "FALSE", "witness": {"K_abs_betti": [topo["K_abs_stage0"]["betti_Q"], topo["K_abs_stage2"]["betti_Q"]],
                                          "U_betti": [geom0["U_betti_b0_b1_b2_b3"], geom2["U_betti_b0_b1_b2_b3"]],
                                          "note": "b1(K_abs): 6 -> 0 but b2(U): 18 -> 0 and K_abs b2: 6 -> 0; abstract and geometric topology of the source disagree (non-embedded)"}},
        {"id": "CE-5", "proposed_law": "L5: a change of denominator b along a FIELD-I orbit changes the relation lattice (hence the geometry).",
         "verdict": "FALSE", "witness": {"example_primes": [5, 17, 29], "denominators": [3, 12], "relation": "EQUAL",
                                          "reason": "primes = 1 mod 4 so chi_12 = chi_3 on the active primes; lattice, fibre, K_abs, U unchanged"}}]}
    open(os.path.join(out, "results", "E2_COUNTEREXAMPLES.json"), "w", newline="\n").write(j(ce))
    print("built:", out)


if __name__ == "__main__":
    main()
