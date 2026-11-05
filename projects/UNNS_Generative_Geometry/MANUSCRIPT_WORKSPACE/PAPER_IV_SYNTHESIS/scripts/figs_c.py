import sys, itertools; sys.path.insert(0, '.')
from figlib4 import *
import hist, eng3, trans3
from fractions import Fraction as Fr
# ---------------- Fig 17 same local inventory, different attachment
cases = [([12, 35], [44, 45]), ([33, 280], [14, 20])]
fig, axs = plt.subplots(2, 2, figsize=(W, 3.5))
for j, (D, N) in enumerate(cases):
    for i, DD in enumerate((D, D+N)):
        ax = axs[i][j]; ax.set_aspect("equal"); ax.axis("off")
        K = eng3.complex_of(DD); draw_complex(ax, DD, K, scale=1.0, r=0.2, fs=5.2, new_v=N if i else (), new_e=[e for e in K['E'] if (e[0] in N or e[1] in N)] if i else ())
        ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.45, 1.45)
        f = [len(c) for c in eng3.cellsets(K)]
        ax.set_title(f"{'$D=$' if i==0 else '$D\\cup N$, $N=$'}{DD if i==0 else N}: $f={tuple(f)}$, $\\beta={betti_str(eng3.bettiD(DD))}$", fontsize=5.8)
fig.text(0.5, 0.0, "both columns: $f=(2,0,0)\\to(4,3,0)$, nothing lost, 2 new vertices and 3 new edges; $\\Delta\\beta=(-1,0,0)$ versus $(0,+1,0)$ (SIV-P7)", ha="center", fontsize=6)
save(fig, "fig17_local_inventory")
# ---------------- Fig 18 tower pair
res = json.load(open("../results/c4_pair.json"))
fig, axs = plt.subplots(1, 2, figsize=(W, 2.6), sharex=True)
for S0, st, c in (("126", "-", SRC), ("3094", "--", LOST)):
    seq = res[S0]['seq']
    ks = [s['k'] for s in seq]
    for idx, mk in ((1, "o"), (2, "s"), (3, "^")):
        v = [(s['b'][idx] if idx < len(s['b']) else 0) for s in seq]
        axs[1].plot(ks, v, ls=st, marker=mk, ms=2.6, lw=0.9, c=c, label=f"$S_0={S0}$, $\\beta_{idx}$" if idx == 1 else None)
    axs[0].plot(ks, [math.log2(int(S0)*2**k) for k in ks], ls=st, c=c, lw=1.2, label=f"$\\log_2 L_k$, $S_0={S0}$")
axs[0].set_title("$L_k=S_02^k,\\ G=5$, $C^3(x)=4x$ (12 periods)", fontsize=6.4); axs[0].set_xlabel("$k$"); axs[0].legend(frameon=False, fontsize=5.8); axs[0].grid(alpha=0.3, lw=0.4)
axs[1].set_title("$\\beta_1,\\beta_2,\\beta_3$ of $K(D(x_k))$ ($k=0..14$)", fontsize=6.4); axs[1].set_xlabel("$k$"); axs[1].legend(frameon=False, fontsize=5.8); axs[1].grid(alpha=0.3, lw=0.4)
fig.text(0.5, -0.02, "finite-exact: $k\\leq14$ (Betti), 12 periods (orbit law); equal scaling data, unequal topology (SIV-P8). markers o, s, ^ = beta1, beta2, beta3", ha="center", fontsize=5.8)
save(fig, "fig18_scaling_vs_topology")
# ---------------- Fig 19 five levels
fig, ax = newfig(3.4, (0, 12.4, 0, 6.8))
Lv = [("L1", "numerical ratio", "$C^3=T_1=4x$ on the towers; $R(N)\\in\\mathbf{Z}$ iff $N=1$; coincidences classified (Paper III R3T7)", 'est'),
      ("L2", "occurrence information", "$D(x)\\subseteq D(Cx)$ and ancestor translation on integers (SIV-P9c)", 'fact'),
      ("L3", "event records: restricted", "equal event records on the rigid domain and for listed pairs (Paper III B2T10, R3T7)", 'fact'),
      ("L3", "event records: general", "no general map between history and collective event records known (O3)", 'open'),
      ("L4", "geometric structures", "integer endpoints: $K(D(t))=K_{\\rm move}(t)$ (B2T1); versus history complexes: obstructed (SIV-P5)", 'obs'),
      ("L5", "intertwining: identity", "$\\Phi=\\mathrm{id}$ excluded: $C(x)/x\\leq2<4\\leq T_N(x)/x$; snapshot $C^3=T_1$ is no conjugacy", 'obs'),
      ("L5", "intertwining: general", "a non-identity $\\Phi$ with $\\Phi C=T\\Phi$ is neither excluded nor constructed (O3)", 'open')]
