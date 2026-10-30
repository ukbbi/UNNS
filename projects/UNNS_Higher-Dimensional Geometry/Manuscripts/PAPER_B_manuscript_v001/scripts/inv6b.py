import json
from collections import Counter
from geo2 import *
c6=json.load(open('../src/certificates/C6_rank6.json'))
def inv(X,k):
    C,_=code_from_points(X); Cw=set(C.values()); cs=circuits_of(Cw); n=len(X)
    parts=one_partitions(cs,n)
    pc=[[0]*n for _ in range(n)]; ps=[[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            pc[i][j]=sum(1 for c in cs if c>>i&1 and c>>j&1)
            ps[i][j]=sum(1 for P in parts if len(P)==2 and ((P[0]>>i&1) != (P[0]>>j&1)))
    col=[(sum(1 for c in cs if c>>i&1),) for i in range(n)]
    for it in range(3):
        new=[]
        for i in range(n):
            nb=tuple(sorted((col[j],pc[i][j],ps[i][j]) for j in range(n) if j!=i))
            new.append(hash((col[i],nb)))
        col=new
    return (n,tuple(sorted(Counter(weight(c) for c in cs).items())),tuple(sorted(Counter(len(P) for P in parts).items())),tuple(sorted(col)))
invs=[inv(c['support'],6) for c in c6]
print(len(invs),len(set(invs)))
