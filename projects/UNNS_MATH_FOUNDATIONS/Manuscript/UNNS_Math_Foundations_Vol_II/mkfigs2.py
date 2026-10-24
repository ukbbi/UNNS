#!/usr/bin/env python3
"""Figures of Volume II, generated from exact computations (no stock illustrations).
Run from the package root:  python3 mkfigs2.py   (writes figs/*.pdf and figs/figdata.json)."""
import sys, os, json, random, math
sys.argv = [sys.argv[0], '--quick']          # cheap seed table for the import below
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fractions import Fraction as Fr
from math import gcd, isqrt, log2
from engine import *
from engine_seeds import gen_reset
import check_volume_ii as C

os.makedirs('figs', exist_ok=True)
plt.rcParams.update({'font.family': 'serif', 'font.size': 9, 'mathtext.fontset': 'cm', 'pdf.fonttype': 42,
                     'axes.spines.top': False, 'axes.spines.right': False})
BLUE = '#1f4e8c'; RED = '#b3361f'; GREY = '#8a8a8a'; GREEN = '#2a7a4b'; GOLD = '#b8860b'; PURPLE = '#6b3fa0'
COLS = [BLUE, RED, GREEN, GOLD, PURPLE, GREY]
DATA = {}

def save(fig, name):
    fig.savefig(f'figs/{name}.pdf'); plt.close(fig)

# ---------------------------------------------------------------- 1. growth of R along exact orbits
seedlist = [(Fr(4), '4'), (Fr(36), '36'), (Fr(45828, 5), '45828/5'), (Fr(20736, 5), '20736/5'), (Fr(81, 4), '81/4'), (Fr(220), '220')]
fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.6))
Gdata = {}
for (x0, lab), c in zip(seedlist, COLS):
    st = C.orbit_states(x0, 60)
    R = [len(s[1]) for s in st]; G = [s[2] for s in st]
    ax[0].step(range(len(R)), R, where='post', color=c, lw=1.2, label=f'$x_0={lab}$')
    ax[1].step(range(len(G)), G, where='post', color=c, lw=1.2)
    Gdata[lab] = (R[0], R[-1], G[0], G[-1])
ax[0].set_xlabel('$n$'); ax[0].set_ylabel('$R(x_n)$'); ax[0].legend(fontsize=6.5, frameon=False, loc='upper left')
ax[1].set_yscale('log'); ax[1].set_xlabel('$n$'); ax[1].set_ylabel('$G(x_n)$')
ax[0].set_title('fibre multiplicity (T19)', fontsize=8.5); ax[1].set_title('gcd of the moduli (T31)', fontsize=8.5)
fig.tight_layout(); save(fig, 'fig_growth'); DATA['growth'] = Gdata

# ---------------------------------------------------------------- 2. G-divisor chains
best = None
for x in C.SEEDS:
    D = fibre(x); G0 = Gof(D)
    if G0 < 20 or is_prime(G0): continue
    st = C.orbit_states(x, 45)
    Gs = [s[2] for s in st]
    chain = [Gs[0]] + [Gs[i] for i in range(1, len(Gs)) if Gs[i] != Gs[i - 1]]
    if len(chain) >= 4 and len(st) == 45 and (best is None or len(chain) > len(best[1]) or (len(chain) == len(best[1]) and G0 < best[1][0])):
        best = (x, chain, Gs)
x0, chain, Gs = best
fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.7), gridspec_kw={'width_ratios': [1.15, 1]})
ax[0].step(range(len(Gs)), Gs, where='post', color=BLUE, lw=1.4)
ax[0].set_yscale('log'); ax[0].set_xlabel('$n$'); ax[0].set_ylabel('$G(x_n)$')
ax[0].set_title(f'$x_0={x0}$', fontsize=8.5)
for g in chain: ax[0].axhline(g, color=GREY, lw=.4, ls=':')
ax[0].set_yticks(chain); ax[0].set_yticklabels([str(g) for g in chain])
g0 = chain[0]; divs = sorted(divisors_from(factor(g0)))
lev = {d: sum(factor(d).values()) for d in divs}
byl = {}
for d in divs: byl.setdefault(lev[d], []).append(d)
pos = {}
for l, ds in byl.items():
    for i, d in enumerate(ds): pos[d] = ((i + 1) / (len(ds) + 1), l)
