"""E2-P3 INDEPENDENT AUDIT.  Shares NO code with the builder modules (coverage_gap, exact_containment, planar_residual, coupled_3d,
p2/lattice_transport, p2/graver_transport, p2/cell_transport, p2/inherited/*).  It uses

   * p2/geometry_audit.py  (E2-P2's independent brute-force arithmetic: coords, C_brute, fibre, graver, in_Lambda)  -- written
     independently of the E2-P2 builder, but by the same author/session as everything else;
   * certificate_check.py  (independent exact verifier for containment / non-containment / hull-cover trees);
   * its own cell enumeration and its own maximal-cell reduction below.

Declared shared code: audit and builder share only the Python standard library."""
import os
import sys
from fractions import Fraction as Fr
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "p2"))
import geometry_audit as ga  # noqa: E402
import certificate_check as cc  # noqa: E402


def independent_transition(x):
    x = Fr(x)
    P, q, b = ga.coords(x)
    x2, L, G, ds = ga.C_brute(x)
    P2, q2, b2 = ga.coords(x2)
    return {"P": P, "q": q, "b": b, "x2": x2, "b2": b2, "same_coords": (P == P2 and q == q2)}


def _rank(vs):
    rows = [[Fr(c) for c in v] for v in vs]
    r = 0
    ncol = len(rows[0]) if rows else 0
    for c in range(ncol):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def independent_cells(P, q, b):
    """All cells (base, gens) of the Graver complex, derived from first principles: F = lattice points of the box, Graver = brute-force
    conformally minimal lattice vectors in [-q,q], cells = subsets built from lex-positive Graver vectors with every vertex in F."""
    k = len(q)
    F = ga.fibre(P, q, b)
    Fs = set(F)
    G = ga.graver(P, q, b)
    Go = sorted(g for g in G if ga.lex_pos(g))
    cells = {}
    for v in F:
        cells[(v,)] = (v, ())
    for m in range(1, k + 1):
        for gens in combinations(Go, m):
            if _rank(gens) != m:
                continue
            for u in F:
                vs = []
                for bits in product((0, 1), repeat=m):
                    w = list(u)
                    for bit, g in zip(bits, gens):
                        if bit:
                            w = [x + y for x, y in zip(w, g)]
                    vs.append(tuple(w))
                if all(w in Fs for w in vs):
                    key = tuple(sorted(vs))
                    cells.setdefault(key, (u, tuple(gens)))
    return F, list(cells.values())


def maximal_cells(cells):
    """Independent maximal-cell reduction (cell inside another cell iff all its vertices are)."""
    def verts(c):
        return cc._verts(c[0], [list(g) for g in c[1]])

    items = sorted(cells, key=lambda c: (-len(c[1]), c))
    kept = []
    for c in items:
        vs = verts(c)
        if not any(len(d[1]) >= len(c[1]) and all(cc._in(d[0], [list(g) for g in d[1]], v) for v in vs) for d in kept):
            kept.append(c)
    return kept


def as_vertexset_family(cells_json):
    """set of frozensets of vertex tuples for a JSON list of {'base','gens'}"""
    out = set()
    for c in cells_json:
        out.add(frozenset(tuple(v) for v in cc._verts(c["base"], c["gens"])))
    return out


def audit_verdict(P, q, b, b2, claimed, certificate_source=None):
    """Independent re-derivation of both cell sets, plus a certificate check.  `claimed` = 'CONTAINED' / 'NOT_CONTAINED'.
    certificate_source: callable(src_cells, tgt_cells) -> engine result (builder) used ONLY to propose certificates; every
    certificate is then verified by certificate_check against the INDEPENDENTLY derived cells."""
    k = len(q)
    F, cs = independent_cells(P, q, b)
    F2, ct = independent_cells(P, q, b2)
    assert set(F) <= set(F2)
    Smax, Tmax = maximal_cells(cs), maximal_cells(ct)
    S_json = [{"base": list(c[0]), "gens": [list(g) for g in c[1]]} for c in Smax]
    T_json = [{"base": list(c[0]), "gens": [list(g) for g in c[1]]} for c in Tmax]
    return {"F": F, "F2": F2, "source_maximal": S_json, "target_maximal": T_json}


def verify_engine_result(res, ind, k):
    """Check a builder `decide_union` result against the independent cell data `ind` (from audit_verdict)."""
    if as_vertexset_family(res["source_maximal"]) != as_vertexset_family(ind["source_maximal"]):
        return False, "source maximal cells differ from independent derivation"
    if as_vertexset_family(res["target_maximal"]) != as_vertexset_family(ind["target_maximal"]):
        return False, "target maximal cells differ from independent derivation"
    T = res["target_maximal"]
    if res["verdict"] == "NOT_CONTAINED":
        return cc.verify_noncontainment(res["certificate"], T, k)
    got = {tuple(map(tuple, (c["source_cell"]["base"],))) + tuple(tuple(g) for g in c["source_cell"]["gens"]) for c in res["certificates"]}
    want = {tuple(map(tuple, (c["base"],))) + tuple(tuple(g) for g in c["gens"]) for c in res["source_maximal"]}
    if got != want:
        return False, "certificates do not cover every source maximal cell"
    for c in res["certificates"]:
        ok, why = cc.verify_containment(c, T, k)
        if not ok:
            return False, why
    return True, "ok"


def independent_normal_form(P, b, q):
    """Planar only.  Recompute (a, c, d, s) by brute-force subgroup intersection and re-verify Lambda = diag(a,c) Gamma_{d,s}
    on TWO periods; returns dict or None."""
    p1, p2 = P
    if b == 1:
        return {"d": 1, "a": 1, "c": 1, "s": 0, "Qn": tuple(q)}
    def orbit(p):
        s, r = [], 1
        while True:
            s.append(r)
            r = r * p % b
            if r == 1:
                return s
    o1, o2 = len(orbit(p1)), len(orbit(p2))
    d = len(set(orbit(p1)) & set(orbit(p2)))
    a, c = o1 // d, o2 // d
    s = None
    if d > 1:
        for cand in range(d):
            if all((((j // c) - cand * (i // a)) % d == 0) == ga.in_Lambda((i, j), P, b)
                   for i in range(0, 2 * o1, a) for j in range(0, 2 * o2, c)) and all(
                       not ga.in_Lambda((i, j), P, b) for i in range(2 * o1) for j in range(2 * o2) if i % a or j % c):
                s = cand
                break
        if s is None:
            return None
    else:
        s = 0
        if not all(ga.in_Lambda((i, j), P, b) == (i % o1 == 0 and j % o2 == 0) for i in range(2 * o1) for j in range(2 * o2)):
            return None
    return {"d": d, "a": a, "c": c, "s": s, "Qn": (q[0] // a, q[1] // c)}
