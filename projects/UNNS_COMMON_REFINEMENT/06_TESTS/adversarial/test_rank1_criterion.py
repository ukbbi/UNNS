#!/usr/bin/env python3
import math, itertools

def gcd_all(gens):
    g=0
    for x in gens: g=math.gcd(g,x)
    return g

def Hset(gens, limit):
    H={0}
    for n in range(limit+1):
        if n in H:
            for a in gens:
                if n+a<=limit: H.add(n+a)
    return H

def ambient(a,b,c,d):
    if a+b!=c+d: return []
    out=[]
    for e in range(max(0,c-b), min(a,c)+1):
        f=a-e; g=c-e; h=b-g
        if min(e,f,g,h)>=0 and a==e+f and b==g+h and c==e+g and d==f+h:
            out.append((e,f,g,h))
    return out

checked=0
nonref=0
ref=0

for r in range(1,5):
    for gens in itertools.combinations(range(1,13),r):
        checked+=1
        m=min(gens); g=gcd_all(gens)
        if m==g:
            # Exact: m is a generator and every generator is a multiple of m.
            assert all(x % m == 0 for x in gens)
            ref+=1
            continue

        H=Hset(gens,5000)
        x=min(v for v in H if v>0 and v % m != 0)
        k=2
        while k*x-m not in H:
            k+=1
        a,b,c,d=m,k*x-m,x,(k-1)*x
        W=ambient(a,b,c,d)
        valid=[w for w in W if all(t in H for t in w)]
        assert not valid, (gens,(a,b,c,d),valid)
        assert x-m not in H
        assert (k-1)*x-m not in H
        nonref+=1

print({"checked":checked,"refinement":ref,"nonrefinement":nonref,"status":"PASS"})
