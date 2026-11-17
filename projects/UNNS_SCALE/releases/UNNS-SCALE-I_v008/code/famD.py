"""Theorem A'' (v007): constant-rho linear families, rho = P/Q (lowest terms) = 1 + c d /(c w' - d v') > 1.
Shape (v',w',c,d) with c,d|B, gcd(v',w')=1, Delta=c w'-d v'>0.  rho=(Delta+cd)/Delta = P/Q.
Admissible iff Q^2 | (B/c) v'  and  Q^2 | (B/d) w'  and gcd(c,P)=gcd(d,P)=1.
Class: v' | n, w' | n+1, P | c n/v' + 1  (then P | d (n+1)/w' + 1 automatically).
Route:  Bn --(N = c n/v')--> --(q = Q (c n/v'+1)/P)--> z ;  B(n+1) --(M = d (n+1)/w')--> --(r = Q (d (n+1)/w'+1)/P)--> z
z = (B/c)(v'/Q^2) P (Q(c n/v'+1) - P)       [Q=1: Theorem A']."""
import sys, os, math
sys.dont_write_bytecode = True
import numpy as np
from fractions import Fraction
def shapes(B, K):
    D = [d for d in range(1, B + 1) if B % d == 0]; out = []
    for vp in range(1, K + 1):
        for wp in range(1, K + 1):
            if math.gcd(vp, wp) != 1: continue
            for c in D:
                for d in D:
                    Dl = c * wp - d * vp
                    if Dl <= 0: continue
                    rho = Fraction(Dl + c * d, Dl); P, Q = rho.numerator, rho.denominator
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
def coverage(B, K, N, only_Q1=False):
    hit = np.zeros(N + 1, dtype=bool); S = [s for s in shapes(B, K) if not only_Q1 or s[5] == 1]
    for vp, wp, c, d, P, Q in S:
        L = vp * wp; r0 = next(r for r in range(0, L, vp) if (r + 1) % wp == 0)
        n = np.arange(r0 if r0 >= 2 else r0 + L, N + 1, L, dtype=np.int64)
        v = n // vp; w = (n + 1) // wp; u = c * v + 1; u2 = d * w + 1
        ok = ((u * Q) % P == 0) & ((u2 * Q) % P == 0) & (Q * u >= 2 * P) & (Q * u2 >= 2 * P)
        hit[n[ok]] = True
    return hit, S
if __name__ == "__main__":
    B = 10**6; N = 2_000_000
    for K in (1, 2, 3, 4, 6, 8, 12):
        h1, S1 = coverage(B, K, N, True); h, S = coverage(B, K, N)
        n720 = np.arange(719, N + 1, 720)
        print("K=%2d  Q=1: shapes %5d cov %.4f | rho=P/Q: shapes %5d cov %.4f  (720|n+1: %.4f)" % (K, len(S1), h1[2:].mean(), len(S), h[2:].mean(), h[n720].mean()), flush=True)
