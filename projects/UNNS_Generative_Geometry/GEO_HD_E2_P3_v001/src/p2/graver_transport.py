"""E2-P2 / P2-T2, P2-T3: Graver-generator survival from arithmetic data, without building the target complex."""
import os
import sys
from itertools import product

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "inherited"))
import lattice_transport as lt  # noqa: E402


def conformal_le(g, h):
    return all(a * c >= 0 and abs(a) <= abs(c) for a, c in zip(g, h))


def graver_fast(primes, b, q):
    """Region Graver set: nonzero conformally minimal vectors of Lambda_b in [-q,q].  v is minimal iff no nonzero
    proper conformal subvector (searched in the sub-box of v) lies in Lambda_b."""
    out = []
    for v in product(*[range(-m, m + 1) for m in q]):
        if not any(v) or not lt.in_lambda(v, primes, b):
            continue
        ranges = [range(0, a + 1) if a >= 0 else range(a, 1) for a in v]
        minimal = True
        for w in product(*ranges):
            if any(w) and w != v and lt.in_lambda(w, primes, b):
                minimal = False
                break
        if minimal:
            out.append(v)
    return tuple(sorted(out))


def survives(g, primes, b2):
    """P2-T2: g in Lambda_b (so in Lambda_b2 when ENLARGE/EQUAL) is a region-Graver vector of Lambda_b2 iff
    g in Lambda_b2 and no nonzero proper conformal subvector (bounded sub-box of g) is in Lambda_b2."""
    if not lt.in_lambda(g, primes, b2):
        return False
    ranges = [range(0, a + 1) if a >= 0 else range(a, 1) for a in g]
    for w in product(*ranges):
        if any(w) and w != tuple(g) and lt.in_lambda(w, primes, b2):
            return False
    return True


def order_rule_blocks(g, primes, b2):
    """Necessary-condition (axis/order rule): if |g_i| >= ord_b2(p_i) and g is not +-ord*e_i, then
    +-ord*e_i is a nonzero proper conformal subvector in Lambda_b2, so g does NOT survive.  O(k) test."""
    ms = lt.orders(primes, b2)
    supp = [i for i, t in enumerate(g) if t]
    for i, m in enumerate(ms):
        if abs(g[i]) >= m and not (len(supp) == 1 and supp[0] == i and abs(g[i]) == m):
            return True
    return False


def predict(Gor_src, primes, b2):
    surv = [g for g in Gor_src if survives(g, primes, b2)]
    lost = [g for g in Gor_src if g not in surv]
    return {"survive": surv, "lost": lost}


# ------------------------------------------------------------------ P2-F21 closed forms
def c_r(lo, hi, r, m):
    """#{n in [lo,hi]: n = r mod m}"""
    if hi < lo:
        return 0
    return (hi - r) // m - (lo - 1 - r) // m


def lattice_points_in_rect(I, J, classes):
    """classes: list of (rI, rJ, m) triples describing the union of cosets (rI mod m, rJ mod m); here planar,
    one-parameter families a = c*b + r handled by the callers.  Kept generic: count by residue pairing."""
    return sum(c_r(I[0], I[1], r1, m) * c_r(J[0], J[1], r2, m) for r1, r2, m in classes)


SRC_CLASSES = [(r, r, 4) for r in range(4)]             # a = b (mod 4)
TGT_CLASSES = [(r, r, 2) for r in range(2)]             # a = b (mod 2)


def edge_count(h, g, classes):
    """# edges {u,u+g}: u, u+g in Lambda cap [0,h]^2 minus {0}, for a fixed oriented move g."""
    I = (max(0, -g[0]), h - max(0, g[0]))
    J = (max(0, -g[1]), h - max(0, g[1]))
    n = lattice_points_in_rect(I, J, classes)
    if g[0] >= 0 and g[1] >= 0:
        n -= 1                                           # u = 0 is not a vertex
    return n


SRC_MOVES = [(0, 4), (1, -3), (1, 1), (2, -2), (3, -1), (4, 0)]
TGT_MOVES = [(0, 2), (1, -1), (1, 1), (2, 0)]


def family_counts(h):
    """Closed-form counts for P2-F21, every h >= 1 (theorem P2-TF1): the region Graver set is the full Graver set
    intersected with the box [-h,h]^2 (Lemma P2-L1), so only moves with max|g_i| <= h occur."""
    sm = [g for g in SRC_MOVES if max(abs(t) for t in g) <= h]
    tm = [g for g in TGT_MOVES if max(abs(t) for t in g) <= h]
    src = sum(edge_count(h, g, SRC_CLASSES) for g in sm)
    tgt = sum(edge_count(h, g, TGT_CLASSES) for g in tm)
    kept = edge_count(h, (1, 1), SRC_CLASSES)
    nV_src = lattice_points_in_rect((0, h), (0, h), SRC_CLASSES) - 1
    nV_tgt = lattice_points_in_rect((0, h), (0, h), TGT_CLASSES) - 1
    return {"h": h, "V_src": nV_src, "V_tgt": nV_tgt, "E_src": src, "E_tgt": tgt, "E_kept": kept, "E_lost": src - kept,
            "E_new": tgt - kept}
