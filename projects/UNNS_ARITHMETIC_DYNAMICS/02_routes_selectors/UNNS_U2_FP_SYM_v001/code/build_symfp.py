import sys, json, re, math
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import fibresolve
from fibparam import F
rep=json.load(open(sys.argv[1])); out=sys.argv[2]; data=sys.argv[3]
paths=json.load(open(data+"/class_paths.json")); certs=json.load(open(data+"/class_certificates.json"))
small=json.load(open(data+"/small_fib_paths.json"))
blue,amber,red,grey="#4a78a8","#f2b138","#c0392b","#8a8a8a"
cov=rep["S3"]["classes_covered"]; opn=rep["S3"]["classes_open"]
tot=sum(v["cases"] for v in rep.values() if isinstance(v,dict) and "cases" in v)
maxlen=rep["S3"]["max_length"]
nm=dict(TotalCases=tot,VerSha=rep["verifier_sha256"][:16],NCov=len(cov),NOpen=len(opn),MaxLen=maxlen,
        NSmallMax=rep["S6"]["maximum"],NSelTest=rep["S5"]["cases"],NEdgeSteps=rep["S4"]["cases"],
        CtlStates=rep["S7"]["control_states_path"],MaxDeg=rep["S7"]["max_degree_in_b"],
        DenList=", ".join(str(d) for d in rep["S7"]["coefficient_denominators"] if d>1),OpenList=", ".join(map(str,opn)) if opn else "none",CovList=", ".join(map(str,cov)))
with open(out+"/numbers.tex","w") as f:
    for k,v in nm.items(): f.write("\\newcommand{\\%s}{%s}\n"%(k,v))
# atom names -> latex
AT={"a":"F_{h-1}","b":"F_h","c":"F_{h+1}","Lh":"L_h","Lh1":"L_{h+1}","Lhm":"L_{h-1}","Fh2":"F_{h+2}","Fh3":"F_{h+3}"}
def atom(t):
    m=re.fullmatch(r"(Lh1|Lhm|Lh|Fh2|Fh3|a|b|c)([+-]1)?",t); s=AT[m.group(1)]
    return s if not m.group(2) else "("+s+m.group(2)+")"
def lin(u,v,w,d,xs=("F_{h-1}","F_h")):
    parts=[]
    for co,s in ((u,xs[0]),(v,xs[1])):
        if co==0: continue
        c="" if abs(co)==1 else str(abs(co))
        parts.append(("-" if co<0 else "+")+c+s)
    if w: parts.append(("+" if w>0 else "-")+str(abs(w)))
    t="".join(parts).lstrip("+")
    return t if d==1 else "\\dfrac{%s}{%d}"%(t,d)
def form(e):
    if re.fullmatch(r"\d+",e): return e
    m=re.fullmatch(r"\((-?\d+)a([+-]\d+)b([+-]\d+)\)/(\d+)",e)
    if m: return lin(*map(int,m.groups()))
    m=re.fullmatch(r"\((-?\d+)x([+-]\d+)y([+-]\d+)\)/(\d+)",e)
    if m: return lin(*map(int,m.groups()),xs=("x","y"))
    m=re.fullmatch(r"\[(\d+)\*([^*]+)\*([^*]+)\]",e)
    if m:
        c="" if m.group(1)=="1" else m.group(1)
        p,q=atom(m.group(2)),atom(m.group(3))
        return c+(p+"^2" if p==q else p+q)
    raise ValueError(e)
def label(lab):
    if lab.startswith("S/"):
        e=form(lab[2:])
        if e=="1": return "S"
        return "S/"+e if re.fullmatch(r"[0-9A-Za-z_{}^+\-]+",e) and "+" not in e and "-" not in e.replace("{h-1}","") else "S/\\left("+e+"\\right)"
    if lab.startswith("q=sqrt(S/"): return "\\sqrt{S/\\left("+form(lab[9:-1])+"\\right)}-1"
    if lab.startswith("q="):
        e=lab[2:]
        if re.fullmatch(r"\d+",e): return str(int(e)-1)
        m=re.fullmatch(r"\((-?\d+)([ax])([+-]\d+)([by])([+-]\d+)\)/1",e)
        if m:
            u,v1,w,v2,c=m.groups(); return form("(%s%s%+d%s%+d)/1"%(u,v1,int(w),v2,int(c)-1))
        return form(e)+"-1"
    return form(lab)
