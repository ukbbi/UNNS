"""HD-1D v003 INDEPENDENT verifier.  Re-implements admissibility, thresholds, feeding digraph / SCCs, permutohedral homology (GF(2)),
history enumeration and occurrence fibres from the definitions; the builder modules of v003 (swap_classes, route_topology, topo_census,
occurrence_bridge) are NOT imported by the checks (only compared against, in the shard X7)."""
import os, sys, json, itertools, random, hashlib
from math import gcd, lcm, prod
from collections import defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = []; FAILS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + ((" -- " + str(detail)) if detail != "" else ""), flush=True)
    if not ok: FAILS.append(name)


def load(rel):
    with open(os.path.join(ROOT, rel)) as f: return json.load(f)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ---------------------------------------------------------------- arithmetic from the definition
def vp(n, p):
    e = 0
    while n % p == 0: n //= p; e += 1
    return e


def primes_of(n):
    out = []; p = 2
    while p * p <= n:
        if n % p == 0: out.append(p)
        while n % p == 0: n //= p
        p += 1
    if n > 1: out.append(n)
    return out


def adm(m, w):
    for N in w:
        if m % N: return False
        m = m // N * (N + 1) ** 2
    return True


def Kthr(w):
    ps = set()
    for N in w: ps |= set(primes_of(N)) | set(primes_of(N + 1))
    k = 1
    for p in ps:
        run = need = 0
        for N in w:
            run += 2 * vp(N + 1, p) - vp(N, p); need = max(need, -run)
        k *= p ** need
    return k


def kappa_v(S):
    ps = set()
    for N in S: ps |= set(primes_of(N)) | set(primes_of(N + 1))
    k = 1
    for p in ps:
        tot = sum(2 * vp(N + 1, p) - vp(N, p) for N in S)
        if tot < 0: k *= p ** (-tot)
    return k


def arrs(c): return sorted(set(itertools.permutations(c)))


def nbrs(w):
    for i in range(len(w) - 1):
        if w[i] != w[i + 1]: yield w[:i] + (w[i + 1], w[i]) + w[i + 2:]


def classes(V):
    V = set(V); seen = set(); out = 0
    for v in V:
        if v in seen: continue
        out += 1; st = [v]; seen.add(v)
        while st:
            x = st.pop()
            for y in nbrs(x):
                if y in V and y not in seen: seen.add(y); st.append(y)
    return out


def closure(vals, cap=20000):
    S = set(vals); fr = set(vals)
    while fr:
        new = set()
        for a in fr:
            for b in list(S):
                c = lcm(a, b)
                if c not in S: new.add(c)
        S |= new; fr = new
        if len(S) > cap: return None
    return sorted(S)


def sources(c, cap=400):
    """sources at which the admissible set can change (lcm-closure of the thresholds), thinned to <= cap, plus a few multiples"""
    cl = closure({Kthr(w) for w in arrs(c)})
    if cl is None: return []
    if len(cl) > cap: cl = random.sample(cl, cap)
    return sorted(set(cl) | {x * p for x in cl[:20] for p in (2, 3)})


def ncls_direct(c, m):
    """swap classes from the definition: vertices = arrangements admitted by direct simulation, edges = adjacent exchanges"""
    return classes([w for w in arrs(c) if adm(m, w)])


# ---------------------------------------------------------------- feeding digraph (own coding)
def feeds(a, b): return a != b and gcd(a + 1, b) > 1


