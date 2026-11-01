"""Independent audit code for E2-P2.  Imports NOTHING from the builder modules.
Brute-force definitions (inverse-free lattice test, all-pairs Graver sets, subset-built cells), exact planar
sampling re-implemented from scratch, and homology mod p."""
from fractions import Fraction as Fr
from itertools import combinations, product
from math import gcd, isqrt


# ------------------------------------------------------------------ arithmetic from first principles
def factor_small(n):
    out, p = {}, 2
    while p <= 2000 and p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    assert n == 1 or n < 2000 * 2000 or True
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def squareroot_part(a):
    r = 1
    for p, e in factor_small(a).items():
        r *= p ** (e // 2)
    return r


def D_brute(a, b):
    s = squareroot_part(a)
    return [d for d in range(2, s + 1) if s % d == 0 and (d - 1) % b == 0] if s < 3 * 10 ** 6 else _D_big(a, b)


def _D_big(a, b):
    f = factor_small(a)
    ps = sorted(f)
    es = [f[p] // 2 for p in ps]
    out = []
    for al in product(*[range(e + 1) for e in es]):
        d = 1
        for p, t in zip(ps, al):
            d *= p ** t
        if d >= 2 and (d - 1) % b == 0:
            out.append(d)
    return sorted(out)


def lcm(xs):
    L = 1
    for x in xs:
        L = L * x // gcd(L, x)
    return L


def C_brute(x):
    x = Fr(x)
    ds = D_brute(x.numerator, x.denominator)
    L = lcm(ds)
    G = 0
    for d in ds:
        G = gcd(G, d - 1)
    return x + Fr(L * L, G), L, G, ds


def coords(x):
    x = Fr(x)
    f = factor_small(x.numerator)
    P = tuple(sorted(p for p, e in f.items() if e >= 2))
    return P, tuple(f[p] // 2 for p in P), x.denominator


def in_Lambda(al, P, b):
    """prod p^al = 1 mod b, tested without modular inverses: num == den (mod b) for the exact rational."""
    if b == 1:
        return True
    n, d = 1, 1
    for p, t in zip(P, al):
        if t >= 0:
            n *= p ** t
        else:
            d *= p ** (-t)
    return (n - d) % b == 0


def fibre(P, q, b):
    return [v for v in product(*[range(m + 1) for m in q]) if any(v) and in_Lambda(v, P, b)]


def conf(g, h):
    return all(x * y >= 0 and abs(x) <= abs(y) for x, y in zip(g, h))


def graver(P, q, b):
    L = [v for v in product(*[range(-m, m + 1) for m in q]) if any(v) and in_Lambda(v, P, b)]
    return [v for v in L if not any(w != v and conf(w, v) for w in L)]


def lex_pos(v):
    for t in v:
        if t:
            return t > 0
    return False


def det2(g, h):
    return g[0] * h[1] - g[1] * h[0]


def cells_planar(F, G):
    """cells of K_abs for k=2 built from vertex sets: dict dim->set of frozenset(vertices)."""
    Fs = set(F)
    Go = sorted(g for g in G if lex_pos(g))
    V = {frozenset([v]) for v in F}
    E = set()
    for u in F:
        for g in Go:
            w = (u[0] + g[0], u[1] + g[1])
            if w in Fs:
                E.add(frozenset([u, w]))
    P = set()
    for g, h in combinations(Go, 2):
        if det2(g, h) == 0:
            continue
        for u in F:
            c = [u, (u[0] + g[0], u[1] + g[1]), (u[0] + h[0], u[1] + h[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1])]
            if all(t in Fs for t in c):
                P.add(frozenset(c))
    return {0: V, 1: E, 2: P}


# ------------------------------------------------------------------ lattice relation (exact, periodic box)
def order_brute(p, b):
    r, n = 1 % b, 0
    while True:
        r = r * p % b
        n += 1
        if r == 1 % b:
            return n


def relation_brute(P, b, b2):
    """Both indicator functions are periodic in alpha_i with period M_i = lcm(ord_b p_i, ord_b2 p_i); so inclusion
    is decided exactly on prod [0,M_i)."""
    Ms = [lcm([order_brute(p, b), order_brute(p, b2)]) for p in P]
    inc = rev = True
    for al in product(*[range(M) for M in Ms]):
        x, y = in_Lambda(al, P, b), in_Lambda(al, P, b2)
        if x and not y:
            inc = False
        if y and not x:
            rev = False
        if not inc and not rev:
            break
    return "EQUAL" if inc and rev else "ENLARGE" if inc else "SHRINK" if rev else "INCOMPARABLE"


# ------------------------------------------------------------------ planar geometry (re-implemented)
def seg_line(p, q):
    A, B = q[1] - p[1], p[0] - q[0]
    C = A * p[0] + B * p[1]
    g = gcd(gcd(abs(A), abs(B)), abs(C)) or 1
    A, B, C = A // g, B // g, C // g
    return (A, B, C) if (A > 0 or (A == 0 and B > 0)) else (-A, -B, -C)


def cell_polygon(vs):
    """vs: set of integer vertices of a cell -> ordered corner list (point, segment, or parallelogram hull)."""
    vs = sorted(vs)
    if len(vs) <= 2:
        return vs
    # parallelogram: order around the centroid
    cx = sum(Fr(v[0]) for v in vs) / 4
    cy = sum(Fr(v[1]) for v in vs) / 4
    import math
    return sorted(vs, key=lambda v: math.atan2(float(v[1] - cy), float(v[0] - cx)))


def contains(poly, pt):
    x, y = pt
    if len(poly) == 1:
        return (x, y) == (Fr(poly[0][0]), Fr(poly[0][1]))
    if len(poly) == 2:
        (x1, y1), (x2, y2) = poly
        return ((x2 - x1) * (y - y1) == (y2 - y1) * (x - x1)
                and min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2))
    sgn = 0
    n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        cr = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
        if cr != 0:
            s = 1 if cr > 0 else -1
            if sgn == 0:
                sgn = s
            elif s != sgn:
                return False
    return True


def arrangement_samples(polys, box):
    lines = {(1, 0, 0), (1, 0, box), (0, 1, 0), (0, 1, box)}
    for pl in polys:
        n = len(pl)
        if n == 2:
            lines.add(seg_line(*pl))
        elif n == 4:
            for i in range(4):
                lines.add(seg_line(pl[i], pl[(i + 1) % 4]))
    L = sorted(lines)
    V = set()
    for i in range(len(L)):
        A1, B1, C1 = L[i]
        for j in range(i + 1, len(L)):
            A2, B2, C2 = L[j]
            dt = A1 * B2 - A2 * B1
            if dt:
                x, y = Fr(C1 * B2 - C2 * B1, dt), Fr(A1 * C2 - A2 * C1, dt)
                if 0 <= x <= box and 0 <= y <= box:
                    V.add((x, y))
    for pl in polys:
        if len(pl) == 1:
            V.add((Fr(pl[0][0]), Fr(pl[0][1])))
    xs = sorted({v[0] for v in V} | {Fr(0), Fr(box)})
    S = set(V)
    sloped = [l for l in L if l[1] != 0]
    for lo, hi in zip(xs, xs[1:]):
        xm = (lo + hi) / 2
        ys = sorted({Fr(c - a * xm, bb) for a, bb, c in sloped if 0 <= Fr(c - a * xm, bb) <= box})
        S.update((xm, y) for y in ys)
        S.update((xm, (y1 + y2) / 2) for y1, y2 in zip(ys, ys[1:]))
    for a, bb, c in L:
        if bb == 0:
            xv = Fr(c, a)
            ys = sorted({v[1] for v in V if v[0] == xv} | {Fr(0), Fr(box)})
            S.update((xv, (y1 + y2) / 2) for y1, y2 in zip(ys, ys[1:]))
    return sorted(S)


def planar_compare(cells_s, cells_t, box):
    """cells_*: dict dim -> set(frozenset(vertices)).  Returns exact comparison data."""
    ps = [(d, cell_polygon(c)) for d in (0, 1, 2) for c in sorted(cells_s[d], key=sorted)]
    pt = [(d, cell_polygon(c)) for d in (0, 1, 2) for c in sorted(cells_t[d], key=sorted)]
    S = arrangement_samples([p for _, p in ps] + [p for _, p in pt], box)
    in_t = [any(contains(p, s) for _, p in pt) for s in S]
    in_s = [any(contains(p, s) for _, p in ps) for s in S]
    per = {0: [0, 0], 1: [0, 0], 2: [0, 0]}
    for d, pl in ps:
        bad = any(contains(pl, s) and not in_t[i] for i, s in enumerate(S))
        per[d][1 if bad else 0] += 1
    s_not_t = any(a and not b for a, b in zip(in_s, in_t))
    t_not_s = any(b and not a for a, b in zip(in_s, in_t))
    rel = "EQUAL" if not s_not_t and not t_not_s else "U_SUBSET_U2" if not s_not_t else "U2_SUBSET_U" if not t_not_s else "INCOMPARABLE"
    return {"relation": rel, "per_dim_contained_partial": per, "n_samples": len(S), "S": S, "ps": ps, "pt": pt,
            "in_s": in_s, "in_t": in_t}


def probes(n=3000, box=4, den=24):
    out, s = [], 12345
    for _ in range(n):
        s = (s * 1103515245 + 12345) % 2 ** 31
        a = s % (box * den + 1)
        s = (s * 1103515245 + 12345) % 2 ** 31
        b = s % (box * den + 1)
        out.append((Fr(a, den), Fr(b, den)))
    return out


def union_betti_mod(ps, S, p):
    """Betti numbers b0,b1,b2 of the union by the nerve of its cells (incidence at the exact samples), mod p."""
    n = len(ps)
    inc = []
    for _, pl in ps:
        inc.append(frozenset(i for i, s in enumerate(S) if contains(pl, s)))
    keep = [i for i in range(n) if not any(j != i and inc[i] <= inc[j] and (inc[i] != inc[j] or j < i) for j in range(n))]
    sets = [inc[i] for i in keep]

    def nonempty(t):
        cur = sets[t[0]]
        for k in t[1:]:
            cur = cur & sets[k]
            if not cur:
                return False
        return True
    return nerve_betti_mod(nonempty, len(sets), 3, p)


# ------------------------------------------------------------------ homology mod p
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


def nerve_betti_mod(sets_nonempty, n, maxdim, p):
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
        rows = [{idx[s[:q] + s[q + 1:]]: (-1) ** q for q in range(len(s))} for s in simp[d]]
        ranks[d] = rank_mod(rows, p)
    counts = [len(s) for s in simp]
    return [counts[j] - ranks[j] - ranks[j + 1] for j in range(maxdim)]


def complex_betti_planar(cells, p):
    """Betti numbers of the abstract complex (dims 0,1,2) mod p, boundary from lex-min base + generators."""
    V = sorted(cells[0], key=sorted)
    vidx = {sorted(c)[0]: i for i, c in enumerate(V)}
    E = sorted(cells[1], key=sorted)
    eidx = {c: i for i, c in enumerate(E)}
    rows1 = []
    for c in E:
        a, b = sorted(c)
        rows1.append({vidx[b]: 1, vidx[a]: -1})
    rows2 = []
    for c in sorted(cells[2], key=sorted):
        vs = sorted(c)
        base = vs[0]
        # the two edge directions at the lex-min vertex are the two neighbours among the 4 corners that
        # differ from base by a generator: those whose sum relation closes the parallelogram
        rest = vs[1:]
        found = None
        for i, j in combinations(range(3), 2):
            k = 3 - i - j
            g = (rest[i][0] - base[0], rest[i][1] - base[1])
            h = (rest[j][0] - base[0], rest[j][1] - base[1])
            if (base[0] + g[0] + h[0], base[1] + g[1] + h[1]) == rest[k]:
                found = (rest[i], rest[j], rest[k])
        a, b, d = found
        # oriented boundary of the parallelogram base->a->d->b->base
        loop = [(base, a), (a, d), (d, b), (b, base)]
        row = {}
        for u, w in loop:
            key = frozenset([u, w])
            sign = 1 if u < w else -1
            row[eidx[key]] = row.get(eidx[key], 0) + sign
        rows2.append(row)
    r1, r2 = rank_mod(rows1, p), rank_mod(rows2, p)
    return [len(V) - r1, len(E) - r1 - r2, len(cells[2]) - r2]
