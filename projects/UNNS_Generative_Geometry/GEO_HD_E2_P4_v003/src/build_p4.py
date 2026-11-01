#!/usr/bin/env python3
"""E2-P4 builder.  Usage: python src/build_p4.py [--out DIR] [--stage NAME ...] [--force] [--with-m2]
Stages are individually executable and resumable: each writes an immutable JSON file under data/ or results/ and is skipped when its
file exists (unless --force).  Stages: limits arithmetic lattices geometry_m1 lemmas corner m2 reverse planar p3family"""
import json
import os
import sys
import time
from fractions import Fraction as Fr
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _boot  # noqa: E402

af = _boot.p4("arithmetic_family")
cl = _boot.p4("coupled_lattices")
x4 = _boot.p4("exact_containment")
tg = _boot.p4("target_gap")
import coverage_gap as cg  # noqa: E402
import exact_containment as ec  # noqa: E402
import fibre_transport as ft  # noqa: E402

OUT = os.path.dirname(HERE)
STAGES = sys.argv[sys.argv.index("--stage") + 1:] if "--stage" in sys.argv else None
if "--out" in sys.argv:
    OUT = sys.argv[sys.argv.index("--out") + 1]
FORCE = "--force" in sys.argv
if STAGES:
    STAGES = [s for s in STAGES if not s.startswith("--")]
P = af.P
T0 = time.time()

LIMITS = {
    "arithmetic_m_range": [1, 12],
    "engine_cross_check_m": [1, 2, 3],          # FIELD-I engine (factor/divisor based) vs closed-form enumeration
    "geometry_direct_m": {"1": "forward+reverse exact", "2": "forward exact (opt-in stage m2, ~4-5 min)",
                          "3+": "UNAVAILABLE_COST (target cell complex too large for the exact engine; covered by P4-T1/P4-T2)"},
    "lemma_n_range": [2, 12],                    # even n for cube tiling / hull checks
    "cell_monotonicity_chain": [4, 6, 8],
    "node_limit": 400000,
    "reverse_point_certificates_m": [1, 2, 3],
    "planar": "reclassification of the E2-P3 corpus only (P4-E3 search NOT STARTED)",
    "coupled_3d_census": "NOT STARTED (spec section 14: no broad census before the preflight is certified)",
}


def log(msg):
    print("[%6.0fs] %s" % (time.time() - T0, msg), flush=True)


def dump(obj, rel):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True, default=str)


def done(rel):
    return os.path.exists(os.path.join(OUT, rel)) and not FORCE


def load(rel):
    with open(os.path.join(OUT, rel), encoding="utf-8") as fh:
        return json.load(fh)


def want(name):
    return STAGES is None or name in STAGES


# ---------------------------------------------------------------------------------------------------------- stages
def st_limits():
    dump(LIMITS, "data/SEARCH_LIMITS.json")
    log("limits recorded")


def st_arithmetic():
    if done("results/P4_ARITHMETIC.json"):
        return log("arithmetic: exists, skipped")
    rows = [af.verify_member(m) for m in range(LIMITS["arithmetic_m_range"][0], LIMITS["arithmetic_m_range"][1] + 1)]
    cross = []
    for m in LIMITS["engine_cross_check_m"]:
        r = ft.C_step(af.x_m(m))
        mine = af.field_I_step(af.x_m(m))
        cd, cd2 = ft.coordinate_data(af.x_m(m)), ft.coordinate_data(af.y_m(m))
        cross.append({"m": m, "engine_next_equals_target": r["next"] == af.y_m(m), "engine_D_equals_closed_form": tuple(sorted(ft.D(af.x_m(m)))) == tuple(mine["D"]),
                      "engine_L": str(r["L"]), "engine_G": r["G"], "primes_preserved": cd["primes"] == cd2["primes"] == P,
                      "box_preserved": cd["box"] == cd2["box"] == af.box(m)})
    out = {"family": "x_m = 2*110^(4m)/9  --C-->  110^(4m)/3", "primes": list(P), "members": rows, "engine_cross_check": cross,
           "all_members_pass": all(r["all_pass"] for r in rows),
           "all_cross_checks_pass": all(c["engine_next_equals_target"] and c["engine_D_equals_closed_form"] and c["primes_preserved"] and c["box_preserved"] for c in cross)}
    dump(out, "results/P4_ARITHMETIC.json")
    log("arithmetic: members pass=%s, engine cross-check pass=%s" % (out["all_members_pass"], out["all_cross_checks_pass"]))


