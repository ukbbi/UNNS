"""GEO-I v008, Programme C: series-class (blow-up) reduction and support classification of binary 0/1 boxes.

Setting (v006/v007): columns c_i in F_2^m of M, code C = ker M (dim k = n - rank M = nullity), box 1^n.  Two coordinates i,j are PARALLEL (a series pair of the matroid of M,
'twins' of the code) if c_i = c_j for every codeword c in C.  Parallelism is an equivalence relation; its classes N_1..N_p ('classes') partition the coordinates.
Every codeword is a union of classes, so C is the pull-back of a code C_red of length p ('reduced code') in which no two coordinates are parallel.

THEOREM B-SERIES (v008, proved in MINIMAL_RANK.md).  Let (C,n) be the blow-up of (C_red,p) (each coordinate of C_red replaced by a class of size n_j >= 1).  Then
 (a) circuits, cells, centres and collisions of the box of C are the blow-ups of those of C_red (cells <-> cells, collisions <-> collisions);
 (b) the box of C is embedded iff the box of C_red is;
 (c) witness ranks are unchanged (blow-up repeats coordinates of the generator vectors);
 (d) deletion of one coordinate of a class equals deletion of the whole class (all coordinates of the class are forced to 0), so  C is minimal non-embedded  iff C_red is.
THEOREM B-NULL' (v008).  Any collision needs a cell with >=2 circuits and a codeword outside its span: nullity >= 3 for every non-embedded box.
THEOREM B-NULL3 (v008, classification of nullity 3).  A minimal non-embedded box of nullity exactly 3 is the blow-up of the parity-4 code (classes N_1..N_4, all nonempty,
 codewords = unions of an even number of classes); all its witnesses have rank 3.  (finite check over the 127 supports of F_2^3, theory/binary_min.py:classify_nullity3).
Functions below implement the reduction and the support-level classification with the same exact engines as v006/v007."""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import binary_01 as B, centre_collisions as CC, rank_reduction as RR


def kernel_code(cols):
    return [0] + B.codewords(cols)


def classes_of(cols):
    """parallel classes (list of coordinate-index lists) of the box with parity-check columns `cols`."""
    n = len(cols); C = kernel_code(cols); prof = {}
    for i in range(n): prof.setdefault(tuple((c >> i) & 1 for c in C), []).append(i)
    return list(prof.values())


def reduced_columns(cols):
    """parity-check columns of the reduced code (one representative per class): recompute M_red from the reduced code."""
    n = len(cols); cl = classes_of(cols); C = kernel_code(cols); p = len(cl)
    red = [sum(((c >> cls[0]) & 1) << t for t, c in enumerate(C)) for cls in cl]   # coordinate j -> its profile over the codewords (generator columns of C_red)
    return cl, red


def code_to_parity_columns(gen_cols, p):
    """given generator columns g_j in F_2^k (j<p) of a code (rows = basis codewords), return parity-check columns of length-p code (kernel basis)."""
    k = max(g.bit_length() for g in gen_cols) if gen_cols else 0
    rows = [0] * k
    for j, g in enumerate(gen_cols):
        for r in range(k):
            if (g >> r) & 1: rows[r] |= 1 << j
    red = []; pivs = []
    for r in rows:
        for pv, v in zip(pivs, red):
            if (r >> pv) & 1: r ^= v
        if r:
            pv = r.bit_length() - 1
            red = [v ^ r if (v >> pv) & 1 else v for v in red]; red.append(r); pivs.append(pv)
    free = [i for i in range(p) if i not in pivs]; null = []
    for f in free:
        h = 1 << f
        for pv, v in zip(pivs, red):
            if (v >> f) & 1: h |= 1 << pv
        null.append(h)
    return [sum((((null[t] >> i) & 1) << t) for t in range(len(null))) for i in range(p)]


def blowup_parity_columns(gen_cols, mult):
    """parity-check columns of the blow-up of the code with generator columns gen_cols, class sizes mult."""
    G = [g for g, m in zip(gen_cols, mult) for _ in range(m)]
    return code_to_parity_columns(G, len(G))


def classify_nullity3():
    """all supports Sigma subset of F_2^3\\0 (class level, multiplicity 1): which are non-embedded?  returns (non_embedded_supports, all_witness_ranks)."""
    out = []; ranks = set()
    for mask in range(1, 128):
        sig = [v for v in range(1, 8) if (mask >> (v - 1)) & 1]
        sp = {0}
        for g in sig: sp |= {a ^ g for a in sp}
        if len(sp) < 8: continue                                    # dimension of C must be 3
        cols = code_to_parity_columns(sig, len(sig))
        if B.is_embedded(cols): continue
        out.append(tuple(sig))
        for cen, a, b in CC.collisions(cols): ranks.add(RR.witness_rank(len(cols), a, b)[0])
    return out, ranks


