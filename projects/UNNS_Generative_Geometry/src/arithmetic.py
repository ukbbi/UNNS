"""Exact A0 occurrence arithmetic. Standard library only."""
from fractions import Fraction


def factor(n):
    if n < 1:
        raise ValueError("positive integer required")
    out = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p + 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def valuations(n):
    """Finite-support nonnegative prime valuation dictionary."""
    return factor(n)


def square_root_part(n):
    out = 1
    for p, e in factor(n).items():
        out *= p ** (e // 2)
    return out


def all_divisors(n):
    ds = [1]
    for p, e in factor(n).items():
        ds = [d * p ** k for d in ds for k in range(e + 1)]
    return sorted(ds)


def D(x):
    x = Fraction(x)
    if x <= 0:
        raise ValueError("positive rational x required")
    a, b = x.numerator, x.denominator
    return tuple(d for d in all_divisors(square_root_part(a)) if d >= 2 and (d - 1) % b == 0)


def occurrences(x):
    """Return (N,M) sorted by d=N+1; x = M(N+1)^2/N."""
    x = Fraction(x)
    a, b = x.numerator, x.denominator
    out = []
    for d in D(x):
        N = d - 1
        q, r = divmod(a * N, b * d * d)
        assert r == 0
        out.append((N, q))
    return tuple(out)


def exponent_fibre(x):
    """Return exact exponent tuples and primes for the finite fibre."""
    x = Fraction(x)
    ps = tuple(sorted(factor(square_root_part(x.numerator))))
    return ps, tuple(tuple(factor(d).get(p, 0) for p in ps) for d in D(x))
