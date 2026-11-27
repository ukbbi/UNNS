"""Checks for ANS-II-ND v001. Python 3.8+ with numpy, sympy, gmpy2; reads ../../v002."""
import json, os, platform, sys, time
from math import exp, floor, log
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "v002"))
import numpy as np
from sympy import factorint, isprime, primerange

import certify
from rate import Grammar

CHECKS, OUT = [], {}


def check(theorem, text, ok, detail=None):
    CHECKS.append({"theorem": theorem, "check": text, "status": "PASS" if ok else "FAIL", "detail": detail})
    print("PASS" if ok else "FAIL", theorem, text, "" if detail is None else detail, flush=True)


# multipliers > 1 with a negative exponent somewhere
EXTS = {"2/sqrt3": [(2 / 3 ** 0.5, {2: 1, 3: -0.5})],
        "4/3": [(4 / 3, {2: 2, 3: -1})],
        "11/9": [(11 / 9, {11: 1, 3: -2})],
        "8/7, 9/8": [(8 / 7, {2: 3, 7: -1}), (9 / 8, {3: 2, 2: -3})]}


def root(G, cap):
    lo, hi, th = 1.2, 6.0, {}
    for _ in range(34):
        mid = (lo + hi) / 2
        th, term = G.minimise(mid, th, cap=cap, sweeps=400, tol=1e-13)
        lo, hi = (mid, hi) if term.sum() > 1 else (lo, mid)
    th, term = G.minimise(lo, th, cap=cap, sweeps=2000, tol=1e-15)
    return lo, th, term


def neutral_laws():
    """Orthant minimiser against cube minimiser, drifts of the Gibbs law, entropy identity."""
    rows, ok_same, ok_neutral, ok_entropy, ok_bound = [], True, True, True, True
    for name, alphas in EXTS.items():
        for M in (12, 60, 400):
            G = Grammar(alphas, M)
            a, th, term = root(G, cap=1e9)
            a1, th1, _ = root(G, cap=1.0)
            phi = float(term.sum())
            pi = term / phi
            drift = {p: float(pi[G.idx[p]] @ G.X[p]) for p in G.primes}
            H = float(-(pi * np.log(pi)).sum())
            cost = float(pi @ G.logmu)
            worst = min(drift.values())
            weighted = max((abs(drift[p]) for p, t in th.items() if t > 1e-6), default=0.0)
            ok_same &= abs(a - a1) < 1e-7
            ok_neutral &= worst > -1e-6 and weighted < 1e-6
            ok_entropy &= abs((H - a * cost + a * sum(th.get(p, 0) * drift[p] * log(p) for p in G.primes)) - log(phi)) < 1e-9 \
                and abs(H / cost - a) < 1e-5
            ok_bound &= max(th.values(), default=0) < 1
            rows.append({"extension": name, "M": M, "root_orthant": a, "root_cube": a1, "largest_theta": max(th.values(), default=0),
                         "smallest_drift": worst, "largest_drift_at_weighted_prime": weighted, "H_over_cost": H / cost})
            print("   ", name, M, round(a, 6), round(a1, 6), round(rows[-1]["largest_theta"], 4), "%.1e %.1e" % (worst, weighted))
    check("ND-T02", "finite alphabets: orthant and cube minimisers give the same root", ok_same)
    check("ND-T02", "optimal finite law has no negative drift; zero drift at weighted primes", ok_neutral)
    check("ND-T01", "H(pi) - a E log mu = log Phi and H / E log mu = root", ok_entropy)
    check("ND-T02", "all optimal weights below 1", ok_bound)
    OUT["neutral_laws"] = rows


def preparation(T, M):
    """Nesting word from 1 whose multiplier is divisible by T (ANS-I v003 Lemma 2). T = {p: exponent}."""
    d = {q: T.get(q, 0) for q in primerange(2, M + 1)}
    blocks = []
    for q in sorted(d, reverse=True):
        n = (d[q] + 1) // 2
        blocks.append((q, n))
        for r, f in factorint(q - 1).items():
            d[r] += n * f
    return [q - 1 for q, n in reversed(blocks) for _ in range(n)]


