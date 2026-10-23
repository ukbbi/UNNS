#!/usr/bin/env python3
"""FIELD-I v006 — independently reproducible tests, exact positive-rational arithmetic.

Tests shadows of proved theorems L1–L7 in THEOREMS.md, never treats finite
sampling as a proof. No imports from, or modifications to, v002–v005.
Python >= 3.10, standard library only.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import gcd, isqrt
from collections import Counter
import os, sys, json, hashlib

QUICK = os.environ.get('FIELD6_QUICK','0') == '1'
results = []; failures = 0

def check(code, ok, detail):
    global failures
    status = 'PASS' if ok else 'FAIL'
    failures += (not ok)
    results.append(dict(id=code,status=status,detail=str(detail)))
    print(f'{status} {code}: {detail}',flush=True)

def info(code,status,detail):
    results.append(dict(id=code,status=status,detail=str(detail)))
    print(f'{status} {code}: {detail}',flush=True)

def lcm(a,b): return a // gcd(a,b) * b

@lru_cache(None)
def factor(n):
    assert n>=1
    parts=[]; p=2
    while p*p<=n:
        if n%p==0:
            e=0
            while n%p==0: n//=p; e+=1
            parts.append((p,e))
        p = 3 if p==2 else p+2
    if n>1: parts.append((n,1))
    return tuple(parts)

@lru_cache(None)
def divisors_from_s(s):
    ds=[1]
    for p,e in factor(s): ds=[v*p**i for v in ds for i in range(e+1)]
    return tuple(sorted(ds))

@lru_cache(None)
def D(x):
    a,b=x.numerator,x.denominator
    s=1
    for p,e in factor(a): s*=p**(e//2)
    return tuple(d for d in divisors_from_s(s) if d>=2 and (d-1)%b==0)

def state(x):
    ds=D(x); assert ds, ('unrealised input',x)
    g=0; L=1
    for d in ds: g=gcd(g,d-1); L=lcm(L,d)
    assert gcd(L,g)==1 and x.denominator and g%x.denominator==0
    return ds,g,L,F(L*L,g)

def C(x): return x+state(x)[3]

def plateau_hit(x):
    """First k>=1 with y+k L^2=0 mod 4g, if L stayed fixed.
       Meaningful for g>1, independent of actual orbit changes.
    """
    ds,g,L,_=state(x); assert g>1
    y=g*x; assert y.denominator==1
    y=int(y)
    if L%2:
        mod=4*g
        assert gcd(L*L,mod)==1
        k=(-y*pow(L*L,-1,mod))%mod
        if k==0:k=mod
        return k,mod
    assert g%2==1 and y%4==0
    mod=g
    z=(L//2)**2
    assert gcd(z,mod)==1
    k=(-(y//4)*pow(z,-1,mod))%mod
    if k==0:k=mod
    return k,mod

seeds=sorted(set([F(M*(N+1)**2,N) for N in range(1, (18 if QUICK else 36)+1)
                  for M in range(1, (5 if QUICK else 9)+1)]))
seed_high=[x for x in seeds if state(x)[1]>1]

# L1: reduced collective steps and modular setup
c=0
for x in seeds:
    ds,g,L,delta=state(x)
    assert delta.numerator==L*L and delta.denominator==g
    assert all((d-1)%g==0 for d in ds)
    c+=1
check('L1.1',c==len(seeds),f'{c} realised exact-rational seeds: Delta=L^2/G in lowest terms; gcd(L,G)=1')

# L2: the exact first forced entry to G=1 assuming no fibre growth
ks=[]; fail=0; odd=even=0
for x in seed_high:
    _,g,L,_=state(x)
    k,mod=plateau_hit(x)
    ks.append(k)
    if L%2:odd+=1
    else:even+=1
    y=int(g*x)
    if k>mod or k<1 or (y+k*L*L)%(4*g)!=0:fail+=1
    # First solution in the respective congruence class
    if any((y+i*L*L)%(4*g)==0 for i in range(1,k)):fail+=1
    if L%2==0 and (g%2==0 or y%4):fail+=1
check('L2.1',fail==0 and len(ks)>0,
      f'{len(ks)} seeds G>1; minimum positive plateau escape k solves y+kL²=0 (mod 4G); {odd} odd-L, {even} even-L; violations {fail}')

# Theoretical general bound k<=4G for odd L, k<=G for even L
bad=sum(k>(4*state(x)[1] if state(x)[2]%2 else state(x)[1])
        for x,k in zip(seed_high,ks))
check('L2.2',bad==0,f'uniform escape bound <=4G (odd L), <=G (even L), violations {bad}')

# An actual collective orbit cannot retain exactly the original fibre for k steps.
bad=0; mx_step=0
for x0,k in zip(seed_high,ks):
    orig=D(x0); x=x0; witness=False
    for j in range(1,k+1):
        x=C(x)
        if D(x)!=orig:
            witness=True;mx_step=max(mx_step,j);break
    if not witness: bad+=1
check('L2.3',bad==0,f'first fibre-growth by exact plateau bound for {len(seed_high)} seeds; violations {bad}, longest first-growth wait {mx_step}')

# L3: G=2 reduction in <=8 steps (v005 theorem, independent check)
def collapse_steps(x,limit):
    for n in range(limit+1):
        if state(x)[1]==1:return n
        if n<limit:x=C(x)
    return None

for gtarget,limit,tag in [(2,7,'L3.1'),(3,2,'L3.2'),(6,29,'L3.3')]:
    pop=[x for x in seeds if state(x)[1]==gtarget]
    waits=[collapse_steps(x,limit) for x in pop]
    check(tag,len(pop)>0 and all(k is not None for k in waits),
          f'G={gtarget} seeds {len(pop)}; all G=1 within <= {limit} steps; max tested {max((k or 0) for k in waits) if waits else None}')

# L3 residue theorem for G=3,6, irrespective of fibre growth while G fixed
bad3=bad6=n3=n6=0
for x in seeds:
    xx=x
    for j in range(45):
        ds,g,L,delta=state(xx)
        if g==3:
            n3+=1
            y=3*xx
            if L%2 or y.denominator!=1 or y.numerator%4 or (((L//2)**2)%3)!=1:bad3+=1
        if g==6:
            n6+=1
            y=6*xx
            if L%2==0 or y.denominator!=1 or (L*L)%24!=1:bad6+=1
        if g==1:break
        xx+=delta
check('L3.4',bad3==0 and n3>0,f'G=3: L even, 3x divisible by 4, (L/2)^2=1 mod 3; {n3} states, {bad3} violations')
check('L3.5',bad6==0 and n6>0,f'G=6: L odd, L²=1 mod 24; {n6} states, {bad6} violations')

# L4: G-divisibility, monotonic D, and exclusion of persistent G=2/3/6
bad=0; hist=Counter(); trajectories=0; gaps=[]
for x0 in seeds:
    x=x0; prev=D(x); g0=state(x)[1]
    for n in range(40):
        nxt=C(x); curr=D(nxt); g1=state(nxt)[1]
        if not set(prev).issubset(curr) or g0%g1:bad+=1
        hist[g1]+=1
        x,prev,g0=nxt,curr,g1
        if g1==1:break
    trajectories+=1
check('L4.1',bad==0,f'{trajectories} orbits, monotone fibres and G_next|G; {bad} violations')
info('L4.DATA','DATA',f'G among post-step states: {dict(sorted(hist.items()))}')

# L5: eventual G=1 scaling law independently tested using exact s²t factorization
def sq_split(n):
    s=t=1
    for p,e in factor(n):
        s*=p**(e//2)
        if e%2:t*=p
    return s,t

def tau(n):
    out=1
    for _,e in factor(n):out*=e+1
    return out

bad=0; cyc_check=0
for x0 in (F(4),F(12),F(16),F(36),F(52),F(100),F(900),F(1500)):
    x=x0;assert state(x)[1]==1
    for j in range(65):
        s,t=sq_split(x.numerator)
        if t in (1,2,3):
            a,b,c = x,C(x),C(C(x)); d=C(c)
            ss,tt=sq_split(x.numerator)
            odd=ss
            while odd%2==0:odd//=2
            if d!=4*x or (state(a)[1]!=1):bad+=1
            if len(D(d))-len(D(x))!=tau(odd):bad+=1
            if [state(z)[1] for z in (a,b,c,d)] != [1]*4:bad+=1
            if [z/state(z)[3] for z in (a,b,c)] != [t, 1+(t%3), 1+((t+1)%3)]:bad+=1
            cyc_check+=1
        x=C(x)
check('L5.1',bad==0 and cyc_check>0,
      f'G=1, t-cycle: x_(n+3)=4x_n; R increment tau(odd(s)); gamma cycle up to rotation; {cyc_check} checks, violations {bad}')

# L6: zero density only established in G=1 regime. Numerically exact reach-count formula
bad=0
for s0 in (2,4,6,10,12,18,30,70,90):
    odd=s0
    while odd%2==0: odd//=2
    for X in (4,10,31,100,1000):
        bound={d*2**k for k in range(X.bit_length()+1) for d in divisors_from_s(odd)
               if d*2**k>=2 and d*2**k<=X}
        count=0
        for q in divisors_from_s(odd):
            if X>=q:count+= (X//q).bit_length()
        count-=1  # exclude d=1
        if len(bound)!=count:bad+=1
check('L6.1',bad==0,'for G=1 eventual reach set {d|odd(s)*2^k}; exact counting formula verified on 45 cases')

# Important scope labels: these are OPEN and aren't registered as successful tests.
info('L7.OPEN1','OPEN','Does every orbit reach G=1? Excluded permanent G=2,3,6; other G>1 unproved.')
info('L7.OPEN2','OPEN','Can a strict global collapse-time bound depend only on initial G? Unknown; fibre growth may alter L.')
info('L7.OPEN3','OPEN','Do persistent G>1 orbits, if any, have density-zero reach sets? Not established by T33.')

os.makedirs('output',exist_ok=True)
with open('output/field6_report.json','w',encoding='utf-8') as f:
    json.dump(dict(version='v006',failed=failures,rows=results),f,indent=2)
print(f'\nSUMMARY {sum(r["status"]=="PASS" for r in results)} PASS, {sum(r["status"]=="DATA" for r in results)} DATA, {sum(r["status"]=="OPEN" for r in results)} OPEN, {failures} FAIL')
print('ALL PASS' if failures==0 else 'SOME FAIL')
sys.exit(1 if failures else 0)
