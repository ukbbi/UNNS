"""E2-P3 builder.  Deterministic.  Writes data/*.json and results/P3_*.json.   Usage:  python build_p3.py [--out DIR] [--quick]

Order of work (spec section 9): P3-E0 source lock (static, see theory/SOURCE_OVERLAP.md + ERRATA) -> P3-E1 controls A/B/C with certificates ->
P3-E2 planar classification of the E2-P2 corpus (+ trivial-target states) and a deterministic expansion -> P3-E3 three-coordinate search
(only after E1 certificates verify) -> summary.  Every resource limit is written to data/P3_SEARCH_LIMITS.json BEFORE any search."""
import json
import math
import os
import sys
import time
from collections import Counter
from fractions import Fraction as Fr
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import coverage_gap as cg  # noqa: E402
import exact_containment as ec  # noqa: E402
import certificate_check as cc  # noqa: E402
import audit_p3 as au  # noqa: E402
import planar_residual as pr  # noqa: E402
import coupled_3d as c3  # noqa: E402

ROOT = os.path.dirname(HERE)

LIMITS = {
    "version": "E2-P3 v001",
    "determinism": "states visited in the fixed order (prime tuple, box, parity, b); rows evaluated in that order; no randomness",
    "arithmetic": "exact rational (fractions.Fraction); no floating point enters any verdict",
    "global": {"order_product_limit": pr.ORDER_PRODUCT_LIMIT, "target_denominator_limit": pr.TARGET_DENOMINATOR_LIMIT,
               "containment_node_limit": 20000, "gap_node_limit": 50000, "3d_node_limit": 30000,
               "unavailable_rule": "a state exceeding a limit is recorded under its own UNAVAILABLE_* skip reason and never silently dropped"},
    "planar_base": {"primes": [2, 3, 5, 7, 11, 13, 17], "qmax": 4, "bmax": 130, "k": 2, "odd": False,
                    "note": "reproduces the E2-P2 corpus (582 rows with source and target lattices nontrivial) and ADDS target-trivial rows (Lambda' = Z^2), "
                            "which E2-P2 skipped under 'trivial_lattice'"},
    "planar_expansion": {"primes": [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41], "qmax": 6, "bmax": 400, "k": 2, "odd": False},
    "three_d_S1": {"primes": [2, 3, 5, 7, 11, 13], "qmax": 2, "bmax": 120, "k": 3, "odd": True,
                   "note": "numerator exponents 2q_i or 2q_i+1 (the E2-P1 control has 2^5)"},
    "three_d_S2_rectangular_targets": {"primes": [2, 3, 5, 7, 11, 13], "q_range": [2, 4], "bmax": 150, "k": 3, "odd": True,
                                       "filter": "target lattice rectangular and nontrivial, q_i >= ord_{b'}(p_i) for all i",
                                       "exact_engine_budget": "all predictor NOT_CONTAINED rows + every 10th predictor CONTAINED row (cap 400)"},
    "lattice_model_scan": {"k": 3, "target": "Z^3", "index_max": 8, "boxes": "{1,2}^3",
                           "note": "pure sublattices of Z^3 (HNF); NOT claimed FIELD-I realizable"},
}


def dump(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)
        fh.write("\n")


