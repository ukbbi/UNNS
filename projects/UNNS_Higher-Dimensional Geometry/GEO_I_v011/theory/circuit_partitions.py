"""GEO-I v011, Programme B.  Circuit partitions of the all-ones word of a minimal non-embedded binary box (exact integer arithmetic).

MODEL (G10-A1, inherited, PROVED).  A minimal box is X subset of AG(k-1,2) = {x in F_2^k : top bit set}, |X| = p, X spanning.  The code is
C = { w_f = (<f,x>)_{x in X} : f in F_2^k }, dim k, all-ones word 1 = w_f for f = top bit.  A circuit is the support of a nonzero word of
minimal support; for f != 0 the support of w_f is a circuit iff X cap f^perp has rank k-1 (so the zero set spans the hyperplane).

NEW in v011 (G11-L5, G11-L6, G11-T3):
  * vector_space_partition(...) : the partitions of 1 give a vector-space partition of C/<1> = F_2^(k-1) (V_P = span of the blocks);
  * parseval_cost, counting_identity, parseval_identity : the two exact identities  sum_P (2^m-2) = 2^k-2  and  sum_P (2^m S_P - 2p^2) = p(2^k-2p);
  * w2_threshold_ok(p) : the exact inequality p(2^m/m-2) >= 2^m-2 for 3 <= m <= p/2 (valid iff p >= 9 for m=3);
  * two_block_certificate(X,k) : a PARTITION certificate (two distinct two-block partitions).
"""
from fractions import Fraction as Fr


def par(x): return bin(x).count('1') & 1


def rank(vs):
    basis = []
    for v in vs:
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    return len(basis)


def support(X, f):
    """bitmask over the index set of X of the word w_f"""
    return sum(1 << i for i, x in enumerate(X) if par(f & x))


def is_circuit_functional(X, k, f):
    """support of w_f (f != 0) is a circuit  iff  X cap f^perp has rank k-1 (and the word is nonzero)"""
    if f == 0: return False
    s = support(X, f)
    if s == 0: return False
    return rank([x for x in X if not par(f & x)]) == k - 1


def circuits(X, k):
    """dict functional -> support mask of every circuit, f in 1..2^k-1 (the circuit of w_f; w_f and w_g may coincide only if f=g since X spans)"""
    return {f: support(X, f) for f in range(1, 1 << k) if is_circuit_functional(X, k, f)}


def partitions(circ, n):
    """all partitions of {0..n-1} into circuits, as frozensets of functionals (deterministic, lowest uncovered element first)"""
    full = (1 << n) - 1
    byLow = {}
    for f, m in sorted(circ.items(), key=lambda kv: (kv[1], kv[0])): byLow.setdefault((m & -m).bit_length() - 1, []).append((f, m))
    out = []

    def rec(cov, chosen):
        if cov == full: out.append(frozenset(chosen)); return
        rem = full & ~cov; low = (rem & -rem).bit_length() - 1
        for f, m in byLow.get(low, []):
            if m & cov == 0: rec(cov | m, chosen + [f])
    rec(0, [])
    return out


def two_block_partitions(circ, n):
    full = (1 << n) - 1; seen = set(); out = []
    for f, m in circ.items():
        g = [h for h, mm in circ.items() if mm == full ^ m]
        if g:
            key = frozenset((f, g[0]))
            if key not in seen: seen.add(key); out.append(tuple(sorted((f, g[0]))))
    return out


def count_partitions_all_subsets(circ, n):
    """cnt[mask] = number of partitions of mask into circuits (E1: the box is non-embedded iff some cnt >= 2)"""
    byLow = {}
    for f, m in circ.items(): byLow.setdefault((m & -m).bit_length() - 1, []).append(m)
    cnt = [0] * (1 << n); cnt[0] = 1
    for mask in range(1, 1 << n):
        low = (mask & -mask).bit_length() - 1; tot = 0
        for m in byLow.get(low, []):
            if m & mask == m: tot += cnt[mask ^ m]
        cnt[mask] = tot
    return cnt


def non_embedded_E1(circ, n):
    return any(c >= 2 for c in count_partitions_all_subsets(circ, n))


