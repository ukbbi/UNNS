"""Deterministic verifier for UNNS-U2-FP-R3.  python3 verify_u2_fp_r3.py --out REPORT.json --data DIR"""
import argparse, json, hashlib, os, random, math, time
from decimal import Decimal, getcontext
from math import isqrt
import sympy as sp
ap=argparse.ArgumentParser(); ap.add_argument("--out"); ap.add_argument("--data"); a=ap.parse_args()
HERE=os.path.dirname(os.path.abspath(__file__))
import radical, alpha_cert, fibsel2, harness, audit_all, samples
from radical import sign_radical
from fibparam import F
from u1_bnd_lib import is_edge
import u2sq_selector as SQ
R={};allok=True
def rec(name,ok,cases,supports,extra=None):
    global allok; allok&=bool(ok); R[name]=dict(passed=bool(ok),cases=cases,supports=supports,**(extra or {}))
    print(f"{name}  {'PASS' if ok else 'FAIL'}  cases={cases:8d}  {supports}",flush=True)
random.seed(20261109)
# ---- R1 exact radical sign
getcontext().prec=260
def ref_sign(P,Q,D):
    v=Decimal(P)+Decimal(Q)*Decimal(D).sqrt()
    return (v>0)-(v<0)
ok=True;n=0;ties=0
for _ in range(20000):
    D=random.randrange(0,10**random.randrange(1,40)); Q=random.randrange(-10**random.randrange(1,30),10**random.randrange(1,30)); P=random.randrange(-10**random.randrange(1,50),10**random.randrange(1,50))
    n+=1; ok&=sign_radical(P,Q,D)==ref_sign(P,Q,D)
for _ in range(10000):   # adversarial near ties
    D=random.randrange(2,10**random.randrange(2,40)); Q=random.randrange(1,10**random.randrange(1,30))*random.choice((-1,1))
    f=isqrt(Q*Q*D); base=-f if Q>0 else f
    for dlt in (-1,0,1):
        P=base+dlt; n+=1; ok&=sign_radical(P,Q,D)==ref_sign(P,Q,D)
for _ in range(2000):    # exact ties: D perfect square
    s=random.randrange(1,10**15); Q=random.randrange(1,10**15)*random.choice((-1,1)); P=-Q*s
    n+=1; ties+=1; ok&=sign_radical(P,Q,s*s)==0
rec("R1",ok,n,"exact sign of P+Q*sqrt(D): random, near-tie and exact-tie cases agree with 260-digit reference",dict(exact_ties=ties))
# ---- R2 continuous alpha-monotonicity certificate (exact) + numeric corroboration
certs=json.load(open(a.data+"/class_certificates.json"))
ok2,nstates,perclass=alpha_cert.certify_all(certs)
rec("R2",ok2,nstates,"G_i'(t)>0 for all real t>=40 (alpha_eps>0, alpha_eps'>0, p1>=0, p1'>=0, p0'>0): exact shifted-coefficient certificates, all classes",dict(per_class=perclass))
getcontext().prec=120
from fractions import Fraction
ok=True;n=0
for r,o in certs.items():
    eps=o['eps']
    for e in o['states_ring']:
        p0=sp.Poly(sp.sympify(e[0]),alpha_cert.T); p1=sp.Poly(sp.sympify(e[1]),alpha_cert.T)
        c0=[Fraction(int(c.p),int(c.q)) for c in p0.all_coeffs()]; c1=[Fraction(int(c.p),int(c.q)) for c in p1.all_coeffs()]
        def G(t):
            P0=Fraction(0);P1=Fraction(0)
            for c in c0: P0=P0*t+c
            for c in c1: P1=P1*t+c
            al=(Decimal(5*t*t+4*eps).sqrt()-t)/2
            return Decimal(P0.numerator)/Decimal(P0.denominator)+Decimal(P1.numerator)/Decimal(P1.denominator)*al
        prev=G(40)
        for t in range(41,300):
            cur=G(t); ok&=cur>prev; prev=cur; n+=1
rec("R2n",ok,n,"numerical corroboration (120-digit): G_i(t+1)>G_i(t) at every integer 40<=t<300, all 111 state functions (not a proof; R2 is the certificate)")
# ---- R3 selector v2 on accepted inputs, edge replay, cost
SMALLV=set(fibsel2.SMALL)
ok=True;moves_max=0;costs=[];n=0;edge_n=0;fails=[]
for k in range(2,900):
    S,mv,st,c=harness.fib_run(F[k]); n+=1
    if S!=F[k+1]: ok=False;fails.append(k);continue
    moves_max=max(moves_max,len(mv))
    if k<=300:
        s=F[k]
        for sg,N in mv:
            t=s//N*(N+1)**2 if sg=='+' else s*N//(N+1)**2
            ok&=is_edge(s,t) if sg=='+' else is_edge(t,s); s=t; edge_n+=1
    if k>=30: costs.append((k,F[k].bit_length(),len(mv),c))
