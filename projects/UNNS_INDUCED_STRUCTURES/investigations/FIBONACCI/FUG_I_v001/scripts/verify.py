#!/usr/bin/env python3
"""Independent backwards-search oracle for FUG-I v001; standard library only.

Does not import fug_i.py or its factorization/divisor enumerator.
"""
import csv
import json
from functools import lru_cache
from math import gcd,isqrt
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'results'
F=[0,1]
for n in range(2,49): F.append(F[-1]+F[-2])


@lru_cache(maxsize=None)
def predecessor_pairs(y):
    # Deliberately independent naive oracle: inspect every possible sqrt-divisor.
    # Each pair is a legal reverse edge (x, N), with x>0 and T_N(x)=y.
    return tuple((y//(d*d)*(d-1),d-1)
                 for d in range(2,isqrt(y)+1) if y%(d*d)==0)


def backwards_routes(end,depth):
    """Yield all forward paths arriving at `end` with precisely `depth` edges."""
    states=[(end,)]
    labels=[()]
    for length in range(depth):
        new_states=[];new_labels=[]
        for s,l in zip(states,labels):
            for x,N in predecessor_pairs(s[0]):
                new_states.append((x,)+s)
                new_labels.append((N,)+l)
        states=new_states;labels=new_labels
    return tuple(zip(states,labels))


def main():
    expected=json.loads((DATA/'summary.json').read_text(encoding='utf-8'))
    observed=set()
    reverse_nodes=0
    val_index={}
    for i in range(1,49): val_index.setdefault(F[i],[]).append(i)
    for j in range(1,49):
        for length in (1,2,3):
            for states,labels in backwards_routes(F[j],length):
                reverse_nodes+=1
                for i in val_index.get(states[0],[]):
                    if i<j:
                        observed.add((i,j,labels,states))
    target={(r['i'],r['j'],tuple(r['labels']),tuple(r['states']))
             for r in expected['all_fibonacci_paths_le3']}
    assert observed==target, f'Backward and forward route sets differ: {observed^target}'
    assert len(observed)==8

    inc=list(csv.DictReader((DATA/'fib_incidence_48.csv').open(encoding='utf-8',newline='')))
    for r in inc:
        n=int(r['n']); d=int(r['d']); N=int(r['N']); M=int(r['M'])
        assert (d-1)==N and M*(N+1)**2==F[n]*N
    assert len(inc)==27
    # Independent direct enumeration of all coordinates (including absent ones).
    for n in range(1,49):
        brute={d for d in range(2,isqrt(F[n])+1) if F[n]%(d*d)==0}
        stored={int(r['d']) for r in inc if int(r['n'])==n}
        assert brute==stored,(n,brute,stored)
    for m in range(1,49):
        for n in range(1,49):
            dm={int(r['d']) for r in inc if int(r['n'])==m}
            dn={int(r['d']) for r in inc if int(r['n'])==n}
            dg={int(r['d']) for r in inc if int(r['n'])==gcd(m,n)}
            assert dm&dn==dg
    # First appearances within the frozen range; all exact integer checks.
    first={}
    for d in (2,3,4,5,6,8,12,24):
        first[d]=next(n for n in range(1,49) if F[n]%(d*d)==0)
    assert first=={2:6,3:12,4:12,5:25,6:12,8:48,12:12,24:48}
    assert expected['index_pair_meet_checks']==48*48
    print('PASS: independent reverse oracle agrees with full forward route enumeration')
    print('PASS: 27 incoming occurrences and 2304 meet checks')
    print('PASS: 8 exact routes, 4 reachable endpoint pairs, lengths <=3')
    print('PASS: first-appearance witnesses',first)
    print('Reverse states examined:',reverse_nodes)


if __name__=='__main__':
    main()
