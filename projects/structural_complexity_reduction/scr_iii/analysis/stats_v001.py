from __future__ import annotations
import math, statistics
from typing import Iterable, Sequence


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float("nan")


def median(xs):
    xs = list(xs)
    return statistics.median(xs) if xs else float("nan")


def _ranks(values: Sequence[float]):
    indexed = sorted(enumerate(values), key=lambda x: x[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        r = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[indexed[k][0]] = r
        i = j
    return ranks


def spearman(x: Sequence[float], y: Sequence[float]):
    if len(x) != len(y) or len(x) < 2:
        return None
    rx = _ranks(list(map(float, x))); ry = _ranks(list(map(float, y)))
    mx = mean(rx); my = mean(ry)
    num = sum((a-mx)*(b-my) for a,b in zip(rx,ry))
    denx = sum((a-mx)**2 for a in rx); deny = sum((b-my)**2 for b in ry)
    if denx <= 0 or deny <= 0:
        return 0.0
    return num / math.sqrt(denx*deny)


def holm_adjust(pvalues):
    """Return Holm-adjusted p-values in original order."""
    m = len(pvalues)
    order = sorted(range(m), key=lambda i: pvalues[i])
    out = [1.0] * m
    running = 0.0
    for rank, idx in enumerate(order):
        adj = min(1.0, (m-rank) * float(pvalues[idx]))
        running = max(running, adj)
        out[idx] = running
    return out

# Pure-Python regularized incomplete beta and inverse for Clopper-Pearson.
def _betacf(a, b, x):
    MAXIT = 250
    EPS = 3e-14
    FPMIN = 1e-300
    qab = a + b; qap = a + 1.0; qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < FPMIN: d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN: d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN: c = FPMIN
        d = 1.0 / d; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN: d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN: c = FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < EPS:
            break
    return h


def betainc_reg(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    bt = math.exp(math.lgamma(a+b)-math.lgamma(a)-math.lgamma(b)+a*math.log(x)+b*math.log1p(-x))
    if x < (a+1.0)/(a+b+2.0):
        return bt * _betacf(a,b,x) / a
    return 1.0 - bt * _betacf(b,a,1.0-x) / b


def beta_ppf(p, a, b):
    if p <= 0: return 0.0
    if p >= 1: return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo+hi)/2
        if betainc_reg(a,b,mid) < p: lo = mid
        else: hi = mid
    return (lo+hi)/2


def clopper_pearson(k: int, n: int, alpha: float = 0.05):
    if n <= 0:
        return [None, None]
    k = int(k); n = int(n)
    lo = 0.0 if k == 0 else beta_ppf(alpha/2, k, n-k+1)
    hi = 1.0 if k == n else beta_ppf(1-alpha/2, k+1, n-k)
    return [lo, hi]