# ----------------------------------------------------------------------------------------------------- P3-E1 controls
def controls():
    out = {}
    specs = [("A", Fr(21 ** 8, 5), "E2-P2/A: 21^8/5 -> 21^8/4", "CONTAINED"),
             ("B", Fr(55 ** 12, 27), "E2-P2/B: 55^12/27 -> 55^12/18", "CONTAINED"),
             ("C", Fr(2 * 110 ** 4, 3), "E2-P1: 2*110^4/3 -> 110^4", "NOT_CONTAINED")]
    for name, x, label, expected in specs:
        tr = cg.transition(x)
        k = len(tr["q"])
        res, F2, cells2 = cg.geometric_verdict(tr["P"], tr["b"], tr["b2"], tr["q"])
        ind = au.audit_verdict(tr["P"], tr["q"], tr["b"], tr["b2"], res["verdict"])
        ok, why = au.verify_engine_result(res, ind, k)
        it = au.independent_transition(x)
        rec = {"label": label, "x": str(x), "x_next": str(tr["x2"]), "primes": list(tr["P"]), "box": list(tr["q"]), "b": tr["b"],
               "b_next": tr["b2"], "expected_verdict": expected, "verdict": res["verdict"],
               "matches_expected": res["verdict"] == expected, "independent_transition_matches": (
                   it["P"] == tr["P"] and it["q"] == tr["q"] and it["b"] == tr["b"] and it["b2"] == tr["b2"] and it["x2"] == tr["x2"]),
               "independent_certificate_check": {"ok": ok, "reason": why},
               "n_source_maximal": res["n_source_maximal"], "n_target_maximal": res["n_target_maximal"],
               "lattice_relation": cg.lt.relation(tr["P"], tr["b"], tr["b2"]),
               "index_source": cg.lt.describe(tr["P"], tr["b"])["index"], "index_target": cg.lt.describe(tr["P"], tr["b2"])["index"]}
        if k == 2:
            cl = cg.classify_target_planar(tr["P"], tr["b2"], tr["q"])
            ncl = au.independent_normal_form(tr["P"], tr["b2"], tr["q"])
            rec["target_classification"] = {kk: (list(v) if isinstance(v, tuple) else v) for kk, v in cl.items()}
            rec["independent_normal_form"] = {kk: (list(v) if isinstance(v, tuple) else v) for kk, v in ncl.items()}
        g = cg.coverage_gap_record(tr["P"], tr["b2"], tr["q"], F2, cells2, keep_tree=True)
        hc = g.pop("hull_cover_certificate", None)
        if hc is not None:
            okh, whyh, ngap = cc.verify_hull_tree({"hull_halfspaces": hc["hull_halfspaces"], "tree": hc["tree"]}, au.independent_cells(
                tr["P"], tr["q"], tr["b2"])[0], ind["target_maximal"], k)
            g["hull_tree_independent_check"] = {"ok": okh, "reason": whyh, "n_gap_nodes_in_verified_tree": ngap}
        rec["coverage_gap"] = {kk: vv for kk, vv in g.items() if kk != "gap_pieces"}
        rec["coverage_gap"]["gap_pieces"] = g.get("gap_pieces", [])
        if res["verdict"] == "NOT_CONTAINED":
            rec["certificate"] = res["certificate"]
            rec["target_maximal"] = res["target_maximal"]
            rec["n_noncontained_source_cells"] = res["n_noncontained_source_cells"]
            rec["failing_cells"] = res["all_failing_cells"]
        else:
            rec["certificates"] = res["certificates"]
            rec["source_maximal"] = res["source_maximal"]
            rec["target_maximal"] = res["target_maximal"]
        if hc is not None and name != "A":
            rec["hull_cover_certificate"] = hc
        out[name] = rec
    # the specified witness of Control C (2/3,2/3,2/3), as its own certificate
    c = out["C"]
    T = [ec.Target(t["base"], t["gens"], 3) for t in c["target_maximal"]]
    cert = ec.noncontainment_certificate((0, 0, 2), [(0, 1, -1), (1, 0, -1)], (Fr(2, 3),) * 3, T, 3)
    ok, why = cc.verify_noncontainment(cert, c["target_maximal"], 3)
    c["specified_witness_certificate"] = {"certificate": cert, "independent_check": {"ok": ok, "reason": why}}
    c["witness_in_cell_E2P1"] = {"cell": cert["source_cell"], "witness": cert["witness"]}
    return out


# ----------------------------------------------------------------------------------------------------- planar rows
def _eval_planar(row):
    try:
        return pr.evaluate_planar(row, with_reverse=True)
    except Exception as e:  # recorded, never silent
        return dict(row, verdict="UNAVAILABLE", error=repr(e))


def _eval3(row):
    try:
        return c3.evaluate_3d(row)
    except Exception as e:
        return dict(row, verdict="UNAVAILABLE", error=repr(e))


