import sys,json,math
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rep=json.load(open(sys.argv[1])); out=sys.argv[2]; data=sys.argv[3]
AU=json.load(open(data+"/state_audit.json")); COST=json.load(open(data+"/cost_records.json"))
LED=rep["R9"]["ledger"]; S=AU["summary"]
blue,amber,red,grey,green="#4a78a8","#f2b138","#c0392b","#8a8a8a","#5a9e6f"
cats=["const","local","algstate","field","target","unexplained"]
lab={"const":"constant","local":"poly in current state","algstate":"algebraic in current state","field":"route-start field","target":"destination state only","unexplained":"not found"}
col={"const":"#d9d9d9","local":green,"algstate":"#9ccc9c","field":blue,"target":amber,"unexplained":red}
nm=dict(NFib=S["fibonacci"]["total"],NSqD=S["squares_direct"]["total"],NSqW=S["squares_wrapper"]["total"],
        FibQ=LED["fibonacci"]["control_states"],SqDQ=LED["squares_direct"]["control_states"],SqWQ=LED["squares_wrapper"]["control_states"],
        FibSmallMoves=LED["fibonacci"]["small_table_moves"],FibSmallPaths=LED["fibonacci"]["small_table_paths"],
        FibMaxDeg=LED["fibonacci"]["max_state_function_degree"],
        NAccRef=rep["R4"]["accepted"]+rep["R4"]["refused"],NAdv=rep["R4"]["adversarial"],NRad=rep["R1"]["cases"],
        NStates=rep["R2"]["cases"],NCrit=rep["R4a"]["cases"],VerSha=rep["verifier_sha256"][:16],
        FibItersMax=rep["R8"]["fibonacci"]["iters"]["max"],FibItersMean=rep["R8"]["fibonacci"]["iters"]["mean"],
        SqDItersMax=rep["R8"]["squares_direct"]["iters"]["max"],SqWItersMax=rep["R8"]["squares_wrapper"]["iters"]["max"])
for k,nmk in (("fibonacci","Fib"),("squares_direct","SqD"),("squares_wrapper","SqW")):
    rows=COST[k]; nm[nmk+"Slope"]="%.1f"%(sum(r["bits"]*r["iters"] for r in rows)/sum(r["bits"]**2 for r in rows))
    nm[nmk+"NoRec"]=sum(S[k]["counts"].get(c,0) for c in ("const","local","algstate")); 
for k in ("fibonacci","squares_direct","squares_wrapper"):
    for c in cats: nm["C"+k[:4].capitalize()+k[-1].upper()+c.capitalize()]=S[k]["counts"].get(c,0)
with open(out+"/numbers.tex","w") as f:
    for k,v in nm.items(): f.write("\\newcommand{\\%s}{%s}\n"%(k,v))
# ledger table
def pct(k,cs): return "%d/%d"%(sum(S[k]["counts"].get(c,0) for c in cs),S[k]["total"])
with open(out+"/audit_table.tex","w") as f:
    f.write("\\begin{tabular}{@{}lrrrrrrr@{}}\\toprule & steps & const & local & alg.\\ in $S$ & field & dest. only & not found\\\\\\midrule\n")
    for k,nmk in (("fibonacci","Fibonacci"),("squares_direct","Squares, direct"),("squares_wrapper","Squares, wrapper")):
        c=S[k]["counts"]; f.write("%s & %d & %s\\\\\n"%(nmk,S[k]["total"]," & ".join(str(c.get(x,0)) for x in cats)))
    f.write("\\bottomrule\\end{tabular}\n")
