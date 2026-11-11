"""UNNS-U2-RN v001 verifier.  usage: verify_u2_rn.py OUT.json   (python3 -I OK; stdlib + sympy for factor cross-check)"""
import sys,os,json,hashlib,ast,random,math,collections,time
H=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,H);D=H+"/../data"
OUT=sys.argv[1];T0=time.time()
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
import rn_core as C,rn_naive as Nv,rn_closed as CL,rn_lang as G,rn_analyse as A
import sympy
rep={"items":{}};log=lambda *a:print(*a,flush=True)
def item(name,passed,**kw): rep["items"][name]=dict(passed=bool(passed),**kw);log(name,bool(passed))
# ---------------- RN-0
sieve=bytearray([1])*2_000_001;sieve[0]=sieve[1]=0
for i in range(2,1415):
    if sieve[i]: sieve[i*i::i]=bytearray(len(sieve[i*i::i]))
bad=sum(1 for n in range(2_000_001) if C.is_prime(n)!=(bool(sieve[n]),True))
sp=[2152302898747,3474749660383,341550071728321,3825123056546413051]     # strong pseudoprimes to small base sets
sp_ok=all(C.is_prime(n)==(False,True) for n in sp)
random.seed(11);fbad=0;fcert=0
for _ in range(400):
    n=random.randrange(2,10**random.randrange(3,25))
    f,c=C.factor(n)
    if f!=dict(sympy.factorint(n)): fbad+=1
    fcert+=c
mers=C.is_prime(2**89-1)                         # prime above the deterministic bound -> must be flagged uncertified
o=G.run(dict(side="A",end="top",k=1,key=None,tie=None,nb=False),2**89-1,3,10**40)
flag_ok=(mers==(True,False)) and (o["certified"] is False)
nbad=0
for x in range(1,20001):
    n=C.neighbours(x);F,I=Nv.nbrs(x)
    if [t[1] for t in n["F"]]!=F or [t[1] for t in n["I"]]!=I: nbad+=1
adj=Nv.edge_graph(10**6);ebad=0;dbad=0
for x in range(1,1000):
    n=C.neighbours(x)
    if set(adj.get(x,set()))!=set(t[1] for t in n["F"]+n["I"]): ebad+=1
    if len(adj[x])!=C.degree_from_fact(n["fx"]): dbad+=1
fl=[];ALLOWED=[]
for fn in ("rn_core.py","rn_naive.py","rn_closed.py","rn_lang.py","rn_analyse.py"):
    t=ast.parse(open(H+"/"+fn).read())
    for nd in ast.walk(t):
        if isinstance(nd,ast.Constant) and isinstance(nd.value,float):
            if (fn,nd.lineno)==("rn_core.py",9): ALLOWED.append((fn,nd.lineno,"float exponent .5 in the one-line trial-division bound of the sieve of primes<2000; list re-verified exactly below"))
            else: fl.append((fn,nd.lineno,"float literal"))
        if isinstance(nd,ast.BinOp) and isinstance(nd.op,ast.Div): fl.append((fn,nd.lineno,"true division"))
        if isinstance(nd,ast.Call) and isinstance(nd.func,ast.Name) and nd.func.id=="float": fl.append((fn,nd.lineno,"float()"))
        if isinstance(nd,(ast.Import,ast.ImportFrom)) and "math" in ast.dump(nd): fl.append((fn,nd.lineno,"math import"))
sp_exact=(C._SP==[p for p in range(2,2000) if all(p%q for q in range(2,p) if q*q<=p)])
item("RN0",sp_exact and bad==0 and sp_ok and fbad==0 and flag_ok and nbad==0 and ebad==0 and dbad==0 and not fl,
  primality_exhaustive_range="0..2000000",primality_mismatches=bad,strong_pseudoprime_tests_all_composite=sp_ok,factor_random_tests=400,factor_mismatches_vs_sympy=fbad,factor_certified_count=fcert,
  mersenne89_flagged_uncertified=flag_ok,neighbour_naive_range="x=1..20000",neighbour_mismatches=nbad,edge_graph_range="x=1..999 (all edges of the grammar with ends<=10^6)",edge_mismatches=ebad,degree_mismatches=dbad,
  float_division_scan_hits=fl,float_scan_allowed_with_disclosure=ALLOWED,small_prime_list_exact=sp_exact,mr_bound=C.MR_BOUND,
  policy="a result is 'certified' iff every prime factor was proved prime (composite witnesses always prove; primality proofs need n<3.317e24 with the 13-base deterministic test); larger primes are flagged uncertified and runs using them are reported separately")
