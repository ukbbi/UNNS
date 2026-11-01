"""GEO_HD_BRIDGE_v001 INDEPENDENT verifier (shards Z0-Z7).  Z0-Z6 re-implement SELECT-II arithmetic, the permutohedral homology, the family F_j,
the occurrence incidence/churn, and the FIELD-I map from the definitions and do NOT import the builder modules; Z7 compares with the builder."""
import os, sys, json, itertools, random, hashlib
from fractions import Fraction
from math import gcd, lcm
from itertools import permutations, combinations, product
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


def pf(n):
    out = {}; p = 2
    while p * p <= n:
        while n % p == 0: out[p] = out.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: out[n] = out.get(n, 0) + 1
    return out


def adm(m, w):
    for N in w:
        if m % N: return False
        m = m // N * (N + 1) ** 2
    return True


def words(m, cnt):
    """all admissible orderings of the multiset cnt={label:count}"""
    labs = sorted(cnt); out = []
    def rec(m, c, acc):
        if not sum(c.values()): out.append(tuple(acc)); return
        for N in labs:
            if c[N] and m % N == 0:
                c[N] -= 1; acc.append(N); rec(m // N * (N + 1) ** 2, c, acc); acc.pop(); c[N] += 1
    rec(m, dict(cnt), []); return out


def states(m, w):
    out = [m]
    for N in w: m = m // N * (N + 1) ** 2; out.append(m)
    return out


# ---------------- independent permutohedral GF(2) homology
def betti_perm(admset, k):
    """admset: set of permutation tuples of range(k) (vertex = word).  face = ordered partition (blocks as tuples); included iff all facets included."""
    def parts(rem):
        if not rem: yield (); return
        rem = tuple(rem)
        for r in range(1, len(rem) + 1):
            for B in combinations(rem, r):
                rest = tuple(x for x in rem if x not in B)
                for tail in parts(rest): yield (B,) + tail
    faces = sorted(parts(range(k)), key=lambda f: -len(f))
    incl = {}
    def facets(f):
        for i, B in enumerate(f):
            if len(B) >= 2:
                for r in range(1, len(B)):
                    for C in combinations(B, r):
                        D = tuple(x for x in B if x not in C); yield f[:i] + (C, D) + f[i + 1:]
    for f in faces:
        if len(f) == k: incl[f] = tuple(B[0] for B in f) in admset
        else: incl[f] = all(incl[g] for g in facets(f))
    bydim = {}
    for f in faces:
        if incl[f]: bydim.setdefault(k - len(f), []).append(f)
    idx = {d: {f: i for i, f in enumerate(L)} for d, L in bydim.items()}
    def rank(d):
        if d <= 0 or d not in bydim: return 0
        piv = {}; rk = 0
        for f in bydim[d]:
            row = 0
            for g in facets(f): row ^= 1 << idx[d - 1][g]
            while row:
                h = row.bit_length() - 1
                if h in piv: row ^= piv[h]
                else: piv[h] = row; rk += 1; break
        return rk
    return tuple(len(bydim.get(d, [])) - rank(d) - rank(d + 1) for d in range(k))


def route_betti(C, m, relax=()):
    """Betti vector of the route complex of the distinct labels C at source m; primes in `relax` are not enforced"""
    C = sorted(C); k = len(C)
    perms = set()
    for perm in permutations(range(k)):
        w = [C[i] for i in perm]; mm = m
        # admissibility with relaxed primes: track valuations explicitly
        primes = set()
        for N in C: primes |= set(pf(N)) | set(pf(N + 1))
        u = {p: vp(m, p) for p in primes}; ok = True
        for N in w:
            for p in primes:
                if p not in relax and u[p] < vp(N, p): ok = False; break
            if not ok: break
            for p in primes: u[p] += 2 * vp(N + 1, p) - vp(N, p)
        if ok: perms.add(perm)
    return betti_perm(perms, k) if perms else None


# ================================================================ shards
def shard_Z0(full=False):
    pins = load("results/PINS.json")
    check("Z0 pinned copied modules unchanged (%d)" % len(pins), all(sha(os.path.join(ROOT, "src", f)) == s for f, s in pins.items()))
    for ver in ("v001", "v002", "v003", "v004"):
        mp = os.path.join(os.path.dirname(ROOT), "GEO_HD_1D_" + ver, "MANIFEST.json")
        if os.path.exists(mp):
            mf = json.load(open(mp))["files"]; d = os.path.dirname(mp)
            check("Z0 sibling GEO_HD_1D_%s untouched (manifest hashes)" % ver, all(sha(os.path.join(d, p)) == h for p, h in mf.items() if not p.startswith("figures/")))  # rendered PNGs excluded: matplotlib output is not byte-stable
    st = load("STATUS.json")
    check("Z0 STATUS gates", st["gates"]["C3"] == "NOT_CLAIMED" and st["gates"]["NOVELTY"] == "NOT_ASSESSED" and "same author" in st["independence_caveat"])
    need = ["theory/" + n + ".md" for n in ("SOURCE_CROSSWALK", "VALUATION_GEOMETRY", "ACTIVE_DIMENSIONS", "HISTORY_REALIZATION", "OCCURRENCE_EVENTS", "FIELD_STRANDS", "BRIDGE_RELATIONS", "THEOREMS", "OPEN_PROBLEMS", "ADDENDUM_D4_T7B")]
    check("Z0 required documents present", all(os.path.exists(os.path.join(ROOT, p)) for p in need), [p for p in need if not os.path.exists(os.path.join(ROOT, p))])


def shard_Z1(full=False):
    """passive-coordinate theorem"""
    rng = random.Random(21); n = bad = ctrl = 0
    for _ in range(3000 if not full else 8000):
        A = rng.sample(range(2, 61), rng.randint(2, 5)); c = {N: rng.randint(0, 2) for N in A}
        if not 0 < sum(c.values()) <= 6: continue
        m = 1
        for p in (2, 3, 5, 7, 11, 13): m *= p ** rng.randint(0, 4)
        act = sorted({p for N in A for p in pf(N)})
        base = []
        for N, k in c.items(): base += [N] * k
        for w in set(permutations(base)):
            n += 1
            u = {p: vp(m, p) for p in act}; ok = True
            for N in w:
                if any(u[p] < vp(N, p) for p in act): ok = False; break
                for p in act: u[p] += 2 * vp(N + 1, p) - vp(N, p)
            bad += (ok != adm(m, w))
            if len(act) > 1:
                q = rng.choice(act); u = {p: vp(m, p) for p in act if p != q}; ok2 = True
                for N in w:
                    if any(u[p] < vp(N, p) for p in u): ok2 = False; break
                    for p in u: u[p] += 2 * vp(N + 1, p) - vp(N, p)
                ctrl += (ok2 != adm(m, w))
    check("Z1 passive theorem: admissibility is decided by the valuations at ACTIVE primes only (%d histories); dropping an active prime does change it (%d control changes)" % (n, ctrl), bad == 0 and ctrl > 0, bad)
    # algebraic content: Delta_p(N) = 2 v_p(N+1) >= 0 when p does not divide N
    ok = all(2 * vp(N + 1, p) - vp(N, p) >= 0 for N in range(1, 400) for p in (2, 3, 5, 7, 11, 13) if N % p)
    check("Z1 Delta_p(N) = 2 v_p(N+1) >= 0 for every prime p not dividing N", ok)
    # spec controls: displacement vectors of {2,3,8,9,14} over primes 2,3,5,7
    D = lambda N: tuple(2 * vp(N + 1, p) - vp(N, p) for p in (2, 3, 5, 7))
    check("Z1 spec displacement vectors: D(2)=(-1,2,0,0) D(3)=(4,-1,0,0) D(8)=(-3,4,0,0) D(9)=(2,-2,2,0) D(14)=(-1,2,2,-1)",
          [D(2), D(3), D(8), D(9), D(14)] == [(-1, 2, 0, 0), (4, -1, 0, 0), (-3, 4, 0, 0), (2, -2, 2, 0), (-1, 2, 2, -1)])


def shard_Z2(full=False):
    """route-complex dimensionality: independent homology"""
    ex = load("results/DIMENSIONS.json")["explicit_irreducible_examples"]; ok = True
    for name, v in ex.items():
        C, m = v["alphabet"], v["m"]; b = route_betti(C, m)
        primes = sorted({p for N in C for p in pf(N)})
        rel = {p: route_betti(C, m, relax=(p,)) for p in primes}
        triv = (1,) + (0,) * (len(C) - 1)
        good = b == tuple(v["betti"]) and all(r == triv for r in rel.values()) and (b != triv)
        check("Z2 %s: alphabet %s at m=%d has Betti %s and every single-prime relaxation (primes %s) is contractible" % (name, C, m, b, primes), good)
    # spec benchmarks
    check("Z2 C-B1 {2,3,8,9}@72 Betti (1,1,0,0), void-free", route_betti([2, 3, 8, 9], 72) == (1, 1, 0, 0))
    b = route_betti([2, 3, 8, 9, 14], 1008)
    check("Z2 C-B2 {2,3,8,9,14}@1008 Betti (1,0,1,0,0); relaxing prime 7 leaves it unchanged, so the void needs only primes 2,3", b == (1, 0, 1, 0, 0) and route_betti([2, 3, 8, 9, 14], 1008, relax=(7,)) == b and route_betti([2, 3, 8, 9, 14], 1008, relax=(2,)) != b)
    check("Z2 C-B1 relaxing prime 2 or 3 destroys the loop; prime 5 is passive", route_betti([2, 3, 8, 9], 72, relax=(2,)) == (1, 0, 0, 0) and route_betti([2, 3, 8, 9], 72, relax=(3,)) == (1, 0, 0, 0) and route_betti([2, 3, 8, 9], 72, relax=(5,)) == (1, 1, 0, 0))
    check("Z2 A3* {2,3,4,5,6}@30 is contractible (feasibility control); @4 it is disconnected", route_betti([2, 3, 4, 5, 6], 30) == (1, 0, 0, 0, 0) and route_betti([2, 3, 4, 5, 6], 4) == (2, 0, 0, 0, 0))
    # reproduce a random sample of census examples
    for fn in ("CENSUS_K4_30", "CENSUS_K5_16", "CENSUS_K5_with2_26"):
        d = load("results/%s.json" % fn); n = 0; good = True
        for e in d["examples"]:
            C = e["content"]; src = 1
            for p, a in e["source_valuations"].items(): src *= int(p) ** a
            b = route_betti(C, src); good &= (b == tuple(e["betti"]))
            for p in e["essential"]: good &= route_betti(C, src, relax=(p,)) == (1,) + (0,) * (len(C) - 1)
            n += 1
        check("Z2 %s: all %d catalogued example features reproduced (Betti, essential primes)" % (fn, n), good)


def shard_Z3(full=False):
    """all-j exposure dichotomy (D4-T7b); own code"""
    J = 16 if full else 11; bad = n = 0
    def ws(m, cnt): return words(m, cnt)
    for j in range(1, J + 1):
        cU, cV = {2: 4, 3: j}, {1: 1, 8: 2, 3: j}
        for a in range(7):
            for b in range(j + 1):
                m = 2 ** a * 3 ** b; U = ws(m, cU); V = ws(m, cV); W = U + V; idx = {w: i for i, w in enumerate(W)}
                real = (b + 8 >= j) and not (a == 0 and b == 0)
                n += 1
                if bool(U) != real or bool(V) != real: bad += 1; continue
                if not real: continue
                par = list(range(len(W)))
                def f(x):
                    while par[x] != x: par[x] = par[par[x]]; x = par[x]
                    return x
                for w in W:
                    for i in range(len(w) - 1):
                        if w[i] != w[i + 1]:
                            t = w[:i] + (w[i + 1], w[i]) + w[i + 2:]
                            if t in idx: par[f(idx[w])] = f(idx[t])
                cu = len({f(idx[w]) for w in U}); cv = len({f(idx[w]) for w in V})
                for w in W:
                    for i in range(len(w) - 3):
                        if w[i:i + 4] == (2, 2, 2, 2):
                            for v in ((1, 8, 8), (8, 1, 8), (8, 8, 1)):
                                t = w[:i] + v + w[i + 4:]
                                if t in idx: par[f(idx[w])] = f(idx[t])
                comps = len({f(i) for i in range(len(W))})
                if cu != 1 or cv != 1 or (comps == 1) != (b >= 1 or a >= 4) or (comps not in (1, 2)): bad += 1
                # witnesses
                wit = ({"U": (3,) + (2,) * 4 + (3,) * (j - 1), "V": (3, 1, 8, 8) + (3,) * (j - 1)} if b >= 1 else {"U": (2, 3, 2, 2, 2) + (3,) * (j - 1), "V": (1, 8, 3, 8) + (3,) * (j - 1)})
                bad += (not adm(m, wit["U"])) or (not adm(m, wit["V"]))
                if b >= 1 or a >= 4:
                    # the explicit joining redex (executed at the front, after a leading 3 when 3|m)
                    pre = (3,) if b >= 1 else ()
                    wu = pre + (2,) * 4 + (3,) * (j - len(pre)); wv = pre + (1, 8, 8) + (3,) * (j - len(pre))
                    bad += not (adm(m, wu) and adm(m, wv) and states(m, wu)[-1] == states(m, wv)[-1])
    check("Z3 D4-T7b for j = 1..%d, all (v2<=6, v3<=j) [gcd reduction]: realizable iff b+8>=j and (a,b)!=(0,0); one swap class per content; rewrite-connected iff b>=1 or a>=4, else exactly two classes; explicit witnesses admissible  (%d cases)" % (J, n), bad == 0, bad)
    check("Z3 R(2)^4 = R(1) R(8)^2 = 3^8/2^4", Fraction(9, 2) ** 4 == 4 * Fraction(81, 8) ** 2 == Fraction(3 ** 8, 2 ** 4))
    # swap-connectivity lemma for the two-letter pairs (2,3) and (8,3) from arbitrary states
    bad = 0
    for A_ in (2, 8):
        for x in range(0, 6):
            for y in range(0, 6):
                for na in range(0, 4):
                    for nb in range(0, 5):
                        if na + nb == 0: continue
                        m = 2 ** x * 3 ** y; W = words(m, {A_: na, 3: nb}); idx = {w: i for i, w in enumerate(W)}
                        if not W: continue
                        par = list(range(len(W)))
                        def f(z):
                            while par[z] != z: par[z] = par[par[z]]; z = par[z]
                            return z
                        for w in W:
                            for i in range(len(w) - 1):
                                t = w[:i] + (w[i + 1], w[i]) + w[i + 2:]
                                if w[i] != w[i + 1] and t in idx: par[f(idx[w])] = f(idx[t])
                        bad += len({f(i) for i in range(len(W))}) != 1
    check("Z3 two-letter lemma: admissible orderings of {2^a,3^b} and {8^a,3^b} from any state 2^x 3^y form one swap class (x,y<=5)", bad == 0, bad)


def shard_Z4(full=False):
    """history realization"""
    # trace injectivity: states strictly increase, so the set of states determines the word
    rng = random.Random(8); n = bad = 0
    for _ in range(400):
        A = rng.sample(range(1, 25), rng.randint(2, 4)); m = 1
        for p in (2, 3, 5, 7): m *= p ** rng.randint(0, 5)
        seen = {}
        for c in product(*[range(3)] * len(A)):
            if not 0 < sum(c) <= 5: continue
            for w in words(m, {N: k for N, k in zip(A, c) if k}):
                t = frozenset(states(m, w)); n += 1
                if t in seen and seen[t] != w: bad += 1
                seen[t] = w
    check("Z4 distinct histories from one source have distinct state sets (%d histories); states strictly increase because R(N) > 1" % n, bad == 0 and all(Fraction((N + 1) ** 2, N) > 1 for N in range(1, 300)))
    # parallel displacement: independent cross-product test over the full prime support (N <= 400)
    vec = {}
    for N in range(1, 401):
        vec[N] = {p: 2 * vp(N + 1, p) - vp(N, p) for p in set(pf(N)) | set(pf(N + 1))}
    par_pairs = []
    for a, b in combinations(range(1, 401), 2):
        P = sorted(set(vec[a]) | set(vec[b])); va = [vec[a].get(p, 0) for p in P]; vb = [vec[b].get(p, 0) for p in P]
        if all(va[i] * vb[j] == va[j] * vb[i] for i in range(len(P)) for j in range(i + 1, len(P))): par_pairs.append((a, b))
    check("Z4 no two distinct labels N<M<=400 have parallel displacement vectors (so every swap diamond has nonzero area in some coordinate plane)", par_pairs == [])
    # bigon area
    A = (1,) * 7; B = (2, 2, 3, 3, 3, 3)
    def dd(N): return (2 * vp(N + 1, 2) - vp(N, 2), 2 * vp(N + 1, 3) - vp(N, 3))
    def path(w):
        x = (vp(4, 2), vp(4, 3)); out = [x]
        for N in w: d = dd(N); x = (x[0] + d[0], x[1] + d[1]); out.append(x)
        return out
    pa, pb = path(A), path(B); poly = pa + pb[::-1][1:-1]
    s2 = sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]))
    tri = (0, 4); verts = [(2, 0), (0, 4), (16, 0)]
    t2 = abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(verts, verts[1:] + verts[:1])))
    check("Z4 the 1^7 vs 2^2 3^4 recombination bigon is the lattice triangle (2,0),(0,4),(16,0): twice-area 56, area 28 = 4 x |det(D2,D3)|", abs(s2) == 56 == t2 and pa[-1] == pb[-1] == (16, 0) and [p for p in pb[1:-1] if p[1] == 0] == [])
    # omega potential: swap changes omega by exactly the pair determinant; weighted inversion formula
    def omega(w):
        ds = [dd(N) for N in w]; return sum(ds[i][0] * ds[j][1] - ds[i][1] * ds[j][0] for i in range(len(ds)) for j in range(i + 1, len(ds)))
    det23 = dd(2)[0] * dd(3)[1] - dd(2)[1] * dd(3)[0]
    vals = {}
    for w in set(permutations(B)):
        inv = sum(1 for i in range(6) for j in range(i + 1, 6) if w[i] == 3 and w[j] == 2)
        vals[w] = omega(w); assert vals[w] == det23 * (8 - 2 * inv), (w, vals[w])
    check("Z4 omega(w) = det(D2,D3)(c2 c3 - 2 inv(w)) on arrangements of 2^2 3^4: values %s, step 14, det = %d" % (sorted(set(vals.values())), det23), sorted(set(vals.values())) == list(range(-56, 57, 14)) and det23 == -7)
    rng = random.Random(6); ok = True
    for _ in range(300):
        u, v = ((1, 8, 8), (2, 2, 2, 2)) if rng.random() < .5 else (B, A)
        pre = tuple(rng.choice([1, 2, 3, 8]) for _ in range(rng.randint(0, 4))); suf = tuple(rng.choice([1, 2, 3, 8]) for _ in range(rng.randint(0, 4)))
        ok &= (omega(pre + u + suf) - omega(pre + v + suf)) == (omega(u) - omega(v))
    check("Z4 omega is a potential: its change under a block replacement depends only on (u,v), not on the context", ok)
    # join example
    L = {2: 1, 8: 1, 63: 1}; R = {5: 1, 9: 1, 35: 1}
    for m in (280, 840):
        U = words(m, L); V = words(m, R); W = U + V
        ends = {states(m, w)[-1] for w in W}
        idx = {w: i for i, w in enumerate(W)}; E = set()
        for w in W:
            for i in range(len(w) - 1):
                t = w[:i] + (w[i + 1], w[i]) + w[i + 2:]
                if t in idx and w != t: E.add(frozenset((w, t)))
        sw = len(E)
        for w in W:
            if w in set(U):
                for t in V: E.add(frozenset((w, t)))   # block replacement 2.8.63 <-> 5.9.35 (arrangements)
        # a rewrite needs the whole word to be a block: both contents are exactly the block
        par = list(range(len(W)))
        def f(z):
            while par[z] != z: par[z] = par[par[z]]; z = par[z]
            return z
        for e in E:
            a, b = tuple(e)
            par[f(idx[a])] = f(idx[b])
        check("Z4 join example m=%d: %d histories, one endpoint, E=%d edges (swaps %d) -> loop rank E-V+components = %d" % (m, len(W), len(E), sw, len(E) - len(W) + len({f(i) for i in range(len(W))})), len(ends) == 1 and len(W) == 4 and len({f(i) for i in range(len(W))}) == 1)


