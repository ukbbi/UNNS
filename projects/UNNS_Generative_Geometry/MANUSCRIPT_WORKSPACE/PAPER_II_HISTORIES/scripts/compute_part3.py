import sys,json,os,time,random
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import *
from swaps import *
from topo import *
from itertools import combinations as C
R={};t0=time.time()
def kappa(S):
    ps=set()
    for x in S: ps|=set(primes_of(x))|set(primes_of(x+1))
    k=1
    for p in ps:
        d=sum(delta(x,p) for x in S)
        if d<0:k*=p**(-d)
    return k
def infeasible(c,m): 
    out=[]
    for r in range(1,len(c)):
        for S in C(c,r):
            if m%kappa(S): out.append(tuple(S))
    return out
# T-DUAL check (k=4, 5): reduced b_{k-3} = components of N(R) - 1
def nerve_components(c,m):
    labs=tuple(sorted(c));A=[w for w in permutations(labs) if m%K(w)==0]
    Rr=[w for w in permutations(labs) if m%K(w)!=0]
    par={w:w for w in Rr}
    def f(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    pre={}
    for w in Rr:
        for j in range(1,len(w)): pre.setdefault(frozenset(w[:j]),[]).append(w)
    for ws in pre.values():
        for x in ws[1:]: par[f(x)]=f(ws[0])
    return len(A),len({f(w) for w in Rr})
bad=0;n=0;pats=0
for k,lab,cap in ((4,range(2,15),130),(5,range(2,12),25)):
    cs=list(C(lab,k));random.seed(k);random.shuffle(cs)
    for c in cs[:cap]:
        ks=sorted({K(w) for w in permutations(c)})
        from math import lcm
        cl=set(ks);ch=True
        while ch:
            ch=False
            for a in list(cl):
                for b in ks:
                    l=lcm(a,b)
                    if l not in cl and len(cl)<400: cl.add(l);ch=True
        for m in sorted(cl):
            nA,cR=nerve_components(c,m)
            if nA==0 or cR==0: continue
            f_,b=perm_complex(c,m); b=b+[0]*(k+1-len(b))
            n+=1
            if b[k-3]!=cR-1 and not(k==3): bad+=1
            # b_{k-2}=0 means index k-2 absent/zero
            if len(b)>k-2 and b[k-2]!=0: bad+=1
R['T_DUAL']={'complexes':n,'violations':bad,'k':[4,5],'note':'reduced b_{k-3} vs components of N(R) minus 1; b_{k-2}=0'}
print('dual',n,bad,time.time()-t0,flush=True)
# T-LOWER: acyclic feeding -> contractible
bad=0;n=0
for c in C(range(1,16),4):
    if any(len(b)>1 for b in sccs(c)): continue
    ks=sorted({K(w) for w in permutations(c)})
    for m in ks[:6]:
        f_,b=perm_complex(c,m) if any(m%K(w)==0 for w in permutations(c)) else ([],[])
        if not f_: continue
        n+=1
        if b!=[1]+[0]*(len(b)-1): bad+=1
    if n>300: break
R['T_LOWER']={'complexes':n,'violations':bad,'k':4}
print('lower',n,bad,time.time()-t0,flush=True)
# T-SPHERE family
rows=[];bad=0
X_all=[8,9,14,15,20,21]
for r in (1,2,3):
    for X in C(X_all,r):
        c=(2,3)+X; m=1
        for x in X:m*=x
        inf=infeasible(c,m)
        Ev={x for x in c if x%6==2};Od={x for x in c if x%6==3}
        ok=sorted(map(tuple,map(sorted,inf)))==sorted([tuple(sorted(Ev)),tuple(sorted(Od))])
        f_,b=perm_complex(c,m); b=b+[0]*(len(c)+1-len(b))
        k=len(c);exp=[0]*k
        exp=[1]+[0]*(k-1); exp[k-3]+=1
        if k==3: exp=[2,0,0]
        good=(b[:k]==exp)
        rows.append({'content':list(c),'m':m,'infeasible_exact_E_O':ok,'betti':b})
        if not ok or not good: bad+=1
R['T_SPHERE']={'rows':rows,'violations':bad}
print('sphere',len(rows),bad,[ (r['content'],r['betti']) for r in rows][:6],flush=True)
# Four-label loop family: {2,3,N,M} at NM
lf=[];bad=0
for N in range(4,40):
    for M in range(N+1,40):
        has=False
        for m in (N*M,):
            c=(2,3,N,M)
            if any(m%K(w)==0 for w in permutations(c)):
                f_,b=perm_complex(c,m)
                if len(b)>1 and b[1]>0: has=True
        pred=(N>=8 and N%6 in (2,3) and M%6 in (2,3))
        if has!=pred and N>=8: pass
        if pred and not has: bad+=1
R['loop_family_at_NM_forward']={'violations_of_forward_direction':bad,'range':'8<=N<M<40, N,M = 2,3 mod 6'}
print('loopfam',bad,flush=True)
json.dump(R,open('../results/RESULTS_II_part3.json','w'),indent=1,default=str)
