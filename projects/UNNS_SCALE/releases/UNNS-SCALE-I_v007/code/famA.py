"""Family A (v007): divisor-generated four-step routes, generalised.
Parameters (a,b,t): gcd(a,b)=1, a>b>=1, t>=1;  c=(a-b)*t*a, d=(a-b)*t*b, s=t*a*b+1.   Need c|B, d|B.
For n with s | c*n+1 (and automatically s | d*(n+1)+1 when gcd(c,s)=1) and c*n+1>=2s, d*(n+1)+1>=2s:
  Bn --(N=c n)--> (B/c)(cn+1)^2 --(q=(cn+1)/s)--> B s (n-1+...)  ... common midpoint
  B(n+1) --(M=d(n+1))--> (B/d)(d(n+1)+1)^2 --(r=(d(n+1)+1)/s)--> same.
Midpoint value  m = (B/c) * s * (c n + 1 - s)."""
import sys, os, math, itertools
sys.dont_write_bytecode = True
def divisors_of(B):
    return sorted(d for d in range(1, B + 1) if B % d == 0) if B <= 10**7 else None
def families(B):
    D = set(divisors_of(B)); out = []
    for c in sorted(D):
        for d in sorted(D):
            if d >= c: continue
            g = math.gcd(c, d); a, b = c // g, d // g
            # need (s-1)=cd/(c-d) integer
            if (c * d) % (c - d): continue
            s = c * d // (c - d) + 1
            out.append((c, d, s))
    return out
def route(B, n, c, d, s):
    """return explicit path of length 4 or None"""
    if (c * n + 1) % s or (d * (n + 1) + 1) % s: return None
    q = (c * n + 1) // s; r = (d * (n + 1) + 1) // s
    if q < 2 or r < 2: return None
    x = B * n; y = B * (n + 1)
    x1 = x // (c * n) * (c * n + 1) ** 2; y1 = y // (d * (n + 1)) * (d * (n + 1) + 1) ** 2
    m = x1 // (q * q) * (q - 1); m2 = y1 // (r * r) * (r - 1)
    assert m == m2 == B // c * s * (c * n + 1 - s), (m, m2)
    return [x, x1, m, y1, y]
if __name__ == "__main__":
    B = 10**6
    F = families(B); print(len(F)); print(F)
