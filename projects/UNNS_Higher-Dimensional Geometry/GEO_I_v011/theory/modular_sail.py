"""GEO-I v010, Programme A: explicit modular-sail covers for the hollow box Q = (d,d)   (THEOREMS G10-S1, G10-S2; proofs in MATHEMATICS.md section 2).

Setting (frozen, hollow.py): Gamma = {(i,j): j = s*i mod d}, t = s^-1 mod d, F = Gamma cap [0,d]^2 minus {0}, H0 = conv F, A=(0,d), B=(d,0), C=(d,d),
T1 = tri(A, P_{d-t}, C), T2 = tri(B, P_{d-1}, C), P_i = (i, s i mod d).  A CELL is (u,g,h): g,h Graver elements of Gamma (conformally minimal), lex-positive,
linearly independent, with all four corners u, u+g, u+h, u+g+h in F (frozen geo2lib.build_cells).  U0 = union of all cells and Graver segments with corners in F.

G10-S1 (d = s*m + 1, s >= 2, m >= 2):   conv(F) = quadrilateral (0,d),(1,s),(d,0),(d,d);   conv(F) = U1 u T1 u R2 u T2,
        U1 = parallelogram (0,d),(1,s),(d,0),(d-1,d-s) = union of the s cells P((km, d-k); (1, s-d), (m, -1)),  k = 0..s-1,
        R2 = triangle (m,d-1),(d-1,d-s),C = half of the cell P((m-1, d-1-s); (1,s), (d-m,1)).
G10-S2 (d = s*M - 1, s >= 3, M >= 3; here t = M):   conv(F) = pentagon (0,d),(1,s),(M,1),(d,0),(d,d);  conv(F) \\ (T1 u T2) is covered by the four cells
        P(A; (1,s-d), (M-1,1-s)),  P(N; (1,s-d), (d-M,-1)),  P(A; (d-M,-1), (M-1,1-s)),  P((d-M-1, d-s-1); (1,s), (M,1)),   N = (M-1, d+1-s)
        (the first three are the three faces of the zonotope A + [0,1](1,s-d) + [0,1](M-1,1-s) + [0,1](d-M,-1), the fourth contains the triangle R2).
By the transposition (i,j) -> (j,i) (Gamma_{d,s} <-> Gamma_{d,t}, T1(s) <-> T2(t), cells <-> cells) the same holds when the roles of s and t = s^-1 are exchanged.
Everything below is exact (integers/Fractions) and is used both to build the covers and to re-verify them, independently of the v005 cell engine."""
from fractions import Fraction as Fr
from math import gcd
import itertools


def inv(s, d): return pow(s, -1, d)
def in_gamma(d, s, p): return (p[1] - s * p[0]) % d == 0
def fibre(d, s):
    """F = Gamma cap [0,d]^2 minus the origin: for each x the y in [0,d] with y = s x mod d (two values y = 0, d when d | s x)"""
    out = []
    for x in range(d + 1):
        y = (s * x) % d
        for yy in ((y, y + d) if y == 0 else (y,)):
            if yy <= d and (x or yy): out.append((x, yy))
    return out


def is_graver(d, s, g):
    """g in Gamma is Graver iff no other nonzero lattice vector lies in the closed box spanned by 0 and g with the same sign pattern (exact scan)."""
    if g == (0, 0) or not in_gamma(d, s, g): return False
    sa = 1 if g[0] >= 0 else -1; sb = 1 if g[1] >= 0 else -1
    return not any((a, b) not in ((0, 0), (abs(g[0]), abs(g[1]))) and in_gamma(d, s, (sa * a, sb * b)) for a in range(abs(g[0]) + 1) for b in range(abs(g[1]) + 1))


def lexpos(g): return g > (0, 0)
def corners(c): u, g, h = c; return [u, (u[0] + g[0], u[1] + g[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1]), (u[0] + h[0], u[1] + h[1])]
def det(g, h): return g[0] * h[1] - g[1] * h[0]


def is_cell(d, s, c, Fset=None):
    u, g, h = c; Fs = Fset if Fset is not None else set(fibre(d, s))
    return lexpos(g) and lexpos(h) and det(g, h) != 0 and is_graver(d, s, g) and is_graver(d, s, h) and all(p in Fs for p in corners(c))


