"""Figures 12-15 (Sections 9 and 10)."""
from figlib import *
from lattice_cells import *
from figs_a import planar_holes, planar_polys
from fractions import Fraction as Fr
from itertools import product, combinations

def cells0(inlat, q):
    """Cells of the origin-allowed complex (corners may be 0)."""
    G = sorted(g for g in graver(inlat, q) if lexpos(g))
    F = set(fibre(inlat, q)) | {tuple(0 for _ in q)}
    out = {0: {(u, ()) for u in F}}
    for j in range(1, len(q)+1):
        S = set()
        for gens in combinations(G, j):
            if rank(gens) < j: continue
            for u in F:
                ok = all(add(u, tuple(sum(m*gg[i] for m, gg in zip(mask, gens)) for i in range(len(q)))) in F for mask in product((0, 1), repeat=j))
                if ok: S.add((u, gens))
        out[j] = S
    return out

def planar_geoms(C):
    from shapely.geometry import Polygon, LineString
    polys, lines = [], []
    for c in C.get(2, ()):
        u, (g, h) = c; polys.append([u, add(u, g), add(add(u, g), h), add(u, h)])
    for c in C.get(1, ()):
        u, (g,) = c; lines.append((u, add(u, g)))
    return polys, lines

# ------------------------------------------------------------------ Figure 12: slab structure (corrected, with U vs U0)
def fig12():
    E2 = lambda v: (v[0]+v[1]) % 2 == 0
    q2 = (2, 2); k = 2; J = 2
    Cu, C0 = cells(E2, q2), cells0(E2, q2)
    polysU, linesU = planar_geoms(Cu); polys0, lines0 = planar_geoms(C0)
    fig = plt.figure(figsize=(W, 3.1))
    a = fig.add_subplot(1, 2, 1, projection="3d"); b = fig.add_subplot(1, 2, 2)
    setup3d(a, (0, 0, 0), (2, 2, k*J), view=(24, -55), ticks=[[0, 1, 2], [0, 1, 2], [0, k, k*J]])
    # lower slab: walls over the edges of U for z in [0,k]
    for (p0, p1) in linesU:
        poly3(a, [(p0[0], p0[1], 0), (p1[0], p1[1], 0), (p1[0], p1[1], k), (p0[0], p0[1], k)], fc=TGT_L, ec=TGT, alpha=0.55, lw=0.8)
    # upper slab: solid block U0 x [k,kJ] = [0,2]^2 x [k,kJ]
    wirebox(a, (0, 0, k), (2, 2, k*J), color=UNC_E, lw=1.1, ls="-")
    for z in (k, k*J):
        poly3(a, [(0, 0, z), (2, 0, z), (2, 2, z), (0, 2, z)], fc=UNC, ec=UNC_E, alpha=0.30, lw=0.6)
    pts3(a, [(0, 0, 0)], facecolor="w", edgecolor="k", s=26, depthshade=False)
    a.set_title("$U(\\Lambda',Q)$, $k=2$, $J=2$", fontsize=7.8)
    # (b) planar slices
    b.set_title("planar slices", fontsize=7.8)
    ox = 0.0
    # slice below k : U (edges only)  -- left; slice at/above k: U0 (filled) -- right
    for (p0, p1) in linesU:
        b.plot([p0[0], p1[0]], [p0[1], p1[1]], color=TGT, lw=1.9, ls=(0, (4, 1.5)), zorder=3)
    for pts in polysU:
        b.add_patch(MPoly(pts, fc=TGT_L, ec=TGT, lw=1.0, zorder=2))
    sh = 3.3
    for pts in polys0:
        b.add_patch(MPoly([(x+sh, y) for x, y in pts], fc=UNC, ec=UNC_E, lw=1.0, hatch="////", zorder=2))
    for (p0, p1) in lines0:
        b.plot([p0[0]+sh, p1[0]+sh], [p0[1], p1[1]], color=UNC_E, lw=1.0, zorder=3)
    for pt in fibre(E2, q2): b.scatter([pt[0]], [pt[1]], s=14, color="k", zorder=5); b.scatter([pt[0]+sh], [pt[1]], s=14, color="k", zorder=5)
    b.scatter([0, sh], [0, 0], s=34, facecolor="w", edgecolor="k", linewidths=1.0, zorder=6)
    b.text(1, -0.55, "$0\\leq x_3<k$:\n$U(E_2,(2,2))$\n(origin excluded)", ha="center", va="top", fontsize=6.3)
    b.text(1+sh, -0.55, "$k\\leq x_3\\leq kJ$:\n$U^0(E_2,(2,2))$\n(origin allowed)", ha="center", va="top", fontsize=6.3)
    b.set_xlim(-0.4, sh+2.4); b.set_ylim(-1.7, 2.4); b.set_aspect("equal"); b.axis("off")
    for t_, a_ in zip("ab", (a, b)): tag(a_, t_)
    fig.suptitle("Split target $\\Lambda'=E_2\\oplus2\\mathbf{Z}e_3$, $Q=(2,2,4)$ (exact planar complexes)", fontsize=7.8, y=1.01)
    fig.tight_layout(w_pad=0.4)
    save(fig, "fig12_slab_structure")
    DATA["fig12"] = dict(planar_target="E_2", box_planar=[2, 2], k=k, J=J, edges_U=len(linesU), squares_U=len(polysU), edges_U0=len(lines0), squares_U0=len(polys0),
                         note="U is one-dimensional here (edges), U0 is the filled square [0,2]^2 plus edges; slab drawn schematically between exact planar complexes")
    # exactness: the 3D target complex slices agree with theorem slab-i on sample points
    Lp3 = lambda v: (v[0]+v[1]) % 2 == 0 and v[2] % k == 0
    C3 = cells(Lp3, (2, 2, k*J))
    for (x, y) in ((Fr(1, 2), Fr(1, 2)), (Fr(1, 2), Fr(3, 2)), (Fr(3, 2), Fr(1, 2)), (Fr(1), Fr(1))):
        zin = in_union(C3, (x, y, Fr(1, 1)))        # height 1 < k : slice U
        zup = in_union(C3, (x, y, Fr(3, 1)))        # height 3 >= k : slice U0
        inU = in_union(Cu, (x, y)); inU0 = in_union(C0, (x, y))
        assert zin == inU and zup == inU0, (x, y, zin, inU, zup, inU0)

