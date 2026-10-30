"""Generates tex/gen_tables.tex: exact data tables for the appendices (integer arithmetic; areas of unions via shapely, compared with exact formulas)."""
import itertools, sys
from math import gcd
from fractions import Fraction as Fr
from geo import *
out=[]
def P(x): out.append(x)
def area2(poly):  # twice the area, exact
    return abs(sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly))))
def hull_vertices(F):
    pts=sorted(F)
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[]
    for p in pts:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    up=[]
    for p in reversed(pts):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
def fr(x):
    x=Fr(x); return str(x.numerator) if x.denominator==1 else r"\tfrac{%d}{%d}"%(x.numerator,x.denominator)
def pt(p): return "(%d,%d)"%p
units=lambda d:[s for s in range(1,d) if gcd(s,d)==1]

# ---- B: parameter table
rows=[]
def order(p,b):
    k=1;v=p%b
    while v!=1: v=v*p%b;k+=1
    return k
def gcdl(a,b): return gcd(a,b)
import math
for b in (11,13,19,29,31):
    for (p1,p2) in ((2,3),(3,5),(2,5),(5,7),(3,7)):
        if p1%b==0 or p2%b==0: continue
        o1,o2=order(p1,b),order(p2,b)
        # D0 = <r1> cap <r2>, subgroup of cyclic group of order b-1: |D0| = gcd(o1,o2) in a cyclic group
        d=math.gcd(o1,o2)
        if d<2: continue
        l1,l2=o1//d,o2//d
        g1=pow(p1,l1,b); g2=pow(p2,l2,b)
        sig=[k for k in range(1,d) if pow(g2,k,b)==g1 and gcd(k,d)==1]
        assert len(sig)==1; s=(-sig[0])%d
        # check: Lambda = {(l1 i,l2 j): j = s i mod d}
        for i in range(0,2*d):
            for j in range(0,2*d):
                assert (pow(p1,l1*i,b)*pow(p2,l2*j,b)%b==1)==((j-s*i)%d==0)
        rows.append((b,p1,p2,o1,o2,d,l1,l2,s))
P(r"\begin{longtable}{@{}rrr rr r rr r@{}}")
P(r"\toprule $b$ & $p_1$ & $p_2$ & $o_1$ & $o_2$ & $d$ & $\lambda_1$ & $\lambda_2$ & $s$\\\midrule\endhead")
for r in rows: P(" & ".join(str(x) for x in r)+r"\\")
P(r"\bottomrule\caption{Normalization data $(d,s,\lambda_1,\lambda_2)$ of Proposition~\ref{prop:norm} for some primes $p_1,p_2$ and denominators $b$ (computed; the congruence $p_1^{\lambda_1i}p_2^{\lambda_2j}\equiv1\iff j\equiv si\pmod d$ was verified for $0\le i,j<2d$ in each row; rows with $d=1$ omitted).}\label{tab:param}\end{longtable}")
open('../tex/gen_param.tex','w').write("\n".join(out)); out.clear()

# ---- C: Graver sets
P(r"\begin{longtable}{@{}rrp{9.2cm}@{}}")
P(r"\toprule $d$ & $s$ & Graver vectors of $\Gamma_{d,s}$ up to sign (computed by exhaustive conformal minimality in $[-d,d]^2$)\\\midrule\endhead")
for d in range(3,10):
    for s in units(d):
        G=graver(d,s,d,d)
        reps=sorted({max(g,(-g[0],-g[1])) for g in G})
        t=pow(s,-1,d)
        std={(d,0),(0,d),(1,s),(1,s-d),(t,1),(d-t,-1)}
        stdn={max(g,(-g[0],-g[1])) for g in std}
        kind="the six standard vectors only" if set(reps)==stdn else "extra vectors"
        P(f"{d} & {s} & "+", ".join("$"+pt(g)+"$" for g in reps)+f" ({kind}; {len(reps)} vectors)\\\\")
P(r"\bottomrule\caption{Graver vectors of $\Gamma_{d,s}$ for $3\le d\le9$. For nonspecial $(d,s)$ the set is exactly the six standard vectors of Lemma~\ref{lem:std-graver}; for $s=\pm1$ it is the larger list of Lemma~\ref{lem:special-graver}.}\label{tab:graver}\end{longtable}")
open('../tex/gen_graver.tex','w').write("\n".join(out)); out.clear()

