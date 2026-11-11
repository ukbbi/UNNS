"""Generative Knowledge Audit: per-step knowledge category for the Fibonacci selector, the direct squares selector (U2-SQ) and the 45-state wrapper.
Categories (first match wins):
  const     label is the same constant for all sample points
  local     label = poly(deg<=3) in the current state S_before            -> computable with NO parameter recovery
  algstate  algebraic relation P(N,S_before)=0 of degrees <= (2,2): computable from the current state with a fixed-order root, no recovery
  field     label in the route-start field (Fib: Q[x0,L_k]; squares: Q[n], n=isqrt(x0); wrapper: Q[m] with m = state after the first move)
  target    label = poly(deg<=3) in S_after only                           -> needs the destination state
  unexplained  none of the above found in this vocabulary (NOT a necessity claim)"""
import json,sys
from math import isqrt
from audit_state import newton_ok,alg_relation,in_field
from samples import fib_samples,sq_direct_samples,wrapper_samples
def poly_in(V,Ns,dmax=3):
    if len(set(V))!=len(V): return None
    for d in range(1,dmax+1):
        if newton_ok(V,Ns,d): return d
def step_record(Ns,Sb,Sa,fieldfn):
    if len(set(Ns))==1: return dict(cat="const")
    d=poly_in(Sb,Ns)
    if d: return dict(cat="local",deg=d)
    r=alg_relation(Ns,Sb)
    if r and max(r)<=2: return dict(cat="algstate",deg=list(r))
    f=fieldfn(Ns)
    if f is not None: return dict(cat="field",deg=f)
    d=poly_in(Sa,Ns)
    if d: return dict(cat="target",deg=d)
    return dict(cat="unexplained")
def lucas_of(x):
    t=5*x*x+4; r=isqrt(t)
    return r if r*r==t else isqrt(5*x*x-4)
def run_family(name,samples_by_class,fieldmaker):
    out={}
    for c,smp in samples_by_class.items():
        m=len(smp[0]['steps']); recs=[]
        for i in range(m):
            Ns=[s['steps'][i][1] for s in smp]; Sb=[s['steps'][i][2] for s in smp]; Sa=[s['steps'][i][3] for s in smp]
            recs.append(step_record(Ns,Sb,Sa,fieldmaker(smp,i)))
        out[str(c)]=recs
    return out
def fib_field(smp,i):
    Xs=[s['x0'] for s in smp]; Ls=[lucas_of(x) for x in Xs]
    return lambda Ns: in_field(Ns,Xs,Ls,maxd=9)
def sq_field(smp,i):
    ns=[isqrt(s['x0']) for s in smp]; return lambda Ns: poly_in(ns,Ns,4)
def wrap_field(smp,i):
    if i==0: return lambda Ns: None
    ms=[s['steps'][1][2] for s in smp]; return lambda Ns: poly_in(ms,Ns,4)
def summarize(res):
    from collections import Counter
    C=Counter(r['cat'] for v in res.values() for r in v); return dict(C),sum(C.values())
if __name__=="__main__":
    out={}
    out['fibonacci']=run_family('fib',{r:fib_samples(r) for r in range(12)},lambda smp: None) if False else None
    fs={r:fib_samples(r) for r in range(12)}
    res={}
    for r,smp in fs.items():
        res[str(r)]=[]
        for i in range(len(smp[0]['steps'])):
            Ns=[s['steps'][i][1] for s in smp]; Sb=[s['steps'][i][2] for s in smp]; Sa=[s['steps'][i][3] for s in smp]
            res[str(r)].append(step_record(Ns,Sb,Sa,fib_field(smp,i)))
    out['fibonacci']=res
    ss=sq_direct_samples()
    out['squares_direct']={str(r):[step_record([s['steps'][i][1] for s in smp],[s['steps'][i][2] for s in smp],[s['steps'][i][3] for s in smp],sq_field(smp,i)) for i in range(len(smp[0]['steps']))] for r,smp in ss.items()}
    ws=wrapper_samples()
    out['squares_wrapper']={str(c):[step_record([s['steps'][i][1] for s in smp],[s['steps'][i][2] for s in smp],[s['steps'][i][3] for s in smp],wrap_field(smp,i)) for i in range(len(smp[0]['steps']))] for c,smp in ws.items()}
    summ={k:summarize(v) for k,v in out.items()}
    print(json.dumps(summ,indent=1))
    json.dump(dict(per_step=out,summary={k:dict(counts=v[0],total=v[1]) for k,v in summ.items()}),open(sys.argv[1],'w'),indent=1)