for d in divs:
    for e in divs:
        if d != e and e % d == 0 and lev[e] == lev[d] + 1:
            on = d in chain and e in chain and chain.index(e) == chain.index(d) - 1
            ax[1].plot([pos[d][0], pos[e][0]], [pos[d][1], pos[e][1]], color=RED if on else GREY, lw=1.6 if on else .6, zorder=1)
for d in divs:
    ax[1].scatter(*pos[d], s=220, color='white', edgecolor=RED if d in chain else GREY, zorder=2, lw=1.2)
    ax[1].text(pos[d][0], pos[d][1], str(d), ha='center', va='center', fontsize=7)
ax[1].set_axis_off(); ax[1].set_title(f'divisor lattice of $g_0={g0}$; realised chain in red', fontsize=8.5)
fig.tight_layout(); save(fig, 'fig_gchain'); DATA['gchain'] = {'x0': str(x0), 'chain': chain}

# ---------------------------------------------------------------- 3. regime I entry times
ts = [t for t in range(1, 2001) if all(e == 1 for e in factor(t).values())]
ent = []
for t in ts:
    n = 0; tt = t
    while tt > 3: tt = C.squarefree_part(tt + 1); n += 1
    ent.append(n)
fig, ax = plt.subplots(figsize=(6.2, 2.4))
ax.scatter(ts, ent, s=5, color=BLUE, label='observed entry time $N(t)$ (steps)')
xs = list(range(1, 2001))
ax.step(xs, [4 * kappa3(t) for t in xs], where='post', color=RED, lw=1, label='bound $4\\kappa_3(t)$ (T32)')
ax.set_xscale('log'); ax.set_xlabel('squarefree part $t$ of the starting integer'); ax.set_ylabel('steps to the cycle $1\\to2\\to3$')
ax.legend(frameon=False, fontsize=8)
fig.tight_layout(); save(fig, 'fig_regimeI'); DATA['regimeI'] = {'max_entry_t<=2000': max(ent), 'bound_at_max': max(4 * kappa3(t) for t in ts)}

# ---------------------------------------------------------------- 4. gamma sawtooth panels
fig, axs = plt.subplots(2, 2, figsize=(6.4, 3.9))
panels = []
# regime I: x=4: gamma = t
st = C.orbit_states(Fr(4 * 3 * 7), 14); g_reg = [int(s[0] / (s[3] ** 2)) for s in st]
panels.append(('regime I ($G=1$): $\\gamma=t$ cycles $1,2,3$', g_reg, BLUE))
mo = C.machine_orbit(11, 1, {2: 2, 3: 3, 5: 4}, 25); panels.append(('$g=11$, $q=3$: cycle $1,\\dots,8$ (T50)', [m[0] for m in mo], RED))
mo = C.machine_orbit(31, 1, {2: 5, 101: 2}, 70); panels.append(('$g=31$, carries $2^2,2^2,2^1$: $P=33$ (T56)', [m[0] for m in mo], GREEN))
E7 = q_seed = C.q_seed(7, 367); mo = C.machine_orbit(367, 1, E7, 110); panels.append(('$g=367$, $q=7$: cycle $1,\\dots,48$ (T57)', [m[0] for m in mo], GOLD))
for a, (t, ys, c) in zip(axs.flat, panels):
    a.plot(range(len(ys)), ys, '.-', ms=2.6, lw=.7, color=c); a.set_title(t, fontsize=8)
    a.set_xlabel('$n$', fontsize=8); a.set_ylabel('$\\gamma_n$', fontsize=8)
fig.tight_layout(); save(fig, 'fig_gamma'); DATA['gamma_panels'] = [t for t, _, _ in panels]

# ---------------------------------------------------------------- 5. odometer wheel, g=31
E = {2: 5, 101: 2}
o, Abs = abs_set(31, E, 2)
gaps = cyc_gaps(Abs, o)
fig = plt.figure(figsize=(6.4, 2.9))
ax = fig.add_axes([0.02, 0.02, 0.44, 0.9], projection='polar')
th = [2 * math.pi * k / o for k in range(o)]
ax.set_theta_zero_location('N'); ax.set_theta_direction(-1)
for k in range(o):
    ax.scatter([th[k]], [1], s=380, color=GREEN if k in Abs else 'white', edgecolor='black', zorder=3)
    ax.text(th[k], 1, str(k), ha='center', va='center', color='white' if k in Abs else 'black', fontsize=9, zorder=4)
