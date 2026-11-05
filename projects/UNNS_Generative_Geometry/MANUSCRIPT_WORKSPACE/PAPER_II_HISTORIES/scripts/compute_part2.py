"""Part 2 of the Paper II computations (stdlib only). Writes ../results/RESULTS_II_part2.json"""
import sys,json,time,os,random
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import *
from swaps import *
from topo import *
from rewrite import *
from math import lcm
from itertools import combinations
from collections import Counter
R={};t0=time.time()
def lg(*a): print(*a,round(time.time()-t0,1),flush=True)
# ---- feeding digraph / NF / F2
bad=0;n=0
for A in range(1,60):
    for B in range(1,60):
        if A==B or gcd(A+1,B)>1: continue
        for m in range(1,A*B+1):
            if m%K((A,B))==0:
                n+=1
                if m%K((B,A))!=0: bad+=1
R['NF']={'instances':n,'violations':bad}; lg('NF',n,bad)
def class_count_blocks(content,m):
    blocks=sccs(content); L=sorted(set(content)); E=feeding(content)
    bi={x:i for i,b in enumerate(blocks) for x in b}
    order=[];rem=set(range(len(blocks)))
    while rem:
        for i in sorted(rem):
            if not any((a,b) in E and bi[a]!=bi[b] and bi[b]==i and bi[a] in rem for a in L for b in L):
                order.append(i);rem.remove(i);break
    prod=1;cur=Fraction(m)
    for i in order:
        if cur.denominator!=1: return 0
        ci=tuple(x for x in content if bi[x]==i)
        prod*=len(swap_classes(ci,int(cur)))
        for x in ci: cur*=Fraction((x+1)**2,x)
    return prod
random.seed(7);bad=0;n=0
for _ in range(600):
    sz=random.randint(3,5); c=tuple(sorted(random.choice(range(2,16)) for _ in range(sz)))
    Pc=1
    for x in c:Pc*=x
    ks=sorted({K(w) for w in arrangements(c)})
    srcs={random.choice(ks)*random.choice((1,1,2,3,5,7)) for _ in range(4)}|{Pc}
    for m in srcs:
        n+=1
        a=len(swap_classes(c,m)); b=class_count_blocks(c,m)
        if a!=b: bad+=1
R['F2']={'pairs':n,'violations':bad}; lg('F2',n,bad)
# ---- three-label census and T3
def split_sources(c):
    cl=class_count_all_sources(c); return {m:k for m,k in cl.items() if k>=2}
def kappa(S):
    ps=set()
    for x in S: ps|=set(primes_of(x))|set(primes_of(x+1))
    k=1
    for p in ps:
        d=sum(delta(x,p) for x in S)
        if d<0: k*=p**(-d)
    return k
def t3_split(c,m):
    ps=[]
    for (a,b,cc) in set(permutations(c)):
        if a<cc and True or True:
            pass
    for (a,b,cc) in permutations(c):
        if a>cc: continue
        if m%a==0 and m%cc==0 and m%kappa((a,b))==0 and m%kappa((b,cc))==0 and m%kappa((a,b,cc))==0 and m%b!=0 and m%kappa((a,cc))!=0: return True
    return False
cnt=0;tot=0;strong=0;bad=0
from itertools import combinations as C
splits=[]
for c in C(range(1,31),3):
    tot+=1
    if len(sccs(c))==1: strong+=1
    ss=split_sources(c)
    if ss: cnt+=1; splits.append(c)
    for m in class_count_all_sources(c):
        if (len(swap_classes(c,m))>=2)!=t3_split(c,m): bad+=1
R['three_label']={'contents':tot,'strongly_connected':strong,'split':cnt,'t3_violations':bad,'examples_split':[list(c) for c in splits[:12]]}
lg('3label',tot,strong,cnt,bad)
# {2,3,N}
fam=[]
okfam=True
for N in range(4,401):
    if N in (2,3): continue
    ss=split_sources((2,3,N))
    pred_=(N%6 in (2,3)) and N>=8
    if bool(ss)!=pred_: okfam=False
    if ss and min(ss)!=N: okfam=False
    if ss: fam.append(N)
R['family_2_3_N']={'range':[4,400],'count_split_N':len(fam),'criterion_holds':okfam,'first':fam[:10]}
lg('family',len(fam),okfam)
# {2,3,N} strongly connected iff N=2,3 mod 6
R['family_scc_ok']=all((len(sccs((2,3,N)))==1)==(N%6 in (2,3)) for N in range(4,601))
# ---- complexes
def cx(c,m):
    pc,pb=perm_complex(c,m); cc,cb=cubical_complex(c,m)
    return {'content':list(c),'source':m,'perm_f':pc,'perm_betti':pb,'cub_f':cc,'cub_betti':cb,'n_adm':pc[0]}
