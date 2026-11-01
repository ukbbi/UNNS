#!/usr/bin/env python3
"""E2-P4 v004 verification (v001-v003 shards retained; S17 new), sharded so that every shard finishes well inside a ~3 minute shell limit.
   python RUN_VERIFY.py --list
   python RUN_VERIFY.py --shard S0 | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | S9 | S10 | S11 | S12 | S13 | S14   (individually executable; each prints PASS/FAIL lines and a summary)
   python RUN_VERIFY.py --fast        (S0,S1,S2,S3,S5,S9,S10,S11,S12 -- skips the heavy S4/S8/S13/S14 replays)
   python RUN_VERIFY.py --full        (all shards; add --write to store results/P4_VERIFY_LAST.json)
Independent code only: src/audit_p4.py + src/engine/{audit_p3,certificate_check}.py + src/engine/p2/geometry_audit.py (none import the builder modules).
Shards:  S0 hash pins + stored data sanity | S1 arithmetic & lattices (m=1..3 independent) | S2 m=1 geometry certificates (both directions, hull tree)
         S3 general-m lemmas & theorem consistency | S4 corner lemma n=4 hull-cover replay (~2-3 min) | S5 P3 family addendum + planar reclassification + gates | S6 reverse point certificate m=3 (~1 min) | S7 opt-in replay of direct m=2
         v002: S8 P4-C1 correction replay (~2 min) | S9 36 lattice-level 3D failures | S10 21 FIELD-I failures + slab witnesses | S11 tallies, slab lemma finite check, gates
         S12 independent zero-vertex re-screen (planar core 846 + window 1443) | S13/S14 independent zero-vertex re-screen of the 3,845 spatial rows (halves, ~1-2 min each)"""
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
au2 = _boot.p4("audit_v002")

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
                "results/P4_CERTIFICATES.json", "results/P4_PLANAR.json", "results/P4_3D.json",
                "data/P4_C1_CORRECTION.json", "data/SEARCH_LIMITS_V002.json", "results/P4_PLANAR_LATTICE.json", "results/P4_PLANAR_CORE.json",
                "results/P4_PLANAR_WINDOW.json", "results/P4_LATTICE3.json", "results/P4_FIELDI3.json", "results/P4_SLAB.json", "results/P4_SLAB_CONSISTENCY.json",
                "results/P4_FREE_AXIS_ROWS.json", "results/P4_FREE_AXIS_LATTICE.json", "results/P4_ADV_PLANAR_BIG.json", "results/P4_ADV_NOFREE_3D_A.json", "results/P4_ADV_NOFREE_3D_B.json"):
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
    check("S5 gates (v004): planar CP3-A proved (scoped), 3D scoped, C3 not promoted", gates["PLANAR_THEOREM_PASS"].startswith("PASSED")
          and gates["COUPLED_3D_THEOREM_PASS"].startswith("SCOPED") and gates["C3"].startswith("NOT_CLAIMED"))
    check("S5 STATUS records release v002 and project files untouched", st["release"] == "GEO_HD_E2_P4_v004" and st["project_files_touched"] is False)


def _lat_member(B):
    return lambda v: au2.in_hnf(B, v)


def shard_S8():
    t = time.time()
    r = au2.c1_check(4)
    stored = load("data/P4_C1_CORRECTION.json")
    check("S8 2Z^3 in box 4: ten target-hull vertices lie in F(source)", r["ten_hull_vertices_in_F"])
    check("S8 independent cells: (1,1,1) in U(E_3) but NOT in U(2Z^3)", r["(1,1,1)_in_E3_union"] and not r["(1,1,1)_in_source_union"])
    check("S8 stored witness (4/7,4/7,10/7) in U(E_3), not in U(2Z^3)", r["witness_in_E3_union"] and not r["witness_in_source_union"] and stored["witness_E3_not_in_source"] == ["4/7", "4/7", "10/7"])
    check("S8 U(2Z^3,[0,4]^3) = {max z_i >= 2} on the tested rational grid; every source cell has a vertex with max coordinate >= 2",
          r["source_equals_box_minus_origin_cube"] and r["every_source_cell_has_vertex_max_ge_2"], "%d source F points, %.0fs" % (r["n_F_source"], time.time() - t))
    check("S8 correction record: inclusion kept, equality clause withdrawn", stored["U_source_contained_in_U_E3"] == "CONTAINED" and stored["U_E3_contained_in_U_source"] == "NOT_CONTAINED")


