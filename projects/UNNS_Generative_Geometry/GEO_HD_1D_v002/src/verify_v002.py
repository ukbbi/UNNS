"""HD-1D v002 INDEPENDENT verifier: re-implements admissibility and thresholds from the definition (no import of thresholds.py for the checks)."""
import os, sys, json, itertools, random, hashlib
from math import gcd, lcm
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = []; FAILS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + ((" -- " + str(detail)) if detail != "" else ""), flush=True)
    if not ok: FAILS.append(name)


def load(rel):
    with open(os.path.join(ROOT, rel)) as f: return json.load(f)


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
    """smallest K with: K | m  <=>  adm(m,w); built from prefix valuation deficits (independent coding)"""
    ps = set()
    for N in w: ps |= set(primes_of(N)) | set(primes_of(N + 1))
    k = 1
    for p in ps:
        run = 0; need = 0
        for N in w:
            run += 2 * vp(N + 1, p) - vp(N, p)
            need = max(need, -run)
        k *= p ** need
    return k


def nbrs(w):
    for i in range(len(w) - 1):
        if w[i] != w[i + 1]: yield w[:i] + (w[i + 1], w[i]) + w[i + 2:]


def ncomp(V):
    V = set(V); seen = set(); c = 0
    for v in V:
        if v in seen: continue
        c += 1; st = [v]; seen.add(v)
        while st:
            x = st.pop()
            for y in nbrs(x):
                if y in V and y not in seen: seen.add(y); st.append(y)
    return c


def shard_W0(full=False):
    """v001 left untouched (module hashes)"""
    h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
    pins = load("results/V001_PINS.json")
    ok = all(h(os.path.join(ROOT, "src", f)) == s for f, s in pins.items())
    check("W0 copied v001 builder modules are byte-identical to the v001 release (%d files)" % len(pins), ok)


