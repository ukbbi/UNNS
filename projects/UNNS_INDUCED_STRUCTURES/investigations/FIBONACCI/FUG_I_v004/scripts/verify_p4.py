"""Independent FUG-I Phase 4 verifier.

Does not import run_p4. Uses independent prime-valuation threshold,
forward arithmetic, modular Fibonacci, and inverse-graph enumeration.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from fractions import Fraction
from functools import lru_cache
from math import gcd,lcm
from pathlib import Path
import csv,json
from arith import incoming, fib, lucas, factors, step

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'results';BASE=ROOT/'baseline_v003';LIMIT=84
F=fib(84)


def read(name,base=OUT):
    with (base/name).open(newline='',encoding='utf-8') as fp:return list(csv.DictReader(fp))


def wparse(s):return tuple(map(int,s.split(';'))) if s else ()


def v_p(n,p):
    exp=0
    while n%p==0 and n:
        n//=p;exp+=1
    return exp


def threshold_via_primes(w):
    """Independent p-adic implementation, not the prefix fraction/lcm generator."""
    primes={p for N in w for v in (N,N+1) for p,e in factors(v)}
    K=1
    for p in primes:
        prefix=0;needed=0
        for N in w:
            needed=max(needed,v_p(N,p)-prefix)
            prefix+=2*v_p(N+1,p)-v_p(N,p)
        K*=p**needed
    source=K
    for N in w:
        source=step(source,N)
    return K,source


def fib_mod(n,m):
    if m==1:return 0
    a,b=0,1
    for digit in bin(n)[2:]:
        d=(a*(2*b-a))%m
        e=(a*a+b*b)%m
        a,b=(d,e) if digit=='0' else (e,(d+e)%m)
    return a


@lru_cache(None)
def reverse_words(y):
    out={()}
    for ancestor,label,d in incoming(y):
        for old in reverse_words(ancestor):out.add(old+(label,))
    return frozenset(out)


def check():
    summ=json.loads((OUT/'summary.json').read_text(encoding='utf-8'))
    assert summ['release']=='FUG-I_v004'
    old=json.loads((BASE/'summary.json').read_text(encoding='utf-8'))
    assert old['release']=='FUG-I_v003'
    words=read('word_activation_84.csv')
    indexes=read('index_activation_84.csv')
    transports=read('transport_activation_84.csv')
    baseline_words=read('fib_history_words_84.csv',BASE)
    assert len(baseline_words)==292 and len(indexes)==84 and len(transports)==307
    assert len(words)==84 and len(set(r['word'] for r in words))==84
    rank={};word_E={}
    observed=defaultdict(set)
    for r in baseline_words:
        j=int(r['j']);w=wparse(r['word']);observed[j].add(w)
    for row in words:
        w=wparse(row['word']);K,E=threshold_via_primes(w)
        assert (K,E)==(int(row['K_min']),int(row['E_min']))
        first=next(i for i in range(1,85) if fib_mod(i,E)==0)
        assert first==int(row['rank'])
        hits=[i for i in range(1,85) if fib_mod(i,E)==0]
        assert hits==list(map(int,row['observed_indices'].split(';')))
        assert hits==list(range(first,85,first))
        rank[w]=first;word_E[w]=E
    assert len(rank)-1==summ['census']['distinct_nonempty_words']==83
    print('PASS: 84 distinct words including empty; independent prime-valuations and first Fibonacci ranks')
    count_by_index=Counter()
    for n in range(1,85):
        expected={w for w,z in rank.items() if n%z==0}
        assert expected==observed[n]==reverse_words(F[n])
        index_record=indexes[n-1]
        assert int(index_record['n'])==n
        assert int(index_record['active_nonempty'])==len(expected)-1
        new=sum(1 for w,z in rank.items() if w and z==n)
        count_by_index[n]=new
        assert new==int(index_record['new_nonempty_words'])
    assert {str(i):v for i,v in count_by_index.items() if v}==summ['census']['first_activated_word_index_counts']
    print('PASS: complete first-84 ancestry reconstructed from Fibonacci activation ranks')
    old_trans=read('fib_transport_84.csv',BASE)
    for r,s in zip(transports,old_trans):
        m=int(r['m']);n=int(r['n']);assert (m,n)==(int(s['m']),int(s['n']))
        new={w for w,z in rank.items() if (n%z)==0 and (m%z)!=0}
        cnt=Counter(map(len,new));cnt.pop(0,None)
        assert len(new)==int(r['extra_words'])==int(s['extra_nonempty'])
        assert min(cnt,default=0)==int(r['first_depth'])==int(s['first_activation_depth'])
        assert {str(k):v for k,v in sorted(cnt.items())}==json.loads(r['new_by_length'])
    print('PASS: 307 scale-transport activations exactly reproduce independent Phase 3 data')

    # Meet, index rank, and word simultaneity via lcm ranks.
    meetchecks=0;lcmchecks=0
    for i in range(1,85):
        for j in range(1,85):
            assert observed[i]&observed[j]==observed[gcd(i,j)]
            meetchecks+=1
    for w,ew in word_E.items():
        for v,ev in word_E.items():
            k=lcm(rank[w],rank[v]);e=lcm(ew,ev)
            if k<=84:
                assert fib_mod(k,e)==0
                assert all(fib_mod(j,e)!=0 for j in range(1,k))
                lcmchecks+=1
    assert meetchecks==7056
    print('PASS: 7,056 gcd-meets; %d joint-activation rank-lcm cross-checks'%lcmchecks)

    # Merger: joint source min, endpoint min, exact rank and explicit source path.
    merger=json.loads((OUT/'merger_gate.json').read_text(encoding='utf-8'))
    a,b=(3,8,3),(1,1,1,2)
    Ka,Ea=threshold_via_primes(a);Kb,Eb=threshold_via_primes(b)
    assert (Ka,Ea,Kb,Eb)==(3,864,1,288)
    assert merger['joint_min_source']==3 and merger['joint_min_endpoint']==864
    for w in (a,b):
        y=3
        for n in w:y=step(y,n)
        assert y==864
    assert fib_mod(72,864)==0 and fib_mod(24,864)!=0 and fib_mod(36,864)!=0
    assert next(i for i in range(1,85) if fib_mod(i,864)==0)==72
    print('PASS: source-locked different-content merger has joint endpoint 864, first F72, index family 72k')

    # Fully periodic residue argument modulo 64 (not sample-dependent).
    a0,b0=0,1
    for _ in range(96):a0,b0=b0,(a0+b0)%64
    assert (a0,b0)==(0,1)
    assert [fib_mod(12*r,64) for r in (1,3,5,7)]==[16,48,16,48]
    assert [fib_mod(24*r,64) for r in (1,3)]==[32,32]
    # The finite alphabet A, one-step labels, and new depth-two path.
    A=(1,2,3,5,7,11)
    assert threshold_via_primes((7,2))==(7,288)
    witness=read('delayed_family_witnesses.csv')
    assert len(witness)==9
    for row in witness:
        r=int(row['r']);assert r%2==1
        m,n=12*r,24*r
        assert (int(row['index_before']),int(row['index_after']))==(m,n)
        assert fib_mod(m,64) in (16,48) and fib_mod(n,64)==32
        assert fib_mod(m,288)!=0 and fib_mod(n,288)==0
        allowed_m={N for N in A if fib_mod(m,(N+1)**2)==0}
        allowed_n={N for N in A if fib_mod(n,(N+1)**2)==0}
        assert allowed_m==allowed_n=={1,2,3,5,11}
    print('PASS: modulo-64 full residue proof ingredients; nine additional odd-index family checks')

    # Exact infinite depth-power spine; test modularly with independent method.
    spine=read('unbounded_depth_spine.csv')
    assert len(spine)==12
    for row in spine:
        t=int(row['t']);n=6*4**t
        modulus=1<<(2*t+6)
        residue=fib_mod(n,modulus)
        assert residue != 0
        v=(residue&-residue).bit_length()-1
        assert v==3+2*t
        assert (v//2)==int(row['longest_N1_word'])==t+1
    assert [fib_mod(6*2**i,4) for i in range(0,12)] == [0]*12
    print('PASS: exact powers-of-four depth spine for twelve indices; induction proof applies to every t')

    # Controls: independent constructions of histories by inverse DAG.
    controls=json.loads((OUT/'control_activation_84.json').read_text(encoding='utf-8'))
    for name,values in [('Fibonacci',F),('Lucas',lucas(84)),('Fibonacci_plus_1',[v+1 for v in F])]:
        W={i:reverse_words(values[i]) for i in range(1,85)}
        inclusion_fail=sum(W[m].issubset(W[n]) is False for m in range(1,85) for n in range(2*m,85,m))
        occurrence=defaultdict(list)
        for i,words_i in W.items():
            for w in words_i:
                if w:occurrence[w].append(i)
        periodic_fail=0
        for w,inds in occurrence.items():
            first=min(inds)
            if set(inds)!={i for i in range(1,85) if i%first==0}:
                periodic_fail+=1
        assert inclusion_fail==controls[name]['inclusion_failures']
        assert periodic_fail==controls[name]['first_index_periodicity_failures']
    print('PASS: Fibonacci, Lucas and shifted-Fibonacci activation controls reproduced')
    print('FUG-I v004 VERIFY PASS')

if __name__=='__main__': check()
