"""GEO-I v007, Programme C: the hollow box Q=(d,d), general unit s.  Exact, self-contained (integers/Fractions only; no earlier modules).

Gamma = {(i,j): j = s i mod d}, F = Gamma cap [0,d]^2 minus 0 = {P_i=(i, s i mod d): 1<=i<=d-1} u {A=(0,d), B=(d,0), C=(d,d)}      (Lemma H0, checked).
T1 = tri(A, P_{d-t}, C),  T2 = tri(B, P_{d-1}, C),  t = s^-1 mod d;  P_{d-t}=(d-t,d-1), P_{d-1}=(d-1,d-s);  area(T_i)=d/2.
Certificate for  beta_1(U) >= 2  (Alexander duality: for a compact planar polyhedron U, beta_1 = # bounded components of R^2 \\ U):
  (a) the vertices of T_i are in F and Gamma cap closed T_i = vertices only (primitive triangle: |det| = d = index of Gamma);
  (b) every edge of T_i is a Graver segment with endpoints in F, hence a 1-cell of U (so boundary(T_i) subset U);
  (c) int T_i cap U = empty: no cell of K_abs meets int T_i.  Cells are conv of corners in F; checked EXACTLY by (c1) every Graver segment between points of F has relint
      disjoint from int T_i, and (c2) no parallelogram cell contains the centroid of T_i or has a vertex in int T_i (a convex cell meeting the open convex set int T_i
      has a vertex in it, an edge crossing it, or contains it; c2 handles 'contains', and 'vertex in' is excluded by (a)).
  Then int T1, int T2 are open, connected, bounded, disjoint from U and with boundary in U: two distinct bounded components, so beta_1 >= 2.
Upper bound (beta_1 = 2) additionally needs H \\ (T1 u T2) subset U; that is v006's exact area check (d<=45) and is NOT claimed beyond that range."""
from fractions import Fraction as Fr
from math import gcd
import itertools


def inv(s, d): return next(t for t in range(1, d + 1) if (s * t) % d == 1 % d)


def in_gamma(d, s, p): return (p[1] - s * p[0]) % d == 0


def is_graver(d, s, g):
    """g in Gamma\\0 is Graver iff no gamma in Gamma\\{0,g} is conformally below g (same signs, |gamma_k|<=|g_k|)."""
    if g == (0, 0) or not in_gamma(d, s, g): return False
    sa = 1 if g[0] >= 0 else -1; sb = 1 if g[1] >= 0 else -1
    for a in range(abs(g[0]) + 1):
        for b in range(abs(g[1]) + 1):
            c = (sa * a, sb * b)
            if c in ((0, 0), g): continue
            if in_gamma(d, s, c): return False
    return True


def fibre_hollow(d, s): return sorted((i, j) for i in range(d + 1) for j in range(d + 1) if (i or j) and in_gamma(d, s, (i, j)))


def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def inside_open_tri(T, p):
    c = [cross(T[k], T[(k + 1) % 3], p) for k in range(3)]
    return all(x > 0 for x in c) or all(x < 0 for x in c)


def seg_meets_open_tri(T, p, q):
    """does the open segment pq meet the open triangle T?  exact: clip the parametrised segment by the three strict half-planes."""
    if p == q: return inside_open_tri(T, p)
    lo, hi = Fr(0), Fr(1)                      # open interval (0,1) intersected with strict constraints
    sign = 1 if cross(T[0], T[1], T[2]) > 0 else -1
    lo_closed = hi_closed = False
    for k in range(3):
        a, b = T[k], T[(k + 1) % 3]
        f0 = sign * cross(a, b, p); f1 = sign * cross(a, b, q)   # affine along the segment, need >0
        # f(t) = f0 + t (f1 - f0) > 0
        if f1 == f0:
            if f0 <= 0: return False
            continue
        t0 = Fr(-f0, 1) / (f1 - f0)
        if f1 > f0: lo = max(lo, t0)       # t > t0
        else: hi = min(hi, t0)             # t < t0
    return lo < hi


