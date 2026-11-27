"""Cross-grammar controls: both engines on each grammar, closed forms, boundary values."""
from math import gcd, isqrt, fsum
from endpoint_engine import endpoint_census, nesting_labels, unpack, WIDTH
from ancestry_engine import ancestry_census, nesting_pairs
from mobius_check import mobius_transform, primes_upto
from dirichlet import zeta, bisect, B_bracket, hurwitz


def grammars(X):
    """name -> (labels for Engine B, (p,q) pairs for Engine A, has q=1 on every label)."""
    P = primes_upto(X)
    out = {
        "selected_nesting": (nesting_labels(X, 2), nesting_pairs(X, 2), False),
        "integer_scaling": ([(N, N + 1, 1) for N in range(1, X)],
                            [(N + 1, 1) for N in range(1, X)], True),
        "square_scaling": ([(N, (N + 1) ** 2, 1) for N in range(1, isqrt(X))],
                           [((N + 1) ** 2, 1) for N in range(1, isqrt(X))], True),
        "cubic_nesting": (nesting_labels(X, 3), nesting_pairs(X, 3), False),
        "prime_scaling": ([(p, p, 1) for p in P], [(p, 1) for p in P], True),
        "finite_2_3": ([(2, 2, 1), (3, 3, 1)], [(2, 1), (3, 1)], True),
        "empty": ([], [], True),
        "single_label_N1": ([(1, 4, 1)], [(4, 1)], True),
        "consuming_3/2_9/4": ([(1, 3, 2), (2, 9, 4)], [(3, 2), (9, 4)], False),
    }
    return out


def free_coefficients(X, ps):
    """Coefficients of 1/(1 - t sum_p p^-s), packed by depth: the closed form when every q=1."""
    a = [0] * (X + 1)
    a[1] = 1
    for n in range(1, X + 1):
        if a[n]:
            for p in ps:
                if n * p > X:
                    break
                a[n * p] += a[n] << WIDTH
    return a


def run_grammar(X, name, spec):
    labels, pairs, free = spec
    a = endpoint_census(X, labels)
    H = ancestry_census(X, pairs)
    inv = mobius_transform(H)
    bad = sum(inv[n] != a.get(n, 0) for n in range(1, X + 1))
    res = {"grammar": name, "X": X, "engine_mismatches": bad,
           "words": sum(sum(unpack(v)) for v in a.values()), "endpoints": len(a),
           "max_depth": max(len(unpack(v)) for v in a.values()) - 1,
           "max_multiplicity": max(sum(unpack(v)) for v in a.values())}
    if free:
        c = free_coefficients(X, sorted(p for p, _ in pairs))
        res["closed_form_mismatches"] = sum(c[n] != a.get(n, 0) for n in range(1, X + 1))
    # non-multiplicativity witness for H: least coprime product
    h = [sum(unpack(v)) for v in H]
    wit = None
    for n in range(2, min(X, 5000) + 1):
        for m in range(2, isqrt(n) + 1):
            if n % m == 0 and m < n // m and gcd(m, n // m) == 1 and h[n] != h[m] * h[n // m]:
                wit = [m, n // m, h[m], h[n // m], h[n]]
                break
        if wit:
            break
    res["H_multiplicativity_witness"] = wit
    return res


def prime_zeta(s):
    """P(s)=sum_p p^-s = sum_k mu(k)/k log zeta(ks)."""
    from math import log
    from mobius_check import mu
    return fsum(mu(k) / k * log(zeta(k * s)) for k in range(1, 60) if mu(k))


def Bd(sig, d, M=100000):
    """sum_{m>=2} ((m-1)/m^d)^sig, tail by Hurwitz zeta."""
    head = fsum(((m - 1) / m ** d) ** sig for m in range(2, M))
    e = (d - 1) * sig
    return head + hurwitz(e, float(M)) - sig * hurwitz(e + 1, float(M)) \
        + sig * (sig - 1) / 2 * hurwitz(e + 2, float(M))


def boundaries():
    """Convergence abscissa of G(s,1): the point where the total one-step series equals 1."""
    return {
        "selected_nesting": bisect(lambda s: B_bracket(s, 20000)[0] - 1, 1.3, 1.9),
        "integer_scaling": bisect(lambda s: zeta(s) - 2, 1.2, 3.0),
        "square_scaling": bisect(lambda s: zeta(2 * s) - 2, 0.6, 1.2),
        "cubic_nesting": bisect(lambda s: Bd(s, 3, 20000) - 1, 0.55, 1.5),
        "prime_scaling": bisect(lambda s: prime_zeta(s) - 1, 1.1, 2.5),
        "finite_2_3": bisect(lambda s: 2 ** -s + 3 ** -s - 1, 0.1, 2.0),
        "single_label_N1": 0.0,
        "consuming_3/2_9/4": bisect(lambda s: 3 ** -s + 9 ** -s - 1, 0.05, 2.0),
    }


if __name__ == "__main__":
    for nm, sp in grammars(20000).items():
        print(run_grammar(20000, nm, sp))
    print(boundaries())
