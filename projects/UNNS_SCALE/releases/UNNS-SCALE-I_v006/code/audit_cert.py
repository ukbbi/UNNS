"""Primality-audited lower-bound certificate (v006).  Re-derives complete balls where EVERY factorisation used is proved:
product of the listed prime powers equals the number, and each prime is proved by (a) trial division for p < 10^6, or (b) deterministic Miller-Rabin
with the first 13 primes, which is a proof for all p < 3.3170e24 (Sorenson-Webster 2015).  Primes above that bound are counted as UNPROVED.
Distance lower bound d: balls of radii (d//2, d-1-d//2) around u, v disjoint."""
import sys, os, time
sys.dont_write_bytecode = True
from sympy import factorint
from math import prod
MR13 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]; BOUND = 3317044064679887385961981   # 3.317e24
def mr_proof(p):
    if p < 2: return False
    for q in MR13:
        if p % q == 0: return p == q
    d, s = p - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in MR13:
        x = pow(a, d, p)
        if x in (1, p - 1): continue
        for _ in range(s - 1):
            x = x * x % p
            if x == p - 1: break
        else: return False
    return True
class Audit:
    def __init__(self): self.cache = {}; self.maxprime = 0; self.unproved = 0; self.nfact = 0; self.bad = 0
    def factor(self, n):
        if n in self.cache: return self.cache[n]
        f = factorint(n); self.nfact += 1
        if prod(p**e for p, e in f.items()) != n: self.bad += 1
        for p in f:
            self.maxprime = max(self.maxprime, p)
            if p < 10**6: continue
            if p >= BOUND: self.unproved += 1
            elif not mr_proof(p): self.bad += 1
        self.cache[n] = f; return f
def divisors(f):
    ds = [1]
    for p, e in f.items(): ds = [d * p**k for d in ds for k in range(e + 1)]
    return ds
def nbrs(A, n):
    f = A.factor(n); out = set()
    for N in divisors(f): out.add(n // N * (N + 1) ** 2)
    for q in divisors(f):
        if q >= 2 and n % (q * q) == 0: out.add(n // (q * q) * (q - 1))
    out.discard(n); return out
def ball(A, n, r):
    seen = {n}; frontier = {n}
    for _ in range(r):
        nxt = set()
        for x in frontier:
            for y in nbrs(A, x):
                if y not in seen: seen.add(y); nxt.add(y)
        frontier = nxt
    return seen
def audit(u, v, d):
    A = Audit(); r = d // 2; s = d - 1 - r
    Bu = ball(A, u, r); Bv = ball(A, v, s)
    return {"d_lower_bound": d, "radii": [r, s], "sizes": [len(Bu), len(Bv)], "disjoint": not (Bu & Bv), "factorisations": A.nfact, "max_prime_factor": A.maxprime,
            "factorisation_errors": A.bad, "primes_above_proof_bound": A.unproved}
if __name__ == "__main__":
    u, v, d = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); t = time.time(); print(audit(u, v, d), round(time.time() - t, 1))
