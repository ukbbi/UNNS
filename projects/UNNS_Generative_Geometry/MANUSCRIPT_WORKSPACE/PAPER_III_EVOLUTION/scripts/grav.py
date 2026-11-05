import itertools
from fractions import Fraction as Fr
from math import gcd
from eng3 import *
def active_primes(a):
    return {p: e // 2 for p, e in factor(a).items() if e // 2 >= 1}
def lattice_member(g, ps, b):
    """sum g_i * ? -- membership of g in Lambda_b : prod p_i^{g_i} = 1 mod b (b coprime to p)"""
    if b == 1: return True
    num = 1; den = 1
    for p, e in zip(ps, g):
        if e > 0: num = num * pow(p, e, b) % b
        elif e < 0: den = den * pow(p, -e, b) % b
    return (num - den) % b == 0
def region_graver(x):
    x = Fr(x); a, b = x.numerator, x.denominator; q = active_primes(a); ps = sorted(q); box = [q[p] for p in ps]
    vecs = [g for g in itertools.product(*[range(-t, t + 1) for t in box]) if any(g) and lattice_member(g, ps, b)]
    def dom(h, g):  # h conformally <= g
        return all((hi == 0) or (hi * gi > 0 and abs(hi) <= abs(gi)) for hi, gi in zip(h, g))
    gr = [g for g in vecs if not any(h != g and dom(h, g) for h in vecs)]
    return ps, box, sorted(gr)
def fibre(x):
    x = Fr(x); a, b = x.numerator, x.denominator; q = active_primes(a); ps = sorted(q)
    F = []
    for al in itertools.product(*[range(0, q[p] + 1) for p in ps]):
        if not any(al): continue
        d = 1
        for p, e in zip(ps, al): d *= p ** e
        if (d - 1) % b == 0: F.append(al)
    return ps, F
