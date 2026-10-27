"""G6-C2 / E2: hollow box Q=(d,d), general s.  For every unit s (s != -1, d>=3) checks EXACTLY that
   conv(F) \\ U = int T1 u int T2,  T1 = tri((0,d),(d-t,d-1),(d,d)),  T2 = tri((d,0),(d-1,d-s),(d,d)),  t = s^-1 mod d  (total area d),
and (for d <= BMAX) beta_1(U) = 2 via the v005 chain complex.   Method: v005 exact uncovered-region routine (all cells), compare with T1 u T2
by exact polygon area of (uncovered minus T) and (T minus uncovered).  usage: hollow_check.py DMIN DMAX BMAX OUT"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from math import gcd
import coverage as C
from coverage import mpq
from lattice_model import Lat, U_betti


def tri(a, b, c): return [(mpq(p[0]), mpq(p[1])) for p in (a, b, c)]


def a2(poly): return abs(C.area2(poly))


def inter_area2(P, T):
    """twice the area of P cap T for convex polygons (T given as triangle, ccw-normalised)"""
    if C.area2(T) < 0: T = T[::-1]
    r = P
    n = len(T)
    for i in range(n):
        p, q = T[i], T[(i + 1) % n]
        a = -(q[1] - p[1]); b = (q[0] - p[0]); c = a * p[0] + b * p[1]
        r = C.clip(r, -a, -b, -c)
        if len(r) < 3: return 0
    return abs(C.area2(r))


def check(d, s):
    t = next(t for t in range(1, d + 1) if (s * t) % d == 1)
    T1 = tri((0, d), (d - t, d - 1), (d, d)); T2 = tri((d, 0), (d - 1, d - s), (d, d))
    pcs = C.uncovered(Lat(d, d, d, s), (d, d))
    tot = sum(a2(p) for p in pcs)
    inT = sum(inter_area2(p, T1) + inter_area2(p, T2) for p in pcs)
    ok = (tot == 2 * d and inT == tot and a2(T1) + a2(T2) == 2 * d)          # area2 totals: 2*(d/2+d/2) = 2d  -> compare in area2 units
    return ok, tot, inT


if __name__ == '__main__':
    dmin, dmax, bmax, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rows = []; bad = 0
    for d in range(dmin, dmax + 1):
        for s in range(1, d):
            if gcd(s, d) != 1 or s == d - 1: continue
            ok, tot, inT = check(d, s)
            r = {'d': d, 's': s, 'two_triangles_exact': bool(ok), 'uncovered_area2': str(tot)}
            if d <= bmax: b = U_betti(Lat(d, d, d, s), (d, d))[0]; r['beta1'] = b[1]; r['betti'] = b
            rows.append(r); bad += (not ok)
    json.dump({'range': [dmin, dmax], 'n_types': len(rows), 'n_bad': bad, 'rows': rows}, open(out, 'w'))
    print('hollow two-triangle structure: types', len(rows), 'violations', bad)
