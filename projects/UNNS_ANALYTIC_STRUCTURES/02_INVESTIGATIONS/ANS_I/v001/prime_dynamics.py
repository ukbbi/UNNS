"""Prime-coordinate dynamics (ANS-T04) and the saturation mechanism used in ANS-T09."""
from math import gcd, log
import random


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def val(n, p):
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def step(e, N):
    """e'_p = 2 v_p(N+1) + max(e_p - v_p(N), 0) on the exponent dictionary of E(w)."""
    d, u = factor(N), factor(N + 1)
    out = {}
    for p in set(e) | set(d) | set(u):
        x = 2 * u.get(p, 0) + max(e.get(p, 0) - d.get(p, 0), 0)
        if x:
            out[p] = x
    return out


def lindley(word, p):
    """max_{1<=j<=k} ( sum_{i=j..k} u_i - sum_{i=j+1..k} d_i ),  u=2v_p(N+1), d=v_p(N)."""
    if not word:
        return 0
    best, run = None, 0
    for j in range(len(word) - 1, -1, -1):
        N = word[j]
        cand = run + 2 * val(N + 1, p)
        best = cand if best is None else max(best, cand)
        run += 2 * val(N + 1, p) - val(N, p)
    return best


def least_source(word):
    """K(w) from the definition: lcm of the denominators required by every prefix."""
    K, num, den = 1, 1, 1
    for N in word:
        need = den * N // gcd(num, den * N)
        K = K * need // gcd(K, need)
        num, den = num * (N + 1) ** 2, den * N
        g = gcd(num, den)
        num, den = num // g, den // g
    return K, num, den


def words_upto(X):
    """All words with E(w) <= X, with E obtained from least_source (not from the recurrence)."""
    stack = [()]
    while stack:
        w = stack.pop()
        N = 1
        while (N + 1) ** 2 <= X:
            v = w + (N,)
            K, num, den = least_source(v)
            E = K * num // den
            if E <= X:
                stack.append(v)
                yield v, E
            Kw, a, b = least_source(w)
            if Kw * a // b * (N + 1) ** 2 > X * N:     # r_N E(w) > X
                break
            N += 1


def check_T03_T04(X):
    count = bad_rec = bad_vec = bad_lin = 0
    for v, E in words_upto(X):
        count += 1
        Kw, a, b = least_source(v[:-1])
        Ew, N = Kw * a // b, v[-1]
        bad_rec += E != (N + 1) ** 2 * Ew // gcd(Ew, N)
        e1 = step(factor(Ew), N)
        bad_vec += e1 != factor(E)
        primes = set()
        for M in v:
            primes |= set(factor(M)) | set(factor(M + 1))
        bad_lin += any(lindley(v, p) != factor(E).get(p, 0) for p in primes)
    return {"words": count, "recurrence_mismatch": bad_rec,
            "valuation_mismatch": bad_vec, "closed_form_mismatch": bad_lin}


def drift_table(M, sig):
    """Exact finite sums: mean increment E_nu[2 v_p(N+1) - v_p(N)] for nu(N) ~ r_N^-sig, N<=M."""
    w = [0.0] + [(N / (N + 1) ** 2) ** sig for N in range(1, M + 1)]
    B = sum(w)
    primes = [p for p in range(2, M + 1) if factor(p) == {p: 1}]
    return B, {p: sum(w[N] * (2 * val(N + 1, p) - val(N, p)) for N in range(1, M + 1)) / B
               for p in primes}


def saturation_experiment(M, sig, length, samples, seed=20261126):
    """Monte Carlo illustration: starting from a warm-up prefix, how often does a random
    continuation satisfy gcd(E,N)=N at EVERY step (so that E(w0 v)=E(w0)Q(v))?"""
    rng = random.Random(seed)
    labels = list(range(1, M + 1))
    weights = [(N / (N + 1) ** 2) ** sig for N in labels]
    out = []
    for warm in (0, 25, 100, 400):
        good = 0
        for _ in range(samples):
            e = {}
            for N in rng.choices(labels, weights, k=warm):
                e = step(e, N)
            ok = True
            for N in rng.choices(labels, weights, k=length):
                if any(e.get(p, 0) < c for p, c in factor(N).items()):
                    ok = False
                    break
                e = step(e, N)
            good += ok
        out.append({"warmup": warm, "good_fraction": good / samples})
    return out


def restricted_Gk(M, sig, kmax):
    """Exact G_k restricted to labels <= M (dynamic programming over distinct endpoints)."""
    level, out = {1: 1}, []
    for _ in range(kmax):
        nxt = {}
        for E, c in level.items():
            for N in range(1, M + 1):
                F = (N + 1) ** 2 * E // gcd(E, N)
                nxt[F] = nxt.get(F, 0) + c
        level = nxt
        out.append(sum(c * F ** (-sig) for F, c in level.items()))
    return out


if __name__ == "__main__":
    print(check_T03_T04(20000))
    print(drift_table(10, 1.0))
    print(restricted_Gk(6, 1.0, 6))
    print(saturation_experiment(6, 1.0, 100, 400))
