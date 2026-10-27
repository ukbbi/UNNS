"""GEO-I v007, Programme B: circuit-partition / coset description of the cells of a binary 0/1 box (exact, integer bitmasks).

Setting as binary_01 (columns c_i in F_2^m, C = ker M the binary code of codewords, box 1^n).
THEOREM B-COSET (proved in BINARY_RANK.md).  The cells with union U are exactly P(x; S_1..S_r), S_j pairwise disjoint circuits with union U, x in C \\ span(S);
the corner set is the coset x + span(S) of the subspace span(S) = {XOR of subfamilies of S} inside C.  In particular a cell is determined by (partition S of U into
circuits, coset of span(S) in C other than span(S) itself) and two cells with the same union U and the same x outside U collide.
The module enumerates circuit partitions of U and nonzero cosets, and cross-checks against binary_01.cells_01 (independent implementation)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import binary_01 as B


def kernel(cols):
    n = len(cols); return B.codewords(cols) + [0]


def partitions_into_circuits(circ, U):
    """all sets of pairwise disjoint circuits with union exactly U (as sorted tuples of masks)."""
    circ = sorted(c for c in circ if c & ~U == 0); out = []
    def rec(rem, start, chosen):
        if rem == 0:
            out.append(tuple(chosen)); return
        low = rem & -rem
        for j in range(len(circ)):
            c = circ[j]
            if c & low and c & ~rem == 0: rec(rem & ~c, 0, chosen + [c])
    rec(U, 0, []); return sorted(set(tuple(sorted(p)) for p in out))


def cosets(Cset, S):
    """nonzero cosets x + span(S) inside the code (as frozensets of corners)."""
    sp = B.span_mask_xors(list(S)); seen = set(); out = []
    for x in Cset:
        if x in sp: continue
        co = frozenset(x ^ f for f in sp)
        if co not in seen: seen.add(co); out.append(co)
    return out


def full_support_cells(cols):
    """cells whose union is the whole coordinate set: list of (partition, coset)."""
    n = len(cols); C = set(kernel(cols)); circ = B.circuits_of([c for c in C if c])
    U = (1 << n) - 1; out = []
    for p in partitions_into_circuits(circ, U):
        for co in cosets(C, p): out.append((p, co))
    return out


def nullity(cols):
    n = len(cols); basis = []
    for c in cols:
        for b in basis: c = min(c, c ^ b)
        if c: basis.append(c)
    return n - len(basis)
