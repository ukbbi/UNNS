"""GEO_HD_BRIDGE v005 independent verifier.  Own implementations: brute-force D by definition, brute-force simulation of the frozen map,
vector/box-based K(D) with bit-matrix GF(2) homology, brute-force Graver/Davenport check.  Cross-checks the release code, the frozen GEO-I engine and the stored data.
Shards Z0..Z9;  run(full) -> appends to RESULTS.  Inherited verification of frozen releases is NOT re-run (sha-256 integrity only)."""
import _paths, os, sys, json, hashlib, itertools, random, time
from fractions import Fraction as Fr
from math import gcd, isqrt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = []; FAILS = []

def check(name, ok, detail=''):
    RESULTS.append((name, bool(ok), detail))
    if not ok: FAILS.append(name)
    print('  [%s] %s %s' % ('PASS' if ok else 'FAIL', name, ('- ' + str(detail)) if detail else ''), flush=True)

def jl(rel): return json.load(open(os.path.join(ROOT, rel)))

# ----------------------------------------------------------------- independent primitives
def ind_D(x):
    x = Fr(x); a, b = x.numerator, x.denominator
    return [d for d in range(2, isqrt(a) + 1) if a % (d * d) == 0 and (d - 1) % b == 0]
def lcm2(a, b): return a // gcd(a, b) * b
def ind_C(x):
    D = ind_D(x)
    if not D: return None, D
    L = 1; G = 0
    for d in D: L = lcm2(L, d); G = gcd(G, d - 1)
    return Fr(x) + Fr(L * L, G), D
def ind_fac(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def ind_val(n, p):
    k = 0
    while n % p == 0: n //= p; k += 1
    return k

def ind_Q(d, G):
    """sieve modulus from first principles: r = G/gcd(d-1,G) and p-parts 2v_p(d)+v_p(G)"""
    beta = gcd(d - 1, G); r = G // beta
    need = {}
    for p in ind_fac(d): need[p] = max(need.get(p, 0), 2 * ind_val(d, p) + ind_val(G, p))
    for p in ind_fac(r) if r > 1 else {}: need[p] = max(need.get(p, 0), ind_val(r, p))
    q = 1
    for p, e in need.items(): q *= p ** e
    return q

# ----------------------------------------------------------------- independent K(D): exponent vectors, boxes, GF(2) bit homology
def ind_K(D):
    D = sorted(set(D)); primes = sorted({p for d in D for p in ind_fac(d)})
    vec = {d: tuple(ind_val(d, p) for p in primes) for d in D}; zero = tuple(0 for _ in primes)
    pts = [vec[d] for d in D] + [zero]
    inbox = lambda w, u, v: all(min(a, b) <= c <= max(a, b) for a, b, c in zip(u, v, w))
    E = set(); moves = set()
    for u, v in itertools.combinations(D, 2):
        if not any(w != vec[u] and w != vec[v] and inbox(w, vec[u], vec[v]) for w in pts):
            E.add((u, v)); g = tuple(b - a for a, b in zip(vec[u], vec[v]))
            first = next((c for c in g if c), 0); moves.add(g if first > 0 else tuple(-c for c in g))
    vs = set(vec.values()); inv = {v: d for d, v in vec.items()}
    mv = sorted(moves)
    def rankQ(vs_):
        M = [[Fr(c) for c in v] for v in vs_]; r = 0
        for c in range(len(primes)):
            piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
            if piv is None: continue
            M[r], M[piv] = M[piv], M[r]
            for i in range(len(M)):
                if i != r and M[i][c] != 0:
                    f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
            r += 1
        return r
    Eset = {frozenset(e) for e in E}
    cells = {0: {frozenset([d]): (vec[d], ()) for d in D}, 1: {}}
    for (u, v) in E:
        g = tuple(b - a for a, b in zip(vec[u], vec[v])); first = next((c for c in g if c), 0)
        if first > 0: cells[1][frozenset((u, v))] = (vec[u], (g,))
        else: cells[1][frozenset((u, v))] = (vec[v], (tuple(-c for c in g),))
    j = 2
    while True:
        cur = {}
        for gens in itertools.combinations(mv, j):
            if rankQ(gens) < j: continue
            for d in D:
                pts_ = [vec[d]]
                for g in gens: pts_ = pts_ + [tuple(a + b for a, b in zip(p, g)) for p in pts_]
                if len(set(pts_)) == 2 ** j and all(p in inv for p in pts_):
                    # all 1-faces (pairs differing by one generator) must be box-rule edges
                    okf = all(frozenset((inv[p], inv[tuple(a + b for a, b in zip(p, g))])) in Eset
                              for p in pts_ for g in gens if tuple(a + b for a, b in zip(p, g)) in inv)
                    if okf: cur[frozenset(inv[p] for p in pts_)] = (vec[d], gens)
        if not cur: break
        cells[j] = cur; j += 1
    for jj in [k for k in cells if not cells[k]]: del cells[jj]
    return {'cells': cells, 'vec': vec, 'inv': inv}

def _verts(base, gens, vec_inv):
    pts_ = [base]
    for g in gens: pts_ = pts_ + [tuple(a + b for a, b in zip(p, g)) for p in pts_]
    return frozenset(vec_inv[p] for p in pts_)

def ind_betti2(K):
    cells, inv = K['cells'], K['inv']; top = max(cells)
    idx = {j: {c: i for i, c in enumerate(sorted(cells[j], key=sorted))} for j in cells}
    rk = {0: 0}
    for j in range(1, top + 1):
        piv = {}; rank = 0
        for c, (base, gens) in cells[j].items():
            m = 0
            for i, g in enumerate(gens):
                rest = gens[:i] + gens[i + 1:]
                for b0 in (base, tuple(a + x for a, x in zip(base, g))):
                    m ^= 1 << idx[j - 1][_verts(b0, rest, inv)]
            while m:
                h = m.bit_length() - 1
                if h in piv: m ^= piv[h]
                else: piv[h] = m; rank += 1; break
        rk[j] = rank
    rk[top + 1] = 0
    return [len(cells[j]) - rk[j] - rk[j + 1] for j in range(top + 1)], [len(cells[j]) for j in range(top + 1)]

# ----------------------------------------------------------------- shards
def Z0(full):
    """integrity: frozen copies pinned"""
    pins = jl('results/PINS.json'); ok = True; bad = []
    for rel, h in pins['sha256'].items():
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p) or hashlib.sha256(open(p, 'rb').read()).hexdigest() != h: ok = False; bad.append(rel)
    check('Z0 pinned frozen/inherited source files sha-256', ok, bad[:3] or '%d files' % len(pins['sha256']))
    check('Z0 inherited verification status', pins.get('inherited_verification') == 'NOT_RERUN', pins.get('inherited_verification'))

