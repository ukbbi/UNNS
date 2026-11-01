#!/usr/bin/env python3
"""E2-P4 v005 verification.  New mathematics only; the v004 verification (S0-S17) is NOT re-run (protocol: record NOT_RERUN with preserved baseline hashes).
   python RUN_VERIFY.py --list
   python RUN_VERIFY.py --fast            (S0..S9, about 2-3 minutes)
   python RUN_VERIFY.py --shard S3        (one shard)
   python RUN_VERIFY.py --full            (adds heavy replays: all 192 stored failures, larger planar / split-criterion runs)
Shards: S0 hash pins (engine byte-identical to v004; v004 baseline sha256; inherited verification NOT_RERUN) | S1 Lemma T (tiling) exact random checks
        S2 L1 / LG / H1 structural lemmas | S3 3D counterexamples CE0-CE4 + contrast (three independent routes) | S4 dilation invariance P5-D1
        S5 split-slab union identity (brute force) | S6 split-slab criterion vs the pinned exact engine | S7 planar P5-P1 independent audit
        S8 stored scan results: tallies + exact re-verification of stored failures | S9 gates / status consistency.
Independence: mini.py (third implementation), tiling_lemma.py, planar_audit.py share no code with the pinned engine or with geo3.py; the author of the proofs wrote all of them."""
import hashlib
import json
import os
import random
import sys
import time
from fractions import Fraction as Fr

ROOT = os.path.dirname(os.path.abspath(__file__))
if "--root" in sys.argv:
    ROOT = sys.argv[sys.argv.index("--root") + 1]
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)
sys.path.insert(0, os.path.join(SRC, "engine"))

