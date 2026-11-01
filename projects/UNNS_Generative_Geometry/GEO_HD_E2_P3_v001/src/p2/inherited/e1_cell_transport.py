"""GEO-HD-1B / E2-P1 -- exact cell complexes K_abs, geometric union U, survival under transport.

Definitions follow GEO-I v002 sec. 1 and v003/v004 sec. 0: a j-cell is a parallelotope
P(u;g_1..g_j), g_i lex-positive, independent, allowed moves, all 2^j corners in the fibre.
K_abs is face-closed; U is the union of the closed parallelotopes in R^k.
All arithmetic is integer / Fraction.  Geometry is done in R^3 (k=3).
"""
from fractions import Fraction
from itertools import combinations, product
from math import gcd

# ---------------------------------------------------------------- linear algebra helpers


def rank_q(rows):
    """Exact rank over Q of sparse rows (dict col->int)."""
    piv, r = {}, 0
    for row in rows:
        row = {c: Fraction(v) for c, v in row.items() if v}
        while row:
            c = min(row)
            if c in piv:
                f = row[c] / piv[c][c]
                for cc, vv in piv[c].items():
                    nv = row.get(cc, 0) - f * vv
                    if nv:
                        row[cc] = nv
                    else:
                        row.pop(cc, None)
            else:
                piv[c] = row
                r += 1
                break
    return r


