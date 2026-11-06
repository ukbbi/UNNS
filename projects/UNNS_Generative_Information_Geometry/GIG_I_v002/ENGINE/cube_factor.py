"""GIG-I v002 -- cubical admissibility factorization (theorem GIG-T11).

A *commuting-swap cube* of the permutohedron P_k is a face (B_1|...|B_j) all of whose blocks have size <= 2.
It has d = #(blocks of size 2) coordinates; vertex coordinate c_i in {0,1} says whether pair i is in
(lower rank first)=0 or (higher rank first)=1 order.  T11:  A_C(m) restricted to the cube is  G x E_1 x ... x E_d
(G in {0,1} global, E_i subset {0,1}) -- in particular its size is 0 or a power of two.
"""
import _v1path  # noqa: F401
from itertools import product, combinations
from fractions import Fraction
from functools import lru_cache
import history_complex as hc


@lru_cache(maxsize=None)
def cube_faces(k, d=None):
    """list of cubes: (face, pair_blocks, vertex_index_by_coordinates dict{coords tuple: perm index}).
    d = required dimension (None = every dimension >= 1 )."""
    pidx = hc.perm_index(k)
    out = []
    for f in hc._ordered_partitions(k):
        if any(len(B) > 2 for B in f):
            continue
        pairs = [i for i, B in enumerate(f) if len(B) == 2]
        if not pairs or (d is not None and len(pairs) != d):
            continue
        vmap = {}
        for coords in product((0, 1), repeat=len(pairs)):
            word = ()
            for i, B in enumerate(f):
                if len(B) == 1:
                    word += B
                else:
                    c = coords[pairs.index(i)]
                    word += B if c == 0 else (B[1], B[0])
            vmap[coords] = pidx[word]
        out.append((f, tuple(pairs), vmap))
    return out


def restriction(mask, cube):
    f, pairs, vmap = cube
    return {c for c, i in vmap.items() if mask >> i & 1}


def is_box(S, d):
    """S subset of {0,1}^d equals the product of its coordinate projections (empty set counts as a box)."""
    if not S:
        return True
    proj = [{c[i] for c in S} for i in range(d)]
    n = 1
    for p in proj:
        n *= len(p)
    return len(S) == n


def check_mask(mask, k, d=None):
    """verify T11's conclusion for every commuting cube of dimension d (all if None).
    Returns (cubes checked, number of violations of 'box' or 'power of two')."""
    bad = 0
    cubes = cube_faces(k, d)
    for cube in cubes:
        S = restriction(mask, cube)
        dd = len(cube[1])
        n = len(S)
        if not is_box(S, dd) or (n and n & (n - 1)):
            bad += 1
    return len(cubes), bad


def cube_slice_counts(mask, k, d=3):
    """histogram {count: #cubes} of |A cap Q| over all d-dimensional commuting cubes."""
    h = {}
    for cube in cube_faces(k, d):
        n = len(restriction(mask, cube))
        h[n] = h.get(n, 0) + 1
    return h


# ------------------------------------------------ the arithmetic proof, executed (formal-state recursion)
def local_orientations(s, a, b):
    """E = set of orders of the adjacent pair {a,b} (a<b; 0=(a,b), 1=(b,a)) that are admissible at the
    FORMAL entry state s (a Fraction; if s is not an integer nothing is admissible)."""
    E = set()
    if s.denominator != 1:
        return E
    s = int(s)
    for o, (x, y) in ((0, (a, b)), (1, (b, a))):
        if s % x == 0:
            t = s // x * (x + 1) ** 2
            if t % y == 0:
                E.add(o)
    return E


def formal_factors(m0, face, labels):
    """Execute the proof of T11 for the cube `face` and sorted distinct content `labels`.
    The formal state before every block is  s = m0 * prod_{earlier blocks} prod R(label), independent of all
    orientation choices.  Returns (G, [E_1..E_d]) with G in {0,1}: all singleton steps locally admissible."""
    s = Fraction(m0)
    G = 1
    Es = []
    for B in face:
        if len(B) == 1:
            x = labels[B[0]]
            if s.denominator != 1 or int(s) % x:
                G = 0
            s *= Fraction((x + 1) ** 2, x)
        else:
            a, b = labels[B[0]], labels[B[1]]
            lo, hi = (a, b) if a < b else (b, a)
            # orientation 0 = lower RANK first; labels sorted so rank order == label order
            Es.append(local_orientations(s, lo, hi))
            s *= Fraction((a + 1) ** 2, a) * Fraction((b + 1) ** 2, b)
    return G, Es


def predicted_set(m0, cube, labels):
    f, pairs, vmap = cube
    G, Es = formal_factors(m0, f, labels)
    if not G:
        return set()
    return set(product(*[sorted(E) for E in Es])) if Es else {()}


@lru_cache(maxsize=None)
def cube_masks(k, dmin=2):
    """[(vertex bitmask, dimension d, cube)] for every commuting cube of dimension >= dmin."""
    return [(sum(1 << i for i in c[2].values()), len(c[1]), c) for c in cube_faces(k) if len(c[1]) >= dmin]


def fast_check(mask, k):
    """T11 verification of one arrangement set against ALL commuting cubes of dimension >= 2 (popcount for the size law,
    explicit coordinate test for the product/sub-cube law).  Returns (#cubes, #violations, histogram of 3-cube counts)."""
    bad = 0
    hist = {}
    cubes = cube_masks(k)
    for cm, d, cube in cubes:
        n = (mask & cm).bit_count()
        if n == 0:
            if d == 3:
                hist[0] = hist.get(0, 0) + 1
            continue
        if n & (n - 1):
            bad += 1
        elif n != (1 << d):
            if not is_box(restriction(mask, cube), d):
                bad += 1
        if d == 3:
            hist[n] = hist.get(n, 0) + 1
    return len(cubes), bad, hist
