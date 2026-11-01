"""GEO_HD_BRIDGE v005 -- A5-T3/T4: the transition calculus for a growth of the occurrence set D -> D' (D subset D').

Everything is computed from the two divisor sets and the interval rule (divisor_complex.py); no frozen-engine call.
  K = K(D),  K' = K(D'),  Dead = cells of K not in K',  New = cells of K' not in K,  K° = K ∩ K' (survivor subcomplex).
Proved structure (theory/MOVE_TRANSITIONS.md):
  (a) non-edges persist; (b) an edge {u,v} dies iff some new occurrence lies in its divisor interval; (c) new edges/cells contain a new vertex;
  (d) a cell dies iff one of its edges dies; (e) K° = K minus Dead is a subcomplex of both K and K'.
Homology (A5-T4):  with r_i = rank(H_i(K°)->H_i(K)), r'_i = rank(H_i(K°)->H_i(K')), h_i = dim H_i(K,K°), h'_i = dim H_i(K',K°):
      beta_i(K) = r_i + h_i - (beta_{i-1}(K°) - r_{i-1}),    Delta beta_i = (h'_i - h_i) + (r'_i - r_i) + (r'_{i-1} - r_{i-1}).
  h_i, h'_i are LOCAL (dead / new cells only); r, r' are the only global terms.  Necessary conditions:  Delta beta_i < 0 => Dead_i or New_{i+1} non-empty;
  Delta beta_i > 0 => New_i or Dead_{i+1} non-empty."""
from divisor_complex import complex_of, betti_ranks, rank_mod, components, edges, _bd
from math import gcd

def cell_key(c, K):
    d, gens = c; vec = K['vec']; inv = K['inv']
    vs = [vec[d]]
    for h in gens: vs = vs + [tuple(a + b for a, b in zip(v, h)) for v in vs]
    return frozenset(inv[v] for v in vs)

def cellsets(K):
    return [{cell_key(c, K): c for c in cs} for cs in K['cells']]

def _nullspace_mod(cols_idx_rows, ncols, nrows, p):
    """left as a helper; see _cycle_space"""
    raise NotImplementedError

def _dense_boundary(Kc, j, rows_keys, cols_keys, K, p):
    """matrix of d_j restricted to given j-cells (cols) -> given (j-1)-cells (rows); entries mod p, as list of column dicts"""
    ridx = {k: i for i, k in enumerate(rows_keys)}
    cols = []
    for k in cols_keys:
        c = Kc[j][k]; col = {}
        for face, sg in _bd(c, K['vec'], K['inv']).items():
            fk = cell_key(face, K)
            if fk in ridx and sg % p: col[ridx[fk]] = col.get(ridx[fk], 0) + sg
        cols.append(col)
    return cols

def _kernel_basis(cols, nrows_unused, p):
    """basis of {c : sum c_i col_i = 0} over GF(p); cols = list of sparse dict columns. returns list of dict(index->coeff)."""
    # gaussian elimination tracking combinations
    piv = {}; basis = []
    for i, col in enumerate(cols):
        c = {k: v % p for k, v in col.items() if v % p}; comb = {i: 1}
        while c:
            k0 = min(c)
            if k0 in piv:
                pc, pcomb = piv[k0]; f = c[k0] * pow(pc[k0], -1, p) % p
                for k, v in pc.items():
                    nv = (c.get(k, 0) - f * v) % p
                    if nv: c[k] = nv
                    else: c.pop(k, None)
                for k, v in pcomb.items():
                    nv = (comb.get(k, 0) - f * v) % p
                    if nv: comb[k] = nv
                    else: comb.pop(k, None)
            else:
                piv[k0] = (c, comb); break
        else:
            basis.append(comb)
    return basis