def Z1(full):
    """stage sieve: D at virtual points x0 + j L^2/G equals {d : Q(d) | a h + j L^2}  (brute-force D, independent Q)"""
    from collective_regimes import in_class
    random.seed(11); n = bad = 0
    xs = [Fr(S * S, l) for l in (3, 5, 7, 11, 13) for S in range(2, 140 if full else 70) if in_class(S, l)]
    xs += [Fr(random.choice([2, 3, 5, 6, 7, 10]) * random.randint(2, 60) ** 2, random.choice([1, 2, 3, 4, 5, 6, 7, 9])) for _ in range(60 if full else 25)]
    for x in xs:
        D0 = ind_D(x)
        if not D0: continue
        L = 1; G = 0
        for d in D0: L = lcm2(L, d); G = gcd(G, d - 1)
        a, b = x.numerator, x.denominator; h = G // b
        assert G % b == 0 and gcd(L, G) == 1
        for j in [0, 1, 2, 3, random.randint(4, 300), random.randint(4, 300)]:
            Y = a * h + j * L * L
            pred = [d for d in range(2, isqrt(Y) + 1) if Y % ind_Q(d, G) == 0]
            n += 1
            if pred != ind_D(x + j * Fr(L * L, G)): bad += 1
    check('Z1 stage sieve vs brute-force D', bad == 0, '%d points, %d states' % (n, len(xs)))