# ------------------------------------------------------------------ Figure 13: the strict-slab correction
def fig13():
    Lam = lambda v: all(x % 2 == 0 for x in v)
    Lp = lambda v: v[2] % 2 == 0
    q = (2, 2, 2); k = 2
    Cs, Ct = cells(Lam, q), cells(Lp, q)
    cell = ((0, 0, 2), ((0, 2, 0), (2, 0, 0)))
    assert cell in Cs[2] and cell not in Ct[2]
    pt = (Fr(1, 2), Fr(1, 2), Fr(2))
    assert in_union(Ct, pt)                     # exactly in U(Lambda',Q)
    Cplan = cells(lambda v: True, (2, 2))       # U(Z^2,(2,2))
    assert not in_union(Cplan, (Fr(1, 2), Fr(1, 2)))
    # full containment of the cell, exactly, on a grid
    for i in range(11):
        for j in range(11):
            assert in_union(Ct, (Fr(2*i, 10), Fr(2*j, 10), Fr(2)))
    fig = plt.figure(figsize=(W, 2.9))
    a = fig.add_subplot(1, 3, 1, projection="3d"); b = fig.add_subplot(1, 3, 2); c = fig.add_subplot(1, 3, 3)
    setup3d(a, (0, 0, 0), (2, 2, 2), view=(24, -55), ticks=[[0, 1, 2]]*3)
    # slab below k : prism over L-shape  U(Z^2,(2,2)) = {max(x,y)>=1}
    L_ = [(1, 0), (2, 0), (2, 2), (0, 2), (0, 1), (1, 1)]
    for i in range(len(L_)):
        p0, p1 = L_[i], L_[(i+1) % len(L_)]
        poly3(a, [(p0[0], p0[1], 0), (p1[0], p1[1], 0), (p1[0], p1[1], k), (p0[0], p0[1], k)], fc=TGT_L, ec=TGT, alpha=0.35, lw=0.6)
    poly3(a, [(p[0], p[1], 0) for p in L_], fc=TGT_L, ec=TGT, alpha=0.5, lw=0.8)
    poly3(a, [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], fc=UNC, ec=UNC_E, alpha=0.8, lw=0.9)
    poly3(a, [(0, 0, k), (2, 0, k), (2, 2, k), (0, 2, k)], fc=SRC_L, ec=SRC, alpha=0.6, lw=1.8)
    witness3(a, (0.5, 0.5, 2.0))
    pts3(a, [(0, 0, 0)], facecolor="w", edgecolor="k", s=26, depthshade=False)
    a.set_title("$U(\\Lambda',Q)$ and the cell $c$ at height $k$", fontsize=7.4)
    # (b) slice below k
    for (pts, fc, ec, hat, ttl) in (((b, 0), None, None, None, None),):
        pass
    b.add_patch(Rectangle((0, 0), 1, 1, fc=UNC, ec=UNC_E, hatch="////", lw=0.8, zorder=1))
    b.add_patch(MPoly([(1, 0), (2, 0), (2, 2), (0, 2), (0, 1), (1, 1)], fc=TGT_L, ec=TGT, lw=0.9, ls=(0, (4, 1.5)), zorder=1))
    b.add_patch(Rectangle((0, 0), 2, 2, fc="none", ec=SRC, lw=1.8, ls=(0, (6, 2)), zorder=3))
    witness2(b, (0.5, 0.5)); style_axes2(b, (-0.2, 2.3), (-0.2, 2.3), [0, 1, 2], [0, 1, 2])
    b.set_title("slice $x_3<k$: $U(\\mathbf{Z}^2,(2,2))$", fontsize=7.4)
    b.set_xlabel("closed-height test: projection of $c$ (blue dashed)\nvs this slice $\\Rightarrow$ rejects $c$ (wrong)", fontsize=6.1, labelpad=2)
    c.add_patch(Rectangle((0, 0), 2, 2, fc=TGT_L, ec=TGT, lw=0.9, ls=(0, (4, 1.5)), zorder=1))
    c.add_patch(Rectangle((0, 0), 2, 2, fc="none", ec=SRC, lw=1.8, zorder=3))
    witness2(c, (0.5, 0.5)); c.scatter([0], [0], s=30, facecolor="w", edgecolor="k", linewidths=1.0, zorder=6)
    c.text(0.12, 0.12, "$(0,0,2)\\neq0$", fontsize=6.0, zorder=7)
    style_axes2(c, (-0.2, 2.3), (-0.2, 2.3), [0, 1, 2], [0, 1, 2])
    c.set_title("slice $x_3=k$: $U^0$ (full square)", fontsize=7.4)
    c.set_xlabel("corrected test: $\\min x_3=k$, so no part of $c$\nlies below $k$; $c\\subseteq U'$ (accepted)", fontsize=6.1, labelpad=2)
    for t_, a_ in zip("abc", (a, b, c)): tag(a_, t_)
    fig.suptitle("Erratum E1: $\\Lambda=2\\mathbf{Z}^2\\oplus2\\mathbf{Z}\\subset\\Lambda'=\\mathbf{Z}^2\\oplus2\\mathbf{Z}$, $Q=(2,2,2)$, $c=[0,2]^2\\times\\{2\\}$, $p=(\\frac{1}{2},\\frac{1}{2},2)$", fontsize=7.2, y=1.02)
    fig.tight_layout(w_pad=0.5)
    save(fig, "fig13_strict_slab")
    DATA["fig13"] = dict(source="2Z^2 + 2Z", target="Z^2 + 2Z", k=2, box=[2, 2, 2], cell=[list(cell[0]), [list(x) for x in cell[1]]], point=["1/2", "1/2", "2"],
                         exact="p in U(target) (exact); (1/2,1/2) not in U(Z^2,(2,2)) (exact); 121 grid points of c in U(target) (exact)")

