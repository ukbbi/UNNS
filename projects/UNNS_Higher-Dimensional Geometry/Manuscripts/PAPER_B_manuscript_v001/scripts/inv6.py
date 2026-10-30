import json
from collections import Counter
from geo2 import *
c6=json.load(open('../src/certificates/C6_rank6.json'))
def inv(X,k):
    C,_=code_from_points(X); Cw=set(C.values()); cs=circuits_of(Cw); n=len(X)
    parts=one_partitions(cs,n)
    pt=[]
    for i in range(n):
        pt.append((sum(1 for c in cs if c>>i&1), tuple(sorted(Counter(weight(next(c for c in P if c>>i&1)) for P in parts).items())) ))
    # pairs of points: number of circuits containing both
    return (n, tuple(sorted(Counter(weight(c) for c in cs).items())), tuple(sorted(Counter(len(P) for P in parts).items())), tuple(sorted(pt)))
invs=[inv(c['support'],6) for c in c6]
print(len(invs),len(set(invs)))
cnt=Counter(invs); print(sorted(cnt.values())[-5:])
import pickle
