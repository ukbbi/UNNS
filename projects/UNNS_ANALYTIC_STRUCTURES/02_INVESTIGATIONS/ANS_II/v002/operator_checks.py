"""Finite checks for ANS-II v002. Python 3.8+ with numpy, sympy and mpmath; reads ../v001/ansii_checks.py."""
import json, os, platform, random, sys, time
from fractions import Fraction as Fr
from functools import lru_cache
from itertools import product
from math import floor, gcd, log

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v001"))
from sympy import divisors, factorint, mobius

from ansii_checks import EXT, formula_K, layers, rand_word, value
from rate import Grammar, TWO_OVER_SQRT3, bracket

CHECKS, OUT = [], {}


def check(theorem, text, ok, detail=None):
    CHECKS.append({"theorem": theorem, "check": text, "status": "PASS" if ok else "FAIL", "detail": detail})
    print("PASS" if ok else "FAIL", theorem, text, "" if detail is None else detail)


def class_step(mults, psi, j):
    """Image class and carry c = u/v of the letter alpha_j applied in class psi."""
    new, c = {}, Fr(1)
    for p in set(psi) | set(mults[j]):
        t = psi.get(p, 0) + mults[j].get(p, 0)
        if t % 1:
            new[p] = t % 1
        c *= Fr(p) ** floor(t)
    return new, c


def letter_data(mults, psi, letter):
    kind, k = letter
    if kind == "N":
        return psi, (k + 1) ** 2, k
    new, c = class_step(mults, psi, k)
    return new, c.numerator, c.denominator


def terminal(mults, phi, word):
    """(terminal class, integer part n of the minimal endpoint) from the source formula."""
    psi, carry = dict(phi), Fr(1)
    Q = Fr(1)
    for kind, k in word:
        if kind == "N":
            Q *= Fr((k + 1) ** 2, k)
        else:
            psi, c = class_step(mults, psi, k)
            Q *= c
    n = formula_K(word, mults, phi) * Q
    assert n.denominator == 1
    return psi, n.numerator


def pullback(u, v, d):
    D = 1
    fu, fv = factorint(u), factorint(v)
    for p, e in factorint(d).items():
        if e > fu.get(p, 0):
            D *= p ** (fv.get(p, 0) + e - fu.get(p, 0))
    return D


def one_step():
    rng = random.Random(4)
    ok_end = ok_pull = True
    count = 0
    for name, m in EXT.items():
        for phi in layers(m):
            for _ in range(250):
                w = rand_word(rng, m, rng.randint(0, 8), 30)
                psi, n = terminal(m, phi, w)
                letter = ("A", rng.randrange(len(m))) if m and rng.random() < 0.5 else ("N", rng.randint(1, 60))
                psi2, u, v = letter_data(m, psi, letter)
                predicted = u * n // gcd(n, v)
                got_psi, got = terminal(m, phi, w + [letter])
                ok_end &= got == predicted and got_psi == psi2 and gcd(u, v) == 1
                for d in (rng.randint(1, 400), rng.choice(divisors(got)), got * rng.choice((2, 3, 5))):
                    ok_pull &= (got % d == 0) == (n % pullback(u, v, d) == 0)
                    count += 1
    check("ANS2-T14", "appending any letter gives n' = u n / gcd(n, v)", ok_end)
    check("ANS2-T10", "d divides n' exactly when the pullback divides n", ok_pull, count)