def is_minimal_E1(X, k):
    """non-embedded (G10-E1) and every single deletion (shortening: drop the circuits through i) embedded.  Feasible for n <= ~18."""
    n = len(X); circ = circuits(X, k)
    if not non_embedded_E1(circ, n): return False
    for i in range(n):
        sub = {f: m for f, m in circ.items() if not (m >> i) & 1}
        # relabel not needed for the count: masks simply never contain bit i
        cnt = count_partitions_all_subsets(sub, n)
        if any(c >= 2 for c in cnt): return False
    return True


# ------------------------------------------------------------------------------------------------ identities
def block_sizes(circ, part): return [bin(circ[f]).count('1') for f in part]


def counting_identity(parts, k):
    """sum_P (2^{m_P}-2) = 2^k - 2   (every word other than 0, 1 lies in exactly one V_P, G10-R)"""
    return sum((1 << len(P)) - 2 for P in parts) == (1 << k) - 2


def parseval_cost(circ, P, p):
    ds = block_sizes(circ, P); m = len(ds); S = sum(d * d for d in ds)
    return (1 << m) * S - 2 * p * p


def parseval_identity(circ, parts, p, k):
    """sum_P (2^m S_P - 2p^2) = p(2^k - 2p)"""
    return sum(parseval_cost(circ, P, p) for P in parts) == p * ((1 << k) - 2 * p)


def parseval_direct(X, k):
    """sum_f (sum_x (-1)^<f,x>)^2 = 2^k p   (independent computation of the same quantity, Parseval on F_2^k)"""
    tot = 0
    for f in range(1 << k):
        s = sum(-1 if par(f & x) else 1 for x in X); tot += s * s
    return tot == (1 << k) * len(X)


def weight_second_moment(X, k):
    """sum over the code of |w|^2 = 2^(k-2) p (p+1)   when X consists of p distinct points of AG(k-1,2)"""
    p = len(X); return sum(bin(support(X, f)).count('1') ** 2 for f in range(1 << k)) == (1 << (k - 2)) * p * (p + 1)


def vector_space_partition(circ, parts, X, k):
    """V_P = span of the block indicator words (dim m_P, contains 1).  Returns True iff the V_P are pairwise meeting exactly in {0,1}
    and cover the code (sizes 2^m_P sum correctly) -- i.e. {V_P/<1>} is a vector-space partition of F_2^(k-1)."""
    seen = {}
    for idx, P in enumerate(parts):
        fs = sorted(P)
        words = {0}
        for f in fs: words |= {w ^ f for w in words}      # span of the functionals of the blocks (functional of a block indicator)
        # the functionals of the blocks sum to the functional of 1 (top bit): consistent iff xor == top
        top = 1 << (k - 1)
        x = 0
        for f in fs: x ^= f
        if x != top: return False
        for w in words:
            if w in (0, top): continue
            if w in seen: return False
            seen[w] = idx
    return len(seen) == (1 << k) - 2


# ------------------------------------------------------------------------------------------------ the W2 inequality
def w2_threshold_ok(p, mmax=None):
    """exact check of  p*(2^m/m - 2) >= 2^m - 2  for every 3 <= m <= p/2 (rational arithmetic).  True for every p >= 9, false for p = 6,7,8 at m = 3."""
    mmax = p // 2 if mmax is None else mmax
    return all(Fr(p) * (Fr(1 << m, m) - 2) >= (1 << m) - 2 for m in range(3, mmax + 1))


def w2_threshold_all(pmax=400):
    return {p: w2_threshold_ok(p) for p in range(6, pmax + 1)}


def w2_lower_bound(p):
    """the bound proved in G11-L6: for a minimal non-embedded box with p >= 9 points, n_2 >= p-1"""
    return p - 1 if p >= 9 else None


# ------------------------------------------------------------------------------------------------ certificates
def two_block_certificate(X, k, label=''):
    circ = circuits(X, k); n = len(X); tb = two_block_partitions(circ, n)
    return {'type': 'PARTITION', 'label': label, 'k': k, 'points': list(X), 'two_blocks': [list(t) for t in tb[:3]], 'n_two_blocks': len(tb)}