R['cx']={'a':cx((2,3,8,9),72),'b':cx((2,3,8,9,14),1008)}
# d^2=0 sanity inside topo via rank: recompute with check
R['cx']['lower_set']=cx((2,3,4),12) if False else None
# ---- complementary-pair sphere test: contents with k labels, E,O complementary antipodal arrangement pair and nothing else admissible among... 
sph=[]
for c,m in [((2,3,8),8),((2,3,14),14),((2,3,8,9),8)]:
    sph.append({'content':list(c),'m':m,'perm_f':perm_complex(c,m)[0],'perm_betti':perm_complex(c,m)[1],'adm':[list(w) for w in adm_set(c,m)]})
R['sphere_tests']=sph
# ---- B-T3 obstructions
def cc_(c,m): return len(swap_classes(c,m))
ob={}
for c,m in [((2,3,4,5,6),4),((2,3,4,5,6,7),4)]:
    ps=sorted({p for x in c for p in primes_of(x)}|{p for x in c for p in primes_of(x+1)})
    ob[str(c)+'@'+str(m)]={'m':m,'comps':cc_(c,m),'relax':{str(p):cc_(c,m*p**10) for p in ps}}
for c,m in [((2,3,4,5,8),32),((2,3,4,5,6,7),24)]:
    ps=sorted({p for x in c for p in primes_of(x)}|{p for x in c for p in primes_of(x+1)})
    ob[str(c)+'@'+str(m)]={'m':m,'betti':perm_complex(c,m)[1],'relax':{str(p):perm_complex(c,m*p**10)[1] for p in ps}}
R['irreducible']=ob; lg('irred')
# ---- kernel
R['kernel']={'V':[[delta(N,p) for N in (1,2,3)] for p in (2,3)],'vec':[7,-2,-4],
  'h1':run(4,(1,)*7),'h2':run(4,(2,2,3,3,3,3)),'n_adm_2234':len(adm_perms((2,2,3,3,3,3),4)),
  'all_adm_2234':[list(w) for w in adm_perms((2,2,3,3,3,3),4)],
  'K_u':K((1,)*7),'K_v':min(K(w) for w in perms((2,2,3,3,3,3))),'mult_equal':str(mult((1,)*7))+'='+str(mult((2,2,3,3,3,3)))}
R['kernel']['mult_equal_bool']=mult((1,)*7)==mult((2,2,3,3,3,3))
# kernel minimal-source antichain test: block replacement criterion
bad=0;n=0
for _ in range(3000):
    u=tuple(random.choice((1,2,3,8)) for _ in range(random.randint(1,4)))
    # find v of same multiplier among small words
    vs=[v for v in [tuple(random.choice((1,2,3,8)) for _ in range(random.randint(1,7))) for _ in range(40)] if mult(v)==mult(u) and sorted(v)!=sorted(u)]
    for v in vs[:2]:
        pre=tuple(random.choice((1,2,3,8)) for _ in range(random.randint(0,2))); suf=tuple(random.choice((1,2,3,8)) for _ in range(random.randint(0,2)))
        for x in random.sample(range(1,5000),25):
            n+=1
            a=(run(x,pre+u+suf) is not None) and (run(x,pre+v+suf) is not None)
            mid=run(x,pre)
            if mid is None: continue
            lhs=a
            rhs=(mid[-1]%lcm(K(u),K(v))==0) and run(x,pre+u+suf) is not None and run(x,pre+v+suf) is not None
            if lhs and not rhs: bad+=1
            # block-level claim: with state y after pre, u and v both admissible iff lcm | y
            y=mid[-1]
            if ((run(y,u) is not None) and (run(y,v) is not None))!=(y%lcm(K(u),K(v))==0): bad+=1
R['block_criterion']={'tests':n,'violations':bad}; lg('block',n,bad)
# ---- F_j table
tab=[];badF=0
for j in range(1,7):
    U=(2,)*4+(3,)*j; V=(1,8,8)+(3,)*j
    for a in range(0,7):
        for b in range(0,j+1):
            m=2**a*3**b
            if adm_perms(U,m) and adm_perms(V,m):
                comps,nv=space_components(m,[U,V],[((2,2,2,2),(1,8,8))])
                pred_=1 if (b>=1 or a>=4) else 2
                if comps!=pred_: badF+=1
                tab.append((j,a,b,comps,nv))
