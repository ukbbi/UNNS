#!/usr/bin/env python3
"""Candidate deterministic tie policy (PROPOSED FOR TESTING ONLY -- constants are NOT frozen).

Target membership:   s in T  <=>  E(s) <= E0 + W + tau          (tolerance can only ENLARGE the target)
Preservation:        PRESERVED  <=>  W + tau < Delta           (Delta = min over excluded states of E - E0)
Consequence: tolerance can never turn an excluded target into a preserved one; it can only turn a marginal PASS into a FAIL
(conservative). The tolerance is relative to a scale that is known BEFORE any scan: sum_{i<j} |K_ij| >= max|H|.
"""
from fractions import Fraction

PROPOSED_REL = 1e-9          # proposed for test; final constant must be frozen before inspecting real 3x3 thresholds


def tau_abs(sum_abs_K, rel=PROPOSED_REL):
    return rel * sum_abs_K


def members(E, E0, W, tau):
    return {i for i, e in enumerate(E) if e <= E0 + W + tau}


def members_exact(E, E0, W):
    """Exact-rational reference (no tolerance, inclusive endpoint)."""
    t = Fraction(E0) + Fraction(W)
    return {i for i, e in enumerate(E) if Fraction(e) <= t}


def classify(delta, W, tau):
    """delta = min_{excluded}(E - E0) or None if nothing is excluded."""
    if delta is None:
        return "NOT_INFORMATIVE_EMPTY_EXCLUDED_SET"
    if delta <= tau:
        return "NO_PRESERVING_WINDOW_GROUND_LEVEL_EXCLUDED"
    return "PRESERVED" if (W + tau) < delta else "FAIL_AT_OR_ABOVE_GAP"


def boundary_flag(delta, W, tau):
    return delta is not None and abs(W - delta) <= tau
