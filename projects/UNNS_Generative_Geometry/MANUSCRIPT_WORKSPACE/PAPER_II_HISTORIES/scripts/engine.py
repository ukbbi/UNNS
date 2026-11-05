"""Independent exact engine for Paper II (stdlib only).
SELECT-II: R(N)=(N+1)^2/N, T_N(m)=m*R(N), admissible iff N | m, N>=2."""
from math import gcd
from functools import lru_cache
from itertools import permutations
from fractions import Fraction

def vp(n,p):
    k=0
    while n%p==0: n//=p; k+=1
    return k
def primes_of(n):
    ps=[];d=2
    while d*d<=n:
        if n%d==0:
            ps.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:ps.append(n)
    return ps
def step(m,N):
    assert N>=1 and m%N==0
    return m//N*(N+1)**2
def run(m,w):
    out=[m]
    for N in w:
        if m%N: return None
        m=step(m,N); out.append(m)
    return out
def delta(N,p): return 2*vp(N+1,p)-vp(N,p)
def K(w):
    ps=set()
    for N in w: ps|=set(primes_of(N))|set(primes_of(N+1))
    k=1
    for p in ps:
        s=0;b=0
        for N in w:
            s+=delta(N,p); b=max(b,-s)
        k*=p**b
    return k
def admissible(m,w): return m%K(w)==0

# ---- complete ancestry H(t) ----
def sqdivs(t):
    return [d for d in range(2,int(t**0.5)+2) if d*d<=t and t%(d*d)==0]
@lru_cache(None)
def H(t):
    ds=sqdivs(t)
    if not ds: return 1
    return sum(H(t*(d-1)//(d*d)) for d in ds)
def pred(t):
    """predecessors of t: (d, s) with s=t(d-1)/d^2, s*(d+1)^2/d... """
    return [(d,t*(d-1)//(d*d)) for d in sqdivs(t)]
def histories(t):
    """all complete histories (source squarefree) ending at t, as (source, word)"""
    ds=sqdivs(t)
    res=[]
    if not ds: return [(t,())]
    for d in ds:
        s=t*(d-1)//(d*d)
        # forward edge s --N--> t with N+1=d? t = s*(N+1)^2/N : (N+1)=d requires t/s=d^2/(d-1)
        for src,w in histories(s): res.append((src,w+(d-1,)))
    return res
