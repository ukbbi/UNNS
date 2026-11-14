#!/usr/bin/env python3
"""Figure generator for GIG_MANUSCRIPT_v002. Every diagram that depicts a
mathematical object is drawn from an exact construction computed here (verify/gigmini.py);
schematics and bar charts of registered numbers are labelled as such in the captions."""
import sys, os, json, math, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "verify"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch, Circle, Rectangle, FancyBboxPatch
import numpy as np
from gigmini import *
plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.size": 8, "axes.linewidth": 0.6,
                     "font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})
C = {"ink": "#222222", "gray": "#b8b8b8", "light": "#e6e6e6", "blue": "#1f5fa8", "red": "#c0392b", "green": "#2e7d32", "orange": "#d98e04", "violet": "#6a4c93"}
def save(fig, name): fig.savefig(os.path.join(HERE, name), bbox_inches="tight"); plt.close(fig)

# ---------------- Figure 1: ancestry of 72 and ambiguity growth ----------------
def fig1():
    fig = plt.figure(figsize=(6.6, 2.7))
    ax = fig.add_axes([0.0, 0.0, 0.58, 1]); ax.axis("off"); ax.set_xlim(0, 6.2); ax.set_ylim(-0.3, 4.3)
    pos = {"1": (0.3, 3.2), "3": (0.3, 1.5), "10": (0.3, 0.3), "4": (1.9, 3.2), "16": (3.5, 3.6), "18": (3.5, 2.5), "72": (5.5, 1.8)}
    pos["3b"] = (1.9, 1.5)
    def node(k, label, sq=False):
        x, y = pos[k]
        ax.add_patch(FancyBboxPatch((x - 0.3, y - 0.2), 0.6, 0.4, boxstyle="round,pad=0.02", fc="white" if not sq else C["light"], ec=C["ink"], lw=0.8))
        ax.text(x, y, label, ha="center", va="center", fontsize=8)
    for k, l in [("1", "1"), ("3", "3"), ("10", "10")]: node(k, l, sq=True)
    for k, l in [("4", "4"), ("16", "16"), ("18", "18"), ("72", "72")]: node(k, l)
    def arrow(a, b, lab, col, off=(0, 0.13), rad=0.0):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.add_patch(FancyArrowPatch((x1 + 0.3, y1), (x2 - 0.3, y2), arrowstyle="-|>", mutation_scale=7, lw=1.1, color=col, connectionstyle=f"arc3,rad={rad}"))
        ax.text((x1 + x2) / 2 + off[0], (y1 + y2) / 2 + off[1], lab, color=col, fontsize=7.5, ha="center")
    arrow("1", "4", "1", C["blue"]); arrow("4", "16", "1", C["blue"], off=(-0.05, 0.2)); arrow("4", "18", "2", C["orange"], off=(0.25, -0.05))
    arrow("16", "72", "2", C["orange"], off=(0.2, 0.18)); arrow("18", "72", "1", C["blue"], off=(0.25, -0.2))
    arrow("3", "16", "3", C["green"], off=(0, 0.2), rad=0.0); arrow("10", "72", "5", C["violet"], off=(0, -0.2), rad=-0.1)
    ax.text(0.3, 3.72, "sources", ha="center", fontsize=7, color=C["ink"]); ax.text(5.5, 2.35, "endpoint", ha="center", fontsize=7)
    ax.text(3.2, -0.25, "classes: {(1;1,1,2),(1;1,2,1)} swap-connected;\n(3;3,2) and (10;5) isolated", ha="center", fontsize=6.5)
    ax.text(0.0, 4.25, "(a)", fontweight="bold", fontsize=8)
    ax2 = fig.add_axes([0.66, 0.2, 0.33, 0.68])
    cnts = [4, 100, 3601, 194864, 14177856, 1258011667, 127958272791, 14628387999697, 1831257259071051, 247547117576968617]
    r = np.arange(1, 11)
    A = [math.log2(c) for c in cnts]; lb = [math.log2(math.comb(2 * k, k)) for k in r]
    ax2.plot(r, A, "o-", color=C["blue"], ms=3, lw=1, label=r"$\log_2|F_{72^r}|$")
    ax2.plot(r, lb, "s--", color=C["red"], ms=3, lw=1, label=r"$\log_2\binom{2r}{r}$")
    ax2.set_xlabel(r"$r$"); ax2.set_ylabel("bits"); ax2.legend(frameon=False, fontsize=6.5, loc="upper left")
    ax2.set_title("(b) ambiguity of $72^r$", fontsize=8, loc="left")
    save(fig, "fig_ancestry.pdf")

# ---------------- Figure 2: legal-swap geometry (P_4 with an admissible subset; local cells) ----------------
def perm_xyz(p):  # 3D coordinates of permutohedron vertex (inverse-permutation convention), orthonormal basis of sum-zero plane
    k = len(p); pos = [0] * k
    for i, v in enumerate(p): pos[v] = i + 1
    v = np.array(pos, float) - (k + 1) / 2
    B = np.array([[1, -1, 0, 0], [1, 1, -2, 0], [1, 1, 1, -3]], float)
    B = B / np.linalg.norm(B, axis=1)[:, None]
    return B @ v
