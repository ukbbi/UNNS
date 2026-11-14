"""Generate LaTeX tables for UNNS_PRIME_DYN_v001 from the engine and from data/*.json."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdyn import *
from paths import *
import verify_prime_dyn as V
from mpmath import mp, mpf, log as mlog

def w(name, s): open(os.path.join(TAB, name), 'w').write(s)

# --- orbits table
rows = []
for x0 in [2, 3, 5, 7, 12, 30, 97, 1009, 10 ** 6 + 3, 2 ** 20]:
    it, ab, T, Ts, lb = V.regime(x0, V.EXACT + 400)
    pre = ''.join(map(str, it[:24]))
    xs = f'${x0}$' if x0 < 10 ** 7 and x0 != 2 ** 20 else '$2^{20}$'
    rows.append(f"{xs} & {T} & {Ts} & {ab[Ts][0]} & {ab[Ts][1]} & \\texttt{{{pre}}} \\\\")
w('orbits.tex', '\\begin{tabular}{@{}rrrrrl@{}}\\toprule\n$x_0$ & $T$ & $T^*$ & $\\alpha_{T^*}$ & $\\beta_{T^*}$ & first 24 letters of the itinerary\\\\\\midrule\n' + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\n')

# --- regimes table (prime-fire rules)
mp_ = json.load(open(os.path.join(DATA, 'minpp_periods.json')))
reg = [('SPF', 'smallest prime factor', '$(3,2,2,2,2)^\\infty$', '5', 'proved (Thm~\\ref{thm:spf})'),
       ('LPF', 'largest prime factor', '$(2,3,3)^\\infty$', '3', 'proved (Thm~\\ref{thm:lpf})'),
       ('MINPP', 'smallest prime-power part $p^{v_p}$', 'period $3$ ($%d$ starts) or $5$ ($%d$ starts)' % (mp_['3'], mp_['5']), '3 or 5', 'computed, $2\\le x_0\\le400$'),
       ('MAXPP', 'largest prime-power part $p^{v_p}$', 'Sturmian, $p(k)=k+1$', '$\\infty$ (aperiodic)', 'proved (Thm~\\ref{thm:B})')]
w('regimes.tex', '\\begin{tabular}{@{}llllp{0.2\\textwidth}@{}}\\toprule\nrule & selects & eventual itinerary & period & status\\\\\\midrule\n' + '\n'.join(f'{a} & {b} & {c} & {d} & {e} \\\\' for a, b, c, d, e in reg) + '\n\\bottomrule\\end{tabular}\n')

# --- Stormer
S = json.load(open(os.path.join(DATA, 'stormer_tables.json')))
rows = []
for key, v in S.items():
    sset = key.strip('[]').replace(' ', '')
    rows.append(f"$\\{{{sset}\\}}$ & {len(v)} & {max(v)} & {', '.join(map(str, v[:10]))}{', \\dots' if len(v) > 10 else ''} \\\\")
w('stormer.tex', '\\begin{tabular}{@{}lrrp{0.5\\textwidth}@{}}\\toprule\n$S$ & $\\#\\{N\\ge2\\}$ & $\\max N$ & smallest values of $N$ with $N,N+1$ both $S$-smooth\\\\\\midrule\n' + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\n')

# --- continued fraction of theta
x = mlog(mpf(48)) / mlog(mpf(864)); cf = []
for _ in range(14):
    a = int(mp.floor(x)); cf.append(a); x = 1 / (x - a)
h0, h1, k0, k1 = 1, cf[0], 0, 1; conv = [(h1, k1)]
for a in cf[1:]:
    h0, h1 = h1, a * h1 + h0; k0, k1 = k1, a * k1 + k0; conv.append((h1, k1))
th = mlog(mpf(48)) / mlog(mpf(864))
rows = [f"{i} & {cf[i]} & {p}/{q} & ${mp.nstr(abs(q * th - p), 4)}$ \\\\" for i, (p, q) in enumerate(conv)]
w('cf.tex', '\\begin{tabular}{@{}rrlr@{}}\\toprule\n$i$ & $a_i$ & convergent $p_i/q_i$ & $|q_i\\theta-p_i|$\\\\\\midrule\n' + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\n')
json.dump({'cf': cf}, open(os.path.join(DATA, 'theta_cf.json'), 'w'))

# --- Theorem E rows
E = json.load(open(os.path.join(DATA, 'thmE_rows.json')))
rows = []
for r in E[:8]:
    d, nb, Q, M, cnt, bd = r
    rows.append(f"{d} & {nb} & {Q} & {M} & {cnt} & ${bd:.2e}$ \\\\".replace('e+0', '\\cdot10^{').replace('e+', '\\cdot10^{') if False else f"{d} & {nb} & {Q} & {M} & {cnt} & {bd:,} \\\\".replace(',', '\\,'))
w('thmE_rows.tex', '\\begin{tabular}{@{}rrrrrr@{}}\\toprule\n$d$ & $|\\mathcal N|$ & $|Q|$ & $M$ & $p_{\\rm all}(6)$ & bound of Thm~\\ref{thm:E}\\\\\\midrule\n' + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\n')

# --- ORDER tables
O = json.load(open(os.path.join(DATA, 'order_blocks.json')))
rows = [f"{k} & {O['counts'][str(k)]} & {2**k} & {2**math.ceil(2*k/math.pi**2)} \\\\" for k in range(1, 15)]
w('order_blocks.tex', '\\begin{tabular}{@{}rrrr@{}}\\toprule\n$k$ & $p_u(k)$ (computed) & $2^k$ & $2^{\\lceil 2k/\\pi^2\\rceil}$ (proved lower bound)\\\\\\midrule\n' + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\n')
rows = [f"{k} & {v[0]} & {v[1]} & {v[2]} \\\\" for k, v in O['crt'].items()]
w('order_crt.tex', '\\begin{tabular}{@{}rrrr@{}}\\toprule\n$k$ & $|E_r|$ & patterns $2^{|E_r|}$ & realised by an explicit $m$\\\\\\midrule\n' + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\n')

# --- checks table
R = json.load(open(os.path.join(REP, 'verification_report.json')))
def esc(s):
    return s.replace('\\', '').replace('_', '\\_').replace('&', '\\&').replace('%', '\\%').replace('#', '\\#').replace('^', '\\^{}').replace('{', '\\{').replace('}', '\\}').replace('<', '$<$').replace('>', '$>$')
rows = [f"\\texttt{{{c['check'].replace('_', chr(92)+'_')}}} & {'pass' if c['pass'] else 'FAIL'} \\\\" for c in R['checks']]
w('checks.tex', '{\\small\\begin{longtable}{@{}lr@{}}\\toprule\ncheck & outcome\\\\\\midrule\\endhead\n' + '\n'.join(rows) + '\n\\bottomrule\\end{longtable}}\n')
print('tables ok')
