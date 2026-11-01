"""HD-1D v003 builder: swap-class theory (D-Q1).  Feeding digraph, SCC block factorisation (Lemma NF, F1, F2) and the hub-descent criterion.

Feeding relation on labels: A feeds B  iff  gcd(A+1, B) > 1  (A != B).
Lemma NF : if x does not feed y and (x,y) is admissible from s, then (y,x) is admissible from s.
F1       : acyclic feeding => at most one swap class at every source; K(tau) | K(w) for all w, tau any linear extension.
F2       : swap classes factor over SCC blocks of the feeding digraph (blocks in a topological order, entry states chained).
Hub      : an arrangement h with K(h) | K(w) for all w and divisibility-descending swap paths from every w to h forces connectivity at every source.
"""
from math import gcd
from fractions import Fraction
from thresholds import threshold_table, classes_at, neighbours


def feeds(a, b):
    return a != b and gcd(a + 1, b) > 1


def scc_blocks(labels):
    """SCCs of the feeding digraph on the DISTINCT labels, returned in a topological order of the condensation (feeders first)."""
    L = sorted(set(labels)); R = {a: {b for b in L if feeds(a, b)} for a in L}
    ch = True
    while ch:
        ch = False
        for a in L:
            for b in list(R[a]):
                n = R[b] - R[a]
                if n: R[a] |= n; ch = True
    comp = {a: frozenset([a] + [b for b in L if b != a and b in R[a] and a in R[b]]) for a in L}
    blocks = sorted(set(comp.values()), key=lambda s: min(s))
    # Kahn order on the condensation
    pred = {B: {C for C in blocks if C != B and any(feeds(x, y) for x in C for y in B)} for B in blocks}
    order = []; done = set()
    while len(order) < len(blocks):
        for B in blocks:
            if B not in done and pred[B] <= done:
                order.append(B); done.add(B); break
    return order


def is_acyclic(labels):
    return all(len(B) == 1 for B in scc_blocks(labels))


def strongly_connected(labels):
    return len(scc_blocks(labels)) == 1


def block_product_classes(content, m):
    """number of swap classes of `content` at source m computed from the F2 product formula (0 if some block inadmissible)"""
    total = 1; cur = Fraction(m)
    for B in scc_blocks(content):
        sub = tuple(sorted(x for x in content if x in B))
        if cur.denominator != 1: return 0
        c = len(classes_at(threshold_table(sub), int(cur)))
        if c == 0: return 0
        total *= c
        for N in sub: cur = cur / N * (N + 1) ** 2
    return total


def direct_classes(content, m):
    return len(classes_at(threshold_table(content), m))


def has_hub(content):
    thr = threshold_table(content); V = list(thr)
    for h in V:
        if any(thr[w] % thr[h] for w in V): continue
        # reverse BFS from h along edges v->u where thr[u] | thr[v] ... build: w reaches h if exists nbr u with thr[u] | thr[w] and u reaches h
        reach = {h}; ch = True
        while ch:
            ch = False
            for w in V:
                if w in reach: continue
                if any(u in reach and thr[w] % thr[u] == 0 for u in neighbours(w)):
                    reach.add(w); ch = True
        if len(reach) == len(V): return True
    return False


# ------------------------------------------------------------------ prefix-set form and the exact 3-label criterion
from thresholds import _delta_table
from math import lcm
from itertools import permutations as _perm


def kappa(S, content=None):
    """threshold of a SET (multiset) of labels: kappa(S) = prod_p p^{max(0, -sum_{x in S} Delta_p(x))}  (feasible from m iff kappa(S) | m)"""
    tab = _delta_table(list(S)); primes = set()
    for x in S: primes |= set(tab[x])
    k = 1
    for p in primes:
        s = sum(tab[x].get(p, 0) for x in S)
        if s < 0: k *= p ** (-s)
    return k


def K_prefix(w):
    """K(w) = lcm_j kappa({N_1..N_j})   (prefix-set form of the threshold law)"""
    out = 1
    for j in range(1, len(w) + 1): out = lcm(out, kappa(w[:j]))
    return out


def three_label_splits(content):
    """exact 3-label criterion: [(a,b,c,L)] over labelings with b in the middle; the content has a split source iff the list is non-empty.
    L = lcm(kappa{a}, kappa{c}, kappa{a,b}, kappa{b,c}, kappa{a,b,c}); the split sources of that labeling are the multiples m of L with b not| m and kappa{a,c} not| m."""
    out = []
    for a, b, c in _perm(sorted(content)):
        if a > c: continue
        L = lcm(kappa((a,)), kappa((c,)), kappa((a, b)), kappa((b, c)), kappa((a, b, c)))
        if L % kappa((b,)) and L % kappa((a, c)): out.append((a, b, c, L))
    return out
