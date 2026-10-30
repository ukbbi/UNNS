import json, itertools
from collections import Counter
from geo2 import *
exec(open('inv6c.py').read().split("invs=")[0])  # reuse inv()
def pointcolors(X,k):
    C,_=code_from_points(X); Cw=set(C.values()); cs=circuits_of(Cw); n=len(X)
    parts=one_partitions(cs,n)
    base=[(sum(1 for c in cs if c>>i&1), tuple(sorted(Counter(weight(next(c for c in P if c>>i&1)) for P in parts).items()))) for i in range(n)]
    pc=[[sum(1 for c in cs if c>>i&1 and c>>j&1) for j in range(n)] for i in range(n)]
    ps=[[sum(1 for P in parts if len(P)==2 and ((P[0]>>i&1) != (P[0]>>j&1))) for j in range(n)] for i in range(n)]
    col=[hash(b) for b in base]
    for it in range(3):
        col=[hash((col[i],tuple(sorted((col[j],pc[i][j],ps[i][j]) for j in range(n) if j!=i)))) for i in range(n)]
    return col
def lin_extend(B,T,k):
    # solve linear map g with g(B_i)=T_i; return function
    # express x in basis B via elimination
    rows=[(b,1<<i) for i,b in enumerate(B)]
    basis=[]
    for v,tag in rows:
        for bv,bt in basis:
            if v^bv<v: v^=bv; tag^=bt
        basis.append((v,tag)) if False else None
    # simple gaussian with reduction table
    red=[]
    for v,tag in rows:
        for rv,rt in red:
            if (v^rv)<v: v^=rv; tag^=rt
        if v==0: return None
        red.append((v,tag)); red.sort(reverse=True)
    def apply(x):
        tag=0
        for rv,rt in red:
            if (x^rv)<x: x^=rv; tag^=rt
        if x: return None
        r=0
        for i in range(len(B)):
            if tag>>i&1: r^=T[i]
        return r
    return apply
def equivalent(X,Y,k=6):
    if len(X)!=len(Y): return False
    cx,cy=pointcolors(X,k),pointcolors(Y,k)
    if sorted(cx)!=sorted(cy): return False
    # choose basis from X greedily preferring rare colors
    cnt=Counter(cx); order=sorted(range(len(X)),key=lambda i:(cnt[cx[i]],i))
    B=[];idx=[]
    for i in order:
        if rank_bits(B+[X[i]])>len(B): B.append(X[i]); idx.append(i)
        if len(B)==k: break
    Ys=set(Y)
    cand=[[j for j in range(len(Y)) if cy[j]==cx[i]] for i in idx]
    def rec(t,T):
        if t==k:
            g=lin_extend(B,[Y[j] for j in T],k)
            if g is None: return False
            img=[g(x) for x in X]
            return None not in img and set(img)==Ys
        for j in cand[t]:
            if j in T: continue
            if rank_bits([Y[u] for u in T]+[Y[j]])<len(T)+1: continue
            if rec(t+1,T+[j]): return True
        return False
    return rec(0,[])
if __name__=='__main__':
    c6=json.load(open('../src/certificates/C6_rank6.json'))
    invs=[inv(c['support'],6) for c in c6]
    groups={}
    for i,v in enumerate(invs): groups.setdefault(v,[]).append(i)
    out=[]
    for v,g in groups.items():
        if len(g)>1:
            for a,b in itertools.combinations(g,2):
                e=equivalent(c6[a]['support'],c6[b]['support'])
                out.append((a,b,e)); print(a,b,e,flush=True)
    # sanity: a random affine image is equivalent
    import random
    X=c6[53]['support']; 
    def rand_aff(X,k=6):
        while True:
            B=[random.choice(range(1<<(k-1),1<<k)) for _ in range(k)]
            if rank_bits(B)==k:
                g=lin_extend([1<<i for i in range(k)],B,k); return [g(x) for x in X]
    print('sanity random image equivalent:',equivalent(X,rand_aff(X)) )
    json.dump(out,open('../logs/equiv6.json','w'))
