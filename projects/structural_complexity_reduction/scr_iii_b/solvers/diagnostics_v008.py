#!/usr/bin/env python3
"""Gap diagnostics: Delta_G = min_{s not in S_G} [H(s) - E0]  and  rho_G = W / Delta_G.

IMPLEMENTED AND UNIT-TESTED HERE; deliberately NOT executed on the real 3x3 patch or on 3x3 nulls in v008 (that belongs after
preregistration freeze and primary unblinding). Public 1x1 / 2x2 values are used only as regression checks of the theorem
   S_T(W) subset S_G  <=>  W < Delta_G.
"""
from tie_policy_v008 import classify, boundary_flag


def delta_G(E, in_grammar, E0=None):
    E0 = min(E) if E0 is None else E0
    ex = [e - E0 for e, g in zip(E, in_grammar) if not g]
    return min(ex) if ex else None


def rho_G(delta, W):
    if delta is None or delta <= 0:
        return None
    return W / delta


def verdict(delta, W, tau):
    """Returns (classification, rho or None, boundary_flag). rho >= 1 <=> FAIL when tau = 0."""
    return classify(delta, W, tau), rho_G(delta, W), boundary_flag(delta, W, tau)
