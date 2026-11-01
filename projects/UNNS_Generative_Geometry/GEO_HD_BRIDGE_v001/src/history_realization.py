"""HD-C2/C3: realization of histories as lattice paths in valuation space; area bivector; injectivity; closure polygons."""
from fractions import Fraction
from itertools import combinations
from prime_geometry import delta, traj, vp, factor, full_prime_support


def omega(w, P):
    """area bivector Omega(w) = sum_{i<j} d_i ^ d_j  as dict {(p,q): sum_{i<j}(d_i^p d_j^q - d_i^q d_j^p)} for p<q in P"""
    ds = [delta(N, P) for N in w]; out = {}
    for a, p in enumerate(P):
        for b, q in enumerate(P):
            if a < b:
                s = 0
                for i in range(len(ds)):
                    for j in range(i + 1, len(ds)):
                        s += ds[i][a] * ds[j][b] - ds[i][b] * ds[j][a]
                out[(p, q)] = s
    return out


def shoelace2(pts):
    """twice the signed area of the closed lattice polygon"""
    s = 0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]): s += x1 * y2 - x2 * y1
    return s


def state_trace(m, w):
    out = [m]
    for N in w:
        m = m // N * (N + 1) ** 2; out.append(m)
    return out


def parallel_pairs(Nmax):
    """pairs a<b<=Nmax whose displacement vectors are parallel (linearly dependent) over the full prime support"""
    from fractions import Fraction
    res = []
    vec = {}
    for N in range(1, Nmax + 1):
        P = sorted(set(factor(N)) | set(factor(N + 1)))
        vec[N] = {p: 2 * vp(N + 1, p) - vp(N, p) for p in P}
    for a, b in combinations(range(1, Nmax + 1), 2):
        P = sorted(set(vec[a]) | set(vec[b]))
        va = [vec[a].get(p, 0) for p in P]; vb = [vec[b].get(p, 0) for p in P]
        if all(va[i] * vb[j] - va[j] * vb[i] == 0 for i in range(len(P)) for j in range(i + 1, len(P))): res.append((a, b))
    return res
