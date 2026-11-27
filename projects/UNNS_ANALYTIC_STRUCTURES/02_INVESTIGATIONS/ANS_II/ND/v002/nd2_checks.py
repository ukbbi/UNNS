"""Checks for ANS-II-ND v002. Needs numpy, sympy and gmpy2.
Floating-point checks of identities and finite-alphabet inequalities, a rerun of the hardened
certificate, and computed observations. None of them proves an infinite-alphabet statement."""
import json, os, platform, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "v002"))
sys.path.insert(0, HERE)
from math import log

import numpy as np
from sympy import factorint, isprime, primerange

import certify
from rate import Grammar, TWO_OVER_SQRT3

results, observations = {}, {}


def check(name, ok, info=""):
    results[name] = {"pass": bool(ok), "info": info}
    print(("PASS " if ok else "FAIL ") + name + "  " + info, flush=True)


def alpha(num, den):
    w = dict(factorint(num))
    for p, e in factorint(den).items():
        w[p] = w.get(p, 0) - e
    return (num / den, w)


LISTS = {"2/sqrt3": (TWO_OVER_SQRT3, 2.06064),
         "3^12/2^19": ([alpha(3 ** 12, 2 ** 19)], 2.0),
         "(2m+1)/(2m), m<=200": ([alpha(2 * m + 1, 2 * m) for m in range(1, 201)], 2.0)}


def optimum(name, M, sweeps=150):
    lst, a = LISTS[name]
    G = Grammar(lst, M)
    th, term = G.minimise(a, {}, sweeps=sweeps, tol=1e-13)
    return G, a, th, term


def kkt_residual(G, a, th, term):
    g = G.gradient(a, term)
    return max(abs(g[p]) if th.get(p, 0) > 1e-9 else max(0.0, -g[p]) for p in G.primes) / term.sum()


def weight_validation():
    certify.SPF = certify.sieve(1000)
    bad = [{2: float("nan")}, {3: -1e-9}, {3: 0.2}, {9: 0.01}, {1009: 0.01}, {5: float("inf")}]
    rejected = 0
    for th in bad:
        try:
            certify.check_weights(th, 0.10, 500)
        except (ValueError, IndexError):
            rejected += 1
    certify.check_weights({2: 0.0, 3: 0.1, 499: 0.05}, 0.10, 500)
    check("certificate rejects invalid trial weights", rejected == len(bad), "%d/%d rejected" % (rejected, len(bad)))


def certificate():
    r = certify.run(report=lambda s: print("   " + s, flush=True))
    old = json.load(open(os.path.join(HERE, "..", "v001", "results", "nd_checks.json")))

    def find(o):
        if isinstance(o, dict):
            if "lower_minus_1" in o:
                return o
            for v in o.values():
                f = find(v)
                if f:
                    return f
    o = find(old)
    same = o is not None and all(abs(o[k] - r[k]) <= 1e-9 * abs(r[k]) for k in ("lower_minus_1", "upper_minus_1"))
    check("hardened certificate certifies the interval", r["lower_ok"] and r["upper_ok"],
          "[%.5f, %.5f]" % tuple(r["interval"]))
    check("margins agree with the stored v001 run", same)
    observations["certificate"] = r


def euler_majorant():
    rng = np.random.default_rng(7)
    worst = 0.0
    M = 20000
    G = Grammar([], M)
    for a in (1.3, 2.0, 3.0):
        for _ in range(5):
            th = {p: float(rng.uniform(0, (a - 1) / (2 * a))) for p in G.primes}
            lhs = G.terms(a, th).sum()
            rhs = np.prod([1 / (1 - p ** (-a * (1 - 2 * th.get(p, 0.0)))) for p in primerange(2, M + 2)])
            worst = max(worst, lhs / rhs)
    check("Euler majorant on truncations (15 random weightings)", worst <= 1, "largest ratio %.3e" % worst)


def identity_and_moments():
    errs, table = [], {}
    for name in LISTS:
        rows = []
        for M in (1000, 10000, 100000):
            G, a, th, term = optimum(name, M)
            L = term.sum()
            pi = term / L
            E = float(pi @ G.logmu)
            H = -float(pi @ np.log(pi))
            ap = (1 + a) / 2
            base = np.exp(-ap * G.logmu)
            B = base.sum()
            KL = float(pi @ np.log(pi / (base / B)))
            errs.append(abs((H - a * E) - (log(B) - KL - (a - ap) * E)))
            top = sorted(th.items(), key=lambda x: -x[1])[:3]
            rows.append({"M": M, "a": a, "L_M": float(L), "E_log_mu": E,
                         "weight_at_2": th.get(2, 0.0), "top_weights": [[p, t] for p, t in top],
                         "kkt_residual": float(kkt_residual(G, a, th, term))})
        table[name] = rows
    check("entropy decomposition identity (Theorem 8)", max(errs) < 1e-9, "max error %.1e" % max(errs))
    check("finite optimality residuals", all(r["kkt_residual"] < 1e-5 for v in table.values() for r in v),
          "max %.1e" % max(r["kkt_residual"] for v in table.values() for r in v))
    observations["finite_optima"] = table


