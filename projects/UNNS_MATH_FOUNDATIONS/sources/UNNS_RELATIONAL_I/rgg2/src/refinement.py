"""Partially defined value-preserving route refinements."""
from .anchor_routes import Anchor
from .joint_ops import j_join

def t(q: int, r: Anchor) -> Anchor | None:
    if type(q) is not int or q < 1:
        raise ValueError("q must be a positive integer")
    q2 = q * q
    return Anchor(r.k // q2, r.d * q) if r.k % q2 == 0 else None

def simultaneous_covariance(q: int, r: Anchor, s: Anchor) -> bool | None:
    tr, ts = t(q, r), t(q, s)
    if tr is None or ts is None:
        return None
    return j_join(tr, ts) == t(q, j_join(r, s))
