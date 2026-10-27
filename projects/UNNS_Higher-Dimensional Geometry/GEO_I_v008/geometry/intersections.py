"""GEO-III.A  Exact intersection geometry.  Integer / Fraction arithmetic only.

Cells are parallelotopes (u; g_1..g_j) with linearly independent integer generators, as in GEO-I v002.
  seg_relation      : exact edge-edge classification in any ambient dimension (integer Cramer, no Fractions needed)
  point_in_cell     : exact membership
  cell_relation     : disjoint / common_face / non_face for two parallelotopes (exact LP)
  nonempty_common   : exact test that several cells share a point (used for the nerve)
"""
import itertools
from fractions import Fraction as Fr
from exactlp import lp_box

# ----------------------------------------------------------------------------- vectors
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def add(a, b): return tuple(x + y for x, y in zip(a, b))

def cell_vertices(u, gens):
    vs = [tuple(u)]
    for g in gens: vs = vs + [add(v, g) for v in vs]
    return vs                      # index bit i  <->  generator i

def cell_bbox(u, gens):
    vs = cell_vertices(u, gens); k = len(u)
    return [min(v[i] for v in vs) for i in range(k)], [max(v[i] for v in vs) for i in range(k)]

# ----------------------------------------------------------------------------- segment / segment
def _minor_pair(g, h):
    """index pair (i,j) with g_i h_j - g_j h_i != 0, or None if g, h are parallel."""
    k = len(g)
    for i in range(k):
        for j in range(i + 1, k):
            if g[i] * h[j] - g[j] * h[i] != 0: return i, j
    return None

def seg_relation(u, v, r, s):
    """Exact relation of the closed segments [u,v], [r,s] (integer endpoints, any dimension).
    kind in: 'disjoint', 'shared_endpoint', 'endpoint_on_interior', 'interior_cross', 'collinear_overlap', 'collinear_touch'.
    Returns (kind, point) where point is a tuple of Fractions (the unique common point) or None."""
    g = sub(v, u); h = sub(s, r); d = sub(r, u)
    pr = _minor_pair(g, h)
    k = len(u)
    if pr is not None:
        i, j = pr
        D = g[i] * h[j] - g[j] * h[i]
        # t g - lam h = d  (two equations i, j)
        tn = d[i] * h[j] - d[j] * h[i]          # t = tn / D
        ln = d[i] * g[j] - d[j] * g[i]          # lam = ln / D   (derived from Cramer on  t g - lam h = d)
        # verify all coordinates:  tn*g_c - ln*h_c == d_c * D
        for c in range(k):
            if tn * g[c] - ln * h[c] != d[c] * D: return 'disjoint', None
        if D < 0: D, tn, ln = -D, -tn, -ln
        if not (0 <= tn <= D and 0 <= ln <= D): return 'disjoint', None
        t_end = tn in (0, D); l_end = ln in (0, D)
        pt = tuple(Fr(u[c]) + Fr(tn, D) * g[c] for c in range(k))
        if t_end and l_end: return 'shared_endpoint', pt
        if t_end or l_end: return 'endpoint_on_interior', pt
        return 'interior_cross', pt
    # parallel (g,h dependent; both nonzero).  collinear iff d parallel to g
    if _minor_pair(g, d) is not None and any(d): return 'disjoint', None
    # collinear: parametrize along g
    c0 = next(c for c in range(k) if g[c] != 0)
    gg = g[c0]
    a0, a1 = 0, 1                                 # [u,v] -> t in [0,1]
    tr = Fr(r[c0] - u[c0], gg); ts = Fr(s[c0] - u[c0], gg)
    lo, hi = min(tr, ts), max(tr, ts)
    L, H = max(a0, lo), min(a1, hi)
    if L > H: return 'disjoint', None
    if L == H: return 'collinear_touch', tuple(Fr(u[c]) + L * g[c] for c in range(k))
    return 'collinear_overlap', None

# ----------------------------------------------------------------------------- point in cell
def _solve_t(u, gens, x):
    """coordinates t with x - u = sum t_i g_i, or None (exact Gaussian elimination on k x j system)."""
    j = len(gens); k = len(u)
    if j == 0: return () if tuple(x) == tuple(u) else None
    M = [[Fr(gens[c][i]) for c in range(j)] + [Fr(x[i]) - Fr(u[i])] for i in range(k)]
    r = 0; piv = []
    for col in range(j):
        p = next((i for i in range(r, k) if M[i][col] != 0), None)
        if p is None: return None            # generators dependent (should not happen)
        M[r], M[p] = M[p], M[r]
        pv = M[r][col]; M[r] = [v / pv for v in M[r]]
        for i in range(k):
            if i != r and M[i][col] != 0:
                f = M[i][col]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(col); r += 1
    for i in range(r, k):
        if M[i][j] != 0: return None
    return tuple(M[i][j] for i in range(j))

