#!/usr/bin/env python3
"""FUG-I v001. Exact Fibonacci-UNNS overlay: standard library only.

Output lives in ../results (relative to this file), not in a system-dependent CWD.
The fixed substrate and the selected SELECT-II self-substitution are distinguished.
"""
import csv
import json
from collections import defaultdict
from functools import lru_cache
from math import gcd, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
LIMIT = 48


def primes_through(upper):
    sieve = bytearray(b"\x01") * (upper+1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(upper)+1):
        if sieve[p]:
            sieve[p*p: upper+1:p] = b"\x00" * (((upper-p*p)//p)+1)
    return tuple(p for p in range(2,upper+1) if sieve[p])


PRIMES = primes_through(400000)


@lru_cache(maxsize=None)
def factor(n):
    assert isinstance(n,int) and n>=1
    val=n
    ret=[]
    for p in PRIMES:
        if p*p>val: break
        if val%p==0:
            e=0
            while val%p==0:
                val//=p;e+=1
            ret.append((p,e))
    if val>1:
        # This path is exact for n <= 10**11 used by the v001 run,
        # since our prime table reaches 400000 > sqrt(10**11).
        assert n<=10**11, "Increase prime table for larger values before running"
        ret.append((val,1))
    return tuple(ret)


@lru_cache(maxsize=None)
def divisors(n):
    div=[1]
    for p,e in factor(n):
        div=[d*p**a for d in div for a in range(e+1)]
    return tuple(sorted(div))


def fibonacci(k):
    out=[0,1]
    while len(out)<=k: out.append(out[-1]+out[-2])
    return out


def lucas(k):
    out=[2,1]
    while len(out)<=k: out.append(out[-1]+out[-2])
    return out


def square_divisor_coordinates(x):
    q=1
    for p,e in factor(x): q *= p**(e//2)
    return tuple(d for d in divisors(q) if d>1),q


def successor(x,N):
    assert N>0 and x%N==0
    return x//N*(N+1)**2


def predecessors(y):
    # All incoming integer-anchor predecessors of y, with edge labels.
    ds,_=square_divisor_coordinates(y)
    return tuple((y//(d*d)*(d-1),d-1) for d in ds)


def get_paths(values,limit=LIMIT,max_depth=3):
    """Return *all* 1-, 2-, 3-edge forward routes between indexed observations.

    For all j<=limit, y=values[j], only possible paths stay <=y because T_N>=4.
    Enumerates two forward steps and joins against exact one-step predecessor
    fibres; complete for length<=3 by the monotonicity theorem.
    """
    assert max_depth==3
    val_to_indices=defaultdict(list)
    for j in range(1,limit+1): val_to_indices[values[j]].append(j)
    pred_to_target=defaultdict(list)
    for j in range(1,limit+1):
        for z,N in predecessors(values[j]):
            pred_to_target[z].append((j,N))

    cap=max(values[1:limit+1])
    records=[]
    for i in range(1,limit+1):
        x=values[i]
        for n1 in divisors(x):
            y=successor(x,n1)
            if y>cap: continue
            for j in val_to_indices.get(y,()):
                if j>i:
                    records.append(dict(i=i,j=j,length=1,labels=(n1,),states=(x,y)))
            for j,n2 in pred_to_target.get(y,()):
                if j>i:
                    records.append(dict(i=i,j=j,length=2,labels=(n1,n2),states=(x,y,values[j])))
            for n2 in divisors(y):
                z=successor(y,n2)
                if z>cap:continue
                for j,n3 in pred_to_target.get(z,()):
                    if j>i:
                        records.append(dict(i=i,j=j,length=3,labels=(n1,n2,n3),states=(x,y,z,values[j])))
    records.sort(key=lambda a:(a['length'],a['i'],a['j'],a['labels']))
    # Every route is generative and exact; confirm no duplicate route encoding.
    keys={(p['i'],p['j'],p['labels']) for p in records}
    assert len(keys)==len(records)
    for p in records:
        assert p['states'][0]==values[p['i']] and p['states'][-1]==values[p['j']]
        for x,N,y in zip(p['states'],p['labels'],p['states'][1:]):
            assert y==successor(x,N)
    return records


def write_csv(path,rows,fieldnames):
    with path.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader();writer.writerows(rows)




def analyze(values,limit=LIMIT):
    paths=get_paths(values,limit)
    by_length={str(k):sum(1 for p in paths if p['length']==k) for k in (1,2,3)}
    pairs={str(k):len({(p['i'],p['j']) for p in paths if p['length']==k}) for k in (1,2,3)}
    # Distinct endpoint pairs accessible in at most three steps.
    min_dist={}
    for p in paths:
        min_dist.setdefault((p['i'],p['j']),p['length'])
    return paths,{'routes_exact_length':by_length,'pairs_exact_length':pairs,
                  'pairs_min_distance':{str(k):sum(v==k for v in min_dist.values()) for k in (1,2,3)},
                  'reachable_pairs_le3':len(min_dist)}


def run(limit=LIMIT):
    if limit!=48:
        raise ValueError('v001 is frozen at 48 Fibonacci indices; use v002 for a larger window')
    RESULTS.mkdir(parents=True,exist_ok=True)
    F=fibonacci(limit)
    layers=[]
    incidence=[]
    layer_coords={}
    for n in range(1,limit+1):
        x=F[n]
        ds,q=square_divisor_coordinates(x)
        layer_coords[n]=set(ds)
        layers.append(dict(n=n,F=x,prime_factors=' * '.join(f'{p}^{e}' for p,e in factor(x)) or '1',
                           q=q,R=len(ds),d_coordinates=';'.join(str(d) for d in ds),
                           forward_labels=len(divisors(x))))
        for d in ds:
            M=x//(d*d)*(d-1)
            assert M>0 and successor(M,d-1)==x
            incidence.append(dict(n=n,F=x,d=d,N=d-1,M=M))
    write_csv(RESULTS/'fib_layers_48.csv',layers,
              ['n','F','prime_factors','q','R','d_coordinates','forward_labels'])
    write_csv(RESULTS/'fib_incidence_48.csv',incidence,['n','F','d','N','M'])
    assert sum(x['R'] for x in layers)==len(incidence)
    for m in range(1,limit+1):
        for n in range(1,limit+1):
            assert layer_coords[m]&layer_coords[n]==layer_coords[gcd(m,n)]
            if n%m==0:
                assert layer_coords[m]<=layer_coords[n]
                for d in layer_coords[m]:
                    M=F[m]//d**2*(d-1)
                    M2=F[n]//F[m]*M
                    assert successor(M2,d-1)==F[n]
    paths,counts=analyze(F,limit)
    write_csv(RESULTS/'fib_paths_le3_48.csv',[
        dict(i=p['i'],j=p['j'],F_i=p['states'][0],F_j=p['states'][-1],length=p['length'],
             labels=';'.join(map(str,p['labels'])),states=';'.join(map(str,p['states'])))
        for p in paths],['i','j','F_i','F_j','length','labels','states'])
    # Exact benchmark conditions, including count of distinct routes vs distinct pairs.
    assert counts['routes_exact_length']=={'1':1,'2':4,'3':3},counts
    assert counts['pairs_exact_length']=={'1':1,'2':2,'3':1},counts
    assert counts['pairs_min_distance']=={'1':1,'2':2,'3':1},counts
    assert len(paths)==8
    assert all(p['j']-p['i']>=3 for p in paths)
    targets=[(p['i'],p['j'],p['length']) for p in paths]
    assert (3,6,1) in targets
    assert {(5,12,2),(6,12,2),(3,12,3)}.issubset(targets)

    # A finite, declared arithmetic discrimination control, not a null p-value.
    L=lucas(limit)
    P=[v+1 for v in F]
    controls={}
    for name,seq in [('Lucas',L),('Fibonacci_plus_1',P)]:
        records,stats=analyze(seq,limit)
        controls[name]={**stats,'paths_le3':[
             dict(i=p['i'],j=p['j'],length=p['length'],labels=list(p['labels']),states=list(p['states']))
             for p in records]}
    (RESULTS/'controls_48.json').write_text(json.dumps(controls,indent=2)+'\n',encoding='utf-8')
    result={'release':'FUG-I_v001','mode':'exact','limit':limit,'fibonacci_F1':F[1],
            'fibonacci_F48':F[48],'nonempty_incidence_layers':sum(r['R']>0 for r in layers),
            'total_occurrence_points':len(incidence),
            'index_pair_meet_checks':limit*limit,
            'paths':counts,
            'all_fibonacci_paths_le3':[
              dict(i=p['i'],j=p['j'],length=p['length'],labels=list(p['labels']),states=list(p['states']))
              for p in paths],
            'controls':{k:{kk:vv for kk,vv in s.items() if kk!='paths_le3'} for k,s in controls.items()}}
    (RESULTS/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('FUG-I v001 exact run PASS')
    print('Indexed Fibonacci observations:',limit,' occurrence points:',len(incidence))
    print('Directed routes (length 1,2,3):',counts['routes_exact_length'])
    print('Distinct endpoint pairs (minimum distances 1,2,3):',counts['pairs_min_distance'])
    print('No actual recurrence-adjacent T_N transition; all paths have index gap >=3')
    print('Output:',RESULTS)
    return result


if __name__=='__main__':
    run()
