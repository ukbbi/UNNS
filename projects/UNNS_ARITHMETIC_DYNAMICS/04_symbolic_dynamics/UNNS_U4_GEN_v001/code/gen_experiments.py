"""UNNS_U4_GEN_v001 registered experiments (prime-fire and divisor-fire exponent-vector dynamics) + independent big-integer cross-check.
Usage: python3 gen_experiments.py out.json"""
import os,sys,json,math,time
from functools import lru_cache
H=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,H)
import sympy
import indep_graph as I
CFG=json.load(open(H+"/../data/gen_config.json"))
@lru_cache(None)
def fac(n): return tuple(sorted(sympy.factorint(n).items()))
def init(x): return {p:k for p,k in fac(x)}
def can_fire(e,N): return all(e.get(q,0)>=k for q,k in fac(N))
def fire(e,N):
    e=dict(e)
    for q,k in fac(N):
        e[q]-=k
        if e[q]==0: del e[q]
    for q,k in fac(N+1): e[q]=e.get(q,0)+2*k
    return e
def pp(e,p): return p**e[p]                      # exact prime-power part
# ---- prime-fire rules: state = current vertex (exponent vector), history h = previous fired prime (only rotate_next)
def pf_rule(name,e,h):
    if name=="maxpp": return max(e,key=lambda p:pp(e,p))
    if name=="minpp": return min(e,key=lambda p:pp(e,p))
    if name=="spf": return min(e)
    if name=="lpf": return max(e)
    if name=="maxexp_small": return min(e,key=lambda p:(-e[p],p))
    if name=="oddexp_small": return min([p for p in e if e[p]%2] or list(e))
    if name=="rotate_next": return (min([p for p in e if p>h] or [min(e)]) if h else min(e))
    raise KeyError(name)
def divisors_le(e,cap): return [d for d in range(2,cap+1) if can_fire(e,d)]
def df_rule(name,e,c,cap):
    D=divisors_le(e,cap);fb=0
    if not D: return min(e),c,1
    if name=="maxdiv": return D[-1],c,0
    if name=="mindiv4":
        D4=[d for d in D if d>=4]; return (D4[0] if D4 else min(e)),c,0
    if name=="rankcycle5": return D[c%len(D)],(c+1)%5,0
    raise KeyError(name)
def run_pf(x,rule,Hn):
    e=init(x);w=[];h=0
    for _ in range(Hn):
        p=pf_rule(rule,e,h);w.append(p);h=p;e=fire(e,p)
    return w,e
def run_df(x,rule,Hn,cap):
    e=init(x);w=[];c=0;fb=0
    for _ in range(Hn):
        N,c,f=df_rule(rule,e,c,cap);fb+=f;w.append(N);e=fire(e,N)
    return w,e,fb
def eventual_period(t,maxp):
    for p in range(1,maxp+1):
        if all(t[i]==t[i+p] for i in range(len(t)-p)): return p
    return None
def cx(t,n): return len({tuple(t[i:i+n]) for i in range(len(t)-n+1)})
def log2x(e): return sum(k*math.log2(p) for p,k in e.items())
def analyse(w,e,tail,maxp,ns):
    t=w[-tail:];per=eventual_period(t,maxp);c=[cx(t,n) for n in ns]
    return dict(eventual_period=per,symbols_tail=sorted(set(t)),complexity=dict(zip(map(str,ns),c)),
      complexity_equals_n_plus_1=all(cx(t,n)==n+1 for n in ns),log2_x_end=log2x(e),max_prime_end=max(e) if e else None,
      tail_head=t[:12])
# ---- independent big-integer engine (shares no code with the exponent engine): factor by trial division by the small primes
PR=list(sympy.primerange(2,2000))
def vals(x):
    v={}
    for p in PR:
        if x%p==0:
            k=0
            while x%p==0: x//=p;k+=1
            v[p]=k
    assert x==1,"cofactor outside prime table"
    return v
