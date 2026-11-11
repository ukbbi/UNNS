"""UNNS-U2-TI v001 deterministic verifier.  usage: verify_u2_ti.py OUT.json"""
import sys,os,json,hashlib,collections,time,ast,zlib,random,statistics
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
OUT=sys.argv[1]; D=HERE+"/../data"; FR=HERE+"/../frozen_KI"
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
def log(*a): print(*a,flush=True)
rep={"items":{}}; T0=time.time()
# ============================================================ TI-0
log("TI-0")
import ti0_exact as X
import ki_selectors as KS
from math import isqrt
ast_hits={p:X.ast_float_scan(FR+"/"+p) for p in ("baseline_R3_frozen/code/fibsel2.py","baseline_R3_frozen/code/radical.py","baseline_R3_frozen/code/sq/u2_selector.py","baseline_R3_frozen/code/sq/u2sq_selector.py","code/ki_selectors.py")}
la=X.label_audit()
ns=list(range(1,3001))+list(range(3001,20001,7))+[10**5,10**6+3,10**7+11,10**9+7,10**12+39,10**15+1]
bad=0
for n in ns:
    x=n*n; a=KS.sqw_baseline(x); S1,m1=X.run(X.sigma_wrap_exact,x); S2,m2=X.run(X.sigma_wrap_ki_exact,x)
    if not(a[1]==m1==m2 and S1==S2==(n+1)**2): bad+=1
random.seed(7); ext=[random.randrange(10**10,10**60) for _ in range(150)]; bad_ext=0; frozen_agree=0
import ti0_exact
for n in ext:
    x=n*n; S1,m1=X.run(X.sigma_wrap_exact,x); S2,m2=X.run(X.sigma_wrap_ki_exact,x)
    if not(m1==m2 and S1==S2==(n+1)**2): bad_ext+=1
    a=KS.sqw_baseline(x)          # frozen lambdified evaluator
    if a[1]==m1: frozen_agree+=1
# float trap works
try: X._chk(1.0); trap=False
except X.FloatTrap: trap=True
truediv_exec=[(p,h) for p,hs in ast_hits.items() for h in hs]
rep["items"]["TI0"]=dict(passed=(bad==0 and bad_ext==0 and trap and not any(not r['integer_coeffs'] or r['has_division'] or r['has_dot'] for r in la) and frozen_agree==len(ext)),
    label_expressions=len(la),non_integer_label_polynomials=sum(1 for r in la if not r['integer_coeffs']),labels_with_division_or_float_literal=sum(1 for r in la if r['has_division'] or r['has_dot']),
    static_scan_hits=truediv_exec,static_scan_note="all hits are true-division in sympy symbolic code at import or in Fraction arithmetic (u2_selector.py lines 16,56; u2sq_selector.py line 27); no float literal, float() or math.* call in any executed selector",
    domain_inputs=len(ns),domain_mismatches=bad,extended_inputs=len(ext),extended_range="10^10..10^60 (n)",extended_mismatches=bad_ext,frozen_lambdified_agrees_on_extended=frozen_agree,float_trap_functional=trap)
