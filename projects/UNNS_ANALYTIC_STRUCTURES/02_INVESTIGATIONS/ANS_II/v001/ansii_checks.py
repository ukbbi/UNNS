"""Finite checks and computed constants for ANS-II v001. Python 3.8+ with sympy and mpmath."""
import json, os, random, sys, time
from fractions import Fraction as Fr
from math import floor, log

from mpmath import mp, mpf, zeta, binomial, findroot
from sympy import factorint

mp.dps = 30
HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS, OUT = [], {}


def check(theorem, text, ok, detail=None):
    CHECKS.append({"theorem": theorem, "check": text, "status": "PASS" if ok else "FAIL", "detail": detail})
    print("PASS" if ok else "FAIL", theorem, text, "" if detail is None else detail)


# multipliers are exponent dictionaries {prime: Fraction}; nesting letters are positive integers
def vec(d):
    return {p: Fr(e) for p, e in d.items() if e}


H = Fr(1, 2)
EXT = {
    "none": [],
    "sqrt2": [vec({2: H})],
    "sqrt3": [vec({3: H})],
    "cbrt2": [vec({2: Fr(1, 3)})],
    "fifth2": [vec({2: Fr(1, 5)})],
    "sqrt2,sqrt3": [vec({2: H}), vec({3: H})],
    "2": [vec({2: 1})],
    "2^(3/2)": [vec({2: Fr(3, 2)})],
    "2/sqrt3": [vec({2: 1, 3: -H})],
    "2/cbrt3": [vec({2: 1, 3: Fr(-1, 3)})],
    "3/sqrt2": [vec({3: 1, 2: -H})],
}


def value(v):
    r = mpf(1)
    for p, e in v.items():
        r *= mpf(p) ** (mpf(e.numerator) / e.denominator)
    return r


def B(a):
    return sum((-1) ** j * binomial(a, j) * (zeta(a + j) - 1) for j in range(110))


def sigma(mults):
    vals = [value(v) for v in mults]
    return findroot(lambda a: B(a) + sum(x ** (-a) for x in vals) - 1, (mpf("1.05"), mpf(8)), solver="anderson")


def exponents():
    rows, ok = [], True
    n0 = 200000
    for name, m in EXT.items():
        s = sigma(m)
        a = float(s)
        head = sum((n / (n + 1) ** 2) ** a for n in range(1, n0 + 1)) + sum(float(value(v)) ** (-a) for v in m)
        # (n/(n+1)^2)^a lies between (n+2)^-a and (n+1)^-a
        lo = head + (n0 + 3) ** (1 - a) / (a - 1)
        hi = head + (n0 + 1) ** (1 - a) / (a - 1)
        ok &= lo - 1e-9 <= 1 <= hi + 1e-9
        rows.append({"extension": name, "sigma_formula": mp.nstr(s, 12), "one_over_sigma": mp.nstr(1 / s, 10),
                     "direct_sum_bracket": [lo, hi]})
        print("  ", name, rows[-1]["sigma_formula"], rows[-1]["one_over_sigma"])
    check("ANS2-T02", "roots of the characteristic equation agree with a direct-sum bracket", ok)
    OUT["exponents"] = rows


def drifts():
    rows = []
    n0 = 200000
    for name, m in EXT.items():
        if not m:
            continue
        a = float(sigma(m))
        support = sorted({p for v in m for p in v})
        for p in support:
            s = 0.0
            for n in range(1, n0 + 1):
                x, t = 0, n + 1
                while t % p == 0:
                    t //= p
                    x += 2
                t = n
                while t % p == 0:
                    t //= p
                    x -= 1
                if x:
                    s += x * (n / (n + 1) ** 2) ** a
            s += sum(float(value(v)) ** (-a) * float(v.get(p, 0)) for v in m)
            # |X_p(n)| <= 2 log_p(n+1); the summand is decreasing for large n
            b = a - 1
            tail = 2 / log(p) * n0 ** (-b) * (log(n0 + 1) / b + 1 / b ** 2) * 1.001
            rows.append({"extension": name, "prime": p, "drift": s, "tail_bound": tail,
                         "sign": "+" if s > tail else "-" if s < -tail else "undetermined"})
    OUT["drift"] = rows
    table = {(r["extension"], r["prime"]): r for r in rows}
    check("ANS2-T02", "drift is positive at every support prime of the nonnegative-exponent extensions",
          all(r["sign"] == "+" for r in rows if all(e > 0 for v in EXT[r["extension"]] for e in v.values())))
    r = table[("2/sqrt3", 3)]
    check("ANS2-T05", "2/sqrt3 has negative drift at the prime 3", r["sign"] == "-", round(r["drift"], 5))
    for name in ("2/cbrt3", "3/sqrt2"):
        print("   drift", name, [(q["prime"], round(q["drift"], 5), q["sign"]) for q in rows if q["extension"] == name])


