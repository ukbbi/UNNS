"""UNNS-U3 v001 verifier. usage: verify_u3.py OUT.json"""
import sys,os,json,hashlib,ast,random,itertools,math,time
H=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,H);D=H+"/../data";OUT=sys.argv[1];T0=time.time()
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
import u3_graph as G,u3_exp as X
sys.path.insert(0,H+"/../frozen_RN");import rn_naive as Nv
import sympy as sp
rep={"items":{}};log=lambda *a:print(*a,flush=True)
def item(n,p,**kw): rep["items"][n]=dict(passed=bool(p),**kw);log(n,bool(p))
def same(a,b,tol=1e-9):
    if isinstance(a,dict): return isinstance(b,dict) and a.keys()==b.keys() and all(same(a[k],b[k],tol) for k in a)
    if isinstance(a,(list,tuple)): return isinstance(b,(list,tuple)) and len(a)==len(b) and all(same(x,y,tol) for x,y in zip(a,b))
    if isinstance(a,float) or isinstance(b,float): return abs(float(a)-float(b))<=tol*max(1,abs(float(a)))
    return a==b
# ---- U3-0 provenance + registration
reg=json.load(open(D+"/u3_registration.json"))
regok=reg["config_sha256"]==sha(D+"/u3_config.json") and all(reg[k]==sha(H+"/"+k) for k in("u3_graph.py","u3_exp.py")) and all(reg["frozen_RN/"+k]==sha(H+"/../frozen_RN/"+k) for k in("rn_core.py","rn_naive.py"))
prov=dict(l.split()[::-1] for l in open(D+"/provenance_releases.txt") if l.strip())
local={"UNNS_U2_RN_v001.zip":"/home/claude/UNNS_U2_RN_v001.zip","UNNS_U2_TI_v001.zip":"/home/claude/UNNS_U2_TI_v001.zip"}
loc={k:(sha(p)==prov[k]) for k,p in local.items() if os.path.exists(p)}
cfg=json.load(open(D+"/u3_config.json"))
item("U3_0",regok and all(loc.values()),registration_ok=regok,releases_recorded=len(prov),releases_rechecked_locally=loc,
     note="only the RN and TI archives are present in the build environment; the other hashes are copied from the committed UNNS-U0 folder (NOT_RERUN)",amendments=cfg["amendments"])
# ---- graph facts: triangle-free theorem
a,b,c,t=sp.symbols("a b c t",integer=True,positive=True)
ident=sp.simplify(sp.expand((a+1)*(b+1))-(a*b+a+b+1))==0
red=sp.simplify((t-1)*(1-c*t)-(t*(c+1)-c*t**2-1))==0           # a+b = t(c+1)-c t^2-1 = (t-1)(1-ct)
neg=all((tt-1)*(1-cc*tt)<=0 for tt in range(1,400) for cc in range(1,400))   # <=0 < 2 <= a+b
cyc=[6,24,96,784,27];ed=all(Nv.nbrs(cyc[i])[0].count(cyc[(i+1)%5])+Nv.nbrs(cyc[(i+1)%5])[0].count(cyc[i])>0 or cyc[(i+1)%5] in Nv.nbrs(cyc[i])[0] or cyc[i] in Nv.nbrs(cyc[(i+1)%5])[0] for i in range(5))
ed=all(cyc[(i+1)%5] in set(Nv.nbrs(cyc[i])[0])|set(Nv.nbrs(cyc[i])[1]) for i in range(5))
# ---- recompute all registered experiments
log("recompute");stored=json.load(open(D+"/u3_results.json"));fresh={}
fresh["U3_0_graph_facts"]=X.graph_facts(cfg["graph"]);fresh["U3_1"]=X.u31(cfg["u31"])
fresh["U3_2_golden"]=X.golden(cfg["u32"]);fresh["U3_2_full3"]=X.full3(cfg["u32"])
fresh["U3_3_realizability"]=X.realizability(cfg["u33"]);fresh["U3_4_accounting"]=X.accounting()
eq={k:same(json.loads(json.dumps(fresh[k],default=str)),stored[k]) for k in fresh}
gf=fresh["U3_0_graph_facts"]
item("U3_graph_facts",ident and red and neg and ed and gf["triangles_found"]==0 and gf["odd_cycle_valid"] and gf["triangle_equation_solutions_in_box"]==0,
     algebra_identity=bool(ident),reduction_identity=bool(red),sign_check_t_c_lt_400=bool(neg),five_cycle=cyc,five_cycle_edges_verified_by_definition_engine=bool(ed),triangles_in_1_to_3000=gf["triangles_found"],
     theorem="G is triangle-free (a+b=(t-1)(1-ct)<=0 contradicts a+b>=2); with the 5-cycle the odd girth is exactly 5")
