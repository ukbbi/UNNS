"""FUG-I Phase 2 independent audit, Python standard library only.

A. Independent square-divisor brute-force predecessor oracle for EVERY
   reverse-reachable state of Fibonacci targets F1..F60.
B. Independent memoized route-count DP for F1..F84 (not path enumeration).
C. Exact edge checks, MR prime certificates, Fibonacci inclusion and scaling.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from math import gcd,isqrt
from pathlib import Path
import csv,json
from arith import incoming,factors,is_prime,step,fib

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'results'
F=fib(84)
index=defaultdict(list)
for i in range(1,85):index[F[i]].append(i)


def brute_pred(y):
    out=[]
    for d in range(2,isqrt(y)+1):
        if y%(d*d)==0:
            out.append((y//(d*d)*(d-1),d-1,d))
    return tuple(sorted(out))


@lru_cache(None)
def reverse_nodes(y):
    s={y}
    for x,N,d in incoming(y):
        s.update(reverse_nodes(x))
    return frozenset(s)


@lru_cache(None)
def dp(y):
    # Count each source-index and path length, never construct all label words.
    result=Counter({(i,0):1 for i in index.get(y,())})
    for x,N,d in incoming(y):
        for (i,k),count in dp(x).items():
            result[i,k+1]+=count
    return result


@lru_cache(None)
def depth_hist(y):
    h=Counter({0:1})
    for x,N,d in incoming(y):
        for k,c in depth_hist(x).items():h[k+1]+=c
    return h


def main():
    summary=json.loads((OUT/'summary.json').read_text(encoding='utf-8'))
    assert summary['limit']==84
    # Each recorded labelled path must be a legal path with the indicated endpoints.
    routes=list(csv.DictReader((OUT/'fib_routes_all_84.csv').open(encoding='utf-8',newline='')))
    actual=Counter()
    for row in routes:
        i=int(row['i']);j=int(row['j']);length=int(row['length'])
        states=list(map(int,row['states'].split(';')))
        labels=list(map(int,row['labels'].split(';')))
        assert len(labels)==length and len(states)==length+1
        assert states[0]==F[i] and states[-1]==F[j] and i<j
        for x,N,y in zip(states,labels,states[1:]):
            assert N>0 and x%N==0 and step(x,N)==y
            # independent reduced-fraction edge signature
            g=gcd(x,y)
            assert x//g==N and y//g==(N+1)**2
        actual[(i,j,length)]+=1
    assert len(routes)==8
    assert len(set((r['i'],r['j'],r['labels']) for r in routes))==8
    # Independent DP exhausts *all depths*, not just depth<=3.
    expected=Counter()
    for j in range(1,85):
        for (i,k),count in dp(F[j]).items():
            if i<j and k>0:
                expected[(i,j,k)]+=count
    assert expected==actual, f'Extra or missing paths: {expected-actual}; {actual-expected}'
    assert len({(i,j) for i,j,k in expected})==4
    assert sum(expected.values())==8
    # Exact non-target ancestry profiles. Includes all length-zero paths.
    rows=list(csv.DictReader((OUT/'fib_ancestry_84.csv').open(encoding='utf-8',newline='')))
    assert len(rows)==84
    for row in rows:
        j=int(row['j']);y=F[j]
        assert int(row['F_j'])==y
        assert int(row['one_step'])==len(incoming(y))
        assert int(row['distinct_ancestor_nodes'])==len(reverse_nodes(y))-1
        hist=depth_hist(y)
        assert int(row['ancestry_height'])==max(hist)
        assert int(row['total_nonempty_ancestral_routes'])==sum(hist.values())-1
        asserted=json.loads(row['route_counts_by_length'])
        assert asserted=={str(k):v for k,v in sorted(hist.items()) if k>0}
        roots={r for r in reverse_nodes(y) if len(incoming(r))==0}
        assert len(roots)==int(row['terminal_squarefree_roots'])
        assert ';'.join(map(str,sorted(roots)))==row['roots']
        # Every terminal root is squarefree: no square divisor d>=2.
        assert all(all(e==1 for p,e in factors(r)) or r==1 for r in roots)
    # Independent brute force checks on the complete reverse closure for F1..F60.
    oracle_nodes=set()
    for j in range(1,61):oracle_nodes.update(reverse_nodes(F[j]))
    for y in sorted(oracle_nodes):
        assert brute_pred(y)==incoming(y),f'Brute oracle mismatch at {y}'
    # Check every prime factor emitted by the factorization module.
    all_nodes=set()
    for j in range(1,85):all_nodes.update(reverse_nodes(F[j]))
    for y in all_nodes:
        prod=1
        for p,e in factors(y):
            assert is_prime(p)
            prod*=p**e
        assert prod==y
    # New scaling and index-divisibility height law.
    for m in range(1,85):
        for n in range(m,85,m):
            B=F[n]//F[m]
            assert B*F[m]==F[n]
            hm=depth_hist(F[m]);hn=depth_hist(F[n])
            for k,c in hm.items():
                assert c<=hn.get(k,0),(m,n,k,c,hn.get(k,0))
            for x,N,d in incoming(F[m]):
                assert step(B*x,N)==F[n]
    assert max(max(depth_hist(F[j])) for j in range(1,85))==5
    assert reverse_nodes(F[12]) != reverse_nodes(F[24])
    r12={x for x in reverse_nodes(F[12]) if not incoming(x)}
    r24={x for x in reverse_nodes(F[24]) if not incoming(x)}
    assert r12.isdisjoint(r24)
    print('PASS: all 8 recorded routes checked by exact edge/gcd identities')
    print('PASS: independent all-depth counting DP agrees on 4 pairs and 8 routes')
    print('PASS: all 84 ancestry profiles match independent route counts')
    print('PASS: full naive square-divisor oracle on',len(oracle_nodes),'reverse states from F1..F60')
    print('PASS: every visited reverse node has certified <2**64 factorization; count',len(all_nodes))
    print('PASS: index-divisibility monotonicity at every depth (m|n), all pairs <=84')
    print('PASS: F12 vs F24 terminal-root sets are disjoint, though F12 divides F24')
    print('FUG-I v002 VERIFY PASS')

if __name__=='__main__':main()
