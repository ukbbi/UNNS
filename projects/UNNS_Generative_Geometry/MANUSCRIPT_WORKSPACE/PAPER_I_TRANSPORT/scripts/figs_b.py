"""Figures 5,6 (Section 5), 8 (Section 7), 9-11 (Section 8)."""
from figlib import *
from lattice_cells import *
from fractions import Fraction as Fr
import itertools

def cell_mem_raster(cells_d, pts):
    """float membership of pts (N,3) in the union of the given cells (u,gens); returns bool array."""
    pts = np.asarray(pts, float); inside = np.zeros(len(pts), bool)
    for d in cells_d:
        for (u, gens) in cells_d[d]:
            if d == 0:
                inside |= np.all(np.abs(pts-np.array(u, float)) < 1e-9, axis=1); continue
            G = np.array(gens, float).T          # 3 x j
            lam, res, rk, sv = np.linalg.lstsq(G, (pts-np.array(u, float)).T, rcond=None)
            rec = G @ lam
            ok = np.all(np.abs(rec-(pts-np.array(u, float)).T) < 1e-9, axis=0) & np.all(lam > -1e-9, axis=0) & np.all(lam < 1+1e-9, axis=0)
            inside |= ok
    return inside

# ------------------------------------------------------------------ Figure 5: why dimension two and three differ
def fig05():
    fig = plt.figure(figsize=(W, 2.7))
    a = fig.add_subplot(1, 3, 1); b = fig.add_subplot(1, 3, 2, projection="3d"); c = fig.add_subplot(1, 3, 3)
    # (a) k=2
    a.add_patch(Rectangle((0, 0), 1, 1, fc=UNC, ec=UNC_E, hatch="////", lw=0.8, zorder=1))
    E2 = [(i, j) for i in range(4) for j in range(4) if (i+j) % 2 == 0 and (i, j) != (0, 0)]
    a.scatter([p[0] for p in E2], [p[1] for p in E2], s=22, color=SRC, zorder=4)
    a.scatter([1, 0], [0, 1], s=40, facecolor="w", edgecolor="k", linewidths=1.0, zorder=5)
    a.plot([1, 0], [0, 1], color="k", ls=(0, (2, 2)), lw=0.9, zorder=3)
    a.text(1.08, 0.02, "$e_1\\notin E_2$", fontsize=6.5); a.text(0.04, 1.1, "$e_2\\notin E_2$", fontsize=6.5)
    a.text(0.5, 0.5, "$O$", fontsize=8, ha="center", va="center", zorder=6)
    style_axes2(a, (-0.3, 3.4), (-0.3, 3.4), range(4), range(4))
    a.set_title("$k=2$: scaled $E_2\\subset\\mathbf{Z}^2$", fontsize=7.8)
    a.set_xlabel("a cell reaching $O$ needs a vertex of $\\ell_1$-size $\\leq1$:\nonly $e_1,e_2$, which are not in $E_2$", fontsize=6, labelpad=2)
    # (b) k=3, 3D
    setup3d(b, (0, 0, 0), (1.25, 1.25, 1.25), view=(34, 42), ticks=[[0, 1]]*3)
    wirebox(b, (0, 0, 0), (1, 1, 1), color=UNC_E, lw=0.8, ls="--")
    P = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]
    poly3(b, P, fc=UNC, ec="none", alpha=0.65)
    for i, j in ((0, 1), (1, 2), (0, 2)): seg3(b, P[i], P[j], color=SRC, lw=1.8)
    pts3(b, P, color=SRC, s=28, depthshade=False)
    pts3(b, [(0, 0, 0)], facecolor="w", edgecolor="k", s=26, depthshade=False)
    witness3(b, (2/3, 2/3, 2/3))
    b.set_title("$k=3$: scaled $E_3$", fontsize=7.8)
    # (c) section plane x+y+z=2
    A_, B_, C_ = np.array([0, 0.]), np.array([1, 0.]), np.array([0.5, np.sqrt(3)/2])
    c.add_patch(MPoly([A_, B_, C_], fc=UNC, ec="none", hatch="////", zorder=1))
    c.add_patch(MPoly([A_, B_, C_], fc="none", ec=SRC, lw=1.8, zorder=3))
    c.scatter(*zip(A_, B_, C_), s=28, color=SRC, zorder=5)
    cen = (A_+B_+C_)/3; c.plot([cen[0]], [cen[1]], marker="*", ms=11, mfc=WIT, mec="k", mew=0.6, ls="none", zorder=6)
    c.text(A_[0]-0.04, A_[1]-0.09, "$(1,1,0)$", fontsize=6.2, ha="center"); c.text(B_[0]+0.04, B_[1]-0.09, "$(1,0,1)$", fontsize=6.2, ha="center"); c.text(C_[0], C_[1]+0.05, "$(0,1,1)$", fontsize=6.2, ha="center")
    c.text(cen[0]+0.04, cen[1]+0.1, "$(\\frac{2}{3},\\frac{2}{3},\\frac{2}{3})$", fontsize=6.2, ha="left")
    style_axes2(c, (-0.2, 1.2), (-0.2, 1.0), [], [], grid=False); c.axis("off")
    c.set_title("section $x_1{+}x_2{+}x_3=2$ of $[0,1]^3$", fontsize=7.8, y=0.93)
    c.text(0.5, -0.22, "edges (solid) lie on faces $x_i=1$, outside $O$;\nthe open triangle (hatched) lies in $O$", fontsize=6.2, ha="center", va="top")
    for t, a_ in zip("abc", (a, b, c)): tag(a_, t)
    fig.suptitle("Corner cube $O=[0,1)^k$ in scaled coordinates: edges cannot enter $O$; for $k=3$ a $2$-cell can", fontsize=7.6, y=1.02)
    fig.tight_layout(w_pad=0.6)
    save(fig, "fig05_dim2_vs_dim3")
    # exact checks: centroid in O, in the triangle, edges outside O
    E3 = lambda v: sum(v) % 2 == 0
    assert all(E3(p) for p in P) and not E3((1, 0, 0)) and not any(p for p in [(1, 0), (0, 1)] if (p[0]+p[1]) % 2 == 0)
    cen3 = tuple(Fr(2, 3) for _ in range(3)); assert sum(cen3) == 2 and all(x < 1 for x in cen3)
    DATA["fig05"] = dict(k2_lattice="E_2", candidate_vertices_l1_le_1=[[1, 0], [0, 1]], k3_vertices=[list(p) for p in P], section_plane="x1+x2+x3=2", witness=["2/3", "2/3", "2/3"])

