"""GEO-HD-1B / E2-P1 -- exact arithmetic of the FIELD-I orbit and its occurrence fibres.

Standard library only; every quantity is an int or a Fraction.

Objects (kept distinct):  x (rational state) -> D(x) (occurrence indices d=N+1)
-> F_x (fibre in exponent coordinates over the primes of s(a)) -> Lambda_b (relation lattice)
-> G (region Graver set).  Scope: FIELD-I collective map C(x)=x+L^2/G, never SELECT-II.
"""
from fractions import Fraction
from itertools import product
from math import gcd


# ------------------------------------------------------------------ number theory
def factor(n):
    if n < 1:
        raise ValueError("positive integer required")
    out, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p + 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def sqrt_part(n):
    s = 1
    for p, e in factor(n).items():
        s *= p ** (e // 2)
    return s


def divisors(n):
    ds = [1]
    for p, e in factor(n).items():
        ds = [d * p ** k for d in ds for k in range(e + 1)]
    return sorted(ds)


def D(x):
    """Occurrence indices d=N+1 of x=a/b: {d>=2 : d^2 | a, d = 1 mod b} (Vol. I Thm 1.2)."""
    x = Fraction(x)
    a, b = x.numerator, x.denominator
    return tuple(d for d in divisors(sqrt_part(a)) if d >= 2 and (d - 1) % b == 0)


def occurrences(x):
    """(N, M) with M(N+1)^2/N = x, sorted by d=N+1."""
    x = Fraction(x)
    a, b = x.numerator, x.denominator
    out = []
    for d in D(x):
        N = d - 1
        M, r = divmod(a * N, b * d * d)
        assert r == 0
        out.append((N, M))
    return tuple(out)


def lcm_list(vs):
    L = 1
    for v in vs:
        L = L * v // gcd(L, v)
    return L


def C_step(x):
    """FIELD-I collective map: L=lcm D(x), G=gcd{d-1}, C(x)=x+L^2/G.  Returns a record."""
    x = Fraction(x)
    ds = D(x)
    if not ds:
        raise ValueError("empty fibre: C undefined")
    L = lcm_list(ds)
    G = 0
    for d in ds:
        G = gcd(G, d - 1)
    inc = Fraction(L * L, G)
    return {"x": x, "L": L, "G": G, "increment": inc, "next": x + inc}


def orbit(x0, steps):
    x = Fraction(x0)
    recs = []
    for n in range(steps + 1):
        ds = D(x)
        r = {"n": n, "x": x, "a": x.numerator, "b": x.denominator, "D": ds}
        if ds and n < steps:
            r.update({k: v for k, v in C_step(x).items() if k != "x"})
            r["L"] = r["L"]
        elif ds:
            r["L"] = lcm_list(ds)
            g = 0
            for d in ds:
                g = gcd(g, d - 1)
            r["G"] = g
        recs.append(r)
        if n < steps:
            x = r["next"]
    return recs


# ------------------------------------------------------------------ fibre in exponent coordinates
def coordinate_data(x):
    """primes P of s(a), box q_p=floor(v_p(a)/2), denominator b."""
    x = Fraction(x)
    a, b = x.numerator, x.denominator
    fa = factor(a)
    P = tuple(sorted(p for p, e in fa.items() if e // 2 >= 1))
    q = tuple(fa[p] // 2 for p in P)
    return {"primes": P, "box": q, "b": b}


def chi(alpha, primes, b):
    """prod p_i^alpha_i mod b (negative exponents by modular inverse)."""
    r = 1 % b
    for p, a in zip(primes, alpha):
        base = pow(p, -1, b) if a < 0 else p
        r = r * pow(base, abs(a), b) % b if b > 1 else 0
    return r % b if b > 1 else 0


def in_lattice(alpha, primes, b):
    return b == 1 or chi(alpha, primes, b) == 1


def fibre(x):
    """F_x = (Lambda_b cap [0,q]) minus {0}, as sorted exponent tuples."""
    cd = coordinate_data(x)
    P, q, b = cd["primes"], cd["box"], cd["b"]
    pts = [a for a in product(*[range(m + 1) for m in q]) if any(a) and in_lattice(a, P, b)]
    return tuple(sorted(pts))


def index_of(alpha, primes):
    d = 1
    for p, a in zip(primes, alpha):
        d *= p ** a
    return d


def check_fibre_matches_D(x):
    """Cross-check of Vol. I Thm 1.2 in exponent coordinates (assert)."""
    cd = coordinate_data(x)
    ds = {index_of(a, cd["primes"]) for a in fibre(x)}
    assert ds == set(D(x)), (ds, D(x))
    return True


# ------------------------------------------------------------------ region Graver set
def conformal_le(g, h):
    return all(gi * hi >= 0 and abs(gi) <= abs(hi) for gi, hi in zip(g, h))


def region_graver(primes, b, q):
    """Conformally minimal nonzero vectors of Lambda_b inside [-q,q] (GEO-I v002 sec. 1)."""
    box = [range(-m, m + 1) for m in q]
    L = [v for v in product(*box) if any(v) and in_lattice(v, primes, b)]
    out = []
    for v in L:
        if not any(w != v and conformal_le(w, v) for w in L):
            out.append(v)
    return tuple(sorted(out))


def lex_positive(v):
    for t in v:
        if t:
            return t > 0
    return False


def oriented(G):
    return tuple(g for g in G if lex_positive(g))


# ------------------------------------------------------------------ transport at vertex / move level
def vertex_transport(F_src, F_tgt):
    """Occurrence-vertex map F_src -> F_tgt (identity on exponent tuples over a common prime set)."""
    T = set(F_tgt)
    return {"preserved": sorted(v for v in F_src if v in T),
            "lost": sorted(v for v in F_src if v not in T),
            "new": sorted(v for v in F_tgt if v not in set(F_src))}


def move_transport(G_src, G_tgt):
    T = set(G_tgt)
    return {"surviving_moves": sorted(g for g in G_src if g in T),
            "lost_moves": sorted(g for g in G_src if g not in T),
            "new_moves": sorted(g for g in G_tgt if g not in set(G_src))}


def stage_record(n, x):
    cd = coordinate_data(x)
    P, q, b = cd["primes"], cd["box"], cd["b"]
    F = fibre(x)
    G = region_graver(P, b, q)
    return {"n": n, "x": str(x), "a": x.numerator, "b": b, "primes": list(P), "box": list(q),
            "fibre_size": len(F), "fibre": [list(v) for v in F],
            "indices_D": list(D(x)), "occurrences_NM": [list(t) for t in occurrences(x)],
            "lattice": "Z^k" if b == 1 else "ker chi_%d" % b,
            "graver_region": [list(g) for g in G]}
