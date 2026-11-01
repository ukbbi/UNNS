"""GEO-HD-1B / E2-P1 -- INDEPENDENT audit.  Imports nothing from fibre_transport.py or
cell_transport.py (standard library only; every number is an int or Fraction).

Different methods from the builder:
  * D(x) by brute-force trial of d^2 | a (no factorisation); C(x) from its definition;
  * fibres / lattice vectors / Graver sets by brute force over the box (no modular inverses:
    chi is tested with the congruence  prod p^alpha_+ == prod p^alpha_-  (mod b));
  * cells by searching 2^j-subsets of the fibre for parallelotopes (not by choosing generators);
  * geometry by an exact linear-programming feasibility test (two-phase simplex, Bland rule),
    NOT by candidate vertices;
  * ranks over GF(2), GF(3) and GF(2^31-1) (builder: exact Q).
"""
from fractions import Fraction
from itertools import combinations, product
from math import isqrt

# ----------------------------------------------------------------------------- arithmetic


def D_brute(a, b):
    out = []
    for d in range(2, isqrt(a) + 1):
        if a % (d * d) == 0 and (d - 1) % b == 0:
            out.append(d)
    return out


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def C_brute(x):
    a, b = x.numerator, x.denominator
    ds = D_brute(a, b)
    L = 1
    for d in ds:
        L = L * d // gcd(L, d)
    G = 0
    for d in ds:
        G = gcd(G, d - 1)
    return x + Fraction(L * L, G), L, G, ds


def prime_exponents(n):
    out = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def in_Lambda(alpha, primes, b):
    """prod p^alpha == 1 (mod b) written without inverses: positive part == negative part."""
    pos = neg = 1
    for p, t in zip(primes, alpha):
        if t > 0:
            pos = pos * p ** t
        elif t < 0:
            neg = neg * p ** (-t)
    return (pos - neg) % b == 0 if b > 1 else True


