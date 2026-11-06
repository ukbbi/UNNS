"""Self-contained, elimination-light certificates for one system (content C, source m0) -- written from the DEFINITIONS, independent of history_complex / cert.

arithmetic:  arrangements = orderings of C; admissible iff stepwise  m -> m/N*(N+1)^2  stays integral (direct simulation).
cellular:    K = faces of the permutohedron P_6 (ordered set partitions of ranks 0..5) all of whose vertices are admissible; boundary splits one block in two.
positive:    cycle z (set of 2-faces), cochain phi (set of 2-faces): z is a 2-cycle, phi(z)=1, phi(d f)=0 for EVERY admitted 3-face f  => z not a boundary, beta_2>0.
negative:    beta_2=0 via f_2 = rank d2 + rank d3 with ranks by plain GF(2) elimination on python-int rows (two independent rank routines, one with sorted-pivot, one by column reduction)."""
from itertools import permutations, combinations, product


def admissible_orderings(content, m0):
    labs = sorted(content)
    k = len(labs)
    out = []
    for p in permutations(range(k)):
        m, ok = m0, True
        for r in p:
            N = labs[r]
            if m % N:
                ok = False
                break
            m = m // N * (N + 1) ** 2
        if ok:
            out.append(p)
    return out


def ordered_partitions(k):
    res = []
    def rec(rem, acc):
        if not rem:
            res.append(tuple(acc)); return
        for r in range(1, len(rem) + 1):
            for B in combinations(rem, r):
                rec([x for x in rem if x not in B], acc + [B])
    rec(list(range(k)), [])
    return res


def vertices(face):
    parts = [list(permutations(B)) for B in face]
    return {tuple(x for blk in combo for x in blk) for combo in product(*parts)}


def boundary(face):
    out = []
    for i, B in enumerate(face):
        for r in range(1, len(B)):
            for C in combinations(B, r):
                D = tuple(x for x in B if x not in C)
                out.append(face[:i] + (C, D) + face[i + 1:])
    return out


def complex_of(A, k=6):
    A = set(A)
    by = {}
    for f in ordered_partitions(k):
        if vertices(f) <= A:
            by.setdefault(k - len(f), []).append(f)
    return by


def rank_rows(rows):
    piv = {}
    rk = 0
    for r in rows:
        while r:
            h = r.bit_length() - 1
            if h in piv:
                r ^= piv[h]
            else:
                piv[h] = r; rk += 1; break
    return rk


def rank_cols(rows, ncols):
    """rank by reducing the transposed matrix (column space), a second routine."""
    cols = [0] * ncols
    for i, r in enumerate(rows):
        for j in range(ncols):
            if r >> j & 1:
                cols[j] |= 1 << i
    return rank_rows(cols)


def boundary_rows(by, d):
    idx = {f: i for i, f in enumerate(by.get(d - 1, []))}
    rows = []
    for f in by.get(d, []):
        r = 0
        for g in boundary(f):
            r ^= 1 << idx[g]
        rows.append(r)
    return rows, len(idx)


def betti2_by_ranks(by):
    r2, n1 = boundary_rows(by, 2)
    r3, n2 = boundary_rows(by, 3)
    f2 = len(by.get(2, []))
    return f2 - rank_rows(r2) - (rank_rows(r3) if r3 else 0), f2 - rank_cols(r2, n1) - (rank_cols(r3, n2) if r3 else 0), len(r3)


def find_certificate(by):
    """returns (z_ids, phi_ids) for a positive system, else None. 2-faces indexed in by[2] order."""
    r2, _ = boundary_rows(by, 2)
    r3, _ = boundary_rows(by, 3)
    f2 = len(by[2])
    # kernel of d2 (rows are images of basis faces): reduce with tracking
    piv = {}
    kern = []
    for i, r in enumerate(r2):
        t = 1 << i
        while r:
            h = r.bit_length() - 1
            if h in piv:
                pr, pt = piv[h]
                r ^= pr; t ^= pt
            else:
                piv[h] = (r, t); break
        if r == 0:
            kern.append(t)
    bpiv = {}
    for r in r3:
        while r:
            h = r.bit_length() - 1
            if h in bpiv:
                r ^= bpiv[h]
            else:
                bpiv[h] = r; break
    z = None
    for k_ in kern:
        t = k_
        while t:
            h = t.bit_length() - 1
            if h in bpiv:
                t ^= bpiv[h]
            else:
                break
        if t:
            z = k_; break
    if z is None:
        return None
    eqs = [(r, 0) for r in r3] + [(z, 1)]
    piv = {}
    for m, rhs in eqs:
        while m:
            h = m.bit_length() - 1
            if h in piv:
                pm, pr = piv[h]; m ^= pm; rhs ^= pr
            else:
                piv[h] = (m, rhs); break
        assert not (m == 0 and rhs == 1)
    phi = 0
    for h in sorted(piv):
        m, rhs = piv[h]
        phi_val = rhs ^ (bin((m ^ (1 << h)) & phi).count("1") & 1)
        if phi_val:
            phi |= 1 << h
    bits = lambda x: [i for i in range(f2) if x >> i & 1]
    return bits(z), bits(phi)


def verify(A, z_faces, phi_faces, k=6):
    """direct verification from the definition; faces given as tuples of tuples."""
    A = set(A)
    z, phi = set(map(lambda f: tuple(map(tuple, f)), z_faces)), set(map(lambda f: tuple(map(tuple, f)), phi_faces))
    if any(len(f) != k - 2 or not vertices(f) <= A for f in z | phi):
        return False, "face outside complex"
    cnt = {}
    for f in z:
        for g in boundary(f):
            cnt[g] = cnt.get(g, 0) ^ 1
    if any(cnt.values()):
        return False, "z not a cycle"
    if len(z & phi) % 2 != 1:
        return False, "phi(z) even"
    for f in ordered_partitions(k):
        if len(f) == k - 3 and vertices(f) <= A:
            if sum(1 for g in boundary(f) if g in phi) % 2:
                return False, "phi not a cocycle on an admitted 3-face"
    return True, "ok"