log(rep["items"]["TI0"]["passed"])
# ============================================================ TI-1 registration
import ti_lang as G, ti_recog as R, ti_explore as E
reg=json.load(open(D+"/registration.json")); cfg=json.load(open(D+"/ti_config.json"))
reg_ok=(reg["config_sha256"]==sha(D+"/ti_config.json") and reg["ti_lang_sha256"]==sha(HERE+"/ti_lang.py") and reg["ti_recog_sha256"]==sha(HERE+"/ti_recog.py"))
rules_ok=(cfg["rules_F"]==G.rules_F() and cfg["rules_M"]==G.rules_M())
rep["items"]["TI1"]=dict(passed=(reg_ok and rules_ok),registration=reg,files_match_registration=reg_ok,rule_lists_match_grammar=rules_ok,n_rules_F=len(cfg["rules_F"]),n_rules_M=len(cfg["rules_M"]),starts=cfg["starts"],horizon=cfg["horizon_T"],escape=cfg["escape_ESC"],amendments=cfg["amendments"])
# ============================================================ TI-2 recompute registered run
log("TI-2")
stored=json.load(open(D+"/ti_results.json")); fresh=[]
for cls,rules in (("F",cfg["rules_F"]),("M",cfg["rules_M"])):
    for ri,rule in enumerate(rules):
        for x0 in cfg["starts"]:
            res=G.run(rule,x0,cfg["horizon_T"],cfg["escape_ESC"]); a=R.analyse(res)
            fresh.append(dict(cls=cls,rule_index=ri,rule=rule,start=x0,analysis=a,prefix=res["seq"][:60],moves=len(res["moves"]),cand=res["cand"],channels=res["channels"]))
same=(json.loads(json.dumps(fresh,default=str))==stored)
def succ(a):
    return a['status'] in('escape','horizon') and bool(a['linrec_V'] or a['linrec_R'] or any(d.get('consecutive') for k in('fam_V','fam_R') for d in a[k].values()))
status=collections.Counter((r['cls'],r['analysis']['status']) for r in fresh)
S=[r for r in fresh if succ(r['analysis'])]
fibhits=[r for r in fresh if any(d.get('consecutive') for k in('fam_V','fam_R') for f,d in r['analysis'][k].items() if f=="fibonacci")]
fibrec=[r for r in fresh if r['analysis']['status'] in('escape','horizon') and any((r['analysis'][k] and r['analysis'][k][1]==['1','1']) for k in('linrec_V','linrec_R'))]
cons=[r for r in fresh if any(d.get('consecutive') for k in('fam_V','fam_R') for f,d in r['analysis'][k].items())]
recs=collections.Counter(); 
for r in S:
    for k in('linrec_V','linrec_R'):
        if r['analysis'][k]: recs[tuple(r['analysis'][k][1])]+=1
fam_subset=collections.Counter((f,r['cls']) for r in fresh for k in('fam_V',) for f,d in r['analysis'][k].items() if d.get('subset'))
distinct_succ_prefix=len({tuple(r['prefix'][:14]) for r in S})
rep["items"]["TI2"]=dict(passed=same,stored_equals_fresh=same,orbits=len(fresh),status={f"{a}:{b}":n for (a,b),n in sorted(status.items())},
    registered_successes=len(S),successes_F=sum(1 for r in S if r['cls']=="F"),successes_M=sum(1 for r in S if r['cls']=="M"),
    distinct_successful_prefixes=distinct_succ_prefix,fibonacci_consecutive_hits=len(fibhits),fibonacci_recurrence_hits=len(fibrec),any_family_consecutive_hits=len(cons),
    linear_recurrence_coefficient_patterns={",".join(k):v for k,v in recs.items()},family_subset_hits={f"{a}:{b}":n for (a,b),n in sorted(fam_subset.items())})
log(rep["items"]["TI2"]["passed"],len(S))
# exploratory move laws
log("explore")
ex=[]
for rec in fresh:
    a=rec['analysis']
    if a['status'] not in('escape','horizon'): continue
    r,tail=E.law(rec['rule'],rec['start'],cfg['horizon_T'],cfg['escape_ESC'])
    ex.append(dict(cls=rec['cls'],tail=tail,success=succ(a)))
laws=collections.Counter((o['success'],tuple(o['tail'][-2:])) for o in ex)
xlaw=[o for o in ex if o['tail'][-2:]==("+x","+x")]
rep["items"]["TI2_exploratory"]=dict(passed=True,label="exploratory (added after the registered results were seen)",non_cyclic_orbits=len(ex),
    law_counts={f"registered_success={s}:{'|'.join(t)}":n for (s,t),n in laws.most_common(12)},
    x_to_xplus1_squared_orbits=len(xlaw),x_to_xplus1_squared_registered_successes=sum(1 for o in xlaw if o['success']))
