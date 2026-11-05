"""Transition calculus (independent): D -> D' growth, zig-zag K <- K0 -> K' over GF(2) with bitset linear algebra."""
import sys; sys.path.insert(0,'.')
from eng3 import *
from eng3 import _bd
def xor_basis(vs):
    """returns dict lead->vec"""
    b = {}
    for v in vs:
        while v:
            h = v.bit_length() - 1
            if h in b: v ^= b[h]
            else: b[h] = v; break
    return b
def rk(vs): return len(xor_basis(vs))
def kernel(cols):
    """cols: list of ints (images). return list of ints (bitsets over column indices) spanning kernel"""
    piv = {}; ker = []
    for i, c in enumerate(cols):
        comb = 1 << i
        while c:
            h = c.bit_length() - 1
            if h in piv: pc, pm = piv[h]; c ^= pc; comb ^= pm
            else: piv[h] = (c, comb); break
        else: ker.append(comb)
    return ker
def analyse(D, D2):
    D = sorted(set(D)); D2 = sorted(set(D2)); assert set(D) <= set(D2)
    K = complex_of(D); K2 = complex_of(D2)
    C1, C2 = cellsets(K), cellsets(K2); top = max(len(C1), len(C2)) + 1
    C1 += [set()] * (top - len(C1)); C2 += [set()] * (top - len(C2))
    surv = [C1[j] & C2[j] for j in range(top)]
    dead = [C1[j] - C2[j] for j in range(top)]; new = [C2[j] - C1[j] for j in range(top)]
    newv = set(D2) - set(D)
    # structural claims
    E1, E2 = K['E'], K2['E']
    old_pairs = {(u, v) for u in D for v in D if u < v}
    chk = {}
    chk['non_edges_persist'] = (E2 & old_pairs) <= E1
    pierced = {(u, v) for (u, v) in E1 if any(w % gcd(u, v) == 0 and lcm(u, v) % w == 0 for w in newv)}
    chk['edge_dies_iff_pierced'] = (E1 - E2) == pierced
    chk['new_edges_have_new_vertex'] = all(u in newv or v in newv for (u, v) in E2 - E1)
    chk['new_cells_have_new_vertex'] = all(all(c & newv for c in new[j]) for j in range(1, top))
    chk['cell_dies_iff_edge_dies'] = all(
        (c in dead[j]) == any(frozenset(e) in {frozenset(p) for p in pierced} for e in itertools_pairs(c, E1)) for j in range(2, top) for c in C1[j])
    chk['K0_is_intersection_subcomplex'] = all(surv[j] == C1[j] - dead[j] for j in range(top))
    # Betti numbers
    def bet(Kc): return betti(Kc, 2)[2] if Kc['cells'][0] else []
    b1 = bet(K); b2 = bet(K2)
    # survivor complex: cells = surv ; build boundaries by vertex-set faces
    def bd_faces(c, j, Kc):  # faces of cell with vertex set c: we use Kc boundary via stored tuple
        pass
    # Use cell lists with boundary computed through K / K2 objects (cells keyed by vertex set)
    def cellmap(Kc):
        out = []
        for j, cs in enumerate(Kc['cells']):
            m = {}
            for cell in cs:
                d, gens = cell; vs = [Kc['vec'][d]]
                for h in gens: vs = vs + [tuple(a + b for a, b in zip(v, h)) for v in vs]
                m[frozenset(Kc['inv'][v] for v in vs)] = cell
            out.append(m)
        return out
    M1 = cellmap(K); M1 += [{}] * (top - len(M1))
    def faces(key_j, cell, Kc):
        res = []
        for f, s in _bd(cell, Kc).items():
            if s % 2:
                d, gens = f; vs = [Kc['vec'][d]]
                for h in gens: vs = vs + [tuple(a + b for a, b in zip(v, h)) for v in vs]
                res.append(frozenset(Kc['inv'][v] for v in vs))
        return res
    # index cells of K by dimension for bitset encoding
    idx = [{k: i for i, k in enumerate(sorted(M1[j], key=lambda s: sorted(s)))} for j in range(top)]
    M2 = cellmap(K2); M2 += [{}] * (top - len(M2))
    idx2 = [{k: i for i, k in enumerate(sorted(M2[j], key=lambda s: sorted(s)))} for j in range(top)]
    def bdmat(M, ix, Kc, j, keys=None):
        keys = list(M[j]) if keys is None else keys
        cols = []
        for k in keys:
            v = 0
            for f in faces(k, M[j][k], Kc):
                v ^= 1 << ix[j - 1][f]
            cols.append(v)
        return keys, cols
    def cycles_and_boundaries(M, ix, Kc, subkeys):
        """Z_j(K0) as bitsets over the j-cells of Kc (embedding), B_j(Kc) bitsets."""
        Z = []; B = []
        for j in range(top):
            if j == 0:
                Z.append([1 << ix[0][k] for k in subkeys[0]])
            else:
                keys = list(subkeys[j]); _, cols = bdmat(M, ix, Kc, j, keys)
                ker = kernel(cols)
                Z.append([sum(1 << ix[j][keys[i]] for i in range(len(keys)) if (kv >> i) & 1) for kv in ker])
            if j + 1 < top:
                keys = list(M[j + 1]); _, cols = bdmat(M, ix, Kc, j + 1, keys); B.append(cols)
            else: B.append([])
        return Z, B
    surv_keys = [list(surv[j]) for j in range(top)]
    Z1, B1 = cycles_and_boundaries(M1, idx, K, surv_keys)
    Z2, B2 = cycles_and_boundaries(M2, idx2, K2, surv_keys)
    r1 = [rk(Z1[j] + B1[j]) - rk(B1[j]) for j in range(top)]   # rank H_j(K0)->H_j(K)
    r2 = [rk(Z2[j] + B2[j]) - rk(B2[j]) for j in range(top)]
    # beta(K0)
    K0 = {'cells': None}
    b0 = []
    for j in range(top):
        zj = rk(Z1[j])
        # B_j(K0) = boundaries of surviving (j+1)-cells
        if j + 1 < top and surv_keys[j + 1]:
            _, cols = bdmat(M1, idx, K, j + 1, surv_keys[j + 1]); bj = rk(cols)
        else: bj = 0
        b0.append(zj - bj)
    # relative homology H_j(K,K0): chain group on dead cells, boundary mod survivors
    def rel(M, ix, Kc, deadk):
        h = []; rr = [0] * (top + 1)
        for j in range(1, top):
            keys = list(deadk[j]); cols = []
            for k in keys:
                v = 0
                for f in faces(k, M[j][k], Kc):
                    if f in set(deadk[j - 1]): v ^= 1 << (sorted(deadk[j - 1], key=lambda s: sorted(s)).index(f))
                cols.append(v)
            rr[j] = rk(cols)
        return [len(deadk[j]) - rr[j] - rr[j + 1] for j in range(top)]
    hh = rel(M1, idx, K, dead); hh2 = rel(M2, idx2, K2, new)
    pad = lambda l: l + [0] * (top - len(l))
    b1, b2 = pad(b1), pad(b2)
    db = [b2[i] - b1[i] for i in range(top)]
    zz = [ (hh2[i]-hh[i]) + (r2[i]-r1[i]) + ((r2[i-1]-r1[i-1]) if i>0 else 0) for i in range(top)]
    chk['zigzag_identity'] = (db == zz)
    # reconstruction beta_i(K) = r_i + h_i - (beta_{i-1}(K0) - r_{i-1})
    rec1 = [r1[i] + hh[i] - ((b0[i-1] - r1[i-1]) if i > 0 else 0) for i in range(top)]
    rec2 = [r2[i] + hh2[i] - ((b0[i-1] - r2[i-1]) if i > 0 else 0) for i in range(top)]
    chk['reconstruct'] = (rec1 == b1 and rec2 == b2)
    f1 = [len(C1[j]) for j in range(top)]; f2 = [len(C2[j]) for j in range(top)]
    chk['euler_local'] = (sum((-1)**j * (f2[j] - f1[j]) for j in range(top)) == sum((-1)**j * (len(new[j]) - len(dead[j])) for j in range(top)))
    chk['cause_criteria'] = all((db[i] >= 0 or len(dead[i]) > 0 or len(new[i+1] if i+1<top else []) > 0) and
                                (db[i] <= 0 or len(new[i]) > 0 or len(dead[i+1] if i+1<top else []) > 0) for i in range(top))
    return {'b': b1, 'b2': b2, 'db': db, 'f': f1, 'f2': f2, 'dead': [len(x) for x in dead], 'new': [len(x) for x in new],
            'surv': [len(x) for x in surv], 'r': r1, 'r2': r2, 'h': hh, 'h2': hh2, 'b0': b0, 'chk': chk, 'nnew': len(newv),
            'pierced': len(pierced), 'newedges': len(E2 - E1)}
def itertools_pairs(c, E):
    c = list(c); return [(u, v) for u in c for v in c if u < v and (u, v) in E]
def etype(t):
    db = t['db']
    if all(x == 0 for x in db): return 'V'     # a vertex is always added, Type I impossible
    up = any(x > 0 for x in db); dn = any(x < 0 for x in db)
    return 'IV' if up and dn else ('II' if up else 'III')
if __name__ == '__main__':
    t = analyse([55], [10, 22, 55]); print(t)
