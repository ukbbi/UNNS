"""usage: build_ki.py REPORT DATA MANUSCRIPT FIGURES -> numbers.tex, tables, figures"""
import sys,json,collections,os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
REP,DATA,MAN,FIG=sys.argv[1:5]
rep=json.load(open(REP)); k1=json.load(open(DATA+"/ki1_identities.json")); k2=json.load(open(DATA+"/ki2_degrees.json")); cost=json.load(open(DATA+"/cost_records_ki.json"))
def n(x): return f"{x:,}".replace(",","\\,")
def pct(a,b): return f"{100*(1-b/a):.1f}"
N=[]
def mac(name,val): N.append("\\newcommand{\\%s}{%s}"%(name,val))
led=rep["items"]["ledger"]
fam3=[("Fib","fibonacci"),("SqD","squares_direct"),("SqW","squares_wrapper")]
for tag,f in fam3:
    L=led[f]; mac(tag+"Total",L['total']); mac(tag+"Const",L['const']); mac(tag+"Aff",L['affine']); mac(tag+"Quad",L['quad']); mac(tag+"Closed",L['closed_form']); mac(tag+"Rec",L['not_closed_form'])
    mac(tag+"ClosedPct",f"{100*L['closed_form']/L['total']:.1f}")
for tag,f in (("Fib","fibonacci"),("SqD","squares_direct"),("SqW","squares_wrapper")):
    it={"Fib":rep["items"]["K3_fibonacci"]["totals_route"]}.get(tag) or rep["items"]["K3_squares_direct" if tag=="SqD" else "K3_squares_wrapper"]["totals"]
    mac(tag+"IterB",n(it['b_iters'])); mac(tag+"IterK",n(it['k_iters'])); mac(tag+"IterRed",pct(it['b_iters'],it['k_iters']))
    mac(tag+"RecB",n(it['b_rec'])); mac(tag+"RecK",n(it['k_rec'])); mac(tag+"RecRed",pct(it['b_rec'],it['k_rec']))
    mac(tag+"OpsB",n(it['b_ops'])); mac(tag+"OpsK",n(it['k_ops'])); mac(tag+"OpsRed",pct(it['b_ops'],it['k_ops']))
    mac(tag+"Short",n(it['k_short']))
kf=rep["items"]["K3_fibonacci"]; mac("FibInputs",kf['inputs']); mac("FibRouteInputs",kf['route_inputs']); mac("FibSmallInputs",kf['small_table_inputs']); mac("FibRejects",n(kf['reject_cases']))
mac("FibMaxIterB",n(kf['max_b_iters'])); mac("FibMaxIterK",n(kf['max_k_iters']))
for tag,key in (("SqD","K3_squares_direct"),("SqW","K3_squares_wrapper")):
    k=rep["items"][key]; mac(tag+"Inputs",n(k['inputs'])); mac(tag+"Rejects",n(k['reject_cases'])); mac(tag+"MaxMoves",k['max_moves'])
mac("FibMaxMoves",kf['max_moves'])
cs=led["control_states"]; mac("CtrlFib",cs['fibonacci']); mac("CtrlSqD",cs['squares_direct']); mac("CtrlSqW",cs['squares_wrapper'])
mac("ConstAll",sum(led[f]['const'] for _,f in fam3)); mac("AffAll",sum(led[f]['affine'] for _,f in fam3)); mac("QuadAll",sum(led[f]['quad'] for _,f in fam3))
mac("ClosedAll",sum(led[f]['closed_form'] for _,f in fam3)); mac("RecAll",sum(led[f]['not_closed_form'] for _,f in fam3)); mac("StepsAll",sum(led[f]['total'] for _,f in fam3))
for tag,f,key in (("Fib","fibonacci","fibonacci"),("SqD","squares_direct","squares_direct"),("SqW","squares_wrapper","squares_wrapper")):
    rows=[r for r in cost[key] if r.get('status','route')=='route']
    mac(tag+"MeanRecB",f"{sum(r['b_rec'] for r in rows)/len(rows):.2f}"); mac(tag+"MeanRecK",f"{sum(r['k_rec'] for r in rows)/len(rows):.2f}")
    mac(tag+"Regress",sum(1 for r in rows if r['k_ops']>r['b_ops'] or r['k_iters']>r['b_iters'])); mac(tag+"RouteN",n(len(rows)))
