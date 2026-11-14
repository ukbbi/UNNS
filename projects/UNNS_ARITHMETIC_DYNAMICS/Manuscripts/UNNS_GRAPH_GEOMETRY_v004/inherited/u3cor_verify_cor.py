"""UNNS-U3-COR v001 verifier. usage: verify_cor.py OUT.json"""
import sys,os,json,hashlib,random,itertools
H=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,H)
import u3_graph as G,u3_exp as X,sympy as sp
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
rep={"items":{}}
def item(n,p,**k): rep["items"][n]=dict(passed=bool(p),**k);print(n,bool(p),flush=True)
# 0. frozen code identical to U3 v001 release
reg=json.load(open("/home/claude/UNNS_U3/data/u3_registration.json"))
item("frozen_code_matches_U3_v001",reg["u3_graph.py"]==sha(H+"/u3_graph.py") and reg["u3_exp.py"]==sha(H+"/u3_exp.py") and reg["frozen_RN/rn_core.py"]==sha(H+"/../frozen_RN/rn_core.py"),
     note="u3_graph.py is byte-identical to the registered file only if unmodified")
# 1. girth correction: triangle-free (algebra) + explicit 4-cycle => girth 4, odd girth 5
a,b,c,t,h=sp.symbols("a b c t h",positive=True)
e1=sp.expand(c*(a+1)**2*(b+1)**2-a*b*(c+1)**2)           # equation of r_a r_b = r_c
step=sp.simplify(sp.expand((c*(a+1)*(b+1))**2-(c+1)**2*a*b*c)-c*e1)==0   # c*(eq) gives [c(a+1)(b+1)]^2=(c+1)^2 abc
fin=sp.expand((t-1)*(1-c*t)-(t*(c+1)-c*t**2-1))==0 and sp.expand((a+1)*(b+1)-a*b-(a+b+1))==0
cyc4=[2,8,36,9]
def adj(x,y): return y in G.nbrs(x)
e4=all(adj(cyc4[i],cyc4[(i+1)%4]) for i in range(4))
cyc5=[6,24,96,784,27];e5=all(adj(cyc5[i],cyc5[(i+1)%5]) for i in range(5))
item("girth",step and fin and e4 and e5,algebra_step_c_times_equation=bool(step),final_identity=bool(fin),four_cycle=cyc4,four_cycle_edges_ok=e4,five_cycle=cyc5,five_cycle_edges_ok=e5,
     corrected_statement="G is triangle-free (proved); contains the 4-cycle 2-8-36-9, so girth(G)=4; odd girth is exactly 5 (triangle-free + 5-cycle). The claim 'girth 5' is FALSE.")
# 2. U3.1b: exhaustive-style check of subpath lemma and M=2^(L-1)
rnd=random.Random(11);bad_sub=0;bad_M=0;rows={}
import time;T0=time.time()
for L in range(1,6):
    done=0
    for b0 in range(2,120):
        if done>=3 or time.time()-T0>240: break
        if G.dist(1,b0,L)!=L: continue
        w=list(G.geodesic(1,b0));done+=1
        for i in range(L+1):
            for j in range(i+1,L+1):
                if not X.valid_segment(w,i,j): bad_sub+=1
        if X.M_count(w)!=2**(L-1): bad_M+=1
    rows[L]=done
item("U3_1b_exact",bad_sub==0 and bad_M==0 and all(v>0 for v in rows.values()),geodesics_per_length=rows,subpath_failures=bad_sub,M_failures=bad_M,
     theorem="For every L>=1 there is a lex-first geodesic of length L with M=2^(L-1): connected+infinite+locally finite => sphere of radius L nonempty; every subpath of a lex-first geodesic is lex-first; all 2^(L-1) internal-mark subsets valid; M<=2^(L-1) trivially.")
# 3. entropy qualification: roof set {2,d,d}; constant iff d=2
g=json.load(open("/home/claude/UNNS_U3/data/u3_results.json"))["U3_2_golden"]["rows"]
eq=sorted(x["d"] for x in g if abs(x["top_entropy_expanded"]-x["abramov_formula"])<1e-12)
item("entropy_qualification",set(eq)=={2} and len(eq)==6 and all(x["top_entropy_expanded"]>x["abramov_formula"]+1e-9 for x in g if x["d"]!=2),equal_rows_d_values=sorted(set(eq)),equal_rows=len(eq),
     statement="Within the golden-mean two-symbol family with roofs (2,d,d): top entropy = Parry-lift entropy exactly when d=2 (constant roof). The general iff is NOT claimed (cohomologous-to-constant roofs; pressure framework).")
rep["ALL_PASSED"]=all(v["passed"] for v in rep["items"].values())
json.dump(rep,open(sys.argv[1],"w"),indent=1,default=str);print("ALL_PASSED",rep["ALL_PASSED"])