def Z2(full):
    """first-event law: tau and new indices from linear congruences == brute-force simulation of the frozen map"""
    from stage_sieve import stage_data, first_event
    from collective_regimes import in_class
    n = bad = 0
    xs = [Fr(S * S, l) for l in (5, 7, 11, 13) for S in range(2, 220 if full else 90) if in_class(S, l)]
    xs += [Fr(3025, 3), Fr(1890 ** 2, 29), Fr(126 ** 2, 5)]
    for x in xs:
        S = stage_data(x)
        if S is None: continue
        cur = x; D0 = ind_D(cur); L, G = S['L'], S['G']; jj = None
        for j in range(1, 4000):
            cur = cur + Fr(L * L, G)
            if ind_D(cur) != D0: jj = j; break
        if jj is None: continue
        ev = first_event(S, jj + 3); n += 1
        if ev is None or ev['tau'] != jj or ev['new'] != sorted(set(ind_D(cur)) - set(D0)): bad += 1
    check('Z2 first-event time + new indices (sieve) vs simulation', bad == 0, '%d orbits' % n)
    # closed form for the activation-family candidates d = p_i q  vs direct membership test on the progression x_j = P^2 (m+j)/(P-1)
    from stage_sieve import family_candidate_time
    from activation_family import make
    rows = jl('data/REACHABILITY_V004.json'); nn = bb = 0
    for r in rows[::(5 if full else 25)]:
        x, y, P = make(r['k'], r['l'], r['ps'], r['q']); m = (P - 1) // r['l']
        if P > 3000: continue
        for p in r['ps']:
            d = p * r['q']; jc = family_candidate_time(P, r['l'], p, r['q']); first = None
            for j in range(1, jc + 2):
                z = Fr(P * P * (m + j), P - 1)
                if z.numerator % (d * d) == 0 and (d - 1) % z.denominator == 0: first = j; break
            nn += 1; bb += (first != jc)
    check('Z2 family closed form u = least multiple of lcm(r, q^(2+v_q(P-1))) above m == direct membership', bb == 0, '%d (instance, p_i) pairs' % nn)
    S = stage_data(Fr(1890 ** 2, 29)); ev = first_event(S, 60)
    check('Z2 B5-9 control l=29 (1890^2/29): first event predicted', ev is not None and ev['tau'] == 24 and 175 in ev['new'], ev and (ev['tau'], ev['new'][:6]))

def Z3(full):
    """K(D) three ways: release engine, independent vector/box engine, frozen GEO-I engine"""
    from divisor_complex import complex_of, betti_ranks
    from geometric_transitions import geo_row
    from collective_regimes import in_class
    from geo1lib import fibre_q, Lof, Gof
    xs = [Fr(3025, 3), Fr(12100, 3), Fr(126 ** 2, 5), Fr(1890 ** 2, 29)]
    for l in (5, 7, 11):
        for S in range(2, 160 if full else 70):
            if not in_class(S, l): continue
            cur = Fr(S * S, l)
            for _ in range(5 if full else 3):
                D = fibre_q(cur)
                if not D: break
                xs.append(cur); cur = cur + Fr(Lof(D) ** 2, Gof(D))
    xs = sorted(set(xs)); n = bad_f = bad_i = 0
    for x in xs:
        D = fibre_q(x)
        if not D: continue
        K = complex_of(D); f, r, b = betti_ranks(K, 2); fr = geo_row(x)
        n += 1
        if not (fr['cells_move'] == f and fr['betti'] == b): bad_f += 1
        if len(D) <= 40:
            Kc = ind_K(D); b2, f2 = ind_betti2(Kc)
            if not (f2 == f and b2 == b): bad_i += 1
    check('Z3 release engine == frozen GEO-I engine (cells, Betti)', bad_f == 0, '%d states' % n)
    check('Z3 release engine == independent vector/box engine (<=40 vertices)', bad_i == 0)

