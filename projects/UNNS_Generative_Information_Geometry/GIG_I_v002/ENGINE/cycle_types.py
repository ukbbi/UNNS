"""GIG-I v002 -- classification of the 6-cycles of the permutohedron graph P_k (experiment E5).

Vertices = permutations (arrangements); edge colour j (1..k-1) = swap of positions j, j+1.  Every 6-cycle is a closed
reduced walk g_1..g_6 from the identity.  Types (all computed, none assumed):
  braid-hexagon : colours {i,i+1}, the 2-face of type (3-block);
  cube-*        : three pairwise commuting colours (|i-j|>=2): lies in a commuting cube Q_3;
                  'petrie' = chordless 6-cycle (cube minus two antipodal vertices), 'domino' = boundary of two adjacent squares;
  mixed-domino  : colours {i,i+1,j} j commuting with both -- two squares sharing an edge;
  other         : anything else.
"""
import _v1path  # noqa: F401
from collections import Counter
import history_complex as hc


def _swap(p, j):  # j in 0..k-2 : swap positions j, j+1
    return p[:j] + (p[j + 1], p[j]) + p[j + 2:]


def six_cycles_through_identity(k):
    """all simple 6-cycles through the identity as tuples of generator indices (0-based), each cycle listed once per
    (start orientation) -- i.e. 12 times; deduplicated to canonical cyclic/reflection class by the caller."""
    idt = tuple(range(k))
    out = []

    def rec(p, path, seq):
        if len(seq) == 6:
            return
        for j in range(k - 1):
            if seq and seq[-1] == j:
                continue
            q = _swap(p, j)
            if len(seq) == 5:
                if q == idt:
                    out.append(tuple(seq + [j]))
                continue
            if q in path:
                continue
            rec(q, path | {q}, seq + [j])
    rec(idt, {idt}, [])
    return out


def _canon(seq):
    n = len(seq)
    forms = []
    for s in (seq, seq[::-1]):
        for r in range(n):
            forms.append(s[r:] + s[:r])
    return min(forms)


def cycle_classes(k):
    """canonical generator words of the 6-cycle classes under left translation (= relabelling), with counts."""
    c = Counter(_canon(s) for s in six_cycles_through_identity(k))
    return sorted(c)


def cycle_vertices(word, k, start=None):
    p = tuple(range(k)) if start is None else start
    vs = [p]
    for j in word[:-1]:
        p = _swap(p, j)
        vs.append(p)
    return vs


def induced_edges(vs):
    S = set(vs)
    k = len(vs[0])
    e = 0
    for p in vs:
        for j in range(k - 1):
            if _swap(p, j) in S:
                e += 1
    return e // 2


def classify(word):
    """(type name, colour set) from the generator word alone plus structure of its induced graph at the identity."""
    J = sorted(set(word))
    k = max(J) + 2
    vs = cycle_vertices(word, k)
    ie = induced_edges(vs)
    comm = all(abs(a - b) >= 2 for a in J for b in J if a < b)
    if len(J) == 2 and J[1] - J[0] == 1:
        t = "braid-hexagon"
    elif len(J) == 3 and comm:
        t = "cube-petrie" if ie == 6 else "cube-domino"
    elif len(J) == 3 and sum(1 for a in J for b in J if a < b and b - a == 1) == 1:
        t = "mixed-domino"
    else:
        t = "other"
    return t, tuple(j + 1 for j in J), ie


def all_cycles(k):
    """every 6-cycle of P_k as (vertex tuple sorted by index, type); each cycle once."""
    pidx = hc.perm_index(k)
    seen = {}
    for p in hc.perms(k):
        for w in cycle_classes(k):
            t = classify(w)[0]
            vs = cycle_vertices(w, k, start=p)
            key = frozenset(pidx[v] for v in vs)
            # a vertex set may carry two different cycles (rare); keep by (set, type)
            seen[(key, t)] = vs
    return seen
