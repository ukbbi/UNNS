#!/usr/bin/env python3
"""GEO-I v007 standalone certificate checker (D1-D3).  Uses ONLY the Python standard library (fractions, itertools, json); imports nothing from this release.
   python3 checker.py FILE.json [FILE2.json ...]        exit status 0 iff every certificate is VALID.
Certificate kinds (field 'kind'):
 D1_coverage   : lattice (d,s), box Q, list of cells [u,g,h] and a SUBDIVISION of conv(F): convex pieces [[(x,y),...],...] each tagged with the index of a cell.
                 VALID iff: F recomputed; every cell has corners in F and independent Graver generators (conformal-minimality recomputed); every piece is a convex polygon
                 (vertices as 'a/b' strings) contained in its cell; pieces have pairwise disjoint interiors; sum of piece areas == area(conv F)  (hence conv F = union of
                 the pieces subset U).
 D2_rank       : binary columns (list of ints, F_2^m as bitmasks); claim: box 1^n is MINIMAL non-embedded and the minimum witness rank equals 'min_rank';
                 checker recomputes codewords/circuits, cells with union U as (circuit partition, coset), collisions, deletions and ranks (exact rational Gaussian elimination).
                 Also exhibits the shared point z (1/2 on U, x outside U) and verifies z lies in both cells' relative interiors.
 D3_hollow     : (d,s), claim beta_1(U) >= 2 via the two-triangle certificate; checker recomputes F, all Graver segments and parallelogram cells and the exact tests.
"""
import sys, json, itertools
from fractions import Fraction as Fr
from math import gcd


def fr(x): return Fr(x) if not isinstance(x, str) else Fr(x)
def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


# ------------------------------------------------------------------ lattice basics
def in_gamma(d, s, p): return (p[1] - s * p[0]) % d == 0
def fibre(d, s, Q): return [(i, j) for i in range(Q[0] + 1) for j in range(Q[1] + 1) if (i or j) and in_gamma(d, s, (i, j))]
def is_graver(d, s, g):
    if g == (0, 0) or not in_gamma(d, s, g): return False
    sa = 1 if g[0] >= 0 else -1; sb = 1 if g[1] >= 0 else -1
    return not any((a, b) not in ((0, 0), (abs(g[0]), abs(g[1]))) and in_gamma(d, s, (sa * a, sb * b)) for a in range(abs(g[0]) + 1) for b in range(abs(g[1]) + 1))
def hull(P):
    P = sorted(set(P))
    if len(P) < 3: return P
    def half(pts):
        h = []
        for p in pts:
            while len(h) >= 2 and cross(h[-2], h[-1], p) <= 0: h.pop()
            h.append(p)
        return h
    lo = half(P); up = half(P[::-1]); return lo[:-1] + up[:-1]
