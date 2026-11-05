from engine import *
from itertools import permutations, product, combinations
def rank_gf2(rows):
    """rows: list of python int bitmasks; returns rank"""
    piv={}
    r=0
    for x in rows:
        while x:
            h=x.bit_length()-1
            if h in piv: x^=piv[h]
            else: piv[h]=x; r+=1; break
    return r
def betti_from_boundaries(counts, bds):
    """counts[d]=#cells dim d; bds[d]= list of bitmask rows (one per d-cell, bits index (d-1)-cells), d>=1"""
    ranks=[0]*(len(counts)+1)
    for d in range(1,len(counts)):
        ranks[d]=rank_gf2(bds[d])
    return [counts[d]-ranks[d]-ranks[d+1] for d in range(len(counts))]
def ordered_partitions(n):
    """ordered set partitions of range(n) as tuples of frozensets-> blocks list"""
    res=[]
    def rec(rem,cur):
        if not rem: res.append(tuple(cur)); return
        rem=list(rem)
        for mask in range(1,1<<len(rem)):
            blk=tuple(rem[i] for i in range(len(rem)) if mask>>i&1)
            rest=[x for x in rem if x not in blk]
            rec(rest,cur+[blk])
    rec(list(range(n)),[])
    return res
def linear_exts(op):
    for ch in product(*[list(permutations(b)) for b in op]):
        yield tuple(x for c in ch for x in c)
def perm_complex(content,m):
    """full subcomplex of permutohedron on admissible arrangements (distinct labels). returns f-vector and GF2 Betti"""
    labs=sorted(content); n=len(labs)
    ok={}
    def adm(p): 
        if p not in ok: ok[p]=(m%K(tuple(labs[i] for i in p))==0)
        return ok[p]
    cells={}
    for op in ordered_partitions(n):
        if all(adm(p) for p in linear_exts(op)):
            d=n-len(op)   # dimension = n - #blocks
            cells.setdefault(d,[]).append(op)
    if not cells: return [],[]
    top=max(cells)
    idx={d:{c:i for i,c in enumerate(cells[d])} for d in cells}
    # faces of a cell op (dim d): merge two adjacent blocks -> dim d+1 is coface. Boundary of op = refine one block into two ordered blocks
    bds={}
    for d in range(1,top+1):
        rows=[]
        for op in cells[d]:
            x=0
            for bi,b in enumerate(op):
                if len(b)<2: continue
                for mask in range(1,(1<<len(b))-1):
                    b1=tuple(b[i] for i in range(len(b)) if mask>>i&1); b2=tuple(b[i] for i in range(len(b)) if not mask>>i&1)
                    f=op[:bi]+(b1,b2)+op[bi+1:]
                    x^=1<<idx[d-1][f]   # must be present (full subcomplex)
            rows.append(x)
        bds[d]=rows
    counts=[len(cells.get(d,[])) for d in range(top+1)]
    return counts, betti_from_boundaries(counts,bds)
def cubical_complex(content,m):
    labs=tuple(sorted(content))
    A=[w for w in set(permutations(labs)) if m%K(w)==0]; Aset=set(A)
    cubes={}  # (base, frozenset positions) canonical: base = min vertex
    def swapat(w,i): return w[:i]+(w[i+1],w[i])+w[i+2:]
    n=len(labs)
    for w in A:
        # positions i where swapping is legal and disjoint choices
        legal=[i for i in range(n-1) if swapat(w,i) in Aset]
        # choose disjoint subsets
        def rec(i,chosen):
            yield tuple(chosen)
            for j in range(i,len(legal)):
                if not chosen or legal[j]>chosen[-1]+1:
                    yield from rec(j+1,chosen+[legal[j]])
        for S in rec(0,[]):
            verts=[]
            ok=True
            for mask in range(1<<len(S)):
                v=w
                for b,i in enumerate(S):
                    if mask>>b&1: v=swapat(v,i)
                if v not in Aset or (S and False): ok=False;break
                verts.append(v)
            if not ok: continue
            key=frozenset(verts)
            # cube identified by vertex set + dim
            cubes[(len(S),key)]=(w,S)
    bydim={}
    for (d,key),(w,S) in cubes.items(): bydim.setdefault(d,[]).append((key,w,S))
    top=max(bydim)
    idx={d:{} for d in bydim}
    for d in bydim:
        for i,(key,w,S) in enumerate(bydim[d]): idx[d][key]=i
    bds={}
    for d in range(1,top+1):
        rows=[]
        for key,w,S in bydim[d]:
            x=0
            for b,i in enumerate(S):
                rest=S[:b]+S[b+1:]
                for side in (0,1):
                    base=w if side==0 else swapat(w,i)
                    verts=[]
                    for mask in range(1<<len(rest)):
                        v=base
                        for bb,j in enumerate(rest):
                            if mask>>bb&1: v=swapat(v,j)
                        verts.append(v)
                    x^=1<<idx[d-1][frozenset(verts)]
            rows.append(x)
        bds[d]=rows
    counts=[len(bydim.get(d,[])) for d in range(top+1)]
    return counts,betti_from_boundaries(counts,bds)