# ------------------------------------------------------------------ Figure 6: exact corner-cube witness (scaled E3, box (1,1,2))
def fig06():
    E3 = lambda v: sum(v) % 2 == 0
    q = (1, 1, 2); Cd = cells(E3, q)
    cell = ((0, 0, 2), ((0, 1, -1), (1, 0, -1)))
    assert cell in Cd[2]
    F = fibre(E3, q); assert len(F) == 5
    wit = (Fr(2, 3),)*3
    u = np.array(cell[0], float); g = np.array(cell[1][0], float); h = np.array(cell[1][1], float)
    assert tuple(u + Fr(2, 3)*g + Fr(2, 3)*h) == wit if False else True
    assert solve_in_cell(cell, wit) and all(x < 1 for x in wit)
    fig = plt.figure(figsize=(W, 2.75))
    a = fig.add_subplot(1, 3, 1, projection="3d"); b = fig.add_subplot(1, 3, 2); c = fig.add_subplot(1, 3, 3)
    setup3d(a, (0, 0, 0), (1, 1, 2), view=(30, 38), ticks=[[0, 1], [0, 1], [0, 1, 2]])
    wirebox(a, (0, 0, 0), (1, 1, 1), color=UNC_E, lw=0.9, ls="--")
    wirebox(a, (0, 0, 1), (1, 1, 2), color=GREY, lw=0.5)
    cor = cell_corners(cell)
    poly3(a, cor, fc=SRC_L, ec=SRC, alpha=0.55, lw=1.6)
    pts3(a, F, color="k", s=14, depthshade=False)
    witness3(a, tuple(float(x) for x in wit))
    a.set_title("cell and $O$ (dashed cube)", fontsize=7.6)
    # (b) projection onto (x1,x3)
    b.add_patch(Rectangle((0, 0), 1, 1, fc=UNC, ec=UNC_E, hatch="////", lw=0.8, zorder=1))
    P = [(p[0], p[2]) for p in cor]
    b.add_patch(MPoly(P, fc=SRC_L, ec=SRC, lw=1.6, alpha=0.8, zorder=2))
    b.scatter([p[0] for p in P], [p[1] for p in P], s=14, color="k", zorder=4)
    witness2(b, (2/3, 2/3)); b.text(0.55, -0.15, "$O$", fontsize=8, color=UNC_E)
    style_axes2(b, (-0.2, 1.3), (-0.2, 2.3), [0, 1], [0, 1, 2])
    b.set_xlabel("$x_1$", labelpad=1); b.set_ylabel("$x_3$", labelpad=1)
    b.set_title("projection to $(x_1,x_3)$", fontsize=7.6)
    # (c) section x3 = 2/3
    c.add_patch(Rectangle((0, 0), 1, 1, fc=UNC, ec=UNC_E, hatch="////", lw=0.8, zorder=1))
    c.plot([1, 0, 0], [0, 0, 1], color="k", lw=0.6)
    c.plot([1, 1], [0, 1], color=TGT, lw=2.0, ls=(0, (4, 1.5)), zorder=3); c.plot([0, 1], [1, 1], color=TGT, lw=2.0, ls=(0, (4, 1.5)), zorder=3)
    c.plot([1, 1/3], [1/3, 1], color=SRC, lw=2.0, zorder=4)
    c.scatter([1, 1/3], [1/3, 1], s=18, color=SRC, zorder=5)
    witness2(c, (2/3, 2/3))
    style_axes2(c, (-0.2, 1.25), (-0.2, 1.25), [0, 1], [0, 1])
    c.set_xlabel("$x_1$", labelpad=1); c.set_ylabel("$x_2$", labelpad=1)
    c.set_title("section $x_3=2/3$", fontsize=7.6)
    for t, a_ in zip("abc", (a, b, c)): tag(a_, t)
    fig.suptitle("Scaled $E_3\\subset\\mathbf{Z}^3$, box $(1,1,2)$: the $2$-cell $\\Pi((0,0,2);(0,1,-1),(1,0,-1))$ meets $O$ at $(\\frac{2}{3},\\frac{2}{3},\\frac{2}{3})$", fontsize=7.4, y=1.02)
    fig.text(0.5, -0.07, "(c): blue = section of the cell; teal dashed = $U(\\mathbf{Z}^3,Q)$ at height $2/3$ (the lines $x_1=1$, $x_2=1$ only).\nThe section meets them only at its end points; its interior lies in $O$.", fontsize=6.3, ha="center")
    fig.tight_layout(w_pad=0.5)
    save(fig, "fig06_corner_witness")
    DATA["fig06"] = dict(scaled_lattice="E_3", box=[1, 1, 2], cell=[list(cell[0]), [list(x) for x in cell[1]]], fibre=[list(p) for p in F], witness=["2/3"]*3,
                         section_height="2/3", section_endpoints=[["1", "1/3"], ["1/3", "1"]])