def shard_Z5(full=False):
    """occurrence events"""
    def inD(d, m): return all(vp(m, p) >= 2 * a for p, a in pf(d).items())
    def churn(rho):
        V = sum(abs(rho[i] - rho[i - 1]) for i in range(1, len(rho))); return (V - abs(rho[-1] - rho[0])) // 2
    A = (1,) * 7; B = (2, 2, 3, 3, 3, 3)
    sA, sB = states(4, A), states(4, B)
    check("Z5 C-B4: chi_2(h_A) = 0, chi_2(h_B) = 1, incidence of 2 along h_B = 1,0,0,1,1,1,1", churn([inD(2, m) for m in sA]) == 0 and churn([inD(2, m) for m in sB]) == 1 and [int(inD(2, m)) for m in sB] == [1, 0, 0, 1, 1, 1, 1])
    # monotone lemma + dip lemma + necessary churn
    bad = n = 0; cnt_min = None
    for a in range(0, 13):
        for b in range(0, 9):
            m = 2 ** a * 3 ** b
            cands = [2 ** i * 3 ** j for i in range(0, a // 2 + 8) for j in range(0, b // 2 + 4) if 2 ** i * 3 ** j >= 2]
            if adm(m, A):
                st = states(m, A); bad += any(churn([inD(d, x) for x in st]) for d in cands)
            for w in set(permutations(B)):
                if not adm(m, w): continue
                n += 1; st = states(m, w)
                ch = [d for d in cands if churn([inD(d, x) for x in st])]
                bad += (len(ch) == 0); cnt_min = len(ch) if cnt_min is None else min(cnt_min, len(ch))
    check("Z5 necessary churn: for EVERY source (v2<=12,v3<=8) and EVERY arrangement of 2^2 3^4 some occurrence index has chi >= 1, while h_A has chi = 0 for all indices  (%d source-arrangement pairs; minimum #churning indices %d)" % (n, cnt_min), bad == 0 and n > 500, bad)
    # the combinatorial core: walks with two +2 steps and four -1 steps from 0 to 0 either exceed b by >=2, or (max=+1 / min<=-1) in a parity-resolved way
    ok = True
    for arr in set(permutations(B)):
        walk = [0]
        for N in arr: walk.append(walk[-1] + (2 if N == 2 else -1))   # v3 increments: R(2): +2 ; R(3): -1
        for b in range(0, 9):
            if arr[0] == 3 and b < 1: continue
            top = b // 2 * 2
            lost = (min(walk) + b < top) and b >= top
            born = max(walk) + b >= (b // 2 + 1) * 2
            ok &= (lost or born)
    check("Z5 case analysis of the v3-walk: every arrangement either dips below the top level 2*floor(b/2) of v3 or transiently reaches 2*(floor(b/2)+1)", ok)
    # swap Lipschitz and swap of equal ends
    rng = random.Random(4); n = bad = 0
    for _ in range(3000):
        lab = [rng.choice([1, 2, 3, 8, 9, 14]) for _ in range(rng.randint(2, 7))]; m = 1
        for p in (2, 3, 5, 7): m *= p ** rng.randint(0, 7)
        if not adm(m, lab): continue
        i = rng.randrange(len(lab) - 1); w2 = lab[:i] + [lab[i + 1], lab[i]] + lab[i + 2:]
        if not adm(m, w2): continue
        s1, s2 = states(m, lab), states(m, w2)
        for d in {2, 3, 4, 6, 9, 12}:
            n += 1; bad += abs(churn([inD(d, x) for x in s1]) - churn([inD(d, x) for x in s2])) > 1
    check("Z5 adjacent swap changes chi_d by at most 1 (%d tests)" % n, bad == 0)
    check("Z5 chi_d <= floor(l/2) for a history of length l (variation <= l)", all(churn(r) <= len(r) // 2 for r in product((0, 1), repeat=7)))


def shard_Z6(full=False):
    """FIELD-I: own implementation of D, C; strand geometry"""
    def D(x):
        a, b = x.numerator, x.denominator; sq = [1]
        for p, e in pf(a).items(): sq = [t * p ** i for t in sq for i in range(e // 2 + 1)]
        return sorted(d for d in sq if d >= 2 and (d - 1) % b == 0)
    def C(x):
        d = D(x)
        if not d: return None
        L = 1
        for t in d: L = lcm(L, t)
        G = 0
        for t in d: G = gcd(G, t - 1)
        return x + Fraction(L * L, G)
    def strand(x, n):
        xs = [Fraction(x)]
        for _ in range(n):
            y = C(xs[-1])
            if y is None: break
            xs.append(y)
        return xs
    cc = load("results/FIELD_CROSSCHECK.json")
    check("Z6 D(x) of the adapter equals FIELD-I's own admissible_d on %d states (recorded cross-check, FIELD-I source not shipped)" % cc["compared_states"], cc["D_mismatches"] == 0 and cc["compared_states"] > 20000)
    # rigid orbit
    good = True; shapes = set()
    for x0 in [4, 8, 16, 36, 100, 144, Fraction(9, 2), 18, 20, 387, 495, Fraction(495, 2), 522, 250, 40, 160]:
        xs = strand(Fraction(x0), 90); e = None
        for n in range(len(xs) - 3):
            if all(xs[i + 3] == 4 * xs[i] for i in range(n, len(xs) - 3)): e = n; break
        good &= e is not None
        if e is None: continue
        shapes.add(tuple(xs[e + i + 1] / xs[e + i] for i in range(3)))
        good &= all(xs[i + 3] == 4 * xs[i] for i in range(e, len(xs) - 3))
        good &= {xs[e + i + 1] / xs[e + i] for i in range(3)} == {Fraction(2), Fraction(3, 2), Fraction(4, 3)}
    check("Z6 sample strands reach the rigid regime x_{n+3} = 4 x_n; the three step ratios are exactly {2, 3/2, 4/3} in cyclic order (shapes %s)" % sorted(map(lambda s: tuple(map(str, s)), shapes)), good)
    # valuation displacement of a period is 2 e_2; rank 2
    def vals(x): return {p: vp(x.numerator, p) - vp(x.denominator, p) for p in set(pf(x.numerator)) | set(pf(x.denominator))}
    xs = strand(Fraction(387), 60); ok = True
    for i in range(20, 50):
        a, b = vals(xs[i]), vals(xs[i + 3])
        ok &= all(b.get(p, 0) - a.get(p, 0) == (2 if p == 2 else 0) for p in set(a) | set(b))
    check("Z6 rigid orbit: v(x_{n+3}) - v(x_n) = 2 e_2 exactly; only primes 2,3 move inside the period", ok)
    # plateau / arithmetic progression
    xs = strand(Fraction(1369, 9), 175); delta = Fraction(37 ** 2, 36)
    ap = all(xs[n + 1] - xs[n] == delta for n in range(0, 139)) and all(xs[n] == delta * (n + 4) for n in range(0, 141))
    ent = next(n for n in range(len(xs) - 3) if all(xs[i + 3] == 4 * xs[i] for i in range(n, len(xs) - 3)))
    check("Z6 1369/9: transient is the arithmetic progression x_n = (37^2/36)(n+4) for 0 <= n < 140; rigid regime starts at n = %d (x_140 = 4*37^2)" % ent, ap and ent == 140 and xs[140] == 4 * 37 ** 2)
    ok = all(vp((n + 4), p) == vals(xs[n]).get(p, 0) - (vals(delta).get(p, 0)) for n in range(0, 100) for p in (2, 3, 5, 7, 11, 13))
    check("Z6 valuation law on a plateau: v_p(x_n) = v_p(delta) + v_p(n + c)  (ruler functions); strand dimension grows with the primes <= n + c", ok)
    ranks = []
    for l in (10, 20, 40, 80, 139):
        pts = [vals(x) for x in xs[:l + 1]]; P = sorted(set().union(*[set(q) for q in pts]))
        rows = [[Fraction(pts[i + 1].get(p, 0) - pts[i].get(p, 0)) for p in P] for i in range(l)]; r = 0
        for c in range(len(P)):
            piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
            if piv is None: continue
            rows[r], rows[piv] = rows[piv], rows[r]
            for i in range(len(rows)):
                if i != r and rows[i][c] != 0:
                    f_ = rows[i][c] / rows[r][c]; rows[i] = [a_ - f_ * b_ for a_, b_ in zip(rows[i], rows[r])]
            r += 1
        ranks.append((l, r, len([p for p in range(2, 4 + l + 1) if all(p % q for q in range(2, int(p ** .5) + 1))])))
    check("Z6 plateau displacement rank = number of primes <= c+l on the long windows %s (l, rank, pi(c+l))" % ranks, all(r == k for l, r, k in ranks))
    S = load("results/FIELD_STRANDS.json")["sample"]["counts"]
    check("Z6 recorded sample: %s" % S, S.get("dies", 0) == 0 and S.get("rigid_period3_x4", 0) > 500 and S.get("not_period3", 0) == 0)


def shard_Z7(full=False):
    """bridge facts + builder cross-check + documents"""
    # C^3 = T_1 on rigid orbits is covered by Z6; here the one-step obstruction and the stride-3 relation
    ok = all((N + 1) ** 2 >= 4 * N for N in range(1, 100000)) and all((N + 1) ** 2 > 4 * N for N in range(2, 100000))
    check("Z7 R(N) >= 4 for all N >= 1 with equality only at N = 1 ((N+1)^2 - 4N = (N-1)^2): no rigid FIELD-I step ratio (<= 2) is a SELECT-II edge ratio", ok)
    B = load("results/BRIDGE.json")
    check("Z7 recorded: C^3 = T_1 on %d rigid-orbit states; R_P snapshot: SELECT-II states 4^k match FIELD-I index 3(k-1)" % B["C3_equals_T1_on_rigid_orbit"]["checked_states"],
          B["C3_equals_T1_on_rigid_orbit"]["holds"] == B["C3_equals_T1_on_rigid_orbit"]["checked_states"] and [s["FIELD_I_indices_with_equal_(v2,v3)"] for s in B["snapshot_relation_R_P_4_to_1^7"]] == [[3 * i] for i in range(8)])
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import prime_geometry as PG, dimension_tests as DT, field_adapter as FA, history_realization as HR
    c = DT.Content((2, 3, 8, 9)); check("Z7 builder Content((2,3,8,9)) agrees with the verifier on Betti at m=72 and on the active primes", tuple(c.betti_at((3, 2))) == route_betti([2, 3, 8, 9], 72) and c.act == [2, 3])
    rng = random.Random(7); ok = True
    for _ in range(300):
        C = tuple(sorted(rng.sample(range(2, 16), 4))); cc = DT.Content(C)
        for e in list(product(*[range(x + 1) for x in cc.mx]))[:6]:
            m = 1
            for p, a in zip(cc.act, e): m *= p ** a
            bb = cc.betti_at(e)
            vb = route_betti(C, m) if all(p ** a == 1 or True for p, a in zip(cc.act, e)) else None
            ok &= (bb == vb) or (bb is None and vb is None)
    check("Z7 builder route complexes = verifier route complexes on 300 random 4-label contents (up to 6 resource vectors each)", ok)
    ok = all(FA.C(Fraction(x)) is not None for x in (4, 8, 12, 16)) and FA.strand(4, 3) == [Fraction(4), Fraction(8), Fraction(12), Fraction(16)]
    check("Z7 builder FIELD-I adapter: strand(4) = 4, 8, 12, 16", ok)
    T = open(os.path.join(ROOT, "theory", "THEOREMS.md")).read(); O = open(os.path.join(ROOT, "theory", "OPEN_PROBLEMS.md")).read()
    check("Z7 THEOREMS.md uses PROVED / FINITE-EXACT / OPEN and lists B-T1..B-T12", all(w in T for w in ("PROVED", "FINITE-EXACT", "OPEN")) and all("B-T%d" % i in T for i in range(1, 13)))
    check("Z7 OPEN_PROBLEMS.md keeps SELECT-II and FIELD-I distinct and records that no dynamical equivalence is claimed", "FIELD-I" in O and "SELECT-II" in O and "conjugacy" in O)
    mfp = os.path.join(ROOT, "MANIFEST.json")
    if os.path.exists(mfp):
        mf = json.load(open(mfp))["files"]
        check("Z7 MANIFEST hashes match", all(sha(os.path.join(ROOT, p)) == h for p, h in mf.items() if p != "results/VERIFY_LAST.json"))


SHARDS = {"Z0": shard_Z0, "Z1": shard_Z1, "Z2": shard_Z2, "Z3": shard_Z3, "Z4": shard_Z4, "Z5": shard_Z5, "Z6": shard_Z6, "Z7": shard_Z7}