def fig2():
    lab, m = (2, 3, 14, 15), 210
    A = admissible_perms(lab, m); k = 4
    allp = list(permutations(range(k)))
    R = np.array([[0.80, -0.55, 0.25], [0.45, 0.82, 0.35], [-0.38, -0.15, 0.91]])
    R = np.linalg.qr(np.random.RandomState(3).randn(3, 3))[0]
    # choose a pleasant viewing rotation
    th, ph = 0.55, 0.45
    Rz = np.array([[math.cos(th), -math.sin(th), 0], [math.sin(th), math.cos(th), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, math.cos(ph), -math.sin(ph)], [0, math.sin(ph), math.cos(ph)]])
    xy = {p: (Rx @ Rz @ perm_xyz(p))[:2] for p in allp}
    depth = {p: (Rx @ Rz @ perm_xyz(p))[2] for p in allp}
    fig = plt.figure(figsize=(6.6, 2.9))
    ax = fig.add_axes([0.0, 0.0, 0.5, 1]); ax.axis("off"); ax.set_aspect("equal")
    # faces of K_A
    faces = complex_from_vertex_set(k, A)
    for F in faces:
        if len(F) == k - 2:
            V = face_vertices(F)
            P = np.array([xy[tuple(v)] for v in V])
            c = P.mean(0); order = np.argsort([math.atan2(q[1] - c[1], q[0] - c[0]) for q in P])
            ax.add_patch(Polygon(P[order], closed=True, fc=C["blue"], alpha=0.22, ec="none"))
    for p in allp:
        for i in range(k - 1):
            q = p[:i] + (p[i + 1], p[i]) + p[i + 2:]
            if p < q:
                inA = p in A and q in A
                ax.plot([xy[p][0], xy[q][0]], [xy[p][1], xy[q][1]], color=C["ink"] if inA else C["gray"], lw=1.3 if inA else 0.5, zorder=2 if inA else 1, alpha=1 if inA else 0.8)
    for p in allp:
        ax.scatter(*xy[p], s=14 if p in A else 7, color=C["ink"] if p in A else "white", edgecolor=C["ink"] if p in A else C["gray"], lw=0.6, zorder=3)
    ax.set_title("(a) $P_4$ and the admissible set of $\\{2,3,14,15\\}$ at source $210$\n16 of 24 vertices; $\\beta=(1,1,0,0)$", fontsize=7.5, loc="left")
    # (b) local cells: square, braid hexagon, cube with Petrie 6-cycle
    ax2 = fig.add_axes([0.52, 0.0, 0.48, 1]); ax2.axis("off"); ax2.set_aspect("equal"); ax2.set_xlim(0, 10); ax2.set_ylim(0, 5)
    def poly(cx, cy, n, r, rot=0):
        return [(cx + r * math.cos(rot + 2 * math.pi * i / n), cy + r * math.sin(rot + 2 * math.pi * i / n)) for i in range(n)]
    sq = poly(1.4, 3.3, 4, 0.9, math.pi / 4); hx = poly(4.2, 3.3, 6, 1.0)
    for pts, nm, col in [(sq, "square\n(commuting swaps)", C["blue"]), (hx, "hexagon\n(braid relation)", C["orange"])]:
        ax2.add_patch(Polygon(pts, closed=True, fc=col, alpha=0.2, ec=C["ink"], lw=1))
        for q in pts: ax2.scatter(*q, s=10, color=C["ink"], zorder=3)
    ax2.text(1.4, 2.1, "square\n(commuting swaps)", ha="center", va="top", fontsize=6.8); ax2.text(4.2, 2.1, "hexagon\n(braid relation)", ha="center", va="top", fontsize=6.8)
    # cube with Petrie hexagon
    def proj(v): x, y, z = v; return (6.9 + x * 1.5 + z * 0.8, 1.8 + y * 1.5 + z * 0.7)
    verts = list(itertools.product([0, 1], repeat=3))
    for a in verts:
        for b in verts:
            if sum(abs(i - j) for i, j in zip(a, b)) == 1 and a < b:
                ax2.plot(*zip(proj(a), proj(b)), color=C["gray"], lw=0.8)
    pet = [(0, 0, 1), (1, 0, 1), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)]
    for a, b in zip(pet[:-1], pet[1:]): ax2.plot(*zip(proj(a), proj(b)), color=C["red"], lw=1.6)
    for v in verts: ax2.scatter(*proj(v), s=9, color=C["ink"], zorder=3)
    ax2.text(7.9, 2.0 + 0.0, "", fontsize=6)
    ax2.text(8.0, 1.6, "commuting cube $Q_3$ with a\nPetrie 6-cycle (never a slice\nof an arithmetic $A$)", ha="center", va="top", fontsize=6.3)
    ax2.set_title("(b) local cells of the permutohedral complex", fontsize=7.5, loc="left")
    save(fig, "fig_swap_geometry.pdf")

