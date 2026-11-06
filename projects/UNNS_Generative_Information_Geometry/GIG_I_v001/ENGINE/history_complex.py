"""GIG-I v001 -- the inherited higher-dimensional history complex (GEO-HD-1D v003 cell rule), re-implemented.

For a content of k DISTINCT labels, arrangements are permutations of the k labels.  The permutohedral
complex K_A of a set A of admissible arrangements is the full subcomplex of the permutohedron P_k:
  faces of P_k  = ordered set partitions (B_1|...|B_j) of the k label ranks; the face has as vertices the
                  arrangements listing B_1 first (in any order), then B_2, ...; dim = k - j.
  K_A keeps a face iff ALL its vertices belong to A.            (NOT: fill every graph clique.)
Its 1-skeleton is exactly the legal-swap graph (induced subgraph of the permutohedron on A).
Betti numbers are over GF(2).  Contents with repeated labels are outside the inherited complex definition.
"""
from itertools import permutations, combinations
from functools import lru_cache
from history_fibres import is_admissible


@lru_cache(maxsize=None)
def perms(k):
    return list(permutations(range(k)))


@lru_cache(maxsize=None)
def perm_index(k):
    return {p: i for i, p in enumerate(perms(k))}


def _ordered_partitions(k):
    out = []

    def rec(rem, acc):
        if not rem:
            out.append(tuple(acc))
            return
        for r in range(1, len(rem) + 1):
            for B in combinations(rem, r):
                rec([x for x in rem if x not in B], acc + [B])
    rec(list(range(k)), [])
    return out


def _face_vertices(face):
    res = [()]
    for B in face:
        res = [p + q for p in res for q in permutations(B)]
    return res


def _boundary(face):
    out = []
    for i, B in enumerate(face):
        if len(B) < 2:
            continue
        for r in range(1, len(B)):
            for C in combinations(B, r):
                D = tuple(x for x in B if x not in C)
                out.append(face[:i] + (C, D) + face[i + 1:])
    return out


@lru_cache(maxsize=None)
def _complex_data(k):
    """faces with vertex bitmask, dimension, index and boundary (by global face index)."""
    pidx = perm_index(k)
    faces = _ordered_partitions(k)
    fidx = {f: i for i, f in enumerate(faces)}
    mask = []
    for f in faces:
        m = 0
        for v in _face_vertices(f):
            m |= 1 << pidx[v]
        mask.append(m)
    dim = [k - len(f) for f in faces]
    bnd = [[fidx[g] for g in _boundary(f)] for f in faces]
    return faces, mask, dim, bnd


def _gf2_rank(rows):
    piv, rank = {}, 0
    for r in rows:
        while r:
            h = r.bit_length() - 1
            if h in piv:
                r ^= piv[h]
            else:
                piv[h] = r
                rank += 1
                break
    return rank


def vertex_mask(A, k):
    """A: iterable of permutations of range(k)."""
    pidx = perm_index(k)
    m = 0
    for p in A:
        m |= 1 << pidx[tuple(p)]
    return m


def betti(A, k, cubical=False):
    """GF(2) Betti numbers (b_0..b_{k-1}) of the full subcomplex on the arrangement set A (empty set -> all 0)."""
    Am = A if isinstance(A, int) else vertex_mask(A, k)
    faces, mask, dim, bnd = _complex_data(k)
    keep = [i for i in range(len(faces)) if mask[i] & ~Am == 0 and (not cubical or all(len(B) <= 2 for B in faces[i]))]
    bydim = {}
    for i in keep:
        bydim.setdefault(dim[i], []).append(i)
    local = {d: {g: j for j, g in enumerate(L)} for d, L in bydim.items()}
    rk = {0: 0}
    for d, L in bydim.items():
        if d == 0:
            continue
        rows = []
        for g in L:
            r = 0
            for b in bnd[g]:
                r ^= 1 << local[d - 1][b]
            rows.append(r)
        rk[d] = _gf2_rank(rows)
    return tuple(len(bydim.get(d, [])) - rk.get(d, 0) - rk.get(d + 1, 0) for d in range(k))


def admissible_arrangements(content, m0):
    """set of permutations p of range(k) (p[i] = rank of the label in position i) whose arrangement of the
    SORTED distinct content is admissible from m0 (simulation-based)."""
    labs = sorted(content)
    assert len(set(labs)) == len(labs), "complex defined for distinct labels"
    k = len(labs)
    return [p for p in perms(k) if is_admissible(m0, tuple(labs[i] for i in p))]


def induced_adjacency(Aset, k):
    """adjacency (index lists) of the permutohedron graph induced on the permutation set Aset; returns (order, adj)."""
    order = sorted(Aset)
    idx = {p: i for i, p in enumerate(order)}
    adj = [[] for _ in order]
    for p, i in idx.items():
        for j in range(k - 1):
            q = p[:j] + (p[j + 1], p[j]) + p[j + 2:]
            if q in idx:
                adj[i].append(idx[q])
        adj[i].sort()
    return order, adj


def f_vector(A, k):
    """number of faces of the full subcomplex K_A in each dimension 0..k-1."""
    Am = A if isinstance(A, int) else vertex_mask(A, k)
    faces, mask, dim, bnd = _complex_data(k)
    f = [0] * k
    for i in range(len(faces)):
        if mask[i] & ~Am == 0:
            f[dim[i]] += 1
    return tuple(f)


def square_hexagon_counts(A, k):
    """(#square faces, #hexagon faces) present in K_A.  A square face = two commuting adjacent swaps (blocks sizes 2,2,1,..);
    a hexagon face = a braid relation (one block of size 3, rest singletons)."""
    Am = A if isinstance(A, int) else vertex_mask(A, k)
    faces, mask, dim, bnd = _complex_data(k)
    sq = hx = 0
    for i, f in enumerate(faces):
        if mask[i] & ~Am:
            continue
        sizes = sorted(len(B) for B in f)
        if sizes.count(2) == 2 and max(sizes) == 2 and dim[i] == 2:
            sq += 1
        elif dim[i] == 2 and max(sizes) == 3:
            hx += 1
    return sq, hx


def euler_characteristic(A, k):
    return sum((-1) ** d * c for d, c in enumerate(f_vector(A, k)))
