#!/usr/bin/env python3
"""SCR-III-B PREFLIGHT_v009 -- numerical tolerance policy (PROPOSED FOR TESTING; constants are NOT frozen).

Four distinct quantities (all relative to Q = sum_{i<j}|K_ij|, a scale known before any scan; Q >= max|H|):

  eps_input   = 2^-52 Q            resolution of the INPUT DATA: couplings are stored as binary64, so energies closer than this to a threshold
                                   cannot be ordered physically from the stored data -> UNRESOLVED_BOUNDARY.
  eps_direct  = (npairs+4) 2^-53 Q rigorous bound on the error of ONE direct double-precision energy evaluation (sequential sum of npairs terms).
  eps_gray    = 1e-10 Q            margin for ALL incremental/bounded energies (Gray code resynchronised every 256 steps => rigorous drift
                                   <= 256^2 * 2^-53 * Q ~ 1.4e-11 Q; G2/B1 accumulate <= 24 steps; margin is >7x the rigorous bound).
  tau         = 1e-9 Q  (PROPOSED) target-membership tolerance: S_T^tau(W) = { H <= E0 + W + tau }.
  (level grouping) 1e-9 * max|E|   physical level-degeneracy clustering used by v006/v007 for REPORTING levels (not for membership).

Ordering that must hold: eps_input < eps_direct < eps_gray < tau.
Membership cascade used by every solver: scan energy certain (|E-Ecut| > eps_gray) -> else direct energy certain (|E-Ecut| > eps_direct)
-> else __float128 energy; if |E_hp - Ecut| <= eps_input the state is UNRESOLVED_BOUNDARY and is CONSERVATIVELY INCLUDED in the target
(the target is only ever enlarged, so a tolerance can never turn an excluded target into a preserved one).

Preservation of the tolerance-expanded target:   PRESERVED  <=>  W + tau < Delta_nonG      (Delta_nonG = min_{s not in S_G}(H - E0))
"""
from fractions import Fraction

REL_TAU = 1e-9
REL_GRAY = 1e-10
LEVEL_GROUPING_REL = 1e-9


def Q_of(pairs):
    return sum(abs(k) for _, _, k in pairs)


def hierarchy(Q, npairs, rel_tau=REL_TAU):
    h = dict(Q=Q, eps_input=2.0 ** -52 * Q, eps_direct=(npairs + 4) * 2.0 ** -53 * Q, eps_gray=REL_GRAY * Q, tau=rel_tau * Q,
             level_grouping_rel_of_max_abs_E=LEVEL_GROUPING_REL)
    h["ordering_ok"] = h["eps_input"] < h["eps_direct"] < h["eps_gray"] < h["tau"]
    return h


def drift_bound_rigorous(Q, resync=256):
    """Worst-case accumulated rounding of the incremental energy between exact resynchronisations (first-order bound)."""
    return resync * resync * 2.0 ** -53 * Q


def energy_exact(n, pairs, s):
    """Exact rational energy of state s (couplings are exactly the stored binary64 values)."""
    e = Fraction(0)
    for i, j, k in pairs:
        e += -Fraction(k) if ((s >> i) ^ (s >> j)) & 1 else Fraction(k)
    return e


def membership_oracle(E_exact, E0, W, tau, eps_input):
    """Exact-rational oracle: 'IN' / 'OUT' / 'UNRESOLVED' (unresolved is treated as IN by the policy)."""
    cut = Fraction(E0) + Fraction(W) + Fraction(tau)
    d = Fraction(E_exact) - cut
    if abs(d) <= Fraction(eps_input):
        return "UNRESOLVED"
    return "IN" if d < 0 else "OUT"


def members_tau(E, E0, W, tau):
    return {i for i, e in enumerate(E) if e <= E0 + W + tau}


def preservation(delta, W, tau, eps_input=0.0, empty_excluded=False):
    """Classification of the tolerance-expanded preservation criterion.  delta=None or empty_excluded -> S_G = S_0.
    returns (status, reason, flags)."""
    if empty_excluded or delta is None:
        return "PASS", "NO_EXCLUDED_STATE", ["EMPTY_EXCLUDED_SET_NOT_INFORMATIVE"]
    if delta == 0:
        return "FAIL", "ZERO_GAP_GROUND_LEVEL_EXCLUDED", []
    cut = W + tau
    if abs(delta - cut) <= eps_input:
        return "FAIL", "UNRESOLVED_BOUNDARY_TREATED_CONSERVATIVELY", ["UNRESOLVED_BOUNDARY"]
    if delta > cut:
        return "PASS", "GAP_ABOVE_W_PLUS_TAU", []
    if delta == cut:
        return "FAIL", "GAP_EQUALS_W_PLUS_TAU", []
    return "FAIL", "GAP_BELOW_W_PLUS_TAU", []


def rho(delta, W):
    return None if (delta is None or delta <= 0) else W / delta
