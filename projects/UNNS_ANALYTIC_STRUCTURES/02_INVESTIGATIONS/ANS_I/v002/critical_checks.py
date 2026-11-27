"""Finite checks of the ANS-I v002 lemmas at and near the critical boundary.
Needs Python 3.8+ (standard library) and sympy for factorization; reads v001 modules (not modified).
Monte Carlo values are statistical estimates, not bounds."""
import json, math, os, random, sys, time
from bisect import bisect_left
from math import gcd, log
from sympy import factorint, primerange

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.join(HERE, "..", "v001")
sys.path.insert(0, V1)
from dirichlet import zeta, G2_representation

SIG = 1.5463810457225
RES = os.path.join(HERE, "results")
CHECKS = []


def check(theorem, text, ok, detail=None):
    CHECKS.append({"theorem": theorem, "check": text, "status": "PASS" if ok else "FAIL", "detail": detail})
    print("PASS" if ok else "FAIL", theorem, text, "" if detail is None else detail)


def nu(n, a=SIG):
    return (n / (n + 1) ** 2) ** a


def val(n, p):
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


class Sampler:
    """Numerical sampler of P(N) = nu_c(N): floating-point table up to N0 with an approximate tail mass,
    Pareto rejection beyond, and a fallback when the proposal density is below floating resolution."""

    def __init__(self, N0=10 ** 6):
        self.N0, self.cum, t = N0, [], 0.0
        for n in range(1, N0 + 1):
            t += nu(n)
            self.cum.append(t)
        # tail mass by Euler-Maclaurin on nu(x) ~ (x+2)^-s (relative error O(N0^-2))
        self.tail = (N0 + 2.5) ** (1 - SIG) / (SIG - 1)
        self.total = t + self.tail

    def draw(self, rng):
        u = rng.random() * self.total
        if u < self.cum[-1]:
            return bisect_left(self.cum, u) + 1
        N0 = self.N0
        c = (1 + 1.0 / N0) ** SIG
        while True:
            x = (N0 + 1) * rng.random() ** (-1.0 / (SIG - 1))
            n = int(x)
            q = (n ** (1 - SIG) - (n + 1) ** (1 - SIG)) / (SIG - 1)
            if q <= 0:                       # beyond floating resolution
                return n
            if rng.random() * c * q <= nu(n):
                return n


def ratios_and_injections():
    worst = max((n + 2) ** 2 * n / (n + 1) ** 3 for n in range(1, 10 ** 5))
    check("T17", "r_{N+1}/r_N <= 2 for N < 10^5", worst <= 2, round(worst, 6))
    M = 200000
    w = [0.0] + [nu(n) for n in range(1, M + 1)]
    bad = []
    for p in primerange(2, 500):
        d = sum(w[p::p])
        u = sum(w[p - 1::p])
        if not (d <= u <= 2 ** SIG * d):
            bad.append(p)
    check("T17", "nu(D_p) <= nu(U_p) <= 2^s nu(D_p), primes < 500, labels <= 200000", not bad, bad[:5])


def exponential_moment():
    rows, ok_ratio, ok_mgf = [], True, True
    for a in (1.05, SIG, 3.0):
        C = 2 ** a * sum(j * j * (math.exp(0.1 * j) / 2 + 2) * 2 ** (1 - j) for j in range(1, 400))
        eta = min(0.1, 1 / C)
        for M in (10, 100, 5000, 100000):
            w = [0.0] + [nu(n, a) for n in range(1, M + 1)]
            B = sum(w)
            worst = 0.0
            for p in primerange(2, min(M, 300) + 1):
                pi = []
                q = p
                while q - 1 <= M:
                    pi.append(sum(w[q - 1::q]) / B)
                    q *= p
                for j, x in enumerate(pi, 1):
                    ok_ratio &= x <= 2 ** a * 2 ** (1 - j) * pi[0] * (1 + 1e-12)
                mgf = 1.0
                q, j = p, 1
                while q <= M + 1:
                    if q <= M:
                        mgf += sum(w[q::q]) / B * (math.exp(eta * j) - math.exp(eta * (j - 1)))
                    mgf += sum(w[q - 1::q]) / B * (math.exp(-2 * eta * j) - math.exp(-2 * eta * (j - 1)))
                    q *= p
                    j += 1
                worst = max(worst, mgf - 1)
            ok_mgf &= worst <= 1e-13
            rows.append({"a": a, "M": M, "eta": eta, "max_E_exp_minus_1": worst})
    check("T23-lower", "pi_j <= 2^a 2^(1-j) pi_1 (primes <= 300)", ok_ratio)
    check("T23-lower", "E_M exp(-eta X_p) <= 1 with the explicit eta", ok_mgf)
    return rows


