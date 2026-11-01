"""HD-1D v001: history-count recurrence H(t) = sum_{d>=2, d^2|t} H(t (d-1)/d^2),  H(squarefree) = 1."""
import sys
from functools import lru_cache
from math import comb
sys.setrecursionlimit(10000)
from select_history import predecessors, is_squarefree


@lru_cache(maxsize=None)
def H(t):
    if is_squarefree(t):
        return 1
    return sum(H(m) for _, m in predecessors(t))


@lru_cache(maxsize=None)
def H_from(t, m0):
    """number of histories from the FIXED source m0 to t (m0 arbitrary, empty history counts when t == m0)"""
    if t == m0:
        return 1
    if t < m0 or is_squarefree(t):
        return 0
    return sum(H_from(m, m0) for _, m in predecessors(t))


def binom_lower_bound(r):
    return comb(2 * r, r)
