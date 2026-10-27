"""GEO-I v005, Programme B.  Witness dimension of obstructions.

DEFINITIONS (exact).  A *witness* of non-embeddedness of K_abs(Lambda,q) is a forbidden template T=(A,B,delta) (see
obstruction_templates, T-FIN) that is realized in the box q, i.e. P(u;A) and P(u+delta;B) have all corners in [0,q]\\{0}.
Theorem T-REL says: K_abs(Lambda,q) is non-embedded iff at least one witness exists; and the witnesses are exactly the
non-face pairs of cells of the actual complex at q (complete enumeration, no cap).
For a witness T:
   d_span(T)         = rank_Q [A, B, delta]                   (affine span of the two cells together)
   d_support(T)      = number of coordinates i with a nonzero entry in some generator or in delta
   d_intersection(T) = dim( P(u;A) cap P(u+delta;B) ) = |A|+|B|-d_span(T)
(the last because delta lies in the span of A u B, so aff P(u;A) cap aff P(u+delta;B) has dimension |A|+|B|-rank and
the common point of the relative interiors, guaranteed by the open-zonotope condition, makes the intersection full-dimensional in it).
A box q is an *essential coordinate obstruction* if K_abs(Lambda,q) is non-embedded while K_abs(Lambda,q with q_i:=0) is
embedded for every i (computed from the restricted complexes, not assumed).
minimal obstruction boxes: non-embedded boxes minimal for the product order (up-set property of non-embeddedness).
"""
import os, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from obstruction_templates import (Lattice, rank, _gens, zonotope_box, in_open_zonotope, corners, classify)


def realized(lat, A, B, delta, m):
    """is the template realized in box m ?  (exact search over u in Lambda)"""
    k = lat.k
    C = corners((0,) * k, A) + corners(tuple(delta), B)
    lo = [min(c[i] for c in C) for i in range(k)]; hi = [max(c[i] for c in C) for i in range(k)]
    if any(hi[i] - lo[i] > m[i] for i in range(k)): return False
    zero = {tuple(-x for x in c) for c in C}
    for u in itertools.product(*[range(-lo[i], m[i] - hi[i] + 1) for i in range(k)]):
        if u in zero or not lat.member(u): continue
        return True
    return False


def witnesses(lat, m, maxdim=None, stop_at_first=False):
    """all templates realized in box m (complete).  Templates are up to (A,B,d)~(B,A,-d); A,B independent Graver tuples."""
    k = lat.k; maxdim = maxdim or k
    P = [g for g in lat.P if all(abs(g[i]) <= m[i] for i in range(k))]
    subs = []
    def rec(start, cur):
        for i in range(start, len(P)):
            nxt = cur + [i]
            if rank([P[j] for j in nxt]) == len(nxt):
                subs.append(tuple(nxt))
                if len(nxt) < maxdim: rec(i + 1, nxt)
    rec(0, [])
    out = []
    for ia, ta in enumerate(subs):
        A = [P[i] for i in ta]
        for tb in subs[ia:]:
            B = [P[i] for i in tb]
            W = _gens(A, B); lo, hi = zonotope_box(W, k); indep = rank(W) == len(W)
            rngs = [range(max(lo[i], -m[i]), min(hi[i], m[i]) + 1) for i in range(k)]
            for d in itertools.product(*rngs):
                if not lat.member(d): continue
                if not any(d):
                    if ta == tb: continue
                else:
                    if ta == tb and not _lexpos(d): continue
                if not in_open_zonotope(d, W, indep): continue
                if not realized(lat, A, B, d, m): continue
                out.append(describe(lat, A, B, d))
                if stop_at_first: return out
    return out


def _lexpos(g):
    for c in g:
        if c: return c > 0
    return False


def describe(lat, A, B, d):
    gens = [tuple(g) for g in A] + [tuple(g) for g in B]
    sup = sorted({i for v in gens + [tuple(d)] for i in range(lat.k) if v[i]})
    sp = rank(gens + [tuple(d)])
    return {'A': [list(a) for a in A], 'B': [list(b) for b in B], 'delta': list(d), 'kind': classify(lat, A, B, tuple(d)),
            'd_span': sp, 'd_span_gens': rank(gens), 'd_support': len(sup), 'support': sup, 'd_intersection': len(A) + len(B) - sp}