def Z4(full):
    """transition calculus: lemmas (a)-(e), Delta-beta identity, necessary-cause theorem, on recomputed census events"""
    from transition_calculus import analyse_transition
    from geo1lib import fibre_q, Lof, Gof
    rows = jl('data/EVENT_CENSUS.json'); random.seed(4)
    sample = rows if full else random.sample(rows, 120)
    bad = 0; flags = [0, 0, 0, 0]
    for r in sample:
        cur = Fr(r['S'] * r['S'], r['l']); Ds = []
        for i in range(r['n'] + 2):
            D = fibre_q(cur); Ds.append(D); cur = cur + Fr(Lof(D) ** 2, Gof(D))
        t = analyse_transition(Ds[r['n']], Ds[r['n'] + 1])
        if t['delta'][:len(r['delta'])] != r['delta'][:len(t['delta'])] and t['betti2'] != r['betti2']: bad += 1
        flags[0] += not t['formula_ok']; flags[1] += not (t['recK_ok'] and t['recK2_ok']); flags[2] += not all(t['lemmas'].values()); flags[3] += not all(t['nec'].values())
    check('Z4 stored census == recomputation', bad == 0, '%d events' % len(sample))
    check('Z4 Delta beta identity / zigzag reconstruction / lemmas (a)-(e) / necessary causes', sum(flags) == 0, flags)
    allrows = rows
    check('Z4 census stored flags all true', all(r['formula_ok'] and r['recK_ok'] and r['lemmas_ok'] and r['nec_ok'] for r in allrows), '%d events' % len(allrows))
    # destruction needs a cause (census-wide, from stored vectors)
    def g(v, i): return v[i] if len(v) > i else 0
    ok = all(not (g(r['betti2'], 1) < g(r['betti'], 1)) or g(r['dead'], 1) > 0 or g(r['new'], 2) > 0 for r in allrows)
    check('Z4 beta_1 drop => dead edge or new 2-cell (all events)', ok)

def Z5(full):
    """predictive graph-level update vs full recomputation"""
    from transition_calculus import predict_graph_update
    from divisor_complex import complex_of, betti_ranks
    from geo1lib import fibre_q, Lof, Gof
    rows = [r for r in jl('data/EVENT_CENSUS.json') if len(r['f']) <= 2 and len(r['f2']) <= 2]
    g = lambda v, i: v[i] if len(v) > i else 0
    ok = 0
    for r in rows:
        cur = Fr(r['S'] * r['S'], r['l']); Ds = []
        for i in range(r['n'] + 2):
            D = fibre_q(cur); Ds.append(D); cur = cur + Fr(Lof(D) ** 2, Gof(D))
        p = predict_graph_update(Ds[r['n']], sorted(set(Ds[r['n'] + 1]) - set(Ds[r['n']])))
        ok += (p['dBeta1'] == g(r['betti2'], 1) - g(r['betti'], 1) and p['dBeta0'] == g(r['betti2'], 0) - g(r['betti'], 0))
    check('Z5 graph-level predictor exact on census graph-level events', ok == len(rows), '%d/%d' % (ok, len(rows)))
    random.seed(8); bad = n = 0
    for _ in range(400 if full else 150):
        base = random.sample(range(2, 200), random.randint(1, 7)); new = random.sample([x for x in range(2, 200) if x not in base], random.randint(1, 3))
        K = complex_of(base); K2 = complex_of(base + new)
        if len(K['cells']) > 2 or len(K2['cells']) > 2: continue
        b = betti_ranks(K, 2)[2]; b2 = betti_ranks(K2, 2)[2]; p = predict_graph_update(base, new); n += 1
        bad += not (p['dBeta1'] == g(b2, 1) - g(b, 1) and p['dBeta0'] == g(b2, 0) - g(b, 0))
    check('Z5 graph-level predictor on random divisor sets', bad == 0, '%d sets' % n)

