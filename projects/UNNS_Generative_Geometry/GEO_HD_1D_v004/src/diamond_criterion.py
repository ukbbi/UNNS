"""HD-1D v001: exact two-label interchange (arithmetic diamond) criterion and its generalisations.

Theorem D-T1.   Let A, B >= 1, m >= 1.
 (a) The route m -A-> -B-> exists  iff  m_{A->B} | m,  where  m_{A->B} = A*B / gcd(B, (A+1)^2).
 (b) Both routes (AB and BA) exist  iff  A*B | m.      [lcm(m_{A->B}, m_{B->A}) = A*B]
 (c) All arrangements of the multiset {N_1,..,N_k} are admissible from m  iff  N_1*...*N_k | m.
"""
from math import gcd
from select_history import T, is_admissible, factor, vp


def m_ordered(A, B):
    """smallest state admitting the ordered route A then B; the admitting states are exactly its multiples"""
    return A * B // gcd(B, (A + 1) ** 2)


def ordered_ok_direct(m, A, B):
    return m % A == 0 and T(A, m) % B == 0


def ordered_ok(m, A, B):
    return m % m_ordered(A, B) == 0


def diamond_direct(m, A, B):
    return ordered_ok_direct(m, A, B) and ordered_ok_direct(m, B, A)


def diamond(m, A, B):
    return m % (A * B) == 0


def padic_form(m, A, B):
    """the p-adic form of D-T1 as stated in the HD-1D specification (section 5.2)"""
    primes = {p for n in (m, A, B, A + 1, B + 1) for p, _ in factor(n)}
    for p in primes:
        u, a, b = vp(m, p), vp(A, p), vp(B, p)
        if not (u >= a and u >= b and u + 2 * vp(A + 1, p) - a >= b and u + 2 * vp(B + 1, p) - b >= a):
            return False
    return True


def classify(m, A, B):
    """exact classification of the pair (A,B) at state m (A != B)"""
    ab, ba = ordered_ok(m, A, B), ordered_ok(m, B, A)
    if ab and ba: return "DIAMOND"
    if ab: return "ONLY_AB"
    if ba: return "ONLY_BA"
    if m % A == 0 and m % B == 0: return "BOTH_LABELS_ADMISSIBLE_NEITHER_ORDER"
    if m % A == 0 or m % B == 0: return "ONE_LABEL_ONLY"
    return "NEITHER_LABEL"


def all_arrangements_ok(m, labels):
    """criterion (c): product divisibility"""
    p = 1
    for n in labels: p *= n
    return m % p == 0


def all_arrangements_direct(m, labels):
    from itertools import permutations
    return all(is_admissible(m, p) for p in set(permutations(labels)))


def cube_vertices(m, labels):
    """the 2^k states reached by executing a subset of the (distinct) labels, order irrelevant"""
    out = {}
    k = len(labels)
    for mask in range(1 << k):
        x = m; num = 1; den = 1
        for i in range(k):
            if mask >> i & 1:
                num *= (labels[i] + 1) ** 2; den *= labels[i]
        out[mask] = m * num // den if (m * num) % den == 0 else None
    return out