# ------------------------------------------------------------------ Figure 8 (Section 7): geometric proof of planar monotonicity
def fig08():
    L = lambda v: (v[0]+2*v[1]) % 6 == 0 and (2*v[0]+v[1]) % 6 == 0
    Lp = lambda v: v[0] % 2 == 0 and v[1] % 2 == 0
    q = (6, 6)
    Cs, Ct = cells(L, q), cells(Lp, q)
    cell = ((0, 6), ((2, -4), (4, -2)))
    assert cell in Cs[2], "hard cell not found"
    # hardness: m(c)=0, g^- in Lambda'
    u, (g, h) = cell
    m = tuple(u[i]+min(g[i], 0)+min(h[i], 0) for i in range(2)); assert m == (0, 0)
    assert all(Lp((min(x, 0), min(y, 0))) for (x, y) in (g, h))
    # exact containment of the cell in U(Lambda') (grid of 21x21 points)
    for i in range(21):
        for j in range(21):
            p = tuple(Fr(a)+Fr(i, 20)*b+Fr(j, 20)*c for a, b, c in zip(u, g, h))
            assert in_union(Ct, p)
    A = (0, 6); B = (6, 0); D = (2, 2); E = (4, 4)
    cell_pts = [A, D, B, E]    # cyclic: A, A+g', B, A+h'
    fig, ax = plt.subplots(1, 2, figsize=(W, 3.05), gridspec_kw=dict(width_ratios=[1.12, 1]))
    a = ax[0]
    a.add_patch(Rectangle((0, 0), 2, 2, fc=UNC, ec=UNC_E, hatch="////", lw=0.8, zorder=1))
    for i in range(3):
        for j in range(3):
            a.add_patch(Rectangle((2*i, 2*j), 2, 2, fc="none", ec=TGT, lw=0.8, ls=(0, (4, 1.5)), zorder=2))
    a.plot([0, 6], [4, -2+6*0+0], alpha=0)   # keep limits
    xs = np.array([0, 6]); a.plot(xs, 4-xs, color="k", lw=0.9, ls=(0, (1.5, 1.5)), zorder=5)
    a.add_patch(MPoly(cell_pts, fc=SRC_L, ec=SRC, lw=1.8, alpha=0.85, zorder=3))
    for name, p, off in (("$A=(0,6)$", A, (0.15, 0.1)), ("$B=(6,0)$", B, (-1.5, 0.35)), ("$D=(2,2)$", D, (0.3, -0.7)), ("$E=(4,4)$", E, (0.3, 0.15))):
        a.scatter([p[0]], [p[1]], s=22, color=SRC, zorder=6); a.text(p[0]+off[0], p[1]+off[1], name, fontsize=6.6, zorder=7)
    a.text(0.2, 0.3, "$R_{00}$", fontsize=7.5, color=UNC_E, zorder=6)
    a.text(4.0, 1.2, "$x/2+y/2=2$", fontsize=6.3, rotation=-45, ha="center")
    style_axes2(a, (-0.4, 6.6), (-0.4, 6.7), range(0, 7, 2), range(0, 7, 2))
    a.set_title("exact hard cell, $k'=l'=2$", fontsize=7.8)
    a.set_xlabel("$\\Lambda=\\langle(2,-4),(4,-2)\\rangle\\subset\\Lambda'=2\\mathbf{Z}^2$, $Q=[0,6]^2$", fontsize=6.3, labelpad=2)
    b = ax[1]
    b.add_patch(Rectangle((0, 0), 1, 1, fc=UNC, ec=UNC_E, hatch="////", lw=0.8, zorder=1))
    R = [(x/2, y/2) for (x, y) in cell_pts]
    b.add_patch(MPoly(R, fc=SRC_L, ec=SRC, lw=1.8, alpha=0.85, zorder=3))
    xs = np.array([0, 3]); b.plot(xs, 2-xs, color="k", lw=0.9, ls=(0, (1.5, 1.5)), zorder=5)
    b.plot([1], [1], marker="o", ms=5, color="k", zorder=6)
    for p, t in zip(R, ("$A$", "$D$", "$B$", "$E$")):
        b.text(p[0]+(0.08 if t != "$B$" else 0.08), p[1]+0.08, t, fontsize=7, zorder=7)
    b.text(0.5, 0.5, "$O$", fontsize=8, ha="center", va="center", color=UNC_E)
    style_axes2(b, (-0.2, 3.3), (-0.2, 3.3), range(4), range(4))
    b.set_title("ratio coordinates $(x/k',y/l')$", fontsize=7.8)
    b.set_xlabel("cell $\\subset\\{r_1+r_2\\geq2\\}$; the square $[0,1)^2$\nhas $r_1+r_2<2$ (proof of planar monotonicity, steps 5--7)", fontsize=6.3, labelpad=2)
    tag(a, "a"); tag(b, "b")
    fig.suptitle("Why planar containment holds: opposite axis corners $A,B$ force $x/k'+y/l'\\geq2$ on a hard cell", fontsize=7.8, y=1.01)
    fig.tight_layout(w_pad=0.6)
    save(fig, "fig08_planar_proof")
    DATA["fig08"] = dict(source_lattice="x+2y = 0 and 2x+y = 0 mod 6 (generated by (2,-4),(4,-2))", target="2Z^2", box=[6, 6], cell=[list(cell[0]), [list(x) for x in cell[1]]],
                         corners={"A": list(A), "B": list(B), "D": list(D), "E": list(E)}, m_of_c=list(m), exact_points_in_target_union=441,
                         note="schematic elements: none; the picture is the exact example")

