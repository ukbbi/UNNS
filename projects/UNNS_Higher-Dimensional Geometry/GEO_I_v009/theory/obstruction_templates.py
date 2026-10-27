"""GEO-I v004, Programme B.  Finite obstruction templates.

THEOREM T-REL (relative-interior criterion).  K_abs is face-closed.  It is embedded (distinct cells meet exactly in a common face)
iff the relative interiors of any two distinct cells are disjoint.
THEOREM T-FIN (finite template criterion; G4-T3).  A *template* is a triple (A, B, delta): A, B are independent tuples of
(lex-positive) Graver vectors of Lambda and delta is a lattice point of Lambda in the open zonotope
        Z(A,B) = { sum t_i g_i - sum l_j h_j : 0 < t_i, l_j < 1 },       (A,delta) != (B,0) .
It is *forbidden*.  For a box q it is *realized* iff some u in Lambda has all corners of P(u,A) and P(u+delta,B) in [0,q] minus {0}.
Realization is an up-set in q whose minimal elements are computed here.  Hence
        K_abs(Lambda,q) embedded  <=>  q >= no minimal realization box of any forbidden template.
Proofs are in MATHEMATICS.md; this module is the exact finite algorithm."""
import os, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'experiments'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from fractions import Fraction as Fr
from math import gcd
from exactlp import lp_box
from arith import graver_complete, in_lambda, order_mod


def lexpos(g):
    for c in g:
        if c: return c > 0
    return False


def rank(vs):
    M = [[Fr(x) for x in v] for v in vs]; r = 0
    if not M: return 0
    n = len(M[0])
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


class Lattice:
    """relation lattice of residues res mod b (any k).  member(alpha) and the complete Graver basis."""
    def __init__(self, res, b):
        self.res, self.b, self.k = tuple(res), b, len(res)
        self.o = [order_mod(r, b) for r in res]
        self.G = graver_complete(res, b)
        self.P = sorted(g for g in self.G if lexpos(g))
    def member(self, a): return in_lambda(self.res, self.b, a)
    @property
    def key(self): return (self.b, self.res)


class LatticeFromLat(Lattice):
    """k = 2 general modular model (o1,o2,d,s) (see lattice_model.Lat)."""
    def __init__(self, L):
        self.L, self.k, self.o = L, 2, [L.o1, L.o2]
        self.res, self.b = None, None
        self.G = L.graver_complete(); self.P = sorted(g for g in self.G if lexpos(g))
    def member(self, a): return a in self.L
    @property
    def key(self): return ('Lat', self.L.o1, self.L.o2, self.L.d, self.L.s)


def independent_subsets(P, k):
    out = []
    def rec(start, cur):
        for i in range(start, len(P)):
            nxt = cur + [i]
            if rank([P[j] for j in nxt]) == len(nxt):
                out.append(tuple(nxt))
                if len(nxt) < k: rec(i + 1, nxt)
    rec(0, [])
    return out


def _gens(A, B): return [tuple(g) for g in A] + [tuple(-c for c in h) for h in B]


def _solve_unique(W, delta):
    """W independent (rows = generators).  Returns the unique t with sum t_m W_m = delta, or None if delta is not in the span."""
    m, n = len(W), len(delta)
    M = [[Fr(W[j][i]) for j in range(m)] + [Fr(delta[i])] for i in range(n)]
    r = 0; piv = []
    for c in range(m):
        p = next((i for i in range(r, n) if M[i][c] != 0), None)
        if p is None: return None
        M[r], M[p] = M[p], M[r]; pv = M[r][c]; M[r] = [v / pv for v in M[r]]
        for i in range(n):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    if any(M[i][m] != 0 for i in range(r, n)): return None
    return [M[i][m] for i in range(m)]


def in_open_zonotope(delta, W, independent=None):
    """delta in relint { sum t_m w_m : t in [0,1]^m }  (exact).  W: list of generator vectors."""
    m, n = len(W), len(delta)
    if m == 0: return all(c == 0 for c in delta)
    # coordinatewise necessary test
    for i in range(n):
        lo = sum(min(0, w[i]) for w in W); hi = sum(max(0, w[i]) for w in W)
        if lo == hi:
            if delta[i] != lo: return False
        elif not (lo < delta[i] < hi): return False
    if independent is None: independent = rank(W) == m
    if independent:
        t = _solve_unique(W, delta)
        return t is not None and all(0 < x < 1 for x in t)
    c0 = [Fr(sum(w[i] for w in W), 2) for i in range(n)]
    dc = [Fr(delta[i]) - c0[i] for i in range(n)]
    A = [[Fr(W[j][i]) for j in range(m)] + [-dc[i]] for i in range(n)]
    st, val, z = lp_box(A, [Fr(x) for x in delta], [0] * m + [1], m + 1)
    return st == 'optimal' and val > 0