def prime_word_lengths(P=10 ** 6):
    L, worst = {}, 0.0
    spf = list(range(P))
    for i in range(2, int(P ** .5) + 1):
        if spf[i] == i:
            for j in range(i * i, P, i):
                if spf[j] == j:
                    spf[j] = i
    for p in range(2, P):
        if spf[p] != p:
            continue
        if p == 2:
            L[p] = log(4)
        else:
            n, t = p - 1, log(p * p / (p - 1))
            while n > 1:
                q = spf[n]
                t += L[q]
                n //= q
            L[p] = t
        worst = max(worst, L[p] / log(p) ** 2)
    check("T23-lower", "log Q(w_p) <= 3 log^2 p for p < 10^6", worst <= 3, round(worst, 4))
    from generative_record import prime_word
    memo, ok = {}, True
    for p in primerange(2, 3000):
        x = 1
        for N in prime_word(p, memo):
            ok &= x % N == 0
            x = x * (N + 1) ** 2 // N
        ok &= x % p == 0 and abs(math.log(x) - L[p]) < 1e-6 * max(1, L[p])
    check("T23-lower", "words w_p are admissible from 1, reach p, and have the stated size (p < 3000)", ok)


def pathwise(sampler, words=3000, k=30):
    rng = random.Random(20261126)
    c0 = 1 / (1 + 2 ** SIG)
    fresh = success = 0
    div_ok = grow_ok = mono_ok = True
    done = 0
    while done < words:
        w = [sampler.draw(rng) for _ in range(k)]
        if max(w) > 10 ** 18:
            continue
        done += 1
        seen, E, K, prod = set(), 1, 1, 1
        for N in w:
            d, u = set(factorint(N)), set(factorint(N + 1))
            new_d, new_u = d - seen, u - seen
            g = gcd(E, N)
            E2, K2 = (N + 1) ** 2 * E // g, K * N // g
            if new_d or new_u:
                fresh += 1
                if new_d:
                    success += 1
                    for p in new_d:
                        div_ok &= E % p != 0
                    prod *= min(new_d)
            seen |= d | u
            mono_ok &= K2 % K == 0
            grow_ok &= E2 >= 4 * E
            E, K = E2, K2
            div_ok &= K % prod == 0
    check("T18", "K_k divides K_{k+1} on sampled words", mono_ok)
    check("T20", "E_{k+1} >= 4 E_k on sampled words", grow_ok)
    check("T23-upper", "a newly met prime dividing a label is absent from E and divides every later K", div_ok)
    check("T23-upper", "observed success frequency among fresh letters >= 1/(1+2^s)", success / fresh >= c0,
          {"fresh": fresh, "success": success, "frequency": round(success / fresh, 4), "bound": round(c0, 4)})
    return {"words": words, "length": k, "fresh": fresh, "success": success}