def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull(P):
    P = sorted(set(P))
    def half(pts):
        h = []
        for p in pts:
            while len(h) >= 2 and cross(h[-2], h[-1], p) <= 0: h.pop()
            h.append(p)
        return h
    lo = half(P); up = half(P[::-1]); return lo[:-1] + up[:-1]


def area2(P): return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))


def clip(P, a, b, c):
    """part of the convex polygon P (list of Fraction pairs) with a x + b y + c >= 0"""
    out = []
    n = len(P)
    for i in range(n):
        p, q = P[i], P[(i + 1) % n]; fp = a * p[0] + b * p[1] + c; fq = a * q[0] + b * q[1] + c
        if fp >= 0: out.append(p)
        if (fp > 0 and fq < 0) or (fp < 0 and fq > 0):
            t = fp / (fp - fq); out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def halfplanes(poly):
    """closed halfplanes a x + b y + c >= 0 (as Fractions) of a convex polygon given by its vertices in any orientation"""
    P = [(Fr(x), Fr(y)) for x, y in poly]
    if area2(P) < 0: P = P[::-1]
    out = []
    for i in range(len(P)):
        p, q = P[i], P[(i + 1) % len(P)]; a = -(q[1] - p[1]); b = q[0] - p[0]; out.append((a, b, -(a * p[0] + b * p[1])))
    return out


def subtract(pieces, region):
    """pieces minus the convex region (given by its halfplanes), as a list of convex pieces of positive area (closures)."""
    new = []
    for pc in pieces:
        r = pc
        for (a, b, c) in region:
            o = clip(r, -a, -b, -c)
            if len(o) >= 3 and area2(o) > 0: new.append(o)
            r = clip(r, a, b, c)
            if len(r) < 3 or area2(r) <= 0: r = None; break
    return new


def hollow_triangles(d, s):
    t = inv(s, d); return [((0, d), (d - t, d - 1), (d, d)), ((d, 0), (d - 1, d - s), (d, d))]


def remainder_area2(d, s, cells):
    """twice the area of conv(F) minus (T1 u T2 u cells) -- 0 iff conv(F) is contained in T1 u T2 u (union of the cells)."""
    H = [(Fr(x), Fr(y)) for x, y in hull(fibre(d, s))]; pieces = [H]
    for T in hollow_triangles(d, s): pieces = subtract(pieces, halfplanes(T))
    for c in cells: pieces = subtract(pieces, halfplanes(corners(c)))
    return sum(area2(p) for p in pieces)


# ---------------------------------------------------------------------------------------------------------------- the two families
def family_S1(d, s):
    """cells for d = s*m + 1 (s >= 2, m >= 2) or None"""
    if s < 2 or d % s != 1 or (d - 1) // s < 2: return None
    m = (d - 1) // s
    cells = [((k * m, d - k), (1, s - d), (m, -1)) for k in range(s)]
    cells.append(((m - 1, d - 1 - s), (1, s), (d - m, 1)))
    return cells


def family_S2(d, s):
    """cells for d = s*M - 1 (s >= 3, M >= 3) or None"""
    if s < 3 or (d + 1) % s != 0 or (d + 1) // s < 3: return None
    M = (d + 1) // s; A = (0, d); N = (M - 1, d + 1 - s); g = (1, s - d); h = (d - M, -1); h4 = (M - 1, 1 - s)
    return [(A, g, h4), (N, g, h), (A, h4, h), ((d - M - 1, d - s - 1), (1, s), (M, 1))]


def normalise(d, c):
    """re-express the parallelogram with corner set corners(c) as (u,g,h) with u the lexicographically smallest corner and lex-positive g<h (engine convention)"""
    pts = sorted(corners(c)); u = pts[0]; rest = pts[1:]
    for a, b in itertools.combinations(rest, 2):
        third = [p for p in rest if p not in (a, b)][0]
        if (a[0] + b[0] - u[0], a[1] + b[1] - u[1]) == third:
            g = (a[0] - u[0], a[1] - u[1]); h = (b[0] - u[0], b[1] - u[1]); return (u, min(g, h), max(g, h))
    raise ValueError('not a parallelogram')


