"""Engine for UNNS_GRAPH_ENT_v001: arithmetic graph G, subgraphs F(x), nonbacktracking matrices, theta-graph formulas."""
import math, itertools
from math import gcd
from fractions import Fraction
import numpy as np
from mpmath import mp, mpf, findroot, log as mlog
mp.dps = 50

def adjacent(u, v):
    """u~v in G iff some k,N>=1 with {u,v}={kN,k(N+1)^2}. Equivalent: smaller/larger in lowest terms is q/(q+1)^2."""
    if u == v: return False
    if u > v: u, v = v, u
    g = gcd(u, v); q = u // g; p = v // g
    return p == (q + 1) ** 2

def adjacent_def(u, v):
    """Direct definition (slow): exists N>=1, N | u, v = u (N+1)^2 / N, for the smaller u."""
    if u > v: u, v = v, u
    return any(u % N == 0 and u * (N + 1) ** 2 == v * N for N in range(1, u + 1))

def divisors(n):
    ds = [1]
    for p, k in factor(n).items():
        ds = [d * p ** j for d in ds for j in range(k + 1)]
    return sorted(ds)

def factor(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1 if d == 2 else 2
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def tau(n):
    t = 1
    for k in factor(n).values(): t *= k + 1
    return t

def up_neighbours(x):
    return [(N, x * (N + 1) ** 2 // N) for N in divisors(x)]

def down_neighbours(x):
    out = []
    d = 2
    while d * d <= x:
        if x % (d * d) == 0: out.append((d - 1, x * (d - 1) // (d * d)))
        d += 1
    return out

def degree(x): return len(up_neighbours(x)) + len(down_neighbours(x))

# ---- the finite arithmetic subgraphs F(x): hub edge {x,4x} and one path x - y_N - 4y_N - 4x per divisor N>=2
def F_edges(x):
    E = [(x, 4 * x)]
    for N in divisors(x):
        if N >= 2:
            y = x * (N + 1) ** 2 // N
            E += [(x, y), (y, 4 * y), (4 * y, 4 * x)]
    return E

def F_vertices(x):
    V = {x, 4 * x}
    for N in divisors(x):
        if N >= 2:
            y = x * (N + 1) ** 2 // N; V |= {y, 4 * y}
    return sorted(V)

def Fm_edges(m): return F_edges(2 ** m)

# ---- nonbacktracking edge matrix
def nb_matrix(edges):
    """B on directed edges: (a->b) -> (b->c) iff c != a. Returns (list of directed edges, integer numpy matrix)"""
    de = []
    for a, b in edges: de += [(a, b), (b, a)]
    idx = {e: i for i, e in enumerate(de)}
    out = {}
    for (a, b) in de: out.setdefault(a, []).append(b)
    n = len(de); B = np.zeros((n, n), dtype=np.int64)
    for (a, b) in de:
        for c in out.get(b, []):
            if c != a: B[idx[(a, b)], idx[(b, c)]] = 1
    return de, B

# ---- theta graphs
def theta_edges(lengths):
    """vertices 'u','v' joined by internally disjoint paths of the given lengths"""
    E = []
    for i, l in enumerate(lengths):
        pts = ['u'] + [(i, t) for t in range(1, l)] + ['v']
        E += [(pts[t], pts[t + 1]) for t in range(l)]
    return E

def theta_root(lengths):
    """largest real root > 1 of sum 1/(lam^l+1) = 1 (requires >=3 paths), 50 digits"""
    f = lambda lam: sum(1 / (lam ** l + 1) for l in lengths) - 1
    lo, hi = mpf(1), mpf(2)
    while f(hi) > 0: hi *= 2
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def lam_m(m):
    """positive root of lam^3 - lam^2 + lam = m"""
    lo, hi = mpf(0), mpf(m) + 2
    for _ in range(220):
        mid = (lo + hi) / 2
        if mid ** 3 - mid ** 2 + mid < m: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def power_sums_cubic(m, N):
    """s_n = sum of n-th powers of the roots of l^3 - l^2 + l - m"""
    s = [3, 1, -1]
    s.append(s[2] - s[1] + 3 * m)  # s_3 = e1 s_2 - e2 s_1 + 3 e3
    # recurrence s_n = s_{n-1} - s_{n-2} + m s_{n-3}, n>=4 (also valid n=3 up to the 3 e3 term, handled above)
    while len(s) <= N: s.append(s[-1] - s[-2] + m * s[-3])
    return s

def trace_formula(m, n):
    """tr(B_m^n) from the factorisation det(l - B) = (l^6-1)^{m-1} (l^2-1) g(l) (-g(-l))"""
    s = power_sums_cubic(m, max(n, 4))
    return 6 * (m - 1) * (1 if n % 6 == 0 else 0) + (1 + (-1) ** n) * (1 + s[n])

def int_matrix_power_trace(B, n):
    M = np.array(B, dtype=object); R = np.identity(len(B), dtype=object)
    e = n
    while e:
        if e & 1: R = R.dot(M)
        M = M.dot(M); e >>= 1
    return int(sum(R[i, i] for i in range(len(B))))