def monte_carlo(sampler, samples=200000, kmax=60):
    rng = random.Random(7)
    sums, sq, ones = [0.0] * (kmax + 1), [0.0] * (kmax + 1), [0] * (kmax + 1)
    for _ in range(samples):
        E = K = 1
        for k in range(1, kmax + 1):
            N = sampler.draw(rng)
            g = gcd(E, N)
            E, K = (N + 1) ** 2 * E // g, K * (N // g)
            x = math.exp(-SIG * log(K))
            sums[k] += x
            sq[k] += x * x
            ones[k] += K == 1
            if x < 1e-12:              # K only grows: the rest of this word contributes < 1e-12 per depth
                break
    rows = []
    for k in range(1, kmax + 1):
        m = sums[k] / samples
        se = math.sqrt(max(sq[k] / samples - m * m, 0) / samples)
        rows.append({"k": k, "G_k": m, "standard_error": se, "fraction_K_equal_1": ones[k] / samples})
    G1 = zeta(2 * SIG) - 1
    G2 = G2_representation(SIG, 20000)
    for k, exact in ((1, G1), (2, G2)):
        r = rows[k - 1]
        check("T16", "Monte Carlo G_%d agrees with the exact value within 4 standard errors" % k,
              abs(r["G_k"] - exact) < 4 * r["standard_error"] + 2e-4,
              {"estimate": round(r["G_k"], 5), "exact": round(exact, 5), "se": round(r["standard_error"], 5)})
    return {"samples": samples, "G1_exact": G1, "G2_representation": G2, "rows": rows}


def census_ratios():
    rows = []
    for s in "ABCDE":
        c = json.load(open(os.path.join(V1, "results", "census_stage_%s.json" % s)))
        X = c["X"]
        rows.append({"X": X, "A_over_Xs": c["A"] / X ** SIG, "C_over_Xs": c["C"] / X ** SIG,
                     "scaled_log_deficit_A": -log(c["A"] / X ** SIG) / log(X) ** (1 / SIG)})
    check("T21", "A(X)/X^s decreases along the census", all(
        rows[i + 1]["A_over_Xs"] < rows[i]["A_over_Xs"] for i in range(len(rows) - 1)))
    return rows


def finite_alphabet(M=6, samples=20000, length=600):
    lo, hi = 0.0, 3.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if sum(nu(n, mid) for n in range(1, M + 1)) > 1 else (lo, mid)
    a = lo
    cum, t = [], 0.0
    for n in range(1, M + 1):
        t += nu(n, a)
        cum.append(t)
    rng = random.Random(11)
    marks = [25, 50, 100, 200, 400, 600]
    tot = {m: 0.0 for m in marks}
    last_change = []
    for _ in range(samples):
        E = K = 1
        lc = 0
        for k in range(1, length + 1):
            N = bisect_left(cum, rng.random() * t) + 1
            g = gcd(E, N)
            E = (N + 1) ** 2 * E // g
            if N != g:
                K *= N // g
                lc = k
            if k in tot:
                tot[k] += math.exp(-a * log(K))
        last_change.append(lc)
    rows = [{"k": m, "G_k": tot[m] / samples} for m in marks]
    frac = sum(x <= length // 2 for x in last_change) / samples
    check("T26", "labels <= 6: minimal source has stopped changing by half length in > 99% of samples",
          frac > 0.99, round(frac, 4))
    return {"M": M, "sigma_M": a, "samples": samples, "rows": rows}


def main():
    t0 = time.time()
    os.makedirs(RES, exist_ok=True)
    s = Sampler()
    check("T16", "critical labels have total probability 1", abs(s.total - 1) < 1e-7, s.total)
    ratios_and_injections()
    out = {"sigma": SIG, "exponential_moment": exponential_moment()}
    prime_word_lengths()
    out["pathwise"] = pathwise(s)
    out["monte_carlo"] = monte_carlo(s)
    out["census_ratios"] = census_ratios()
    out["finite_alphabet"] = finite_alphabet()
    out["checks"] = CHECKS
    out["passed"] = sum(c["status"] == "PASS" for c in CHECKS)
    out["failed"] = len(CHECKS) - out["passed"]
    json.dump(out, open(os.path.join(RES, "critical_checks.json"), "w"), indent=1)
    print("%d passed, %d failed, %.1f s" % (out["passed"], out["failed"], time.time() - t0))
    sys.exit(1 if out["failed"] else 0)


if __name__ == "__main__":
    main()
