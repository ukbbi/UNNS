"""E2-P2: abstract-cell transport and exact PLANAR geometric transport (k = 2).

Abstract layer reuses the frozen E2-P1 engine (src/inherited/).  Planar geometry: every cell is a point, segment or
parallelogram with integer corners.  The union U is analysed on the line arrangement of all cell edges of source and
target (plus the bounding box).  Every relatively open face of that arrangement contains one SAMPLE point produced
by the strip construction below, so  P <= U'  iff every sample in P lies in U'  (exact, rational arithmetic).
Intersections of closed convex cells are unions of arrangement faces, so cell incidence at the samples gives the
exact nerve (nerve theorem => Betti numbers of U).
"""
import os
import sys
from fractions import Fraction as Fr
from itertools import combinations
from math import gcd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "inherited"))
import e1_cell_transport as ct0  # noqa: E402   (frozen E2-P1 engine)
import fibre_transport as ft  # noqa: E402


def complex_of(primes, b, q, graver):
    F = tuple(sorted(a for a in __import__("itertools").product(*[range(m + 1) for m in q])
                     if any(a) and __import__("lattice_transport").in_lambda(a, primes, b)))
    G = ft.oriented(graver)
    return F, G, ct0.build_complex(F, G, len(q))


def abstract_survival(cx_s, cx_t):
    return ct0.abstract_survival(cx_s, cx_t)


# ------------------------------------------------------------------ planar primitives
def _line(p, q):
    (x1, y1), (x2, y2) = p, q
    A, B = y2 - y1, x1 - x2
    C = A * x1 + B * y1
    g = gcd(gcd(abs(A), abs(B)), abs(C)) or 1
    A, B, C = A // g, B // g, C // g
    if A < 0 or (A == 0 and B < 0):
        A, B, C = -A, -B, -C
    return (A, B, C)


def _in_cell(p, cell_pts):
    """closed membership of rational point p in point / segment / parallelogram (corner list)."""
    x, y = p
    n = len(cell_pts)
    if n == 1:
        return p == (Fr(cell_pts[0][0]), Fr(cell_pts[0][1]))
    xs = [c[0] for c in cell_pts]
    ys = [c[1] for c in cell_pts]
    if x < min(xs) or x > max(xs) or y < min(ys) or y > max(ys):
        return False
    if n == 2:
        (x1, y1), (x2, y2) = cell_pts
        return (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) == 0
    base = cell_pts[0]
    others = [c for c in cell_pts[1:]]
    # parallelogram corners: base, base+g1, base+g2, base+g1+g2  (sorted lex): find g1,g2 as the two with a
    # difference-sum equal to the fourth corner
    for i, j in combinations(range(3), 2):
        g1 = (others[i][0] - base[0], others[i][1] - base[1])
        g2 = (others[j][0] - base[0], others[j][1] - base[1])
        k = 3 - i - j
        if (base[0] + g1[0] + g2[0], base[1] + g1[1] + g2[1]) == tuple(others[k]):
            det = g1[0] * g2[1] - g1[1] * g2[0]
            s = Fr((x - base[0]) * g2[1] - (y - base[1]) * g2[0], det)
            t = Fr(g1[0] * (y - base[1]) - g1[1] * (x - base[0]), det)
            return 0 <= s <= 1 and 0 <= t <= 1
    raise AssertionError("not a parallelogram")


def cell_corners(cx):
    out = []
    for j in sorted(cx):
        for key, c in cx[j].items():
            out.append({"dim": j, "key": key, "base": c.base, "gens": c.gens, "pts": [tuple(v) for v in c.verts]})
    return out


def _lines_of(cells):
    L = set()
    for c in cells:
        if c["dim"] == 1:
            L.add(_line(*c["pts"]))
        elif c["dim"] == 2:
            b, (g1, g2) = c["base"], c["gens"]
            p = [b, (b[0] + g1[0], b[1] + g1[1]), (b[0] + g2[0], b[1] + g2[1]),
                 (b[0] + g1[0] + g2[0], b[1] + g1[1] + g2[1])]
            L.add(_line(p[0], p[1]))
            L.add(_line(p[0], p[2]))
            L.add(_line(p[1], p[3]))
            L.add(_line(p[2], p[3]))
    return L


