#!/usr/bin/env python3
"""GEO-I v010 standalone certificate checker for kinds RANK6 and BOUNDARY.  Python standard library ONLY; imports nothing from this release.
   python3 checker10.py FILE.json [...]     exit status 0 iff every certificate is VALID.
A RANK6 certificate for a REDUCED binary box states: support (distinct nonzero points of F_2^k as ints, spanning), nullity k, and
  claim: the box is minimal non-embedded and its minimum witness rank is 3, with an explicit common-base collision of rank 3.
The checker recomputes from the support alone:
  1. the code C (2^k words), its circuits (minimal supports), and that the support spans (nullity = k);
  2. NON-EMBEDDED by the definition (v006 centre criterion): two distinct cells (S,x),(T,y) -- S,T families of pairwise disjoint circuits, x not in span(S), y not in span(T) --
     with equal union U and x = y off U.  The supplied witness (S,T,x) is verified directly AND an exhaustive collision search is run;
  3. MINIMAL: for every coordinate the shortened code has NO collision (exhaustive search over all cells);
  4. the witness rank: exact rank over Q of the +-1 generator vectors of the collision = 3;  a lower bound 3 holds for every collision (theorem B-LOW, MINIMAL_RANK.md), so min rank = 3.
Also checks the optional claim 'two_blocks' = number of unordered pairs of complementary circuits (partitions of the all-ones word into two circuits)."""
import sys, json, itertools
from fractions import Fraction as Fr


def rank_f2(vs):
    basis = []
    for v in vs:
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    return len(basis)


def code_of(support, k):
    out = set()
    for u in range(1 << k):
        m = 0
        for i, s in enumerate(support):
            if bin(u & s).count('1') & 1: m |= 1 << i
        out.add(m)
    return sorted(out)


def circuits(C):
    circ = []
    for x in sorted((c for c in C if c), key=lambda v: (bin(v).count('1'), v)):
        if not any(c & x == c for c in circ): circ.append(x)
    return circ


def families(circ):
    def rec(i, chosen, used):
        if chosen: yield tuple(chosen), used
        for j in range(i, len(circ)):
            if circ[j] & used == 0: yield from rec(j + 1, chosen + [circ[j]], used | circ[j])
    yield from rec(0, [], 0)


def span(S):
    sp = {0}
    for m in S: sp |= {a ^ m for a in sp}
    return sp


def has_collision(C):
    circ = circuits(C); cells = {}
    for S, U in families(circ):
        sp = span(S); seen = set()
        for x in C:
            if x in sp: continue
            co = min(x ^ f for f in sp)
            if co in seen: continue
            seen.add(co); lst = cells.setdefault((U, x & ~U), [])
            if lst: return True          # a second distinct cell (different family or different coset) with the same key
            lst.append((S, co))
    return False


def witness_rank(n, S, x, T, y):
    g = [[(1 - 2 * ((x >> i) & 1)) if (m >> i) & 1 else 0 for i in range(n)] for m in S]
    h = [[(1 - 2 * ((y >> i) & 1)) if (m >> i) & 1 else 0 for i in range(n)] for m in T]
    M = [[Fr(v) for v in r] for r in g + h]; rk = 0
    for col in range(n):
        p = next((i for i in range(rk, len(M)) if M[i][col] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][col] != 0:
                f = M[i][col] / M[rk][col]; M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk


def check_RANK6(c):
    try:
        sup = list(c['support']); k = int(c['nullity']); n = len(sup)
        if len(set(sup)) != n or 0 in sup or any(s >> k for s in sup): return False, 'support must be distinct nonzero points of F_2^k'
        if rank_f2(sup) != k: return False, 'support does not span F_2^k (nullity mismatch)'
        C = code_of(sup, k)
        if len(C) != 1 << k: return False, 'code size'
        circ = set(circuits(C)); w = c['witness']
        S = tuple(w['S']); T = tuple(w['T']); x = int(w['x'])
        if not all(m in circ for m in S + T): return False, 'witness part is not a circuit'
        for F in (S, T):
            if any(a & b for a, b in itertools.combinations(F, 2)): return False, 'circuits of a family overlap'
        US = 0
        for m in S: US |= m
        UT = 0
        for m in T: UT |= m
        if US != UT: return False, 'unions differ'
        if set(S) == set(T): return False, 'families equal'
        if x not in C or x in span(S) or x in span(T): return False, 'base x invalid'
        if not has_collision(C): return False, 'exhaustive search finds no collision (box embedded)'
        for i in range(n):
            if has_collision([v for v in C if not (v >> i) & 1]): return False, 'deleting coordinate %d leaves a collision: not minimal' % i
        rk = witness_rank(n, S, x, T, x)
        if rk != int(c['min_rank']) or rk != 3: return False, 'witness rank %d' % rk
        if 'two_blocks' in c:
            full = (1 << n) - 1
            tb = {tuple(sorted((a, full ^ a))) for a in circ if (full ^ a) in circ}
            if len(tb) != int(c['two_blocks']): return False, 'two_blocks %d' % len(tb)
        return True, 'ok k=%d p=%d rank=%d' % (k, n, rk)
    except (KeyError, TypeError, ValueError) as e:
        return False, 'malformed: %r' % (e,)


# ---------------------------------------------------------------------------------------------------------------- BOUNDARY
FULL_LIMIT = 48


def _fibre(d, s):
    out = []
    for x in range(d + 1):
        y = (s * x) % d
        for yy in ((y, y + d) if y == 0 else (y,)):
            if yy <= d and (x or yy): out.append((x, yy))
    return out


def _in_gamma(d, s, p): return (p[1] - s * p[0]) % d == 0


def _graver(d, s, g):
    if g == (0, 0) or not _in_gamma(d, s, g): return False
    sa = 1 if g[0] >= 0 else -1; sb = 1 if g[1] >= 0 else -1
    return not any((a, b) not in ((0, 0), (abs(g[0]), abs(g[1]))) and _in_gamma(d, s, (sa * a, sb * b)) for a in range(abs(g[0]) + 1) for b in range(abs(g[1]) + 1))


def _cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _hull(P):
    P = sorted(set(P))
    def half(pts):
        h = []
        for p in pts:
            while len(h) >= 2 and _cross(h[-2], h[-1], p) <= 0: h.pop()
            h.append(p)
        return h
    lo = half(P); up = half(P[::-1]); return lo[:-1] + up[:-1]


def _area2(P): return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))