def operator():
    """Operator recursion against direct enumeration, exact rationals at s = 2."""
    for name in ("none", "sqrt2", "2/sqrt3", "3/sqrt2"):
        m = EXT[name]
        letters = [("N", N) for N in range(1, 7)] + [("A", j) for j in range(len(m))]
        classes = layers(m)
        key = lambda psi: tuple(sorted(psi.items()))
        incoming = {}
        for psi in classes:
            for letter in letters:
                psi2, u, v = letter_data(m, psi, letter)
                mult = Fr((letter[1] + 1) ** 2, letter[1]) if letter[0] == "N" else None
                a2 = Fr(1)                       # alpha^-2 is rational for these extensions
                if letter[0] == "A":
                    for p, e in m[letter[1]].items():
                        assert (2 * e).denominator == 1
                        a2 *= Fr(p) ** int(-2 * e)
                weight = mult ** -2 if mult else a2
                incoming.setdefault(key(psi2), []).append((key(psi), u, v, weight / v ** 2))

        def a_inv2(phi):
            r = Fr(1)
            for p, e in phi.items():
                r *= Fr(p) ** int(-2 * e)
            return r

        def J2(h):
            return sum(mobius(e) * (h // e) ** 2 for e in divisors(h))
        ok = True
        for phi in classes:
            @lru_cache(maxsize=None)
            def F(k, psi, d, phik=key(phi)):
                if k == 0:
                    return a_inv2(phi) if (psi == phik and d == 1) else Fr(0)
                total = Fr(0)
                for psi0, u, v, w in incoming.get(psi, []):
                    D = pullback(u, v, d)
                    total += w * sum(J2(h) * F(k - 1, psi0, h * D // gcd(h, D)) for h in divisors(v))
                return total
            direct = {}
            for k in range(0, 4):
                for w in product(letters, repeat=k):
                    psi, n = terminal(m, phi, list(w))
                    E2 = a_inv2(psi) / n ** 2
                    for d in (1, 2, 3, 4, 6, 9, 18, 25):
                        if n % d == 0:
                            t = (k, key(psi), d)
                            direct[t] = direct.get(t, 0) + E2
                for psi in classes:
                    for d in (1, 2, 3, 4, 6, 9, 18, 25):
                        ok &= F(k, key(psi), d) == direct.get((k, key(psi), d), 0)
        check("ANS2-T13", "operator recursion equals enumeration (exact, depth <= 3, N <= 6), " + name, ok)


def weighted_norm():
    rng = random.Random(9)
    ok = sharp = True
    for name, m in EXT.items():
        if not m:
            continue
        for _ in range(3000):
            phi = rng.choice(layers(m))
            n = rng.randint(1, 10 ** 6)
            letter = ("A", rng.randrange(len(m))) if rng.random() < 0.4 else ("N", rng.randint(1, 200))
            psi2, u, v = letter_data(m, phi, letter)
            if rng.random() < 0.3:
                n *= v
            s, theta = 1.0 + rng.random() * 2, {p: rng.random() for p in (2, 3, 5, 7, 11)}
            mu = ((letter[1] + 1) ** 2 / letter[1]) if letter[0] == "N" else float(value(m[letter[1]]))
            n2 = u * n // gcd(n, v)
            lhs = mu ** -s * (gcd(n, v) / v) ** s
            bound = mu ** -s
            for p, t in theta.items():
                v0 = factorint(n).get(p, 0) + float(phi.get(p, 0))
                v1 = factorint(n2).get(p, 0) + float(psi2.get(p, 0))
                lhs *= p ** (t * s * (v1 - v0))
                X = (factorint(letter[1] + 1).get(p, 0) * 2 - factorint(letter[1]).get(p, 0)) if letter[0] == "N" \
                    else float(m[letter[1]].get(p, 0))
                bound *= p ** (t * s * X)
            ok &= lhs <= bound * (1 + 1e-9)
            if n % v == 0:
                sharp &= abs(lhs / bound - 1) < 1e-9
    check("ANS2-T15", "weighted one-step bound mu^-s q^(theta s X) holds", ok)
    check("ANS2-T15", "with equality when v divides n", sharp)


def growth():
    """Finite alphabet N <= 8 plus 2/sqrt3: exact-in-law dynamic programme for G_k against min Phi."""
    m, M, kmax = EXT["2/sqrt3"], 8, 20
    G = Grammar(TWO_OVER_SQRT3, M)
    rows, ok = [], True
    for a in (1.8, 2.0):
        th, term = G.minimise(a, {}, sweeps=400, tol=1e-13)
        lowest = float(term.sum())
        cert = G.lower_certificate(a, th, term)
        letters = [("N", N) for N in range(1, M + 1)] + [("A", 0)]
        mass, cache, Gk = {((), 1): 1.0}, {}, [1.0]
        for k in range(1, kmax + 1):
            new = {}
            for (psi, n), w in mass.items():
                if psi not in cache:
                    cache[psi] = []
                    for letter in letters:
                        psi2, u, v = letter_data(m, dict(psi), letter)
                        mu = ((letter[1] + 1) ** 2 / letter[1]) if letter[0] == "N" else float(value(m[0]))
                        cache[psi].append((tuple(sorted(psi2.items())), u, v, mu ** -a))
                for psi2, u, v, base in cache[psi]:
                    g = gcd(n, v)
                    t = (psi2, u * n // g)
                    new[t] = new.get(t, 0.0) + w * base * (g / v) ** a
            mass = new
            Gk.append(sum(mass.values()))
        C = 3 ** (a * 0.5)
        trials = [th, {}, {3: 0.05}, {2: 0.1, 3: 0.2}]
        for t in trials:
            phi = float(G.terms(a, t).sum())
            ok &= all(Gk[k] <= C * phi ** k * (1 + 1e-9) for k in range(1, kmax + 1))
        rows.append({"a": a, "min_Phi": lowest, "certified_lower": cert, "theta": {str(p): t for p, t in th.items() if t},
                     "free_B": float(G.terms(a, {}).sum()),
                     "G_k^(1/k)": {str(k): Gk[k] ** (1 / k) for k in (5, 10, 15, kmax)},
                     "G_k/min_Phi^k": {str(k): Gk[k] / lowest ** k for k in (5, 10, 15, kmax)}})
        print("   a", a, "minPhi", round(lowest, 6), "B", round(rows[-1]["free_B"], 6), "roots",
              [round(x, 5) for x in rows[-1]["G_k^(1/k)"].values()])
    check("ANS2-T16", "G_k <= C Phi(a, theta)^k for k <= 20 and four weights (N <= 8)", ok)
    OUT["finite_alphabet"] = rows


def abscissa():
    G = Grammar(TWO_OVER_SQRT3, 200000)
    low, high = bracket(G, 2.0, 2.1, steps=17)
    th, _ = G.minimise(high, {}, cap=0.10, sweeps=6)
    big = Grammar(TWO_OVER_SQRT3, 1000000)
    l, h = low, high
    for _ in range(14):
        mid = (l + h) / 2
        if big.upper_certificate(mid, th, big.terms(mid, th)) < 1:
            h = mid
        else:
            l = mid
    # primes that remain deficient when only the prime 3 is weighted
    keep, G.primes = G.primes, [3]
    th3, term = G.minimise(high, {})
    G.primes = keep
    grad = G.gradient(high, term)
    deficient = [p for p in G.primes if p != 3 and grad[p] < -1e-12]
    OUT["abscissa_2_over_sqrt3"] = {"lower": low, "upper": h, "largest_weight": max(th.values()),
                                    "weighted_primes": sum(t > 1e-6 for t in th.values()),
                                    "deficient_after_weighting_3_only": len(deficient), "first_deficient": deficient[:10]}
    check("ANS2-T16", "abscissa of 2/sqrt3: certified lower value below upper value, width < 0.001",
          low < h < low + 1e-3, (round(low, 5), round(h, 5)))
    check("ANS2-T16", "weighting the prime 3 alone leaves other primes with negative drift", len(deficient) > 0,
          (len(deficient), deficient[:6]))


def main():
    t0 = time.time()
    one_step()
    operator()
    weighted_norm()
    growth()
    abscissa()
    import numpy, sympy
    OUT["versions"] = {"python": platform.python_version(), "numpy": numpy.__version__, "sympy": sympy.__version__}
    OUT["checks"] = CHECKS
    OUT["passed"] = sum(c["status"] == "PASS" for c in CHECKS)
    OUT["failed"] = len(CHECKS) - OUT["passed"]
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    json.dump(OUT, open(os.path.join(HERE, "results", "operator_checks.json"), "w"), indent=1)
    print("%d passed, %d failed, %.1f s" % (OUT["passed"], OUT["failed"], time.time() - t0))
    sys.exit(1 if OUT["failed"] else 0)


if __name__ == "__main__":
    main()
