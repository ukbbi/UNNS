"""GEO-I v006, Programme A.  Machine-checked cell families of the proofs of G6-T1a/b (general-s stabilization, thick and thin boxes).

SETTING (frozen, v004/v005).  Gamma = Gamma_(d,s) = {(i,j) in Z^2 : j = s*i (mod d)}, gcd(s,d)=1, d >= 2.  Box Q=(Q1,Q2) >= (d,d), Q != (d,d).
F = Gamma cap [0,Q] \\ {0}.  Cells: points, segments, parallelograms P(u;g,h) with g,h independent *Graver* vectors of Gamma and all four
corners in F.  U = union of the cells, H = conv(F).  U is always contained in H.

This module constructs, for a given (d,s,Q), the *exact list of cells used in the proof* (and nothing else):
  * SQUARES      P(u;(d,0),(0,d)),  u in Gamma, u != 0, u+(d,d) <= Q;
  * SAIL CELLS   at each of the four box corners: for the Pareto-minimal points m_0,...,m_k of the corner coset (in the corner's own
                 coordinates), consecutive differences g_i = m_{i+1}-m_i are Graver (Lemma P) and the cell P(m_i; g_i, (0,+-d)) covers the
                 right triangle (m_i, m_{i+1}, (x_{i+1}, y_i)) between the staircase and the sail;
  * CHAIN CELLS  (thin boxes Q1 < 2d only)  P(B_k; B_{k+1}-B_k, (0,d)) over the lowest points B_k of the columns, and the analogous cells over
                 the highest points of the columns, whose generators (1,s) / (1,s-d) are Graver.
and checks, in exact rational arithmetic, (i) every cell is a legitimate cell of K_abs (corners in F, Graver generators, independent) and
(ii) the exact union of exactly these cells contains conv(F).
Independent of v005's generic cell enumeration (theory/coverage.py is only reused for the elementary polygon clipping routines)."""
import os, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from math import gcd
import coverage as C
from coverage import mpq


def gamma_has(d, s, p): return (p[1] - s * p[0]) % d == 0


def fibre(d, s, Q):
    return [(i, j) for i in range(Q[0] + 1) for j in range(Q[1] + 1) if (i or j) and (j - s * i) % d == 0]


def graver_all(d, s):
    """complete Graver basis, both signs (all components in [-d,d]); brute force, used only to *check* generators."""
    cand = [(a, b) for a in range(-d, d + 1) for b in range(-d, d + 1) if (a or b) and (b - s * a) % d == 0]
    cand.sort(key=lambda g: (abs(g[0]) + abs(g[1]), g)); G = []
    for g in cand:
        if not any(h[0] * g[0] >= 0 and h[1] * g[1] >= 0 and abs(h[0]) <= abs(g[0]) and abs(h[1]) <= abs(g[1]) for h in G): G.append(g)
    return set(G)


_GCACHE = {}
def graver_set(d, s):
    if (d, s) not in _GCACHE: _GCACHE[(d, s)] = graver_all(d, s)
    return _GCACHE[(d, s)]


def lexpos(g): return g[0] > 0 or (g[0] == 0 and g[1] > 0)


def make_cell(corners):
    """four corners of a parallelogram -> (u, g, h) with u the lex-minimal corner, g,h lex-positive adjacent edge vectors."""
    S = sorted(set(corners))
    if len(S) != 4: return None
    u = S[0]; rest = S[1:]
    for o in rest:                                     # the corner opposite to u: u + o = b + c for the other two
        b, c = [x for x in rest if x != o]
        if (u[0] + o[0], u[1] + o[1]) == (b[0] + c[0], b[1] + c[1]):
            return (u, (b[0] - u[0], b[1] - u[1]), (c[0] - u[0], c[1] - u[1]))
    return None


# ----------------------------------------------------------------------------------------------------------- Pareto chains (corner sails)
def corner_chain(d, s, Q, corner):
    """Pareto-minimal points of the coset seen from a box corner, returned as ORIGINAL coordinates, ordered along the sail.
    corner = (fx,fy) in {0,1}^2: fx=1 means the x axis is reflected (corner at x=Q1).  The fibre point set is F (origin excluded)."""
    fx, fy = corner
    def orig(xp, yp): return (Q[0] - xp if fx else xp, Q[1] - yp if fy else yp)
    F = set(fibre(d, s, Q))
    chain = []; best = None
    for xp in range(0, min(Q[0], 2 * d) + 1):
        for yp in range(0, min(Q[1], 2 * d) + 1):
            p = orig(xp, yp)
            if p in F:
                if best is None or yp < best:
                    chain.append(((xp, yp), p)); best = yp
                break
    return chain                                       # list of ((x',y'), original point), x' increasing, y' decreasing


def sail_cells(d, s, Q, corner, completion):
    """cells P(m_i; g_i, completion) for consecutive Pareto points; completion in {'v','h'} (vertical (0,d) / horizontal (d,0) in primed
    coordinates, pointing INTO the box)."""
    fx, fy = corner; ch = corner_chain(d, s, Q, corner); cells = []
    sx = -1 if fx else 1; sy = -1 if fy else 1
    h = (0, sy * d) if completion == 'v' else (sx * d, 0)
    F = set(fibre(d, s, Q))
    for (a, pa), (b, pb) in zip(ch, ch[1:]):
        corners = [pa, pb, (pa[0] + h[0], pa[1] + h[1]), (pb[0] + h[0], pb[1] + h[1])]
        cells.append(make_cell(corners))
    return cells, ch


