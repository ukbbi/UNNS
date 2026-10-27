"""GEO-I v012.  The universal small-box cap-cover construction (G12-T3 .. G12-T8), exact (integers / Fractions).

Setting: Gamma = {(i,j): j = s i mod d}, d>=5, 2<=s<=d-2, gcd(s,d)=1, t = s^-1.  Q=(d+u,d+v), 0<=u,v<d, (u,v)!=(0,0).  F_Q, H_Q = conv F_Q.
OMEGA = the boundary of H_Q counter-clockwise from B=(d,0) to A=(0,d), listing ALL Gamma-points on the boundary (collinear ones included).
Cells (all of the form P(w; step, h) with Graver step and h in {(d,0),(0,d)}, plus two bottom cells):
  L-cells  P(w; w2-w, (-d,0)) for consecutive Omega points w,w2 with x>=d both, except the first step (B,b1);
  D-cells  P(w; w2-w, (0,-d)) for consecutive Omega points with y>=d both, except the last step (a1,A);
  bottom cell   P(B-g; g, M)  with M=b1-B, g in {(1,s-d),(d-t,-1)}  (the one with cr(g,M) >= x_M y_M; exists by G11-A, now a theorem);
  left cell     the transpose of the bottom cell for the transposed box (d,t,Q^T).
verify(d,s,u,v): legitimacy of every cell (corners in F_Q, Graver by box scan, independence) and exact rational proof that  H_Q minus (H_0 u cells)  has no area."""
import os, sys
from fractions import Fraction as Fr
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cap_cells as K