def st_lattices():
    if done("data/P4_F110.json"):
        return log("lattices: exists, skipped")
    d9, d3 = cl.describe(P, 9), cl.describe(P, 3)
    out = {"primes": list(P), "lattice_9": d9, "lattice_3": d3, "relation_9_to_3": cl.relation(P, 9, 3),
           "claimed_lattice_9": "a - b + c = 0 (mod 6)", "claimed_lattice_3": "a + b + c = 0 (mod 2)",
           "both_nonrectangular": d9["nonrectangular"] and d3["nonrectangular"], "members": {}}
    for m in (1, 2, 3, 4, 5):
        q = af.box(m)
        F9 = cg.fibre_of(P, 9, q)
        F3 = cg.fibre_of(P, 3, q)
        ok9 = set(F9) == {e for e in product(range(q[0] + 1), repeat=3) if any(e) and (e[0] - e[1] + e[2]) % 6 == 0}
        ok3 = set(F3) == {e for e in product(range(q[0] + 1), repeat=3) if any(e) and sum(e) % 2 == 0}
        out["members"][str(m)] = {"box": list(q), "n_F9": len(F9), "n_F3": len(F3), "F9_matches_claimed_congruence": ok9,
                                  "F3_matches_claimed_congruence": ok3, "fibre_inclusion": set(F9) <= set(F3)}
        if m == 1:
            out["members"]["1"]["F9"] = [list(v) for v in F9]
            out["members"]["1"]["F3"] = [list(v) for v in F3]
    dump(out, "data/P4_F110.json")
    log("lattices recorded; both nonrectangular=%s" % out["both_nonrectangular"])


def st_geometry_m1():
    if done("results/P4_GEOMETRY.json") and "geometry_m1" in load("results/P4_GEOMETRY.json"):
        return log("geometry_m1: exists, skipped")
    q = af.box(1)
    r = x4.compare(P, 9, 3, q, LIMITS["node_limit"], reverse=True)
    F2 = cg.fibre_of(P, 3, q)
    cells2 = x4.side(P, 3, q)["cells"]
    gap = cg.coverage_gap_record(P, 3, q, F2, cells2, LIMITS["node_limit"], keep_tree=True)
    S = x4.side(P, 9, q)
    gap_src = cg.coverage_gap_record(P, 9, q, S["F"], S["cells"], LIMITS["node_limit"], keep_tree=False)
    res = load("results/P4_GEOMETRY.json") if os.path.exists(os.path.join(OUT, "results/P4_GEOMETRY.json")) else {}
    summary = {k: v for k, v in r.items() if k not in ("forward", "reverse")}
    summary["forward_verdict"] = r["forward"]["verdict"]
    summary["reverse_verdict"] = r["reverse"]["verdict"]
    summary["n_source_maximal"], summary["n_target_maximal"] = r["forward"]["n_source_maximal"], r["forward"]["n_target_maximal"]
    summary["target_gap"] = {k: v for k, v in gap.items() if k not in ("hull_cover_certificate",)}
    summary["target_hull_covered"] = gap["hull_covered"]
    summary["source_gap_status"] = {k: gap_src[k] for k in ("status", "hull_covered", "n_gap_pieces") if k in gap_src}
    summary["reverse_witness"] = r["reverse"].get("certificate", {}).get("witness")
    res["geometry_m1"] = summary
    dump(res, "results/P4_GEOMETRY.json")
    certs = load("results/P4_CERTIFICATES.json") if os.path.exists(os.path.join(OUT, "results/P4_CERTIFICATES.json")) else {}
    certs["m1_forward"] = {"primes": list(P), "box": list(q), "b": 9, "b_next": 3, "verdict": r["forward"]["verdict"],
                           "source_maximal": r["forward"]["source_maximal"], "target_maximal": r["forward"]["target_maximal"],
                           "certificates": r["forward"]["certificates"]}
    certs["m1_reverse"] = {"primes": list(P), "box": list(q), "b": 3, "b_next": 9, "verdict": r["reverse"]["verdict"],
                           "source_maximal": r["reverse"]["source_maximal"], "target_maximal": r["reverse"]["target_maximal"],
                           "certificate": r["reverse"].get("certificate"), "n_noncontained_source_cells": r["reverse"].get("n_noncontained_source_cells")}
    certs["m1_target_hull_cover"] = gap["hull_cover_certificate"]
    certs["m1_target_hull_cover"]["fibre"] = [list(v) for v in F2]
    dump(certs, "results/P4_CERTIFICATES.json")
    log("geometry m=1: %s (forward %s, reverse %s); target gap pieces=%s" % (r["classification"], r["forward"]["verdict"], r["reverse"]["verdict"], gap["n_gap_pieces"]))