# ============================================================ TI-3 audit
log("TI-3")
# A. neighbour cross-check
import u1_bnd_lib as L
nb_bad=[x for x in range(1,3001) if set(c[0] for c in G.neighbours(x))!=L.neighbours_simple(x)]
# B. locality + history perturbation
def replay(rule,x0,T):
    x=x0; hist=(); trip=[]
    hw={"none":0,"h1":1,"h12":2}[rule["hist"]]
    for _ in range(T):
        r=G.step(rule,x,hist,set(),G.Channels())
        if r is None: break
        trip.append((x,hist,r[0])); hist=((x,)+hist)[:hw] if hw else (); x=r[0]
        if x>cfg["escape_ESC"]: break
    return trip
loc_bad=0; pert_bad=0; checked=0
for rule in cfg["rules_F"]:
    for x0 in cfg["starts"][:6]:
        for (x,hist,y) in replay(rule,x0,25):
            checked+=1
            if G.step(rule,x,hist,set(),G.Channels())[0]!=y: loc_bad+=1
            hw={"none":0,"h1":1,"h12":2}[rule["hist"]]
            junk=hist+(10**30+7,10**30+9)            # entries beyond the declared window must not matter
            if G.step(rule,x,junk,set(),G.Channels())[0]!=y: pert_bad+=1
# C. channel totals
chan=collections.defaultdict(lambda:collections.Counter())
for r in fresh:
    for k,v in r['channels'].items(): chan[r['cls']][k]+=v
chan={c:dict(v) for c,v in chan.items()}
# D. static scan of the interpreter
src=open(HERE+"/ti_lang.py").read(); tree=ast.parse(src)
imports=sorted({n.names[0].name for n in ast.walk(tree) if isinstance(n,ast.Import)}|{n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)})
ints=sorted({n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,int) and not isinstance(n.value,bool)})
opens=[n.lineno for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="open"]
jsonuse=[n.lineno for n in ast.walk(tree) if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=="json"]
rep["items"]["TI3_audit"]=dict(passed=(not nb_bad and loc_bad==0 and pert_bad==0 and not opens and not jsonuse and chan["F"].get("V",1)==0),
    neighbour_crosscheck_range="x=1..3000 against the independent trial-division engine",neighbour_mismatches=len(nb_bad),locality_states_checked=checked,locality_mismatches=loc_bad,
    history_beyond_window_perturbation_mismatches=pert_bad,channel_reads_by_class=chan,interpreter_imports=imports,interpreter_integer_literals=ints,file_reads_in_interpreter=len(opens),json_use_in_interpreter=len(jsonuse),
    note="class M reads V (visited set) by design: unbounded memory, reference class, not finite control; class F never reads V")
