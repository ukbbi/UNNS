"""GIG-I v001 -- information observables of a finite history fibre.

All probabilities are exact Fractions.  Logarithms are evaluated with the standard-library `decimal` module
at a stated working precision (default 50 digits), so every reported value carries its precision.
Probability model is always explicit: 'uniform' means the uniform distribution on the finite fibre.
"""
from decimal import Decimal, getcontext
from fractions import Fraction
from math import log2 as _flog2

PREC = 50


def _ctx():
    getcontext().prec = PREC + 10


def log2_dec(x):
    """log2 of a positive int/Fraction as Decimal (working precision PREC+10)."""
    _ctx()
    x = Fraction(x)
    assert x > 0
    return (Decimal(x.numerator).ln() - Decimal(x.denominator).ln()) / Decimal(2).ln()


def fmt(d, digits=PREC):
    """format a Decimal to `digits` significant digits"""
    _ctx()
    return format(+d, ".%df" % digits) if abs(d) < 10 ** 6 else str(d)


def empty_fibre_convention():
    """A(t) for an empty fibre: undefined as log2(0); we use the convention A(t) = None (no history exists)."""
    return None


def hartley(n):
    """A = log2 n for a nonempty finite fibre of size n (Decimal)."""
    if n == 0:
        return empty_fibre_convention()
    return log2_dec(n)


def shannon(probs):
    """H = -sum p log2 p for exact Fractions p (zero terms omitted); probs must sum to 1."""
    probs = [Fraction(p) for p in probs]
    assert sum(probs) == 1, "probabilities must sum to 1"
    _ctx()
    return -sum((Decimal(p.numerator) / Decimal(p.denominator)) * log2_dec(p) for p in probs if p > 0)


def class_entropy(sizes):
    """H(C|T=t) under the uniform model: sizes = component sizes n_1..n_k, N = sum."""
    N = sum(sizes)
    return shannon([Fraction(n, N) for n in sizes])


def within_class_entropy(sizes):
    """H(W|C,T=t) under the uniform model = sum_i (n_i/N) log2 n_i."""
    N = sum(sizes)
    _ctx()
    return sum((Decimal(n) / Decimal(N)) * log2_dec(n) for n in sizes if n > 1)


def information_profile(prof, rmax=None):
    """I_r(t) = (1/N) sum_v log2 |B_r(v)|  for r = 0..rmax (default: up to stabilisation). Returns list of Decimal.
    `prof` is a swap_graph.ball_profile."""
    from swap_graph import ball_product
    N = len(prof)
    if rmax is None:
        rmax = max(len(p) - 1 for p in prof)
    out = []
    for r in range(rmax + 1):
        out.append(log2_dec(ball_product(prof, r)) / Decimal(N))
    return out


def uniform_chain(pieces):
    """Exact uniform-model chain rule for a fibre that is a disjoint union of pieces, each a disjoint union of
    swap classes.  `pieces` = {piece_key: [class sizes]}.  Returns dict of Decimals:
      H(P|T)   piece entropy (source+content)
      H(C|P,T) class entropy inside pieces
      H(W|C,T) within-class entropy
      H(W|T)   = log2 N  (and the sum of the three)."""
    N = sum(sum(s) for s in pieces.values())
    _ctx()
    HP = shannon([Fraction(sum(s), N) for s in pieces.values()])
    HC = Decimal(0)
    HW = Decimal(0)
    for s in pieces.values():
        n = sum(s)
        w = Decimal(n) / Decimal(N)
        HC += w * class_entropy(s)
        HW += w * within_class_entropy(s)
    return {"H(P|T)": HP, "H(C|P,T)": HC, "H(W|C,T)": HW, "H(W|T)": HP + HC + HW, "A": log2_dec(N), "N": N}