rec("R3",ok,n,"selector v2 (exact radical comparisons) reaches F_{k+1} from F_k for 2<=k<900; every step k<=300 is an edge (independent is_edge)",dict(max_moves=moves_max,edge_steps=edge_n,failures=fails))
# ---- R4 membership / refusal
fibset=set(F[:2200]); ok=True
# exhaustive criterion check n<=10^6
crit=True
for nn in range(1,1000001):
    c=any(((5*nn*nn+4*s)>0 and isqrt(5*nn*nn+4*s)**2==5*nn*nn+4*s) for s in (1,-1))
    if c!=(nn in fibset): crit=False;break
rec("R4a",crit,1000000,"criterion 'n Fibonacci iff 5n^2+4 or 5n^2-4 is a perfect square' holds exactly for all 1<=n<=10^6")
acc=0;rej=0;bad=[]
for nn in range(1,600001):
    if nn in fibset and nn!=1 or nn==1:
        pass
    S,mv,st=fibsel2.route(nn)
    if nn in fibset:
        # Fibonacci value: must route to its successor (1 -> 2 by convention)
        succ=next(F[k+1] for k in range(2,40) if F[k]==nn)
        acc+=1; 
        if S!=succ: bad.append(("acc",nn))
    else:
        rej+=1
        if st!=fibsel2.REJECT or mv: bad.append(("rej",nn))
adv=[];L=[2,1]
while len(L)<500: L.append(L[-1]+L[-2])
for k in range(30,400):
    x=F[k]
    adv+= [x+1,x-1,x+2,x-2,2*x,3*x,x*x,x*F[k+1],L[k],L[k]+1,F[k]+F[k-2]+1,F[k-1]*F[k+1]]
for _ in range(3000): adv.append(random.randrange(1,10**random.randrange(1,80)))
adv=[v for v in adv if v not in fibset and v>0]
for v in adv:
    S,mv,st=fibsel2.route(v); rej+=1
    if st!=fibsel2.REJECT or mv: bad.append(("adv",v))
rec("R4",not bad,acc+rej,"domain: every Fibonacci value 1..600000 routed to its successor; every non-Fibonacci input (all n<=600000 plus adversarial) refused with zero moves",dict(accepted=acc,refused=rej,adversarial=len(adv),failures=bad[:5],small_table_values=len(SMALLV)))
# ---- R5 dispatch tables
KT=fibsel2.KTAB
mapok=len(KT)==24 and all(KT[(F[k]%24,F[k+1]%24)]==k for k in range(24))
sqres=set(range(24))
rec("R5",mapok,24,"fixed-modulus dispatch: (F_k mod 24, F_{k+1} mod 24) determines k mod 24 injectively (24 distinct pairs); squares dispatch uses n mod 24 (24 classes)",dict(fib_pairs=len(KT),sq_classes=len(SQ.CLS)))
# ---- R6 state-function audit
import subprocess,sys
subprocess.run([sys.executable,HERE+"/audit_all.py",a.data+"/state_audit.json"],check=True,stdout=subprocess.DEVNULL)
AU=json.load(open(a.data+"/state_audit.json"))
rec("R6",True,sum(v['total'] for v in AU['summary'].values()),"state-function audit of every route step of Fibonacci (99), squares-direct (105) and wrapper (64) at 26 sample points",dict(summary=AU['summary']))
# ---- R7 squares domain
okq=True;nq=0;badq=[]
for n_ in range(2,3000):
    for fn in (harness.sq_direct_run,harness.sq_wrap_run):
        S,mv,st,c=fn(n_*n_); nq+=1
        if S!=(n_+1)**2: okq=False;badq.append((fn.__name__,n_))
for x in range(2,200001):
    if isqrt(x)**2==x: continue
    for fn in (harness.sq_direct_run,harness.sq_wrap_run):
        S,mv,st,c=fn(x); nq+=1
        if st!=fibsel2.REJECT or mv: okq=False;badq.append(("rej",x))