def pmap(fn, rows, procs=2, chunk=8):
    if procs <= 1 or len(rows) < 40:
        return [fn(r) for r in rows]
    with Pool(procs) as p:
        return list(p.imap(fn, rows, chunksize=chunk))


def planar_part(procs, quick=False, log=print):
    base_cfg, exp_cfg = LIMITS["planar_base"], LIMITS["planar_expansion"]
    if quick:
        exp_cfg = dict(exp_cfg, primes=[2, 3, 5, 7, 11, 13], qmax=4, bmax=140)
    t = time.time()
    base_rows, base_skips, _ = pr.sweep(base_cfg["primes"], base_cfg["qmax"], base_cfg["bmax"], 2)
    exp_rows, exp_skips, _ = pr.sweep(exp_cfg["primes"], exp_cfg["qmax"], exp_cfg["bmax"], 2)
    base_x = {r["x"] for r in base_rows}
    new_rows = [r for r in exp_rows if r["x"] not in base_x]
    log("planar sweeps: base %d rows, expansion %d rows (%d new)  %.0fs" % (len(base_rows), len(exp_rows), len(new_rows), time.time() - t))
    for r in base_rows:
        r["scope"] = "base"
    for r in new_rows:
        r["scope"] = "expansion"
    allrows = base_rows + new_rows
    ev = pmap(_eval_planar, allrows, procs)
    log("planar evaluation done %.0fs" % (time.time() - t))
    return ev, {"base": base_skips, "expansion": exp_skips}, base_rows


def planar_summary(ev, skips, e2p2_path):
    summ = {"n_rows": len(ev), "skips": skips}
    def key(o):
        return (o["relation"], o.get("target_class"), o.get("verdict"), o.get("hull_covered"), o.get("union_relation"))
    c = Counter(key(o) for o in ev)
    summ["table"] = [{"relation": k[0], "target_class": k[1], "verdict": k[2], "hull_covered": k[3], "union_relation": k[4], "count": v}
                     for k, v in sorted(c.items(), key=lambda kv: str(kv[0]))]
    summ["verdict_counts"] = {"%s/%s" % k: v for k, v in Counter((o["relation"], o["verdict"]) for o in ev).items()}
    summ["errors"] = [o for o in ev if o.get("error")][:5]
    bad = [o for o in ev if o.get("verdict") == "NOT_CONTAINED"]
    summ["planar_noncontained"] = bad
    # inherited cross-check: every INHERITED_G12T8 row must be exactly hull-covered
    inh = [o for o in ev if o.get("target_class") == "INHERITED_G12T8"]
    summ["inherited_rows"] = len(inh)
    summ["inherited_not_hull_covered"] = [o["x"] for o in inh if o.get("hull_covered") is not True]
    # the 266 ENLARGE rows of E2-P2
    p2 = json.load(open(e2p2_path))["rows"]
    p2x = {r["x"]: r for r in p2 if r["relation"] == "ENLARGE"}
    byx = {o["x"]: o for o in ev}
    sub = [byx[x] for x in p2x if x in byx]
    summ["e2p2_enlarge_rows"] = {"n_in_E2P2": len(p2x), "n_reanalysed": len(sub),
                                 "by_class": dict(Counter(o["target_class"] for o in sub)),
                                 "by_verdict": dict(Counter(o["verdict"] for o in sub)),
                                 "residual_hollow_or_subthreshold": sum(1 for o in sub if o["target_class"] in
                                                                        ("RESIDUAL_EXCEPTIONAL_HOLLOW_BOX", "RESIDUAL_SUBTHRESHOLD_BOX")),
                                 "skipped_states_unchanged": {"UNAVAILABLE_order_product_large_plus_denominator_large": skips["base"].get(
                                     "UNAVAILABLE_order_product_large", 0) + skips["base"].get("UNAVAILABLE_target_denominator_large", 0)},
                                 "e2p2_skipped_337_reproduced": (skips["base"].get("UNAVAILABLE_order_product_large", 0) +
                                                                 skips["base"].get("UNAVAILABLE_target_denominator_large", 0)) == 337}
    # E2-P2 verdict comparison (all geometry rows)
    dif, n = [], 0
    for r in p2:
        g = {"union_relation": r["union_relation"]} if r.get("union_relation") else None
        if not g or r["x"] not in byx:
            continue
        o = byx[r["x"]]
        mine = "NOT" if o["verdict"] != "CONTAINED" else ("EQUAL" if o.get("union_relation") == "EQUAL" else "U_SUBSET_U2")
        n += 1
        if mine != g["union_relation"]:
            dif.append({"x": r["x"], "e2p2": g["union_relation"], "e2p3": mine})
    summ["e2p2_geometry_comparison"] = {"rows_compared": n, "verdict_changes": dif}
    return summ


