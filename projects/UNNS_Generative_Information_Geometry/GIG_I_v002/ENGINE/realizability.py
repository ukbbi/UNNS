"""GIG-I v002 -- exhaustive census of arithmetically realizable arrangement sets (experiment E6) and graph data.

For every k-subset C of {1..L} (k distinct labels) ALL sets A_C(m), m >= 1 are enumerated by the per-prime level-mask
construction of threshold_closure (no source cap, no truncation); each realizable set is stored once with
 - the first content that realizes it, its minimal source L(S), whether L(S) is squarefree (T12) and whether ANY content
   with a squarefree-L realizes it,
 - the number of contents (<= L) realizing it.
"""
import _v1path  # noqa: F401
from itertools import combinations
from collections import Counter
import threshold_closure as tc
import history_complex as hc
import swap_graph as sg
import graph_iso as gi
import cell_signature as cs


def census(k, L, progress=None):
    """returns (found, coverage). found: mask -> {'content','L','sq','sqcontent','n'}."""
    found = {}
    ncont = 0
    for C in combinations(range(1, L + 1), k):
        ncont += 1
        ms = tc.realizable_masks_of_content(C)
        for mask in ms:
            ex = tc.minimal_source_exponents(C, mask)
            sqf = all(e <= 1 for e in ex.values())
            rec = found.get(mask)
            if rec is None:
                found[mask] = {"content": C, "ex": ex, "sq": sqf, "sqcontent": C if sqf else None, "n": 1}
            else:
                rec["n"] += 1
                if sqf and rec["sqcontent"] is None:
                    rec["sqcontent"] = C
                    rec["sq"] = True
        if progress:
            progress(ncont)
    cov = {"k": k, "L": L, "contents": ncont, "distinct_realizable_sets": len(found),
           "closure_cap_exclusions": 0, "source_enumeration": "all divisor patterns of the threshold lcm (per-prime levels)",
           "squarefree_realizable_sets": sum(1 for r in found.values() if r["sqcontent"] is not None)}
    return found, cov


def source_value(ex):
    v = 1
    for q, e in ex.items():
        v *= q ** e
    return v


def graph_record(mask, k):
    """graph + topology data of one realizable set (v001 engine for Betti / f; adjacency from the coloured graph)."""
    adj = cs.adjacency(mask, k)
    comps = sg.components(adj)
    return {"N": len(adj), "E": sum(map(len, adj)) // 2, "deg": tuple(sorted(map(len, adj))),
            "sizes": tuple(sorted(len(c) for c in comps)), "betti": hc.betti(mask, k), "f": hc.f_vector(mask, k),
            "wl": hash(gi.wl_hash(adj)), "adj": adj}


def iso_classes(found, k, progress=None):
    """exact isomorphism classes of the uncoloured swap graphs of all realizable sets.
    Returns (classes, stats): classes = list of lists of masks (each list = one exact iso class, first = representative);
    stats = counts of cheap-invariant groups and exact comparisons performed."""
    recs = {}
    groups = {}
    for i, mask in enumerate(found):
        r = graph_record(mask, k)
        recs[mask] = r
        groups.setdefault((r["N"], r["E"], r["deg"], r["sizes"], r["wl"]), []).append(mask)
        if progress:
            progress(i)
    classes = []
    exact = 0
    for key, ms in groups.items():
        reps = []   # list of lists
        for mask in ms:
            placed = False
            for cl in reps:
                exact += 1
                if gi.find_isomorphism(recs[cl[0]]["adj"], recs[mask]["adj"]) is not None:
                    cl.append(mask)
                    placed = True
                    break
            if not placed:
                reps.append([mask])
        classes.extend(reps)
    return classes, recs, {"invariant_groups": len(groups), "exact_comparisons": exact, "iso_classes": len(classes)}
