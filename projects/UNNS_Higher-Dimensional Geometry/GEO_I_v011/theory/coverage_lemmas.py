"""GEO-I v007, Programme A: drivers for Theorem A-COL, the HYP-LL classification, the leftover (uncovered-region) routine and the squareless-zone definition.
All checks are exact (Fractions / integers)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from math import gcd
import modular_layers as ML, coverage as C, corner_sail as CS


def units(d): return [s for s in range(1, d) if gcd(s, d) == 1]


def leftover(d, s, Q, cells):
    """convex pieces of conv(F) not covered by the given cells (exact); empty list == covered."""
    F = ML.fibre(d, s, Q); H = C.hull(sorted(F)); pieces = [[(C.mpq(x), C.mpq(y)) for x, y in H]]
    for (u, g, h) in cells:
        hp = C.cell_halfplanes(u, g, h); new = []
        for pc in pieces:
            rem = pc
            for (a, b, c) in hp:
                o = C.clip(rem, -a, -b, -c)
                if len(o) >= 3 and C.area2(o) > 0: new.append(o)
                rem = C.clip(rem, a, b, c)
                if len(rem) < 3 or C.area2(rem) <= 0: rem = None; break
        pieces = new
    return pieces


def centroid(poly):
    n = len(poly); return (sum(p[0] for p in poly) / n, sum(p[1] for p in poly) / n)


def squareless(d, s, Q):
    """St_LL: no nonzero Gamma point in [0,Q1-d]x[0,Q2-d]  (then no d x d square cell exists with lower-left corner in F or at the origin)."""
    r1, r2 = Q[0] - d, Q[1] - d
    return not any((j - s * i) % d == 0 and (i or j) for i in range(r1 + 1) for j in range(r2 + 1))


def hypll_witnesses(d, s, Q):
    """HYP-LL (v006): the corner-sail family of ML.proof_cells covers conv(F).  Returns a witness dict if it does NOT:
    an exact rational point z in conv(F)\\U_family (centroid of an uncovered piece) -- the family, not U, so this does not contradict G7-C1;
    'U_covers_hull' says whether the generic v005 routine shows conv(F) = U for this box."""
    cells, reg = ML.proof_cells(d, s, Q)
    if cells is None: return None
    cells = [c for c in dict.fromkeys(cells) if c]
    rest = leftover(d, s, Q, cells)
    if not rest: return None
    from lattice_model import Lat
    unc = C.uncovered(Lat(d, d, d, s), Q)
    z = centroid(rest[0])
    return {'d': d, 's': s, 'Q': Q, 'regime': reg, 'z': (str(z[0]), str(z[1])), 'pieces': len(rest), 'U_covers_hull': (unc is not None and len(unc) == 0)}


def classify_hypll(dmax):
    out = {'boxes': 0, 'fail': 0, 'fail_with_r_zero': 0, 'fail_other': [], 'U_still_covers': 0, 'examples': []}
    for d in range(3, dmax + 1):
        for s in units(d):
            for q1 in range(d, 3 * d):
                for q2 in range(d, 3 * d):
                    Q = (q1, q2)
                    if Q == (d, d) or max(Q) < 2 * d: continue
                    out['boxes'] += 1
                    w = hypll_witnesses(d, s, Q)
                    if w is None: continue
                    out['fail'] += 1
                    if q1 == d or q2 == d: out['fail_with_r_zero'] += 1
                    else: out['fail_other'].append((d, s, Q))
                    if w['U_covers_hull']: out['U_still_covers'] += 1
                    if len(out['examples']) < 6: out['examples'].append(w)
    return out


def verify_Acol(dmax):
    """Theorem A-COL on all boxes d<=dmax, all units, Q1 in [d,3d], Q2 in [2d,3d]; returns (n_boxes, failures)."""
    n = 0; bad = []
    for d in range(2, dmax + 1):
        for s in (units(d) if d > 2 else [1]):
            for q1 in range(d, 3 * d + 1):
                for q2 in range(2 * d, 3 * d + 1):
                    if (q1, q2) == (d, d): continue
                    n += 1
                    r = CS.verify_col_box(d, s, (q1, q2))
                    if not (r['ok'] and all(r['lemmas'].values())): bad.append((d, s, q1, q2))
    return n, bad


def hypll_step_failures(d, s, Q):
    """HYP-LL as stated in v006: every step (m_i, m_{i+1}) of every corner sail has a legitimate completion by (0,+-d) or (+-d,0) pointing into the box.
    Returns the list of failing steps  (corner, m_i, m_{i+1}) -- each is an exact witness that the hypothesis is false for that box."""
    F = set(ML.fibre(d, s, Q)); G = ML.graver_set(d, s); fails = []
    for corner in ((0, 0), (1, 0), (0, 1), (1, 1)):
        ch = ML.corner_chain(d, s, Q, corner); sx = -1 if corner[0] else 1; sy = -1 if corner[1] else 1
        for (a, pa), (b, pb) in zip(ch, ch[1:]):
            okany = False
            for h in ((0, sy * d), (sx * d, 0)):
                c = ML.make_cell([pa, pb, (pa[0] + h[0], pa[1] + h[1]), (pb[0] + h[0], pb[1] + h[1])])
                if c and ML.legit(d, s, Q, c, F, G): okany = True
            if not okany: fails.append((corner, pa, pb))
    return fails


def classify_hypll_steps(dmax):
    out = {'boxes': 0, 'boxes_failing': 0, 'failing_with_r_zero': 0, 'failing_other': [], 'examples': []}
    for d in range(3, dmax + 1):
        for s in units(d):
            for q1 in range(d, 3 * d):
                for q2 in range(d, 3 * d):
                    Q = (q1, q2)
                    if Q == (d, d): continue
                    out['boxes'] += 1
                    f = hypll_step_failures(d, s, Q)
                    if not f: continue
                    out['boxes_failing'] += 1
                    if q1 == d or q2 == d: out['failing_with_r_zero'] += 1
                    else: out['failing_other'].append([d, s, q1, q2])
                    if len(out['examples']) < 8: out['examples'].append({'d': d, 's': s, 'Q': Q, 'failing_step': f[0]})
    return out
