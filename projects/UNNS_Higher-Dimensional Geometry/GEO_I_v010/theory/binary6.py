"""GEO-I v010, Programme C: partition criterion, full-support/affine reduction and nullity-six engine.

THEOREM G10-E1 (exact criterion).  A binary 0/1 box with code C is non-embedded  iff  there are two DISTINCT partitions S != T of one set U into circuits of C
(circuit = minimal support of a nonzero codeword).  Proof: see MATHEMATICS.md section 1.  This module implements the criterion independently of the cell machinery.
THEOREM G10-F1 (full support).  In a minimal non-embedded box every such pair has U = [n], hence the all-ones word lies in C (this is G8-C3).
COROLLARY G10-A1 (affine reduction).  The reduced support of a minimal box of nullity k lies in the affine hyperplane {sigma : u0.sigma = 1}, u0 unique, so it is a subset of AG(k-1,2)
with at most 2^(k-1) points, spanning; boxes are equivalent iff the subsets are AGL(k-1,2)-equivalent."""
import itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import binary5 as B5


def partition_pairs(C):
    """dict: union -> list of distinct circuit partitions (tuples) of that union (families with >= 2 circuits; a 1-circuit family can never collide)."""
    circ = B5.circuits_of_code(C); out = {}
    for S, U in B5.disjoint_families(circ):
        if len(S) >= 2: out.setdefault(U, []).append(S)
    return out


def non_embedded(C):
    """criterion G10-E1 (families of >= 2 circuits suffice: a 1-circuit partition {U} of U forces every other partition of U to equal it)."""
    circ = B5.circuits_of_code(C); seen = {}
    for S, U in B5.disjoint_families(circ):
        if len(S) < 2: continue
        if U in seen: return True
        seen[U] = S
    return False


def first_pair(C):
    circ = B5.circuits_of_code(C); seen = {}
    for S, U in B5.disjoint_families(circ):
        if len(S) < 2: continue
        if U in seen: return U, seen[U], S
        seen[U] = S
    return None


def double_two_decomposition(C):
    """W2: a codeword that is a disjoint union of two circuits in two distinct ways; returns (U, (a,b), (c,d)) or None."""
    circ = B5.circuits_of_code(C); d = {}
    for a, b in itertools.combinations(circ, 2):
        if a & b == 0:
            u = a | b
            if u in d and d[u] != (a, b): return u, d[u], (a, b)
            d.setdefault(u, (a, b))
    return None


def minimal_criterion(C, n):
    return non_embedded(C) and all(not non_embedded(B5.delete(C, i)) for i in range(n))


def all_ones(C, n): return ((1 << n) - 1) in set(C)


# ----------------------------------------------------------------------------------------------- affine orbit enumeration
def weight_enum(sig):
    from collections import Counter
    k = max(s.bit_length() for s in sig)
    return tuple(sorted(Counter(bin(m).count('1') for m in B5.code_masks(sig)).items()))


def strong_invariants(sig):
    """per-point invariant: number of codewords of each weight having a 1 at the point, plus the (3-circuit, 4-circuit) counts."""
    from collections import Counter
    C = B5.code_masks(sig); base = B5.point_invariants(sig); out = {}
    for i, s in enumerate(sig):
        cnt = Counter(bin(m).count('1') for m in C if (m >> i) & 1)
        out[s] = (tuple(sorted(cnt.items())), base[s])
    return out


def affine_fingerprint(sig):
    inv = strong_invariants(sig)
    return (len(sig), weight_enum(sig), tuple(sorted(inv.values())))


