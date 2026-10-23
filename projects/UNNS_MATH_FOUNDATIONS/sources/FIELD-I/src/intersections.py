"""Exact positive rational outputs common to fixed nests."""
from fractions import Fraction
from math import gcd, lcm
from .nest import positive, index_number


def common_step(N1: int, N2: int) -> Fraction:
    """Intersection is positive integer multiples of common_step."""
    positive(N1, 'N1'); positive(N2, 'N2')
    return Fraction(lcm(N1 + 1, N2 + 1) ** 2, gcd(N1, N2))


def common_integer_step(N1: int, N2: int) -> int:
    positive(N1, 'N1'); positive(N2, 'N2')
    return lcm(N1 + 1, N2 + 1) ** 2


def is_output_of(x: Fraction, N: int) -> bool:
    positive(N, 'N')
    x = Fraction(x)
    return x > 0 and (x / index_number(N)).denominator == 1


def is_common_output(x: Fraction, N1: int, N2: int) -> bool:
    return is_output_of(x, N1) and is_output_of(x, N2)


def first_common_occurrences(N1: int, N2: int) -> tuple[Fraction, int, int]:
    x = common_step(N1, N2)
    return (x, int(x / index_number(N1)), int(x / index_number(N2)))