def run_word(word, mults, phi, n):
    """Exact admissibility from the state a_phi * n. word: ('N', N) or ('A', index). Returns final state or None."""
    state = dict(phi)
    for p, e in factorint(n).items():
        state[p] = state.get(p, 0) + e
    for kind, k in word:
        if kind == "N":
            step = {p: -e for p, e in factorint(k).items()}
            for p, e in factorint(k + 1).items():
                step[p] = step.get(p, 0) + 2 * e
        else:
            step = mults[k]
        for p, e in step.items():
            state[p] = state.get(p, 0) + e
            if state[p] < 0:          # integrality preservation: source and image lie in the cone
                return None
    return state


def formula_K(word, mults, phi):
    S, need = {}, {}
    for kind, k in word:
        if kind == "N":
            step = {p: -e for p, e in factorint(k).items()}
            for p, e in factorint(k + 1).items():
                step[p] = step.get(p, 0) + 2 * e
        else:
            step = mults[k]
        for p, e in step.items():
            S[p] = S.get(p, 0) + e
            need[p] = max(need.get(p, 0), -floor(phi.get(p, 0) + S[p]))
    K = 1
    for p, v in need.items():
        K *= p ** v
    return K


def layers(mults):
    seen, todo = {()}, [{}]
    while todo:
        phi = todo.pop()
        for m in mults:
            new = dict(phi)
            for p, e in m.items():
                new[p] = (new.get(p, 0) + e) % 1
            key = tuple(sorted((p, e) for p, e in new.items() if e))
            if key not in seen:
                seen.add(key)
                todo.append(dict(key))
    return [dict(k) for k in sorted(seen)]


def rand_word(rng, mults, length, top):
    return [("A", rng.randrange(len(mults))) if mults and rng.random() < 0.3 else ("N", rng.randint(1, top))
            for _ in range(length)]




def admissibility():
    rng = random.Random(7)
    least = multiples = True
    count = 0
    for name, m in EXT.items():
        for phi in layers(m):
            for _ in range(120):
                w = rand_word(rng, m, rng.randint(1, 5), 7)
                K = formula_K(w, m, phi)
                if K > 3000:
                    continue
                good = [n for n in range(1, 2 * K + 40) if run_word(w, m, phi, n) is not None]
                least &= bool(good) and good[0] == K
                multiples &= all(n % K == 0 for n in good)
                count += 1
    check("ANS2-L1", "least source equals the valuation formula (step-by-step search)", least, count)
    check("ANS2-L1", "admissible integer parts are multiples of the least source", multiples)


def comparison_and_first_letter():
    rng = random.Random(11)
    cmp_ok = first_ok = True
    for name, m in EXT.items():
        if not m:
            continue
        R = 1
        for p in {p for v in m for p in v}:
            R *= p
        ls = layers(m)
        for _ in range(400):
            w = rand_word(rng, m, rng.randint(1, 30), 60)
            K0 = formula_K(w, m, {})
            for phi in ls:
                K = formula_K(w, m, phi)
                cmp_ok &= K0 % K == 0 and (R * K) % K0 == 0
                j = rng.randrange(len(m))
                psi, c = {}, Fr(1)
                for p in set(phi) | set(m[j]):
                    t = phi.get(p, 0) + m[j].get(p, 0)
                    psi[p] = t % 1
                    c *= Fr(p) ** floor(t)
                if c.denominator != 1:
                    continue           # identity stated for integer carries
                c = c.numerator
                K1 = formula_K([("A", j)] + w, m, phi)
                Kp = formula_K(w, m, psi)
                from math import gcd
                first_ok &= K1 == Kp // gcd(Kp, c)
    check("ANS2-L2", "K_phi divides K_0 and K_0 divides R*K_phi in every class", cmp_ok)
    check("ANS2-T06", "first-letter identity K_phi(alpha w) = K_psi(w) / gcd(K_psi(w), c) for integer carries", first_ok)


def words_below(mults, phi, X):
    """All words with least endpoint <= X, as (word, endpoint). Appending a letter multiplies E by at least min multiplier."""
    a_phi = value(phi) if phi else mpf(1)
    out = []

    def rec(w, Q):
        K = formula_K(w, mults, phi)
        E = a_phi * K * Q
        if E > X * (1 + mpf(10) ** -20):
            return
        out.append((tuple(w), E))
        for i, m in enumerate(mults):
            rec(w + [("A", i)], Q * value(m))
        N = 1
        while E * mpf((N + 1) ** 2) / N <= X * (1 + mpf(10) ** -20):
            rec(w + [("N", N)], Q * mpf((N + 1) ** 2) / N)
            N += 1
    rec([], mpf(1))
    return out


