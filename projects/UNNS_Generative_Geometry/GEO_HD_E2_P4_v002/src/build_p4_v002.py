#!/usr/bin/env python3
"""E2-P4 v002 builder (P4-E3 planar, P4-E4 spatial, zero-vertex screen P4-Z1).
Usage: python src/build_p4_v002.py --stage NAME [--out DIR] [--procs N] [--force] [--quick]
Stages (each writes one immutable file; skipped if present unless --force):
  limits  c1check  planar_lattice  planar_core  planar_window  lattice3  fieldI3"""
import json
import math
import os
import sys
import time
from collections import Counter
from fractions import Fraction as Fr
from itertools import product
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _boot  # noqa: E402

lm = _boot.p4("lattice_model")
zv = _boot.p4("zero_vertex")
cl = _boot.p4("coupled_lattices")
import coverage_gap as cg  # noqa: E402
import exact_containment as ec  # noqa: E402
import planar_residual as pr  # noqa: E402  (engine version)
import coupled_3d as c3  # noqa: E402  (engine version)
import certificate_check as cc  # noqa: E402

OUT = os.path.dirname(HERE)
ARGV = sys.argv
if "--out" in ARGV:
    OUT = ARGV[ARGV.index("--out") + 1]
PROCS = int(ARGV[ARGV.index("--procs") + 1]) if "--procs" in ARGV else 2
FORCE = "--force" in ARGV
QUICK = "--quick" in ARGV
STAGES = []
if "--stage" in ARGV:
    i = ARGV.index("--stage") + 1
    while i < len(ARGV) and not ARGV[i].startswith("--"):
        STAGES.append(ARGV[i])
        i += 1
T0 = time.time()
lt, ft = cg.lt, cg.ft

LIMITS = {
    "planar_lattice": {"max_index_of_source": 24, "pairs": "all sublattice pairs L < L' of Z^2 with [Z^2:L] <= 24 (HNF enumeration)", "boxes": "all (Q1,Q2) in [1,6]^2"},
    "planar_core": "all 846 ENLARGE rows of the two open planar classes in the E2-P3 corpus (reference file), ZV statistics",
    "planar_window": {"primes": "<= 41 (13 primes)", "box": "[1,7]^2", "q_max": 7, "old_q_max": 6, "old_b_max": 400, "b_max": 4000,
                      "b": "401..4000 for boxes with max <= 6; 2..4000 for boxes containing a 7 (E2-P3 expansion covered q <= 6, b <= 400)",
                      "odd_exponents": False, "classes_evaluated": ["RESIDUAL_EXCEPTIONAL_HOLLOW_BOX", "RESIDUAL_SUBTHRESHOLD_BOX"],
                      "geometry_node_limit": 20000},
    "lattice3": {"targets": "nonrectangular lattices L' of Z^3 with index 2..6 (HNF)", "sources": "L < L', [Z^3:L] <= 12",
                 "boxes": "{1,2}^3 and (2,2,3),(2,3,2),(3,2,2)", "exact_engine_on": "every ZV-flagged pair/box (node_limit 100000) + every 6th ZV-free pair/box with box sum <= 5 (validation sample)"},
    "fieldI3": {"pool": [2, 3, 5, 7, 11, 13], "q_max": 3, "b_max": 100, "odd_exponents": True, "target_filter": "nonrectangular target relation lattice",
                "exact_engine_on": "every ZV-flagged row with box sum <= 8 (node_limit 60000) + every 25th ZV-free row with box sum <= 6 (validation)"},
}


def log(m):
    print("[%6.0fs] %s" % (time.time() - T0, m), flush=True)


def dump(obj, rel):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True, default=str)


def exists(rel):
    return os.path.exists(os.path.join(OUT, rel)) and not FORCE


def load(rel):
    return json.load(open(os.path.join(OUT, rel), encoding="utf-8"))


def pmap(fn, items, chunk=1):
    if PROCS <= 1 or len(items) < 4:
        return [fn(i) for i in items]
    with Pool(PROCS) as p:
        return list(p.imap(fn, items, chunksize=chunk))