with open(out+"/class_table.tex","w") as f:
    f.write("\\begin{tabular}{@{}rrrll@{}}\\toprule k mod 12 & steps & forward & sign pattern & source\\\\\\midrule\n")
    for r in sorted(paths,key=int):
        p=paths[r]; sg="".join(s for s,_ in p["steps"])
        src="$(x,y)$ vocabulary" if p["source"].startswith("fibparam") else "$(a,b)$ vocabulary"
        f.write("%s & %d & %d & \\texttt{%s} & %s\\\\\n"%(r,len(p["steps"]),p["nf"],sg,src))
    for r in opn: f.write("%d & \\multicolumn{4}{l}{open: no route found within the search cap (Section~\\ref{sec:open})}\\\\\n"%r)
    f.write("\\bottomrule\\end{tabular}\n")
with open(out+"/labels_appendix.tex","w") as f:
    for r in sorted(paths,key=int):
        p=paths[r]
        f.write("\\begin{minipage}{\\linewidth}\\noindent\\textbf{Class $k\\equiv %s \\pmod{12}$.}\\\\[1pt]\n"%r)
        f.write("\\begin{tabular}{@{\\hspace{1.5em}}rcl@{}}\n")
        for i,(sg,lab) in enumerate(p["steps"]):
            side="$S$ = state before the move" if i<p["nf"] else "$S$ = state after the move"
            f.write("%d & $%s$ & $N=%s$\\\\\n"%(i+1,sg,label(lab)))
        f.write("\\end{tabular}\\end{minipage}\\par\\medskip\n")
# figure 1: path length by class
fig,ax=plt.subplots(figsize=(6.6,3.0))
rs=list(range(12)); ln=[len(paths[str(r)]["steps"]) if str(r) in paths else 0 for r in rs]
cols=[blue if str(r) in paths else "white" for r in rs]
ax.bar(rs,ln,color=cols,edgecolor=blue,hatch=None)
for r in rs:
    if str(r) not in paths: ax.text(r,0.4,"open",ha="center",fontsize=8,color=red)
    else: ax.text(r,ln[r]+0.15,str(ln[r]),ha="center",fontsize=8)
ax.set_xticks(rs); ax.set_xlabel("k mod 12"); ax.set_ylabel("certified route length")
ax.set_ylim(0,12); [ax.spines[s].set_visible(False) for s in ("top","right")]
ax.set_title("Symbolically certified route length per residue class of $k$",fontsize=9.5)
fig.savefig(out+"/figures/fig1_classes.pdf",bbox_inches="tight"); fig.savefig(out+"/figures/fig1_classes.png",dpi=150,bbox_inches="tight"); plt.close(fig)
# figure 2: log10 of state along the route
fig,ax=plt.subplots(figsize=(6.6,3.3))
cm=plt.get_cmap("tab20")
for r in sorted(paths,key=int):
    p=paths[r]; k=[k for k in range(560,640) if k%12==int(r)][0]
    good,Ns=fibresolve.replay([tuple(s) for s in p["steps"]],p["nf"],k); assert good
    S=F[k]; ys=[math.log10(S)-math.log10(F[k])]
    for (sg,_),N in zip(p["steps"],Ns):
        S=S//N*(N+1)**2 if sg=="+" else S*N//(N+1)**2; ys.append(math.log10(S)-math.log10(F[k]))
    ax.plot(range(len(ys)),ys,marker="o",ms=3,lw=1.2,color=cm(int(r)),label=str(r))
ax.axhline(0,color=grey,lw=.6)
ax.set_xlabel("step"); ax.set_ylabel("$\\log_{10}(S/F_k)$"); ax.legend(title="k mod 12",ncol=6,fontsize=7,title_fontsize=7,frameon=False,loc="upper left")
[ax.spines[s].set_visible(False) for s in ("top","right")]
ax.set_title("Size of the intermediate state along each route ($k\\approx 600$)",fontsize=9.5)
fig.savefig(out+"/figures/fig2_trajectory.pdf",bbox_inches="tight"); fig.savefig(out+"/figures/fig2_trajectory.png",dpi=150,bbox_inches="tight"); plt.close(fig)
# small distance table
with open(out+"/small_table.tex","w") as f:
    h={}
    for k,v in small.items(): h[v["d"]]=h.get(v["d"],0)+1
    f.write("\\begin{tabular}{@{}lrrrrr@{}}\\toprule $d$ & 2 & 3 & 4 & 5 & 6\\\\\\midrule number of $k\\in[2,29]$ & "+" & ".join(str(h.get(d,0)) for d in range(2,7))+"\\\\\\bottomrule\\end{tabular}\n")
print("built")
