"""GEO-I v005: machine check of the proofs of G5-T3 (s=-1) and G5-T4 (s=+1) -- every step of the hand proof in OBSTRUCTIONS.md.

PROOF OUTLINE (full text in OBSTRUCTIONS.md).  By T-FIN embeddedness is a down-set in Q.  Hence
   Obs = minimal non-embedded boxes   <=>   (W) each claimed box is non-embedded (explicit witness),
                                              (M) every claimed box is *minimal* and every box not dominating one is embedded; since embeddedness is a
                                                  down-set it suffices to exhibit the finitely many maximal boxes not dominating a claimed box and
                                                  prove those embedded (explicit planar graphs).
   Axis boxes (Q1=0 or Q2=0) are one-dimensional and embedded.
This module re-derives (W), (M) *by exact computation for each d* from the definitions only (no use of the template machinery),
and checks the finitely many combinatorial facts (the staircase).  The statements for all d are the theorems; the d-by-d runs are
a regression of the proof's ingredients, not a substitute for the proof."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pure_lattice import fibre, graver_s_plus, graver_s_minus, in_gamma
from planar_embed import embedded, cells, add, sub, det, lexpos, _poly, _open_param_inside


def claimed_T3(d): return [(i, 2 * d + 1 - i) for i in range(1, 2 * d + 1)]
def claimed_T4(d): return [(1, 2 * d), (2, d + 1), (d, d), (d + 1, 2), (2 * d, 1)]
def maximal_T3(d): return [(i, 2 * d - i) for i in range(1, 2 * d)]
def maximal_T4(d): return [(1, 2 * d - 1), (d - 1, d), (d, d - 1), (2 * d - 1, 1)]


def dominates(Q, claimed): return any(Q[0] >= c[0] and Q[1] >= c[1] for c in claimed)


def staircase_ok(claimed, maximal, d, rng):
    """(i) every Q with Q1,Q2>=1 in rng not dominating a claimed box lies below a maximal box;
       (ii) every maximal box and every proper predecessor of a claimed box is non-dominating (=> claimed boxes are minimal)."""
    for Q in rng:
        if Q[0] < 1 or Q[1] < 1: continue
        if not dominates(Q, claimed) and not any(Q[0] <= m[0] and Q[1] <= m[1] for m in maximal): return False, Q
    for m in maximal:
        if dominates(m, claimed): return False, m
    for c in claimed:
        for p in ((c[0] - 1, c[1]), (c[0], c[1] - 1)):
            if p[0] >= 1 and p[1] >= 1 and dominates(p, claimed): return False, p
    return True, None


def witness_T3(d, Q):
    """(Q1+Q2=2d+1).  returns the explicit non-face pair: parallelogram P(u;(1,-1),(a,d-a)) and its chord (a-1,d-a+1).  Q1 = a+1 (1<=a+1<=d+1) or
    the transposed configuration."""
    s = d - 1; G = graver_s_minus(d); F = set(fibre(d, s, Q))
    for transpose in (False, True):
        q = (Q[1], Q[0]) if transpose else Q
        a = q[0] - 1
        if not (0 <= a <= d): continue
        u = (0, d); g = (1, -1); h = (a, d - a)
        corners = [u, add(u, g), add(u, h), add(add(u, g), h)]
        if transpose: corners = [(y, x) for x, y in corners]
        chord_a, chord_b = (add(u, g), add(u, h)) if a >= 1 else (u, add(u, (1, d - 1)))
        if transpose: chord_a, chord_b = (chord_a[1], chord_a[0]), (chord_b[1], chord_b[0])
        v = sub(chord_b, chord_a)
        ok = all(c in F for c in corners) and (v in G or (-v[0], -v[1]) in G) and det(g, h) != 0 and chord_a in F and chord_b in F
        if ok: return {'Q': list(Q), 'corners': corners, 'chord': [list(chord_a), list(chord_b)], 'transpose': transpose, 'a': a}
    return None


def witness_T4(d, Q):
    """explicit non-face pair for s=1: returns the cell and an edge whose relative interior lies in the cell interior."""
    s = 1; G = graver_s_plus(d); F = set(fibre(d, s, Q))
    if Q == (1, 2 * d): u, g, h, e = (0, d), (0, d), (1, 1 - d), ((0, d), (1, d + 1))
    elif Q == (2 * d, 1): u, g, h, e = (d, 0), (d, 0), (1 - d, 1), ((d, 0), (d + 1, 1))   # transposed
    elif Q == (2, d + 1): u, g, h, e = (1, 1), (1, 1), (-1, d - 1), ((1, 1), (1, d + 1))
    elif Q == (d + 1, 2): u, g, h, e = (1, 1), (1, 1), (d - 1, -1), ((1, 1), (d + 1, 1))
    elif Q == (d, d): u, g, h, e = (0, d), (1, 1 - d), (d - 1, -1), ((1, 1), (2, 2))
    else: return None
    corners = [u, add(u, g), add(u, h), add(add(u, g), h)]
    ok = all(c in F for c in corners) and g in G and h in G and det(g, h) != 0 and e[0] in F and e[1] in F
    ev = sub(e[1], e[0]); ok = ok and (ev in G or (-ev[0], -ev[1]) in G)
    if ok:       # the open edge meets the open cell (exact)
        ok = _open_param_inside(e[0], e[1], _poly(u, g, h)) is not None
    return {'Q': list(Q), 'corners': corners, 'edge': [list(e[0]), list(e[1])], 'ok': ok} if ok else None


def check_T3(d, brute=False):
    s = d - 1; claimed = claimed_T3(d); maximal = maximal_T3(d)
    stair, bad = staircase_ok(claimed, maximal, d, [(i, j) for i in range(1, 3 * d + 2) for j in range(1, 3 * d + 2)])
    wit = {c: witness_T3(d, c) for c in claimed}
    # witness is a non-face pair <=> the exact test finds an offending pair (independent confirmation)
    nonemb = all(not embedded(d, s, c) for c in claimed)
    emb = all(embedded(d, s, m) for m in maximal)
    out = {'d': d, 's': s, 'staircase': stair, 'witnesses_explicit': all(w is not None for w in wit.values()),
           'claimed_nonembedded_exact': nonemb, 'maximal_embedded_exact': emb, 'ok': stair and nonemb and emb and all(w is not None for w in wit.values())}
    if brute:
        mins = brute_obs(d, s, 2 * d + 3); out['brute_obs_equals_claim'] = sorted(mins) == sorted(claimed); out['ok'] = out['ok'] and out['brute_obs_equals_claim']
    out['witnesses'] = {str(k): v for k, v in wit.items()}
    return out


def check_T4(d, brute=False):
    assert d >= 3
    claimed = claimed_T4(d); maximal = maximal_T4(d)
    stair, bad = staircase_ok(claimed, maximal, d, [(i, j) for i in range(1, 3 * d + 2) for j in range(1, 3 * d + 2)])
    wit = {c: witness_T4(d, c) for c in claimed}
    nonemb = all(not embedded(d, 1, c) for c in claimed)
    emb = all(embedded(d, 1, m) for m in maximal)
    out = {'d': d, 's': 1, 'staircase': stair, 'witnesses_explicit': all(w is not None for w in wit.values()),
           'claimed_nonembedded_exact': nonemb, 'maximal_embedded_exact': emb, 'ok': stair and nonemb and emb and all(w is not None for w in wit.values())}
    if brute:
        mins = brute_obs(d, 1, 2 * d + 3); out['brute_obs_equals_claim'] = sorted(mins) == sorted(claimed); out['ok'] = out['ok'] and out['brute_obs_equals_claim']
    out['witnesses'] = {str(k): v for k, v in wit.items()}
    return out


def brute_obs(d, s, bound):
    """minimal non-embedded boxes with Q_i <= bound by the independent exact test (complete in the window)."""
    nonemb = set(); mins = []
    for Q in sorted(((i, j) for i in range(1, bound + 1) for j in range(1, bound + 1)), key=lambda q: (sum(q), q)):
        preds = [p for p in ((Q[0] - 1, Q[1]), (Q[0], Q[1] - 1)) if p[0] >= 1 and p[1] >= 1]
        if any(p in nonemb for p in preds): nonemb.add(Q); continue
        if not embedded(d, s, Q): nonemb.add(Q); mins.append(Q)
    return mins