# ---------------- Figure 3: divisibility activation and survival ----------------
def fig3():
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.5), sharey=False)
    for ax, (nm, lab, m0, pr) in zip(axs, [("A", (2, 3, 4, 5, 8, 9), 288, (2, 3, 5)), ("B", (2, 3, 6, 7, 8, 9), 432, (2, 3, 7))]):
        cache = {}; xs, ys, sv = [], [], []
        for t in range(1, 61):
            m = m0 * t; Aset = frozenset(admissible_perms(lab, m))
            if Aset not in cache:
                f, b = betti_arith(lab, m); cache[Aset] = (len(Aset), b[2] if len(b) > 2 else 0)
            xs.append(t); ys.append(cache[Aset][0]); sv.append(cache[Aset][1] > 0)
        xs, ys, sv = np.array(xs), np.array(ys), np.array(sv)
        ax.scatter(xs[~sv], ys[~sv], s=9, color=C["gray"], label=r"$\beta_2=0$")
        ax.scatter(xs[sv], ys[sv], s=14, color=C["red"], label=r"$\beta_2=1$ (hole survives)")
        ax.set_xlabel(f"$t$   (source $m={m0}\\,t$)"); ax.set_ylabel("number of admissible histories $N$")
        ax.set_title(f"({'ab'[nm=='B']}) content {lab}", fontsize=7.5, loc="left")
        for p in pr: ax.axvline(p, color=C["blue"], lw=0.4, ls=":")
        ax.text(0.98, 0.96, "dotted lines: $t\\in\\{%s\\}$" % ",".join(map(str, pr)), transform=ax.transAxes, ha="right", va="top", fontsize=6.3, color=C["blue"])
        if nm == "A": ax.legend(frameon=False, fontsize=6.3, loc="center right")
    save(fig, "fig_activation_series.pdf")

# ---------------- Figure 5: equal history count, different topology ----------------
def graph_stats(k, A):
    adj = swap_graph(k, A)
    d = {w: len(adj[w]) for w in adj}
    def ball2(w):
        B = {w} | set(adj[w]) | {x for u in adj[w] for x in adj[u]}; return len(B)
    return adj, d, {w: ball2(w) for w in adj}
def swap_graph(k, A):
    A = set(A); adj = {p: [] for p in A}
    for p in A:
        for i in range(k - 1):
            q = p[:i] + (p[i + 1], p[i]) + p[i + 2:]
            if q in A: adj[p].append(q)
    return adj
def fig5():
    sysA = ((2, 4, 5, 9, 14, 15), 2520, 3780); sysB = ((2, 3, 4, 5, 8, 15), 480, 800)
    fig, axs = plt.subplots(1, 3, figsize=(6.6, 2.3), gridspec_kw={"width_ratios": [1.15, 1, 1]})
    res = {}
    for (lab, mp, mn) in (sysB, sysA):
        for m in (mp, mn):
            A = admissible_perms(lab, m); f, b = betti(6, complex_from_vertex_set(6, A))
            adj, d, b2 = graph_stats(6, A)
            h1 = {}; h2 = {}
            for w in adj: h1[d[w]] = h1.get(d[w], 0) + 1; h2[b2[w]] = h2.get(b2[w], 0) + 1
            res[(lab, m)] = dict(N=len(A), f=f, b=b, h1=h1, h2=h2, SB22=sum(v * v for v in b2.values()), E=f[1])
    json.dump({f"{k[0]}@{k[1]}": {kk: (vv if not isinstance(vv, dict) else {str(a): c for a, c in vv.items()}) for kk, vv in v.items()} for k, v in res.items()}, open(os.path.join(HERE, "fig5_data.json"), "w"), indent=1)
    ax = axs[0]
    P = res[(sysB[0], 480)]; Nn = res[(sysB[0], 800)]
    x = np.arange(5)
    ax.bar(x - 0.2, P["f"][:5], 0.4, color=C["red"], label=r"$m=480$, $\beta_2=1$"); ax.bar(x + 0.2, Nn["f"][:5], 0.4, color=C["blue"], label=r"$m=800$, $\beta_2=0$")
    ax.set_xticks(x); ax.set_xticklabels(["$f_0$", "$f_1$", "$f_2$", "$f_3$", "$f_4$"]); ax.set_yscale("log"); ax.set_ylim(5, 4000); ax.legend(frameon=False, fontsize=6.0, loc="upper right")
    ax.set_title("(a) $f$-vectors, content (2,3,4,5,8,15),\n$N=396$ for both", fontsize=7.2, loc="left")
    ax = axs[1]
    pr = res[(sysA[0], 2520)]; ng = res[(sysA[0], 3780)]
    keys = sorted(set(pr["h2"]) | set(ng["h2"]))
    xx = np.arange(len(keys))
    ax.bar(xx - 0.2, [pr["h2"].get(q, 0) for q in keys], 0.4, color=C["red"]); ax.bar(xx + 0.2, [ng["h2"].get(q, 0) for q in keys], 0.4, color=C["blue"])
    ax.set_xticks(xx); ax.set_xticklabels(keys, fontsize=6, rotation=90); ax.set_xlabel("radius-2 ball size $|B_2(w)|$", fontsize=7); ax.set_ylabel("vertices", fontsize=7)
    ax.set_title("(b) $m=2520$ vs $3780$: equal $N,h_1$,\ndifferent $h_2$", fontsize=7.2, loc="left")
    ax = axs[2]
    diff = [pr["h2"].get(q, 0) - ng["h2"].get(q, 0) for q in keys]
    ax.bar(xx, diff, 0.6, color=[C["red"] if q > 0 else C["blue"] for q in diff]); ax.axhline(0, color=C["ink"], lw=0.5)
    ax.set_xticks(xx); ax.set_xticklabels(keys, fontsize=6, rotation=90); ax.set_xlabel("$|B_2(w)|$", fontsize=7); ax.set_ylabel("difference in count", fontsize=7)
    ax.set_title("(c) difference of the two\nradius-2 histograms", fontsize=7.2, loc="left")
    fig.tight_layout(); save(fig, "fig_equal_N.pdf")
    return res