def check_hollow(d, s):
    assert d >= 3 and gcd(s, d) == 1 and 1 <= s < d
    t = inv(s, d); F = fibre_hollow(d, s); Fs = set(F)
    A, B, Cc = (0, d), (d, 0), (d, d)
    P = {i: (i, (s * i) % d) for i in range(1, d)}
    expected = {P[i] for i in range(1, d)} | {A, B, Cc}
    res = {'F_structure': Fs == expected and len(F) == d + 2}
    T1 = [A, P[d - t], Cc]; T2 = [B, P[d - 1], Cc]
    res['vertices_in_F'] = all(v in Fs for v in T1 + T2)
    res['areas'] = abs(cross(*T1)) == d and abs(cross(*T2)) == d
    def closed_pts(T):
        xs = [v[0] for v in T]; ys = [v[1] for v in T]; out = []
        for i in range(min(xs), max(xs) + 1):
            for j in range(min(ys), max(ys) + 1):
                if in_gamma(d, s, (i, j)) and all(cross(T[k], T[(k + 1) % 3], (i, j)) * cross(*T) >= 0 for k in range(3)): out.append((i, j))
        return out
    res['primitive'] = all(sorted(closed_pts(T)) == sorted(T) for T in (T1, T2))
    edges = lambda T: [(T[k], T[(k + 1) % 3]) for k in range(3)]
    res['edges_graver_in_F'] = all(is_graver(d, s, (q[0] - p[0], q[1] - p[1])) and p in Fs and q in Fs for T in (T1, T2) for p, q in edges(T))
    # (c1) Graver segments between points of F
    c1 = True; nseg = 0
    for p, q in itertools.combinations(F, 2):
        g = (q[0] - p[0], q[1] - p[1])
        if is_graver(d, s, g):
            nseg += 1
            if any(seg_meets_open_tri(T, p, q) for T in (T1, T2)): c1 = False
    res['c1_segments_miss'] = c1
    # (c2) parallelogram cells: corners in F, independent Graver g,h; test containment of the centroid of T_i and vertices-in-T
    c2 = True; npar = 0
    Gv = {}
    def gr(g):
        if g not in Gv: Gv[g] = is_graver(d, s, g)
        return Gv[g]
    cen = [(Fr(sum(v[0] for v in T), 3), Fr(sum(v[1] for v in T), 3)) for T in (T1, T2)]
    for u in F:
        for v, w in itertools.combinations(F, 2):
            g = (v[0] - u[0], v[1] - u[1]); h = (w[0] - u[0], w[1] - u[1])
            if cross((0, 0), g, h) == 0: continue
            z = (v[0] + w[0] - u[0], v[1] + w[1] - u[1])
            if z not in Fs: continue
            if not (gr(g) and gr(h)): continue
            if u > min(v, w, z) and False: continue
            npar += 1
            cs = [u, v, z, w]
            for c in cen:
                if all(cross(cs[k], cs[(k + 1) % 4], c) * cross(u, v, w) >= 0 for k in range(4)) and cross(u, v, w) != 0:
                    # centroid in closed parallelogram: then check whether this parallelogram really contains T entirely or meets its interior
                    c2 = False
    res['c2_parallelograms_miss_centroids'] = c2
    res['n_graver_segments'] = nseg; res['n_parallelograms_ordered'] = npar
    res['ok'] = all(v for k, v in res.items() if isinstance(v, bool))
    res['beta1_lower_bound'] = 2 if res['ok'] else None
    return res


if __name__ == '__main__':
    import sys
    for d in range(3, int(sys.argv[1]) + 1):
        for s in range(1, d):
            if gcd(s, d) == 1:
                r = check_hollow(d, s)
                if not r['ok']: print('FAIL', d, s, r)
    print('done')