def boundary_ccw(F):
    H = K.hull(list(F)); n = len(H); seq = []
    for i in range(n):
        p, q = H[i], H[(i + 1) % n]
        on = sorted((x for x in F if K.cross(p, q, x) == 0 and min(p[0], q[0]) <= x[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= x[1] <= max(p[1], q[1])),
                    key=lambda x: (x[0] - p[0]) ** 2 + (x[1] - p[1]) ** 2)
        seq += on[:-1]
    return seq


def omega(d, s, Q):
    F = K.fibreQ(d, s, Q); seq = boundary_ccw(F); B = (d, 0); A = (0, d)
    i = seq.index(B); seq = seq[i:] + seq[:i]; j = seq.index(A)
    return seq[:j + 1], F


def cell4(corners):
    """four corner points of a parallelogram -> normalised (u,g,h) (K.norm_cell); None if degenerate"""
    S = sorted(set(corners))
    if len(S) != 4: return None
    return K.norm_cell(corners)


def bottom_choice(d, s, M):
    t = K.inv(s, d); x, y = M
    for g in ((1, s - d), (d - t, -1)):
        if g[0] * y - g[1] * x >= x * y: return g
    raise AssertionError('G11-A fails (cannot happen)')


def construct(d, s, u, v):
    Q = (d + u, d + v); Om, F = omega(d, s, Q); cells = []; B = (d, 0); A = (0, d)
    # L- and D-cells
    for k, (w, w2) in enumerate(zip(Om, Om[1:])):
        if w[0] >= d and w2[0] >= d and k > 0:
            c = cell4([w, w2, (w[0] - d, w[1]), (w2[0] - d, w2[1])])
            if c: cells.append(('L', c))
        if w[1] >= d and w2[1] >= d and k < len(Om) - 2:
            c = cell4([w, w2, (w[0], w[1] - d), (w2[0], w2[1] - d)])
            if c: cells.append(('D', c))
    # bottom cell
    if u >= 1:
        b1 = Om[1]; M = (b1[0] - B[0], b1[1] - B[1]); g = bottom_choice(d, s, M)
        p = (B[0] - g[0], B[1] - g[1]); cells.append(('B', cell4([p, B, (p[0] + M[0], p[1] + M[1]), (B[0] + M[0], B[1] + M[1])])))
    # left cell = transposed bottom cell of the transposed configuration (d,t,Q^T): first step there is (a1-A)^T
    if v >= 1:
        a1 = Om[-2]; Mt = (a1[1] - A[1], a1[0] - A[0]); t = K.inv(s, d); g = bottom_choice(d, t, Mt)
        p = (B[0] - g[0], B[1] - g[1]); cT = [p, B, (p[0] + Mt[0], p[1] + Mt[1]), (B[0] + Mt[0], B[1] + Mt[1])]
        cells.append(('T', cell4([(y, x) for x, y in cT])))
    return cells, Om, F


def verify(d, s, u, v):
    Q = (d + u, d + v); cells, Om, F = construct(d, s, u, v); G = {}
    for tag, c in cells:
        cs = K.corners(c)
        if not all(p in F for p in cs): return False, ('corner outside F_Q', tag, c)
        for g in (c[1], c[2]):
            if not K.graver_scan(d, s, g): return False, ('not Graver', tag, g)
        if c[1][0] * c[2][1] - c[1][1] * c[2][0] == 0: return False, ('dependent', tag)
    H = K.hull(list(F)); H0 = K.hull(list(K.fibreQ(d, s, (d, d))))
    pieces = K.subtract([[(Fr(x), Fr(y)) for x, y in H]], K.halfplanes(H0))
    for tag, c in cells:
        pieces = K.subtract(pieces, K.halfplanes(K.corners(c)))
        if not pieces: break
    return (not pieces), ('uncovered pieces', len(pieces))


def sweep(dmin, dmax):
    n = 0; bad = []
    for d in range(dmin, dmax + 1):
        for s in range(2, d - 1):
            if gcd(s, d) != 1: continue
            for u in range(d):
                for v in range(d):
                    if u == v == 0: continue
                    n += 1; ok, info = verify(d, s, u, v)
                    if not ok: bad.append((d, s, u, v, info))
    return n, bad


if __name__ == '__main__':
    a, b = int(sys.argv[1]), int(sys.argv[2]); n, bad = sweep(a, b); print(n, len(bad), bad[:5])


# ----------------------------------------------------------------------------------------------- structural lemmas (checked on every box)
def structure_check(d, s, u, v):
    """Instances of the lemmas used in the proof (G12-L4 .. G12-L6):
    (S1) H_Q cap [0,d]^2 = H_0 (area test);  (S2) every Omega point has x>=d or y>=d (no 'N' points);  (S3) along Omega the x>=d flag is monotone 1..1 0..0 and the y>=d flag 0..0 1..1;
    (S4) no consecutive pair (w,w2) with w in R=(x>=d,y<d) and w2 in T=(x<d,y>=d);  (S5) the first step is B+M with M the record minimum of s*i mod d, i<=u (u>=1);
    (S6) every step is Graver (reflection lemma, exact scan)."""
    Q = (d + u, d + v); Om, F = omega(d, s, Q); H = K.hull(list(F)); H0 = K.hull(list(K.fibreQ(d, s, (d, d))))
    sq = [(Fr(0), Fr(0)), (Fr(d), Fr(0)), (Fr(d), Fr(d)), (Fr(0), Fr(d))]; P = [(Fr(x), Fr(y)) for x, y in H]
    for (a, b, c) in K.halfplanes(sq): P = K.clip(P, a, b, c)
    s1 = len(P) >= 3 and K.area2(P) == K.area2([(Fr(x), Fr(y)) for x, y in H0]) and all(K.pip(H0, p) for p in P)
    a = [1 if w[0] >= d else 0 for w in Om]; b = [1 if w[1] >= d else 0 for w in Om]
    s2 = all(a[i] or b[i] for i in range(len(Om)) if i not in (0,)) or True
    s2 = all((w[0] >= d or w[1] >= d) for w in Om)
    s3 = a == sorted(a, reverse=True) and b == sorted(b)
    s4 = not any(w[0] >= d and w[1] < d and w2[0] < d and w2[1] >= d for w, w2 in zip(Om, Om[1:]))
    s5 = True
    if u >= 1:
        xm, ym = 1, s
        for i in range(1, u + 1):
            if (s * i) % d < ym: xm, ym = i, (s * i) % d
        s5 = Om[1] == (d + xm, ym)
    s6 = all(K.graver_scan(d, s, (w2[0] - w[0], w2[1] - w[1])) for w, w2 in zip(Om, Om[1:]))
    return dict(S1=s1, S2=s2, S3=s3, S4=s4, S5=s5, S6=s6)


def structure_sweep(dmin, dmax):
    n = 0; bad = []
    for d in range(dmin, dmax + 1):
        for s in range(2, d - 1):
            if gcd(s, d) != 1: continue
            for u in range(d):
                for v in range(d):
                    if u == v == 0: continue
                    n += 1; r = structure_check(d, s, u, v)
                    if not all(r.values()): bad.append((d, s, u, v, r))
    return n, bad
