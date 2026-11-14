"""Exact engine for the UNNS arithmetic graph G.
V = positive integers, E = {{kN, k(N+1)^2} : k,N >= 1}   (N = 1 included).
Written for UNNS_GRAPH_GEOMETRY_v001; independent of the earlier release code."""
from math import isqrt
from functools import lru_cache
from sympy import factorint

def is_edge_def(x, y):
    """Literal reading of the definition (slow, for cross-checks)."""
    for a, b in ((x, y), (y, x)):
        for N in range(1, a + 1):
            if a % N == 0 and (a // N) * (N + 1) ** 2 == b:
                return True
    return False

def fwd(x, N):
    assert N >= 1 and x % N == 0, ("illegal +N", x, N)
    return x // N * (N + 1) ** 2

def inv(x, N):
    assert N >= 1 and x % ((N + 1) ** 2) == 0, ("illegal -N", x, N)
    return x // ((N + 1) ** 2) * N

def move(x, sign, N):
    return fwd(x, N) if sign == '+' else inv(x, N)

@lru_cache(maxsize=None)
def _fac(m):
    return factorint(m)

def divisors(m):
    ds = [1]
    for p, e in _fac(m).items():
        ds = [d * p ** k for d in ds for k in range(e + 1)]
    return ds

def square_roots(m):
    """all q >= 2 with q^2 | m"""
    qs = [1]
    for p, e in _fac(m).items():
        qs = [q * p ** k for q in qs for k in range(e // 2 + 1)]
    return [q for q in qs if q >= 2]

def nbrs(m):
    """neighbour set of m; forward: N | m  -> m(N+1)^2/N ; inverse: q^2 | m (q=N+1>=2) -> m(q-1)/q^2."""
    s = {m // N * (N + 1) ** 2 for N in divisors(m)}
    s |= {m // (q * q) * (q - 1) for q in square_roots(m)}
    return s

def nbrs_trial(m):
    """second, independent implementation: trial division only."""
    s = set()
    for N in range(1, m + 1):
        if m % N == 0:
            s.add(m // N * (N + 1) ** 2)
    q = 2
    while q * q <= m:
        if m % (q * q) == 0:
            s.add(m // (q * q) * (q - 1))
        q += 1
    return s

def degree_formula(m):
    return len(divisors(m)) + len(square_roots(m))

def ball(x, r):
    dist = {x: 0}; front = [x]
    for d in range(1, r + 1):
        nxt = []
        for m in front:
            for v in nbrs(m):
                if v not in dist:
                    dist[v] = d; nxt.append(v)
        front = nxt
    return dist

def distance(a, b, maxd=8):
    """exact d(a,b) if <= maxd else None (meet in the middle on growing balls)."""
    if a == b: return 0
    for t in range(1, maxd + 1):
        A = ball(a, (t + 1) // 2); B = ball(b, t // 2)
        if any(v in B for v in A): return t
    return None

def geodesic(a, b, t):
    """one shortest path of known length t via parent pointers (BFS from a to radius ceil(t/2), from b floor(t/2))."""
    def tree(x, r):
        par = {x: None}; front = [x]
        for _ in range(r):
            nxt = []
            for m in front:
                for v in nbrs(m):
                    if v not in par: par[v] = m; nxt.append(v)
            front = nxt
        return par
    PA, PB = tree(a, (t + 1) // 2), tree(b, t // 2)
    mid = min(v for v in PA if v in PB)
    left = []; v = mid
    while v is not None: left.append(v); v = PA[v]
    left.reverse()
    right = []; v = PB[mid]
    while v is not None: right.append(v); v = PB[v]
    return left + right

def label_of(x, y):
    """signed label of the edge x -> y: ('+',N) if y>x else ('-',N)."""
    lo, hi = (x, y) if x < y else (y, x)
    for N in divisors(lo):
        if lo // N * (N + 1) ** 2 == hi:
            return ('+', N) if x < y else ('-', N)
    raise ValueError("not an edge")
