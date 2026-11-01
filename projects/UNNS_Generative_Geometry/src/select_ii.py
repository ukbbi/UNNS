"""Exact A2 SELECT-II edges, square-root transport and finite histories."""
from math import gcd
from .arithmetic import D, all_divisors, factor, square_root_part, valuations


def T(m, N):
    if m < 1 or N < 1 or m % N:
        raise ValueError("N must be a positive divisor of m")
    return (m // N) * (N + 1) ** 2


def transport(m, N):
    t = T(m, N)
    S, Sp = square_root_part(m), square_root_part(t)
    g = gcd(S, Sp)
    fm, fN = factor(m), factor(N)
    c = 1
    for p, n in fN.items():
        c *= p ** (n // 2 if fm[p] % 2 else (n + 1) // 2)
    assert S == g * c and Sp == g * (N + 1)
    ds0, ds1 = set(D(m)), set(D(t))
    return dict(N=N, m=m, t=t, S=S, Sp=Sp, g=g, c=c,
                lost=sorted(ds0 - ds1), shared=sorted(ds0 & ds1), gained=sorted(ds1 - ds0))


def edges(m):
    return [transport(m, N) for N in all_divisors(m)]


def history(start, labels):
    states = [start]
    for N in labels:
        states.append(T(states[-1], N))
    return states
