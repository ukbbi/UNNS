"""HD-E0: source-locked FIELD-I adapter.  Implements ONLY the frozen definitions recorded in GEO_HD_1_PROJECT/DEFINITIONS.md:
    x = a/b reduced;  D(x) = {d >= 2 : d^2 | a and d = 1 (mod b)};  L = lcm D(x);  G = gcd{d-1 : d in D(x)};  C(x) = x + L^2/G.
x is 'realized' iff D(x) is non-empty.  Nothing here is a SELECT-II object."""
from fractions import Fraction
from math import gcd, lcm
from functools import reduce
from prime_geometry import factor, vp


def D(x):
    x = Fraction(x); a, b = x.numerator, x.denominator
    s = 1
    for p, e in factor(a).items(): s *= p ** (e // 2)
    divs = [1]
    for p, e in factor(s).items(): divs = [d * p ** i for d in divs for i in range(e + 1)]
    return sorted(d for d in divs if d >= 2 and (d - 1) % b == 0)


def LG(x):
    d = D(x)
    if not d: return None
    return reduce(lcm, d), reduce(gcd, [t - 1 for t in d])


def C(x):
    x = Fraction(x); lg = LG(x)
    if lg is None: return None
    L, G = lg
    return x + Fraction(L * L, G)


def strand(x0, n):
    xs = [Fraction(x0)]
    for _ in range(n):
        y = C(xs[-1])
        if y is None: break
        xs.append(y)
    return xs


def val(x, P):
    x = Fraction(x); out = []
    for p in P:
        out.append(vp(x.numerator, p) - vp(x.denominator, p))
    return tuple(out)


def prime_support(xs):
    s = set()
    for x in xs:
        s |= set(factor(x.numerator)) | set(factor(x.denominator))
    return sorted(s)
