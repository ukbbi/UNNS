"""Independent exact (Fraction/int) implementation of the objects of Manuscript I.
Written for the manuscript checks; shares no code with the frozen GEO-HD-1 engines.
Lattice = predicate on integer vectors (full-rank sublattice of Z^k).  Box Q=(q_1..q_k).
"""
from fractions import Fraction as Fr
from itertools import product, combinations

def conf_le(w, v):           # w conformally below v
    return all(a*b >= 0 and abs(a) <= abs(b) for a, b in zip(w, v))

def graver(inlat, q):
    """Conformally minimal nonzero lattice vectors in [-q,q] (= Graver ∩ box, Lemma P2-L1)."""
    vs = [v for v in product(*[range(-c, c+1) for c in q]) if any(v) and inlat(v)]
    return [v for v in vs if not any(w != v and conf_le(w, v) for w in vs)]

def fibre(inlat, q):
    return [v for v in product(*[range(0, c+1) for c in q]) if any(v) and inlat(v)]

def lexpos(v):
    for a in v:
        if a: return a > 0
    return False

def rank(rows):
    M = [[Fr(x) for x in r] for r in rows]; rk = 0
    if not M: return 0
    for c in range(len(M[0])):
        p = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c]/M[rk][c]; M[i] = [a-f*b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk

def add(u, v): return tuple(a+b for a, b in zip(u, v))

def cells(inlat, q):
    """All cells (u; g_1<..<g_j) of K_abs as dict dim -> {(u,gens)}; vertices in F."""
    G = sorted(g for g in graver(inlat, q) if lexpos(g))
    F = set(fibre(inlat, q)); k = len(q)
    out = {0: {(u, ()) for u in F}}
    for j in range(1, k+1):
        S = set()
        for gens in combinations(G, j):
            if rank(gens) < j: continue
            for u in F:
                ok = True
                for mask in product((0, 1), repeat=j):
                    w = u
                    for m, g in zip(mask, gens):
                        if m: w = add(w, g)
                    if w not in F: ok = False; break
                if ok: S.add((u, gens))
        out[j] = S
    return out

def vertices(cell):
    u, gens = cell; vs = []
    for mask in product((0, 1), repeat=len(gens)):
        w = u
        for m, g in zip(mask, gens):
            if m: w = add(w, g)
        vs.append(w)
    return frozenset(vs)

def solve_in_cell(cell, p):
    """Is p in the closed parallelotope?  exact."""
    u, gens = cell; j = len(gens)
    d = [Fr(a)-b for a, b in zip(p, u)]
    if j == 0: return all(x == 0 for x in d)
    k = len(d)
    A = [[Fr(gens[c][r]) for c in range(j)] + [d[r]] for r in range(k)]
    rk = 0
    for c in range(j):
        piv = next((i for i in range(rk, k) if A[i][c] != 0), None)
        if piv is None: return False
        A[rk], A[piv] = A[piv], A[rk]
        A[rk] = [x/A[rk][c] for x in A[rk]]
        for i in range(k):
            if i != rk and A[i][c] != 0:
                f = A[i][c]; A[i] = [a-f*b for a, b in zip(A[i], A[rk])]
        rk += 1
    if any(A[i][j] != 0 for i in range(rk, k)): return False
    return all(0 <= A[i][j] <= 1 for i in range(j))

def in_union(cellsd, p):
    return any(solve_in_cell(c, p) for dim in cellsd for c in cellsd[dim])

def betti(cellsd):
    """Betti numbers over Q of the abstract complex (unreduced)."""
    top = max(d for d in cellsd if cellsd[d]) 
    idx = {d: {c: i for i, c in enumerate(sorted(cellsd[d]))} for d in cellsd}
    mats = {}
    for j in range(1, top+1):
        rows = []
        for (u, gens) in sorted(cellsd[j]):
            r = {}
            for i, g in enumerate(gens):
                rest = gens[:i]+gens[i+1:]
                sgn = (-1)**i
                a = (add(u, g), rest); b = (u, rest)
                r[idx[j-1][a]] = r.get(idx[j-1][a], 0)+sgn
                r[idx[j-1][b]] = r.get(idx[j-1][b], 0)-sgn
            rows.append(r)
        mats[j] = rows
    def dense(rows, n): return [[r.get(c, 0) for c in range(n)] for r in rows]
    # boundary-of-boundary check
    for j in range(2, top+1):
        for r in mats[j]:
            acc = {}
            for c, s in r.items():
                for c2, s2 in mats[j-1][c].items(): acc[c2] = acc.get(c2, 0)+s*s2
            assert all(v == 0 for v in acc.values()), "boundary^2 != 0"
    rk = {j: rank(dense(mats[j], len(cellsd[j-1]))) if cellsd[j] else 0 for j in mats}
    rk[top+1] = 0
    return [len(cellsd[d]) - rk.get(d, 0) - rk.get(d+1, 0) for d in range(top+1)]

def fvec(cellsd): return tuple(len(cellsd[d]) for d in sorted(cellsd))