def point_in_cell(x, cell):
    u, gens = cell
    t = _solve_t(u, gens, x)
    return t is not None and all(0 <= ti <= 1 for ti in t)

def cell_in_cell(A, B):
    """A subset of B (both convex): iff every vertex of A lies in B."""
    return all(point_in_cell(v, B) for v in cell_vertices(*A))

# ----------------------------------------------------------------------------- LP assembly
def _system(cells):
    """equations forcing all cells to share a point: x_1 = x_l.  Variables: concatenated t-vectors."""
    k = len(cells[0][0]); sizes = [len(c[1]) for c in cells]; n = sum(sizes)
    offs = [0]
    for s in sizes: offs.append(offs[-1] + s)
    A, b = [], []
    u1, G1 = cells[0]
    for l in range(1, len(cells)):
        ul, Gl = cells[l]
        for coord in range(k):
            row = [Fr(0)] * n
            for i, g in enumerate(G1): row[offs[0] + i] += g[coord]
            for i, g in enumerate(Gl): row[offs[l] + i] -= g[coord]
            A.append(row); b.append(ul[coord] - u1[coord])
    return A, b, n, offs

LP_CALLS = [0]

def nonempty_common(cells):
    if len(cells) == 1: return True
    # bounding-box prefilter (exact)
    boxes = [cell_bbox(*c) for c in cells]; k = len(cells[0][0])
    for i in range(k):
        if max(bx[0][i] for bx in boxes) > min(bx[1][i] for bx in boxes): return False
    A, b, n, _ = _system(cells)
    if n == 0: return all(tuple(c[0]) == tuple(cells[0][0]) for c in cells)
    LP_CALLS[0] += 1
    return lp_box(A, b, [0] * n, n)[0] == 'optimal'

# ----------------------------------------------------------------------------- face tests
def _face_signature(cell, S):
    """If S (set of points) is the vertex set of a face of the parallelotope, return (fixed, eps): the generator indices that are
    frozen and their values.  Else None.  S empty -> None (handled by caller)."""
    u, gens = cell; j = len(gens)
    vs = cell_vertices(u, gens); idx = {v: n for n, v in enumerate(vs)}
    if not S or any(p not in idx for p in S): return None
    bits = [idx[p] for p in S]
    fixed, eps = [], {}
    for i in range(j):
        vals = {(n >> i) & 1 for n in bits}
        if len(vals) == 1: fixed.append(i); eps[i] = vals.pop()
    expect = 1 << (j - len(fixed))
    if len(S) != expect: return None
    return fixed, eps

def cell_relation(P, Q):
    """exact relation of two parallelotopes P=(u,gens), Q=(w,gens').  Returns (kind, info) with
    kind: 'disjoint' | 'common_face' | 'non_face'; info['why'] explains non_face."""
    boxP, boxQ = cell_bbox(*P), cell_bbox(*Q); k = len(P[0])
    for i in range(k):
        if max(boxP[0][i], boxQ[0][i]) > min(boxP[1][i], boxQ[1][i]): return 'disjoint', {}
    if not nonempty_common([P, Q]): return 'disjoint', {}
    VP, VQ = set(cell_vertices(*P)), set(cell_vertices(*Q)); S = VP & VQ
    if not S: return 'non_face', {'why': 'meet_without_common_vertex'}
    sigP, sigQ = _face_signature(P, S), _face_signature(Q, S)
    if sigP is None: return 'non_face', {'why': 'common_vertices_not_a_face_of_first'}
    if sigQ is None: return 'non_face', {'why': 'common_vertices_not_a_face_of_second'}
    # I = P∩Q  must be contained in conv(S), the face of P cut by t_i = eps_i (i fixed)
    A, b, n, offs = _system([P, Q])
    fixed, eps = sigP
    for i in fixed:
        c = [0] * n
        # maximize  |t_i - eps_i|  :  eps=0 -> maximize t_i ; eps=1 -> maximize -t_i (value then compared with -1)
        c[offs[0] + i] = 1 if eps[i] == 0 else -1
        st, val, _ = lp_box(A, b, c, n)
        target = 0 if eps[i] == 0 else -1
        if val != target: return 'non_face', {'why': 'intersection_exceeds_common_face'}
    return 'common_face', {'S': sorted(S)}
