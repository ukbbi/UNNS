"""Parity-congruence occurrence families and classical parity-lattice Graver vectors."""
from itertools import product
from math import prod
from fractions import Fraction
from .arithmetic import D, factor


def parity_benchmark(primes):
    primes = tuple(primes)
    if len(set(primes)) != len(primes) or any(p <= 1 or p % 3 != 2 or factor(p) != {p: 1} for p in primes):
        raise ValueError("distinct primes, all congruent to 2 mod 3, required")
    k = len(primes)
    x = Fraction(prod(primes) ** 4, 3)
    pts = [tuple(a) for a in product(range(3), repeat=k) if sum(a) % 2 == 0 and any(a)]
    from_indices = {prod(p ** a for p, a in zip(primes, v)) for v in pts}
    assert set(D(x)) == from_indices
    return x, tuple(pts)


def graver_basis(k, oriented=False):
    """±2e_i and ±e_i±e_j. oriented=True takes one of each opposite pair."""
    V = set()
    for i in range(k):
        for sign in (-1, 1):
            v = [0] * k
            v[i] = 2 * sign
            V.add(tuple(v))
    for i in range(k):
        for j in range(i + 1, k):
            for si in (-1, 1):
                for sj in (-1, 1):
                    v = [0] * k
                    v[i], v[j] = si, sj
                    V.add(tuple(v))
    if oriented:
        V = {v for v in V if next(t for t in v if t) > 0}
    return tuple(sorted(V))
