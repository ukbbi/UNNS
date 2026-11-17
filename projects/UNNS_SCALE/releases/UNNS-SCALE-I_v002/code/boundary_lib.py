"""UNNS-SCALE-I v002 -- closed forms for the boundary arithmetic (stdlib + optional numpy)."""
from itertools import product
from math import gcd, floor, log, isqrt

EULER_GAMMA = 0.5772156649015329


def _union(fa, fb):
    return sorted(set(fa) | set(fb))


def tau_e(f):
    t = 1
    for e in f.values():
        t *= e + 1
    return t


def sq1_e(f):
    """s(u)+1 = #{q >= 1 : q^2 | u}."""
    t = 1
    for e in f.values():
        t *= e // 2 + 1
    return t


def deg_e(f):
    return tau_e(f) + sq1_e(f) - 1


def mul_e(f, g):
    h = dict(f)
    for p, e in g.items():
        h[p] = h.get(p, 0) + e
    return h


def eps_closed(fB, fx):
    """Theorem A1:  eps_B(x) = prod(a+b+1) - prod(a+1) + prod(floor((a+b)/2)+1) - prod(floor(a/2)+1)."""
    ps = _union(fB, fx)
    t1 = t0 = s1 = s0 = 1
    for p in ps:
        a, b = fx.get(p, 0), fB.get(p, 0)
        t1 *= a + b + 1; t0 *= a + 1
        s1 *= (a + b) // 2 + 1; s0 *= a // 2 + 1
    return t1 - t0 + s1 - s0


def strata(radices_f, fx):
    """Level profile of u = P_d x for the chain radices_f = [fB_1,...,fB_d] (factorisation dicts).
    Returns [n_0,...,n_d] where n_j = number of neighbours of u in P_j Z but not in P_{j+1} Z (n_d = deg(x))."""
    d = len(radices_f)
    # u / P_j = B_{j+1}...B_d x
    degs = []
    for j in range(d + 1):
        f = dict(fx)
        for g in radices_f[j:]:
            f = mul_e(f, g)
        degs.append(deg_e(f))
    return [degs[j] - degs[j + 1] for j in range(d)] + [degs[d]]


# ----------------------------------------------------------- asymptotic mean
def c_B(fB):
    """Leading coefficient of the mean of tau(Bx):  prod (b + 1 - b/p)."""
    c = 1.0
    for p, b in fB.items():
        c *= b + 1 - b / p
    return c


def _h_terms(fB):
    """Squarefree divisors m of rad(B) with h(m) = prod_{p|m} (-b_p/(b_p+1))."""
    ps = sorted(fB)
    out = []
    for choice in product([0, 1], repeat=len(ps)):
        m, h = 1, 1.0
        for p, c in zip(ps, choice):
            if c:
                m *= p; h *= -fB[p] / (fB[p] + 1)
        out.append((m, h))
    return out


def tau_mean_const(fB):
    """Constants (c, d) with  (1/X) sum_{n<=X} tau(Bn) = c*(log X + 2g - 1) - d + O(X^-1/2),
    c = c_B,  d = tau(B) * sum_m h(m) log(m) / m."""
    tB = tau_e(fB)
    c = tB * sum(h / m for m, h in _h_terms(fB))
    d = tB * sum(h * log(m) / m for m, h in _h_terms(fB))
    return c, d


def s_mean_const(fB):
    """K_B = sum_{q>=1} (gcd(q^2,B) - 1) / q^2  (closed Euler product form)."""
    zeta2 = 1.6449340668482264
    prod = 1.0
    for p, b in fB.items():
        a0 = b // 2 + 1
        L = a0 + p ** (b - 2 * a0) / (1 - p ** -2.0)
        prod *= (1 - p ** -2.0) * L
    return zeta2 * (prod - 1)


def predicted_mean(fB, X):
    c, d = tau_mean_const(fB)
    return (c - 1) * (log(X) + 2 * EULER_GAMMA - 1) - d + s_mean_const(fB)
