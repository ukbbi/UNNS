"""Targeted four-step test of word type (+-|+-) at scale B: exists N | Bn, q^2 | Bn(N+1)^2/N, M | B(n+1), r^2 | B(n+1)(M+1)^2/M with equal results
   Bn(N+1)^2(q-1)/(N q^2) = B(n+1)(M+1)^2(r-1)/(M r^2).   Exact (complete divisor enumeration); returns a witness (N,q,M,r) or None."""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import factor, _divisors
def zset(x):
    """dict z -> (N, q) over all words '+-' from x"""
    fx = factor(x); out = {}
    for N in _divisors(fx):
        x1 = x // N * (N + 1) ** 2; f1 = dict(fx)
        for p, e in factor(N).items():
            f1[p] = f1.get(p, 0) - e
            if f1[p] == 0: del f1[p]
        for p, e in factor(N + 1).items(): f1[p] = f1.get(p, 0) + 2 * e
        for q in _divisors(f1, cap=lambda e: e // 2):
            if q >= 2: out.setdefault(x1 // (q * q) * (q - 1), (N, q))
    return out
def pm_meet(B, n):
    a, b = zset(B * n), zset(B * (n + 1))
    for z, (N, q) in a.items():
        if z in b: return (N, q) + b[z] + (z,)
    return None
if __name__ == "__main__":
    for n in (11, 13, 3239, 5039): print(n, pm_meet(10**6, n))