# ---------------- Figure 6: radius-dependent information recovery (registered values) ----------------
def fig6():
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.5))
    ax = axs[0]
    lab = ["none", "$N$", "$(N,h_1)$", "$(N,h_1,h_q)$", "$(N,h_1,h_2)$"]; vals = [1.0, 0.4552, 0.0126, 0.0016, 0.0]
    ax.bar(range(5), vals, color=[C["gray"], C["blue"], C["blue"], C["blue"], C["green"]])
    ax.set_xticks(range(5)); ax.set_xticklabels(lab, fontsize=6.5, rotation=20, ha="right"); ax.set_ylabel(r"residual $H(Y\,|\,O)$ in bits"); ax.set_yscale("symlog", linthresh=1e-3)
    ax.set_title("(a) in-sample, balanced ensemble\n(609,983 six-label systems)", fontsize=7.2, loc="left")
    ax = axs[1]
    names = ["$N$", "radius-1\nscalars", "radius-1\n+ squares", "all radius-2\nscalars", "$(Q,S_2)$", "exact\nlookup"]
    a = [0.31, 0.28, 0.44, 0.44, 0.29, -1.05]; b = [0.38, 0.52, 0.66, 0.68, 0.45, -1.19]
    x = np.arange(6)
    ax.bar(x - 0.2, a, 0.4, color=C["violet"], label="train $D$ → test $H_6$"); ax.bar(x + 0.2, b, 0.4, color=C["orange"], label="train $H_6$ → test $D$")
    ax.axhline(0, color=C["ink"], lw=0.5); ax.axhline(1, color=C["gray"], lw=0.5, ls=":")
    ax.set_xticks(x); ax.set_xticklabels(names, fontsize=6, rotation=0); ax.set_ylabel("bits gained about $Y$"); ax.legend(frameon=False, fontsize=6.2, loc="lower left")
    ax.set_title("(b) out-of-sample, balanced test ensemble", fontsize=7.2, loc="left")
    fig.tight_layout(); save(fig, "fig_recovery.pdf")

# ---------------- Figure 7 & 8: dead-set nerves and collapse cores ----------------
def dead_sets(k, A):
    byI = {}
    for p in permutations(range(k)):
        for I in prefix_sets(p): byI.setdefault(I, []).append(p)
    return sorted(I for I, L in byI.items() if all(p not in A for p in L))
def comparable(a, b): return (a & b) == a or (a & b) == b
def nerve_facets(k, D):
    full = (1 << k) - 1; fac = set()
    for z in range(1, full):
        Cz = frozenset(d for d in D if comparable(d, z))
        if Cz: fac.add(Cz)
    # keep only maximal
    fac = [f for f in fac if not any(f < g for g in fac)]
    return fac
def simplices_upto2(fac):
    S = set()
    for f in fac:
        f = sorted(f)
        for r in range(1, min(3, len(f)) + 1):
            for s in itertools.combinations(f, r): S.add(s)
    return S
def lab_of(I, lab):
    return "{" + ",".join(str(lab[r]) for r in range(len(lab)) if I >> r & 1) + "}"
def strong_collapse(fac):
    fac = [frozenset(f) for f in fac]
    changed = True
    while changed:
        changed = False
        V = sorted(set().union(*fac)) if fac else []
        for v in V:
            st = [f for f in fac if v in f]
            for w in V:
                if w != v and all(w in f for f in st):
                    fac = [f - {v} if v in f else f for f in fac]
                    fac = [f for f in fac if f]
                    fac = [f for f in fac if not any(f < g for g in fac)]
                    changed = True; break
            if changed: break
    return fac
