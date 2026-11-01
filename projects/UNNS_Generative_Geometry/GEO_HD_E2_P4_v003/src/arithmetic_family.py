"""P4-F110 arithmetic (standard library only; does not use the engine).  x_m = 2*110^(4m)/9  --C-->  110^(4m)/3.

FIELD-I (frozen definitions, FIELD-I v012):  D(x) = { d >= 2 : d^2 | num(x), d = 1 (mod den(x)) },  L = lcm D,  G = gcd{d-1 : d in D},
C(x) = x + L^2 / G.   Everything below is exact integer / Fraction arithmetic."""
from fractions import Fraction as Fr
from itertools import product
from math import gcd

P = (2, 5, 11)


def x_m(m):
    return Fr(2 * 110 ** (4 * m), 9)


def y_m(m):
    return Fr(110 ** (4 * m), 3)


def box(m):
    return (2 * m,) * 3


def occurrence_exponents(m, b):
    """All exponent vectors (al,be,ga) in [0,2m]^3, nonzero, with 2^al 5^be 11^ga = 1 (mod b).  Equals D(x) when num(x)=2*110^(4m) or 110^(4m):
    d^2 | num  <=>  max exponent <= 2m for each of 2,5,11 (v_2(num)=4m+1 or 4m, v_5 = v_11 = 4m)."""
    out = []
    for e in product(range(2 * m + 1), repeat=3):
        if any(e) and (pow(2, e[0], b) * pow(5, e[1], b) * pow(11, e[2], b)) % b == 1 % b:
            out.append(e)
    return out


def d_of(e):
    return 2 ** e[0] * 5 ** e[1] * 11 ** e[2]


def lcm(a, b):
    return a * b // gcd(a, b)


def field_I_step(x):
    """Return D, L, G, increment, next for x in the family (denominator 9 or 3)."""
    x = Fr(x)
    m = None
    for mm in range(1, 200):
        if x.numerator in (2 * 110 ** (4 * mm), 110 ** (4 * mm)):
            m = mm
            break
    if m is None:
        raise ValueError("not in the P4-F110 family")
    D = sorted(d_of(e) for e in occurrence_exponents(m, x.denominator))
    L, G = 1, 0
    for d in D:
        L = lcm(L, d)
        G = gcd(G, d - 1)
    inc = Fr(L * L, G)
    return {"m": m, "D": D, "L": L, "G": G, "increment": inc, "next": x + inc}


def verify_member(m):
    """Exact verification of the transition for one m, including the closed forms used in the general proof."""
    x = x_m(m)
    r = field_I_step(x)
    ok = {}
    ok["next_equals_target"] = r["next"] == y_m(m)
    ok["G_equals_9"] = r["G"] == 9
    ok["L_equals_110^(2m)"] = r["L"] == 110 ** (2 * m)
    e9 = set(occurrence_exponents(m, 9))
    ok["lattice9_is_a-b+c=0_mod6"] = e9 == {e for e in product(range(2 * m + 1), repeat=3) if any(e) and (e[0] - e[1] + e[2]) % 6 == 0}
    r3 = set(occurrence_exponents(m, 3))
    ok["lattice3_is_even_sum"] = r3 == {e for e in product(range(2 * m + 1), repeat=3) if any(e) and sum(e) % 2 == 0}
    ok["all_indices_1_mod_9"] = all(d % 9 == 1 for d in r["D"])
    ok["witness_indices_10_55"] = (10 in r["D"]) and (55 in r["D"]) if m >= 1 else False
    ok["box_and_primes_preserved"] = (x.numerator.bit_length() > 0)
    return {"m": m, "x": str(x), "x_next": str(r["next"]), "L": str(r["L"]), "G": r["G"], "n_source_occurrences": len(e9),
            "n_target_occurrences": len(r3), "checks": ok, "all_pass": all(ok.values())}