# ------------------------------------------------------------------------------------------------ c1check
def st_c1check():
    if exists("data/P4_C1_CORRECTION.json"):
        return log("c1check exists")
    inS = lambda v: all(x % 2 == 0 for x in v)  # noqa: E731
    inE = lambda v: sum(v) % 2 == 0  # noqa: E731
    q = (4, 4, 4)
    F, cs = lm.cells_of_member(inS, q)
    F2, ct = lm.cells_of_member(inE, q)
    tg = _boot.p4("target_gap")
    ok, verts = tg.hull_check_e3(4)
    Fs = set(F)
    ten_in = all(tuple(int(x) for x in v) in Fs for v in verts)
    r_rev = ec.decide_union(ct, cs, 3, 200000)
    r_fwd = ec.decide_union(cs, ct, 3, 200000)
    # explicit statement of the withdrawn clause's failure: U(2Z^3)={max>=2}; (1,1,1) in H, in U(E3), not in U(2Z3)
    Smax = ec.geometric_maximal(cs, 3)
    pt = tuple(Fr(1) for _ in range(3))
    in_src = any(ec.in_cell(b, g, pt) for b, g in Smax)
    Tmax = ec.geometric_maximal(ct, 3)
    in_tgt = any(ec.in_cell(b, g, pt) for b, g in Tmax)
    dump({"lattice": "2Z^3 inside E_3", "box": list(q), "n_F_source": len(F), "ten_hull_vertices_in_F_source": ten_in,
          "U_source_contained_in_U_E3": r_fwd["verdict"], "U_E3_contained_in_U_source": r_rev["verdict"],
          "witness_E3_not_in_source": r_rev.get("certificate", {}).get("witness"),
          "point_1_1_1": {"in_U_E3": in_tgt, "in_U_source": in_src},
          "source_U_equals_box_minus_origin_cube_checked_on": "all 117 source cells have a vertex with max coordinate >= 2 (see audit)",
          "all_source_cells_have_max_coord_ge_2": all(max(max(v) for v in [tuple(c) for c in _verts(b, g)]) >= 2 for b, g in Smax)},
         "data/P4_C1_CORRECTION.json")
    log("c1 correction record: ten vertices in F(2Z^3) = %s; U(E3) in U(2Z3) = %s; (1,1,1) in U(E3)=%s, in U(2Z3)=%s" % (ten_in, r_rev["verdict"], in_tgt, in_src))


def _verts(base, gens):
    out = []
    for bits in product((0, 1), repeat=len(gens)):
        v = list(base)
        for bit, g in zip(bits, gens):
            if bit:
                v = [a + b for a, b in zip(v, g)]
        out.append(tuple(v))
    return out


# ------------------------------------------------------------------------------------------------ planar lattice scan
def _planar_pair(args):
    B, Bp, boxes = args
    inL, outL = lm.member2(B), lm.member2(Bp)
    rows = []
    for q in boxes:
        F, cs = lm.cells_of_member(inL, q)
        if not F:
            continue
        F2, ct = lm.cells_of_member(outL, q)
        Smax = ec.geometric_maximal(cs, 2)
        n, fl = zv.screen_cells(Smax, outL)
        r = ec.decide_union(cs, ct, 2, 100000)
        rec = {"q": list(q), "verdict": r["verdict"], "n_src_max": n, "n_zv": len(fl)}
        if r["verdict"] != "CONTAINED":
            rec["witness"] = r["certificate"]["witness"]
            rec["cell"] = r["certificate"]["source_cell"]
            rec["cert_ok"] = cc.verify_noncontainment(r["certificate"], r["target_maximal"], 2)[0]
        if fl and len(rows) < 1000:
            rec["zv_example"] = fl[0]
        rows.append(rec)
    return {"B": B, "Bp": Bp, "rows": rows}


