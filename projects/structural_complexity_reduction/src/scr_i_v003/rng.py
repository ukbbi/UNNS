from __future__ import annotations

import math


class P4LCG:
    """Exact port of Chamber LIII `seededRandom` (32-bit LCG)."""

    __slots__ = ("state",)

    def __init__(self, seed: int):
        self.state = int(seed) & 0xFFFFFFFF

    def random(self) -> float:
        self.state = (self.state * 1664525 + 1013904223) & 0xFFFFFFFF
        return self.state / 4294967296.0


class LIISeededRandom:
    """Port of Chamber LII's JS Number + bitwise LCG.

    JavaScript evaluates the multiplication as IEEE-754 Number and then applies a
    bitwise `& 0x7fffffff`. Python float is IEEE-754 binary64 as well, so the
    float multiplication is intentional here before conversion to int.
    """

    __slots__ = ("state",)

    def __init__(self, seed: int):
        self.state = int(seed)

    def random(self) -> float:
        expr = float(self.state) * 1103515245.0 + 12345.0
        # JS bitwise conversion keeps the low 32 bits; & 0x7fffffff keeps 31.
        self.state = int(expr) & 0x7FFFFFFF
        return self.state / 0x7FFFFFFF


def js_floor(x: float) -> int:
    return math.floor(x)
