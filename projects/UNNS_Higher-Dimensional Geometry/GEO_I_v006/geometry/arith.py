"""GEO-III.D  arithmetic of Graver edges: complete Graver basis, crossing offsets, saturation index iota.
Everything depends on (res_i = p_i mod b, b) only."""
import itertools
from math import gcd, prod
from fractions import Fraction as Fr


def order_mod(r, b):
    if b == 1: return 1
    k, x = 1, r % b
    while x != 1 % b:
        x = x * r % b; k += 1
    return k


def in_lambda(res, b, alpha):
    if b == 1: return True
    r = 1
    for p, e in zip(res, alpha): r = r * pow(p, e, b) % b
    return r == 1 % b


def group_order(res, b):
    """|<res_1..res_k>| in (Z/b)^*  =  index [Z^k : Lambda_b]."""
    if b == 1: return 1
    S = {1 % b}; frontier = [1 % b]
    while frontier:
        x = frontier.pop()
        for r in res:
            y = x * r % b
            if y not in S: S.add(y); frontier.append(y)
    return len(S)


def graver_complete(res, b):
    """complete Graver basis (both signs).  Every Graver vector satisfies |g_i| <= ord_b(p_i) (proof in MATHEMATICS.md), so the
    region-Graver computation in that box is complete."""
    k = len(res)
    if b == 1:
        return [tuple((s if i == j else 0) for i in range(k)) for j in range(k) for s in (1, -1)]
    ords = [order_mod(r, b) for r in res]
    cand = [g for g in itertools.product(*[range(-o, o + 1) for o in ords]) if any(g) and in_lambda(res, b, g)]
    cand.sort(key=lambda g: (sum(abs(c) for c in g), g))
    G = []
    for g in cand:
        if not any(all(hi * gi >= 0 and abs(hi) <= abs(gi) for hi, gi in zip(h, g)) for h in G): G.append(g)
    return G


def _rank2(g, h):
    k = len(g)
    return any(g[i] * h[j] - g[j] * h[i] != 0 for i in range(k) for j in range(i + 1, k))


def crossing_offsets(res, b, g, h):
    """all w in Lambda with w = t g - lam h, 0<t,lam<1  (open parallelogram).  Returns list of (w, t, lam).
    iota(g,h) = 1 + len(result)  (see MATHEMATICS.md, Thm G3-T1)."""
    k = len(g)
    if not _rank2(g, h): return []
    # integer points in the bounding box of the open parallelogram with corners 0, g, -h, g-h
    lo = [min(0, g[i], -h[i], g[i] - h[i]) for i in range(k)]; hi = [max(0, g[i], -h[i], g[i] - h[i]) for i in range(k)]
    i0, j0 = next((i, j) for i in range(k) for j in range(i + 1, k) if g[i] * h[j] - g[j] * h[i] != 0)
    D = g[i0] * (-h[j0]) - g[j0] * (-h[i0])
    out = []
    for w in itertools.product(*[range(lo[i], hi[i] + 1) for i in range(k)]):
        if not any(w) or not in_lambda(res, b, w): continue
        # solve t g - lam h = w on coordinates (i0,j0)
        tn = w[i0] * (-h[j0]) - w[j0] * (-h[i0]); ln = g[i0] * w[j0] - g[j0] * w[i0]
        t, lam = Fr(tn, D), Fr(ln, D)
        if not (0 < t < 1 and 0 < lam < 1): continue
        if all(t * g[c] - lam * h[c] == w[c] for c in range(k)): out.append((w, t, lam))
    return out


def iota(res, b, g, h):
    return 1 + len(crossing_offsets(res, b, g, h)) if _rank2(g, h) else None


def crossing_free_for_all_boxes(res, b):
    G = [g for g in graver_complete(res, b)]
    pos = [g for g in G if next(c for c in g if c) > 0]
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            if _rank2(pos[i], pos[j]):
                # the pair (g,h) and (g,-h)-type orientations: offsets are defined for edge vectors with either sign
                for s in (1, -1):
                    h = tuple(s * c for c in pos[j])
                    if crossing_offsets(res, b, pos[i], h): return False, (pos[i], pos[j])
    return True, None
