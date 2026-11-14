"""Independent specification of the ADJ4 selector. Written from the statement in the ADJ4 addendum only.
No code from the original release is imported or consulted."""
PRIMES=(2,3,5,7)
# priority order (first enabled wins), as stored in the frozen release data/order.txt
ORDER=[2400,3,35,15,27,4,14,2,5,48,4374,80,63,125,224,6,24,49,9,8,20,7]
X0_EXP=(4,6,4,3)          # x0 = 2^4 3^6 5^4 7^3
def val(n,p):
    c=0
    while n%p==0: n//=p; c+=1
    return c
def vec(n):
    """exponent vector of a 7-smooth integer n; raises if not 7-smooth"""
    v=[]
    for p in PRIMES:
        c=val(n,p); n//=p**c; v.append(c)
    if n!=1: raise ValueError(n)
    return tuple(v)
def smooth(n):
    for p in PRIMES:
        while n%p==0: n//=p
    return n==1
def moves_recomputed(limit):
    """all N in [2,limit] with N and N+1 both 7-smooth (forward moves of the prime set {2,3,5,7})"""
    return [n for n in range(2,limit+1) if smooth(n) and smooth(n+1)]
REQ={N:vec(N) for N in ORDER}
DELTA={N:tuple(2*a-b for a,b in zip(vec(N+1),vec(N))) for N in ORDER}
def enabled(v,N): return all(x>=r for x,r in zip(v,REQ[N]))
def select(v):
    for N in ORDER:
        if enabled(v,N): return N
    return None
def step(v):
    N=select(v)
    d=DELTA[N]; return N,tuple(x+y for x,y in zip(v,d))
def in_S(v): return v[1]==0 and v[3]==0 and v[0] in (0,1) and v[2]>=50000