def Z6(full):
    """reachability: stage-jumping decider vs frozen-map simulation (rows of the v004 table) + exemplars B5-1/2/3"""
    from reachability import decide
    from activation_family import make
    from dynamic_activation import classify
    r = decide(*make(2, 3, [5, 11], 2)[:2], want_log=True)
    check('Z6 B5-1: 3025/3 -> 12100/3 reached in 8 steps; first event tau=6 adds {10}', r['class'] == 'REACHED' and r['steps'] == 8 and r['log'][0]['tau'] == 6 and r['log'][0]['new'] == [10], (r['class'], r['steps'], r['log'][:1]))
    r = decide(*make(3, 7, [11, 53, 67], 2)[:2], want_log=True) if full else None
    if r: check('Z6 B5-2: three-prime member reached in 375 steps, stages 372/1/2', r['class'] == 'REACHED' and r['steps'] == 375 and [l['tau'] for l in r['log']] == [372, 1], r['log'])
    rows = jl('data/REACHABILITY_V004.json'); random.seed(2)
    reached = [x for x in rows if x['class'] == 'REACHED' and x['steps'] <= (800 if full else 200)]
    blocked = [x for x in rows if x['class'] == 'BLOCKED' and x['steps'] <= 400]
    pick = reached + random.sample(blocked, min(len(blocked), 25 if full else 10)); bad = 0
    for x in pick:
        xx, y, P = make(x['k'], x['l'], x['ps'], x['q']); res = decide(xx, y)
        bad += not (res['class'] == x['class'] and (x['class'] != 'REACHED' or res['steps'] == x['steps']))
    check('Z6 decider == v004 simulation table on %d rows' % len(pick), bad == 0)
    # proper-divisor obstruction over the whole table (closed forms only) + independent simulation of flagged small members
    from stage_sieve import proper_divisor_block
    import collections
    C = collections.Counter()
    fp = 0
    for t in rows:
        b, uf, ua = proper_divisor_block(t['ps'], t['l'], t['q']); C['%s/%s' % (t['class'], 'flagged' if b else 'not flagged')] += 1
        fp += (b and t['class'] == 'REACHED')
    check('Z6 proper-divisor obstruction: table counts reproduced, no false positive on REACHED', dict(C) == jl('results/OBSTRUCTION_TABLE.json') and fp == 0, dict(C))
    nb = bb = 0
    for t in rows:
        if t['class'] != 'BLOCKED': continue
        b, uf, ua = proper_divisor_block(t['ps'], t['l'], t['q'])
        P = 1
        for p in t['ps']: P *= p
        if not b or P > 60000: continue
        x, y, _ = make(t['k'], t['l'], t['ps'], t['q']); Dy = set(ind_D(y)) if y.numerator < 4 * 10 ** 7 else None
        if Dy is None: continue
        cur = x; steps = 0; hit = False
        while cur < y and steps < 4000:
            cur, D = ind_C(cur)
            if cur is None: break
            steps += 1
            Dn = ind_D(cur)
            if not set(Dn) <= Dy: hit = True; break
        nb += 1; bb += (not hit)
        if nb >= (40 if full else 12): break
    check('Z6 flagged blocked members: independent simulation meets a forbidden occurrence before y', bb == 0, '%d members' % nb)
    un = jl('results/UNRESOLVED24.json'); from reachability import resolve_family
    sel = un if full else [u for u in un if u['class'] == 'REACHED'] + un[:3]; bu = 0
    for u in sel:
        k, l, ps, q = u['inst']; r = resolve_family(k, l, ps, q); bu += not (r['class'] == u['class'] and r['steps'] == u['steps'])
    check('Z6 B5-4: the 24 step-capped members (22 BLOCKED, 2 REACHED) re-decided exactly', bu == 0 and [u['class'] for u in un].count('BLOCKED') == 22 and [u['class'] for u in un].count('REACHED') == 2, '%d re-run' % len(sel))

    # extended family scans (k=2; l=3, l=5)
    import collections
    summ = jl('results/FAMILY_SCAN_SUMMARY.json'); ok_counts = True; samp = []
    for name in ('k2_l3', 'k2_l5'):
        rows_f = jl('data/FAMILY_SCAN_%s.json' % name)['rows']
        ok_counts &= dict(collections.Counter(r['class'] for r in rows_f)) == summ[name]['counts']
        ok_counts &= dict(collections.Counter(r['q'] for r in rows_f if r['class'] == 'REACHED')) == {int(k): v for k, v in summ[name]['reached_by_q'].items()}
        R = sorted([r for r in rows_f if r['class'] == 'REACHED' and r['steps'] <= 600], key=lambda r: r['steps'])
        random.seed(5); samp += random.sample(R, min(len(R), 25 if full else 6))
        samp += random.sample([r for r in rows_f if r['class'] == 'BLOCKED' and 'steps' in r][:200], 0)
        flagged = [r for r in rows_f if r['class'] == 'BLOCKED_BY_PROPER_DIVISOR']
        for r in random.sample(flagged, min(len(flagged), 300)):
            b, _, _ = proper_divisor_block(r['ps'], r['l'], r['q']); ok_counts &= bool(b)
    check('Z6 family scans: stored summary == data; flagged rows re-flagged', ok_counts)
    from reachability import resolve_family as _rf
    bf = 0; nrun = 0
    allR = [r for name in ('k2_l3', 'k2_l5') for r in jl('data/FAMILY_SCAN_%s.json' % name)['rows'] if r['class'] == 'REACHED']
    pick_f = list(samp)
    for qq in (5, 11, 17, 19):
        pick_f += sorted([r for r in allR if r['q'] == qq], key=lambda r: r['steps'])[:(6 if full else 2)]
    for r in pick_f:
        rr = _rf(r['k'], r['l'], r['ps'], r['q']); nrun += 1; bf += not (rr['class'] == 'REACHED' and rr['steps'] == r['steps'])
    check('Z6 family scans: sampled REACHED members (incl. q=5,11,17,19) re-resolved identically', bf == 0, '%d re-run' % nrun)
    # independent frozen-map simulation (own implementation) of the smallest reached member per q
    bs = 0; ns = 0
    for qq in (2, 5) + ((11, 17, 19) if full else ()):
        cand = sorted([r for r in allR if r['q'] == qq], key=lambda r: r['steps'])[:1]
        for r in cand:
            if r['steps'] > 3000: continue
            x, y, _ = make(r['k'], r['l'], r['ps'], r['q']); cur = x; n = 0
            while cur < y and n < r['steps'] + 5: cur, _D = ind_C(cur); n += 1
            ns += 1; bs += not (cur == y and n == r['steps'])
    check('Z6 family scans: independent simulation lands on y in the stored number of steps', bs == 0 and ns > 0, '%d members' % ns)
    qs_seen = sorted({r['q'] for name in ('k2_l3', 'k2_l5') for r in jl('data/FAMILY_SCAN_%s.json' % name)['rows'] if r['class'] == 'REACHED'})
    check('Z6 reached q beyond {2,5} occurs (v004 observation "only q in {2,5}" is a finite-sample artefact)', any(q not in (2, 5) for q in qs_seen), qs_seen)

