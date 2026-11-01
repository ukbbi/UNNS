"""GEO_HD_BRIDGE v004 independent verifier.  Own implementations (no import of the builder modules or of the frozen GEO-I engine):
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

# ================================================================== extra independent helpers (v004)
def evec(d): return tuple(sorted(pf(d).items()))
def vsub(a, b):
    r = dict(a)
    for p, e in b: r[p] = r.get(p, 0) - e
    return tuple(sorted((p, e) for p, e in r.items() if e))
def univ(ps, g): return tuple(sorted((p, e) for p, e in zip(ps, g) if e))
def Eset(D):
    ev = {d: evec(d) for d in D}
    return {vsub(ev[v], ev[u]) for u in D for v in D if u != v}
def betti_state(x):
    ps, q, b, F = Fset(x)
    if not F: return [1]
    return betti_gf2(complex_from(F, kmove_from_F_only(F, len(ps)), kmax=len(ps)))
def inst_xy(k, l, ps, q):
    P = prod(ps); return Fr(P * P, l), Fr((P * q) ** 2, l), P
def step_orbit(x, y, cap=40000):
    """own collective orbit until x>=y or cap; returns list of (state, D)"""
    out = []; cur = x
    for n in range(cap):
        r = DLG(cur)
        if r is None: out.append((cur, None)); break
        out.append((cur, r[0]))
        if cur >= y: break
        cur = cur + Fr(r[1] ** 2, r[2])
    return out

# ================================================================== shards
def shard_Z0(full=False):
    """integrity: pins, sibling manifests (hash only, NOT_RERUN), STATUS gates, required documents"""
    pins = load('results/PINS.json')
    check('Z0 pinned frozen libraries unchanged (%d)' % len(pins), all(sha(os.path.join(ROOT, 'src', f)) == s for f, s in pins.items()))
    for name in ['GEO_HD_1D_v00%d' % i for i in (1, 2, 3, 4)] + ['GEO_HD_BRIDGE_v001', 'GEO_HD_BRIDGE_v002', 'GEO_HD_BRIDGE_v003', 'GEO_HD_E2_P4_v005']:
        mp = os.path.join(os.path.dirname(ROOT), name, 'MANIFEST.json')
        if os.path.exists(mp):
            mf = json.load(open(mp)); mf = mf.get('files', mf); d = os.path.dirname(mp)
            ok = all(sha(os.path.join(d, p)) == h for p, h in mf.items() if not p.startswith('figures/') and p != 'results/VERIFY_LAST.json')
            check('Z0 sibling %s untouched (manifest hashes; inherited verification NOT_RERUN)' % name, ok)
    st = load('STATUS.json')
    check('Z0 STATUS gates', st['gates']['C3'] == 'NOT_CLAIMED' and st['gates']['NOVELTY'] == 'NOT_ASSESSED' and 'same author' in st['independence_caveat'])
    need = ['theory/' + n + '.md' for n in ('SOURCE_CROSSWALK', 'ACTIVATION_DEFINITIONS', 'INFINITE_FAMILIES', 'PRIMITIVE_RELATIONS', 'MOVE_TOPOLOGY', 'DYNAMIC_ACTIVATION', 'COLLECTIVE_TOWERS', 'HISTORY_CONNECTION', 'THEOREMS', 'OPEN_PROBLEMS')]
    miss = [n for n in need if not os.path.exists(os.path.join(ROOT, n))]
    check('Z0 required documents present', not miss, miss)

def shard_Z1(full=False):
    """[NEW] A4-T1/T2: activation family -- D(x), D(y), Graver, dormant->active relations, K_move(y)=K_{k+1} without 2-cells"""
    rows = load('results/ACTIVATION_FAMILY.json'); bad = []; n = 0
    for r in rows:
        k, l, ps, q = r['k'], r['l'], r['primes'], r['q']; x, y, P = inst_xy(k, l, ps, q)
        hyp = (isprime(l) and (l - 1) % k == 0 and all(isprime(p) and p % l == ps[0] % l for p in ps) and len(set(ps)) == k and isprime(q) and q not in ps
               and all(pow(ps[0], j, l) != 1 for j in range(1, k)) and pow(ps[0], k, l) == 1 and q * ps[0] % l == 1)
        px, qx, bx, Fx = Fset(x); py, qy, by, Fy = Fset(y)
        Dx, Dy = Dset(x), Dset(y)
        okD = Dx == {P} and Dy == {P} | {p * q for p in ps}
        Gx, Gy = graver(px, qx, bx), graver(py, qy, by)
        rel = [univ(ps, tuple(1 if i == a else -1 if i == b else 0 for i in range(k))) for a in range(k) for b in range(k) if a != b]
        inGx = {univ(px, g) for g in Gx}; inGy = {univ(py, g) for g in Gy}
        okR = all(g in inGx and g in inGy for g in rel) and Eset(Dx) == set() and all(g in Eset(Dy) for g in rel)
        okG = len(Gx) == k * (k - 1) + 2 and len(Gy) == (k + 1) * (k + 2)
        mv = kmove_from_F_only(Fy, len(py)); cells = complex_from(Fy, mv, kmax=len(py))
        bt = betti_gf2(cells)
        okT = len(Fy) == k + 1 and 2 not in cells and bt == [1, k * (k - 1) // 2] + [0] * (len(bt) - 2) and len(cells.get(1, [])) == (k + 1) * k // 2
        # axis complex of y: discrete
        ax = [(u, v) for u, v in itertools.combinations(Fy, 2) if sum(a != b for a, b in zip(u, v)) == 1]
        okA = len(ax) == 0
        ok = hyp and okD and okR and okG and okT and okA; n += 1
        if not ok: bad.append((k, l, q, hyp, okD, okR, okG, okT, okA))
    check('Z1 [NEW] A4-T1/T2 on %d instances (k=2..5, several l, q=2 and q large): D(x)={P}, D(y)={P,p_i q}, e_i-e_j in Gr(x),Gr(y), E empty at x, nonempty at y, |Gr|=k(k-1)+2 / (k+1)(k+2), K_move(y)=K_{k+1}, no 2-cells, beta_1=k(k-1)/2, K_axis(y) has no edges' % n, not bad, bad[:2])
    # extra instance generation (independent of the builder): all k=2 triples for l=3
    ex = 0; ok = True
    for ps in itertools.combinations([5, 11, 17, 23, 29, 41, 47], 2):
        for q in (2, 17, 23):
            x, y, P = inst_xy(2, 3, list(ps), q)
            if q in ps: continue
            ok &= (Dset(y) == {P} | {p * q for p in ps} and betti_state(y) == [1, 1]); ex += 1
    check('Z1 [NEW] A4-T2 k=2 further %d members: beta_1(K_move(y))=1' % ex, ok)
    # congruence lemma behind A4-T1:  subproducts of P are 1 mod l only for the empty set and P
    ok = True
    for r in rows:
        k, l, ps = r['k'], r['l'], r['primes']
        sub = [S for j in range(1, k + 1) for S in itertools.combinations(ps, j) if prod(S) % l == 1]
        ok &= sub == [tuple(ps)]
    check('Z1 [NEW] congruence lemma: among nonempty sub-products of p_1..p_k only the full product is 1 mod l (c has order exactly k)', ok)

def shard_Z2(full=False):
    """[NEW] A4-T3 / T4 lemma: D is monotone along collective orbits (hence realised relations persist); progression lemma"""
    starts = []
    for l in (3, 5, 7, 11, 13):
        for S in range(2, 400 if not full else 900):
            x = Fr(S * S, l)
            if Dset(x): starts.append(x)
    starts = starts[:60 if not full else 250]
    bad = 0; steps = 0
    for x in starts:
        cur = x; prev = None
        for _ in range(14):
            r = DLG(cur)
            if r is None: break
            if prev is not None and not prev <= r[0]: bad += 1
            prev = r[0]; cur = cur + Fr(r[1] ** 2, r[2]); steps += 1
    check('Z2 [NEW] D(C(x)) contains D(x): %d orbits, %d steps, 0 violations' % (len(starts), steps), bad == 0, bad)
    # persistence of realised relations E_g follows; test it too on the tower
    x = Fr((126) ** 2, 5); prevE = None; ok = True
    for _ in range(30):
        D, L, G = DLG(x); E = Eset(D)
        if prevE is not None and not prevE <= E: ok = False
        prevE = E; x = x + Fr(L * L, G)
    check('Z2 [NEW] realised relation sets E(x_n) are increasing along the l=5 tower (30 steps)', ok)
    # progression lemma
    rows = load('results/REACHABILITY.json'); bad = 0; n = 0
    for r in rows[::7][: (60 if not full else 140)]:
        k, l, ps, q = r['k'], r['l'], r['ps'], r['q']; x, y, P = inst_xy(k, l, ps, q); m = (P - 1) // l
        cur = x; j = 0
        while True:
            D, L, G = DLG(cur)
            if D != {P}: break
            if cur != Fr(P * P * (m + j), l * m): bad += 1; break
            cur = cur + Fr(L * L, G); j += 1
            if j > 40000: break
        n += 1
    check('Z2 [NEW] progression lemma: x_j = P^2 (m+j)/(l m), m=(P-1)/l, while D={P} (%d instances)' % n, bad == 0, bad)

def shard_Z3(full=False):
    """[NEW] A4-T3 positive: actual FIELD-I orbits connect x=P^2/l to y=(Pq)^2/l; dormant relation becomes realised; topology at x,y and in between"""
    ex = load('results/EXEMPLARS.json'); okall = True; det = []
    for e in ex:
        k, l, ps, q = e['inst']; x, y, P = inst_xy(k, l, ps, q)
        orb = step_orbit(x, y)
        reached = orb[-1][0] == y; steps = len(orb) - 1
        Dy = Dset(y); mono = all(a[1] <= b[1] for a, b in zip(orb, orb[1:]) if a[1] is not None and b[1] is not None) and all(D <= Dy for _, D in orb)
        rel = univ(ps, tuple([1, -1] + [0] * (k - 2)))
        px, qx, bx, Fx = Fset(x); gx = {univ(px, g) for g in graver(px, qx, bx)}
        dormant_x = rel in gx and rel not in Eset(Dset(x)); active_y = rel in Eset(Dy)
        first_active = next(i for i, (s, D) in enumerate(orb) if rel in Eset(D))
        bx_, by_ = betti_state(x), betti_state(y)
        bx_ = (bx_ + [0, 0])[:2]
        ok = reached and steps == e['steps'] and mono and dormant_x and active_y and by_[1] == k * (k - 1) // 2 and bx_[1] == 0
        # relation is absent from the lattice (not primitive) at the state before the last one only when b changes: record
        det.append((e['inst'][:2], e['inst'][3], steps, first_active))
        okall &= ok
    check('Z3 [NEW] A4-T3 exemplars %s: actual map reaches y; D monotone and inside D(y); e_1-e_2 dormant at x, realised at y; beta_1 0 -> k(k-1)/2' % det, okall)
    # beta_1 of the intermediate event states and the excursion through other denominators
    e0 = ex[0]; k, l, ps, q = e0['inst']; x, y, P = inst_xy(k, l, ps, q); orb = step_orbit(x, y)
    bs = [Fr(s).denominator for s, _ in orb]
    check('Z3 [NEW] excursion: the denominator along the reached orbit of 3025/3 -> 12100/3 is %s (b leaves 3 and returns)' % bs, bs[0] == 3 and bs[-1] == 3 and max(bs) == 54 and 9 in bs)

def shard_Z4(full=False):
    """[NEW] A4-T3 negative: monotone-D blocking criterion; reachability table re-run with independent code; necessary divisibility conditions at the first event"""
    rows = load('results/REACHABILITY.json'); import random
    rnd = random.Random(4)
    pick = [r for r in rows if r['class'] == 'REACHED'] + rnd.sample([r for r in rows if r['class'] == 'BLOCKED'], 40 if not full else 160)
    bad = []
    for r in pick:
        k, l, ps, q = r['k'], r['l'], r['ps'], r['q']; x, y, P = inst_xy(k, l, ps, q); Dy = Dset(y)
        cur = x; cls = 'UNRESOLVED'
        for n in range(30000):
            if cur == y: cls = 'REACHED'; break
            if cur > y: cls = 'OVERSHOT'; break
            D, L, G = DLG(cur)
            if not D <= Dy: cls = 'BLOCKED'; break
            cur = cur + Fr(L * L, G)
        if cls != r['class']: bad.append((k, l, ps, q, cls, r['class']))
    check('Z4 [NEW] reachability classes re-derived by independent code on %d rows (%d REACHED + sampled BLOCKED)' % (len(pick), sum(1 for r in pick if r['class'] == 'REACHED')), not bad, bad[:2])
    allrows = rows
    cnt = {c: sum(1 for r in allrows if r['class'] == c) for c in ('REACHED', 'BLOCKED', 'OVERSHOT', 'UNRESOLVED', 'D_EMPTY')}
    check('Z4 [NEW] table totals %s: no overshoot, no D-empty exit anywhere in the table (finite-exact)' % cnt, cnt['OVERSHOT'] == 0 and cnt['D_EMPTY'] == 0 and cnt['REACHED'] > 0)
    # necessary arithmetic condition at the first event of every reached instance:  new element d = p_i q, q^2 | u/g, d = 1 mod b
    ok = True; nn = 0
    for r in rows:
        if r['class'] != 'REACHED': continue
        k, l, ps, q = r['k'], r['l'], r['ps'], r['q']; x, y, P = inst_xy(k, l, ps, q); m = (P - 1) // l
        cur = x
        while True:
            D, L, G = DLG(cur)
            if D != {P}: break
            cur = cur + Fr(L * L, G)
        u = cur * l * m / (P * P); assert u.denominator == 1; u = int(u); g = gcd(u, l * m); b = l * m // g
        new = D - {P}
        ok &= all(d in {p * q for p in ps} for d in new) and (u // g) % (q * q) == 0 and all(d % b == 1 % b for d in new) and cur.denominator == b and u < q * q * m
        nn += 1
    check('Z4 [NEW] first event of each of the %d reached instances: new elements are p_i q, q^2 | u/gcd(u,lm), d=1 mod lm/gcd(u,lm), and u<q^2 m' % nn, ok)
    # blocking by the integer state P^2: if the orbit were still on the progression at u=lm, D(P^2) has a divisor of P other than P
    ok = all(Dset(Fr(prod(ps) ** 2)) >= {p for p in ps} for ps in ([5, 11], [23, 37, 79], [7, 17, 37, 47]))
    check('Z4 [NEW] D(P^2) contains every prime p_i (so not inside D(y)): the progression cannot run to u=l m inside D(y)', ok)

def shard_Z5(full=False):
    """[NEW] B4-4: scan of actual orbits from S^2/l for dormant->active events; persistence; topology effect (own recomputation of a sample)"""
    scan = load('data/ACTIVATION_SCAN.json'); scan = [r for r in scan if 'error' not in r]
    check('Z5 [NEW] scan file: %d orbits, persistence violations %d' % (len(scan), sum(r['persist_viol'] for r in scan)), sum(r['persist_viol'] for r in scan) == 0 and len(scan) > 300)
    ev = [(r['l'], r['S'], a) for r in scan for a in r['act_steps']]
    pad = lambda b: (list(b) + [0] * 5)[:5]
    ch = sum(1 for l, S, a in ev if pad(a['betti_before']) != pad(a['betti_after'])); un = len(ev) - ch
    check('Z5 [NEW] step-level activation events: %d total, Betti vector changes at %d and is unchanged at %d' % (len(ev), ch, un), ch > 0 and un > 0)
    # own recomputation of activation counts on a sample orbit set
    import random; rnd = random.Random(5); sample = rnd.sample(scan, 10 if not full else 40); bad = []
    for r in sample:
        l, S, N = r['l'], r['S'], r['n']; xs = [Fr(S * S, l)]
        for _ in range(N):
            xs.append(Cmap(xs[-1]))
        recs = []
        for x in xs:
            ps, q, b, F = Fset(x); recs.append((Dset(x), {univ(ps, g) for g in graver(ps, q, b)}))
        sa = 0; cr = 0
        for n in range(N):
            new = Eset(recs[n + 1][0]) - Eset(recs[n][0])
            for g in new:
                if g in recs[n][1]: sa += 1
                else: cr += 1
        if (sa, cr) != (r['n_step_act'], r['n_creat']): bad.append((l, S, sa, cr, r['n_step_act'], r['n_creat']))
    check('Z5 [NEW] independent recount of step-activation / creation-realisation on %d sampled orbits' % len(sample), not bad, bad[:2])
    # first orbit with an activation that leaves the whole Betti vector unchanged
    un = [(l, S, a) for l, S, a in ev if pad(a['betti_before']) == pad(a['betti_after'])]
    l, S, a = min(un, key=lambda t: (t[2]['n'], t[0], t[1]))
    xs = [Fr(S * S, l)]
    for _ in range(a['n'] + 1): xs.append(Cmap(xs[-1]))
    b0, b1 = betti_state(xs[a['n']]), betti_state(xs[a['n'] + 1])
    n = max(len(b0), len(b1)); b0 += [0] * (n - len(b0)); b1 += [0] * (n - len(b1))
    check('Z5 [NEW] first topology-preserving activation event (l=%d, S=%d, step %d): own Betti %s -> %s (counterexample to "activation always changes Betti numbers")' % (l, S, a['n'], b0, b1), b0 == b1 and pad(a['betti_before']) == pad(a['betti_after']))
    # activation that destroys a cycle (Betti decreases)
    dec = [(l, S, a) for l, S, a in ev if len(a['betti_before']) > 1 and len(a['betti_after']) > 1 and a['betti_after'][1] < a['betti_before'][1]]
    check('Z5 [NEW] activation events can also lower beta_1 (%d recorded in the scan)' % len(dec), len(dec) > 0)

def shard_Z6(full=False):
    """[NEW] A4-T5/T6: tower Betti tables recomputed with independent code (G=11, G=5), count laws, periodicity"""
    T = load('results/TOWERS.json'); S11 = lambda k: 2 ** 2 * 3 ** (3 + k) * 5 ** 4; S5 = lambda k: 126 * 2 ** k
    ks11 = [0, 1, 2, 3, 6, 9, 12] if not full else list(range(0, 16))
    ks5 = [0, 1, 2, 3, 7, 12] if not full else list(range(0, 16))
    bad = []
    for k in ks11:
        b = betti_state(Fr(S11(k) ** 2, 11)); r = T['tower11'][k]
        if b != r['betti']: bad.append(('11', k, b, r['betti']))
    for k in ks5:
        b = betti_state(Fr(S5(k) ** 2, 5)); r = T['tower5'][k]
        if b != r['betti']: bad.append(('5', k, b, r['betti']))
    check('Z6 [NEW] stored Betti rows reproduced by independent code (G=11 k in %s, G=5 k in %s)' % (ks11, ks5), not bad, bad[:2])
    t11 = T['tower11']; t5 = T['tower5']
    check('Z6 [NEW] G=11: |D_k| = 2k+7 (proved by counting residues mod 5 of the c-exponent) for k=0..45', all(r['nF'] == 2 * r['k'] + 7 for r in t11) and all(len(Fset(Fr(S11(k) ** 2, 11))[3]) == 2 * k + 7 for k in range(0, 46 if full else 20)))
    check('Z6 [NEW] G=11: no dormant Graver move and |Gr|=22 for k>=3 (k=0..45)', all(r['dormant'] == 0 for r in t11) and all(r['graver'] == 22 for r in t11 if r['k'] >= 3))
    pd = lambda r, i: (list(r['betti']) + [0] * 5)[i]
    b1 = [pd(r, 1) for r in t11]; b2 = [pd(r, 2) for r in t11]; b3 = [pd(r, 3) for r in t11]
    check('Z6 [NEW] G=11 FINITE-EXACT: beta_1=8 for 2<=k<=45 and beta_2=17 for 6<=k<=45; beta_3=0 for k<=8', all(v == 8 for v in b1[2:]) and all(v == 17 for v in b2[6:]) and all(v == 0 for v in b3[:9]) and [b1[0], b1[1]] == [6, 7])
    inc = [b3[k + 1] - b3[k] for k in range(9, 45)]
    check('Z6 [NEW] G=11 FINITE-EXACT: beta_3 increments for k=9..44 are periodic (0,3,1,1,4) with period 5 = ord_11(3); beta_3(k+5)=beta_3(k)+9 (k>=9, to k=45)', inc == [(0, 3, 1, 1, 4)[i % 5] for i in range(len(inc))] and all(b3[k + 5] == b3[k] + 9 for k in range(9, 41)))
    check('Z6 [NEW] G=11: Euler characteristic chi = 10 - beta_3 for k>=6 (cells and Betti agree)', all(r['chi'] == 10 - pd(r, 3) for r in t11 if r['k'] >= 6))
    check('Z6 [NEW] ord_11(3)=5 and 3=2^8, 5=2^4 mod 11 (discrete-log source of the period)', pow(3, 5, 11) == 1 and pow(2, 8, 11) == 3 and pow(2, 4, 11) == 5)
    c5 = [(list(r['betti']) + [0] * 5)[:4] for r in t5]
    check('Z6 [NEW] G=5 FINITE-EXACT: Betti vector is [1,6,5,0] for 7<=k<=45; |Gr|=18 for k>=3; dormant 0 for k>=2; dormant 2/6 at k=0/1', all(b == [1, 6, 5, 0] for b in c5[7:]) and all(r['graver'] == 18 for r in t5 if r['k'] >= 3) and all(r['dormant'] == 0 for r in t5[2:]) and t5[0]['dormant'] == 2 and t5[1]['dormant'] == 6)
    check('Z6 [NEW] G=5 vs G=11 at k=45: same engine, different outcome (beta_3 = 0 vs %d); both tops are finite-exact' % b3[45], b3[45] > 0 and c5[45][3] == 0)
    # l=29 tower (state 1890^2/29): correct description is l=29, G=29, (P,rho^2)=(35,900); first 24 steps
    x = Fr(1890 ** 2, 29); Ds = []
    for n in range(25):
        Ds.append(Dset(x)); x = Cmap(x)
    x24 = Fr(1890 ** 2, 29)
    for _ in range(24): x24 = Cmap(x24)
    prev = Fr(1890 ** 2, 29)
    for _ in range(23): prev = Cmap(prev)
    pp, qp, bp, Fp = Fset(prev); grp = {univ(pp, g) for g in graver(pp, qp, bp)}
    newrel = Eset(Ds[24]) - Eset(Ds[23]); act = [g for g in newrel if g in grp]
    check('Z6 [NEW] l=29 (G=29, not G=35): D={30,378} for n<=23, gains 175 at n=24 with beta_1(K_move) 0 -> 1; %d of %d newly realised relations were primitive (in Gr) one step earlier' % (len(act), len(newrel)),
          all(D == {30, 378} for D in Ds[:24]) and Ds[24] == {30, 175, 378} and betti_state(x24) == [1, 1] and betti_state(prev) == [1, 0] and len(act) == 2)

def shard_Z7(full=False):
    """[NEW] A4-T7: K_move of integer states is contractible (nerve lemma) while SELECT-II history complexes have several components"""
    H = load('results/HISTORY_BRIDGE.json'); bad = []
    for r in H['integer_kmove']:
        b = betti_state(Fr(r['m']))
        if not (b[0] == 1 and all(v == 0 for v in b[1:])): bad.append((r['m'], b))
    check('Z7 [NEW] K_move(m) has Betti vector (1,0,..,0) for %d integer states (independent code)' % len(H['integer_kmove']), not bad, bad[:2])
    # K_move = K_axis for integers (b = 1): hull rule gives grid adjacency only
    ok = True
    for r in H['integer_kmove'][:6]:
        ps, q, b, F = Fset(Fr(r['m'])); F0 = set(F) | {tuple([0] * len(ps))}
        full_box = set(itertools.product(*[range(e + 1) for e in q]))
        ok &= F0 == full_box
    check('Z7 [NEW] integers: F u {0} is the whole box (Lambda_1 = Z^k), so cells are the grid cubes avoiding the corner', ok)
    # own history side
    def words(m, content):
        from collections import Counter
        cnt = Counter(content); out = []
        def rec(s, pref):
            if not any(cnt.values()): out.append(tuple(pref)); return
            for N in sorted(k for k, v in cnt.items() if v):
                if s % N: continue
                cnt[N] -= 1; pref.append(N); rec(s * (N + 1) ** 2 // N, pref); pref.pop(); cnt[N] += 1
        rec(m, []); return out
    def ncomp(ws):
        S = set(ws); par = {w: w for w in ws}
        def f(a):
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        for w in ws:
            for i in range(len(w) - 1):
                if w[i] != w[i + 1]:
                    v = w[:i] + (w[i + 1], w[i]) + w[i + 2:]
                    if v in S: par[f(w)] = f(v)
        return len({f(w) for w in ws})
    ok = True
    for r in H['bridge']:
        ws = words(4, tuple(sorted((2, 4) + tuple(r['A'])))); E = Fr(4)
        for N in (2, 4) + tuple(r['A']): E *= Fr((N + 1) ** 2, N)
        b = betti_state(E)
        ok &= (int(E) == r['E'] and ncomp(ws) == r['history_components'] >= 2 and b[0] == 1 and all(v == 0 for v in b[1:]))
    check('Z7 [NEW] A4-T7 obstruction: history endpoints E with %s history components all have contractible K_move' % [r['history_components'] for r in H['bridge']], ok)
    # activation-family orbits pass through integer states where the topology collapses
    ex = load('results/EXEMPLARS.json')[0]; x, y, P = inst_xy(*[ex['inst'][0], ex['inst'][1], ex['inst'][2], ex['inst'][3]]); cur = y; ints = None
    for n in range(40):
        D, L, G = DLG(cur)
        if cur.denominator == 1: ints = (n, cur, betti_state(cur)); break
        cur = cur + Fr(L * L, G)
    check('Z7 [NEW] after reaching y=12100/3 (beta_1=1) the same orbit becomes integral at %s with Betti %s: K_move topology is not monotone along C-orbits' % (ints[1] if ints else None, ints[2] if ints else None), ints is not None and betti_state(y)[1] == 1 and ints[2][1:] == [0] * (len(ints[2]) - 1))

def shard_Z8(full=False):
    """docs and manifest"""
    st = open(os.path.join(ROOT, 'theory', 'THEOREMS.md')).read()
    check('Z8 THEOREMS.md lists A4-T1..A4-T7 and PROVED / FINITE-EXACT / OPEN / COUNTEREXAMPLE tags', all(('A4-T%d' % i) in st for i in range(1, 8)) and all(t in st for t in ('PROVED', 'FINITE-EXACT', 'OPEN', 'COUNTEREXAMPLE')))
    op = open(os.path.join(ROOT, 'theory', 'OPEN_PROBLEMS.md')).read()
    check('Z8 OPEN_PROBLEMS.md states the infinitude question and no extrapolation of tower Betti numbers', 'infinitely many' in op.lower() and 'extrapolat' in op.lower())
    ac = open(os.path.join(ROOT, 'theory', 'ACTIVATION_DEFINITIONS.md')).read()
    check('Z8 ACTIVATION_DEFINITIONS.md separates dynamical activation from arithmetic comparison and activation from creation', 'arithmetic activation comparison' in ac.lower() and 'creation' in ac.lower() and 'K_real' in ac)
    mp = os.path.join(ROOT, 'MANIFEST.json')
    if os.path.exists(mp):
        mf = json.load(open(mp))['files']
        check('Z8 MANIFEST hashes match', all(sha(os.path.join(ROOT, p)) == h for p, h in mf.items() if p != 'results/VERIFY_LAST.json'))

SHARDS = {'Z0': shard_Z0, 'Z1': shard_Z1, 'Z2': shard_Z2, 'Z3': shard_Z3, 'Z4': shard_Z4, 'Z5': shard_Z5, 'Z6': shard_Z6, 'Z7': shard_Z7, 'Z8': shard_Z8}
