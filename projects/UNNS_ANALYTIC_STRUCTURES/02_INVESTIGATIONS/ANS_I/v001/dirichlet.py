"""Analytic evaluations (standard library only): zeta, Hurwitz zeta, B(sigma), convergence
boundaries, depth-two representation (ANS-T05/T13), coupling constant kappa, summatory growth."""
from math import gcd, isqrt, log, fsum

BERN = [1/6, -1/30, 1/42, -1/30, 5/66, -691/2730, 7/6, -3617/510]


def hurwitz(s, a=1.0, N=30):
    """Hurwitz zeta by Euler-Maclaurin, real or complex s with Re s > -8, s != 1."""
    head = sum((a + k) ** (-s) for k in range(N))
    x = a + N
    tot = head + x ** (1 - s) / (s - 1) + 0.5 * x ** (-s)
    term, fact = s, 2.0
    xp = x ** (-s - 1)
    for j, b in enumerate(BERN, start=1):
        tot += b / fact * term * xp
        term *= (s + 2 * j - 1) * (s + 2 * j)
        fact *= (2 * j + 1) * (2 * j + 2)
        xp /= x * x
    return tot


def zeta(s):
    return hurwitz(s, 1.0)


def B_bracket(sig, M=100000):
    """Rigorous bracket (up to floating rounding) for B(sig)=sum_{m>=2} (m-1)^sig / m^(2 sig),
    1 < sig < 2, using 1 - sig x <= (1-x)^sig - [sig(sig-1)x^2/2 >= 0] ."""
    head = fsum((m - 1) ** sig / m ** (2 * sig) for m in range(2, M))
    z0, z1, z2 = (hurwitz(sig + j, float(M)) for j in range(3))
    lo = head + z0 - sig * z1 + sig * (sig - 1) / 2 * z2
    # (1-x)^sig <= 1 - sig x + sig(sig-1)/2 x^2 (1-1/M)^(sig-2)   for 0 <= x <= 1/M
    hi = head + z0 - sig * z1 + sig * (sig - 1) / 2 * (1 - 1 / M) ** (sig - 2) * z2
    return lo, hi


def bisect(f, lo, hi, it=60):
    """root of a decreasing function f with f(lo) > 0 > f(hi)."""
    assert f(lo) > 0 > f(hi), (f(lo), f(hi))
    for _ in range(it):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def sigma_c():
    """Enclosure of the root of B(sigma)=1 with a 1e-9 certified-margin bracket."""
    r = bisect(lambda s: B_bracket(s, 20000)[0] - 1, 1.3, 1.9, 45)
    lo, hi = r - 5e-9, r + 5e-9
    ok = B_bracket(lo)[0] > 1 + 1e-12 and B_bracket(hi)[1] < 1 - 1e-12
    return lo, hi, ok


def spf_table(n):
    s = list(range(n + 1))
    for i in range(2, isqrt(n) + 1):
        if s[i] == i:
            for j in range(i * i, n + 1, i):
                if s[j] == j:
                    s[j] = i
    return s


def G2_representation(s, D):
    """sum_{d<=D} J_s(d) d^(-2s) zeta(2s,1+1/d) (c(d)^(-2s) zeta(2s) - [d=1])."""
    spf = spf_table(D)
    z = zeta(2 * s)
    tot = 0
    for d in range(1, D + 1):
        n, J, c = d, 1, 1
        while n > 1:
            p, e = spf[n], 0
            while n % p == 0:
                n //= p
                e += 1
            J *= p ** (e * s) * (1 - p ** (-s))
            c *= p ** ((e + 1) // 2)
        tot += J * d ** (-2 * s) * hurwitz(2 * s, 1 + 1 / d, 12) * (c ** (-2 * s) * z - (d == 1))
    return tot


def G2_direct(s, A):
    """Partial double sum over 1 <= a,b <= A."""
    return fsum((gcd((a + 1) ** 2, b) / ((a + 1) ** 2 * (b + 1) ** 2)) ** s
                for a in range(1, A + 1) for b in range(1, A + 1))


def kappa_local(p, terms=60):
    x = p ** -0.5
    return 1 + (1 - x) * fsum(p ** (-k / 2 - (k + 1) // 2) for k in range(1, terms)
                              if k * 0.5 * log(p) < 80)


def kappa(P=2_000_000):
    """Euler product for kappa up to P with first-order tail correction.
    log kappa_p = p^(-3/2) + O(p^(-2)); returns (partial, corrected, tail_estimate)."""
    s = bytearray([1]) * (P + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, isqrt(P) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(range(i * i, P + 1, i)))
    L = fsum(log(kappa_local(p)) for p in range(2, P + 1) if s[p])
    # sum_{p>P} p^(-3/2) ~ integral dt / (t^(3/2) log t) ~ 2/(sqrt(P) log P) * (1 - 2/log P)
    tail = 2 / (P ** 0.5 * log(P)) * (1 - 2 / log(P))
    from math import exp
    return exp(L), exp(L + tail), tail


def digamma(x):
    r = 0.0
    while x < 20:
        r -= 1 / x
        x += 1
    return r + log(x) - 1 / (2 * x) - 1 / (12 * x * x) + 1 / (120 * x ** 4) - 1 / (252 * x ** 6)


def second_constant(P=2_000_000, D=100000):
    """Coefficient of sqrt(X) in the residue of G_2(s) X^s / s at s = 1/2:
    c = 2 gamma kappa + F'(1/2)/2 + S - 1 - kappa, with F(s) the Euler product equal to kappa at
    s = 1/2 and S = sum_d J_{1/2}(d)/(d c(d)) (-psi(1+1/d) - gamma). Numerical, not certified."""
    gam = 0.5772156649015329
    k = kappa(P)[1]
    spf_P = bytearray([1]) * (P + 1)
    spf_P[0:2] = b"\x00\x00"
    for i in range(2, isqrt(P) + 1):
        if spf_P[i]:
            spf_P[i * i::i] = bytearray(len(range(i * i, P + 1, i)))

    def f(p, s):
        return 1 + (1 - p ** -s) * fsum(p ** (-j * s - 2 * s * ((j + 1) // 2))
                                         for j in range(1, 60) if j * s * log(p) < 45)
    h = 1e-5
    dlog = fsum((log(f(p, .5 + h)) - log(f(p, .5 - h))) / (2 * h)
                for p in range(2, P + 1) if spf_P[p]) - 6 / P ** 0.5
    spf = spf_table(D)
    S = 0.0
    for d in range(1, D + 1):
        n, J, c = d, 1.0, 1
        while n > 1:
            p, e = spf[n], 0
            while n % p == 0:
                n //= p
                e += 1
            J *= p ** (e * .5) * (1 - p ** -.5)
            c *= p ** ((e + 1) // 2)
        S += J / (d * c) * (-digamma(1 + 1 / d) - gam)
    return 2 * gam * k + k * dlog / 2 + S - 1 - k


def A2_count(X):
    """Number of depth-two words with minimal endpoint <= X (exact)."""
    total = 0
    for m in range(2, isqrt(X) + 1):           # m = a+1
        m2 = m * m
        bmax = X // m2                          # E >= m^2 (b+1)
        for b in range(1, bmax + 1):
            if (b + 1) ** 2 * (m2 // gcd(m2, b)) <= X:
                total += 1
    return total


if __name__ == "__main__":
    print("zeta(2) =", zeta(2.0))
    print("sigma_c enclosure:", sigma_c())
    print("kappa:", kappa(200000))
