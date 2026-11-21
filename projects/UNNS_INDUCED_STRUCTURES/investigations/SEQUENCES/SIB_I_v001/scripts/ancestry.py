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

@lru_cache(None)
def routes(x, depth):
    if depth == 0: return ((x,()),)
    return tuple((s,w+(label,)) for y,label in incoming(x)
                 for s,w in routes(y,depth-1))

def profile(x, depth=3):
    rr = [r for k in range(1,depth+1) for r in routes(x,k)]
    groups = defaultdict(list)
    for s,w in rr: groups[s].append(w)
    permutation = different = 0
    witness = None
    for s,words in groups.items():
        contents = Counter(tuple(sorted(w)) for w in words)
        permutation += sum(v*(v-1)//2 for v in contents.values())
        different += len(words)*(len(words)-1)//2 - sum(v*(v-1)//2 for v in contents.values())
        if witness is None and len(words)>1: witness = [s,words[0],words[1]]
    return dict(value=x, incoming=len(incoming(x)),
                depth1=len(routes(x,1)),depth2=len(routes(x,2)),depth3=len(routes(x,3)),
                routes=len(rr),distinct_words=len(set(w for _,w in rr)),
                sources=len(groups), min_depth=1 if rr else None,
                max_observed_depth=max((len(w) for _,w in rr),default=0),
                merger_sources=sum(len(w)>1 for w in groups.values()),
                permutation_pairs=permutation,different_content_pairs=different,
                witness=witness)
