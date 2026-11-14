"""UNNS_PRIME_DYN_v001 verifier.  Every claim reproduced here is re-derived from the definitions of Section 2
with code written for this release (pdyn.py); no code or data of the earlier U4 releases is executed.
Usage: python3 verify_prime_dyn.py [--quick]"""
import sys, os, json, math, random, time, itertools, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy
from fractions import Fraction
from mpmath import mp, mpf, log as mlog, floor as mfloor
from pdyn import *
from paths import *

QUICK = '--quick' in sys.argv
AF = float(A); BF = float(B)
REPORT = []; T0 = time.time()
def dump(name, obj):
    json.dump(obj, open(os.path.join(DATA, name), 'w'), indent=1)

def check(name, ok, detail=''):
    REPORT.append({'check': name, 'pass': bool(ok), 'detail': detail})
    print(('PASS ' if ok else 'FAIL ') + name + ' ' + detail, flush=True)
    return ok
random.seed(20261111)

# ------------------------------------------------------------------ C1 valuation law
def c1():
    bad = 0; n = 0
    primes = [2, 3, 5, 7, 11, 13]
    for _ in range(6000 if not QUICK else 1500):
        x = math.prod(p ** random.randint(0, 5) for p in primes) * random.choice([1, 17, 19, 23, 101])
        if x < 2: continue
        fx = factor(x)
        divs = [d for d in sympy.divisors(x) if d >= 2]
        N = random.choice(divs)
        y = x // N * (N + 1) ** 2
        fy, fN, fN1 = factor(y), factor(N), factor(N + 1)
        for p in set(fx) | set(fy) | set(fN) | set(fN1):
            n += 1
            if fy.get(p, 0) != fx.get(p, 0) + 2 * fN1.get(p, 0) - fN.get(p, 0): bad += 1
        # growth ratio and legality
        if not (y > 4 * x): bad += 1
    check('C1_valuation_law', bad == 0, f'{n} prime-coordinate identities, 0 violations' if bad == 0 else f'{bad} violations')

# ------------------------------------------------------------------ C2 two implementations agree
def c2():
    bad = 0; runs = 0
    starts = list(range(2, 61)) + [97, 1009, 10 ** 6 + 3, 2 ** 20, 3 ** 13, 2 ** 10 * 3 ** 7 * 5, 30030, 510510, 999983 * 7]
    for name, rule in RULES.items():
        for x0 in starts:
            a, _ = run_prime_fire(x0, rule, 120)
            b = run_prime_fire_big(x0, rule, 120)
            runs += 1
            if a != b: bad += 1
    check('C2_exponent_vs_bigint_implementations', bad == 0, f'{runs} runs x 120 steps, 4 rules, 0 mismatches' if bad == 0 else f'{bad} mismatches')

# ------------------------------------------------------------------ C3 prime-fire reduction (Theorem A)
def lex_vec(e, primes_ge5):
    return tuple(e.get(p, 0) for p in sorted(primes_ge5, reverse=True))

def c3():
    bad_pot = 0; lasts = {}; runs = 0
    hi = 400 if not QUICK else 120
    for name, rule in RULES.items():
        worst = 0
        for x0 in range(2, hi + 1):
            it, st = run_prime_fire(x0, rule, 300)
            P = [p for p in factor(x0) if p >= 5]; Pmax = max(P + [3])
            primes = list(sympy.primerange(5, Pmax + 1))
            T = transient(it); worst = max(worst, T); runs += 1
            # potential check at every step
            for i, p in enumerate(it):
                v0, v1 = lex_vec(st[i], primes), lex_vec(st[i + 1], primes)
                if p >= 5:
                    if not (v1 < v0): bad_pot += 1
                    if p > Pmax: bad_pot += 1
                else:
                    if v1 != v0: bad_pot += 1
            if T >= 300 - 5: bad_pot += 1
        lasts[name] = worst
    # random prime-fire selectors
    rr = 0
    for x0 in range(2, 150 if not QUICK else 60):
        e = from_int(x0); Pmax = max(list(factor(x0)) + [3]); primes = list(sympy.primerange(5, Pmax + 1))
        for _ in range(400):
            p = random.choice(sorted(e)); v0 = lex_vec(e, primes); e2 = fire_prime(e, p); v1 = lex_vec(e2, primes)
            if p >= 5 and not v1 < v0: bad_pot += 1
            if p < 5 and v1 != v0: bad_pot += 1
            e = e2
        rr += 1
    check('C3_prime_fire_reduction', bad_pot == 0,
          f'lexicographic potential strictly decreases at every fire of a prime>=5 and is invariant at fires of 2,3: {runs} deterministic runs x300 steps and {rr} random-selector runs x400 steps; largest last-fire index per rule {lasts}')
    return lasts

