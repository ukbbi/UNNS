"""Two-sided computation of the abscissa from rho(a) = min over theta in [0,1]^primes of Phi(a, theta).

Lower bound: restrict nesting labels to N <= M (Phi only decreases) and certify min Phi_M >= 1 by convexity:
Phi_M(theta) >= Phi_M(t0) + grad . (theta - t0) over the whole box.
Upper bound: Phi(a, t1) + tail < 1 for one t1 with all components <= CAP.
Floating-point arithmetic."""
from math import log, sqrt

import numpy as np

CAP = 0.10


class Grammar:
    """alphas: list of (multiplier, {prime: exponent})."""

    def __init__(self, alphas, M):
        self.M = M
        spf = np.zeros(M + 2, dtype=np.int64)
        for p in range(2, M + 2):
            if spf[p] == 0:
                block = spf[p::p]
                block[block == 0] = p
                spf[p::p] = block
        spf = spf.tolist()
        table = {}

        def add(p, i, x):
            row = table.setdefault(p, {})
            row[i] = row.get(i, 0) + x
        for i, N in enumerate(range(1, M + 1)):
            for m, factor in ((N, -1), (N + 1, 2)):
                while m > 1:
                    p, e = spf[m], 0
                    while m % p == 0:
                        m //= p
                        e += 1
                    add(p, i, factor * e)
        base = [log((N + 1) ** 2 / N) for N in range(1, M + 1)]
        for j, (mult, w) in enumerate(alphas):
            base.append(log(mult))
            for p, e in w.items():
                add(p, M + j, e)
        self.logmu = np.array(base)
        self.primes = sorted(table)
        self.idx = {p: np.fromiter(table[p].keys(), dtype=np.int64) for p in self.primes}
        self.X = {p: np.array(list(table[p].values()), dtype=float) for p in self.primes}

    def terms(self, a, theta):
        e = -a * self.logmu
        for p, t in theta.items():
            if t:
                e[self.idx[p]] += a * t * log(p) * self.X[p]
        return np.exp(e)

    def gradient(self, a, term):
        return {p: a * log(p) * float(term[self.idx[p]] @ self.X[p]) for p in self.primes}

    def minimise(self, a, theta=None, cap=1.0, sweeps=40, tol=1e-9):
        theta = dict(theta or {})
        term = self.terms(a, theta)
        for _ in range(sweeps):
            moved = 0.0
            for p in self.primes:
                i, X, c = self.idx[p], self.X[p], a * log(p)
                t = theta.get(p, 0.0)
                tx = term[i]
                g = c * float(tx @ X)
                if (t <= 0 and g >= 0) or (t >= cap and g <= 0):
                    continue
                h = c * c * float(tx @ (X * X))
                new = min(cap, max(0.0, t - g / h))
                step = max(-0.05, min(0.05, new - t))
                if step:
                    term[i] = tx * np.exp(c * step * X)
                    theta[p] = t + step
                    moved = max(moved, abs(step * g))
            if moved < tol:
                break
        return theta, term

    def lower_certificate(self, a, theta, term):
        g = self.gradient(a, term)
        gap = sum(min(g[p] * (0 - theta.get(p, 0.0)), g[p] * (1 - theta.get(p, 0.0))) for p in self.primes)
        return float(term.sum()) + gap

    def upper_certificate(self, a, theta, term):
        th = max(theta.values(), default=0.0)
        c = a * (1 - 2 * th)
        tail = (1 + 1 / self.M) ** (2 * a * th) * self.M ** (1 - c) / (c - 1)
        return float(term.sum()) + tail


def bracket(G, lo, hi, steps=16):
    """Largest a with a certified lower bound >= 1 and smallest a with a certified upper bound < 1."""
    t_low, t_up, l, h = {}, {}, lo, hi
    for _ in range(steps):
        mid = (l + h) / 2
        t_low, term = G.minimise(mid, t_low)
        if G.lower_certificate(mid, t_low, term) >= 1:
            l = mid
        else:
            h = mid
    low = l
    l, h = lo, hi
    for _ in range(steps):
        mid = (l + h) / 2
        t_up, term = G.minimise(mid, t_up, cap=CAP)
        if G.upper_certificate(mid, t_up, term) < 1:
            h = mid
        else:
            l = mid
    return low, h


TWO_OVER_SQRT3 = [(2 / sqrt(3), {2: 1, 3: -0.5})]
