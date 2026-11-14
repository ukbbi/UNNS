"""
UNNS-U1-BND shared library: exact graph engines and the nine path identities.

The graph G has vertex set the positive integers and edges
        k*N  ---  k*(N+1)**2          (k, N >= 1).
All arithmetic is exact (Python integers, sympy rationals). No floating point.
"""
import random
from math import gcd, isqrt, prod

import sympy as sp

# ------------------------------------------------------------------ edges
def is_edge(x, y):
    """Closed-form edge test (x ~ y in G), O(1) arithmetic.
    For x < y the relation y = x (N+1)^2 / N, N | x, is equivalent to
    N^2 + (2 - y/x) N + 1 = 0 with N a positive integer dividing x."""
    if x == y:
        return False
    if x > y:
        x, y = y, x
    disc = y * y - 4 * x * y
    if disc < 0:
        return False
    r = isqrt(disc)
    if r * r != disc:
        return False
    for sgn in (1, -1):
        num = (y - 2 * x) + sgn * r
        if num > 0 and num % (2 * x) == 0:
            N = num // (2 * x)
            if N >= 1 and x % N == 0 and x // N * (N + 1) ** 2 == y:
                return True
    return False


def is_edge_bruteforce(x, y):
    """Direct reading of the definition: {x, y} = {kN, k(N+1)^2}."""
    for a, b in ((x, y), (y, x)):
        for N in range(1, a + 1):
            if a % N == 0 and (a // N) * (N + 1) ** 2 == b:
                return True
    return False


def fwd(x, N):
    if N < 1 or x % N:
        raise ValueError(("forward step not admissible", x, N))
    return x // N * (N + 1) ** 2


def inv(x, N):
    q = N + 1
    if N < 1 or x % (q * q):
        raise ValueError(("inverse step not admissible", x, N))
    return x // (q * q) * N


# --------------------------------------------- fast engine (Pollard rho)
_SMALL = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
_rng = random.Random(20261108)


def _is_prime(n):
    if n < 2:
        return False
    for p in _SMALL:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _SMALL:
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
        c = _rng.randrange(1, n)
        x = y = _rng.randrange(2, n)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return d


_FAC = {}


def factor(n):
    if n in _FAC:
        return _FAC[n]
    res, m = {}, n
    for p in _SMALL + [41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        while m % p == 0:
            res[p] = res.get(p, 0) + 1
            m //= p
    stack = [m] if m > 1 else []
    while stack:
        x = stack.pop()
        if x == 1:
            continue
        if _is_prime(x):
            res[x] = res.get(x, 0) + 1
            continue
        d = _rho(x)
        stack += [d, x // d]
    _FAC[n] = res
    return res


def divisors(m):
    ds = [1]
    for p, e in factor(m).items():
        ds = [d * p ** k for d in ds for k in range(e + 1)]
    return ds


def sq_roots(m):
    """all q >= 2 with q^2 | m"""
    qs = [1]
    for p, e in factor(m).items():
        qs = [q * p ** k for q in qs for k in range(e // 2 + 1)]
    return [q for q in qs if q > 1]


def neighbours_fast(m):
    s = set()
    for N in divisors(m):
        s.add(m // N * (N + 1) ** 2)
    for q in sq_roots(m):
        s.add(m // (q * q) * (q - 1))
    s.discard(m)
    return s


# -------------------------------- independent engine (trial division only)
def neighbours_simple(m):
    s, i = set(), 1
    while i * i <= m:
        if m % i == 0:
            for N in {i, m // i}:
                s.add(m // N * (N + 1) ** 2)
        i += 1
    q = 2
    while q * q <= m:
        if m % (q * q) == 0:
            s.add(m // (q * q) * (q - 1))
        q += 1
    s.discard(m)
    return s


def ball(x, r, nb):
    """All vertices within distance r of x (uncapped). Returns {vertex: distance}."""
    dist, front = {x: 0}, [x]
    for d in range(1, r + 1):
        nxt = []
        for m in front:
            for v in nb(m):
                if v not in dist:
                    dist[v] = d
                    nxt.append(v)
        front = nxt
    return dist


def distance(a, b, nb=neighbours_fast, maxd=6):
    """Exact d(a,b) when d <= maxd (maxd <= 6), else None.
    If d(a,b) = t, a geodesic has a vertex within ceil(t/2) of a and floor(t/2) of b;
    so the first t at which the radius-(ceil, floor) balls meet is the exact distance."""
    for t in range(0, maxd + 1):
        da = ball(a, (t + 1) // 2, nb)
        db = ball(b, t // 2, nb)
        small, large = (da, db) if len(da) < len(db) else (db, da)
        if any(v in large for v in small):
            return t
    return None


def lower_bound_certificate(a, b, t, nb=neighbours_fast):
    """Sizes of the balls whose empty intersection certifies d(a,b) >= t+1."""
    ra, rb = (t + 1) // 2, t // 2
    da, db = ball(a, ra, nb), ball(b, rb, nb)
    small, large = (da, db) if len(da) < len(db) else (db, da)
    return dict(radius_a=ra, radius_b=rb, size_a=len(da), size_b=len(db),
                intersection=sum(1 for v in small if v in large))


# ------------------------------------------------------- the nine identities
T = sp.symbols("t", integer=True, nonnegative=True)

# (name, M, r, t0, steps) ; n = M*t + r ; steps = [(dir, N(t))] ; '+' forward, '-' inverse
_I = [
    ("A", 4, 1, 1, [("+", 4*T+1), ("-", 2*T), ("+", T), ("-", 2*T+1)]),
    ("B", 8, 0, 1, [("+", 2), ("+", 2), ("-", 8), ("+", 4*T), ("-", 8*T+1)]),
    ("C", 8, 2, 0, [("+", 2), ("+", 4*T+1), ("+", 2), ("-", 8), ("-", 8*T+3)]),
    ("D", 8, 4, 0, [("+", 2), ("+", 2), ("-", 8), ("+", 2*(2*T+1)), ("-", 8*T+5)]),
    ("E", 8, 6, 0, [("+", 2), ("+", 4*T+3), ("+", 2), ("-", 8), ("-", 8*T+7)]),
    ("F", 24, 3, 1, [("+", 8*T+1), ("-", 4*T), ("+", 3*T), ("-", 6*T+1)]),
    ("G", 8, 7, 0, [("+", 8*T+7), ("+", T+1), ("+", T+1), ("-", 2*T+3), ("-", 2*T+3), ("-", 2*(T+1))]),
    ("H", 24, 11, 0, [("+", 24*T+11), ("+", 24), ("-", 2*(25*T+12)), ("+", 25*T+12), ("-", 25*(2*T+1)), ("-", 4)]),
    ("I", 24, 19, 0, [("+", 1), ("+", 24*T+19), ("-", 3), ("-", 3*(4*T+3)), ("+", 4*T+3), ("-", 6*T+5)]),
]
IDENTITIES = [dict(name=n, M=M, r=r, t0=t0, steps=[(d, sp.sympify(e)) for d, e in st])
              for (n, M, r, t0, st) in _I]
SPECIAL = {1: [1, 4, 18, 81, 8, 2], 3: [3, 16, 4]}   # explicit paths for n = 1, 3


def identity_for(n):
    """Return (identity, t) covering n, or None for n in SPECIAL."""
    if n in SPECIAL:
        return None
    if n % 4 == 1:
        return IDENTITIES[0], (n - 1) // 4
    m8 = n % 8
    if m8 in (0, 2, 4, 6):
        k = {0: 1, 2: 2, 4: 3, 6: 4}[m8]
        return IDENTITIES[k], (n - IDENTITIES[k]["r"]) // 8
    if m8 == 7:
        return IDENTITIES[6], (n - 7) // 8
    k = {3: 5, 11: 7, 19: 8}[n % 24]            # n == 3 mod 8
    return IDENTITIES[k], (n - IDENTITIES[k]["r"]) // 24


_LAMBDA = {}


def labels_at(ident, t):
    key = ident["name"]
    if key not in _LAMBDA:
        _LAMBDA[key] = [(d, sp.lambdify(T, e, modules=[])) for d, e in ident["steps"]]
    return [(d, int(f(t)) if callable(f) else int(f)) for d, f in _LAMBDA[key]]


def replay(n):
    """Walk n -> n+1 with plain integers via the identity (or explicit special path).
    Returns the list of states, validating every step against the edge definition."""
    if n in SPECIAL:
        path = SPECIAL[n]
        # special paths end at n+1 only for n=3 -> 4; n=1 -> 2
        assert path[0] == n and path[-1] == n + 1
        return path
    ident, t = identity_for(n)
    x, states = n, [n]
    for d, N in labels_at(ident, t):
        x = fwd(x, N) if d == "+" else inv(x, N)
        states.append(x)
    assert x == n + 1
    return states


# ---------------------------------------------------- symbolic certificates
def certify(ident):
    """Exact symbolic certificate of one identity. Returns dict with per-step data
    and a boolean 'ok'. Each step is certified by its cofactor k(t):
       forward  step:  s_i = k * N,        s_{i+1} = k * (N+1)^2
       inverse  step:  s_i = k * (N+1)^2,  s_{i+1} = k * N
    Requirements for all integers t >= t0: N(t) >= 1 and integral, k(t) >= 1 and integral."""
    M, r, t0 = ident["M"], ident["r"], ident["t0"]
    s = sp.expand(M * T + r)
    rows, ok, notes = [], True, []

    def integer_valued(poly_expr):
        p = sp.Poly(sp.expand(poly_expr), T)
        deg = max(p.degree(), 0)
        return all(sp.Rational(p.eval(k)).q == 1 for k in range(0, deg + 1))

    def positive_from_t0(poly_expr):
        # sufficient: all coefficients >= 0 and value at t0 >= 1
        p = sp.Poly(sp.expand(poly_expr), T)
        return all(c >= 0 for c in p.all_coeffs()) and p.eval(t0) >= 1

    for i, (d, N) in enumerate(ident["steps"]):
        N = sp.expand(N)
        okN = integer_valued(N) and positive_from_t0(N)
        den = N if d == "+" else (N + 1) ** 2
        q, rem = sp.div(sp.Poly(s, T), sp.Poly(sp.expand(den), T))
        if rem.as_expr() != 0:
            ok = False
            notes.append(f"step {i+1}: cofactor not polynomial")
            k = sp.nan
            nxt = sp.nan
        else:
            k = sp.expand(q.as_expr())
            okk = integer_valued(k) and positive_from_t0(k)
            if not okk:
                ok = False
                notes.append(f"step {i+1}: cofactor not integral/positive on t>=t0")
            nxt = sp.expand(k * (N + 1) ** 2) if d == "+" else sp.expand(k * N)
        if not okN:
            ok = False
            notes.append(f"step {i+1}: label not integral/positive on t>=t0")
        rows.append(dict(step=i + 1, dir=d, N=N, k=k, before=s, after=nxt))
        s = nxt
    if sp.expand(s - (M * T + r + 1)) != 0:
        ok = False
        notes.append("endpoint is not n+1")
    return dict(name=ident["name"], M=M, r=r, t0=t0, length=len(ident["steps"]),
                rows=rows, ok=ok, notes=notes)
