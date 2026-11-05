import sys,json,os,itertools,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import *
from swaps import *
from rewrite import *
R={}
def Dset(m):
    out=set()
    d=2
    while d*d<=m:
        if m%(d*d)==0: out.add(d)
        d+=1
    return out
def Dfast(m):
    # d>=2 with d^2 | m  (d | s where s=sqrt-part) : compute via valuations
    ps=primes_of(m); q=1
    for p in ps: q*=p**(vp(m,p)//2)
    return {d for d in range(2,q+1) if q%d==0}
def churn(states):
    ds=set()
    for s in states: ds|=Dfast(s)
    out={}
    for d in ds:
        rho=[1 if (s%(d*d)==0) else 0 for s in states]
        V=sum(abs(rho[i+1]-rho[i]) for i in range(len(rho)-1))
        out[d]=(V-abs(rho[-1]-rho[0]))//2
    return out
# B-T8
bad=0;n=0
for a in range(0,9):
    for b in range(0,7):
        m=2**a*3**b
        for w in adm_perms((2,2,3,3,3,3),m):
            n+=1
            st=run(m,w); c=churn(st)
            if max(c.values(),default=0)<1: bad+=1
        h=run(m,(1,)*7); assert all(v==0 for v in churn(h).values())
R['B_T8']={'sources':'v2<=8,v3<=6','arrangement_cases':n,'violations':bad}
# B-T7 (i),(ii)
bad=0;n=0
hs=histories(72**2)
for s,w in hs[:400]:
    st=run(s,w); c=churn(st)
    for d,x in c.items():
        n+=1
        if x>len(w)//2: bad+=1
R['B_T7_i']={'cases':n,'violations':bad}
bad=0;n=0
for s,w in hs:
    for i in range(len(w)-1):
        if w[i]!=w[i+1]:
            v=w[:i]+(w[i+1],w[i])+w[i+2:]
            if run(s,v) is None: continue
            c1=churn(run(s,w));c2=churn(run(s,v))
            for d in set(c1)|set(c2):
                n+=1
                if abs(c1.get(d,0)-c2.get(d,0))>1: bad+=1
    if n>20000: break
R['B_T7_ii']={'cases':n,'violations':bad}
# B-T5: trace injectivity & Omega
def disp(N,ps=(2,3)): return tuple(delta(N,p) for p in ps)
def Omega(w):
    t=0
    for i in range(len(w)):
        for j in range(i+1,len(w)):
            a=disp(w[i]);b=disp(w[j]); t+=a[0]*b[1]-a[1]*b[0]
    return t
vals={}
ok=True
for w in perms((2,2,3,3,3,3)):
    inv=sum(1 for i in range(6) for j in range(i+1,6) if w[i]==3 and w[j]==2)
    if Omega(w)!=-7*(8-2*inv): ok=False
    vals[Omega(w)]=1
R['B_T5_Omega']={'formula_ok':ok,'values':sorted(vals)}
# swap changes Omega by d_a ^ d_b
bad=0
for w in perms((2,2,3,3,3,3)):
    for i in range(5):
        if w[i]!=w[i+1]:
            v=w[:i]+(w[i+1],w[i])+w[i+2:]
            a=disp(w[i]);b=disp(w[i+1])
            if Omega(v)-Omega(w)!=-2*(a[0]*b[1]-a[1]*b[0]): bad+=1
R['B_T5_swap']={'violations':bad}
# closure triangle area from (2,0)... path 1^7 from state 4 : (v2,v3)=(2,0); area between the two paths
def trace(m,w):
    pts=[(vp(m,2),vp(m,3))];
    for x in w:
        m=m//x*(x+1)**2; pts.append((vp(m,2),vp(m,3)))
    return pts
p1=trace(4,(1,)*7); p2=trace(4,(2,2,3,3,3,3))
poly=p1+p2[::-1][1:-1]
A=0
for i in range(len(poly)):
    x1,y1=poly[i];x2,y2=poly[(i+1)%len(poly)];A+=x1*y2-x2*y1
R['B_T5_triangle']={'p1':p1,'p2':p2,'twice_area':abs(A),'area':abs(A)/2}
# trace injectivity on histories of 72^2
tr={}
bad=0
for s,w in histories(72**2):
    k=tuple(run(s,w)); 
    if (s,k) in tr: bad+=1
    tr[(s,k)]=1
R['B_T5_trace_inj']={'histories':len(tr),'violations':bad}
# B-T6
vs={}
par=0
for N in range(1,401):
    ps=primes_of(N)+primes_of(N+1)
    v=tuple(sorted((p,delta(N,p)) for p in set(ps)))
    # normalise direction
    from math import gcd as g
    gg=0
    for _,x in v: gg=g(gg,abs(x))
    key=tuple((p,x//gg) for p,x in v)
    if key in vs: par+=1
    vs[key]=N
R['B_T6']={'labels':'1..400','parallel_pairs':par}
# B-T1 passive primes: dropping inactive prime constraint does not change admissibility
bad=0;n=0
import random
random.seed(5)
for _ in range(3000):
    c=tuple(random.choice(range(1,30)) for _ in range(random.randint(1,5)))
    act=set()
    for N in c: act|=set(primes_of(N))
    w=c; m=random.randint(1,4000)
    # admissibility via constraints on active primes only
    ok=True
    for p in act:
        s=0
        for N in w:
            s+=delta(N,p)
            if vp(m,p)+s<0: ok=False
    n+=1
    if ok!=(m%K(w)==0): bad+=1
R['B_T1']={'cases':n,'violations':bad}
# D-T4 faithfulness and Lemma L
bad=0;n=0
for t in (72,72**2):
    seqs={}
    for s,w in histories(t):
        f=(s,tuple(frozenset(Dfast(x)) for x in run(s,w)))
        if f in seqs: bad+=1
        seqs[f]=1
    n+=len(seqs)
R['D_T4_faithful']={'histories':n,'collisions':bad}
bad=0;n=0
for m in range(1,3000):
    adm=[N for N in range(1,60) if m%N==0]
    ds={}
    for N in adm:
        f=frozenset(Dfast(m//N*(N+1)**2))
        n+=1
        if f in ds: bad+=1
        ds[f]=N
R['D_T4_lemmaL']={'cases':n,'collisions':bad}
# D4-T9: births-losses
R['D4_T9_note']='births-losses = |D(end)|-|D(start)| (telescoping)'
# D4-T5 cube family counts
def cube_family(r):
    # histories from 4: r independent blocks A=1^7 or B=2^2 3^4(any admissible arrangement not required); here canonical block arrangement (2,2,3,3,3,3)
    ends=set();ct=0
    for bits in itertools.product((0,1),repeat=r):
        m=4;w=[]
        for b in bits: w+=list((2,2,3,3,3,3) if b else (1,)*7)
        st=run(4,tuple(w)); ends.add(st[-1]); ct+=1
    return ct,ends
R['D4_T5']={str(r):{'histories':cube_family(r)[0],'endpoints':[str(x) for x in cube_family(r)[1]],'expected':str(4**(7*r+1))} for r in (1,2,3)}
# D-T3(c): triples pairwise diamonds but no triple cell, m<400
cnt=0
for m in range(1,400):
    ls=[N for N in range(2,60)]
json.dump(R,open('../results/RESULTS_II_part4.json','w'),indent=1,default=str)
for k,v in R.items(): print(k,v if len(str(v))<200 else str(v)[:200])