def draw_nerve(ax, D, fac, lab, highlight=None, title=None, labels=True):
    n = len(D)
    ang = {d: 2 * math.pi * i / n + 0.3 for i, d in enumerate(D)}
    xy = {d: (math.cos(ang[d]), math.sin(ang[d])) for d in D}
    S = simplices_upto2(fac)
    for s in sorted(S, key=len):
        if len(s) == 3:
            ax.add_patch(Polygon([xy[d] for d in s], closed=True, fc=C["blue"], alpha=0.10, ec="none"))
    for s in S:
        if len(s) == 2: ax.plot([xy[s[0]][0], xy[s[1]][0]], [xy[s[0]][1], xy[s[1]][1]], color=C["ink"], lw=0.5, alpha=0.7)
    if highlight:
        hs = list(highlight)
        for a, b in itertools.combinations(hs, 2):
            ax.plot([xy[a][0], xy[b][0]], [xy[a][1], xy[b][1]], color=C["red"], lw=1.8)
    for d in D:
        ax.scatter(*xy[d], s=22, color=C["red"] if highlight and d in highlight else C["ink"], zorder=3)
        if labels:
            ax.text(xy[d][0] * 1.28, xy[d][1] * 1.22, lab_of(d, lab), ha="center", va="center", fontsize=5.8)
    ax.set_xlim(-1.75, 1.75); ax.set_ylim(-1.55, 1.55); ax.set_aspect("equal"); ax.axis("off")
    if title: ax.set_title(title, fontsize=7, loc="left")
def hollow_triangle(fac, D):
    S = simplices_upto2(fac); E = {s for s in S if len(s) == 2}; T = {s for s in S if len(s) == 3}
    for a, b, c in itertools.combinations(D, 3):
        if all(tuple(sorted(p)) in E for p in [(a, b), (a, c), (b, c)]) and tuple(sorted((a, b, c))) not in T: return (a, b, c)
    return None
def fig7():
    lab = (2, 4, 5, 9, 14, 15)
    fig, axs = plt.subplots(1, 3, figsize=(6.6, 2.45), gridspec_kw={"width_ratios": [1, 1, 1.0]})
    out = {}
    for ax, m, t in zip(axs[:2], (2520, 3780), ("(a) $m=2520$: $\\beta_2=1$", "(b) $m=3780$: $\\beta_2=0$")):
        A = admissible_perms(lab, m); D = dead_sets(6, A); fac = nerve_facets(6, D)
        hol = hollow_triangle(fac, D)
        draw_nerve(axs[0] if m == 2520 else axs[1], D, fac, lab, highlight=hol, title=t + "\ndead-set nerve $N[D_A]$")
        out[m] = dict(dead=[lab_of(d, lab) for d in D], hollow=[lab_of(d, lab) for d in hol] if hol else None)
    ax = axs[2]; ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    rows = [("history complex $K_A$", C["blue"], 8.2), ("forbidden complex $Y_A\\subset S^{4}$", C["orange"], 5.0), ("dead-set nerve $N[D_A]$", C["green"], 1.8)]
    for txt, col, y in rows:
        ax.add_patch(FancyBboxPatch((0.4, y), 9.0, 1.3, boxstyle="round,pad=0.05", fc="white", ec=col, lw=1.2)); ax.text(4.9, y + 0.65, txt, ha="center", va="center", fontsize=7)
    ax.add_patch(FancyArrowPatch((4.9, 8.2), (4.9, 6.45), arrowstyle="<|-|>", mutation_scale=7, lw=0.9, color=C["ink"])); ax.text(5.2, 7.3, "Alexander duality\n$\\tilde H_j(K)\\cong\\tilde H^{3-j}(Y)$", fontsize=6.2, va="center")
    ax.add_patch(FancyArrowPatch((4.9, 5.0), (4.9, 3.25), arrowstyle="<|-|>", mutation_scale=7, lw=0.9, color=C["ink"])); ax.text(5.2, 4.1, "nerve theorem\n$Y\\simeq N[D]$", fontsize=6.2, va="center")
    ax.text(4.9, 0.3, "$\\beta_2(K_A)=\\dim H_1(N[D_A])$", ha="center", fontsize=7.5, fontweight="bold")
    ax.set_title("(c) the chain of equivalences", fontsize=7, loc="left")
    save(fig, "fig_nerves.pdf")
    json.dump({str(k): v for k, v in out.items()}, open(os.path.join(HERE, "fig7_data.json"), "w"), indent=1)

