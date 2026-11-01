"""HD-CQ1: constraint-essential and topologically-essential prime coordinates of route complexes (distinct-label contents).
word -> per-active-prime threshold b_p(w); source = resource vector e (v_p(m) capped at max_w b_p, gcd reduction).
relaxing prime p  <=>  setting e_p = max_w b_p.   Feature = Betti vector (GF(2), permutohedral complex K_A of HD-1D v003)."""
from itertools import permutations, product, combinations
from prime_geometry import active_primes, delta
from route_topology import betti


def thresholds(C):
    act = active_primes(C); lab = sorted(C); out = {}
    for perm in permutations(range(len(lab))):
        w = [lab[i] for i in perm]; b = []
        for p in act:
            s = bm = 0
            for N in w:
                s += delta(N, [p])[0]; bm = max(bm, -s)
            b.append(bm)
        out[perm] = tuple(b)
    return act, out


class Content:
    def __init__(self, C):
        self.C = tuple(sorted(C)); self.k = len(C)
        self.act, self.ex = thresholds(self.C); self.n = len(self.act)
        self.mx = tuple(max(v[i] for v in self.ex.values()) for i in range(self.n))
        self.cache = {}
        self.triv = (1,) + (0,) * (self.k - 1)

    def betti_at(self, e):
        if e not in self.cache:
            adm = frozenset(w for w, v in self.ex.items() if all(v[i] <= e[i] for i in range(self.n)))
            self.cache[e] = betti(adm, self.k)[0] if adm else None
        return self.cache[e]

    def box_size(self):
        s = 1
        for x in self.mx: s *= x + 1
        return s

    def relax(self, e, S):
        return tuple(self.mx[i] if i in S else e[i] for i in range(self.n))

    def features(self):
        """list of (e, betti, support_primes, essential_primes, cut_order) over the resource box, nontrivial vectors only"""
        rows = []
        for e in product(*[range(x + 1) for x in self.mx]):
            b = self.betti_at(e)
            if b is None or b == self.triv: continue
            sup = None
            for r in range(self.n + 1):
                for S in combinations(range(self.n), r):          # keep S, relax the rest
                    rel = tuple(i for i in range(self.n) if i not in S)
                    if self.betti_at(self.relax(e, rel)) == b: sup = [self.act[i] for i in S]; break
                if sup is not None: break
            ess = [self.act[i] for i in range(self.n)
                   if self.relax(e, (i,)) != e and self.betti_at(self.relax(e, (i,))) == self.triv]
            cut = None
            for r in range(1, self.n + 1):
                if any(self.betti_at(self.relax(e, S)) == self.triv for S in combinations(range(self.n), r)): cut = r; break
            rows.append((e, b, sup, ess, cut))
        return rows


def kind(b):
    return "b0>1" if b[0] > 1 else ("b1" if b[1] else "b2+")
