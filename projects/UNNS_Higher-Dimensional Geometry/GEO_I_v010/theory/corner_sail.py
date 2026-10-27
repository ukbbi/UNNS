"""GEO-I v007, Programme A.  The COLUMN-STRIP construction (the mathematically defined replacement of the v006 "corner-sail" idea).

SETTING (frozen).  Gamma = Gamma_(d,s) = {(i,j) in Z^2 : j = s*i (mod d)}, d >= 2, 0 <= s < d (gcd(s,d)=1 where stated), box Q = (Q1,Q2) >= (d,d),
Q != (d,d); F = (Gamma cap [0,Q]) \\ {0}; cells = points, segments, parallelograms P(u;g,h) with independent Graver g,h and all four corners in F;
U = union of cells; H = conv(F).

DEFINITIONS (all integers).
  column i (0 <= i <= Q1):  F_i = {(i,j) in F}.   bottom b_i = (s*i mod d) for i >= 1 and b_0 := d  (the origin is removed);
  K_i = floor((Q2 - b_i)/d)  =  (number of points of column i) - 1;   B_i = (i,b_i);  T_i = (i,b_i + K_i*d)  (bottom and top points).
  Lower envelope  l(x): lower convex envelope of the points B_0..B_Q1 (this IS the lower boundary of H);  upper envelope u(x) of the T_i.
  Lower hull vertices a_0=0<a_1<...<a_r=Q1;  a *lower hull piece* is a pair (B_i,B_i') of bottoms that are consecutive among the bottoms lying on one
  edge of the lower envelope (so the open segment B_iB_i' contains no point of F).  Upper hull pieces likewise for the tops.
CELLS of the construction (Q2 >= 2d):
  (S)  strip cells      P(B_i + k(0,d); (1,delta_i), (0,d)),  0 <= k < min(K_i,K_{i+1}),   delta_i = b_{i+1} - b_i in {s, s-d};
  (M)  mismatch cells   P(T_i; T_{i+1}-T_i, (0,-d))  for K_i != K_{i+1}   (T_{i+1}-T_i = (1,s) or (1,s-d));
  (L)  lower sliver     P(B_i; B_i' - B_i, (0,d))      for every lower hull piece;
  (Up) upper sliver     P(T_i; T_i' - T_i, (0,-d))     for every upper hull piece.
THEOREM A-COL (proved in COVERAGE.md):  if Q2 >= 2d, the cells (S),(M),(L),(Up) are legitimate cells of K_abs and their union contains H.
This module builds the cells and checks every lemma of the proof on the concrete instance in exact arithmetic."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from math import gcd
import modular_layers as ML


def columns(d, s, Q):
    """returns dict i -> (b_i, K_i, B_i, T_i) for 0 <= i <= Q1 (needs Q2 >= d so every column is nonempty except possibly the origin)."""
    out = {}
    for i in range(Q[0] + 1):
        b = d if i == 0 else (s * i) % d
        if b > Q[1]: continue
        K = (Q[1] - b) // d
        out[i] = (b, K, (i, b), (i, b + K * d))
    return out


def lower_pieces(points):
    """points = [(x,y)] with strictly increasing x.  Returns the list of pairs of consecutive points lying on one edge of the LOWER convex envelope
    (includes collinear intermediate points)."""
    hull = []
    for p in points:
        while len(hull) >= 2 and ((hull[-1][0] - hull[-2][0]) * (p[1] - hull[-2][1]) - (hull[-1][1] - hull[-2][1]) * (p[0] - hull[-2][0])) <= 0 \
                and False: hull.pop()
        hull.append(p)
    # strict lower hull (monotone chain), vertices only
    st = []
    for p in points:
        while len(st) >= 2 and ((st[-1][0] - st[-2][0]) * (p[1] - st[-2][1]) - (st[-1][1] - st[-2][1]) * (p[0] - st[-2][0])) <= 0: st.pop()
        st.append(p)
    pieces = []
    for v, w in zip(st, st[1:]):
        on = [p for p in points if v[0] <= p[0] <= w[0] and (w[0] - v[0]) * (p[1] - v[1]) == (w[1] - v[1]) * (p[0] - v[0])]
        on.sort()
        pieces += list(zip(on, on[1:]))
    return pieces


def upper_pieces(points):
    neg = [(x, -y) for x, y in points]
    return [((a[0], -a[1]), (b[0], -b[1])) for a, b in lower_pieces(neg)]


def strip_cells(d, s, Q):
    """the cells (S),(M),(L),(Up) as (u,g,h) triples (u lex-minimal corner as produced by ML.make_cell) with provenance tags."""
    assert Q[1] >= 2 * d, 'Theorem A-COL needs Q2 >= 2d'
    col = columns(d, s, Q); cells = []; tags = []
    def add(corners, tag):
        c = ML.make_cell(corners)
        if c: cells.append(c); tags.append(tag)
    for i in range(Q[0]):
        b0, K0, B0, T0 = col[i]; b1, K1, B1, T1 = col[i + 1]
        m = min(K0, K1)
        for k in range(m):
            add([(i, b0 + k * d), (i + 1, b1 + k * d), (i, b0 + (k + 1) * d), (i + 1, b1 + (k + 1) * d)], ('S', i, k))
        if K0 != K1:
            add([T0, T1, (T0[0], T0[1] - d), (T1[0], T1[1] - d)], ('M', i))
    Bs = [col[i][2] for i in range(Q[0] + 1)]; Ts = [col[i][3] for i in range(Q[0] + 1)]
    for (p, q) in lower_pieces(Bs): add([p, q, (p[0], p[1] + d), (q[0], q[1] + d)], ('L', p[0], q[0]))
    for (p, q) in upper_pieces(Ts): add([p, q, (p[0], p[1] - d), (q[0], q[1] - d)], ('Up', p[0], q[0]))
    return cells, tags


def check_lemmas(d, s, Q):
    """machine check of every ingredient of the proof of Theorem A-COL on the instance; returns dict of booleans / counts."""
    col = columns(d, s, Q); r = {}
    r['all_columns_nonempty'] = len(col) == Q[0] + 1
    r['K_ge_1'] = all(col[i][1] >= 1 for i in col)                                  # Lemma 1
    r['K_step_le_1'] = all(abs(col[i][1] - col[i + 1][1]) <= 1 for i in range(Q[0]))   # Lemma 2
    r['bottom_step'] = all(((col[i + 1][0] - col[i][0]) in (s, s - d)) for i in range(Q[0]))  # Lemma 2
    G = ML.graver_set(d, s)
    r['bridges_graver'] = (1, s) in G and (1, s - d) in G and (0, d) in G                # Lemma 3
    Bs = [col[i][2] for i in range(Q[0] + 1)]; Ts = [col[i][3] for i in range(Q[0] + 1)]
    lp = lower_pieces(Bs); up = upper_pieces(Ts)
    r['hull_pieces_graver'] = all(((q[0] - p[0], q[1] - p[1]) in G) for p, q in lp + up)   # Lemma E
    r['sliver_height'] = all(b <= d for b, K, B, T in col.values()) and all(Q[1] - T[1] < d for b, K, B, T in col.values())  # Lemma 5
    return r


def verify_col_box(d, s, Q):
    cells, tags = strip_cells(d, s, Q)
    F = set(ML.fibre(d, s, Q)); G = ML.graver_set(d, s)
    bad = [c for c in cells if not ML.legit(d, s, Q, c, F, G)]
    if bad: return {'ok': False, 'why': 'illegal', 'cells': bad[:2]}
    ok, n = ML.covered(d, s, Q, list(dict.fromkeys(cells)))
    return {'ok': ok, 'n_cells': len(set(cells)), 'uncovered_pieces': n, 'lemmas': check_lemmas(d, s, Q)}
