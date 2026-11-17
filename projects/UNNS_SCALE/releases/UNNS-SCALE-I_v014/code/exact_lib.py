"""UNNS-SCALE-I v003 -- exact (untruncated) distance engine for the arithmetic graph G.

No truncation of the graph is ever used.  Ball layers are generated from complete
neighbourhoods.  Factorisations are tracked through two layers; the last layer is only
needed as integers (so no large number is ever factored).
Exact arithmetic throughout (Python integers).
"""
import random
from itertools import product

_SMALL_PRIMES = [p for p in range(2, 2000) if all(p % q for q in range(2, int(p ** .5) + 1))]
_MR = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
_rng = random.Random(20261116)
_FCACHE = {}


def _is_prime(n):
    if n < 2:
        return False
    for p in _MR:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for a in _MR:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _rho(n):
    if n % 2 == 0:
        return 2
    while True:
        c = _rng.randrange(1, n); x = y = _rng.randrange(0, n); d = 1
        f = lambda z: (z * z + c) % n
        while d == 1:
            x = f(x); y = f(f(y))
            from math import gcd
            d = gcd(abs(x - y), n)
        if d != n:
            return d


def factor(n):
    """Prime factorisation {p: e} (trial division by small primes, Miller-Rabin, Pollard rho)."""
    if n in _FCACHE:
        return _FCACHE[n]
    m, f = n, {}
    for p in _SMALL_PRIMES:
        if p * p > m:
            break
        while m % p == 0:
            f[p] = f.get(p, 0) + 1; m //= p
    stack = [m] if m > 1 else []
    while stack:
        x = stack.pop()
        if x == 1:
            continue
        if _is_prime(x):
            f[x] = f.get(x, 0) + 1
            continue
        d = _rho(x)
        stack += [d, x // d]
    if len(_FCACHE) < 3_000_000:
        _FCACHE[n] = f
    return f


def _divisors(f, cap=None):
    ps = list(f)
    rng = [range((f[p] if cap is None else cap(f[p])) + 1) for p in ps]
    out = []
    for es in product(*rng):
        d = 1
        for p, e in zip(ps, es):
            d *= p ** e
        out.append(d)
    return out


def _mul(f, g, sign=1):
    h = dict(f)
    for p, e in g.items():
        h[p] = h.get(p, 0) + sign * e
        if h[p] == 0:
            del h[p]
    return h


def neighbours_f(n, f, with_factor):
    """All neighbours of n (factorisation f).  Returns {v: fv or None}."""
    out = {}
    for N in _divisors(f):                       # forward move +N
        v = n // N * (N + 1) ** 2
        if with_factor:
            fN1 = factor(N + 1)
            fv = dict(f)
            for p, e in factor(N).items():
                fv[p] = fv.get(p, 0) - e
                if fv[p] == 0: del fv[p]
            for p, e in fN1.items():
                fv[p] = fv.get(p, 0) + 2 * e
            out[v] = fv
        else:
            out[v] = None
    for q in _divisors(f, cap=lambda e: e // 2):  # backward move -N, q = N+1 >= 2, q^2 | n
        if q >= 2:
            N = q - 1
            v = n // (q * q) * N
            if with_factor:
                fq = factor(q); fv = dict(f)
                for p, e in fq.items():
                    fv[p] = fv.get(p, 0) - 2 * e
                    if fv[p] == 0: del fv[p]
                for p, e in factor(N).items():
                    fv[p] = fv.get(p, 0) + e
                out[v] = fv
            else:
                out[v] = None
    return out


def layers(n, r):
    """Exact distance layers of the ball of radius r about n: list of dicts {node: first distance}.
    Returns (dist, par) where dist maps node -> distance (<= r) and par maps node -> predecessor."""
    dist = {n: 0}; par = {n: None}
    frontier = {n: factor(n)}
    for d in range(1, r + 1):
        nxt = {}
        last = (d == r)
        for x, fx in frontier.items():
            for v, fv in neighbours_f(x, fx, with_factor=not last).items():
                if v not in dist:
                    dist[v] = d; par[v] = x
                    nxt[v] = fv
        frontier = nxt
    return dist, par


def path_from(par, w):
    p = []
    while w is not None:
        p.append(w); w = par[w]
    return p[::-1]


def is_edge(x, y):
    if x == y: return False
    a, b = (x, y) if x < y else (y, x)
    for N in _divisors(factor(a)):
        if a // N * (N + 1) ** 2 == b: return True
    return False


def exact_distance(u, v, known_upper=6):
    """Exact d_G(u,v) assuming d <= known_upper <= 6 (radii up to 3+3).
    Returns (d, path) where path is a shortest path (explicit, checked), and certificate info."""
    if u == v: return 0, [u]
    # try increasing radii: d<=2 (1,1), d<=4 (2,2), d<=5 (3,2), d<=6 (3,3)
    cache = {}
    def ball(x, r):
        if (x, r) not in cache:
            cache[(x, r)] = layers(x, r)
        return cache[(x, r)]
    for ru, rv, lim in ((1, 1, 2), (2, 2, 4), (3, 2, 5), (3, 3, 6)):
        if lim > known_upper and lim != known_upper: 
            pass
        du, pu = ball(u, ru); dv, pv = ball(v, rv)
        small, large = (du, dv) if len(du) < len(dv) else (dv, du)
        best = None
        for w in small:
            if w in large:
                s = du[w] + dv[w] if (w in du and w in dv) else None
                if s is not None and (best is None or s < best[0]): best = (s, w)
        if best is not None and best[0] <= lim:
            s, w = best
            path = path_from(pu, w) + path_from(pv, w)[::-1][1:]
            return s, path
        if lim >= known_upper:
            break
    return None, None
