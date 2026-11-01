"""v005 independent 3D tooling (numpy, exact integer arithmetic for lattices; float only for point-in-cell screening with margin 1e-9
that is always re-verified exactly before any verdict).  Shares no code with the v004 builder modules."""
import numpy as np, itertools, math, time

# ---------------------------------------------------------------- lattices (row-style Hermite normal form of Z^3 sublattices)
def hnf3_enum(n):
    out = []
    for a in range(1, n + 1):
        if n % a: continue
        for b in range(1, n // a + 1):
            if (n // a) % b: continue
            c = n // (a * b)
            for x in range(b):
                for y in range(c):
                    for z in range(c):
                        out.append(((a, x, y), (0, b, z), (0, 0, c)))
    return out

def hnf_rows(R):
    rows = [list(map(int, r)) for r in R]
    r = 0
    for col in range(3):
        while True:
            nz = [i for i in range(r, len(rows)) if rows[i][col] != 0]
            if len(nz) <= 1: break
            nz.sort(key=lambda i: abs(rows[i][col]))
            p = nz[0]
            for i in nz[1:]:
                q = rows[i][col] // rows[p][col]
                rows[i] = [x - q * y for x, y in zip(rows[i], rows[p])]
        nz = [i for i in range(r, len(rows)) if rows[i][col] != 0]
        if not nz: raise ValueError("rank deficient")
        p = nz[0]
        rows[r], rows[p] = rows[p], rows[r]
        if rows[r][col] < 0: rows[r] = [-x for x in rows[r]]
        r += 1
    rows = rows[:3]
    for j in (1, 2):
        for i in range(j):
            q = rows[i][j] // rows[j][j]
            rows[i] = [x - q * y for x, y in zip(rows[i], rows[j])]
    return tuple(tuple(r) for r in rows)

def sublattice(Bp, M):
    """lattice with basis rows M @ Bp (M integer 3x3, rows in Bp-coordinates)"""
    Bp = np.array(Bp, dtype=object); M = np.array(M, dtype=object)
    return hnf_rows((M.dot(Bp)).tolist())

def index_of(B): return B[0][0] * B[1][1] * B[2][2]

def member_arr(B, V):
    V = np.asarray(V, dtype=np.int64)
    (a, x, y), (_, b, z), (_, _, c) = B
    i, r = np.divmod(V[..., 0], a); ok = (r == 0)
    v1 = V[..., 1] - i * x; v2 = V[..., 2] - i * y
    j, r = np.divmod(v1, b); ok &= (r == 0)
    v2 = v2 - j * z
    ok &= (np.mod(v2, c) == 0)
    return ok

def member(B, v): return bool(member_arr(B, np.array(v, dtype=np.int64)))

def axis_orders(B):
    ks = []
    for i in range(3):
        for t in range(1, index_of(B) + 1):
            e = [0, 0, 0]; e[i] = t
            if member(B, e): ks.append(t); break
    return tuple(ks)

def contains_lattice(Bp, B):
    return all(member(Bp, r) for r in B)

# ---------------------------------------------------------------- Graver set inside [-Q,Q] (sieve by L1 level)
def lattice_points(B, lo, hi):
    rng = [np.arange(l, h + 1) for l, h in zip(lo, hi)]
    X, Y, Z = np.meshgrid(*rng, indexing='ij')
    V = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1).astype(np.int64)
    V = V[member_arr(B, V)]
    return V[np.any(V != 0, axis=1)]

def graver(B, Q):
    V = lattice_points(B, [-q for q in Q], list(Q))
    l1 = np.abs(V).sum(1); o = np.argsort(l1, kind='stable'); V = V[o]; l1 = l1[o]
    G = np.zeros((0, 3), dtype=np.int64)
    for lev in np.unique(l1):
        W = V[l1 == lev]
        if len(G):
            dom = ((G[None] * W[:, None] >= 0) & (np.abs(G[None]) <= np.abs(W[:, None]))).all(2).any(1)
            W = W[~dom]
        if len(W): G = np.vstack([G, W])
    return G

def lexpos(G):
    G = np.asarray(G)
    if not len(G): return G
    first = np.zeros(len(G), dtype=np.int64)
    for c in (2, 1, 0):
        first = np.where(G[:, c] != 0, G[:, c], first)
    return G[first > 0]

# ---------------------------------------------------------------- hard cells (P4-Z2: m(C)=0 and g^+-, g^- in the target; base is forced)
def hard_generators(Gp, Bprime):
    gp = np.maximum(Gp, 0); gn = np.minimum(Gp, 0)
    ok = member_arr(Bprime, gp) & member_arr(Bprime, gn)
    return Gp[ok]

def _corners_nonzero(u, gens):
    j = len(gens)
    for mask in range(1 << j):
        c = np.array(u, dtype=np.int64)
        for i in range(j):
            if mask >> i & 1: c = c + gens[i]
        if not c.any(): return False
    return True

def hard_cells(Gp, B, Bprime, Qmax, dims=(2, 3)):
    """all hard cells of the pair (B <= Bprime) whose bounding box is <= Qmax.  Returns list of (u, gens(list of np arrays))."""
    H = hard_generators(Gp, Bprime)
    n = len(H); out = []
    if n < 2: return out
    Hp = np.maximum(H, 0); Hn = np.minimum(H, 0)
    Qm = np.array(Qmax)
    if 2 in dims:
        for i in range(n):
            js = np.arange(i + 1, n)
            u = -(Hn[i] + Hn[js])
            top = u + Hp[i] + Hp[js]
            cr = np.cross(H[i], H[js])
            ok = (np.abs(cr).sum(1) > 0) & (top <= Qm).all(1) & member_arr(B, u)
            for j in js[ok]:
                uu = -(Hn[i] + Hn[j])
                if _corners_nonzero(uu, [H[i], H[j]]): out.append((uu, [H[i], H[j]]))
    if 3 in dims and n >= 3:
        for i in range(n):
            for j in range(i + 1, n):
                ks = np.arange(j + 1, n)
                if not len(ks): continue
                u = -(Hn[i] + Hn[j] + Hn[ks])
                top = u + Hp[i] + Hp[j] + Hp[ks]
                det = np.einsum('c,kc->k', np.cross(H[i], H[j]), H[ks])
                ok = (det != 0) & (top <= Qm).all(1) & member_arr(B, u)
                for k in ks[ok]:
                    uu = -(Hn[i] + Hn[j] + Hn[k])
                    if _corners_nonzero(uu, [H[i], H[j], H[k]]): out.append((uu, [H[i], H[j], H[k]]))
    return out

# ---------------------------------------------------------------- target complex  U(Lambda', Q)
class Complex:
    def __init__(self, Bp, Q):
        self.Bp, self.Q = Bp, tuple(Q)
        D = tuple(q + 1 for q in Q)
        pts = lattice_points(Bp, [0, 0, 0], list(Q))
        self.F = pts
        inF = np.zeros(D, dtype=bool); inF[pts[:, 0], pts[:, 1], pts[:, 2]] = True
        self.inF = inF
        Gp = lexpos(graver(Bp, Q)); self.Gp = Gp
        Qa = np.array(Q)
        cells = {0: [], 1: [], 2: [], 3: []}
        def isF(W):
            W = np.asarray(W)
            inb = ((W >= 0) & (W <= Qa)).all(-1)
            res = np.zeros(inb.shape, dtype=bool)
            Wi = W[inb]
            res[inb] = inF[Wi[:, 0], Wi[:, 1], Wi[:, 2]]
            return res
        for u in pts:
            cells[0].append((u, ()))
            idx = np.nonzero(isF(u + Gp))[0]
            m = len(idx)
            for a in idx: cells[1].append((u, (Gp[a],)))
            if m < 2: continue
            PV = np.zeros((m, m), dtype=bool)
            for ia in range(m):
                ga = Gp[idx[ia]]
                W = u + ga + Gp[idx]
                cr = np.abs(np.cross(ga, Gp[idx])).sum(1) > 0
                PV[ia] = isF(W) & cr & (np.arange(m) > ia)
            for ia in range(m):
                for ib in np.nonzero(PV[ia])[0]:
                    cells[2].append((u, (Gp[idx[ia]], Gp[idx[ib]])))
                    cs = np.nonzero(PV[ia] & PV[ib] & (np.arange(m) > ib))[0]
                    if not len(cs): continue
                    gsum = Gp[idx[ia]] + Gp[idx[ib]]
                    ok = isF(u + gsum + Gp[idx[cs]])
                    det = np.einsum('c,kc->k', np.cross(Gp[idx[ia]], Gp[idx[ib]]), Gp[idx[cs]]) != 0
                    for c in cs[ok & det]:
                        cells[3].append((u, (Gp[idx[ia]], Gp[idx[ib]], Gp[idx[c]])))
        self.cells = cells
        self._arrays()

    def _arrays(self):
        """per dimension: base, completed basis inverse, bbox lo/hi"""
        self.arr = {}
        for j in (0, 1, 2, 3):
            L = self.cells[j]
            if not L: self.arr[j] = None; continue
            n = len(L)
            base = np.array([c[0] for c in L], dtype=np.float64)
            lo = np.array([c[0] + sum((np.minimum(g, 0) for g in c[1]), np.zeros(3, dtype=np.int64)) for c in L], dtype=np.int64)
            hi = np.array([c[0] + sum((np.maximum(g, 0) for g in c[1]), np.zeros(3, dtype=np.int64)) for c in L], dtype=np.int64)
            Minv = np.zeros((n, 3, 3))
            for t, c in enumerate(L):
                gs = [np.array(g, dtype=np.float64) for g in c[1]]
                if j == 0: M = np.eye(3)
                elif j == 1:
                    g = gs[0]; e = np.eye(3)[int(np.argmin(np.abs(g)))]
                    n1 = np.cross(g, e); n2 = np.cross(g, n1); M = np.stack([g, n1, n2], 1)
                elif j == 2: M = np.stack([gs[0], gs[1], np.cross(gs[0], gs[1])], 1)
                else: M = np.stack(gs, 1)
                Minv[t] = np.linalg.inv(M)
            self.arr[j] = (base, Minv, lo, hi)

    def covers(self, p, Qc, eps=1e-9):
        """is the point p (float 3-vector) in some cell with bounding box <= Qc ?"""
        p = np.asarray(p, dtype=np.float64)
        for j in (3, 2, 1, 0):
            A = self.arr[j]
            if A is None: continue
            base, Minv, lo, hi = A
            m = (lo - eps <= p).all(1) & (hi + eps >= p).all(1) & (hi <= Qc).all(1)
            if not m.any(): continue
            lam = np.einsum('nij,nj->ni', Minv[m], p - base[m])
            ok = (lam[:, :j] >= -eps).all(1) & (lam[:, :j] <= 1 + eps).all(1)
            if j < 3: ok &= (np.abs(lam[:, j:]) <= eps).all(1)
            if ok.any(): return True
        return False

    def targets_for(self, lo, hi, Qc):
        """cells (all dims) with bbox inside Qc and meeting [lo,hi], as (base tuple, gens tuple) lists"""
        out = []
        for j in (0, 1, 2, 3):
            A = self.arr[j]
            if A is None: continue
            base, Minv, l, h = A
            m = (l <= np.array(hi)).all(1) & (h >= np.array(lo)).all(1) & (h <= Qc).all(1)
            for t in np.nonzero(m)[0]:
                c = self.cells[j][t]
                out.append((tuple(int(x) for x in c[0]), tuple(tuple(int(x) for x in g) for g in c[1])))
        return out

SAMPLES_FINE = [Fr for Fr in ()]
def sample_points(u, gens, denoms=(4, 3)):
    from fractions import Fraction
    vals = sorted({Fraction(k, d) for d in denoms for k in range(1, d)})
    pts = []
    for lam in itertools.product(vals, repeat=len(gens)):
        pts.append(tuple(Fraction(int(u[c])) + sum(l * int(g[c]) for l, g in zip(lam, gens)) for c in range(3)))
    return pts

# ---------------------------------------------------------------- splitting of a target lattice along a coordinate
def _reduce(B, v):
    (a, x, y), (_, b, z), (_, _, c) = B
    v = list(v); i = v[0] // a; v = [v[0] - i * a, v[1] - i * x, v[2] - i * y]
    j = v[1] // b; v = [v[0], v[1] - j * b, v[2] - j * z]
    k = v[2] // c; return (v[0], v[1], v[2] - k * c)

def section_index(B, i):
    """[Z^2 : B cap {z_i=0}] = size of the subgroup of Z^3/B generated by the two other unit vectors"""
    S = [c for c in range(3) if c != i]
    seen = {(0, 0, 0)}; fr = [(0, 0, 0)]
    while fr:
        h = fr.pop()
        for c in S:
            e = [0, 0, 0]; e[c] = 1
            n = _reduce(B, tuple(a + b for a, b in zip(h, e)))
            if n not in seen: seen.add(n); fr.append(n)
    return len(seen)

def split_coordinates(B):
    """coordinates i with B = (B cap {z_i=0}) (+) (B cap Z e_i)  <=>  index = k_i * section_index"""
    ks = axis_orders(B); N = index_of(B)
    return [i for i in range(3) if ks[i] * section_index(B, i) == N]
