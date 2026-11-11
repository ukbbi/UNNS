"""Independent exact graph layer for the Stage-2 verifiers. Deliberately shares NO code with engine/u3_graph.py or frozen_RN:
neighbours by sympy divisor enumeration / trial division of square divisors; plain bidirectional BFS."""
import math
from functools import lru_cache
import sympy
@lru_cache(maxsize=None)
def nbrs(x):
    out=set()
    for d in sympy.divisors(x): out.add(x*(d+1)**2//d)                 # forward: N=d divides x
    q=2
    while q*q<=x:
        if x%(q*q)==0: out.add(x*(q-1)//(q*q))                       # inverse: q^2 | x
        q+=1
    out.discard(x)
    return tuple(sorted(out))
def dist(a,b,maxd=8):
    """exact distance (None if > maxd): complete layers alternately; stop at the first completed layer with an intersection"""
    if a==b: return 0
    A={a:0};B={b:0};fa=[a];fb=[b];da=db=0
    while da+db<maxd and (fa or fb):
        if fa and (len(fa)<=len(fb) or not fb):
            nf=[]
            for v in fa:
                for w in nbrs(v):
                    if w not in A: A[w]=A[v]+1;nf.append(w)
            fa=nf;da+=1
        else:
            nf=[]
            for v in fb:
                for w in nbrs(v):
                    if w not in B: B[w]=B[v]+1;nf.append(w)
            fb=nf;db+=1
        common=set(A)&set(B)
        if common: return min(A[w]+B[w] for w in common)
    return None
def deg(x): return len(nbrs(x))