# ------------------------------------------------------------------ Figure 14: hard-cell decomposition (Minkowski sum)
def fig14():
    Lam = lambda v: all(x % 2 == 0 for x in v) and sum(x//2 for x in v) % 2 == 0
    Lp = lambda v: all(x % 2 == 0 for x in v)
    q = (2, 4, 2)
    cell = ((0, 2, 2), ((0, 2, -2), (2, -2, 0)))
    assert cell in cells(Lam, q)[2]
    u, (g, h) = cell
    gp = tuple(max(x, 0) for x in g); gm = tuple(-min(x, 0) for x in g); hp = tuple(max(x, 0) for x in h); hm = tuple(-min(x, 0) for x in h)
    a1, b1, a2, b2 = gm, gp, hm, hp
    assert tuple(x+y for x, y in zip(a1, a2)) == u and all(Lp(v) for v in (a1, b1, a2, b2))
    fig = plt.figure(figsize=(W, 3.0))
    a = fig.add_subplot(1, 2, 1, projection="3d"); b = fig.add_subplot(1, 2, 2, projection="3d")
    for ax_ in (a, b): setup3d(ax_, (0, 0, 0), (2, 4, 2), view=(32, 30), ticks=[[0, 2], [0, 2, 4], [0, 2]])
    # (a) the two segments [a_i,b_i] and their Minkowski sum
    seg3(a, a1, b1, color=SRC, lw=2.4); seg3(a, a2, b2, color=SRC, lw=2.4, ls=(0, (4, 1.5)))
    poly3(a, cell_corners(cell), fc=SRC_L, ec=SRC, alpha=0.45, lw=1.0)
    for P_, n, dy in ((a1, "$a_1$", 0.0), (b1, "$b_1=a_2$", 0.0), (b2, "$b_2$", 0.0)):
        a.text(P_[0], P_[1]+dy, P_[2]+0.2, n, fontsize=7)
    pts3(a, [a1, b1, a2, b2], color="k", s=14, depthshade=False)
    a.set_title("$c=[a_1,b_1]+[a_2,b_2]$", fontsize=7.6)
    # (b) Z^0 = box, tiling and the star of the origin
    wirebox(b, (0, 0, 0), (2, 4, 2), color=GREY, lw=0.6)
    wirebox(b, (0, 0, 0), (2, 2, 2), color=UNC_E, lw=1.2, ls="--")
    wirebox(b, (0, 2, 0), (2, 4, 2), color=TGT, lw=1.2)
    poly3(b, cell_corners(cell), fc=SRC_L, ec=SRC, alpha=0.40, lw=1.2)
    T0 = [(0, 2, 2), (2, 0, 2), (2, 2, 0)]
    poly3(b, T0, fc=UNC, ec=UNC_E, alpha=0.9, lw=1.0)
    pts3(b, [(0, 0, 0)], facecolor="w", edgecolor="k", s=28, depthshade=False)
    b.text2D(0.30, 0.20, "$\\mathrm{St}(0)=[0,2]^3$", transform=b.transAxes, fontsize=6.5, color=UNC_E)
    b.set_title("tiling of $Z^0=[0,2]\\times[0,4]\\times[0,2]$ by $2\\mathbf{Z}^3$-cells", fontsize=7.4)
    for t_, a_ in zip("ab", (a, b)): tag(a_, t_)
    fig.suptitle("Hard cell of the no-free-coordinate example: $a_1=(0,0,2)$, $b_1=(0,2,0)$, $a_2=(0,2,0)$, $b_2=(2,0,0)$; $u=a_1+a_2$", fontsize=7.3, y=1.02)
    fig.text(0.5, -0.04, "Every tile of the tiling not containing $0$ is a cell of $U(\\Lambda',Q_c)$; only the triangle $T_0=c\\cap\\mathrm{St}(0)$ (orange) can lie outside it.", fontsize=6.4, ha="center")
    fig.tight_layout(w_pad=0.4)
    save(fig, "fig14_hard_cell")
    DATA["fig14"] = dict(cell=[list(u), [list(g), list(h)]], a1=list(a1), b1=list(b1), a2=list(a2), b2=list(b2), Q_c=[2, 4, 2], u_equals_sum_a=True,
                         tiles=["[0,2]x[0,2]x[0,2] (contains the origin: excluded)", "[0,2]x[2,4]x[0,2] (cell)"])

# ------------------------------------------------------------------ Figure 15: P4-F110 coupled specimen
def fig15():
    E3 = lambda v: sum(v) % 2 == 0
    L9 = lambda v: (v[0]-v[1]+v[2]) % 6 == 0
    q1, q2 = (2, 2, 2), (4, 4, 4)
    Fe1, F91 = fibre(E3, q1), fibre(L9, q1)
    Fe2, F92 = fibre(E3, q2), fibre(L9, q2)
    assert set(F91) <= set(Fe1) and set(F92) <= set(Fe2)
    C1 = cells(E3, q1)
    wit = (Fr(0), Fr(1), Fr(3, 2))
    assert not in_union(C1, wit)
    # hull membership of the witness
    assert sum(wit) >= 2 and all(0 <= x <= 2 for x in wit)
    fig = plt.figure(figsize=(W, 3.0))
    a = fig.add_subplot(1, 3, 1, projection="3d"); b = fig.add_subplot(1, 3, 2); c = fig.add_subplot(1, 3, 3, projection="3d")
    # (a) n=2
    setup3d(a, (0, 0, 0), (2, 2, 2), view=(32, 40), ticks=[[0, 1, 2]]*3)
    wirebox(a, (0, 0, 0), (2, 2, 2), color=GREY, lw=0.5)
    tri = [(2, 0, 0), (0, 2, 0), (0, 0, 2)]
    poly3(a, tri, fc=UNC, ec=UNC_E, alpha=0.55, lw=1.0)
    pts3(a, [p for p in Fe1 if p not in set(F91)], color=TGT, s=14, marker="s", depthshade=False)
    pts3(a, F91, color=SRC, s=26, depthshade=False)
    witness3(a, tuple(float(x) for x in wit))
    a.set_title("$n=2$ ($m=1$): $F(\\Lambda_9)\\subset F(E_3)$", fontsize=7.2)
    # (b) face x1=0 for n=2: E_2 in the hollow box (2,2) : coordinates (x2,x3)
    E2 = lambda v: (v[0]+v[1]) % 2 == 0
    C2 = cells(E2, (2, 2))
    polys, lines = planar_geoms(C2)
    tri1 = [(1, 1), (2, 0), (2, 2)]; tri2 = [(1, 1), (0, 2), (2, 2)]
    for tr in (tri1, tri2): b.add_patch(MPoly(tr, fc=UNC, ec="none", hatch="////", zorder=1))
    for (p0, p1) in lines: b.plot([p0[0], p1[0]], [p0[1], p1[1]], color=TGT, lw=1.8, ls=(0, (4, 1.5)), zorder=3)
    for pt in fibre(E2, (2, 2)): b.scatter([pt[0]], [pt[1]], s=18, color="k", zorder=5)
    witness2(b, (1, 1.5)); b.text(1.12, 1.55, "$(1,\\frac{3}{2})$", fontsize=6.5)
    style_axes2(b, (-0.3, 2.4), (-0.3, 2.4), [0, 1, 2], [0, 1, 2])
    b.set_xlabel("$x_2$", labelpad=1); b.set_ylabel("$x_3$", labelpad=1)
    b.set_title("face $x_1=0$: $E_2$, box $(2,2)$", fontsize=7.2)
    # (c) n=4 hull
    setup3d(c, (0, 0, 0), (4, 4, 4), view=(32, 40), ticks=[[0, 2, 4]]*3)
    wirebox(c, (0, 0, 0), (4, 4, 4), color=GREY, lw=0.5)
    for i, j in ((0, 1), (1, 2), (0, 2)):
        seg3(c, tri[i], tri[j], color=UNC_E, lw=1.3, ls="--")
    pts3(c, [p for p in Fe2 if p not in set(F92)], color=TGT_L, s=6, marker="s", depthshade=False)
    pts3(c, F92, color=SRC, s=14, depthshade=False)
    poly3(c, tri, fc=UNC, ec=UNC_E, alpha=0.5, lw=0.8)
    c.set_title("$n=4$ ($m=2$): $U(E_3)=\\{\\sum x_i\\geq2\\}$", fontsize=7.2)
    for t_, a_ in zip("abc", (a, b, c)): tag(a_, t_)
    fig.suptitle("P4-F110: $x_m=2\\cdot110^{4m}/9\\to110^{4m}/3$, $\\Lambda_9=\\{a-b+c\\equiv0\\ (6)\\}\\subset E_3$, $Q_m=[0,2m]^3$", fontsize=7.6, y=1.01)
    fig.text(0.5, -0.05, "(a) blue: $F(\\Lambda_9)$, teal squares: $F(E_3)\\setminus F(\\Lambda_9)$; the orange triangle $x_1+x_2+x_3=2$ is the cut of $\\mathrm{conv}\\,F(E_3)$, and the star is the exact gap point $(0,1,\\frac{3}{2})$ lying in no cell.\n(b) its trace in the planar hollow-box face. (c) for $n=4$ the union equals $\\mathrm{conv}\\,F(E_3)$ (hull theorem; $n=4$ by the cited certificate), so every source union is contained.", fontsize=6.0, ha="center")
    fig.tight_layout(w_pad=0.4)
    save(fig, "fig15_f110")
    DATA["fig15"] = dict(m1_box=list(q1), m2_box=list(q2), F_E3_m1=len(Fe1), F_L9_m1=len(F91), F_E3_m2=len(Fe2), F_L9_m2=len(F92), gap_point=["0", "1", "3/2"],
                         gap_point_in_conv_F=True, gap_point_in_any_cell_E3_box2=False, note="m=2 containment rests on Theorem 10.3 (n=4 certificate cited); no claim is drawn from the picture alone")

def run():
    fig12(); fig13(); fig14(); fig15()
if __name__ == "__main__":
    run(); print("C ok")
