"""E2-P3: transition pipeline (builder side): FIELD-I state -> lattices, fibres, Graver sets, cells, coverage gap,
G12-T8 / v004-S1 classification of the target, exact containment verdict.

Shares code with E2-P2 (src/p2/*, byte-identical copies, hashes pinned in RUN_VERIFY): FIELD-I step, lattice relation, region Graver
set, abstract complex.  The independent audit (audit_p3.py) re-derives all of these from scratch."""
import os
import sys
from fractions import Fraction as Fr
from itertools import product
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "p2"))
import lattice_transport as lt  # noqa: E402
import fibre_transport as ft  # noqa: E402
import graver_transport as gt  # noqa: E402
import e1_cell_transport as ct0  # noqa: E402
import exact_containment as ec  # noqa: E402


def fibre_of(P, b, q):
    return tuple(sorted(a for a in product(*[range(m + 1) for m in q]) if any(a) and lt.in_lambda(a, P, b)))


def cells_of(P, b, q):
    """Return (F, Gor, list of (base, gens)) : every cell of the abstract Graver complex as a geometric parallelotope."""
    F = fibre_of(P, b, q)
    G = gt.graver_fast(P, b, q)
    Go = ft.oriented(G)
    cx = ct0.build_complex(F, Go, len(q))
    cells = []
    for j in sorted(cx):
        for key, c in cx[j].items():
            cells.append((tuple(c.base), tuple(tuple(g) for g in c.gens)))
    return F, Go, cells


def transition(x):
    """FIELD-I transition data for a state x (Fraction): P, q, b, b2, same-coordinate check."""
    x = Fr(x)
    r = ft.C_step(x)
    x2 = r["next"]
    cd, cd2 = ft.coordinate_data(x), ft.coordinate_data(x2)
    same = cd["primes"] == cd2["primes"] and cd["box"] == cd2["box"]
    return {"x": x, "x2": x2, "P": cd["primes"], "q": cd["box"], "b": cd["b"], "b2": cd2["b"], "same_coords": same}


# ------------------------------------------------------------------ planar normalization (v004 S1) and G12-T8 classification
def _orbit_group(p, b):
    out, r = [], 1 % b
    while True:
        out.append(r)
        r = r * p % b
        if r == 1 % b:
            return out