def fig8():
    lab = (2, 3, 4, 5, 8, 15)
    fig = plt.figure(figsize=(6.6, 2.5))
    A = admissible_perms(lab, 480); D = dead_sets(6, A); fac = nerve_facets(6, D); core = strong_collapse(fac)
    axa = fig.add_axes([0.0, 0.05, 0.32, 0.85]); draw_nerve(axa, D, fac, lab, highlight=hollow_triangle(fac, D), title=f"(a) $N[D_A]$, $m=480$: {len(D)} dead sets", labels=False)
    Dc = sorted(set().union(*core)) if core else []
    axb = fig.add_axes([0.33, 0.05, 0.28, 0.85]); draw_nerve(axb, Dc, core, lab, highlight=Dc if len(Dc) == 3 else None, title=f"(b) strong-collapse core:\n{len(Dc)} vertices", labels=True)
    axc = fig.add_axes([0.70, 0.2, 0.29, 0.62])
    sizes = [3, 5, 6, 7, 8, 14, 19, 20, 21, 33]; cnt = [105, 23, 6, 1, 2, 5, 1, 3, 3, 2]
    axc.bar(range(len(sizes)), cnt, color=C["blue"]); axc.set_xticks(range(len(sizes))); axc.set_xticklabels(sizes, fontsize=6.5); axc.set_xlabel("core size (vertices)", fontsize=7); axc.set_ylabel("positive patterns", fontsize=7)
    axc.set_title("(c) cores of the 151 positive\ndead-set patterns", fontsize=7, loc="left")
    save(fig, "fig_core.pdf")
    json.dump({"dead": len(D), "core_vertices": len(Dc), "core": [[lab_of(d, lab) for d in sorted(f)] for f in core]}, open(os.path.join(HERE, "fig8_data.json"), "w"), indent=1)

# ---------------- Figure 9: pairwise vs triple-local constraints ----------------
def fig9():
    fig = plt.figure(figsize=(6.6, 2.4))
    ax = fig.add_axes([0.06, 0.2, 0.28, 0.65])
    k = 6; rng = np.random.RandomState(5)
    b2s = []; b1s = []
    import random as _r
    rnd = _r.Random(11)
    for _ in range(70):
        pr = rnd.choice([0.45, 0.6, 0.75, 0.85])
        arcs = {(x, y) for x in range(6) for y in range(6) if x != y and rnd.random() < pr}
        A = {p for p in permutations(range(6)) if all((p[i], p[i + 1]) in arcs for i in range(5))}
        if not A or len(A) == 720: continue
        f, b = betti(6, complex_from_vertex_set(6, A)); b = b + [0] * 6
        b1s.append(b[1]); b2s.append(b[2])
    ax.hist(b2s, bins=[-0.5, 0.5], color=C["blue"], rect=None) if False else None
    ax.bar([0, 1], [sum(1 for v in b1s if v == 0), sum(1 for v in b1s if v > 0)], color=C["blue"], width=0.6)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["$\\beta_1=0$", "$\\beta_1>0$"]); ax.set_ylabel("random pairwise systems")
    ax.set_title(f"(a) {len(b2s)} random pairwise\ngrammars: $\\max\\beta_2={max(b2s)}$", fontsize=7.2, loc="left")
    ax = fig.add_axes([0.42, 0.2, 0.22, 0.65])
    def hasc(p, trip): return any(p[i:i + 3] == trip for i in range(len(p) - 2))
    A3 = {p for p in permutations(range(6)) if not hasc(p, (1, 2, 0)) and not hasc(p, (5, 4, 3))}
    f3, b3 = betti(6, complex_from_vertex_set(6, A3))
    ax.bar(range(3), b3[:3], color=[C["gray"], C["orange"], C["red"]], width=0.6)
    for i, v in enumerate(b3[:3]): ax.text(i, v + 0.1, str(v), ha="center", fontsize=7)
    ax.set_xticks(range(3)); ax.set_xticklabels(["$\\beta_0$", "$\\beta_1$", "$\\beta_2$"]); ax.set_ylim(0, 6.2)
    ax.set_title(f"(b) two forbidden triples:\n$N={len(A3)}$", fontsize=7.2, loc="left")
    # (c) Mayer-Vietoris schematic from the exact component count of Z_1 cap Z_2
    ax = fig.add_axes([0.70, 0.05, 0.3, 0.85]); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.add_patch(Circle((3.6, 6.2), 3.0, fc=C["blue"], alpha=0.15, ec=C["blue"])); ax.add_patch(Circle((6.4, 6.2), 3.0, fc=C["orange"], alpha=0.15, ec=C["orange"]))
    ax.text(2.0, 9.0, "$Z_{(1,2,0)}$", fontsize=7, color=C["blue"]); ax.text(7.0, 9.0, "$Z_{(5,4,3)}$", fontsize=7, color=C["orange"])
    for i in range(6): ax.scatter(5.0 + 0.0, 3.6 + 0.0, s=0)
    for i, yy in enumerate(np.linspace(4.2, 8.2, 6)): ax.add_patch(Circle((5.0, yy), 0.22, fc=C["red"], ec="none"))
    ax.text(5.0, 1.8, "$Z_1\\cap Z_2$: 6 components\n$\\Rightarrow H_1(Y)\\cong\\mathrm{GF}(2)^{5}$", ha="center", fontsize=6.6)
    ax.set_title("(c) Mayer–Vietoris mechanism", fontsize=7.2, loc="left")
    save(fig, "fig_locality.pdf")


