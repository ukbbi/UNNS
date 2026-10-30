#!/usr/bin/env python3
"""Brute-force classification of minimal non-embedded reduced boxes of nullity k=3,4,5 (own engine),
orbit counts under AGL(k-1,2) via union-find, Burnside counts, E1-vs-definition cross-check, identities."""
import sys, json, itertools, time
from geo2 import *

def aff_perms(m):
    """generators of AGL(m,2) acting on the 2^m points of AG(m,2) (points = m-bit ints)"""
    N=1<<m; gens=[]
    # translations
    for i in range(m):
        gens.append([p^(1<<i) for p in range(N)])
    # elementary linear maps x_i += x_j, and coordinate transposition
    for i in range(m):
        for j in range(m):
            if i!=j:
                gens.append([p ^ (((p>>j)&1)<<i) for p in range(N)])
    return gens

def group_closure(gens,N,limit=10**6):
    idt=tuple(range(N)); seen={idt}; fr=[idt]
    g=[tuple(x) for x in gens]
    while fr:
        nf=[]
        for a in fr:
            for h in g:
                b=tuple(h[a[i]] for i in range(N))
                if b not in seen:
                    seen.add(b); nf.append(b)
        fr=nf
        if len(seen)>limit: raise RuntimeError
    return seen

def burnside(m):
    N=1<<m
    G=group_closure(aff_perms(m),N)
    tot=0
    for g in G:
        seen=[0]*N; c=0
        for i in range(N):
            if not seen[i]:
                c+=1; j=i
                while not seen[j]:
                    seen[j]=1; j=g[j]
        tot+=1<<c
    assert tot%len(G)==0
    return len(G), tot//len(G)

def orbits(m, subsets):
    N=1<<m; gens=aff_perms(m)
    parent={s:s for s in subsets}
    def find(a):
        while parent[a]!=a:
            parent[a]=parent[parent[a]]; a=parent[a]
        return a
    for s in subsets:
        for g in gens:
            t=0; x=s
            while x:
                b=x&-x; i=b.bit_length()-1; t|=1<<g[i]; x^=b
            if t in parent:
                ra,rb=find(s),find(t)
                if ra!=rb: parent[ra]=rb
    cls={}
    for s in subsets: cls.setdefault(find(s),[]).append(s)
    return list(cls.values())

def run(k):
    m=k-1; pts=affine_points(m)  # k-bit ints with top bit
    N=len(pts)
    idx={p:i for i,p in enumerate(pts)}
    res=dict(k=k,subsets=0,spanning=0,nonemb=0,minimal=0)
    minimal=[]
    for mask in range(1<<N):
        X=[pts[i] for i in range(N) if mask>>i&1]
        if len(X)<k+1: continue
        if rank_bits(X)<k: continue
        res['spanning']+=1
        C,_=code_from_points(X); cs=circuits_of(set(C.values()))
        if not is_nonembedded_E1(cs): continue
        res['nonemb']+=1
        if is_minimal_nonembedded(cs,len(X)): minimal.append(mask)
    res['minimal']=len(minimal)
    cl=orbits(m,minimal)
    res['classes']=len(cl)
    info=[]
    for c in sorted(cl,key=lambda c:(bin(c[0]).count('1'),min(c))):
        mask=min(c); X=[pts[i] for i in range(N) if mask>>i&1]
        d=check_identities(X,k)
        info.append(dict(p=len(X),orbit_size=len(c),rep=X,n2=d['n2'],m=d['m'],ok=d['counting'] and d['parseval'] and d['vsp'] and d['pair_ok']))
    res['info']=info
    return res

if __name__=='__main__':
    out={}
    for m in (2,3,4):
        out['burnside_AG%d'%m]=burnside(m)
    print(out)
    for k in (3,4,5):
        t=time.time(); r=run(k); r['seconds']=round(time.time()-t,1)
        out['k%d'%k]=r
        print(k,{a:b for a,b in r.items() if a!='info'},[(i['p'],i['n2'],i['ok']) for i in r['info']],flush=True)
    json.dump(out,open('../logs/classify.json','w'),indent=1)
