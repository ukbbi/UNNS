"""UNNS-U3 graph layer: exact neighbours (frozen RN core), BFS distances, canonical lexicographically-first geodesic."""
import sys,os
H=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,H+"/../frozen_RN")
import rn_core as C
_NB={}
def nbrs(x):
    r=_NB.get(x)
    if r is None:
        n=C.neighbours(x)
        for t in n["F"]+n["I"]:           # carry composed factorizations (no refactoring of neighbours)
            C._FC.setdefault(t[1],(t[2],n["cert"]))
        r=(sorted(t[1] for t in n["F"]+n["I"]),n["cert"]);_NB[x]=r
    return r[0]
CERT=[True]
def layers(a,R,stop=None):
    """exact BFS layers around a to radius R: list of dicts v->parent-set-free (just sets)."""
    seen={a:0};cur=[a];L=[[a]]
    for i in range(1,R+1):
        nxt=[]
        for v in cur:
            for w in nbrs(v):
                if w not in seen: seen[w]=i;nxt.append(w)
        L.append(nxt);cur=nxt
        if stop is not None and stop in seen: break
    return seen,L
def dist(a,b,maxd=12):
    """exact graph distance by bidirectional BFS; None if > maxd"""
    if a==b: return 0
    sa={a:0};sb={b:0};fa=[a];fb=[b];da=db=0
    while da+db<maxd:
        if len(fa)<=len(fb):
            nf=[]
            for v in fa:
                for w in nbrs(v):
                    if w not in sa:
                        sa[w]=sa[v]+1;nf.append(w)
                        if w in sb: return sa[w]+sb[w]
            fa=nf;da+=1
        else:
            nf=[]
            for v in fb:
                for w in nbrs(v):
                    if w not in sb:
                        sb[w]=sb[v]+1;nf.append(w)
                        if w in sa: return sa[w]+sb[w]
            fb=nf;db+=1
        if not fa or not fb: return None
    return None
def geodesic(a,b,maxd=12):
    """canonical routing P(a,b): lexicographically first shortest path (by vertex values); P(a,a)=(a,4a,a)."""
    if a==b: return (a,4*a,a)
    d=dist(a,b,maxd)
    if d is None: raise ValueError("distance exceeds maxd")
    # distances to b for vertices that matter: BFS from b to radius d gives D_b on the ball; ball can be large, so go greedily:
    sb,_=layers(b,d)         # exact ball of radius d around b (complete)
    path=[a];x=a
    for i in range(d):
        c=[w for w in nbrs(x) if sb.get(w,99)==d-1-i]
        x=min(c);path.append(x)
    assert path[-1]==b and len(path)==d+1
    return tuple(path)
