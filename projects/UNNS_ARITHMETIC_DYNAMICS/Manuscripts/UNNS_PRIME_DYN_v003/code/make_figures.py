"""UNNS_PRIME_DYN_v001 figures (computed from the engine pdyn.py and from data/*.json written by the verifier)."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, FancyArrowPatch
from pdyn import *
from mpmath import log as mlog, mpf
from paths import *
import verify_prime_dyn as V

plt.rcParams.update({'font.size': 9, 'axes.titlesize': 9.5, 'axes.labelsize': 9, 'figure.dpi': 150,
                     'axes.spines.top': False, 'axes.spines.right': False})
C2c, C3c, GR = '#1b6ca8', '#c0392b', '#7f8c8d'
Af, Bf, Lf = float(A), float(B), float(L); th = float(THETA)

def save(fig, name):
    fig.savefig(os.path.join(FIG, name + '.pdf'), bbox_inches='tight'); fig.savefig(os.path.join(FIG, name + '.png'), bbox_inches='tight', dpi=170); plt.close(fig)

def regime_tail(x0, n):
    it, ab, T, Ts, _ = V.regime(x0, V.EXACT + n)
    return it, ab, T, Ts

# ---------------- Fig 1: the circle of length ln 864 (to scale)
def fig1():
    fig, ax = plt.subplots(1, 2, figsize=(8.6, 3.8), gridspec_kw={'width_ratios': [1.05, 1]})
    a = ax[0]; a.set_aspect('equal'); a.axis('off')
    # angle fraction: f in [-A,B) mapped to angle 360*(f+A)/L starting from top, clockwise
    def ang(f): return 90 - 360 * (f + Af) / Lf
    a.add_patch(Wedge((0, 0), 1.0, ang(0), ang(-Af), width=0.22, color=C3c, alpha=.85))     # f in [-A,0): fire 3
    a.add_patch(Wedge((0, 0), 1.0, ang(Bf), ang(0), width=0.22, color=C2c, alpha=.85))      # f in [0,B): fire 2
    for f, lab in [(-Af, r'$-\ln18$'), (0, r'$0$')]:
        t = math.radians(ang(f)); a.text(1.22 * math.cos(t), 1.22 * math.sin(t), lab, ha='center', va='center')
    a.text(0, 0.1, 'circle of length', ha='center', fontsize=8); a.text(0, -0.1, r'$\ln864=\ln18+\ln48$', ha='center', fontsize=8)
    a.text(0.0, 0.62, '', ha='center')
    t = math.radians(ang(Bf / 2)); a.text(1.62 * math.cos(t), 1.62 * math.sin(t), 'fire 2: $f>0$\n$f\\mapsto f-\\ln18$\n(arc length $\\ln48$)', ha='center', va='center', color=C2c, fontsize=8)
    t = math.radians(ang(-Af / 2)); a.text(1.62 * math.cos(t), 1.62 * math.sin(t), 'fire 3: $f<0$\n$f\\mapsto f+\\ln48$\n(arc length $\\ln18$)', ha='center', va='center', color=C3c, fontsize=8)
    a.set_xlim(-2.3, 2.3); a.set_ylim(-1.5, 1.5); a.set_title('(a) the two valuation translations as one rotation (to scale)')
    # orbit points
    it, ab, T, Ts = regime_tail(2, 40)
    pts = []
    for i in range(Ts, Ts + 14):
        f = ab[i][0] * LN2F - ab[i][1] * LN3F
        pts.append(f)
    for j, f in enumerate(pts):
        t = math.radians(ang(f)); a.plot(1.11 * math.cos(t), 1.11 * math.sin(t), 'o', ms=3.2, color='k')
    b = ax[1]
    f0 = pts[0]
    zs = [(f + Af) / Lf for f in pts]
    b.plot(range(len(zs)), zs, 'o-', color='k', ms=3, lw=.7)
    b.axhline(1 - th, color=GR, ls='--', lw=.8); b.text(len(zs) - 1, 1 - th + .02, r'$1-\theta$', ha='right', color=GR)
    b.set_xlabel('step $j$'); b.set_ylabel(r'$z_j=\{z+j\theta\}$'); b.set_title(r'(b) $z_j$ for the orbit of $x_0=2$ ($\theta=\ln48/\ln864$)')
    b.set_ylim(0, 1); b.set_xticks(range(0, len(zs), 2))
    save(fig, 'fig1_rotation')

# ---------------- Fig 2: the valuation plane
def fig2():
    fig, ax = plt.subplots(1, 2, figsize=(8.6, 3.5))
    for k, x0 in enumerate([2, 97]):
        it, ab, T, Ts = regime_tail(x0, 300)
        a = np.array(ab[:300]); ax[0].plot(a[:, 0], a[:, 1], '-', lw=.6, color=[C2c, C3c][k], label=f'$x_0={x0}$')
        ax[0].plot(a[0, 0], a[0, 1], 'o', ms=3.5, color=[C2c, C3c][k])
    xs = np.linspace(0, 700, 2); ax[0].plot(xs, xs * math.log(2) / math.log(3), 'k--', lw=.8, label=r'$\alpha\ln2=\beta\ln3$')
    ax[0].set_xlabel(r'$\alpha=v_2(x)$'); ax[0].set_ylabel(r'$\beta=v_3(x)$'); ax[0].legend(frameon=False); ax[0].set_title('(a) valuation path, 300 steps')
    it, ab, T, Ts = regime_tail(2, 3000)
    f = np.array([ab[i][0] * LN2F - ab[i][1] * LN3F for i in range(len(ab))])
    ax[1].plot(f[:400], lw=.6, color='k')
    ax[1].axhline(Bf, color=C2c, ls='--', lw=.8); ax[1].axhline(-Af, color=C3c, ls='--', lw=.8); ax[1].axhline(0, color=GR, lw=.5)
    ax[1].text(398, Bf + .08, r'$\ln48$', ha='right', color=C2c); ax[1].text(398, -Af - .35, r'$-\ln18$', ha='right', color=C3c)
    ax[1].set_xlabel('step $n$'); ax[1].set_ylabel(r'$f_n=\alpha_n\ln2-\beta_n\ln3$'); ax[1].set_title('(b) $f_n$ stays in $[-\\ln18,\\ln48)$')
    fig.tight_layout(); save(fig, 'fig2_valuation_plane')

# ---------------- Fig 3: itinerary and complexity
def fig3():
    fig, ax = plt.subplots(1, 2, figsize=(8.8, 3.3), gridspec_kw={'width_ratios': [1.1, 1]})
    it, ab, T, Ts = regime_tail(2, 6000)
    w = it[Ts:Ts + 90]
    for i, c in enumerate(w):
        ax[0].add_patch(plt.Rectangle((i % 45, -(i // 45)), .9, .8, color=C2c if c == 2 else C3c))
    ax[0].set_xlim(0, 45); ax[0].set_ylim(-2, 1); ax[0].axis('off')
    ax[0].set_title('(a) first 90 letters of the tail, $x_0=2$ (blue 2, red 3)')
    ax[0].text(0, -2.3, 'no two consecutive 3s; no three consecutive 2s', fontsize=8)
    ks = np.arange(1, 31)
    for x0, mk in [(2, 'o'), (97, 's'), (10 ** 6 + 3, '^'), (30030, 'd')]:
        it, ab, T, Ts = regime_tail(x0, 6000)
        tail = it[Ts:]
        ax[1].plot(ks, [factor_complexity(tail, k) for k in ks], mk, ms=3.2, label=f'$x_0={x0}$')
    ax[1].plot(ks, ks + 1, 'k-', lw=.7, label='$k+1$'); ax[1].plot(ks, 2.0 ** ks, color=GR, ls=':', lw=.8, label='$2^k$')
    ax[1].set_yscale('log'); ax[1].set_ylim(1.5, 4000); ax[1].set_xlabel('$k$'); ax[1].set_ylabel('$p(k)$'); ax[1].legend(frameon=False, fontsize=7)
    ax[1].set_title('(b) factor complexity of the tail')
    fig.tight_layout(); save(fig, 'fig3_itinerary_complexity')

# ---------------- Fig 4: discrepancy and equidistribution
def fig4():
    fig, ax = plt.subplots(1, 2, figsize=(8.6, 3.2))
    it, ab, T, Ts = regime_tail(2, 20000)
    tail = it[Ts:]
    C = np.cumsum([1 if c == 2 else 0 for c in tail]); n = np.arange(1, len(tail) + 1)
    dev = C - n * th
    ax[0].plot(n[:400], dev[:400], lw=.6, color='k')
    f0 = ab[Ts][0] * LN2 - ab[Ts][1] * LN3; z0 = float((f0 + A) / L)
    ax[0].axhline(z0, color=C2c, ls='--', lw=.8); ax[0].axhline(z0 - 1, color=C3c, ls='--', lw=.8)
    ax[0].text(398, z0 + .03, r'$z$', ha='right', color=C2c); ax[0].text(398, z0 - 1 - .12, r'$z-1$', ha='right', color=C3c)
    ax[0].set_xlabel('$n$'); ax[0].set_ylabel(r'$C_2(n)-n\theta$'); ax[0].set_title('(a) discrepancy stays in $(z-1,z]$')
    zs = [(ab[i][0] * LN2F - ab[i][1] * LN3F + Af) / Lf for i in range(Ts, Ts + 20000)]
    ax[1].hist(zs, bins=40, range=(0, 1), color=GR, edgecolor='w'); ax[1].axhline(len(zs) / 40, color='k', lw=.7)
    ax[1].set_xlabel('$z_j$'); ax[1].set_ylabel('count'); ax[1].set_title('(b) equidistribution of $z_j$ (20000 steps)')
    fig.tight_layout(); save(fig, 'fig4_discrepancy')

# ---------------- Fig 5: growth
def fig5():
    fig, ax = plt.subplots(1, 2, figsize=(8.6, 3.2))
    it, ab, T, Ts = regime_tail(2, 3000)
    lg = [0.0]
    x = 2; lgx = math.log2(2)
    lgs = [lgx]
    for p in it:
        lgx += math.log2(4.5) if p == 2 else math.log2(16 / 3)   # valid for 2/3 fires; itinerary of x0=2 has no other prime
        lgs.append(lgx)
    n = np.arange(len(lgs)); rate = float(THETA * mlog(mpf(9) / 2, 2) + (1 - THETA) * mlog(mpf(16) / 3, 2))
    ax[0].plot(n[:300], np.array(lgs[:300]), color='k', lw=.8, label=r'$\log_2x_n$'); ax[0].plot(n[:300], 1 + rate * n[:300], color=C2c, ls='--', lw=.8, label=f'$1+{rate:.4f}\\,n$')
    ax[0].set_xlabel('$n$'); ax[0].set_ylabel('bits'); ax[0].legend(frameon=False); ax[0].set_title('(a) logarithmic growth, $x_0=2$')
    res = np.array(lgs) - (1 + rate * n)
    ax[1].plot(n[:300], res[:300], lw=.8, color='k'); ax[1].set_xlabel('$n$'); ax[1].set_ylabel(r'$\log_2x_n-1-\rho n$'); ax[1].set_title(r'(b) residual is bounded: $\rho=2.2747033$')
    fig.tight_layout(); save(fig, 'fig5_growth')

# ---------------- Fig 6: renewal
def fig6():
    fig, ax = plt.subplots(1, 3, figsize=(10.4, 3.2))
    for x0, col in [(41, C2c), (42, C3c), (43, 'k')]:
        Ns, ss, tot = V.logcap_run(x0, 300)
        ax[0].plot(ss, lw=.8, color=col, label=f'$x_0={x0}$')
        ax[1].plot(Ns, lw=.6, color=col)
    it, st = run_prime_fire(41, r_maxpp, 300)
    ax[0].plot([len(e) for e in st[1:]], color=GR, lw=1.2, ls='--', label='MAXPP, $x_0=41$')
    ax[0].set_xlabel('step $n$'); ax[0].set_ylabel(r'$|\mathrm{supp}(x_n)|$'); ax[0].legend(frameon=False, fontsize=7); ax[0].set_title('(a) prime support')
    ax[1].set_yscale('log'); ax[1].set_xlabel('step $n$'); ax[1].set_ylabel('branch value $N_n$'); ax[1].set_title('(b) log-cap rule: branch values')
    S = json.load(open(os.path.join(DATA, 'stormer_tables.json')))
    for (key, col) in zip(S, [C2c, C3c, 'k', GR]):
        v = S[key]; ax[2].plot(range(1, len(v) + 1), v, 'o-', ms=2.5, lw=.6, color=col, label=key.replace('[', '$\\{').replace(']', '\\}$'))
    ax[2].set_yscale('log'); ax[2].set_xlabel('index'); ax[2].set_ylabel('$N$ with $N,N+1$ $S$-smooth'); ax[2].legend(frameon=False, fontsize=6.5); ax[2].set_title("(c) St\u00f8rmer: finitely many")
    fig.tight_layout(); save(fig, 'fig6_renewal')

# ---------------- Fig 7: transients
def fig7():
    xs = list(range(2, 3001)); Ts = []; Tt = []
    for x0 in xs:
        it, ab, T = maxpp_full(x0, 80)
        Ts.append(T)
        a, b = ab[T]; j = T
        while not (-Af <= a * LN2F - b * LN3F < Bf):
            a, b = (a - 1, b + 2) if a * LN2F - b * LN3F > 0 else (a + 4, b - 1); j += 1
        Tt.append(j)
    fig, ax = plt.subplots(1, 2, figsize=(8.6, 3.0))
    ax[0].plot(xs, Ts, '.', ms=1.5, color='k'); ax[0].set_xlabel('$x_0$'); ax[0].set_ylabel('index of the last fire of a prime $\\geq5$'); ax[0].set_title('(a) transient before the two-counter regime')
    ax[1].hist(Tt, bins=range(0, max(Tt) + 2), color=GR, edgecolor='w'); ax[1].set_xlabel('entry index $T^*$'); ax[1].set_ylabel('number of starts'); ax[1].set_title('(b) entry into the rotation regime, $2\\leq x_0\\leq3000$')
    fig.tight_layout(); save(fig, 'fig7_transients')
    return max(Ts), max(Tt)

# ---------------- Fig 8: ORDER
def fig8():
    D = json.load(open(os.path.join(DATA, 'order_blocks.json')))
    counts = {int(k): v for k, v in D['counts'].items()}
    fig, ax = plt.subplots(1, 2, figsize=(8.8, 3.3))
    u = [V.u_obs(m) for m in range(2, 202)]
    for i, c in enumerate(u):
        ax[0].add_patch(plt.Rectangle((i % 100, -(i // 100)), .9, .8, color='k' if c else 'w', ec=GR, lw=.3))
    ax[0].set_xlim(0, 100); ax[0].set_ylim(-2, 1); ax[0].axis('off'); ax[0].set_title('(a) $u(m)$ for $m=2,\\dots,201$ (black: exponents unequal)')
    ks = np.array(sorted(counts)); ax[1].semilogy(ks, [counts[k] for k in ks], 'o-', ms=3, color='k', label=f'$p_u(k)$, $m\\leq{D["Nmax"]/1e6:.0f}\\cdot10^6$')
    ax[1].semilogy(ks, 2.0 ** ks, color=GR, ls=':', label='$2^k$'); ax[1].semilogy(ks, [2.0 ** math.ceil(2 * k / math.pi ** 2) for k in ks], color=C3c, ls='--', label=r'$2^{\lceil2k/\pi^2\rceil}$ (proved)')
    ax[1].set_xlabel('$k$'); ax[1].legend(frameon=False, fontsize=7); ax[1].set_title('(b) block counts of $u$ along consecutive integers')
    fig.tight_layout(); save(fig, 'fig8_order')

if __name__ == '__main__':
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); mx = fig7(); fig8()
    json.dump({'max_last_prime_ge5_fire_x0_le_3000': mx[0], 'max_entry_index_x0_le_3000': mx[1]}, open(os.path.join(DATA, 'transient_stats.json'), 'w'))
    print('figures ok', mx)