def analyse_transition(D, D2, p=2, kmax=6):
    D = sorted(set(D)); D2 = sorted(set(D2)); assert set(D) <= set(D2)
    K = complex_of(D, kmax); K2 = complex_of(D2, kmax)
    C1, C2 = cellsets(K), cellsets(K2)
    top = max(len(C1), len(C2)); C1 += [{}] * (top - len(C1)); C2 += [{}] * (top - len(C2))
    surv = [set(C1[j]) & set(C2[j]) for j in range(top)]
    dead = [set(C1[j]) - set(C2[j]) for j in range(top)]
    new = [set(C2[j]) - set(C1[j]) for j in range(top)]
    newv = set(D2) - set(D)
    # --- structural lemmas, checked on this instance
    E1, E2 = K['E'], K2['E']
    pairs_old = {(u, v) for u in D for v in D if u < v}
    chk = {}
    chk['non_edges_persist'] = (E2 & pairs_old) <= E1
    pierced = {(u, v) for (u, v) in E1 if any(gcd(u, v) and w % gcd(u, v) == 0 and (u * v // gcd(u, v)) % w == 0 for w in newv)}
    chk['edge_dies_iff_pierced'] = (E1 - E2) == pierced
    chk['new_edges_touch_new_vertex'] = all(u in newv or v in newv for (u, v) in E2 - E1)
    chk['new_cells_have_new_vertex'] = all(any(v in newv for v in k) for j in range(top) for k in new[j])
    def edge_keys(cell_vs):
        return None
    deadedge = {frozenset(e) for e in E1 - E2}
    def cell_edges(k, j):
        c = C1[j][k]
        # edges of the parallelotope = vertex pairs differing by one generator
        vs = list(k); out = set()
        d, gens = c
        vec = K['vec']; inv = K['inv']
        for v in vs:
            for g in gens:
                w = tuple(a + b for a, b in zip(vec[v], g))
                if w in inv and inv[w] in k: out.add(frozenset((v, inv[w])))
        return out
    chk['cell_dies_iff_edge_dies'] = all((k in dead[j]) == bool(cell_edges(k, j) & deadedge) for j in range(1, top) for k in C1[j])
    chk['survivors_subcomplex'] = True
    # faces of survivors survive: check one level down
    for j in range(2, top):
        for k in surv[j]:
            c = C1[j][k]
            for face in _bd(c, K['vec'], K['inv']):
                if cell_key(face, K) not in surv[j - 1]: chk['survivors_subcomplex'] = False
    # --- homology pieces
    f1, r1, b1 = betti_ranks(K, p); f2, r2, b2 = betti_ranks(K2, p)
    f1 += [0] * (top - len(f1)); f2 += [0] * (top - len(f2)); b1 += [0] * (top - len(b1)); b2 += [0] * (top - len(b2))
    # K° as a complex: survivor cells; compute its Betti numbers & cycle spaces
    surv_keys = [sorted(surv[j], key=lambda k: sorted(k)) for j in range(top)]
    ker_bases = []; bd_surv = []
    for j in range(top):
        if j == 0: ker_bases.append([{i: 1} for i in range(len(surv_keys[0]))]); continue
        cols = _dense_boundary(C1, j, surv_keys[j - 1], surv_keys[j], K, p)
        bd_surv.append(cols)
        ker_bases.append(_kernel_basis(cols, len(surv_keys[j - 1]), p))
    zs = [len(kb) for kb in ker_bases]                        # dim Z_i(K°)
    # rank of B_{i+1}(K°)
    rb = [0] * (top + 1)
    for j in range(1, top): rb[j] = rank_mod(bd_surv[j - 1], p)
    bK0 = [zs[i] - rb[i + 1] for i in range(top)]            # Betti of K°
    # r_i = dim( (Z_i(K°)+B_i(K)) / B_i(K) ) and r'_i likewise for K'
    def rmap(Kbig, Cbig):
        res = []
        for i in range(top):
            bigkeys = sorted(Cbig[i], key=lambda k: sorted(k)); idx = {k: n for n, k in enumerate(bigkeys)}
            # B_i(Kbig): columns = boundaries of (i+1)-cells in rows of i-cells
            cols = []
            if i + 1 < top:
                for k, c in Cbig[i + 1].items():
                    col = {}
                    for face, sg in _bd(c, Kbig['vec'], Kbig['inv']).items():
                        fk = cell_key(face, Kbig)
                        if sg % p: col[idx[fk]] = col.get(idx[fk], 0) + sg
                    cols.append(col)
            rB = rank_mod(cols, p)
            zc = []
            for comb in ker_bases[i]:
                col = {}
                for t, cf in comb.items():
                    k = surv_keys[i][t]; col[idx[k]] = cf
                zc.append(col)
            rBZ = rank_mod(cols + zc, p)
            res.append(rBZ - rB)
        return res
    r_i = rmap(K, C1); rp_i = rmap(K2, C2)
    # relative homology dims: h_i = |Dead_i| - rho_i - rho_{i+1}, rho_j = rank of d_j restricted (dead j-cells -> dead (j-1)-cells)
    def rel(C, dead_or_new):
        keys = [sorted(dead_or_new[j], key=lambda k: sorted(k)) for j in range(top)]
        rho = [0] * (top + 1)
        for j in range(1, top):
            cols = _dense_boundary(C, j, keys[j - 1], keys[j], K if C is C1 else K2, p)
            rho[j] = rank_mod(cols, p)
        return [len(keys[i]) - rho[i] - rho[i + 1] for i in range(top)]
    h = rel(C1, dead); hp = rel(C2, new)
    delta = [b2[i] - b1[i] for i in range(top)]
    formula = []
    for i in range(top):
        rm1 = (rp_i[i - 1] - r_i[i - 1]) if i >= 1 else 0
        formula.append((hp[i] - h[i]) + (rp_i[i] - r_i[i]) + rm1)
    # beta_i(K) reconstruction
    recK = [r_i[i] + h[i] - ((bK0[i - 1] - r_i[i - 1]) if i >= 1 else 0) for i in range(top)]
    recK2 = [rp_i[i] + hp[i] - ((bK0[i - 1] - rp_i[i - 1]) if i >= 1 else 0) for i in range(top)]
    nec = {'destroy_needs_cause': all(not (delta[i] < 0) or bool(dead[i]) or bool(new[i + 1] if i + 1 < top else False) for i in range(top)),
           'create_needs_cause': all(not (delta[i] > 0) or bool(new[i]) or bool(dead[i + 1] if i + 1 < top else False) for i in range(top))}
    return {'D': D, 'D2': D2, 'newv': sorted(newv), 'f': f1, 'f2': f2, 'betti': b1, 'betti2': b2, 'delta': delta,
            'dead': [len(x) for x in dead], 'new': [len(x) for x in new], 'surv': [len(x) for x in surv],
            'beta_surv': bK0, 'r': r_i, 'rp': rp_i, 'h': h, 'hp': hp, 'formula': formula, 'formula_ok': formula == delta,
            'recK_ok': recK == b1, 'recK2_ok': recK2 == b2, 'lemmas': chk, 'nec': nec,
            'comp': (components(D, E1) if D else 0, components(D2, E2))}

def event_type(t):
    """A5-F types from Betti vectors and cell counts"""
    d = t['delta']
    up = any(x > 0 for x in d); dn = any(x < 0 for x in d)
    if up and dn: return 'IV'
    if up: return 'II'
    if dn: return 'III'
    return 'V' if (t['dead'] != [0] * len(t['dead']) or any(t['new'])) else 'I'


# ------------------------------------------------------------------ predictive graph-level update (A5-T4, no rebuilding of K')
def pierced_edges(E_old, newv):
    """old edges killed by the new occurrences: {u,v} in E_old with gcd(u,v) | w | lcm(u,v) for some new w"""
    out = set()
    for (u, v) in E_old:
        g = gcd(u, v); l = u * v // g
        if any(w % g == 0 and l % w == 0 for w in newv): out.add((u, v))
    return out

def new_edges(D, newv):
    """pairs touching a new vertex whose divisor interval holds no other point of D u newv u {1}"""
    pts = set(D) | set(newv) | {1}; out = set()
    D2 = sorted(set(D) | set(newv))
    for w in sorted(newv):
        for v in D2:
            if v == w: continue
            u, vv = (w, v) if w < v else (v, w)
            if (u, vv) in out: continue
            g = gcd(w, v); l = w * v // g
            if not any(z != w and z != v and z % g == 0 and l % z == 0 for z in pts): out.add((u, vv))
    return out

def predict_graph_update(D, newv, E_old=None):
    """returns the predicted (dV, dE, dBeta0, dBeta1) of a D-event from the OLD edge set, the pierced edges and the new vertices' neighbourhoods only.
    Valid (dBeta1 = dE - dV + dBeta0) when neither K nor K' has 2-cells (graph level)."""
    D = sorted(set(D)); newv = sorted(set(newv))
    E_old = edges(D) if E_old is None else E_old
    P = pierced_edges(E_old, newv); N = new_edges(D, newv)
    E_new = (set(E_old) - P) | N
    b0_old = components(D, E_old); b0_new = components(sorted(set(D) | set(newv)), E_new)
    dV = len(newv); dE = len(N) - len(P); db0 = b0_new - b0_old
    return {'dV': dV, 'dE': dE, 'dBeta0': db0, 'dBeta1': dE - dV + db0, 'pierced': sorted(P), 'new_edges': sorted(N)}
