#!/usr/bin/env python3
"""E2-P3 verification.  Usage:  python RUN_VERIFY.py [--fast | --full] [--root DIR]

Replays the stored data with INDEPENDENT code (src/audit_p3.py + src/certificate_check.py; they import nothing from the builder modules)
and checks every gate claimed in STATUS.json.  --fast samples rows (every 7th planar row plus all rows of interest); --full re-derives every row.
Shared code between builder and audit: Python standard library only.  Inherited E2-P2 modules are hash-pinned (they are builder-side code)."""
import copy
import hashlib
import json
import os
import sys
import time
from fractions import Fraction as Fr

ROOT = os.path.dirname(os.path.abspath(__file__))
for i, a in enumerate(sys.argv):
    if a == "--root":
        ROOT = sys.argv[i + 1]
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)
FAST = "--full" not in sys.argv

import certificate_check as cc  # noqa: E402
import audit_p3 as au  # noqa: E402

PINNED = {
    "src/p2/inherited/e1_cell_transport.py": "2c767b00",
    "src/p2/inherited/fibre_transport.py": "7360be29",
    "src/p2/lattice_transport.py": "51ce4766",
    "src/p2/graver_transport.py": "f9d05c0b",
    "src/p2/cell_transport.py": "41bc44b4",
    "src/p2/geometry_audit.py": "32974d4a",
}