def area2(poly): return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))
def clip(poly, a, b, c):
    """keep a*x+b*y <= c (Sutherland-Hodgman, exact)."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]; fp = a * p[0] + b * p[1] - c; fq = a * q[0] + b * q[1] - c
        if fp <= 0: out.append(p)
        if (fp < 0 and fq > 0) or (fp > 0 and fq < 0):
            t = fp / (fp - fq); out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out
def halfplanes_ccw(poly):
    if area2(poly) < 0: poly = poly[::-1]
    hp = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        # interior is left of p->q:  cross(p,q,x) >= 0  <=>  -(q_y-p_y)(x-p_x) + (q_x-p_x)(y-p_y) >= 0  <=> a x + b y <= c with a=(q_y-p_y), b=-(q_x-p_x)
        a = (q[1] - p[1]); b = -(q[0] - p[0]); hp.append((a, b, a * p[0] + b * p[1]))
    return hp
def inter_area2(P, T):
    r = [(Fr(x), Fr(y)) for x, y in P]
    for a, b, c in halfplanes_ccw(T):
        r = clip(r, a, b, c)
        if len(r) < 3: return Fr(0)
    return abs(area2(r))


def check_D1(c):
    d, s, Q = c['d'], c['s'], tuple(c['Q']); F = set(fibre(d, s, Q)); why = []
    cells = [tuple(map(tuple, x)) for x in c['cells']]
    cache = {}
    def gv(g):
        if g not in cache: cache[g] = is_graver(d, s, g)
        return cache[g]
    for (u, g, h) in cells:
        cs = [u, (u[0] + g[0], u[1] + g[1]), (u[0] + h[0], u[1] + h[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1])]
        if not all(p in F for p in cs): why.append('corner not in F %s' % [u, g, h])
        if not (gv(g) and gv(h) and g[0] * h[1] - g[1] * h[0] != 0): why.append('generators %s' % [g, h])
    H = [(Fr(x), Fr(y)) for x, y in hull(list(F))]
    tot = Fr(0); polys = []
    for pc in c['pieces']:
        poly = [(Fr(x), Fr(y)) for x, y in pc['poly']]; k = pc['cell']
        if area2(poly) <= 0: poly = poly[::-1]
        # convexity: all turns left
        if not all(cross(poly[i], poly[(i + 1) % len(poly)], poly[(i + 2) % len(poly)]) >= 0 for i in range(len(poly))): why.append('piece not convex')
        u, g, h = cells[k]; cp = [u, (u[0] + g[0], u[1] + g[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1]), (u[0] + h[0], u[1] + h[1])]
        cp = [(Fr(x), Fr(y)) for x, y in cp]
        if area2(cp) < 0: cp = cp[::-1]
        for v in poly:
            if not all(a * v[0] + b * v[1] <= cc for a, b, cc in halfplanes_ccw(cp)): why.append('piece vertex outside its cell'); break
        # piece inside H
        for v in poly:
            if not all(a * v[0] + b * v[1] <= cc for a, b, cc in halfplanes_ccw(H)): why.append('piece vertex outside conv F'); break
        polys.append(poly); tot += area2(poly)
    for i in range(len(polys)):
        for j in range(i + 1, len(polys)):
            if inter_area2(polys[i], polys[j]) != 0: why.append('pieces %d,%d overlap' % (i, j)); break
        if len(why) > 6: break
    if tot != abs(area2(H)): why.append('area mismatch %s vs %s' % (tot, abs(area2(H))))
    return not why, why[:4]


# ------------------------------------------------------------------ D2 : binary rank
def rank_q(rows):
    M = [[Fr(x) for x in r] for r in rows]; rk = 0
    if not M: return 0
    for col in range(len(M[0])):
        p = next((i for i in range(rk, len(M)) if M[i][col] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][col] != 0:
                f = M[i][col] / M[rk][col]; M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk


def kernel_codes(cols, mask):
    n = len(cols); out = []
    for x in range(1, 1 << n):
        if x & ~mask: continue
        v = 0
        for i in range(n):
            if x >> i & 1: v ^= cols[i]
        if v == 0: out.append(x)
    return out


def circuits(C):
    Cs = sorted(C, key=lambda x: bin(x).count('1')); out = []
    for x in Cs:
        if not any(c & x == c for c in out): out.append(x)
    return out


def span(masks):
    sp = {0}
    for m in masks: sp |= {a ^ m for a in sp}
    return sp


def disjoint_families(circ):
    def rec(i, chosen, used):
        if chosen: yield tuple(chosen)
        for j in range(i, len(circ)):
            if circ[j] & used == 0: yield from rec(j + 1, chosen + [circ[j]], used | circ[j])
    yield from rec(0, [], 0)


def cells_by_centre(cols, mask):
    """independent implementation: cell = (disjoint circuit family S, coset x+span(S) with 0 not in it); centre key (U, x outside U)."""
    C = kernel_codes(cols, mask); circ = circuits(C); Cset = set(C); cells = {}
    for S in disjoint_families(circ):
        U = 0
        for m in S: U |= m
        sp = span(S)
        for x in C:
            if x in sp: continue
            co = frozenset(x ^ f for f in sp)
            key = (U, x & ~U)
            cells.setdefault(key, {})[co] = (x, S)
    return cells


def collisions(cols, mask):
    return [(k, v) for k, v in cells_by_centre(cols, mask).items() if len(v) > 1]


def check_D2(c):
    cols = c['columns']; n = len(cols); full = (1 << n) - 1; why = []
    col = collisions(cols, full)
    if not col: why.append('box is embedded (no collision)')
    for i in range(n):
        if collisions(cols, full & ~(1 << i)): why.append('deletion of coordinate %d is not embedded' % i)
    ranks = []
    for (U, xo), cs in col:
        items = list(cs.values())
        for a in range(len(items)):
            for b in range(a + 1, len(items)):
                (x, S), (y, T) = items[a], items[b]
                g = [[(1 - 2 * ((x >> i) & 1)) if (m >> i) & 1 else 0 for i in range(n)] for m in S]
                h = [[(1 - 2 * ((y >> i) & 1)) if (m >> i) & 1 else 0 for i in range(n)] for m in T]
                dlt = [((y >> i) & 1) - ((x >> i) & 1) for i in range(n)]
                ranks.append(rank_q(g + h + [dlt]))
                # exact shared point z: 1/2 on U, x outside U ; lies in relint of both cells because each generator coordinate is interior (1/2 = x_i + t g_i, t=1/2 for every circuit)
                z = [Fr(1, 2) if U >> i & 1 else Fr((x >> i) & 1) for i in range(n)]
                for (xx, SS, gg) in ((x, S, g), (y, T, h)):
                    t = [Fr(1, 2)] * len(SS)
                    pt = [Fr((xx >> i) & 1) + sum(t[j] * gg[j][i] for j in range(len(SS))) for i in range(n)]
                    if pt != z: why.append('shared point mismatch')
    if not ranks: return False, why
    if min(ranks) != c['min_rank']: why.append('min rank %s != claimed %s' % (min(ranks), c['min_rank']))
    if max(ranks) != c.get('max_rank', max(ranks)): why.append('max rank mismatch')
    return not why, why[:4]


# ------------------------------------------------------------------ D3 : hollow
def check_D3(c):
    d, s = c['d'], c['s']; why = []
    if gcd(s, d) != 1 or d < 3: return False, ['bad (d,s)']
    Q = (d, d); F = fibre(d, s, Q); Fs = set(F)
    t = next(t for t in range(1, d + 1) if (s * t) % d == 1)
    A, B, Cc = (0, d), (d, 0), (d, d)
    if Fs != {(i, (s * i) % d) for i in range(1, d)} | {A, B, Cc}: why.append('F structure')
    T = [[A, (d - t, d - 1), Cc], [B, (d - 1, d - s), Cc]]
    for tri in T:
        if not all(v in Fs for v in tri): why.append('vertex not in F')
        if abs(cross(*tri)) != d: why.append('area')
        for p, q in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
            if not is_graver(d, s, (q[0] - p[0], q[1] - p[1])): why.append('edge not Graver')
        # primitive: no other Gamma point in closed triangle
        xs = [v[0] for v in tri]; ys = [v[1] for v in tri]
        inside = [(i, j) for i in range(min(xs), max(xs) + 1) for j in range(min(ys), max(ys) + 1) if in_gamma(d, s, (i, j)) and
                  all(cross(tri[k], tri[(k + 1) % 3], (i, j)) * cross(*tri) >= 0 for k in range(3))]
        if sorted(inside) != sorted(tri): why.append('not primitive')
    # all 1-cells and 2-cells vs open triangles (exact)
    def open_tri_meets(tri, pts):
        poly = [(Fr(x), Fr(y)) for x, y in pts]
        if len(poly) == 2:
            p, q = poly; lo, hi = Fr(0), Fr(1); sg = 1 if cross(*tri) > 0 else -1
            for k in range(3):
                a, b = tri[k], tri[(k + 1) % 3]; f0 = sg * cross(a, b, p); f1 = sg * cross(a, b, q)
                if f0 == f1:
                    if f0 <= 0: return False
                    continue
                t0 = -f0 / (f1 - f0)
                if f1 > f0: lo = max(lo, t0)
                else: hi = min(hi, t0)
            return lo < hi
        return inter_area2(poly, tri) > 0
    for p, q in itertools.combinations(F, 2):
        if is_graver(d, s, (q[0] - p[0], q[1] - p[1])) and any(open_tri_meets(tri, [p, q]) for tri in T): why.append('a 1-cell meets an open triangle'); break
    for u in F:
        for v, w in itertools.combinations(F, 2):
            g = (v[0] - u[0], v[1] - u[1]); h = (w[0] - u[0], w[1] - u[1])
            if g[0] * h[1] - g[1] * h[0] == 0: continue
            z = (v[0] + w[0] - u[0], v[1] + w[1] - u[1])
            if z in Fs and is_graver(d, s, g) and is_graver(d, s, h):
                cp = [u, v, z, w]
                if cross(u, v, w) < 0: cp = cp[::-1]
                if any(open_tri_meets(tri, cp) for tri in T): why.append('a 2-cell meets an open triangle'); break
        if why and why[-1].startswith('a 2-cell'): break
    return not why, why[:4]


KINDS = {'D1_coverage': check_D1, 'D2_rank': check_D2, 'D3_hollow': check_D3}
if __name__ == '__main__':
    allok = True
    for fn in sys.argv[1:]:
        obj = json.load(open(fn)); items = obj if isinstance(obj, list) else [obj]
        for i, c in enumerate(items):
            ok, why = KINDS[c['kind']](c); allok &= ok
            print('%s %s[%d] %s %s' % ('VALID  ' if ok else 'INVALID', fn, i, c['kind'], ('' if ok else why)))
    sys.exit(0 if allok else 1)