def isomorphic_strong(A, B, k):
    """exact GL(k,2) isomorphism of two point sets using strong per-point invariants (backtracking over images of an invariant-rare basis)."""
    if len(A) != len(B): return False
    if B5.rank_of(A) != B5.rank_of(B): return False
    r = B5.rank_of(A); invA = strong_invariants(A); invB = strong_invariants(B); Bs = set(B)
    if sorted(invA.values()) != sorted(invB.values()): return False
    from collections import Counter
    cnt = Counter(invA.values()); order = sorted(A, key=lambda s: (cnt[invA[s]], s)); basis = []
    for s in order:
        if B5.rank_of(basis + [s]) > len(basis): basis.append(s)
        if len(basis) == r: break
    def coords(v):
        red = []
        for i, b in enumerate(basis):
            tag = 1 << i; x = b
            for pb, pt in red:
                if x ^ pb < x: x ^= pb; tag ^= pt
            if x: red.append((x, tag)); red.sort(reverse=True)
        c = 0
        for pb, pt in sorted(red, reverse=True):
            if v ^ pb < v: v ^= pb; c ^= pt
        return c if v == 0 else None
    cA = {s: coords(s) for s in A}
    cand = [[t for t in B if invB[t] == invA[b]] for b in basis]
    def img(c, chosen):
        x = 0
        for j in range(len(chosen)):
            if (c >> j) & 1: x ^= chosen[j]
        return x
    def rec(i, chosen):
        if i == len(basis): return {img(cA[s], chosen) for s in A} == Bs
        for t in cand[i]:
            if t in chosen or B5.rank_of(chosen + [t]) <= len(chosen): continue
            ok = True; ch = chosen + [t]
            for s in A:
                c = cA[s]
                if (c >> (i + 1)) == 0:
                    y = img(c, ch)
                    if y not in Bs or invB[y] != invA[s]: ok = False; break
            if ok and rec(i + 1, ch): return True
        return False
    return rec(0, [])


def affine_orbit_representatives(m, verbose=False):
    """orbits of subsets of AG(m,2) = {(a,1)} subset F_2^(m+1) under AGL(m,2) (= stabiliser of the hyperplane in GL(m+1,2)); nonempty subsets, all sizes.
    returns dict size -> list of sorted tuples (points are ints with bit m set)."""
    k = m + 1; top = 1 << m; pts = [top | a for a in range(1 << m)]
    level = {1: [(top,)]}; allreps = {1: [(top,)]}
    for size in range(2, len(pts) + 1):
        buckets = {}; reps = []
        for R in level[size - 1]:
            for p in pts:
                if p in R: continue
                cand = tuple(sorted(R + (p,))); fp = affine_fingerprint(cand); lst = buckets.setdefault(fp, [])
                if any(isomorphic_strong(list(cand), list(o), k) for o in lst): continue
                lst.append(cand); reps.append(cand)
        level[size] = reps; allreps[size] = reps
        if verbose: print('size', size, 'orbits', len(reps), flush=True)
    return allreps


def rank3_witness(C, n):
    """explicit collision from a double 2-decomposition: cells (S,x),(T,x), S=(a,b), T=(c,d) partitions of one word, x a codeword outside span(S) u span(T) (exists for nullity >= 3).
    returns (rank, S, T, x) with the exact affine rank of its generators (B5.witness_rank), or None when there is no double 2-decomposition."""
    r = double_two_decomposition(C)
    if r is None: return None
    U, S, T = r; spS = B5.span_set(S); spT = B5.span_set(T)
    x = next((c for c in C if c not in spS and c not in spT), None)
    if x is None: return None
    return B5.witness_rank(n, S, x, T, x), S, T, x


# ----------------------------------------------------------------------------------------------- the cut-space family K_{2,t}  (THEOREM G10-K)
def cut_space_k2t(t):
    """code (list of all 2^(t+1) codewords as 2t-bit masks) of the cut space of K_{2,t}; coordinates: bit 2i = edge x z_i, bit 2i+1 = edge y z_i.
    Vertices x, y, z_0..z_{t-1}; the cut delta(U) has edge e=uv iff exactly one endpoint lies in U."""
    n = 2 * t; words = set()
    for ux in (0, 1):
        for uy in (0, 1):
            for uz in range(1 << t):
                m = 0
                for i in range(t):
                    zi = (uz >> i) & 1
                    if ux ^ zi: m |= 1 << (2 * i)
                    if uy ^ zi: m |= 1 << (2 * i + 1)
                words.add(m)
    return sorted(words)


def two_blocks(C, n):
    """all unordered pairs {a, b} of circuits with a | b = all ones, a & b = 0 (two-circuit partitions of the full set)."""
    circ = B5.circuits_of_code(C); full = (1 << n) - 1; cs = set(circ)
    return sorted({tuple(sorted((a, full ^ a))) for a in circ if (full ^ a) in cs})


def decomposition_profile(C, n):
    """{word: number of partitions of supp(word) into circuits} for every nonzero word, plus the number of non-empty disjoint circuit families (G10-R rigidity and counting identity)."""
    circ = B5.circuits_of_code(C); cnt = {}; total = 0
    for S, U in B5.disjoint_families(circ):
        cnt[U] = cnt.get(U, 0) + 1; total += 1
    return cnt, total