def embedded(lat, m, maxdim=None):
    return not witnesses(lat, m, maxdim, stop_at_first=True)


def audit_oracle(res, b):
    """independent embeddedness oracle: the v003 polyhedral cell-level audit (exact LP), used to locate minimal boxes at k=4.
    Resource exhaustion is reported as UNAVAILABLE (exception), never as embedded."""
    sys.path.insert(0, os.path.join(HERE, '..', 'experiments'))
    from high_dimensional import audit_box
    def emb(lat, q, maxdim=None):
        st = audit_box(res, b, q)['status']
        if st not in ('embedded', 'empty_fibre', 'non_embedded'): raise RuntimeError('UNAVAILABLE: audit at %s gave %s' % (q, st))
        return st != 'non_embedded'
    return emb


def minimal_boxes(lat, bound, maxdim=None, progress=None, oracle=None):
    """minimal non-embedded boxes with all q_i <= bound (exact; up-set pruning).  bound is a search limit: the result is the
    set of minimal obstruction boxes inside [0,bound]^k, complete there."""
    k = lat.k; nonemb = set(); mins = []
    for q in sorted(itertools.product(range(bound + 1), repeat=k), key=lambda q: (sum(q), q)):
        if not any(q): continue
        preds = [q[:i] + (q[i] - 1,) + q[i + 1:] for i in range(k) if q[i] > 0]
        if any(p in nonemb for p in preds): nonemb.add(q); continue
        if not (oracle or embedded)(lat, q, maxdim):
            nonemb.add(q); mins.append(q)
            if progress: progress(q)
    return mins


def analyse_box(lat, m, maxdim=None):
    """full witness table of a (minimal) obstruction box and the essential-coordinate flag."""
    W = witnesses(lat, m, maxdim)
    restr = []
    for i in range(lat.k):
        r = tuple(0 if j == i else m[j] for j in range(lat.k))
        restr.append({'coord': i, 'restricted_box': list(r), 'embedded': (not any(r)) or embedded(lat, r, maxdim)})
    return {'box': list(m), 'n_witnesses': len(W),
            'min_span': min((w['d_span'] for w in W), default=None), 'max_span': max((w['d_span'] for w in W), default=None),
            'min_support': min((w['d_support'] for w in W), default=None),
            'span_histogram': {str(s): sum(1 for w in W if w['d_span'] == s) for s in sorted({w['d_span'] for w in W})},
            'support_histogram': {str(s): sum(1 for w in W if w['d_support'] == s) for s in sorted({w['d_support'] for w in W})},
            'essential_coordinate': all(r['embedded'] for r in restr) and all(x > 0 for x in m),
            'restrictions': restr, 'kinds': sorted({w['kind'] for w in W}),
            'example_min_span_witness': min(W, key=lambda w: (w['d_span'], w['d_support']), default=None),
            'weak_C3_holds': any(w['d_span'] <= 2 for w in W)}


# ---------------------------------------------------------------------------------------------------------------------
# audit-based complete enumeration (scales to k = 4): witnesses = non-face pairs of the cells that are actually present.
# ---------------------------------------------------------------------------------------------------------------------
def witnesses_from_cells(res, b, m, lat=None, cap=None):
    """Complete list of witnesses at box m, from the actual complex K_abs(Lambda,m): for every pair of present cells
    (u;A), (v;B) the pair is a non-face pair iff delta=v-u lies in the open zonotope Z(A,B) and (A,delta)!=(B,0) (T-REL);
    this is the same exact criterion as T-FIN but the pairs come from the complex, not from the template universe."""
    sys.path.insert(0, os.path.join(HERE, '..', 'geometry')); sys.path.insert(0, os.path.join(HERE, '..', 'frozen'))
    from realization import fibre_complex_data
    lat = lat or Lattice(res, b); k = lat.k
    fc = fibre_complex_data(res, m, b)
    allc = [c for dim in fc['cells'] for c in dim]
    out = []; seen = set()
    for i, (u, A) in enumerate(allc):
        for (v, B) in allc[i:]:
            A_, B_ = [tuple(a) for a in A], [tuple(x) for x in B]
            delta = tuple(vi - ui for ui, vi in zip(u, v))
            if A_ == B_ and delta == (0,) * k: continue
            W = _gens(A_, B_); indep = rank(W) == len(W)
            if not in_open_zonotope(delta, W, indep): continue
            key = (tuple(sorted(A_)), tuple(sorted(B_)), delta)
            if key in seen: continue
            seen.add(key); out.append(describe(lat, A_, B_, delta)); out[-1]['base'] = [list(u), list(v)]
            if cap and len(out) >= cap: return out
    return out