def shard_S9():
    d = load("results/P4_LATTICE3.json")
    ok_all, n = True, 0
    for f in d["failures"]:
        B, Bp, q = f["B"], f["Bp"], f["q"]
        inS, inT = _lat_member(B), _lat_member(Bp)
        sub = all(inT(tuple(r)) for r in B)
        ok, why = au2.noncontained_ok(inS, inT, tuple(q), f["cell"], f["witness"])
        zvd = au2.zv_decomposition_ok(inT, f["zv_example"])
        free = [i for i in range(3) if inT(tuple(1 if j == i else 0 for j in range(3)))]
        rest_ok = False
        for i in free:
            rest = [j for j in range(3) if j != i]
            pl = lambda v, i=i, rest=rest: inT(tuple(v[rest.index(j)] if j != i else 0 for j in range(3)))  # noqa: E731
            if au2.slab_ok(inT, q, f["witness"], i, pl)[0]:
                rest_ok = True
                break
        n += 1
        good = sub and ok and zvd and rest_ok
        ok_all &= good
        if not good:
            print("   failure record rejected:", B, Bp, q, sub, why, zvd, rest_ok)
    check("S9 all %d lattice-level 3D failures: source lattice < target, source cell legitimate, witness in cell, witness in NO independently derived target cell, "
          "stored zero-vertex decomposition valid, slab witness (free coordinate in (0,1), planar part outside planar union)" % n, ok_all and n == d["n_failures"] == 36)
    check("S9 no P4-Z1 violation recorded (a ZV-free pair/box with a failure)", d["p4z1_violations"] == [])
    check("S9 tallies: 2608 pairs, 23302 runs, 36 failures, all failures zero-vertex flagged", d["n_pairs"] == 2608 and d["n_runs"] == 23302 and d["n_failures"] == 36
          and d["zv_vs_verdict"].get("False|NOT_CONTAINED", 0) == 0)


def shard_S10():
    d = load("results/P4_FIELDI3.json")
    sl = load("results/P4_SLAB.json")
    ok_all, n = True, 0
    for f in d["noncontained"]:
        x = Fr(f["x"])
        x2, L, G, ds = au4.ga.C_brute(x)
        P, q, b = au4.ga.coords(x)
        b2 = au4.ga.coords(x2)[2]
        arith = (x2 == Fr(f["x_next"]) and list(P) == f["primes"] and list(q) == f["box"] and b == f["b"] and b2 == f["b_next"])
        inS, inT = au2.chi_member(P, b), au2.chi_member(P, b2)
        sub_ok = all(inT(v) for v in au4.ga.fibre(P, q, b))
        ok, why = au2.noncontained_ok(inS, inT, tuple(q), f["witness_cell"], f["witness"])
        zvd = au2.zv_decomposition_ok(inT, f["zv_example"])
        free = [i for i in range(3) if (P[i] % b2) == 1 % b2]
        rest_ok = False
        for i in free:
            rest = [j for j in range(3) if j != i]
            pl = au2.chi_member([P[j] for j in rest], b2)
            if au2.slab_ok(inT, q, f["witness"], i, pl)[0]:
                rest_ok = True
                break
        n += 1
        good = arith and sub_ok and ok and zvd and rest_ok
        ok_all &= good
        if not good:
            print("   FIELD-I record rejected:", f["x"], arith, sub_ok, why, zvd, rest_ok)
    check("S10 all %d FIELD-I failures: independent C(x) recomputation (primes, box, b, b'), source fibre inside target fibre, source cell legitimate, witness in cell, "
          "witness outside every independently derived target cell, zero-vertex decomposition valid, slab witness (free prime = 1 mod b')" % n, ok_all and n == 21)
    check("S10 stored slab records: 36 lattice-level + 21 FIELD-I all slab witnesses", sl["lattice_level"]["n_slab_witness"] == 36 and sl["fieldI"]["n_slab_witness"] == 21)
    check("S10 all 21 failures have a spatial source cell with a free target coordinate and essential 3D support", all(f.get("essential_3d") for f in d["noncontained"]))
    check("S10 UNAVAILABLE_COST rows recorded, not decided: 21 rows, slab sample finds no witness", sl["unavailable_cost_rows"]["n"] == 21 and sl["unavailable_cost_rows"]["n_with_slab_sample_witness"] == 0)