# ---- D: exceptional data
P(r"\begin{longtable}{@{}rrr p{4.6cm} rrrc@{}}")
P(r"\toprule $d$ & $s$ & $t$ & lower-left chain $A\to B$ (steps) & $2|H_0|$ & $|Z|$ & $|U_0|$ & $=|H_0|-d$?\\\midrule\endhead")
cnt=0
for d in range(5,12):
    for s in units(d):
        if s in (1,d-1): continue
        t=pow(s,-1,d)
        Q=(d,d); F=Fpts(d,s,Q)
        pts=ccw_boundary_points(d,s,Q,F)
        iA=pts.index((0,d)); chain=pts[iA:]+[(d,0)]
        steps=[(chain[i+1][0]-chain[i][0],chain[i+1][1]-chain[i][1]) for i in range(len(chain)-1)]
        H2=area2(hull_vertices(F))
        # zonogon: Minkowski sum of segments with the distinct step vectors (parallel steps merged); area = sum_{i<j}|cr|
        # group parallel steps
        vs=[]
        for v in steps:
            for k,w in enumerate(vs):
                if v[0]*w[1]-v[1]*w[0]==0: vs[k]=(w[0]+v[0],w[1]+v[1]); break
            else: vs.append(v)
        Z=sum(abs(a[0]*b[1]-a[1]*b[0]) for a,b in itertools.combinations(vs,2))
        Fx,G,pars,segs=cells_all(d,s,Q)
        U=unary_union([Polygon(p) for p in pars])
        U2=U.union(unary_union([__import__('shapely.geometry',fromlist=['LineString']).LineString(sg) for sg in segs]))
        ok = abs(U2.area-(Fr(H2,2)-d))<1e-9
        cnt+=1
        P(f"{d} & {s} & {t} & "+", ".join("$"+pt(v)+"$" for v in steps)+f" & {H2} & {Z} & ${fr(Fr(H2,2)-d)}$ & {'yes' if ok else 'NO'}\\\\")
        assert ok
P(r"\bottomrule\caption{The exceptional box $Q=(d,d)$ for $5\le d\le11$, nonspecial $s$. $2|H_0|$ and $2|Z|$ are twice the areas of the hull and of the zonogon of Lemma~\ref{lem:zonogon} (integers); $|U_0|$ is $|H_0|-d$, and the last column records the floating-point comparison with the area of the union of all admissible parallelograms (tolerance $10^{-9}$).}\label{tab:exc}\end{longtable}")
open('../tex/gen_exc.tex','w').write("\n".join(out)); out.clear()
print("exc rows",cnt)

# ---- E: special classes
P(r"\begin{longtable}{@{}rrrrr@{}}")
P(r"\toprule $d$ & $s$ & $|H_0|$ & $|U_0|$ (computed) & $\beta_1$ (Thm~\ref{thm:betti})\\\midrule\endhead")
from shapely.geometry import LineString
for d in range(2,9):
    for s in units(d):
        if s not in (1,d-1): continue
        Q=(d,d); F=Fpts(d,s,Q); H2=area2(hull_vertices(F))
        Fx,G,pars,segs=cells_all(d,s,Q)
        U=unary_union([Polygon(p) for p in pars]+[LineString(sg) for sg in segs])
        beta = d if s==d-1 else 2
        P(f"{d} & {s} & ${fr(Fr(H2,2))}$ & {U.area:.6g} & {beta}\\\\")
P(r"\bottomrule\caption{Special classes in the exceptional box. For $s=1$, $d\ge3$: $|U_0|=|W|=d(d-2)$ and $|H_0|=d^2-d$. For $s=d-1$ the union is a graph and has area $0$. (For $d=2$, $s=1=d-1$.)}\label{tab:special}\end{longtable}")
open('../tex/gen_special.tex','w').write("\n".join(out)); out.clear()

