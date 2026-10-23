"""Exact positive-rational fibres F(a/b), without floating point."""
from fractions import Fraction
from math import isqrt
from .nest import value


def _fraction(x: Fraction | int) -> Fraction:
    if isinstance(x, bool) or not isinstance(x, (int, Fraction)):
        raise TypeError('value must be an int or Fraction')
    x = Fraction(x)
    if x <= 0:
        raise ValueError('value must be positive')
    return x


def admissible_d(x: Fraction | int) -> list[int]:
    """d>=2, d*d | numerator a, d==1 (mod denominator b)."""
    x = _fraction(x)
    a, b = x.numerator, x.denominator
    return [d for d in range(2, isqrt(a) + 1)
            if a % (d * d) == 0 and (d - 1) % b == 0]


def occurrences(x: Fraction | int) -> list[tuple[int, int]]:
    """All positive integer (M,N) with M (N+1)^2 / N == x."""
    x = _fraction(x)
    a, b = x.numerator, x.denominator
    return sorted([((a // (d * d)) * ((d - 1) // b), d - 1)
                   for d in admissible_d(x)], key=lambda z: (z[1], z[0]))


def multiplicity(x: Fraction | int) -> int:
    return len(admissible_d(x))


def is_field(x: Fraction | int) -> bool:
    return _fraction(x).denominator > 1


def brute_occurrences(x: Fraction | int, max_M: int, max_N: int) -> list[tuple[int, int]]:
    """Independent bounded enumeration (test oracle, not a theorem)."""
    x = _fraction(x)
    return sorted(((M, N) for N in range(1, max_N + 1)
                   for M in range(1, max_M + 1)
                   if value(M, N) == x), key=lambda z: (z[1], z[0]))