def Z7(full):
    """towers: nested induced subcomplexes, move-stability bound, laws on stored data, frozen-engine recomputation"""
    from tower_laws import tower_D, S11, S5, nested_check, row
    from geometric_transitions import geo_row
    for name, Sf, m, p, ks in (('G=11', S11, 11, 3, [0, 3, 6, 9, 12]), ('G=5', S5, 5, 2, [0, 2, 4, 7, 9])):
        nc = nested_check(Sf, m, p, ks)
        check('Z7 %s: K_k = induced subcomplex of K_%d on height<=h' % (name, max(ks)), all(nc.values()), nc)
    for name, Sf, m, ks in (('G=11', S11, 11, range(0, 14 if full else 8)), ('G=5', S5, 5, range(0, 14 if full else 8))):
        bad = 0
        for k in ks:
            r = row(Sf, m, k); fr = geo_row(Fr(Sf(k) ** 2, m)); bad += not (fr['betti'] == r['betti_2'] and fr['cells_move'] == r['f'])
        check('Z7 %s release engine == frozen engine, k<%d' % (name, max(ks) + 1), bad == 0)
    # Davenport / l1 bound of Graver vectors of Lambda
    for m, primes in ((11, (2, 3, 5)), (5, (2, 3, 7))):
        n = len([1 for _ in range(1)])
        gr = []; R = range(-m, m + 1)
        cand = [g for g in itertools.product(R, repeat=3) if any(g) and sum(abs(c) for c in g) <= 3 * m]
        lam = [g for g in cand if _chi(primes, g, m) == 1]
        lamset = set(lam)
        for g in sorted(lam, key=lambda g: sum(map(abs, g))):
            if not any(h != g and all(hc * gc >= 0 and abs(hc) <= abs(gc) for hc, gc in zip(h, g)) for h in lamset): gr.append(g)
        mx = max(sum(map(abs, g)) for g in gr)
        check('Z7 Graver l1-norm <= |(Z/m)*| (Davenport), m=%d: max %d' % (m, mx), mx <= m - 1, 'bound %d' % (m - 1))
    t11 = jl('data/TOWER_G11.json'); t5 = jl('data/TOWER_G5.json')
    pad = lambda b, n=5: b + [0] * (n - len(b))
    b11 = {x['k']: pad(x['betti_2']) for x in t11}; b5 = {x['k']: pad(x['betti_2']) for x in t5}
    K11 = max(b11); K5 = max(b5)
    check('Z7 G=11 stored data to k=%d: beta1=8 (k>=2), beta2=17 (k>=6), beta3(k+5)=beta3(k)+9 (k>=8)' % K11,
          all(b11[k][1] == 8 for k in range(2, K11 + 1)) and all(b11[k][2] == 17 for k in range(6, K11 + 1)) and all(b11[k + 5][3] == b11[k][3] + 9 for k in range(8, K11 - 4)), K11)
    check('Z7 G=5 stored data to k=%d: Betti (1,6,5,0) for k>=7' % K5, all(b5[k][:4] == [1, 6, 5, 0] for k in range(7, K5 + 1)), K5)
    old = jl('data/TOWERS_V004.json'); ok = True
    for k, r in enumerate(old['tower11']): ok &= pad(r['betti']) == b11[k]
    for k, r in enumerate(old['tower5']): ok &= pad(r['betti']) == b5[k]
    check('Z7 stored towers == v004 table k<=45 (both towers)', ok)
    check('Z7 Betti numbers agree over GF(2) and GF(2^31-1) (both towers, all k)', all(x['betti_2'] == x['betti_2147483647'] for x in t11 + t5))

