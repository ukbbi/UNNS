"""Original within-nest unary successor and exact leakage witnesses."""
from fractions import Fraction
from math import isqrt
from .nest import value, next_occurrence, next_integer_occurrence, index_number
from .fibres import occurrences


def next_value(M: int, N: int) -> Fraction:
    return value(*next_occurrence(M, N))


def next_integer_value(M: int, N: int) -> int:
    return int(value(*next_integer_occurrence(M, N)))


def reconstruct_consecutive(x: Fraction, y: Fraction) -> tuple[int, int]:
    """Inverse coordinate chart for (S_N(M), S_N(M+1)); not a relational selection."""
    x, y = Fraction(x), Fraction(y)
    delta = y - x
    if delta <= 0:
        raise ValueError('not a positive fixed-nest increment')
    N = 1 if delta == 4 else (delta.numerator // delta.denominator - 2)
    if N < 1 or index_number(N) != delta:
        raise ValueError('difference is not a fixed-nest index number')
    M = x / index_number(N)
    if M.denominator != 1 or M.numerator < 1:
        raise ValueError('starting value is not an occurrence at this nest')
    M = int(M)
    if next_value(M, N) != y:
        raise ValueError('not consecutive fixed-nest values')
    return M, N


def reconstruct_integer_neighbors(x: int, y: int) -> tuple[int, int]:
    """Recover an integer anchor (M,N) from its current and next integer terms."""
    if not isinstance(x, int) or not isinstance(y, int) or x < 1 or y <= x:
        raise ValueError('positive increasing integer values required')
    d = isqrt(y - x)
    if d < 2 or d * d != y - x:
        raise ValueError('difference is not a square of a nest index')
    N = d - 1
    M = Fraction(x, index_number(N))
    if M.denominator != 1 or M.numerator < 1 or M.numerator % N:
        raise ValueError('current value is not an integer anchor of this nest')
    return M.numerator, N


def next_options(x: Fraction) -> list[tuple[tuple[int, int], Fraction]]:
    """Endpoint-level set of possible successors; no route selection intended."""
    return [(occ, next_value(*occ)) for occ in occurrences(x)]
