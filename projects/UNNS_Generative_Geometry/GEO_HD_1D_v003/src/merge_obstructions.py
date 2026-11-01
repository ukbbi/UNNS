"""HD-1D v001: obstructions - hexagon failures, same-content swap-class splits, bounded common futures."""
from itertools import permutations
from select_history import complete_histories, run, successors, is_admissible, T, admissible_labels
from route_complex import swap_classes, content


def split_contents(t):
    """(source, content) groups of complete histories of t whose swap graph has several components"""
    hs = list(complete_histories(t)); cl = swap_classes(hs)
    grp = {}
    for c in cl:
        grp.setdefault((c[0][0], content(c[0])), []).append(c)
    return {k: v for k, v in grp.items() if len(v) > 1}


def hexagon_failures(m, labels):
    """for a history (m; a,b,c) with distinct labels where both adjacent swaps are legal: the arrangements actually admissible"""
    a, b, c = labels
    if not (is_admissible(m, labels) and is_admissible(m, (b, a, c)) and is_admissible(m, (a, c, b))):
        return None
    ok = [p for p in permutations(labels) if is_admissible(m, p)]
    return ok


def reach_plus(a, bound):
    """all states reachable from a by >= 1 step, not exceeding bound (BOUNDED enumeration, not a universal statement)"""
    seen = set(); stack = [a]
    while stack:
        m = stack.pop()
        for N, t in successors(m):
            if t <= bound and t not in seen:
                seen.add(t); stack.append(t)
    return seen
