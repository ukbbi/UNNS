"""GEN-0 corroboration of Theorem GEN-1 (finite return-state obstruction) + independent replay of Stage-2 selector cycles."""
import os,sys,json,hashlib,time
H=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,H)
import indep_graph as I
CFG=json.load(open(H+"/../data/gen_config.json"))
def hh(*a): return int(hashlib.sha256(repr(a).encode()).hexdigest(),16)
def ball(h,R):
    seen={h:0};fr=[h]
    for r in range(R):
        nf=[]
        for v in fr:
            for w in I.nbrs(v):
                if w not in seen: seen[w]=r+1;nf.append(w)
        fr=nf
    return seen
def selector_run(h,K,Q,seed,steps,W):
    # configuration at time n: (q, x_n, x_{n-1},..,x_{n-K}); deterministic, time-independent; next vertex chosen inside window W
    hist=[h]*(K+1);q=0;visits=[];traj=[h]
    for n in range(steps):
        x=hist[0];cfg=(q,)+tuple(hist)
        if x==h: visits.append((n,cfg))
        nb=[y for y in I.nbrs(x) if y in W]
        y=nb[hh(seed,K,Q,"move",cfg)%len(nb)];q=hh(seed,K,Q,"ctl",cfg)%Q
        hist=[y]+hist[:K];traj.append(y)
    return visits,traj
def test_random():
    T=CFG["theory_checks"]["random_selectors"];R=T["radius"];rows=[];bad=0
    for h in T["hubs"]:
        W=ball(h,R)
        for K in T["K"]:
            BK=sum(1 for v,d in W.items() if d<=K)
            for Q in T["Q"]:
                for s in range(T["per_cell"]):
                    visits,traj=selector_run(h,K,Q,1000*s+7,T["steps"],W)
                    cfgs=[c for _,c in visits];bound=Q*BK**K
                    first={};rep=None
                    for i,c in enumerate(cfgs):
                        if c in first: rep=(first[c],i);break
                        first[c]=i
                    ok=True;per=None
                    if rep:
                        i,j=rep;per=j-i
                        # determinism: from visit i onward the configuration sequence and the time gaps are periodic with period j-i (as far as observed)
                        for t in range(i,len(cfgs)-per):
                            ok&=(cfgs[t]==cfgs[t+per])
                            if t+1<len(visits)-per: ok&=((visits[t+1][0]-visits[t][0])==(visits[t+per+1][0]-visits[t+per][0]))
                    pig=len(cfgs)>bound   # pigeonhole forces a repeat
                    if pig and not rep: ok=False
                    bad+=(not ok)
                    rows.append(dict(hub=h,K=K,Q=Q,seed=s,ball_K=BK,config_bound=bound,visits=len(cfgs),repeat_found=bool(rep),visit_period=per,pigeonhole_applies=pig,consistent=ok))
    return dict(rows=rows,violations=bad,runs=len(rows),runs_with_repeat=sum(r["repeat_found"] for r in rows),runs_pigeonhole=sum(r["pigeonhole_applies"] for r in rows))
KEYS={"val_asc":lambda v,d:(v,),"val_desc":lambda v,d:(-v,),"deg_asc_then_val":lambda v,d:(d,v),"deg_desc_then_val":lambda v,d:(-d,v)}
def replay_one(start,key,rank,nb_mem,horizon=400,xmax=10**14):
    x=start;p=None;seen={};path=[]
    for step in range(horizon+1):
        st=(x,p) if nb_mem else (x,)
        if st in seen: return dict(outcome="CYCLE",preperiod=seen[st],period=step-seen[st])
        seen[st]=step
        if x>xmax: return dict(outcome="SKIP_BIG")
        E=[y for y in I.nbrs(x) if not(nb_mem and y==p)]
        if len(E)<rank: return dict(outcome="STUCK")
        E.sort(key=lambda v:KEYS[key](v,I.deg(v) if key.startswith("deg") else 0));p,x=x,E[rank-1]
    return dict(outcome="HORIZON")
def test_replay():
    S=json.load(open(H+"/../inherited/stage2_selector_results.json"));rows=[];mism=0;skip=0
    for r in S["rows"]:
        if r["outcome"]!="CYCLE": continue
        if 10**r["maxlog10"]>CFG["theory_checks"].get("xmax",1e14): skip+=1;continue
        a=replay_one(r["start"],r["key"],r["rank"],r["memory"]=="NB")
        ok=(a["outcome"]=="CYCLE" and a["period"]==r["period"] and a["preperiod"]==r["preperiod"])
        mism+=(not ok);rows.append(dict(start=r["start"],key=r["key"],rank=r["rank"],memory=r["memory"],stored_period=r["period"],replay=a,match=ok))
    return dict(rows=rows,mismatches=mism,replayed=len(rows),skipped_big=skip,
       period_histogram={str(p):sum(1 for x in rows if x["stored_period"]==p) for p in sorted({x["stored_period"] for x in rows})})
def run():
    t=time.time();a=test_random();b=test_replay()
    return dict(random_selectors=a,stage2_replay=b,passed=(a["violations"]==0 and b["mismatches"]==0),wall_seconds=round(time.time()-t))
if __name__=="__main__":
    r=run();json.dump(r,open(sys.argv[1],"w"),indent=1,default=str)
    print({k:(v if not isinstance(v,dict) else {kk:vv for kk,vv in v.items() if kk!='rows'}) for k,v in r.items()})