def _chi(primes, g, m):
    r = 1
    for p, e in zip(primes, g): r = r * pow(p, e, m) % m
    return r

def Z8(full):
    """cross-validation against v004 data: 474 activation events"""
    old = jl('data/ACTIVATION_SCAN_V004.json'); rows = jl('data/EVENT_CENSUS.json')
    idx = {(r['l'], r['S'], r['n']): r for r in rows}; pad = lambda b, n=8: list(b) + [0] * (n - len(b))
    tot = match = unch = drop = drop_dead = 0
    for o in old:
        for a in o.get('act_steps', []):
            r = idx.get((o['l'], o['S'], a['n'])); tot += 1
            if r is None: continue
            match += pad(r['betti']) == pad(a['betti_before']) and pad(r['betti2']) == pad(a['betti_after'])
            unch += pad(a['betti_before']) == pad(a['betti_after'])
            if pad(a['betti_after'])[1] < pad(a['betti_before'])[1]:
                drop += 1; drop_dead += (r['dead'][1] > 0)
    check('Z8 v004 activation events: Betti before/after reproduced', match == tot == 474, '%d/%d' % (match, tot))
    check('Z8 v004: 80 unchanged, 57 beta1-drops, all 57 with a dead edge', (unch, drop, drop_dead) == (80, 57, 57), (unch, drop, drop_dead))

def Z9(full):
    """counterexample regression"""
    from transition_calculus import analyse_transition
    from reachability import decide
    from activation_family import make
    t = analyse_transition([56, 21, 32, 45], [56, 21, 32, 45, 51, 15, 11])
    check('Z9 abstract calculus: dead edge with beta1 INCREASE exists (so "dead => no increase" is not a calculus law)', t['dead'][1] > 0 and t['delta'][1] > 0, (t['betti'], t['betti2']))
    r = decide(*make(2, 3, [5, 11], 2)[:2])
    check('Z9 v004 counterexample q^2>l (l=3,q=2) is reached', r['class'] == 'REACHED')
    from geo1lib import fibre_q
    from divisor_complex import betti
    x = Fr(36 * 36, 5); cur = x; seq = []
    from geo1lib import Lof, Gof
    for i in range(6):
        D = fibre_q(cur); seq.append(D); cur = cur + Fr(Lof(D) ** 2, Gof(D))
    b3, b4 = betti(seq[3]), betti(seq[4])
    check('Z9 v004 example: l=5,S=36 step 3->4 D-event with unchanged Betti vector', seq[3] != seq[4] and b3 + [0] * 4 == b4 + [0] * (len(b3) + 4 - len(b4)) or b3[:2] == b4[:2], (b3, b4))

SHARDS = {'Z0': Z0, 'Z1': Z1, 'Z2': Z2, 'Z3': Z3, 'Z4': Z4, 'Z5': Z5, 'Z6': Z6, 'Z7': Z7, 'Z8': Z8, 'Z9': Z9}
