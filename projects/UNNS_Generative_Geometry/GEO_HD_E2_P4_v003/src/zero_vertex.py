"""Zero-vertex screen (E2-P4 v002, theorem P4-Z1).  Standard library + pinned engine cell lists.

Setting: Lambda <= Lambda' lattices of Z^k, box Q, C = P(u; g_1..g_j) a cell of K_abs(Lambda, Q) (u != 0, all corners nonzero).
A *zero-vertex decomposition* of C is a choice of vectors s_i in Lambda' with s_i conformally below g_i (s_i = 0 allowed, s_i = g_i allowed)
and u + s_1 + ... + s_j = 0.
Theorem P4-Z1: if C has NO zero-vertex decomposition then C is contained in U(Lambda', Q).  (Necessary condition for any containment failure.)
For j = 1 a zero-vertex decomposition never exists (Graver minimality), so edges never obstruct, in every dimension.
The screen reads only (u, g_i) and a membership oracle for Lambda' -- it never builds the target complex."""
from itertools import product


def conformal_below(g):
    """All integer vectors s with s_c = 0 or (same sign as g_c and |s_c| <= |g_c|); includes 0 and g."""
    ranges = []
    for x in g:
        ranges.append(range(0, x + 1) if x >= 0 else range(x, 1))
    return [s for s in product(*ranges)]


def zero_vertex_decomposition(u, gens, inLp):
    """Return a list [s_1..s_j] with u + sum s_i = 0, each s_i in Lambda' conformally below g_i, or None."""
    cand = [[s for s in conformal_below(g) if inLp(s)] for g in gens]
    k = len(u)
    need = tuple(-x for x in u)
    # depth-first with the last generator solved directly (j <= 3 in practice)
    def rec(i, acc, chosen):
        if i == len(gens) - 1:
            last = tuple(n - a for n, a in zip(need, acc))
            if last in cand_sets[i]:
                return chosen + [last]
            return None
        for s in cand[i]:
            r = rec(i + 1, tuple(a + b for a, b in zip(acc, s)), chosen + [s])
            if r is not None:
                return r
        return None
    cand_sets = [set(c) for c in cand]
    if not gens:
        return None if any(u) else []
    return rec(0, (0,) * k, [])


def screen_cells(maximal_cells, inLp):
    """maximal_cells: list of (base, gens).  Returns (n_cells, list of cells that HAVE a zero-vertex decomposition with the decomposition)."""
    flagged = []
    for base, gens in maximal_cells:
        if len(gens) == 0:
            continue
        d = zero_vertex_decomposition(base, gens, inLp)
        if d is not None:
            flagged.append({"base": list(base), "gens": [list(g) for g in gens], "decomposition": [list(s) for s in d]})
    return len(maximal_cells), flagged