with open(out+"/ledger_table.tex","w") as f:
    f.write("\\begin{tabular}{@{}p{3.1cm}p{3.6cm}p{3.6cm}p{3.6cm}@{}}\\toprule & Fibonacci & Squares, direct & Squares, wrapper\\\\\\midrule\n")
    MEM={"fibonacci":"\\texttt{isqrt} test: $5x^2+4$ or $5x^2-4$ a square","squares_direct":"\\texttt{isqrt} test: $x=n^2$","squares_wrapper":"\\texttt{isqrt} test: $x=n^2$"}
    DIS={"fibonacci":"$(x \\bmod 24,\\ y \\bmod 24)$, $y=(x+L_k)/2$","squares_direct":"$n \\bmod 24$","squares_wrapper":"$n \\bmod 24$ (class table inside U2-001)"}
    rows=[("Membership",lambda L:MEM[L["_k"]]),
          ("Fixed-modulus dispatch",lambda L:DIS[L["_k"]]),
          ("Parameter recovery",lambda L:{"fibonacci":"algebraic state functions $G_i$ (with $\\alpha_\\varepsilon$), exact radical bisection","squares_direct":"polynomial state functions, bisection","squares_wrapper":"polynomial state functions (U2-001), bisection"}[L["_k"]]),
          ("Control states",lambda L:str(L["control_states"])),
          ("Route labels",lambda L:str(L["route_labels"])),
          ("Moves (max)",lambda L:str(L["max_moves"])),
          ("Target value formed at READY",lambda L:"yes" if L["target_formed_in_ready"] else "no (computable)"),
          ("External information",lambda L:L["external_information"])]
    for nme,fn in rows:
        cells=[]
        for k in ("fibonacci","squares_direct","squares_wrapper"):
            L=dict(LED[k]); L["_k"]=k; cells.append(fn(L))
        f.write(nme+" & "+" & ".join(cells)+"\\\\\n")
    f.write("\\bottomrule\\end{tabular}\n")
# fig1: stacked bar of categories (fraction)
fig,ax=plt.subplots(figsize=(6.6,2.9))
names=[("fibonacci","Fibonacci"),("squares_direct","Squares, direct"),("squares_wrapper","Squares, wrapper")]
for yi,(k,nmk) in enumerate(names):
    left=0;tot=S[k]["total"]
    for c in cats:
        v=S[k]["counts"].get(c,0)/tot
        if v==0: continue
        ax.barh(yi,v,left=left,color=col[c],edgecolor="white",label=lab[c] if yi==0 or c not in S["fibonacci"]["counts"] else None)
        if v>0.05: ax.text(left+v/2,yi,str(S[k]["counts"][c]),ha="center",va="center",fontsize=8,color="white" if c in("field","unexplained") else "black")
        left+=v
ax.set_yticks(range(3)); ax.set_yticklabels([n for _,n in names]); ax.invert_yaxis(); ax.set_xlim(0,1); ax.set_xlabel("share of route steps")
h,l=ax.get_legend_handles_labels(); d=dict(zip(l,h)); ax.legend(d.values(),d.keys(),ncol=3,fontsize=7,frameon=False,loc="upper center",bbox_to_anchor=(.5,-.28))
[ax.spines[s].set_visible(False) for s in ("top","right")]
ax.set_title("What each route step needs: audit of every label",fontsize=9.5)
fig.savefig(out+"/figures/fig1_audit.pdf",bbox_inches="tight"); fig.savefig(out+"/figures/fig1_audit.png",dpi=150,bbox_inches="tight"); plt.close(fig)
# fig2: recovery cost vs input size
fig,ax=plt.subplots(figsize=(6.6,3.2))
fb=[(r["bits"],r["iters"]) for r in COST["fibonacci"]]; sd=[(r["bits"],r["iters"]) for r in COST["squares_direct"]]; sw=[(r["bits"],r["iters"]) for r in COST["squares_wrapper"]]
for pts,c,l in ((fb,blue,"Fibonacci (algebraic $G_i$)"),(sd,green,"Squares, direct"),(sw,amber,"Squares, wrapper")):
    ax.scatter([p[0] for p in pts],[p[1] for p in pts],s=5,color=c,label=l,alpha=.7)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("bit length of the input"); ax.set_ylabel("bisection iterations per input")
ax.legend(fontsize=7.5,frameon=False); [ax.spines[s].set_visible(False) for s in ("top","right")]
ax.set_title("Recovery work is separate from graph moves and grows with input size",fontsize=9.5)
fig.savefig(out+"/figures/fig2_cost.pdf",bbox_inches="tight"); fig.savefig(out+"/figures/fig2_cost.png",dpi=150,bbox_inches="tight"); plt.close(fig)
# per-class audit table for Fibonacci (appendix)
ab={"const":"c","local":"l","algstate":"a","field":"F","target":"t","unexplained":"?"}
with open(out+"/fib_class_audit.tex","w") as f:
    f.write("\\begin{tabular}{@{}rl@{}}\\toprule $k\\bmod 12$ & step categories (c const, l local, a algebraic in $S$, F route-start field, ? not found)\\\\\\midrule\n")
    for r in sorted(AU["per_step"]["fibonacci"],key=int):
        f.write("%s & \\texttt{%s}\\\\\n"%(r,"".join(ab[x["cat"]] for x in AU["per_step"]["fibonacci"][r])))
    f.write("\\bottomrule\\end{tabular}\n")
print("built")
