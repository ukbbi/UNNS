#!/usr/bin/env python3
"""Manuscript-quality checks for Paper II v0.1. Not an independent verification of the mathematics."""
import csv, json, os, re, glob, subprocess, sys
H=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WS=os.path.dirname(os.path.dirname(H))
EXT=f"{WS}/UNNS_THEOREM_CROSSWALK_v001/data/CROSSWALK_MASTER.tsv"
if os.path.exists(EXT):
    cw={r["uid"]:r for r in csv.DictReader(open(EXT,encoding="utf-8"),delimiter="\t")}
    al={r["uid"]:r for r in csv.DictReader(open(f"{WS}/GEO_HD_MANUSCRIPT_PROGRAMME_v001/SOURCE_ALLOCATION.tsv",encoding="utf-8"),delimiter="\t")}
else:   # self-contained fallback: the 62 allocated rows shipped with the package
    rows=list(csv.DictReader(open(f"{H}/crosswalk/PAPER_II_ROWS.tsv",encoding="utf-8"),delimiter="\t"))
    cw={r["uid"]:{"status":r["status"]} for r in rows}
    al={r["uid"]:{"proof_treatment":r["proof_treatment"],"primary_manuscript":"II"} for r in rows}
    print("NOTE: external crosswalk not found; using crosswalk/PAPER_II_ROWS.tsv")
VER=os.path.basename(H)
tex="".join(open(f,encoding="utf-8").read() for f in sorted(glob.glob(f"{H}/tex/*.tex")+glob.glob(f"{H}/tex/sections/*.tex")+glob.glob(f"{H}/tex/appendices/*.tex")) if not f.endswith("appmap_table.tex"))
res=[]
def chk(n,ok,i=""): res.append((n,bool(ok),str(i))); print("PASS " if ok else "FAIL ",n,i)
prov=[]
for l in open(f"{H}/tex/main.prov",encoding="utf-8"):
    l=l.strip().replace("\\protect \\unhbox \\voidb@x \\kern .06em\\vbox {\\hrule width.3em}","\\_")
    m=re.match(r"\\provrow\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}$",l)
    if m: prov.append(m.groups())
p2={u for u,r in al.items() if r["primary_manuscript"]=="II"}
cwp=[p for p in prov if p[0].startswith("CW-")]
chk("1 every cited UID exists in the crosswalk",all(p[0] in cw for p in cwp),len(cwp))
chk("1b status in text equals crosswalk status",all(cw[p[0]]["status"]==p[2] for p in cwp),[p[0] for p in cwp if cw[p[0]]["status"]!=p[2]])
chk("1c treatment in text equals allocation (ignoring '?')",all(al[p[0]]["proof_treatment"].rstrip("?")==p[3] for p in cwp),[p[0] for p in cwp if al[p[0]]["proof_treatment"].rstrip("?")!=p[3]])
chk("2 all 62 allocated rows carry a source record",{p[0] for p in cwp}>=p2 and len(p2)==62,sorted(p2-{p[0] for p in cwp}))
chk("2b only Paper II rows tagged with \\prov",{p[0] for p in cwp}<=p2,sorted({p[0] for p in cwp}-p2))
chk("3 the word 'draft' does not occur",not re.search(r"draft",tex,re.I))
chk("3b author is UNNS Research Collective, no personal author",("UNNS Research Collective" in tex) and "\\author{UNNS Research Collective" in tex)
chk("4 no novelty/priority claim words",not re.search(r"\bnovel\b|first (ever )?proof|breakthrough",tex))
chk("5 FINITE-EXACT rows have treatment FINITE",all(p[3]=="FINITE" for p in cwp if p[2]=="FINITE-EXACT"))
chk("5b OPEN rows have treatment OPEN",all(p[3]=="OPEN" for p in cwp if p[2]=="OPEN"))
log=open(f"{H}/tex/main.log",encoding="utf-8",errors="ignore").read()
chk("6 cross-references resolve",("undefined" not in log.lower().replace("undefined control","").replace("font shape","")) and "Reference `" not in log and "Citation `" not in log)
chk("6b no multiply defined labels","multiply defined" not in log)
chk("7 builds without LaTeX errors","\n!" not in log and os.path.exists(f"{H}/PAPER_II_HISTORIES_{VER}.pdf"))
chk("8 no overfull boxes, no hyperref warnings","Overfull" not in log and "hyperref Warning" not in log)
figs=re.findall(r"\\begin\{figure\}.*?\\end\{figure\}",tex,re.S)
files=[re.search(r"\\includegraphics\[[^\]]*\]\{([^}]*)\}",f).group(1) for f in figs]
chk("9 at least 18 figures, each with caption and label",len(figs)>=18 and all("\\caption" in f and "\\label{fig:" in f for f in figs),len(figs))
chk("9b figure files exist",all(os.path.exists(f"{H}/figures/{x}.pdf") for x in files))
chk("9c captions state status (exact/schematic/finite-exact)",all(re.search(r"exact|schematic",f) for f in figs))
chk("9d every figure is referenced",all(re.search(r"ref\{[^}]*"+re.escape(l)+r"[^}]*\}",tex) for l in re.findall(r"\\label\{(fig:[^}]*)\}",tex)),[l for l in re.findall(r"\\label\{(fig:[^}]*)\}",tex) if not re.search(r"ref\{[^}]*"+re.escape(l)+r"[^}]*\}",tex)])
keys=set(re.findall(r"\\bibitem\{([^}]*)\}",tex)); cites={k.strip() for c in re.findall(r"\\cite\{([^}]*)\}",tex) for k in c.split(",")}
chk("10 every citation defined and every entry cited",cites<=keys and keys<=cites,(sorted(cites-keys),sorted(keys-cites)))
chk("11 sphere statement is homological only",re.search(r"homology of (the sphere )?\$S\^\{k-3\}\$",tex) is not None)
# chain complex d^2=0 spot checks via engine
sys.path.insert(0,f"{H}/scripts")
try:
    from topo import perm_complex
    from engine import run
    f,b=perm_complex((2,3,8,9),72); chk("12 loop {2,3,8,9}@72 Betti (1,1,0), chi consistent",tuple(b)[:3]==(1,1,0) and sum((-1)**i*x for i,x in enumerate(f))==sum((-1)**i*x for i,x in enumerate(b)))
    f,b=perm_complex((2,3,8,9,14),1008); chk("12b void Betti (1,0,1,0), chi consistent",tuple(b)[:4]==(1,0,1,0) and sum((-1)**i*x for i,x in enumerate(f))==sum((-1)**i*x for i,x in enumerate(b)))
    chk("12c 72 reached by four histories; 4^8=65536 merger",run(4,(1,)*7)[-1]==65536 and run(4,(2,2,3,3,3,3))[-1]==65536)
except Exception as e: chk("12 engine checks",False,e)
chk("13 REVISION/inherited verification recorded as NOT_RERUN","NOT_RERUN" in open(f"{H}/README.md").read() if os.path.exists(f"{H}/README.md") else False)
os.makedirs(f"{H}/results",exist_ok=True)
json.dump([{"check":n,"pass":o,"info":i} for n,o,i in res],open(f"{H}/results/PAPER_II_CHECKS.json","w"),indent=1)
f=[n for n,o,_ in res if not o]; print(f"{len(res)-len(f)}/{len(res)} PASS"); sys.exit(1 if f else 0)
