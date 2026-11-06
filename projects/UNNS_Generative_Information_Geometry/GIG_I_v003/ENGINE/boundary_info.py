"""GIG-I v003 -- third-boundary invariants and domain-relative information measures.
J_3 = rank d_3 ;  D_3 = f_3 - J_3 = dim ker d_3 restricted to 3-chains (3-cycle space of the 3-skeleton) ;
A_3([G]; D) = log2 |R_3([G]; D)|,  R_3([G]; D) = { J_3(X) : X in D, swap graph of X ~ G }   (domain-relative: depends on D).
Accounting identity: beta_2 = f_2 - rank d_2 - J_3."""
import math
from collections import Counter, defaultdict


def invariants(f, ranks):
    """f = (f_0..f_{k-1}); ranks = (rank d_1..rank d_{k-1}).  returns dict with J3, D3, beta2 via the accounting identity."""
    J3 = ranks[2] if len(ranks) > 2 else 0
    return {"f3": f[3], "J3": J3, "D3": f[3] - J3, "beta2": f[2] - ranks[1] - J3}


def entropy(counter):
    n = sum(counter.values())
    return -sum(c / n * math.log2(c / n) for c in counter.values() if c)


def cond_entropy(pairs):
    """H(Y|X) in bits for a list of (x, y) pairs, uniform over the list."""
    byx = defaultdict(Counter)
    for x, y in pairs:
        byx[x][y] += 1
    n = len(pairs)
    return sum(sum(c.values()) / n * entropy(c) for c in byx.values())


def A3(values_in_class):
    """A_3 of one graph class given the J_3 values of its domain members."""
    return math.log2(len(set(values_in_class)))