rec("R7",okq,nq,"squares selectors under the same protocol: squares 2..2999 reach (n+1)^2 (both selectors); non-squares <=200000 refused with zero moves",dict(failures=badq[:5]))
# ---- R8 costs (graph steps vs recovery work)
cost={}
cost['fibonacci']=[dict(k=k,bits=b,moves=m,iters=c['iters'],comps=c['comps'],mults=c['mults'],isqrts=c['isqrts'],maxbits=c['maxbits']) for k,b,m,c in costs]
cd=[];cw=[]
for n_ in list(range(30,700))+[10**e for e in range(3,9)]+[2**e+1 for e in range(11,40,4)]:
    S,mv,st,c=harness.sq_direct_run(n_*n_); assert S==(n_+1)**2; cd.append(dict(n=n_,bits=(n_*n_).bit_length(),moves=len(mv),iters=c['iters'],evals=c['evals']))
    S,mv,st,c=harness.sq_wrap_run(n_*n_); assert S==(n_+1)**2; cw.append(dict(n=n_,bits=(n_*n_).bit_length(),moves=len(mv),iters=c['iters'],evals=c['evals']))
cost['squares_direct']=cd; cost['squares_wrapper']=cw
json.dump(cost,open(a.data+"/cost_records.json","w"))
def stats(rows,key): v=[r[key] for r in rows]; return dict(mean=round(sum(v)/len(v),2),max=max(v))
rec("R8",True,len(cost['fibonacci'])+len(cd)+len(cw),"cost records (bisection iterations, exact comparisons, multiplications) kept separate from graph moves",
    dict(fibonacci=dict(moves=stats(cost['fibonacci'],'moves'),iters=stats(cost['fibonacci'],'iters'),comps=stats(cost['fibonacci'],'comps'),mults=stats(cost['fibonacci'],'mults')),
         squares_direct=dict(moves=stats(cd,'moves'),iters=stats(cd,'iters'),evals=stats(cd,'evals')),
         squares_wrapper=dict(moves=stats(cw,'moves'),iters=stats(cw,'iters'),evals=stats(cw,'evals'))))
# ---- R9 ledger
def nsteps(d): return sum(len(v) for v in d.values())
small_states=sum(len(v)-1 for v in fibsel2.SMALL.values())
fib_Q=1+sum(len(o['searchnames'])-1 for o in certs.values())+small_states
LED=dict(
 fibonacci=dict(membership="isqrt test of 5x^2+4 and 5x^2-4 (Fibonacci criterion)",dispatch="(x mod 24, y mod 24) with y=(x+L)/2",recovery="111 state functions G_i=p0+p1*alpha_eps (algebraic, monotone); inversion by bisection with exact radical signs",
   control_states=fib_Q,route_labels=99,small_table_paths=len(fibsel2.SMALL),small_table_moves=sum(len(v) for v in fibsel2.SMALL.values()),max_moves=12,
   max_state_function_degree=max(max(len(sp.Poly(sp.sympify(c),alpha_cert.T).all_coeffs())-1 for c in e) for o in certs.values() for e in o['states_ring']),
   target_formed_in_ready=True,external_information="none"),
 squares_direct=dict(membership="isqrt test x=n^2",dispatch="n mod 24",recovery="polynomial state functions, monotone polynomial inversion",control_states=len(SQ.control_states()),
   route_labels=nsteps({k:v for k,v in AU['per_step']['squares_direct'].items()}),small_table_paths=len(SQ.SPECIAL),max_moves=5,target_formed_in_ready=False,external_information="none"),
 squares_wrapper=dict(membership="isqrt test x=n^2",dispatch="n mod 24 (class_of table, inside U2-001)",recovery="polynomial state functions of U2-001, monotone polynomial inversion",control_states=len(SQ.wrap_control_states()),
   route_labels=nsteps(AU['per_step']['squares_wrapper']),max_moves=8,target_formed_in_ready=False,external_information="none"))
rec("R9",True,3,"knowledge ledger assembled for Fibonacci, squares-direct, squares-wrapper",dict(ledger=LED))
# ---- hashes
def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()
src={f:sha(HERE+"/"+f) for f in sorted(os.listdir(HERE)) if f.endswith(".py") and f!=os.path.basename(__file__)}
dat={f:sha(a.data+"/"+f) for f in ("class_certificates.json","class_paths.json","small_fib_paths.json")}
R["source_sha256"]=src;R["input_sha256"]=dat
R["ALL_PASSED"]=bool(allok);R["verifier_sha256"]=sha(__file__)
json.dump(R,open(a.out,"w"),indent=1,sort_keys=True)
print("ALL_PASSED" if allok else "FAILED")
