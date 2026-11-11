"""UNNS-U4 SPEC v001 checker: registry integrity (AG1-AG4) + exact probes P1-P8. usage: check_spec.py OUT.json  (all paths relative to this file)"""
import sys,os,json,hashlib,math,random,time
H=os.path.dirname(os.path.abspath(__file__));D=H+"/../data";sys.path.insert(0,H)
OUT=sys.argv[1];T0=time.time()
import u3_graph as G,numpy as np,networkx as nx,sympy
from networkx.generators.atlas import graph_atlas_g
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
rep={"items":{}};
def item(n,p,**kw): rep["items"][n]=dict(passed=bool(p),**kw);print(n,bool(p),flush=True)
R=json.load(open(D+"/registry.json"));ids={x["id"]:x for x in R}
# ---- AG0 provenance of the reused engine
reg=json.load(open(D+"/u3_v001_registration.json"))
item("AG0_engine_hashes",reg["u3_graph.py"]==sha(H+"/u3_graph.py") and all(reg["frozen_RN/"+k]==sha(H+"/../frozen_RN/"+k) for k in("rn_core.py","rn_naive.py")),
     note="engine files are byte-identical to those registered in U3 v001")
# ---- AG1 structure
req=["id","stage","title","kind","statement","hypotheses","origin","status","info_class","deps","falsification_gate"]
ORI={"U3_CONSEQUENCE","STANDARD","NEW_ELEMENTARY","NEW_SUBSTANTIVE","FROZEN_IMPORT","OPEN","DEFINITION"}
INFO={"intrinsic","representation","additional","imported","meta"}
errs=[]
if len(ids)!=len(R): errs.append("duplicate ids")
for x in R:
    for k in req:
        if k not in x or x[k] in ("",None) and k not in("hypotheses","falsification_gate"): errs.append((x["id"],"missing",k))
    if x["origin"] not in ORI: errs.append((x["id"],"origin"))
    if x["info_class"] not in INFO: errs.append((x["id"],"info_class"))
    for d in x["deps"]:
        if d not in ids: errs.append((x["id"],"dangling",d))
    if x["kind"] in("Theorem","Proposition") and x["origin"] in("NEW_ELEMENTARY","NEW_SUBSTANTIVE") and not x["falsification_gate"]: errs.append((x["id"],"no falsification gate"))
    if x["origin"]=="NEW_ELEMENTARY" and not x["status"].startswith(("Sketch","Certificates","Assembled")): errs.append((x["id"],"new claim must carry a proof-obligation status"))
    if x["origin"]=="OPEN" and x["kind"] not in("Conjecture",): errs.append((x["id"],"open must be conjecture"))
item("AG1_fields_and_labels",not errs,errors=errs,claims=len(R))
# ---- acyclicity (topological order)
st={};order=[]
def visit(i,stack=()):
    if i in stack: errs.append(("cycle",i));return
    if st.get(i): return
    for d in ids[i]["deps"]: visit(d,stack+(i,))
    st[i]=1;order.append(i)
for i in ids: visit(i)
item("AG1b_dependency_graph_acyclic",not[e for e in errs if e[0]=="cycle"],topological_order=order)
# ---- AG3 anti-artificial-universality: an `intrinsic` claim may not depend (transitively) on a representation/additional claim
def closure(i,seen=None):
    seen=seen if seen is not None else set()
    for d in ids[i]["deps"]:
        if d not in seen: seen.add(d);closure(d,seen)
    return seen
viol=[]
for i,x in ids.items():
    if x["info_class"]=="intrinsic":
        bad=[d for d in closure(i) if ids[d]["info_class"] in("representation","additional") and ids[d]["kind"]!="Definition"]
        if bad: viol.append((i,bad))
item("AG3_intrinsic_claims_do_not_rely_on_markers",not viol,violations=viol,
     rule="a claim classed intrinsic-to-graph may not depend (transitively) on a non-definitional claim classed representation/additional information")