cur = sorted(Abs)
for i, a in enumerate(cur):
    b = cur[(i + 1) % len(cur)]; ang = (b - a) % o or o
    ts_ = [2 * math.pi * (a + ang * s / 30) / o for s in range(31)]
    ax.plot(ts_, [1.0 + 0.18 * math.sin(math.pi * s / 30) for s in range(31)], color=RED, lw=1.2)
ax.set_ylim(0, 1.5); ax.set_axis_off()
ax.set_title(f'phases $e_2 \\ \\mathrm{{mod}}\\ {o}$ ($g=31$); green = $\\mathrm{{Abs}}_2$', fontsize=8.5)
ax2 = fig.add_axes([0.55, 0.2, 0.42, 0.62])
mo = C.machine_orbit(31, 1, E, 70)
gs_ = [m[0] for m in mo]
ax2.plot(range(len(gs_)), gs_, '.-', ms=2.5, lw=.7, color=GREEN)
ax2.set_xlabel('$n$'); ax2.set_ylabel('$\\gamma_n$')
ax2.set_title(f'carries $2^{{{gaps[0]}}},2^{{{gaps[1]}}},2^{{{gaps[2]}}}$; cycle lengths $2^{{2j}}-1$', fontsize=8.5)
save(fig, 'fig_wheel'); DATA['wheel'] = {'o': o, 'Abs': sorted(Abs), 'gaps': gaps}

# ---------------------------------------------------------------- 6. exact scaling, g=31 example
fig, ax = plt.subplots(2, 1, figsize=(6.2, 3.7), sharex=True)
mo = C.machine_orbit(31, 1, E, 110)
xs_ = [state_to_x(31, m[0], m[1]) for m in mo]
ax[0].plot(range(len(xs_)), [log2(x.numerator) - log2(x.denominator) for x in xs_], color=GREEN, lw=1)
ax[0].set_ylabel('$\\log_2 x_n$')
P = 33
rat = [xs_[n + P] / xs_[n] for n in range(len(xs_) - P)]
ax[1].plot(range(len(rat)), [float(r) for r in rat], 'o', ms=2.5, color=RED)
ax[1].set_yscale('log'); ax[1].set_ylabel(f'$x_{{n+{P}}}/x_n$'); ax[1].set_xlabel('$n$')
ax[1].axhline(1024, color=GREY, lw=.5, ls=':'); ax[1].text(1, 1024 * 1.3, '$\\rho^2=2^{10}$', fontsize=8)
assert all(r == 1024 for r in rat), set(rat)
fig.tight_layout(); save(fig, 'fig_scaling'); DATA['scaling'] = {'P': P, 'ratio': 1024}

# ---------------------------------------------------------------- 7. T50 ratios and R
fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.5))
S = 4 * 3 ** 3 * 5 ** 4
rows = direct(Fr(S * S, 11), 40, keepx=True)
rat = [rows[j + 3][5] / rows[j][5] for j in range(8)]
ax[0].bar(range(8), [float(r) for r in rat], color=BLUE)
for j, r in enumerate(rat): ax[0].text(j, float(r) + .05, str(r), ha='center', fontsize=7)
ax[0].set_xlabel('$j$ (phase in the eight-cycle)'); ax[0].set_ylabel('$x_{n+3}/x_n$'); ax[0].set_title('no three-step law (T50(iv))', fontsize=8.5)
ax[1].step(range(len(rows)), [r[4] for r in rows], where='post', color=RED)
ax[1].set_xlabel('$n$'); ax[1].set_ylabel('$R(x_n)$'); ax[1].set_title('$R(x_{n+8})=R(x_n)+2$', fontsize=8.5)
fig.tight_layout(); save(fig, 'fig_ratios'); DATA['ratios'] = [str(r) for r in rat]

# ---------------------------------------------------------------- 8. carry competition (real orbit g=53)
g = 53; E0 = {2: 2, 3: 2, 13: 3, 197: 4}
gam, Ec = 1, dict(E0)
n0 = normalise(g, 1, E0); assert n0 is not None and n0[0] == 1
Ec = n0[1]
hist = []; fires = []
for k in range(26):
    pend = {}
    for p in (2, 3, 5, 7):
        j = pend_j(g, Ec, p)
        pend[p] = p ** j if j else None
    nm = next_M(g, Ec)
    hist.append(pend); fires.append(nm[0] if nm else None)
    if nm is None: break
    Ec = nm[1]
