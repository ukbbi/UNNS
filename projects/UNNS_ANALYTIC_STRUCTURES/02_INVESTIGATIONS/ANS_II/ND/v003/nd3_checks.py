"""Checks for ANS-II-ND v003. Needs numpy and sympy.
Finite-alphabet checks of the identities and inequalities used in the proofs, and computed
observations. None of them proves an infinite-alphabet statement.
usage: nd3_checks.py [checks | families | large M]"""
import json, os, platform, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "v002"))
sys.path.insert(0, os.path.join(HERE, "..", "v002"))
from math import log

import numpy as np
from sympy import factorint, primerange

from nd2_checks import alpha, LISTS, optimum
from rate import Grammar

OUT = os.path.join(HERE, "results", "nd3_checks.json")
data = json.load(open(OUT)) if os.path.exists(OUT) else {"checks": {}, "observations": {}}


def check(name, ok, info=""):
    data["checks"][name] = {"pass": bool(ok), "info": info}
    print(("PASS " if ok else "FAIL ") + name + "  " + info, flush=True)


def tail_letter_bound():
    """Lower bound for the letter C p^v - 1 used in Theorem 12, in logarithms."""
    rng = np.random.default_rng(3)
    worst, n = float("inf"), 0
    for _ in range(400):
        a = float(rng.uniform(1.1, 3))
        p = int(rng.choice([2, 3, 5, 7]))
        S = [q for q in (2, 3, 5, 7, 11) if q != p and rng.random() < 0.5]
        C = int(np.prod(S)) if S else 1
        v = int(rng.integers(1, 20 if p < 5 else 10))
        N = C * p ** v - 1
        if N < 2:
            continue
        t = float(rng.uniform(0, 1))
        w = {q: float(rng.uniform(0, 1)) for q in S + [p]}
        fN = factorint(N)
        for q in fN:
            w[q] = float(rng.uniform(0, t))
        lt = a * (log(N) - 2 * log(N + 1))
        for q, e in factorint(N + 1).items():
            lt += 2 * a * w.get(q, 0.0) * e * log(q)
        for q, e in fN.items():
            lt -= a * w[q] * e * log(q)
        bound = -a * log(2) - a * (1 + t) * log(C * p ** v) + 2 * a * w[p] * v * log(p)
        worst = min(worst, lt - bound)
        n += 1
    check("letter lower bound behind Theorem 12", worst >= -1e-9, "%d letters, smallest slack %.2e" % (n, worst))


def entropy_identities():
    e1, e2, zok = 0.0, 0.0, True
    for name in LISTS:
        for M in (1000, 20000):
            G, a, th, term = optimum(name, M)
            L = term.sum()
            pi = term / L
            H = -float(pi @ np.log(pi))
            E = float(pi @ G.logmu)
            drift = sum(th.get(p, 0.0) * log(p) * float(pi[G.idx[p]] @ G.X[p]) for p in G.primes)
            e1 = max(e1, abs(H - (log(L) + a * E - a * drift)))
            n = np.arange(2, M + 2)
            for S, s, t in (([2], 1.2, 0.9), ([2, 3, 5], 1.05, 0.95)):
                f = np.zeros(len(pi))
                f[:M] = s * np.log(n)
                for p in S:
                    q, i = p, 0
                    while q <= M + 1:
                        f[:M][q - 2::q] -= t * log(p)
                        q *= p
                Z = float(np.exp(-f).sum())
                KL = float(pi @ np.log(pi / (np.exp(-f) / Z)))
                e2 = max(e2, abs(H - (float(pi @ f) + log(Z) - KL)))
                euler = 1.0
                for p in primerange(2, M + 2):
                    euler *= 1 / (1 - p ** (-(s - t) if p in S else -s))
                zok &= Z - (len(pi) - M) <= euler and f.min() >= -1e-12
    check("finite-alphabet entropy identity (Theorem 13)", e1 < 1e-9, "max error %.1e" % e1)
    check("reference-measure identity and Euler bound (Theorem 14)", e2 < 1e-9 and zok, "max error %.1e" % e2)