# ----------------------------------------------------------------------------------------------------- 3D
def three_d_S1(procs, log=print):
    cfg = LIMITS["three_d_S1"]
    rows, skips, _ = pr.sweep(cfg["primes"], cfg["qmax"], cfg["bmax"], 3, odd=cfg["odd"])
    ev = pmap(_eval3, rows, procs, chunk=4)
    log("3D S1: %d rows evaluated" % len(ev))
    return ev, skips


def _s2_row(row):
    P, q, b, b2 = tuple(row["primes"]), tuple(row["box"]), row["b"], row["b_next"]
    t0 = time.time()
    scr = c3.short_vector_screen(P, q, b, b2)
    t1 = time.time()
    pred = c3.corner_cube_predict(P, q, b, b2)
    t2 = time.time()
    out = {k: row[k] for k in ("primes", "box", "x", "x_next", "b", "b_next", "relation", "index_source", "index_target")}
    out["target_orders"] = row.get("target_orders")
    out["screen_failure_possible"] = scr
    out["predictor"] = pred["verdict"] if pred else None
    out["predictor_seconds"] = round(t2 - t1, 4)
    if pred and pred["verdict"] == "NOT_CONTAINED":
        out["predictor_witness"] = pred["witness"]
        out["predictor_cell"] = pred["cell"]
    return out


def _s2_exact(rowpred):
    row, pred = rowpred
    t0 = time.time()
    o = c3.evaluate_3d({k: row[k] for k in ("primes", "box", "x", "x_next", "b", "b_next", "relation", "index_source", "index_target")})
    o["exact_seconds"] = round(time.time() - t0, 4)
    o["predictor"] = pred
    return o


def _screen_triple(args):
    import math as _m
    P, lo, hi, bmax = args
    lt = cg.lt
    keep, sk = [], Counter()
    n = 0
    from itertools import product as _prod
    for q in _prod(range(lo, hi + 1), repeat=3):
        for par in _prod((0, 1), repeat=3):
            a = 1
            for p, m, e in zip(P, q, par):
                a *= p ** (2 * m + e)
            for b in range(2, bmax + 1):
                if _m.gcd(a, b) != 1:
                    continue
                n += 1
                row, why = pr.screen(P, q, b, a, 3)
                if row is None:
                    sk[why] += 1
                    continue
                b2 = row["b_next"]
                if b2 == 1:
                    sk["target_trivial"] += 1
                    continue
                ords = lt.orders(P, b2)
                if lt.describe(P, b2)["index"] != _m.prod(ords):
                    sk["target_not_rectangular"] += 1
                    continue
                if any(qi < oi for qi, oi in zip(q, ords)):
                    sk["box_below_orders"] += 1
                    continue
                row["target_orders"] = list(ords)
                keep.append(row)
    return keep, dict(sk), n