# degrees
dd=collections.Counter(); pow2=collections.Counter(); ten=[]
for f,v in k2.items():
    for key,Ls in v.items():
        for i,r in Ls.items():
            dd[(f,r['audit'],r['d'])]+=1
            if r['audit']=='field': pow2[(f,r['pow2'])]+=1
            if r['audit']=='unexplained': ten.append((int(key),int(i),r))
ten.sort(key=lambda z:(z[0],z[1]))
mac("NonClosed",sum(dd.values())); mac("FieldFib",sum(v for (f,a,d),v in dd.items() if f=='fibonacci' and a=='field'))
mac("FieldSq",sum(v for (f,a,d),v in dd.items() if f!='fibonacci'))
fieldnp2=sum(v for (f,p),v in pow2.items() if not p); fieldp2=sum(v for (f,p),v in pow2.items() if p)
mac("FieldNotPowTwo",fieldnp2); mac("FieldPowTwo",fieldp2)
mac("TenDegMin",min(r['d'] for _,_,r in ten)); mac("TenDegMax",max(r['d'] for _,_,r in ten))
mac("VerifierSha",__import__('hashlib').sha256(open(REP,'rb').read()).hexdigest()[:16])
open(MAN+"/numbers.tex","w").write("\n".join(N)+"\n")
# ---- tables
def sym(r): return {'const':'c','affine':'a','quad':'q','none':'R'}[r['kind']]
rows=[]
rows.append("\\begin{tabular}{@{}ll@{}}\\toprule class & step pattern ($\\mathtt{c}$ const, $\\mathtt{a}$ affine, $\\mathtt{q}$ one isqrt, $\\cdot$ recovery) \\\\\\midrule")
fibpat=" ".join(f"{r}:\\texttt{{{''.join(sym(x) for x in k1['fibonacci'][str(r)])}}}" for r in range(12))
sqdpat=" ".join(f"{r}:\\texttt{{{''.join(sym(x) for x in k1['squares_direct'][str(r)])}}}" for r in sorted(map(int,k1['squares_direct'])))
sqwpat=" ".join(f"{nm}:\\texttt{{{''.join(sym(x) for x in k1['squares_wrapper'][nm])}}}" for nm in sorted(k1['squares_wrapper']))
open(MAN+"/tab_patterns.tex","w").write("\\begin{description}[leftmargin=1.2em,itemsep=2pt,font=\\normalfont\\small]\n\\item[Fibonacci, $k \\bmod 12$:] "+fibpat+"\n\\item[Squares direct, $n \\bmod 24$:] "+sqdpat+"\n\\item[Squares wrapper, U2-001 class:] "+sqwpat+"\n\\end{description}\n".replace("\\texttt{","\\texttt{") if False else "\\begin{description}[leftmargin=1.2em,itemsep=2pt,font=\\normalfont\\small]\n\\item[Fibonacci, $k \\bmod 12$:] "+fibpat+"\n\\item[Squares direct, $n \\bmod 24$:] "+sqdpat+"\n\\item[Squares wrapper, U2-001 class:] "+sqwpat+"\n\\end{description}\n")
# ten table
T=["\\begin{tabular}{@{}rrrrrll@{}}\\toprule class & step & $\\deg_m N$ & $\\deg_m S$ & $d$ & $(p,s_0)$ & factor degrees of $S(m)=s_0 \\bmod p$ \\\\\\midrule"]
for cl,st,r in ten:
    tw=r['tower']; T.append(f"{cl} & {st} & {r['degN']} & {r['degS']} & {r['d']} & ({tw['prime']},{tw['s0']}) & {{\\footnotesize ${','.join(map(str,tw['factor_degrees']))}$}}; order {tw['order']} \\\\")
T.append("\\bottomrule\\end{tabular}")
open(MAN+"/tab_ten.tex","w").write("\n".join(T)+"\n")
# degree distribution table
D=["\\begin{tabular}{@{}lrrrrrrrr@{}}\\toprule family / audit class & $d{=}3$ & $4$ & $6$ & $8$ & $10$ & $12$ & $14$ & $16$ \\\\\\midrule"]
for lab,sel in (("Fibonacci, \\emph{field}",lambda f,a:f=='fibonacci' and a=='field'),("Fibonacci, \\emph{unexplained}",lambda f,a:f=='fibonacci' and a=='unexplained'),("Squares (direct + wrapper), \\emph{field}",lambda f,a:f!='fibonacci')):
    c=collections.Counter()
    for (f,a,d),v in dd.items():
        if sel(f,a): c[d]+=v
    D.append(lab+" & "+" & ".join(str(c.get(d,0)) if c.get(d,0) else "--" for d in (3,4,6,8,10,12,14,16))+" \\\\")
