"""Proposition B (v007): linear-label four-step routes at scale B.
Data: c|B, v|n, s|(c v+1) with q=(c v+1)/s>=2;  d|B, w|(n+1), s'|(d w+1) with r=(d w+1)/s'>=2.
  Bn --(N=c v)--> (B/c)(n/v)(cv+1)^2 --(q)--> z = (B/c)(n/v) s (c v+1-s)
  B(n+1) --(M=d w)--> (B/d)((n+1)/w)(dw+1)^2 --(r)--> z' = (B/d)((n+1)/w) s'(d w+1-s')
If z = z' the route has length 4.   Exact enumeration (complete divisor lists)."""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import factor, _divisors
def side(B, m, fB):
    """dict z -> (v,c,s)  for the number m (m=n or n+1) in place of n"""
    out = {}
    for v in _divisors(factor(m)):
        for c in fB:
            u = c * v + 1
            for s in _divisors(factor(u)):
                if 2 * s <= u:
                    z = (B // c) * (m // v) * s * (u - s)
                    out.setdefault(z, (v, c, s))
    return out
def propB(B, n):
    fB = sorted(_divisors(factor(B)))
    a = side(B, n, fB); b = side(B, n + 1, fB)
    for z, t in a.items():
        if z in b: return t + b[z] + (z,)
    return None
def check(B, n, w):
    (v, c, s, w_, d, s2, z) = (w[0], w[1], w[2], w[3], w[4], w[5], w[6])
    N = c * v; M = d * w_; x = B * n; y = B * (n + 1)
    assert x % N == 0 and y % M == 0 and B % c == 0 and B % d == 0 and n % v == 0 and (n + 1) % w_ == 0
    q = (c * v + 1) // s; r = (d * w_ + 1) // s2
    assert q * s == c * v + 1 and r * s2 == d * w_ + 1 and q >= 2 and r >= 2
    x1 = x // N * (N + 1) ** 2; y1 = y // M * (M + 1) ** 2
    assert x1 % (q * q) == 0 and y1 % (r * r) == 0
    assert x1 // (q * q) * (q - 1) == z == y1 // (r * r) * (r - 1)
    return True
if __name__ == "__main__":
    for n in (11, 13, 3239, 5039): print(n, propB(10**6, n))
