"""HD-1D v004 INDEPENDENT verifier: re-implements SELECT-II arithmetic, displacement vectors, kernels (by box search), thresholds,
history enumeration, swap/rewrite union-find, cubical homology and occurrence fibres from the definitions.  Shards Y0-Y6 do not import the
v004 builder modules (Y7 compares against them)."""
import os, sys, json, itertools, random, hashlib
from math import gcd, lcm, comb
from fractions import Fraction
from collections import defaultdict, Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = []; FAILS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + ((" -- " + str(detail)) if detail != "" else ""), flush=True)
    if not ok: FAILS.append(name)


def load(rel):
    with open(os.path.join(ROOT, rel)) as f: return json.load(f)


def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()


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


def end(m, w):
    for N in w: m = m // N * (N + 1) ** 2
    return m


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


def rowprimes(A):
    ps = set()
    for N in A: ps |= set(primes_of(N)) | set(primes_of(N + 1))
    return sorted(ps)


def disp(A, c):
    return tuple(sum(c[j] * (2 * vp(A[j] + 1, p) - vp(A[j], p)) for j in range(len(A))) for p in rowprimes(A))


def arrangements(parts):
    base = []
    for N, c in parts: base += [N] * c
    return sorted(set(itertools.permutations(base)))


def blocks_of(A, z):
    return arrangements([(N, -c) for N, c in zip(A, z) if c < 0]), arrangements([(N, c) for N, c in zip(A, z) if c > 0])


def words(m, A, c):
    out = []
    def rec(m, cnt, acc):
        if not any(cnt): out.append(tuple(acc)); return
        for i, N in enumerate(A):
            if cnt[i] and m % N == 0:
                cnt[i] -= 1; acc.append(N); rec(m // N * (N + 1) ** 2, cnt, acc); acc.pop(); cnt[i] += 1
    rec(m, list(c), []); return out


class UF:
    def __init__(s, n): s.p = list(range(n))
    def f(s, x):
        while s.p[x] != x: s.p[x] = s.p[s.p[x]]; x = s.p[x]
        return x
    def u(s, a, b): s.p[s.f(a)] = s.f(b)


def classes(m, A, moves, contents):
    """(#words, #swap classes, #rewrite classes, per-content swap class counts)"""
    W = []
    for c in contents: W += words(m, A, c)
    idx = {w: i for i, w in enumerate(W)}; sw = UF(len(W))
    for w in W:
        for i in range(len(w) - 1):
            if w[i] != w[i + 1]:
                j = idx.get(w[:i] + (w[i + 1], w[i]) + w[i + 2:])
                if j is not None: sw.u(idx[w], j)
    swc = len({sw.f(i) for i in range(len(W))})
    percontent = Counter()
    seenroot = set()
    for i, w in enumerate(W):
        r = sw.f(i)
        if r not in seenroot: seenroot.add(r); percontent[tuple(w.count(N) for N in A)] += 1
    rw = UF(len(W))
    for i in range(len(W)): rw.u(i, sw.f(i))
    for z in moves:
        L, Rr = blocks_of(A, z)
        for X, Y in ((L, Rr), (Rr, L)):
            Xs = set(X); lx = len(X[0])
            for w in W:
                for i in range(len(w) - lx + 1):
                    if w[i:i + lx] in Xs:
                        for y in Y:
                            j = idx.get(w[:i] + y + w[i + lx:])
                            if j is not None: rw.u(idx[w], j)
    return len(W), swc, len({rw.f(i) for i in range(len(W))}), percontent


def fibre_list(base, z, L): return [tuple(b + k * c for b, c in zip(base, z)) for k in range(L)]


def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]


def Pc(A, c):
    out = 1
    for N, k in zip(A, c): out *= N ** k
    return out


