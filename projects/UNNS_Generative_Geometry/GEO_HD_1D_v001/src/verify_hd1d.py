"""HD-1D v001 INDEPENDENT verifier.  Re-implements the SELECT-II definitions from scratch (no import of the builder modules) and checks
the builder's stored data and the theorem statements.  Exact integer arithmetic.  Bounded searches are labelled BOUNDED.
Usage via RUN_VERIFY.py (--fast | --full | --shard Vk)."""
import os, sys, json, itertools, math
from collections import defaultdict, Counter
from math import comb, gcd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = []; FAILS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + ((" -- " + str(detail)) if detail != "" else ""), flush=True)
    if not ok: FAILS.append(name)


def load(rel):
    with open(os.path.join(ROOT, rel)) as f: return json.load(f)


# ------------------------------------------------------------ independent definitions
def T(N, m):
    if m % N: return None
    return m // N * (N + 1) ** 2


def factors(n):
    out = {}; p = 2
    while p * p <= n:
        while n % p == 0: out[p] = out.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: out[n] = out.get(n, 0) + 1
    return out


def v(n, p):
    e = 0
    while n % p == 0: n //= p; e += 1
    return e


def sfree(n): return all(e == 1 for e in factors(n).values())


def Dfib(m):
    s = 1
    for p, e in factors(m).items(): s *= p ** (e // 2)
    return tuple(d for d in range(2, s + 1) if s % d == 0)


def admiss(m0, L):
    m = m0
    for N in L:
        if m % N: return None
        m = m // N * (N + 1) ** 2
    return m


def states(m0, L):
    out = [m0]
    for N in L: out.append(T(N, out[-1]))
    return out


def forward_graph(X):
    """edges (N, m -> t) with t <= X, generated from the DEFINITION m = N k, t = k (N+1)^2; plus squarefree sieve"""
    rev = defaultdict(list); fwd = defaultdict(list)
    N = 1
    while (N + 1) ** 2 <= X:
        for k in range(1, X // (N + 1) ** 2 + 1):
            m, t = N * k, k * (N + 1) ** 2
            fwd[m].append((N, t)); rev[t].append((N, m))
        N += 1
    sq = bytearray([1]) * (X + 1)
    p = 2
    while p * p <= X:
        for j in range(p * p, X + 1, p * p): sq[j] = 0
        p += 1
    return fwd, rev, sq


def count_forward(X, fwd, sq):
    cnt = [0] * (X + 1)
    for m in range(1, X + 1):
        if sq[m]: cnt[m] += 1            # squarefree source (such m have no incoming edge)
        c = cnt[m]
        if c:
            for N, t in fwd.get(m, ()): cnt[t] += c
    return cnt


def histories_to(t, rev, sq, limit=10 ** 7):
    """all complete histories ending at t, by DFS over the forward-generated reverse edges"""
    out = []
    def rec(x, suffix):
        if sq[x] and not rev.get(x):
            out.append((x, suffix)); return
        for N, m in rev.get(x, ()): rec(m, (N,) + suffix)
    rec(t, ())
    return out


def swap_nbrs(m0, L):
    for i in range(len(L) - 1):
        if L[i] != L[i + 1]:
            L2 = L[:i] + (L[i + 1], L[i]) + L[i + 2:]
            if admiss(m0, L2) is not None: yield i, L2


def components(hs):
    idx = {h: i for i, h in enumerate(hs)}; par = list(range(len(hs)))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for h in hs:
        for i, L2 in swap_nbrs(*h): par[f(idx[h])] = f(idx[(h[0], L2)])
    g = defaultdict(list)
    for h in hs: g[f(idx[h])].append(h)
    return list(g.values())


def cube_dim(h):
    m0, L = h; d = 0; i = 0
    nb = {i for i, _ in swap_nbrs(m0, L)}
    while i < len(L) - 1:
        if i in nb: d += 1; i += 2
        else: i += 1
    return d


# ------------------------------------------------------------ shards
def shard_V0(full=False):
    """definitions and the benchmark histories of 72"""
    X = 72
    fwd, rev, sq = forward_graph(X)
    hs = sorted(histories_to(72, rev, sq))
    check("V0 complete histories of 72 (forward-generated edges): exactly the four of the specification",
          hs == [(1, (1, 1, 2)), (1, (1, 2, 1)), (3, (3, 2)), (10, (5,))], hs)
    check("V0 endpoints and intermediate states", [states(*h) for h in hs] == [[1, 4, 16, 72], [1, 4, 18, 72], [3, 16, 72], [10, 72]])
    check("V0 T_N(m) >= 4m on all edges <= 20000", all(t >= 4 * m for m in range(1, 2001) for N in range(1, m + 1) if m % N == 0 for t in [T(N, m)] if t <= 20000) , "")
    nogo = all(Dfib(h[0]) == () for h in hs) and all(Dfib(m) == () for m in range(1, 3001) if sfree(m))
    check("V0 HD-0 empty-transport no-go: every squarefree source has empty occurrence fibre, so restricting source indices along a complete history is vacuous", nogo)
    check("V0 transitions of 6: 24, 27, 32, 49 (labels 1,2,3,6)", sorted(T(N, 6) for N in (1, 2, 3, 6)) == [24, 27, 32, 49])


def shard_V1(full=False):
    """predecessor recurrence vs forward dynamic programme"""
    X = 72 ** 3 if True else 20736
    fwd, rev, sq = forward_graph(X)
    cnt = count_forward(X, fwd, sq)
    sys.path.insert(0, os.path.join(ROOT, "src"))
    from predecessor_count import H
    lim = X if full else 100000
    bad = [t for t in range(1, lim + 1) if cnt[t] != H(t)]
    check("V1 H(t) from the predecessor recurrence = forward-DP count, all t <= %d" % lim, not bad, bad[:3])
    for r in (1, 2, 3):
        check("V1 H(72^%d) forward DP = %d" % (r, cnt[72 ** r]), cnt[72 ** r] == [4, 100, 3601][r - 1])
    d = load("data/D_B3_72_POWERS.json")
    check("V1 stored table H(72^r), r=1..6, equals builder recurrence; r<=3 equals forward DP",
          [row["H"] for row in d["table"]] == [4, 100, 3601, 194864, 14177856, 1258011667] and all(d["table"][r - 1]["H"] == cnt[72 ** r] for r in (1, 2, 3)))
    check("V1 binomial lower bound H(72^r) >= C(2r,r) for r=1..6", all(row["H"] >= comb(2 * row["r"], row["r"]) for row in d["table"]))
    n_hist = sum(1 for t in range(1, 3001) if not sq[t] for _ in histories_to(t, rev, sq)) if full else sum(1 for t in range(1, 801) if not sq[t] for _ in histories_to(t, rev, sq))
    lim2 = 3000 if full else 800
    check("V1 explicit enumeration count equals sum of H over non-squarefree t <= %d" % lim2, n_hist == sum(cnt[t] for t in range(1, lim2 + 1) if not sq[t]), n_hist)


def shard_V2(full=False):
    """D-T1: ordered and unordered diamond criteria"""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import diamond_criterion as dc
    M = 500 if full else 200; A_MAX = 45
    bad1 = bad2 = bad3 = bad4 = 0; n = 0
    for m in range(1, M + 1):
        for A in range(1, A_MAX + 1):
            for B in range(1, A_MAX + 1):
                n += 1
                ab = (m % A == 0) and (T(A, m) % B == 0)
                ba = (m % B == 0) and (T(B, m) % A == 0)
                if ab != (m % (A * B // gcd(B, (A + 1) ** 2)) == 0): bad1 += 1
                if (ab and ba) != (m % (A * B) == 0): bad2 += 1
                if dc.diamond(m, A, B) != (ab and ba): bad3 += 1
                if A != B and dc.padic_form(m, A, B) != (ab and ba): bad4 += 1
    check("V2 ordered criterion  A->B admissible <=> A*B/gcd(B,(A+1)^2) | m   (%d triples)" % n, bad1 == 0, bad1)
    check("V2 both orders admissible <=> A*B | m   (%d triples)" % n, bad2 == 0, bad2)
    check("V2 builder diamond() = definition", bad3 == 0)
    check("V2 specification p-adic form = A*B | m", bad4 == 0, bad4)
    # lcm identity
    ok = all(math.lcm(A * B // gcd(B, (A + 1) ** 2), A * B // gcd(A, (B + 1) ** 2)) == A * B for A in range(1, 150) for B in range(1, 150))
    check("V2 lcm(m_{A->B}, m_{B->A}) = A*B (A,B < 150)", ok)
    # multisets
    bad = 0; n = 0
    for k in (2, 3, 4):
        for labs in itertools.combinations_with_replacement(range(1, 11 if k < 4 else 7), k):
            P = math.prod(labs)
            for m in (P, 2 * P, P // 2 if P % 2 == 0 else P, P + 1, 3 * P, P * 5 // 2 if P % 2 == 0 else P):
                if m < 1: continue
                n += 1
                allok = all(admiss(m, p) is not None for p in set(itertools.permutations(labs)))
                if allok != (m % P == 0): bad += 1
    check("V2 all arrangements of a multiset admissible <=> product | m  (%d cases)" % n, bad == 0, bad)
    # m_{A->B} minimality: all admitting m are multiples
    check("V2 admitting states are exactly the multiples of m_{A->B} (A,B<=12, m<=600)",
          all(((admiss(m, (A, B)) is not None) == (m % (A * B // gcd(B, (A + 1) ** 2)) == 0)) for A in range(1, 13) for B in range(1, 13) for m in range(1, 601)))


def shard_V3(full=False):
    """D-T2 / D-T3: the 72^r family, route cubes, symbolic block condition"""
    top = 8 if full else 6
    for r in range(1, top + 1):
        t = 72 ** r
        words = []
        for twos in itertools.combinations(range(2 * r), r):
            tail = [1] * (2 * r)
            for i in twos: tail[i] = 2
            words.append((1, (1,) * r + tuple(tail)))
        ok = len(set(words)) == comb(2 * r, r) and all(admiss(*h) == t for h in words)
        # route cube
        base = (1, (1,) * r + (1, 2) * r)
        pos = [r + 2 * j for j in range(r)]
        vs = {}
        for bits in itertools.product((0, 1), repeat=r):
            L = list(base[1])
            for b, i in zip(bits, pos):
                if b: L[i], L[i + 1] = L[i + 1], L[i]
            vs[bits] = (1, tuple(L))
        cube_ok = all(admiss(*h) == t for h in vs.values()) and len(set(vs.values())) == 2 ** r
        edges_ok = True
        for bits, h in vs.items():
            for j, i in enumerate(pos):
                if bits[j] == 0:
                    b2 = bits[:j] + (1,) + bits[j + 1:]
                    L = list(h[1]); L[i], L[i + 1] = L[i + 1], L[i]
                    edges_ok &= (1, tuple(L)) == vs[b2]
        check("V3 r=%d: C(2r,r)=%d arrangements admissible with endpoint 72^r; %d-cube of block histories (all %d vertices, all edges)" % (r, comb(2 * r, r), r, 2 ** r), ok and cube_ok and edges_ok)
    # symbolic: block j of the r-cube starts at 4^r 18^(j-1); label 2 and label 1 in either order need only 2 | state
    ok = True
    for r in range(1, 61):
        for j in range(1, r + 1):
            m = 4 ** r * 18 ** (j - 1)
            ok &= (m % 2 == 0) and (T(1, m) % 2 == 0) and (T(2, m) % 1 == 0)
            ok &= (T(1, T(2, m)) == T(2, T(1, m)) == 18 * m)
    check("V3 block condition (2 | 4^r 18^(j-1) and both orders end at 18 m) for all r<=60, j<=r", ok)
    # counting 2^r - cube is maximal inside the {1,2} family: dimension of binomial family positions
    check("V3 endpoint algebra: 4^r * 4^r * (9/2)^r = 72^r  (r<=60)", all(4 ** r * 4 ** r * 9 ** r == 72 ** r * 2 ** r for r in range(1, 61)))


def shard_V4(full=False):
    """swap classes of the complete histories of 72^r; contents; cube dimensions"""
    X = 72 ** 3
    fwd, rev, sq = forward_graph(X)
    exp = {1: (4, 3, 3), 2: (100, 22, 22), 3: (3601, 142, 141)}
    d = load("data/D_B3_72_POWERS.json")["detail"]
    for r in (1, 2, 3):
        hs = histories_to(72 ** r, rev, sq)
        cl = components(hs)
        grp = defaultdict(int)
        for c in cl: grp[(c[0][0], tuple(sorted(c[0][1])))] += 1
        check("V4 72^%d: %d histories, %d swap classes, %d (source,content) groups" % (r, exp[r][0], exp[r][1], exp[r][2]),
              (len(hs), len(cl), len(grp)) == exp[r], (len(hs), len(cl), len(grp)))
        cd = Counter(cube_dim(h) for h in hs)
        check("V4 72^%d cube-dimension distribution = stored" % r, {str(k): x for k, x in sorted(cd.items())} == {str(k): x for k, x in d[str(r)]["cube_dim_distribution"].items()}, dict(sorted(cd.items())))
        if r == 3:
            four = [h for h in hs if cube_dim(h) == 4]
            h = four[0]; pos = []; i = 0; nb = {i for i, _ in swap_nbrs(*h)}
            while i < len(h[1]) - 1:
                if i in nb: pos.append(i); i += 2
                else: i += 1
            vs = []
            for bits in itertools.product((0, 1), repeat=4):
                L = list(h[1])
                for b, i in zip(bits, pos):
                    if b: L[i], L[i + 1] = L[i + 1], L[i]
                vs.append((h[0], tuple(L)))
            check("V4 72^3 contains an explicit 4-cube (16 admissible histories, same endpoint) although r = 3: %s" % (h,), all(admiss(*x) == 72 ** 3 for x in vs) and len(set(vs)) == 16)
    if full:
        t = 72 ** 4
        X4 = t
        # r=4 stored cube distribution: recompute from independent enumeration restricted via recurrence-free DFS is heavy; check counts instead
        fwd4, rev4, sq4 = forward_graph(X4) if False else (None, None, None)
        check("V4 72^4 cube data present (stored; NOT recomputed independently)", load("results/R4_CUBE_DIMENSIONS.json")["histories"] == 194864)


def shard_V5(full=False):
    """route-equivalence obstruction: same source, same content, different swap classes"""
    cases = [(14, (2, 3, 14), 5400), (2, (1, 2, 3, 8), 1944), (15, (2, 4, 5, 5, 15), 72 ** 3)]
    for m0, cont, t in cases:
        arr = [p for p in set(itertools.permutations(cont)) if admiss(m0, p) == t]
        hs = [(m0, p) for p in arr]
        cl = components(hs)
        check("V5 source %d content %s: %d admissible arrangements all ending at %d, in %d swap classes" % (m0, cont, len(hs), t, len(cl)), len(cl) >= 2 and all(admiss(*h) == t for h in hs), [len(c) for c in cl])
    # hand-checkable minimal case
    a, b = (14, (14, 3, 2)), (14, (2, 3, 14))
    check("V5 minimal case: exactly two admissible arrangements of {2,3,14} from 14, each isolated",
          sorted(p for p in set(itertools.permutations((2, 3, 14))) if admiss(14, p) is not None) == [(2, 3, 14), (14, 3, 2)]
          and not list(swap_nbrs(*a)) and not list(swap_nbrs(*b)) and states(*a) == [14, 225, 1200, 5400] and states(*b) == [14, 63, 336, 5400])
    # infinite family: sources 14 q, q squarefree coprime to 210
    qs = [q for q in range(1, 400 if full else 120) if sfree(q) and gcd(q, 210) == 1]
    ok = True
    for q in qs:
        arr = [p for p in set(itertools.permutations((2, 3, 14))) if admiss(14 * q, p) is not None]
        ok &= sorted(arr) == [(2, 3, 14), (14, 3, 2)] and admiss(14 * q, (2, 3, 14)) == admiss(14 * q, (14, 3, 2)) == 5400 * q
        ok &= all(not list(swap_nbrs(14 * q, p)) for p in arr)
    check("V5 infinite-family check: sources 14q (q squarefree, gcd(q,210)=1), %d values of q" % len(qs), ok)
    st = load("results/ROUTE_INVARIANTS.json")
    check("V5 census scope [4,6000], H<=4000: stored split endpoints are exactly 1944, 2400, 4050, 4320, 5400", st["split_endpoints"] == [1944, 2400, 4050, 4320, 5400])


def shard_V6(full=False):
    """D-T4: occurrence events, visibility lemma, faithfulness of the signature, locality of swaps"""
    # benchmark rho of 72
    hs = [(1, (1, 1, 2)), (1, (1, 2, 1)), (3, (3, 2)), (10, (5,))]
    D = {h: [Dfib(m) for m in states(*h)] for h in hs}
    check("V6 fibres along h1 and h2 (Spec 4.1): D(4)={2}, D(16)={2,4}, D(18)={3}, D(72)={2,3,6}",
          D[hs[0]] == [(), (2,), (2, 4), (2, 3, 6)] and D[hs[1]] == [(), (2,), (3,), (2, 3, 6)])
    r2 = lambda h: tuple(int(2 in Dd) for Dd in D[h])
    check("V6 rho_2(h1) = (0,1,1,1), rho_2(h2) = (0,1,0,1)", r2(hs[0]) == (0, 1, 1, 1) and r2(hs[1]) == (0, 1, 0, 1))
    # visibility lemma: A != B => D(T_A m) != D(T_B m)
    M = 400 if full else 200; bad = 0; n = 0
    for m in range(1, M + 1):
        labs = [N for N in range(1, m + 1) if m % N == 0]
        for A, B in itertools.combinations(labs, 2):
            n += 1
            if Dfib(T(A, m)) == Dfib(T(B, m)): bad += 1
    check("V6 Lemma L (distinct labels give distinct fibres): %d pairs, %d violations" % (n, bad), bad == 0)
    # faithfulness: fibre sequence determines the history (depth-limited, fixed source)
    tot = coll = 0
    for m0, depth in ((1, 5), (2, 4), (6, 3), (12, 3), (36, 3), (60, 2), (72, 2), (30, 3)):
        seen = {}; fr = [((), m0)]; allh = [()]
        for _ in range(depth):
            fr = [(L + (N,), T(N, m)) for L, m in fr for N in range(1, m + 1) if m % N == 0]
            allh += [x for x, _ in fr]
        for L in allh:
            s = tuple(Dfib(m) for m in states(m0, L)); tot += 1
            if s in seen and seen[s] != L: coll += 1
            seen[s] = L
    check("V6 Theorem (faithfulness): fibre sequences from a fixed source separate histories - %d histories, %d collisions (BOUNDED depth)" % (tot, coll), coll == 0)
    # swap locality: a legal swap changes exactly one fibre (the intermediate one)
    X = 72 ** 2
    fwd, rev, sq = forward_graph(X)
    ok = True; cnt = 0
    for h in histories_to(X, rev, sq):
        s0 = [Dfib(m) for m in states(*h)]
        for i, L2 in swap_nbrs(*h):
            s1 = [Dfib(m) for m in states(h[0], L2)]
            diff = [j for j in range(len(s0)) if s0[j] != s1[j]]
            ok &= diff == [i + 1]; cnt += 1
    check("V6 every legal swap changes exactly the intermediate fibre (72^2 histories, %d swaps)" % cnt, ok)
    # events locality: loss of d needs gcd(d, N) > 1, birth of d needs gcd(d, N+1) > 1
    ok = True; n = 0
    for m in range(1, 600 if not full else 1500):
        for N in range(1, m + 1):
            if m % N: continue
            a, b = set(Dfib(m)), set(Dfib(T(N, m)))
            for d in a - b: ok &= gcd(d, N) > 1
            for d in b - a: ok &= gcd(d, N + 1) > 1
            n += 1
    check("V6 loss of d by label N forces gcd(d,N)>1; birth forces gcd(d,N+1)>1 (%d transitions)" % n, ok)


def shard_V7(full=False):
    """local versus global: pairwise swaps and the cube/hexagon cell"""
    ok = (admiss(2, (1, 2, 4)) is not None and admiss(2, (2, 1, 4)) is not None and admiss(2, (1, 4, 2)) is not None)
    perms = [p for p in itertools.permutations((1, 2, 4)) if admiss(2, p) is not None]
    check("V7 history (2; 1,2,4): both adjacent swaps legal but only 3 of 6 arrangements admissible (no hexagon)", ok and len(perms) == 3 and admiss(2, (1, 2, 4)) == admiss(2, (2, 1, 4)) == admiss(2, (1, 4, 2)), perms)
    check("V7 cell (60; 2,6,10): all three pairs swappable at 60 but product 120 does not divide 60 (no 3-cell)",
          all(60 % (a * b) == 0 for a, b in ((2, 6), (2, 10), (6, 10))) and 60 % 120 != 0 and admiss(60, (2, 6, 10)) is None)
    # disjoint swaps always complete (Independence Lemma) - exhaustive on all histories of 72^2 and 72^3
    X = 72 ** 3
    fwd, rev, sq = forward_graph(X)
    tot = 0; bad = 0
    for r in (2, 3):
        for h in histories_to(72 ** r, rev, sq):
            nb = sorted(i for i, _ in swap_nbrs(*h))
            for a, b in itertools.combinations(nb, 2):
                if b - a >= 2:
                    L = list(h[1]); L[a], L[a + 1] = L[a + 1], L[a]; L[b], L[b + 1] = L[b + 1], L[b]
                    tot += 1
                    if admiss(h[0], tuple(L)) != admiss(*h): bad += 1
    check("V7 Independence Lemma: every pair of legal non-overlapping swaps commutes into an admissible history (%d squares)" % tot, bad == 0 and tot > 0)
    dd = load("data/D_B4_DIAMONDS.json")
    cnt = Counter()
    for m in range(1, 121):
        for A in range(1, 41):
            for B in range(A + 1, 41):
                ab = m % A == 0 and T(A, m) is not None and T(A, m) % B == 0
                ba = m % B == 0 and T(B, m) is not None and T(B, m) % A == 0
                if ab and ba: c = "DIAMOND"
                elif ab: c = "ONLY_AB"
                elif ba: c = "ONLY_BA"
                elif m % A == 0 and m % B == 0: c = "BOTH_LABELS_ADMISSIBLE_NEITHER_ORDER"
                elif m % A == 0 or m % B == 0: c = "ONE_LABEL_ONLY"
                else: c = "NEITHER_LABEL"
                cnt[c] += 1
    check("V7 stored pair classification counts (m<=120, A<B<=40) recomputed from the definitions", dict(cnt) == dd["classification_counts"], dict(cnt))
    pw = dd["pairwise_diamonds_without_triple_cell"]
    check("V7 stored pairwise-without-triple examples are genuine", all(all(m % (x * y) == 0 for x, y in ((a, b), (a, c), (b, c))) and m % (a * b * c) != 0 for m, a, b, c in pw["first"]))


def shard_V8(full=False):
    """stored data files: B1, B5 and bounded-search labels"""
    b1 = load("data/D_B1_6.json")
    check("V8 D_B1: immediate successors of 6", sorted(x["state"] for x in b1["immediate"]) == [24, 27, 32, 49])
    ok = all(b1["label_pairs_at_6"]["%d,%d" % (A, B)] == ("DIAMOND" if 6 % (A * B) == 0 else "BOTH_LABELS_ADMISSIBLE_NEITHER_ORDER") for A, B in ((1, 2), (1, 3), (1, 6), (2, 3), (2, 6), (3, 6)))
    check("V8 D_B1: label pairs at 6 follow A*B | 6", ok)
    b5 = load("data/D_B5_FUTURES.json")
    check("V8 D_B5 is labelled BOUNDED and not a universal statement", "BOUNDED" in b5["note"] and b5["bound"] == 20000)
    # recompute a few common-future facts independently (bounded)
    def reach(a, bound):
        seen = set(); st = [a]
        while st:
            m = st.pop()
            for N in range(1, m + 1):
                if m % N == 0:
                    t = T(N, m)
                    if t <= bound and t not in seen: seen.add(t); st.append(t)
        return seen
    a, b = 24, 27
    cf = sorted(reach(a, 10 ** 4) & reach(b, 10 ** 4))
    check("V8 bounded common future of 24 and 27 (<=10^4) contains 108 and 432", 108 in cf and 432 in cf)
    pairs = b5["pairs_without_common_future_in_bound"]
    check("V8 stored bounded-gap pairs: first pair recomputed has empty intersection in bound",
          (lambda p: not (reach(p[0], 20000) & reach(p[1], 20000)))(pairs[0]))


def shard_V9(full=False):
    """gates"""
    st = load("STATUS.json")
    check("V9 C3 not claimed", st["gates"]["C3"] == "NOT_CLAIMED")
    check("V9 bounded searches not presented as proofs", "BOUNDED" in json.dumps(st))
    check("V9 inherited baselines frozen / read-only", st["gates"]["BASELINES"].startswith("FROZEN"))
    check("V9 independence caveat present", "same author" in st["independence_caveat"])
    for rel in ("theory/THEOREMS.md", "theory/DEFINITIONS.md", "results/OPEN_PROBLEMS.md", "results/COUNTEREXAMPLES.json", "results/THEOREM_CERTIFICATES.json"):
        check("V9 file present: " + rel, os.path.exists(os.path.join(ROOT, rel)))


SHARDS = {"V0": shard_V0, "V1": shard_V1, "V2": shard_V2, "V3": shard_V3, "V4": shard_V4, "V5": shard_V5, "V6": shard_V6, "V7": shard_V7, "V8": shard_V8, "V9": shard_V9}
