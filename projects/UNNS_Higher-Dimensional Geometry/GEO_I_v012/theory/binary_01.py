"""GEO-I v006, Programme B/C: EXACT combinatorial theory of 0/1 boxes for binary relation lattices.

SETTING.  c_1..c_n in F_2^m (nonzero columns), Lambda = { alpha in Z^n : sum alpha_i c_i = 0 in F_2^m }  (exponent-2 residue groups; every such
lattice is a relation lattice of genuine residues mod a suitable b).  Box q = (1,...,1).  Fibre F = nonzero codewords x of C = ker M, seen as 0/1 vectors.
LEMMA B1 (cells).  The cells of K_abs are (i) points, (ii) parallelotopes P(x; S_1..S_r) with S_j PAIRWISE DISJOINT circuits of the matroid (minimal
nonempty supports of codewords), x a codeword, generator g_j = ((1-2x_i)_{i in S_j}) (the sign pattern is forced by x), all 2^r corners nonzero.
 (a 0/1 corner cannot absorb two generators sharing a coordinate: u_i+a, u_i+b, u_i+a+b all in {0,1} forces a=0 or b=0.)
THEOREM B2 (centre criterion).  Let c = P(x;S_1..S_r), c' = P(y;T_1..T_t) (r,t >= 1).  relint c meets relint c' iff  U := cup S_j = cup T_l  and x = y
outside U.  In that case the common point z = (1/2 on U, x outside U) always works.  Hence K_abs is embedded iff no two DISTINCT cells have the same
centre (U, x|outside U).  (Proof: coordinates in S_j \\ cup T_l would be strictly between 0 and 1 on c but in {0,1} on c'; if supports agree, the linear
system t_j = s_l  or  t_j = 1 - s_l  is solved by t = s = 1/2.)
All functions are exact (integers); spans are exact ranks over Q."""
import itertools
from fractions import Fraction as Fr


def rank_int(rows):
    M = [[Fr(x) for x in r] for r in rows]; rk = 0
    if not M: return 0
    for c in range(len(M[0])):
        p = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c] / M[rk][c]; M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk


def codewords(cols):
    n = len(cols); out = []
    for x in range(1, 1 << n):
        s = 0
        for i in range(n):
            if x >> i & 1: s ^= cols[i]
        if s == 0: out.append(x)
    return out


def circuits_of(C):
    Cs = sorted(C, key=lambda x: bin(x).count('1'))
    circ = []
    for x in Cs:
        if not any((c & x) == c for c in circ): circ.append(x)
    return circ


def span_mask_xors(masks):
    s = {0}
    for m in masks: s |= {a ^ m for a in s}
    return s


def cells_01(cols, subset_mask=None):
    """all cells of dimension >= 1 as dict centre -> {canonical corner tuple -> (x, [S masks])}.  subset_mask restricts to coordinates in the mask (deletion)."""
    n = len(cols)
    full = (1 << n) - 1 if subset_mask is None else subset_mask
    cs = [cols[i] if full >> i & 1 else None for i in range(n)]
    # codewords supported inside `full`
    sub = [i for i in range(n) if full >> i & 1]
    C = []
    for x in range(1, 1 << n):
        if x & ~full: continue
        s = 0
        for i in sub:
            if x >> i & 1: s ^= cols[i]
        if s == 0: C.append(x)
    circ = circuits_of(C)
    byc = {}
    cellset = {}
    def rec(start, chosen, used):
        if chosen:
            fl = span_mask_xors(chosen)
            for x in C:
                if x in fl: continue                      # a corner would be the zero vector (x xor flips = 0 <=> x in span)
                corners = tuple(sorted(x ^ f for f in fl))
                if corners in cellset: continue
                cellset[corners] = (x, tuple(chosen))
        for j in range(start, len(circ)):
            if circ[j] & used: continue
            rec(j + 1, chosen + [circ[j]], used | circ[j])
    rec(0, [], 0)
    for corners, (x, S) in cellset.items():
        U = 0
        for m in S: U |= m
        byc.setdefault((U, x & ~U), []).append((corners, x, S))
    return byc, C, circ


def witness_pairs(byc):
    for cen, lst in byc.items():
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)):
                yield cen, lst[a], lst[b]


def gen_vec(x, S, n):
    return [((1 - 2 * ((x >> i) & 1)) if (S >> i) & 1 else 0) for i in range(n)]


def witness_span(n, a, b):
    (_, x, S), (_, y, T) = a, b
    gens = [gen_vec(x, m, n) for m in S] + [gen_vec(y, m, n) for m in T]
    delta = [((y >> i) & 1) - ((x >> i) & 1) for i in range(n)]
    return rank_int(gens + [delta]), rank_int(gens)


def _vec(x, n): return tuple((x >> i) & 1 for i in range(n))


def v005_form(cell, n):
    """(base u0 = lexicographically least corner, sorted tuple of lex-positive generators): the translation-normal form used by v005 witnesses."""
    corners, x, S = cell
    V = sorted(_vec(c, n) for c in corners); u0 = V[0]
    gens = []
    for m in S:
        g = tuple(((1 - 2 * ((x >> i) & 1)) if (m >> i) & 1 else 0) for i in range(n))
        first = next(v for v in g if v)
        gens.append(g if first > 0 else tuple(-v for v in g))
    return u0, tuple(sorted(gens))


def witness_classes(byc, n):
    """distinct witnesses (A,B,delta) up to translation and swap (v005 definition) -> {key: (cellA, cellB)}"""
    out = {}
    for cen, a, b in witness_pairs(byc):
        (ua, A), (ub, Bg) = v005_form(a, n), v005_form(b, n)
        d = tuple(q - p for p, q in zip(ua, ub))
        k1 = (A, Bg, d); k2 = (Bg, A, tuple(-v for v in d)); k = min(k1, k2)
        out.setdefault(k, (a, b))
    return out


def analyse(cols, subset_mask=None):
    """returns dict(embedded, n_witnesses, min_span, span_hist, ...)"""
    n = len(cols)
    byc, C, circ = cells_01(cols, subset_mask)
    wit = list(witness_pairs(byc))
    if not wit: return {'embedded': True, 'n_codewords': len(C), 'n_circuits': len(circ)}
    spans = {}
    for k, (a, b) in witness_classes(byc, n).items():
        sp, spg = witness_span(n, a, b)
        spans[sp] = spans.get(sp, 0) + 1
    # support dimension: coordinates used by the union of supports
    sup = sorted({bin(cen[0]).count('1') for cen, a, b in wit})
    return {'embedded': False, 'n_witnesses': sum(spans.values()), 'n_cell_pairs': len(wit), 'min_span': min(spans), 'max_span': max(spans), 'span_hist': spans,
            'support_sizes': sup, 'n_codewords': len(C), 'n_circuits': len(circ)}


def is_embedded(cols, subset_mask=None):
    byc, C, circ = cells_01(cols, subset_mask)
    return not any(len(v) > 1 for v in byc.values())


def minimal_nonembedded(cols):
    """box 1^n is a MINIMAL non-embedded box iff non-embedded and every coordinate deletion is embedded."""
    n = len(cols); full = (1 << n) - 1
    if is_embedded(cols): return False
    return all(is_embedded(cols, full & ~(1 << i)) for i in range(n))
