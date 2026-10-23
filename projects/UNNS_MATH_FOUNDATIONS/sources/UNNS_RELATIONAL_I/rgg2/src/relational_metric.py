"""Exact fibre lift and weighted-L1 logarithmic metric."""
from math import gcd, lcm, log
from .anchor_routes import Anchor, prime_exponents
from .joint_ops import j_join

def lift_ratio(r: Anchor, s: Anchor) -> int:
    """Exact integer v(join)/m, only for equal-value anchors."""
    if r.value != s.value:
        raise ValueError("lift ratio is defined within one value fibre")
    d_ratio = lcm(r.d, s.d) // gcd(r.d, s.d)
    return d_ratio * d_ratio

def distance(r: Anchor, s: Anchor) -> float:
    if r.value != s.value:
        raise ValueError("distance is defined within one value fibre")
    return 2.0 * log(lcm(r.d, s.d) // gcd(r.d, s.d))

def weighted_l1(r: Anchor, s: Anchor) -> float:
    if r.value != s.value:
        raise ValueError("weighted L1 is defined within one value fibre")
    x, y = prime_exponents(r.d), prime_exponents(s.d)
    return 2.0 * sum(abs(x.get(p, 0)-y.get(p, 0))*log(p) for p in x.keys() | y.keys())

def verify_lift(r: Anchor, s: Anchor) -> bool:
    return j_join(r, s).value == r.value * lift_ratio(r, s)
