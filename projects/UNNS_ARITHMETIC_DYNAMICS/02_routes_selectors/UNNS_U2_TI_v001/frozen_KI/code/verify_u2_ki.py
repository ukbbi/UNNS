"""UNNS-U2-KI v001 deterministic verifier.  usage: python3 verify_u2_ki.py OUT.json DATA_DIR"""
import sys,os,json,hashlib,collections,time
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
OUT=sys.argv[1]; DATA=sys.argv[2]
import ki_core as K, ki_ident as I, ki_run_ident as RI, ki_run_degree as RD, ki_selectors as S
import u1_bnd_lib as L
from fibparam import F
from math import isqrt
import fibsel2, u2sq_selector as Q
rep={"items":{}}; T0=time.time(); timing={}
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def log(*a): print(*a,flush=True)
def canon(o): return json.loads(json.dumps(o,sort_keys=True,default=str))
# ------------------------------------------------------------------ K1
log("K1 identities"); t=time.time()
fresh=canon(RI.run()); stored=json.load(open(DATA+"/ki1_identities.json"))
au=json.load(open(K.DATA+"/state_audit.json"))['per_step']
mp={'const':'const','affine':'local','quad':'algstate'}; mism=[]; tot=0; cnt=collections.Counter(); cert_fail=[]
for fam,v in fresh.items():
    for key,Ls in v.items():
        for i,r in enumerate(Ls):
            tot+=1; a=au[fam][str(key)][i]['cat']; e=mp.get(r['kind'],'rest'); cnt[(fam,r['kind'])]+=1
            if not ((a==e) or (e=='rest' and a in('field','target','unexplained'))): mism.append((fam,key,i,a,r['kind']))
            if r['kind'] in('affine','quad') and not r['certified']: cert_fail.append((fam,key,i))
            if r['kind']=='quad' and (r['sign_A2']!=1 or r['sign_W']!=1): cert_fail.append((fam,key,i,'sign'))
rep["items"]["K1"]=dict(passed=(fresh==stored and not mism and not cert_fail and tot==268),steps=tot,audit_mismatches=len(mism),uncertified=len(cert_fail),
    stored_equals_fresh=(fresh==stored),counts={f"{a}:{b}":n for (a,b),n in sorted(cnt.items())})
timing['K1']=time.time()-t; log(rep["items"]["K1"])
# ------------------------------------------------------------------ K2
log("K2 degrees"); t=time.time()
fresh2=canon(RD.run()); stored2=json.load(open(DATA+"/ki2_degrees.json"))
bad=[]; dist=collections.Counter(); ten=[]
for fam,v in fresh2.items():
    for key,Ls in v.items():
        for i,r in Ls.items():
            dist[(fam,r['audit'],r['d'])]+=1
            if not(r['exists'] and r['identity_verified']) or r['d']<=2: bad.append((fam,key,i))
            if r['audit']=='unexplained':
                ten.append((int(key),int(i),r['degN'],r['degS'],r['d'],r['tower']))
                if r['tower'] is None or r['tower']['order']&(r['tower']['order']-1)==0: bad.append((fam,key,i,'tower'))
n82=sum(len(Ls) for v in fresh2.values() for Ls in v.values())
rep["items"]["K2"]=dict(passed=(fresh2==stored2 and not bad and n82==82 and len(ten)==10),non_shortcut_steps=n82,failures=len(bad),stored_equals_fresh=(fresh2==stored2),
    degree_distribution={f"{a}:{b}:d={c}":n for (a,b,c),n in sorted(dist.items(),key=str)},
    unresolved_ten=[dict(cls=a,step=b,deg_m_label=c,deg_m_state=d,degree_over_state=e,tower_certificate=f) for a,b,c,d,e,f in sorted(ten)])
timing['K2']=time.time()-t; log({k:v for k,v in rep["items"]["K2"].items() if k!='unresolved_ten'})
# ------------------------------------------------------------------ K3
def legal(x,mv):
    S_=x
    for sg,N in mv:
        S2=S_//N*(N+1)**2 if sg=='+' else S_*N//(N+1)**2
        if not L.is_edge(S_,S2): return False
        S_=S2
    return True
def agg(rows,keys):
    n=len(rows); return {k:sum(r[k] for r in rows) for k in keys}|{"n":n}
cost={}
# --- Fibonacci
log("K3 fibonacci"); t=time.time()
fib_ks=list(range(2,900))+[1200,1500]; rows=[]; fails=[]; legalfails=0
for k in fib_ks:
    x=F[k]; a=S.fib_route_baseline(x); b=S.fib_route_ki(x)
    ok=(a[2]==b[2]=="route" or a[2]==b[2]=="small-table") and a[1]==b[1] and a[0]==b[0]==F[k+1] and legal(x,a[1]) and legal(x,b[1])
    if not ok: fails.append(k)
    rows.append(dict(k=k,bits=x.bit_length(),moves=len(a[1]),status=a[2],
        b_iters=a[3]['iters'],k_iters=b[3]['iters'],b_rec=a[3]['recoveries'],k_rec=b[3]['recoveries'],k_short=b[3]['shortcuts'],
        b_ops=a[3]['mults']+a[3]['isqrts']+a[3]['comps'],k_ops=b[3]['mults']+b[3]['isqrts']+b[3]['comps'],
        b_maxbits=a[3]['maxbits'],k_maxbits=b[3]['maxbits']))
rej=0; rejfail=[]
cands=sorted(x for x in set([x for x in range(1,3001)]+[F[k]+d for k in range(2,301) for d in (-2,-1,1,2)]) if x>=1)
fibset=set(F[:2200])
for x in cands:
    if x in fibset: continue
    a=S.fib_route_baseline(x); b=S.fib_route_ki(x); rej+=1
    if not(a[2]==b[2]=="REJECT" and a[0] is None and b[0] is None): rejfail.append(x)