x_ = range(len(hist))
fig, ax = plt.subplots(figsize=(6.4, 2.7))
for p, c in zip((2, 3, 5, 7), (BLUE, RED, GREEN, GOLD)):
    ys = [h[p] if h[p] else float('nan') for h in hist]
    ax.plot(x_, ys, '-', color=c, lw=.8, alpha=.7)
    idx = [i for i in x_ if fires[i] and any(fires[i] == p ** j for j in range(1, 9)) and hist[i][p] == fires[i]]
    ax.plot(idx, [hist[i][p] for i in idx], 'o', color=c, ms=5, label=f'$p={p}$ (markers: carries that fire)')
ax.axhline(isqrt(g - 1) + 0.0, color=GREY, ls='--', lw=.7); ax.text(0, isqrt(g - 1) * 1.06, '$\\sqrt{g}$ (window)', fontsize=7.5, ha='left')
ax.set_yscale('log'); ax.set_xlabel('carry number $k$ (reset states of the orbit)'); ax.set_ylabel('pending carry $c_p(E_k)$')
ax.legend(frameon=False, fontsize=6.8, loc='center right')
ax.set_title('$g=53$, $E_0=\\{2^2,3^2,13^3,197^4\\}$: $3$ fires five times, then starves', fontsize=8.5)
fig.tight_layout(); save(fig, 'fig_competition')
DATA['competition'] = {'g': g, 'E0': E0, 'fires': [f for f in fires], 'direct_check': None}
# direct confirmation of the first 16 steps against iteration of C
x0_ = state_to_x(g, 1, n0[1]); dr = direct(x0_, 16); mo = C.machine_orbit(g, 1, n0[1], 16)
assert all(a[0] == b[1] and lval(a[1]) == b[2] and b[3] == g for a, b in zip(mo, dr))
DATA['competition']['direct_check'] = 'first 16 steps agree with direct iteration of C'

# ---------------------------------------------------------------- 9. selection: worst-case carries and certificate
g = 127; Ef = {2: 6, 3: 6, 11: 2, 41: 6}          # a statically certified reset state (survivor r=2, m=4)
assert normalise(g, 1, Ef) == (1, Ef)
fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.6))
rows_ = []
for p in (2, 3, 5, 7):
    o_, A_ = abs_set(g, Ef, p)
    sat = Ef.get(p, 0) >= o_ - 1
    j = pend_j(g, Ef, p)
    rows_.append((p, o_, sorted(A_), p ** C.maxgap(A_, o_) if (A_ and sat) else None, sat, p ** j if j else None, Ef.get(p, 0)))
lab = [f'$p={r[0]}$' for r in rows_]
ax[0].bar(lab, [r[5] or 0 for r in rows_], color=[BLUE if r[4] else GREY for r in rows_])
for i, r in enumerate(rows_):
    ax[0].text(i, (r[5] or 0) * 1.05 + .2, f'$c_p={r[5]}$', ha='center', fontsize=7)
    if r[3]: ax[0].plot([i - .4, i + .4], [r[3], r[3]], color=RED, lw=1.6)