def shard_W1(full=False):
    """D-T7: threshold law"""
    random.seed(7)
    labs = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 20, 21, 27]
    n = bad = 0
    for _ in range(60000 if full else 20000):
        w = tuple(random.choice(labs) for _ in range(random.randint(1, 6))); m = random.randint(1, 5000)
        n += 1; bad += (adm(m, w) != (m % Kthr(w) == 0))
    check("W1 random words: admissible from m  <=>  K(w) | m   (%d tests)" % n, bad == 0, bad)
    # minimality: K(w) itself admits and no proper divisor does
    ok = True
    for _ in range(3000):
        w = tuple(random.choice(labs) for _ in range(random.randint(1, 5))); K = Kthr(w)
        ok &= adm(K, w) and all(not adm(K // p, w) for p in primes_of(K))
    check("W1 K(w) is the smallest admitting source (K admits; K/p does not, all p | K)", ok)
    # builder agrees
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import thresholds as th
    check("W1 builder K(w) equals independent K(w) on 3000 random words", all(th.K(w) == Kthr(w) for w in [tuple(random.choice(labs) for _ in range(random.randint(1, 5))) for _ in range(3000)]))


def shard_W2(full=False):
    """swap graph = induced subgraph; connection by path thresholds; monotonicity"""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import thresholds as th
    ok = True; n = 0
    for c in [(2, 3, 14), (1, 2, 3, 8), (1, 2, 4), (2, 6, 10), (2, 3, 4, 5), (2, 2, 3, 9)]:
        arr = sorted(set(itertools.permutations(c)))
        for m in list(range(1, 400)) + [k * 14 for k in range(1, 200)]:
            A = [w for w in arr if adm(m, w)]
            # direct swap graph: edge iff both admissible (a swap of admissible words is a legal swap)
            n += 1
            ok &= (A == [w for w in arr if m % Kthr(w) == 0])
            ok &= (len(th.classes_at(th.threshold_table(c), m)) == ncomp(A))
    check("W2 induced-graph law: admissible set and swap classes from thresholds = direct enumeration (%d (content,m) cases)" % n, ok)
    # monotonicity: multiplying the source keeps admissible arrangements admissible and connections
    ok = True
    for c in [(2, 3, 14), (1, 2, 3, 8), (2, 3, 4, 5)]:
        arr = sorted(set(itertools.permutations(c)))
        for m in range(1, 200):
            for q in (2, 3, 5, 7):
                A, B = {w for w in arr if adm(m, w)}, {w for w in arr if adm(m * q, w)}
                ok &= A <= B
    check("W2 monotonicity: admissible arrangements persist when the source is multiplied", ok)
    thr = th.threshold_table((2, 3, 14))
    hexa = [(14, 3, 2), (3, 14, 2), (3, 2, 14), (2, 3, 14), (2, 14, 3), (14, 2, 3)]
    p1 = lcm(*[Kthr(w) for w in hexa[:4]]); p2 = lcm(*[Kthr(w) for w in [hexa[0], hexa[5], hexa[4], hexa[3]]])
    check("W2 the two paths of the hexagon for {2,3,14} have thresholds 42 and 28; builder antichain = [28, 42]", (p1, p2) == (42, 28) and th.connect_thresholds(thr, (14, 3, 2), (2, 3, 14)) == [28, 42])
    # connection thresholds = brute force over all simple paths on the hexagon for a sample of contents
    ok = True
    for c in [(2, 3, 14), (2, 3, 8), (2, 3, 9), (1, 2, 4), (2, 8, 15)]:
        arr = sorted(set(itertools.permutations(c))); t = th.threshold_table(c)
        a, b = arr[0], arr[-1]
        allp = set()
        def dfs(x, seen, cur):
            if x == b: allp.add(cur); return
            for y in nbrs(x):
                if y not in seen: dfs(y, seen | {y}, lcm(cur, Kthr(y)))
        dfs(a, {a}, Kthr(a))
        mins = sorted(v for v in allp if not any(u != v and v % u == 0 for u in allp))
        ok &= (mins == th.connect_thresholds(t, a, b))
    check("W2 minimal path thresholds (antichain) = brute force over simple paths", ok)


def shard_W2b(full=False):
    """class counts are not monotone; three components"""
    def cnt(c, m): return ncomp([w for w in set(itertools.permutations(c)) if adm(m, w)])
    check("W2b {2,3,8}: 1 class at source 2, 2 classes at source 8 (count can increase when the source is multiplied)", (cnt((2, 3, 8), 2), cnt((2, 3, 8), 8)) == (1, 2))
    check("W2b {2,3,14}: 2 classes at 14, 1 class at 28 (count can decrease)", (cnt((2, 3, 14), 14), cnt((2, 3, 14), 28)) == (2, 1))
    check("W2b {2,3,8,9} at source 8 has 3 swap classes (sizes 1,1,4)", cnt((2, 3, 8, 9), 8) == 3)
    check("W2b {2,3,14}: complete count by source m: 0 if 14 and 21 do not divide m; 2 if 14|m and gcd(m/14,6)=1; else 1 (m<=3000)",
          all(cnt((2, 3, 14), m) == (2 if (m % 14 == 0 and gcd(m // 14, 6) == 1) else (1 if (m % 14 == 0 or m % 21 == 0) else 0)) for m in range(1, 3001)))


def shard_W3(full=False):
    """the 14q family"""
    c = (2, 3, 14); arr = sorted(set(itertools.permutations(c)))
    table = {w: Kthr(w) for w in arr}
    check("W3 six thresholds of {2,3,14}: (14,3,2)=14, (2,3,14)=14, (14,2,3)=28, (2,14,3)=28, (3,14,2)=21, (3,2,14)=21",
          table == {(14, 3, 2): 14, (2, 3, 14): 14, (14, 2, 3): 28, (2, 14, 3): 28, (3, 14, 2): 21, (3, 2, 14): 21})
    top = 3000 if full else 800
    bad = 0
    for q in range(1, top + 1):
        A = [w for w in arr if adm(14 * q, w)]
        if ncomp(A) != (2 if gcd(q, 6) == 1 else 1): bad += 1
    check("W3 swap classes of {2,3,14} from source 14q: 2 if gcd(q,6)=1 else 1  (q <= %d, direct enumeration)" % top, bad == 0, bad)
    ends = all((lambda m, w: [m := m // N * (N + 1) ** 2 for N in w][-1])(14 * q, w) == 5400 * q for q in range(1, 200) for w in arr if adm(14 * q, w))
    check("W3 every admissible arrangement from 14q ends at 5400 q", ends)
    d = load("results/FAMILY_14Q.json")
    check("W3 stored table equals the rule", all(r["classes"] == r["predicted_classes"] for r in d["table"]) and d["connection_thresholds"] == [28, 42])


def shard_W4(full=False):
    """D-T9: content {2,3,N}"""
    # (a) N = 2,3 mod 6, N >= 8: at source m = N exactly the two opposite arrangements are admissible
    top = 4000 if full else 1500
    bad = 0; n = 0
    for N in range(8, top):
        if N % 6 not in (2, 3): continue
        arr = sorted(set(itertools.permutations((2, 3, N))))
        A = [w for w in arr if adm(N, w)]
        n += 1
        if ncomp(A) != 2 or len(A) != 2: bad += 1
    check("W4 N = 2,3 (mod 6), 8 <= N < %d: at source m=N exactly two arrangements are admissible and they are swap-disconnected (%d values of N)" % (top, n), bad == 0, bad)
    # explicit formulas for the pair
    # opposite vertices of the hexagon: N = 2 (mod 6) -> (N,3,2) and (2,3,N)... verified as: the two admissible arrangements are at graph distance 3
    ok = True
    for N in range(8, 600):
        if N % 6 not in (2, 3): continue
        A = sorted(w for w in itertools.permutations((2, 3, N)) if adm(N, w))
        ok &= len(A) == 2
        # reversal pair: the two admissible arrangements are reverses of each other, hence opposite on the 6-cycle
        ok &= A[0] == tuple(reversed(A[1]))
        ok &= A[1] not in set(nbrs(A[0]))
    check("W4 the two admissible arrangements at m=N are opposite vertices of the hexagon", ok)
    # explicit threshold formulas of D-T9(a)
    ok = True; nn = 0
    for N in range(8, 3000):
        if N % 6 not in (2, 3): continue
        a, b = vp(N, 2), vp(N, 3); R = N // (2 ** a * 3 ** b); nn += 1
        if N % 6 == 2:
            want = {(2, 3, N): 2 ** max(1, a - 3) * R, (2, N, 3): 2 * N, (N, 2, 3): 2 * N, (N, 3, 2): N, (3, N, 2): 3 * 2 ** max(0, a - 3) * R, (3, 2, N): 3 * 2 ** max(0, a - 3) * R}
        else:
            want = {(2, 3, N): 2 * 3 ** (b - 1) * R, (2, N, 3): 2 * 3 ** (b - 1) * R, (N, 2, 3): N, (N, 3, 2): 3 * N, (3, N, 2): 3 * N, (3, 2, N): 3 ** max(1, b - 1) * R}
        ok &= all(Kthr(w) == k for w, k in want.items())
    check("W4 explicit threshold formulas of D-T9(a), both residue classes (%d values of N)" % nn, ok)
    # (b) converse, finite
    res = load("results/THRESHOLD_CENSUS.json")["family_2_3_N"]
    splitN = set(res["split_N"])
    exp = {N for N in range(4, 401) if N % 6 in (2, 3) and N >= 8}
    check("W4 converse (FINITE-EXACT): for 4 <= N <= 400 the content {2,3,N} has a split source iff N = 2,3 (mod 6), N >= 8 (stored census)", splitN == exp and res["all_minimal_sources_equal_N"])
    # independent recomputation of the converse for N <= 120 using direct admissibility over a divisibility-closed set of sources
    ok = True
    for N in range(4, 121 if not full else 300):
        arr = sorted(set(itertools.permutations((2, 3, N)))); Ks = [Kthr(w) for w in arr]
        cl = set(Ks); changed = True
        while changed:
            changed = False
            for a in list(cl):
                for b in Ks:
                    c = lcm(a, b)
                    if c not in cl: cl.add(c); changed = True
        splits = any(ncomp([w for w in arr if adm(m, w)]) >= 2 for m in cl)
        ok &= (splits == (N % 6 in (2, 3) and N >= 8))
    check("W4 independent re-derivation of the converse over the lcm-closure of thresholds, N < %d" % (121 if not full else 300), ok)
    # parameter box for the converse (exponent pattern; R irrelevant)
    bad = 0
    for a, b, c2, c3 in itertools.product(range(0, 9 if not full else 13), repeat=4):
        if (a >= 1) == (c2 >= 1) or (b >= 1 and c3 >= 1): continue
        vec = {'x': (-1, 2), 'y': (4, -1), 'z': (2 * c2 - a, 2 * c3 - b)}
        T = {}
        for w in itertools.permutations(vec):
            d = []
            for p in (0, 1):
                s = bb = 0
                for n in w: s += vec[n][p]; bb = max(bb, -s)
                d.append(bb)
            T[w] = tuple(d)
        sp = False
        for e2 in range(0, 30):
            for e3 in range(0, 30):
                A = [w for w, (d2, d3) in T.items() if d2 <= e2 and d3 <= e3]
                if A and ncomp(A) >= 2: sp = True; break
            if sp: break
        pred = (a >= 1 and c3 >= 1) or (b >= 1 and c2 >= 1)
        bad += (sp != pred)
    check("W4 exponent-box check of the converse: valuations (v2(N),v3(N),v2(N+1),v3(N+1)) in a box, mismatches", bad == 0, bad)


def shard_W5(full=False):
    """census cross-check"""
    cen = load("results/THRESHOLD_CENSUS.json")
    sys.path.insert(0, os.path.join(ROOT, "src"))
    def splits(c):
        arr = sorted(set(itertools.permutations(c))); Ks = [Kthr(w) for w in arr]
        cl = set(Ks); changed = True
        while changed:
            changed = False
            for a in list(cl):
                for b in Ks:
                    cc = lcm(a, b)
                    if cc not in cl: cl.add(cc); changed = True
        return [m for m in cl if ncomp([w for w in arr if adm(m, w)]) >= 2]
    top = 22 if not full else 30
    mine = sorted(c for c in itertools.combinations(range(1, top + 1), 3) if splits(c))
    stored = sorted(tuple(x["content"]) for x in cen["three_distinct_split"]["contents"] if max(x["content"]) <= top)
    check("W5 three distinct labels <= %d: split contents recomputed independently = stored (%d contents)" % (top, len(mine)), mine == stored)
    t4 = 12 if not full else 14
    mine4 = sorted(c for c in itertools.combinations(range(1, t4 + 1), 4) if splits(c))
    stored4 = sorted(tuple(x["content"]) for x in cen["four_distinct_split"]["contents"] if max(x["content"]) <= t4)
    check("W5 four distinct labels <= %d: split contents recomputed = stored (%d contents)" % (t4, len(mine4)), mine4 == stored4)
    check("W5 v001 minimal case (source 14, {2,3,14}) and (source 2, {1,2,3,8}) appear as split sources",
          [14] == [x for x in cen["three_distinct_split"]["contents"] if x["content"] == [2, 3, 14]][0]["minimal_split_sources"] and any(x["content"] == [1, 2, 3, 8] and 2 in x["minimal_split_sources"] for x in cen["four_distinct_split"]["contents"]))


def shard_W6(full=False):
    """gates"""
    st = load("STATUS.json")
    check("W6 C3 not claimed", st["gates"]["C3"] == "NOT_CLAIMED")
    check("W6 same-author caveat", "same author" in st["independence_caveat"])
    check("W6 fixed-source vs complete-history scope recorded", "FIXED source" in json.dumps(st))
    check("W6 converse of D-T9 recorded as FINITE-EXACT, not proved", any("converse" in x and "FINITE" in x for x in st["claims"]["finite_exact"]))


SHARDS = {"W0": shard_W0, "W1": shard_W1, "W2": shard_W2, "W2b": shard_W2b, "W3": shard_W3, "W4": shard_W4, "W5": shard_W5, "W6": shard_W6}
