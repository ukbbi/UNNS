"""Finite checks of the ANS-I v003 lemmas. Python 3.8+ with sympy; reads v001 and v002 modules.
Monte Carlo values are statistical and use the numerical sampler of v002."""
import json, math, os, random, sys, time
from bisect import bisect_left
from math import gcd, log

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v002"))
from sympy import factorint, primerange
from critical_checks import Sampler, SIG, nu

BETA = 1 / SIG
CHECKS = []


def check(theorem, text, ok, detail=None):
    CHECKS.append({"theorem": theorem, "check": text, "status": "PASS" if ok else "FAIL", "detail": detail})
    print("PASS" if ok else "FAIL", theorem, text, "" if detail is None else detail)


def preparation_word(target):
    """Lemma D: demand-driven word admissible from 1 whose endpoint is divisible by prod p^target[p].
    Returns [(prime q, number of copies of the letter q-1)] in execution order."""
    if not target:
        return []
    need = dict(target)
    blocks = []
    primes = list(primerange(2, max(target) + 1))
    for q in reversed(primes):
        t = need.get(q, 0)
        if not t:
            continue
        n = (t + 1) // 2
        blocks.append((q, n))
        for r, f in factorint(q - 1).items():
            need[r] = need.get(r, 0) + n * f
    return blocks[::-1]


def lemma_D():
    rng = random.Random(3)
    ok_adm = ok_div = ok_cost = True
    worst = 0.0
    for trial in range(300):
        M = rng.choice([10, 50, 200, 1000, 3000])
        primes = list(primerange(2, M + 1))
        target = {p: rng.randint(1, 6) for p in rng.sample(primes, rng.randint(1, len(primes)))}
        x = 1
        for q, n in preparation_word(target):
            for _ in range(n):
                ok_adm &= x % (q - 1) == 0
                x = x // (q - 1) * q * q
        T = 1
        for p, t in target.items():
            T *= p ** t
        ok_div &= x % T == 0
        bound = 2 * log(T) + 2 * sum(log(p) for p in primes)
        ok_cost &= log(x) <= bound + 1e-9
        worst = max(worst, log(x) / bound)
    check("T24a", "preparation words are admissible from 1 (300 random targets)", ok_adm)
    check("T24a", "their endpoint is divisible by the target", ok_div)
    check("T24a", "log Q(w) <= 2 log T + 2 theta(M)", ok_cost, round(worst, 4))


def source_formula():
    rng = random.Random(5)
    ok = True
    for _ in range(3000):
        w = [rng.randint(1, 60) for _ in range(rng.randint(1, 25))]
        E = K = 1
        for N in w:
            g = gcd(E, N)
            E, K = (N + 1) ** 2 * E // g, K * (N // g)
        for p in (2, 3, 5, 7, 11, 13):
            S = low = 0
            for N in w:
                n, m = N, N + 1
                while n % p == 0:
                    n //= p
                    S -= 1
                while m % p == 0:
                    m //= p
                    S += 2
                low = min(low, S)
            v, k = 0, K
            while k % p == 0:
                k //= p
                v += 1
            ok &= v == -low
    check("T23a", "v_p(K_k) = max_j (-S_p(j)) on random words", ok)


def mean_log_source(s):
    rng = random.Random(17)
    rows = []
    for k, samples in ((100, 600), (300, 400), (1000, 200), (3000, 80)):
        tot = 0.0
        for _ in range(samples):
            E = K = 1
            for _ in range(k):
                N = s.draw(rng)
                g = gcd(E, N)
                E, K = (N + 1) ** 2 * E // g, K * (N // g)
            tot += log(K)
        rows.append({"k": k, "samples": samples, "mean_log_K": tot / samples,
                     "over_k^beta": tot / samples / k ** BETA})
    print("observed  E log K_k / k^beta:", [round(r["over_k^beta"], 3) for r in rows])
    return rows


def prime_recursion():
    worst = 0.0
    for q in primerange(3, 10 ** 6):
        worst = max(worst, sum(factorint(q - 1)) / q)
    check("T28a", "sum of the distinct primes of q-1 is at most 5q/7 (q < 10^6)", worst <= 5 / 7 + 1e-12,
          round(worst, 6))


def supply_first(s, runs=60, k=2000):
    """Under the law conditioned to introduce no new prime through N: first-occurrence times T_q."""
    rng = random.Random(23)
    cache = {}

    def fac(n):
        if n not in cache:
            cache[n] = frozenset(factorint(n))
        return cache[n]
    marks = (2, 3, 5, 7, 11, 13, 17, 19, 23)
    tot = {q: 0.0 for q in marks}
    rejected = {100: 0, 500: 0, k: 0}
    primes_seen = {100: 0, 500: 0, k: 0}
    for _ in range(runs):
        seen, first, rej = set(), {}, 0
        for i in range(1, k + 1):
            while True:
                N = s.draw(rng)
                if N < 10 ** 18 and fac(N) <= seen:
                    break
                rej += 1
            for p in fac(N + 1):
                if p not in seen:
                    seen.add(p)
                    first[p] = i
            if i in rejected:
                rejected[i] += rej
                primes_seen[i] += len(seen)
        for q in marks:
            tot[q] += first.get(q, k)
    t_rows = [{"q": q, "mean_T_q": tot[q] / runs, "over_q^sigma": tot[q] / runs / q ** SIG} for q in marks]
    rows = [{"k": i, "mean_rejections": rejected[i] / runs, "scaled": rejected[i] / runs / (i ** BETA / log(i)),
             "mean_primes_seen": primes_seen[i] / runs} for i in rejected]
    print("observed  mean T_q / q^sigma:", [round(r["over_q^sigma"], 2) for r in t_rows])
    print("observed  mean rejections / (k^beta/log k):", [round(r["scaled"], 2) for r in rows])
    return {"runs": runs, "times": t_rows, "rejections": rows}


def main():
    t0 = time.time()
    s = Sampler()
    lemma_D()
    source_formula()
    out = {"mean_log_source": mean_log_source(s)}
    prime_recursion()
    out["supply_first"] = supply_first(s)
    out["checks"] = CHECKS
    out["passed"] = sum(c["status"] == "PASS" for c in CHECKS)
    out["failed"] = len(CHECKS) - out["passed"]
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "results", "v003_checks.json"), "w"), indent=1)
    print("%d passed, %d failed, %.1f s" % (out["passed"], out["failed"], time.time() - t0))
    sys.exit(1 if out["failed"] else 0)


if __name__ == "__main__":
    main()