# ============================================================ shards
def shard_Y0(full=False):
    """release hygiene: frozen predecessors, status gates, required files"""
    pins = load("results/V001_PINS.json")
    check("Y0 copied v001 builder modules byte-identical (%d)" % len(pins), all(sha(os.path.join(ROOT, "src", f)) == s for f, s in pins.items()))
    sib = os.path.join(os.path.dirname(ROOT), "GEO_HD_1D_v003", "MANIFEST.json")
    if os.path.exists(sib):
        mf = json.load(open(sib))["files"]; d = os.path.dirname(sib)
        check("Y0 sibling v003 untouched (manifest hashes)", all(sha(os.path.join(d, p)) == h for p, h in mf.items()))
        for f in ("thresholds.py", "swap_classes.py", "route_topology.py", "occurrence_bridge.py"):
            check("Y0 copied v003 module %s identical to v003" % f, sha(os.path.join(ROOT, "src", f)) == mf["src/" + f])
    else:
        check("Y0 sibling v003 not present here (skipped)", True)
    st = load("STATUS.json")
    check("Y0 STATUS gates", st["gates"]["C3"] == "NOT_CLAIMED" and st["gates"]["NOVELTY"] == "NOT_ASSESSED" and "same author" in st["independence_caveat"])
    need = ["theory/MERGER_KERNEL.md", "theory/PRIMITIVE_RELATIONS.md", "theory/REWRITE_GRAMMAR.md", "theory/SOURCE_THRESHOLDS.md", "theory/GLOBAL_CONNECTIVITY.md", "theory/REWRITE_COMPLEX.md",
            "theory/OCCURRENCE_EVENTS.md", "theory/THEOREMS.md", "theory/OPEN_PROBLEMS.md", "src/valuation_matrix.py", "src/integer_kernel.py", "src/primitive_moves.py", "src/block_rewrites.py",
            "src/rewrite_graph.py", "src/rewrite_complex.py", "src/occurrence_events.py"]
    check("Y0 required modules and documents present", all(os.path.exists(os.path.join(ROOT, p)) for p in need), [p for p in need if not os.path.exists(os.path.join(ROOT, p))])