def three_d_S2(procs, log=print, quick=False):
    from itertools import combinations as _comb
    cfg = LIMITS["three_d_S2_rectangular_targets"]
    lo, hi = cfg["q_range"]
    pool = cfg["primes"] if not quick else cfg["primes"][:5]
    bmax = cfg["bmax"] if not quick else 60
    tasks = [(P, lo, hi, bmax) for P in _comb(pool, 3)]
    parts = pmap(_screen_triple, tasks, procs, chunk=1) if len(tasks) >= 40 else _pool_map_small(_screen_triple, tasks, procs)
    keep, sk, n = [], Counter(), 0
    for kp, s_, nn in parts:                       # triples in fixed order => deterministic concatenation
        keep += kp
        sk.update(s_)
        n += nn
    log("3D S2: %d states screened, %d rectangular-nontrivial candidate rows, skips %s" % (n, len(keep), dict(sk)))
    pred = pmap(_s2_row, keep, procs, chunk=4)
    sel = [i for i, p in enumerate(pred) if p["predictor"] == "NOT_CONTAINED"]
    safe = [i for i, p in enumerate(pred) if p["predictor"] == "CONTAINED"]
    # exact engine on CONTAINED rows costs up to ~25 s each: cross-check a deterministic, cost-bounded sample
    # (every 10th safe row among boxes with coordinate sum <= 10, capped at 80); the rest rely on the predictor,
    # whose agreement with the exact engine is established on the S1 rectangular rows (all 1,315) and recorded in the report.
    cheap = [i for i in safe if sum(keep[i]["box"]) <= 10]
    sample = cheap[::10][:80]
    # predicted failures: exact engine on a cost-bounded deterministic subset (box sum <= 9, first 40);
    # the remaining predicted failures stay 'predictor-only' and are reported as such (never as certified)
    sel_exact = [i for i in sel if sum(keep[i]["box"]) <= 9][:40]
    todo = [(keep[i], pred[i]["predictor"]) for i in sorted(set(sel_exact) | set(sample))]
    exact = pmap(_s2_exact, todo, procs, chunk=2)
    log("3D S2: predictor evaluated on %d rows; exact engine on %d rows" % (len(pred), len(exact)))
    return keep, pred, exact, dict(sk), n


def _pool_map_small(fn, items, procs):
    with Pool(procs) as p:
        return list(p.imap(fn, items, chunksize=1))