def zonotope_box(W, k):
    lo = [sum(min(0, w[i]) for w in W) for i in range(k)]; hi = [sum(max(0, w[i]) for w in W) for i in range(k)]
    return lo, hi


def corners(u, A):
    pts = [tuple(u)]
    for g in A: pts = pts + [tuple(a + b for a, b in zip(p, g)) for p in pts]
    return pts


def min_boxes(lat, A, B, delta, ucap=2):
    """minimal boxes q in which the template (A,B,delta) is realized: all corners in [0,q]^k \\ {0}, base u in Lambda."""
    k = lat.k
    C = corners((0,) * k, A) + corners(tuple(delta), B)
    lo = [min(c[i] for c in C) for i in range(k)]; hi = [max(c[i] for c in C) for i in range(k)]
    excluded = {tuple(-x for x in c) for c in C}                      # u that puts a corner on the origin
    rng = [range(-lo[i], -lo[i] + (ucap + 1) * lat.o[i] + 1) for i in range(k)]
    cand = []
    for u in itertools.product(*rng):
        if u in excluded or not lat.member(u): continue
        cand.append(tuple(u[i] + hi[i] for i in range(k)))
    cand = sorted(set(cand), key=lambda q: (sum(q), q))
    mins = []
    for q in cand:
        if not any(all(m[i] <= q[i] for i in range(k)) for m in mins): mins.append(q)
    return mins


def classify(lat, A, B, delta):
    """geometric kind of a forbidden template (dimension pair and whether an edge is a chord of the other cell)."""
    r, s = len(A), len(B)
    if r > s: A, B, delta, r, s = B, A, tuple(-x for x in delta), s, r
    if r == 1 and s == 1: return 'O-E' if tuple(A[0]) != tuple(B[0]) and rank([A[0], B[0]]) == 2 else 'O-E(parallel)'
    if r == 1:
        # edge [0,g] vs cell P(delta,B): is it a chord (both endpoints are vertices of the cell)?
        verts = set(corners(tuple(delta), B)); e0, e1 = (0,) * lat.k, tuple(A[0])
        # and the edge may lie in either orientation inside the cell
        return 'O-D' if (e0 in verts and e1 in verts) else 'O-T'
    return 'O-C'


def templates(lat, maxdim=None, progress=None):
    """all forbidden templates of the lattice (up to the symmetry (A,B,delta) ~ (B,A,-delta))."""
    k = lat.k; P = lat.P; maxdim = maxdim or k
    subs = [t for t in independent_subsets(P, k) if len(t) <= maxdim]
    out = []
    for ia, ta in enumerate(subs):
        A = [P[i] for i in ta]
        for tb in subs[ia:]:
            B = [P[i] for i in tb]
            W = _gens(A, B); lo, hi = zonotope_box(W, k); indep = rank(W) == len(W)
            for d in itertools.product(*[range(lo[i], hi[i] + 1) for i in range(k)]):
                if not any(d) or not lat.member(d):
                    if not any(d) and ta != tb: pass
                    else: continue
                if ta == tb and not lexpos(d): continue           # (A,A,delta)~(A,A,-delta)
                if ta == tb and not any(d): continue
                if not in_open_zonotope(d, W, indep): continue
                out.append({'A': A, 'B': B, 'delta': d})
    return out


def obstruction_atlas(lat, maxdim=None):
    """forbidden templates with their kind and minimal realization boxes, plus the global antichain of minimal obstruction boxes."""
    ts = templates(lat, maxdim)
    for t in ts:
        t['kind'] = classify(lat, t['A'], t['B'], t['delta'])
        t['min_boxes'] = min_boxes(lat, t['A'], t['B'], t['delta'])
        sup = sorted({i for v in t['A'] + t['B'] for i in range(lat.k) if v[i]})
        t['support'] = sup
        t['span_dim'] = rank(t['A'] + t['B'])
    allmins = sorted({q for t in ts for q in t['min_boxes']}, key=lambda q: (sum(q), q))
    anti = []
    for q in allmins:
        if not any(all(m[i] <= q[i] for i in range(lat.k)) for m in anti): anti.append(q)
    return ts, anti


def embedded_by_templates(anti, q): return not any(all(m[i] <= q[i] for i in range(len(q))) for m in anti)
