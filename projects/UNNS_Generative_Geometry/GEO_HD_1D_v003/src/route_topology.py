r"""HD-1D v003 builder (D-Q2): route complexes of a content of DISTINCT labels.

Permutohedral complex K_A : faces of the permutohedron P_k = ordered set partitions (B_1|...|B_j) of {0..k-1}; a face has the
    permutations that list B_1 first, then B_2, ... as vertices; dim = k - j.  K_A keeps a face iff ALL its vertices lie in A.
Cubical complex Q_A       : the subcomplex of K_A on faces with all |B_i| <= 2 (cubes = sets of independent adjacent swaps).
A is a set of permutations of range(k) (positions -> label rank).  Betti numbers over GF(2).
Dual (Alexander) picture  : for A != S_k, K_A sits in the sphere bdry P_k = S^{k-2} and  K_A ~ S^{k-2} \ N(R) with
    N(R) the nerve of the non-admissible set R = S_k \ A (simplices = subsets of R inside a common PROPER face)."""
from itertools import permutations, combinations
from functools import lru_cache


def ordered_partitions(k):
    """all ordered set partitions of range(k) as tuples of sorted tuples"""
    out = []
    def rec(rem, acc):
        if not rem: out.append(tuple(acc)); return
        rem = list(rem)
        for r in range(1, len(rem) + 1):
            for B in combinations(rem, r):
                rec([x for x in rem if x not in B], acc + [B])
    rec(range(k), [])
    return out


def face_vertices(face):
    res = [()]
    for B in face:
        res = [p + q for p in res for q in permutations(B)]
    return res


def boundary(face):
    out = []
    for i, B in enumerate(face):
        if len(B) < 2: continue
        for r in range(1, len(B)):
            for C in combinations(B, r):
                D = tuple(x for x in B if x not in C)
                out.append(face[:i] + (C, D) + face[i + 1:])
    return out


def gf2_rank(rows):
    """rows: list of python ints (bitsets)"""
    piv = {}; rank = 0
    for r in rows:
        while r:
            h = r.bit_length() - 1
            if h in piv: r ^= piv[h]
            else: piv[h] = r; rank += 1; break
    return rank


@lru_cache(maxsize=None)
def _faces(k): return ordered_partitions(k)


@lru_cache(maxsize=None)
def _fverts(k): return {f: frozenset(face_vertices(f)) for f in _faces(k)}


def betti(A, k, cubical=False):
    """GF(2) Betti numbers (b_0..b_{k-1}) and Euler characteristic of the full subcomplex on vertex set A"""
    A = frozenset(A); fv = _fverts(k)
    faces = [f for f in _faces(k) if fv[f] <= A and (not cubical or all(len(B) <= 2 for B in f))]
    bydim = {}
    for f in faces: bydim.setdefault(k - len(f), []).append(f)
    idx = {d: {f: i for i, f in enumerate(L)} for d, L in bydim.items()}
    rk = {}
    for d in bydim:
        if d == 0: rk[d] = 0; continue
        rows = []
        for f in bydim[d]:
            m = 0
            for g in boundary(f): m ^= 1 << idx[d - 1][g]
            rows.append(m)
        rk[d] = gf2_rank(rows)
    b = []
    for d in range(k):
        n = len(bydim.get(d, []))
        b.append(n - rk.get(d, 0) - rk.get(d + 1, 0))
    chi = sum((-1) ** d * len(bydim.get(d, [])) for d in range(k))
    return tuple(b), chi


def nerve_components(R, k):
    """number of components of the nerve of R (non-admissible vertices; adjacent iff in a common PROPER face)"""
    R = list(R); fv = _fverts(k); proper = [f for f in _faces(k) if len(f) >= 2]
    par = {v: v for v in R}
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    Rs = set(R)
    for f in proper:
        inside = [v for v in fv[f] if v in Rs]
        for v in inside[1:]: par[find(v)] = find(inside[0])
    return len({find(v) for v in R})