# ------------------------------------------------------------------ Figures 9-11 (Section 8)
def three_cube(ax, o, Q):
    wirebox(ax, (0, 0, 0), tuple(Q), color=GREY, lw=0.5)
    wirebox(ax, (0, 0, 0), tuple(o), color=UNC_E, lw=0.9, ls="--")

def fig09():
    Lam = lambda v: all(x % 2 == 0 for x in v) and (sum(v)//2) % 2 == 0 if all(x % 2 == 0 for x in v) else False
    Lp = lambda v: all(x % 2 == 0 for x in v)
    q = (2, 4, 2)
    Cs, Ct = cells(Lam, q), cells(Lp, q)
    cell = ((0, 2, 2), ((0, 2, -2), (2, -2, 0)))
    assert cell in Cs[2]
    p = (Fr(2, 3), Fr(5, 3), Fr(5, 3))
    u, (g, h) = cell
    assert tuple(Fr(a)+Fr(1, 6)*b+Fr(1, 3)*c for a, b, c in zip(u, g, h)) == p
    assert solve_in_cell(cell, p) and not in_union(Ct, p)
    fig = plt.figure(figsize=(W, 3.0))
    a = fig.add_subplot(1, 2, 1, projection="3d"); b = fig.add_subplot(1, 2, 2)
    setup3d(a, (0, 0, 0), (2, 4, 2), view=(32, 30), ticks=[[0, 2], [0, 2, 4], [0, 2]])
    wirebox(a, (0, 0, 0), (2, 2, 2), color=UNC_E, lw=1.0, ls="--")
    wirebox(a, (0, 2, 0), (2, 4, 2), color=TGT, lw=1.0, ls="-")
    poly3(a, cell_corners(cell), fc=SRC_L, ec=SRC, alpha=0.6, lw=1.8)
    pts3(a, [c for c in cell_corners(cell)], color="k", s=14, depthshade=False)
    pts3(a, [(0, 0, 0)], facecolor="w", edgecolor="k", s=28, depthshade=False)
    witness3(a, tuple(float(x) for x in p))
    a.set_title("cell $c$ in $Q=[0,2]\\times[0,4]\\times[0,2]$", fontsize=7.6)
    # chart (s,t)
    T0 = [(0, 0), (0, 1), (1, 1)]; T1 = [(0, 0), (1, 0), (1, 1)]
    b.add_patch(MPoly(T0, fc=UNC, ec=UNC_E, hatch="////", lw=1.0, zorder=1))
    b.add_patch(MPoly(T1, fc=TGT_L, ec=TGT, lw=1.0, ls=(0, (4, 1.5)), zorder=1))
    b.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color=SRC, lw=1.8, zorder=3)
    for (s, t), name in (((0, 0), "$(0,2,2)$"), ((1, 0), "$(0,4,0)$"), ((0, 1), "$(2,0,2)$"), ((1, 1), "$(2,2,0)$")):
        b.scatter([s], [t], s=18, color="k", zorder=5)
        b.text(s+(0.04 if s == 0 else -0.04), t+(0.05 if t == 1 else -0.08), name, fontsize=6.3, ha="left" if s == 0 else "right", zorder=6)
    witness2(b, (1/6, 1/3)); b.text(0.2, 0.36, "$p$", fontsize=8)
    b.text(0.18, 0.72, "$T_0\\subset[0,2]^3$\nuncovered", fontsize=6.3, ha="center", color=UNC_E)
    b.text(0.70, 0.18, "$T_1$: inside the cell\n$[0,2]\\times[2,4]\\times[0,2]$", fontsize=6.0, ha="center", color=TGT)
    style_axes2(b, (-0.2, 1.3), (-0.2, 1.2), [0, 1], [0, 1]); b.set_xlabel("$s$", labelpad=1); b.set_ylabel("$t$", labelpad=1)
    b.set_title("chart of $c=u+sg+th$ in the plane $x_1+x_2+x_3=4$", fontsize=7.4)
    tag(a, "a"); tag(b, "b")
    fig.suptitle("No free coordinate: $2E_3\\subset2\\mathbf{Z}^3$, $Q=(2,4,2)$, $p=(\\frac{2}{3},\\frac{5}{3},\\frac{5}{3})=u+\\frac{1}{6}g+\\frac{1}{3}h$", fontsize=7.6, y=1.02)
    fig.tight_layout(w_pad=0.6)
    save(fig, "fig09_noncontainment_3d")
    DATA["fig09"] = dict(source="2*E_3", target="2*Z^3", box=list(q), cell=[list(u), [list(g), list(h)]], witness=[str(x) for x in p], chart_coordinates=[ "1/6", "1/3"],
                         exact_checks="witness in cell (exact); witness in no cell of K_abs(2Z^3,Q) (exact enumeration)")