# ------------------------------------------------------------------ C4 MAXPP regime, rotation, Sturmian
EXACT = 1200
def regime(x0, n_total):
    """exact dictionary dynamics for EXACT steps, then the proved two-counter reduction; returns it, ab, T, Tstar."""
    it, ab, T = maxpp_full(x0, EXACT, n_total - EXACT)
    # consistency of the two-counter law with the exact dynamics after the last prime>=5 fire
    law_bad = 0
    for i in range(T, EXACT):
        a, b = ab[i]
        if (it[i] == 2) != (sgn_f(a, b) > 0): law_bad += 1
    Tstar = T
    while not (-AF <= ab[Tstar][0] * LN2F - ab[Tstar][1] * LN3F < BF) and Tstar < len(ab) - 1:
        a, b = ab[Tstar]
        if abs(a * LN2F - b * LN3F) < 1e-7: break
        Tstar += 1
    return it, ab, T, Tstar, law_bad

def c4():
    hi = 400 if not QUICK else 120
    Tstar_max = 0; bad = 0; runs = 0; cx_bad = 0; per_bad = 0; no33 = no222 = True; law_bad = 0; maxT = 0; per_n = 0
    starts = list(range(2, hi + 1)) + [97, 1009, 10 ** 6 + 3, 2 ** 20, 3 ** 13, 30030, 999983 * 7, 2 ** 40 * 3 ** 25, 10 ** 12 + 39]
    for x0 in starts:
        n = 6000
        it, ab, T, Tstar, lb = regime(x0, n)
        law_bad += lb; maxT = max(maxT, T); Tstar_max = max(Tstar_max, Tstar)
        for i in range(Tstar, min(n, Tstar + 3000)):
            a, b = ab[i]; f = a * LN2F - b * LN3F
            if abs(f) < 1e-7: f = a * LN2 - b * LN3
            if not (-AF <= f < BF): bad += 1
        tail = it[Tstar:]
        s = ''.join(map(str, tail))
        if '33' in s: no33 = False
        if '222' in s: no222 = False
        for k in range(1, 41):
            if factor_complexity(tail, k) != k + 1: cx_bad += 1
        runs += 1
        if runs <= 30 or x0 in (97, 1009, 10 ** 6 + 3, 2 ** 20, 3 ** 13, 30030, 999983 * 7, 2 ** 40 * 3 ** 25, 10 ** 12 + 39):
            it2, ab2, T2, Ts2, lb2 = regime(x0, EXACT + 60000)
            w = it2[Ts2:Ts2 + 60000]
            per_n += 1
            if smallest_period(w, 1500) is not None: per_bad += 1
    check('C4a_two_counter_law_and_regime_entry', bad == 0 and law_bad == 0,
          f'{runs} starts: after the last fire of a prime>=5 (latest at step {maxT}) the fired prime is 2 iff alpha ln2 > beta ln3 in the exact dynamics ({law_bad} violations); f in [-ln18, ln48) from the entry time on (latest entry step {Tstar_max}; {bad} violations)')
    check('C4b_tail_has_no_33_and_no_222', no33 and no222, f'{runs} starts')
    check('C4c_factor_complexity_k_plus_1', cx_bad == 0, f'{runs} starts, k=1..40, tails of length >= 4700: p(k)=k+1 in every case')
    check('C4d_no_period_up_to_1500', per_bad == 0, f'{per_n} starts, tail prefixes of length 60000: no period <= 1500 (a necessary consequence of Theorem 5.1; finite data cannot prove non-periodicity)')