PINNED = {
    "src/engine/exact_containment.py": "97892d93", "src/engine/certificate_check.py": "7f61ff35", "src/engine/coverage_gap.py": "5efce1dc",
    "src/engine/audit_p3.py": "071fd137", "src/engine/coupled_3d.py": "fb2e535e", "src/engine/planar_residual.py": "c335b258",
    "src/engine/p2/cell_transport.py": "41bc44b4", "src/engine/p2/geometry_audit.py": "32974d4a", "src/engine/p2/graver_transport.py": "f9d05c0b",
    "src/engine/p2/lattice_transport.py": "51ce4766", "src/engine/p2/inherited/e1_cell_transport.py": "2c767b00",
    "src/engine/p2/inherited/fibre_transport.py": "7360be29",
}
V004_ZIP_SHA256 = "c0f53036ad3a582c632e81cb1b415b9002f885ce5237a79d1d050a7a1638b614"
RESULTS, FAILS = [], []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + ((" -- " + detail) if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


def shard_S0(full=False):
    for rel, h in PINNED.items():
        d = hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()
        check("S0 pinned engine module %s (byte-identical to v004)" % rel, d.startswith(h), d[:8])
    z = os.path.join(ROOT, "..", "GEO_HD_E2_P4_v004.zip")
    if os.path.exists(z):
        d = hashlib.sha256(open(z, "rb").read()).hexdigest()
        check("S0 v004 baseline zip sha256 unchanged", d == V004_ZIP_SHA256, d[:12])
    else:
        print("INFO  S0 v004 baseline zip not found next to this folder: NOT_AVAILABLE (not a failure); expected sha256 " + V004_ZIP_SHA256[:12])
    print("INFO  S0 inherited v004 verification S0-S17 (95 fast checks, full shards) = NOT_RERUN (preserved baseline, hash pins above)")


def shard_S1(full=False):
    import tiling_lemma as tl
    rng = random.Random(20261031)
    for d, cnt in ((1, 25), (2, 25), (3, 25 if not full else 80)):
        bad = tiles = 0
        for V in tl.random_configs(rng, d, cnt, 6):
            while True:
                try:
                    vo, co, nt = tl.check_configuration(V, rng)
                    break
                except ValueError:
                    continue
            tiles += nt
            bad += (not (vo and co))
        check("S1 Lemma T (lifting tiles): volume identity + coverage, d=%d, %d configurations" % (d, cnt), bad == 0, "%d tiles" % tiles)


def shard_S2(full=False):
    import mini, geo3, tiling_lemma as tl
    # L1: conformal decomposition into Graver vectors of the lattice
    E3 = geo3.hnf_rows([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
    L = geo3.hnf_rows([[2, 1, 0], [0, 3, 1], [0, 0, 5]])
    ok = True
    rng = random.Random(5)
    for B in (E3, L):
        m = lambda v, B=B: geo3.member(B, v)
        G = set(mini.graver_region(m, (6, 6, 6)))
        for _ in range(30):
            v = tuple(rng.randint(-5, 5) for _ in range(3))
            v = tuple(a * 1 for a in v)
            # force lattice membership by taking a random combination of basis rows
            c = [rng.randint(-2, 2) for _ in range(3)]
            v = tuple(sum(c[i] * B[i][j] for i in range(3)) for j in range(3))
            if any(abs(x) > 6 for x in v) or not any(v):
                continue
            parts = tl.conformal_decomposition(v, m)
            s = tuple(sum(p[j] for p in parts) for j in range(3))
            ok &= (s == v) and all(mini.conf_le(p, v) and p in G for p in parts)
    check("S2 L1 conformal Graver decomposition (E_3 and an index-30 lattice)", ok)
    # LG: adjacent corners overlap in support; H1: hard cell = sum of segments [a_i,b_i]
    for name, B, Q in (("E_3", E3, (4, 4, 4)), ("BCC", geo3.hnf_rows([[1, 1, 1], [0, 2, 0], [0, 0, 2]]), (4, 4, 4)), ("2Z^2 x Z", geo3.hnf_rows([[2, 0, 0], [0, 2, 0], [0, 0, 1]]), (4, 4, 3))):
        m = lambda v, B=B: geo3.member(B, v)
        cells, F, G = mini.cells(m, Q)
        bad = n = 0
        for u, gs in cells:
            if not gs:
                continue
            from itertools import product
            pts = {}
            for bits in product((0, 1), repeat=len(gs)):
                v = u
                for b, g in zip(bits, gs):
                    if b:
                        v = mini.add(v, g)
                pts[bits] = v
            for bits, v in pts.items():
                for i in range(len(gs)):
                    if bits[i] == 0:
                        b2 = list(bits); b2[i] = 1
                        w = pts[tuple(b2)]
                        n += 1
                        bad += (not (set(c for c in range(3) if v[c]) & set(c for c in range(3) if w[c])))
        check("S2 LG adjacent corners share a support coordinate (%s box %s)" % (name, Q), bad == 0, "%d adjacent corner pairs" % n)
    # H1 on all hard cells of a few pairs
    Bp = geo3.hnf_rows([[1, 1, 1], [0, 2, 0], [0, 0, 2]])
    cnt = bad = 0
    import numpy as np
    for M in [M for m in (2, 3, 4) for M in geo3.hnf3_enum(m)]:
        B = geo3.sublattice(Bp, M)
        G = geo3.lexpos(geo3.graver(B, (6, 6, 6)))
        for u, gens in geo3.hard_cells(G, B, Bp, (6, 6, 6)):
            a = [-np.minimum(g, 0) for g in gens]; b = [np.maximum(g, 0) for g in gens]
            ok = (np.array(u) == sum(a)).all()
            from itertools import product
            for bits in product((0, 1), repeat=len(gens)):
                corner = np.array(u) + sum((g for g, t in zip(gens, bits) if t), np.zeros(3, dtype=np.int64))
                alt = sum((b[i] if bits[i] else a[i] for i in range(len(gens))), np.zeros(3, dtype=np.int64))
                ok &= (corner == alt).all()
            ok &= all(not (set(np.nonzero(a[i])[0]) & set(np.nonzero(b[i])[0])) for i in range(len(gens)))
            cnt += 1; bad += (not ok)
    check("S2 H1 hard cell = sum of segments [a_i,b_i], a_i=-g_i^-, b_i=g_i^+ (BCC target)", bad == 0 and cnt > 0, "%d hard cells" % cnt)


def shard_S3(full=False):
    import ce_check
    for name, c in ce_check.CASES.items():
        r = ce_check.check_case(name, c)
        check("S3 %s: source cell verified from definitions, witness in C, witness NOT in U(Lambda',Q) (mini)" % name, r["FAILURE_CONFIRMED_A"],
              "axis orders %s, split %s" % (r["axis_orders_target"], r["split_coordinates_target"]))
        check("S3 %s: pinned engine NOT_CONTAINED + independent certificate check" % name, r.get("B_engine_verdict") == "NOT_CONTAINED" and r.get("B_certificate_independently_verified"),
              "engine witness %s" % (r.get("B_engine_witness"),))
        check("S3 %s: numpy complex agrees (witness uncovered)" % name, not r["C_witness_covered_float"])
    import _boot, geo3
    lm = _boot.p4("lattice_model")
    for name, c in ce_check.CONTRAST.items():
        B = tuple(map(tuple, c["B"])); Bp = tuple(map(tuple, c["Bp"]))
        r = lm.compare_lattices(lm.member3(B), lm.member3(Bp), c["Q"])
        check("S3 %s: contrast, whole union U(2E_3,Q) inside U(E_3,Q) (non-split target), engine exact" % name, r["verdict"] == "CONTAINED", r["verdict"])
    # hand proof facts of P5-C1
    import mini
    E3m = lambda v: sum(v) % 2 == 0
    G = set(mini.graver_region(E3m, (2, 2, 2)))
    expect = {(2, 0, 0), (0, 2, 0), (0, 0, 2), (-2, 0, 0), (0, -2, 0), (0, 0, -2)} | {tuple(s * a for a in v) for s in (1, -1) for v in ((1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1))}
    check("S3 Graver(E_3) = {2e_i, e_i +- e_j} (inside [-2,2]^3)", G == expect, "%d vectors" % len(G))
    p = (Fr(2, 3), Fr(5, 3), Fr(5, 3))
    check("S3 hand proof: p = u + g/6 + h/3 and p lies in the open box (0,2)^3", mini.in_cell((0, 2, 2), ((0, 2, -2), (2, -2, 0)), p) and all(0 < x < 2 for x in p))


def shard_S4(full=False):
    import _boot, ce_check, geo3
    lm = _boot.p4("lattice_model")
    # dilation invariance of verdicts: the pair (E_3 <= Z^3, Q=(1,2,1)) and diag(t) dilations, plus a contained pair
    pairs = [("fail", [[1, 0, 1], [0, 1, 1], [0, 0, 2]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], (1, 2, 1)),
             ("contained", [[2, 0, 0], [0, 2, 0], [0, 0, 2]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], (2, 2, 2))]
    for tag, B, Bp, Q in pairs:
        base = None
        for t in ((1, 1, 1), (2, 2, 2), (1, 2, 3), (3, 1, 2)):
            Bt = geo3.hnf_rows([[B[i][j] * t[j] for j in range(3)] for i in range(3)])
            Bpt = geo3.hnf_rows([[Bp[i][j] * t[j] for j in range(3)] for i in range(3)])
            Qt = tuple(Q[j] * t[j] for j in range(3))
            if max(Qt) > 8:
                continue
            r = lm.compare_lattices(lm.member3(Bt), lm.member3(Bpt), Qt)["verdict"]
            base = r if base is None else base
            check("S4 dilation invariance (%s pair, diag%s, Q=%s): verdict %s" % (tag, t, Qt, r), r == base)


def shard_S5(full=False):
    import split_slab as ss
    cases = [(((1, 0), (0, 1)), 2, (3, 2, 4)), (((1, 1), (0, 2)), 2, (3, 2, 4)), (((1, 0), (0, 2)), 3, (2, 3, 5)), (((2, 0), (0, 2)), 1, (3, 2, 4))]
    if full:
        cases += [(L2, k, Q) for L2 in (((1, 0), (0, 1)), ((1, 0), (0, 2)), ((1, 1), (0, 2)), ((2, 0), (0, 2))) for k in (1, 2, 3) for Q in ((2, 2, 3), (3, 2, 4), (2, 3, 5))]
    for L2, k, Q in cases:
        n, bad = ss.check_identity(L2, k, Q, denom=3)
        check("S5 P5-S4 union identity, planar lattice %s, period k=%d, box %s" % (L2, k, Q), bad == 0, "%d grid points" % n)


def shard_S6(full=False):
    import split_slab as ss
    st = dict(hard=0, agree=0, disagree=0, noncontained=0)
    todo = [(((1, 0), (0, 2)), 2)] + ([(((1, 1), (0, 2)), 2)] if True else [])
    for L2, k in todo:
        s, bad = ss.check_criterion(L2, k, m_list=(2,), stats=st, time_budget=60 if not full else 600)
    check("S6 P5-S4 criterion == pinned exact engine on every hard cell (split targets)", st["disagree"] == 0 and st["hard"] > 0,
          "%d hard cells, %d non-contained, %d disagreements" % (st["hard"], st["noncontained"], st["disagree"]))


def shard_S7(full=False):
    import planar_audit as pa
    st, fl = pa.audit(11, 60 if not full else 300, 14, nmax_src=9, nmax_tgt=6, time_budget=25 if not full else 120)
    check("S7 planar P5-P1: random nested pairs, all 2-cells exact polygon containment", st["failures"] == 0 and st["cells2"] > 0, "%d cells, %d hard, %d failures" % (st["cells2"], st["hard"], st["failures"]))
    st, fl = pa.hard_driven_audit(7, 3000 if not full else 12000, time_budget=40 if not full else 200, nmax_src=4, nmax_tgt=4, cap=14)
    check("S7 planar P5-P1: hard cells vs own worst box, containment + proof structure (1)-(6)", st["failures"] == 0 and st["structure_violations"] == 0 and st["hard"] > 0,
          "%d hard cells, %d failures, %d structure violations" % (st["hard"], st["failures"], st["structure_violations"]))


def shard_S8(full=False):
    import mini, geo3
    d = load("results/P5_SCAN3D_NOFREE.json")
    s = d["summary"]
    per = d["per_target"]
    check("S8 stored scan tallies consistent", s["hard_cells_total"] == sum(t["hard_cells"] for t in per) and s["noncontained"] == sum(t["noncontained_hard_cells"] for t in per) == len(d["failures"]),
          "%d hard cells, %d failing" % (s["hard_cells_total"], s["noncontained"]))
    check("S8 stored class tallies", s["split_with_failures"] == 12 == s["split"] and s["nonsplit_with_failures"] == 7 and s["targets"] == 96 and s["float_alarm"] == 0)
    check("S8 every stored target has no free coordinate", all(min(t["axis_orders"]) >= 2 for t in per))
    check("S8 split classification reproduced", all(geo3.split_coordinates(tuple(map(tuple, t["Bp"]))) == t["split_coordinates"] for t in per))
    import _boot
    lm = _boot.p4("lattice_model")
    fails = d["failures"]
    small = [f for f in fails if max(f["Qc"]) <= 6]
    sample = small if full else small[:6]
    ok_all = True
    for f in sample:
        B = tuple(map(tuple, f["B"])); Bp = tuple(map(tuple, f["Bp"])); Qc = tuple(f["Qc"])
        mB = lambda v, B=B: geo3.member(B, v); mBp = lambda v, Bp=Bp: geo3.member(Bp, v)
        okc, _ = mini.is_cell_of(mB, Qc, tuple(f["base"]) if "base" in f else tuple(f["u"]), [tuple(g) for g in f["gens"]])
        w = tuple(Fr(x) for x in f["witness"])
        tc, _, _ = mini.cells(mBp, Qc)
        ok_all &= okc and mini.in_cell(tuple(f["u"]), [tuple(g) for g in f["gens"]], w) and not mini.in_union(tc, w)
        if not full:
            r = lm.compare_lattices(lm.member3(B), lm.member3(Bp), Qc)
            ok_all &= (r["verdict"] == "NOT_CONTAINED")
    check("S8 stored failures re-verified from the definitions (%d of %d with box <= 6)%s" % (len(sample), len(fails), "" if full else " + engine"), ok_all and len(sample) > 0)


def shard_S9(full=False):
    st = load("STATUS.json")
    check("S9 C3 not claimed", st["gates"]["C3"] == "NOT_CLAIMED")
    check("S9 inherited verification recorded as NOT_RERUN with baseline hash", st["gates"]["V004_VERIFICATION"].startswith("NOT_RERUN") and V004_ZIP_SHA256[:12] in st["gates"]["V004_VERIFICATION"])
    check("S9 independence caveat present", "same author" in st["independence_caveat"])
    check("S9 3D no-free-coordinate conjecture recorded FALSE", "P5-K2" in " ".join(st["claims"]["falsified"]))
    check("S9 FIELD-I planar corollary scope correction recorded", any("Lambda_x" in c for c in st["claims"]["proved"]))


SHARDS = {"S0": shard_S0, "S1": shard_S1, "S2": shard_S2, "S3": shard_S3, "S4": shard_S4, "S5": shard_S5, "S6": shard_S6, "S7": shard_S7, "S8": shard_S8, "S9": shard_S9}

if __name__ == "__main__":
    full = "--full" in sys.argv
    if "--list" in sys.argv:
        for k, f in SHARDS.items():
            print(k, (f.__doc__ or "").strip().split("\n")[0] if f.__doc__ else "")
        sys.exit(0)
    if "--shard" in sys.argv:
        todo = [sys.argv[sys.argv.index("--shard") + 1]]
    else:
        todo = list(SHARDS)
    t0 = time.time()
    for k in todo:
        t = time.time()
        print("== shard %s ==" % k, flush=True)
        SHARDS[k](full)
        print("   (%s: %.1fs)" % (k, time.time() - t), flush=True)
    print("\nSUMMARY: %d checks, %d PASS, %d FAIL, %.0fs" % (len(RESULTS), sum(1 for r in RESULTS if r[1]), len(FAILS), time.time() - t0))
    if "--write" in sys.argv:
        json.dump([{"name": n, "ok": ok, "detail": dt} for n, ok, dt in RESULTS], open(os.path.join(ROOT, "results", "P5_VERIFY_LAST.json"), "w"), indent=1)
    sys.exit(1 if FAILS else 0)
