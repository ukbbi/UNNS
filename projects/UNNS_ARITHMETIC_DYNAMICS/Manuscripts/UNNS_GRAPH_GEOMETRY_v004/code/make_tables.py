import json, csv, sympy as sp
from paths import *
t = sp.symbols('t'); a, b = sp.symbols('a b')
def L(e): return sp.latex(sp.factor(e)) if e != 0 else '0'
def Lx(e): return sp.latex(e)
P = lambda s: sp.sympify(s, locals={'t': t})
U1 = json.load(open(f'{INH}/u1_identities.json'))
# --- summary of successor identities
rows = []
for d in U1:
    lab = ',\\ '.join(('+' if s['direction'] == 'forward' else '-') + '(' + L(P(s['N'])) + ')' if not P(s['N']).is_number else ('+' if s['direction'] == 'forward' else '-') + str(P(s['N'])) for s in d['steps'])
    rows.append(f"{d['name']} & ${sp.latex(P(d['n']))}$ & $t\\ge {d['t_min']}$ & {len(d['steps'])} & ${lab}$ \\\\")
open(f'{TAB}/succ_summary.tex', 'w').write('\\begin{tabular}{@{}cllcl@{}}\\toprule\nclass & $n$ & range & moves & labels $N_1,\\dots,N_\\ell$ (sign $+$ forward, $-$ inverse)\\\\\\midrule\n' + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\n')
# --- full certificates (states and cofactors)
out = []
for d in U1:
    out.append(f"\\paragraph{{Class {d['name']}: $n={sp.latex(P(d['n']))}$, $t\\ge {d['t_min']}$.}}\n\\begin{{center}}\\small\\begin{{tabular}}{{@{{}}clllc@{{}}}}\\toprule\nstep & state before & move & cofactor $c$ & state after\\\\\\midrule")
    for s in d['steps']:
        sg = '+' if s['direction'] == 'forward' else '-'
        out.append(f"{s['step']} & ${L(P(s['state_before']))}$ & ${sg}\\,{L(P(s['N']))}$ & ${L(P(s['cofactor']))}$ & ${L(P(s['state_after']))}$ \\\\")
    out.append('\\bottomrule\\end{tabular}\\end{center}')
open(f'{TAB}/succ_certificates.tex', 'w').write('\n'.join(out) + '\n')
# --- squares: 24 identities
SQ = json.load(open(f'{INH}/u2sq_square_identities.json'))
rows = []
for r in range(24):
    c = SQ['classes'][str(r)]
    lab = ',\\ '.join((sg + (L(P(e)) if not P(e).is_number else str(P(e)))) if False else (sg + '(' + L(P(e)) + ')' if not P(e).is_number else sg + str(P(e))) for sg, e in c['steps'])
    rows.append(f"{r} & {c['t0']} & {len(c['steps'])} & ${lab}$ \\\\")
open(f'{TAB}/sq_identities.tex', 'w').write('{\\footnotesize\\begin{longtable}{@{}rcrp{0.7\\textwidth}@{}}\\toprule\n$r$ & $t\\ge$ & moves & labels $N_i(t)$ for $n=24t+r$\\\\\\midrule\\endhead\n' + '\n'.join(rows) + '\n\\bottomrule\\end{longtable}}\n')
# --- squares: full states (symbolic) for the 24 classes
out = []
for r in range(24):
    c = SQ['classes'][str(r)]; s = sp.expand((24 * t + r) ** 2); chain = [s]; cofs = []
    for sg, e in c['steps']:
        N = P(e); den = N if sg == '+' else (N + 1) ** 2
        cof = sp.cancel(s / den); s = sp.expand(cof * ((N + 1) ** 2 if sg == '+' else N)); chain.append(s); cofs.append(cof)
    assert sp.expand(s - (24 * t + r + 1) ** 2) == 0
    out.append(f"\\item[$r={r}$] $" + ' \\to '.join(L(x) if i in (0, len(chain) - 1) else L(x) for i, x in enumerate(chain)) + '$')
open(f'{TAB}/sq_states.tex', 'w').write('{\\footnotesize\\begin{description}[leftmargin=2.2em,itemsep=2pt]\n' + '\n'.join(out) + '\n\\end{description}}\n')
# --- Fibonacci classes
CC = json.load(open(f'{INH}/u2fpsym_class_certificates.json'))
rows = []
for r in range(12):
    c = CC[str(r)]
    labs = []
    for sg, pair in zip([l[0] for l in c['labels']], c['labels_ring']):
        e = sp.sympify(pair[0], locals={'b': b}) + sp.sympify(pair[1], locals={'b': b}) * a
        labs.append(sg + '(' + sp.latex(sp.factor(e)) + ')' if not e.is_number else sg + str(e))
    rows.append(f"{r} & {'$+1$' if c['eps']==1 else '$-1$'} & {len(labs)} & " + ',\\ '.join('$' + l + '$' for l in labs) + " \\\\")
open(f'{TAB}/fib_classes.tex', 'w').write('{\\scriptsize\\begin{longtable}{@{}rcrp{0.74\\textwidth}@{}}\\toprule\n$k \\bmod 12$ & $\\varepsilon$ & moves & labels $N_i$ as elements $p_0(b)+p_1(b)a$, $b=F_h$, $a=F_{h-1}$, $h=\\lfloor k/2\\rfloor$\\\\\\midrule\\endhead\n' + '\n'.join(rows) + '\n\\bottomrule\\end{longtable}}\n')
# --- Fibonacci classes, one move per line (long form)
out = []
for r in range(12):
    c = CC[str(r)]
    out.append(f"\\needspace{{14\\baselineskip}}\\subsection*{{Class $k\\equiv {r}\\pmod{{12}}$ \\quad ($\\varepsilon={'+1' if c['eps']==1 else '-1'}$, {len(c['labels'])} moves)}}\n\\begin{{center}}\\renewcommand{{\\arraystretch}}{{1.35}}\\begin{{tabular}}{{@{{}}r@{{\\quad}}l@{{}}}}\\toprule\ni & move $\\pm N_i$ \\\\\\midrule")
    for i, (sg, pair) in enumerate(zip([l[0] for l in c['labels']], c['labels_ring']), 1):
        e = sp.sympify(pair[0], locals={'b': b}) + sp.sympify(pair[1], locals={'b': b}) * a
        lab = sg + '(' + sp.latex(sp.factor(e)) + ')' if not e.is_number else sg + str(e)
        out.append(f"{i} & ${lab}$ \\\\")
    out.append("\\bottomrule\\end{tabular}\\end{center}\n")
open(f'{TAB}/fib_classes_long.tex', 'w').write('\n'.join(out))
# --- small Fibonacci table
SM = json.load(open(f'{INH}/u2fpsym_small_fib_paths.json'))
rows = []
for k in range(2, 30):
    p = SM[str(k)]
    rows.append(f"{k} & {p['d']} & ${' \\to '.join(str(x) for x in p['path'])}$ \\\\")
open(f'{TAB}/fib_small.tex', 'w').write('{\\footnotesize\\begin{longtable}{@{}rcp{0.78\\textwidth}@{}}\\toprule\n$k$ & $d(F_k,F_{k+1})$ & a shortest path\\\\\\midrule\\endhead\n' + '\n'.join(rows) + '\n\\bottomrule\\end{longtable}}\n')
print('tables ok')
