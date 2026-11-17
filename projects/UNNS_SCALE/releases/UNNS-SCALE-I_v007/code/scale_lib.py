"""UNNS-SCALE-I  --  shared library (standard library only).

Arithmetic graph G of the SELECT-II transition  T_N(x) = x (N+1)^2 / N,  N | x.
Vertices: positive integers.  Edges: { kN , k(N+1)^2 },  k, N >= 1.

Nothing here modifies or imports frozen UNNS releases; the graph is rebuilt
from the definition quoted in PROVENANCE.md.
"""
from collections import deque
from itertools import product


# ---------------------------------------------------------------- factoring
def factor(n):
    """Prime factorisation of n >= 1 as {p: e} by trial division."""
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def merge(f, g):
    h = dict(f)
    for p, e in g.items():
        h[p] = h.get(p, 0) + e
    return h


def divisors(f, cap=None):
    """All divisors of the number with factorisation f (exponent cap optional)."""
    ps = sorted(f)
    ranges = [range((f[p] if cap is None else min(f[p], cap(f[p]))) + 1) for p in ps]
    out = []
    for es in product(*ranges):
        d = 1
        for p, e in zip(ps, es):
            d *= p ** e
        out.append(d)
    return out


def from_factor(f):
    n = 1
    for p, e in f.items():
        n *= p ** e
    return n


# ---------------------------------------------------------- local structure
def tau(f):
    t = 1
    for e in f.values():
        t *= e + 1
    return t


def sq_count(f):
    """s(u) = #{q >= 2 : q^2 | u}."""
    t = 1
    for e in f.values():
        t *= e // 2 + 1
    return t - 1


def degree(f):
    """deg_G(u) = tau(u) + #{q>=2: q^2 | u}   (derived in THEORY, Lemma 0)."""
    return tau(f) + sq_count(f)


def neighbours(f):
    """Complete neighbourhood of u (factorisation f) as a set of
    (direction, N, v):  '+' : v = u(N+1)^2/N  with N | u
                        '-' : v = uN/(N+1)^2  with (N+1)^2 | u."""
    u = from_factor(f)
    out = set()
    for N in divisors(f):
        out.add(("+", N, u // N * (N + 1) ** 2))
    for q in divisors(f, cap=lambda e: e // 2):
        if q >= 2:
            N = q - 1
            out.add(("-", N, u // (q * q) * N))
    return out


# ------------------------------------------------------------- finite graph
def build_graph(L):
    """Adjacency lists of G[1..L] (induced subgraph on 1..L)."""
    adj = [[] for _ in range(L + 1)]
    N = 1
    while (N + 1) ** 2 <= L:
        s = (N + 1) ** 2
        for k in range(1, L // s + 1):
            u, v = k * N, k * s
            adj[u].append(v)
            adj[v].append(u)
        N += 1
    return adj


def edge_set(L):
    """Set of edges (u,v), u<v, of G[1..L]."""
    E = set()
    N = 1
    while (N + 1) ** 2 <= L:
        s = (N + 1) ** 2
        for k in range(1, L // s + 1):
            E.add((k * N, k * s))
        N += 1
    return E


def bfs_distance(adj, src, dst):
    """Shortest-path length src->dst inside the given finite graph (None if unreachable)."""
    if src == dst:
        return 0
    seen = {src}
    q = deque([(src, 0)])
    while q:
        u, d = q.popleft()
        for v in adj[u]:
            if v not in seen:
                if v == dst:
                    return d + 1
                seen.add(v)
                q.append((v, d + 1))
    return None


# ------------------------------------------------------------ representation
def to_coords(n, B):
    return divmod(n, B)


def from_coords(q, r, B):
    if not (0 <= r < B):
        raise ValueError("remainder out of range")
    return B * q + r


def to_mixed(n, radices):
    """Mixed-radix digits, least significant radix first (radices = [B1,...,Bd])."""
    digs = []
    for B in radices:
        n, r = divmod(n, B)
        digs.append(r)
    digs.append(n)  # leading (unbounded) coordinate
    return digs


def from_mixed(digs, radices):
    n = digs[-1]
    for r, B in zip(reversed(digs[:-1]), reversed(radices)):
        if not (0 <= r < B):
            raise ValueError("digit out of range")
        n = n * B + r
    return n


# ------------------------------------------------- compact graph (needs numpy)
def build_csr(L):
    """CSR adjacency of G[1..L] using numpy (indptr, indices)."""
    import numpy as np
    us, vs = [], []
    N = 1
    while (N + 1) ** 2 <= L:
        s = (N + 1) ** 2
        k = np.arange(1, L // s + 1, dtype=np.int64)
        us.append(k * N)
        vs.append(k * s)
        N += 1
    u = np.concatenate(us); v = np.concatenate(vs)
    src = np.concatenate([u, v]); dst = np.concatenate([v, u])
    order = np.argsort(src, kind="stable")
    src, dst = src[order], dst[order]
    indptr = np.zeros(L + 2, dtype=np.int64)
    np.add.at(indptr, src + 1, 1)
    indptr = np.cumsum(indptr)
    return indptr, dst


def csr_distance(csr, a, b, max_d=40):
    """Exact distance a-b inside the CSR graph by bidirectional layered BFS.
    Returns None if unreachable inside the truncation."""
    indptr, ind = csr
    if a == b:
        return 0
    da, db = {a: 0}, {b: 0}
    fa, fb = [a], [b]
    ra = rb = 0
    while fa and fb and ra + rb < max_d:
        if len(fa) <= len(fb):
            new = []
            for u in fa:
                for v in ind[indptr[u]:indptr[u + 1]].tolist():
                    if v not in da:
                        da[v] = ra + 1
                        new.append(v)
            fa, ra = new, ra + 1
            hit = [da[v] + db[v] for v in new if v in db]
        else:
            new = []
            for u in fb:
                for v in ind[indptr[u]:indptr[u + 1]].tolist():
                    if v not in db:
                        db[v] = rb + 1
                        new.append(v)
            fb, rb = new, rb + 1
            hit = [da[v] + db[v] for v in new if v in da]
        if hit:
            return min(hit)
    return None
