"""GEO-I v009, Programme C: exact engine and orbit enumeration for reduced binary boxes of arbitrary nullity k (used for k = 3,4,5).

A REDUCED box of nullity k is a set Sigma of p distinct nonzero points of F_2^k spanning F_2^k; coordinate sigma carries the functional u -> u.sigma, so the code is
C = { c_u = (u.sigma)_{sigma in Sigma} : u in F_2^k } (dimension k).  Everything below works on explicit codeword bitmasks, never on 2^n enumerations.
 deletion of coordinate sigma0 = the subcode { c_u : u.sigma0 = 0 } on the same coordinates (coordinate sigma0 becomes identically zero)  [v006 definition].
Cells with union U: (S = pairwise disjoint circuits with union U, coset x+span(S) in C, x not in span(S));  centre key (U, x outside U);  collision = two distinct cells, same key.
Independent of binary_01.py (different code path; cross-checked in tests)."""
import itertools, os, sys
from fractions import Fraction as Fr


def code_masks(sig):
    """all 2^k codewords (including 0) as p-bit masks for the support list sig (points = ints in 1..2^k-1)."""
    k = max(sig).bit_length() if sig else 0
    k = max(k, 1)
    out = []
    for u in range(1 << 11 if False else 1 << max(1, max(s.bit_length() for s in sig))):
        m = 0
        for i, s in enumerate(sig):
            if bin(u & s).count('1') & 1: m |= 1 << i
        out.append(m)
    return sorted(set(out))


def circuits_of_code(C):
    nz = sorted((c for c in C if c), key=lambda x: bin(x).count('1')); circ = []
    for x in nz:
        if not any((c & x) == c for c in circ): circ.append(x)
    return circ


def disjoint_families(circ):
    def rec(i, chosen, used):
        if chosen: yield tuple(chosen), used
        for j in range(i, len(circ)):
            if circ[j] & used == 0: yield from rec(j + 1, chosen + [circ[j]], used | circ[j])
    yield from rec(0, [], 0)


def span_set(S):
    sp = {0}
    for m in S: sp |= {a ^ m for a in sp}
    return sp


def collisions(C):
    """list of (U, x, S, y, T): distinct cells (S,x),(T,y) with the same centre key.  C = list of all codewords incl. 0."""
    circ = circuits_of_code(C); cells = {}
    for S, U in disjoint_families(circ):
        sp = span_set(S); seen = set()
        for x in C:
            if x in sp: continue
            co = min(x ^ f for f in sp)
            if co in seen: continue
            seen.add(co); cells.setdefault((U, x & ~U), []).append((S, x))
    out = []
    for (U, xo), lst in cells.items():
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)): out.append((U, lst[a][1], lst[a][0], lst[b][1], lst[b][0]))
    return out


def has_collision(C):
    circ = circuits_of_code(C); cells = {}
    for S, U in disjoint_families(circ):
        if len(S) < 2: continue                                 # F1: collisions need >= 2 circuits per cell
        sp = span_set(S); seen = set()
        for x in C:
            if x in sp: continue
            co = min(x ^ f for f in sp)
            if co in seen: continue
            seen.add(co); k = (U, x & ~U)
            if k in cells: return True
            cells[k] = 1
    return False


def embedded(C): return not has_collision(C)


def delete(C, i): return [c for c in C if not (c >> i) & 1]


def minimal(C, n):
    return (not embedded(C)) and all(embedded(delete(C, i)) for i in range(n))