for i, (a, b, c, s) in enumerate(Lv):
    y = 5.85 - i*0.88
    mbox(ax, 0.1, y-0.34, 1.0, 0.68, a, "space", 7)
    mbox(ax, 1.3, y-0.34, 2.4, 0.68, b, "obj", 5.2)
    sarrow(ax, (3.7, y), (4.4, y), s)
    mbox(ax, 4.4, y-0.38, 7.9, 0.76, c, "open" if s in ('open', 'obs') else "result", 5.1)
legend5(ax, 0.1, 0.0, dy=0.0) if False else None
ax.text(0.1, 6.55, "levels of correspondence; arrow style = status", fontsize=6.2)
save(fig, "fig19_correspondence_levels")
# ---------------- Fig 20 factorization diagram
fig, ax = newfig(3.3, (0, 12.4, -0.7, 6.2))
bx = [("histories\n$(m_0;w)$", 0.2), ("swap class\n$[w]$", 2.6), ("content $c$\n(fixed $m_0$)", 5.0), ("endpoint $t$", 7.4), ("$D(t)$", 9.8)]
for t, x in bx: mbox(ax, x, 4.2, 2.0, 1.2, t, "obj", 6.4)
for i in range(4): sarrow(ax, (bx[i][1]+2.0, 4.8), (bx[i+1][1], 4.8), 'fact' if i < 4 else 'est')
mbox(ax, 9.8, 2.2, 2.4, 1.0, "$K(D(t))$ = $K_{\\rm move}(t)$", "obj", 6.4); sarrow(ax, (11.0, 4.2), (11.0, 3.2), 'fact', "Thm. R3T1a", off=(0.9, 0))
mbox(ax, 9.8, 0.3, 2.4, 1.0, "$\\beta(K(D(t)))$", "obj", 6.4); sarrow(ax, (11.0, 2.2), (11.0, 1.3), 'est')
mbox(ax, 4.6, 2.2, 3.6, 1.0, "swap-class count, history count", "open", 6.2)
sarrow(ax, (9.8, 4.5), (8.2, 3.0), 'obs', "no factorization", off=(0.0, 0.25))
mbox(ax, 0.2, 2.2, 3.8, 1.0, "$\\mathrm{Gr}_q(x)$ (primitive system)", "open", 6.2)
sarrow(ax, (9.8, 4.2), (4.0, 2.7), 'obs', "Thm. R3T1(i)", off=(-1.1, 0.5), rad=0.0)
mbox(ax, 0.2, 0.3, 4.6, 1.0, "integers: $\\max D$ recovers the record (B2T1)", "result", 6.0)
ax.text(0.2, -0.45, "domain: Hist$(m_0)$ for fixed $m_0$, or $t\\in\\mathbf{Z}$ (SIV-P1, P2); green = proved factorization, red = proved obstruction", fontsize=5.8)
save(fig, "fig20_factorization_D")


