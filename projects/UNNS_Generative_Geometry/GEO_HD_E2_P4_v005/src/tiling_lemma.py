"""v005 explicit tiling lemma (Lemma T) -- exact implementation of the LIFTING construction used in the proof, and its checks.
Lemma T.  V = (v_1..v_n) nonzero integer vectors spanning R^d, Z(V) = sum [0,1] v_i.  For generic integer heights w, put
v~_i = (v_i, w_i) in R^{d+1}.  For every d-subset S with det(V_S) != 0 let nu_S be the normal of span(v~_S) with nu_S[d] < 0 and
A_S = { i not in S : nu_S . v~_i > 0 }.  Then the parallelotopes  T_S = sum_{i in A_S} v_i + Z(V_S)  are the projections of the lower facets of
the lifted zonotope; they cover Z(V), have disjoint interiors (fine zonotopal tiling, Bohne-Dress / lifting), and every vertex of every T_S
is a SUBSET SUM of V."""
from fractions import Fraction as Fr
from itertools import combinations
import random


def det(M):
    n = len(M)
    A = [[Fr(x) for x in row] for row in M]
    d = Fr(1)
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None:
            return Fr(0)
        if p != c:
            A[c], A[p] = A[p], A[c]
            d = -d
        d *= A[c][c]
        for i in range(c + 1, n):
            if A[i][c] != 0:
                f = A[i][c] / A[c][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return d


def lift_tiles(V, w):
    d = len(V[0]); n = len(V)
    Vt = [tuple(v) + (wi,) for v, wi in zip(V, w)]
    tiles = []
    for S in combinations(range(n), d):
        if det([V[i] for i in S]) == 0:
            continue
        rows = [Vt[i] for i in S]
        nu = [(-1) ** j * det([[r[c] for c in range(d + 1) if c != j] for r in rows]) for j in range(d + 1)]
        if nu[d] > 0:
            nu = [-x for x in nu]
        assert nu[d] != 0
        A = []
        for i in range(n):
            if i in S:
                continue
            s = sum(a * b for a, b in zip(nu, Vt[i]))
            if s == 0:
                raise ValueError("heights not generic")
            if s > 0:
                A.append(i)
        tiles.append((tuple(A), S))
    return tiles


def zonotope_volume(V):
    d = len(V[0])
    return sum(abs(det([V[i] for i in S])) for S in combinations(range(len(V)), d))


def solve(M, rhs):
    n = len(M)
    A = [[Fr(x) for x in row] + [Fr(r)] for row, r in zip(M, rhs)]
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None:
            return None
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [A[i][n] for i in range(n)]


def in_tile(V, tile, x):
    A, S = tile
    d = len(V[0])
    base = [sum(V[i][c] for i in A) for c in range(d)]
    M = [[V[s][c] for s in S] for c in range(d)]  # columns = generators
    mu = solve(M, [Fr(x[c]) - base[c] for c in range(d)])
    return mu is not None and all(0 <= m <= 1 for m in mu)


def check_configuration(V, rng, n_points=60):
    """returns (volume_ok, covered_ok, n_tiles); raises on non-generic heights (caller retries)"""
    n = len(V); d = len(V[0])
    w = [rng.randint(-10 ** 6, 10 ** 6) for _ in range(n)]
    tiles = lift_tiles(V, w)
    vol_ok = sum(abs(det([V[i] for i in S])) for A, S in tiles) == zonotope_volume(V)
    cov_ok = True
    for _ in range(n_points):
        lam = [Fr(rng.randint(0, 12), 12) for _ in range(n)]
        x = [sum(l * v[c] for l, v in zip(lam, V)) for c in range(d)]
        if not any(in_tile(V, t, x) for t in tiles):
            cov_ok = False
            break
    return vol_ok, cov_ok, len(tiles)


def random_configs(rng, d, count, nmax, rmax=4):
    out = []
    while len(out) < count:
        n = rng.randint(d, nmax)
        V = [tuple(rng.randint(-rmax, rmax) for _ in range(d)) for _ in range(n)]
        if any(not any(v) for v in V):
            continue
        if rank_int(V) < d:
            continue
        out.append(V)
    return out


def rank_int(V):
    from mini import rank
    return rank(V)


def conformal_decomposition(v, member):
    """Graver conformal decomposition by induction on the L1 norm: returns a list of conformally-minimal vectors summing to v, each conformally below v.
    member(x) -> bool is the lattice oracle (v itself must be a member)."""
    from itertools import product
    from mini import conf_le
    if not any(v):
        return []
    # find a conformally-below, nonzero, lattice vector of minimal L1 norm: it is Graver
    rng = [range(0, x + 1) if x >= 0 else range(x, 1) for x in v]
    below = [s for s in product(*rng) if any(s) and member(s)]
    g = min(below, key=lambda s: sum(abs(t) for t in s))
    rest = tuple(a - b for a, b in zip(v, g))
    return [g] + conformal_decomposition(rest, member)
