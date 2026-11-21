"""Exact integer ancestry; deterministic primality on unsigned 64-bit integers."""
from functools import lru_cache
from math import gcd, prod
from collections import Counter, defaultdict

def prime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d, s = n-1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2,325,9375,28178,450775,9780504,1795265022):
        if a % n == 0: continue
        x = pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

@lru_cache(None)
def factor(n):
    assert 1 <= n < 2**64
    if n == 1: return ()
    if prime(n): return ((n,1),)
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0:
            c = Counter(dict(factor(n//p))); c[p] += 1
            return tuple(sorted(c.items()))
    c = 1
    while True:
        x = y = 2; g = 1
        while g == 1:
            x = (x*x+c) % n
            y = (y*y+c) % n; y = (y*y+c) % n
            g = gcd(abs(x-y),n)
        if g != n: break
        c += 1
    counts = Counter(dict(factor(g))) + Counter(dict(factor(n//g)))
    return tuple(sorted(counts.items()))

@lru_cache(None)
def incoming(x):
    ds = [1]
    for p,e in factor(x):
        ds = [d*p**j for d in ds for j in range(e//2+1)]
    return tuple((x//(d*d)*(d-1),d-1) for d in sorted(ds) if d > 1)