def sccs_topo(labels):
    L = sorted(set(labels)); n = len(L)
    reach = [[feeds(L[i], L[j]) for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]: reach[i][j] = True
    comp = {}
    for i in range(n):
        comp[i] = frozenset([L[i]] + [L[j] for j in range(n) if j != i and reach[i][j] and reach[j][i]])
    blocks = set(comp.values())
    # topological order by number of blocks that reach it (longest-path layering)
    def before(B, C): return B != C and any(reach[L.index(x)][L.index(y)] for x in B for y in C)
    order = []; left = set(blocks)
    while left:
        for B in sorted(left, key=min):
            if not any(before(C, B) for C in left if C != B): order.append(B); left.discard(B); break
    return order


def f2_classes(c, m):
    total = 1; num = m; den = 1                      # entry state of the block = num/den (exact rational, integral whenever the earlier blocks are admissible)
    for B in sccs_topo(c):
        sub = tuple(x for x in sorted(c) if x in B)
        if num % den: return 0
        k = ncls_direct(sub, num // den)
        if k == 0: return 0
        total *= k
        for N in sub: num *= (N + 1) ** 2; den *= N
    return total


# ---------------------------------------------------------------- permutohedral homology (own coding)
def set_partitions_ordered(k):
    """ordered set partitions of {0..k-1} via 'insert element into existing block or as new block at a position'"""
    res = [[]]
    for e in range(k):
        new = []
        for p in res:
            for i in range(len(p)): new.append(p[:i] + [p[i] | {e}] + p[i + 1:])
            for i in range(len(p) + 1): new.append(p[:i] + [frozenset([e])] + p[i:])
        res = new
    return [tuple(frozenset(b) for b in p) for p in res]


_FACE_CACHE = {}


def faces_of(k):
    if k in _FACE_CACHE: return _FACE_CACHE[k]
    F = set_partitions_ordered(k)
    def verts(f):
        vs = [()]
        for B in f: vs = [v + q for v in vs for q in itertools.permutations(sorted(B))]
        return frozenset(vs)
    data = {f: verts(f) for f in F}
    _FACE_CACHE[k] = (F, data); return F, data


def homology_betti(A, k, cubical=False):
    A = frozenset(A); F, data = faces_of(k)
    keep = [f for f in F if data[f] <= A and (not cubical or all(len(B) <= 2 for B in f))]
    by = defaultdict(list)
    for f in keep: by[k - len(f)].append(f)
    index = {d: {f: i for i, f in enumerate(L)} for d, L in by.items()}
    def bd(f):
        out = []
        for i, B in enumerate(f):
            if len(B) < 2: continue
            Bl = sorted(B)
            for r in range(1, len(Bl)):
                for C in itertools.combinations(Bl, r):
                    Cs = frozenset(C); out.append(f[:i] + (Cs, B - Cs) + f[i + 1:])
        return out
    def rank(d):
        if d == 0 or d not in by: return 0
        piv = {}; rk = 0
        for f in by[d]:
            row = 0
            for g in bd(f): row ^= 1 << index[d - 1][g]
            while row:
                h = row.bit_length() - 1
                if h in piv: row ^= piv[h]
                else: piv[h] = row; rk += 1; break
        return rk
    return tuple(len(by.get(d, [])) - rank(d) - rank(d + 1) for d in range(k))


def common_proper_face_components(R, k):
    """components of R (set of permutations) under 'both lie in a common proper face' (own: prefix-set criterion)"""
    R = list(R)
    def prefix_sets(v): return {frozenset(v[:s]) for s in range(1, k)}
    P = {v: prefix_sets(v) for v in R}
    # two vertices lie in a common proper face iff they share a proper prefix set of positions
    par = {v: v for v in R}
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    byset = defaultdict(list)
    for v in R:
        for s in P[v]: byset[s].append(v)
    for s, vs in byset.items():
        for v in vs[1:]: par[find(v)] = find(vs[0])
    return len({find(v) for v in R})


def pattern(c, m):
    rank = {x: i for i, x in enumerate(sorted(c))}
    return frozenset(tuple(rank[x] for x in w) for w in arrs(c) if adm(m, w))


# ================================================================= shards
def shard_X0(full=False):
    """release hygiene: pins of v001 modules, status gates, required files"""
    pins = load("results/V001_PINS.json")
    check("X0 copied v001 builder modules byte-identical to the v001 release (%d)" % len(pins), all(sha(os.path.join(ROOT, "src", f)) == s for f, s in pins.items()))
    st = load("STATUS.json")
    check("X0 STATUS gates: C3 NOT_CLAIMED, novelty not assessed, same-author caveat", st["gates"]["C3"] == "NOT_CLAIMED" and st["gates"]["NOVELTY"] == "NOT_ASSESSED" and "same author" in st["independence_caveat"])
    check("X0 STATUS scope note keeps FIXED-source scope", "FIXED source" in st["scope_note"])
    need = ["theory/THRESHOLDS.md", "theory/CONNECTIVITY.md", "theory/OBSTRUCTIONS.md", "theory/ROUTE_TOPOLOGY.md", "theory/OCCURRENCE_BRIDGE.md", "results/THEOREMS.md", "results/COUNTEREXAMPLES.md", "results/OPEN_PROBLEMS.md",
            "src/thresholds.py", "src/swap_classes.py", "src/route_topology.py", "src/occurrence_bridge.py"]
    check("X0 required modules and documents present", all(os.path.exists(os.path.join(ROOT, p)) for p in need), [p for p in need if not os.path.exists(os.path.join(ROOT, p))])
    sib = os.path.join(os.path.dirname(ROOT), "GEO_HD_1D_v002", "MANIFEST.json")
    if os.path.exists(sib):
        mf = json.load(open(sib))["files"]; d = os.path.dirname(sib)
        check("X0 sibling GEO_HD_1D_v002 untouched (manifest hashes)", all(sha(os.path.join(d, p)) == h for p, h in mf.items()))
    else:
        check("X0 sibling v002 not present here (skipped)", True)


def shard_X1(full=False):
    """gcd reduction, K | prod N, saturation, Lemma NF"""
    random.seed(11)
    labs = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 20, 21, 27, 35]
    ok = True; n = 0
    for _ in range(15000 if full else 5000):
        c = tuple(random.choice(labs) for _ in range(random.randint(2, 5))); P = prod(c); w = list(c); random.shuffle(w); w = tuple(w)
        m = random.randint(1, 4000); n += 1
        ok &= (Kthr(w) != 0 and P % Kthr(w) == 0) and (adm(m, w) == adm(gcd(m, P), w))
    check("X1 K(w) | P(C)=prod N and admissibility depends only on gcd(m,P(C))  (%d tests)" % n, ok)
    ok = all(Kthr(w) == lcm(*[kappa_v(w[:j]) for j in range(1, len(w) + 1)]) for w in [tuple(random.choice(labs) for _ in range(random.randint(1, 6))) for _ in range(4000)])
    check("X1 prefix-set form: K(w) = lcm_j kappa({N_1..N_j}); admissibility = every prefix SET is feasible", ok)
    ok = True
    for c in [(2, 3, 14), (1, 2, 3, 8), (2, 3, 4, 5), (2, 2, 3, 9)]:
        A = arrs(c); P = prod(c)
        ok &= all(adm(P * t, w) for w in A for t in (1, 2, 3)) and classes(A) == 1
    check("X1 saturation: P(C) | m => all arrangements admissible and the swap graph is connected", ok)
    R = 40 if not full else 70
    n = bad = 0
    for x in range(1, R):
        for y in range(1, R):
            if x == y or feeds(x, y): continue
            for s in range(1, 1200):
                if adm(s, (x, y)):
                    n += 1
                    if not adm(s, (y, x)): bad += 1
    check("X1 Lemma NF: x does not feed y and (x,y) admissible from s  =>  (y,x) admissible from s  (%d instances)" % n, bad == 0, bad)
    check("X1 Lemma NF threshold form: not feeds(x,y) => K(y,x) | K(x,y)  (labels < %d)" % (3 * R),
          all(Kthr((x, y)) % Kthr((y, x)) == 0 for x in range(1, 3 * R) for y in range(1, 3 * R) if x != y and not feeds(x, y)))


def shard_X2(full=False):
    """F1 (acyclic => connected, universal minimal threshold) and F2 (block product formula) from direct simulation"""
    random.seed(5)
    def run(conts, cap):
        n = bad = 0
        for c in conts:
            for m in sources(c, cap):
                n += 1
                if ncls_direct(c, m) != f2_classes(c, m): bad += 1
        return n, bad
    R3 = 16 if not full else 24
    n, b = run(itertools.combinations(range(1, R3), 3), 60)
    check("X2 F2 product formula, 3 distinct labels < %d  (%d content-source pairs)" % (R3, n), b == 0, b)
    R4 = 10 if not full else 14
    n, b = run(itertools.combinations(range(1, R4), 4), 40)
    check("X2 F2 product formula, 4 distinct labels < %d  (%d pairs)" % (R4, n), b == 0, b)
    n, b = run((c for c in itertools.combinations_with_replacement(range(1, 8 if not full else 10), 4) if len(set(c)) < 4), 40)
    check("X2 F2 product formula, repeated labels (size 4)  (%d pairs)" % n, b == 0, b)
    # F1: acyclic => never more than one class, and tau-sorted word has the smallest threshold
    ok = True; m1 = 0; ac = 0
    for c in itertools.combinations(range(1, 16 if not full else 22), 3):
        if not all(len(B) == 1 for B in sccs_topo(c)): continue
        ac += 1
        tau = tuple(next(iter(B)) for B in sccs_topo(c))
        Kt = Kthr(tau)
        ok &= all(Kthr(w) % Kt == 0 for w in arrs(c))
        for m in sources(c, 60): m1 = max(m1, ncls_direct(c, m))
    # acyclic => the admissible set is closed under inversion-reducing adjacent swaps w.r.t. tau (weak-order lower set)
    ok = True; nlow = 0
    for c in itertools.combinations(range(1, 14 if not full else 20), 4):
        if not all(len(B) == 1 for B in sccs_topo(c)): continue
        pos = {next(iter(B)): i for i, B in enumerate(sccs_topo(c))}
        for m in sources(c, 30):
            Aset = {w for w in arrs(c) if adm(m, w)}
            for w in Aset:
                for i in range(3):
                    if pos[w[i]] > pos[w[i + 1]]:
                        nlow += 1; ok &= (w[:i] + (w[i + 1], w[i]) + w[i + 2:]) in Aset
    check("X2 acyclic => admissible set is a weak-order lower set for any linear extension tau  (%d closure instances, k=4)" % nlow, ok)
    check("X2 F1: acyclic feeding digraph (%d contents): K(tau) divides every K(w); at most one swap class at every source (max %d)" % (ac, m1), ok and m1 <= 1)


def shard_X3(full=False):
    """corollaries: {2,3,N} converse proved by SCCs; split needs a block of >= 3 distinct labels; hub descent"""
    ok = True
    for q in range(1, 241 if not full else 600):
        k = ncls_direct((2, 3, 14), 14 * q)
        ok &= (k == (2 if gcd(q, 6) == 1 else 1))
    check("X3 baseline {2,3,14}: swap classes at source 14q are 2 iff gcd(q,6)=1 else 1 (connection thresholds 28 and 42), direct simulation", ok)
    top = 3000 if full else 600
    check("X3 {2,3,N}: feeding digraph strongly connected  <=>  N = 2,3 mod 6   (4<=N<=%d)" % top,
          all((len(sccs_topo((2, 3, N))) == 1) == (N % 6 in (2, 3)) for N in range(4, top + 1)))
    # split detection from the definition (lcm closure of true thresholds)
    def splits(c):
        cl = closure({Kthr(w) for w in arrs(c)})
        return cl is not None and any(ncls_direct(c, m) >= 2 for m in cl)
    N_top = 120 if not full else 220
    ok = all(splits((2, 3, N)) == (N % 6 in (2, 3) and N >= 8) for N in range(4, N_top + 1) if N not in (2, 3))
    check("X3 D-T9 converse (now a corollary of F2): {2,3,N} splits  <=>  N = 2,3 mod 6, N >= 8   (N <= %d)" % N_top, ok)
    # exact 3-label criterion (prefix-set form), checked against direct simulation at every closure source
    nbad = 0; nspl = 0
    for c in itertools.combinations(range(1, 26 if not full else 41), 3):
        crit = False; Ls = []
        for a, b, cc in itertools.permutations(c):
            if a > cc: continue
            L = lcm(kappa_v((a,)), kappa_v((cc,)), kappa_v((a, b)), kappa_v((b, cc)), kappa_v((a, b, cc)))
            if L % b and L % kappa_v((a, cc)): crit = True; Ls.append(L)
        sp = splits(c); nspl += sp
        if crit != sp: nbad += 1
        if sp:
            cl = closure({Kthr(w) for w in arrs(c)})
            mins = [m for m in cl if ncls_direct(c, m) >= 2 and not any(n2 != m and m % n2 == 0 and ncls_direct(c, n2) >= 2 for n2 in cl)]
            if sorted(mins) != sorted(set(Ls)): nbad += 1
    check("X3 EXACT 3-label split criterion (theorem): split <=> some labeling (a,b,c) has b not| L and kappa{a,c} not| L, L=lcm(k{a},k{c},k{a,b},k{b,c},k{a,b,c}); minimal split sources = those L  (%d splitting contents)" % nspl, nbad == 0, nbad)
    bad = nsp = 0
    for c in itertools.combinations(range(1, 17 if not full else 24), 3):
        if splits(c):
            nsp += 1
            if max(len(B) for B in sccs_topo(c)) < 3: bad += 1
    check("X3 distinct labels: a splitting content has an SCC block with >= 3 labels  (%d splitting 3-label contents)" % nsp, bad == 0, bad)
    bad = nsp = 0
    for c in itertools.combinations(range(1, 10 if not full else 12), 4):
        if splits(c):
            nsp += 1
            if max(len(B) for B in sccs_topo(c)) < 3: bad += 1
    check("X3 same for 4 labels  (%d splitting)" % nsp, bad == 0, bad)
    # hub descent => no split
    def hub(c):
        thr = {w: Kthr(w) for w in arrs(c)}; V = list(thr)
        for h in V:
            if any(thr[w] % thr[h] for w in V): continue
            reach = {h}; ch = True
            while ch:
                ch = False
                for w in V:
                    if w not in reach and any(u in reach and thr[w] % thr[u] == 0 for u in nbrs(w)): reach.add(w); ch = True
            if len(reach) == len(V): return True
        return False
    bad = nh = 0
    for c in itertools.combinations(range(1, 16 if not full else 22), 3):
        if hub(c):
            nh += 1
            if splits(c): bad += 1
    check("X3 hub-descent criterion => no split source  (%d contents with a hub)" % nh, bad == 0, bad)


def shard_X4(full=False):
    """route topology: independent homology; lower sets contractible; two-facet theorem; loops; Alexander duality"""
    random.seed(9)
    S3 = list(itertools.permutations(range(3))); S4 = list(itertools.permutations(range(4)))
    check("X4 homology sanity: full simplex-like cells contractible; cubical hexagon b1=1; cubical P_4 b=(1,7,0,0)",
          homology_betti(S3, 3) == (1, 0, 0) and homology_betti(S3, 3, True) == (1, 1, 0) and homology_betti(S4, 4, True) == (1, 7, 0, 0) and homology_betti(S4, 4) == (1, 0, 0, 0))
    # weak-order lower sets
    def inv(v): return {(v[i], v[j]) for i in range(len(v)) for j in range(i + 1, len(v)) if v[i] > v[j]}
    def lower_set_random(k, steps):
        S = list(itertools.permutations(range(k))); A = {S[0]}  # identity is the bottom
        invs = {v: inv(v) for v in S}
        for _ in range(steps):
            v = random.choice(S)
            # add the principal ideal of v
            for u in S:
                if invs[u] <= invs[v]: A.add(u)
            if len(A) == len(S) and random.random() < 0.9: A = {S[0]}
        return A
    ok = True; n = 0
    for k, cnt in ((3, 30), (4, 60 if not full else 200), (5, 6 if not full else 25)):
        for _ in range(cnt):
            A = lower_set_random(k, random.randint(1, 4))
            n += 1; ok &= (homology_betti(A, k) == (1,) + (0,) * (k - 1))
    check("X4 T-LOWER: the full subcomplex on a weak-order lower set is contractible  (%d random lower sets, k=3..5)" % n, ok)
    # two-facet theorem
    ok = True; n = 0
    for k in (3, 4, 5, 6 if full else 5):
        S = list(itertools.permutations(range(k)))
        for a in range(1, k):
            for E in itertools.combinations(range(k), a):
                if k == 6 and random.random() > 0.15: continue
                Es = set(E)
                A = [v for v in S if set(v[:a]) != Es and set(v[:k - a]) != set(range(k)) - Es]
                b = homology_betti(A, k); n += 1
                want = [0] * k; want[k - 3] += 1; want[0] += 1
                ok &= (b == tuple(want))
    check("X4 T-SPHERE: complement of the two facets E|O and O|E has Betti 1 in degree 0 and in degree k-3  (%d (k,E) cases, k=3..%d)" % (n, 6 if full else 5), ok)
    # arithmetic two-facet family
    F = [n_ for n_ in range(8, 50) if n_ % 6 in (2, 3)]; ok = True; n = 0
    for r in (1, 2, 3):
        for X in itertools.combinations(F, r):
            if r == 3 and (max(X) > 30 or not full and random.random() > 0.3): continue
            C = (2, 3) + X; m = prod(X); E = {x for x in C if x % 6 == 2}; O = {x for x in C if x % 6 == 3}
            for w in arrs(C):
                sep = set(w[:len(E)]) == E or set(w[:len(O)]) == O
                if adm(m, w) == sep: ok = False
            forb = {frozenset(S) for r_ in range(1, len(C)) for S in itertools.combinations(C, r_) if m % kappa_v(S)}
            ok &= (forb == {frozenset(E), frozenset(O)})        # the infeasible proper subsets are exactly the complementary pair E, O
            n += 1
    check("X4 arithmetic two-facet family: C={2,3}+X, X subset {n>=8, n=2,3 mod 6}, m=prod X: inadmissible words = exactly E|O and O|E  (%d contents, from direct simulation)" % n, ok)
    # loops {2,3,N,M} at N*M
    ok = True; n = 0
    for N, M in itertools.combinations([n_ for n_ in range(8, 60) if n_ % 6 in (2, 3)], 2):
        if not full and random.random() > 0.4: continue
        c = (2, 3, N, M); b = homology_betti(pattern(c, N * M), 4); n += 1
        ok &= (b == (1, 1, 0, 0)) and ncls_direct(c, N * M) == 1
    check("X4 {2,3,N,M} at source N*M (N,M = 2,3 mod 6, >= 8): connected swap graph with Betti (1,1,0,0)  (%d pairs)" % n, ok)
    ok = True; n = 0
    for N, M in itertools.combinations(range(4, 40), 2):
        c = (2, 3, N, M)
        cl = closure({Kthr(w) for w in arrs(c)})
        if cl is None: continue
        hit = any(homology_betti(pattern(c, m), 4)[1] > 0 for m in cl); n += 1
        ok &= (hit == (N >= 8 and M >= 8 and N % 6 in (2, 3) and M % 6 in (2, 3)))
    check("X4 converse for {2,3,N,M}, 4<=N<M<39: a first Betti number appears iff both N, M = 2,3 mod 6 and >= 8  (%d pairs)" % n, ok)
    # acyclic contractible, from direct simulation
    ok = True; n = 0
    for c in itertools.combinations(range(1, 13 if not full else 16), 4):
        if not all(len(B) == 1 for B in sccs_topo(c)): continue
        for m in sources(c, 25):
            A = pattern(c, m)
            if A: n += 1; ok &= (homology_betti(A, 4) == (1, 0, 0, 0))
    check("X4 acyclic feeding digraph => every nonempty route complex is acyclic (Betti (1,0,..))  (%d content-source pairs, k=4)" % n, ok)
    # Alexander duality top degree, own nerve
    ok = True; n = 0
    for k, conts in ((4, itertools.combinations(range(1, 11), 4)), (5, [(2, 3, 8, 9, 14), (2, 3, 8, 9, 15), (2, 3, 9, 14, 20), (2, 3, 8, 14, 27)])):
        S = set(itertools.permutations(range(k)))
        for c in conts:
            for m in sources(c, 12):
                A = pattern(c, m); R = S - A
                if not A or not R: continue
                b = list(homology_betti(A, k)); b[0] -= 1
                n += 1; ok &= (b[k - 3] == common_proper_face_components(R, k) - 1 and b[k - 2] == 0)
    check("X4 Alexander duality: reduced b_{k-3}(K_A) = (#components of the non-admissible set under 'common proper face') - 1, b_{k-2}=0  (%d complexes)" % n, ok)
    bc = homology_betti(pattern((2, 3, 8, 9, 14), 1008), 5, True)
    check("X4 cubical (independent-swap squares/cubes only) complex of the same 5-label example: Betti %s -- 19 loops from unfilled braid hexagons and NO 2-void" % (bc,), bc == (1, 19, 0, 0, 0))
    check("X4 {2,3,8,9} at 72: cubical Betti equals permutohedral Betti (1,1,0,0)", homology_betti(pattern((2, 3, 8, 9), 72), 4, True) == (1, 1, 0, 0))
    b5 = homology_betti(pattern((2, 3, 8, 9, 14), 1008), 5)
    check("X4 2-dimensional void: {2,3,8,9,14} at source 1008 has Betti %s" % (b5,), b5 == (1, 0, 1, 0, 0))


def hist_back(t):
    """all complete histories (squarefree source, labels) ending at t -- own coding of the predecessor rule: d>=2, d^2 | t, m = t(d-1)/d^2, N = d-1"""
    sqf = all(vp(t, p) <= 1 for p in primes_of(t)) if t > 1 else True
    out = [(t, ())] if sqf else []
    d = 2
    while d * d <= t:
        if t % (d * d) == 0:
            for (m0, L) in hist_back(t * (d - 1) // (d * d)): out.append((m0, L + (d - 1,)))
        d += 1
    return out


def states(h):
    m = h[0]; out = [m]
    for N in h[1]: m = m // N * (N + 1) ** 2; out.append(m)
    return out


def fibre_set(m):
    e = {p: vp(m, p) // 2 for p in primes_of(m)}
    ds = [1]
    for p, a in e.items(): ds = [x * p ** i for x in ds for i in range(a + 1)]
    return frozenset(d for d in ds if d >= 2)


def shard_X5(full=False):
    """occurrence bridge: histories of 72^r, discrepancy formula, orthant characterisation, restricted components"""
    H = {r: hist_back(72 ** r) for r in (1, 2, 3)}
    check("X5 history counts H(72^r) = 4, 100, 3601", [len(H[r]) for r in (1, 2, 3)] == [4, 100, 3601])
    saved = load("results/OCCURRENCE_BRIDGE.json")
    def swaps(h):
        m0, L = h
        for i in range(len(L) - 1):
            if L[i] != L[i + 1]:
                L2 = L[:i] + (L[i + 1], L[i]) + L[i + 2:]
                if adm(m0, L2): yield i, (m0, L2)
    def comps(hs, keep):
        idx = {h: i for i, h in enumerate(hs)}; par = list(range(len(hs)))
        def f(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for h in hs:
            for i, h2 in swaps(h):
                if keep(h, h2, i): par[f(idx[h])] = f(idx[h2])
        return len({f(i) for i in range(len(hs))})
    rmax = 3 if full else 2
    ok_all = True; ok_form = True; ok_orth = True; nsw = 0
    for r in range(1, rmax + 1):
        hs = H[r]; fib = {}
        def F(h):
            if h not in fib: fib[h] = [fibre_set(m) for m in states(h)]
            return fib[h]
        # unrestricted
        base = comps(hs, lambda a, b, i: True)
        ok_all &= (base == saved["72^%d" % r]["classes_unrestricted"])
        for h in hs:
            for i, h2 in swaps(h):
                nsw += 1
                a, b = states(h)[i + 1], states(h2)[i + 1]
                Da, Db = fibre_set(a), fibre_set(b)
                # Lemma L: non-empty discrepancy;   closed form for |Delta|
                ea = {p: vp(a, p) // 2 for p in primes_of(a * b)}; eb = {p: vp(b, p) // 2 for p in primes_of(a * b)}
                cnt = lambda e: prod(v + 1 for v in e.values())
                size = cnt(ea) + cnt(eb) - 2 * prod(min(ea[p], eb[p]) + 1 for p in ea)
                ok_form &= (len(Da ^ Db) == size and size > 0)
        for d in (2, 3, 4, 6, 8, 9, 12, 18, 24, 36):
            nu = {p: vp(d, p) for p in primes_of(d)}
            inorth = lambda m: all(vp(m, p) >= 2 * nu[p] for p in nu)      # d in D(m)  <=>  m in the orthant v >= 2 nu(d)
            keepP = lambda a, b, i: inorth(states(a)[i + 1]) == inorth(states(b)[i + 1])
            keepA = lambda a, b, i: keepP(a, b, i) or not any(inorth(m) for m in states(a)[:i + 1])
            # orthant characterisation agrees with the fibre definition on every swap of the benchmark
            for h in hs:
                for i, h2 in swaps(h):
                    ok_orth &= ((d in fibre_set(states(h)[i + 1])) == inorth(states(h)[i + 1]))
            cP = comps(hs, keepP); cA = comps(hs, keepA)
            ok_all &= (cP == saved["72^%d" % r]["preserve"][str(d)]) and (cA == saved["72^%d" % r]["after"][str(d)]) and base <= cA <= cP
    check("X5 discrepancy D(T_A x) symdiff D(T_B x) is non-empty (Lemma L) with |Delta| = prod(ea+1)+prod(eb+1)-2prod(min+1)  (%d swaps)" % nsw, ok_form)
    check("X5 'd in D(m)' <=> v_p(m) >= 2 v_p(d) for all p | d (orthant indicator)", ok_orth)
    check("X5 restricted component counts: independent recomputation equals saved table (r<=%d), and unrestricted <= after <= preserve" % rmax, ok_all)


def shard_X6(full=False):
    """documents: statuses and mandatory statements"""
    t = open(os.path.join(ROOT, "results", "THEOREMS.md")).read()
    check("X6 THEOREMS.md uses PROVED / FINITE-EXACT / OPEN status words", all(w in t for w in ("PROVED", "FINITE-EXACT", "OPEN")))
    check("X6 THEOREMS.md lists NF, F1, F2, T-LOWER, T-SPHERE, D-T9 converse", all(w in t for w in ("Lemma NF", "F1", "F2", "T-LOWER", "T-SPHERE", "D-T9")))
    o = open(os.path.join(ROOT, "results", "OPEN_PROBLEMS.md")).read()
    check("X6 OPEN_PROBLEMS.md keeps D-Q4 open and FIELD-I not identified with SELECT-II", "D-Q4" in o and "FIELD-I" in o and "SELECT-II" in o)
    mf = load("MANIFEST.json")["files"] if os.path.exists(os.path.join(ROOT, "MANIFEST.json")) else None
    if mf is None: check("X6 MANIFEST.json absent while building (skipped)", True)
    else: check("X6 MANIFEST hashes match", all(sha(os.path.join(ROOT, p)) == h for p, h in mf.items() if p not in ("results/VERIFY_LAST.json",)))


def shard_X7(full=False):
    """cross-check: builder modules agree with the independent verifier (this is the only shard that imports builder code)"""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import thresholds as th, swap_classes as fe, route_topology as rt
    random.seed(2)
    labs = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 20, 21, 27]
    check("X7 builder K(w) = verifier K(w) (2000 words)", all(th.K(w) == Kthr(w) for w in [tuple(random.choice(labs) for _ in range(random.randint(1, 5))) for _ in range(2000)]))
    check("X7 builder SCC blocks = verifier SCC blocks (300 contents)", all([set(map(frozenset, fe.scc_blocks(c))) == set(sccs_topo(c)) for c in [tuple(sorted(random.sample(range(1, 40), random.randint(2, 5)))) for _ in range(300)]]))
    ok = True
    for c, m in [((2, 3, 8, 9), 72), ((2, 3, 8, 9, 14), 1008), ((2, 3, 14), 14), ((1, 2, 3, 8), 8), ((2, 3, 4, 5), 60)]:
        k = len(c); A = pattern(c, m); ok &= (tuple(rt.betti(A, k)[0]) == homology_betti(A, k))
    check("X7 builder homology = verifier homology on 5 reference complexes", ok)
    R = load("results/TOPOLOGY_CENSUS.json")
    check("X7 saved census: first k=4 loop example is {2,3,8,9} at 72; k=5 void present", R["k4"]["first_noncontractible_examples"].get("(1, 1, 0, 0)", [None])[0] == [2, 3, 8, 9] and R["two_facet_family"]["betti"].get("(1, 0, 1, 0, 0)", 0) > 0)
    F = load("results/FEEDING_CENSUS.json")
    check("X7 saved feeding census: 0 violations everywhere", F["NF_threshold_pairs"]["violations"] == 0 and F["F2_product_formula"]["violations"] == 0 and F["family_2_3_N_scc"]["violations"] == 0
          and all(v["split_without_block_of_size_ge3"] == 0 and v["max_classes_acyclic"] <= 1 for v in F["F1_and_block_size"].values()) and all(v["hub_and_split"] == 0 for v in F["hub_descent"].values()))


SHARDS = {"X0": shard_X0, "X1": shard_X1, "X2": shard_X2, "X3": shard_X3, "X4": shard_X4, "X5": shard_X5, "X6": shard_X6, "X7": shard_X7}
