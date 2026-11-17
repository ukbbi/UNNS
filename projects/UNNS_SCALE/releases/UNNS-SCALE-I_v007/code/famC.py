"""Constant-s linear families (v007 Theorem A').
Shape (v',w',c,d,s): c,d|B, gcd(v',w')=1, Delta=c*w'-d*v'>0, Delta | c*d, s=cd/Delta+1.
Class: n = 0 mod v', n = -1 mod w', s | c*(n/v')+1, and automatically s | d*((n+1)/w')+1 if gcd(c,s)=1.
Route:  Bn --(N=c n/v')--> --(q=(cn/v'+1)/s)--> z ;  B(n+1) --(M=d(n+1)/w')--> --(r=(d(n+1)/w'+1)/s)--> z
z = (B/c) v' s (c n/v' + 1 - s).  """
import sys, os, math
sys.dont_write_bytecode = True
import numpy as np
def shapes(B, K):
    D = [d for d in range(1, B + 1) if B % d == 0]; out = []
    for vp in range(1, K + 1):
        for wp in range(1, K + 1):
            if math.gcd(vp, wp) != 1: continue
            for c in D:
                for d in D:
                    Dl = c * wp - d * vp
                    if Dl <= 0 or (c * d) % Dl: continue
                    s = c * d // Dl + 1
                    if math.gcd(c, s) != 1 or math.gcd(d, s) != 1: continue
                    out.append((vp, wp, c, d, s))
    return out
def route(B, n, sh):
    vp, wp, c, d, s = sh
    if n % vp or (n + 1) % wp: return None
    v = n // vp; w = (n + 1) // wp
    if (c * v + 1) % s or (d * w + 1) % s: return None
    q = (c * v + 1) // s; r = (d * w + 1) // s
    if q < 2 or r < 2: return None
    x = B * n; y = B * (n + 1); N = c * v; M = d * w
    x1 = x // N * (N + 1) ** 2; y1 = y // M * (M + 1) ** 2
    z = x1 // (q * q) * (q - 1); z2 = y1 // (r * r) * (r - 1)
    assert z == z2 == (B // c) * vp * s * (c * v + 1 - s)
    return [x, x1, z, y1, y]
def coverage(B, K, N):
    hit = np.zeros(N + 1, dtype=bool); S = shapes(B, K)
    for vp, wp, c, d, s in S:
        # n = vp*m with n = -1 mod wp
        L = vp * wp
        r0 = next(r for r in range(0, L, vp) if (r + 1) % wp == 0)
        n = np.arange(r0 if r0 >= 2 else r0 + L, N + 1, L, dtype=np.int64)
        v = n // vp; w = (n + 1) // wp
        ok = ((c * v + 1) % s == 0) & ((d * w + 1) % s == 0) & ((c * v + 1) >= 2 * s) & ((d * w + 1) >= 2 * s)
        hit[n[ok]] = True
    return hit, S
if __name__ == "__main__":
    B = 10**6; N = 2_000_000
    for K in (1, 2, 3, 4, 6, 8, 12):
        hit, S = coverage(B, K, N)
        n720 = np.arange(719, N + 1, 720)
        print("K=%2d shapes=%5d covered %.4f   among 720|n+1: %.4f" % (K, len(S), hit[2:].mean(), hit[n720].mean()), flush=True)