# ---------------------------------------------------------------------------------------------- general nullity k classification
def gl_generators(k):
    """permutations of the 2^k-1 nonzero points of F_2^k induced by the elementary transvections x -> x ^ (bit_j(x) << i)."""
    gens = []
    for i in range(k):
        for j in range(k):
            if i == j: continue
            gens.append([((v ^ (((v >> j) & 1) << i)) - 1) for v in range(1, 1 << k)])
    return gens


def support_orbits(k):
    """orbits (representative masks) of subsets of F_2^k\\0 that span F_2^k, under GL(k,2).  mask bit (v-1) <-> point v."""
    npts = (1 << k) - 1; gens = gl_generators(k); parent = {}
    def find(a):
        while parent.setdefault(a, a) != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    def span_dim_full(mask):
        sp = {0}
        for v in range(1, 1 << k):
            if (mask >> (v - 1)) & 1: sp |= {a ^ v for a in sp}
        return len(sp) == (1 << k)
    reps = {}
    for mask in range(1, 1 << npts):
        a = find(mask)
        for g in gens:
            m2 = 0; mm = mask
            while mm:
                lb = mm & -mm; b = lb.bit_length() - 1; m2 |= 1 << g[b]; mm ^= lb
            b2 = find(m2)
            if b2 != a: parent[b2] = a
    for mask in list(parent):
        reps.setdefault(find(mask), []).append(mask)
    return [(r, len(v)) for r, v in reps.items() if span_dim_full(r)]


def classify_nullity(k, verbose=False):
    """Complete classification of the REDUCED minimal non-embedded boxes of nullity exactly k (all lengths n then follow by B-SERIES).
    returns dict: reps (list of supports), count_orbits, min_ranks histogram."""
    out = []; hist = {}
    for rep, sz in support_orbits(k):
        sig = [v for v in range(1, 1 << k) if (rep >> (v - 1)) & 1]
        cols = code_to_parity_columns(sig, len(sig))
        if len(sig) < 4 or B.is_embedded(cols): continue
        if not B.minimal_nonembedded(cols): continue
        rk = min(RR.witness_rank(len(cols), a, b)[0] for cen, a, b in CC.collisions(cols))
        hist[rk] = hist.get(rk, 0) + 1
        out.append({'support': sig, 'p': len(sig), 'min_rank': rk, 'orbit_size': sz})
    return {'k': k, 'minimal_reduced_orbits': out, 'min_rank_histogram': hist}


# ---------------------------------------------------------------------------------------------- Reed-Muller family and B-COMMON / B-LOW
def rm_support(k):
    """generator columns of RM(1,k-1): the 2^(k-1) points of F_2^k with last coordinate 1 (affine hyperplane complement)."""
    return [v for v in range(1, 1 << k) if (v >> (k - 1)) & 1]


def simplex_support(m):
    return list(range(1, 1 << m))


def two_circuit_partitions(cols):
    """partitions of [n] into two circuits (as pairs of masks)."""
    n = len(cols); full = (1 << n) - 1; C = [0] + B.codewords(cols); circ = B.circuits_of([c for c in C if c]); cs = set(circ)
    return [(a, full ^ a) for a in circ if a < (full ^ a) and (full ^ a) in cs], C


def common_base_witness(cols):
    """B-COMMON: return (S,T,x) with S != T two-circuit partitions of [n] and x in C outside span(S) and span(T), or None.  The collision of cells (S,x),(T,x) has rank <= 3."""
    parts, C = two_circuit_partitions(cols)
    sp = [{0, a, b, a ^ b} for a, b in parts]
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            for x in C:
                if x not in sp[i] and x not in sp[j]: return parts[i], parts[j], x
    return None


def collision_rank_of(cols, S, T, x):
    """exact witness rank of cells (S,x),(T,x) (B-DELTA: rank of generators)."""
    n = len(cols)
    g = [[(1 - 2 * ((x >> i) & 1)) if (m >> i) & 1 else 0 for i in range(n)] for m in S]; h = [[(1 - 2 * ((x >> i) & 1)) if (m >> i) & 1 else 0 for i in range(n)] for m in T]
    return B.rank_int(g + h)