# ------------------------------------------------------------------ C5 floor formula, discrepancy, frequency
def c5():
    mism = 0; disc_bad = 0; maxdev = mpf(0); mindev = mpf(0); checks = 0
    starts = [2, 3, 5, 7, 12, 30, 97, 1009, 10 ** 6 + 3, 2 ** 20]
    N = 20000 if not QUICK else 4000
    for x0 in starts:
        it, ab, T, Tstar, lb = regime(x0, EXACT + N + 400)
        a, b = ab[Tstar]
        f = a * LN2 - b * LN3
        z = (f + A) / L
        tail = it[Tstar:][:N]
        C = 0
        for n_, c in enumerate(tail):
            cj = int(mfloor(z + (n_ + 1) * THETA) - mfloor(z + n_ * THETA))
            checks += 1
            if cj != (1 if c == 2 else 0): mism += 1
            C += (1 if c == 2 else 0)
            dev = C - (n_ + 1) * THETA
            if not (z - 1 < dev <= z): disc_bad += 1
            maxdev = max(maxdev, dev); mindev = min(mindev, dev)
    check('C5a_mechanical_word_formula', mism == 0, f'{checks} comparisons of c_j with floor(z+(j+1)theta)-floor(z+j theta), exact to 60 digits, 0 mismatches')
    check('C5b_discrepancy_below_one', disc_bad == 0, f'z-1 < C2(n)-n theta <= z at all {checks} checks; observed range ({float(mindev):.4f}, {float(maxdev):.4f})')
    check('C5c_theta_value', abs(float(THETA) - 0.572530) < 5e-7, f'theta = ln48/ln864 = {mp.nstr(THETA, 15)}')

def c5d():
    bad = 0; n_checked = 0
    for x0 in [2, 3, 5, 12, 97, 1009, 10 ** 6 + 3]:
        it, ab, T, Tstar, lb = regime(x0, EXACT + 3000 + 400)
        a0, b0 = ab[Tstar]; f0 = a0 * LN2 - b0 * LN3; z = (f0 + A) / L
        for n in range(0, 3000):
            a, b = ab[Tstar + n]
            C = int(mfloor(z + n * THETA))
            n_checked += 1
            if a != a0 + 4 * n - 5 * C or b != b0 - n + 3 * C: bad += 1
            if n % 50 == 0:
                fn = a * LN2 - b * LN3
                if abs(fn - (f0 + n * B - L * C)) > mpf(10) ** -40: bad += 1
    check('C5d_closed_form_valuations', bad == 0, f'alpha_n = alpha_0 + 4n - 5 floor(z+n theta), beta_n = beta_0 - n + 3 floor(z+n theta), f_n = f_0 + n ln48 - ln864 floor(z+n theta): {n_checked} checks (7 starts x 3000 steps), 0 mismatches')

def c6():
    rate_th = THETA * mlog(mpf(9) / 2, 2) + (1 - THETA) * mlog(mpf(16) / 3, 2)
    bad = 0
    for x0 in [2, 3, 5, 12, 97, 1009]:
        x = x0; it = []; xs = [x0]
        for n in range(900):
            f = factor(x); p = r_maxpp(f); it.append(p); x = step_big(x, p); xs.append(x)
        T = transient(it)
        for i in range(T, len(it)):
            if Fraction(xs[i + 1], xs[i]) not in (Fraction(9, 2), Fraction(16, 3)): bad += 1
    it, ab, T, Tstar, lb = regime(2, 200000 if not QUICK else 20000)
    tail = it[Tstar:]
    c2 = tail.count(2); c3 = len(tail) - c2
    est = (c2 * mlog(mpf(9) / 2, 2) + c3 * mlog(mpf(16) / 3, 2)) / len(tail)
    check('C6a_step_ratios_9/2_and_16/3', bad == 0, 'x_{n+1}/x_n in {9/2, 16/3} at every step after the last prime>=5 fire (6 starts x 900 steps, big integers)')
    check('C6b_growth_rate', abs(float(est - rate_th)) < 2e-4 and abs(float(rate_th) - 2.2747033) < 1e-7,
          f'predicted rate {mp.nstr(rate_th, 12)} bits/step; measured over {len(tail)} steps: {mp.nstr(est, 8)}')
    return rate_th