D.append("\\bottomrule\\end{tabular}")
open(MAN+"/tab_degrees.tex","w").write("\n".join(D)+"\n")
# ---- figures
os.makedirs(FIG,exist_ok=True)
plt.rcParams.update({"font.size":8,"axes.spines.top":False,"axes.spines.right":False})
C=["#6b7a8f","#2f7fa8","#d98e2b","#b8433a"]
fig,ax=plt.subplots(figsize=(6.4,2.2))
labs=["Fibonacci\n(99 steps)","Squares direct\n(105 steps)","Squares wrapper\n(64 steps)"]
for j,(tag,f) in enumerate(fam3):
    L=led[f]; left=0
    for val,col,nm in ((L['const'],C[0],"constant label"),(L['affine'],C[1],"affine in state"),(L['quad'],C[2],"one isqrt of state"),(L['not_closed_form'],C[3],"recovery required")):
        ax.barh(j,val,left=left,color=col,label=nm if j==0 else None,edgecolor="white")
        if val>=6: ax.text(left+val/2,j,str(val),ha="center",va="center",color="white",fontsize=7)
        left+=val
ax.set_yticks(range(3)); ax.set_yticklabels(labs); ax.invert_yaxis(); ax.set_xlabel("route steps")
ax.legend(ncol=4,fontsize=6.5,frameon=False,loc="upper center",bbox_to_anchor=(0.5,1.25))
fig.tight_layout(); fig.savefig(FIG+"/fig1_categories.pdf"); fig.savefig(FIG+"/fig1_categories.png",dpi=200); plt.close(fig)
fig,axs=plt.subplots(1,3,figsize=(6.8,2.3))
f=[r for r in cost['fibonacci'] if r['status']=='route']
axs[0].plot([r['k'] for r in f],[r['b_iters'] for r in f],".",ms=1.5,color=C[0],label="baseline R3"); axs[0].plot([r['k'] for r in f],[r['k_iters'] for r in f],".",ms=1.5,color=C[1],label="KI")
axs[0].set_xlabel("index $k$"); axs[0].set_ylabel("bisection iterations"); axs[0].set_title("Fibonacci",fontsize=8); axs[0].legend(markerscale=5,frameon=False,fontsize=6.5)
for ax,key,tt in ((axs[1],'squares_direct',"Squares direct"),(axs[2],'squares_wrapper',"Squares wrapper")):
    rows=[r for r in cost[key] if r['n']>=30]; xs=[r['bits'] for r in rows]
    ax.plot(xs,[max(r['b_iters'],0.8) for r in rows],".",ms=1.5,color=C[0]); ax.plot(xs,[max(r['k_iters'],0.8) for r in rows],".",ms=1.5,color=C[1])
    ax.set_yscale("log"); ax.set_xlabel("bits of $x$"); ax.set_title(tt,fontsize=8)
axs[1].set_ylabel("bisection iterations")
fig.tight_layout(); fig.savefig(FIG+"/fig2_cost.pdf"); fig.savefig(FIG+"/fig2_cost.png",dpi=200); plt.close(fig)
fig,ax=plt.subplots(figsize=(4.6,2.2))
ds=sorted({d for (f,a,d) in dd}); w=0.38
fa=[sum(v for (f,a,d),v in dd.items() if d==x and a!='unexplained') for x in ds]; un=[sum(v for (f,a,d),v in dd.items() if d==x and a=='unexplained') for x in ds]
ax.bar(range(len(ds)),fa,color=C[0],label="audit: field (51 + 21 steps)"); ax.bar(range(len(ds)),un,bottom=fa,color=C[3],label="audit: unexplained (10 labels)")
ax.set_xticks(range(len(ds))); ax.set_xticklabels(ds); ax.set_xlabel("exact degree $d=[\\mathbb{Q}(S,N):\\mathbb{Q}(S)]$"); ax.set_ylabel("steps"); ax.legend(frameon=False,fontsize=6.5)
fig.tight_layout(); fig.savefig(FIG+"/fig3_degrees.pdf"); fig.savefig(FIG+"/fig3_degrees.png",dpi=200); plt.close(fig)
print("built")
