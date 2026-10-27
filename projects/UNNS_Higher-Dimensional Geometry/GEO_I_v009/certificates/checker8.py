#!/usr/bin/env python3
"""GEO-I v008 standalone certificate checker.  Uses ONLY the Python standard library; imports nothing from this release.
   python3 checker8.py FILE.json [FILE2.json ...]        exit status 0 iff every certificate is VALID.
Kinds:
 COVER     : exact hull vertices, cell list with corner incidence, and a subdivision of conv(F) into convex pieces each inside a cell (VALID iff F, hull, Graver
             generators, corners, containment, pairwise disjointness and the area sum are all recomputed and agree: conv(F) = union of pieces, a subset of U).
 GAP       : an exact point z with z in conv(F) and z in no cell of K_abs (all Graver segments and all Graver parallelograms with corners in F are recomputed).
             A VALID GAP certificate is a decisive counterexample to  U = conv(F)  for that box.
 HOMOLOGY  : an explicit planar chain complex (vertices, edges, faces as vertex cycles).  VALID iff every face boundary is a closed walk on listed edges,
             d1 d2 = 0 (computed), each edge lies in at most two faces, ranks of d1,d2 are recomputed over Q, the claimed Betti numbers equal the recomputed ones and
             the Euler-Poincare identity V - E + F = b0 - b1 + b2 holds.   (It certifies the homology of the SUPPLIED complex; that the complex is the one of U is a separate COVER/arrangement statement.)
 RANK      : binary 0/1 box: columns, claim 'minimal non-embedded with minimum witness rank r', plus the series-class (B-SERIES) data: parallel classes and nullity recomputed.
 D1_coverage, D2_rank, D3_hollow : the v007 kinds, kept so that v007 certificates remain checkable (provenance: copied unchanged from certificates/checker.py of v007).
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



# ================================================================== v008 kinds
def hull_vertices_claim(c, F):
    H = hull(list(F)); got = sorted((Fr(x), Fr(y)) for x, y in H)
    return got


def cells_incidence(cells):
    return [[list(p) for p in ((u), (u[0] + g[0], u[1] + g[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1]), (u[0] + h[0], u[1] + h[1]))] for (u, g, h) in cells]


def check_COVER(c):
    ok, why = check_D1(c); why = list(why)
    d, s, Q = c['d'], c['s'], tuple(c['Q']); F = set(fibre(d, s, Q))
    claimed = sorted((Fr(x), Fr(y)) for x, y in c['hull'])
    if claimed != hull_vertices_claim(c, F): why.append('hull vertices differ from recomputed conv(F)')
    cells = [tuple(map(tuple, x)) for x in c['cells']]
    if [[tuple(p) for p in inc] for inc in c['incidence']] != [[tuple(p) for p in inc] for inc in cells_incidence(cells)]: why.append('cell incidence differs')
    used = {pc['cell'] for pc in c['pieces']}
    if used != set(range(len(cells))): why.append('some listed cell carries no piece (or index out of range)')
    return (not why), why[:4]


def all_cells(d, s, Q):
    """every Graver segment and Graver parallelogram with corners in F (independent recomputation)."""
    F = fibre(d, s, Q); Fs = set(F); G = {}
    def gv(g):
        if g not in G: G[g] = is_graver(d, s, g)
        return G[g]
    segs = [(p, q) for p, q in itertools.combinations(F, 2) if gv((q[0] - p[0], q[1] - p[1]))]
    pars = []
    for u in F:
        for v, w in itertools.combinations(F, 2):
            g = (v[0] - u[0], v[1] - u[1]); h = (w[0] - u[0], w[1] - u[1])
            if g[0] * h[1] - g[1] * h[0] == 0: continue
            z = (v[0] + w[0] - u[0], v[1] + w[1] - u[1])
            if z in Fs and gv(g) and gv(h): pars.append((u, v, z, w))
    return F, segs, pars


def in_closed_convex(poly, z):
    sg = [cross(poly[i], poly[(i + 1) % len(poly)], z) for i in range(len(poly))]
    return all(x >= 0 for x in sg) or all(x <= 0 for x in sg)


def check_GAP(c):
    d, s, Q = c['d'], c['s'], tuple(c['Q']); z = (Fr(c['z'][0]), Fr(c['z'][1])); why = []
    F, segs, pars = all_cells(d, s, Q)
    if not F: return False, ['F empty']
    H = [(Fr(x), Fr(y)) for x, y in hull(F)]
    if len(H) < 3 or not in_closed_convex(H, z): why.append('z not in conv(F)')
    for p, q in segs:
        if cross(p, q, z) == 0 and min(p[0], q[0]) <= z[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= z[1] <= max(p[1], q[1]): why.append('z lies on a 1-cell %s-%s' % (p, q)); break
    if not why:
        for cp in pars:
            if in_closed_convex(list(cp), z): why.append('z lies in a 2-cell %s' % (cp,)); break
    return (not why), why[:3]


def rank_over_Q(cols):
    piv = {}; r = 0
    for col in cols:
        c = {k: Fr(v) for k, v in col.items() if v}
        while c:
            p = min(c)
            if p in piv:
                pc = piv[p]; f = c[p] / pc[p]
                for k2, v in pc.items():
                    nv = c.get(k2, 0) - f * v
                    if nv: c[k2] = nv
                    else: c.pop(k2, None)
            else:
                piv[p] = c; r += 1; break
    return r


def check_HOMOLOGY(c):
    V = c['vertices']; E = [tuple(e) for e in c['edges']]; Fc = c['faces']; why = []
    nV, nE, nF = len(V), len(E), len(Fc)
    if len(set(map(lambda p: (Fr(p[0]), Fr(p[1])), V))) != nV: why.append('duplicate vertices')
    Eidx = {}
    for i, (a, b) in enumerate(E):
        if a == b or not (0 <= a < nV and 0 <= b < nV): why.append('bad edge'); return False, why
        Eidx[(a, b)] = (i, 1); Eidx.setdefault((b, a), (i, -1))
    d1 = [{a: -1, b: 1} for a, b in E]; d1 = [{k: v for k, v in col.items()} for col in d1]
    d2 = []; use = [0] * nE
    for cyc in Fc:
        col = {}
        for k in range(len(cyc)):
            a, b = cyc[k], cyc[(k + 1) % len(cyc)]
            if (a, b) not in Eidx: why.append('face edge not listed'); return False, why
            i, sg = Eidx[(a, b)]; col[i] = col.get(i, 0) + sg; use[i] += 1
        d2.append({k: v for k, v in col.items() if v})
    if max(use or [0]) > 2: why.append('an edge lies in more than two faces')
    for col in d2:                                                   # d1 d2 = 0
        acc = {}
        for i, cf in col.items():
            for vtx, sg in d1[i].items(): acc[vtx] = acc.get(vtx, 0) + cf * sg
        if any(acc.values()): why.append('d1 d2 != 0'); break
    r1 = rank_over_Q(d1); r2 = rank_over_Q(d2)
    b0, b1, b2 = nV - r1, nE - r1 - r2, nF - r2
    if [b0, b1, b2] != list(c['betti']): why.append('betti %s != claimed %s' % ([b0, b1, b2], c['betti']))
    if nV - nE + nF != b0 - b1 + b2: why.append('Euler-Poincare fails')
    return (not why), why[:3]


def code_profile_classes(cols):
    n = len(cols); C = [x for x in range(1 << n) if all(sum((x >> i) & 1 for i in range(n) if (cols[i] >> k) & 1) % 2 == 0 for k in range(max(cols).bit_length()))]
    prof = {}
    for i in range(n): prof.setdefault(tuple((x >> i) & 1 for x in C), []).append(i)
    return list(prof.values()), len(C).bit_length() - 1


def check_RANK(c):
    ok, why = check_D2(c); why = list(why)
    cl, k = code_profile_classes(c['columns'])
    if c.get('nullity') is not None and k != c['nullity']: why.append('nullity %d != claimed %d' % (k, c['nullity']))
    if c.get('series_classes') is not None and len(cl) != c['series_classes']: why.append('series classes %d != claimed %d' % (len(cl), c['series_classes']))
    if k < 3: why.append('nullity < 3 contradicts non-embedded (B-NULL prime)')
    return (not why), why[:4]


KINDS = {'D1_coverage': check_D1, 'D2_rank': check_D2, 'D3_hollow': check_D3, 'COVER': check_COVER, 'GAP': check_GAP, 'HOMOLOGY': check_HOMOLOGY, 'RANK': check_RANK}

if __name__ == '__main__':
    allok = True
    for fn in sys.argv[1:]:
        obj = json.load(open(fn)); items = obj if isinstance(obj, list) else [obj]
        for i, c in enumerate(items):
            ok, why = KINDS[c['kind']](c); allok &= ok
            print('%s %s[%d] %s %s' % ('VALID  ' if ok else 'INVALID', fn, i, c['kind'], ('' if ok else why)))
    sys.exit(0 if allok else 1)