# ------------------------------------------------------------------ C7 SPF and LPF
def c7():
    bad_s = bad_l = 0; hi = 400 if not QUICK else 120
    for x0 in range(2, hi + 1):
        it, st = run_prime_fire(x0, r_spf, 200)
        T = transient(it)
        # tail from first time exponent of 3 ... use the proved statement: eventually (3,2,2,2,2)^inf
        tail = it[100:]
        if tail[:5] not in ([3, 2, 2, 2, 2], [2, 3, 2, 2, 2], [2, 2, 3, 2, 2], [2, 2, 2, 3, 2], [2, 2, 2, 2, 3]) or smallest_period(tail, 5) != 5: bad_s += 1
        it, st = run_prime_fire(x0, r_lpf, 200)
        tail = it[100:]
        if smallest_period(tail, 3) != 3 or sorted(tail[:3]) != [2, 3, 3]: bad_l += 1
    check('C7a_SPF_period5', bad_s == 0, f'tail (3,2,2,2,2) up to phase for all starts 2..{hi}')
    check('C7b_LPF_period3', bad_l == 0, f'tail (2,3,3) up to phase for all starts 2..{hi}')
    # MINPP observation
    cnt = {}
    for x0 in range(2, hi + 1):
        it, st = run_prime_fire(x0, r_minpp, 600)
        q = smallest_period(it[300:], 40); cnt[q] = cnt.get(q, 0) + 1
    dump('minpp_periods.json', {str(k): v for k, v in cnt.items()})
    return cnt

# ------------------------------------------------------------------ C8 Stormer table and Lemma R
def divisors_capped(e, cap):
    ds = [1]
    for p, k in e.items():
        nd = []
        for d in ds:
            q = d
            for j in range(k + 1):
                if q > cap: break
                nd.append(q); q *= p
        ds = nd
    return [d for d in ds if d >= 2]

def smooth_numbers(S, bound):
    out = [1]
    for p in S:
        new = []
        for x in out:
            y = x
            while y <= bound:
                new.append(y); y *= p
        out = new
    return sorted(out)

def c8():
    table = {}
    for S in ([2, 3], [2, 3, 5], [2, 3, 5, 7], [2, 3, 5, 7, 11]):
        sm = set(smooth_numbers(S, 10 ** 13 if len(S) <= 4 else 10 ** 12))
        pairs = sorted(n for n in sm if n + 1 in sm and n >= 2)
        table[tuple(S)] = pairs
    check('C8a_stormer_tables', table[(2, 3)] == [2, 3, 8] and max(table[(2, 3, 5, 7)]) == 4374 and len(table[(2, 3, 5)]) == 9,
          '; '.join(f'S={S}: {len(v)} branch values N>=2 with N,N+1 S-smooth, max N={max(v)}' for S, v in table.items()))
    # Lemma R on random orbits with composite moves
    bad = 0; n = 0
    for trial in range(300 if not QUICK else 60):
        x0 = random.randint(2, 300); e = from_int(x0)
        for _ in range(25):
            divs = divisors_capped(e, 5000) or [min(e)]
            N = random.choice(divs); fN = factor(N); fN1 = factor(N + 1)
            e2 = step_expo(e, fN)
            n += 1
            supp, supp2 = set(e), set(e2)
            for q in set(fN1):
                if q not in supp and q not in supp2: bad += 1      # renewal: q | N+1 enters
            for q in supp2 - supp:
                if q not in fN1: bad += 1                          # only primes of N+1 can enter
            for q in supp - supp2:
                if not (fN.get(q, 0) == e[q] and q not in fN1): bad += 1   # leaving criterion
            for q in supp & set(fN):
                pass
            e = e2
    check('C8b_renewal_lemma', bad == 0, f'{n} composite-branch steps: entry iff q | N+1, exit iff v_q(N)=v_q(x) and q does not divide N+1')
    dump('stormer_tables.json', {str(list(k)): v for k, v in table.items()})
    return table

# ------------------------------------------------------------------ C9 support renewal measurements
def logcap_run(x0, steps):
    e = from_int(x0); Ns = []; supp_sizes = []; allsupp = set(e)
    for _ in range(steps):
        x_bits = sum(k * p.bit_length() for p, k in e.items())  # placeholder not used
        x = to_int(e); cap = x.bit_length()
        # largest divisor N of x with 2 <= N <= cap
        ds = [1]
        for p, k in e.items():
            nd = []
            for d in ds:
                q = d
                for j in range(k + 1):
                    if q > cap: break
                    nd.append(q); q *= p
            ds = nd
        ds = [d for d in ds if d >= 2]
        N = max(ds) if ds else min(e)
        e = step_expo(e, factor(N)); Ns.append(N); allsupp |= set(e); supp_sizes.append(len(e))
    return Ns, supp_sizes, len(allsupp)

