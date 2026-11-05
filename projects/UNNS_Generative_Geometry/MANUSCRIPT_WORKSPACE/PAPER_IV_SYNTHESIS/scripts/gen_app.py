"""Generates tex/tables/*.tex for appendices E and F from exact recomputation (stdlib)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hist, eng3
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(H+'/results/c6_witnesses.json')); C5 = json.load(open(H+'/results/c5_checks.json')); C4 = json.load(open(H+'/results/c4_pair.json'))
C1 = json.load(open(H+'/results/c1_collide.json')); C7 = json.load(open(H+'/results/c7_dim2.json'))
def w(s): return '$('+','.join(map(str, s))+')$'
out = []
# histories to 900 and 9000 from source 4
out.append('\\begin{tabular}{@{}lp{4.6cm}p{6.4cm}@{}}\\toprule target & histories from source $4$ & swap classes\\\\\\midrule')
for t in (900, 9000, 288, 4320):
    Hs = hist.histories(4, t); Hh, cl = hist.classes(4, t)
    cls = '; '.join('\\{'+', '.join(w(x) for x in sorted(c))+'\\}' for c in cl)
    out.append(f'{t} & {", ".join(w(x) for x in Hs)} & {len(cl)}: {cls}\\\\')
out.append('\\bottomrule\\end{tabular}')
open(H+'/tex/tables/hist_witness.tex', 'w').write('\n'.join(out)+'\n')
# tower table
rows = ['\\begin{tabular}{@{}rll@{}}\\toprule $k$ & $\\beta(K(D(x_k)))$, $S_0=126$ & $S_0=3094$\\\\\\midrule']
for k in range(15):
    b1 = C4['126']['seq'][k]['b']; b2 = C4['3094']['seq'][k]['b']
    def tr(b):
        b = list(b)
        while len(b) > 1 and b[-1] == 0: b = b[:-1]
        return '('+','.join(map(str, b))+')'
    rows.append(f'{k} & {tr(b1)} & {tr(b2)}\\\\')
rows.append('\\bottomrule\\end{tabular}')
open(H+'/tex/tables/tower_table.tex', 'w').write('\n'.join(rows)+'\n')
# local inventory table
A = R['W5']
def fv(t): return '('+','.join(map(str, t))+')'
rows = ['\\scriptsize\\setlength{\\tabcolsep}{3pt}\\begin{tabular}{@{}llllll@{}}\\toprule event & $f\\to f\'$ & new cells & $\\beta\\to\\beta\'$ & $\\Delta\\beta$ & cl\\\\\\midrule']
ev = [('$D=\\{385,27720\\},N=\\{11,72\\}$', A['pairA'][0], '1\\to1'), ('$D=\\{15,315\\},N=\\{4,21\\}$', A['pairA'][1], '1\\to2'), ('$D=\\{12,35\\},N=\\{44,45\\}$', A['pairB'][0], '2\\to1'), ('$D=\\{33,280\\},N=\\{14,20\\}$', A['pairB'][1], '2\\to2')]
for name, t, cl in ev:
    rows.append(f"{name} & ${fv(t['f'])}\\to{fv(t['f2'])}$ & ${fv(t['new'])}$ & ${fv(t['b'])}\\to{fv(t['b2'])}$ & ${fv(t['db'])}$ & ${cl}$\\\\")
rows.append('\\bottomrule\\end{tabular}')
open(H+'/tex/tables/local_table.tex', 'w').write('\n'.join(rows)+'\n')
print('tables written')
