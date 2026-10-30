#!/usr/bin/env python3
"""W2 for p<=8 by simplex extension (own proof-support computation).
Any spanning X in AG(k-1,2) with p points is AGL-equivalent to {e_1..e_k} u R, R a set of p-k odd-weight vectors of weight>=3 in F_2^k.
Enumerate all such R; record minimal non-embedded ones and their n_2."""
import itertools, json
from geo2 import *
res={}
for p in range(4,9):
    for k in range(3,p):          # k+1<=p
        odd=[v for v in range(1<<k) if bin(v).count('1')%2==1 and bin(v).count('1')>=3]
        base=[1<<i for i in range(k)]
        r=p-k
        tested=0; nonemb=0; minimal=0; minn2=None; allW2=True; dists={}
        for R in itertools.combinations(odd,r):
            X=base+list(R); tested+=1
            C,_=code_from_points(X); cs=circuits_of(set(C.values()))
            if not is_nonembedded_E1(cs): continue
            nonemb+=1
            if not is_minimal_nonembedded(cs,p): continue
            minimal+=1
            n2=n2_count(one_partitions(cs,p))
            minn2=n2 if minn2 is None else min(minn2,n2)
            if n2<2: allW2=False
        res['k%d_p%d'%(k,p)]=dict(k=k,p=p,candidates=tested,nonembedded=nonemb,minimal=minimal,min_n2=minn2,all_W2=allW2)
        print(res['k%d_p%d'%(k,p)],flush=True)
json.dump(res,open('../logs/small_p.json','w'),indent=1)