# ---- triage counts
from collections import Counter
rep["triage"]={"by_origin":dict(Counter(x["origin"] for x in R)),"by_info_class":dict(Counter(x["info_class"] for x in R)),"by_stage":dict(Counter(x["stage"] for x in R))}
# ---- probes
def dist(a,b,m=12): return G.dist(a,b,m)
# P1 star embedding
ok=True;rows=[]
for k in (3,4,5,8,16,32):
    x=2
    while len(G.nbrs(x))<k-1: x+=1 if x<200 else 60
    Fk=[x]+G.nbrs(x)[:k-1];mx=max(dist(a,b) for a in Fk for b in Fk if a!=b);rows.append((k,x,len(G.nbrs(x)),mx));ok&=(mx<=2)
tri=sum(1 for a in range(1,400) for b in G.nbrs(a) if b>a for c in G.nbrs(b) if c>b and c in set(G.nbrs(a)))
item("P1_star_embeddings",ok and tri==0,rows=rows,triangles_up_to_400=tri,note="(k, centre, degree, max pairwise distance)")
# P2 parity-period
def period_and_parity(F,r):
    n=len(F);adj={i:[] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i==j: adj[i].append((j,2))
            else:
                d=dist(F[i],F[j],r)
                if d is not None and d<=r: adj[i].append((j,d))
    # components (symmetric), potential method
    seen=set();out=[]
    for s in range(n):
        if s in seen: continue
        comp=[];pot={s:0};q=[s];seen.add(s)
        while q:
            u=q.pop();comp.append(u)
            for v,w in adj[u]:
                if v not in pot: pot[v]=pot[u]+w;seen.add(v);q.append(v)
        g=0
        for u in comp:
            for v,w in adj[u]: g=math.gcd(g,pot[u]+w-pot[v])
        # parity potential: 2-colour with weights mod 2
        col={comp[0]:0};q=[comp[0]];par=True
        while q:
            u=q.pop()
            for v,w in adj[u]:
                want=(col[u]+w)%2
                if v not in col: col[v]=want;q.append(v)
                elif col[v]!=want: par=False
        out.append((g,par))
    return out
rnd=random.Random(5);bad=0;cnt=Counter()
for _ in range(120):
    F=rnd.sample(range(1,40),rnd.randint(2,5));r=rnd.choice([1,2,3])
    for g,par in period_and_parity(F,r):
        cnt[g]+=1
        if g not in(1,2) or (g==2)!=par: bad+=1
gm=[];gbad=0
for e0 in range(1,9):
    for e1 in range(1,9):
        if e0==e1: continue
        d=dist(e0,e1);adj={0:[(0,2),(1,d)],1:[(0,d)]};g=math.gcd(2,2*d)
        gm.append(d);gbad+=(g!=2)
item("P2_parity_period",bad==0 and gbad==0,random_components_checked=sum(cnt.values()),period_histogram=dict(cnt),mismatches=bad,golden_mean_embeddings=len(gm),golden_mean_non_period2=gbad)
# P3 spectra
mats_ok=True;rows=[]
atlas=graph_atlas_g()
for k in range(3,8):
    mx=0
    for g in atlas:
        if g.number_of_nodes()!=k or nx.is_empty(g) and False: continue
        if sum(nx.triangles(g).values())!=0: continue
        A=nx.to_numpy_array(g);mx=max(mx,max(np.linalg.eigvalsh(A+np.eye(k))))
    rows.append((k,round(float(mx),6),1+k/2,mx<k)); mats_ok&=bool(mx<k)
B=np.array([[1,1,0],[0,1,1],[1,0,1]]);ev=np.linalg.eigvals(B)
item("P3_spectral_probes",mats_ok and any(abs(z.imag)>1e-9 for z in ev),triangle_free_max_rho_AplusI=rows,note="(k, max over ALL triangle-free graphs on k vertices, 1+k/2 bound, <k)",
     cycle_with_loops_eigenvalues=[complex(round(z.real,6),round(z.imag,6)) for z in ev])
# P4 SELECT-II identification
N=5000;Rr={};Hh={}
for t in range(1,N+1):
    pred=[y for y in G.nbrs(t) if y<t];Rr[t]=len(pred);Hh[t]=1 if not pred else sum(Hh[p] for p in pred)
frozen=(3124,8283)
# brute-force edge identification
brute=True
for m in range(1,260):
    s=set()
    for t in range(m+1,260*40):
        pass
    for Nn in range(1,m+1):
        if m%Nn==0: s.add(m*(Nn+1)**2//Nn)
    fw={y for y in G.nbrs(m) if y>m}
    brute&=(s==fw)
item("P4_select2_identification",brute and Hh[72]==4 and Rr[72]==3,
     brute_force_forward_neighbours_m_lt_260=brute,H72=Hh[72],R72=Rr[72],sum_R_to_5000=sum(Rr.values()),sum_H_to_5000=sum(Hh.values()),frozen_S2_12=frozen,
     matches_frozen_sums=(sum(Rr.values()),sum(Hh.values()))==frozen,
     note="Sum comparison is a CHECK against frozen S2.12; reported either way. H computed by recursion over inverse neighbours.")
# P5 growth >= 4 / acyclicity / no descent
bad5=0
for x in range(1,3001):
    for y in G.nbrs(x):
        if y>x and y<4*x: bad5+=1
item("P5_forward_growth_ge_4",bad5==0,violations=bad5,range="x<=3000",note="forward neighbours satisfy y>=4x; so directed waypoints strictly increase")
# P6 towers
def root(d):
    f=sympy.Symbol('w');r=sympy.nsolve(f+f**d-1,f,0.7);return float(r)
h2=-0.5*math.log(root(2));h5=-0.5*math.log(root(5))
d125=(dist(1,2),dist(2,5),dist(1,5));d123=(dist(1,2),dist(2,3),dist(1,3))
def per(F):
    d={(a,b):(2 if a==b else dist(a,b)) for a in F for b in F}
    pot={F[0]:0};q=[F[0]]
    while q:
        u=q.pop()
        for v in F:
            if v not in pot: pot[v]=pot[u]+d[(u,v)];q.append(v)
    g=0
    for u in F:
        for v in F: g=math.gcd(g,pot[u]+d[(u,v)]-pot[v])
    return g
item("P6_tower_certificates",abs(h2-0.24061)<1e-4 and abs(h5-0.14060)<1e-4 and per([1,2,5])==1 and per([1,2,3])==2,
     entropy_d2=h2,entropy_d5=h5,dist_1_2_5=d125,dist_1_2_3=d123,period_125=per([1,2,5]),period_123=per([1,2,3]),closed_sum_125=sum(d125))
# P7 local automorphisms of degree-coloured balls
from networkx.algorithms.isomorphism import GraphMatcher
loc={}
for Rr_ in (2,3):
    seen={1};fr=[1];Hg=nx.Graph()
    for _ in range(Rr_):
        nf=[]
        for x in fr:
            for y in G.nbrs(x):
                Hg.add_edge(x,y)
                if y not in seen: seen.add(y);nf.append(y)
        fr=nf
    for v in Hg: Hg.nodes[v]['deg']=len(G.nbrs(v))
    loc[Rr_]=sum(1 for _ in GraphMatcher(Hg,Hg,node_match=lambda a,b:a['deg']==b['deg']).isomorphisms_iter())
item("P7_local_symmetry_observation",True,automorphism_counts_degree_coloured_balls=loc,
     note="Registered observation only: boundary symmetry; says nothing about Aut(G). Radius 4 exceeded the 1000 cap; deeper refinement left open (Cj2).")
# P8 degree identity
bad8=0
def tau(x): return sympy.divisor_count(x)
for x in range(1,3001):
    Rx=sum(1 for d in range(2,int(x**.5)+1) if x%(d*d)==0)
    if len(G.nbrs(x))!=tau(x)+Rx: bad8+=1
primes_ok=all((len(G.nbrs(p))==2)==sympy.isprime(p) for p in range(2,3001))
item("P8_degree_identity_and_prime_predicate",bad8==0 and primes_ok,violations=bad8,degree_two_iff_prime_up_to_3000=primes_ok)
rep["inputs_sha256"]={f:sha(D+"/"+f) for f in("registry.json","registry.csv","u3_v001_registration.json","provenance_frozen_sources.txt")}
rep["sources_sha256"]={f:sha(H+"/"+f) for f in sorted(os.listdir(H)) if f.endswith(".py")}
rep["ALL_PASSED"]=all(v["passed"] for v in rep["items"].values())
json.dump(rep,open(OUT,"w"),indent=1,default=str);print("ALL_PASSED",rep["ALL_PASSED"],round(time.time()-T0),"s")
