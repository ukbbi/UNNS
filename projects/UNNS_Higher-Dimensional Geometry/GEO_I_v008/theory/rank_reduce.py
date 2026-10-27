"""GEO-I v008, Programme C: series-class reduction used by Theorem B-SERIES (see MINIMAL_RANK.md) with its exact verification.
reduce_box(cols)  -> (classes, reduced parity columns)
check_series_invariance(cols) -> dict comparing a box with its reduction: embeddedness, minimality, number of collisions and multiset of witness ranks."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import binary_01 as B, binary_min as BM, centre_collisions as CC, rank_reduction as RR


def reduce_box(cols):
    """parallel classes and parity-check columns of the reduced code (generator columns profile -> kernel basis)."""
    cl, gen = BM.reduced_columns(cols)
    return cl, BM.code_to_parity_columns(gen, len(gen))


def _rank_multiset(cols):
    n = len(cols); return sorted(RR.witness_rank(n, a, b)[0] for cen, a, b in CC.collisions(cols))


def check_series_invariance(cols):
    cl, red = reduce_box(cols)
    e1, e2 = B.is_embedded(cols), B.is_embedded(red)
    out = {'n': len(cols), 'classes': len(cl), 'embedded_equal': e1 == e2}
    if not e1:
        out['minimal_equal'] = B.minimal_nonembedded(cols) == B.minimal_nonembedded(red)
        r1, r2 = _rank_multiset(cols), _rank_multiset(red)
        out['collisions'] = (len(r1), len(r2)); out['rank_sets_equal'] = set(r1) == set(r2); out['min_rank'] = (min(r1), min(r2))
        out['collision_counts_equal'] = len(r1) == len(r2)
    return out