def st_planar_lattice():
    rel = "results/P4_PLANAR_LATTICE.json"
    if exists(rel):
        return log("planar_lattice exists")
    nmax = 8 if QUICK else 24
    hi = 4 if QUICK else 6
    lats = [(n, B) for n in range(1, nmax + 1) for B in lm.hnf2(n)]
    pairs = []
    for n, B in lats:
        for n2, Bp in lats:
            if n2 < n and n % n2 == 0 and all(lm.member2(Bp)(r) for r in B):
                pairs.append((B, Bp))
    boxes = [q for q in product(range(1, hi + 1), repeat=2)]
    log("planar lattice scan: %d pairs x %d boxes" % (len(pairs), len(boxes)))
    res = pmap(_planar_pair, [(B, Bp, boxes) for B, Bp in pairs], chunk=4)
    runs = [r for x in res for r in x["rows"]]
    verd = Counter(r["verdict"] for r in runs)
    zvc = Counter((r["n_zv"] > 0, r["verdict"]) for r in runs)
    failures = []
    for x in res:
        for r in x["rows"]:
            if r["verdict"] != "CONTAINED":
                failures.append({"B": x["B"], "Bp": x["Bp"], **r})
    ex = []
    for x in res:
        for r in x["rows"]:
            if r.get("zv_example") and len(ex) < 8 and r["n_zv"] > 0:
                ex.append({"B": x["B"], "Bp": x["Bp"], "q": r["q"], "zv_cell": r["zv_example"]})
    dump({"limits": LIMITS["planar_lattice"] if not QUICK else "QUICK", "n_pairs": len(pairs), "n_runs": len(runs), "verdicts": dict(verd),
          "zv_vs_verdict": {"%s|%s" % k: v for k, v in zvc.items()}, "failures": failures, "zv_flagged_contained_examples": ex,
          "n_runs_with_zero_vertex_cell": sum(1 for r in runs if r["n_zv"] > 0), "n_runs_total": len(runs)}, rel)
    log("planar lattice scan done: verdicts %s; zv-flagged runs %d of %d; failures %d" % (dict(verd), sum(1 for r in runs if r["n_zv"] > 0), len(runs), len(failures)))


# ------------------------------------------------------------------------------------------------ planar core (FIELD-I rows from E2-P3 corpus)
def _zv_row(args):
    P, b, b2, q = args
    F, G, cells = cg.cells_of(P, b, q)
    Smax = ec.geometric_maximal(cells, len(q))
    n, fl = zv.screen_cells(Smax, lambda v: lt.in_lambda(v, P, b2))
    return n, fl


def st_planar_core():
    rel = "results/P4_PLANAR_CORE.json"
    if exists(rel):
        return log("planar_core exists")
    ref = json.load(open(os.path.join(OUT, "data", "E2P3_PLANAR_REFERENCE.json")))
    rows = ref["residual_open"]["rows"]
    res = pmap(_zv_row, [(tuple(r["primes"]), r["b"], r["b_next"], tuple(r["box"])) for r in rows], chunk=8)
    tab = Counter()
    out_rows = []
    for r, (n, fl) in zip(rows, res):
        key = (r["target_class"], "hull_covered" if r["hull_covered"] else "hollow", "ZV" if fl else "noZV")
        tab[key] += 1
        out_rows.append({"x": r["x"], "x_next": r["x_next"], "primes": r["primes"], "box": r["box"], "b": r["b"], "b_next": r["b_next"],
                         "target_class": r["target_class"], "hull_covered": r["hull_covered"], "verdict": r["verdict"], "n_src_max": n, "n_zv": len(fl),
                         "zv_example": fl[0] if fl else None})
    summary = {"n_rows": len(rows), "table": {"|".join(k): v for k, v in sorted(tab.items())},
               "proved_by_hull_cover": sum(v for k, v in tab.items() if k[1] == "hull_covered"),
               "core_hollow_rows": sum(v for k, v in tab.items() if k[1] == "hollow"),
               "core_hollow_proved_by_P4Z1": sum(v for k, v in tab.items() if k[1] == "hollow" and k[2] == "noZV"),
               "core_hollow_needing_geometry": sum(v for k, v in tab.items() if k[1] == "hollow" and k[2] == "ZV")}
    dump({"summary": summary, "rows": out_rows}, rel)
    log("planar core: %s" % summary)


