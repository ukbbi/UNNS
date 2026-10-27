"""GEO-I v007, Programme B: the witness-rank functional and its exact reduction.

For a collision (A,B) the v005 obstruction witness is (A,B,delta) with delta = y - x (difference of the base points).  Its rank is
 rank{ generators of A, generators of B, delta }.
THEOREM B-DELTA (proved).  delta lies in the span of the generators (at the common centre): on U,  y-x = (s_x - s_y)/2 with s_x = 1-2x = sum_j g_j, s_y = sum_l h_l, and
delta = 0 outside U.  Hence  witness rank = rank{g_1..g_r,h_1..h_t} <= r+t.
THEOREM B-ATOM (proved for r=t=2, full support).  With atoms S_i cap T_j and z = x xor y, the four generators are dependent (rank<=3) iff some connected component of the
atom graph has z constant on every atom and consistent signs eps = 1-2z around its cycle (for the 4-cycle: eps_11 eps_22 = eps_12 eps_21).
This module computes ranks exactly and checks both theorems on every collision of a box."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import binary_01 as B, centre_collisions as CC


def gens(n, cell):
    corners, x, S = cell
    return [B.gen_vec(x, m, n) for m in S]


def witness_rank(n, a, b):
    g = gens(n, a) + gens(n, b)
    (_, x, _), (_, y, _) = a, b
    delta = [((y >> i) & 1) - ((x >> i) & 1) for i in range(n)]
    return B.rank_int(g + [delta]), B.rank_int(g)


def atom_criterion(n, a, b):
    """exact prediction of 'generator rank <= 3' for r=t=2 cells with union U (Theorem B-ATOM).  Bipartite graph on {S_1,S_2} u {T_1,T_2}, one edge per non-empty atom
    S_i cap T_j carrying eps = 1 - 2 z_k (z = x xor y) if z is constant on the atom; a non-constant atom 'kills' (forces 0 on) both endpoints.  A non-zero dependency
    (alpha_i = eps_ij gamma_j on every edge) exists iff some connected component has only constant-z edges and consistent signs around its (at most one) cycle."""
    (_, x, S), (_, y, T) = a, b
    z = x ^ y; edges = {}
    for i in range(2):
        for j in range(2):
            at = S[i] & T[j]
            if at == 0: continue
            vals = {(z >> k) & 1 for k in range(n) if at >> k & 1}
            edges[(i, j)] = (1 - 2 * vals.pop()) if len(vals) == 1 else None
    verts = [('S', 0), ('S', 1), ('T', 0), ('T', 1)]; seen = set()
    for v in verts:
        if v in seen: continue
        comp = {v: 1}; stack = [v]; ok = True; seen.add(v)
        while stack:
            u = stack.pop()
            for (i, j), e in edges.items():
                if u == ('S', i): w = ('T', j)
                elif u == ('T', j): w = ('S', i)
                else: continue
                if e is None: ok = False; continue
                want = comp[u] * e
                if w in comp:
                    if comp[w] != want: ok = False
                else: comp[w] = want; seen.add(w); stack.append(w)
        if ok: return True
    return False


def check_box(cols):
    n = len(cols); res = {'delta_in_span': True, 'atom_ok': True, 'min_rank': None, 'n_coll': 0}
    for cen, a, b in CC.collisions(cols):
        res['n_coll'] += 1
        rk, rg = witness_rank(n, a, b)
        if rk != rg: res['delta_in_span'] = False
        res['min_rank'] = rk if res['min_rank'] is None else min(res['min_rank'], rk)
        if len(a[2]) == 2 and len(b[2]) == 2 and cen[0] == (1 << n) - 1:
            if (rg <= 3) != atom_criterion(n, a, b): res['atom_ok'] = False
    return res
