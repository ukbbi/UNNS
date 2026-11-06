"""GIG-INFO v001 -- exact information-observation hierarchy for an arithmetic grammar.

A SYSTEM is a pair (content C of 6 distinct labels, source m).  Its admissible histories are the arrangements (permutations) of C admissible from m
(simulation-based, v001), its swap graph is the induced permutohedron graph, K_A(m) its permutohedral complex (GF(2)).
Observation levels (each a function of the previous one's refinement):
  O0 = N                                  number of admissible histories (H_hist = log2 N under uniform sampling)
  O1 = (N, histogram of |B_1|, histogram of |B_2|)    exact radius-1/2 accessibility histograms of the swap graph
  O2 = isomorphism class of the uncolored swap graph  (exact: explicit bijections / exhaustive negative search, v002)
  O2c = (O2, Betti vector, f-vector)      uncolored graph plus cellular invariants of K_A
  O3 = the labelled arrangement set itself (exact admissibility data); determines Y.
Anchored hole state Y(m): fix the anchor source m0 with beta_2(K_A(m0))=1 and its generator class [z].  For A(m) >= A(m0) (comparable), Y(m)=1 iff the image of [z] in H_2(K_A(m);GF(2)) is non-zero; Y(m)=0 otherwise ("filled").
If A(m) does not contain A(m0), the class is undefined: Y3(m)='NA'.  A(m) = {I : D(I) | m} (rank-subset admissibility), a face of P_6 is present iff all its prefix rank-subsets lie in A(m)."""
import hashlib
from collections import Counter
from fractions import Fraction
from math import gcd
import _vpath  # noqa: F401
import history_complex as hc
import swap_graph as sg
from graph_iso import are_isomorphic, wl_hash
from information import shannon, fmt
from pk import PK
import fi, cert

P6 = PK(6)


def denominators(labels):
    k = len(labels)
    D = [1] * (1 << k); num = [1] * (1 << k); den = [1] * (1 << k)
    for I in range(1, 1 << k):
        j = (I & -I).bit_length() - 1
        J = I & (I - 1)
        num[I] = num[J] * labels[j]
        den[I] = den[J] * (labels[j] + 1) ** 2
        D[I] = num[I] // gcd(num[I], den[I])
    return D


def vp(n, p):
    e = 0
    while n % p == 0:
        n //= p; e += 1
    return e


class System:
    def __init__(self, content, m):
        self.content, self.m = tuple(sorted(content)), m
        self.D = denominators(list(self.content))
        self.Amask = sum(1 << s for s in range(1, 64) if m % self.D[s] == 0)
        self.A = hc.admissible_arrangements(self.content, m)
        self.N = len(self.A)
        order, self.adj = hc.induced_adjacency(set(self.A), 6)
        prof = sg.ball_profile(self.adj) if self.N else []
        self.h1 = tuple(sorted(Counter(sg.ball_size(p, 1) for p in prof).items()))
        self.h2 = tuple(sorted(Counter(sg.ball_size(p, 2) for p in prof).items()))
        self.betti = hc.betti(set(self.A), 6) if self.N else (0,) * 6
        self.fvec = hc.f_vector(set(self.A), 6) if self.N else (0,) * 6
        self.wl = wl_hash(self.adj) if self.N else ()
        self.key3 = hashlib.sha256(repr(sorted(self.A)).encode()).hexdigest()

    @property
    def O0(self): return (self.N,)
    @property
    def O1(self): return (self.N, self.h1, self.h2)


def iso_classes(systems):
    """exact isomorphism classes of the swap graphs: dict index -> class id (WL hash used only as a bucket filter)."""
    cls, reps = {}, []
    for i, s in enumerate(systems):
        for cid, j in enumerate(reps):
            t = systems[j]
            if t.N == s.N and t.wl == s.wl and are_isomorphic(t.adj, s.adj):
                cls[i] = cid
                break
        else:
            cls[i] = len(reps)
            reps.append(i)
    return cls


class Anchor:
    def __init__(self, content, m0):
        self.content, self.m0 = tuple(sorted(content)), m0
        s0 = System(content, m0)
        self.s0 = s0
        A0 = s0.Amask
        # a generator of H_2(K_A(m0)): kernel of d_2 modulo boundaries
        ids = [i for i in range(len(P6.FS)) if P6.DIM[i] == 2 and not P6.PM[i] & ~A0]
        ker = fi.cycle_basis(P6, A0, 2)
        B = fi.Bounder(P6, A0, 2)
        gens = [z for z in ker if not B.contains(z)]
        # beta_2 = dim ker - rank(boundaries)
        import jmap
        r, keep = jmap.rank_mod_boundaries(B, ker)
        self.beta2 = r
        self.z = gens[0] if gens else None
        self.A0 = A0

    def state(self, s):
        """'NA' | 0 | 1 for a System s."""
        if s.Amask & self.A0 != self.A0:
            return "NA"
        return 0 if P6.bounds(self.z, s.Amask, 2) else 1

    def certificate(self, s):
        st = self.state(s)
        if st == 1:
            phi = cert.solve(P6, s.Amask, 2, self.z)
            ok, msg = cert.verify_certificate(P6, s.Amask, 2, self.z, phi)
            return {"kind": "cochain", "support": len(phi), "verified": ok}
        if st == 0:
            ch = fi.Bounder(P6, s.Amask, 2).express(self.z)
            acc = 0
            for g in ch:
                for b in P6.BND[g]:
                    acc ^= 1 << b
            return {"kind": "filling_chain", "size": len(ch), "verified": acc == self.z}
        return {"kind": "NA"}


# ------------------------------------------------------------------ exact entropies
def entropy_of_counts(counts):
    tot = sum(counts)
    return shannon([Fraction(c, tot) for c in counts])


def cond_entropy(samples):
    """samples: list of (y, sig) with uniform weight.  Returns (H(Y), H(Y|O), I) as Decimals (fmt) plus the exact class table."""
    n = len(samples)
    from decimal import Decimal
    HY = entropy_of_counts(list(Counter(y for y, _ in samples).values()))
    by = {}
    for y, sig in samples:
        by.setdefault(sig, []).append(y)
    HYO = Decimal(0)
    for sig, ys in by.items():
        HYO += Decimal(len(ys)) / Decimal(n) * entropy_of_counts(list(Counter(ys).values()))
    HO = entropy_of_counts([len(v) for v in by.values()])
    return HY, HYO, HY - HYO, len(by), HO


def hartley_dec(n):
    from information import log2_dec
    from decimal import Decimal
    return log2_dec(n) if n > 0 else None
