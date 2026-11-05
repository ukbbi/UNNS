"""Generates appendices B-F and tables for Paper III from results/*.json and the stdlib engine eng3.py."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eng3 import *
from eng3 import _bd
from fractions import Fraction as Fr
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
T = os.path.join(R, 'tex')
os.makedirs(T + '/tables', exist_ok=True)
J = lambda n: json.load(open(os.path.join(R, 'results', n)))
def tex(fr):
    fr = Fr(fr); return str(fr.numerator) if fr.denominator == 1 else '%d/%d' % (fr.numerator, fr.denominator)
def dl(D): return '\\{' + ','.join(map(str, D)) + '\\}'
def bl(b): return '(' + ','.join(map(str, b)) + ')'
def W(path, s): open(os.path.join(T, path), 'w').write(s)
c1 = J('c1_traj.json')
# ---------------- tables/t8_table.tex
t8 = c1['t8']; rows = []
for n, (xs, D, b, mv) in enumerate(zip(t8['orbit'], t8['D'], t8['betti'], t8['moves'])):
    x = Fr(xs)
    rows.append('%d & $%s$ & %d & $%s$ & %d & $%s$\\\\\n' % (n, tex(x), x.denominator, dl(D), len(mv), bl(b)))
W('tables/t8_table.tex', '\\begin{table}[tbp]\\centering\\small\n\\begin{tabular}{@{}rrrlrl@{}}\\toprule\n$n$ & $x_n$ & $b_n$ & $D(x_n)$ & move edges & $(\\beta_0,\\beta_1)$\\\\\\midrule\n' + ''.join(rows) +
  '\\bottomrule\\end{tabular}\n\\caption{\\textbf{The eight-step orbit $x_0=3025/3$} (exact, \\cref{thm:A4T3c}). Events occur at $n=6$ (new occurrence $10$) and $n=8$ (new occurrence $22$); the move complex of $D$ gains the edge $\\{10,55\\}$ at $n=6$ and the triangle with edges $\\{10,22\\},\\{10,55\\},\\{22,55\\}$ at $n=8$, so $\\beta_1$ rises $0\\to1$ at the last step only. The state $x_8=12100/3=(55\\cdot2)^2/3$ is the activated target with $q=2$.}\\label{tab:t8}\n\\end{table}\n')
# ---------------- appendix B
W('appendices/appB_definitions.tex', r"""\section{Collective-state definitions}\label{app:definitions}
\paragraph{State and map.} A \emph{state} is a reduced rational $x=a/b>0$ with $b\ge1$. Its occurrence set is $D(x)=\{d\ge2: d^2\mid a,\ d\equiv1 \pmod b\}$. If $D(x)\ne\emptyset$ put $L=\operatorname{lcm}D(x)$, $G=\gcd\{d-1:d\in D(x)\}$ and $C(x)=x+L^2/G$. Then $b\mid G$, and $C(x)=(ah+L^2)/G$ with $G=bh$.
\paragraph{Move complex.} For a finite set $D\subset\{2,3,\dots\}$ with $1\notin D$, the exponent vectors $v(d)\in\mathbb Z^P$ over the primes $P$ dividing some $d\in D$ give $D$ the structure of a point set. Two occurrences $u<v$ span an edge iff the open interval $[u,v]^\circ$ in the divisibility order contains no other point of $D\cup\{1\}$ (the divisor-interval rule, \cref{thm:A5T31}). The cells of $K(D)$ are the faces of the cubes spanned by edge directions all of whose vertices lie in $D$ and whose pairs of vertices differing by a generator are edges; $\beta_i$ denotes the Betti numbers over $\mathbb F_2$ (checked against $\mathbb F_{2^{31}-1}$ in the finite-exact ranges).
\paragraph{Universal sparse coordinates and Graver sets.} For $x=a/b$ the active primes are those $p$ with $p^2\mid a$; the box is $[-t_p,t_p]$ with $t_p=\lfloor v_p(a)/2\rfloor$. The lattice $\Lambda_b=\{g:\prod p^{g_p}\equiv1\pmod b\}$ and its Graver basis $\mathrm{Gr}(x)$ (conformally minimal elements of $\Lambda_b\cap\mathrm{box}$) are as in \cref{def:universal}. Positive elements are occurrences, edge elements are differences of occurrences along an edge, and the remaining elements are dormant.
\paragraph{Status and treatment vocabulary.} \textsc{Proved}: a complete proof is given. \textsc{Mixed}: a proved part and a part checked on finite data, separated in the statement. \textsc{Finite-exact}: an exact computation on an explicit finite range; no extrapolation. \textsc{Counterexample}: an explicit object. \textsc{Open}: a problem. Treatments: \textsc{Full} (principal proof in this paper), \textsc{Finite}, \textsc{Split} (proved part and finite part), \textsc{Open}, \textsc{Example}, \textsc{Corrected} (an earlier statement is corrected here) and \textsc{Cited} (proved in another paper of the programme and used here). Inherited verifier suites are marked \textsc{NOT\_RERUN} in the package \texttt{README.md}.
""")
# ---------------- appendix C
x0 = Fr(c1['t375']['x']); n375 = c1['t375']['n']
o = orbit(x0, n375); assert len(o) == n375 + 1
seg = []
for n, x in enumerate(o):
    D = tuple(Dset(x)); b = x.denominator
    if seg and seg[-1]['D'] == D:
        seg[-1]['to'] = n; seg[-1]['bmin'] = min(seg[-1]['bmin'], b); seg[-1]['bmax'] = max(seg[-1]['bmax'], b)
    else: seg.append({'D': D, 'fr': n, 'to': n, 'bmin': b, 'bmax': b})
rows = []
for s_ in seg:
    s_['b'] = betti(complex_of(list(s_['D'])), 2)[2] if s_['D'] else []
    rows.append('%d--%d & $%s$ & $%s$ & %d--%d\\\\\n' % (s_['fr'], s_['to'], dl(s_['D']), bl(s_['b']), s_['bmin'], s_['bmax']))
json.dump([{'from': s_['fr'], 'to': s_['to'], 'D': list(s_['D']), 'betti': s_['b']} for s_ in seg], open(os.path.join(R, 'results', 'c1_375_segments.json'), 'w'))
C = r"""\section{Complete activation trajectories}\label{app:trajectories}
\subsection{The eight-step orbit}
\Cref{tab:t8} lists the complete orbit of $x_0=3025/3$ of \cref{sec:activation}; every entry is exact. The denominators are $3,54,27,18,27,54,9,9,3$. The orbit enters the activated state $x_8=12100/3=(55\cdot2)^2/3$, the target with $q=2$ (not $17$). The occurrence sets are $\{55\}$ for $n\le5$, $\{10,55\}$ for $n=6,7$ and $\{10,22,55\}$ for $n=8$.
\subsection{The 375-step orbit}
The orbit of $x_0=@X0@$ is run for $@N@$ steps with exact rational arithmetic. \Cref{tab:t375} lists the maximal runs of constant occurrence set with the Betti numbers $(\beta_0,\beta_1,\dots)$ of the move complex and the range of denominators in the run. The events are at steps $372$ (new occurrence $106$), $373$ ($22$) and $375$ ($134$), and $\beta_1$ goes from $0$ to $3$ (\cref{thm:A4T3c375}). This is an exact finite example; no pattern is extrapolated from it.
\begin{table}[tbp]\centering\small
\begin{tabular}{@{}lllr@{}}\toprule
steps & $D$ & $\beta$ & $b_n$ range\\\midrule
@ROWS@\bottomrule\end{tabular}
\caption{\textbf{The $375$-step orbit} (exact, finite). Runs of constant occurrence set $D(x_n)$, with Betti numbers over $\mathbb F_2$ and the range of denominators.}\label{tab:t375}
\end{table}
"""
C = C.replace('@X0@', tex(x0)).replace('@N@', str(n375)).replace('@ROWS@', ''.join(rows))
W('appendices/appC_trajectories.tex', C)
# ---------------- appendix D: relations
inst = c1['inst']
rows = ''.join('%d & %d & $%s$ & %d & %d & $%s$ & %d\\\\\n' % (r['k'], r['ell'], dl(r['ps']), r['q'], r['P'], bl(r['betti2']), r['pred']) for r in inst)
rg = []
for n, xs in enumerate(t8['orbit']):
    x = Fr(xs)
    if not Dset(x): continue
    from grav import region_graver
    ps, box, gr = region_graver(x)
    pos = sum(1 for g in gr if all(c >= 0 for c in g) or all(c <= 0 for c in g))
    rg.append((n, ps, box, len(gr), pos))
rows8 = ''.join('%d & $%s$ & $%s$ & %d & %d\\\\\n' % (n, '\\{' + ','.join(map(str, ps)) + '\\}', '(' + ','.join(map(str, box)) + ')', ng, pos) for n, ps, box, ng, pos in rg)
Dm = r"""\section{Primitive-relation and region-Graver calculations}\label{app:relations}
\subsection{The activation family for \texorpdfstring{$k=2,\dots,5$}{k=2..5}}
For $x=P^2/\ell$ and $y=(Pq)^2/\ell$ with $P=\prod_{i\le k}p_i$, \cref{thm:A4T2} gives $\beta_1(K_{\mathrm{move}}(y))=k(k-1)/2$. The four instances of \cref{ex:A4T1}:
\begin{center}\small\begin{tabular}{@{}rrllrll@{}}\toprule
$k$ & $\ell$ & $p_1,\dots,p_k$ & $q$ & $P$ & $\beta(y)$ & predicted $\beta_1$\\\midrule
@ROWS@\bottomrule\end{tabular}\end{center}
(the column $\beta(y)$ lists $(\beta_0,\beta_1,\dots)$ of $K(D(y))$ computed by the engine; the last column is $k(k-1)/2$).
\subsection{Region Graver sets along the eight-step orbit}
The number of conformally minimal elements of the lattice $\Lambda_b$ in the box, split into those that are signed occurrence vectors (all coordinates of one sign: ``positive'') and the others (edge or dormant elements). For $n=0$ the region has $|\mathrm{Gr}|=4$, for $n=1,\dots,5$ it has $2$, for $n=6,7$ it has $6$ and for $n=8$ it has $12$ (\cref{prop:A4T4b}).
\begin{center}\small\begin{tabular}{@{}rllrr@{}}\toprule
$n$ & active primes & box & $|\mathrm{Gr}|$ & of one sign\\\midrule
@ROWS8@\bottomrule\end{tabular}\end{center}
"""
Dm = Dm.replace('@ROWS@', rows).replace('@ROWS8@', rows8)
W('appendices/appD_relations.tex', Dm)
# ---------------- appendix E: zig-zag example boundaries
D0 = [8, 22, 176]; D1 = [2, 4, 8, 11, 16, 22, 44, 88, 176]
K0 = complex_of(D0); K1 = complex_of(D1)
def lab(c, K):
    d, g = c; vs = [K['vec'][d]]
    for h in g: vs = vs + [tuple(a + b for a, b in zip(v, h)) for v in vs]
    return '\\{' + ','.join(str(x) for x in sorted(K['inv'][v] for v in vs)) + '\\}'
E1 = K1['cells'][1]; F2 = K1['cells'][2]
idx0 = {c: i for i, c in enumerate(K1['cells'][0])}; idx1 = {c: i for i, c in enumerate(E1)}
# check d^2 = 0 over Z
for c in F2:
    acc = {}
    for f, s in _bd(c, K1).items():
        for f2, s2 in _bd(f, K1).items(): acc[f2] = acc.get(f2, 0) + s * s2
    assert all(v == 0 for v in acc.values())
rows1 = ''
for c in E1:
    bd = _bd(c, K1); rows1 += '%s & %s\\\\\n' % (lab(c, K1), ',\\ '.join(('+' if s > 0 else '-') + str(K1['inv'][K1['vec'][f[0]]]) for f, s in sorted(bd.items(), key=lambda kv: K1['inv'][K1['vec'][kv[0][0]]])))
rows2 = ''
for c in F2:
    bd = _bd(c, K1); rows2 += '%s & %s\\\\\n' % (lab(c, K1), ',\\ '.join(('+' if s > 0 else '-') + lab(f, K1) for f, s in sorted(bd.items(), key=lambda kv: lab(kv[0], K1))))
bet0 = betti(K0, 2)[2]; bet1 = betti(K1, 2)[2]
Em = r"""\section{Cellular boundary and homology calculations}\label{app:homology}
\subsection{Chain complex of the zig-zag example}
For the event of \cref{ex:zigzag} ($D=\{8,22,176\}\to D'=\{2,4,8,11,16,22,44,88,176\}$), $K(D)$ has $f=@F0@$ and $\beta=@B0@$, and $K(D')$ has $f=@F1@$ and $\beta=@B1@$. The cells of $K(D')$ with their integral boundaries are listed; the check $\partial_1\partial_2=0$ over $\mathbb Z$ was carried out by the generating script \texttt{gen\_app.py} for each $2$-cell. An edge $\{u,v\}$ with $u<v$ has boundary $+v-u$ in the orientation of the exponent vector (the sign convention of the engine is the one implied by the listing).
\paragraph{Edges.}\begin{center}\small\begin{tabular}{@{}ll@{}}\toprule
edge & $\partial_1$\\\midrule
@E@\bottomrule\end{tabular}\end{center}
\paragraph{Two-cells.}\begin{center}\small\begin{tabular}{@{}ll@{}}\toprule
cell & $\partial_2$\\\midrule
@F@\bottomrule\end{tabular}\end{center}
\subsection{Counts used in the identity}
$(r,h)=((1,0),(0,3))$, $(r',h')=((1,0),(0,2))$, $|\mathrm{Dead}|=(0,3,0)$, $|\mathrm{New}|=(6,11,3)$ and $\Delta\beta=(0,-1)$ (\cref{ex:zigzag}). These are recomputed by the check script \texttt{check\_paper\_III.py}.
"""
Em = Em.replace('@F0@', '(%s)' % ','.join(str(len(c)) for c in K0['cells'])).replace('@B0@', bl(bet0)).replace('@F1@', '(%s)' % ','.join(str(len(c)) for c in K1['cells'])).replace('@B1@', bl(bet1)).replace('@E@', rows1).replace('@F@', rows2)
W('appendices/appE_homology.tex', Em)
# ---------------- appendix F: towers
t5 = J('tower5.json'); t11 = J('tower11.json')
n = min(len(t5), len(t11))
rows = ''.join('%d & %d & $%s$ & %d & $%s$\\\\\n' % (a['k'], a['nV'], bl(a['b']), b['nV'], bl(b['b'])) for a, b in zip(t5, t11))
Fm = r"""\section{Supplemental tower calculations}\label{app:towers}
The Betti numbers of the move complex $K(D(S_k^2/\ell))$ for the two collective towers, $G=5$ ($S_k=126\cdot2^k$, $\ell=5$) and $G=11$ ($S_k=2^2\,3^{3+k}\,5^4$, $\ell=11$), for $0\le k\le @N@$ (finite-exact; $\mathbb F_2$ and $\mathbb F_{2^{31}-1}$ agree on the ranges of \cref{thm:A5T6}). Here $|D|$ is the number of occurrences. The listed values are the data on which the laws of \cref{sec:towertop} are checked and from which no extrapolation is made.
\begin{center}\scriptsize\begin{longtable}{@{}rrlrl@{}}\toprule
 & \multicolumn{2}{c}{$G=5$} & \multicolumn{2}{c}{$G=11$}\\\cmidrule(lr){2-3}\cmidrule(lr){4-5}
$k$ & $|D|$ & $\beta$ & $|D|$ & $\beta$\\\midrule\endhead
@ROWS@\bottomrule\end{longtable}\end{center}
"""
Fm = Fm.replace('@N@', str(n - 1)).replace('@ROWS@', rows)
W('appendices/appF_towers.tex', Fm)
print('generated; tower rows', n, 'segments', len(seg))
