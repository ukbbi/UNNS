"""GEO-I exact-integer library. Written from the definitions in Vol I/II (A0, A2, C). No floating point in any check."""
import random
from fractions import Fraction as Fr
from math import gcd, isqrt

_SP = (2,3,5,7,11,13,17,19,23,29,31,37)
def is_prime(n):
    if n < 2: return False
    for p in _SP:
        if n % p == 0: return n == p
    d, r = n-1, 0
    while d % 2 == 0: d//=2; r+=1
    for a in _SP:
        x = pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True
def _rho(n, rng=random.Random(2026)):
    if n % 2 == 0: return 2
    while True:
        c = rng.randrange(1,n); x = y = rng.randrange(0,n); d = 1
        while d == 1:
            x=(x*x+c)%n; y=(y*y+c)%n; y=(y*y+c)%n; d=gcd(abs(x-y),n)
        if d != n: return d
def factor(n, res=None):
    if res is None: res = {}
    if n == 1: return res
    for p in _SP:
        while n % p == 0: res[p]=res.get(p,0)+1; n//=p
    f = 41
    while f < 3000 and f*f <= n:
        while n % f == 0: res[f]=res.get(f,0)+1; n//=f
        f += 2
    if n == 1: return res
    if is_prime(n): res[n]=res.get(n,0)+1; return res
    d=_rho(n); factor(d,res); factor(n//d,res); return res
def divisors_from(f):
    ds=[1]
    for p,e in f.items(): ds=[d*p**k for d in ds for k in range(e+1)]
    return ds
def lcm(a,b): return a//gcd(a,b)*b
def val(n, p):
    k=0
    while n % p == 0: n//=p; k+=1
    return k

# ---- A0: fibre of an integer; occurrence indices d=N+1 with d^2 | m
def fibre(m):
    f = factor(m)
    s = {p:e//2 for p,e in f.items() if e//2}
    return sorted(d for d in divisors_from(s) if d>=2)
def R(m): return len(fibre(m))
def Lof(D):
    L=1
    for d in D: L=lcm(L,d)
    return L
def Gof(D):
    g=0
    for d in D: g=gcd(g,d-1)
    return g
def fibre_q(x):
    """D(x) for a positive rational x=a/b (lowest terms): d>=2, d^2|a, d=1 mod b"""
    a,b=x.numerator,x.denominator
    f=factor(a) if a>1 else {}
    s={p:e//2 for p,e in f.items() if e//2}
    return sorted(d for d in divisors_from(s) if d>=2 and (d-1)%b==0)
def Cstep(x):
    x=Fr(x); D=fibre_q(x)
    if not D: return None
    L,G=Lof(D),Gof(D)
    y=x+Fr(L*L,G)
    return y.numerator if y.denominator==1 else y
def orbit(x0, n):
    xs=[x0]
    while len(xs)<n:
        y=Cstep(xs[-1])
        if y is None: break
        xs.append(y)
    return xs

# ---- A2: SELECT-II
def succ(m):
    return [(N, m*(N+1)**2//N) for N in range(1,m+1) if m % N == 0]
def build_graph(limit):
    """edges m -> m' with m' <= limit; returns preds dict (m' -> list of (m,N))"""
    preds={k:[] for k in range(1,limit+1)}
    for m in range(1,limit+1):
        for N in range(1,m+1):
            if m % N: continue
            mp = m*(N+1)**2//N
            if mp>limit: break   # (N+1)^2/N increasing in N
            preds[mp].append((m,N))
    return preds
