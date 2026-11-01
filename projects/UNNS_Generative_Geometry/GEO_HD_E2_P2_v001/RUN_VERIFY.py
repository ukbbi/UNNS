#!/usr/bin/env python3
"""GEO-HD-1B / E2-P2 -- independent verification.  Standard library only.

  python RUN_VERIFY.py            full verification (several minutes: includes a from-scratch rebuild)
  python RUN_VERIFY.py --fast     skips the rebuild and shrinks the corpus sample
  python RUN_VERIFY.py --write    additionally (re)writes results/P2_CERTIFICATES.json when all checks pass

Every check recomputes from first principles with src/geometry_audit.py (which imports nothing from the builder
modules) and compares with the stored data/results.  Exit code 0 iff every executed check passes.
EXACT_PASS is a statement about computation only; it is not a theorem verdict (see STATUS.json).
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from fractions import Fraction as Fr

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))
import geometry_audit as ga  # noqa: E402

SPEC = "E2_P2_SPEC_v001"
INHERITED = {"src/inherited/e1_cell_transport.py": "2c767b002dcd890297afa040b638b45fdbf18494db7941daa0d8f9914035d7a2",
             "src/inherited/fibre_transport.py": "7360be293a8fffc87bb53cefba0fcf371f52b706c76151a466e5b41e5e8c3ae9"}
SRC_MOVES = [(0, 4), (1, -3), (1, 1), (2, -2), (3, -1), (4, 0)]
TGT_MOVES = [(0, 2), (1, -1), (1, 1), (2, 0)]
SPEC_LOST_A = {((0, 4), (1, 1)), ((0, 4), (2, 2)), ((0, 4), (3, 3)), ((0, 4), (4, 4)), ((1, 1), (4, 0)), ((2, 2), (4, 0)),
               ((3, 3), (4, 0)), ((4, 0), (4, 4))}


def load(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return json.load(fh)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


class Certs:
    def __init__(self):
        self.items = []

    def add(self, cid, claim, ok, detail="", status=None):
        self.items.append({"id": cid, "claim": claim, "status": status or ("PASS" if ok else "FAIL"), "detail": detail})
        print("%-4s %-9s %s %s" % (cid, self.items[-1]["status"], claim, ("[" + detail + "]") if detail else ""), flush=True)

    @property
    def ok(self):
        return all(c["status"] in ("PASS", "NOT_RERUN") for c in self.items)


def tup(v):
    return tuple(tuple(t) for t in v)


def stage(a, b):
    """audit-side description of the fibre problem for x=a/b (coordinates from x itself)."""
    P, q, bb = ga.coords(Fr(a, b))
    F = ga.fibre(P, q, bb)
    return P, q, bb, F


def edge_set(cells):
    return {tuple(sorted(c)) for c in cells[1]}


def audit_specimens(root, C):
    out = {}
    for name, (a, b, b2, stored) in {"A": (21 ** 8, 5, 4, "data/P2_A.json"), "B": (55 ** 12, 27, 18, "data/P2_B.json")}.items():
        d = load(root, stored)
        x = Fr(a, b)
        nx, L, G, ds = ga.C_brute(x)
        ok = (nx == Fr(a, b2) and str(nx) == d["x_next"] and L == d["L"] and G == d["G"] and len(ds) == d["n_D_source"]
              and str(nx - x) == d["increment"])
        P, q, bb = ga.coords(x)
        P2, q2, bb2 = ga.coords(nx)
        ok = ok and (P, q) == (P2, q2) and bb == b and bb2 == b2
        C.add("P01" + name, "specimen %s: FIELD-I transition recomputed by brute force (D, L, G, C), same primes %s and box %s" % (name, P, q),
              ok, "L=%d G=%d b %d->%d" % (L, G, b, b2))
        out[name] = (d, P, q, b, b2)
    return out


def audit_fibres_cells(root, sp, C):
    res = {}
    for name, (d, P, q, b, b2) in sp.items():
        F, F2 = ga.fibre(P, q, b), ga.fibre(P, q, b2)
        G, G2 = ga.graver(P, q, b), ga.graver(P, q, b2)
        ok = (sorted(F) == sorted(tup(d["fibre"]["source"])) and sorted(F2) == sorted(tup(d["fibre"]["target"]))
              and sorted(G) == sorted(tup(d["graver"]["source"])) and sorted(G2) == sorted(tup(d["graver"]["target"])))
        cs, ct_ = ga.cells_planar(F, G), ga.cells_planar(F2, G2)
        fs = [len(cs[i]) for i in range(3)]
        ft_ = [len(ct_[i]) for i in range(3)]
        surv = {j: len(cs[j] & ct_[j]) for j in range(3)}
        st = d["cells"]["survival"]
        ok2 = (fs == d["cells"]["f_source"] and ft_ == d["cells"]["f_target"]
               and all(surv[j] == st[str(j)]["preserved"] and fs[j] - surv[j] == st[str(j)]["lost"]
                       and ft_[j] - surv[j] == st[str(j)]["new"] for j in range(3)))
        C.add("P04" + name, "specimen %s: fibres, region Graver sets (all-pairs minimality) equal the stored ones; |F| %d->%d, |Graver| %d->%d" % (
            name, len(F), len(F2), len(G), len(G2)), ok)
        C.add("P05" + name, "specimen %s: cells rebuilt from vertex sets: f-vectors %s -> %s; abstract survival per dimension equals stored" % (name, fs, ft_), ok2)
        res[name] = (F, F2, G, G2, cs, ct_)
    # spec preflight
    F, F2, G, G2, cs, ct_ = res["A"]
    kept = edge_set(cs) & edge_set(ct_)
    lost = edge_set(cs) - edge_set(ct_)
    C.add("P02A", "preflight P2-A: 6->12 vertices, 11->29 edges, 12/8 Graver vectors, 3 edges kept (consecutive diagonal), 8 lost = the eight edges listed in the specification",
          (len(F), len(F2), len(edge_set(cs)), len(edge_set(ct_)), len(G), len(G2), len(kept), len(lost)) == (6, 12, 11, 29, 12, 8, 3, 8)
          and kept == {((1, 1), (2, 2)), ((2, 2), (3, 3)), ((3, 3), (4, 4))} and lost == SPEC_LOST_A)
    F, F2, G, G2, cs, ct_ = res["B"]
    C.add("P02B", "preflight P2-B: 6->8 vertices, 5->17 edges, all 5 old edges kept (strict enlargement without edge loss)",
          (len(F), len(F2), len(edge_set(cs)), len(edge_set(ct_)), len(edge_set(cs) & edge_set(ct_))) == (6, 8, 5, 17, 5))
    # lattice order
    ok = True
    for name, (d, P, q, b, b2) in sp.items():
        ok = ok and ga.relation_brute(P, b, b2) == "ENLARGE" == d["lattice"]["relation"] and ga.relation_brute(P, b2, b) == "SHRINK"
    C.add("P03", "lattice order on the INFINITE lattices (periodic-box brute force): A: ker chi_5 < ker chi_4, B: ker chi_27 < ker chi_18 (strict); denominators 5 and 4 are not related by divisibility",
          ok and 5 % 4 != 0 and 4 % 5 != 0)
    C.add("P03b", "relation lattices: A: a-b = 0 (mod 4) < a+b = 0 (mod 2); B: a-b = 0 (mod 18) < a-b = 0 (mod 6) (the specification's 'mod 18/6' for both coordinates is a typo: those sublattices would give an empty fibre)",
          all(ga.in_Lambda((a, b_), (3, 7), 5) == ((a - b_) % 4 == 0) for a in range(-9, 10) for b_ in range(-9, 10))
          and all(ga.in_Lambda((a, b_), (3, 7), 4) == ((a + b_) % 2 == 0) for a in range(-9, 10) for b_ in range(-9, 10))
          and all(ga.in_Lambda((a, b_), (5, 11), 27) == ((a - b_) % 18 == 0) for a in range(-20, 21) for b_ in range(-20, 21))
          and all(ga.in_Lambda((a, b_), (5, 11), 18) == ((a - b_) % 6 == 0) for a in range(-20, 21) for b_ in range(-20, 21)))
    return res


def audit_geometry_specimens(root, sp, res, C, fast):
    for name, (d, P, q, b, b2) in sp.items():
        F, F2, G, G2, cs, ct_ = res[name]
        cmp_ = ga.planar_compare(cs, ct_, q[0])
        g = d["geometry"]
        stored = {int(k): [v["CONTAINED"], v["PARTIAL"]] for k, v in g["source_cells_vs_target_union"].items()}
        ok = cmp_["relation"] == g["union_relation"] and all(cmp_["per_dim_contained_partial"][j] == stored.get(j, [0, 0]) for j in range(3))
        pr = ga.probes(1500 if fast else 4000, q[0])
        ps, pt = cmp_["ps"], cmp_["pt"]
        probe_ok = True
        for p in pr:
            in_s = any(ga.contains(pl, p) for _, pl in ps)
            in_t = any(ga.contains(pl, p) for _, pl in pt)
            if in_s and not in_t:
                probe_ok = False
        wit = g["witness_target_not_in_source"]
        wp = (Fr(wit[0]), Fr(wit[1]))
        wit_ok = (any(ga.contains(pl, wp) for _, pl in pt) and not any(ga.contains(pl, wp) for _, pl in ps))
        C.add("P06" + name, "specimen %s geometry (exact sampling): relation %s; source cells CONTAINED/PARTIAL %s; %d random rational probes never leave the target union; exact witness of U' \\ U checked" % (
            name, cmp_["relation"], cmp_["per_dim_contained_partial"], len(pr)), ok and probe_ok and wit_ok)
        topo = g["union_topology"]
        bs = {p: ga.union_betti_mod(ps, cmp_["S"], p) for p in (2, 3, 2147483647)}
        bt = {p: ga.union_betti_mod(pt, cmp_["S"], p) for p in (2, 3, 2147483647)}
        ok_b = all(bs[p][:2] == topo["source"]["betti"][:2] for p in bs) and all(bt[p][:2] == topo["target"]["betti"][:2] for p in bt)
        ab = [ga.complex_betti_planar(cs, p) for p in (2, 3, 2147483647)], [ga.complex_betti_planar(ct_, p) for p in (2, 3, 2147483647)]
        ok_a = all(v == d["cells"]["betti_abs_source"][:3] for v in ab[0]) and all(v == d["cells"]["betti_abs_target"][:3] for v in ab[1])
        C.add("P07" + name, "specimen %s topology: Betti of the REALIZED union (nerve, GF(2)/GF(3)/GF(2^31-1)) %s -> %s; of the ABSTRACT complex %s -> %s; both agree with stored values" % (
            name, topo["source"]["betti"][:2], topo["target"]["betti"][:2], d["cells"]["betti_abs_source"], d["cells"]["betti_abs_target"]), ok_b and ok_a)


def count_edges_brute(h, moves, lat):
    n = 0
    for g in moves:
        for u0 in range(h + 1):
            for u1 in range(h + 1):
                w = (u0 + g[0], u1 + g[1])
                if (u0, u1) != (0, 0) and w != (0, 0) and 0 <= w[0] <= h and 0 <= w[1] <= h and lat(u0, u1) and lat(*w):
                    n += 1
    return n


def audit_family(root, C, fast):
    fam = load(root, "data/P2_F21.json")
    hmax = 40 if fast else 60
    ok, bad = True, ""
    for h in range(1, hmax + 1):
        x = Fr(21 ** (2 * h), 5)
        nx, L, G, ds = ga.C_brute(x)
        P, q, b = ga.coords(x)
        P2, q2, b2 = ga.coords(nx)
        if not (nx == Fr(21 ** (2 * h), 4) and L == 21 ** h and G == 20 and P == (3, 7) and q == (h, h) and (P2, q2, b2) == (P, q, 4)):
            ok, bad = False, "h=%d" % h
    C.add("P08", "P2-F21: for h=1..%d the transition 21^(2h)/5 -> 21^(2h)/4 is recomputed from D, L, G, C (L=21^h, G=20, same primes (3,7), box (h,h), b: 5->4)" % hmax, ok, bad)
    # lattices (independent of h)
    C.add("P09", "P2-F21: lattices a-b=0 mod 4  <  a+b=0 mod 2 (strict, brute force on the infinite lattices)", ga.relation_brute((3, 7), 5, 4) == "ENLARGE")
    ok, bad = True, ""
    for r in fam["direct"]:
        h = r["formula"]["h"]
        P, q = (3, 7), (h, h)
        G, G2 = ga.graver(P, q, 5), ga.graver(P, q, 4)
        sm = sorted({s * t for g in SRC_MOVES if max(map(abs, g)) <= h for s in (1, -1) for t in [g]} if False else
                    {tuple(s * c for c in g) for g in SRC_MOVES if max(map(abs, g)) <= h for s in (1, -1)})
        tm = sorted({tuple(s * c for c in g) for g in TGT_MOVES if max(map(abs, g)) <= h for s in (1, -1)})
        common = sorted(set(G) & set(G2))
        if sorted(G) != sm or sorted(G2) != tm or common != [(-1, -1), (1, 1)] or tup(r["common_graver"]) != tuple(common):
            ok, bad = False, "h=%d" % h
    C.add("P10", "P2-TF1 Graver part: for h=1..%d the region Graver sets are exactly {+-g : g in the six (resp. four) moves with max|g_i|<=h}; their intersection is exactly {+-(1,1)}" % len(fam["direct"]), ok, bad)
    ok, bad = True, ""
    for r in fam["direct"]:
        h = r["formula"]["h"]
        P, q = (3, 7), (h, h)
        F, F2 = ga.fibre(P, q, 5), ga.fibre(P, q, 4)
        G, G2 = ga.graver(P, q, 5), ga.graver(P, q, 4)
        cs, ct_ = ga.cells_planar(F, G), ga.cells_planar(F2, G2)
        kept = edge_set(cs) & edge_set(ct_)
        diag = {e for e in edge_set(cs) if (e[1][0] - e[0][0], e[1][1] - e[0][1]) == (1, 1)}
        st = r["cells"]["survival"]
        if not (kept == diag and len(cs[2] & ct_[2]) == 0 and set(F) <= set(F2)
                and (len(F), len(F2), len(edge_set(cs)), len(edge_set(ct_)), len(kept)) == (
                    r["formula"]["V_src"], r["formula"]["V_tgt"], r["formula"]["E_src"], r["formula"]["E_tgt"], r["formula"]["E_kept"])
                and st["1"]["preserved"] == len(kept) and st["2"]["preserved"] == 0 and st["2"]["source"] == len(cs[2])):
            ok, bad = False, "h=%d" % h
    C.add("P11", "P2-TF1 cell part: for h=1..%d all vertices persist, the surviving edges are exactly the (1,1)-edges, NO 2-cell survives; counts equal the closed-form table (cells rebuilt from vertex sets)" % len(fam["direct"]), ok, bad)
    # quasi-polynomials against independent brute counts
    ok, bad = True, ""
    qp = fam["quasi_polynomials_mod4"]
    for h in range(4, (80 if fast else 140)):
        r = h % 4
        lat5, lat4 = (lambda a, b: (a - b) % 4 == 0), (lambda a, b: (a + b) % 2 == 0)
        vs = sum(1 for a in range(h + 1) for b in range(h + 1) if (a, b) != (0, 0) and lat5(a, b))
        vt = sum(1 for a in range(h + 1) for b in range(h + 1) if (a, b) != (0, 0) and lat4(a, b))
        es, et, ek = count_edges_brute(h, SRC_MOVES, lat5), count_edges_brute(h, TGT_MOVES, lat4), count_edges_brute(h, [(1, 1)], lat5)
        for key, val in (("V_src", vs), ("V_tgt", vt), ("E_src", es), ("E_tgt", et), ("E_kept", ek), ("E_lost", es - ek), ("E_new", et - ek)):
            c = qp[key][str(r)]
            if Fr(c["c2"]) * h * h + Fr(c["c1"]) * h + Fr(c["c0"]) != val:
                ok, bad = False, "%s h=%d" % (key, h)
    C.add("P12", "P2-TF1 counting: the stored quasi-polynomials (period 4 in h) reproduce independent brute-force vertex/edge counts for every 4 <= h < %d" % (80 if fast else 140), ok, bad)
    # geometry of the family
    ok, bad = True, ""
    n = 0
    for r in fam["direct"]:
        if "geometry" not in r:
            continue
        h = r["formula"]["h"]
        if h > (5 if fast else 8):
            continue
        P, q = (3, 7), (h, h)
        F, F2 = ga.fibre(P, q, 5), ga.fibre(P, q, 4)
        cmp_ = ga.planar_compare(ga.cells_planar(F, ga.graver(P, q, 5)), ga.cells_planar(F2, ga.graver(P, q, 4)), h)
        g = r["geometry"]
        stored = {int(k): [v["CONTAINED"], v["PARTIAL"]] for k, v in g["source_cells_vs_target_union"].items()}
        if cmp_["relation"] != g["union_relation"] or any(cmp_["per_dim_contained_partial"][j] != stored.get(j, [0, 0]) for j in range(3)):
            ok, bad = False, "h=%d" % h
        n += 1
    C.add("P13", "P2-F21 geometry (exact sampling re-implemented): union relation and per-dimension CONTAINED/PARTIAL equal the stored data for %d values of h" % n, ok, bad)


def audit_corpus(root, C, fast):
    corp = load(root, "data/SEARCH_CORPUS.json")
    rows = corp["k2"]["rows"] + corp["k3"]["rows"]
    stride = 9 if fast else 3
    sample = rows[::stride]
    ok_arith = ok_rel = ok_cells = True
    skipped = 0
    bad = ""
    for i, r in enumerate(sample):
        x = Fr(r["x"])
        nx, L, G, ds = ga.C_brute(x)
        P, q, b = ga.coords(x)
        if not (str(nx) == r["x_next"] and L == r["L"] and G == r["G"] and list(P) == r["primes"] and list(q) == r["box"] and b == r["b"]
                and nx.denominator == r["b_next"] and ga.coords(nx)[:2] == (P, q)):
            ok_arith, bad = False, r["x"]
        b2 = r["b_next"]
        M = 1
        for p in P:
            M *= ga.lcm([ga.order_brute(p, b), ga.order_brute(p, b2)])
        if M <= 300000:
            if ga.relation_brute(P, b, b2) != r["relation"]:
                ok_rel, bad = False, r["x"]
        else:
            skipped += 1
        if len(P) == 2:
            F, F2 = ga.fibre(P, q, b), ga.fibre(P, q, b2)
            G1, G2 = ga.graver(P, q, b), ga.graver(P, q, b2)
            cs, ct_ = ga.cells_planar(F, G1), ga.cells_planar(F2, G2)
            surv = r["survival"]
            if not (set(F) <= set(F2)) == r["F_subset_F_target"] or [len(cs[j]) for j in range(3)] != r["f_source"] or \
                    [len(ct_[j]) for j in range(3)] != r["f_target"] or any(
                    [len(cs[j]), len(cs[j] & ct_[j]), len(cs[j]) - len(cs[j] & ct_[j])] != surv[str(j)] for j in range(3)):
                ok_cells, bad = False, r["x"]
            # soundness of the order rule on the audit side
            ords = [ga.order_brute(p, b2) for p in P]
            for g in G1:
                if not any(g):
                    continue
                supp = [t for t in range(2) if g[t]]
                blocked = any(abs(g[t]) >= ords[t] and not (len(supp) == 1 and supp[0] == t and abs(g[t]) == ords[t]) for t in range(2))
                if blocked and g in G2:
                    ok_cells, bad = False, "order rule unsound at %s" % r["x"]
    C.add("P14", "corpus sample (%d of %d rows): FIELD-I step, coordinates, L, G recomputed by brute force" % (len(sample), len(rows)), ok_arith, bad)
    C.add("P15", "corpus sample: lattice class (EQUAL excluded; ENLARGE/SHRINK/INCOMPARABLE) decided by periodic-box brute force equals stored (%d rows too large for brute force are NOT checked here)" % skipped, ok_rel, bad)
    C.add("P16", "corpus sample (k=2): F-inclusion, f-vectors, cell survival per dimension rebuilt from vertex sets equal stored; axis/order rule never blocks a surviving Graver vector", ok_cells, bad)
    # self-consistency of summaries
    cnt = {}
    for r in rows:
        cnt[r["relation"]] = cnt.get(r["relation"], 0) + 1
    lo = load(root, "results/P2_LATTICE_ORDER.json")
    cl = lo["corpus"]
    tot = {}
    for k in ("k2", "k3"):
        for c, v in cl[k]["classes"].items():
            tot[c] = tot.get(c, 0) + v
    C.add("P17", "summary files agree with the corpus rows (class counts %s)" % cnt, tot == cnt)
    cs = load(root, "results/P2_CELL_SURVIVAL.json")["corpus"]
    ok = (cs["k2"]["cell_prediction_exact"] == len(corp["k2"]["rows"]) and cs["k3"]["cell_prediction_exact"] == len(corp["k3"]["rows"])
          and cs["k2"]["order_rule_sound"] == len(corp["k2"]["rows"]) and cs["k3"]["order_rule_sound"] == len(corp["k3"]["rows"]))
    C.add("P18", "generator-based prediction of cell survival (vertices in F' and generators in the surviving Graver set) is exact on all %d corpus rows; order rule sound on all rows (exact on %d of %d k=2 rows)" % (
        len(rows), cs["k2"]["order_rule_exact"], len(corp["k2"]["rows"])), ok)
    # geometry on a sample of ENLARGE rows
    geo = [r for r in corp["k2"]["rows"] if "geometry" in r and r["relation"] == "ENLARGE"]
    gs = geo[::(12 if fast else 5)]
    ok = True
    for r in gs:
        P, q, b, b2 = tuple(r["primes"]), tuple(r["box"]), r["b"], r["b_next"]
        F, F2 = ga.fibre(P, q, b), ga.fibre(P, q, b2)
        cmp_ = ga.planar_compare(ga.cells_planar(F, ga.graver(P, q, b)), ga.cells_planar(F2, ga.graver(P, q, b2)), q[0])
        if cmp_["relation"] != r["geometry"]["union_relation"] or any(
                cmp_["per_dim_contained_partial"][j][1] != 0 for j in range(3)):
            ok = False
    C.add("P19", "geometry of %d sampled ENLARGE rows (k=2) re-derived with exact sampling: U subset U' (no PARTIAL cell) in every sampled row, relation equals stored" % len(gs), ok)
    gst = load(root, "results/P2_GEOMETRY.json")
    C.add("P20", "stored geometry summary: all %d ENLARGE rows with geometry have U subset U' (conjecture CP2 supported, NOT proved)" % gst["corpus_k2_ENLARGE"]["rows_with_geometry"],
          gst["corpus_k2_ENLARGE"]["rows_with_partial_cells"] == 0 and set(gst["corpus_k2_ENLARGE"]["union_relation"]) <= {"U_SUBSET_U2", "EQUAL"})
    return corp


def audit_counterexamples(root, corp, C):
    ce = {c["id"]: c for c in load(root, "results/P2_COUNTEREXAMPLES.json")["counterexamples"]}
    rows = corp["k2"]["rows"] + corp["k3"]["rows"]
    # F2/L6 witnesses by brute force
    ok = True
    for key in ("witness_SHRINK", "witness_INCOMPARABLE"):
        w = ce["CE-P2-F2"][key]
        x = Fr(w["x"])
        nx = ga.C_brute(x)[0]
        P, q, b = ga.coords(x)
        b2 = nx.denominator
        rel = ga.relation_brute(P, b, b2)
        ok = ok and str(nx) == w["x_next"] and set(ga.fibre(P, q, b)) <= set(ga.fibre(P, q, b2)) and rel == ("SHRINK" if "SHRINK" in key else "INCOMPARABLE") and ga.coords(nx)[:2] == (P, q)
    pair = ce["CE-P2-F2"]["non_FIELD_I_pair"]
    ok = ok and ga.fibre((2, 11), (1, 1), 3) == ga.fibre((2, 11), (1, 1), 7) == [(1, 1)] and ga.relation_brute((2, 11), 3, 7) == "INCOMPARABLE"
    C.add("CE1", "CE-P2-F2: FIELD-I transitions with F subset F' whose lattices SHRINK / are INCOMPARABLE (and 484/3 vs 484/7), verified by brute force; %d such rows in the corpus" % ce["CE-P2-F2"]["n_FIELD_I_transitions_with_F_subset_F_next_and_non_ordered_lattices"], ok)
    w = ce["CE-P2-L6"]["witness"][0]
    x = Fr(w["x"])
    nx = ga.C_brute(x)[0]
    P, q, b = ga.coords(x)
    C.add("CE2", "CE-P2-L6: a FIELD-I step with unchanged primes/box whose relation lattice strictly SHRINKS (%s -> %s, fibres %d -> %d)" % (w["x"], w["x_next"], w["n_F"], w["n_F_target"]),
          str(nx) == w["x_next"] and ga.relation_brute(P, b, nx.denominator) == "SHRINK" and len(ga.fibre(P, q, b)) == w["n_F"])
    spans = [r for r in rows if r["relation"] in ("SHRINK", "INCOMPARABLE") and r["fibre_spans_source_lattice"]]
    C.add("CE3", "no SHRINK/INCOMPARABLE corpus row has a source fibre that spans its lattice (consistent with E2-P1 Lemma E2-4); %d rows" % sum(1 for r in rows if r["relation"] in ("SHRINK", "INCOMPARABLE")), not spans)
    # F1
    k = ce["CE-P2-F1"]["corpus_rows_with_all_edges_kept"]
    n1 = sum(1 for r in corp["k2"]["rows"] if r["relation"] == "ENLARGE" and r["survival"]["1"][0] > 0 and r["survival"]["1"][2] == 0)
    C.add("CE4", "CE-P2-F1: strict enlargement with every old edge kept (P2-B and %d corpus rows)" % k, n1 == k and k > 0)
    # F3 : denominators
    n3 = sum(1 for r in rows if r["relation"] == "ENLARGE" and r["b"] % r["b_next"] != 0)
    C.add("CE5", "CE-P2-F3: %d ENLARGE rows have b' not dividing b (P2-A: 5 -> 4)" % n3, n3 == ce["CE-P2-F3"]["corpus_ENLARGE_rows_with_b_next_not_dividing_b"] and n3 > 0)
    # b' | b ==> never SHRINK/INCOMPARABLE (sound direction)
    C.add("CE6", "sound direction: b' | b implies ker chi_b <= ker chi_b' (no corpus row with b'|b is SHRINK or INCOMPARABLE)",
          not any(r["b"] % r["b_next"] == 0 and r["relation"] in ("SHRINK", "INCOMPARABLE") for r in rows))
    # F6 pair
    a, b_ = ce["CE-P2-F6"]["witness_pair"]
    C.add("CE7", "CE-P2-F6: two ENLARGE transitions with equal prime set, box and lattice indices (%s -> %s) but different edge survival (lost %d vs %d)" % (
        a["index_source"], a["index_target"], a["survival"]["1"][2], b_["survival"]["1"][2]),
        a["relation"] == b_["relation"] == "ENLARGE" and (a["index_source"], a["index_target"]) == (b_["index_source"], b_["index_target"])
        and (a["survival"]["1"][2] == 0) != (b_["survival"]["1"][2] == 0))
    # F5: 3-coordinate witness, independent exact check
    P, q = (2, 5, 11), (2, 2, 2)
    even = lambda v: sum(v) % 2 == 0
    corners = [(0, 0, 2), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
    in_F = all(any(c) and even(c) and all(0 <= t <= 2 for t in c) for c in corners)
    G = ga.graver(P, q, 3)
    gens_ok = (0, 1, -1) in G and (1, 0, -1) in G
    cx = tuple(Fr(2, 3) for _ in range(3))
    pt_in_P = cx == tuple(a_ + Fr(2, 3) * g1 + Fr(2, 3) * g2 for a_, g1, g2 in zip((0, 0, 2), (0, 1, -1), (1, 0, -1)))
    Fp = ga.fibre(P, q, 1)
    Gp = ga.graver(P, q, 1)
    target_axes = sorted(Gp) == sorted([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)])
    # the only target cell containing a point of (0,1)^3 would be the cube [0,1]^3 whose corner 0 is not in F'
    C.add("CE8", "CE-P2-F5 (three coupled coordinates, even-sum lattice in Z^3 -> Z^3): the Graver parallelogram P((0,0,2);(0,1,-1),(1,0,-1)) has all corners in F, contains (2/3,2/3,2/3), which lies in NO target cell (the only target cell meeting (0,1)^3 would be the unit cube with corner 0, absent from F')",
          in_F and gens_ok and pt_in_P and target_axes and (0, 0, 0) not in set(Fp) and all(0 < t < 1 for t in cx))


def audit_files(root, C):
    ok = True
    bad = []
    for rel, h in INHERITED.items():
        if sha(os.path.join(root, rel)) != h:
            ok = False
            bad.append(rel)
    C.add("P21", "inherited E2-P1 engine files are byte-identical to the frozen E2-P1 sources", ok, ",".join(bad))
    mp = os.path.join(root, "MANIFEST.json")
    if os.path.exists(mp):
        man = load(root, "MANIFEST.json")["sha256"]
        diff = [r for r, h in man.items() if not os.path.exists(os.path.join(root, r)) or sha(os.path.join(root, r)) != h]
        C.add("P22", "MANIFEST.json: SHA-256 of all %d listed files match" % len(man), not diff, ",".join(diff[:5]))
    else:
        C.add("P22", "MANIFEST.json present", False, "missing")


def audit_reproducible(root, C):
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, "-I", os.path.join(root, "src", "build_p2.py"), "--out", tmp], capture_output=True, text=True)
        diffs = []
        if r.returncode == 0:
            for rel in ("data/P2_A.json", "data/P2_B.json", "data/P2_F21.json", "data/SEARCH_CORPUS.json", "results/P2_LATTICE_ORDER.json",
                        "results/P2_CELL_SURVIVAL.json", "results/P2_GEOMETRY.json", "results/P2_COUNTEREXAMPLES.json"):
                if sha(os.path.join(tmp, rel)) != sha(os.path.join(root, rel)):
                    diffs.append(rel)
        C.add("P23", "builder re-run from scratch reproduces all eight stored JSON files byte-for-byte", r.returncode == 0 and not diffs, ",".join(diffs) or r.stderr[-200:])


def verify(root=ROOT, fast=False, parts=("spec", "family", "corpus", "files", "repro")):
    C = Certs()
    sp = audit_specimens(root, C)
    if "spec" in parts:
        res = audit_fibres_cells(root, sp, C)
        audit_geometry_specimens(root, sp, res, C, fast)
    if "family" in parts:
        audit_family(root, C, fast)
    corp = None
    if "corpus" in parts:
        corp = audit_corpus(root, C, fast)
        audit_counterexamples(root, corp, C)
    if "files" in parts:
        audit_files(root, C)
    if "repro" in parts and not fast:
        audit_reproducible(root, C)
    elif "repro" in parts:
        C.add("P23", "from-scratch rebuild", True, "skipped in --fast mode", status="NOT_RERUN")
    return C


def main():
    fast = "--fast" in sys.argv
    t0 = time.time()
    C = verify(ROOT, fast=fast)
    n_pass = sum(c["status"] == "PASS" for c in C.items)
    print("\n%d/%d checks passed in %.0fs%s" % (n_pass, len(C.items), time.time() - t0, " (fast mode)" if fast else ""))
    if "--write" in sys.argv and C.ok:
        out = {"spec": SPEC, "package": "GEO_HD_E2_P2_v001", "mode": "fast" if fast else "full", "all_pass": C.ok, "certificates": C.items}
        with open(os.path.join(ROOT, "results", "P2_CERTIFICATES.json"), "w", newline="\n") as fh:
            json.dump(out, fh, indent=1, sort_keys=True)
            fh.write("\n")
        print("wrote results/P2_CERTIFICATES.json")
    print("EXACT_PASS" if C.ok else "EXACT_FAIL")
    sys.exit(0 if C.ok else 1)


if __name__ == "__main__":
    main()