def st_survival():
    """Abstract-cell survival (vertex sets of ALL cells, any dimension) of the source complex inside the target complex, m=1,2."""
    res = load("results/P4_GEOMETRY.json")
    if "abstract_survival" in res and not FORCE:
        return log("survival: exists, skipped")
    out = {}
    for m in (1, 2):
        q = af.box(m)
        S, T = x4.side(P, 9, q), x4.side(P, 3, q)
        ks = lambda sd: {c.key for j in sd["cx"] for c in sd["cx"][j].values()}  # noqa: E731
        a, b = ks(S), ks(T)
        out[str(m)] = {"source_cells": len(a), "persisting_in_target": len(a & b), "all_persist": a <= b}
    res["abstract_survival"] = out
    dump(res, "results/P4_GEOMETRY.json")
    log("abstract survival: %s" % out)


def st_lemmas():
    if done("data/P4_LEMMAS.json"):
        return log("lemmas: exists, skipped")
    lo, hi = LIMITS["lemma_n_range"]
    out = {"cube_tiling": {}, "hull": {}, "graver": {}, "cell_monotone": {}}
    for n in range(lo, hi + 1, 2):
        ok, det = tg.cube_tiling_lemma(n)
        out["cube_tiling"][str(n)] = {"ok": ok, **det}
        ok2, verts = tg.hull_check_e3(n)
        out["hull"][str(n)] = {"ok": ok2, "vertices": verts}
    out["graver"]["E3_graver_identical_n2_to_n8"] = all(tg.graver_equal(2, n) for n in (4, 6, 8))
    chain = LIMITS["cell_monotonicity_chain"]
    sets = {n: tg.cell_vertex_sets(n) for n in chain}
    out["cell_monotone"] = {"chain": chain, "sizes": {str(n): len(sets[n]) for n in chain},
                            "subset_4_in_6": sets[4] <= sets[6], "subset_6_in_8": sets[6] <= sets[8]}
    dump(out, "data/P4_LEMMAS.json")
    log("lemmas: cube tiling %s; hull %s; monotone %s" % (all(v["ok"] for v in out["cube_tiling"].values()), all(v["ok"] for v in out["hull"].values()),
                                                       out["cell_monotone"]["subset_4_in_6"] and out["cell_monotone"]["subset_6_in_8"]))


def st_corner():
    """Exact hull-cover certificate for E_3 at n=4 (the finite 'corner lemma' of P4-T1)."""
    certs = load("results/P4_CERTIFICATES.json") if os.path.exists(os.path.join(OUT, "results/P4_CERTIFICATES.json")) else {}
    if "n4_target_hull_cover" in certs and not FORCE:
        return log("corner: exists, skipped")
    q = (4, 4, 4)
    F2 = cg.fibre_of(P, 3, q)
    cells2 = x4.side(P, 3, q)["cells"]
    gap = cg.coverage_gap_record(P, 3, q, F2, cells2, LIMITS["node_limit"], keep_tree=True)
    cert = gap["hull_cover_certificate"]
    cert["fibre"] = [list(v) for v in F2]
    certs["n4_target_hull_cover"] = cert
    dump(certs, "results/P4_CERTIFICATES.json")
    res = load("results/P4_GEOMETRY.json") if os.path.exists(os.path.join(OUT, "results/P4_GEOMETRY.json")) else {}
    res["corner_n4"] = {"hull_covered": gap["hull_covered"], "n_gap_pieces": gap["n_gap_pieces"], "n_fibre": len(F2), "n_cells": len(cells2),
                        "n_target_maximal": len(cert["target_maximal"])}
    dump(res, "results/P4_GEOMETRY.json")
    log("corner n=4: hull_covered=%s" % gap["hull_covered"])


