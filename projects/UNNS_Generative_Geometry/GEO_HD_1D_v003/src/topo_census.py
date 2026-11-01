"""HD-1D v003: topology census over contents of distinct labels. Returns pattern table {frozenset(A as rank-perms): (betti, chi, cubical betti)}."""
import itertools, sys, time, json
from collections import Counter
from thresholds import threshold_table, lcm_closure
from route_topology import betti, nerve_components


def patterns(content):
    """yield the distinct admissible-set patterns (as frozensets of rank permutations) over all lcm-closure sources, with a representative source"""
    srt = sorted(content); rank = {x: i for i, x in enumerate(srt)}
    thr = threshold_table(content)
    cl = lcm_closure(set(thr.values()), cap=400000)
    seen = {}
    for m in cl:
        A = frozenset(tuple(rank[x] for x in w) for w, k in thr.items() if m % k == 0)
        if A not in seen: seen[A] = m
    return seen


def census(k, rng, cache=None, report=None):
    cache = {} if cache is None else cache
    ncont = nsrc = 0; hist = Counter(); examples = {}
    for c in itertools.combinations(range(1, rng + 1), k):
        try: pats = patterns(c)
        except OverflowError: continue
        ncont += 1
        for A, m in pats.items():
            nsrc += 1
            if A not in cache:
                b, chi = betti(A, k)
                cache[A] = (b, chi)
            b, chi = cache[A]
            key = tuple(b)
            hist[key] += 1
            if key not in examples and any(x > 0 for x in key[1:]): examples[key] = (c, m, len(A))
    return cache, hist, examples, ncont, nsrc
