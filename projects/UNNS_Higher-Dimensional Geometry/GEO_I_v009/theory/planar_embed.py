"""GEO-I v005: independent exact planar embeddedness test (third validation path; uses only the definitions).
Cells of K_abs(Gamma_(d,s),Q): points of F; segments [p,p+g] (g lex-positive Graver, both ends in F);
parallelograms P(u;g,h) (g,h independent lex-positive Graver, four corners in F).  By T-REL the complex is embedded iff the relative
interiors of distinct cells are pairwise disjoint.  All arithmetic is exact (Fractions).  Returns the list of offending pairs."""
import os, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fractions import Fraction as Fr
from pure_lattice import fibre, graver


def lexpos(g): return g[0] > 0 or (g[0] == 0 and g[1] > 0)
def det(a, b): return a[0] * b[1] - a[1] * b[0]
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def add(a, b): return (a[0] + b[0], a[1] + b[1])


def cells(d, s, Q):
    F = fibre(d, s, Q); S = set(F); G = [g for g in graver(d, s) if lexpos(g)]
    pts = [('P', (p,)) for p in F]
    segs = {}
    for p in F:
        for g in G:
            q = add(p, g)
            if q in S: segs[frozenset((p, q))] = ('E', (p, q))
    pars = {}
    for p in F:
        for a, b in itertools.combinations(G, 2):
            if det(a, b) == 0: continue
            c = [p, add(p, a), add(p, b), add(add(p, a), b)]
            if all(x in S for x in c): pars[frozenset(c)] = ('C', (p, a, b))
    return pts, list(segs.values()), list(pars.values())


def _open_param_inside(p0, p1, poly):
    """open parameter interval (lo,hi) of the segment p0+t(p1-p0) lying in the OPEN convex polygon poly (ccw list); None if empty."""
    lo, hi = Fr(0), Fr(1)
    # we need relint(segment)=(0,1) intersect interior: use strict halfplanes
    lo_open, hi_open = True, True
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        e = sub(b, a)
        f0 = det(e, sub(p0, a)); f1 = det(e, sub(p1, a))          # >0 inside
        # f(t) = f0 + t (f1-f0) > 0
        dlt = f1 - f0
        if dlt == 0:
            if f0 <= 0: return None
        elif dlt > 0:
            t = Fr(-f0, dlt)
            if t > lo: lo = t
        else:
            t = Fr(-f0, dlt)
            if t < hi: hi = t
    return (lo, hi) if lo < hi else None


def _poly(p, a, b):
    c = [p, add(p, a), add(add(p, a), b), add(p, b)]
    if det(a, b) < 0: c = [p, add(p, b), add(add(p, a), b), add(p, a)]
    return c


def _pt_in_open_poly(x, poly):
    return all(det(sub(poly[(i + 1) % 4], poly[i]), sub(x, poly[i])) > 0 for i in range(4))


def _pt_in_open_seg(x, a, b):
    if det(sub(b, a), sub(x, a)) != 0: return False
    t = Fr(sub(x, a)[0] * sub(b, a)[0] + sub(x, a)[1] * sub(b, a)[1], (sub(b, a)[0] ** 2 + sub(b, a)[1] ** 2))
    return 0 < t < 1


def _seg_seg(a, b, c, d_):
    u, v = sub(b, a), sub(d_, c); w = sub(c, a)
    den = det(u, v)
    if den != 0:
        t = Fr(det(w, v), den); s_ = Fr(det(w, u), den)
        return 0 < t < 1 and 0 < s_ < 1
    if det(u, w) != 0: return False                        # parallel, not collinear
    uu = u[0] ** 2 + u[1] ** 2
    t0 = Fr(w[0] * u[0] + w[1] * u[1], uu); t1 = Fr(sub(d_, a)[0] * u[0] + sub(d_, a)[1] * u[1], uu)
    lo, hi = min(t0, t1), max(t0, t1)
    return max(lo, 0) < min(hi, 1)


def _poly_poly(P, R):
    for poly in (P, R):                                    # SAT with edge normals; open sets overlap iff no separating axis
        for i in range(4):
            e = sub(poly[(i + 1) % 4], poly[i]); nrm = (-e[1], e[0])
            pr = [nrm[0] * x[0] + nrm[1] * x[1] for x in P]; qr = [nrm[0] * x[0] + nrm[1] * x[1] for x in R]
            if max(pr) <= min(qr) or max(qr) <= min(pr): return False
    return True


def relint_meet(c1, c2):
    k1, k2 = c1[0], c2[0]
    if (k1, k2) == ('P', 'P'): return c1[1][0] == c2[1][0]
    if k1 > k2 and (k1, k2) != ('P', 'P') and k1 != k2: c1, c2, k1, k2 = c2, c1, k2, k1       # order P < E < C (alphabetical: C<E<P so re-rank)
    rank = {'P': 0, 'E': 1, 'C': 2}
    if rank[k1] > rank[k2]: c1, c2, k1, k2 = c2, c1, k2, k1
    if k1 == 'P' and k2 == 'E': return _pt_in_open_seg(c1[1][0], *c2[1])
    if k1 == 'P' and k2 == 'C': return _pt_in_open_poly(c1[1][0], _poly(*c2[1]))
    if k1 == 'E' and k2 == 'E': return _seg_seg(*c1[1], *c2[1])
    if k1 == 'E' and k2 == 'C': return _open_param_inside(c1[1][0], c1[1][1], _poly(*c2[1])) is not None
    return _poly_poly(_poly(*c1[1]), _poly(*c2[1]))


def offending_pairs(d, s, Q, limit=None):
    pts, segs, pars = cells(d, s, Q)
    allc = pts + segs + pars; out = []
    for i in range(len(allc)):
        for j in range(i + 1, len(allc)):
            if relint_meet(allc[i], allc[j]):
                out.append((allc[i], allc[j]))
                if limit and len(out) >= limit: return out
    return out


def embedded(d, s, Q): return not offending_pairs(d, s, Q, limit=1)