def canon(w):
    """canonical key of a witness up to (A,B,delta) ~ (B,A,-delta) and generator order."""
    A = tuple(sorted(map(tuple, w['A']))); B = tuple(sorted(map(tuple, w['B']))); d = tuple(w['delta'])
    k1 = (A, B, d); k2 = (B, A, tuple(-x for x in d))
    return min(k1, k2)


def analyse_box_cells(res, b, m, oracle=None, lat=None):
    """full witness table (from the actual complex) of a box + essential-coordinate flag using the independent LP audit oracle
    for the restrictions q_i := 0."""
    lat = lat or Lattice(res, b); k = lat.k
    W = witnesses_from_cells(res, b, m, lat)
    oracle = oracle or audit_oracle(res, b)
    restr = []
    for i in range(k):
        r = tuple(0 if j == i else m[j] for j in range(k))
        restr.append({'coord': i, 'restricted_box': list(r), 'embedded': (not any(r)) or oracle(lat, r)})
    hist = lambda key: {str(v): sum(1 for w in W if w[key] == v) for v in sorted({w[key] for w in W})}
    return {'box': list(m), 'n_witnesses': len(W), 'min_span': min((w['d_span'] for w in W), default=None),
            'max_span': max((w['d_span'] for w in W), default=None), 'min_support': min((w['d_support'] for w in W), default=None),
            'span_histogram': hist('d_span'), 'support_histogram': hist('d_support'), 'intersection_histogram': hist('d_intersection'),
            'kinds': sorted({w['kind'] for w in W}), 'essential_coordinate': all(r['embedded'] for r in restr) and all(x > 0 for x in m),
            'restrictions': restr, 'weak_C3_holds': any(w['d_span'] <= 2 for w in W),
            'witnesses': W}


def _faces(u, A):
    """all faces (including the cell itself) of the parallelotope P(u;A) as (base, sorted generator tuple)."""
    A = [tuple(a) for a in A]; out = set(); n = len(A)
    for mask in range(1 << n):                     # which generators survive as directions of the face
        keep = [A[i] for i in range(n) if mask >> i & 1]
        rest = [A[i] for i in range(n) if not mask >> i & 1]
        for sub in range(1 << len(rest)):          # which of the remaining generators are added to the base (the opposite facet)
            base = tuple(u)
            for j, r in enumerate(rest):
                if sub >> j & 1: base = tuple(x + y for x, y in zip(base, r))
            out.add((base, tuple(sorted(keep))))
    return out


def irreducibility(W):
    """Definition.  A witness (c1,c2) (a non-face pair of cells of one complex) is IRREDUCIBLE if no other pair (f1,f2) of faces
    f1 <= c1, f2 <= c2, (f1,f2) != (c1,c2), is itself a non-face pair.  Faces of cells are cells, and a non-face pair of faces is a witness
    of the same box, so irreducibility is decided inside the (complete) witness list W of the box."""
    cells = []
    for w in W:
        u, v = w['base']
        cells.append(((tuple(u), tuple(sorted(map(tuple, w['A'])))), (tuple(v), tuple(sorted(map(tuple, w['B']))))))
    pairs = {frozenset(c) if c[0] != c[1] else frozenset([c[0], c[0], 'x']) for c in cells}
    S = set(cells) | {(b, a) for a, b in cells}
    flags = []
    for (c1, c2) in cells:
        F1 = _faces(*c1); F2 = _faces(*c2); red = False
        for f1 in F1:
            for f2 in F2:
                if (f1, f2) == (c1, c2): continue
                if (f1, f2) in S: red = True; break
            if red: break
        flags.append(not red)
    return flags
