import json, os, sympy as sp, numpy as np
from graphent import *
from paths import *
from mpmath import mpf, log as mlog
lam = sp.symbols('lam')
def bmat(m, eps):
    # even/odd sector matrix, coordinates: D | P1(1..3) | ... | Pm(1..3)
    n = 1 + 3 * m; M = sp.zeros(n, n)
    first = [0] + [1 + 3 * j for j in range(m)]; last = [0] + [3 + 3 * j for j in range(m)]
    for j in range(m):
        M[1 + 3 * j, 2 + 3 * j] = 1; M[2 + 3 * j, 3 + 3 * j] = 1
    for i in range(m + 1):
        for k in range(m + 1):
            if k != i: M[last[i], first[k]] = eps
    return M
def tex(M): return sp.latex(M, mat_delim='(', mat_str='array').replace('\\left(\\begin{array}{' + 'c' * M.shape[1] + '}', '\\left(\\begin{array}{' + 'c' * M.shape[1] + '}')
out = {}
for m in (2,):
    for eps, nm in ((1, 'Bplus'), (-1, 'Bminus')):
        M = bmat(m, eps); cp = sp.expand(M.charpoly(lam).as_expr())
        L = [1] + [3] * m
        pr = sp.prod([lam ** l + eps for l in L]); S = sum(sp.prod([lam ** L[j] + eps for j in range(len(L)) if j != i]) for i in range(len(L)))
        assert sp.expand(cp - (pr - eps * S)) == 0, 'sector charpoly'
        s = tex(M); out[nm] = s
        open(os.path.join(TAB, f'{nm}_m{m}.tex'), 'w').write(s.replace('\\left(', '\\setlength{\\arraycolsep}{2pt}\\left(', 1))
# label transfer matrix
x = sp.symbols('u'); m = 3
T = sp.Matrix(m + 1, m + 1, lambda i, j: 0 if i == j else x ** ([1] + [3] * m)[j]); open(os.path.join(TAB, 'T_m3.tex'), 'w').write(sp.latex(T))
# lambda table
rows = []
for m in (1, 2, 3, 4, 5, 6, 8, 10, 16, 32, 64, 128, 256, 1024):
    L = lam_m(m); rows.append((m, float(L), float(mlog(L)), float(mlog(m) / 3), float(mlog(m) / 4), float(mlog(m))))
with open(os.path.join(TAB, 'lambda_table.tex'), 'w') as f:
    f.write('\\begin{tabular}{rrrrrr}\\toprule $m$ & $\\lambda_m$ & $\\log\\lambda_m$ & $\\tfrac13\\log m$ & $\\tfrac14\\log m$ & $\\log m$\\\\\\midrule\n')
    for r in rows: f.write(f'{r[0]} & {r[1]:.6f} & {r[2]:.6f} & {r[3]:.6f} & {r[4]:.6f} & {r[5]:.6f}\\\\\n')
    f.write('\\bottomrule\\end{tabular}\n')
# trace table
with open(os.path.join(TAB, 'trace_table.tex'), 'w') as f:
    f.write('\\begin{tabular}{rrrrrrrrr}\\toprule $m$ & $n{=}4$ & $6$ & $8$ & $10$ & $12$ & $14$ & $16$ & $18$\\\\\\midrule\n')
    for m in (2, 3, 4, 5, 6):
        f.write(f'{m} & ' + ' & '.join(str(trace_formula(m, n)) for n in (4, 6, 8, 10, 12, 14, 16, 18)) + '\\\\\n')
    f.write('\\bottomrule\\end{tabular}\n')