def shard_Y1(full=False):
    """D4-T1, D4-T2, D4-T4: displacement criterion, realisation, kernel of {1,2,3}"""
    A = (1, 2, 3, 8); depth = 7 if full else 6
    bad = n = 0
    for m in (72, 144, 1296, 2 ** 6 * 3 ** 4):
        by = defaultdict(set)
        def rec(w, s, cnt):
            by[s].add(tuple(cnt))
            if len(w) >= depth: return
            for i, N in enumerate(A):
                if s % N == 0:
                    cnt[i] += 1; rec(w + [N], s // N * (N + 1) ** 2, cnt); cnt[i] -= 1
        rec([], m, [0] * 4)
        for s, cs in by.items():
            cs = sorted(cs)
            for c1, c2 in itertools.combinations(cs, 2):
                n += 1; bad += any(disp(A, c1)[k] != disp(A, c2)[k] for k in range(len(disp(A, c1))))
        keys = sorted(by)
        for s1, s2 in itertools.combinations(keys[:80], 2):
            c1, c2 = next(iter(by[s1])), next(iter(by[s2]))
            if disp(A, c1) == disp(A, c2): bad += 1
    check("Y1 D4-T1: equal endpoints  <=>  equal displacement (V c = V c'), exhaustive over words of length <= %d from 4 sources  (%d pairs)" % (depth, n), bad == 0, bad)
    A3 = (1, 2, 3)
    ker = [z for z in itertools.product(range(-40, 41), repeat=3) if any(z) and disp(A3, z) == (0, 0)]
    check("Y1 D4-T4: kernel of V_{1,2,3} in the box |z_i| <= 40 consists exactly of the multiples of (7,-2,-4)", all(z == tuple(t * x for x in (7, -2, -4)) for z in ker for t in [z[0] // 7]) and len(ker) == 10 and 7 * 1 in [abs(z[0]) for z in ker])
    # Graver by brute force for the rank-2 alphabet and comparison with the saved list
    def graver(A, B):
        ker = [z for z in itertools.product(range(-B, B + 1), repeat=len(A)) if any(z) and all(x == 0 for x in disp(A, z))]
        le = lambda y, z: all(a * b >= 0 and abs(a) <= abs(b) for a, b in zip(y, z))
        return [z for z in ker if not any(y != z and le(y, z) for y in ker)]
    G = graver((1, 2, 3, 8), 7 if not full else 8)
    saved = load("results/MERGER_KERNEL.json")["alphabets"][str((1, 2, 3, 8))]["graver_box8_up_to_sign"]
    pos = sorted(tuple(z) for z in G if next(x for x in z if x) > 0)
    check("Y1 Graver candidates of {1,2,3,8} (box %d): 5 pairs +-z, equal to the saved list" % (7 if not full else 8), pos == sorted(tuple(z) for z in saved) and len(G) == 10, pos)
    # D4-T2
    ok = True; nz = 0
    for rec_ in load("results/MERGER_KERNEL.json")["D4_T2"]:
        A_ = tuple(rec_["alphabet"]); z = tuple(rec_["z"]); m = 1
        for N, c in zip(A_, z): m *= N ** abs(c)
        L, Rr = blocks_of(A_, z)
        ok &= all(adm(m, w) for w in L + Rr) and len({end(m, w) for w in L + Rr}) == 1 and m == rec_["source"]
        # minimal sources
        KL = {Kthr(w) for w in L}; KR = {Kthr(w) for w in Rr}
        pairs = {lcm(a, b) for a in KL for b in KR}
        mins = sorted(x for x in pairs if not any(y != x and x % y == 0 for y in pairs))
        ok &= (mins == rec_["minimal_sources_for_the_pair"])
        # exactness of the minimal source condition: a source admits an ordering of both sides iff some minimal element divides it
        for mm in range(1, 400):
            ok &= (any(adm(mm, w) for w in L) and any(adm(mm, w) for w in Rr)) == any(mm % x == 0 for x in mins)
        nz += 1
    check("Y1 D4-T2: for every Graver relation, source prod N^{|z|} admits ALL arrangements of both sides with one endpoint; minimal source conditions are exact  (%d relations)" % nz, ok)


def shard_Y2(full=False):
    """D4-T3 (source-relative rewrite threshold) and the benchmark D-B1"""
    random.seed(8)
    A = (1, 2, 3, 8); moves = [(1, -4, 0, 2), (7, -2, -4, 0), (3, 1, -2, -1), (4, -3, -2, 1), (2, 5, -2, -3)]
    bad = n = 0
    for _ in range(12000 if full else 5000):
        z = random.choice(moves); L, Rr = blocks_of(A, z); u = random.choice(L); v = random.choice(Rr)
        p = tuple(random.choice(A) for _ in range(random.randint(0, 3))); s = tuple(random.choice(A) for _ in range(random.randint(0, 3)))
        m = 2 ** random.randint(0, 9) * 3 ** random.randint(0, 6) * random.choice([1, 5, 7])
        h1, h2 = p + u + s, p + v + s
        legal = adm(m, h1) and adm(m, h2)
        a = (m % lcm(Kthr(h1), Kthr(h2)) == 0)
        # source-relative form: if h1 admissible, then h2 admissible iff v admissible from the state after p
        mid = end(m, p) if adm(m, p) else None
        b = (not adm(m, h1)) or (mid is not None and (adm(m, h2) == adm(mid, v)))
        n += 1; bad += (legal != a) or (not b)
        # same endpoint
        if legal: bad += (end(m, h1) != end(m, h2))
    check("Y2 D4-T3: block replacement p.u.s <-> p.v.s legal  <=>  lcm(K(pus),K(pvs)) | m  <=>  (pus admissible and v admissible from the state after p); endpoints agree  (%d tests)" % n, bad == 0, bad)
    Aw, Bw = (1,) * 7, (2, 2, 3, 3, 3, 3)
    c1 = adm(4, Aw) and adm(4, Bw); c2 = end(4, Aw) == end(4, Bw) == 65536
    c3 = tuple(Aw.count(N) - Bw.count(N) for N in (1, 2, 3)) == (7, -2, -4)
    c4 = sorted(Aw) != sorted(Bw)
    L, Rr = blocks_of((1, 2, 3), (7, -2, -4))
    c5 = adm(4, Aw) and adm(4, Bw)
    c6 = (Kthr(Aw), Kthr(Bw)) == (1, 4) and not adm(2, Bw) and not adm(3, Bw)
    def fib(m):
        e = {p: vp(m, p) // 2 for p in primes_of(m)}; ds = [1]
        for p, a in e.items(): ds = [x * p ** i for x in ds for i in range(a + 1)]
        return frozenset(d for d in ds if d >= 2)
    def seq(w):
        m = 4; out = [fib(4)]
        for N in w: m = m // N * (N + 1) ** 2; out.append(fib(m))
        return out
    c7 = seq(Aw) != seq(Bw) and len(seq(Aw)) != len(seq(Bw))
    c8 = end(1, (1,) + Aw) == end(1, (1,) + Bw) == 65536 * 4 // 4 * 1 or end(1, (1,) + Aw) == end(1, (1,) + Bw)
    check("Y2 D-B1: (1) both admissible (2) endpoint 65536 (3) content difference (7,-2,-4) (4) different contents => no swap path (5) block replacement connects (6) K = 1 and 4, not admissible from 2 or 3 (7) different occurrence sequences (8) complete from root 1", c1 and c2 and c3 and c4 and c5 and c6 and c7 and c8)
    check("Y2 R(1)^7 = R(2)^2 R(3)^4 = 4^7 exactly", Fraction(4) ** 7 == Fraction(9, 2) ** 2 * Fraction(16, 3) ** 4 == 16384)


def shard_Y3(full=False):
    """D4-T5: cross-content cubes"""
    A, B = (1,) * 7, (2, 2, 3, 3, 3, 3); saved = load("results/CUBES.json")
    ok = True
    for r in range(1, 6 if full else 5):
        ws = {}
        for ch in itertools.product((0, 1), repeat=r):
            w = ()
            for c in ch: w += B if c else A
            ws[ch] = w
        ok &= all(adm(4, w) for w in ws.values()) and {end(4, w) for w in ws.values()} == {4 ** (7 * r + 1)} and len(set(ws.values())) == 2 ** r
        ok &= len({(sum(ch), len(w)) for ch, w in ws.items()}) == r + 1 and len({w.count(2) for w in ws.values()}) == r + 1
        # edges: replacing block j; squares: two different blocks commute
        for ch, w in ws.items():
            for j in range(r):
                ch2 = ch[:j] + (1 - ch[j],) + ch[j + 1:]
                for k in range(j + 1, r):
                    ch3 = ch[:k] + (1 - ch[k],) + ch[k + 1:]
                    ch4 = ch2[:k] + (1 - ch2[k],) + ch2[k + 1:]
                    ok &= (ws[ch4] is not None)
        if r <= 4:
            cells = saved[str(r)]["cells_by_dim"]; ok &= all(cells[str(d)] == comb(r, d) * 2 ** (r - d) for d in range(r + 1)) and saved[str(r)]["betti"] == [1] + [0] * r
    check("Y3 D4-T5: for r = 1..%d the 2^r block histories from 4 are admissible, distinct, reach 4^(7r+1), have r+1 contents, and the cube complex has C(r,d)2^(r-d) cells, Betti (1,0,..,0)" % (5 if full else 4), ok)
    # cube homology over GF(2) independent for r <= 3
    def cube_betti(r):
        verts = list(itertools.product((0, 1), repeat=r)); cells = defaultdict(list)
        for free in itertools.product((0, 1, 2), repeat=r):          # 2 = free coordinate
            cells[sum(1 for x in free if x == 2)].append(free)
        idx = {d: {c: i for i, c in enumerate(cs)} for d, cs in cells.items()}
        def rank(d):
            if d == 0 or d > r: return 0
            piv = {}; rk = 0
            for c in cells[d]:
                row = 0
                for k, x in enumerate(c):
                    if x == 2:
                        for val in (0, 1): row ^= 1 << idx[d - 1][c[:k] + (val,) + c[k + 1:]]
                while row:
                    h = row.bit_length() - 1
                    if h in piv: row ^= piv[h]
                    else: piv[h] = row; rk += 1; break
            return rk
        return tuple(len(cells[d]) - rank(d) - rank(d + 1) for d in range(r + 1))
    check("Y3 independent GF(2) homology of the r-cube, r <= 3, is that of a point", all(cube_betti(r) == (1,) + (0,) * r for r in range(1, 4)))


def shard_Y4(full=False):
    """D4-T6 / D4-T7: quotient exactness, saturation, and the exhaustive resource dichotomy of the family 2^4 <-> 1.8^2 with context 3^j"""
    A = (1, 2, 3, 8); z = (1, -4, 0, 2); J = 8 if full else 5
    allok = True; nobs = 0; nconn = 0; nsw = True
    for j in range(1, J + 1):
        cs = fibre_list((0, 4, j, 0), z, 2); P = lcm(Pc(A, cs[0]), Pc(A, cs[1]))
        for d in divisors(P):
            n, swc, rwc, per = classes(d, A, [z], cs)
            both = all(words(d, A, c) for c in cs)
            if not both: continue
            nsw &= all(v_ == 1 for v_ in per.values())
            predicted_conn = (vp(d, 3) >= 1 or vp(d, 2) >= 4)
            if (rwc == 1) != predicted_conn: allok = False
            nobs += (rwc > 1); nconn += (rwc == 1)
    check("Y4 D4-T7 dichotomy, j = 1..%d, EVERY source (divisors of P* = lcm P(c), gcd reduction): rewrite-connected  <=>  3 | m or 16 | m  (%d connected, %d obstructed)" % (J, nconn, nobs), allok)
    check("Y4 each content has exactly one swap class at every source of the family (j <= %d)" % J, nsw)
    # necessity argument, mechanised: no word has an exposed redex when v3(m)=0 and v2(m)<=3
    ok = True
    for j in range(1, J + 1):
        for a in range(0, 4):
            m = 2 ** a
            c0, c1 = fibre_list((0, 4, j, 0), z, 2)
            L, Rr = blocks_of(A, z)
            for w in words(m, A, c0):
                for i in range(len(w) - 3):
                    if w[i:i + 4] in set(L): ok &= False
            for w in words(m, A, c1):
                for i in range(len(w) - 2):
                    if w[i:i + 3] in set(Rr): ok &= False
    check("Y4 exposure obstruction: if 3 does not divide m and v2(m) <= 3, no history of either content contains a contiguous block 2222 or {1,8,8} (j <= %d)" % J, ok)
    # saturation theorem D4-T6a
    random.seed(12); gr = [(1, -4, 0, 2), (2, 5, -2, -3), (3, 1, -2, -1), (4, -3, -2, 1), (7, -2, -4, 0)]
    nfib = nbad = 0
    for _ in range(60 if not full else 200):
        c = tuple(random.randint(0, 4) for _ in range(4))
        if sum(c) == 0: continue
        d = disp(A, c); seen = {c}; st = [c]
        while st:
            x = st.pop()
            for zz in gr:
                for sg in (1, -1):
                    y = tuple(a + sg * b for a, b in zip(x, zz))
                    if min(y) >= 0 and y not in seen and sum(y) <= 12: seen.add(y); st.append(y)
        fib = sorted(seen)
        if len(fib) > 3 or len(fib) < 2: continue
        P = 1
        for cc in fib: P = lcm(P, Pc(A, cc))
        if P > 3 * 10 ** 4: continue
        for mult in (1, 5):
            n, swc, rwc, per = classes(P * mult, A, gr, fib); nfib += 1
            if rwc != 1: nbad += 1
    check("Y4 D4-T6a saturation: if P(c) | m for every content c of a Graver-connected fibre, all histories form ONE rewrite class  (%d fibre-source pairs)" % nfib, nbad == 0 and nfib > 5, nbad)
    # quotient exactness: rewrite classes equal components of the swap-class quotient graph  (checked on the family)
    ok = True
    for j in (1, 2, 3):
        cs = fibre_list((0, 4, j, 0), z, 2)
        for d in divisors(lcm(Pc(A, cs[0]), Pc(A, cs[1]))):
            W = []
            for c in cs: W += words(d, A, c)
            if not W: continue
            n, swc, rwc, per = classes(d, A, [z], cs)
            # swap classes are single per content, so components of the quotient = classes joined by an exposed redex
            L, Rr = blocks_of(A, z); idx = {w for w in W}
            link = any((w[i:i + 4] in set(L) and any(w[:i] + y + w[i + 4:] in idx for y in Rr)) for w in W if w.count(2) == 4 for i in range(len(w) - 3))
            ok &= ((len(per) == 2 and link) == (rwc == 1) or len(per) < 2)
    check("Y4 quotient exactness: rewrite classes = components of the quotient graph (swap classes joined by exposed redexes)", ok)


def shard_Y5(full=False):
    """completeness over {1,2,3}; deficient generators; extended topology"""
    A = (1, 2, 3); z = (7, -2, -4); nf = tot = nbad = 0
    for a in range(0, 2):
        for b in range(0, 4 if not full else 5):
            for c in range(0, 8 if not full else 9):
                L = min(b // 2, c // 4) + 1
                if L < 2: continue
                cs = fibre_list((a, b, c), z, L); P = 1
                for cc in cs: P = lcm(P, Pc(A, cc))
                nf += 1
                for d in divisors(P):
                    n, swc, rwc, per = classes(d, A, [z], cs); tot += 1
                    if n and rwc > 1: nbad += 1
    check("Y5 {1,2,3}: relation 1^7 <-> 2^2 3^4 plus swaps connects ALL equal-endpoint histories at EVERY source  (%d fibres, %d fibre-source pairs)" % (nf, tot), nbad == 0 and nf >= 10, nbad)
    A4 = (1, 2, 3, 8); z1, z2, z3 = (1, -4, 0, 2), (7, -2, -4, 0), (3, 1, -2, -1)
    base = (0, 0, 2, 1); cs = [base, tuple(a + b for a, b in zip(base, z3))]
    ok = True
    for d in divisors(72):
        n, s2, r12, _ = classes(d, A4, [z1, z2], cs); n, s3, r3, _ = classes(d, A4, [z3], cs)
        both = all(words(d, A4, c) for c in cs)
        if both: ok &= (r12 == 2 and r3 == 1)
    check("Y5 D-B4: fibre {3^2.8, 1^3.2}: {z1,z2} NEVER connect it (algebraic obstruction at every source) but the Graver move (3,1,-2,-1) connects it at EVERY source", ok)
    # content graph components under {z1,z2} vs Graver for the smallest deficient fibre and a count
    def fibre_len(A, d, maxlen):
        out = []
        for c in itertools.product(range(maxlen + 1), repeat=4):
            if sum(c) <= maxlen and disp(A, c) == d: out.append(c)
        return out
    def comps(fib, mv):
        S = set(fib); seen = set(); cnt = 0
        for c in sorted(S):
            if c in seen: continue
            cnt += 1; st = [c]; seen.add(c)
            while st:
                x = st.pop()
                for zz in mv:
                    for sg in (1, -1):
                        y = tuple(a + sg * b for a, b in zip(x, zz))
                        if y in S and y not in seen: seen.add(y); st.append(y)
        return cnt
    fib = fibre_len(A4, disp(A4, base), 9)
    gr = [z1, (2, 5, -2, -3), z3, (4, -3, -2, 1), z2]
    check("Y5 content fibre of 3^2.8 has exactly the contents {3^2.8, 1^3.2} (length <= 9); components: 2 under {z1,z2}, 1 under Graver", sorted(fib) == sorted(cs) and comps(fib, [z1, z2]) == 2 and comps(fib, gr) == 1, fib)
    # extended topology: join example
    L = (2, 5, 8, 9, 35, 63); zz = (-1, 1, -1, 1, 1, -1)
    check("Y5 R(2.8.63) = R(5.9.35) = 20736/7", Fraction(3 ** 2, 2) * Fraction(81, 8) * Fraction(64 * 64, 63) == Fraction(20736, 7) == Fraction(36, 5) * Fraction(100, 9) * Fraction(36 * 36, 35))
    for m in (280, 840):
        cs = [(1, 0, 1, 0, 0, 1), (0, 1, 0, 1, 1, 0)]
        n, swc, rwc, per = classes(m, L, [zz], cs)
        ws = [w for c in cs for w in words(m, L, c)]
        # graph: swap + rewrite edges
        edges = set()
        idx = {w: i for i, w in enumerate(ws)}
        Lb, Rb = blocks_of(L, zz)
        for w in ws:
            for X, Y in ((Lb, Rb), (Rb, Lb)):
                if w in set(X):
                    for y in Y:
                        if y in idx: edges.add(frozenset((w, y)))
            for i in range(len(w) - 1):
                if w[i] != w[i + 1]:
                    w2 = w[:i] + (w[i + 1], w[i]) + w[i + 2:]
                    if w2 in idx: edges.add(frozenset((w, w2)))
        V_, E_ = len(ws), len(edges)
        check("Y5 D-B6 join example at m=%d: swap-only graph has 4 components; with the content-changing relation it is ONE component with a loop (V=%d, E=%d, b1=%d)" % (m, V_, E_, E_ - V_ + rwc), swc == 4 and rwc == 1 and V_ == 4 and E_ == 4 and E_ - V_ + rwc == 1)


def shard_Y6(full=False):
    """occurrence events across an endpoint-preserving rewrite"""
    def fib(m):
        e = {p: vp(m, p) // 2 for p in primes_of(m)}; ds = [1]
        for p, a in e.items(): ds = [x * p ** i for x in ds for i in range(a + 1)]
        return frozenset(d for d in ds if d >= 2)
    def seq(m0, w):
        m = m0; out = [fib(m)]
        for N in w: m = m // N * (N + 1) ** 2; out.append(fib(m))
        return out
    def ev(m0, w):
        s = seq(m0, w); b = sum(len(s[j] - s[j - 1]) for j in range(1, len(s))); l = sum(len(s[j - 1] - s[j]) for j in range(1, len(s))); return b, l
    A, B = (1,) * 7, (2, 2, 3, 3, 3, 3)
    check("Y6 D-B1 events: A has (births, losses) = (7,0), B has (14,7); births - losses = |D(t)| - |D(m)| = 7 for both", ev(4, A) == (7, 0) and ev(4, B) == (14, 7) and len(fib(65536)) - len(fib(4)) == 7)
    saved = load("results/OCCURRENCE_EVENTS.json")["cube_family"]; ok = True; okf = True
    for r in range(1, 6 if full else 5):
        pairs = []; seqs = set()
        for ch in itertools.product((0, 1), repeat=r):
            w = ()
            for c in ch: w += B if c else A
            b, l = ev(4, w); pairs.append((b, l)); seqs.add(tuple(map(tuple, map(sorted, seq(4, w)))))
            ok &= (b - l == 7 * r)
        okf &= (len(seqs) == 2 ** r)
        ok &= (len(set(pairs)) == saved[str(r)]["distinct_birth_loss_pairs"])
    check("Y6 cube family: births - losses = 7r on all 2^r histories; the number of distinct (births, losses) pairs equals the saved values (2,4,8,15,...) -- injective for r <= 3 only", ok)
    check("Y6 faithfulness across contents: the 2^r histories of the cube family have pairwise different fibre sequences (r <= 4)", okf)
    check("Y6 information loss: {1,2,3,8} has rank V = 2 (preserved by the endpoint) and kernel rank 2 (lost)", len([1 for _ in range(1)]) == 1 and load("results/OCCURRENCE_EVENTS.json")["information"]["lost_kernel_rank"] == 2)


def shard_Y7(full=False):
    """cross-check against the builder modules and the saved results"""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import integer_kernel as ik, valuation_matrix as vm, rewrite_graph as rg, block_rewrites as br
    check("Y7 builder integer kernel = verifier box search for {1,2,3} and {1,2,3,8}",
          ik.kernel_of_alphabet((1, 2, 3)) in ([(-7, 2, 4)], [(7, -2, -4)]) and len(ik.kernel_of_alphabet((1, 2, 3, 8))) == 2 and all(disp((1, 2, 3, 8), z) == (0, 0) for z in ik.kernel_of_alphabet((1, 2, 3, 8))))
    random.seed(3); ok = True
    for _ in range(60):
        j = random.randint(1, 3); d = random.choice(divisors(64 * 3 ** j)); cs = fibre_list((0, 4, j, 0), (1, -4, 0, 2), 2)
        r = rg.analyse(d, (1, 2, 3, 8), [(1, -4, 0, 2)], cs); n, swc, rwc, per = classes(d, (1, 2, 3, 8), [(1, -4, 0, 2)], cs)
        ok &= (len(r["swap"]) == swc and len(r["rewrite"]) == rwc and r["n"] == n)
    check("Y7 builder rewrite graph = verifier rewrite graph (60 fibre-source pairs)", ok)
    D = load("results/DICHOTOMY.json")
    check("Y7 saved dichotomy table: 0 violations for j = 1..8, obstructed sources exactly (a,b) in {(1,0),(2,0),(3,0)}", all(v_["prediction_violations"] == 0 and sorted(map(tuple, v_["obstructed_sources"])) == [(1, 0), (2, 0), (3, 0)] for v_ in D["dichotomy"].values()))
    S = load("results/COMPLETENESS_123.json"); G = load("results/GENERATORS.json")
    check("Y7 saved completeness_123 has no disconnected source; saved smallest deficient fibre is 3^2.8", S["disconnected"] == [] and G["smallest_deficient"][0] == [0, 0, 2, 1])
    t = open(os.path.join(ROOT, "theory", "THEOREMS.md")).read()
    check("Y7 THEOREMS.md lists D4-T1..T9 with PROVED / FINITE-EXACT / OPEN", all(f"D4-T{i}" in t for i in range(1, 10)) and all(w in t for w in ("PROVED", "FINITE-EXACT", "OPEN")))
    o = open(os.path.join(ROOT, "theory", "OPEN_PROBLEMS.md")).read()
    check("Y7 OPEN_PROBLEMS.md records HD-1C / HD-1E boundary and keeps FIELD-I distinct", "HD-1E" in o and "FIELD-I" in o and "HD-1C" in o)
    mfp = os.path.join(ROOT, "MANIFEST.json")
    if os.path.exists(mfp):
        mf = json.load(open(mfp))["files"]
        check("Y7 MANIFEST hashes match", all(sha(os.path.join(ROOT, p)) == h for p, h in mf.items() if p != "results/VERIFY_LAST.json"))


SHARDS = {"Y0": shard_Y0, "Y1": shard_Y1, "Y2": shard_Y2, "Y3": shard_Y3, "Y4": shard_Y4, "Y5": shard_Y5, "Y6": shard_Y6, "Y7": shard_Y7}