# ============================================================ TI-3 accounting
def jbytes(o): return len(json.dumps(o,sort_keys=True,separators=(",",":")).encode())
def zbytes(o): return len(zlib.compress(json.dumps(o,sort_keys=True,separators=(",",":")).encode(),9))
base=FR+"/baseline_R3_frozen/data"; kid=FR+"/data"
cc=json.load(open(base+"/class_certificates.json")); sm=json.load(open(base+"/small_fib_paths.json")); sq=json.load(open(base+"/sq/square_identities.json")); k1=json.load(open(kid+"/ki1_identities.json"))
fibtab={"classes":{r:{k:c[k] for k in ("searchnames","states_ring","labels_ring","eps","hres")} for r,c in cc.items()},"small":sm,"ki":k1["fibonacci"]}
sqdtab={"identities":sq,"ki":k1["squares_direct"]}
srcU=open(FR+"/baseline_R3_frozen/code/u1_bnd_lib.py").read().split("\n"); i0=[i for i,l in enumerate(srcU) if l.startswith("T = sp.symbols")][0]
wraptab={"u2_identity_source":"\n".join(srcU[i0:i0+20]),"ki":k1["squares_wrapper"]}
codeb=lambda *fs:sum(len(open(FR+"/"+f).read().encode()) for f in fs)
cost=json.load(open(kid+"/cost_records_ki.json"))
def mean(rows,key): return sum(r[key] for r in rows)/len(rows)
fr=[r for r in cost["fibonacci"] if r["status"]=="route"]; sd=cost["squares_direct"]; sw=cost["squares_wrapper"]
acct={"fibonacci_KI":dict(table_bytes=jbytes(fibtab),table_zlib_bytes=zbytes(fibtab),code_bytes=codeb("baseline_R3_frozen/code/fibsel2.py","baseline_R3_frozen/code/radical.py"),control_states=201,moves_per_term=mean(fr,"moves"),recoveries_per_term=mean(fr,"k_rec"),bisection_iterations_per_term=mean(fr,"k_iters"),arith_ops_per_term=mean(fr,"k_ops")),
 "squares_direct_KI":dict(table_bytes=jbytes(sqdtab),table_zlib_bytes=zbytes(sqdtab),code_bytes=codeb("baseline_R3_frozen/code/sq/u2sq_selector.py"),control_states=85,moves_per_term=mean(sd,"moves"),recoveries_per_term=mean(sd,"k_rec"),bisection_iterations_per_term=mean(sd,"k_iters"),arith_ops_per_term=mean(sd,"k_ops")),
 "squares_wrapper_KI":dict(table_bytes=jbytes(wraptab),table_zlib_bytes=zbytes(wraptab),code_bytes=codeb("baseline_R3_frozen/code/sq/u2_selector.py","baseline_R3_frozen/code/sq/u2sq_selector.py"),control_states=45,moves_per_term=mean(sw,"moves"),recoveries_per_term=mean(sw,"k_rec"),bisection_iterations_per_term=mean(sw,"k_iters"),arith_ops_per_term=mean(sw,"k_ops"))}
Frules=[r for r in fresh if r['cls']=="F" and r['moves']>0]
ti=dict(rule_bytes=jbytes(cfg["rules_F"][0]),rule_zlib_bytes=zbytes(cfg["rules_F"][0]),grammar_bits=__import__("math").log2(len(cfg["rules_F"])),interpreter_code_bytes=len(src.encode()),
        moves_per_term=1.0,candidates_inspected_per_move=sum(r['cand'] for r in Frules)/sum(r['moves'] for r in Frules),sequence_specific_tables=0)
rep["items"]["TI3_accounting"]=dict(passed=True,encoding="canonical minified JSON (sorted keys) of the data tables each selector consults; zlib level 9 as a rough compression proxy; code bytes = UTF-8 size of the selector sources; NOT a measure of intrinsic complexity",
    knowledge_rich=acct,graph_local_rule=ti,mean_cost_note="knowledge-rich means are over route inputs of the KI test domain; graph-local candidates are neighbours enumerated per move (divisor enumeration)")
# ============================================================ provenance + gates
srcs={f:sha(HERE+"/"+f) for f in sorted(os.listdir(HERE)) if f.endswith(".py")}
frozen={}
for root,_,fs in os.walk(FR):
    for f in sorted(fs):
        if f.endswith((".py",".json")) and "__pycache__" not in root: frozen[os.path.relpath(os.path.join(root,f),FR)]=sha(os.path.join(root,f))
rep["sources_sha256"]=srcs; rep["frozen_KI_sha256"]=frozen
rep["inputs_sha256"]={f:sha(D+"/"+f) for f in ("ti_config.json","registration.json","ti_results.json","ti_explore.json") if os.path.exists(D+"/"+f)}
rep["ALL_PASSED"]=all(v.get("passed",True) for v in rep["items"].values())
json.dump(rep,open(OUT,"w"),indent=1,sort_keys=True,default=str)
log("ALL_PASSED",rep["ALL_PASSED"],round(time.time()-T0))
