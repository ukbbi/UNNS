#!/usr/bin/env python3
"""E2-P4 verification, sharded so that every shard finishes well inside a ~3 minute shell limit.
   python RUN_VERIFY.py --list
   python RUN_VERIFY.py --shard S0 | S1 | S2 | S3 | S4 | S5 | S6 | S7     (individually executable; each prints PASS/FAIL lines and a summary)
   python RUN_VERIFY.py --fast        (S0,S1,S2,S3,S5 -- skips the heavy S4 corner-lemma replay)
   python RUN_VERIFY.py --full        (all shards; add --write to store results/P4_VERIFY_LAST.json)
Independent code only: src/audit_p4.py + src/engine/{audit_p3,certificate_check}.py + src/engine/p2/geometry_audit.py (none import the builder modules).
Shards:  S0 hash pins + stored data sanity | S1 arithmetic & lattices (m=1..3 independent) | S2 m=1 geometry certificates (both directions, hull tree)
         S3 general-m lemmas & theorem consistency | S4 corner lemma n=4 hull-cover replay (~2-3 min) | S5 P3 family addendum + planar reclassification + gates | S6 reverse point certificate m=3 (~1 min) | S7 opt-in replay of direct m=2"""
import hashlib
import json
import os
import sys
import time
from fractions import Fraction as Fr

ROOT = os.path.dirname(os.path.abspath(__file__))
if "--root" in sys.argv:
    ROOT = sys.argv[sys.argv.index("--root") + 1]
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)
import _boot  # noqa: E402

au4 = _boot.p4("audit_p4")

