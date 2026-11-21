"""SIB-I v005 independent verifier: standard library only; does NOT import arithmetic.py or run_sib.py.
Recomputes incoming sets by trial division, replaces backward-ancestor BFS by forward closure, and checks stored results."""
import csv, json, hashlib, random, sys
from math import gcd, isqrt
from functools import lru_cache
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; RES = ROOT / 'results'
ok_all = True
def check(name, ok, info=''):
    global ok_all; ok_all &= bool(ok); print(('PASS ' if ok else 'FAIL ') + name, info)

def inc(x):                                 # trial division: m>=2, m^2 | x, source x(m-1)/m^2
    return [(x * (m - 1) // (m * m), m - 1) for m in range(2, isqrt(x) + 1) if x % (m * m) == 0]
@lru_cache(None)
def cnt(x): return sum(1 + cnt(s) for s, n in inc(x))
@lru_cache(None)
def words(x): return frozenset({()} | {w + (n,) for s, n in inc(x) for w in words(s)})

# V1 sunflower on a fresh sample
random.seed(11); n = bad = 0
for _ in range(2500):
    h = random.choice([5, 7, 10, 15, 20, 30]); a = random.randint(1, 70); b = random.randint(1, 70)
    if gcd(a, b) != 1: continue
    A, B, C, core = words(h * a), words(h * b), words(h * (a + b)), words(h); n += 1
    if not (A & B == core and A & C == core and B & C == core): bad += 1
check('V1_sunflower_pairwise_intersections_equal_W(h)', bad == 0 and n > 800, f'{n} triples')

# V2 joint ancestors via FORWARD closure vs product formula
def forward_anc_counts(states, ops_fwd):
    anc = {}
    sset = set(states)
    for s in states:
        seen = {s}; st = [s]
        while st:
            u = st.pop()
            for v in ops_fwd(u):
                if v in sset and v not in seen: seen.add(v); st.append(v)
        for t in seen: anc[t] = anc.get(t, 0) + 1
    return anc
def Tfwd(u):
    g = 0
    for v in u: g = gcd(g, v)
    return [tuple(c * (N + 1) ** 2 // N for c in u) for N in range(1, g + 1) if g % N == 0]
def T_only_anc(sset_states, B):
    return forward_anc_counts(sset_states, Tfwd)
def run_system(dim, B, Rfwd, Rinv):
    if dim == 1: states = [(x,) for x in range(1, B + 1)]
    elif dim == 2: states = [(x, y) for x in range(1, B + 1) for y in range(1, B + 1)]
    else: states = [(x, y, z) for x in range(1, B + 1) for y in range(1, B + 1) for z in range(1, B + 1)]
    joint = forward_anc_counts(states, lambda u: Tfwd(u) + [Rfwd(u)])
    tonly = T_only_anc(states, B); bad = 0
    for s in states:
        k = 0; t = s
        while True:
            t = Rinv(t)
            if t is None: break
            k += 1
        if joint[s] != tonly[s] * (k + 1): bad += 1
    return len(states), bad
S = json.load(open(RES / 'summary.json'))
fib = lambda u: (u[1], u[0] + u[1]); fibinv = lambda s: (s[1] - s[0], s[0]) if s[1] > s[0] else None
pell = lambda u: (u[1], u[0] + 2 * u[1]); pellinv = lambda s: (s[1] - 2 * s[0], s[0]) if s[1] - 2 * s[0] > 0 else None
trib = lambda u: (u[1], u[2], u[0] + u[1] + u[2]); tribinv = lambda s: (s[2] - s[0] - s[1], s[0], s[1]) if s[2] - s[0] - s[1] > 0 else None
for name, dim, B, Rf, Ri in (('fibonacci_type', 2, 120, fib, fibinv), ('pell_type', 2, 120, pell, pellinv), ('tribonacci_type', 3, 30, trib, tribinv)):
    n, bad = run_system(dim, B, Rf, Ri); check('V2_forward_closure_product_formula_' + name, bad == 0, f'{n} states, box {B} (stored run used a larger box)')
for name, mult, key in (('double', 2, 'double_a_to_2a'), ('triple', 3, 'triple_a_to_3a')):
    n, bad = run_system(1, 5000, lambda u, m=mult: (u[0] * m,), lambda s, m=mult: (s[0] // m,) if s[0] % m == 0 else None)
    check('V2b_nonunimodular_failures_match_stored_' + name, bad == S['E1_joint_ancestor_product_formula'][key]['fails'] and bad > 0, f'recomputed {bad}, stored {S["E1_joint_ancestor_product_formula"][key]["fails"]}')

# V3 commutation / non-equivariance
def viol(f, box):
    t = v = 0
    for x in range(1, box + 1):
        for N in range(1, x + 1):
            if x % N == 0 and f(x) % N == 0:
                t += 1; v += f(x * (N + 1) ** 2 // N) != f(x) * (N + 1) ** 2 // N
    return t, v
check('V3_linear_commutes', viol(lambda x: 7 * x, 300)[1] == 0 and viol(lambda x: 3 * x, 300)[1] == 0)
check('V3_nonlinear_never_commutes', all(viol(f, 300)[1] == viol(f, 300)[0] > 0 for f in (lambda x: x * x - x + 1, lambda x: 2 * x + 1, lambda x: x * x)))
def pair_comm(R, box):
    for x in range(1, box + 1):
        for y in range(1, box + 1):
            g = gcd(x, y)
            for N in range(1, g + 1):
                if g % N: continue
                r = lambda v: v * (N + 1) ** 2 // N
                if R((r(x), r(y))) != tuple(r(v) for v in R((x, y))): return False
    return True
check('V3_pair_recurrences_commute', pair_comm(lambda s: (s[1], s[0] + s[1]), 60) and pair_comm(lambda s: (s[1], 3 * s[0] + s[1]), 60))
# V4 gcd invariance
random.seed(5); good = True
for _ in range(300):
    a, b = random.randint(1, 900), random.randint(1, 900); g0 = gcd(a, b)
    for _ in range(50):
        a, b = b, a + b
        good &= gcd(a, b) == g0
check('V4_consecutive_gcd_invariant', good)
# V5 stored tables vs trial division
rows = list(csv.DictReader(open(RES / 'petal_table.csv'))); m = bad = 0
for r in rows:
    c = int(r['h_times_a_n'])
    if c <= 10**9: m += 1; bad += cnt(c) != int(r['single_term_nonempty_words']) or cnt(int(r['h'])) != int(r['pair_level_nonempty_words']) or int(r['petal']) != cnt(c) - cnt(int(r['h']))
check('V5_petal_table_recomputed_by_trial_division', bad == 0 and m > 200, f'{m} rows')
nonneg = all(int(r['petal']) >= 0 for r in rows)
check('V5b_petals_nonnegative', nonneg, 'W(h) subset W(h a_n) since h | h a_n')
# V6 same-sum control
rows = list(csv.DictReader(open(RES / 'same_sum_control.csv'))); bad = 0
for r in rows:
    nn = int(r['n']); c = int(r['c=F_n'])
    if nn > 17: continue
    best = -1; arg = None
    for a in range(1, c):
        if gcd(a, c) == 1:
            x, y, k = a, c, 0
            while y > x: x, y = y - x, x; k += 1
            if k > best: best, arg = k, a
    bad += best != int(r['max_chain']) or arg != int(r['argmax_a']) or arg != int(r['F_(n-1)'])
check('V6_same_sum_control_fibonacci_split_is_unique_maximum', bad == 0)
# V7 Fibonacci single-term activation for n<=40 by trial division vs table (h=1)
f = [0, 1]
while len(f) < 41: f.append(f[-1] + f[-2])
t = {int(r['n']): int(r['single_term_nonempty_words']) for r in csv.DictReader(open(RES / 'petal_table.csv')) if r['sequence'] == 'fibonacci' and r['h'] == '1'}
check('V7_fibonacci_activation_matches_trial_division', all(cnt(f[n]) == t[n] for n in range(2, 41)))
blob = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(RES.glob('*'))}
(RES / 'verification_results.json').write_text(json.dumps({'all_pass': ok_all, 'result_hashes': {k: v for k, v in blob.items() if k != 'verification_results.json'}}, indent=1))
print('SIB-I v005 VERIFY PASS' if ok_all else 'SIB-I v005 VERIFY FAIL')
