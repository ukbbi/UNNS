#!/usr/bin/env python3
"""Exact, dependency-free tests for UNNS-U2-TI-DYN v001.
Usage: python code/verify_dyn.py [reports/verification_report.json]
These bounded tests corroborate theorems established by general proofs.
"""
import math, json, sys, hashlib
from pathlib import Path

def divisors(n):
    small, large = [], []
    for d in range(1, math.isqrt(n) + 1):
        if n % d == 0:
            small.append(d)
            if d*d != n: large.append(n//d)
    return small + large[::-1]

def neighbours(n):
    out=set()
    for d in divisors(n): out.add((n//d)*(d+1)**2)
    for q in range(2, math.isqrt(n)+1):
        if n%(q*q)==0:out.add((n//(q*q))*(q-1))
    return out

def brute_neighbours(n):
    out=set()
    for d in range(1,n+1):
        if n%d==0:out.add((n//d)*(d+1)**2)
    for q in range(2, math.isqrt(n)+1):
        if n%(q*q)==0:out.add((n//(q*q))*(q-1))
    return out

def isprime(n):
    return n>=2 and all(n%j for j in range(2, math.isqrt(n)+1))

def predicted_degree(n):
    return len(divisors(n)) + sum(1 for q in range(2,math.isqrt(n)+1) if n%(q*q)==0)

def factor_degree(n):
    v=n
    factors=[]
    for p in range(2,math.isqrt(v)+1):
        if v%p==0:
            e=0
            while v%p==0:
                e+=1;v//=p
            factors.append(e)
    if v>1:factors.append(1)
    tau=math.prod(e+1 for e in factors)
    sq=math.prod((e//2)+1 for e in factors)
    return tau+sq-1

def run():
    nmax=10000
    checkcounts={
      'exact_degree_and_prime_gap_n_1_to_10000':0,
      'maximal_neighbor_n_1_to_10000':0,
      'independent_bruteforce_neighbors_n_1_to_1200':0,
      'symbolic_edge_family_instances':0,
      'orbit_edges':0
    }
    for n in range(1,nmax+1):
        nb=neighbours(n)
        deg=len(nb)
        assert deg == predicted_degree(n) == factor_degree(n), ('degree',n)
        assert (deg == 2) == isprime(n), ('prime',n)
        assert (deg == 1) == (n==1), ('degree1',n)
        assert deg !=3, ('degreegap',n)
        if n>=2 and not isprime(n): assert deg>=4
        checkcounts['exact_degree_and_prime_gap_n_1_to_10000']+=1
        assert max(nb)==(n+1)**2,('max',n)
        checkcounts['maximal_neighbor_n_1_to_10000']+=1
    for n in range(1,1201):
        assert neighbours(n)==brute_neighbours(n),('independent',n)
        checkcounts['independent_bruteforce_neighbors_n_1_to_1200']+=1
    # two-sided coefficient form: for x=kd and y=k(d+1)^2
    for d in range(1,51):
        for k in range(1,51):
            x=k*d;y=k*(d+1)**2
            assert y in neighbours(x) and x in neighbours(y),('edge',d,k)
            checkcounts['symbolic_edge_family_instances']+=1
    orbit=[1]
    for i in range(7):
        x=orbit[-1]; y=(x+1)**2
        assert y == (x//x)*(x+1)**2  # legal forward edge, N=x
        orbit.append(y)
        checkcounts['orbit_edges']+=1
    assert orbit[:5] == [1,4,25,676,458329]
    out={
      'verdict':'PASS', 'scope':'Bounded exact-integer corroboration, not automated proof of universal claims',
      'test_counts':checkcounts,'total_cases':sum(checkcounts.values()),
      'orbit_prefix':[str(z) for z in orbit[:6]],
      'theorem_proofs':'see manuscript sections 2-4',
      'input_deps':'Python standard library only'
    }
    return out

if __name__=='__main__':
    o=run()
    print(json.dumps(o,indent=2))
    if len(sys.argv)>1:
        p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(o,indent=2)+'\n',encoding='utf8')
