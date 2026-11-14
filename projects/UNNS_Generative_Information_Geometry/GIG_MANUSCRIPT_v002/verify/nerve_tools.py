"""Stdlib-only nerve and strong-collapse helpers (same code as in figures/make_figures.py)."""
import itertools, sys
from gigmini import *
def dead_sets(k, A):
    byI = {}
    for p in permutations(range(k)):
        for I in prefix_sets(p): byI.setdefault(I, []).append(p)
    return sorted(I for I, L in byI.items() if all(p not in A for p in L))
def comparable(a, b): return (a & b) == a or (a & b) == b
def nerve_facets(k, D):
    full = (1 << k) - 1; fac = set()
    for z in range(1, full):
        Cz = frozenset(d for d in D if comparable(d, z))
        if Cz: fac.add(Cz)
    # keep only maximal
    fac = [f for f in fac if not any(f < g for g in fac)]
    return fac
def simplices_upto2(fac):
    S = set()
    for f in fac:
        f = sorted(f)
        for r in range(1, min(3, len(f)) + 1):
            for s in itertools.combinations(f, r): S.add(s)
    return S
def lab_of(I, lab):
    return "{" + ",".join(str(lab[r]) for r in range(len(lab)) if I >> r & 1) + "}"
def strong_collapse(fac):
    fac = [frozenset(f) for f in fac]
    changed = True
    while changed:
        changed = False
        V = sorted(set().union(*fac)) if fac else []
        for v in V:
            st = [f for f in fac if v in f]
            for w in V:
                if w != v and all(w in f for f in st):
                    fac = [f - {v} if v in f else f for f in fac]
                    fac = [f for f in fac if f]
                    fac = [f for f in fac if not any(f < g for g in fac)]
                    changed = True; break
            if changed: break
    return fac