def square_cells(d, s, Q):
    out = []
    for u in fibre(d, s, Q):
        if u[0] + d <= Q[0] and u[1] + d <= Q[1]: out.append((u, (0, d), (d, 0)) if False else make_cell([u, (u[0] + d, u[1]), (u[0], u[1] + d), (u[0] + d, u[1] + d)]))
    return out


def chain_cells_vertical(d, s, Q):
    """thin boxes (Q2 >= 2d): cells over the lowest / highest point of every column; generators (1,s) or (1,s-d) and (0,d)."""
    cells = []
    low = {}; high = {}
    F = fibre(d, s, Q)
    for p in F:
        low[p[0]] = min(low.get(p[0], 10 ** 9), p[1]); high[p[0]] = max(high.get(p[0], -1), p[1])
    for k in range(Q[0]):
        if k in low and k + 1 in low:
            a, b = (k, low[k]), (k + 1, low[k + 1])
            if a[1] + d <= Q[1] and b[1] + d <= Q[1]: cells.append(make_cell([a, b, (a[0], a[1] + d), (b[0], b[1] + d)]))
            a, b = (k, high[k]), (k + 1, high[k + 1])
            if a[1] - d >= 0 and b[1] - d >= 0 and (a[1] - d or a[0]) and (b[1] - d or b[0]):
                cells.append(make_cell([a, b, (a[0], a[1] - d), (b[0], b[1] - d)]))
    return [c for c in cells if c]


def legit(d, s, Q, cell, F=None, G=None):
    u, g, h = cell
    F = F if F is not None else set(fibre(d, s, Q)); G = G if G is not None else graver_set(d, s)
    cs = [u, (u[0] + g[0], u[1] + g[1]), (u[0] + h[0], u[1] + h[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1])]
    return all(c in F for c in cs) and g in G and h in G and (g[0] * h[1] - g[1] * h[0]) != 0


def covered(d, s, Q, cells):
    """exact: conv(F) minus union of the given cells is empty ?  returns (bool, number of uncovered convex pieces)."""
    F = fibre(d, s, Q); H = C.hull(sorted(F))
    if len(H) < 3: return True, 0
    pieces = [[(mpq(x), mpq(y)) for x, y in H]]
    for (u, g, h) in sorted(cells, key=lambda c: -abs(c[1][0] * c[2][1] - c[1][1] * c[2][0])):
        bb = (min(u[0], u[0] + g[0], u[0] + h[0], u[0] + g[0] + h[0]), max(u[0], u[0] + g[0], u[0] + h[0], u[0] + g[0] + h[0]),
              min(u[1], u[1] + g[1], u[1] + h[1], u[1] + g[1] + h[1]), max(u[1], u[1] + g[1], u[1] + h[1], u[1] + g[1] + h[1]))
        hp = C.cell_halfplanes(u, g, h); new = []
        for pc in pieces:
            xs = [p[0] for p in pc]; ys = [p[1] for p in pc]
            if max(xs) < bb[0] or min(xs) > bb[1] or max(ys) < bb[2] or min(ys) > bb[3]: new.append(pc); continue
            rem = pc
            for (a, b, c) in hp:
                outp = C.clip(rem, -a, -b, -c)
                if len(outp) >= 3 and C.area2(outp) > 0: new.append(outp)
                rem = C.clip(rem, a, b, c)
                if len(rem) < 3 or C.area2(rem) <= 0: rem = None; break
        pieces = new
        if not pieces: return True, 0
    return False, len(pieces)


def proof_cells(d, s, Q):
    """the cells of the proof of G6-T1 for Q with max(Q1,Q2) >= 2d (Q >= (d,d)).  Returns (cells, regime)."""
    F = set(fibre(d, s, Q)); cells = list(square_cells(d, s, Q))
    thick = Q[0] >= 2 * d and Q[1] >= 2 * d
    if thick:
        for corner in ((0, 0), (1, 0), (0, 1), (1, 1)):
            cs, _ = sail_cells(d, s, Q, corner, 'v'); cells += cs
        return cells, 'thick'
    if Q[1] >= 2 * d:                                         # thin in x
        cells += chain_cells_vertical(d, s, Q)
        for corner in ((0, 0), (1, 0), (0, 1), (1, 1)):
            cs, _ = sail_cells(d, s, Q, corner, 'v'); cells += cs
        return cells, 'thin_x'
    if Q[0] >= 2 * d:                                         # thin in y: use the transposed lattice
        t = next(t for t in range(1, d + 1) if (s * t) % d == 1 % d)
        cT, reg = proof_cells(d, t, (Q[1], Q[0]))
        return [make_cell([(c[0][1], c[0][0]), (c[0][1] + c[1][1], c[0][0] + c[1][0]), (c[0][1] + c[2][1], c[0][0] + c[2][0]),
                           (c[0][1] + c[1][1] + c[2][1], c[0][0] + c[1][0] + c[2][0])]) for c in cT], 'thin_y'
    return None, 'small'


def verify_box(d, s, Q):
    cells, reg = proof_cells(d, s, Q)
    if cells is None: return {'Q': Q, 'regime': reg, 'ok': None}
    cells = [c for c in dict.fromkeys(cells) if c]
    F = set(fibre(d, s, Q)); G = graver_set(d, s)
    bad = [c for c in cells if not legit(d, s, Q, c, F, G)]
    if bad: return {'Q': Q, 'regime': reg, 'ok': False, 'why': 'illegal cells', 'cells': bad[:3]}
    ok, n = covered(d, s, Q, cells)
    return {'Q': Q, 'regime': reg, 'ok': ok, 'n_cells': len(cells), 'uncovered_pieces': n}