def st_m2():
    certs = load("results/P4_CERTIFICATES.json") if os.path.exists(os.path.join(OUT, "results/P4_CERTIFICATES.json")) else {}
    if "m2_forward" in certs and not FORCE:
        return log("m2: exists, skipped")
    q = af.box(2)
    S, T = x4.side(P, 9, q), x4.side(P, 3, q)
    t = time.time()
    fwd = ec.decide_union(S["cells"], T["cells"], 3, LIMITS["node_limit"])
    sec = round(time.time() - t, 1)
    certs["m2_forward"] = {"primes": list(P), "box": list(q), "b": 9, "b_next": 3, "verdict": fwd["verdict"], "source_maximal": fwd["source_maximal"],
                           "target_maximal": fwd["target_maximal"], "certificates": fwd.get("certificates"), "seconds": sec}
    dump(certs, "results/P4_CERTIFICATES.json")
    res = load("results/P4_GEOMETRY.json")
    res["geometry_m2"] = {"forward_verdict": fwd["verdict"], "n_source_maximal": fwd["n_source_maximal"], "n_target_maximal": fwd["n_target_maximal"],
                          "census_source": x4.census(S), "census_target": x4.census(T), "seconds": sec}
    dump(res, "results/P4_GEOMETRY.json")
    log("m=2 direct forward: %s in %ss" % (fwd["verdict"], sec))


def st_reverse():
    certs = load("results/P4_CERTIFICATES.json") if os.path.exists(os.path.join(OUT, "results/P4_CERTIFICATES.json")) else {}
    if "reverse_points" in certs and not FORCE:
        return log("reverse: exists, skipped")
    pts = {}
    for m in LIMITS["reverse_point_certificates_m"]:
        q = af.box(m)
        cert, tmax = x4.point_noncontainment(P, 3, 9, q, (2, 0, 0))
        pts[str(m)] = {"box": list(q), "b_target_union": 9, "point": [2, 0, 0], "certificate": cert, "target_maximal": tmax}
        log("reverse point certificate m=%d: %d source-union cells each with a violated inequality" % (m, len(tmax)))
    certs["reverse_points"] = pts
    dump(certs, "results/P4_CERTIFICATES.json")


def st_planar():
    """P4-E3 is NOT executed.  Only the spec-6.4 reclassification of the E2-P3 corpus (reference file shipped in data/)."""
    if done("results/P4_PLANAR.json"):
        return log("planar: exists, skipped")
    ref = os.path.join(OUT, "data", "E2P3_PLANAR_REFERENCE.json")
    if not os.path.exists(ref):
        return log("planar: reference missing (copy data/E2P3_PLANAR_REFERENCE.json first)")
    d = json.load(open(ref))
    out = {"status": "RECLASSIFICATION_ONLY__P4_E3_NOT_STARTED", "e2p2_enlarge_partition": d["partition"], "n_e2p2_enlarge": d["n_e2p2_enlarge"],
           "residual_open_targets": d["residual_open"], "inherited_note": "INHERITED_G12T8 rows: U'=H' (GEO-I v012), containment automatic",
           "rectangular_note": "RESIDUAL_D1_RECTANGULAR: settled by P3-T3/P3-T2a (corner-cube criterion)",
           "cp3a_status": "OPEN for RESIDUAL_EXCEPTIONAL_HOLLOW_BOX and RESIDUAL_SUBTHRESHOLD_BOX (finite evidence only)",
           "p3_totals": d["p3_totals"]}
    dump(out, "results/P4_PLANAR.json")
    dump({"status": "reference only; see results/P4_PLANAR.json", "p3_corpus_provenance": d["provenance"]}, "data/P4_PLANAR_CORPUS.json")
    log("planar reclassification recorded: %s" % d["partition"])