# ---------------- new figures for v002 ----------------
def vp(n, p):
    c = 0
    while n % p == 0: n //= p; c += 1
    return c
def mk(sx): return sum(1 << int(ch) for ch in sx)
def fig_thresholds():
    lab = (2, 3, 4, 5, 8, 9); primes = (2, 3, 5)
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.4), gridspec_kw={"width_ratios": [1.1, 1]})
    ax = axs[0]
    W = np.array([[vp(l, p) - 2 * vp(l + 1, p) for l in lab] for p in primes])
    lim = np.abs(W).max()
    ax.imshow(W, cmap="RdBu", vmin=-lim, vmax=lim, aspect="auto")
    ax.set_xticks(range(6)); ax.set_xticklabels([f"$r={r}$\n$c_r={lab[r]}$" for r in range(6)], fontsize=6.3)
    ax.set_yticks(range(3)); ax.set_yticklabels([f"$p={p}$" for p in primes], fontsize=7)
    for i in range(3):
        for j in range(6): ax.text(j, i, str(W[i, j]), ha="center", va="center", fontsize=7, color="white" if abs(W[i, j]) > 2 else C["ink"])
    ax.spines[:].set_visible(False)
    ax.set_title(r"(a) weights $\omega_p(r)=v_p(c_r)-2v_p(c_r+1)$", fontsize=7.2, loc="left")
    ax = axs[1]
    gates = [("$\\{024\\}$", ["024"]), ("$\\{15,125\\}$", ["15", "125"]), ("$\\{3\\}$", ["3"])]
    need = []
    for (nm, sets), p in zip(gates, primes):
        need.append(max(vp(Dmask(lab, mk(s)), p) for s in sets))
    have = [vp(288, p) for p in primes]
    x = np.arange(3)
    ax.bar(x - 0.2, have, 0.4, color=C["blue"], label=r"$v_p(288)$")
    ax.bar(x + 0.2, need, 0.4, color=C["red"], label="needed to open the gate")
    ax.set_xticks(x); ax.set_xticklabels([f"$p={p}$\ngate {g[0]}" for p, g in zip(primes, gates)], fontsize=6.5)
    ax.set_ylabel("exponent"); ax.legend(frameon=False, fontsize=6.3, loc="upper right")
    ax.set_title("(b) valuations of $288$ vs gate thresholds", fontsize=7.2, loc="left")
    save(fig, "fig_thresholds.pdf")
    return have, need

def fig_activation_cube():
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.9))
    out = {}
    for ax, (nm, lab, m0, pr) in zip(axs, [("A", (2, 3, 4, 5, 8, 9), 288, (2, 3, 5)), ("B", (2, 3, 6, 7, 8, 9), 432, (2, 3, 7))]):
        pos = {}
        for sub in itertools.product([0, 1], repeat=3):
            x, y, z = sub
            pos[sub] = (x * 2.2 + z * 1.0, y * 2.2 + z * 0.8)
        info = {}
        for sub in pos:
            t = 1
            for b, p in zip(sub, pr):
                if b: t *= p
            m = m0 * t; A = admissible_perms(lab, m); f, bb = betti_arith(lab, m)
            info[sub] = (len(A), (bb[2] if len(bb) > 2 else 0) > 0, t)
        out[nm] = {str(k): v for k, v in info.items()}
        for a in pos:
            for b in pos:
                if a < b and sum(abs(i - j) for i, j in zip(a, b)) == 1:
                    ax.plot(*zip(pos[a], pos[b]), color=C["gray"], lw=0.9, zorder=1)
        for sub, (N, sv, t) in info.items():
            ax.scatter(*pos[sub], s=420, color=C["red"] if sv else "white", edgecolor=C["ink"], lw=0.8, zorder=2)
            ax.text(pos[sub][0], pos[sub][1], str(N), ha="center", va="center", fontsize=6.3, color="white" if sv else C["ink"], zorder=3)
            ax.text(pos[sub][0], pos[sub][1] - 0.55, f"$t={t}$", ha="center", va="top", fontsize=5.8, color=C["blue"])
        ax.set_title(f"({'ab'[nm=='B']}) content {lab}, $m=m_0t$, $m_0={m0}$\naxes: divisibility of $t$ by {pr[0]}, {pr[1]}, {pr[2]}", fontsize=7, loc="left")
        ax.axis("off"); ax.set_aspect("equal"); ax.set_xlim(-0.8, 4.4); ax.set_ylim(-1.1, 3.8)
    save(fig, "fig_activation_cube.pdf")
    json.dump(out, open(os.path.join(HERE, "fig_cube_data.json"), "w"), indent=1)