# ---- F: column data
d,s,Q=5,2,(8,13)
P(r"\begin{tabular}{@{}r rrrr c@{}}")
P(r"\toprule $i$ & $b_i$ & $K_i$ & $B_i$ & $T_i$ & $T_{i+1}-T_i$ if $K_{i+1}\ne K_i$\\\midrule")
b=[d]+[(s*i)%d for i in range(1,Q[0]+1)]
K=[(Q[1]-bi)//d for bi in b]
for i in range(Q[0]+1):
    Bi=(i,b[i]); Ti=(i,b[i]+K[i]*d)
    last="" 
    if i<Q[0] and K[i+1]!=K[i]:
        Tn=(i+1,b[i+1]+K[i+1]*d); last="$"+pt((Tn[0]-Ti[0],Tn[1]-Ti[1]))+"$"
    P(f"{i} & {b[i]} & {K[i]} & ${pt(Bi)}$ & ${pt(Ti)}$ & {last}\\\\")
P(r"\bottomrule\end{tabular}")
open('../tex/gen_columns.tex','w').write("\n".join(out)); out.clear()

# ---- G: boundary chains and D9 statistics
P(r"\begin{tabular}{@{}lp{9.5cm}@{}}")
P(r"\toprule $(d,s,Q)$ & $\Omega$ with classes\\\midrule")
for (d,s,Q) in [(5,2,(6,5)),(5,2,(8,8)),(7,3,(11,12)),(7,2,(9,13)),(8,3,(12,10))]:
    Om=omega(d,s,Q)
    word="".join(cls(p,d) for p in Om)
    import re
    assert re.fullmatch(r"R*C*T*",word),word
    P(f"$({d},{s},({Q[0]},{Q[1]}))$ & "+", ".join("$"+pt(p)+"^{"+cls(p,d)+"}$" for p in Om)+f"\\\\")
P(r"\bottomrule\end{tabular}")
open('../tex/gen_omega.tex','w').write("\n".join(out)); out.clear()
# statistics
tot=interior=0; wordok=0
for d in range(5,9):
    for s in units(d):
        if s in (1,d-1): continue
        for u in range(d):
            for v in range(d):
                if (u,v)==(0,0): continue
                Q=(d+u,d+v); tot+=1
                F=Fpts(d,s,Q); H=hull_poly(F)
                if H.exterior.distance(Point(d,d))>1e-9: interior+=1
                Om=omega(d,s,Q); w="".join(cls(p,d) for p in Om)
                import re
                wordok+= bool(re.fullmatch(r"R*C*T*",w))
open('../tex/gen_stats.tex','w').write(r"\newcommand{\statTotal}{%d}\newcommand{\statInterior}{%d}\newcommand{\statWord}{%d}"%(tot,interior,wordok))
print("stats",tot,interior,wordok)

# ---- H: cell family and records
d,s,Q=7,3,(11,12)
fam=cap_family(d,s,Q)
P(r"\begin{tabular}{@{}llp{8.2cm}@{}}")
P(r"\toprule family & number & corner 4-tuples $(w,w+g,w+g+h,w+h)$\\\midrule")
for k,nm in (('L','L-cells'),('D','D-cells'),('bottom','bottom cell'),('left','left cell')):
    P(f"{nm} & {len(fam[k])} & "+"; ".join("$"+",".join(pt(p) for p in c)+"$" for c in fam[k])+r"\\")
fc=fill_cells(d,s,Q)
P(f"hole-filling & {len(fc)} & "+"; ".join("$"+",".join(pt(p) for p in c)+"$" for c in fc)+r"\\")
P(r"\bottomrule\end{tabular}")
open('../tex/gen_family.tex','w').write("\n".join(out)); out.clear()
d,s=13,5; t=pow(s,-1,d); a=d-s; c=d-t
P(r"\begin{tabular}{@{}rrrcc@{}}")
P(r"\toprule $u$ & record $M=(x,y)$ & $g$ & $\cross(g,M)$ & $xy$\\\midrule")
for u in range(1,d):
    r=[(s*i)%d for i in range(1,u+1)]
    y=min(r); x=r.index(y)+1; M=(x,y)
    g=(1,-a) if (1*y-(-a)*x)>=x*y else (c,-1)
    cr=g[0]*M[1]-g[1]*M[0]
    assert cr>=x*y
    P(f"{u} & ${pt(M)}$ & ${pt(g)}$ & {cr} & {x*y}\\\\")
P(r"\bottomrule\end{tabular}")
open('../tex/gen_records.tex','w').write("\n".join(out)); out.clear()
print("ok")
