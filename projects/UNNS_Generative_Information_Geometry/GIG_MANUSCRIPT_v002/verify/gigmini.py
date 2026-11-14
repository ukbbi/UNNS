"""gigmini -- compact, self-contained exact engine for the GIG manuscript (v001).
Integer / Fraction / GF(2) arithmetic only.  Independent of all frozen GIG packages.
Conventions: labels are addressed by rank 0..k-1; a history/arrangement is a permutation
(tuple of ranks); a face of the permutohedron P_k is an ordered set partition
(tuple of bit-masks); dim(face) = k - #blocks.  Homology is over GF(2).
"""
from fractions import Fraction
from itertools import permutations, combinations
from math import gcd

def lcm(a, b): return a // gcd(a, b) * b

# ---------- arithmetic realisation (SELECT-II) ----------
def ratio(l): return Fraction((l + 1) ** 2, l)

def Dmask(labels, mask):
    """D(I): reduced denominator of prod_{r in I} (l_r+1)^2/l_r  (D(empty)=1)."""
    x = Fraction(1)
    for r in range(len(labels)):
        if mask >> r & 1: x *= ratio(labels[r])
    return x.denominator

def feasible_family(labels, m):
    k = len(labels)
    return {I for I in range(1, 2 ** k - 1) if m % Dmask(labels, I) == 0}

def prefix_sets(perm):
    I, out = 0, []
    for r in perm[:-1]:
        I |= 1 << r; out.append(I)
    return out

def admissible_by_simulation(labels, m, perm):
    x = m
    for r in perm:
        l = labels[r]
        if x % l: return False
        x = x // l * (l + 1) ** 2
    return True

def admissible_perms_arith(labels, m):
    fam = feasible_family(labels, m)
    k = len(labels)
    full = (1 << k) - 1
    return {p for p in permutations(range(k)) if all(I in fam for I in prefix_sets(p))}
    # (the last prefix set, the full set, is excluded: D(full)|m is not needed? see note)

# NOTE: Lemma F requires D(I)|m for EVERY prefix set including the full set.
def admissible_perms(labels, m):
    k = len(labels); full = (1 << k) - 1
    fam = {I for I in range(1, 2 ** k) if m % Dmask(labels, I) == 0}
    return {p for p in permutations(range(k)) if all((I in fam) for I in prefix_sets(p) + [full])}

# ---------- permutohedron faces ----------
def ordered_partitions(k):
    """all ordered set partitions of {0..k-1} as tuples of masks"""
    res = []
    def rec(remaining, cur):
        if remaining == 0:
            res.append(tuple(cur)); return
        sub = remaining
        while sub:
            cur.append(sub); rec(remaining ^ sub, cur); cur.pop()
            sub = (sub - 1) & remaining
    rec((1 << k) - 1, [])
    return res

def block_perms(mask):
    els = [i for i in range(mask.bit_length()) if mask >> i & 1]
    return list(permutations(els))

def face_vertices(F):
    verts = [()]
    for B in F:
        verts = [v + p for v in verts for p in block_perms(B)]
    return verts

def face_dim(F, k): return k - len(F)

def face_boundary(F):
    """GF(2) boundary: split one block into ordered pair (S|T)."""
    out = []
    for i, B in enumerate(F):
        S = (B - 1) & B
        while S:
            T = B ^ S
            out.append(F[:i] + (S, T) + F[i + 1:])
            S = (S - 1) & B
    return out

def prefsets_of_face(F):
    out, acc = set(), 0
    for B in F:
        sub = B
        while sub:
            out.add(acc | sub); sub = (sub - 1) & B
        acc |= B
    return out

def complex_from_prefix_family(k, fam):
    """full subcomplex of P_k whose faces F satisfy Pref(F) subset fam  (prefix-defined A)."""
    return [F for F in ordered_partitions(k) if prefsets_of_face(F) <= fam]

def complex_from_vertex_set(k, A):
    faces = []
    for F in ordered_partitions(k):
        if all(v in A for v in face_vertices(F)): faces.append(F)
    return faces

# ---------- GF(2) homology ----------
def rank_gf2(rows):
    piv, r = {}, 0
    for v in rows:
        while v:
            h = v.bit_length() - 1
            if h in piv: v ^= piv[h]
            else: piv[h] = v; r += 1; break
    return r

def betti(k, faces):
    bydim = {}
    for F in faces: bydim.setdefault(k - len(F), []).append(F)
    idx = {d: {F: i for i, F in enumerate(L)} for d, L in bydim.items()}
    rho = {}
    for d in bydim:
        if d == 0: rho[0] = 0; continue
        rows = []
        for F in bydim[d]:
            v = 0
            for G in face_boundary(F):
                j = idx[d - 1].get(G)
                if j is not None: v ^= 1 << j
            rows.append(v)
        rho[d] = rank_gf2(rows)
    top = max(bydim) if bydim else -1
    f = [len(bydim.get(d, [])) for d in range(top + 1)]
    b = [f[d] - rho.get(d, 0) - rho.get(d + 1, 0) for d in range(top + 1)]
    return f, b

def betti_arith(labels, m):
    k = len(labels)
    full = (1 << k) - 1
    fam = {I for I in range(1, 2 ** k) if m % Dmask(labels, I) == 0}
    faces = complex_from_prefix_family(k, fam)
    return betti(k, faces)