def stage_data(x):
    a, b = x.numerator, x.denominator
    e = prime_exponents(a)
    primes = tuple(sorted(p for p in e if e[p] >= 2))
    q = tuple(e[p] // 2 for p in primes)
    F = [al for al in product(*[range(m + 1) for m in q]) if any(al) and in_Lambda(al, primes, b)]
    return primes, q, b, sorted(F)


def graver_brute(primes, b, q):
    L = [v for v in product(*[range(-m, m + 1) for m in q]) if any(v) and in_Lambda(v, primes, b)]
    S = set(L)

    def below(w, v):
        return w != v and all(wi * vi >= 0 and abs(wi) <= abs(vi) for wi, vi in zip(w, v))
    return sorted(v for v in L if not any(below(w, v) for w in L))


# ----------------------------------------------------------------------------- cells by subset search


def parallelotope_gens(S, F, G):
    """If the point set S (2^j integer points) is a parallelotope with edge vectors in G,
    return (base, sorted gens) else None.  Base = lex-min vertex; gens = lex-positive edges."""
    pts = sorted(S)
    j = len(pts).bit_length() - 1
    base = pts[0]
    cand = [tuple(p[i] - base[i] for i in range(len(base))) for p in pts[1:]]
    Gset = set(G)
    edges = [c for c in cand if c in Gset]
    for gens in combinations(sorted(edges), j):
        built = set()
        for bits in product((0, 1), repeat=j):
            built.add(tuple(base[i] + sum(b * g[i] for b, g in zip(bits, gens)) for i in range(len(base))))
        if built == set(pts) and len(built) == 2 ** j:
            return base, gens
    return None


def cells_by_subsets(F, G, jmax):
    """All parallelotope cells with 2^j <= |F| corners, j=1..jmax, by scanning subsets of F."""
    out = {}
    for j in range(1, jmax + 1):
        res = {}
        n = 2 ** j
        if n > len(F):
            out[j] = res
            continue
        for S in combinations(F, n):
            r = parallelotope_gens(S, F, G)
            if r:
                res[S] = r
        out[j] = res
    return out


# ----------------------------------------------------------------------------- exact LP


def lp_feasible(A, b):
    """Is {x >= 0 : A x = b} nonempty?  Two-phase simplex (phase I), Fractions, Bland's rule."""
    m = len(A)
    n = len(A[0]) if m else 0
    T = [[Fraction(v) for v in row] + [Fraction(bb)] for row, bb in zip(A, b)]
    for r in T:
        if r[-1] < 0:
            for c in range(len(r)):
                r[c] = -r[c]
    # artificial variables
    nt = n + m
    for i, r in enumerate(T):
        r[n:n] = [Fraction(1 if i == k else 0) for k in range(m)]
    basis = [n + i for i in range(m)]
    cost = [Fraction(0)] * n + [Fraction(1)] * m + [Fraction(0)]
    # reduced costs row z = cost - sum of rows
    z = cost[:]
    for r in T:
        for c in range(nt + 1):
            z[c] -= r[c]
    while True:
        enter = next((c for c in range(nt) if z[c] < 0), None)
        if enter is None:
            break
        best, row = None, None
        for i, r in enumerate(T):
            if r[enter] > 0:
                ratio = r[-1] / r[enter]
                if best is None or ratio < best or (ratio == best and basis[i] < basis[row]):
                    best, row = ratio, i
        if row is None:
            break
        pv = T[row][enter]
        T[row] = [v / pv for v in T[row]]
        for i, r in enumerate(T):
            if i != row and r[enter] != 0:
                f = r[enter]
                T[i] = [u - f * v for u, v in zip(r, T[row])]
        f = z[enter]
        z = [u - f * v for u, v in zip(z, T[row])]
        basis[row] = enter
    return -z[-1] == 0


def intersection_nonempty(cells):
    """cells: list of (base, gens).  Variables: x in [0,box], t^c in [0,1]; equalities x = u_c + sum t g.
    Bounds handled with slack variables."""
    k = 3
    var = []  # (name)
    for ci, (u, gs) in enumerate(cells):
        for gi in range(len(gs)):
            var.append(("t", ci, gi))
    nt = len(var)
    # columns: x_1..x_3 (>=0), t..., slacks for t<=1, slack for x<=2 -> build rows
    cols = 3 + nt
    rows, rhs = [], []
    for ci, (u, gs) in enumerate(cells):
        for r in range(k):
            row = [0] * cols
            row[r] = 1
            for gi, g in enumerate(gs):
                row[3 + var.index(("t", ci, gi))] = -g[r]
            rows.append(row)
            rhs.append(u[r])
    # slack variables
    extra = nt + 3
    rows = [row + [0] * extra for row in rows]
    for i in range(nt):
        row = [0] * (cols + extra)
        row[3 + i] = 1
        row[cols + i] = 1
        rows.append(row)
        rhs.append(1)
    for r in range(3):
        row = [0] * (cols + extra)
        row[r] = 1
        row[cols + nt + r] = 1
        rows.append(row)
        rhs.append(2)
    return lp_feasible(rows, rhs)


def meets_open_corner(base, gens):
    """Does the cell meet R = {x : x_i < 1 for all i} (x>=0)?  LP: maximise eps s.t. x_i + eps <= 1."""
    k = 3
    nt = len(gens)
    # variables: x(3)>=0, t(nt)>=0, eps>=0, slacks: t<=1 (nt), x_i+eps<=1 (3)
    # decide eps>0 via feasibility with eps >= 1/10^6? exact: use eps scaled: test feasibility with eps = 1/N
    # feasibility with a fixed eps0 = 1/(2^20) is sufficient: R-cell intersection is an open condition
    eps0 = Fraction(1, 2 ** 20)
    cols = 3 + nt
    rows, rhs = [], []
    for r in range(k):
        row = [0] * cols
        row[r] = 1
        for gi, g in enumerate(gens):
            row[3 + gi] = -g[r]
        rows.append(row)
        rhs.append(base[r])
    rows = [row + [0] * (nt + 3) for row in rows]
    for i in range(nt):
        row = [0] * (cols + nt + 3)
        row[3 + i] = 1
        row[cols + i] = 1
        rows.append(row)
        rhs.append(1)
    for r in range(3):
        row = [0] * (cols + nt + 3)
        row[r] = 1
        row[cols + nt + r] = 1
        rows.append(row)
        rhs.append(1 - eps0)
    return lp_feasible(rows, rhs)


# ----------------------------------------------------------------------------- homology mod p


def rank_mod(rows, p):
    piv = {}
    r = 0
    for row in rows:
        row = {c: v % p for c, v in row.items() if v % p}
        while row:
            c = min(row)
            if c in piv:
                f = row[c] * pow(piv[c][c], -1, p) % p
                for cc, vv in piv[c].items():
                    nv = (row.get(cc, 0) - f * vv) % p
                    if nv:
                        row[cc] = nv
                    else:
                        row.pop(cc, None)
            else:
                piv[c] = row
                r += 1
                break
    return r


def complex_boundary_rows(cells_by_dim):
    """cells_by_dim: {j: {vertex-tuple: (base, gens)}} including j=0 vertices as {(v,):(v,())}."""
    rows_by_j = {}
    for j in range(1, max(cells_by_dim) + 1):
        low = sorted(cells_by_dim[j - 1])
        idx = {}
        for i, key in enumerate(low):
            idx[key] = i
        rows = []
        for key in sorted(cells_by_dim[j]):
            base, gens = cells_by_dim[j][key]
            row = {}
            for i, g in enumerate(gens):
                rest = gens[:i] + gens[i + 1:]
                sg = -1 if i % 2 else 1
                hi = verts_of(tuple(base[t] + g[t] for t in range(len(base))), rest)
                lo = verts_of(base, rest)
                row[idx[hi]] = row.get(idx[hi], 0) + sg
                row[idx[lo]] = row.get(idx[lo], 0) - sg
            rows.append(row)
        rows_by_j[j] = rows
    return rows_by_j


def verts_of(base, gens):
    vs = []
    for bits in product((0, 1), repeat=len(gens)):
        vs.append(tuple(base[t] + sum(b * g[t] for b, g in zip(bits, gens)) for t in range(len(base))))
    return tuple(sorted(vs))


def betti_mod(cells_by_dim, p):
    rows = complex_boundary_rows(cells_by_dim)
    top = max(cells_by_dim)
    rk = {0: 0}
    for j in range(1, top + 1):
        rk[j] = rank_mod(rows[j], p)
    return [len(cells_by_dim[j]) - rk[j] - (rk[j + 1] if j + 1 <= top else 0) for j in range(top + 1)]


def nerve_betti_mod(sets_nonempty, n, maxdim, p):
    """sets_nonempty(subset tuple)->bool (monotone).  Builds nerve skeleton up to maxdim, Betti mod p."""
    simp = [dict() for _ in range(maxdim + 1)]
    for i in range(n):
        simp[0][(i,)] = 1

    def grow(prefix):
        d = len(prefix) - 1
        if d == maxdim:
            return
        for k in range(prefix[-1] + 1, n):
            t = prefix + (k,)
            if sets_nonempty(t):
                simp[d + 1][t] = 1
                grow(t)
    for i in range(n):
        grow((i,))
    ranks = {0: 0}
    for d in range(1, maxdim + 1):
        idx = {s: i for i, s in enumerate(simp[d - 1])}
        rows = []
        for s in simp[d]:
            rows.append({idx[s[:q] + s[q + 1:]]: (-1) ** q for q in range(len(s))})
        ranks[d] = rank_mod(rows, p)
    counts = [len(s) for s in simp]
    return counts, [counts[j] - ranks[j] - ranks[j + 1] for j in range(maxdim)]