def fixed_source():
    """Sample words from the optimal finite law for 2/sqrt3 and realise them from the state 1."""
    alphas, M = EXTS["2/sqrt3"], 30
    G = Grammar(alphas, M)
    a, th, term = root(G, cap=1e9)
    pi = term / term.sum()
    cost, H = float(pi @ G.logmu), float(-(pi * np.log(pi)).sum())
    free = G.terms(a, {})
    free /= free.sum()
    vec = [factorint_letter(i, M) for i in range(M + 1)]
    top = M + 1
    primes = [p for p in primerange(2, top + 1)]
    theta_M = sum(log(p) for p in primes)
    ok_adm = ok_size = True
    rows = []
    for law_name, law in (("optimal (resource-neutral)", pi), ("unweighted nu_a", free)):
        rng = np.random.default_rng(7)
        for k in (250, 1000, 4000, 16000):
            logK, total = [], []
            for rep in range(5):
                word = rng.choice(M + 1, size=k, p=law / law.sum())
                S, need = {}, {}
                for i in word:
                    for p, x in vec[i].items():
                        S[p] = S.get(p, 0) + x
                        need[p] = max(need.get(p, 0), -floor(S[p]))
                T = {p: v for p, v in need.items() if v > 0}
                lk = sum(v * log(p) for p, v in T.items())
                prep = preparation(T, top)
                state = {}
                for N in prep:
                    for p, x in factorint(N).items():
                        ok_adm &= state.get(p, 0) >= x
                    for p, x in vec[N - 1].items():
                        state[p] = state.get(p, 0) + x
                lq = sum(log((N + 1) ** 2 / N) for N in prep)
                ok_size &= lq <= 2 * lk + 2 * theta_M + 1e-6
                ok_adm &= all(state.get(p, 0) >= v for p, v in T.items())
                for i in word:
                    for p, x in vec[i].items():
                        state[p] = state.get(p, 0) + x
                        ok_adm &= state[p] >= 0
                logK.append(lk)
                total.append(lq + float(G.logmu[word].sum()))
            rows.append({"law": law_name, "k": k, "log_K_over_k": float(np.mean(logK)) / k,
                         "fixed_source_log_endpoint_over_k": float(np.mean(total)) / k, "E_log_mu": float(law @ G.logmu) / float(law.sum())})
            print("   ", law_name, k, round(rows[-1]["log_K_over_k"], 4), round(rows[-1]["fixed_source_log_endpoint_over_k"], 4),
                  round(rows[-1]["E_log_mu"], 4))
    check("ND-T04", "preparation word then sampled word is admissible from the state 1 (exact exponents)", ok_adm, "40 words, k <= 16000")
    check("ND-T04", "preparation size log Q <= 2 log K + 2 theta(M)", ok_size)
    best = [r["log_K_over_k"] for r in rows if r["law"].startswith("optimal")]
    other = [r["log_K_over_k"] for r in rows if r["law"].startswith("unweighted")]
    check("ND-T04", "log K / k falls under the neutral law and stays higher under the unweighted law",
          best[-1] < best[0] / 3 and other[-1] > 5 * best[-1], (round(best[-1], 4), round(other[-1], 4)))
    OUT["fixed_source"] = {"M": M, "a": a, "H": H, "E_log_mu": cost, "rows": rows}


def factorint_letter(i, M):
    if i == M:
        return {2: 1.0, 3: -0.5}
    N, out = i + 1, {}
    for m, f in ((N, -1), (N + 1, 2)):
        for p, e in factorint(m).items():
            out[p] = out.get(p, 0) + f * e
    return out


def support():
    """The inequality behind the infinite-support theorem, for the one-prime weight on 3."""
    a, t = 2.0607, 0.0918
    J = 10 ** 6
    v3 = np.zeros(J + 1)
    q = 3
    while q <= J:
        v3[q::q] += 1
        q *= 3
    j = np.arange(1, J + 1, dtype=float)
    partial = float(np.sum(2 * (1 + np.log2(j)) * j ** -a * 3 ** (2 * a * t * v3[1:])))
    tail = 10 * J ** (1 - a * (1 - 2 * t)) * (1 + log(J)) / (a * (1 - 2 * t) - 1) ** 2
    C = partial + tail
    rows, ok = [], True
    for n in (30, 40, 50):
        c = 1
        while not isprime(c * 3 ** n - 1):
            c += 1
        q = c * 3 ** n - 1
        lead = (q / (q + 1)) ** (2 * a) * 3 ** (2 * a * t * n)       # q^a times the weight of the letter q
        rows.append({"n": n, "c": c, "q": str(q), "q^a_w(q)": lead, "C_bound": C})
        ok &= lead > C
    check("ND-T05", "primes q = -1 mod 3^n exist whose letter q outweighs every supply of q", ok,
          (round(C, 1), [round(r["q^a_w(q)"]) for r in rows]))
    OUT["support"] = rows


def interval():
    res = certify.run(report=lambda s: print("   ", s, flush=True))
    check("ND-T06", "directed-rounding certificate: 2.06055 <= abscissa of 2/sqrt3 <= 2.06072",
          res["lower_ok"] and res["upper_ok"], (res["lower_minus_1"], res["upper_minus_1"]))
    OUT["certificate"] = res


def main():
    t0 = time.time()
    neutral_laws()
    fixed_source()
    support()
    interval()
    import sympy
    OUT["versions"] = {"python": platform.python_version(), "numpy": np.__version__, "sympy": sympy.__version__}
    OUT["checks"] = CHECKS
    OUT["passed"] = sum(c["status"] == "PASS" for c in CHECKS)
    OUT["failed"] = len(CHECKS) - OUT["passed"]
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    json.dump(OUT, open(os.path.join(HERE, "results", "nd_checks.json"), "w"), indent=1)
    print("%d passed, %d failed, %.1f s" % (OUT["passed"], OUT["failed"], time.time() - t0))
    sys.exit(1 if OUT["failed"] else 0)


if __name__ == "__main__":
    main()