def int_rank(vectors):
    return rank_q([{i: v for i, v in enumerate(vec) if v} for vec in vectors])


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def primitive_sign(v):
    g = 0
    for t in v:
        g = gcd(g, abs(t))
    if g == 0:
        return None
    v = tuple(t // g for t in v)
    for t in v:
        if t:
            return v if t > 0 else tuple(-s for s in v)


def add(u, g, b=1):
    return tuple(ui + b * gi for ui, gi in zip(u, g))


# ---------------------------------------------------------------- abstract complex K_abs


class Cell:
    __slots__ = ("base", "gens", "verts", "dim", "key")

    def __init__(self, base, gens):
        self.base, self.gens, self.dim = tuple(base), tuple(gens), len(gens)
        vs = []
        for bits in product((0, 1), repeat=self.dim):
            v = self.base
            for b, g in zip(bits, self.gens):
                if b:
                    v = add(v, g)
            vs.append(v)
        self.verts = tuple(sorted(vs))
        self.key = self.verts


def build_complex(F, Gor, kdim):
    """All cells of K_abs: dict dim -> {key: Cell}.  F fibre (tuples), Gor oriented moves."""
    Fs = set(F)
    cx = {0: {(v,): Cell(v, ()) for v in F}}
    Gs = sorted(Gor)
    for j in range(1, kdim + 1):
        cx[j] = {}
        for gens in combinations(Gs, j):
            if int_rank(gens) != j:
                continue
            for u in F:
                c = Cell(u, gens)
                if all(v in Fs for v in c.verts):
                    if c.key in cx[j]:
                        raise AssertionError("duplicate vertex set with different generators")
                    cx[j][c.key] = c
    return cx


def faces_of(cell):
    """All faces (including the cell, excluding nothing) as Cell objects: each generator is
    dropped (face spanned by remaining generators, at base or base+g) or kept."""
    out = {}
    j = cell.dim
    for choice in product((0, 1, 2), repeat=j):  # 0: drop g at 0, 1: drop g at 1, 2: keep
        base, gens = cell.base, []
        for c, g in zip(choice, cell.gens):
            if c == 1:
                base = add(base, g)
            elif c == 2:
                gens.append(g)
        f = Cell(base, gens)
        out[f.key] = f
    return out


def boundary_rows(cx, j):
    """Boundary matrix of j-cells as sparse rows (one row per j-cell)."""
    idx = {key: i for i, key in enumerate(sorted(cx[j - 1]))}
    rows = []
    for key in sorted(cx[j]):
        c = cx[j][key]
        row = {}
        for i, g in enumerate(c.gens):
            rest = c.gens[:i] + c.gens[i + 1:]
            sgn = 1 if i % 2 == 0 else -1
            hi = Cell(add(c.base, g), rest).key
            lo = Cell(c.base, rest).key
            row[idx[hi]] = row.get(idx[hi], 0) + sgn
            row[idx[lo]] = row.get(idx[lo], 0) - sgn
        rows.append({k: v for k, v in row.items() if v})
    return rows


def check_boundary_squared(cx):
    for j in range(2, max(cx) + 1):
        up = boundary_rows(cx, j)
        low = boundary_rows(cx, j - 1)
        for row in up:
            acc = {}
            for col, v in row.items():
                for c2, w in low[col].items():
                    acc[c2] = acc.get(c2, 0) + v * w
            if any(acc.values()):
                return False
    return True


def betti_from_ranks(counts, ranks):
    """counts[j]=#j-simplices/cells, ranks[j]=rank of boundary j->j-1 (ranks[0]=0)."""
    top = len(counts) - 1
    b = []
    for j in range(top + 1):
        up = ranks[j + 1] if j + 1 <= top else 0
        b.append(counts[j] - ranks[j] - up)
    return b


def betti_complex(cx):
    top = max(cx)
    counts = [len(cx[j]) for j in range(top + 1)]
    ranks = [0] + [rank_q(boundary_rows(cx, j)) for j in range(1, top + 1)]
    return betti_from_ranks(counts, ranks)


def f_vector(cx):
    return [len(cx[j]) for j in range(max(cx) + 1)]


def euler(f):
    return sum((-1) ** j * n for j, n in enumerate(f))


def face_maximal(cx):
    """Cells that are not a proper face of another cell."""
    allfaces = set()
    for j in cx:
        for c in cx[j].values():
            for k, f in faces_of(c).items():
                if f.dim < c.dim:
                    allfaces.add(k)
    return [c for j in sorted(cx) for c in cx[j].values() if c.key not in allfaces]


# ---------------------------------------------------------------- geometry: exact candidate points


class Geometry:
    """Exact candidate-vertex machinery for convex polytopes in R^3 whose supporting planes
    belong to a finite plane family.  If the intersection of finitely many cells is nonempty, it
    is a compact polytope, hence has a vertex, hence a point lying on three independent family
    planes.  So a family of cells meets iff some candidate point lies in all of them."""

    def __init__(self, box, generators, extra_points=()):
        self.box = tuple(box)
        normals = set()
        for n in product((-1, 0, 1), repeat=3):
            p = primitive_sign(n)
            if p:
                normals.add(p)
        gs = [g for g in generators]
        for a, b in combinations(gs, 2):
            c = primitive_sign(cross(a, b))
            if c:
                normals.add(c)
        self.normals = sorted(normals)
        pts = list(product(*[range(m + 1) for m in box]))
        planes = set()
        for n in self.normals:
            for p in pts:
                planes.add((n, sum(a * b for a, b in zip(n, p))))
        self.planes = sorted(planes)
        cand = set(pts)
        pl = self.planes
        for (n1, c1), (n2, c2), (n3, c3) in combinations(pl, 3):
            det = (n1[0] * (n2[1] * n3[2] - n2[2] * n3[1]) - n1[1] * (n2[0] * n3[2] - n2[2] * n3[0])
                   + n1[2] * (n2[0] * n3[1] - n2[1] * n3[0]))
            if det == 0:
                continue
            dx = (c1 * (n2[1] * n3[2] - n2[2] * n3[1]) - n1[1] * (c2 * n3[2] - n2[2] * c3)
                  + n1[2] * (c2 * n3[1] - n2[1] * c3))
            dy = (n1[0] * (c2 * n3[2] - n2[2] * c3) - c1 * (n2[0] * n3[2] - n2[2] * n3[0])
                  + n1[2] * (n2[0] * c3 - c2 * n3[0]))
            dz = (n1[0] * (n2[1] * c3 - c2 * n3[1]) - n1[1] * (n2[0] * c3 - c2 * n3[0])
                  + c1 * (n2[0] * n3[1] - n2[1] * n3[0]))
            x = (Fraction(dx, det), Fraction(dy, det), Fraction(dz, det))
            if all(0 <= x[i] <= box[i] for i in range(3)):
                cand.add(x)
        self.cand = sorted(cand)
        den = 1
        for x in self.cand:
            for t in x:
                den = den * Fraction(t).denominator // gcd(den, Fraction(t).denominator)
        self.den = den
        self.scaled = [tuple(int(t * den) for t in x) for x in self.cand]
        self.index = {x: i for i, x in enumerate(self.cand)}
        self._mask = {}

    def mask(self, cell):
        """Bitmask of candidate points lying in the closed cell (exact integer test)."""
        if cell.key in self._mask:
            return self._mask[cell.key]
        D = self.den
        u = cell.base
        gens = cell.gens
        j = len(gens)
        m = 0
        if j == 0:
            m = 1 << self.index[tuple(Fraction(t) for t in u)]
        else:
            rows = None
            for J in combinations(range(3), j):
                A = [[gens[i][r] for i in range(j)] for r in J]
                if j == 1:
                    det, adj = A[0][0], [[1]]
                elif j == 2:
                    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
                    adj = [[A[1][1], -A[0][1]], [-A[1][0], A[0][0]]]
                else:
                    a_ = A
                    det = (a_[0][0] * (a_[1][1] * a_[2][2] - a_[1][2] * a_[2][1])
                           - a_[0][1] * (a_[1][0] * a_[2][2] - a_[1][2] * a_[2][0])
                           + a_[0][2] * (a_[1][0] * a_[2][1] - a_[1][1] * a_[2][0]))
                    adj = [[0] * 3 for _ in range(3)]
                    for r in range(3):
                        for c in range(3):
                            mi = [[a_[(c + 1) % 3][(r + 1) % 3], a_[(c + 1) % 3][(r + 2) % 3]],
                                  [a_[(c + 2) % 3][(r + 1) % 3], a_[(c + 2) % 3][(r + 2) % 3]]]
                            adj[r][c] = mi[0][0] * mi[1][1] - mi[0][1] * mi[1][0]
                if det != 0:
                    rows = (J, det, adj)
                    break
            assert rows is not None
            J, det, adj = rows
            sg = 1 if det > 0 else -1
            for i, Y in enumerate(self.scaled):
                diff = [Y[r] - D * u[r] for r in range(3)]
                tn = [sum(adj[a][b] * diff[J[b]] for b in range(j)) for a in range(j)]
                ok = True
                for r in range(3):  # consistency: sum_i g_i[r]*t_i == diff[r]
                    lhs = sum(gens[a][r] * tn[a] for a in range(j))
                    if lhs != diff[r] * det:
                        ok = False
                        break
                if not ok:
                    continue
                for a in range(j):
                    t = tn[a] * sg
                    if t < 0 or t > abs(det) * D:
                        ok = False
                        break
                if ok:
                    m |= 1 << i
        self._mask[cell.key] = m
        return m

    # ---- point predicates over the candidate set
    def mask_where(self, pred):
        m = 0
        for i, x in enumerate(self.cand):
            if pred(x):
                m |= 1 << i
        return m


def geometric_maximal(cells, geo):
    """Drop cells whose corners all lie in another cell (geometric containment)."""
    ms = [(c, geo.mask(c)) for c in cells]
    vertmask = {}
    for c, _ in ms:
        vm = 0
        for v in c.verts:
            vm |= 1 << geo.index[tuple(Fraction(t) for t in v)]
        vertmask[c.key] = vm
    keep = []
    for c, m in ms:
        vm = vertmask[c.key]
        inside = False
        for c2, m2 in ms:
            if c2.key != c.key and (vm & ~m2) == 0 and (vertmask[c2.key] & ~m) != 0:
                inside = True
                break
            if c2.key != c.key and (vm & ~m2) == 0 and (vertmask[c2.key] & ~m) == 0 and c2.key < c.key:
                inside = True  # identical corner sets impossible; tie-break defensively
                break
        if not inside:
            keep.append(c)
    return keep


# ---------------------------------------------------------------- nerve and homology of U


def nerve_betti(masks, maxdim=3):
    """Betti numbers b_0..b_{maxdim-1} of the nerve of convex sets with given candidate masks
    (nerve theorem: homotopy equivalent to the union).  Simplices up to dimension maxdim."""
    n = len(masks)
    simp = [dict() for _ in range(maxdim + 1)]  # dim -> {tuple: None}
    for i in range(n):
        if masks[i]:
            simp[0][(i,)] = None

    def extend(prefix, m, last):
        d = len(prefix) - 1
        if d == maxdim:
            return
        for k in range(last + 1, n):
            mm = m & masks[k]
            if mm:
                t = prefix + (k,)
                simp[d + 1][t] = None
                extend(t, mm, k)

    for i in range(n):
        if masks[i]:
            extend((i,), masks[i], i)
    counts = [len(s) for s in simp]
    ranks = [0]
    for d in range(1, maxdim + 1):
        idx = {s: i for i, s in enumerate(simp[d - 1])}
        rows = []
        for s in simp[d]:
            row = {}
            for pos in range(len(s)):
                row[idx[s[:pos] + s[pos + 1:]]] = (-1) ** pos
            rows.append(row)
        ranks.append(rank_q(rows))
    # b_j valid for j <= maxdim-1 (needs rank of boundary from dim j+1)
    b = []
    for j in range(maxdim):
        b.append(counts[j] - ranks[j] - ranks[j + 1])
    return {"simplex_counts": counts, "betti": b, "simplices": [sorted(sd) for sd in simp]}


# ---------------------------------------------------------------- embedding test (pairwise common faces)


def is_embedded(maximal_cells, geo, return_witness=False):
    """Face-closed K_abs is embedded iff any two (face-)maximal cells meet in a common face
    (shown in the proof obligations).  Uses exact candidate masks."""
    fm = {}
    for c in maximal_cells:
        fm[c.key] = (c, faces_of(c))
    vm = {}

    def vmask(cell):
        if cell.key not in vm:
            m = 0
            for v in cell.verts:
                m |= 1 << geo.index[tuple(Fraction(t) for t in v)]
            vm[cell.key] = m
        return vm[cell.key]

    items = list(fm.values())
    for i in range(len(items)):
        P, FP = items[i]
        mP = geo.mask(P)
        for jx in range(i + 1, len(items)):
            Q, FQ = items[jx]
            S = mP & geo.mask(Q)
            if S == 0:
                continue

            def has_common(FF, other):
                mo = geo.mask(other)
                for f in FF.values():
                    mf = geo.mask(f)
                    if (vmask(f) & ~mo) == 0 and (S & ~mf) == 0:
                        return True
                return False
            if not (has_common(FP, Q) and has_common(FQ, P)):
                if return_witness:
                    return False, (P.key, Q.key)
                return False
    return (True, None) if return_witness else True


# ---------------------------------------------------------------- survival / transport


def abstract_survival(cx_src, cx_tgt):
    """For every dimension: source cells that are also cells of the target complex."""
    out = {}
    for j in sorted(cx_src):
        s = set(cx_src[j])
        t = set(cx_tgt.get(j, {}))
        out[j] = {"source": len(s), "target": len(t), "preserved": len(s & t),
                  "lost": len(s - t), "new": len(t - s)}
    return out


def corner_region_status(cell, geo, ones_masks, le1_mask):
    """Is the closed cell inside Y = {x in box : max_i x_i >= 1}?  P subset Y iff
    W = P cap [0,1]^3 is empty or lies in one plane {x_i=1}."""
    S = geo.mask(cell) & le1_mask
    if S == 0:
        return "CONTAINED"
    for m1 in ones_masks:
        if (S & ~m1) == 0:
            return "CONTAINED"
    return "PARTIAL"


# ---------------------------------------------------------------- integer lattice generated by vectors


def hnf_index(vectors, k):
    """Index [Z^k : span_Z(vectors)] (None if the span has rank < k).  Integer row reduction."""
    rows = [list(v) for v in vectors if any(v)]
    det = 1
    for col in range(k):
        # Euclid on column `col` among remaining rows
        while True:
            nz = [r for r in rows if r[col] != 0]
            if len(nz) <= 1:
                break
            nz.sort(key=lambda r: abs(r[col]))
            piv = nz[0]
            for r in nz[1:]:
                f = r[col] // piv[col]
                for c in range(k):
                    r[c] -= f * piv[c]
        nz = [r for r in rows if r[col] != 0]
        if not nz:
            return None
        piv = nz[0]
        det *= abs(piv[col])
        rows.remove(piv)
        rows = [r for r in rows if any(r)]
    return det