def bigint_run(x,rule,steps):
    w=[];h=0;edges_ok=True;graph_checked=0;prev=None
    for n in range(steps):
        v=vals(x)
        if rule=="maxpp": p=max(v,key=lambda q:q**v[q])
        elif rule=="minpp": p=min(v,key=lambda q:q**v[q])
        elif rule=="spf": p=min(v)
        elif rule=="lpf": p=max(v)
        elif rule=="maxexp_small": p=min(v,key=lambda q:(-v[q],q))
        elif rule=="oddexp_small": p=min([q for q in v if v[q]%2] or list(v))
        elif rule=="rotate_next": p=(min([q for q in v if q>h] or [min(v)]) if h else min(v))
        y=(x//p)*(p+1)**2
        edges_ok&=(x%p==0 and y>x)
        if x<CFG["independent_check"]["graph_edge_steps_x_lt"]:
            edges_ok&=(y in I.nbrs(x)) and (prev is None or I.dist(prev,y)==2);graph_checked+=1
        w.append(p);h=p;prev=x;x=y
    return w,edges_ok,graph_checked
def run():
    t0=time.time();PF=CFG["prime_fire"];DF=CFG["divisor_fire"];res=dict(prime_fire={},divisor_fire={},independent={},summary={})
    for rule in PF["rules"]:
        rows=[];lastbig=[]
        for x in PF["starts"]:
            w,e=run_pf(x,rule,PF["horizon"])
            a=analyse(w,e,PF["tail"],PF["max_period"],PF["complexity_n"])
            big=[i for i,p in enumerate(w) if p>=5];a["fires_ge5"]=len(big);a["last_fire_ge5"]=big[-1] if big else None
            a["start"]=x;rows.append(a)
        res["prime_fire"][rule]=rows
    for rule in DF["rules"]:
        rows=[]
        for x in DF["starts"]:
            w,e,fb=run_df(x,rule,DF["horizon"],DF["cap"])
            a=analyse(w,e,DF["tail"],DF["max_period"],DF["complexity_n"]);a["start"]=x;a["fallbacks"]=fb;a["distinct_symbols_total"]=len(set(w))
            rows.append(a)
        res["divisor_fire"][rule]=rows
    # independent cross-check
    bi=CFG["independent_check"]["bigint_steps"];ok=True;n=0;gc=0
    for rule in PF["rules"]:
        xs=PF["starts"][::8] if rule in("maxpp","spf") else PF["starts"][::40]
        for x in xs:
            wb,eo,g=bigint_run(x,rule,bi);wa,_=run_pf(x,rule,bi)
            ok&=(wb==wa) and eo;n+=1;gc+=g
    res["independent"]=dict(runs=n,all_itineraries_equal_and_edges_legal=ok,graph_edges_checked=gc)
    # predictions
    pf=res["prime_fire"]
    res["summary"]=dict(
     P1_spf_period5_all=all(r["eventual_period"]==5 for r in pf["spf"]),
     P2_maxpp_aperiodic_sturmian_all=all(r["eventual_period"] is None and r["complexity_equals_n_plus_1"] for r in pf["maxpp"]),
     P3_finitely_many_ge5_all=all((r["last_fire_ge5"] is None) or r["last_fire_ge5"]<PF["horizon"]-PF["tail"] for rule in pf for r in pf[rule]),
     prime_fire_period_histogram={rule:{str(k):sum(1 for r in pf[rule] if r["eventual_period"]==k) for k in sorted({r["eventual_period"] for r in pf[rule]},key=lambda z:(z is None,z))} for rule in pf},
     divisor_fire_period_histogram={rule:{str(k):sum(1 for r in res["divisor_fire"][rule] if r["eventual_period"]==k) for k in sorted({r["eventual_period"] for r in res["divisor_fire"][rule]},key=lambda z:(z is None,z))} for rule in res["divisor_fire"]},
     wall_seconds=round(time.time()-t0))
    return res
if __name__=="__main__":
    r=run();json.dump(r,open(sys.argv[1],"w"),indent=1,default=str);print(json.dumps(r["summary"],indent=1));print(r["independent"])
