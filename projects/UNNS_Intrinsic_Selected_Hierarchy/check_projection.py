"""Exact checks for the v1.2 projection subsection."""
import itertools
from math import gcd
def divs(n): return [d for d in range(1,n+1) if n%d==0]
def nbrs(x):
    S=set()
    for N in divs(x): S.add(x//N*(N+1)**2)
    q=2
    while q*q<=x:
        if x%(q*q)==0: S.add(x//(q*q)*(q-1))
        q+=1
    return S
assert nbrs(1)=={4} and nbrs(4)=={1,16,18,25}
print("N(36)=",sorted(nbrs(36)))
print("4~36?",36 in nbrs(4),"common nbrs:",nbrs(4)&nbrs(36))
print("1~5?",5 in nbrs(1)); print("edges {1,4},{5,36}:",4 in nbrs(1),36 in nbrs(5))
# T_2(6)=27 ; legality of N=5 at 6 and 30
print(6*9//2, 6%5, 30%5)
# Proposition: pi_P determines legality of T_N  iff supp(N) subset P  (tested on a box)
def vp(x,p):
    c=0
    while x%p==0: x//=p;c+=1
    return c
P=[2,3]
def proj(x): return tuple(vp(x,p) for p in P)
def fac_primes(n):
    s=set();p=2
    while p*p<=n:
        while n%p==0: s.add(p);n//=p
        p+=1
    if n>1:s.add(n)
    return s
ok=True
for N in range(1,61):
    fib={}
    for x in range(1,4001): fib.setdefault(proj(x),set()).add(x%N==0)
    determined=all(len(s)==1 for s in fib.values())
    pred=fac_primes(N)<=set(P) if N>1 else True
    if determined!=pred: ok=False;print("MISMATCH",N,determined,pred)
print("legality-determination iff supp(N) in P  (N<=60, x<=4000):",ok)
# E8 root system
import numpy as np
roots=[]
for i,j in itertools.combinations(range(8),2):
    for si in (1,-1):
        for sj in (1,-1):
            v=[0]*8;v[i]=si;v[j]=sj;roots.append(v)
for s in itertools.product((1,-1),repeat=8):
    if s.count(-1)%2==0: roots.append([x/2 for x in s])
R=np.array(roots,float);print("roots",len(R),"norm^2",set((R*R).sum(1)))
G=R@R.T; print("neighbours (ip=1):",set((G==1).sum(1)),"edges",int((G==1).sum()//2))
