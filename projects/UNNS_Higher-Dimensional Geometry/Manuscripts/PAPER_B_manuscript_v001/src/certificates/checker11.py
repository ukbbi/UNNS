#!/usr/bin/env python3
"""GEO-I v011 standalone certificate checker.  Run:  python3 -I certificates/checker11.py FILE.json [...]
Standard library only; no import from the release.  Formats:
  PARTITION  {type,k,points,two_blocks:[[f,g],...],n_two_blocks}   k = nullity, points = X subset of AG(k-1,2) (k-bit ints with top bit set), f,g functionals in F_2^k.
      Accepts iff: points distinct, top bit set, rank k; for >=2 listed pairs (distinct as unordered pairs) supp(w_f), supp(w_g) are disjoint circuits covering X
      (circuit test: X cap f^perp has rank k-1); n_two_blocks equals an independent recount over all functionals.
      Consequence (G10-E1, G10-L5): two distinct two-circuit partitions of 1 => non-embedded box with a collision of generator rank 3.
  CAPCOVER   {type,d,s,u,cells:[[ux,uy,gx,gy,hx,hy],...]}  one-sided small box Q=(d+u,d).
      Accepts iff: gcd(s,d)=1, 2<=s<=d-2, 1<=u<d; every cell has all four corners in F_Q = Gamma cap [0,Q] minus 0, generators in Gamma and Graver (box scan) and independent;
      K = B + conv({0,(0,d)} u {(i, s i mod d)}) lies in the union of the cells (exact rational polygon subtraction); area(conv F_Q) = area(conv F_(d,d)) + area(K).
      Consequence: conv F_Q = H_0 u K is covered by cells once H_0 is (G10-R1, inherited): the cap of the one-sided small box is inside U_Q."""
import sys, json
from fractions import Fraction as Fr
from math import gcd


def par(x): return bin(x).count('1') & 1


def rank(vs):
    b = []
    for v in vs:
        for c in b: v = min(v, v ^ c)
        if v: b.append(v)
    return len(b)


def check_PARTITION(c):
    k = c['k']; X = c['points']; n = len(X); top = 1 << (k - 1)
    if len(set(X)) != n or any(not (x & top) or x >= (1 << k) for x in X): return False, 'points not distinct points of AG(k-1,2)'
    if rank(X) != k: return False, 'points do not span'
    full = (1 << n) - 1

    def supp(f): return sum(1 << i for i, x in enumerate(X) if par(f & x))

    def circ(f): return f != 0 and supp(f) != 0 and rank([x for x in X if not par(f & x)]) == k - 1
    seen = set()
    for f, g in c['two_blocks']:
        a, b = supp(f), supp(g)
        if not (circ(f) and circ(g) and a & b == 0 and a | b == full and a and b): return False, 'pair %s is not a two-circuit partition' % ([f, g],)
        seen.add(frozenset((f, g)))
    if len(seen) < 2: return False, 'fewer than two distinct pairs'
    cs = {f: supp(f) for f in range(1, 1 << k) if circ(f)}; tot = set()
    for f, a in cs.items():
        for g, b in cs.items():
            if f < g and a & b == 0 and a | b == full: tot.add(frozenset((f, g)))
    if len(tot) != c['n_two_blocks']: return False, 'n_two_blocks mismatch: recount %d' % len(tot)
    return True, 'k=%d p=%d two-blocks=%d' % (k, n, len(tot))


# ------------------------------------------------------------------------------------------ planar
def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull(P):
    P = sorted(set(P)); lo = []
    for p in P:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(P):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def area2(P): return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))


