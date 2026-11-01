"""HD-E0/E1: valuation-strand geometry of FIELD-I collective trajectories."""
from fractions import Fraction
from field_adapter import C, D, strand, val, prime_support

STEP_CYCLE = (Fraction(2), Fraction(3, 2), Fraction(4, 3))


def rigid_entry(xs, tail=12):
    """first index e such that x_{n+3} = 4 x_n for all n >= e within the computed window (requires the last `tail` instances to hold)"""
    n = len(xs); ok = [xs[i + 3] == 4 * xs[i] for i in range(n - 3)]
    if len(ok) < tail or not all(ok[-tail:]): return None
    e = len(ok)
    while e > 0 and ok[e - 1]: e -= 1
    return e


def step_ratios(xs): return [xs[i + 1] / xs[i] for i in range(len(xs) - 1)]


def displacement_rank(xs, P=None):
    P = P or prime_support(xs); rows = []
    for i in range(len(xs) - 1):
        a = val(xs[i], P); b = val(xs[i + 1], P); rows.append([Fraction(q - p) for p, q in zip(a, b)])
    r = 0
    rows = [list(x) for x in rows]
    for c in range(len(P)):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]; rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


def occurrence_sequence(xs): return [tuple(D(x)) for x in xs]
