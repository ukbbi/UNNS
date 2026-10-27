"""GEO-III.C  homology of: K_abs (v002 cells), the coordinate complex, the clique complex, and the geometric image U_x (nerve)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'geometry')); sys.path.insert(0, HERE)
from realization import *
from chain_complex import betti, simplex_bd
from geo2lib import boundary as cube_bd
import intersections as X


def betti_abs(cells, field='Q'):
    return betti(cells, cube_bd, field)


class NerveBudget(Exception): pass


def nerve(cover, maxdim=3, max_simplices=200000, max_lp=None):
    """Nerve of a closed convex cover (each member a parallelotope).  Returns (cells_by_dim, truncated, resource_limited)."""
    r = len(cover); lp0 = X.LP_CALLS[0]
    if r == 0: return [[]], False, False
    dim0 = [(i,) for i in range(r)]
    adj = [set() for _ in range(r)]
    for i in range(r):
        for j in range(i + 1, r):
            if max_lp is not None and X.LP_CALLS[0] - lp0 > max_lp: return [dim0], True, True
            if X.nonempty_common([cover[i], cover[j]]): adj[i].add(j); adj[j].add(i)
    levels = [dim0, [(i, j) for i in range(r) for j in sorted(adj[i]) if j > i]]
    total = r + len(levels[1])
    truncated = False
    d = 1
    while levels[-1] and d < maxdim:
        nxt = []
        for s in levels[-1]:
            common = set.intersection(*[adj[v] for v in s])
            for w in sorted(common):
                if max_lp is not None and X.LP_CALLS[0] - lp0 > max_lp: return levels, True, True
                if w > s[-1] and X.nonempty_common([cover[v] for v in s] + [cover[w]]): nxt.append(s + (w,))
        total += len(nxt)
        if total > max_simplices: return levels, True, True
        levels.append(nxt); d += 1
    # completeness: the complex is complete if no simplex of dimension maxdim+1 exists
    complete = True
    if levels and levels[-1] and len(levels) == maxdim + 1:
        for s in levels[-1]:
            common = set.intersection(*[adj[v] for v in s])
            if any(w > s[-1] and X.nonempty_common([cover[v] for v in s] + [cover[w]]) for w in common): complete = False; break
    while len(levels) > 1 and not levels[-1]: levels.pop()
    return levels, (not complete), False


def betti_nerve(cover, maxdim=3, field='Q', max_lp=None):
    lv, trunc, lim = nerve(cover, maxdim, max_lp=max_lp)
    if lim: return None, {'resource_limited': True}
    # when truncated we only trust Betti numbers in degree < maxdim
    b, d2, eul = betti(lv, simplex_bd, field)
    trust = len(b) - 1 if trunc else len(b)
    return b[:trust] if trunc else b, {'cells': [len(c) for c in lv], 'truncated': trunc, 'd2_ok': d2, 'euler_ok': (eul if not trunc else None), 'trusted_degrees': trust}


def betti_clique(F, G, maxdim=3, field='Q'):
    cells = flag_cells(F, set(G), maxdim)
    trunc = len(cells) > maxdim
    b, d2, eul = betti(cells, simplex_bd, field)
    return (b[:-1] if trunc else b), {'cells': [len(c) for c in cells], 'truncated': trunc, 'd2_ok': d2}