def transpose_cell(c):
    """image of the cell under the coordinate swap (x,y) -> (y,x), normalised to the engine convention"""
    cs = [(q[1], q[0]) for q in corners(c)]
    return normalise(0, (cs[0], (cs[1][0] - cs[0][0], cs[1][1] - cs[0][1]), (cs[3][0] - cs[0][0], cs[3][1] - cs[0][1])))


def sail_cover(d, s):
    """(family name, cells in the coordinates of Gamma_{d,s}) if d,s fall under G10-S1 or G10-S2 directly or after transposition (s -> t = s^-1), else None"""
    for name, fam in (('S1', family_S1), ('S2', family_S2)):
        c = fam(d, s)
        if c is not None: return name, [normalise(d, x) for x in c], False
    t = inv(s, d)
    for name, fam in (('S1', family_S1), ('S2', family_S2)):
        c = fam(d, t)
        if c is not None: return name, [transpose_cell(x) for x in c], True
    return None


def verify_cover(d, s):
    """exact verification of one instance: returns dict with the checks (all must be True)."""
    r = sail_cover(d, s)
    if r is None: return None
    name, cells, tr = r; Fs = set(fibre(d, s))
    ok_cells = all(is_cell(d, s, c, Fs) for c in cells)
    H = hull(list(Fs)); rem = remainder_area2(d, s, cells)
    return {'d': d, 's': s, 'family': name, 'transposed': tr, 'cells': len(cells), 'cells_valid': ok_cells, 'remainder_area2': int(rem), 'hull_vertices': len(H)}


# ---------------------------------------------------------------------------------------------------------------- the general zonogon cover (THEOREM G10-Z)
def sail_steps(d, s):
    """primitive steps of the lower-left boundary chain of conv(F) from A=(0,d) to B=(d,0): the F points on that chain in order, and the steps between them.
    Every step is (a,-b) with a,b > 0 and the slopes are non-decreasing (convexity)."""
    F = set(fibre(d, s)); H = hull(list(F)); A = (0, d); B = (d, 0)
    iA = H.index(A); iB = H.index(B)
    # hull() returns counter-clockwise vertices: the chain from A to B (lower-left side) is A, ..., B going counter-clockwise from A
    chain = []; i = iA
    while True:
        chain.append(H[i])
        if H[i] == B: break
        i = (i + 1) % len(H)
    pts = [chain[0]]
    for k in range(len(chain) - 1):
        p, q = chain[k], chain[k + 1]
        on = sorted((x for x in F if cross(p, q, x) == 0 and min(p[0], q[0]) <= x[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= x[1] <= max(p[1], q[1])), key=lambda x: x[0])
        pts += [x for x in on if x != p]
    assert all(x in F for x in pts), 'chain point outside F'
    return [(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]


def zonogon_cells(A, steps):
    """tiling of the zonogon A + sum [0,1] v_i, v_i = steps sorted by increasing slope (steep first), by parallelograms P(u; w, v); degenerate (parallel) pairs are omitted.
    Induction: Z_n = Z_{n-1} u (strip swept by the upper path of Z_{n-1} along v_n)."""
    cells = []
    for n in range(1, len(steps)):
        vn = steps[n]; u = A
        # upper-right path of Z_n-1: A -> steps[n-1] -> steps[n-2] -> ... -> steps[0]  (reverse order)
        for w in reversed(steps[:n]):
            if w[0] * vn[1] - w[1] * vn[0] != 0: cells.append((u, w, vn))
            u = (u[0] + w[0], u[1] + w[1])
    return cells


def general_cover(d, s):
    """cells covering conv(F) minus (T1 u T2) for ANY unit s with 2 <= s <= d-2:  the zonogon on the hull steps (g, e_1..e_r, h) and the cell containing R2."""
    steps = sail_steps(d, s); t = inv(s, d)
    cells = [normalise(d, c) for c in zonogon_cells((0, d), steps)]
    cells.append(normalise(d, ((d - t - 1, d - s - 1), (1, s), (t, 1))))
    return cells


def verify_general(d, s):
    cells = general_cover(d, s); Fs = set(fibre(d, s))
    return {'d': d, 's': s, 'cells': len(cells), 'cells_valid': all(is_cell(d, s, c, Fs) for c in cells), 'remainder_area2': int(remainder_area2(d, s, cells))}
