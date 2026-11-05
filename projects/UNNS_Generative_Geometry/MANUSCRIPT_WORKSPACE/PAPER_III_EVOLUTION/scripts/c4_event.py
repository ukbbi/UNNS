import sys, json, time; sys.path.insert(0,'.')
from eng3 import *
R={}
# ---- next-event law vs brute force
def stage(x0):
    x0=Fr(x0); D0=Dset(x0); L,G=LG(D0); a,b=x0.numerator,x0.denominator; assert G%b==0 and gcd(L,G)==1
    return D0,L,G,a,b,G//b
def solve(c,rhs,m):
    c%=m; rhs%=m; g=gcd(c,m)
    if rhs%g: return None
    m2=m//g
    return 0 if m2==1 else (rhs//g)*pow(c//g,-1,m2)%m2
def sieve_event(x0,jmax=10**6):
    D0,L,G,a,b,h=stage(x0); Y0=a*h; best=None; arg=[]
    dmax=isqrt(Y0+jmax*L*L)
    for d in range(2,dmax+1):
        if d in D0: continue
        q=Q(d,G); c=L*L%q
        j=solve(L*L,-Y0,q)
        if j is None: continue
        if j==0: j=q//gcd(L*L,q) if q//gcd(L*L,q)>0 else 1
        if j>jmax: continue
        # j must be least j>=1
        if best is None or j<best: best,arg=j,[d]
        elif j==best: arg.append(d)
    if best is None: return None
    Y=Y0+best*L*L
    new=sorted(d for d in range(2,isqrt(Y)+1) if d not in D0 and Y%Q(d,G)==0)
    return best,new
def brute_event(x0,jmax=10**6):
    x=Fr(x0); D0=Dset(x); L,G=LG(D0)
    for j in range(1,jmax+1):
        x=x+Fr(L*L,G); D=Dset(x)
        if D!=D0: return j,[d for d in D if d not in D0]

tests=[]; ok=0; bad=0
cases=[Fr(3025,3),Fr(1525761721,7)]
for l in (5,7,11,13):
    d=json.load(open('../results/census_l%d.json'%l))
    for S in sorted({r['S'] for r in d['rows']})[:12]: cases.append(Fr(S*S,l))
t0=time.time()
for x0 in cases:
    if not Dset(x0): continue
    b=brute_event(x0,200)
    if b is None: continue
    D0_,L_,G_,a_,b_,h_=stage(x0)
    if isqrt(a_*h_+b[0]*L_*L_)>30000: continue
    s=sieve_event(x0,b[0])
    good=(s is not None and s[0]==b[0] and s[1]==b[1]); ok+=good; bad+=(not good)
    tests.append({'x0':str(x0),'tau':b[0],'new':b[1],'ok':good})
R['next_event']={'n':len(tests),'ok':ok,'bad':bad,'tests':tests}
print('next event',len(tests),ok,bad,time.time()-t0,flush=True)
def predict_graph(D,N):
    D=sorted(D); Dn=sorted(set(D)|set(N)); E=edges(D); N=set(N)
    pierced={(u,v) for (u,v) in E if any(w%gcd(u,v)==0 and lcm(u,v)%w==0 for w in N)}
    pts=set(Dn)|{1}; newE=set()
    for w in N:
        for u in Dn:
            if u==w: continue
            a,b=min(u,w),max(u,w)
            if (a,b) in newE: continue
            g=gcd(a,b); l=lcm(a,b)
            if not any(z!=a and z!=b and z%g==0 and l%z==0 for z in pts): newE.add((a,b))
    surv=(E-pierced)|newE
    return len(surv)-len(Dn)+ncomp(Dn,surv), len(pierced), len(newE)
cnt=good=0; fails=[]
for l in (5,7,11,13):
    d=json.load(open('../results/census_l%d.json'%l)); cache={}
    for r in d['rows']:
        S=r['S']; n=r['n']
        if len(r['f'])>2 and any(r['f'][2:]): continue
        if len(r['f2'])>2 and any(r['f2'][2:]): continue
        key=(l,S)
        if key not in cache:
            cur=Fr(S*S,l); Ds=[]
            for k in range(25):
                D=Dset(cur); Ds.append(tuple(D))
                if not D: break
                L,G=LG(D); cur=cur+Fr(L*L,G)
            cache[key]=Ds
        Ds=cache[key]; D=Ds[n]; D2=Ds[n+1]; N=[x for x in D2 if x not in D]
        pb,_,_=predict_graph(D,N); cnt+=1
        E=edges(D); b1_old=len(E)-len(D)+ncomp(D,E)
        okk=(pb==r['b2'][1]) and (b1_old==r['b'][1]); good+=okk
        if not okk: fails.append((l,S,n))
R['graph_level']={'n':cnt,'ok':good,'fails':fails}
print('graph level',cnt,good,fails[:5],flush=True)
json.dump(R,open('../results/c4_event.json','w'))