def st_p3family():
    """E2-P3 follow-up (Addendum 004): the (2,7,13) infinite family, arithmetic + witness checks for parameters a,b,c in {0,1}."""
    if done("results/P4_3D.json"):
        return log("p3family: exists, skipped")
    from math import gcd
    rows = []
    for a, b, c in product((0, 1), repeat=3):
        q = (2 + 6 * a, 2 + 3 * b, 3 + 3 * c)
        R = 2 ** q[0] * 7 ** q[1] * 13 ** q[2]
        x = Fr(2 * R * R, 9)
        D = [2 ** i * 7 ** j * 13 ** k for i, j, k in product(range(q[0] + 1), range(q[1] + 1), range(q[2] + 1))
             if (i or j or k) and (pow(2, i, 9) * pow(7, j, 9) * pow(13, k, 9)) % 9 == 1]
        L, G = 1, 0
        for d in D:
            L = L * d // gcd(L, d)
            G = gcd(G, d - 1)
        nxt = x + Fr(L * L, G)
        # witness persistence: source cell vertices in Lambda_9, cell inside the box, witness outside the target corner criterion
        u, g, h = (0, 0, 3), (0, 1, -2), (2, 0, -1)
        verts = [tuple(u[i] + s * g[i] + t * h[i] for i in range(3)) for s in (0, 1) for t in (0, 1)]
        in9 = all((pow(2, v[0], 9) * pow(7, v[1], 9) * pow(13, v[2], 9)) % 9 == 1 for v in verts)
        inbox = all(0 <= v[i] <= q[i] for v in verts for i in range(3))
        w = (Fr(4, 3), Fr(5, 6), Fr(2, 3))
        w_in_cell = w == tuple(u[i] + Fr(5, 6) * g[i] + Fr(2, 3) * h[i] for i in range(3))
        o = (2, 1, 1)  # orders of 2,7,13 mod 3 (target lattice a even)
        corner = all(w[i] < o[i] for i in range(3))
        rows.append({"abc": [a, b, c], "box": list(q), "G": G, "L_equals_R": L == R, "next_equals_R2_over_3": nxt == Fr(R * R, 3),
                     "source_cell_vertices_in_Lambda9": in9, "source_cell_in_box": inbox, "witness_in_source_cell": w_in_cell,
                     "witness_in_open_corner_cube_of_target": corner, "box_ge_target_orders": all(q[i] >= o[i] for i in range(3))})
    ok = all(r["G"] == 9 and r["L_equals_R"] and r["next_equals_R2_over_3"] and r["source_cell_vertices_in_Lambda9"] and r["source_cell_in_box"]
             and r["witness_in_source_cell"] and r["witness_in_open_corner_cube_of_target"] and r["box_ge_target_orders"] for r in rows)
    out = {"p3_infinite_family": {"definition": "q=(2+6a,2+3b,3+3c), R=2^q1 7^q2 13^q3, x=2R^2/9 -> R^2/3, primes (2,7,13)", "instances": rows,
                                  "all_instances_pass": ok, "target_rectangular": True,
                                  "note": "control only (rectangular target); see ERRATA/E2_P3_ADDENDUM_004_INFINITE_FAMILY.md"},
           "coupled_3d_census": {"status": "NOT_STARTED", "reason": "spec section 14: no broad coupled-lattice census before the P4-F110 preflight is certified"}}
    dump(out, "results/P4_3D.json")
    log("p3 family instances pass=%s" % ok)


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "results"), exist_ok=True)
    order = [("limits", st_limits), ("arithmetic", st_arithmetic), ("lattices", st_lattices), ("geometry_m1", st_geometry_m1),
             ("survival", st_survival), ("lemmas", st_lemmas), ("corner", st_corner), ("reverse", st_reverse), ("planar", st_planar), ("p3family", st_p3family)]
    if "--with-m2" in sys.argv or (STAGES and "m2" in STAGES):
        order.append(("m2", st_m2))
    for name, fn in order:
        if want(name):
            fn()
    log("build finished")
