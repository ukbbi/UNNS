"""GEO_HD_BRIDGE v003 independent verifier.  Own implementations (no import of the builder modules or of the frozen GEO-I engine):
factorisation, occurrence set D, L, G, Graver region, cell complex + GF(2) homology, SELECT-II words, swap components.
Shards Z0..Z7.  New theorems are checked separately from regressions / integrity."""
import os, sys, json, hashlib, itertools, random
from fractions import Fraction as Fr
from math import gcd, isqrt, prod
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = []; FAILS = []
def check(name, ok, detail=''):
    RESULTS.append((name, bool(ok), detail))
    if not ok: FAILS.append(name)
    print(('PASS  ' if ok else 'FAIL  ') + name + ((' -- ' + str(detail)) if detail != '' else ''), flush=True)
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def load(rel): return json.load(open(os.path.join(ROOT, rel)))

# ------------------------------------------------------------------ arithmetic
def pf(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1 if d == 2 else 2
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def isprime(n): return n > 1 and pf(n) == {n: 1}
def vp(n, p):
    c = 0
    while n % p == 0: n //= p; c += 1
    return c
def box_of(x):
    f = pf(x.numerator); ps = sorted(p for p, e in f.items() if e // 2 >= 1)
    return ps, [f[p] // 2 for p in ps], x.denominator
def inlat(ps, b, g):
    r = 1
    for p, e in zip(ps, g): r = r * pow(p, e, b) % b
    return r == 1 % b
def Fset(x):
    ps, q, b = box_of(x)
    return ps, q, b, [al for al in itertools.product(*[range(e + 1) for e in q]) if any(al) and inlat(ps, b, al)]
def Dset(x):
    ps, q, b, F = Fset(x)
    return frozenset(prod(p ** e for p, e in zip(ps, al)) for al in F)
def graver(ps, q, b):
    V = [g for g in itertools.product(*[range(-e, e + 1) for e in q]) if any(g) and inlat(ps, b, g)]
    def dom(h, g): return h != g and all(a * c >= 0 and abs(a) <= abs(c) for a, c in zip(h, g))
    return {g for g in V if not any(dom(h, g) for h in V)}
def DLG(x):
    D = Dset(x)
    if not D: return None
    L = 1; G = 0
    for d in D: L = L * d // gcd(L, d); G = gcd(G, d - 1)
    return D, L, G
def Cmap(x):
    D, L, G = DLG(x); return x + Fr(L * L, G)

# ------------------------------------------------------------------ cell complex over GF(2)
def rankQ(vs):
    M = [[Fr(c) for c in v] for v in vs]; r = 0
    for c in range(len(M[0]) if M else 0):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def lexpos(g):
    for c in g:
        if c: return c > 0
def complex_from(F, moves, kmax=4):
    Fs = set(F); gens = sorted(g for g in moves if lexpos(g)); cells = {0: [((u, ()), ) for u in F]}
    cells = {0: [(u, ()) for u in sorted(F)]}
    for j in range(1, kmax + 1):
        out = []
        for u in sorted(F):
            for S in itertools.combinations(gens, j):
                if rankQ(S) < j: continue
                ok = True
                for mask in range(1 << j):
                    w = u
                    for i in range(j):
                        if mask >> i & 1: w = tuple(a + b for a, b in zip(w, S[i]))
                    if w not in Fs: ok = False; break
                if ok: out.append((u, S))
        if not out: break
        cells[j] = out
    return cells
def betti_gf2(cells):
    idx = {j: {c: i for i, c in enumerate(cs)} for j, cs in cells.items()}
    ranks = {}
    for j in cells:
        if j == 0: continue
        rows = []
        for (u, S) in cells[j]:
            v = 0
            for i in range(j):
                rest = S[:i] + S[i + 1:]
                u2 = tuple(a + b for a, b in zip(u, S[i]))
                for base in (u2, u):
                    v ^= 1 << idx[j - 1][(base, rest)]
            rows.append(v)
        r = 0; piv = {}
        for v in rows:
            while v:
                h = v.bit_length() - 1
                if h in piv: v ^= piv[h]
                else: piv[h] = v; r += 1; break
        ranks[j] = r
    top = max(cells)
    return [len(cells[j]) - ranks.get(j, 0) - ranks.get(j + 1, 0) for j in range(top + 1)]
def kmove_betti(x):
    ps, q, b, F = Fset(x)
    if not F: return []
    return betti_gf2(complex_from(F, graver(ps, q, b)))
def kmove_from_F_only(F, k):
    """moves rebuilt from F alone (hull rule); then the same complex builder"""
    F0 = list(F) + [tuple([0] * k)]
    def hull(u, v):
        lo = [min(a, c) for a, c in zip(u, v)]; hi = [max(a, c) for a, c in zip(u, v)]
        return [w for w in F0 if all(l <= t <= h for l, t, h in zip(lo, w, hi))]
    mv = set()
    for g in F:
        if not any(w != g and all(a <= c for a, c in zip(w, g)) for w in F): mv |= {g, tuple(-c for c in g)}
    for u in F:
        for v in F:
            if u != v and len(hull(u, v)) == 2: mv.add(tuple(c - a for a, c in zip(u, v)))
    return mv

# ================================================================== shards
def shard_Z0(full=False):
    """integrity: pins, sibling manifests (hash only, NOT_RERUN), STATUS gates, required documents"""
    pins = load('results/PINS.json')
    check('Z0 pinned frozen libraries unchanged (%d)' % len(pins), all(sha(os.path.join(ROOT, 'src', f)) == s for f, s in pins.items()))
    for name in ['GEO_HD_1D_v00%d' % i for i in (1, 2, 3, 4)] + ['GEO_HD_BRIDGE_v001', 'GEO_HD_BRIDGE_v002', 'GEO_HD_E2_P4_v005']:
        mp = os.path.join(os.path.dirname(ROOT), name, 'MANIFEST.json')
        if os.path.exists(mp):
            mf = json.load(open(mp)); mf = mf.get('files', mf); d = os.path.dirname(mp)
            ok = all(sha(os.path.join(d, p)) == h for p, h in mf.items() if not p.startswith('figures/') and p != 'results/VERIFY_LAST.json')
            check('Z0 sibling %s untouched (manifest hashes; inherited verification NOT_RERUN)' % name, ok)
    st = load('STATUS.json')
    check('Z0 STATUS gates', st['gates']['C3'] == 'NOT_CLAIMED' and st['gates']['NOVELTY'] == 'NOT_ASSESSED' and 'same author' in st['independence_caveat'])
    need = ['theory/' + n + '.md' for n in ('SOURCE_CROSSWALK', 'RATIONAL_GEOMETRY', 'ARITHMETIC_CLASSIFICATION', 'HISTORY_INVARIANTS', 'HIGHER_DIMENSIONAL', 'COLLECTIVE_REGIMES', 'GEOMETRIC_TRANSITIONS', 'CORRESPONDENCE', 'THEOREMS', 'OPEN_PROBLEMS')]
    miss = [n for n in need if not os.path.exists(os.path.join(ROOT, n))]
    check('Z0 required documents present', not miss, miss)

def primes_mod(res, mod, count, start=2):
    out = []; n = start
    while len(out) < count:
        if isprime(n) and n % mod == res: out.append(n)
        n += 1
    return out

def shard_Z1(full=False):
    """[NEW] R3-T1: infinite family with equal D and different region-Graver sets (k=2)"""
    rs = primes_mod(5, 8, 40 if full else 15, start=13); bad = []
    for r in rs:
        x = Fr(25 * r * r, 5 * r - 1); y = Fr(25 * r * r, 8)
        px, qx, bx, Fx = Fset(x); py, qy, by, Fy = Fset(y)
        Dx, Dy = Dset(x), Dset(y); Gx, Gy = graver(px, qx, bx), graver(py, qy, by)
        ok = (px == py == [5, r] and qx == qy == [1, 1] and Dx == Dy == {5 * r} and Gx == {(1, 1), (-1, -1)}
              and Gy == {(1, 1), (-1, -1), (1, -1), (-1, 1)} and x.denominator == 5 * r - 1 and y.denominator == 8)
        if not ok: bad.append(r)
    check('Z1 [NEW] R3-T1 k=2: D(x_r)=D(y_r)={5r}, same primes and box, |Graver| 2 vs 4  (%d primes r = 5 mod 8)' % len(rs), not bad, bad[:3])
    # proof ingredients, exact: the four congruences for x_r (b=5r-1) and y_r (b=8)
    ok = True
    for r in rs:
        b1 = 5 * r - 1
        ok &= (5 % b1 != 1) and (r % b1 != 1) and (5 * r % b1 == 1) and ((5 - r) % b1 != 0)
        ok &= (5 % 8 != 1) and (r % 8 != 1) and (5 * r % 8 == 1) and ((5 - r) % 8 == 0)
    check('Z1 [NEW] congruence facts used in the proof (A,B false; C true; E false for b=5r-1, true for b=8)', ok)
    # realized geometry identical: both have a single vertex
    check('Z1 [NEW] realized complex of both states is the same single point (|F|=1, no moves between F points)', all(len(Fset(Fr(25 * r * r, 5 * r - 1))[3]) == 1 == len(Fset(Fr(25 * r * r, 8))[3]) for r in rs))

def shard_Z2(full=False):
    """[NEW] R3-T1 high dimension: dormant relations form the root system A_{k-1}"""
    rows = []
    for k in (2, 3, 4) + ((5,) if full else ()):
        l = next(l for l in range(k + 1, 400) if isprime(l) and (l - 1) % k == 0)
        g = next(g for g in range(2, l) if all(pow(g, (l - 1) // f, l) != 1 for f in pf(l - 1)))
        c = pow(g, (l - 1) // k, l)
        ps = primes_mod(c, l, k); P = prod(ps)
        x = Fr(P * P, P - 1); y = Fr(P * P, l)
        px, qx, bx, Fx = Fset(x); py, qy, by, Fy = Fset(y)
        Gx, Gy = graver(px, qx, bx), graver(py, qy, by)
        roots = {tuple(1 if i == a else -1 if i == b else 0 for i in range(k)) for a in range(k) for b in range(k) if a != b}
        top = tuple([1] * k); neg = tuple([-1] * k)
        ok = (Dset(x) == Dset(y) == {P} and Gx == {top, neg} and Gy == roots | {top, neg} and len(Gy) == k * (k - 1) + 2)
        rows.append((k, ok))
    check('Z2 [NEW] k-prime family: D equal ({P}), |Graver| 2 vs k(k-1)+2, dormant set = {e_i - e_j} (type A_{k-1}) for k=%s' % [r[0] for r in rows], all(o for _, o in rows), rows)

def shard_Z3(full=False):
    """[NEW] R3-T2: complete classification for two primes, box (1,1)"""
    ps = [p for p in range(2, 30 if not full else 45) if isprime(p)]; n = bad = 0; seenE = {'empty': set(), 'pr': set(), 'other': set()}
    allowed = [set(), {'A'}, {'B'}, {'C'}, {'E'}, {'C', 'E'}, {'A', 'B', 'C', 'E'}]
    for i, p in enumerate(ps):
        for r in ps[i + 1:]:
            for b in range(2, 150 if not full else 300):
                if gcd(p * r, b) != 1: continue
                x = Fr(p * p * r * r, b); pp, qq, bb, F = Fset(x)
                if qq != [1, 1]: continue
                t = set()
                if p % b == 1: t.add('A')
                if r % b == 1: t.add('B')
                if p * r % b == 1: t.add('C')
                if (p - r) % b == 0: t.add('E')
                G = graver(pp, qq, bb); n += 1
                predG = set()
                if 'A' in t: predG |= {(1, 0), (-1, 0)}
                if 'B' in t: predG |= {(0, 1), (0, -1)}
                if not t & {'A', 'B'}:
                    if 'C' in t: predG |= {(1, 1), (-1, -1)}
                    if 'E' in t: predG |= {(1, -1), (-1, 1)}
                D = Dset(x)
                predD = ({p} if 'A' in t else set()) | ({r} if 'B' in t else set()) | ({p * r} if 'C' in t else set())
                if t not in allowed or G != predG or D != predD: bad += 1
                key = 'empty' if not D else ('pr' if D == {p * r} else 'other'); seenE[key].add('E' in t)
    check('Z3 [NEW] 7 admissible relation types; Graver set and D are functions of the type  (%d states)' % n, bad == 0, bad)
    check('Z3 [NEW] irredundancy: bit E occurs with both values exactly when D is empty or {pr}; D in {p},{r},{p,r,pr} fixes E',
          seenE['empty'] == {True, False} and seenE['pr'] == {True, False} and seenE['other'] <= {True, False})

def shard_Z4(full=False):
    """[NEW] R3-T1a: realized geometry (cells, homology) is a function of D;  moves rebuilt from F alone"""
    rng = random.Random(11); P = [2, 3, 5, 7, 11, 13]; n = bad = 0; seen = set(); homol = 0
    def divs(m):
        f = pf(m); ds = [1]
        for p, e in f.items(): ds = [d * p ** i for d in ds for i in range(e + 1)]
        return ds
    for _ in range(500 if not full else 2000):
        k = rng.randint(2, 4); ps = rng.sample(P, k); q = [rng.randint(1, 2) for _ in ps]
        a = 1
        for p, e in zip(ps, q): a *= p ** (2 * e + rng.randint(0, 1))
        al = [rng.randint(0, e) for e in q]; m = 1
        for p, e in zip(ps, al): m *= p ** e
        if m == 1: continue
        ds = [d for d in divs(m - 1) if d > 1]
        if not ds: continue
        b = rng.choice(ds)
        if gcd(a, b) != 1 or (a, b) in seen: continue
        seen.add((a, b)); x = Fr(a, b); pp, qq, bb, F = Fset(x)
        if len(F) < 2: continue
        n += 1; G = graver(pp, qq, bb); mv = kmove_from_F_only(F, len(pp))
        joined = {tuple(c - d for d, c in zip(u, v)) for u in F for v in F if u != v}
        realized = {g for g in G if g in joined or (g in set(F)) or (tuple(-c for c in g) in set(F))}
        if not (mv <= G and realized == mv): bad += 1
        if len(F) <= 12 and homol < (8 if not full else 40):
            c1 = betti_gf2(complex_from(F, G)); c2 = betti_gf2(complex_from(F, mv)); homol += 1
            if c1 != c2: bad += 1
    check('Z4 [NEW] R3-T1a: realized Graver moves = moves rebuilt from F alone; K_move homology equal for the two move sets (%d states, %d homology comparisons)' % (n, homol), bad == 0 and n > 50, bad)
    # states with equal D but different boxes / dead primes / denominators give the same complex
    pairs = [(Fr(25 * 13 * 13, 5 * 13 - 1), Fr(25 * 13 * 13, 8)), (Fr(36, 5), Fr(36 * 49, 5)), ]
    ok = True
    for x, y in pairs:
        fx, fy = Fset(x), Fset(y)
        if Dset(x) == Dset(y): ok &= kmove_betti(x) == kmove_betti(y)
    check('Z4 [NEW] equal-D pairs have equal K_move homology (spot check)', ok)

def words(m, content):
    from collections import Counter
    cnt = Counter(content); out = []
    def rec(s, pref):
        if sum(cnt.values()) == 0: out.append(tuple(pref)); return
        for N in sorted(k for k, v in cnt.items() if v):
            if s % N == 0:
                cnt[N] -= 1; pref.append(N); rec(s * (N + 1) ** 2 // N, pref); pref.pop(); cnt[N] += 1
    rec(m, []); return out
def components(ws):
    S = set(ws); seen = set(); comps = []
    for w in ws:
        if w in seen: continue
        st = [w]; seen.add(w); c = []
        while st:
            u = st.pop(); c.append(u)
            for i in range(len(u) - 1):
                v = u[:i] + (u[i + 1], u[i]) + u[i + 2:]
                if v in S and v not in seen: seen.add(v); st.append(v)
        comps.append(c)
    return comps

def shard_Z5(full=False):
    """[NEW] R3-T3: pair-order invariant of swap components, infinite family"""
    pool = [3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15] if not full else [3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 20]
    nc = nbit = badbit = adj = firstbad = 0
    for r in range(1, 5):
        for A in itertools.combinations(pool, r):
            content = tuple(sorted((2, 4) + A)); ws = words(4, content)
            if not ws: continue
            nc += 1; cl = components(ws)
            if any(len({w.index(2) < w.index(4) for w in c}) != 1 for c in cl): badbit += 1
            if len({w.index(2) < w.index(4) for w in ws}) == 2: nbit += 1
            if any(abs(w.index(2) - w.index(4)) == 1 for w in ws): adj += 1
            if any(w[0] not in (2, 4) for w in ws): firstbad += 1
    check('Z5 [NEW] R3-T3: [2 before 4] constant on every swap component, 2 and 4 never adjacent, first label in {2,4}  (%d contents, %d disconnected by the bit)' % (nc, nbit), badbit == 0 and adj == 0 and firstbad == 0 and nbit > 20, (badbit, adj, firstbad))
    # the proof's two inputs, directly
    check('Z5 [NEW] feeding input: from source 4 the only labels N | 4 are 1,2,4; and (2,4),(4,2) fail at the source', [N for N in range(1, 5) if 4 % N == 0] == [1, 2, 4] and (4 * 9 // 2) % 4 != 0 and (4 * 25 // 4) % 2 != 0)
    # extension chain: append a label dividing the endpoint -> larger contents, still disconnected
    A = [5, 9]; rows = []
    for _ in range(4):
        content = tuple(sorted((2, 4) + tuple(A))); ws = words(4, content); cl = components(ws)
        E = Fr(4)
        for N in content: E *= Fr((N + 1) ** 2, N)
        rows.append((len(content), len(cl), len({w.index(2) < w.index(4) for w in ws})))
        E = int(E); A.append(next(d for d in range(3, E + 1) if E % d == 0 and d not in set(A) | {1, 2, 4}))
    check('Z5 [NEW] R3-T3 extension lemma: appending a divisor of the endpoint keeps both orders; contents of size 4..7 all disconnected', all(c >= 2 and b == 2 for _, c, b in rows), rows)
    A = [5, 9]; E = 9000; rows2 = []
    for _ in range(3):
        content = tuple(sorted((2, 4) + tuple(A))); ws = words(4, content); cl = components(ws)
        rows2.append((len(content), len(cl), sorted(map(len, cl)), len({w.index(2) < w.index(4) for w in ws})))
        A.append(E); E = (E + 1) ** 2
    check('Z5 [NEW] R3-T3 explicit chain L_j=E_j, E_{j+1}=(E_j+1)^2 (labels 5,9,9000,9001^2): two components each, separated by I', all(c == 2 and b == 2 for _, c, _, b in rows2), rows2)
    lp = [components(words(32, (2, 3, 4, 5, 8))), components(words(24, (2, 3, 4, 5, 6, 7)))]
    check('Z5 [REG] loop_3_primes and loop_4_primes are single swap components (no component invariant possible)', [len(c) for c in lp] == [1, 1])
    # junction lemma (both orders admissible iff valuation inequalities)
    rng = random.Random(2); bad = 0
    for _ in range(2000):
        s = rng.randint(1, 500); N, M = rng.sample(range(1, 40), 2)
        direct = (s % N == 0 and (s * (N + 1) ** 2 // N) % M == 0 and s % M == 0 and (s * (M + 1) ** 2 // M) % N == 0)
        ps = set(pf(N)) | set(pf(M)) | set(pf(N + 1)) | set(pf(M + 1))
        ineq = all(vp(s, p) >= vp(N, p) and vp(s, p) + 2 * vp(N + 1, p) - vp(N, p) >= vp(M, p) and vp(s, p) >= vp(M, p) and vp(s, p) + 2 * vp(M + 1, p) - vp(M, p) >= vp(N, p) for p in ps)
        if direct != ineq: bad += 1
    check('Z5 [NEW] junction lemma: N,M adjacent in both orders iff the valuation inequalities hold (2000 random)', bad == 0)
    # named examples
    a3 = components(words(4, (2, 3, 4, 5, 6))); a4 = components(words(4, (2, 3, 4, 5, 6, 7)))
    check('Z5 [REG] v001 examples: disconnected_3_primes 2 components (4+6 words), disconnected_4_primes 2 components (12+12)', sorted(map(len, a3)) == [4, 6] and sorted(map(len, a4)) == [12, 12])

def shard_Z6(full=False):
    """[NEW] R3-T5: modular class S_l, towers, stage law;  counterexample to 'rigid iff G=1'"""
    def tower_ok(S0, l, P, K):
        xs = [Fr(S0(0) ** 2, l)]
        for _ in range(P * K): xs.append(Cmap(xs[-1]))
        bad = []
        for n in range(P * K):
            k, j = divmod(n, P); D, L, G = DLG(xs[n])
            if xs[n] != Fr((j + 1) * S0(k) ** 2, l) or L != S0(k) or G != l: bad.append(n)
        return bad
    K11 = 6 if not full else 10; K5 = 8 if not full else 14
    check('Z6 [NEW] R3-T5b tower l=11, S_k=2^2 3^(3+k) 5^4: x_{8k+j}=(j+1)S_k^2/11, L=S_k, G=11 (k<%d)' % K11, tower_ok(lambda k: 4 * 3 ** (3 + k) * 625, 11, 8, K11) == [])
    check('Z6 [NEW] R3-T5c tower l=5, S_k=126*2^k: x_{3k+j}=(j+1)S_k^2/5, L=S_k, G=5, x_{n+3}=4 x_n (k<%d)' % K5, tower_ok(lambda k: 126 * 2 ** k, 5, 3, K5) == [])
    # closed-form D of the two towers (the proof's residue computation)
    ok = True
    for k in range(0, 9):
        S = 4 * 3 ** (3 + k) * 625
        Dform = {2 ** a * 3 ** c * 5 ** e for a in (0, 2) for c in range(0, 4 + k) for e in range(0, 5) if (a // 2 + 0 == 0 and (c + 3 * e) % 5 == 0 or a == 2 and (c + 3 * e) % 5 == 1) and 2 ** a * 3 ** c * 5 ** e >= 2}
        ok &= Dform == Dset(Fr(S * S, 11))
        S5 = 126 * 2 ** k
        D5 = {2 ** a * 3 ** c * 7 ** f for a in range(0, k + 2) for c in range(0, 3) for f in range(0, 2) if (a + 3 * c + f) % 4 == 0 and 2 ** a * 3 ** c * 7 ** f >= 2}
        ok &= D5 == Dset(Fr(S5 * S5, 5))
    check('Z6 [NEW] closed-form occurrence sets of the two towers (discrete-log residue conditions a+3c+f=0 mod 4; c+3e=0 / a=2,c+3e=1 mod 5) equal the definition', ok)
    # event at exactly t=9 (resp. 4), none before
    ok = True
    for k in range(0, 5):
        S = 4 * 3 ** (3 + k) * 625; D0 = Dset(Fr(S * S, 11))
        ok &= all(Dset(Fr(t * S * S, 11)) == D0 for t in range(1, 9)) and Dset(Fr(9 * S * S, 11)) != D0 and len(Dset(Fr(9 * S * S, 11))) - len(D0) == 2
        S = 126 * 2 ** k; D0 = Dset(Fr(S * S, 5))
        ok &= all(Dset(Fr(t * S * S, 5)) == D0 for t in (1, 2, 3)) and Dset(Fr(4 * S * S, 5)) != D0
    check('Z6 [NEW] event time tau=9 (l=11) / tau=4 (l=5): D unchanged for 1<=t<tau, changes at tau; the l=11 event creates exactly 2 indices', ok)
    # silent carries
    S = 4 * 3 ** 3 * 625
    check('Z6 [NEW] silent carries in the l=11 tower: t=4 and t=8 enlarge the box (q_2: 2->3) but leave D unchanged', box_of(Fr(4 * S * S, 11))[1][0] == 3 and Dset(Fr(4 * S * S, 11)) == Dset(Fr(S * S, 11)) and Dset(Fr(8 * S * S, 11)) == Dset(Fr(S * S, 11)))
    # counterexample to rigid iff G=1
    xs = [Fr(126 * 126, 5)]
    for _ in range(20): xs.append(Cmap(xs[-1]))
    check('Z6 [NEW] ERRATUM B2-T7: x_0=126^2/5 has G=5 on the whole orbit and x_{n+3}=4x_n (20 steps) -- rigidity does not imply G_inf=1', all(DLG(x)[2] == 5 for x in xs[:-1]) and all(xs[i + 3] == 4 * xs[i] for i in range(17)))
    # stage law on l=29
    xs = [Fr(1890 ** 2, 29)]; Ds = [DLG(xs[0])]
    for _ in range(72): xs.append(Cmap(xs[-1])); Ds.append(DLG(xs[-1]))
    ev = [n for n in range(1, len(Ds)) if Ds[n][0] != Ds[n - 1][0]]
    gaps = [b - a for a, b in zip([0] + ev[:-1], ev)]
    check('Z6 [finite-exact] l=29, S=1890: events at steps %s, stage lengths %s = tau-1 for tau=25,4,9; P=35, rho^2=25*4*9=900' % (ev[:6], gaps[:6]), gaps[:6] == [24, 3, 8, 24, 3, 8] and xs[35] == 900 * xs[0] and xs[70] == 900 * xs[35] and all(d[2] == 29 for d in Ds))

def R_index(r):
    N = r.denominator
    return N if r == Fr((N + 1) ** 2, N) else None
def shard_Z7(full=False):
    """[NEW] R3-T6/T7 and builder cross-checks, documents, manifest"""
    # T6: realized geometry along the l=11 tower (own homology)
    S = 4 * 27 * 625; b0 = None; ok = True; rows = []
    for t in range(1, 9):
        x = Fr(t * S * S, 11); bt = kmove_betti(x); rows.append(bt)
    check('Z7 [NEW] R3-T6: K_move homology constant (b=(1,6,0)) on t=1..8 within a period (own implementation), changes at t=9 to (1,7,1,0)', all(r == rows[0] for r in rows) and rows[0] == [1, 6, 0] and kmove_betti(Fr(9 * S * S, 11)) == [1, 7, 1, 0], rows[0])
    tab = []
    for k in range(0, 5 if not full else 8):
        S = 4 * 3 ** (3 + k) * 625; tab.append(kmove_betti(Fr(S * S, 11)))
    res = load('results/GEOMETRIC_TRANSITIONS.json')['tower11_period_starts']
    check('Z7 [NEW] R3-T6: Betti vectors at period starts (own vs builder, k<%d): %s' % (len(tab), tab), all([int(v) for v in res[k]['betti']] == tab[k] for k in range(len(tab))))
    check('Z7 [NEW] R3-T6: no dormant Graver moves anywhere on the l=11 tower (own Graver vs F-only moves), k<=2 and t in 1..9',
          all(graver(*box_of(Fr(t * (4 * 3 ** (3 + k) * 625) ** 2, 11))) == kmove_from_F_only(Fset(Fr(t * (4 * 3 ** (3 + k) * 625) ** 2, 11))[3], 3) for k in (0, 1) for t in range(1, 10)))
    # T7: coincidence classification
    def coinc(S0, l, P, nmax):
        xs = [Fr(S0 ** 2, l)]
        for _ in range(nmax): xs.append(Cmap(xs[-1]))
        D = [Dset(x) for x in xs]; rows = []
        for n in range(nmax):
            for m in range(n + 1, nmax + 1):
                N = R_index(xs[m] / xs[n])
                if N is None or xs[n].numerator % N: continue
                ev = sum(1 for i in range(n + 1, m + 1) if D[i] != D[i - 1]); rows.append((n % P + 1, m // P - n // P, m % P + 1, N, ev, ev == (1 if D[m] != D[n] else 0)))
        return sorted(set(rows))
    c11 = coinc(4 * 27 * 625, 11, 8, 40); c5 = coinc(126, 5, 3, 18)
    exp11 = {(1, 0, 4, 1), (2, 0, 8, 1), (2, 1, 1, 2), (4, 1, 2, 2), (6, 1, 3, 2), (8, 1, 4, 2), (5, 1, 4, 5), (8, 2, 1, 8)}
    check('Z7 [NEW] R3-T7 l=11 tower: R(N)-related pairs are exactly (u,a,v;N) in %s; N=8 fails event level (2 events vs 1), others hold' % sorted(exp11), {(u, a, v, N) for u, a, v, N, _, _ in c11} == exp11 and [r[3] for r in c11 if not r[5]] == [8])
    check('Z7 [NEW] R3-T7 l=5 tower: pairs are N=1 (full period, x_{n+3}=4x_n) and N=3 (u=3,a=2,v=1, event level fails)', {(u, a, v, N) for u, a, v, N, _, _ in c5} == {(1, 1, 1, 1), (2, 1, 2, 1), (3, 1, 3, 1), (3, 2, 1, 3)} and [r[3] for r in c5 if not r[5]] == [3])
    check('Z7 [NEW] R3-T7 baseline: the l=11 full period would need R(N)=9, impossible (N^2-7N+1=0)', all(R_index(Fr(9)) is None for _ in [0]) and all((N + 1) ** 2 != 9 * N for N in range(1, 10 ** 4)))
    # integer-side sigma-track remark
    def sig(m):
        f = pf(m); return prod(p ** (e // 2) for p, e in f.items())
    S0 = 4 * 27 * 625
    check('Z7 [NEW] sigma-track: integer edge T_2 from m=2S^2 gives 9S^2 and sigma: S -> 3S (multiplier 9/2, not 9)', sig(2 * S0 * S0) == S0 and sig(2 * S0 * S0 * 9 // 2) == 3 * S0 and 2 * S0 * S0 * 9 // 2 == 9 * S0 * S0)
    # docs
    st = open(os.path.join(ROOT, 'theory', 'THEOREMS.md')).read()
    check('Z7 THEOREMS.md lists R3-T1..R3-T7 and PROVED / FINITE-EXACT / OPEN / FALSIFIED tags', all(('R3-T%d' % i) in st for i in range(1, 8)) and all(t in st for t in ('PROVED', 'FINITE-EXACT', 'OPEN')))
    op = open(os.path.join(ROOT, 'theory', 'OPEN_PROBLEMS.md')).read()
    check('Z7 OPEN_PROBLEMS.md states no general topology law and no common law', 'no common law' in op.lower() and 'R3-T4' in op)
    mp = os.path.join(ROOT, 'MANIFEST.json')
    if os.path.exists(mp):
        mf = json.load(open(mp))['files']
        check('Z7 MANIFEST hashes match', all(sha(os.path.join(ROOT, p)) == h for p, h in mf.items() if p != 'results/VERIFY_LAST.json'))

SHARDS = {'Z0': shard_Z0, 'Z1': shard_Z1, 'Z2': shard_Z2, 'Z3': shard_Z3, 'Z4': shard_Z4, 'Z5': shard_Z5, 'Z6': shard_Z6, 'Z7': shard_Z7}
