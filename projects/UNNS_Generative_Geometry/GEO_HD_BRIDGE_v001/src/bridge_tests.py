"""HD-E2: shared-observation relation R_P (snapshot level only) and the exact trajectory facts that can be stated."""
from fractions import Fraction
from field_adapter import val, C
from prime_geometry import vp


def R_P(m, x, P):
    """snapshot correspondence: integer SELECT-II state m and FIELD-I state x have equal valuations on P"""
    return tuple(vp(m, p) for p in P) == val(x, P)


def T1(m): return 4 * m          # SELECT-II edge with label 1: m * (1+1)^2 / 1


def cube_C3_equals_T1(x):
    """True iff C^3(x) = 4x (for a realized x with three defined iterates)"""
    y = x
    for _ in range(3):
        y = C(y)
        if y is None: return None
    return y == 4 * Fraction(x)
