"""Computes every number cited in Paper II; writes ../results/RESULTS_II.json. stdlib only."""
import sys,json,time,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import *
from swaps import *
from topo import *
from rewrite import *
from math import lcm
R={}
t0=time.time()
# --- HII-1 ancestry
R['hist72']=[{'source':s,'word':list(w),'states':run(s,w)} for s,w in sorted(histories(72))]
R['H72r']=[H(72**r) for r in range(1,7)]
from math import comb
R['H72r_lower']=[comb(2*r,r) for r in range(1,7)]
R['H_small']={str(t):H(t) for t in (1,2,4,8,12,16,18,24,36,48,72,144,216)}
# predecessor graph of 72 (depth)
def pgraph(t,seen=None,E=None):
    seen=seen if seen is not None else set(); E=E if E is not None else []
    if t in seen: return seen,E
    seen.add(t)
    for d,s in pred(t): E.append((s,t,d-1)); pgraph(s,seen,E)
    return seen,E
S,E=pgraph(72); R['pred72']={'nodes':sorted(S),'edges':sorted(E)}
# --- valuation trajectories & thresholds
def traj(w,ps):
    out={}
    for p in ps:
        s=0;tr=[0]
        for N in w: s+=delta(N,p);tr.append(s)
        out[p]=tr
    return out
R['traj']={'w1':{'word':[2,3,14],'K':K((2,3,14)),'tr':traj((2,3,14),(2,3,7))},
           'w2':{'word':[14,3,2],'K':K((14,3,2)),'tr':traj((14,3,2),(2,3,7))},
           'w3':{'word':[3,14,2],'K':K((3,14,2)),'tr':traj((3,14,2),(2,3,7))}}
R['K_all_2_3_14']={str(w):K(w) for w in arrangements((2,3,14))}
# diamond criterion
bad=0;n=0
for A in range(1,40):
    for B in range(1,40):
        if A==B: continue
        for m in range(1,200):
            n+=1
            ok=(m%K((A,B))==0 and m%K((B,A))==0)
            if ok!=(m%(A*B)==0): bad+=1
        assert K((A,B))==A*B//gcd(B,(A+1)**2)
R['diamond']={'cases':n,'violations':bad}
# commutative-numerical but not admissible example
R['num_comm']={'A':2,'B':3,'m':2,'adm_AB':run(2,(2,3)) is not None,'adm_BA':run(2,(3,2)) is not None}
# saturation test
bad=0;n=0
for c in [(2,3,4),(2,3,5),(2,3,8,9),(2,6,9),(3,4,7,8)]:
    P=1
    for x in c:P*=x
    for m in (P,2*P,P*5):
        n+=1
        if len([w for w in arrangements(c) if m%K(w)==0])!=len(arrangements(c)): bad+=1
R['saturation']={'cases':n,'violations':bad}
# gcd reduction
bad=0;n=0
for c in [(2,3,14),(2,3,8,9),(4,5,6)]:
    P=1
    for x in c:P*=x
    for m in range(1,3*P,7):
        n+=1
        if [w for w in arrangements(c) if m%K(w)==0]!=[w for w in arrangements(c) if gcd(m,P)%K(w)==0]: bad+=1
R['gcd_reduction']={'cases':n,'violations':bad}
# --- swaps: source-14 example
R['src14']={'content':[2,3,14],'classes_at_14':swap_classes((2,3,14),14),
            'hist_14_3_2':run(14,(14,3,2)),'hist_2_3_14':run(14,(2,3,14)),
            'class_counts':class_count_all_sources((2,3,14)),
            'q_table':{str(q):len(swap_classes((2,3,14),14*q)) for q in range(1,31)}}
# 72^r classes and cubes
def classes_and_cubes(t,want_cubes=True):
    hs=histories(t); hset=set(hs); idx={h:i for i,h in enumerate(hs)}
    par=list(range(len(hs)))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    maxc=0
    for (s,w) in hs:
        legal=[]
        for i in range(len(w)-1):
            if w[i]!=w[i+1]:
                v=(s,w[:i]+(w[i+1],w[i])+w[i+2:])
                if v in hset:
                    par[f(idx[(s,w)])]=f(idx[v]); legal.append(i)
        # max set of pairwise non-overlapping legal positions (greedy is optimal on a path)
        c=0;last=-5
        for i in legal:
            if i>last+1: c+=1;last=i
        maxc=max(maxc,c)
    return len(hs),len({f(i) for i in range(len(hs))}),maxc
R['72r']={}
for r in (1,2,3):
    a=classes_and_cubes(72**r); R['72r'][str(r)]={'histories':a[0],'classes':a[1],'maxcube':a[2]}
    print(r,a,time.time()-t0,flush=True)
json.dump(R,open('../results/RESULTS_II_part1.json','w'),indent=1,default=str)
