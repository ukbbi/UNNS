import sys,json,os,itertools,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import *
from swaps import *
from topo import *
from fractions import Fraction
R={};t0=time.time()
# --- groups vs classes for 72^r
def cls(t):
    hs=histories(t); hset=set(hs); idx={h:i for i,h in enumerate(hs)}; par=list(range(len(hs)))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    for (s,w) in hs:
        for i in range(len(w)-1):
            if w[i]!=w[i+1]:
                v=(s,w[:i]+(w[i+1],w[i])+w[i+2:])
                if v in hset: par[f(idx[(s,w)])]=f(idx[v])
    groups={(s,tuple(sorted(w))) for s,w in hs}
    # split groups: groups with >=2 classes
    gcl={}
    for i,(s,w) in enumerate(hs): gcl.setdefault((s,tuple(sorted(w))),set()).add(f(i))
    return len(hs),len({f(i) for i in range(len(hs))}),len(groups),sum(1 for v in gcl.values() if len(v)>1)
R['groups']={str(r):cls(72**r) for r in (1,2,3)}
print(R['groups'],time.time()-t0,flush=True)
# split endpoints census
split=[]
for t in range(4,6001):
    if not sqdivs(t): continue
    if H(t)>4000: continue
    n,c,g,sg=cls(t)
    if sg>0: split.append(t)
R['split_endpoints_4_6000']=split
print(split,time.time()-t0,flush=True)
# --- Q Betti numbers of complete-history cubical complex of 72^r
def Q_betti(t):
    hs=histories(t); hset=set(hs)
    # cells: (base history, frozenset of positions) with all legal; identify cube by min vertex & positions
    def swapped(h,i): s,w=h; return (s,w[:i]+(w[i+1],w[i])+w[i+2:])
    cubes={}  # dim -> dict key->idx ; key = (frozenset of vertices)
    verts=sorted(hset)
    bydim={}
    for h in verts:
        s,w=h
        legal=[i for i in range(len(w)-1) if w[i]!=w[i+1] and swapped(h,i) in hset]
        def rec(j,chosen):
            yield tuple(chosen)
            for k in range(j,len(legal)):
                if not chosen or legal[k]>chosen[-1]+1: yield from rec(k+1,chosen+[legal[k]])
        for S in rec(0,[]):
            vs=[]
            for mask in range(1<<len(S)):
                v=h
                for b,i in enumerate(S):
                    if mask>>b&1: v=swapped(v,i)
                vs.append(v)
            key=frozenset(vs)
            bydim.setdefault(len(S),{})
            if key not in bydim[len(S)]: bydim[len(S)][key]=(h,S)
    top=max(bydim); idx={d:{k:i for i,k in enumerate(bydim[d])} for d in bydim}
    bds={}
    for d in range(1,top+1):
        rows=[]
        for key,(h,S) in bydim[d].items():
            x=0
            for b,i in enumerate(S):
                rest=S[:b]+S[b+1:]
                for side in (0,1):
                    base=h if side==0 else swapped(h,i)
                    vs=[]
                    for mask in range(1<<len(rest)):
                        v=base
                        for bb,j in enumerate(rest):
                            if mask>>bb&1: v=swapped(v,j)
                        vs.append(v)
                    x^=1<<idx[d-1][frozenset(vs)]
            rows.append(x)
        bds[d]=rows
    counts=[len(bydim[d]) for d in range(top+1)]
    return counts,betti_from_boundaries(counts,bds)
R['Q72r']={}
for r in (1,2,3):
    R['Q72r'][str(r)]=Q_betti(72**r); print(r,R['Q72r'][str(r)],time.time()-t0,flush=True)
json.dump(R,open('../results/RESULTS_II_part7.json','w'),indent=1,default=str)