def witness_rank(n, S, x, T, y):
    g = [[(1 - 2 * ((x >> i) & 1)) if (m >> i) & 1 else 0 for i in range(n)] for m in S]
    h = [[(1 - 2 * ((y >> i) & 1)) if (m >> i) & 1 else 0 for i in range(n)] for m in T]
    M = [[Fr(v) for v in r] for r in g + h]; rk = 0
    for col in range(n):
        p = next((i for i in range(rk, len(M)) if M[i][col] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][col] != 0:
                f = M[i][col] / M[rk][col]; M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk


def min_rank(C, n):
    return min(witness_rank(n, S, x, T, y) for U, x, S, y, T in collisions(C))


# ------------------------------------------------------------------------------------------------ orbit enumeration (GL(k,2) on subsets of PG(k-1,2))
def point_invariants(sig):
    """cheap isomorphism invariants per point: (#3-circuits through it, #4-circuits through it)."""
    S = set(sig); inv = {}
    for s in sig:
        t3 = sum(1 for a in sig if a != s and (a ^ s) in S and a < (a ^ s)) if True else 0
        t4 = 0
        for a, b in itertools.combinations([x for x in sig if x != s], 2):
            if (a ^ b ^ s) in S and (a ^ b ^ s) not in (a, b, s) and (a ^ b ^ s) > max(a, b): t4 += 1
        inv[s] = (t3, t4)
    return inv


def fingerprint(sig):
    inv = point_invariants(sig); return (len(sig), tuple(sorted(inv.values())))


def rank_of(points):
    basis = []
    for v in points:
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    return len(basis)


def apply_map(cols_images, v, k):
    """linear map sending e_i -> cols_images[i]; v an int."""
    r = 0
    for i in range(k):
        if (v >> i) & 1: r ^= cols_images[i]
    return r


def isomorphic(A, B, k):
    """exact GL(k,2) isomorphism test of two subsets (lists of points) of F_2^k."""
    if len(A) != len(B): return False
    if rank_of(A) != rank_of(B): return False
    r = rank_of(A)
    invA = point_invariants(A); invB = point_invariants(B); Bs = set(B)
    # choose r independent points of A, with rarest invariants first
    from collections import Counter
    cnt = Counter(invA.values()); order = sorted(A, key=lambda s: (cnt[invA[s]], s)); basis = []
    for s in order:
        if rank_of(basis + [s]) > len(basis): basis.append(s)
        if len(basis) == r: break
    # express every point of A in the basis (coordinates) -- requires A to span a subspace of dim r; work in that subspace
    def coords(v):
        # solve v = sum c_i basis_i over F2 by brute force elimination
        rows = [(b, 1 << i) for i, b in enumerate(basis)]; red = []
        for b, tag in rows:
            for pb, ptag in red:
                if b ^ pb < b: b ^= pb; tag ^= ptag
            if b: red.append((b, tag)); red.sort(reverse=True)
        c = 0
        for pb, ptag in sorted(red, reverse=True):
            if v ^ pb < v: v ^= pb; c ^= ptag
        return c if v == 0 else None
    cA = {s: coords(s) for s in A}
    cand = [[t for t in B if invB[t] == invA[b]] for b in basis]
    def rec(i, chosen):
        if i == len(basis):
            return {sum(((cA[s] >> j) & 1) * 0 for j in range(len(basis))) or _img(cA[s], chosen) for s in A} == Bs
        for t in cand[i]:
            if t in chosen: continue
            if rank_of(chosen + [t]) <= len(chosen): continue
            if rec(i + 1, chosen + [t]): return True
        return False
    def _img(c, chosen):
        r_ = 0
        for j in range(len(chosen)):
            if (c >> j) & 1: r_ ^= chosen[j]
        return r_
    return rec(0, [])


def orbit_representatives(k, maxsize=None, verbose=False):
    """representatives of all GL(k,2)-orbits of nonempty subsets of F_2^k\\0 (every size), by growing one point at a time.  returns dict size -> list of sorted tuples."""
    pts = list(range(1, 1 << k)); level = {1: [(1,)]}; allreps = {1: [(1,)]}
    top = maxsize or len(pts)
    for m in range(2, top + 1):
        buckets = {}; reps = []
        for R in level[m - 1]:
            for p in pts:
                if p in R: continue
                cand = tuple(sorted(R + (p,))); fp = fingerprint(cand)
                lst = buckets.setdefault(fp, [])
                if any(isomorphic(list(cand), list(o), k) for o in lst): continue
                lst.append(cand); reps.append(cand)
        level[m] = reps; allreps[m] = reps
        if verbose: print('size', m, 'orbits', len(reps), flush=True)
    return allreps
