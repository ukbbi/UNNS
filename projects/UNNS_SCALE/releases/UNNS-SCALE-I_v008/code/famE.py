"""v008: constant-ratio shapes INCLUDING rho<1 (Delta<0).  Same route identity as Theorem A'' (v007) -- v007 had restricted to Delta>0.
Shape (v',w',c,d): c,d | B, gcd(v',w')=1, Delta = c w' - d v' != 0, rho = 1 + c d / Delta = P/Q > 0 (lowest terms)."""
import sys, os, math
sys.dont_write_bytecode = True
import numpy as np
from fractions import Fraction
def shapes(B, K, allow_neg=True):
    D = [d for d in range(1, B + 1) if B % d == 0]; out = []
    for vp in range(1, K + 1):
        for wp in range(1, K + 1):
            if math.gcd(vp, wp) != 1: continue
            for c in D:
                for d in D:
                    Dl = c * wp - d * vp
                    if Dl == 0: continue
                    if Dl < 0 and not allow_neg: continue
                    rho = 1 + Fraction(c * d, Dl)
                    if rho <= 0: continue
                    P, Q = rho.numerator, rho.denominator
                    if math.gcd(c, P) != 1 or math.gcd(d, P) != 1: continue
                    if ((B // c) * vp) % (Q * Q) or ((B // d) * wp) % (Q * Q): continue
                    out.append((vp, wp, c, d, P, Q))
    return out
def route(B, n, sh):
    vp, wp, c, d, P, Q = sh
    if n % vp or (n + 1) % wp: return None
    v = n // vp; w = (n + 1) // wp; u = c * v + 1; u2 = d * w + 1
    if (Q * u) % P or (Q * u2) % P: return None
    q = Q * u // P; r = Q * u2 // P
    if q < 2 or r < 2: return None
    x = B * n; y = B * (n + 1); N = c * v; M = d * w
    x1 = x // N * (N + 1) ** 2; y1 = y // M * (M + 1) ** 2
    if x1 % (q * q) or y1 % (r * r): return None
    z = x1 // (q * q) * (q - 1); z2 = y1 // (r * r) * (r - 1)
    assert z == z2, (n, sh)
    return [x, x1, z, y1, y]
def coverage(B, K, N, allow_neg=True):
    hit = np.zeros(N + 1, dtype=bool); S = shapes(B, K, allow_neg)
    for vp, wp, c, d, P, Q in S:
        L = vp * wp; r0 = next(r for r in range(0, L, vp) if (r + 1) % wp == 0)
        n = np.arange(r0 if r0 >= 2 else r0 + L, N + 1, L, dtype=np.int64)
        v = n // vp; w = (n + 1) // wp; u = c * v + 1; u2 = d * w + 1
        ok = ((u * Q) % P == 0) & ((u2 * Q) % P == 0) & (Q * u >= 2 * P) & (Q * u2 >= 2 * P)
        hit[n[ok]] = True
    return hit, S
if __name__ == "__main__":
    B = 10**6; N = 2_000_000
    for K in (1, 2, 3, 4, 6, 8, 12, 20):
        h, S = coverage(B, K, N); h0, S0 = coverage(B, K, N, False); n720 = np.arange(719, N + 1, 720)
        neg = [s for s in S if s[3] * s[0] > s[2] * s[1]]
        print("K=%2d  Delta>0 only: %5d shapes cov %.5f | with rho<1: %5d shapes (%d with Delta<0)  cov %.5f uncovered %d  (720|n+1: %.4f)" % (K, len(S0), h0[2:].mean(), len(S), len(neg), h[2:].mean(), int((~h[2:]).sum()), h[n720].mean()), flush=True)
