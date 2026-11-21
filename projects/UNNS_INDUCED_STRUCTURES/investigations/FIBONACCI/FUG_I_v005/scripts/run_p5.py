"""FUG-I v005: unrestricted T_N activation, Lucas-squarefreeness gate and history classification.

Only Python 3 standard library. No remote access, no writes to earlier releases.
Finite 84-index census remains in the certified 64-bit factorization regime.
The infinite-family statements are proved separately in theory/THEOREMS.md.
"""
from __future__ import annotations
from collections import Counter
from functools import lru_cache
from pathlib import Path
from fractions import Fraction
from math import gcd, lcm
import csv
import json

from arith import incoming, fib, lucas, factors, step

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT/'baseline_v004'
OUT = ROOT/'results'
LIMIT = 84


def read_csv(name):
    with (BASE/name).open(encoding='utf-8', newline='') as fp:
        return list(csv.DictReader(fp))


def write_csv(name, rows, headers):
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT/name).open('w', encoding='utf-8', newline='') as fp:
        wr = csv.DictWriter(fp, fieldnames=headers)
        wr.writeheader()
        wr.writerows(rows)


def fib_mod(n, modulus):
    """Fast doubling, O(log n), no large Fibonacci integer needed."""
    a, b = 0, 1
    for bit in bin(n)[2:]:
        c = (a * (2*b-a)) % modulus
        d = (a*a+b*b) % modulus
        a,b = (c,d) if bit == '0' else (d,(c+d)%modulus)
    return a


def lucas_mod(n, modulus):
    # L_n = 2*F_(n+1) - F_n
    return (2*fib_mod(n+1,modulus)-fib_mod(n,modulus)) % modulus


def v2(x):
    return (x & -x).bit_length()-1