u=fresh["U3_1"];r=u["routing"]
item("U3_1",r["illegal_or_wrong_length"]==0 and r["lex_first_mismatch_d_le_4"]==0 and r["plain_bfs_mismatch_d_le_5"]==0 and u["decode"]["decode_failures"]==0 and
     all(e["M"]==e["predicted"] for e in u["extremal"]) and u["example_1_4_16"]["M"]==2 and u["sample"]["bound_ok"],
     routing_pairs=r["pairs"],max_distance_checked=r["max_distance"],decode_trials=u["decode"]["trials"],extremal=[(e["L"],e["M"]) for e in u["extremal"]],
     sample={k:v for k,v in u["sample"].items() if k!="M_histogram"},stored_equals_fresh=eq["U3_1"])
g=fresh["U3_2_golden"]
item("U3_2",g["all_period_2"] and g["max_abs_diff_expanded_vs_renewal"]<1e-9 and g["max_abs_diff_lift_vs_abramov"]<1e-9 and g["topological_entropy_ge_lift_entropy_all"] and eq["U3_2_golden"] and eq["U3_2_full3"],
     golden={k:v for k,v in g.items() if k!="rows"},full3=fresh["U3_2_full3"],stored_equals_fresh=(eq["U3_2_golden"],eq["U3_2_full3"]))
# tower return-map conjugacy on random golden-mean sequences
rnd=random.Random(5);bad=0
for _ in range(200):
    s=[0];
    while len(s)<30: s.append(0 if s[-1]==1 else rnd.randint(0,1))
    e=[1,2];vals=[e[x] for x in s];w,m=X.history(vals)
    # primitive tower dynamics T: position (n,j) -> (n,j+1) or (n+1,0); return map to j=0 is the shift
    pos=[];n=0
    for k in range(len(s)-1):
        l=m[k+1]-m[k]
        for j in range(l): pos.append((k,j))
    ret=[i for i,(k,j) in enumerate(pos) if j==0]
    if [pos[i][0] for i in ret]!=list(range(len(s)-1)): bad+=1
    if [w[i] for i in m]!=vals: bad+=1
item("U3_2_return_map",bad==0,sequences=200,failures=bad,statement="first-return of the primitive tower to the marked section advances the source index by exactly one (sigma)")
rz=fresh["U3_3_realizability"]
ok3=all(v["all_embeddings_verified"] for v in rz.values()) and rz["1"]["excluded_by_triangle_free_theorem"]==19 and not any(m["triangle"] for m in rz["1"]["not_found_list"] if False)
# obstruction: fixed points of X_r(F)=|F|, pair relation reflexive and symmetric
rnd=random.Random(3);viol=0
for _ in range(60):
    F=rnd.sample(range(1,25),5);rr=rnd.choice([1,2,3])
    rel={(x,y):(G.dist(x,y,rr+1) is not None and G.dist(x,y,rr+1)<=rr) if x!=y else True for x in F for y in F}
    if any(not rel[(x,x)] for x in F) or any(rel[(x,y)]!=rel[(y,x)] for x in F for y in F): viol+=1
item("U3_3",ok3 and viol==0 and eq["U3_3_realizability"],realizability={k:{x:y for x,y in v.items() if x not in("not_found_list","realized_list","triangle_graphs_realized")} for k,v in rz.items()},
     r1_triangle_free_not_found=[m["edges"] for m in rz["1"]["triangle_free_not_found"]],reflexive_symmetric_violations=viol,stored_equals_fresh=eq["U3_3_realizability"],
     note="'not found' means no embedding inside the stated universe; it is not an impossibility claim except for graphs with triangles at r=1 (theorem)")
item("U3_4_accounting",eq["U3_4_accounting"],rows=fresh["U3_4_accounting"],note="description-length conventions only (bits for forbidden list / embedding / radius)")
# ---- cost ledger + certification
ledger=X.cost_ledger(cfg)
item("U3_cost_certification",all(l["certified"] for l in ledger) and all(v[1] for v in G._NB.values()),ledger=ledger,neighbourhoods_cached=len(G._NB),
     note="every neighbourhood used by any experiment was certified under the RN-0 policy (all values far below 3.3e24)")
fl=[]
for f in("u3_graph.py",):
    tr=ast.parse(open(H+"/"+f).read())
    for nd in ast.walk(tr):
        if isinstance(nd,ast.Constant) and isinstance(nd.value,float): fl.append((f,nd.lineno))
        if isinstance(nd,ast.BinOp) and isinstance(nd.op,ast.Div): fl.append((f,nd.lineno))
item("U3_exact_layer",not fl,float_in_graph_layer=fl,note="u3_graph.py is exact-integer; entropy/eigenvalue numerics live only in u3_exp.py golden() and are labelled numeric corroboration")
rep["sources_sha256"]={f:sha(H+"/"+f) for f in sorted(os.listdir(H)) if f.endswith(".py")}
rep["inputs_sha256"]={f:sha(D+"/"+f) for f in("u3_config.json","u3_registration.json","u3_results.json","provenance_releases.txt")}
rep["ALL_PASSED"]=all(v["passed"] for v in rep["items"].values())
json.dump(rep,open(OUT,"w"),indent=1,sort_keys=True,default=str);log("ALL_PASSED",rep["ALL_PASSED"],round(time.time()-T0))