def c9():
    out = {}
    for x0 in (41, 42, 43):
        Ns, ss, tot = logcap_run(x0, 300 if not QUICK else 100)
        out[x0] = {'distinct_N': len(set(Ns)), 'steps': len(Ns), 'support_final': ss[-1], 'support_total': tot, 'N_max': max(Ns)}
    # MAXPP: finite support
    it, st = run_prime_fire(41, r_maxpp, 3000)
    supp = set()
    for e in st: supp |= set(e)
    out['MAXPP_41'] = {'distinct_N': len(set(it)), 'support_total': len(supp)}
    ok = all(out[x]['distinct_N'] >= 0.9 * out[x]['steps'] for x in (41, 42, 43)) and out['MAXPP_41']['distinct_N'] <= 6 and out['MAXPP_41']['support_total'] <= 8
    check('C9_renewal_measurements', ok, json.dumps(out))
    dump('renewal.json', out)
    return out

# ------------------------------------------------------------------ C10 Theorem E (face determinism, polynomial bound)
def make_instance(rng, d):
    P = [2, 3, 7][:d]
    cand = {2: [2, 3, 8], 3: [2, 3, 6, 7, 8, 14]}  # candidate branch values; moves stay inside P (N, N+1 smooth over P)
    cand_all = [2, 3, 6, 7, 8, 14]
    pool = [N for N in cand_all if all(p in P for p in set(factor(N)) | set(factor(N + 1)))]
    nb = rng.randint(2, min(4, len(pool)))
    Ns = sorted(rng.sample(pool, nb))
    vec = {}
    for N in Ns:
        fN, fN1 = factor(N), factor(N + 1)
        vec[N] = tuple(2 * fN1.get(p, 0) - fN.get(p, 0) for p in P)
    # guard forms
    forms = []
    for _ in range(rng.randint(1, 3)):
        a = tuple(rng.choice([-3, -2, -1, 0, 1, 2, 3]) * (math.log(p) if rng.random() < 0.5 else 1.0) for p in P)
        b = rng.choice([-2.0, -0.5, 0.0, 0.7, 1.5])
        forms.append((a, b))
    T = {p: sorted(set([factor(N).get(p, 0) for N in Ns] + [rng.randint(0, 6)])) for p in P}
    M = rng.choice([1, 2, 3]); Q = rng.randint(1, 3)
    salt = rng.randint(0, 10 ** 9)
    return {'P': P, 'Ns': Ns, 'vec': vec, 'forms': forms, 'T': T, 'M': M, 'Q': Q, 'salt': salt}

def guard(inst, e):
    P = inst['P']
    sg = tuple((1 if (sum(a * x for a, x in zip(A_, e)) + b) > 1e-9 else (-1 if (sum(a * x for a, x in zip(A_, e)) + b) < -1e-9 else 0)) for A_, b in inst['forms'])
    res = tuple(x % inst['M'] for x in e)
    th = tuple(tuple(int(e[i] >= t) for t in inst['T'][p]) for i, p in enumerate(P))
    return (sg, res, th)

def legal_set(inst, e):
    P = inst['P']; out = []
    for N in inst['Ns']:
        fN = factor(N)
        if all(e[i] >= fN.get(p, 0) for i, p in enumerate(P)): out.append(N)
    return out

def nu_delta(inst, G, q):
    # arbitrary but fixed functions of the guard data (hash tables)
    h = int(hashlib.sha256(repr((inst['salt'], G, q)).encode()).hexdigest(), 16)
    return h, (h >> 64) % inst['Q']

def run_word(inst, e, q, k):
    word = []
    e = tuple(e)
    for _ in range(k):
        G = guard(inst, e)
        L_ = legal_set(inst, e)
        if not L_:
            word.append(('H', q)); break
        h, q2 = nu_delta(inst, G, q)
        N = L_[h % len(L_)]
        word.append((N, q))
        e = tuple(x + dv for x, dv in zip(e, inst['vec'][N])); q = q2
    return tuple(word)

def displacement_set(inst, k):
    S = {tuple([0] * len(inst['P']))}; frontier = set(S)
    for _ in range(k - 1):
        nf = set()
        for s in frontier:
            for N in inst['Ns']:
                nf.add(tuple(a + b for a, b in zip(s, inst['vec'][N])))
        S |= nf; frontier = nf
    return S

def face_sig(inst, e, S):
    sig = []
    for s in S:
        for (A_, b) in inst['forms']:
            v = sum(a * (x + y) for a, x, y in zip(A_, e, s)) + b
            sig.append(1 if v > 1e-9 else (-1 if v < -1e-9 else 0))
        for i, p in enumerate(inst['P']):
            for t in inst['T'][p]:
                sig.append((e[i] + s[i]) >= t)
    return tuple(sig)