# ------------------------------------------------------------------------------------------------ planar window (new FIELD-I states)
def _planar_task(args):
    P, q, blo, bhi = args
    out, skips, cls = [], Counter(), Counter()
    a = 1
    for p, m in zip(P, q):
        a *= p ** (2 * m)
    for b in range(blo, bhi + 1):
        if math.gcd(a, b) != 1:
            continue
        row, why = pr.screen(P, q, b, a, 2)
        if row is None:
            skips[why] += 1
            continue
        b2 = row["b_next"]
        if b2 == 1:
            skips["target_trivial"] += 1
            continue
        c = cg.classify_target_planar(P, b2, q)
        cls[(row["relation"], c["class"])] += 1
        if c["class"] not in ("RESIDUAL_EXCEPTIONAL_HOLLOW_BOX", "RESIDUAL_SUBTHRESHOLD_BOX"):
            continue
        n, fl = _zv_row((P, b, b2, q))
        rec = {k: row[k] for k in ("primes", "box", "x", "x_next", "b", "b_next", "relation", "index_source", "index_target")}
        rec["target_class"] = c["class"]
        rec["n_src_max"], rec["n_zv"] = n, len(fl)
        try:
            ev = pr.evaluate_planar(row, with_reverse=False, node_limit=LIMITS["planar_window"]["geometry_node_limit"], gap=True)
            rec["verdict"] = ev["verdict"]
            rec["hull_covered"] = ev.get("hull_covered")
            if ev["verdict"] != "CONTAINED":
                rec["witness"], rec["witness_cell"] = ev.get("witness"), ev.get("witness_cell")
        except ec.Exhausted as e:
            rec["verdict"] = "UNAVAILABLE"
            rec["reason"] = str(e)[:80]
        out.append(rec)
    return out, dict(skips), {"%s|%s" % k: v for k, v in cls.items()}


def st_planar_window():
    rel = "results/P4_PLANAR_WINDOW.json"
    if exists(rel):
        return log("planar_window exists")
    W = LIMITS["planar_window"]
    pool = [p for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)]
    if QUICK:
        pool = pool[:5]
    tasks = []
    for P in __import__("itertools").combinations(pool, 2):
        for q in product(range(1, W["q_max"] + 1), repeat=2):
            lo = 2 if max(q) > W["old_q_max"] else W["old_b_max"] + 1     # states outside the E2-P3 expansion window
            tasks.append((P, q, lo, W["b_max"] if not QUICK else lo + 30))
    log("planar window: %d (P,q) tasks" % len(tasks))
    res = pmap(_planar_task, tasks, chunk=4)
    rows = [r for x in res for r in x[0]]
    skips, cls = Counter(), Counter()
    for _, s, c in res:
        skips.update(s)
        for k, v in c.items():
            cls[k] += v
    verd = Counter((r["relation"], r["verdict"]) for r in rows)
    fails = [r for r in rows if r["verdict"] not in ("CONTAINED", "UNAVAILABLE")]
    dump({"limits": W, "n_tasks": len(tasks), "skips": dict(skips), "class_counts": dict(cls),
          "n_residual_rows_evaluated": len(rows), "verdicts": {"%s|%s" % k: v for k, v in verd.items()},
          "n_zv_flagged_rows": sum(1 for r in rows if r["n_zv"] > 0),
          "n_hollow_rows": sum(1 for r in rows if r.get("hull_covered") is False),
          "n_hollow_noZV": sum(1 for r in rows if r.get("hull_covered") is False and r["n_zv"] == 0),
          "noncontained": fails, "rows": rows}, rel)
    log("planar window: %d residual rows; verdicts %s; noncontained %d" % (len(rows), dict(verd), len(fails)))


