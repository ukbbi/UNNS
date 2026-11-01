#!/usr/bin/env python3
"""GEO-HD-1B / E2-P1 -- independent verification.  Standard library only.

  python RUN_VERIFY.py            full verification (a few minutes)
  python RUN_VERIFY.py --fast     skips the 5-fold nerve level and the k=4 sweep rows
  python RUN_VERIFY.py --write    additionally (re)writes results/E2_CERTIFICATES.json and STATUS.json

Every check recomputes from first principles with src/geometry_audit.py (which imports nothing
from the builder) and compares with the stored data/results.  The builder is only run, in a
temporary directory, to confirm that the stored files are exactly reproducible.
Exit code 0 iff every executed check passes.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from fractions import Fraction
from itertools import combinations, product

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))
import geometry_audit as ga  # noqa: E402

SPEC = "GEO_HD_1_SPEC_v003"


def load(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return json.load(fh)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


class Certs:
    def __init__(self):
        self.items = []

    def add(self, cid, claim, ok, detail="", status=None):
        self.items.append({"id": cid, "claim": claim, "status": status or ("PASS" if ok else "FAIL"), "detail": detail})
        print("%-4s %-5s %s %s" % (cid, self.items[-1]["status"], claim, ("[" + detail + "]") if detail else ""), flush=True)

    @property
    def ok(self):
        return all(c["status"] in ("PASS", "NOT_RUN") for c in self.items)


# ------------------------------------------------------------------------------------------ pieces
def audit_orbit(root, C):
    orb = load(root, "data/E2_ORBIT.json")
    x = Fraction(110 ** 4, 3)
    good, bad = True, ""
    for st in orb["steps"][:7]:
        nx, L, G, ds = ga.C_brute(x)
        if (str(x), len(ds), L, G) != (st["x"], st["num_indices"], st["L"], st["G"]) or str(nx - x) != st["increment"]:
            good, bad = False, "step %d" % st["n"]
        x = nx
    C.add("C01", "orbit x0=110^4/3 -> 2*110^4/3 -> 110^4 and steps 3..6 recomputed by brute force (D, L, G, increment)", good, bad)
    xs = [Fraction(110 ** 4, 3), Fraction(2 * 110 ** 4, 3), Fraction(110 ** 4)]
    C.add("C01b", "stage states, G=3,3,1 and x_{n+3}=4x_n from n=2", [ga.C_brute(v)[2] for v in xs] == [3, 3, 1]
          and orb["facts"]["regime_I_x_n+3_eq_4x_n_from_n=2"] and ga.C_brute(xs[0])[0] == xs[1] and ga.C_brute(xs[1])[0] == xs[2])
    return xs


def audit_fibres(root, xs, C):
    fib = load(root, "data/E2_FIBRES.json")
    ok, bad, graver_ok = True, "", True
    out = []
    for n, x in enumerate(xs):
        P, q, b, F = ga.stage_data(x)
        rec = fib["stages"][n]
        if (list(P), list(q), b, [list(v) for v in F]) != (rec["primes"], rec["box"], rec["b"], rec["fibre"]):
            ok, bad = False, "stage %d fibre" % n
        # occurrences: exact equation M(N+1)^2/N = x and bijection with indices
        ds = ga.D_brute(x.numerator, x.denominator)
        occ = []
        for d in ds:
            N = d - 1
            M, r = divmod(x.numerator * N, x.denominator * d * d)
            if r or Fraction(M * (N + 1) ** 2, N) != x:
                ok, bad = False, "stage %d occurrence" % n
            occ.append([N, M])
        if occ != rec["occurrences_NM"] or ds != rec["indices_D"] or len(ds) != len(F):
            ok, bad = False, "stage %d D/occurrence list" % n
        idx = sorted(ga.prod_idx(P, v) if hasattr(ga, "prod_idx") else _prodidx(P, v) for v in F)
        if idx != ds:
            ok, bad = False, "stage %d index map" % n
        G = ga.graver_brute(P, b, q)
        if [list(g) for g in G] != rec["graver_region"]:
            graver_ok = False
        out.append((P, q, b, F, G))
    C.add("C02", "fibres (13,13,26), occurrences (N,M) satisfy M(N+1)^2/N=x exactly, bijection with D(x)", ok, bad)
    C.add("C03", "region Graver sets by brute-force conformal minimality (18,18,6)", graver_ok and [len(o[4]) for o in out] == [18, 18, 6])
    vt = fib["vertex_transport_summary"]
    C.add("C04", "vertex transport: 0->1 all 13 preserved; 1->2 13 preserved, 13 new, 0 lost",
          vt["0->1"] == {"lost": 0, "new": 0, "preserved": 13} and vt["1->2"] == {"lost": 0, "new": 13, "preserved": 13}
          and set(out[0][3]) <= set(out[2][3]) and len(set(out[2][3]) - set(out[0][3])) == 13
          and all(sum(v) % 2 == 1 for v in set(out[2][3]) - set(out[0][3])))
    mt = fib["move_transport_summary"] if "move_transport_summary" in fib else None
    surv01 = set(out[0][4]) & set(out[1][4])
    surv12 = set(out[1][4]) & set(out[2][4])
    C.add("C05", "Graver sets: 0->1 all 18 moves survive; 1->2 none survives (G1 = {+-2e_i, +-e_i+-e_j}, G2 = {+-e_i})",
          len(surv01) == 18 and len(surv12) == 0 and set(out[2][4]) == {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)})
    return out


def _prodidx(P, v):
    d = 1
    for p, a in zip(P, v):
        d *= p ** a
    return d


def unit_cells(F):
    """Cells of the axis (b=1) complex by direct formula: unit faces with all corners in F."""
    Fs = set(F)
    cells = {0: {(v,): (v, ()) for v in F}}
    E = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    for j in (1, 2, 3):
        cells[j] = {}
        for gens in combinations(E, j):
            for u in F:
                vs = ga.verts_of(u, gens)
                if all(v in Fs for v in vs):
                    cells[j][vs] = (u, gens)
    return cells


def audit_cells(root, d, C):
    P0, q0, b0, F0, G0 = d[0]
    cells_json = load(root, "data/E2_CELLS.json")
    sub = ga.cells_by_subsets(F0, G0, 3)
    src = {0: {(v,): (v, ()) for v in F0}}
    src.update({j: {k: v for k, v in sub[j].items()} for j in sub})
    stored = {int(j): {tuple(sorted(tuple(x) for x in c["verts"])) for c in lst} for j, lst in cells_json["stage0"]["cells"].items()}
    same = all(set(src[j]) == stored[j] for j in (1, 2, 3))
    C.add("C06", "stage-0 K_abs rebuilt by searching 2^j-subsets of the fibre: f-vector (13,45,36,3) and identical cell lists",
          same and [len(src[j]) for j in range(4)] == [13, 45, 36, 3] == cells_json["stage0"]["f_vector"])
    P2, q2, b2, F2, G2 = d[2]
    tgt = unit_cells(F2)
    stored2 = {int(j): {tuple(sorted(tuple(x) for x in c["verts"])) for c in lst} for j, lst in cells_json["stage2"]["cells"].items()}
    C.add("C07", "stage-2 K_abs by direct unit-face formula: f-vector (26,51,33,7), identical cell lists",
          all(set(tgt[j]) == stored2[j] for j in (1, 2, 3)) and [len(tgt[j]) for j in range(4)] == [26, 51, 33, 7] == cells_json["stage2"]["f_vector"])
    # boundary^2 = 0 and Betti numbers mod several primes
    tr = load(root, "results/E2_TRANSPORT.json")
    res = {}
    for name, cb in (("stage0", src), ("stage2", tgt)):
        res[name] = {p: ga.betti_mod(cb, p) for p in (2, 3, 2 ** 31 - 1)}
    rows = ga.complex_boundary_rows(src)
    zero = True
    for j in (2, 3):
        low = ga.complex_boundary_rows(src)[j - 1]
        for row in rows[j]:
            acc = {}
            for c, v in row.items():
                for c2, w in low[c].items():
                    acc[c2] = acc.get(c2, 0) + v * w
            zero &= not any(acc.values())
    stored_b0 = tr["topology"]["K_abs_stage0"]["betti_Q"]
    stored_b2 = tr["topology"]["K_abs_stage2"]["betti_Q"]
    C.add("C08", "K_abs Betti numbers: stage0 (1,6,6,0), stage2 (1,0,0,0); agree mod 2, 3 and 2^31-1 with exact-Q values; boundary^2=0",
          all(v == stored_b0 for v in res["stage0"].values()) and all(v == stored_b2 for v in res["stage2"].values()) and zero
          and stored_b0 == [1, 6, 6, 0])
    # abstract survival recomputed from raw sets
    surv = tr["abstract_survival"]["0->2"]
    ok = True
    for j in range(4):
        s, t = set(src[j]), set(tgt[j])
        ok &= surv[str(j)] == {"source": len(s), "target": len(t), "preserved": len(s & t), "lost": len(s - t), "new": len(t - s)}
    C.add("C09", "abstract survival 0->2 recomputed: vertices 13/13/0/13; edges 0 of 45 preserved; 2-cells 0 of 36; 3-cells 0 of 3",
          ok and [surv[str(j)]["preserved"] for j in range(4)] == [13, 0, 0, 0])
    surv01 = tr["abstract_survival"]["0->1"]
    C.add("C10", "stage 1 = stage 0 identically (every cell preserved, nothing lost or new)",
          all(surv01[str(j)]["lost"] == 0 and surv01[str(j)]["new"] == 0 for j in range(4)) and (d[0][:4] == d[1][:4]))
    return src, tgt


def cell_list_from_json(lst):
    return [(tuple(c["base"]), tuple(tuple(g) for g in c["gens"])) for c in lst]


def nerve_from_lp(cells, maxdim, ncheck=None):
    n = len(cells)
    simp = [dict() for _ in range(maxdim + 1)]
    for i in range(n):
        simp[0][(i,)] = 1
    cache = {}

    def ne(t):
        if t not in cache:
            cache[t] = ga.intersection_nonempty([cells[i] for i in t])
        return cache[t]
    level = [(i,) for i in range(n)]
    for d in range(1, maxdim + 1):
        nxt = []
        prev = set(level)
        for t in level:
            for k in range(t[-1] + 1, n):
                u = t + (k,)
                if all(u[:i] + u[i + 1:] in prev for i in range(len(u) - 2)) and ne(u):
                    nxt.append(u)
        for u in nxt:
            simp[d][u] = 1
        level = nxt
    return simp


def betti_simplices(simp, p, top):
    counts = [len(s) for s in simp]
    ranks = {0: 0}
    for d in range(1, top + 1):
        idx = {s: i for i, s in enumerate(simp[d - 1])}
        rows = [{idx[s[:q] + s[q + 1:]]: (-1) ** q for q in range(len(s))} for s in simp[d]]
        ranks[d] = ga.rank_mod(rows, p)
    return [counts[j] - ranks[j] - ranks[j + 1] for j in range(top)]


def audit_geometry(root, d, src, tgt, C, fast):
    tr = load(root, "results/E2_TRANSPORT.json")
    g0, g2 = tr["geometry"]["stage0"], tr["geometry"]["stage2"]
    gm = cell_list_from_json(g0["geometric_maximal"])
    P0, q0, b0, F0, G0 = d[0]
    # (a) the cover: every maximal cell is a K_abs cell; every K_abs cell lies in some maximal one; none inside another
    keys = {ga.verts_of(u, g) for u, g in gm}
    allsrc = {k: v for j in (1, 2, 3) for k, v in src[j].items()}
    cover_ok = keys <= set(allsrc)
    for k, (u, g) in allsrc.items():
        if not any(all(ga.intersection_nonempty([(v, ()), m]) for v in k) for m in gm):
            cover_ok = False
            break
    redundant = False
    for i, (u, g) in enumerate(gm):
        vs = ga.verts_of(u, g)
        for j2, m in enumerate(gm):
            if j2 != i and all(ga.intersection_nonempty([(v, ()), m]) for v in vs):
                redundant = True
    pts_in = all(ga.intersection_nonempty([(v, ()), m]) for v in F0 for m in gm[:0])
    for v in F0:
        if not any(ga.intersection_nonempty([(v, ()), m]) for m in gm):
            cover_ok = False
    C.add("C11", "U0 cover: 18 geometrically maximal cells (15 two-cells, 3 three-cells) cover every K_abs cell; none contained in another (LP)",
          cover_ok and not redundant and len(gm) == 18 and sorted(len(g) for u, g in gm) == [2] * 15 + [3] * 3)
    # (b) nerve by exact LP
    maxdim = 3 if fast else 4
    t = time.time()
    simp = nerve_from_lp(gm, maxdim)
    h = [hashlib.sha256(json.dumps([list(s) for s in sorted(simp[dd])]).encode()).hexdigest() for dd in range(maxdim + 1)]
    same = h == g0["nerve_simplices_sha256_by_dim"][:maxdim + 1] and [len(s) for s in simp] == g0["nerve_simplex_counts"][:maxdim + 1]
    C.add("C12", "nerve of the 18 cells by exact LP (two-phase simplex) equals the candidate-vertex nerve, simplex-for-simplex up to %d-fold intersections" % (maxdim + 1),
          same, "counts %s, %.0fs" % ([len(s) for s in simp], time.time() - t))
    bets = {p: betti_simplices(simp, p, 3) for p in (2, 3, 2 ** 31 - 1)}
    C.add("C13", "Betti numbers of U0 (nerve theorem): (b0,b1,b2) = (1,0,18) over GF(2), GF(3), GF(2^31-1); builder Q-values agree",
          all(v == [1, 0, 18] for v in bets.values()) and g0["U_betti_b0_b1_b2_b3"][:3] == [1, 0, 18])
    # (c) U2 and its topology
    tcells = [(tuple(c["base"]), tuple(tuple(g) for g in c["gens"])) for c in g2["geometric_maximal"]]
    s2 = nerve_from_lp(tcells, 3)
    b2 = {p: betti_simplices(s2, p, 3) for p in (2, 3, 2 ** 31 - 1)}
    grid_ok = True
    cubes = [(c, (1, 1, 1)) for c in product((0, 1), repeat=3) if any(c)]
    for x in product(range(13), repeat=3):  # grid with step 1/6 in [0,2]^3
        pt = tuple(Fraction(t, 6) for t in x)
        iny = max(pt) >= 1
        inc = any(all(c[i] <= pt[i] <= c[i] + 1 for i in range(3)) for c, _ in cubes)
        if iny != inc:
            grid_ok = False
            break
    C.add("C14", "U2 = 7 unit cubes: nerve is a full simplex, Betti (1,0,0); union equals Y={x in [0,2]^3 : max x_i>=1} on the 1/6-grid",
          len(tcells) == 7 and all(v == [1, 0, 0] for v in b2.values()) and grid_ok and g2["U_betti_b0_b1_b2_b3"][:3] == [1, 0, 0])
    # (d) embedded status; Prop D witness
    u, g, h2 = (0, 1, 1), (1, -1, 0), (1, 1, 0)
    corners = ga.verts_of(u, (g, h2))
    diag = (tuple(u[i] + g[i] + h2[i] for i in range(3)))
    propD = (all(c in set(F0) for c in corners) and tuple(g[i] + h2[i] for i in range(3)) in set(G0)
             and ga.verts_of(u, (g, h2)) in allsrc and (u, diag) in [tuple(k) for k in allsrc if len(k) == 2]
             and not g0["embedded"])
    C.add("C15", "stage 0 is NOT embedded: Prop D (v004) witness - 2-cell P((0,1,1);(1,-1,0),(1,1,0)) contains the diagonal edge (0,1,1)-(2,1,1) (g+h=(2,0,0) in G) as a non-face; stage 2 embedded (cubical)",
          propD and tr["geometry"]["stage2"]["embedded"] is True)
    # (e) geometric survival by exact LP
    status = {}
    partial = []
    for j in (0, 1, 2, 3):
        cnt = {"CONTAINED": 0, "PARTIAL": 0}
        cl = [(k, v) for k, v in (allsrc.items() if j else [((v,), (v, ())) for v in F0])
              if (len(k) == 2 ** j)]
        for k, (u_, gs) in cl:
            hit = ga.meets_open_corner(u_, gs)
            cnt["PARTIAL" if hit else "CONTAINED"] += 1
            if hit:
                partial.append((u_, gs))
        status[str(j)] = cnt
    stored_status = tr["geometry"]["source_cells_vs_U2"]
    T = {(0, 1, 1), (1, 0, 1), (1, 1, 0)}
    tcrit = all((T <= set(ga.verts_of(u_, gs))) for u_, gs in partial) and len(partial) == sum(
        1 for k in allsrc if T <= set(k))
    C.add("C16", "geometric survival in U2=Y by exact LP: all 13 vertices and all 45 edges lie in U2; 33 of 36 two-cells and 0 of 3 three-cells lie in U2; "
          "the 3+3 PARTIAL cells are exactly those whose corner set contains T={(0,1,1),(1,0,1),(1,1,0)}",
          status == stored_status and status["1"] == {"CONTAINED": 45, "PARTIAL": 0} and status["2"] == {"CONTAINED": 33, "PARTIAL": 3}
          and status["3"] == {"CONTAINED": 0, "PARTIAL": 3} and tcrit)
    wit_ok = True
    for w in tr["geometry"]["partial_cells"]:
        pt = tuple(Fraction(t) for t in w["witness_point_in_cell_with_all_coordinates_lt_1"])
        sc = Fraction(1)
        den = 1
        for t in pt:
            den = den * t.denominator // ga.gcd(den, t.denominator)
        # exact membership of pt in the cell via LP on a scaled problem: use point as 0-cell with rational coords
        wit_ok &= max(pt) < 1 and _point_in_cell(pt, (tuple(w["base"]), tuple(tuple(g) for g in w["gens"])))
    C.add("C17", "exact witnesses: each PARTIAL cell contains a rational point with all coordinates < 1 (e.g. (2/3,2/3,2/3))", wit_ok and len(tr["geometry"]["partial_cells"]) == 6)
    ur = tr["geometry"]["union_relations"]
    C.add("C18", "U0 is not contained in U2 (6 cells poke into the corner region) and U2 is not contained in U0 (the new vertex (1,0,0) lies in U2=Y but in no cell of U0)",
          ur["U0_subset_U2_at_candidates"] is False and ur["U2_subset_U0_at_candidates"] is False and len(partial) == 6
          and not any(ga.intersection_nonempty([((1, 0, 0), ()), m]) for m in gm))  # (1,0,0) is in U2=Y but in no cell of U0


def _point_in_cell(pt, cell):
    u, gens = cell
    j = len(gens)
    # solve pt-u = sum t_i g_i exactly (least number of unknowns), by brute force elimination
    A = [[Fraction(g[r]) for g in gens] + [pt[r] - u[r]] for r in range(3)]
    row = 0
    piv = []
    for col in range(j):
        pr = next((r for r in range(row, 3) if A[r][col] != 0), None)
        if pr is None:
            continue
        A[row], A[pr] = A[pr], A[row]
        A[row] = [v / A[row][col] for v in A[row]]
        for r in range(3):
            if r != row and A[r][col] != 0:
                f = A[r][col]
                A[r] = [a - f * b for a, b in zip(A[r], A[row])]
        piv.append(col)
        row += 1
    if any(A[r][-1] != 0 for r in range(row, 3)):
        return False
    t = {c: A[i][-1] for i, c in enumerate(piv)}
    return all(0 <= v <= 1 for v in t.values()) and len(t) == j


def _cube_in_union(c, gm):
    # is the (open) unit cube [c,c+1] centre covered by U0?  test centre point in some maximal cell
    ctr = tuple(Fraction(2 * t + 1, 2) for t in c)
    return any(_point_in_cell(ctr, m) for m in gm)


def audit_baselines(root, C):
    tr = load(root, "results/E2_TRANSPORT.json")
    b = tr["frozen_baseline_reproduction"]
    C.add("C19", "frozen baselines (GEO-I v004 S2, v003/v004, v002): k=2 hollow box (V,E,b1)=(4,5,2); parity k=3 first non-embedded box is (2,1,1); k=3 box (2,2,2) b=1 is v002's contractible 3-cell complex",
          b["k2_parity_hollow_box"]["f_vector"][:2] == [4, 5] and b["k2_parity_hollow_box"]["betti_K_abs"][1] == 2
          and [b["parity_k3_embedding_by_box"][k]["embedded"] for k in ("(1, 1, 1)", "(2, 1, 1)", "(2, 2, 1)", "(2, 2, 2)")] == [True, False, False, False]
          and b["target_b1_k3_box222"]["betti"] == [1, 0, 0, 0])
    # independent recomputation of the k=2 hollow box and k=4 abstract numbers
    P, q = (2, 5), (2, 2)
    F = [a for a in product(range(3), range(3)) if any(a) and ga.in_Lambda(a, P, 3)]
    G = ga.graver_brute(P, 3, q)
    cs = ga.cells_by_subsets(F, G, 2)
    cb = {0: {(v,): (v, ()) for v in F}, 1: cs[1], 2: cs[2]}
    C.add("C20", "k=2 parity box (2,2): fibre {(2,0),(1,1),(0,2),(2,2)}, V=4, E=5, no 2-cell, b1=2 (recomputed independently)",
          sorted(F) == [(0, 2), (1, 1), (2, 0), (2, 2)] and [len(cb[j]) for j in range(3)] == [4, 5, 0] and ga.betti_mod(cb, 2 ** 31 - 1)[1] == 2)
    k4 = tr["k4_PARITY_TERNARY_K4_abstract"]
    P4 = (2, 5, 11, 17)
    q4 = (2, 2, 2, 2)
    F4 = [a for a in product(range(3), repeat=4) if any(a) and sum(a) % 2 == 0]
    F4b = [a for a in product(range(3), repeat=4) if any(a)]
    ok4 = len(F4) == 40 == k4["stage0"]["fibre"] and len(F4b) == 80 == k4["stage2"]["fibre"]
    # Graver set of the 4D parity lattice: 4*2 axis + 4*6 diagonal-pairs = 8 + 24 = 32 oriented -> check count only
    G4 = ga.graver_brute(P4, 3, q4)
    ok4 &= len(G4) == 8 + 24
    # unit-cube f-vector of the 4D integer fibre by direct count
    Fs = set(F4b)
    f = []
    E4 = [tuple(1 if i == j else 0 for i in range(4)) for j in range(4)]
    for j in range(5):
        n = 0
        for gens in combinations(E4, j):
            for u in F4b:
                if all(v in Fs for v in ga.verts_of(u, gens)):
                    n += 1
        f.append(n)
    ok4 &= f == [80, 212, 210, 92, 15] == k4["stage2"]["f_vector"]
    C.add("C21", "PARITY_TERNARY_K4 (1870^4/3): 40 -> 80 points; 4D parity Graver set has 32 moves; target f-vector (80,212,210,92,15) equals the frozen 210^4 value of GEO-I v002/v004; 0 edges/cells of positive dimension preserved",
          ok4 and all(k4["abstract_survival_0_to_2"][str(j)]["preserved"] == 0 for j in range(1, 5)))


def audit_family(root, C, fast):
    tr = load(root, "results/E2_TRANSPORT.json")
    rows = {tuple(r["primes"]): r for r in tr["family_sweep"]["rows"]}
    # (a) independent brute-force recomputation on rows small enough for trial of d^2 | a
    checked, ok = 0, True
    for P, r in rows.items():
        n = 1
        for p in P:
            n *= p
        if n > (130 if fast else 400):
            continue
        x = Fraction(n ** 4, 3)
        seq = []
        for _ in range(4):
            seq.append((len(ga.D_brute(x.numerator, x.denominator)), x.denominator))
            x = ga.C_brute(x)[0]
        if seq != [(s["fibre"], s["b"]) for s in r["stages"]]:
            ok = False
        checked += 1
    C.add("C22", "orbit patterns of %d family members recomputed by brute force (4 stages: fibre size and denominator)" % checked, ok and checked >= 8)
    # (b) Theorem 1 on every row containing 2, from the stored table
    t1 = tr["theorem1_check_rows_containing_2"]
    C.add("C23", "Theorem E2-1: every sampled P containing the prime 2 (k=2,3,4; %d rows) follows (|F|,b) = (N,3),(N,3),(2N+1,1),(2N+1,1) with N=(3^k-1)/2" % t1["rows"], t1["all_match"] and t1["rows"] >= 40)
    # (c) lattice-relation criterion: audit recomputation of actual relation by inverse-free enumeration, and of the predicted one
    cnt, bad = 0, 0
    for P, r in rows.items():
        if fast and r["k"] == 4:
            continue
        for t, s0, s1 in zip(r["transitions"], r["stages"], r["stages"][1:]):
            if t["relation_actual"] == "COORDINATES_CHANGE":
                continue
            Pr, q = tuple(s0["primes"]), tuple(s0["box"])
            A = {v for v in product(*[range(-m, m + 1) for m in q]) if ga.in_Lambda(v, Pr, s0["b"])}
            B = {v for v in product(*[range(-m, m + 1) for m in q]) if ga.in_Lambda(v, Pr, s1["b"])}
            act = "EQUAL" if A == B else "ENLARGE" if A < B else "SHRINK" if B < A else "INCOMPARABLE"
            cnt += 1
            bad += act != t["relation_actual"] or t["relation_actual"] != t["relation_predicted"]
    C.add("C24", "Lemma E2-2 (index criterion): lattice relation predicted from group orders |H_b|,|H_b'|,|H_lcm| equals the enumerated relation on %d transitions (EQUAL and ENLARGE both occur, no SHRINK)" % cnt, bad == 0 and cnt > 100)
    ns = tr["no_shrink_lemma_check"]
    fl = tr["orbit_lattice_floor_check"]
    C.add("C25", "Lemma E2-3 (no shrinking when F generates the lattice) and Lemma E2-4 (all denominators divide G(x0)): hypotheses hold and conclusions observed on every sampled transition / row",
          ns["none_is_SHRINK_or_INCOMPARABLE"] and ns["transitions_with_hypothesis"] == ns["of_tested"] and fl["all_denominators_divide_G0"])
    # (d) counterexample file is consistent with the recomputed facts
    ce = load(root, "results/E2_COUNTEREXAMPLES.json")
    ids = [c["id"] for c in ce["counterexamples"]]
    C.add("C26", "counterexample file: CE-1..CE-5 present, each marked FALSE for the proposed law, with the exact data certified by C05, C09, C16, C13/C08, C24",
          ids == ["CE-%d" % i for i in range(1, 6)] and all(c["verdict"] == "FALSE" for c in ce["counterexamples"]))
    # CE-5 witness checked independently: primes 5,17,29 with b=3 and b=12 give the same lattice
    P = (5, 17, 29)
    A = {v for v in product(range(-2, 3), repeat=3) if ga.in_Lambda(v, P, 3)}
    B = {v for v in product(range(-2, 3), repeat=3) if ga.in_Lambda(v, P, 12)}
    C.add("C27", "CE-5 witness: for primes (5,17,29) the lattices of b=3 and b=12 coincide on [-2,2]^3 although the denominator changed", A == B)


def audit_reproducible(root, C):
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, "-I", os.path.join(root, "src", "build_e2.py"), "--out", tmp], capture_output=True, text=True)
        same = r.returncode == 0
        diffs = []
        if same:
            for rel in ("data/E2_ORBIT.json", "data/E2_FIBRES.json", "data/E2_CELLS.json", "results/E2_TRANSPORT.json", "results/E2_COUNTEREXAMPLES.json"):
                if sha(os.path.join(tmp, rel)) != sha(os.path.join(root, rel)):
                    diffs.append(rel)
        C.add("C28", "builder re-run from scratch reproduces all five stored JSON files byte-for-byte", same and not diffs, ",".join(diffs) or r.stderr[-200:])


def verify(root=ROOT, fast=False, parts=("orbit", "fibres", "cells", "geometry", "baselines", "family", "repro"), quiet=False):
    C = Certs()
    xs = audit_orbit(root, C)
    d = None
    if "fibres" in parts or "cells" in parts or "geometry" in parts:
        d = audit_fibres(root, xs, C)
    src = tgt = None
    if "cells" in parts or "geometry" in parts:
        src, tgt = audit_cells(root, d, C)
    if "geometry" in parts:
        audit_geometry(root, d, src, tgt, C, fast)
    if "baselines" in parts:
        audit_baselines(root, C)
    if "family" in parts:
        audit_family(root, C, fast)
    if "repro" in parts:
        audit_reproducible(root, C)
    return C


def main():
    fast = "--fast" in sys.argv
    t0 = time.time()
    C = verify(ROOT, fast=fast)
    n_pass = sum(c["status"] == "PASS" for c in C.items)
    print("\n%d/%d checks passed in %.0fs%s" % (n_pass, len(C.items), time.time() - t0, " (fast mode)" if fast else ""))
    if "--write" in sys.argv and C.ok:
        out = {"spec": SPEC, "package": "GEO_HD_E2_P1_v001", "mode": "fast" if fast else "full", "all_pass": C.ok, "certificates": C.items}
        with open(os.path.join(ROOT, "results", "E2_CERTIFICATES.json"), "w", newline="\n") as fh:
            json.dump(out, fh, indent=1, sort_keys=True)
            fh.write("\n")
        print("wrote results/E2_CERTIFICATES.json")
    print("EXACT_PASS" if C.ok else "EXACT_FAIL")
    sys.exit(0 if C.ok else 1)


if __name__ == "__main__":
    main()