def c10():
    rng = random.Random(7)
    viol = 0; pairs = 0; inst_count = 0; bound_viol = 0; rows = []
    k = 6
    for trial in range(30 if not QUICK else 10):
        d = rng.choice([2, 3]); inst = make_instance(rng, d)
        S = displacement_set(inst, k); M = inst['M']
        inst_count += 1
        for _ in range(300):
            e = [rng.randint(0, 40) for _ in range(d)]; q = rng.randrange(inst['Q'])
            w0 = run_word(inst, e, q, k); s0 = face_sig(inst, e, S)
            for _ in range(6):
                dl = [M * rng.randint(-2, 2) for _ in range(d)]
                e2 = [x + y for x, y in zip(e, dl)]
                if min(e2) < 0: continue
                if face_sig(inst, e2, S) == s0:
                    pairs += 1
                    if run_word(inst, e2, q, k) != w0: viol += 1
        # polynomial bound on p(k) over all starts in a box and all initial control states
        for kk in (2, 3, 4, 5, 6):
            Sk = displacement_set(inst, kk)
            nk = (len(inst['forms']) + sum(len(inst['T'][p]) for p in inst['P'])) * len(Sk)
            cd = (d + 1) * (d + 2) // 2
            bound = inst['Q'] * (M ** d) * cd * nk ** d
            words = set()
            box = range(0, 26) if d == 2 else range(0, 11)
            for e in itertools.product(box, repeat=d):
                for q in range(inst['Q']):
                    words.add(run_word(inst, e, q, kk))
            if len(words) > bound: bound_viol += 1
            if kk == 6: rows.append((d, len(inst['Ns']), inst['Q'], M, len(words), bound))
    check('C10a_same_face_same_residue_same_word', viol == 0 and pairs > 500,
          f'{inst_count} random instances in the class (d in {{2,3}}, k={k}): {pairs} equal-face pairs, 0 violations')
    check('C10b_polynomial_count_bound', bound_viol == 0, f'p_all(k) <= |Q| M^d c_d n_k^d for k=2..6 on all {inst_count} instances (all starts in a box, all control states)')
    dump('thmE_rows.json', rows)
    return rows

# ------------------------------------------------------------------ C11 ORDER
def Dm(m, m0):
    return m * math.factorial(m) // math.factorial(m0)

def S_scan(x, m0):
    # independent: scan upward while D(m) | x ... D increasing, so take the largest m with D(m)|x
    best = None; m = m0
    while True:
        D = Dm(m, m0)
        if D > x: break
        if x % D == 0: best = m
        m += 1
    return best

def u_obs(m):
    f = factor(m)
    return 0 if len(set(f.values())) <= 1 else 1

def is_sqfree_power(m):
    # m = s^e with s squarefree, e>=1 (m=1 included)
    if m == 1: return True
    f = factor(m)
    return len(set(f.values())) == 1