# ------------------------------------------------------------------------------------------------ 3D lattice-level (nonrectangular targets)
def _orders3(B):
    f = lm.member3(B)
    res = []
    for i in range(3):
        k = 1
        while True:
            v = [0, 0, 0]
            v[i] = k
            if f(tuple(v)):
                res.append(k)
                break
            k += 1
    return res


def _lat3_pair(args):
    B, Bp, boxes, idx = args
    inL, outL = lm.member3(B), lm.member3(Bp)
    rows = []
    for j, q in enumerate(boxes):
        F, cs = lm.cells_of_member(inL, q)
        if not F:
            continue
        Smax = ec.geometric_maximal(cs, 3)
        n, fl = zv.screen_cells(Smax, outL)
        do_exact = bool(fl) or (idx % 6 == 0 and sum(q) <= 5)
        rec = {"q": list(q), "n_src_max": n, "n_zv": len(fl)}
        if do_exact:
            F2, ct = lm.cells_of_member(outL, q)
            r = ec.decide_union(cs, ct, 3, 100000)
            rec["verdict"] = r["verdict"]
            if r["verdict"] == "NOT_CONTAINED":
                rec["witness"], rec["cell"] = r["certificate"]["witness"], r["certificate"]["source_cell"]
                rec["cert_ok"] = cc.verify_noncontainment(r["certificate"], r["target_maximal"], 3)[0]
                rec["n_target_F"] = len(F2)
        else:
            rec["verdict"] = "PROVED_BY_P4Z1"
        if fl:
            rec["zv_example"] = fl[0]
        rows.append(rec)
    return {"B": B, "Bp": Bp, "rows": rows}


def st_lattice3():
    rel = "results/P4_LATTICE3.json"
    if exists(rel):
        return log("lattice3 exists")
    lat = {n: lm.hnf3(n) for n in range(1, 13)}
    top = 4 if QUICK else 6
    nr = [(n, B) for n in range(2, top + 1) for B in lat[n] if math.prod(_orders3(B)) != n]
    boxes = [q for q in product((1, 2), repeat=3)] + [(2, 2, 3), (2, 3, 2), (3, 2, 2)]
    tasks, idx = [], 0
    for n2, Bp in nr:
        fp = lm.member3(Bp)
        for n in range(2 * n2, (8 if QUICK else 12) + 1, n2):
            for B in lat[n]:
                if all(fp(r) for r in B):
                    tasks.append((B, Bp, boxes, idx))
                    idx += 1
    log("lattice3: %d nonrectangular targets, %d pairs x %d boxes" % (len(nr), len(tasks), len(boxes)))
    res = pmap(_lat3_pair, tasks, chunk=4)
    runs = [(x, r) for x in res for r in x["rows"]]
    verd = Counter(r["verdict"] for _, r in runs)
    exact = [(x, r) for x, r in runs if r["verdict"] in ("CONTAINED", "NOT_CONTAINED")]
    zvc = Counter((r["n_zv"] > 0, r["verdict"]) for _, r in runs)
    fails = [{"B": x["B"], "Bp": x["Bp"], **r} for x, r in runs if r["verdict"] == "NOT_CONTAINED"]
    unsound = [f for f in fails if f["n_zv"] == 0]
    dump({"limits": LIMITS["lattice3"], "n_targets_nonrect": len(nr), "n_pairs": len(tasks), "n_runs": len(runs), "verdicts": dict(verd),
          "zv_vs_verdict": {"%s|%s" % k: v for k, v in zvc.items()}, "failures": fails, "n_failures": len(fails),
          "p4z1_violations": unsound, "n_exact_runs": len(exact), "n_runs_zv_flagged": sum(1 for _, r in runs if r["n_zv"] > 0)}, rel)
    log("lattice3 done: %s; failures %d; P4-Z1 violations %d" % (dict(verd), len(fails), len(unsound)))


