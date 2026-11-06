"""GIG-I v003 -- feasible-family law and ordered-block admissibility factorization (GIG-T16).

Feasible-family law (Lemma F).  For a multiset I of labels put R(I)=prod_{N in I} R(N), R(N)=(N+1)^2/N.  A word w is admissible
from the integer source m  iff  m*R(I) is an integer for EVERY prefix multiset I of w  (because, for an integer state x,
N | x  <=>  x*R(N) is an integer, as gcd(N,N+1)=1).  Hence admissibility depends on the word only through its prefix SETS
and  D(I) := denominator of R(I) (lowest terms) is the threshold of the set I:  m*R(I) in Z  <=>  D(I) | m,
 K(w) = lcm_j D(prefix_j(w)).
"""
import _v2path  # noqa: F401
from fractions import Fraction
from itertools import permutations
from math import lcm
import history_complex as hc
import threshold_closure as tc


def R(N):
    return Fraction((N + 1) ** 2, N)


def subset_ratio(labels, mask):
    """R(I) for the subset I of `labels` selected by the bitmask (bit j = label j)."""
    r = Fraction(1)
    for j, N in enumerate(labels):
        if mask >> j & 1:
            r *= R(N)
    return r


def denominators(labels):
    """{subset bitmask I : D(I)} for all 2^k subsets (D(empty)=1)."""
    return {I: subset_ratio(labels, I).denominator for I in range(1 << len(labels))}


def feasible_family(labels, m, D=None):
    D = D or denominators(labels)
    return {I for I, d in D.items() if m % d == 0}


def prefix_sets(p):
    """bitmask prefix sets (nonempty) of the arrangement p (p[i] = rank of the label at position i)."""
    out, cur = [], 0
    for r in p:
        cur |= 1 << r
        out.append(cur)
    return out


def threshold_via_D(labels, p, D=None):
    D = D or denominators(labels)
    return lcm(*[D[I] for I in prefix_sets(p)])


def admissible_mask_via_chains(labels, m):
    """A_C(m) as the set of maximal chains of the feasible family (Lemma F) -- no simulation, no threshold exponents."""
    D = denominators(labels)
    F = feasible_family(labels, m, D)
    mask = 0
    for i, p in enumerate(hc.perms(len(labels))):
        if all(I in F for I in prefix_sets(p)):
            mask |= 1 << i
    return mask


# ---------------------------------------------------------------- T16: ordered-block factorization
def block_factorization(labels, m, face):
    """face = ordered set partition (B_1|...|B_r) of the label ranks (tuple of tuples).  Returns
    (G, [E_1..E_r]) where E_i is the set of orderings of block B_i (tuples of ranks) that are admissible from the FORMAL
    entry state s_i = m*R(B_1 u .. u B_{i-1}); the formal state does not depend on any ordering choice.
    The vertex set of `face` intersected with A_C(m) is exactly  E_1 x ... x E_r  (concatenation of orderings)."""
    s = Fraction(m)
    Es = []
    for B in face:
        E = set()
        if s.denominator == 1:
            for pi in permutations(B):
                x = s
                ok = True
                for r in pi:
                    x = x * R(labels[r])
                    if x.denominator != 1:
                        ok = False
                        break
                if ok:
                    E.add(pi)
        Es.append(E)
        for r in B:
            s = s * R(labels[r])
    return Es


def predicted_vertices(labels, m, face):
    """arrangements in face cap A_C(m) predicted by the product formula, as a set of rank tuples."""
    Es = block_factorization(labels, m, face)
    res = [()]
    for E in Es:
        res = [a + b for a in res for b in E]
    return set(res)


def actual_vertices(mask, face, k):
    P = hc.perm_index(k)
    return {v for v in hc._face_vertices(face) if mask >> P[v] & 1}
