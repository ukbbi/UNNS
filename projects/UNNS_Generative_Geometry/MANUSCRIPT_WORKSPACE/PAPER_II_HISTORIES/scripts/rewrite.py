from engine import *
from itertools import permutations
from math import lcm
def Rfrac(N): return Fraction((N+1)**2,N)
def mult(w):
    r=Fraction(1)
    for N in w: r*=Rfrac(N)
    return r
def perms(c):
    from collections import Counter
    cnt=Counter(c); L=sorted(cnt); n=len(c); out=[]
    def rec(cur):
        if len(cur)==n: out.append(tuple(cur)); return
        for x in L:
            if cnt[x]:
                cnt[x]-=1; cur.append(x); rec(cur); cur.pop(); cnt[x]+=1
    rec([]); return out
def adm_perms(c,m):
    """admissible arrangements of multiset c from m, by DFS on states"""
    from collections import Counter
    cnt=Counter(c); L=sorted(cnt); n=len(c); out=[]
    def rec(cur,mm):
        if len(cur)==n: out.append(tuple(cur)); return
        for x in L:
            if cnt[x] and mm%x==0:
                cnt[x]-=1; cur.append(x); rec(cur,mm//x*(x+1)**2); cur.pop(); cnt[x]+=1
    rec([],m); return out
def space_components(m, contents, rel):
    """vertices: admissible words with a content in contents; edges: adjacent swaps; plus block rewrites (u,v) in rel
    (u,v tuples; every arrangement of the multiset is a block)."""
    V=set()
    for c in contents:
        V|=set(adm_perms(c,m))
    par={w:w for w in V}
    def f(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    for w in V:
        for i in range(len(w)-1):
            if w[i]!=w[i+1]:
                v=w[:i]+(w[i+1],w[i])+w[i+2:]
                if v in V: par[f(w)]=f(v)
    for (U,Vv) in rel:
        for ub in perms(U):
            for vb in perms(Vv):
                for w in V:
                    for i in range(len(w)-len(ub)+1):
                        if w[i:i+len(ub)]==ub:
                            x=w[:i]+vb+w[i+len(ub):]
                            if x in V: par[f(w)]=f(x)
                            # symmetric covered by iterating both
                for w in V:
                    for i in range(len(w)-len(vb)+1):
                        if w[i:i+len(vb)]==vb:
                            x=w[:i]+ub+w[i+len(vb):]
                            if x in V: par[f(w)]=f(x)
    return len({f(w) for w in V}), len(V)
def block_admissible(x,u,v):
    assert mult(u)==mult(v)
    return x%lcm(K(u),K(v))==0
