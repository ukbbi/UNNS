"""GEO-I v008, Programme D: COVER / GAP certificate construction.  Exact rational arithmetic (gmpy2 mpq if present, else Fraction), via the v005 clip routines.

cover_certificate(d,s,Q): all Graver parallelograms with corners in F are enumerated (coverage.complex_data), then conv(F) is subdivided by successive subtraction:
 for each cell (largest first) the part of the not-yet-covered convex pieces inside the cell becomes a certificate piece tagged with the cell; the rest stays uncovered.
 Returns (certificate_dict or None, leftover_pieces).  A non-empty leftover is an exact counterexample candidate: gap_certificate() extracts a point of it.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
import coverage as C
from lattice_model import Lat


def _fr(x): return str(x)


def cover_certificate(d, s, Q, keep_unused=False):
    cd = C.complex_data(Lat(d, d, d, s), Q)
    F = sorted(cd['F']); Hv = C.hull(F)
    cells = [(u, g, h) for (u, (g, h)) in cd['cells'][2]]
    cells.sort(key=lambda c: -abs(c[1][0] * c[2][1] - c[1][1] * c[2][0]))
    rem = [[(C.mpq(x), C.mpq(y)) for x, y in Hv]]; pieces = []; used = {}
    for idx, (u, g, h) in enumerate(cells):
        hp = C.cell_halfplanes(u, g, h); new = []
        for pc in rem:
            r = pc
            for (a, b, c) in hp:
                o = C.clip(r, -a, -b, -c)
                if len(o) >= 3 and C.area2(o) > 0: new.append(o)
                r = C.clip(r, a, b, c)
                if len(r) < 3 or C.area2(r) <= 0: r = None; break
            if r is not None and len(r) >= 3 and C.area2(r) > 0:
                used.setdefault(idx, len(used)); pieces.append((idx, r))
        rem = new
        if not rem: break
    if rem: return None, rem
    order = sorted(used, key=lambda i: used[i]); cl = [cells[i] for i in order]
    cert = {'kind': 'COVER', 'claim': 'conv(F) = union of pieces, each inside a cell of K_abs', 'method': 'v008 all-cells successive subtraction (theory/cell_cover.py)',
            'd': d, 's': s, 'Q': list(Q), 'hull': [[x, y] for x, y in Hv],
            'cells': [[list(u), list(g), list(h)] for (u, g, h) in cl],
            'incidence': [[list(p) for p in (u, (u[0] + g[0], u[1] + g[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1]), (u[0] + h[0], u[1] + h[1]))] for (u, g, h) in cl],
            'pieces': [{'cell': used[i], 'poly': [[_fr(x), _fr(y)] for x, y in p]} for i, p in pieces]}
    return cert, []


def gap_certificate(d, s, Q, accept=None):
    """if conv(F) != U return a GAP certificate with an exact point z of a leftover (2-cell-uncovered) piece, else None.
    1-cells (Graver segments) may cross leftover pieces, so candidates (centroids of fan triangles, then midpoints) are tried until accept(cert) holds
    (accept = a standalone checker, e.g. checker8.check_GAP)."""
    pcs = C.uncovered(Lat(d, d, d, s), Q)
    if not pcs: return None
    cands = []
    for p in sorted(pcs, key=lambda q: -C.area2(q)):
        n = len(p); cands.append((sum(v[0] for v in p) / n, sum(v[1] for v in p) / n))
        for i in range(1, n - 1):
            tri = (p[0], p[i], p[i + 1]); cands.append((sum(v[0] for v in tri) / 3, sum(v[1] for v in tri) / 3))
        for a in range(n):
            for b in range(a + 1, n):
                m = ((p[a][0] + p[b][0]) / 2, (p[a][1] + p[b][1]) / 2); cands.append(((m[0] + sum(v[0] for v in p) / n) / 2, (m[1] + sum(v[1] for v in p) / n) / 2))
    for z in cands:
        cert = {'kind': 'GAP', 'claim': 'z in conv(F) and z in no cell: U != conv(F)', 'd': d, 's': s, 'Q': list(Q), 'z': [_fr(z[0]), _fr(z[1])]}
        if accept is None or accept(cert)[0]: return cert
    return None


def homology_certificate(d, s, Q):
    """chain complex of the exact planar arrangement of the cover cells of U (lattice_model.U_betti route), exported for checker8 kind HOMOLOGY."""
    from lattice_model import U_betti
    b, (info, sub) = U_betti(Lat(d, d, d, s), Q, want_sub=True)
    V = sub['vertices']; E = sub['edges']; Fc = sub['faces']; vi = {v: i for i, v in enumerate(V)}
    edges = [[vi[a], vi[b2]] for (a, b2) in E]
    faces = [[vi[v] for v in cyc] for cyc in Fc]
    bb = list(b) + [0] * (3 - len(b))
    return {'kind': 'HOMOLOGY', 'claim': 'Betti numbers of the planar subdivision of U', 'd': d, 's': s, 'Q': list(Q), 'vertices': [[_fr(x), _fr(y)] for x, y in V],
            'edges': edges, 'faces': faces, 'betti': [int(x) for x in bb[:3]]}
