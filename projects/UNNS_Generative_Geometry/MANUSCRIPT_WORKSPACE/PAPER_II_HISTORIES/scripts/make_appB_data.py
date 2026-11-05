"""Generates tex/appB_data.tex (exact tables for Appendix B) from the independent engine."""
import sys, os
from fractions import Fraction
from engine import *
from swaps import *
from topo import perm_complex
def w2s(w): return "$("+",".join(map(str,w))+")$"
out=[]
def sec(t): out.append("\\subsection*{%s}\n"%t)
# B.1 the histories of 72
sec("B.1 The four complete histories of 72")
rows=[]
for (src,w) in sorted(histories(72)):
    st=run(src,w)
    rows.append("%d & %s & $%s$ & $%s$\\\\\n"%(src,w2s(w),"\\to ".join(map(str,st)),str(sorted(w))[1:-1]))
out.append("\\begin{center}\\small\\begin{tabular}{@{}rlll@{}}\\toprule source & word & states & content\\\\\\midrule\n"+"".join(rows)+"\\bottomrule\\end{tabular}\\end{center}\n")
# B.2 thresholds of {2,3,14}
sec("B.2 Thresholds of the arrangements of $\\{2,3,14\\}$")
rows=[]
for w in sorted(arrangements((2,3,14))):
    rows.append("%s & %d\\\\\n"%(w2s(w),K(w)))
out.append("\\begin{center}\\small\\begin{tabular}{@{}lr@{}}\\toprule arrangement $w$ & $K(w)$\\\\\\midrule\n"+"".join(rows)+"\\bottomrule\\end{tabular}\\end{center}\n")
# B.3 the loop and the void
def block(C,m,name):
    A=sorted(adm_set(C,m)); f,b=perm_complex(C,m)
    cl=swap_classes(C,m)
    out.append("\\paragraph{%s}Admissible arrangements: %d of %d. Swap classes: %d. Betti vector of $K_m$ over $\\mathbb F_2$: $(%s)$; $f$-vector $(%s)$.\n"%(name,len(A),len(arrangements(C)),len(cl),",".join(map(str,b)),",".join(map(str,f))))
sec("B.3 Complexes of Section 7 and Section 8")
block((2,3,8,9),72,"$\\{2,3,8,9\\}$ at $72$ (loop)")
block((2,3,8,9,14),1008,"$\\{2,3,8,9,14\\}$ at $1008$ (void)")
for C,m in [((2,3,4,5,6),4),((2,3,4,5,6,7),4),((2,3,4,5,8),32),((2,3,4,5,6,7),24)]:
    block(C,m,"$\\{%s\\}$ at $%d$ (\\cref{prop:irred})"%(",".join(map(str,C)),m))
    cl=swap_classes(C,m); out.append("Component sizes: %s.\n"%(", ".join(str(len(c)) for c in cl)))
# B.4 hexagon failure
sec("B.4 The overlap hexagon")
C=(1,2,4); 
out.append("The content $\\{1,2,4\\}$ from source $2$: admissible arrangements %s of %d; $P(C)=8\\nmid 2$.\n"%(", ".join(w2s(w) for w in sorted(adm_set(C,2))),len(arrangements(C))))
open(os.path.join(os.path.dirname(__file__),"..","tex","appB_data.tex"),"w").write("".join(out))
print("ok")