# ---------------- Fig 21 global diagram (v0.2 layout: no label crosses an arrow)
fig, ax = newfig(7.6, (0, 12.4, -2.0, 10.2), w=W+0.6)
cx = [0.2, 2.75, 5.3, 7.85, 10.4]; bw, bh = 1.85, 0.95
def B(c, y, t, k="obj", fs=5.9): mbox(ax, cx[c], y, bw, bh, t, k, fs); return (cx[c]+bw/2, y+bh/2)
R1, R2, R3, R4, R5 = 8.6, 6.2, 3.3, 1.2, -0.9
ax.text(0.2, 9.95, "GENERATIVE SIDE (SELECT-II): histories and integers", fontsize=6.4, fontweight="bold")
H = B(0, R1, "histories\n$(m_0;w)$", "space"); Cl = B(1, R1, "swap class"); Ct = B(2, R1, "content $c$"); E = B(3, R1, "endpoint $t$"); Dt = B(4, R1, "$D(t)$", "space")
for a, b in ((H, Cl), (Cl, Ct), (Ct, E), (E, Dt)): sarrow(ax, (a[0]+bw/2, a[1]), (b[0]-bw/2, b[1]), 'fact')
RC = B(0, R2, "route complex\nof $\\mathrm{Hist}(m_0,t)$", "obj"); AN = B(1, R2, "#histories,\n#classes", "obj"); KD = B(2, R2, "$K(D(t))$\n$=K_{\\rm move}(t)$"); BE = B(3, R2, "$\\beta(K(D(t)))$")
sarrow(ax, (H[0], R1), (RC[0], R2+bh), 'est', "def.", off=(-0.4, 0))
sarrow(ax, (Dt[0]-0.5, R1), (KD[0]+0.5, R2+bh), 'fact', "R3T1a", off=(0.2, 0.28))
sarrow(ax, (KD[0]+bw/2, KD[1]), (BE[0]-bw/2, BE[1]), 'est')
sarrow(ax, (KD[0]-bw/2, KD[1]), (AN[0]+bw/2, AN[1]), 'obs', "")
ax.text((KD[0]+AN[0])/2, KD[1]+0.62, "SIV-P5", fontsize=5.6, ha="center", color=LOST)
sarrow(ax, (KD[0]-0.3, R2), (RC[0]+0.5, R2), 'open', "ancestry from richer invariants (O2)", rad=0.28, off=(0, -0.62), fs=5.6)
ax.text(0.2, 5.05, "COLLECTIVE SIDE (FIELD-I): rationals and evolution", fontsize=6.4, fontweight="bold")
X = B(0, R3, "state $x=a/b$", "space"); Dx = B(1, R3, "$D(x)$", "space"); Km = B(2, R3, "$K_{\\rm move}(x)$"); Gr = B(3, R3, "$\\mathrm{Gr}_q(x)$\n(primitive system)"); Gc = B(4, R3, "$\\mathrm{Gr}_q(Cx)$")
sarrow(ax, (X[0]+bw/2, X[1]), (Dx[0]-bw/2, Dx[1]), 'est'); sarrow(ax, (Dx[0]+bw/2, Dx[1]), (Km[0]-bw/2, Km[1]), 'fact', "R3T1a", off=(0, 0.62))
sarrow(ax, (KD[0]+0.6, R2), (Km[0]+0.6, R3+bh), 'est', "$t\\in\\mathbf{Z}$: $b=1$", off=(0.95, 0.35))
sarrow(ax, (Dx[0], R3+bh), (Gr[0]-0.2, R3+bh), 'obs', "", rad=-0.30)
ax.text(Dx[0]+0.6, R3+bh+0.62, "R3T1(i)", fontsize=5.6, ha="center", color=LOST)
sarrow(ax, (Gr[0]+bw/2, Gr[1]), (Gc[0]-bw/2, Gc[1]), 'open', "", off=(0, 0.2))
ax.text((Gr[0]+Gc[0])/2+bw/2-0.0, Gr[1]+0.62, "(O7)", fontsize=5.6, ha="center", color="#6b7780")
Xc = B(0, R4, "$C(x)$", "space"); Dc = B(1, R4, "$D(Cx)$", "space"); Kc = B(2, R4, "$K_{\\rm move}(Cx)$"); Tr = B(3, R4, "ancestor translation (P9c):\nconstruction from $(x,C(x))$,\nincrement $L^2/G$", "result")
sarrow(ax, (X[0], R3), (Xc[0], R4+bh), 'est')
sarrow(ax, (Dx[0], R3), (Dc[0], R4+bh), 'est', "$\\subseteq$ (Lemma M)", off=(0.75, 0))
sarrow(ax, (Km[0], R3), (Kc[0], R4+bh), 'obs', "no inclusion:\nedges can die (P6c)", off=(1.0, 0), fs=5.2)
sarrow(ax, (Dc[0]+bw/2, Dc[1]), (Kc[0]-bw/2, Kc[1]), 'fact')
Tn = B(0, R5, "$T_N(x)$\n(SELECT-II edge)", "space"); C3 = B(1, R5, "$C^3(x)=4x$\n(towers)", "obj")
sarrow(ax, (Xc[0]-0.5, R4), (Tn[0]-0.5, R5+bh), 'obs', "$C\\neq T_N$\n(identity only)", off=(-0.95, 0), fs=5.2)
sarrow(ax, (Xc[0]+0.5, R4), (Tn[0]+0.5, R5+bh), 'open', "general $\\Phi$ (O3)", off=(0.85, 0), fs=5.2)
sarrow(ax, (Tn[0]+bw/2, Tn[1]), (C3[0]-bw/2, C3[1]), 'interp', "")
ax.text((Tn[0]+C3[0])/2+bw/2, Tn[1]+0.55, "ratio 4", fontsize=5.6, ha="center", color=WIT)
legend5(ax, 8.4, 0.35, dy=0.38, L=0.55, fs=5.5)
ax.text(0.2, -1.95, "(On) = open problem n of Section 16. No square is claimed to commute; no arrow between successive complexes is an inclusion.", fontsize=5.6)
save(fig, "fig21_global_diagram")
# ---------------- Fig 22 conclusions and open obligations
fig, ax = newfig(3.7, (0, 12.4, 0, 7.0))
mbox(ax, 0.1, 0.2, 6.0, 6.2, "", "result"); mbox(ax, 6.4, 0.2, 5.9, 6.2, "", "open")
ax.text(3.1, 6.1, "established (Papers I--III; SIV-P1 to P9)", ha="center", fontsize=7, fontweight="bold")
ax.text(9.35, 6.1, "open construction obligations", ha="center", fontsize=7, fontweight="bold")
Es = ["endpoint and occurrence projections factor (P1, P2)", "realised set monotone; primitive status not (P3)", "swap classes: arithmetic, non-monotone (P4)", "endpoint geometry misses ancestry (P5)",
      "persistence hierarchy $D\\supseteq$ components $\\supseteq$ edges (P6)", "local inventory insufficient for $\\Delta\\beta$ (P7)", "scaling data insufficient for $\\beta$ (P8)", "levels L1-L5 assembled (P9)"]
Os = ["O1  classify history complexes in general", "O2  ancestry from richer invariants", "O3  maps history geometry $\\leftrightarrow$ occurrence geometry", "O4  predict $\\Delta\\beta_{\\geq2}$ without full target",
      "O5  onset bounds and Betti laws for towers", "O6  reachability of activation families", "O7  transitions of dormant primitive systems", "O8  compatibility of arithmetic guards"]
for i, (e, o) in enumerate(zip(Es, Os)):
    y = 5.4 - i*0.68
    ax.text(0.3, y, "\u2022 "+e, fontsize=6.0, va="center"); ax.text(6.6, y, o, fontsize=6.0, va="center")
tag(ax, "each open item is stated in Section 16 with its nearest proved theorem and missing obligation")
save(fig, "fig22_conclusions_open")
print("figs_c done")
