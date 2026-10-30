#!/usr/bin/env python3
"""Cross-check: (i) E1 criterion == definition-level collision existence; (ii) r_min==3; (iii) circuit tests agree.
Exhaustive over all multisets of non-zero points of F_2^k, k<=3, length n<=7 and all spanning point sets of F_2^4\\0 with n<=8 (random sample of 1500 for k=4)."""
import random, itertools, json
from geo2 import *
random.seed(1)
stat=dict(tested=0,nonemb=0,mismatch=0,minrank=set(),circ_mismatch=0)
def test(X):
    k=max(x.bit_length() for x in X)
    if rank_bits(X)<k: return
    C,_=code_from_points(X); Cw=set(C.values()); n=len(X)
    cs=circuits_of(Cw)
    if cs!=circuits_by_rank(X,k): stat['circ_mismatch']+=1
    e1=is_nonembedded_E1(cs); col=collisions(Cw,n)
    stat['tested']+=1
    if e1!=bool(col): stat['mismatch']+=1
    if e1:
        stat['nonemb']+=1
        r=min(collision_rank(a,b,n) for a,b in col); stat['minrank'].add(r)
for k in (2,3):
    pts=list(range(1,1<<k))
    for n in range(1,8):
        for X in itertools.combinations_with_replacement(pts,n): test(list(X))
pts=list(range(1,16))
for _ in range(1500):
    n=random.randint(5,8); test([random.choice(pts) for _ in range(n)])
stat['minrank']=sorted(stat['minrank']); print(stat)
json.dump(stat,open('../logs/crosscheck.json','w'))
