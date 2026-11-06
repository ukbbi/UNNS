"""GIG-I v005 Stage 2 -- obstruction-atlas machinery for 2-cycles of the permutohedron P_6.
A cycle z (set of 2-face ids of P_6) lives in X_lambda(m) iff P_z <= A(m); it bounds iff z is in the GF(2) span of d3 of the 3-faces F of P_6 with Pref(F) <= A(m)
(T16/T17).  Prefix sets are rank bitmasks (1..63); a family of prefix sets is a 64-bit integer with bit s set iff set s is admissible."""
import _vpath  # noqa: F401
import itertools
import hole_survival as H

FS, DIM, BND = H._FS, H._DIM, H._BND
IDX = H._IDX
ALL = sum(1 << s for s in range(1, 64))


def _pm(face):
    r = 0
    for s in H._pref_sets(face):
        r |= 1 << s
    return r


PM = [_pm(f) for f in FS]                                            # prefix-set family of every face of P_6
F3 = [(PM[i], sum(1 << b for b in BND[i])) for i in range(len(FS)) if DIM[i] == 3]
SIGMAS = list(itertools.permutations(range(6)))


def bounds(zbits, allowed):
    """zbits: int bitmask over global face ids (a 2-cycle). allowed: family bitmask. True iff z bounds among 3-faces with Pref <= allowed."""
    piv = {}
    for pm, b in F3:
        if pm & ~allowed:
            continue
        x = b
        while x:
            h = x.bit_length() - 1
            if h in piv:
                x ^= piv[h]
            else:
                piv[h] = x
                break
    x = zbits
    while x:
        h = x.bit_length() - 1
        if h not in piv:
            return False
        x ^= piv[h]
    return True


def pz(zbits):
    r = 0
    x = zbits
    while x:
        l = x & -x
        r |= PM[l.bit_length() - 1]
        x ^= l
    return r


def minimal_families(zbits, max_iter=10000):
    """all minimal S <= U = ALL \\ P_z with  z bounds when A = P_z | S.  Exact (dualisation: minimal true points = minimal transversals of the
    complements of the maximal false points).  Returns (families, stats)."""
    P = pz(zbits)
    U = ALL & ~P
    elems = [s for s in range(1, 64) if U >> s & 1]
    comps = []
    T = [0]
    calls = 0
    for it in range(max_iter):
        bad = None
        for t in T:
            calls += 1
            if not bounds(zbits, P | t):
                bad = t
                break
        if bad is None:
            return sorted(T), {"q": len(elems), "bound_calls": calls, "maximal_false": len(comps)}
        mf = bad
        for s in elems:                                              # extend to a maximal false point
            if not mf >> s & 1:
                calls += 1
                if not bounds(zbits, P | mf | 1 << s):
                    mf |= 1 << s
        comps.append(U & ~mf)
        T = _transversals(comps)
    raise RuntimeError("no convergence")


def _transversals(comps):
    T = [0]
    for E in comps:
        keep = [t for t in T if t & E]
        new = []
        bits = [1 << s for s in range(1, 64) if E >> s & 1]
        for t in T:
            if not t & E:
                new += [t | b for b in bits]
        cand = list(dict.fromkeys(keep + new))
        cand.sort(key=lambda v: v.bit_count())
        mins = []
        for c in cand:
            if not any(m & c == m for m in mins):
                mins.append(c)
        T = mins
    return T


def survives(zbits_P, fams, allowed):
    """atlas predicate: P_z <= allowed and no minimal family contained in allowed."""
    if zbits_P & ~allowed:
        return False
    return not any(f & allowed == f for f in fams)


# ------------------------------------------------------------------------------------------------ S_6 action
def _rank_map(sig, face):
    return tuple(tuple(sorted(sig[x] for x in B)) for B in face)


_SIGFACE = {}


def act_face(sig, g):
    return IDX[_rank_map(sig, FS[g])]


def act_bits(sig, zbits):
    out = 0
    x = zbits
    while x:
        l = x & -x
        out |= 1 << act_face(sig, l.bit_length() - 1)
        x ^= l
    return out


_CODEPERM = {}


def act_family(sig, fam):
    """image of a family of prefix sets: subset mask I -> sigma(I)."""
    tab = _CODEPERM.get(sig)
    if tab is None:
        tab = [0] * 64
        for I in range(64):
            J = 0
            for r in range(6):
                if I >> r & 1:
                    J |= 1 << sig[r]
            tab[I] = J
        _CODEPERM[sig] = tab
    out = 0
    x = fam
    while x:
        l = x & -x
        out |= 1 << tab[l.bit_length() - 1]
        x ^= l
    return out


def canonical(zbits):
    """(canonical cycle, sigma) -- lexicographically least image of z under S_6 (as a sorted tuple of face ids)."""
    best = None
    ids = []
    x = zbits
    while x:
        l = x & -x
        ids.append(l.bit_length() - 1)
        x ^= l
    for sig in SIGMAS:
        t = tuple(sorted(act_face(sig, g) for g in ids))
        if best is None or t < best[0]:
            best = (t, sig)
    zb = 0
    for g in best[0]:
        zb |= 1 << g
    return zb, best[1]