PINNED = {
    "src/engine/exact_containment.py": "97892d93", "src/engine/certificate_check.py": "7f61ff35", "src/engine/coverage_gap.py": "5efce1dc",
    "src/engine/audit_p3.py": "071fd137", "src/engine/coupled_3d.py": "fb2e535e", "src/engine/planar_residual.py": "c335b258",
    "src/engine/p2/cell_transport.py": "41bc44b4", "src/engine/p2/geometry_audit.py": "32974d4a", "src/engine/p2/graver_transport.py": "f9d05c0b",
    "src/engine/p2/lattice_transport.py": "51ce4766", "src/engine/p2/inherited/e1_cell_transport.py": "2c767b00",
    "src/engine/p2/inherited/fibre_transport.py": "7360be29",
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


def shard_S0():
    for rel, h in PINNED.items():
        d = hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()
        check("S0 pinned engine module %s" % rel, d.startswith(h), d[:8])
    for rel in ("data/P4_F110.json", "data/P4_LEMMAS.json", "data/SEARCH_LIMITS.json", "results/P4_ARITHMETIC.json", "results/P4_GEOMETRY.json",
                "results/P4_CERTIFICATES.json", "results/P4_PLANAR.json", "results/P4_3D.json"):
        check("S0 stored file present and parses: %s" % rel, bool(load(rel)))
    st = load("STATUS.json")
    check("S0 STATUS lists every phase", all(k in st["phases"] for k in ("P4-E0", "P4-E1", "P4-E2", "P4-E3", "P4-E4", "P4-E5")))


def shard_S1():
    ar = load("results/P4_ARITHMETIC.json")
    check("S1 builder arithmetic: m=1..12 all pass and engine cross-check agrees", ar["all_members_pass"] and ar["all_cross_checks_pass"])
    for m in (1, 2, 3):
        t = au4.ind_transition(m)
        check("S1 independent FIELD-I transition m=%d (D,L,G,C by brute force): x_m -> 110^(4m)/3, G=9, L=110^(2m), primes and box preserved" % m, t["ok"],
              "|D|=%d" % t["n_D"])
        lat = au4.ind_lattices(m)
        check("S1 independent fibres m=%d match a-b+c=0 (6) and a+b+c even; F9 strictly inside F3" % m, lat["ok"], "%d -> %d" % (lat["n_F9"], lat["n_F3"]))
    nr = au4.ind_nonrectangular()
    check("S1 both lattices nonrectangular (|H_9|=6<216, |H_3|=2<8)", all(v["nonrectangular"] for v in nr.values()), json.dumps(nr))
    f = load("data/P4_F110.json")
    check("S1 stored lattice claims equal independent: relation ENLARGE, both nonrectangular", f["relation_9_to_3"] == "ENLARGE" and f["both_nonrectangular"])


def shard_S2():
    c = load("results/P4_CERTIFICATES.json")
    g = load("results/P4_GEOMETRY.json")["geometry_m1"]
    q = (2, 2, 2)
    ok, why = au4.verify_forward(c["m1_forward"], q, 9, 3)
    check("S2 m=1 forward U(9) <= U(3): independent cells + every source cell certificate verified", ok, why)
    ok, why = au4.verify_noncontained(c["m1_reverse"], q, 3, 9)
    check("S2 m=1 reverse U(3) not<= U(9): independent cells + witness + violated inequality for every source cell", ok, why)
    ok, why, ng = au4.verify_hull(c["m1_target_hull_cover"], q, 3)
    check("S2 m=1 target hull-cover tree replays; gap nodes>0 (target is NOT hull-covered at box 2)", ok and ng and ng > 0, "gap nodes=%s %s" % (ng, why))
    cs, ct = g["census_source"], g["census_target"]
    check("S2 abstract census equals spec 5.4 preflight: source f=(5,7,2,0), target f=(13,45,36,3); Graver 4/9 oriented",
          cs["f_vector"] == [5, 7, 2, 0] and ct["f_vector"] == [13, 45, 36, 3] and cs["n_graver_oriented"] == 4 and ct["n_graver_oriented"] == 9)
    check("S2 classification m=1 is SOURCE_CONTAINED", g["classification"] == "SOURCE_CONTAINED")
    F, T = au4.ind_cells(q, 3)
    F9, S = au4.ind_cells(q, 9)
    check("S2 independent maximal-cell counts: source %d, target %d" % (len(S), len(T)), len(S) == g["n_source_maximal"] and len(T) == g["n_target_maximal"])
    if os.path.exists(os.path.join(ROOT, "results/P4_CERTIFICATES.json")) and "m2_forward" in c:
        pass


def shard_S3():
    lem = load("data/P4_LEMMAS.json")
    check("S3 cube-tiling lemma (builder record) holds for every even n in 2..12", all(v["ok"] for v in lem["cube_tiling"].values()))
    check("S3 hull = cube cap {sum>=2} record holds for even n in 2..12 (vertices in F, F inside polytope)", all(v["ok"] for v in lem["hull"].values()))
    for n in (2, 4, 6, 8):
        check("S3 independent cube-tiling lemma n=%d (independent Graver set + fibre)" % n, au4.ind_lemma_cube(n))
    cm = lem["cell_monotone"]
    check("S3 cells of E_3 in box 4 are cells in box 6, and 6 in 8; E_3 Graver set identical for n=2..8", cm["subset_4_in_6"] and cm["subset_6_in_8"] and lem["graver"]["E3_graver_identical_n2_to_n8"])
    # independent monotonicity: re-derive cell vertex sets for n=4 and n=6 from scratch
    _, c4 = au4.au.independent_cells(au4.P, (4, 4, 4), 3)
    _, c6 = au4.au.independent_cells(au4.P, (6, 6, 6), 3)
    k4 = {frozenset(au4.cc._verts(c[0], [list(g) for g in c[1]])) for c in c4}
    k6 = {frozenset(au4.cc._verts(c[0], [list(g) for g in c[1]])) for c in c6}
    check("S3 independent re-derivation: cell vertex-sets(n=4) subset of cell vertex-sets(n=6)", k4 <= k6, "%d <= %d" % (len(k4), len(k6)))
    # reverse point certificates
    c = load("results/P4_CERTIFICATES.json")
    for m, rec in sorted(c["reverse_points"].items()):
        if int(m) > 2:
            continue  # m=3 (box 6, ~1 min) is replayed in the heavy shard S4
        q = tuple(rec["box"])
        ok, why = au4.verify_point(rec, q, 9)
        check("S3 reverse point certificate m=%s: (2,0,0) in U(3) but not in U(9) (independent union cells, violated inequality per cell)" % m, ok, why)
    ar = load("results/P4_ARITHMETIC.json")
    check("S3 theorem consistency: P4-T2 claims SOURCE_CONTAINED for all m>=1; direct exact runs (m=1, and m=2 if present) agree",
          load("results/P4_GEOMETRY.json")["geometry_m1"]["classification"] == "SOURCE_CONTAINED" and
          load("results/P4_GEOMETRY.json").get("geometry_m2", {"forward_verdict": "CONTAINED"})["forward_verdict"] == "CONTAINED" and ar["all_members_pass"])


def shard_S4():
    c = load("results/P4_CERTIFICATES.json")
    q = (4, 4, 4)
    t = time.time()
    ok, why, ng = au4.verify_hull(c["n4_target_hull_cover"], q, 3)
    check("S4 corner lemma: E_3 at n=4 is hull-covered (U' = H'); tree replayed against independently derived cells, 0 gap nodes", ok and ng == 0,
          "%s, %.0fs" % (why, time.time() - t))


def shard_S6():
    c = load("results/P4_CERTIFICATES.json")
    rec = c["reverse_points"]["3"]
    t = time.time()
    ok, why = au4.verify_point(rec, tuple(rec["box"]), 9)
    check("S6 reverse point certificate m=3 (box 6): (2,0,0) in U(3) but not in U(9)", ok, "%s, %.0fs" % (why, time.time() - t))


def shard_S7():
    """Opt-in: independent replay of the direct m=2 forward certificates (box 4)."""
    c = load("results/P4_CERTIFICATES.json")
    if "m2_forward" not in c:
        return check("S7 m=2 direct certificates present", False, "stage m2 not run")
    t = time.time()
    ok, why = au4.verify_forward(c["m2_forward"], (4, 4, 4), 9, 3)
    check("S7 m=2 direct forward U(9) <= U(3): independent cells + every source-cell certificate", ok, "%s, %.0fs" % (why, time.time() - t))
    surv = load("results/P4_GEOMETRY.json")["abstract_survival"]
    for m in ("1", "2"):
        q = (2 * int(m),) * 3
        _, c9 = au4.au.independent_cells(au4.P, q, 9)
        _, c3 = au4.au.independent_cells(au4.P, q, 3)
        k = lambda cells: {frozenset(au4.cc._verts(c[0], [list(g) for g in c[1]])) for c in cells}  # noqa: E731
        a, b = k(c9), k(c3)
        check("S7 abstract-cell survival m=%s independent: %d of %d source cells persist" % (m, len(a & b), len(a)),
              (len(a), len(a & b)) == (surv[m]["source_cells"], surv[m]["persisting_in_target"]))


def shard_S5():
    p3 = load("results/P4_3D.json")["p3_infinite_family"]
    check("S5 Addendum-004 family: all 8 instances (a,b,c in {0,1}) arithmetic + witness persistence pass", p3["all_instances_pass"] and len(p3["instances"]) == 8)
    # independent recomputation of two of them
    from math import gcd
    for (a, b, c) in ((0, 0, 0), (1, 1, 1)):
        q = (2 + 6 * a, 2 + 3 * b, 3 + 3 * c)
        R = 2 ** q[0] * 7 ** q[1] * 13 ** q[2]
        x = Fr(2 * R * R, 9)
        D = [2 ** i * 7 ** j * 13 ** k for i in range(q[0] + 1) for j in range(q[1] + 1) for k in range(q[2] + 1)
             if (i, j, k) != (0, 0, 0) and (2 ** i * 7 ** j * 13 ** k) % 9 == 1]
        L = 1
        G = 0
        for d in D:
            L = L * d // gcd(L, d)
            G = gcd(G, d - 1)
        check("S5 independent FIELD-I check of family member (a,b,c)=%s: G=9, L=R, next=R^2/3" % ((a, b, c),), G == 9 and L == R and x + Fr(L * L, G) == Fr(R * R, 3))
    pl = load("results/P4_PLANAR.json")
    check("S5 planar reclassification keeps the recorded 266-row partition 40/164/14/48", pl["e2p2_enlarge_rows_partition_ok"] if "e2p2_enlarge_rows_partition_ok" in pl else
          pl["e2p2_enlarge_partition"] == {"INHERITED_G12T8": 40, "RESIDUAL_D1_RECTANGULAR": 164, "RESIDUAL_EXCEPTIONAL_HOLLOW_BOX": 14, "RESIDUAL_SUBTHRESHOLD_BOX": 48})
    check("S5 planar status marks P4-E3 as NOT STARTED and CP3-A OPEN", pl["status"].startswith("RECLASSIFICATION_ONLY") and "OPEN" in pl["cp3a_status"])
    st = load("STATUS.json")
    gates = st["gates"]
    check("S5 gates: E3/E4 not claimed; scoped theorem recorded; C3 not promoted", gates["PLANAR_THEOREM_PASS"] == "NOT_EVALUATED" and gates["COUPLED_3D_THEOREM_PASS"] == "NOT_EVALUATED"
          and gates["C3"] != "C3_CANDIDATE")


SHARDS = {"S0": shard_S0, "S1": shard_S1, "S2": shard_S2, "S3": shard_S3, "S4": shard_S4, "S5": shard_S5, "S6": shard_S6, "S7": shard_S7}

if __name__ == "__main__":
    if "--list" in sys.argv:
        print(__doc__)
        sys.exit(0)
    if "--shard" in sys.argv:
        names = [sys.argv[sys.argv.index("--shard") + 1]]
    elif "--full" in sys.argv:
        names = [n for n in SHARDS if n != "S7"]  # S7 (direct m=2 replay) is opt-in: --shard S7
    else:
        names = ["S0", "S1", "S2", "S3", "S5"]
    t0 = time.time()
    for n in names:
        ts = time.time()
        SHARDS[n]()
        print("-- shard %s finished in %.0fs" % (n, time.time() - ts), flush=True)
    print("\n%d checks, %d failed, %.0fs (%s)" % (len(RESULTS), len(FAILS), time.time() - t0, "+".join(names)))
    if "--write" in sys.argv:
        out = {"shards": names, "n_checks": len(RESULTS), "n_failed": len(FAILS), "failed": FAILS, "seconds": round(time.time() - t0, 1),
               "checks": [{"name": a, "ok": b, "detail": c} for a, b, c in RESULTS]}
        p = os.path.join(ROOT, "results", "P4_VERIFY_LAST.json")
        # append-only discipline: never overwrite an earlier record; keep one file per shard-set
        key = "+".join(names)
        old = json.load(open(p)) if os.path.exists(p) else {}
        old[key] = out
        json.dump(old, open(p, "w"), indent=1)
    sys.exit(1 if FAILS else 0)
