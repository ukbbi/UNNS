"""numpy sieves for sums of tau(Bx) and s(Bx) over x <= X (exact integer arithmetic)."""
import numpy as np
from math import isqrt

def tau_sieve(X):
    t = np.zeros(X + 1, dtype=np.int64)
    for d in range(1, isqrt(X) + 1):
        t[d * d] += 1
        t[d * (d + 1)::d] += 2
    return t

def valuation(X, p):
    v = np.zeros(X + 1, dtype=np.int64)
    pk = p
    while pk <= X:
        v[pk::pk] += 1
        pk *= p
    return v

def tau_B_sum_exact(X, fB, tau):
    """sum_{x<=X} tau(Bx) = sum tau(x) * prod (a_p+b_p+1)/(a_p+1)  (the division is exact)."""
    num = np.ones(X + 1, dtype=np.int64); den = np.ones(X + 1, dtype=np.int64)
    for p, b in fB.items():
        a = valuation(X, p)
        num *= a + b + 1; den *= a + 1
    assert np.all((tau // den) * den == tau)
    return int(((tau // den) * num)[1:].sum())

def s_sum_exact(X, B):
    """sum_{x<=X} [s(Bx) - s(x)] = sum_{q>=1} ( floor(X g_q/q^2) - floor(X/q^2) ), g_q = gcd(q^2, B)."""
    Q = isqrt(X * B) + 1
    q = np.arange(1, Q + 1, dtype=np.int64)
    g = np.gcd(q * q, B)
    return int(((X * g) // (q * q) - X // (q * q)).sum())

def total_exits_exact(X, fB, B, tau=None):
    """sum_{x<=X} eps_B(x), infinite-graph exit counts of the lattice vertices Bx, x <= X."""
    tau = tau_sieve(X) if tau is None else tau[:X + 1]
    return tau_B_sum_exact(X, fB, tau) - int(tau[1:].sum()) + s_sum_exact(X, B)