def average_inequality():
    worst, n, uni = float("inf"), 0, 0.0
    for name in LISTS:
        M = 100000
        G, a, th, term = optimum(name, M)
        L = float(term.sum())
        for ap in (1 + 0.05 * (a - 1), 1 + 0.3 * (a - 1), 1 + 0.8 * (a - 1), a):
            s = 1 - ap / a
            base = np.exp(-ap * G.logmu)
            B = float(base.sum())
            E = float(base @ G.logmu) / B
            uni = max(uni, abs(G.terms(a, {p: s for p in G.primes}).sum() / B - 1))
            lhs = sum(t * log(p) * float(base[G.idx[p]] @ G.X[p]) / B for p, t in th.items())
            rhs = s * E - 1 / a + L / (a * B)
            worst = min(worst, rhs - lhs)
            n += 1
    check("uniform weighting identity Phi(s) = B(a') (Theorem 15)", uni < 1e-8, "max relative error %.1e" % uni)
    check("finite-alphabet form of Theorem 15(i)", worst >= -1e-6, "%d cases, smallest slack %.2e" % (n, worst))


def drift_asymptotic():
    """The nesting sum behind mu_p against the same two truncated power sums used in the proof."""
    M = 1000000
    G = Grammar([], M)
    n = np.arange(1, M + 2, dtype=float)
    rows, ok = [], True
    for ap in (1.1, 1.5, 2.0, 3.0):
        base = np.exp(-ap * G.logmu)
        power = n ** (-ap)
        for p in (11, 101, 1009):
            value = float(base[G.idx[p]] @ G.X[p])
            v_sum_M, v_sum_M1, q = 0.0, 0.0, p
            while q <= M + 1:
                v_sum_M += power[:M][q - 1::q].sum()
                v_sum_M1 += power[q - 1::q].sum()
                q *= p
            main = float(2 * v_sum_M1 - v_sum_M)
            scaled = abs(value - main) * p ** (ap + 1)
            rows.append({"a'": ap, "p": p, "sum": value, "main": main, "scaled_error": float(scaled)})
            ok &= scaled <= 20
    data["observations"]["drift_asymptotic"] = rows
    check("error term of the drift sum in Theorem 15(ii)", ok,
          "max error times p^(a'+1): %.2f" % max(r["scaled_error"] for r in rows))


def one(K, a, M, th=None, sweeps=250):
    G = Grammar([alpha(2 * m + 1, 2 * m) for m in range(1, K + 1)], M)
    th, term = G.minimise(a, th or {}, sweeps=sweeps, tol=1e-12)
    L = float(term.sum())
    pi = term / L
    g = G.gradient(a, term)
    res = max(abs(g[p]) if th.get(p, 0) > 1e-9 else max(0.0, -g[p]) for p in G.primes) / L
    E = float(pi @ G.logmu)
    tail = float((pi * G.logmu)[G.logmu > log(M) / 2].sum())
    row = {"K": K, "a": a, "M": M, "weight_at_2": th.get(2, 0.0), "E_M": E,
           "moment_above_half_log_M": tail, "kkt_residual": float(res), "sweeps": sweeps}
    data["observations"].setdefault("families", {})["K=%d a=%g M=%d" % (K, a, M)] = row
    print("   K=%d a=%g M=%d weight %.4f E %.4f tail %.4f residual %.1e" % (K, a, M, row["weight_at_2"], E, tail, res), flush=True)
    return th


if __name__ == "__main__":
    t0 = time.time()
    part = sys.argv[1] if len(sys.argv) > 1 else "checks"
    if part == "checks":
        tail_letter_bound()
        entropy_identities()
        average_inequality()
        drift_asymptotic()
    elif part == "families":
        for a in (1.2, 2.0, 3.0):
            for K in (50, 800, 3200):
                th = None
                for M in (1000, 10000, 100000):
                    th = one(K, a, M, th)
    elif part == "large":
        M = int(sys.argv[2])
        th = one(800, 2.0, 100000, sweeps=250)
        one(800, 2.0, M, th, sweeps=120)
    data["software"] = {"python": platform.python_version(), "numpy": np.__version__}
    json.dump(data, open(OUT, "w"), indent=1)
    print("%d/%d checks passed (%.0f s)" % (sum(r["pass"] for r in data["checks"].values()), len(data["checks"]), time.time() - t0))
