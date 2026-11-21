"""FUG-I v005 independent verification of the local output package.

The full finite transport census is reproduced by explicitly enumerating all
incoming histories, independently of run_p5's recursive pair-depth algorithm.
The Lucas factor certificates use elementary trial division (not Pollard rho).
"""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from fractions import Fraction
from math import isqrt, gcd
from collections import Counter
import csv
import json
from arith import incoming, fib, step

ROOT=Path(__file__).resolve().parent.parent
RESULTS=ROOT/'results'
BASE=ROOT/'baseline_v004'


def rows(path):
    with path.open(encoding='utf-8',newline='') as fp:
        return list(csv.DictReader(fp))


@lru_cache(None)
def independent_wordset(y):
    # Inverse-state enumeration, *not* run_p5 paired-depth recursion.
    z={()}
    for x,N,d in incoming(y):
        for prior in independent_wordset(x):
            z.add(prior+(N,))
    return frozenset(z)


def is_prime_trial(x):
    if x<2:return False
    if x%2==0:return x==2
    d=3
    while d*d<=x:
        if x%d==0:return False
        d+=2
    return True


def lucas_exact(n):
    a,b=2,1
    if n==0:return 2
    for _ in range(1,n):a,b=b,a+b
    return b


def fib_mod(n,m):
    a,b=0,1
    for bit in bin(n)[2:]:
        c=(a*(2*b-a))%m
        d=(a*a+b*b)%m
        if bit=='0':a,b=c,d
        else:a,b=d,(c+d)%m
    return a


def lucas_mod(n,m):
    return (2*fib_mod(n+1,m)-fib_mod(n,m))%m


def q_naive(x):
    # Not used on large Fibonacci targets: small-control independent oracle.
    q=1
    p=2
    while p*p<=x:
        e=0
        while x%p==0:
            x//=p;e+=1
        q*=p**(e//2)
        p+=1 if p==2 else 2
    return q


def main():
    summary=json.loads((RESULTS/'summary.json').read_text(encoding='utf-8'))
    assert summary['release']=='FUG-I_v005'
    original=json.loads((BASE/'summary.json').read_text(encoding='utf-8'))
    assert original['census']['transport_pairs']==307
    full=rows(RESULTS/'all_label_pairs_84.csv')
    assert len(full)==307
    F=fib(84)
    cls=Counter()
    for row in full:
        m,n=int(row['m']),int(row['n'])
        wa=independent_wordset(F[m]); wb=independent_wordset(F[n])
        assert wa<=wb
        extra=wb-wa
        depth=min(map(len,extra)) if extra else 0
        assert depth==int(row['depth'])
        assert len(extra)==int(row['extra_words'])
        assert len([w for w in wa if len(w)==1])==int(row['R_m'])
        assert len([w for w in wb if len(w)==1])==int(row['R_n'])
        assert (len([w for w in wa if len(w)==1])==len([w for w in wb if len(w)==1])) == (row['same_immediate']=='True')
        cls[depth]+=1
    assert dict(cls)=={0:193,1:108,2:6}
    print('PASS: 307 unrestricted transports independently reconstructed from full ancestry word sets')

    delayed=rows(RESULTS/'unrestricted_delayed_84.csv')
    assert [(int(v['m']),int(v['n'])) for v in delayed]==[(12,24),(12,36),(12,60),(12,72),(24,72),(36,72)]

    # Independently certify displayed factorizations by recombination and trial-division primality.
    odd=rows(RESULTS/'odd_doubling_certificates.csv')
    assert [int(r['r']) for r in odd]==[1,3,5,7]
    known={
        1:{7:1,23:1},
        3:{7:1,23:1,103681:1},
        5:{7:1,23:1,241:1,2161:1,20641:1},
        7:{7:2,23:1,167:1,14503:1,65740583:1},
    }
    for row in odd:
        r=int(row['r']); n=12*r
        f=known[r]
        assert all(is_prime_trial(p) for p in f)
        P=1
        for p,e in f.items():P*=p**e
        assert P==lucas_exact(n)//2==int(row['lucas_quotient'])
        assert bool(all(e==1 for e in f.values()))==(row['lucas_quotient_squarefree']=='True')
        assert int(row['first_new_depth_full'])==(2 if r!=7 else 1)
        A=F[n] if n<=84 else None
        if A is not None:
            assert A%16==0 and (A//16)%2==1
        assert fib_mod(n,288)!=0 and fib_mod(2*n,288)==0
    assert lucas_mod(84,49)==0 and fib_mod(84,7)!=0 and fib_mod(168,49)==0
    print('PASS: exact squarefree Lucas certificates, odd-r full-label depth gate and first r=7 obstruction')

    # Check infinitely many-family witness rows through independent fast doubling.
    infinity=rows(RESULTS/'infinite_depth1_witnesses.csv')
    assert len(infinity)==12
    for rec in infinity:
        s=int(rec['odd_s']);n=84*s
        assert s%2 and lucas_mod(n,49)==0
        assert fib_mod(n,7)!=0 and fib_mod(2*n,49)==0
        assert fib_mod(n,64) in (16,48) and fib_mod(2*n,64)==32
    print('PASS: sampled infinite obstruction family; general odd-index divisibility proof in THEOREMS.md')

    # Basic matched nulls with naive trial-division square kernels.
    matched=rows(RESULTS/'matched_integer_controls.csv')
    assert len(matched)==10
    for rec in matched:
        a=int(rec['base']);b=int(rec['scaled'])
        assert a==144 and b%a==0
        assert q_naive(a)==q_naive(b)==12
        assert b%288==0 and a%288!=0
        wa=independent_wordset(a);wb=independent_wordset(b)
        extra=wb-wa
        assert min(map(len,extra))==2
        assert (7,2) in extra
    print('PASS: ten matched non-Fibonacci unrestricted delayed-activation controls')

    unbounded=rows(RESULTS/'unbounded_merger_family.csv')
    assert len(unbounded)==8
    for rec in unbounded:
        t=int(rec['t']); x=int(rec['common_source']);y=int(rec['common_endpoint'])
        assert x==2**(2*t)*3**(4*t)
        assert y==2**(16*t)*3**(4*t)
        words=[]
        for j in range(t+1):
            word=(1,)*(7*j)+(2,)*(2*(t-j))+(3,)*(4*(t-j))
            s=x
            for N in word:
                assert s%N==0
                s=s//N*(N+1)**2
            assert s==y
            words.append(word)
        assert len(set(tuple(Counter(w).items()) for w in words))==t+1
    print('PASS: arbitrarily many distinct-content mergers (t=1..8 exact certificates)')

    # Independent brute-force inverse-step oracle on smaller integers.
    for y in range(1,1001):
        naive=[]
        for d in range(2,isqrt(y)+1):
            if y%(d*d)==0:
                x=y//(d*d)*(d-1)
                naive.append((x,d-1,d))
        assert set(naive)==set(incoming(y))
    print('PASS: brute-square-divisor inverse oracle on integers 1..1000')
    # Generalized decision cross-check over thousands of a|b pairs beyond Fibonacci.
    from run_p5 import first_new_depth
    tested=0
    for a in range(1,151):
        for b in range(a,751,a):
            extra=independent_wordset(b)-independent_wordset(a)
            oracle=min(map(len,extra)) if extra else None
            assert first_new_depth(a,b)==oracle,(a,b,oracle)
            tested+=1
    print(f'PASS: unrestricted pair-depth recursion independently checked on {tested} general divisible pairs')
    print('FUG-I v005 VERIFY PASS')

if __name__=='__main__':
    main()
