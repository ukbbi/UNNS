"""Stage 2D: preregistered selector experiment. Reads data/stage2_config.json; deterministic; exact integers; RN-0 certification policy."""
import sys,os,json,math,time
H=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,H);sys.path.insert(0,H+"/../engine")
import u3_graph as G
import rn_core as C
D=H+"/../data"
KEYS={"val_asc":lambda v,d:(v,),"val_desc":lambda v,d:(-v,),"deg_asc_then_val":lambda v,d:(d,v),"deg_desc_then_val":lambda v,d:(-d,v)}
NEED_DEG={"deg_asc_then_val","deg_desc_then_val"}
def nb(x): return G.nbrs(x),G._NB[x][1]
def is_prime_cert(x): return C.is_prime(x)
def run_one(start,key,rank,mem,horizon,bound):
    x=start;p=None;seen={};path=[];unc=0;requests=0;pv=[];prime_total=0
    for step in range(horizon+1):
        state=(x,p) if mem else (x,)
        if state in seen:
            pre=seen[state];return dict(outcome="CYCLE",steps=step,preperiod=pre,period=step-pre,maxlog10=math.log10(max(path)) if path else 0,prime_total=prime_total,prime_distinct=len(set(pv)),uncertified=unc,requests=requests)
        seen[state]=step;path.append(x)
        ok,cert=is_prime_cert(x)
        if ok:
            prime_total+=1;pv.append(x)
        if not cert: unc+=1
        if x>bound: return dict(outcome="ESCAPED",steps=step,preperiod=None,period=None,maxlog10=math.log10(x),prime_total=prime_total,prime_distinct=len(set(pv)),uncertified=unc,requests=requests)
        N,c=nb(x);requests+=1
        if not c: unc+=1
        E=[y for y in N if not(mem and y==p)]
        if len(E)<rank: return dict(outcome="STUCK",steps=step,preperiod=None,period=None,maxlog10=math.log10(max(path)),prime_total=prime_total,prime_distinct=len(set(pv)),uncertified=unc,requests=requests)
        if key in NEED_DEG:
            degs={}
            for y in E:
                fy,cy=C.factor(y);degs[y]=C.degree_from_fact(fy);requests+=1      # degree from the (certified) factorisation: tau(y)+#{q>=2: q^2|y}
                if not cy: unc+=1
            E.sort(key=lambda v:KEYS[key](v,degs[v]))
        else: E.sort(key=lambda v:KEYS[key](v,0))
        p,x=x,E[rank-1]
    return dict(outcome="HORIZON",steps=horizon,preperiod=None,period=None,maxlog10=math.log10(max(path)),prime_total=prime_total,prime_distinct=len(set(pv)),uncertified=unc,requests=requests)
def run():
    cfg=json.load(open(D+"/stage2_config.json"))["selectors_2D"];t0=time.time();rows=[]
    for key in KEYS:
        for rank in (1,2,3):
            for mem in (0,1):
                for s in cfg["starts"]:
                    r=run_one(s,key,rank,mem,cfg["horizon"],cfg["escape_bound"]);r.update(key=key,rank=rank,memory="NB" if mem else "state_only",start=s);rows.append(r)
    agg={}
    for r in rows:
        k=f'{r["key"]}|rank{r["rank"]}|{r["memory"]}';a=agg.setdefault(k,dict(CYCLE=0,ESCAPED=0,STUCK=0,HORIZON=0,prime_total=0,prime_distinct_union=set(),uncertified=0,requests=0))
        a[r["outcome"]]+=1;a["prime_total"]+=r["prime_total"];a["uncertified"]+=r["uncertified"];a["requests"]+=r["requests"]
    # distinct primes: recompute union from rows is not stored per row; store counts only
    for k,a in agg.items(): a.pop("prime_distinct_union")
    # paired comparison state-only vs NB
    pairs=[]
    for key in KEYS:
        for rank in (1,2,3):
            a=agg[f"{key}|rank{rank}|state_only"];b=agg[f"{key}|rank{rank}|NB"]
            pairs.append(dict(key=key,rank=rank,state_only={k:a[k] for k in("CYCLE","ESCAPED","STUCK","HORIZON","prime_total")},NB={k:b[k] for k in("CYCLE","ESCAPED","STUCK","HORIZON","prime_total")}))
    return dict(rows=rows,aggregate=agg,pairs=pairs,all_neighbourhoods_certified=all(r["uncertified"]==0 for r in rows),factor_counters=dict(C.CNT),cache_note="counters depend on run order and cache; deterministic for the fixed order")
if __name__=="__main__":
    t=time.time();r=run();json.dump(r,open(sys.argv[1],"w"),indent=1,default=str)
    print("certified",r["all_neighbourhoods_certified"],round(time.time()-t),"s");
    from collections import Counter
    print(Counter(x["outcome"] for x in r["rows"]))
