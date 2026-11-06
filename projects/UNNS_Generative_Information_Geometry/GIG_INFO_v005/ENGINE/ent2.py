"""Exact weighted conditional entropy and mutual information for finite ensembles (Fractions; 40-digit decimal log2 via the v001 routine).
Ensembles are given by per-item rational weights; natural = uniform, balanced = 1/2 mass on each Y class, uniform inside the class."""
from collections import defaultdict
from decimal import Decimal
from fractions import Fraction
import _vpath  # noqa: F401
from information import shannon, fmt


def weights(Y, mode):
    P = sum(1 for y in Y if y)
    M = len(Y) - P
    if mode == "natural":
        return [Fraction(1, len(Y))] * len(Y)
    assert mode == "balanced" and P and M
    return [Fraction(1, 2 * P) if y else Fraction(1, 2 * M) for y in Y]


def profile(Y, sigs, mode, digits=30):
    w = weights(Y, mode)
    py = defaultdict(Fraction)
    cell = defaultdict(lambda: [Fraction(0), Fraction(0)])
    for y, s, wi in zip(Y, sigs, w):
        py[y] += wi
        cell[s][1 if y else 0] += wi
    HY = shannon([py[0], py[1]])
    HYO = Decimal(0)
    mixed = 0
    for s, (a, b) in cell.items():
        t = a + b
        if a and b:
            mixed += 1
            HYO += Decimal(t.numerator) / Decimal(t.denominator) * shannon([a / t, b / t])
    return {"H(Y)": fmt(HY, digits), "H(Y|O)": fmt(HYO, digits), "I(Y;O)": fmt(HY - HYO, digits), "classes": len(cell), "mixed_classes": mixed}