def square_kernel(y):
    q=1
    for p,e in factors(y):
        q *= p**(e//2)
    return q


@lru_cache(None)
def labels_and_predecessors(y):
    return tuple((N,x) for x,N,_ in incoming(y))


@lru_cache(None)
def first_new_depth(a,b):
    """Exact all-label first depth for a|b (None means no extra word).
    No enumeration of history WORDS; recursion on paired inverse branches.
    """
    assert a>0 and b%a==0
    if a==b:
        return None
    aa=dict(labels_and_predecessors(a)); bb=dict(labels_and_predecessors(b))
    assert set(aa)<=set(bb)
    if set(bb)-set(aa):
        return 1
    result=[]
    for label,old_pre in aa.items():
        new_pre=bb[label]
        assert new_pre%old_pre==0
        child=first_new_depth(old_pre,new_pre)
        if child is not None:
            result.append(1+child)
    return min(result) if result else None


def min_source_and_endpoint(word):
    """Exact prefix divisibility threshold for a finite word."""
    q=Fraction(1)
    K=1
    for N in word:
        K=lcm(K, (q.denominator*N)//gcd(q.numerator, q.denominator*N))
        q *= Fraction((N+1)**2,N)
    assert (K*q).denominator==1
    return K, int(K*q), q


def cert_factor_lucas_odd(r):
    """Full *certified* factorization only for L_(12r)/2 < 2**64."""
    n=12*r
    L=lucas(n)[n]
    assert L%2==0 and (L//2)<2**64
    f=factors(L//2)
    prod=1
    for p,e in f: prod*=p**e
    assert prod==L//2
    return L//2,f, all(e==1 for _,e in f)


def main():
    OUT.mkdir(exist_ok=True,parents=True)
    b=json.loads((BASE/'summary.json').read_text(encoding='utf-8'))
    assert b['release']=='FUG-I_v004' and b['census']['Fibonacci_indices']==84
    data=read_csv('transport_activation_84.csv')
    assert len(data)==307
    F=fib(LIMIT)
    checks=[]
    counts=Counter()
    for row in data:
        m,n=int(row['m']),int(row['n'])
        a,z=F[m],F[n]
        assert z%a==0
        q_a=square_kernel(a)
        q_z=square_kernel(z)
        got=first_new_depth(a,z)
        d=got if got is not None else 0
        expected=int(row['first_depth'])
        assert d==expected,(m,n,d,expected)
        assert (d==1) == (q_a!=q_z)
        counts[d]+=1
        checks.append(dict(m=m,n=n,depth=d,R_m=len(labels_and_predecessors(a)),
                           R_n=len(labels_and_predecessors(z)),
                           same_immediate=(q_a==q_z),extra_words=int(row['extra_words'])))
    assert dict(counts)=={0:193,1:108,2:6}
    write_csv('all_label_pairs_84.csv',checks,['m','n','depth','R_m','R_n','same_immediate','extra_words'])
    delayed=[dict(m=r['m'],n=r['n'],new_depth=r['depth'],
                  labels_before=r['R_m'],labels_after=r['R_n'],new_histories=r['extra_words'])
             for r in checks if r['depth']==2]
    assert len(delayed)==6
    write_csv('unrestricted_delayed_84.csv',delayed,
              ['m','n','new_depth','labels_before','labels_after','new_histories'])

    # Exact odd-r doubling law: F_(24r)=F_(12r)*L_(12r), r odd.
    # Certified examples are limited to moderate r whose Lucas factorization is <2**64.
    odd=[]
    for r in (1,3,5,7):
        n=12*r
        L2,f,sqfree=cert_factor_lucas_odd(r)
        a=fib(n)[n]
        assert v2(a)==4 and lucas_mod(n,4)==2
        assert gcd(a,2*L2)==2
        assert fib_mod(n,288)!=0 and fib_mod(2*n,288)==0
        if r==7:
            assert fib_mod(2*n,49)==0
        got=2 if sqfree else 1
        if 2*n<=LIMIT:
            assert first_new_depth(a,fib(2*n)[2*n])==got
        odd.append(dict(r=r,m=n,n=2*n,lucas_quotient=L2,
                        factorization='*'.join(f'{p}^{e}' for p,e in f),
                        lucas_quotient_squarefree=sqfree,
                        first_new_depth_full=got,
                        new_label_N6=(not sqfree and r==7),
                        new_two_step_word='7;2'))
    write_csv('odd_doubling_certificates.csv',odd,
              ['r','m','n','lucas_quotient','factorization','lucas_quotient_squarefree',
               'first_new_depth_full','new_label_N6','new_two_step_word'])

    # Infinite obstruction (proof by odd-index Lucas divisibility + Fibonacci mod 7).
    infinite=[]
    assert lucas_mod(84,49)==0 and fib_mod(84,7)!=0
    for s in (1,3,5,7,9,11,13,15,17,19,21,23):
        m=84*s
        assert lucas_mod(m,49)==0
        assert fib_mod(m,7)!=0
        assert fib_mod(2*m,49)==0
        assert fib_mod(m,64) in (16,48)
        assert fib_mod(2*m,64)==32
        infinite.append(dict(odd_s=s,earlier_index=m,later_index=2*m,
                             F_earlier_mod7=fib_mod(m,7),Lucas_earlier_mod49=0,
                             F_later_mod49=0,activated_label=6,first_depth=1))
    write_csv('infinite_depth1_witnesses.csv',infinite,
              ['odd_s','earlier_index','later_index','F_earlier_mod7',
               'Lucas_earlier_mod49','F_later_mod49','activated_label','first_depth'])

    # Matched unrestricted delayed-activation controls, with fixed base a=144.
    # B=288*p where p>=5 prime; q(a)==q(B)==12; E(7,2)=288.
    matched=[]
    assert min_source_and_endpoint((7,2))[:2]==(7,288)
    for p in (5,7,11,13,17,19,23,29,31,37):
        a=144;z=288*p
        assert square_kernel(a)==square_kernel(z)==12
        got=first_new_depth(a,z)
        assert got==2
        matched.append(dict(base=a,scaled=z,multiplier=2*p,
                            same_immediate_labels=True,first_depth=2,
                            new_word='7;2',new_word_endpoint=288))
    write_csv('matched_integer_controls.csv',matched,
              ['base','scaled','multiplier','same_immediate_labels','first_depth',
               'new_word','new_word_endpoint'])

    # Unbounded distinct-CONTENT history mergers at Fibonacci targets.
    # r_1^7 = r_2^2 * r_3^4 = 4^7.
    content=[]
    for t in range(1,9):
        common_source=2**(2*t)*3**(4*t)
        endpoint=common_source*4**(7*t)
        assert endpoint==2**(16*t)*3**(4*t)
        words=[]
        for j in range(t+1):
            w=(1,)*(7*j)+(2,)*(2*(t-j))+(3,)*(4*(t-j))
            state=common_source
            for N in w: state=step(state,N)
            assert state==endpoint
            words.append(w)
        assert len(set(words))==t+1
        content.append(dict(t=t,common_source=common_source,
                            common_endpoint=endpoint,
                            distinct_content_classes=t+1,
                            word_examples=' | '.join(';'.join(map(str,w)) for w in (words[0],words[-1]))))
    write_csv('unbounded_merger_family.csv',content,
              ['t','common_source','common_endpoint','distinct_content_classes','word_examples'])

    result={
        'release':'FUG-I_v005',
        'scope':'full positive-label grammar; all 307 transports through Fibonacci index 84; exact infinite family theorems',
        'indexed_fibonacci_layers':84,
        'unrestricted_transport_counts':{str(k):counts[k] for k in (0,1,2)},
        'unrestricted_delayed_pairs':[(int(r['m']),int(r['n'])) for r in delayed],
        'doubling_gate':{'all_odd_r':'depth 2 iff Lucas_(12r)/2 is squarefree; otherwise depth 1',
                         'samples':{str(r['r']):r['first_new_depth_full'] for r in odd}},
        'infinite_obstruction':'(F_(84*s),F_(168*s)) for odd s; new immediate N=6',
        'unrestricted_infinite_delayed_fibonacci_family':'NOT ESTABLISHED; squarefree Lucas quotient infinitude is unresolved here',
        'matched_nonfibonacci_delayed_family':'(144,288*p) for each prime p>=5',
        'unbounded_distinct_content_fibonacci_mergers':'for each t>=1 choose z(2^(16t)*3^(4t)); >=t+1 distinct contents',
        'existing_earlier_releases':'v001-v004 retained as frozen baselines',
    }
    (OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('FUG-I Phase 5 exact run PASS')
    print('All-label 84-index transport classifications:',dict(counts))
    print('Unrestricted delayed pairs:',result['unrestricted_delayed_pairs'])
    print('Odd-r Lucas squarefreeness gate:',result['doubling_gate']['samples'])
    print('Infinite unrestricted depth-1 obstruction: r=7*s, s odd (N=6)')
    print('Unbounded distinct-content Fibonacci mergers: t+1 at rank z(2^(16t)*3^(4t))')
    print('Results:',OUT)

if __name__=='__main__':
    main()