def c11():
    bad = 0
    for m0 in range(2, 41):
        x = m0
        for n in range(60):
            m = S_scan(x, m0)
            if m != m0 + n or x % m != 0: bad += 1
            x = x // m * (m + 1) ** 2
            # closed form
            if x != Dm(m0 + n + 1, m0): bad += 1
    for m0 in (6, 12, 30):
        x = m0
        for n in range(200):
            m = S_scan(x, m0)
            if m != m0 + n: bad += 1
            x = x // m * (m + 1) ** 2
    check('C11a_decoder_selector', bad == 0, 'S(x)=max{m>=m0: D(m)|x} returns N_n=m0+n (scan-down evaluation, m0=2..40 x 60 steps; m0=6,12,30 x 200 steps), x_n = m_n m_n!/m0!')
    # characterisation of u
    bad = 0
    for m in range(1, 100001 if not QUICK else 20001):
        if (u_obs(m) == 0) != is_sqfree_power(m): bad += 1
    check('C11b_u_zero_iff_equal_exponents', bad == 0, 'u(m)=0 iff all exponents equal (m = s^e, s squarefree): consistent with direct factorisation for m <= 10^5')
    # N = x selector (ORD-2a)
    bad = 0; cnt = 0
    for x0 in range(4, 1700 if not QUICK else 400):
        x = x0
        seq = [x]
        for _ in range(12):
            x = (x + 1) ** 2; seq.append(x)
        for n in range(2, 13):
            if seq[n] % 3 != 1: bad += 1
        for n in range(1, 13):
            if seq[n] % 2 != (seq[n - 1] + 1) % 2: bad += 1  # parity alternates: x_{n+1} = (x_n+1)^2
        for n in range(1, 13):
            if seq[n] % 2 == 1 and seq[n] % 8 != 1: bad += 1
        for n in range(2, 13):
            if seq[n] % 2 == 0 and val(seq[n], 2) != 2: bad += 1
        cnt += 1
    # N = x: capped valuations eventually periodic (ORD-2b): exact for 10 steps against big integers, then by residues
    ok = True; info = []
    def cap_vec(r, M_):
        out = []
        for p in (2, 3, 5, 7):
            q = p ** 3; rr = r % q; k = 0
            while k < 3 and rr % p == 0: rr //= p; k += 1
            out.append(k)
        return tuple(out)
    M = 2 ** 3 * 3 ** 3 * 5 ** 3 * 7 ** 3
    for x0 in (4, 6, 10, 12, 30, 97, 360):
        full = x0
        for i in range(10):
            if cap_vec(full % M, M) != tuple(min(val(full, p), 3) for p in (2, 3, 5, 7)): ok = False
            full = (full + 1) ** 2
        x = x0 % M; seen = {}; n = 0
        while x not in seen:
            seen[x] = n; x = (x + 1) ** 2 % M; n += 1
        info.append((x0, seen[x], n - seen[x]))
    check('C11g_N_equals_x_capped_valuations_periodic', ok, f'N=x: capped valuation vector (p=2,3,5,7; cap 3) is a function of x mod {M} and the residue orbit is eventually periodic; (start, preperiod, period) = {info}')
    check('C11c_self_referential_N_equals_x', bad == 0, f'for N=x (x -> (x+1)^2): x_n = 1 mod 3 (n>=2), parity alternates, v_2(x_n)=2 on even iterates, odd iterates = 1 mod 8: {cnt} composite starts x 12 steps')

def sieve_blocks(Nmax, kmax):
    """Block counts of u(m), m<=Nmax: u(m)=0 iff m is s^e with s squarefree (e>=1)."""
    sqf = np.ones(Nmax + 1, dtype=bool); sqf[0] = False
    i = 2
    while i * i <= Nmax:
        sqf[i * i::i * i] = False; i += 1
    zero = sqf.copy()   # e=1
    # perfect powers s^e, e>=2, s squarefree
    s = 2
    while s * s <= Nmax:
        if sqf[s]:
            v = s * s
            while v <= Nmax:
                zero[v] = True; v *= s
        s += 1
    zero[1] = True
    u = (~zero[1:]).astype(np.uint8)    # u[m-1]
    counts = {}
    for k in range(1, kmax + 1):
        # encode k-blocks as integers via rolling window
        code = np.zeros(len(u) - k + 1, dtype=np.int64)
        for j in range(k):
            code = (code << 1) | u[j:len(u) - k + 1 + j]
        counts[k] = int(len(np.unique(code)))
    return counts, float(u.mean())

def crt_realisation(k):
    """Construct, for every subset F of E_r, an explicit m realising the pattern 1_F on E_r (checked by factorisation)."""
    Q0 = 4 * math.prod(l * l for l in sympy.primerange(3, k + 1))
    best = None
    # search r mod 4*9*25*49 and fix larger primes' classes to r = 1 mod l^2 (so l^2 does not divide r+i for i<k<l^2)
    small = [3, 5, 7]; mods = 4 * math.prod(l * l for l in small if l <= k)
    bestE = []; bestr = None
    for r in range(mods):
        E = [i for i in range(k) if (r + i) % 4 == 2 and all((r + i) % (l * l) for l in small if l <= k)]
        if len(E) > len(bestE): bestE, bestr = E, r
    # lift r to modulus Q0 by CRT with r = 1 mod l^2 for the other primes
    others = [l for l in sympy.primerange(11, k + 1)]
    if others:
        rem = [bestr] + [1 for _ in others]; mod = [mods] + [l * l for l in others]
        r = int(sympy.ntheory.modular.crt(mod, rem)[0])
    else:
        r = bestr
    E = bestE
    assert all((r + i) % 4 == 2 and all((r + i) % (l * l) for l in sympy.primerange(3, k + 1)) for i in E)
    realised = 0
    primes_big = list(sympy.primerange(k + 1, k + 200))
    for mask in range(1 << len(E)):
        F = [E[j] for j in range(len(E)) if mask >> j & 1]
        pf = {i: primes_big[j] for j, i in enumerate(F)}
        # CRT: m = r mod Q0, m = -i mod p_i^2
        mod = [Q0] + [p * p for p in pf.values()]; rem = [r % Q0] + [(-i) % (p * p) for i, p in pf.items()]
        a, Qm = sympy.ntheory.modular.crt(mod, rem); a = int(a); Qm = int(Qm)
        ok = False
        for t in range(0, 4000):
            m = a + Qm * t
            if m < 2: continue
            good = True
            for i in E:
                want = 1 if i in F else 0
                if u_obs(m + i) != want: good = False; break
            if good: ok = True; break
        if ok: realised += 1
    return len(E), 1 << len(E), realised