def samples_for(cells_all, box):
    """Exact sample set of the arrangement of all edges in cells_all (list of cell dicts) in [0,h]^2."""
    h0, h1 = Fr(0), Fr(box)
    lines = _lines_of(cells_all) | {(1, 0, 0), (1, 0, int(box)), (0, 1, 0), (0, 1, int(box))}
    lines = sorted(lines)
    verts = set()
    for (A1, B1, C1), (A2, B2, C2) in combinations(lines, 2):
        det = A1 * B2 - A2 * B1
        if det == 0:
            continue
        x = Fr(C1 * B2 - C2 * B1, det)
        y = Fr(A1 * C2 - A2 * C1, det)
        if 0 <= x <= box and 0 <= y <= box:
            verts.add((x, y))
    for c in cells_all:
        if c["dim"] == 0:
            verts.add((Fr(c["pts"][0][0]), Fr(c["pts"][0][1])))
    xs = sorted({v[0] for v in verts} | {h0, h1})
    nonvert = [(A, B, C) for (A, B, C) in lines if B != 0]
    S = set(verts)
    for xa, xb in zip(xs, xs[1:]):
        xm = (xa + xb) / 2
        ys = sorted({Fr(C - A * xm, B) for (A, B, C) in nonvert})
        ys = [y for y in ys if 0 <= y <= box]
        for y in ys:
            S.add((xm, y))
        for ya, yb in zip(ys, ys[1:]):
            S.add((xm, (ya + yb) / 2))
    vlines = sorted({Fr(C, A) for (A, B, C) in lines if B == 0})
    for xv in vlines:
        ys = sorted({v[1] for v in verts if v[0] == xv} | {Fr(0), Fr(box)})
        for ya, yb in zip(ys, ys[1:]):
            S.add((xv, (ya + yb) / 2))
    return sorted(S)


def incidence(cells, S):
    """list of bitmasks (one per cell) over the sample list S."""
    masks = []
    for c in cells:
        m = 0
        for i, p in enumerate(S):
            if _in_cell(p, c["pts"]):
                m |= 1 << i
        masks.append(m)
    return masks


def pt_json(p):
    return [str(p[0]), str(p[1])]


def planar_transport(cx_s, cx_t, box):
    """Exact geometric comparison of U (source) and U' (target) in [0,box]^2.  Returns a JSON-ready dict."""
    cs, ct_ = cell_corners(cx_s), cell_corners(cx_t)
    S = samples_for(cs + ct_, box)
    ms, mt = incidence(cs, S), incidence(ct_, S)
    US = 0
    UT = 0
    for m in ms:
        US |= m
    for m in mt:
        UT |= m
    per = {}
    partial = []
    for c, m in zip(cs, ms):
        out = m & ~UT
        st = "CONTAINED" if out == 0 else "PARTIAL"
        per.setdefault(c["dim"], {"CONTAINED": 0, "PARTIAL": 0})[st] += 1
        if out:
            i = (out & -out).bit_length() - 1
            partial.append({"dim": c["dim"], "base": list(c["base"]), "gens": [list(g) for g in c["gens"]],
                            "witness_not_in_target_union": pt_json(S[i])})
    back_out = UT & ~US
    wit_back = None
    if back_out:
        i = (back_out & -back_out).bit_length() - 1
        wit_back = pt_json(S[i])
    rel = ("EQUAL" if US == UT else "U_SUBSET_U2" if US & ~UT == 0 else "U2_SUBSET_U" if UT & ~US == 0
           else "INCOMPARABLE")
    return {"n_samples": len(S), "source_cells_vs_target_union": {str(k): v for k, v in sorted(per.items())},
            "partial_cells": partial, "union_relation": rel, "witness_target_not_in_source": wit_back,
            "_masks": (cs, ct_, ms, mt, S)}


def nerve_of_union(cells, masks, maxdim=3):
    """Betti numbers of the union via nerve of the geometrically maximal cells."""
    keep = []
    for i, m in enumerate(masks):
        redundant = False
        for j, m2 in enumerate(masks):
            if j != i and (m & ~m2) == 0 and (m != m2 or j < i):
                redundant = True
                break
        if not redundant:
            keep.append(i)
    # compress sample set to the distinct incidence columns
    sub = [masks[i] for i in keep]
    # re-index samples: only columns that occur
    cols = {}
    for pos, m in enumerate(sub):
        mm = m
        while mm:
            lsb = mm & -mm
            cols.setdefault(lsb.bit_length() - 1, []).append(pos)
            mm ^= lsb
    pattern = {}
    for col, poss in cols.items():
        pattern.setdefault(tuple(poss), len(pattern))
    new = [0] * len(sub)
    for pat, idx in pattern.items():
        for pos in pat:
            new[pos] |= 1 << idx
    nb = ct0.nerve_betti(new, maxdim=maxdim)
    return {"maximal_cells": len(keep), "betti_b0_b1_b2": nb["betti"][:3], "nerve_simplex_counts": nb["simplex_counts"],
            "maximal_cell_list": [{"dim": cells[i]["dim"], "base": list(cells[i]["base"]),
                                   "gens": [list(g) for g in cells[i]["gens"]]} for i in keep]}


def planar_embedded(cx, cells, masks):
    """Any two cells meet in a common face (or not at all)?  Returns (bool, witness)."""
    idx = {c["key"]: i for i, c in enumerate(cells)}
    facemask = {}
    for i, c in enumerate(cells):
        facemask[i] = masks[i]
    face_lists = {}
    for j in cx:
        for key, cell in cx[j].items():
            face_lists[key] = set(ct0.faces_of(cell).keys())
    n = len(cells)
    for i in range(n):
        for j in range(i + 1, n):
            inter = masks[i] & masks[j]
            if not inter:
                continue
            common = face_lists[cells[i]["key"]] & face_lists[cells[j]["key"]]
            if not any(masks[idx[k]] == inter for k in common):
                return False, {"cells": [cells[i]["key"], cells[j]["key"]]}
    return True, None