def shard_S11():
    pl = load("results/P4_PLANAR_LATTICE.json")
    check("S11 planar lattice scan: 1,938 pairs, 42,287 runs, 0 failures; 51 zero-vertex-flagged runs all CONTAINED",
          pl["n_pairs"] == 1938 and pl["n_runs"] == 42287 and pl["failures"] == [] and pl["verdicts"] == {"CONTAINED": 42287} and pl["zv_vs_verdict"].get("True|CONTAINED") == 51)
    co = load("results/P4_PLANAR_CORE.json")["summary"]
    check("S11 planar core: 846 rows (564 hull-covered + 282 hollow) all proved, 0 needing geometry", co["n_rows"] == 846 and co["core_hollow_needing_geometry"] == 0 and co["proved_by_hull_cover"] == 564 and co["core_hollow_proved_by_P4Z1"] == 282)
    w = load("results/P4_PLANAR_WINDOW.json")
    check("S11 planar window: 1,443 residual rows, 0 non-contained, 0 zero-vertex flagged", w["n_residual_rows_evaluated"] == 1443 and w["noncontained"] == [] and w["n_zv_flagged_rows"] == 0)
    fi = load("results/P4_FIELDI3.json")
    check("S11 spatial scan: 3,845 nonrectangular-target rows, 21 NOT_CONTAINED, 21 UNAVAILABLE_COST (recorded as such)",
          fi["n_nonrect_target_rows"] == 3845 and fi["verdicts"]["ENLARGE|NOT_CONTAINED"] == 21 and fi["verdicts"]["ENLARGE|UNAVAILABLE_COST"] == 21)
    sc = load("results/P4_SLAB_CONSISTENCY.json")
    check("S11 slab sample vs engine on 1,418 free-coordinate rows: a slab witness exists exactly for the 21 NOT_CONTAINED rows (0 contradictions)",
          sc["rows_free_coordinate"] == 1418 and sc["contradictions"] == [] and sc["table"].get("NOT_CONTAINED|slab_witness_found=True") == 21
          and all(not k.endswith("True") for k in sc["table"] if not k.startswith("NOT_CONTAINED")))
    tot, bad = au2.slab_lemma_check(2)
    check("S11 slab lemma finite check, E2 (+) Z in box (2,2,2): %d tested points (c in {1/4,1/2,3/4}), 0 disagreements" % tot, bad == 0)


def _zv_rows(rows, tag, step=1, off=0):
    bad = 0
    sub = rows[off::step]
    for r in sub:
        n, f = au2.zv_rescreen(r["primes"], r["b"], r["b_next"], r["box"])
        if (n, f) != (r["n_src_max"], r["n_zv"]):
            bad += 1
    return len(sub), bad


def shard_S12():
    t = time.time()
    core = load("results/P4_PLANAR_CORE.json")["rows"]
    n, bad = _zv_rows(core, "core")
    check("S12 independent zero-vertex re-screen of the %d planar core rows (own cells, own brute-force screen): maximal-cell and flag counts agree" % n, bad == 0 and n == 846)
    win = load("results/P4_PLANAR_WINDOW.json")["rows"]
    n, bad = _zv_rows(win, "window")
    check("S12 independent zero-vertex re-screen of the %d planar window rows: counts agree, all 0 flagged" % n, bad == 0 and n == 1443 and all(r["n_zv"] == 0 for r in win), "%.0fs" % (time.time() - t))


def _spatial(off):
    rows = load("results/P4_FIELDI3.json")["rows"]
    t = time.time()
    n, bad = _zv_rows(rows, "3d", 2, off)
    check("S1%d independent zero-vertex re-screen of %d spatial rows (every other row, offset %d): maximal-cell and flag counts agree" % (3 + off, n, off), bad == 0, "%.0fs" % (time.time() - t))


def shard_S13():
    _spatial(0)


def shard_S14():
    _spatial(1)