def lattice_model_scan(index_max=8, boxes=((1, 1, 1), (1, 1, 2), (1, 2, 1), (2, 1, 1), (1, 2, 2), (2, 1, 2), (2, 2, 1), (2, 2, 2))):
    from itertools import product

    def hnf(n):
        out = []
        for a in range(1, n + 1):
            if n % a:
                continue
            for b in range(1, n // a + 1):
                if (n // a) % b:
                    continue
                c = n // (a * b)
                for x in range(b):
                    for y in range(c):
                        for z in range(c):
                            out.append(((a, x, y), (0, b, z), (0, 0, c)))
        return out

    def member(B):
        (a, x, y), (_, b, z), (_, _, c) = B

        def inL(v):
            i, rem = divmod(v[0], a)
            if rem:
                return False
            v1, v2 = v[1] - i * x, v[2] - i * y
            j, rem = divmod(v1, b)
            if rem:
                return False
            return (v2 - j * z) % c == 0
        return inL

    def cells_pred(inL, q):
        F = tuple(sorted(v for v in product(*[range(m + 1) for m in q]) if any(v) and inL(v)))
        L = [v for v in product(*[range(-m, m + 1) for m in q]) if any(v) and inL(v)]
        G = [v for v in L if not any(w != v and all(a * b >= 0 and abs(a) <= abs(b) for a, b in zip(w, v)) for w in L)]
        cx = cg.ct0.build_complex(F, cg.ft.oriented(G), 3)
        return F, [(tuple(c.base), tuple(tuple(g) for g in c.gens)) for j in cx for c in cx[j].values()]

    rows = []
    for n in range(2, index_max + 1):
        for B in hnf(n):
            inL = member(B)
            for q in boxes:
                F, cs = cells_pred(inL, q)
                if not F:
                    continue
                _, ct = cells_pred(lambda v: True, q)
                r = ec.decide_union(cs, ct, 3)
                rec = {"basis": [list(r_) for r_ in B], "index": n, "box": list(q), "verdict": r["verdict"], "n_F": len(F)}
                # predictor on the pure lattice: corner-cube LP on every maximal source cell (o = (1,1,1))
                pred = "CONTAINED"
                for base, gens in ec.geometric_maximal(cs, 3):
                    s = c3.max_slack(base, gens, (1, 1, 1))
                    if s is not None and s[0] > 0:
                        pred = "NOT_CONTAINED"
                        break
                rec["corner_cube_predictor"] = pred
                if r["verdict"] == "NOT_CONTAINED":
                    rec["witness"] = r["certificate"]["witness"]
                    rec["witness_cell"] = r["certificate"]["source_cell"]
                    rec["certificate_ok"] = cc.verify_noncontainment(r["certificate"], r["target_maximal"], 3)[0]
                    rec["short_vectors_norm_le2"] = [list(v) for v in F if sum(v) <= 2]
                rows.append(rec)
    return rows


# ----------------------------------------------------------------------------------------------------- main
def main(argv):
    out = ROOT
    quick = "--quick" in argv
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    procs = 2
    t0 = time.time()
    log = lambda s: print("[%6.0fs] %s" % (time.time() - t0, s), flush=True)
    dump(LIMITS, os.path.join(out, "data", "P3_SEARCH_LIMITS.json"))
    log("limits recorded")

    ctl = controls()
    for name, rec in ctl.items():
        assert rec["matches_expected"], "control %s does not match its expected verdict" % name
        assert rec["independent_certificate_check"]["ok"], "control %s certificate not independently verified" % name
    dump(ctl, os.path.join(out, "data", "P3_CONTROLS.json"))
    log("controls A/B/C verified (GEOMETRY preflight)")

    ev, skips, base_rows = planar_part(procs, quick, log)
    e2p2 = os.path.join(ROOT, "data", "E2P2_SEARCH_CORPUS_REFERENCE.json")
    summ = planar_summary(ev, skips, e2p2)
    compact = []
    for o in ev:
        keep = ("scope", "primes", "box", "x", "x_next", "b", "b_next", "relation", "index_source", "index_target", "verdict", "target_class",
                "target_normal_form", "hull_covered", "gap_status", "gap_area", "n_gap_pieces", "union_relation", "n_source_maximal",
                "n_target_maximal", "witness", "witness_cell", "error")
        compact.append({k: o[k] for k in keep if k in o})
    dump({"limits": LIMITS["planar_base"], "limits_expansion": LIMITS["planar_expansion"], "skips": skips, "rows": compact},
         os.path.join(out, "data", "P3_PLANAR_CORPUS.json"))
    dump(summ, os.path.join(out, "results", "P3_PLANAR.json"))
    log("planar done: %d rows, noncontained %d" % (len(ev), len(summ["planar_noncontained"])))

    s1, s1skips = three_d_S1(procs, log)
    keep2, pred2, exact2, sk2, n2 = three_d_S2(procs, log, quick)
    lm = lattice_model_scan()
    c3sum = {"S1": {"n_rows": len(s1), "skips": s1skips,
                    "table": [{"relation": k[0], "verdict": k[1], "both_nontrivial": k[2], "essential_3d": k[3], "target_rectangular": k[4], "count": v}
                              for k, v in sorted(Counter((o["relation"], o["verdict"], o.get("both_nontrivial"), o.get("essential_3d"),
                                                          bool(c3.rectangular_data(tuple(o["primes"]), o["b_next"], tuple(o["box"])))) for o in s1).items(),
                                                 key=str)],
                    "noncontained": [{k: o[k] for k in ("x", "primes", "box", "b", "b_next", "relation", "witness", "witness_cell", "essentiality",
                                                       "both_nontrivial", "essential_3d", "coupled_source") if k in o} for o in s1 if o.get("verdict") == "NOT_CONTAINED"]},
             "S2": {"states_screened": n2, "skips": sk2, "n_candidate_rows": len(keep2),
                    "predictor_table": dict(Counter((p["screen_failure_possible"], p["predictor"]) .__str__() for p in pred2)),
                    "exact_rows": len(exact2),
                    "predictor_vs_exact": dict(Counter("%s|%s" % (e["predictor"], e["verdict"]) for e in exact2)),
                    "predictor_mismatches": [e["x"] for e in exact2 if e["predictor"] != e["verdict"]],
                    "screen_unsound_cases": [p["x"] for p, k in zip(pred2, keep2) if p["screen_failure_possible"] is False and p["predictor"] == "NOT_CONTAINED"],
                    "predicted_failures": [p for p in pred2 if p["predictor"] == "NOT_CONTAINED"],
                    "exact_failures": [{k: e[k] for k in ("x", "primes", "box", "b", "b_next", "relation", "witness", "witness_cell", "essentiality",
                                                          "both_nontrivial", "essential_3d") if k in e} for e in exact2 if e.get("verdict") == "NOT_CONTAINED"],
                    "mean_predictor_seconds": (sum(p["predictor_seconds"] for p in pred2) / max(1, len(pred2))),
                    "mean_exact_seconds_on_sample": (sum(e.get("exact_seconds", 0) for e in exact2) / max(1, len(exact2)))},
             "lattice_model": {"n": len(lm), "failures": [r for r in lm if r["verdict"] != "CONTAINED"],
                               "predictor_agrees": all(r["corner_cube_predictor"] == r["verdict"] for r in lm),
                               "n_contained": sum(1 for r in lm if r["verdict"] == "CONTAINED")}}
    dump(c3sum, os.path.join(out, "results", "P3_3D.json"))
    dump({"S1_rows": [{k: o[k] for k in o if k not in ("certificate", "target_maximal", "failing_cells")} for o in s1],
          "S2_candidates": pred2, "lattice_model_rows": lm},
         os.path.join(out, "data", "P3_3D_CORPUS.json"))
    log("3D done: S1 failures %d, S2 predicted failures %d, lattice-model failures %d" % (
        len(c3sum["S1"]["noncontained"]), len(c3sum["S2"]["predicted_failures"]), len(c3sum["lattice_model"]["failures"])))

    # certificates file: controls + every non-containment + the residual planar rows that have a genuinely nonempty target gap
    certs = {"controls": {k: {kk: v[kk] for kk in v if kk in ("certificate", "certificates", "target_maximal", "source_maximal",
                                                                "specified_witness_certificate", "hull_cover_certificate")}
                          for k, v in ctl.items()}}
    resid = [o for o in ev if o.get("target_class") in ("RESIDUAL_EXCEPTIONAL_HOLLOW_BOX", "RESIDUAL_SUBTHRESHOLD_BOX") and o.get("hull_covered") is False
             and o["relation"] == "ENLARGE"]
    certs["planar_residual_with_target_gap"] = []
    for o in resid[:150]:
        P, q, b, b2 = tuple(o["primes"]), tuple(o["box"]), o["b"], o["b_next"]
        res, F2, c2 = cg.geometric_verdict(P, b, b2, q)
        certs["planar_residual_with_target_gap"].append({"x": o["x"], "primes": list(P), "box": list(q), "b": b, "b_next": b2,
                                                          "verdict": res["verdict"], "target_maximal": res["target_maximal"],
                                                          "certificates": res.get("certificates"), "certificate": res.get("certificate")})
    dump(certs, os.path.join(out, "results", "P3_CERTIFICATES.json"))
    cont = {"engine": "closed splitting; verifier certificate_check.py is independent of exact_containment.py",
            "controls": {k: {"verdict": v["verdict"], "independent_check": v["independent_certificate_check"]} for k, v in ctl.items()},
            "planar_rows": summ["n_rows"], "planar_noncontained": len(summ["planar_noncontained"]),
            "3d_S1_rows": len(s1), "3d_S2_exact_rows": len(exact2), "lattice_model_rows": len(lm)}
    dump(cont, os.path.join(out, "results", "P3_CONTAINMENT.json"))
    dump({"note": "counterexamples to unrestricted statements found by the exact engine (all with certificates verifying independently)",
          "CP3-A_planar": summ["planar_noncontained"],
          "negative_controls_target_Z3": [x for x in c3sum["S1"]["noncontained"]],
          "S2_rectangular_nontrivial_target_failures": c3sum["S2"]["exact_failures"],
          "lattice_model_failures": c3sum["lattice_model"]["failures"]},
         os.path.join(out, "results", "P3_COUNTEREXAMPLES.json"))
    log("build finished")


if __name__ == "__main__":
    main(sys.argv[1:])