pc = json.load(open(os.path.join(DATA, 'prime_counts.json')))
with open(os.path.join(TAB, 'prime_table.tex'), 'w') as f:
    f.write('\\begin{tabular}{rrrrrrrrr}\\toprule $m$ & $\\pi_4$ & $\\pi_6$ & $\\pi_8$ & $\\pi_{10}$ & $\\pi_{12}$ & $\\pi_{14}$ & $\\pi_{16}$ & $\\pi_{18}$\\\\\\midrule\n')
    for m in (2, 3, 4, 5, 6):
        f.write(f'{m} & ' + ' & '.join(str(pc[f'{m},{n}']) for n in (4, 6, 8, 10, 12, 14, 16, 18)) + '\\\\\n')
    f.write('\\bottomrule\\end{tabular}\n')
# inherited comparison
ic = json.load(open(os.path.join(DATA, 'inherited_comparison.json')))
with open(os.path.join(TAB, 'inherited_table.tex'), 'w') as f:
    f.write('\\begin{tabular}{rrrrr}\\toprule $m$ & $\\rho$ (inherited, float) & $\\lambda_m$ (exact root) & $\\tfrac14\\log m$-type bound & $\\log\\lambda_m$\\\\\\midrule\n')
    for r in ic: f.write(f'{r[0]} & {r[1]:.10f} & {r[2]:.10f} & {r[3]:.6f} & {r[4]:.6f}\\\\\n')
    f.write('\\bottomrule\\end{tabular}\n')
w = json.load(open(os.path.join(DATA, 'window_entropy.json')))
with open(os.path.join(TAB, 'window_table.tex'), 'w') as f:
    f.write('\\begin{tabular}{rrrr}\\toprule $X$ & edges of $G[1,X]$ & $\\rho(B)$ & $h_{\\rm NB}$\\\\\\midrule\n')
    for r in w: f.write(f'{r[0]} & {r[1]} & {r[2]:.4f} & {r[3]:.4f}\\\\\n')
    f.write('\\bottomrule\\end{tabular}\n')
print('tables ok', os.listdir(TAB)); print(ic[:2])

wb=json.load(open(os.path.join(DATA,'window_bound.json')))
with open(os.path.join(TAB,'window_bound_table.tex'),'w') as f:
    f.write('\\begin{tabular}{rrrrr}\\toprule $X$ & best $x$ & $\\tau(x)-1$ & proved bound $\\log\\lambda_{\\tau(x)-1}$ & computed $\\hNB(G[1,X])$\\\\\\midrule\n')
    for X,xb,b,lb,hh in wb:
        if xb is None: f.write(f'{X} & -- & -- & -- & {hh if hh else 0:.4f}\\\\\n')
        else: f.write(f'{X} & {xb} & {b} & {lb:.4f} & {hh:.4f}\\\\\n')
    f.write('\\bottomrule\\end{tabular}\n')
wc=json.load(open(os.path.join(DATA,'walk_counts.json')))
with open(os.path.join(TAB,'walk_counts.tex'),'w') as f:
    f.write('\\begin{tabular}{rrrrrrrrrrr}\\toprule $m$ & $a_1$ & $a_2$ & $a_3$ & $a_4$ & $a_5$ & $a_6$ & $a_7$ & $a_8$ & $a_9$ & $a_{10}$\\\\\\midrule\n')
    for m in ('2','3','4'): f.write(m+' & '+' & '.join(str(t) for t in wc[m])+'\\\\\n')
    f.write('\\bottomrule\\end{tabular}\n')
# F_2 successor table
de,B=nb_matrix(Fm_edges(2))
names={}
with open(os.path.join(TAB,'F2_successors.tex'),'w') as f:
    f.write('\\begin{tabular}{ll}\\toprule directed edge $e$ & successors $e\'$ with $B(e,e\')=1$\\\\\\midrule\n')
    for i,(u,v) in enumerate(de):
        succ=[de[j] for j in range(len(de)) if B[i,j]]
        f.write(f'$({u},{v})$ & '+', '.join(f'$({a},{b})$' for a,b in succ)+'\\\\\n')
    f.write('\\bottomrule\\end{tabular}\n')
print('tables2 ok')
