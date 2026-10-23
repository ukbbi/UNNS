"""Original fixed-nest formula, exactly in rational arithmetic."""
from fractions import Fraction


def positive(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def value(M: int, N: int) -> Fraction:
    positive(M, 'M'); positive(N, 'N')
    return Fraction(M * (N + 1) ** 2, N)


def index_number(N: int) -> Fraction:
    positive(N, 'N')
    return Fraction((N + 1) ** 2, N)


def integer_index(N: int) -> int:
    positive(N, 'N')
    return (N + 1) ** 2


def next_occurrence(M: int, N: int, steps: int = 1) -> tuple[int, int]:
    positive(M, 'M'); positive(N, 'N')
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        raise ValueError('steps must be a nonnegative integer')
    return (M + steps, N)


def next_integer_occurrence(M: int, N: int) -> tuple[int, int]:
    positive(M, 'M'); positive(N, 'N')
    if M % N:
        raise ValueError('the starting occurrence must be an integer-output anchor')
    return (M + N, N)


def is_anchor(M: int, N: int) -> bool:
    positive(M, 'M'); positive(N, 'N')
    return M % N == 0