def _clip(P, a, b, c):
    out = []
    for i in range(len(P)):
        p, q = P[i], P[(i + 1) % len(P)]; fp = a * p[0] + b * p[1] + c; fq = a * q[0] + b * q[1] + c
        if fp >= 0: out.append(p)
        if (fp > 0 and fq < 0) or (fp < 0 and fq > 0):
            u = fp / (fp - fq); out.append((p[0] + u * (q[0] - p[0]), p[1] + u * (q[1] - p[1])))
    return out


def _hp(poly):
    P = [(Fr(x), Fr(y)) for x, y in poly]
    if _area2(P) < 0: P = P[::-1]
    return [(-(P[(i + 1) % len(P)][1] - P[i][1]), P[(i + 1) % len(P)][0] - P[i][0], 0, P[i]) for i in range(len(P))]


def _halfplanes(poly):
    P = [(Fr(x), Fr(y)) for x, y in poly]
    if _area2(P) < 0: P = P[::-1]
    out = []
    for i in range(len(P)):
        p, q = P[i], P[(i + 1) % len(P)]; a = -(q[1] - p[1]); b = q[0] - p[0]; out.append((a, b, -(a * p[0] + b * p[1])))
    return out


def _subtract(pieces, region):
    new = []
    for pc in pieces:
        r = pc
        for (a, b, c) in region:
            o = _clip(r, -a, -b, -c)
            if len(o) >= 3 and _area2(o) > 0: new.append(o)
            r = _clip(r, a, b, c)
            if len(r) < 3 or _area2(r) <= 0: r = None; break
    return new


def _corners(c): u, g, h = c; return [u, (u[0] + g[0], u[1] + g[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1]), (u[0] + h[0], u[1] + h[1])]


def _seg_meets_open_tri(p, q, T):
    lo, hi = Fr(0), Fr(1)                       # parameter interval in which all three strict inequalities hold: open interval (lo,hi) after intersecting
    ok_lo = True
    for (a, b, c) in _halfplanes(T):
        fp = a * p[0] + b * p[1] + c; fq = a * q[0] + b * q[1] + c
        if fp == fq:
            if fp <= 0: return False
            continue
        r = fp / (fp - fq)                      # root of f along the segment
        if fq > fp: lo = max(lo, r)             # f increases: need t > r
        else: hi = min(hi, r)                   # f decreases: need t < r
    return lo < hi


def _cell_area_in(cell, T):
    P = [(Fr(x), Fr(y)) for x, y in _corners(cell)]
    if _area2(P) < 0: P = P[::-1]
    r = P
    for (a, b, c) in _halfplanes(T):
        r = _clip(r, a, b, c)
        if len(r) < 3: return 0
    return abs(_area2(r))