def factorization_and_scaling():
    X = 400
    for name in ("sqrt2", "2/sqrt3"):
        m = EXT[name]
        ok = True
        for phi in layers(m):
            a_phi = value(phi) if phi else mpf(1)
            ws = words_below(m, phi, mpf(X))
            lhs = sum(int(X * (1 + mpf(10) ** -20) / E) for _, E in ws)      # sum over words of floor(X/E)
            rhs = 0
            for n in range(1, int(X / a_phi) + 1):                          # direct search from every source
                stack = [[]]
                while stack:
                    w = stack.pop()
                    st = run_word(w, m, phi, n)
                    if st is None or value(st) > X * (1 + mpf(10) ** -20):
                        continue
                    rhs += 1
                    cur = value(st)
                    stack += [w + [("A", i)] for i, v in enumerate(m) if cur * value(v) <= X * 1.0000001]
                    N = 1
                    while cur * (N + 1) ** 2 / N <= X * 1.0000001:
                        stack.append(w + [("N", N)])
                        N += 1
            ok &= lhs == rhs
            print("  ", name, "class", {p: str(e) for p, e in phi.items()}, "histories", lhs, rhs)
        check("ANS2-T01", "source-by-source count equals the zeta-factorized count, " + name + ", X = 400", ok)
    # classwise scaling, nesting letters only
    rng = random.Random(2)
    ok = True
    for _ in range(3000):
        w = rand_word(rng, [], rng.randint(1, 6), 6)
        n = rng.randint(1, 2000)
        base = run_word(w, [], {}, n)
        for phi in ({2: H}, {3: Fr(2, 3), 5: Fr(1, 5)}):
            other = run_word(w, [], phi, n)
            ok &= (base is None) == (other is None)
            if base is not None:
                ok &= other == {p: base.get(p, 0) + phi.get(p, 0) for p in set(base) | set(phi)}
    check("ANS2-T00", "nesting histories on a_phi*N are exact scaled copies of integer histories", ok)


def contractive_bound():
    """Upper bound for the abscissa for 2/sqrt3: a with Phi(a, theta) < 1 for some theta in [0, 1/4]."""
    p, m = 3, EXT["2/sqrt3"]
    n0 = 100000
    X = []
    for n in range(1, n0 + 1):
        x, t = 0, n + 1
        while t % p == 0:
            t //= p
            x += 2
        t = n
        while t % p == 0:
            t //= p
            x -= 1
        X.append(x)
    base = [log((n + 1) ** 2 / n) for n in range(1, n0 + 1)]
    al = float(value(m[0]))

    def Phi(a, th):
        from math import exp
        s = sum(exp(-a * (r - th * x * log(p))) for r, x in zip(base, X))
        s += al ** (-a) * p ** (th * a * float(m[0][p]))
        c = a * (1 - 2 * th)          # summand <= (n+1)^(2 theta a) n^-a
        tail = (1 + 1 / n0) ** (2 * th * a) * n0 ** (1 - c) / (c - 1)
        return s + tail
    sA = float(sigma(m))
    best = None
    for th in (0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16):
        lo, hi = 1.6, sA
        if Phi(hi, th) >= 1:
            continue
        for _ in range(22):
            mid = (lo + hi) / 2
            if Phi(mid, th) < 1:
                hi = mid
            else:
                lo = mid
        if best is None or hi < best[0]:
            best = (hi, th)
    OUT["contractive"] = {"extension": "2/sqrt3", "formula_root": sA, "computed_upper_bound": best[0], "theta": best[1],
                          "lower_bound_nesting_only": float(sigma([]))}
    check("ANS2-T05", "computed upper bound for the abscissa lies strictly below the formula root", best[0] < sA - 1e-3,
          (round(best[0], 5), best[1], round(sA, 5)))


def main():
    t0 = time.time()
    exponents()
    drifts()
    admissibility()
    comparison_and_first_letter()
    factorization_and_scaling()
    contractive_bound()
    OUT["checks"] = CHECKS
    OUT["passed"] = sum(c["status"] == "PASS" for c in CHECKS)
    OUT["failed"] = len(CHECKS) - OUT["passed"]
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    json.dump(OUT, open(os.path.join(HERE, "results", "ansii_checks.json"), "w"), indent=1)
    print("%d passed, %d failed, %.1f s" % (OUT["passed"], OUT["failed"], time.time() - t0))
    sys.exit(1 if OUT["failed"] else 0)


if __name__ == "__main__":
    main()