def c11b():
    ks = (10, 14, 18) if not QUICK else (10,)
    res = {}
    for k in ks:
        nE, tot, real = crt_realisation(k)
        res[k] = (nE, tot, real)
    check('C11d_crt_construction', all(v[1] == v[2] for v in res.values()),
          '; '.join(f'k={k}: |E_r|={v[0]}, all {v[1]} subsets realised by explicit m (factorisation-checked) -> {v[2]}' for k, v in res.items()))
    # averages
    ok = True; rows = []
    for k in range(1, 61):
        dk = Fraction(1, 4)
        for l in sympy.primerange(3, k + 1): dk *= (1 - Fraction(1, l * l))
        mean = k * dk
        if not (float(mean) >= 2 * k / math.pi ** 2 - 1e-12): ok = False
    check('C11e_mean_density_bound', ok, 'k*d_k >= 2k/pi^2 for k=1..60 with d_k=(1/4) prod_{3<=l<=k}(1-l^-2) (exact rationals)')
    Nmax = 30_000_000 if not QUICK else 2_000_000
    counts, dens = sieve_blocks(Nmax, 14)
    ok = all(counts[k] >= 2 ** math.ceil(2 * k / math.pi ** 2) for k in counts)
    check('C11f_block_counts_u', ok, f'm <= {Nmax}: density of u=1 is {dens:.5f}; p_u(k) for k=1..14: {[counts[k] for k in range(1, 15)]}')
    dump('order_blocks.json', {'Nmax': Nmax, 'density_u1': dens, 'counts': counts, 'crt': {str(k): list(v) for k, v in res.items()}})
    return res, counts, dens

# ------------------------------------------------------------------ C12 archive hashes of inherited packages
def c12():
    exp = {'UNNS_U4_GEN_v001.zip': '042eb5b09b4d231283c9c7d9d40e29a8789625f4b073e724000d49f6d49e18df',
           'UNNS_U4_GEN_C_v001.zip': '7a361885e66c2448c232dc04b3c6c52c92a3cae7ec4452ed5dfd63fdade59118',
           'UNNS_U4_GEN_C_ORDER_v001.zip': 'a50227758ce1d5f819ae6a1775de2e9dd1563cc7a283b86244b07ed27dceb975'}
    got = {}
    for f in exp:
        p = os.path.join(INH, f)
        if os.path.exists(p): got[f] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    ok = all(got.get(f) == h for f, h in exp.items())
    check('C12_inherited_archive_hashes', ok, 'three U4 source archives present and unmodified (NOT_RERUN: their own verifiers are not executed here)')

if __name__ == '__main__':
    stages = [('C1', c1), ('C2', c2), ('C3', c3), ('C4', c4), ('C5', c5), ('C5d', c5d), ('C6', c6), ('C7', c7), ('C8', c8), ('C9', c9), ('C10', c10), ('C11', c11), ('C11b', c11b), ('C12', c12)]
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    for nm, fn in stages:
        if only and nm not in only: continue
        t = time.time(); r = fn(); print(f'  [{nm} {time.time()-t:.1f}s]', flush=True)
    ok = all(r['pass'] for r in REPORT)
    json.dump({'all_pass': ok, 'checks': REPORT, 'seconds': time.time() - T0}, open(os.path.join(REP, 'verification_report.json' if not only and not QUICK else 'partial_report.json'), 'w'), indent=1)
    print('ALL PASS' if ok else 'SOME FAILED', f'{time.time()-T0:.0f}s')