def planar_normal_form(P, b, q):
    """v004 S1.  Returns dict with o1,o2,d,a,c,s,Qn or None when the lattice is trivial in a way the model excludes.
    Lattice = diag(a,c) * Gamma_{d,s};  Qn = (floor(q1/a), floor(q2/c)).  The identity Lambda = diag(a,c)Gamma_{d,s} is verified
    by an exhaustive check on a full period (o1 x o2 residues) before the record is returned."""
    assert len(P) == 2
    p1, p2 = P
    if b == 1:
        return {"o1": 1, "o2": 1, "d": 1, "a": 1, "c": 1, "s": 0, "Qn": tuple(q), "verified": True}
    G1, G2 = _orbit_group(p1, b), _orbit_group(p2, b)
    o1, o2 = len(G1), len(G2)
    C = sorted(set(G1) & set(G2))
    d = len(C)
    a, c = o1 // d, o2 // d
    g1, g2 = pow(p1, a, b), pow(p2, c, b)
    s = None
    for u in range(1, d + 1) if d > 1 else [1]:
        if pow(g1, u, b) == g2 % b:
            if gcd(u, d) == 1:
                s = u
                break
    if d == 1:
        s = 0
    else:
        # g2 = g1^u  =>  (i',j') in Lambda  iff  i' + u j' = 0 mod d  iff  j' = -u^{-1} i' mod d
        uinv = pow(s, -1, d)
        s = (-uinv) % d
    ok = True
    for i in range(o1):
        for j in range(o2):
            inL = lt.in_lambda((i, j), P, b)
            if i % a == 0 and j % c == 0:
                inG = (j // c - s * (i // a)) % d == 0 if d > 1 else True
            else:
                inG = False
            if inL != inG:
                ok = False
                break
        if not ok:
            break
    return {"o1": o1, "o2": o2, "d": d, "a": a, "c": c, "s": s, "Qn": (q[0] // a, q[1] // c), "verified": ok}


def classify_target_planar(P, b2, q):
    """Target-side classification under GEO-I v012 G12-T8 (+ v004 S1 scaling reduction)."""
    nf = planar_normal_form(P, b2, q)
    d, Qn = nf["d"], nf["Qn"]
    out = dict(nf)
    out["Qn"] = list(Qn)
    if not nf["verified"]:
        out["class"] = "OUTSIDE_NORMALIZED_MODEL"
        out["reason"] = "normal form identity failed exhaustive period check"
    elif d == 1:
        out["class"] = "RESIDUAL_D1_RECTANGULAR"
        out["reason"] = "d=1: target lattice is a rectangular grid; G12-T8 (d>=2) does not apply"
    elif Qn[0] >= d and Qn[1] >= d and tuple(Qn) != (d, d):
        out["class"] = "INHERITED_G12T8"
        out["reason"] = "d>=2, unit s, Q'>=(d,d), Q'!=(d,d)  =>  U'=conv F'  (G12-T8 via v004 S1)"
    elif tuple(Qn) == (d, d):
        out["class"] = "RESIDUAL_EXCEPTIONAL_HOLLOW_BOX"
        out["reason"] = "normalized target box equals (d,d)"
    else:
        out["class"] = "RESIDUAL_SUBTHRESHOLD_BOX"
        out["reason"] = "min normalized box coordinate < d"
    return out


# ------------------------------------------------------------------ one planar / spatial row
def geometric_verdict(P, b, b2, q, node_limit=20000):
    """Exact verdict for U(b) <= U(b2) on the common prime set / box, with certificates."""
    k = len(q)
    F, Go, cells = cells_of(P, b, q)
    F2, G2o, cells2 = cells_of(P, b2, q)
    assert set(F) <= set(F2)
    res = ec.decide_union(cells, cells2, k, node_limit)
    res["F"] = [list(v) for v in F]
    res["F2"] = [list(v) for v in F2]
    res["n_cells_source"], res["n_cells_target"] = len(cells), len(cells2)
    return res, F2, cells2


def coverage_gap_record(P, b2, q, F2, cells2, node_limit=50000, keep_tree=False):
    """Exact coverage-gap summary for the target.  Degenerate (collinear) F' is decided through the 1-dimensional hull segment."""
    k = len(q)
    try:
        g = ec.gap_decomposition(F2, cells2, k, node_limit)
    except ec.Exhausted as e:
        if "not full-dimensional" in str(e):
            return _degenerate_gap(F2, cells2, k)
        return {"status": "UNAVAILABLE", "reason": str(e)}
    area = sum((Fr(p["area"]) for p in g["gap_pieces"]), Fr(0)) if k == 2 else None
    rec = {"status": "OK", "hull_covered": len(g["gap_pieces"]) == 0, "n_gap_pieces": len(g["gap_pieces"]),
           "gap_area": (str(area) if area is not None else None), "covered_pieces": g["covered_pieces"],
           "gap_pieces": g["gap_pieces"]}
    if keep_tree:
        rec["hull_cover_certificate"] = {"hull_halfspaces": g["hull_halfspaces"], "tree": g["tree"],
                                         "target_maximal": g["target_maximal"]}
    return rec


def _degenerate_gap(F2, cells2, k):
    """F' contained in a line: H' is a segment [pmin,pmax]; decide whether the cells cover it."""
    pts = sorted(F2)
    if len(pts) == 1:
        return {"status": "OK", "hull_covered": True, "n_gap_pieces": 0, "gap_area": None, "covered_pieces": 1,
                "gap_pieces": [], "degenerate": "single_point"}
    d = tuple(b - a for a, b in zip(pts[0], pts[-1]))
    for p in pts:
        t = ec.cell_params(pts[0], [d], p)
        if t is None:
            return {"status": "UNAVAILABLE", "reason": "F' spans a plane inside k>2 (degenerate hull not implemented)"}
    Tmax = ec.geometric_maximal(cells2, k)
    targets = [ec.Target(b, gs, k) for b, gs in Tmax]
    dec = ec.decide_cell(pts[0], [d], targets, k)
    return {"status": "OK", "hull_covered": dec["verdict"] == "CONTAINED", "n_gap_pieces": None if dec["verdict"] == "CONTAINED" else 1,
            "gap_area": None, "covered_pieces": None, "gap_pieces": [], "degenerate": "collinear"}