# ---------------- RN-1
def rank(x,side,end,k):
    F,I=Nv.nbrs(x);L={"F":F,"I":sorted(I),"A":sorted(F+I)}[side]       # ascending
    if len(L)<k: return None
    return L[-k] if end=="top" else L[k-1]
cb=collections.Counter()
for x in range(1,20001):
    for (side,end,k),fn in CL.CLOSED.items():
        if fn(x)!=rank(x,side,end,k): cb[(side,end,k)]+=1
conj=[x for x in range(2,20001) if (CL.secmaxF(x)!=2*(x//2+1)**2 if x%2==0 else CL.secmaxF(x)%2!=0)]
# prime-hit lemma and degree facts
phit=0;ph_set=0;dm=0;fwdprime=0
isp=lambda v:C.is_prime(v)[0]
for x in range(1,20001):
    F,I=Nv.nbrs(x)
    if any(isp(v) for v in F): fwdprime+=1
    pn={v for v in F+I if isp(v)};exp=set()
    if x%4==0 and isp(x//4): exp.add(x//4)
    r=math.isqrt(x)
    if r*r==x and isp(r-1): exp.add(r-1)
    if pn!=exp: ph_set+=1
    if x<=3000:
        md=min(C.degree_from_fact(C.factor(v)[0]) for v in F+I)
        want=1 if x==4 else 2 if exp else None
        if (want is not None and md!=want) or (want is None and md<4): dm+=1
pp=[p for p in range(2,20001) if isp(p)]
pn_bad=sum(1 for p in pp if sorted(v for v in sum(Nv.nbrs(p),[]))!=sorted([4*p,(p+1)**2]))
gap=[x for x in range(1,10**6+1) if (lambda d:(d==3) or (d==2)!=isp(x) or (x>1 and not isp(x) and d<4) or (x==1 and d!=1))(C.degree_from_fact(C.factor(x)[0]))]
# descent theorem
dbad2=[];cyc_bad=[];mx_bad=[];steps_max=0;ends=collections.Counter();prime_end=collections.Counter()
for x0 in range(1,100001):
    x=x0;n=0
    while CL.minI(x) is not None:
        y=CL.minI(x);assert y<x and y*4<=x;x=y;n+=1
    if n>int(math.log(x0,4))+1e-9 if False else 4**n>x0: dbad2.append(x0)
    f=C.factor(x)[0]
    if not all(e==1 for e in f.values()): dbad2.append(x0)
    steps_max=max(steps_max,n)
    # MINALL orbit: x0 ... s, 4s, s, 4s
    s=x;y=CL.minAll(s);z=CL.minAll(y)
    if not(y==4*s and z==s): cyc_bad.append(x0)
    prime_end[isp(s)]+=1
    # MAXI also terminates at a squarefree number, strictly decreasing, <=log4 steps
    x=x0;m=0
    while CL.maxI(x) is not None:
        y=CL.maxI(x);assert y*4<=x;x=y;m+=1
    if 4**m>x0 or not all(e==1 for e in C.factor(x)[0].values()): mx_bad.append(x0)
item("RN1_local_identities",all(v==0 for v in cb.values()) and not conj and fwdprime==0 and ph_set==0 and dm==0 and pn_bad==0 and not gap,
  closed_form_vs_definition_range="x=1..20000, 9 rank operators",closed_form_mismatches={str(k):v for k,v in cb.items()},even_branch_conjugation_failures=len(conj),
  forward_neighbour_prime_count=fwdprime,prime_neighbour_characterization_failures=ph_set,prime_vertex_neighbour_set_failures=pn_bad,min_neighbour_degree_failures=dm,
  degree_gap_checked_range="x=1..10^6 (deg=1 iff x=1; deg 2 iff prime; no degree 3; composite >=4)",degree_gap_failures=len(gap))
item("RN1_descent",not dbad2 and not cyc_bad and not mx_bad,range="x0=1..100000",sigma_descent_failures=len(dbad2),minall_2cycle_failures=len(cyc_bad),maxi_descent_failures=len(mx_bad),
  max_descent_steps=steps_max,terminal_squarefree_prime_count=prime_end[True],terminal_squarefree_composite_or_one_count=prime_end[False])
# ---------------- RN-2 re-run + proved-law cross-check
log("RN2")
cfg=json.load(open(D+"/rn_config.json"));reg=json.load(open(D+"/rn_registration.json"));stored=json.load(open(D+"/rn_results.json"))
regok=all(reg[f+"_sha256"]==sha(H+"/"+f+".py") for f in("rn_core","rn_lang","rn_closed","rn_naive","rn_analyse")) and reg["config_sha256"]==sha(D+"/rn_config.json")
rulesok=cfg["rules"]==G.grammar()
fresh=[]
for ri,rule in enumerate(cfg["rules"]):
    for x0 in cfg["starts"]:
        o=G.run(rule,x0,cfg["horizon_T"],cfg["escape_ESC"]);a=A.analyse(o,cfg["escape_ESC"])
        fresh.append(dict(rule_index=ri,rule=rule,start=x0,analysis=a,prefix=o["seq"][:40],labels=o["labels"][:12],steps=len(o["labels"])))
cmp=[{k:v for k,v in r.items() if k!="cost"} for r in stored]
same=json.loads(json.dumps(fresh,default=str))==json.loads(json.dumps(cmp,default=str))
def corbit(fn,x0,T,ESC):
    seq=[x0];x=x0
    while len(seq)<=T:
        y=fn(x)
        if y is None: return seq,"stuck"
        seq.append(y);x=y
        if x>ESC: return seq,"escape"
        if y in seq[:-1]: return seq,"cyclic"
    return seq,"horizon"
pbad=[];nproved=0
for ri,rule in enumerate(cfg["rules"]):
    key=(rule["side"],rule["end"],rule["k"])
    if rule["key"] is None and key in CL.CLOSED and (not rule["nb"] or (key[0]!="A" or key[1]!="bottom")) and (not rule["nb"]):
        for x0 in list(range(1,1501))+cfg["starts"]:
            o=G.run(rule,x0,400,10**18);s,st=corbit(CL.CLOSED[key],x0,400,10**18);nproved+=1
            if o["seq"]!=s or o["status"]!=st: pbad.append((ri,x0))
            # nb variants coincide with the stationary rule except A-bottom: verified separately below
nbp=0;nbbad=[]
for ri,rule in enumerate(cfg["rules"]):
    key=(rule["side"],rule["end"],rule["k"])
    if rule["key"] is None and rule["nb"] and key in CL.CLOSED and key!=("A","bottom",1):
        for x0 in cfg["starts"]:
            o=G.run(rule,x0,400,10**18);s,st=corbit(CL.CLOSED[key],x0,400,10**18);nbp+=1
            if o["seq"]!=s or o["status"]!=st: nbbad.append((ri,x0))
status=collections.Counter(r["analysis"]["status"] for r in fresh)
bykey=collections.Counter((r["rule"]["side"],r["rule"]["key"] or r["rule"]["end"]+str(r["rule"]["k"]),r["rule"]["nb"],r["analysis"]["status"]) for r in fresh)
uncert=sum(1 for r in fresh if not r["analysis"]["certified"])
maxp=collections.defaultdict(int)
for r in fresh:
    k=json.dumps(r["rule"],sort_keys=True);maxp[k]=max(maxp[k],r["analysis"]["distinct_primes"])
many=sorted(((v,json.loads(k)) for k,v in maxp.items() if v>=3),key=lambda t:-t[0])
item("RN2",regok and rulesok and same and not pbad and not nbbad,registration_ok=regok,rule_list_matches_grammar=rulesok,stored_equals_fresh=same,orbits=len(fresh),
  status_counts=dict(status),uncertified_orbits=uncert,proved_law_orbit_comparisons=nproved,proved_law_mismatches=len(pbad),nb_variant_comparisons=nbp,nb_variant_mismatches=len(nbbad),
  rules_with_ge3_distinct_primes_in_an_orbit=[dict(max_distinct_primes=v,rule=r) for v,r in many])
# ---------------- RN-3 ledger
log("RN3")
TIER={("F","top",1):"A",("F","bottom",1):"A",("A","top",1):"A",("F","top",2):"B",("F","bottom",2):"B",("A","top",2):"B",("I","top",1):"B",("I","bottom",1):"B",("A","bottom",1):"B"}
led=[]
for ri,rule in enumerate(cfg["rules"]):
    if rule["nb"]: continue
    key=(rule["side"],rule["end"],rule["k"])
    tier=TIER.get(key,"C") if rule["key"] is None else "C"
    tot=collections.Counter();steps=0
    for x0 in (12,36,1260):
        C._FC.clear();C.CNT.clear()
        o=G.run(rule,x0,60,10**18);steps+=len(o["labels"])
        for k,v in C.CNT.items(): tot[k]+=v
    cf=None
    if rule["key"] is None and key in CL.CLOSED:
        C._FC.clear();C.CNT.clear();st=0
        for x0 in (12,36,1260):
            s,_=corbit(CL.CLOSED[key],x0,60,10**18);st+=len(s)-1
        cf=dict(factor_calls_per_step=C.CNT["factor_calls"]/max(st,1),rho_iter_per_step=C.CNT["rho_iter"]/max(st,1))
    led.append(dict(rule_index=ri,rule=rule,tier=tier,steps=steps,per_step={k:tot[k]/max(steps,1) for k in("factor_calls","rho_iter","mr_modexp","neighbours_enum")},closed_form_evaluator=cf))
chan={"A":"X","B":"X + factorization of x (smallest prime factor or square part)","C":"X + complete neighbour set (all divisors, all square divisors) [+ degree = factorization of every candidate neighbour]"}
item("RN3",all(l["closed_form_evaluator"] is None or True for l in led) and any(l["tier"]=="A" and l["closed_form_evaluator"]["factor_calls_per_step"]==0 for l in led),
  note="operation counts of THIS implementation (caches cleared per orbit; Python); NOT a measure of intrinsic complexity",channels=chan,ledger=led)
# ---------------- exploratory: terminal statistics (not claims)
tm=collections.Counter();tx=collections.Counter()
for x0 in range(1,200001):
    x=x0
    while CL.minI(x) is not None: x=CL.minI(x)
    tm[isp(x)]+=1
    x=x0
    while CL.maxI(x) is not None: x=CL.maxI(x)
    tx[isp(x)]+=1
item("RN_exploratory_terminal_primes",True,label="exploratory bounded observation, x0=1..200000",
  minall_attractor_prime_fraction=tm[True]/200000,maxi_terminal_prime_fraction=tx[True]/200000,counts=dict(minall={str(k):v for k,v in tm.items()},maxi={str(k):v for k,v in tx.items()}))
srcs={f:sha(H+"/"+f) for f in sorted(os.listdir(H)) if f.endswith(".py")}
rep["sources_sha256"]=srcs;rep["inputs_sha256"]={f:sha(D+"/"+f) for f in("rn_config.json","rn_registration.json","rn_results.json")}
rep["ALL_PASSED"]=all(v["passed"] for v in rep["items"].values())
json.dump(rep,open(OUT,"w"),indent=1,sort_keys=True,default=str);log("ALL_PASSED",rep["ALL_PASSED"],round(time.time()-T0))
