"""GEO-I v006, Programme A: exact certification of the *small boxes* Q=(d+r1,d+r2), 0<=r_i<d, Q != (d,d)  (the only boxes not covered by the
proved theorems G6-T1a/b).  Sufficient-family certificate: a *subfamily* of the cells of K_abs whose exact union already contains conv(F)
proves U = conv(F) (U is always contained in conv(F)).  The family used here (all members verified to be cells of K_abs before use):
  squares; sail cells with completions (0,+-d), (+-d,0) and the Pareto vectors m_j; column / row chain cells.
If the family fails for a box, the generic v005 test (coverage.uncovered, all cells) is run; nothing is ever skipped."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from math import gcd
import modular_layers as ML
from modular_layers import fibre, graver_set, make_cell, legit, covered, corner_chain, square_cells, chain_cells_vertical


def inv(s, d): return next(t for t in range(1, d + 1) if (s * t) % d == 1 % d)


def pareto_ll(d, s):
    """Pareto-minimal points of Gamma cap R^2_{>=0} \\ {0}  (the Hilbert basis of the positive quadrant), x increasing."""
    ch = []; best = None
    for x in range(0, d + 1):
        y = d if x == 0 else (s * x) % d
        if best is None or y < best: ch.append((x, y)); best = y
    return ch


def transpose_cell(c):
    u, g, h = c
    pts = [u, (u[0] + g[0], u[1] + g[1]), (u[0] + h[0], u[1] + h[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1])]
    return make_cell([(p[1], p[0]) for p in pts])


def chain_cells_horizontal(d, s, Q):
    t = inv(s, d)
    return [transpose_cell(c) for c in chain_cells_vertical(d, t, (Q[1], Q[0]))]


def family(d, s, Q):
    P = pareto_ll(d, s)
    cells = list(square_cells(d, s, Q))
    for corner in ((0, 0), (1, 0), (0, 1), (1, 1)):
        fx, fy = corner; ch = corner_chain(d, s, Q, corner)
        comps = [(0, d), (d, 0)] + [tuple(m) for m in P]
        for (a, pa), (b, pb) in zip(ch, ch[1:]):
            for h in comps:
                hh = (-h[0] if fx else h[0], -h[1] if fy else h[1])
                cells.append(make_cell([pa, pb, (pa[0] + hh[0], pa[1] + hh[1]), (pb[0] + hh[0], pb[1] + hh[1])]))
    cells += chain_cells_vertical(d, s, Q) + chain_cells_horizontal(d, s, Q)
    F = set(fibre(d, s, Q)); G = graver_set(d, s)
    return [c for c in dict.fromkeys(cells) if c and legit(d, s, Q, c, F, G)]


def certify_box(d, s, Q, fallback=True):
    cells = family(d, s, Q); ok, n = covered(d, s, Q, cells)
    if ok: return {'Q': list(Q), 'ok': True, 'method': 'family', 'cells': len(cells)}
    if not fallback: return {'Q': list(Q), 'ok': False, 'method': 'family', 'uncovered_pieces': n}
    import coverage as C
    from lattice_model import Lat
    r = C.uncovered(Lat(d, d, d, s), Q)
    return {'Q': list(Q), 'ok': (r is not None and len(r) == 0), 'method': 'generic_fallback', 'uncovered_pieces': 0 if not r else len(r)}
