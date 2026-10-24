"""Exact engine for the collective map C(x) = x + L(x)^2/G(x) on positive rationals.
Independent of the verifiers in the source records: written from the definitions of Volume II.
Everything is exact integer / Fraction arithmetic."""
import random, math
from fractions import Fraction as Fr
from math import gcd, isqrt

# ---------- primes and factorisation (Miller-Rabin + Pollard rho) ----------
_SP = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
def is_prime(n):
    if n < 2: return False
    for p in _SP:
        if n % p == 0: return n == p
    d, r = n - 1, 0
    while d % 2 == 0: d //= 2; r += 1
    for a in _SP:
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
def _rho(n, rng=random.Random(12345)):
    if n % 2 == 0: return 2
    while True:
        c = rng.randrange(1, n); x = y = rng.randrange(0, n); d = 1
        while d == 1:
            x = (x * x + c) % n; y = (y * y + c) % n; y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n: return d
def factor(n, res=None):
    if res is None: res = {}
    if n == 1: return res
    for p in _SP:
        while n % p == 0: res[p] = res.get(p, 0) + 1; n //= p
    if n == 1: return res
    # small trial division speeds typical cases
    f = 41
    while f < 2000 and f * f <= n:
        while n % f == 0: res[f] = res.get(f, 0) + 1; n //= f
        f += 2
    if n == 1: return res
    if is_prime(n): res[n] = res.get(n, 0) + 1; return res
    d = _rho(n); factor(d, res); factor(n // d, res); return res
def divisors_from(f):
    ds = [1]
    for p, e in f.items(): ds = [d * p ** k for d in ds for k in range(e + 1)]
    return ds
def lcm(a, b): return a // gcd(a, b) * b
def small_primes(n): return [p for p in range(2, n + 1) if is_prime(p)]
def ordmod(a, m):
    if m == 1: return 1
    a %= m; x = a; k = 1
    while x != 1:
        x = x * a % m; k += 1
        if k > m: return None
    return k

# ---------- fibres and the collective map (direct, from the definitions) ----------
def fibre(x):
    """D(x) = {d >= 2 : d^2 | a, d = 1 mod b} for x = a/b in lowest terms (sorted list)."""
    a, b = x.numerator, x.denominator
    f = factor(a)
    s = {p: e // 2 for p, e in f.items() if e // 2}
    return sorted(d for d in divisors_from(s) if d >= 2 and (d - 1) % b == 0)
def Gof(D):
    g = 0
    for d in D: g = gcd(g, d - 1)
    return g
def Lof(D):
    L = 1
    for d in D: L = lcm(L, d)
    return L
def Cstep(x):
    D = fibre(x)
    if not D: return None
    L, G = Lof(D), Gof(D)
    return x + Fr(L * L, G)
def direct(x0, N, keepx=False):
    """first N states of the orbit of x0 under C; rows (n, gamma, L, G, R[, x])."""
    x = Fr(x0); rows = []
    for n in range(N):
        D = fibre(x)
        if not D: return rows
        L, G = Lof(D), Gof(D)
        gam = x * G / (L * L)
        assert gam.denominator == 1
        row = (n, int(gam), L, G, len(D)) + ((x,) if keepx else ())
        rows.append(row)
        x = x + Fr(L * L, G)
    return rows

# ---------- the residue (class) machine of Volume II, Chapter 4 ----------
def _prodset(sets, g):
    cur = {1 % g}
    for R in sets:
        cur = {a * r % g for a in cur for r in R}
    return cur
def _fib_exps(g, w, E):
    """x = w L^2/g with L = prod p^E[p] coprime to g.  Returns (persistent?, exponents of lcm D(x'), exponents of sigma')."""
    h = gcd(g, w); b = g // h
    fw = factor(w // h) if w // h > 1 else {}
    Es = {}
    for p in set(E) | set(fw):
        e = E.get(p, 0) + fw.get(p, 0) // 2
        if e > 0: Es[p] = e
    ps = sorted(Es)
    res = {p: [pow(p, k, g) for k in range(Es[p] + 1)] for p in ps}
    # persistence: every d | sigma', d >= 2, d = 1 mod b must satisfy d = 1 mod g
    # enumerate residues with a 'nontrivial' flag
    cur = {(1 % g, False)}
    for p in ps:
        cur = {(a * r % g, ne or k > 0) for (a, ne) in cur for k, r in enumerate(res[p])}
    ok = all(not (ne and (a - 1) % b == 0 and a != 1 % g) for (a, ne) in cur)
    E1 = {}
    for p in ps:
        oth = _prodset([res[q] for q in ps if q != p], g)
        m = 0
        for k in range(1, Es[p] + 1):
            pk = res[p][k]
            if any((pk * a - 1) % b == 0 for a in oth): m = k
        if m: E1[p] = m
    return ok, E1
def mstep(g, gamma, E):
    """one step of the class machine: (gamma', E', carry dict) or None when the step is not G-preserving."""
    w = gamma + 1
    ok, E1 = _fib_exps(g, w, E)
    if not ok: return None
    D = {p: E1.get(p, 0) - E.get(p, 0) for p in E1 if E1.get(p, 0) > E.get(p, 0)}
    r2 = 1
    for p, d in D.items(): r2 *= p ** (2 * d)
    assert w % r2 == 0
    return w // r2, E1, D
def lval(E):
    v = 1
    for p, e in E.items(): v *= p ** e
    return v
def state_to_x(g, gamma, E): return Fr(gamma * lval(E) ** 2, g)
def exact_G(g, gamma, E, cap=3_000_000):
    """exact G(x) for x = gamma L^2/g (L from E) via lazy enumeration of the divisors of the square-root part."""
    x = state_to_x(g, gamma, E)
    a, b = x.numerator, x.denominator
    # square-root part from known exponents plus factorisation of gamma
    f = dict((p, 2 * e) for p, e in E.items())
    for p, e in (factor(gamma) if gamma > 1 else {}).items(): f[p] = f.get(p, 0) + e
    s = {p: e // 2 for p, e in f.items() if e // 2}
    size = 1
    for e in s.values(): size *= e + 1
    if size > cap: return None
    G = 0
    for d in divisors_from(s):
        if d >= 2 and (d - 1) % b == 0: G = gcd(G, d - 1)
    return G
def normalise(g, gamma0, Eseed):
    """x0 = gamma0 * Lseed^2 / g re-expressed with L = lcm D(x0): returns (gamma, E) or None if G(x0) != g."""
    if any(gcd(p, g) > 1 for p in Eseed): return None
    x = state_to_x(g, gamma0, Eseed)
    D = fibre(x) if max(Eseed.values(), default=0) < 60 and lval(Eseed) < 10 ** 400 else None
    if D is None: return None
    if not D or Gof(D) != g: return None
    L = Lof(D)
    gam = x * g / (L * L)
    assert gam.denominator == 1
    return int(gam), {p: e for p, e in factor(L).items()}

# ---------- carry-level predictor (reset states) ----------
def avail(g, E, M):
    f = factor(M)
    if any(g % p == 0 for p in f): return False
    c = 1
    for p, j in f.items(): c = c * pow(p, E.get(p, 0) + j, g) % g
    qs = [q for q in E if q not in f and E[q] > 0]
    A = _prodset([[pow(q, k, g) for k in range(E[q] + 1)] for q in qs], g)
    return pow(c, -1, g) in A
def next_M(g, E):
    for M in range(2, isqrt(g - 1) + 1):
        if avail(g, E, M):
            E2 = dict(E)
            for p, j in factor(M).items(): E2[p] = E2.get(p, 0) + j
            return M, E2
    return None
def pend_j(g, E, p):
    o = ordmod(p, g)
    if o is None: return None
    qs = [q for q in E if q != p and E[q] > 0]
    A = _prodset([[pow(q, k, g) for k in range(E[q] + 1)] for q in qs], g)
    e = E.get(p, 0)
    for j in range(1, o + 1):
        if pow(pow(p, e + j, g), -1, g) in A: return j
    return None
def abs_set(g, E, p):
    o = ordmod(p, g)
    qs = [q for q in E if q != p and E[q] > 0]
    A = _prodset([[pow(q, k, g) for k in range(E[q] + 1)] for q in qs], g)
    return o, {k for k in range(o) if pow(pow(p, k, g), -1, g) in A}
def cyc_gaps(S, o):
    a = sorted(S)
    return [((a[(i + 1) % len(a)] - a[i]) % o) or o for i in range(len(a))]
def min_period(S, o):
    for s in range(1, o + 1):
        if o % s == 0 and all(((k + s) % o in S) == (k in S) for k in range(o)): return s

# ---------- bounds ----------
def f4(a): return a // 4 + 1
def kappa(a):
    k = 0
    while a > 1: a = f4(a); k += 1
    return k
def kappa_closed(a):
    k = 0
    while 3 * a > 2 * 4 ** k + 1: k += 1
    return k
def kappa3(t):
    k = 0
    while t > 3: t = f4(t); k += 1
    return k
def Pg(g):
    lim = 4 * g if g % 2 == 0 else g
    return [p for p in small_primes(isqrt(lim)) if g % p and p * p < lim] if g > 1 else []
def Hclass(g):
    h = 1
    for p in Pg(g): h *= 2 * ordmod(p, g) - 1
    return h
def Kpoly(g):
    P = Pg(g); o = [ordmod(p, g) for p in P]
    Phi = sum(x - 1 for x in o); Sig = sum(o); om = max(o) if o else 0
    return (Phi + 1) * (Sig + (Sig + 1) * (om + 1) + 1)

# ---- accelerate factoring by remembering primes met so far ----
_KNOWN = set()
_factor_raw = factor
def factor(n, res=None):  # noqa: F811
    if res is None: res = {}
    if n == 1: return res
    for p in sorted(_KNOWN):
        if p * p > n and n > 1: break
        if n % p == 0:
            while n % p == 0: res[p] = res.get(p, 0) + 1; n //= p
    if n == 1: return res
    r = _factor_raw(n, {})
    for p, e in r.items():
        res[p] = res.get(p, 0) + e
        _KNOWN.add(p)
    return res
