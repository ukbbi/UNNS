"""GIG-I v005 Stage 3 -- cycle/cochain/filling machinery for the permutohedron P_k in any dimension.
Faces = ordered set partitions of {0..k-1} (rank coordinates). A prefix-set family is an int with bit I set iff the rank-subset I (bitmask) is admissible."""
import _vpath  # noqa: F401
import history_complex as hc
import face_threshold as ft


class PK:
    _cache = {}

    def __new__(cls, k):
        if k not in cls._cache:
            o = super().__new__(cls)
            o._init(k)
            cls._cache[k] = o
        return cls._cache[k]

    def _init(self, k):
        self.k = k
        self.FS, self.VM, self.DIM, self.BND = hc._complex_data(k)
        self.IDX = {f: i for i, f in enumerate(self.FS)}
        self.ALL = sum(1 << s for s in range(1, 1 << k))
        self.PM = []
        for f in self.FS:
            r = 0
            for s in ft.pref_sets(f):
                r |= 1 << s
            self.PM.append(r)
        self._rows = {}

    def tf(self, f):
        return tuple(tuple(b) for b in f)

    def ids(self, faces):
        return [self.IDX[self.tf(f)] for f in faces]

    def rows(self, d):
        """list of (prefix family, boundary bitmask over global ids) of all faces of dimension d."""
        if d not in self._rows:
            self._rows[d] = [(self.PM[i], sum(1 << b for b in self.BND[i])) for i in range(len(self.FS)) if self.DIM[i] == d]
        return self._rows[d]

    def bits(self, ids):
        z = 0
        for g in ids:
            z |= 1 << g
        return z

    def pz(self, zbits):
        r, x = 0, zbits
        while x:
            l = x & -x
            r |= self.PM[l.bit_length() - 1]
            x ^= l
        return r

    def bounds(self, zbits, allowed, d):
        """zbits: a d-cycle; True iff z lies in the GF(2) span of boundaries of the (d+1)-faces F with Pref(F) <= allowed."""
        piv = {}
        for pm, b in self.rows(d + 1):
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

    def is_cycle(self, zbits):
        acc, x = 0, zbits
        while x:
            l = x & -x
            for b in self.BND[l.bit_length() - 1]:
                acc ^= 1 << b
            x ^= l
        return acc == 0

    def obstructed(self, phibits, d):
        """(d+1)-faces F of P_k with odd |boundary(F) ∩ phi|."""
        return [i for i in range(len(self.FS)) if self.DIM[i] == d + 1 and sum(1 for b in self.BND[i] if phibits >> b & 1) & 1]

    # -------------------------------------------------------------------------------- exact minimal filling families
    def minimal_families(self, zbits, d, max_iter=100000, certificate=False):
        P = self.pz(zbits)
        U = self.ALL & ~P
        elems = [s for s in range(1, 1 << self.k) if U >> s & 1]
        comps, T, calls = [], [0], 0
        for _ in range(max_iter):
            bad = None
            for t in T:
                calls += 1
                if not self.bounds(zbits, P | t, d):
                    bad = t
                    break
            if bad is None:
                st = {"q": len(elems), "bound_calls": calls, "maximal_false": len(comps)}
                if certificate:
                    st["maximal_false_sets"] = [U & ~c for c in comps]
                return sorted(T), st
            mf = bad
            for s in elems:
                if not mf >> s & 1:
                    calls += 1
                    if not self.bounds(zbits, P | mf | 1 << s, d):
                        mf |= 1 << s
            comps.append(U & ~mf)
            T = transversals(comps, self.k)
        raise RuntimeError


def transversals(comps, k):
    T = [0]
    for E in comps:
        keep = [t for t in T if t & E]
        bits = [1 << s for s in range(1, 1 << k) if E >> s & 1]
        new = []
        for t in T:
            if not t & E:
                new += [t | b for b in bits]
        cand = sorted(dict.fromkeys(keep + new), key=lambda v: v.bit_count())
        mins = []
        for c in cand:
            if not any(m & c == m for m in mins):
                mins.append(c)
        T = mins
    return T


def verify_family_certificate(pk, zbits, d, fams, maxfalse):
    r"""independent completeness check.  fams: claimed minimal filling families; maxfalse: claimed maximal non-bounding sets (relative to U = ALL \ P_z).
    (1) every family bounds and is minimal; (2) every listed set is non-bounding and maximal; (3) duality: the minimal transversals of `fams`
    (computed here by a different routine) are exactly the minimal elements among the complements U \ N.  Together these imply that
    a set bounds iff it contains a listed family."""
    P = pk.pz(zbits)
    U = pk.ALL & ~P
    for F in fams:
        if not pk.bounds(zbits, P | F, d):
            return False, "family does not bound"
        x = F
        while x:
            l = x & -x
            if pk.bounds(zbits, P | (F & ~l), d):
                return False, "family not minimal"
            x ^= l
    for N in maxfalse:
        if pk.bounds(zbits, P | N, d):
            return False, "listed false set bounds"
        y = U & ~N
        while y:
            l = y & -y
            if not pk.bounds(zbits, P | N | l, d):
                return False, "false set not maximal"
            y ^= l
    comps = sorted({U & ~N for N in maxfalse}, key=lambda v: v.bit_count())
    mins = [c for c in comps if not any(o != c and o & c == o for o in comps)]
    tr = _berge_independent(list(fams))
    if sorted(tr) != sorted(mins):
        return False, "duality fails"
    return True, "ok"


def _berge_independent(sets):
    """minimal transversals (hitting sets) of a list of int-bitsets, by repeated product and absorption (independent of PK.transversals)."""
    cur = {0}
    for E in sets:
        nxt = set()
        elems = [1 << i for i in range(E.bit_length()) if E >> i & 1]
        for t in cur:
            if t & E:
                nxt.add(t)
            else:
                for e in elems:
                    nxt.add(t | e)
        cur = {t for t in nxt if not any(o != t and o & t == o for o in nxt)}
    return sorted(cur)
