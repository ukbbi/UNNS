import sys,json,os,itertools
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import *
from swaps import *
from topo import *
from fractions import Fraction
R={}
def rank_Q(rows):
    M=[[Fraction(x) for x in r] for r in rows]; rk=0; ncol=len(M[0]) if M else 0
    for c in range(ncol):
        piv=None
        for i in range(rk,len(M)):
            if M[i][c]!=0: piv=i;break
        if piv is None: continue
        M[rk],M[piv]=M[piv],M[rk]
        for i in range(len(M)):
            if i!=rk and M[i][c]!=0:
                f=M[i][c]/M[rk][c]; M[i]=[a-f*b for a,b in zip(M[i],M[rk])]
        rk+=1
    return rk
def Kp(w,P):
    k=1
    for p in P:
        s=0;b=0
        for N in w: s+=delta(N,p); b=max(b,-s)
        k*=p**b
    return k
def adm_with(c,m,P):
    return [w for w in permutations(c) if m%Kp(w,P)==0]
def betti_with(c,m,P):
    # route complex using only constraints at primes P
    labs=tuple(sorted(c)); n=len(labs)
    from topo import ordered_partitions,linear_exts,betti_from_boundaries
    A={w for w in permutations(labs) if m%Kp(w,P)==0}
    cells={}
    for op in ordered_partitions(n):
        if all(tuple(labs[i] for i in p) in A for p in linear_exts(op)):
            cells.setdefault(n-len(op),[]).append(op)
    if not cells: return []
    top=max(cells); idx={d:{c_:i for i,c_ in enumerate(cells[d])} for d in cells}
    bds={}
    for d in range(1,top+1):
        rows=[]
        for op in cells[d]:
            x=0
            for bi,b in enumerate(op):
                if len(b)<2: continue
                for mask in range(1,(1<<len(b))-1):
                    b1=tuple(b[i] for i in range(len(b)) if mask>>i&1); b2=tuple(b[i] for i in range(len(b)) if not mask>>i&1)
                    x^=1<<idx[d-1][op[:bi]+(b1,b2)+op[bi+1:]]
            rows.append(x)
        bds[d]=rows
    counts=[len(cells[d]) for d in range(top+1)]
    return betti_from_boundaries(counts,bds)
def dims(c,m):
    allp=sorted({p for N in c for p in primes_of(N)}|{p for N in c for p in primes_of(N+1)})
    act=sorted({p for N in c for p in primes_of(N)})
    span=rank_Q([[delta(N,p) for p in allp] for N in c])
    base=set(adm_with(c,m,act))
    dc=[p for p in act if set(adm_with(c,m,[q for q in act if q!=p]))!=base]
    b0=betti_with(c,m,act)
    dt=None
    for r in range(0,len(act)+1):
        for S in itertools.combinations(act,r):
            if betti_with(c,m,list(S))==b0: dt=S;break
        if dt is not None: break
    return {'primes':allp,'active':act,'d_span':span,'constraint_primes':dc,'d_constraint':len(dc),'d_topological':len(dt),'S_top':list(dt),'betti':b0}
R['B_T2']={'{2,3,8,9}@72':dims((2,3,8,9),72),'{2,3,8,9,14}@1008':dims((2,3,8,9,14),1008)}
print(R['B_T2'])
# B-T3 relaxed Betti vectors
ob={}
for c,m in [((2,3,4,5,6),4),((2,3,4,5,6,7),4),((2,3,4,5,8),32),((2,3,4,5,6,7),24)]:
    act=sorted({p for N in c for p in primes_of(N)})
    base=betti_with(c,m,act)
    rel={str(p):betti_with(c,m,[q for q in act if q!=p]) for p in act}
    # also: relaxing a passive prime (not active) changes nothing
    ob[f'{c}@{m}']={'active':act,'betti':base,'relax_one':rel,'cut_order_1':all(set(v[1:])=={0} and v[0]==1 for v in rel.values())}
R['B_T3']=ob
for k,v in ob.items(): print(k,v)
json.dump(R,open('../results/RESULTS_II_part8.json','w'),indent=1,default=str)