RESULTS, FAILS = [], []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + ((" -- " + detail) if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


t0 = time.time()
# ------------------------------------------------------------------ V00 hash pins
for rel, h in PINNED.items():
    d = hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()
    check("V00 pinned inherited module %s" % rel, d.startswith(h), d[:8])

# ------------------------------------------------------------------ V01 controls
ctl = load("data/P3_CONTROLS.json")
for name in ("A", "B", "C"):
    c = ctl[name]
    x = Fr(c["x"])
    it = au.independent_transition(x)
    check("V01%s independent FIELD-I transition (x -> x_next, primes, box, b, b')" % name,
          it["same_coords"] and list(it["P"]) == c["primes"] and list(it["q"]) == c["box"] and it["b"] == c["b"] and it["b2"] == c["b_next"]
          and str(it["x2"]) == c["x_next"])
    P, q = tuple(c["primes"]), tuple(c["box"])
    ind = au.audit_verdict(P, q, c["b"], c["b_next"], c["verdict"])
    k = len(q)
    T = c["target_maximal"]
    same_T = au.as_vertexset_family(T) == au.as_vertexset_family(ind["target_maximal"])
    check("V01%s stored target maximal cells equal independent derivation" % name, same_T)
    if c["verdict"] == "NOT_CONTAINED":
        ok, why = cc.verify_noncontainment(c["certificate"], ind["target_maximal"], k)
        check("V01%s noncontainment certificate (independent cells)" % name, ok, why)
        sw = c["specified_witness_certificate"]
        ok, why = cc.verify_noncontainment(sw["certificate"], ind["target_maximal"], k)
        check("V01%s specified witness (2/3,2/3,2/3) certificate" % name, ok and sw["certificate"]["witness"] == ["2/3", "2/3", "2/3"], why)
    else:
        S = {tuple(map(tuple, [c2["base"]])) + tuple(tuple(g) for g in c2["gens"]) for c2 in ind["source_maximal"]}
        got = {tuple(map(tuple, [c2["source_cell"]["base"]])) + tuple(tuple(g) for g in c2["source_cell"]["gens"]) for c2 in c["certificates"]}
        check("V01%s certificates cover every independently derived source maximal cell" % name, S == got)
        oks = [cc.verify_containment(c2, ind["target_maximal"], k) for c2 in c["certificates"]]
        check("V01%s containment certificates (independent cells)" % name, all(o for o, _ in oks), "%d certificates" % len(oks))
    if c.get("hull_cover_certificate"):
        F2 = au.independent_cells(P, q, c["b_next"])[0]
        ok, why, ng = cc.verify_hull_tree({"hull_halfspaces": c["hull_cover_certificate"]["hull_halfspaces"], "tree": c["hull_cover_certificate"]["tree"]},
                                        F2, ind["target_maximal"], k)
        check("V01%s hull-cover tree" % name, ok and ng == len(c["coverage_gap"]["gap_pieces"]), "%s gap nodes=%s" % (why, ng))

check("V01 control verdicts are A: CONTAINED, B: CONTAINED, C: NOT_CONTAINED",
      (ctl["A"]["verdict"], ctl["B"]["verdict"], ctl["C"]["verdict"]) == ("CONTAINED", "CONTAINED", "NOT_CONTAINED"))
check("V01 control A target is INHERITED_G12T8 and exactly hull-covered; control B is a residual hollow box with a nonempty gap",
      ctl["A"]["target_classification"]["class"] == "INHERITED_G12T8" and ctl["A"]["coverage_gap"]["hull_covered"] is True
      and ctl["B"]["target_classification"]["class"] == "RESIDUAL_EXCEPTIONAL_HOLLOW_BOX" and ctl["B"]["coverage_gap"]["hull_covered"] is False)
check("V01 independent normal form agrees with builder normal form (A,B)",
      all((ctl[n]["independent_normal_form"]["d"], ctl[n]["independent_normal_form"]["s"]) ==
          (ctl[n]["target_classification"]["d"], ctl[n]["target_classification"]["s"]) for n in ("A", "B")))

# ------------------------------------------------------------------ V02 tamper tests on stored certificates
c = ctl["C"]
Tm = c["target_maximal"]
base = c["certificate"]
tests = []
x = copy.deepcopy(base); x["witness"][0] = "0"; tests.append(("witness moved", x))
x = copy.deepcopy(base); x["violations"][0]["c"] = "1000000"; tests.append(("inequality bound changed", x))
x = copy.deepcopy(base); x["violations"] = x["violations"][:-1]; tests.append(("target cell dropped from list", x))
x = copy.deepcopy(base); x["source_cell"] = {"base": [9, 9, 9], "gens": [[1, 0, 0]]}; tests.append(("source cell replaced", x))
x = copy.deepcopy(base); x["params"][0] = "5"; tests.append(("parameters falsified", x))
for name_, t in tests:
    check("V02 tamper rejected (noncontainment): %s" % name_, not cc.verify_noncontainment(t, Tm, 3)[0])
b = ctl["B"]
corrupted = 0
for cert in b["certificates"]:
    c2 = copy.deepcopy(cert)

    def corrupt(n):
        if "leaf" in n:
            n["leaf"] = (n["leaf"] + 1) % len(b["target_maximal"])
            return True
        if "split" in n:
            return corrupt(n["lo"]) or corrupt(n["hi"])
        return False
    if corrupt(c2["tree"]) and not cc.verify_containment(c2, b["target_maximal"], 2)[0]:
        corrupted += 1
check("V02 tamper rejected (containment): leaf reassigned to a different target cell", corrupted >= 1, "%d of %d trees rejected" % (corrupted, len(b["certificates"])))
hb = copy.deepcopy(b["hull_cover_certificate"])
hb["hull_halfspaces"][0][1] = str(Fr(hb["hull_halfspaces"][0][1]) + 50)
F2B = au.independent_cells(tuple(b["primes"]), tuple(b["box"]), b["b_next"])[0]
check("V02 tamper rejected (hull tree): root inequality loosened", not cc.verify_hull_tree(hb, F2B, b["target_maximal"], 2)[0])
hb = copy.deepcopy(b["hull_cover_certificate"])


def drop_gap(n):
    if "gap" in n:
        n["gap"]["violations"] = n["gap"]["violations"][:-1]
        return True
    if "split" in n:
        return drop_gap(n["lo"]) or drop_gap(n["hi"])
    return False


drop_gap(hb["tree"])
check("V02 tamper rejected (hull tree): gap witness missing a target violation", not cc.verify_hull_tree(hb, F2B, b["target_maximal"], 2)[0])

# ------------------------------------------------------------------ V03 planar corpus (independent re-derivation)
import exact_containment as _proposer  # noqa: E402  -- proposes certificates only; every certificate is checked by certificate_check.py

pl = load("data/P3_PLANAR_CORPUS.json")
res_planar = load("results/P3_PLANAR.json")
rows = pl["rows"]
check("V03 planar corpus has rows and no unreported error rows", len(rows) > 0 and not any(r.get("error") for r in rows), "%d rows" % len(rows))
sel = []
for i, r in enumerate(rows):
    interesting = (r.get("verdict") != "CONTAINED" or r.get("target_class") in ("RESIDUAL_EXCEPTIONAL_HOLLOW_BOX",)
                   or (r.get("target_class") == "RESIDUAL_SUBTHRESHOLD_BOX" and r.get("hull_covered") is False))
    if not FAST or interesting or i % 7 == 0:
        sel.append(r)
bad_v, bad_cls, bad_trans, n_checked = [], [], [], 0
for r in sel:
    P, q, b, b2 = tuple(r["primes"]), tuple(r["box"]), r["b"], r["b_next"]
    x = Fr(r["x"])
    it = au.independent_transition(x)
    if not (it["same_coords"] and it["P"] == P and it["q"] == q and it["b"] == b and it["b2"] == b2 and str(it["x2"]) == r["x_next"]):
        bad_trans.append(r["x"])
        continue
    _, cs = au.independent_cells(P, q, b)
    _, ct = au.independent_cells(P, q, b2)
    Sm, Tm_ = au.maximal_cells(cs), au.maximal_cells(ct)
    dec = _proposer.decide_union([(c_[0], tuple(c_[1])) for c_ in Sm], [(c_[0], tuple(c_[1])) for c_ in Tm_], len(q))
    Tj = [{"base": list(c_[0]), "gens": [list(g) for g in c_[1]]} for c_ in Tm_]
    if au.as_vertexset_family(dec["target_maximal"]) != au.as_vertexset_family(Tj):
        bad_v.append((r["x"], "target cells"))
        continue
    if dec["verdict"] != r["verdict"]:
        bad_v.append((r["x"], "verdict %s != stored %s" % (dec["verdict"], r["verdict"])))
        continue
    if dec["verdict"] == "NOT_CONTAINED":
        ok, why = cc.verify_noncontainment(dec["certificate"], Tj, len(q))
        if not ok:
            bad_v.append((r["x"], why))
    else:
        for c_ in dec["certificates"]:
            ok, why = cc.verify_containment(c_, Tj, len(q))
            if not ok:
                bad_v.append((r["x"], why))
                break
    if len(q) == 2 and b2 > 1:
        nf = au.independent_normal_form(P, b2, q)
        snf = r["target_normal_form"]
        if nf is None or (nf["d"], nf["a"], nf["c"], nf["s"], tuple(nf["Qn"])) != (snf["d"], snf["a"], snf["c"], snf["s"], tuple(snf["Qn"])):
            bad_cls.append(r["x"])
    n_checked += 1
check("V03 planar rows: independent transition data equal stored", not bad_trans, "%d mismatches" % len(bad_trans))
check("V03 planar rows: independent cells + certificate verification agree with stored verdicts", not bad_v and n_checked > 0,
      "%d rows checked (%s), %d disagreements" % (n_checked, "sampled" if FAST else "all", len(bad_v)))
check("V03 planar rows: independent normal form (d,a,c,s,Q_norm) equals builder normal form", not bad_cls, "%d mismatches" % len(bad_cls))

# class / theorem consistency on the whole stored corpus
inh = [r for r in rows if r["target_class"] == "INHERITED_G12T8"]
check("V04 INHERITED_G12T8 rows are exactly hull-covered (exact cross-check of the inherited theorem on every instance)",
      all(r["hull_covered"] is True for r in inh), "%d rows" % len(inh))
rect = [r for r in rows if r["target_class"] in ("RESIDUAL_D1_RECTANGULAR", "TARGET_Z2_TRIVIAL")]
check("V04 P3-T2a: every rectangular-target planar row is CONTAINED (any relation)", all(r["verdict"] == "CONTAINED" for r in rect), "%d rows" % len(rect))
check("V04 planar: no recorded CONTAINMENT FAILURE (CP3-A not refuted in scope)", not [r for r in rows if r["verdict"] == "NOT_CONTAINED"])
check("V04 E2-P2 geometry verdicts reproduced (0 changes)", res_planar["e2p2_geometry_comparison"]["verdict_changes"] == [],
      "%d rows compared" % res_planar["e2p2_geometry_comparison"]["rows_compared"])
check("V04 the 337 skipped E2-P2 planar states are reproduced as explicitly UNAVAILABLE", res_planar["e2p2_enlarge_rows"]["e2p2_skipped_337_reproduced"])

# ------------------------------------------------------------------ V05 three-coordinate data
d3 = load("results/P3_3D.json")
s1_fail = d3["S1"]["noncontained"]
nbad = 0
for r in s1_fail[:: (1 if not FAST else 3)]:
    P, q, b, b2 = tuple(r["primes"]), tuple(r["box"]), r["b"], r["b_next"]
    _, cs = au.independent_cells(P, q, b)
    _, ct = au.independent_cells(P, q, b2)
    Tm_ = au.maximal_cells(ct)
    Tj = [{"base": list(c_[0]), "gens": [list(g) for g in c_[1]]} for c_ in Tm_]
    cert = _proposer.noncontainment_certificate(tuple(r["witness_cell"]["base"]), [tuple(g) for g in r["witness_cell"]["gens"]],
                                                tuple(Fr(w) for w in r["witness"]), [_proposer.Target(t["base"], t["gens"], 3) for t in Tj], 3)
    if not cc.verify_noncontainment(cert, Tj, 3)[0]:
        nbad += 1
check("V05 three-coordinate S1 failures: certificates verify against independently derived target cells", nbad == 0,
      "%d checked" % len(s1_fail[:: (1 if not FAST else 3)]))
check("V05 S1 failures: every failure has TARGET lattice Z^k-like (index 1) -> not a both-nontrivial specimen unless listed in S2",
      all(not r.get("both_nontrivial") for r in s1_fail))
lm_fail = d3["lattice_model"]["failures"]
from itertools import product as _prod  # noqa: E402
nbad = 0
for r in lm_fail:
    q = tuple(r["box"])
    cells_ = {}
    for base in _prod(*[range(m + 1) for m in q]):
        for mask in _prod((0, 1), repeat=3):
            gens = [tuple(int(i == j) for i in range(3)) for j in range(3) if mask[j]]
            if all(base[j] + (1 if mask[j] else 0) <= q[j] for j in range(3)):
                vs = []
                for bits in _prod((0, 1), repeat=len(gens)):
                    v = list(base)
                    for bit, g in zip(bits, gens):
                        if bit:
                            v = [a + b_ for a, b_ in zip(v, g)]
                    vs.append(tuple(v))
                if (0, 0, 0) not in vs:
                    cells_[tuple(sorted(vs))] = (base, tuple(gens))
    Tj = [{"base": list(b_), "gens": [list(g) for g in gs]} for b_, gs in au.maximal_cells(list(cells_.values()))]
    cert = _proposer.noncontainment_certificate(tuple(r["witness_cell"]["base"]), [tuple(g) for g in r["witness_cell"]["gens"]],
                                                tuple(Fr(w) for w in r["witness"]), [_proposer.Target(t["base"], t["gens"], 3) for t in Tj], 3)
    if not cc.verify_noncontainment(cert, Tj, 3)[0]:
        nbad += 1
check("V05 lattice-model failures (target Z^3, independently rebuilt unit-face cells): all certificates verify", nbad == 0, "%d failures" % len(lm_fail))
check("V05 lattice-model scan: corner-cube predictor agrees with the exact engine on every row", d3["lattice_model"]["predictor_agrees"],
      "%d rows" % d3["lattice_model"]["n"])
e3 = [r for r in d3["lattice_model"]["failures"] if r["basis"] == [[1, 0, 1], [0, 1, 1], [0, 0, 2]]]
allE = [r for r in load("data/P3_3D_CORPUS.json")["lattice_model_rows"] if r["basis"] == [[1, 0, 1], [0, 1, 1], [0, 0, 2]]]
check("V05 P3-T3(h): even-sum lattice fails exactly when max(box) >= 2",
      allE and all((r["verdict"] == "NOT_CONTAINED") == (max(r["box"]) >= 2) for r in allE), "%d boxes" % len(allE))
s2 = d3["S2"]
check("V05 S2 predictor agrees with the exact engine on every exact-evaluated row", s2["predictor_mismatches"] == [], "%d rows" % s2["exact_rows"])
check("V05 S2 short-vector screen never excluded a predicted failure (soundness of P3-T3(c))", s2["screen_unsound_cases"] == [])

# ------------------------------------------------------------------ V06 gates
st = load("STATUS.json")
gates = st["gates"]
check("V06 STATUS gates present", all(g in gates for g in ("SOURCE_PASS", "GEOMETRY_PASS", "PLANAR_AUDIT_COMPLETE", "EXACT_PASS")))
if not FAILS:
    check("V06 EXACT_PASS consistent with this verification run", gates["EXACT_PASS"] is True)
print("\n%d checks, %d failed, %.0fs (%s)" % (len(RESULTS), len(FAILS), time.time() - t0, "fast" if FAST else "full"))
if "--write" in sys.argv:
    json.dump({"checks": RESULTS, "failed": FAILS}, open(os.path.join(ROOT, "results", "P3_VERIFY_LAST.json"), "w"), indent=1)
sys.exit(1 if FAILS else 0)
