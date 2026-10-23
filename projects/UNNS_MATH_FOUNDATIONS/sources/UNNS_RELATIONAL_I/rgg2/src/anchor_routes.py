"""Positive-integer UNNS anchor routes; no dependence on RGG-1 or numpy."""
from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Anchor:
    k: int
    d: int
    def __post_init__(self):
        if type(self.k) is not int or type(self.d) is not int or self.k < 1 or self.d < 2:
            raise ValueError("anchor requires integers k>=1, d>=2")

    @property
    def value(self) -> int:
        return self.k * self.d * self.d

    @property
    def occurrence(self) -> tuple[int, int]:
        return (self.k * (self.d - 1), self.d - 1)


def from_occurrence(m: int, n: int) -> Anchor:
    if type(m) is not int or type(n) is not int or m < 1 or n < 1 or m % n:
        raise ValueError("positive integer occurrence must have n|m")
    return Anchor(m // n, n + 1)


def fibre(m: int) -> tuple[Anchor, ...]:
    if type(m) is not int or m < 1:
        raise ValueError("value must be a positive integer")
    return tuple(Anchor(m // (d*d), d) for d in range(2, __import__('math').isqrt(m)+1) if m % (d*d) == 0)


def prime_exponents(n: int) -> dict[int, int]:
    if type(n) is not int or n < 1:
        raise ValueError("positive integer expected")
    out = {}
    p = 2
    while p*p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p; e += 1
            out[p] = e
        p += 1 if p == 2 else 2
    if n > 1: out[n] = 1
    return out