# ------------------------------------------------------------------------------------------------ FIELD-I spatial window
def _chunk3(states):
    out, skips, cls = [], Counter(), Counter()
    for P, q, b, a in states:
        row, why = pr.screen(P, q, b, a, 3)
        if row is None:
            skips[why] += 1
            continue
        b2 = row["b_next"]
        if b2 == 1:
            skips["target_trivial"] += 1
            continue
        d2 = cl.describe(P, b2) if False else None
        ords = lt.orders(P, b2)
        nonrect = lt.describe(P, b2)["index"] < math.prod(ords)
        srcnr = lt.describe(P, b)["index"] < math.prod(lt.orders(P, b))
        cls[(row["relation"], "target_nonrect" if nonrect else "target_rect", "src_nonrect" if srcnr else "src_rect")] += 1
        if not nonrect:
            continue
        n, fl = _zv_row((P, b, b2, q))
        rec = {k: row[k] for k in ("primes", "box", "x", "x_next", "b", "b_next", "relation", "index_source", "index_target")}
        rec["source_nonrect"] = srcnr
        rec["n_src_max"], rec["n_zv"] = n, len(fl)
        do_exact = (fl and sum(q) <= 8) or (not fl and sum(q) <= 6 and (hash((P, q, b)) % 25 == 0))
        if do_exact:
            try:
                ev = c3.evaluate_3d(row, node_limit=60000)
                rec["verdict"] = ev["verdict"]
                if ev["verdict"] == "NOT_CONTAINED":
                    rec["witness"], rec["witness_cell"], rec["essentiality"] = ev["witness"], ev["witness_cell"], ev.get("essentiality")
                    rec["essential_3d"] = ev.get("essential_3d")
            except Exception as e:  # noqa: BLE001
                rec["verdict"] = "UNAVAILABLE"
                rec["reason"] = repr(e)[:80]
        else:
            rec["verdict"] = "PROVED_BY_P4Z1" if not fl else "UNAVAILABLE_COST"
        if fl:
            rec["zv_example"] = fl[0]
        out.append(rec)
    return out, dict(skips), {"%s|%s|%s" % k: v for k, v in cls.items()}


def st_fieldI3():
    rel = "results/P4_FIELDI3.json"
    if exists(rel):
        return log("fieldI3 exists")
    cfg = LIMITS["fieldI3"]
    pool = cfg["pool"][:4] if QUICK else cfg["pool"]
    qmax, bmax = (2, 40) if QUICK else (cfg["q_max"], cfg["b_max"])
    allst = list(pr.states(pool, qmax, bmax, 3, odd=True))
    log("fieldI3: %d states" % len(allst))
    chunks = [allst[i:i + 3000] for i in range(0, len(allst), 3000)]
    res = pmap(_chunk3, chunks, chunk=1)
    rows = [r for x in res for r in x[0]]
    skips, cls = Counter(), Counter()
    for _, s, c in res:
        skips.update(s)
        for k, v in c.items():
            cls[k] += v
    verd = Counter((r["relation"], r["verdict"]) for r in rows)
    fails = [r for r in rows if r["verdict"] == "NOT_CONTAINED"]
    dump({"limits": cfg if not QUICK else "QUICK", "n_states": len(allst), "skips": dict(skips), "class_counts": dict(cls), "n_nonrect_target_rows": len(rows),
          "verdicts": {"%s|%s" % k: v for k, v in verd.items()}, "noncontained": fails,
          "n_zv_flagged": sum(1 for r in rows if r["n_zv"] > 0), "n_zv_free": sum(1 for r in rows if r["n_zv"] == 0),
          "n_both_nonrect": sum(1 for r in rows if r["source_nonrect"]), "rows": rows}, rel)
    log("fieldI3 done: %d nonrect-target rows; verdicts %s; noncontained %d" % (len(rows), dict(verd), len(fails)))


STAGE_FN = {"c1check": st_c1check, "planar_lattice": st_planar_lattice, "planar_core": st_planar_core, "planar_window": st_planar_window,
            "lattice3": st_lattice3, "fieldI3": st_fieldI3}

if __name__ == "__main__":
    dump(LIMITS, "data/SEARCH_LIMITS_V002.json")
    for s in STAGES:
        STAGE_FN[s]()
    log("finished: %s" % STAGES)
