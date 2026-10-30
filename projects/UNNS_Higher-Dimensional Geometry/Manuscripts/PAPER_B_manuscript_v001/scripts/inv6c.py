import json
from collections import Counter
from geo2 import *
c6=json.load(open('../src/certificates/C6_rank6.json'))
def inv(X,k):
    C,_=code_from_points(X); Cw=set(C.values()); cs=circuits_of(Cw); n=len(X)
    parts=one_partitions(cs,n)
    base=[]
    for i in range(n):
        base.append((sum(1 for c in cs if c>>i&1), tuple(sorted(Counter(weight(next(c for c in P if c>>i&1)) for P in parts).items()))))
    pc=[[sum(1 for c in cs if c>>i&1 and c>>j&1) for j in range(n)] for i in range(n)]
    ps=[[sum(1 for P in parts if len(P)==2 and ((P[0]>>i&1) != (P[0]>>j&1))) for j in range(n)] for i in range(n)]
    col=[hash(b) for b in base]
    for it in range(3):
        col=[hash((col[i],tuple(sorted((col[j],pc[i][j],ps[i][j]) for j in range(n) if j!=i)))) for i in range(n)]
    return (n,tuple(sorted(Counter(weight(c) for c in cs).items())),tuple(sorted(Counter(len(P) for P in parts).items())),tuple(sorted(col)))
invs=[inv(c['support'],6) for c in c6]
print(len(invs),len(set(invs)))
cnt=Counter(invs)
dup=[i for i,v in enumerate(invs) if cnt[v]>1]
print(dup)
for i in dup: print(i,len(c6[i]['support']),c6[i]['two_blocks'])