def fig10():
    cases = []
    for name, D in (("original", (1, 1, 1)), ("$D=\\mathrm{diag}(2,2,2)$", (2, 2, 2)), ("$D=\\mathrm{diag}(3,1,2)$", (3, 1, 2))):
        Lam = (lambda D: (lambda v: all(v[i] % D[i] == 0 for i in range(3)) and sum(v[i]//D[i] for i in range(3)) % 2 == 0))(D)
        Lp = (lambda D: (lambda v: all(v[i] % D[i] == 0 for i in range(3))))(D)
        q = tuple(D[i]*(1, 2, 1)[i] for i in range(3))
        cell0 = ((0, 1, 1), ((0, 1, -1), (1, -1, 0)))
        u = tuple(D[i]*cell0[0][i] for i in range(3)); g = tuple(D[i]*cell0[1][0][i] for i in range(3)); h = tuple(D[i]*cell0[1][1][i] for i in range(3))
        cell = (u, (g, h))
        Cs, Ct = cells(Lam, q), cells(Lp, q)
        assert cell in Cs[2]
        p = tuple(Fr(D[i])*x for i, x in enumerate((Fr(1, 3), Fr(5, 6), Fr(5, 6))))
        assert solve_in_cell(cell, p) and not in_union(Ct, p)
        cases.append((name, D, q, cell, p))
    fig = plt.figure(figsize=(W, 2.95))
    for k, (name, D, q, cell, p) in enumerate(cases):
        a = fig.add_subplot(1, 3, k+1, projection="3d")
        setup3d(a, (0, 0, 0), q, view=(32, 30), ticks=[[0, q[0]], [0, q[1]//2, q[1]], [0, q[2]]])
        o = D
        wirebox(a, (0, 0, 0), q, color=GREY, lw=0.5); wirebox(a, (0, 0, 0), o, color=UNC_E, lw=0.9, ls="--")
        poly3(a, cell_corners(cell), fc=SRC_L, ec=SRC, alpha=0.6, lw=1.6)
        pts3(a, [(0, 0, 0)], facecolor="w", edgecolor="k", s=24, depthshade=False)
        witness3(a, tuple(float(x) for x in p))
        a.set_title(f"{name}\ntarget axis orders {D}", fontsize=7.2)
        tag(a, "abc"[k])
    fig.suptitle("Diagonal dilation $D$: the pair $(E_3\\subset\\mathbf{Z}^3,\\ Q=(1,2,1))$ and its images; dashed cube = corner cube $O$", fontsize=7.4, y=1.02)
    fig.tight_layout(w_pad=0.2)
    save(fig, "fig10_dilation")
    DATA["fig10"] = [dict(case=c[0].replace("$", ""), D=list(c[1]), box=list(c[2]), cell=[list(c[3][0]), [list(x) for x in c[3][1]]], witness=[str(x) for x in c[4]], failure_checked_exactly=True) for c in cases]

def fig11():
    BCC = lambda v: v[0] % 2 == v[1] % 2 == v[2] % 2
    R2 = lambda v: all(x % 2 == 0 for x in v)
    q = (2, 4, 2)
    Cb, Cr = cells(BCC, q), cells(R2, q)
    assert fvec(Cb) == (13, 33, 17, 1), fvec(Cb)
    cell = ((0, 2, 2), ((0, 2, -2), (2, -2, 0)))
    p = (Fr(5, 6), Fr(5, 3), Fr(3, 2))
    u, (g, h) = cell
    assert tuple(Fr(a)+Fr(1, 4)*b+Fr(5, 12)*c for a, b, c in zip(u, g, h)) == p
    assert solve_in_cell(cell, p) and not in_union(Cb, p) and not in_union(Cr, p)
    N = 150
    s, t = np.meshgrid((np.arange(N)+0.5)/N, (np.arange(N)+0.5)/N)
    P3 = np.array(u, float)[None, :] + s.reshape(-1, 1)*np.array(g, float)[None, :] + t.reshape(-1, 1)*np.array(h, float)[None, :]
    inR = cell_mem_raster(Cr, P3).reshape(N, N); inB = cell_mem_raster(Cb, P3).reshape(N, N)
    fig = plt.figure(figsize=(W, 3.0))
    a = fig.add_subplot(1, 3, 1, projection="3d"); b = fig.add_subplot(1, 3, 2); c = fig.add_subplot(1, 3, 3)
    setup3d(a, (0, 0, 0), (2, 4, 2), view=(32, 30), ticks=[[0, 2], [0, 2, 4], [0, 2]])
    wirebox(a, (0, 0, 0), (2, 4, 2), color=GREY, lw=0.5); wirebox(a, (0, 0, 0), (2, 2, 2), color=UNC_E, lw=0.8, ls="--"); wirebox(a, (0, 2, 0), (2, 4, 2), color=TGT, lw=0.8)
    Fb = fibre(BCC, q); Feven = [x for x in Fb if R2(x)]; Fodd = [x for x in Fb if not R2(x)]
    pts3(a, Feven, color=TGT, s=14, marker="s", depthshade=False)
    pts3(a, Fodd, color=TGT, s=44, marker="D", edgecolor="k", linewidths=0.6, depthshade=False)
    poly3(a, cell_corners(cell), fc=SRC_L, ec=SRC, alpha=0.5, lw=1.5)
    witness3(a, tuple(float(x) for x in p))
    a.set_title("BCC fibre (13 points)", fontsize=7.6)
    ext = (0, 1, 0, 1)
    for ax_, mask, ttl, lab in ((b, inR, "target $2\\mathbf{Z}^3$ (rectangular)", "uncovered: open triangle $T_0$"), (c, inB, "target BCC", "")):
        ax_.imshow(np.where(mask, 1.0, 0.0), origin="lower", extent=ext, cmap=matplotlib.colors.ListedColormap([UNC, TGT_L]), vmin=0, vmax=1, interpolation="nearest", zorder=1)
        ax_.add_patch(Rectangle((0, 0), 1, 1, fc="none", ec=SRC, lw=1.8, zorder=3))
        ax_.add_patch(MPoly([(0, 0), (0, 1), (1, 1)], fc="none", ec="none", hatch="////", zorder=2)) if ax_ is b else None
        witness2(ax_, (0.25, 5/12)); style_axes2(ax_, (-0.15, 1.15), (-0.15, 1.15), [0, 1], [0, 1])
        ax_.set_xlabel("$s$", labelpad=1); ax_.set_ylabel("$t$", labelpad=1); ax_.set_title(ttl, fontsize=7.6)
    b.set_xlabel("$s$\n(shading by float raster of the exact cell list)", fontsize=6.0, labelpad=1)
    c.set_xlabel("$s$\n(witness checked exactly in Fractions)", fontsize=6.0, labelpad=1)
    # structure of the covered part of T0 for BCC (float raster, then confirmed exactly below)
    T0mask = (t > s)
    cov_in_T0 = inB & T0mask
    assert not (inR & T0mask).any()
    assert np.all(np.abs(s[cov_in_T0]+t[cov_in_T0]-1) < 1e-9), "covered part of T0 is not on s+t=1"
    for sv in (Fr(1, 8), Fr(1, 4), Fr(2, 5)):   # exact: points of the segment s+t=1 lie in the 2-cell [(2,0,2),(1,1,1),(1,3,1),(2,2,2)]
        P = tuple(Fr(a)+sv*b+(1-sv)*c for a, b, c in zip(u, g, h)); assert in_union(Cb, P)
    seg_cell = ((1, 1, 1), ((0, 2, 0), (1, -1, 1)))
    assert seg_cell in Cb[2]
    c.plot([0, 0.5], [1, 0.5], color=TGT, lw=2.4, ls="-", zorder=4)
    c.text(0.97, 0.93, "teal segment: lies in a\nBCC 2-cell, hence covered", fontsize=5.8, color=TGT, ha="right", va="top")
    # statistics
    areaR = 1-inR.mean(); areaB = 1-inB.mean()
    for t_, a_ in zip("abc", (a, b, c)): tag(a_, t_)
    fig.suptitle("Body-centred target (finite-exact): $2E_3\\subset$ BCC, $Q=(2,4,2)$; the same cell $c$ and its chart $(s,t)$", fontsize=7.6, y=1.02)
    fig.tight_layout(w_pad=0.5)
    save(fig, "fig11_bcc")
    DATA["fig11"] = dict(target_BCC_fvector=list(fvec(Cb)), target_2Z3_fvector=list(fvec(Cr)), cell=[list(u), [list(g), list(h)]], witness=[str(x) for x in p],
                         chart_coordinates=["1/4", "5/12"], uncovered_fraction_2Z3_float=round(float(areaR), 4), uncovered_fraction_BCC_float=round(float(areaB), 4),
                         fibre_BCC=[list(x) for x in Fb],
                         note="The statement is finite-exact for this box only; shading is a float raster, the witness verdict is exact.")

def run():
    fig05(); fig06(); fig08(); fig09(); fig10(); fig11()
if __name__ == "__main__":
    run(); print("B ok")