ax[0].axhline(isqrt(g - 1) + 0.5, color=GREEN, ls='--', lw=.8); ax[0].text(3.45, isqrt(g - 1) + 0.9, '$\\sqrt{g}$', color=GREEN, fontsize=7.5, ha='right')
ax[0].set_ylabel('pending carry $c_p$'); ax[0].set_title('pending carries (red bar: $m_p$)', fontsize=8.5)
r0 = min((r for r in rows_ if r[4]), key=lambda r: r[3])[0]; m0 = min((r for r in rows_ if r[4]), key=lambda r: r[3])[3]
Ms = list(range(2, isqrt(g - 1) + 1)); av = [avail(g, Ef, M) for M in Ms]
ax[1].bar([str(M) for M in Ms], [1 if a_ else 0 for a_ in av], color=[GREEN if (a_ and M == r0 ** round(math.log(M, r0))) else (RED if a_ else '#dddddd') for a_, M in zip(av, Ms)])
ax[1].set_yticks([0, 1]); ax[1].set_yticklabels(['no', 'yes']); ax[1].set_xlabel('candidate carry $M$'); ax[1].set_ylabel('available at the state')
ax[1].set_title(f'survivor $r={r0}$, $m={m0}$ (green: powers of $r$)', fontsize=8.5)
fig.tight_layout(); save(fig, 'fig_selection')
DATA['selection'] = {'g': g, 'rows': [(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows_], 'avail': {M: bool(a_) for M, a_ in zip(Ms, av)}}

# ---------------------------------------------------------------- 10. kappa
fig, ax = plt.subplots(figsize=(6.2, 2.7))
As = sorted({int(a) for a in [2 ** (i / 4) for i in range(4, 84)]} | {1})
xs = sorted({max(1, int(10 ** (i / 60))) for i in range(0, 6 * 60 + 30)})
ax.step(xs, [kappa_closed(a) for a in xs], where='post', color=BLUE, lw=1.5, label='$\\kappa(\\gamma_0)$ (T69)')
ax.plot(xs, [math.ceil(math.log2(a)) if a > 1 else 0 for a in xs], color=GREY, lw=1, ls='--', label='$\\lceil\\log_2\\gamma_0\\rceil$')
W = json.load(open('witnesses.json'))
ax.plot([w[2] for w in W.values()], [int(k) for k in W], 'o', color=RED, ms=5, label='exact orbits attaining $\\kappa$ carries')
ax.set_xscale('log'); ax.set_xlabel('$\\gamma_0$'); ax.set_ylabel('carries to the first reset')
ax.set_xlim(1, 3e6); ax.legend(frameon=False, fontsize=8)
fig.tight_layout(); save(fig, 'fig_kappa')

# ---------------------------------------------------------------- 11. observed vs certified
rng = random.Random(8); obs = []
import time
t0 = time.time()
while len(obs) < 150:
    sd = gen_reset(rng)
    if not sd: continue
    g, E = sd
    fc = C.find_cycle(g, 1, E, cap=4000)
    if fc is None: continue
    n1, n2, states = fc
    resets = [i for i, (ga, _) in enumerate(states) if ga == 1]
    obs.append((g, sum(1 for i in resets if i < n1)))
gs_all = [p for p in range(11, 260) if is_prime(p)]
fig, ax = plt.subplots(figsize=(6.4, 2.9))
ax.plot(gs_all, [Hclass(g) for g in gs_all], color=RED, lw=1.2, label='$H(g)-1$ (T70)')
ax.plot(gs_all, [Kpoly(g) for g in gs_all], color=BLUE, lw=1.2, label='$K_{\\mathrm{poly}}(g)$ (T71)')
ax.plot([o[0] for o in obs], [max(o[1], 0.5) for o in obs], '.', color='black', ms=3.5, label='observed entry index (prime-$g$ reset states)')
ax.set_yscale('log'); ax.set_xlabel('prime $g$'); ax.set_ylabel('carries after the first reset'); ax.legend(frameon=False, fontsize=7.5, loc='upper left')
fig.tight_layout(); save(fig, 'fig_bounds')
DATA['bounds'] = {'n_seeds': len(obs), 'max_observed': max(o[1] for o in obs), 'at_g': [o[0] for o in obs if o[1] == max(x[1] for x in obs)][:1]}

# ---------------------------------------------------------------- 12. reach sets
fig, ax = plt.subplots(figsize=(6.2, 2.6))
Xs = [2 ** k for k in range(1, 21)]
def reach(x0, N):
    U = set()
    for s in C.orbit_states(x0, N): U |= set(s[1])
    return U
U1 = reach(Fr(4), 75); U2 = reach(Fr(36 * 5), 75)
g = 5; s0 = (g + 1) * (g + 2) ** ordmod(2, g); U3 = reach(Fr(s0 * s0, g), 75)
for U, lab, c in [(U1, '$x_0=4$ ($G=1$)', BLUE), (U2, '$x_0=180$ ($G=1$)', GREEN), (U3, '$g=5$ (persistent $P_5$)', RED)]:
    ax.plot(Xs, [sum(1 for d in U if d <= X) for X in Xs], 'o-', ms=3, lw=.8, color=c, label=lab)
ax.set_xscale('log', base=2); ax.set_xlabel('$X$'); ax.set_ylabel('$U(X)=\\#\\{d\\leq X\\}$ reached')
ax.legend(frameon=False, fontsize=7.5, loc='upper left')
fig.tight_layout(); save(fig, 'fig_reach')

# ---------------------------------------------------------------- 13. proof-dependency DAG from the registry
reg = json.load(open('registry.json'))
recs = {r['id']: r for r in reg['records'] if str(r['vol']).startswith('II')}
spine = ['F.T1', 'F.T6', 'F.T8', 'F.CDEF', 'F.T31', 'F.T44', 'F.T49', 'F.T51', 'F.T54', 'F.T55', 'F.T56', 'F.T60', 'F.T64', 'F.T67', 'F.T66', 'F.T70', 'F.T72']
chap = {}
def chapter_of(i):
    t = recs[i]['vol']
    return int(t.split('.')[1])
# manuscript chapter of each record (matches the layout of the volume)
M = {}
for i in recs:
    if i.startswith('O'): continue
    n = i[2:]
    if i in ('F.CDEF', 'F.T31', 'F.T17p', 'F.T17', 'F.T18', 'F.T19', 'F.T26', 'F.T27', 'F.T28'): M[i] = 1
    elif i in ('F.T30', 'F.T32', 'F.T33', 'F.T34', 'F.L1', 'F.L2', 'F.L3', 'F.L4', 'F.L5', 'F.T35', 'F.T36', 'F.T37'): M[i] = 2
    elif i in ('F.L6', 'F.T38', 'F.T38a', 'F.T39', 'F.T40', 'F.T41', 'F.T42', 'F.T43', 'F.T44', 'F.T45', 'F.T46', 'F.T47'): M[i] = 3
    elif i in ('F.T48', 'F.T49', 'F.T50', 'F.T51', 'F.T52', 'F.T53', 'F.T54', 'F.T55', 'F.T56', 'F.T57', 'F.T58'): M[i] = 4
    elif i in ('F.T59', 'F.T60', 'F.T61', 'F.T62', 'F.T63'): M[i] = 5
    elif i in ('F.T64', 'F.T65', 'F.T66', 'F.T67', 'F.T68'): M[i] = 6
    else: M[i] = 7
fig, ax = plt.subplots(figsize=(6.6, 4.9))
cols_ = {c: [] for c in range(1, 8)}
for i, c in M.items(): cols_[c].append(i)
def tnum(i):
    s = i[2:]
    import re
    m = re.match(r'([A-Za-z]+)(\d+)(.*)', s)
    return (0 if m.group(1) == 'CDEF' else 1, int(m.group(2)) if m and m.group(2) else 0, m.group(3)) if m else (0, 0, s)
P = {}
for c, ids in cols_.items():
    ids = sorted(ids, key=lambda i: (tnum(i)))
    for k, i in enumerate(ids): P[i] = (c, -k)
for i, r in recs.items():
    if i not in P: continue
    for d in r['deps']:
        if d in P:
            on = i in spine and d in spine
            ax.annotate('', xy=P[i], xytext=P[d], arrowprops=dict(arrowstyle='-', color=RED if on else '#cccccc', lw=1.0 if on else .35, shrinkA=3, shrinkB=3), zorder=1 if not on else 2)
for i, (c, y) in P.items():
    on = i in spine
    ax.text(c, y, i[2:], ha='center', va='center', fontsize=5.6, color='white' if on else 'black',
            bbox=dict(boxstyle='round,pad=0.18', fc=RED if on else 'white', ec=RED if on else GREY, lw=.5), zorder=3)
ax.set_xlim(0.4, 7.6); ax.set_ylim(min(y for c, y in P.values()) - 1, 1)
ax.set_xticks(range(1, 8)); ax.set_xticklabels([f'Ch. {c}' for c in range(1, 8)], fontsize=8); ax.set_yticks([])
for s in ('left', 'bottom'): ax.spines[s].set_visible(False)
ax.xaxis.tick_top()
fig.tight_layout(); save(fig, 'fig_dag')
DATA['dag'] = {'n_nodes': len(P), 'n_edges': sum(1 for i, r in recs.items() if i in P for d in r['deps'] if d in P), 'spine': spine}

json.dump(DATA, open('figs/figdata.json', 'w'), indent=1, default=str)
print('figures written:', sorted(os.listdir('figs')))
