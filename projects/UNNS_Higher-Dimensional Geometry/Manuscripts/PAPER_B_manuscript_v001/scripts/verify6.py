#!/usr/bin/env python3
"""Re-check of the 215 source-reported nullity-6 classes with the own engine (support sets from C6_rank6.json)
and the 231 PARTITION certificates' supports (k=3..6): minimality, non-embeddedness, identities, n2>=p-1 (p>=9), pairwise
inequivalence by an invariant (p, n2, sorted partition profile, circuit-weight multiset)."""
import json, sys, time
from geo2 import *
src='../src/certificates/'
c6=json.load(open(src+'C6_rank6.json')); c9=json.load(open(src+'C9_partition.json')); c5=json.load(open(src+'C5_rank5.json'))
out=dict(n_c6=len(c6),n_c9=len(c9),bad=[],inv=set())
t=time.time(); invs=[]
for i,c in enumerate(c6):
    X=c['support']; k=6
    assert rank_bits(X)==6 and all(x>>5&1 for x in X)
    C,_=code_from_points(X); Cw=set(C.values()); cs=circuits_of(Cw)
    ok=is_minimal_nonembedded(cs,len(X))
    d=check_identities(X,k)
    good=ok and d['counting'] and d['parseval'] and d['vsp'] and d['pair_ok'] and (len(X)<9 or d['n2']>=len(X)-1) and d['n2']>=2 and d['n2']==c['two_blocks']
    if not good: out['bad'].append(i)
    invs.append((len(X),d['n2'],tuple(d['m']),tuple(sorted(weight(w) for w in cs))))
    if i%25==0: print(i,time.time()-t,flush=True)
out['distinct_invariants']=len(set(invs))
out['p_range']=[min(i[0] for i in invs),max(i[0] for i in invs)]
out['min_n2']=min(i[1] for i in invs)
# C9: all 231
cnt=0
for c in c9:
    X=c['points']; k=c['k']
    C,_=code_from_points(X); cs=circuits_of(set(C.values()))
    d=check_identities(X,k)
    if is_minimal_nonembedded(cs,len(X)) and d['n2']==c['n_two_blocks']: cnt+=1
    else: out['bad'].append(('c9',c['label']))
out['c9_ok']=cnt
out['inv']=None
print(out); json.dump(out,open('../logs/verify6.json','w'))