def clip(P, a, b, c):
    out = []; n = len(P)
    for i in range(n):
        p, q = P[i], P[(i + 1) % n]; fp = a * p[0] + b * p[1] + c; fq = a * q[0] + b * q[1] + c
        if fp >= 0: out.append(p)
        if (fp > 0 and fq < 0) or (fp < 0 and fq > 0):
            t = Fr(fp) / (fp - fq); out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def halfplanes(poly):
    P = [(Fr(x), Fr(y)) for x, y in poly]
    if area2(P) < 0: P = P[::-1]
    out = []
    for i in range(len(P)):
        p, q = P[i], P[(i + 1) % len(P)]; a = -(q[1] - p[1]); b = q[0] - p[0]; out.append((a, b, -(a * p[0] + b * p[1])))
    return out


def subtract(pieces, region):
    new = []
    for pc in pieces:
        r = pc
        for (a, b, c) in region:
            o = clip(r, -a, -b, -c)
            if len(o) >= 3 and area2(o) > 0: new.append(o)
            r = clip(r, a, b, c)
            if len(r) < 3 or area2(r) <= 0: r = None; break
    return new


def is_graver(d, s, g):
    if g == (0, 0) or (g[1] - s * g[0]) % d: return False
    sa = 1 if g[0] >= 0 else -1; sb = 1 if g[1] >= 0 else -1
    return not any((a, b) not in ((0, 0), (abs(g[0]), abs(g[1]))) and (sb * b - s * sa * a) % d == 0 for a in range(abs(g[0]) + 1) for b in range(abs(g[1]) + 1))


def fibre(d, s, Q): return {(x, y) for x in range(Q[0] + 1) for y in range(Q[1] + 1) if (x or y) and (y - s * x) % d == 0}


def check_CAPCOVER(c):
    d, s, u = c['d'], c['s'], c['u']
    if not (gcd(s, d) == 1 and 2 <= s <= d - 2 and 1 <= u < d): return False, 'parameters'
    Q = (d + u, d); F = fibre(d, s, Q); polys = []
    for (ux, uy, gx, gy, hx, hy) in c['cells']:
        U, g, h = (ux, uy), (gx, gy), (hx, hy)
        cs = [U, (ux + gx, uy + gy), (ux + hx, uy + hy), (ux + gx + hx, uy + gy + hy)]
        if not all(p in F for p in cs): return False, 'corner outside F_Q: %s' % (U,)
        if not (is_graver(d, s, g) and is_graver(d, s, h)): return False, 'non-Graver generator'
        if gx * hy - gy * hx == 0: return False, 'dependent generators'
        polys.append([cs[0], cs[1], cs[3], cs[2]])
    W = hull([(0, 0), (0, d)] + [(i, (s * i) % d) for i in range(1, u + 1)])
    K = [(x + d, y) for x, y in W]
    pieces = [[(Fr(x), Fr(y)) for x, y in K]]
    for pl in polys:
        pieces = subtract(pieces, halfplanes(pl))
        if not pieces: break
    if pieces: return False, 'cap not covered: %d pieces left' % len(pieces)
    HQ = hull(list(F)); H0 = hull(list(fibre(d, s, (d, d))))
    if area2(HQ) != area2(H0) + area2(K): return False, 'hull decomposition H_Q = H_0 u K fails'
    return True, 'd=%d s=%d u=%d cells=%d' % (d, s, u, len(polys))


CHECK = {'PARTITION': check_PARTITION, 'CAPCOVER': check_CAPCOVER}


def check_file(path):
    certs = json.load(open(path)); certs = certs if isinstance(certs, list) else [certs]; n_ok = n_bad = 0
    for i, c in enumerate(certs):
        f = CHECK.get(c.get('type'))
        if f is None: print('INVALID  %s[%d]: unknown type %r' % (path, i, c.get('type'))); n_bad += 1; continue
        ok, msg = f(c)
        if ok: n_ok += 1
        else: n_bad += 1; print('INVALID  %s[%d] %s: %s' % (path, i, c['type'], msg))
    print('VALID  %s: %d certificates accepted, %d rejected' % (path, n_ok, n_bad))
    return n_bad


if __name__ == '__main__':
    bad = sum(check_file(p) for p in sys.argv[1:])
    sys.exit(1 if bad else 0)
