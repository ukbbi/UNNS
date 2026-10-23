"""Candidate joint operations. Only J_join is the primary RGG-2 hypothesis."""
from math import gcd, lcm
from .anchor_routes import Anchor, fibre

def j_mul(r: Anchor, s: Anchor) -> Anchor:
    return Anchor(r.k * s.k, r.d * s.d)

def j_join(r: Anchor, s: Anchor) -> Anchor:
    return Anchor(lcm(r.k, s.k), lcm(r.d, s.d))

def j_gcd(r: Anchor, s: Anchor) -> Anchor | None:
    d = gcd(r.d, s.d)
    return Anchor(gcd(r.k, s.k), d) if d >= 2 else None

def j_mixed(r: Anchor, s: Anchor) -> Anchor | None:
    d = gcd(r.d, s.d)
    return Anchor(lcm(r.k, s.k), d) if d >= 2 else None

def j_blind(r: Anchor, s: Anchor) -> tuple[Anchor, ...]:
    """Product-value baseline; not a J_join output comparator."""
    return fibre(r.value * s.value)
