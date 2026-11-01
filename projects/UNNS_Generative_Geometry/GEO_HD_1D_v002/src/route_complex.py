"""HD-1D v001: swap graph / route complex of histories.  A history is a pair (m0, labels)."""
from collections import defaultdict
from itertools import product
from select_history import is_admissible, run, endpoint, T, complete_histories


def content(h):
    return tuple(sorted(h[1]))


def legal_swap_positions(h):
    """positions i with labels[i] != labels[i+1] such that exchanging them gives an admissible history"""
    m0, L = h
    out = []
    for i in range(len(L) - 1):
        if L[i] != L[i + 1] and is_admissible(m0, L[:i] + (L[i + 1], L[i]) + L[i + 2:]):
            out.append(i)
    return out


def do_swap(h, i):
    m0, L = h
    return (m0, L[:i] + (L[i + 1], L[i]) + L[i + 2:])


def swap_classes(hist_list):
    """connected components of the swap graph on the given list of histories (all must be in the list)"""
    idx = {h: i for i, h in enumerate(hist_list)}
    par = list(range(len(hist_list)))
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for h in hist_list:
        for i in legal_swap_positions(h):
            h2 = do_swap(h, i)
            par[f(idx[h])] = f(idx[h2])
    cl = defaultdict(list)
    for h in hist_list: cl[f(idx[h])].append(h)
    return list(cl.values())


def greedy_disjoint_swaps(h):
    """a maximum set of pairwise non-overlapping legal swap positions (greedy is optimal on a path)"""
    legal = set(legal_swap_positions(h)); out = []; i = 0
    L = h[1]
    while i < len(L) - 1:
        if i in legal: out.append(i); i += 2
        else: i += 1
    return out


def cube_histories(h, positions):
    """the 2^d histories obtained by independently swapping or not swapping at the given (non-overlapping) positions"""
    assert all(b - a >= 2 for a, b in zip(positions, positions[1:]))
    out = []
    for bits in product((0, 1), repeat=len(positions)):
        g = h
        for b, i in zip(bits, positions):
            if b: g = do_swap(g, i)
        out.append((bits, g))
    return out


def verify_cube(h, positions):
    """exact check: all 2^d vertices admissible, same endpoint, pairwise distinct, and every cube edge is one legal swap"""
    vs = cube_histories(h, positions)
    end = endpoint(*h)
    ok = all(is_admissible(*g) and endpoint(*g) == end for _, g in vs)
    ok = ok and len({g for _, g in vs}) == len(vs)
    d = {bits: g for bits, g in vs}
    for bits, g in vs:
        for j, i in enumerate(positions):
            if bits[j] == 0:
                b2 = bits[:j] + (1,) + bits[j + 1:]
                ok = ok and do_swap(g, i) == d[b2]
    return ok


def binomial_family(r):
    """the C(2r,r) histories 1^r followed by every arrangement of r labels 1 and r labels 2 (from source 1)"""
    from itertools import combinations
    out = []
    for twos in combinations(range(2 * r), r):
        tail = [1] * (2 * r)
        for i in twos: tail[i] = 2
        out.append((1, (1,) * r + tuple(tail)))
    return out


def route_cube_family(r):
    """the 2^r histories: prefix 1^r, then r blocks each chosen 12 or 21 (spec section 7.2); returns base history and swap positions"""
    base = (1, (1,) * r + (1, 2) * r)
    return base, [r + 2 * j for j in range(r)]


def cube_dim(h):
    return len(greedy_disjoint_swaps(h))