route_rows=[r for r in rows if r['status']=='route']
fib=dict(inputs=len(fib_ks),route_inputs=len(route_rows),small_table_inputs=len(rows)-len(route_rows),failures=fails,reject_cases=rej,reject_failures=len(rejfail),
    totals_route={k:sum(r[k] for r in route_rows) for k in ('b_iters','k_iters','b_rec','k_rec','k_short','b_ops','k_ops')},
    max_b_iters=max(r['b_iters'] for r in rows),max_k_iters=max(r['k_iters'] for r in rows),max_moves=max(r['moves'] for r in rows))
fib['passed']=(not fails and not rejfail)
cost['fibonacci']=rows; timing['fib']=time.time()-t; log(fib)
# --- squares
def sq_inputs():
    ns=list(range(1,3001))+list(range(3001,20001,7))+[10**5,10**6+3,10**7+11,10**9+7,10**12+39,10**15+1]
    return ns
sqres={}
for nm,fb,fk,ready in (("squares_direct",S.sqd_baseline,S.sqd_ki,'d'),("squares_wrapper",S.sqw_baseline,S.sqw_ki,'w')):
    log("K3",nm); t=time.time(); rows=[]; fails=[]
    for n in sq_inputs():
        x=n*n; a=fb(x); b=fk(x)
        ok=(a[2]==b[2]=="route") and a[1]==b[1] and a[4]==b[4] and a[0]==b[0]==(n+1)**2 and legal(x,a[1])
        if not ok: fails.append(n)
        rows.append(dict(n=n,bits=x.bit_length(),moves=len(a[1]),b_iters=a[3]['iters'],k_iters=b[3]['iters'],b_rec=a[3]['recoveries'],k_rec=b[3]['recoveries'],
            k_short=b[3]['shortcuts'],b_ops=a[3]['horner_mults'],k_ops=b[3]['horner_mults']+b[3]['sc_mults']+b[3]['sc_isqrts']))
    rj=0; rjf=[]
    for x in list(range(2,2000))+[n*n+1 for n in range(1,500)]+[n*n-1 for n in range(2,500)]:
        if isqrt(x)**2==x: continue
        a=fb(x); b=fk(x); rj+=1
        if not(a[2]==b[2]=="REJECT"): rjf.append(x)
    d=dict(inputs=len(rows),failures=fails,reject_cases=rj,reject_failures=len(rjf),
        totals={k:sum(r[k] for r in rows) for k in ('b_iters','k_iters','b_rec','k_rec','k_short','b_ops','k_ops')},max_moves=max(r['moves'] for r in rows),passed=(not fails and not rjf))
    sqres[nm]=d; cost[nm]=rows; timing[nm]=time.time()-t; log(nm,d)
rep["items"]["K3_fibonacci"]=fib; rep["items"]["K3_squares_direct"]=sqres["squares_direct"]; rep["items"]["K3_squares_wrapper"]=sqres["squares_wrapper"]
# ------------------------------------------------------------------ ledger numbers (exact, from K1 + K2)
led={}
for fam,tot in (("fibonacci",99),("squares_direct",105),("squares_wrapper",64)):
    c=collections.Counter(r['kind'] for Ls in fresh[fam].values() for r in Ls)
    led[fam]=dict(total=tot,const=c['const'],affine=c['affine'],quad=c['quad'],not_closed_form=c['none'],closed_form=c['const']+c['affine']+c['quad'])
    assert sum(c.values())==tot
# control states unchanged
ctrl_fib=1+sum(len(C.sign)-1 for C in fibsel2.CLS.values())+sum(len(v)-1 for v in fibsel2.SMALL.values())
led["control_states"]=dict(fibonacci=ctrl_fib,squares_direct=len(Q.control_states()),squares_wrapper=len(Q.wrap_control_states()))
nconst=sum(len(TAB) for TAB in [S.TABLES['fib'],S.TABLES['sqd'],S.TABLES['sqw']])
led["shortcut_table_entries"]={k:sum(1 for v in S.TABLES[k].values() if v is not None) for k in S.TABLES}
rep["items"]["ledger"]=dict(passed=(led["control_states"]["fibonacci"]==201 and led["control_states"]["squares_direct"]==85 and led["control_states"]["squares_wrapper"]==45
    and led["fibonacci"]["closed_form"]==38 and led["squares_direct"]["closed_form"]==87 and led["squares_wrapper"]["closed_form"]==61),**led)
# ------------------------------------------------------------------ provenance
srcs={f:sha(HERE+"/"+f) for f in sorted(os.listdir(HERE)) if f.endswith(".py")}
base={}
for root,_,fs in os.walk(HERE+"/../baseline_R3_frozen"):
    for f in sorted(fs):
        if f.endswith((".py",".json")) and "__pycache__" not in root: base[os.path.relpath(os.path.join(root,f),HERE+"/../baseline_R3_frozen")]=sha(os.path.join(root,f))
rep["sources_sha256"]=srcs; rep["baseline_frozen_sha256"]=base
rep["inputs_sha256"]={f:sha(DATA+"/"+f) for f in ("ki1_identities.json","ki2_degrees.json")}
rep["ALL_PASSED"]=all(v.get("passed",True) for v in rep["items"].values())
json.dump(rep,open(OUT,"w"),indent=1,sort_keys=True,default=str)
json.dump(cost,open(DATA+"/cost_records_ki.json","w"))
json.dump(timing,open(os.path.dirname(OUT)+"/timing_informational.json","w"),indent=1)
log("ALL_PASSED",rep["ALL_PASSED"],"total s",round(time.time()-T0))