R['Fj']={'cases':len(tab),'violations':badF,'sample':[t for t in tab if t[0]==2]}
lg('Fj',len(tab),badF)
# saturation bound vs true threshold
R['Fj_thresholds']={'saturation_bound':'2^6 3^j','true_connected_iff':'b>=1 or a>=4 (minimal sources 2^4, 3)','P_U':'2^4 3^j','P_V':'2^6 3^j'}
# ---- D4-T7c
rels={'z1':((2,2,2,2),(1,8,8)),'z2':((1,)*7,(2,2,3,3,3,3)),'z3':((1,1,1,2),(3,3,8))}
assert mult((1,1,1,2))==mult((3,3,8))
t7=[]
for a in range(0,4):
    for b in range(0,3):
        m=2**a*3**b
        n12=space_components(m,[(1,1,1,2),(3,3,8)],[rels['z1'],rels['z2']])
        n3=space_components(m,[(1,1,1,2),(3,3,8)],[rels['z3']])
        t7.append({'a':a,'b':b,'with_z1_z2':n12,'with_z3':n3})
R['D4T7c']=t7
# ---- join example
def hist_graph(m,contents):
    V=set()
    for c in contents: V|=set(adm_perms(c,m))
    V=sorted(V); E=set()
    for w in V:
        for i in range(len(w)-1):
            if w[i]!=w[i+1]:
                v=w[:i]+(w[i+1],w[i])+w[i+2:]
                if v in V: E.add(tuple(sorted((w,v))))
    for w in V:
        for v in V:
            if w<v:
                i=0
                while i<min(len(w),len(v)) and w[i]==v[i]: i+=1
                j=0
                while j<min(len(w),len(v))-i and w[-1-j]==v[-1-j]: j+=1
                u=w[i:len(w)-j]; x=v[i:len(v)-j]
                if sorted(u)!=sorted(x) and mult(u)==mult(x): E.add((w,v))
    return V,E
def comps_of(V,E):
    par={w:w for w in V}
    def f(x):
        while par[x]!=x: par[x]=par[par[x]];x=par[x]
        return x
    for a,b in E: par[f(a)]=f(b)
    return len({f(w) for w in V})
jc=[(2,8,63),(5,9,35)]
jr={}
for m in (280,840):
    V,E=hist_graph(m,jc)
    sw=[e for e in E if sorted(e[0])==sorted(e[1])]
    cs=comps_of(V,sw)
    jr[str(m)]={'V':len(V),'swap_edges':len(sw),'swap_classes':cs,'all_edges':len(E),'rewrite_classes':comps_of(V,E),'b1':len(E)-len(V)+comps_of(V,E),'words':[list(w) for w in V],'edges':[[list(a),list(b)] for a,b in sorted(E)],'mult':str(mult((2,8,63)))+'='+str(mult((5,9,35)))}
R['join']=jr; lg('join',{k:(v['V'],v['swap_classes'],v['rewrite_classes'],v['b1']) for k,v in jr.items()})
# ---- R3-T3 family
fam=[]
for A in [(5,9),(5,9,3),(5,9,3,6)]:
    c=(2,4)+A; cl=swap_classes(c,4)
    E=run(4,cl[0][0])[-1]
    fam.append({'A':list(A),'endpoint':E,'components':len(cl),'sizes':[len(x) for x in cl],'I_values':[sorted({int(w.index(2)<w.index(4)) for w in x}) for x in cl],'adjacent_never':all(abs(w.index(2)-w.index(4))>1 for x in cl for w in x),'I_const_on_comps':all(len({w.index(2)<w.index(4) for w in x})==1 for x in cl)})
R['R3T3']=fam; lg('R3T3',fam)
# R3-T3 sweep: contents {2,4}+A, A subset of labels>=3, |A|<=3 labels in 3..12, endpoint all histories from source 4
sweep=Counter();inv_bad=0;two_vals=0;n=0
for k in (1,2,3):
    for A in C(range(3,13),k):
        c=(2,4)+A
        cl=swap_classes(c,4)
        if not cl: continue
        n+=1
        sweep[len(cl)]+=1
        for x in cl:
            if len({w.index(2)<w.index(4) for w in x})>1: inv_bad+=1
        if len({w.index(2)<w.index(4) for x in cl for w in x})>1: two_vals+=1
R['R3T3_sweep']={'contents':n,'component_hist':dict(sweep),'invariant_violations':inv_bad,'contents_with_both_values':two_vals,'A_range':'subsets of 3..12 of size 1-3'}
lg('sweep',R['R3T3_sweep'])
json.dump(R,open('../results/RESULTS_II_part2.json','w'),indent=1,default=str)