def fig_lift_diagonal():
    k = 4; allp = list(permutations(range(k)))
    faces = [F for F in ordered_partitions(k) if len(F) == 2]
    first = tuple(sorted([1 << 3, 7]))  # ({3}|{0,1,2})
    firstF = (1 << 3, 7); lastF = (7, 1 << 3)
    def cen(F): return np.mean([perm_xyz(tuple(v)) for v in face_vertices(F)], axis=0)
    fig = plt.figure(figsize=(6.6, 3.0))
    for idx, (title, F0) in enumerate([("(a) view from the facet first$(c)$", firstF), ("(b) view from the facet last$(c)$", lastF)]):
        ax = fig.add_axes([0.02 + 0.5 * idx, 0.02, 0.46, 0.84]); ax.axis("off"); ax.set_aspect("equal")
        d0 = cen(F0); d0 = d0 / np.linalg.norm(d0)
        a = np.cross(d0, [0.3, 0.5, 0.8]); a /= np.linalg.norm(a); b = np.cross(d0, a)
        d = d0 + 0.75 * a + 0.35 * b; d = d / np.linalg.norm(d)
        a = np.cross(d, b); a /= np.linalg.norm(a); b = np.cross(d, a)
        proj = lambda v: (np.dot(v, a), np.dot(v, b))
        order = sorted(faces, key=lambda F: np.dot(cen(F), d))
        for F in order:
            c = cen(F)
            if np.dot(c, d) < -1e-9: continue
            P = np.array([proj(perm_xyz(tuple(v))) for v in face_vertices(F)])
            cc = P.mean(0); o = np.argsort([math.atan2(q[1] - cc[1], q[0] - cc[0]) for q in P])
            col = C["blue"] if F == firstF else (C["red"] if F == lastF else C["gray"])
            ax.add_patch(Polygon(P[o], closed=True, fc=col, alpha=0.55 if col != C["gray"] else 0.35, ec=C["ink"], lw=0.7))
        ax.set_title(title, fontsize=7.2, loc="left")
        ax.autoscale_view(); ax.set_xlim(-3.3, 3.3); ax.set_ylim(-3.3, 3.3)
    fig.text(0.5, 0.0, "blue: first$(c)$   red: last$(c)$   grey: $\\Lambda(z)$ (twelve facets)", ha="center", fontsize=7)
    save(fig, "fig_lift_diagonal.pdf")

def fig_duality():
    k = 3
    orders = [(0, 1, 2), (1, 0, 2), (1, 2, 0), (2, 1, 0), (2, 0, 1), (0, 2, 1)]
    A = set(orders[:4])
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.6))
    ang = [math.pi / 2 - 2 * math.pi * i / 6 for i in range(6)]
    ax = axs[0]; ax.axis("off"); ax.set_aspect("equal")
    xy = [(math.cos(a), math.sin(a)) for a in ang]
    for i in range(6):
        j = (i + 1) % 6; inA = orders[i] in A and orders[j] in A
        ax.plot([xy[i][0], xy[j][0]], [xy[i][1], xy[j][1]], color=C["blue"] if inA else C["gray"], lw=2.4 if inA else 0.8, ls="-" if inA else ":")
    for i, o in enumerate(orders):
        ax.scatter(*xy[i], s=60, color=C["blue"] if o in A else "white", edgecolor=C["ink"], zorder=3)
        ax.text(xy[i][0] * 1.28, xy[i][1] * 1.2, "".join(map(str, o)), ha="center", va="center", fontsize=7.5)
    ax.set_title("(a) $\\partial P_3$: vertices = orderings; $K_A$ in blue", fontsize=7.5, loc="left"); ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.5, 1.5)
    ax = axs[1]; ax.axis("off"); ax.set_aspect("equal")
    subs = ["{0}", "{0,1}", "{1}", "{1,2}", "{2}", "{0,2}"]
    # flag of ordering i joins subs[i] and subs[i+1]
    for i in range(6):
        j = (i + 1) % 6; miss = orders[i] not in A
        ax.plot([xy[i][0], xy[j][0]], [xy[i][1], xy[j][1]], color=C["red"] if miss else C["gray"], lw=2.4 if miss else 0.8, ls="-" if miss else ":")
        mx, my = (xy[i][0] + xy[j][0]) / 2, (xy[i][1] + xy[j][1]) / 2
        ax.text(mx * 1.25, my * 1.25, "".join(map(str, orders[i])), ha="center", va="center", fontsize=6.3, color=C["red"] if miss else C["gray"])
    for i, s in enumerate(subs):
        ax.scatter(*xy[i], s=40, color="white", edgecolor=C["ink"], zorder=3)
        ax.text(xy[i][0] * 1.32, xy[i][1] * 1.25, s, ha="center", va="center", fontsize=7)
    ax.set_title("(b) $T$: vertices = proper subsets, edges = flags; $Y_A$ in red", fontsize=7.5, loc="left"); ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.5, 1.5)
    save(fig, "fig_duality.pdf")

if __name__ == "__main__":
    for f in (fig1, fig2, fig3, fig5, fig6, fig7, fig8, fig9, fig_thresholds, fig_activation_cube, fig_lift_diagonal, fig_duality):
        f(); print("ok", f.__name__)