def _edge_covered(p, q, segs, cells):
    """is the closed segment [p,q] contained in the union of the given segments (pairs) and cells?  (exact: union of closed parameter intervals)"""
    ivs = []
    dx, dy = q[0] - p[0], q[1] - p[1]
    def add(lo, hi):
        if lo <= hi: ivs.append((max(lo, Fr(0)), min(hi, Fr(1))))
    for (a, b) in segs:
        if _cross(a, b, p) == 0 and _cross(a, b, q) == 0:
            L = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
            ta = Fr((a[0] - p[0]) * dx + (a[1] - p[1]) * dy, dx * dx + dy * dy); tb = Fr((b[0] - p[0]) * dx + (b[1] - p[1]) * dy, dx * dx + dy * dy)
            add(min(ta, tb), max(ta, tb))
    for c in cells:
        lo, hi = Fr(0), Fr(1); P = [(Fr(x), Fr(y)) for x, y in _corners(c)]; empty = False
        for (a, b, cc) in _halfplanes(P):
            fp = a * p[0] + b * p[1] + cc; fq = a * q[0] + b * q[1] + cc
            if fp == fq:
                if fp < 0: empty = True; break
                continue
            r = fp / (fp - fq)
            if fq > fp: lo = max(lo, r)
            else: hi = min(hi, r)
        if not empty: add(lo, hi)
    ivs = sorted(i for i in ivs if i[0] <= i[1]); cur = Fr(0)
    for lo, hi in ivs:
        if lo > cur: return False
        cur = max(cur, hi)
    return cur >= 1


def check_BOUNDARY(c):
    try:
        d = int(c['d']); s = int(c['s']); cells = [(tuple(u), tuple(g), tuple(h)) for u, g, h in c['cells']]
        if d < 3 or s % d == 0 or any(d % p == 0 and s % p == 0 for p in range(2, d + 1)): return False, 'bad (d,s)'
        s %= d; F = _fibre(d, s); Fs = set(F); t = next(t for t in range(1, d + 1) if (s * t) % d == 1 % d)
        for (u, g, h) in cells:
            if not (g > (0, 0) and h > (0, 0) and g[0] * h[1] - g[1] * h[0] != 0): return False, 'cell generators not lex-positive/independent'
            if not (_graver(d, s, g) and _graver(d, s, h)): return False, 'generator not Graver'
            if not all(p in Fs for p in _corners((u, g, h))): return False, 'cell corner not in F'
        T1 = [(0, d), (d - t, d - 1), (d, d)]; T2 = [(d, 0), (d - 1, d - s), (d, d)]
        if not (all(p in Fs for p in T1 + T2)): return False, 'triangle vertex not in F'
        pieces = [[(Fr(x), Fr(y)) for x, y in _hull(F)]]
        for T in (T1, T2): pieces = _subtract(pieces, _halfplanes(T))
        for cl in cells: pieces = _subtract(pieces, _halfplanes(_corners(cl)))
        rem = sum(_area2(p) for p in pieces)
        if rem != 0: return False, 'conv(F) not covered: remainder area %s' % (rem / 2)
        if d > FULL_LIMIT: return True, 'cover-only (d=%d > %d): conv(F) in U0 u T1 u T2 verified; disjointness is theorem G7-T3' % (d, FULL_LIMIT)
        # full recomputation of U0
        cand = [(a, b) for a in range(-d, d + 1) for b in range(-d, d + 1) if (a, b) != (0, 0) and _in_gamma(d, s, (a, b))]
        cand.sort(key=lambda g: (abs(g[0]) + abs(g[1]), g)); G = []
        for g in cand:
            if not any(h[0] * g[0] >= 0 and h[1] * g[1] >= 0 and abs(h[0]) <= abs(g[0]) and abs(h[1]) <= abs(g[1]) for h in G): G.append(g)
        Gp = sorted(g for g in G if g > (0, 0)); segs = [(u, (u[0] + g[0], u[1] + g[1])) for u in F for g in Gp if (u[0] + g[0], u[1] + g[1]) in Fs]
        allcells = []
        for u in F:
            for i, g in enumerate(Gp):
                for h in Gp[i + 1:]:
                    if g[0] * h[1] - g[1] * h[0] != 0 and all(p in Fs for p in _corners((u, g, h))): allcells.append((u, g, h))
        for T in (T1, T2):
            if any(_seg_meets_open_tri(p, q, T) for p, q in segs): return False, 'a Graver segment meets an open triangle'
            if any(_cell_area_in(cl, T) > 0 for cl in allcells): return False, 'a cell meets an open triangle'
            for i in range(3):
                if not _edge_covered(T[i], T[(i + 1) % 3], segs, allcells): return False, 'a triangle edge is not contained in U0'
        return True, 'exact (all %d Graver elements, %d segments, %d cells recomputed): conv(F) minus U0 = int T1 u int T2' % (len(G), len(segs), len(allcells))
    except (KeyError, TypeError, ValueError, StopIteration) as e:
        return False, 'malformed: %r' % (e,)


def main(paths):
    bad = 0
    for p in paths:
        data = json.load(open(p)); data = data if isinstance(data, list) else [data]
        for i, c in enumerate(data):
            if c.get('kind') not in ('RANK6', 'BOUNDARY'): print('SKIP   %s[%d] kind %s' % (p, i, c.get('kind'))); continue
            ok, msg = (check_RANK6 if c['kind'] == 'RANK6' else check_BOUNDARY)(c); bad += (not ok); print(('VALID    ' if ok else 'INVALID  ') + '%s[%d] %s' % (p, i, msg))
    return 1 if bad else 0


if __name__ == '__main__': sys.exit(main(sys.argv[1:]))
