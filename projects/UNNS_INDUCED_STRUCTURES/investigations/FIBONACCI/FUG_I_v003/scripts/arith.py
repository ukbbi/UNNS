"""Exact integer UNNS arithmetic for FUG-I v002 (no third-party packages).

All tested operands are < 2**64. A fixed-witness Miller-Rabin test is
DETERMINISTIC on that interval. Pollard rho only locates factors; factors
are independently certified prime and recombined to the original integer.
"""
from functools import lru_cache
from math import gcd

MAX_U64 = 1 << 64
_MR_WITNESSES = (2, 325, 9375, 28178, 450775, 9780504, 179526502)


def is_prime(n):
    if n < 2:
        return False
    if n >= MAX_U64:
        raise ValueError('v002 certificate is limited to integers below 2**64')
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    s = 0
    d = n - 1
    while not d % 2:
        s += 1
        d //= 2
    for a in _MR_WITNESSES:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _rho(n):
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23):
        if n % p == 0:
            return p
    for c in range(1, 1000):
        x = y = 2
        for _ in range(180000):
            x = (x*x+c) % n
            y = (y*y+c) % n
            y = (y*y+c) % n
            g = gcd(abs(x-y), n)
            if g == 1:
                continue
            if g != n:
                return g
            break
    raise RuntimeError('Pollard rho factor search failed on an integer < 2**64')


@lru_cache(None)
def factors(n):
    if n < 1 or n >= MAX_U64:
        raise ValueError('only positive integers below 2**64 are supported')
    original=n
    raw=[]
    def split(m):
        if m==1:return
        if is_prime(m):
            raw.append(m);return
        d=_rho(m)
        split(d);split(m//d)
    split(n)
    counts={}
    for p in raw:
        counts[p]=counts.get(p,0)+1
    fact=tuple(sorted(counts.items()))
    assert all(is_prime(p) for p,e in fact)
    prod=1
    for p,e in fact:prod *=p**e
    assert prod==original
    return fact


@lru_cache(None)
def divisors(n):
    ds=[1]
    for p,e in factors(n):
        ds=[d*p**i for d in ds for i in range(e+1)]
    return tuple(sorted(ds))


@lru_cache(None)
def incoming(y):
    """All labelled predecessor edges x --N--> y as triples (x,N,d=N+1)."""
    q=1
    for p,e in factors(y):q*=p**(e//2)
    out=[]
    for d in divisors(q):
        if d==1:continue
        x=(y//(d*d))*(d-1)
        N=d-1
        assert x%N==0 and (x//N)*d*d==y
        out.append((x,N,d))
    return tuple(sorted(out))


def step(x,N):
    if x<=0 or N<=0 or x%N:
        raise ValueError('inadmissible step; require positive x,N and N|x')
    return (x//N)*(N+1)**2


def fib(k):
    vals=[0,1]
    while len(vals)<=k:vals.append(vals[-1]+vals[-2])
    return vals


def lucas(k):
    vals=[2,1]
    while len(vals)<=k:vals.append(vals[-1]+vals[-2])
    return vals