def variational_and_supply():
    rng = np.random.default_rng(11)
    low, total, bad = float("inf"), 0, 0
    for name in LISTS:
        M = 20000
        G, a, th, term = optimum(name, M)
        g = G.gradient(a, term)
        for _ in range(50):
            w = rng.uniform(0, 0.49, len(G.primes)) * (rng.random(len(G.primes)) < 0.3)
            s = sum(g[p] * (wp - th.get(p, 0.0)) for p, wp in zip(G.primes, w)) / term.sum()
            low = min(low, s)
        P0 = set()
        for _, wt in LISTS[name][0]:
            P0 |= set(wt)
        F = {}

        def F_of(n):
            r = F.get(n)
            if r is None:
                r = 1.0
                for p, e in factorint(n).items():
                    r *= p ** (2 * a * th.get(p, 0.0) * e)
                F[n] = r
            return r
        for q in primerange(2, M + 1):
            if q in P0:
                continue
            C = 0.0
            for j in range(1, (M + 1) // q + 1):
                v, m = 0, j
                while m % q == 0:
                    m //= q
                    v += 1
                C += 2 * (1 + v) * j ** (-a) * F_of(j)
            t = th.get(q, 0.0)
            lhs = q ** (-a * (1 - 2 * t)) * C
            rhs = 2 ** (-2 * a) * q ** (-a * (1 + t)) * F_of(q + 1)
            total += 1
            bad += lhs < rhs * (1 - 1e-6)
    check("finite-alphabet variational inequality (150 random w)", low > -1e-5, "smallest value %.1e" % low)
    check("supply >= demand bound of Theorem 11 on finite alphabets", bad == 0, "%d primes, %d violations" % (total, bad))


def forced_primes():
    G, a, th, term = optimum("2/sqrt3", 200000, 80)
    rows = []
    for n in range(2, 12):
        for k in range(1, 200):
            q = k * 3 ** n - 1
            if q < 150000 and isprime(q):
                rows.append({"n": n, "q": q, "weight": th.get(q, 0.0)})
                break
    G2, a2, th2, _ = optimum("3^12/2^19", 200000)
    mers = [{"q": q, "weight": th2.get(q, 0.0)} for q in (31, 127, 8191, 131071)]
    observations["forced_primes"] = {"2/sqrt3 least prime q = -1 mod 3^n": rows,
                                     "3^12/2^19 Mersenne primes": mers, "3^12/2^19 weight_at_2": th2.get(2, 0.0),
                                     "2/sqrt3 weight_at_3": th.get(3, 0.0)}
    G3, a3, th3, term3 = optimum("(2m+1)/(2m), m<=200", 200000)
    observations["finite_optima"]["(2m+1)/(2m), m<=200"].append(
        {"M": 200000, "a": a3, "weight_at_2": th3.get(2, 0.0), "kkt_residual": float(kkt_residual(G3, a3, th3, term3))})
    print("   weight at 2, 200-letter list, M=2e5: %.4f" % th3.get(2, 0.0))


if __name__ == "__main__":
    t0 = time.time()
    part = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = os.path.join(HERE, "results", "nd2_checks.json")
    if part in ("all", "certificate"):
        weight_validation()
        certificate()
    if part in ("all", "analysis"):
        euler_majorant()
        identity_and_moments()
        variational_and_supply()
        forced_primes()
    if part != "all" and os.path.exists(out):
        old = json.load(open(out))
        results = {**old.get("checks", {}), **results}
        observations = {**old.get("observations", {}), **observations}
    import gmpy2, sympy
    json.dump({"checks": results, "observations": observations,
               "software": {"python": platform.python_version(), "numpy": np.__version__, "sympy": sympy.__version__,
                            "gmpy2": gmpy2.version(), "mpfr": gmpy2.mpfr_version()}}, open(out, "w"), indent=1)
    print("%d/%d checks passed (%.0f s)" % (sum(r["pass"] for r in results.values()), len(results), time.time() - t0))