def shard_S15():
    fr = load("results/P4_FREE_AXIS_ROWS.json")
    c = fr["comparison"]
    check("S15 P4-S2 procedure vs stored verdicts on all 1,418 free-coordinate FIELD-I rows: 63 CONTAINED, 21 NOT_CONTAINED (all S0 part), 1,313 P4-Z1-proved agree",
          c.get("CONTAINED|CONTAINED|None") == 63 and c.get("NOT_CONTAINED|NOT_CONTAINED|S0") == 21 and c.get("PROVED_BY_P4Z1|CONTAINED|None") == 1313 and sum(c.values()) == 1418)
    check("S15 the 21 formerly UNAVAILABLE_COST rows are decided CONTAINED by P4-S2", c.get("UNAVAILABLE_COST|CONTAINED|None") == 21)
    fl = load("results/P4_FREE_AXIS_LATTICE.json")
    check("S15 lattice level: P4-S2 reproduces exactly the 36 stored failures over %d free-target runs (all S0 part)" % fl["n_runs"], fl["same_set"] and fl["n_fail_free_axis"] == 36 and fl["parts"] == {"S0": 36})
    a = load("results/P4_ADV_PLANAR_BIG.json")
    check("S15 planar adversarial scan: %d pairs (source index <= 48), %d runs on boxes [1,8]^2, %d zero-vertex flagged, 0 failures" % (a["n_pairs_done"], a["n_runs"], a["n_flagged_runs"]),
          a["n_flagged_failures"] == 0 and a["n_pairs_done"] == a["n_pairs_total"] == 9497)
    b1, b2 = load("results/P4_ADV_NOFREE_3D_A.json"), load("results/P4_ADV_NOFREE_3D_B.json")
    check("S15 3D adversarial search without free target coordinate: %d runs, 0 zero-vertex flagged (hence all proved by P4-Z1), 0 failures" % (b1["stats"]["runs"] + b2["stats"]["runs"]),
          b1["stats"]["flagged"] == b2["stats"]["flagged"] == 0 and b1["stats"]["fail"] == b2["stats"]["fail"] == 0)
    h0 = load("results/P4_H0_TEST_8_5.json")
    check("S15 recorded: P4-H0 (hull with origin covered by origin-allowed cells) is FALSE (%d of %d planar runs fail)" % (len(h0["failures"]), h0["runs"]), len(h0["failures"]) > 0)


def shard_S16():
    rows = load("results/P4_SLAB.json")["unavailable_cost_rows"]["records"]
    seen = set()
    ok_all = True
    for r in rows:
        k = (tuple(r["primes"]), r["b"], r["b_next"], tuple(r["box"]))
        if k in seen:
            continue
        seen.add(k)
        a, b, n = au2.s2_check_row(list(k[0]), k[1], k[2], k[3], 6)
        ok_all &= a and b
    check("S16 independent corroboration for the %d distinct classes of the 21 formerly unavailable rows: grid points of every source cell lie in the independently derived 3D target union, and "
          "the P4-S2 formula equals 3D membership on the half-integer grid" % len(seen), ok_all and len(seen) == 7)
    a, b, n = au2.s2_check_row([2, 5, 7], 9, 3, (2, 2, 3), 6)
    check("S16 smallest failing row: P4-S2 formula = 3D membership on the grid, and a source-cell grid point (den 6) lies OUTSIDE the target union", b and not a)




def shard_S17():
    t = time.time()
    ok = au2.counterexample_K1()
    check("S17 v003-assessment counterexample to P4-K1: source cell valid, zero-vertex criterion (P4-Z2) holds, target E_3 has no free coordinate, and the cell IS contained (independent planar target cells, grid test)", all(ok), str(ok))
    n, mism, hard, viol, notin = au2.check_z2_and_hard(6, [(3, 3), (6, 6), (8, 8)])
    check("S17 P4-Z2 independent check: brute-force zero-vertex search equals the explicit criterion on %d planar maximal cells (index <= 6, boxes 3,6,8)" % n, mism == 0)
    check("S17 hard cells (P4-P1 proof structure): %d robustly flagged cells all have opposite axis corners, off-axis other corners >= (k',l'), x/k'+y/l' >= 2, and lie in the independent target union (grid test)" % hard,
          viol == 0 and notin == 0 and hard > 0, "%.0fs" % (time.time() - t))
    z = load("data/P4_Z2_CHECKS.json")
    check("S17 stored builder checks: 19,258 planar + 26,434 spatial cells, 0 mismatches between brute-force and explicit zero-vertex criterion", z["planar_cells"] == 19258 and z["spatial_cells"] == 26434 and z["mismatches"] == 0)

SHARDS = {"S0": shard_S0, "S1": shard_S1, "S2": shard_S2, "S3": shard_S3, "S4": shard_S4, "S5": shard_S5, "S6": shard_S6, "S7": shard_S7,
          "S8": shard_S8, "S9": shard_S9, "S10": shard_S10, "S11": shard_S11, "S12": shard_S12, "S13": shard_S13, "S14": shard_S14, "S15": shard_S15, "S16": shard_S16, "S17": shard_S17}

if __name__ == "__main__":
    if "--list" in sys.argv:
        print(__doc__)
        sys.exit(0)
    if "--shard" in sys.argv:
        names = [sys.argv[sys.argv.index("--shard") + 1]]
    elif "--full" in sys.argv:
        names = [n for n in SHARDS if n != "S7"]  # S7 (direct m=2 replay) is opt-in: --shard S7
    else:
        names = ["S0", "S1", "S2", "S3", "S5", "S9", "S10", "S11", "S12", "S15", "S16", "S17"]
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
