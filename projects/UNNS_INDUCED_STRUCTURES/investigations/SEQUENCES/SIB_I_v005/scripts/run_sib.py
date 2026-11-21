"""SIB-I v005 - recurrence-mediated structural activation (research; standard library only).
Joint system: a recurrence step R acting on state vectors of consecutive terms, together with the unchanged
UNNS steps T_N applied diagonally to the state (N must divide every coordinate).
Run: python3 run_sib.py   -> results/*.csv, results/summary.json   (deterministic; seeds fixed)."""
import csv, json, random, sys
from math import gcd, isqrt
from functools import lru_cache
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from arithmetic import incoming, factor
OUT = Path(__file__).resolve().parent.parent / 'results'; OUT.mkdir(exist_ok=True)
SEED = 20261121

@lru_cache(None)
def count(x):                      # nonempty admissible words at x (same definition as v004)
    return sum(1 + count(s) for s, n in incoming(x))
def Wsize(x): return 1 + count(x)  # including the empty word

# ---------------- state-space operations (pair or triple states)
def Tinv(state, N):
    q = (N + 1) ** 2
    return tuple(v // q * N for v in state) if all(v % q == 0 for v in state) else None
def Tback_all(state):              # all T^{-1} images (N = m-1 with m^2 | gcd)
    g = 0
    for v in state: g = gcd(g, v)
    out = []
    for m in range(2, isqrt(g) + 1):
        if g % (m * m) == 0: out.append(Tinv(state, m - 1))
    return out
def Rinv_fib(s):  x, y = s; return (y - x, x) if y > x else None
def Rinv_pell(s): x, y = s; return (y - 2 * x, x) if y - 2 * x > 0 else None
def Rinv_trib(s): x, y, z = s; w = z - x - y; return (w, x, y) if w > 0 else None
def Rinv_double(s): x, = s; return (x // 2,) if x % 2 == 0 else None   # non-unimodular order-1 recurrence a->2a
def Rinv_triple(s): x, = s; return (x // 3,) if x % 3 == 0 else None
def ancestors(state, Rinv):        # all states from which `state` is reachable (including itself)
    seen = {state}; stack = [state]
    while stack:
        s = stack.pop(); nxt = [Rinv(s)] + Tback_all(s)
        for t in nxt:
            if t is not None and t not in seen: seen.add(t); stack.append(t)
    return seen
def T_ancestors(state):
    seen = {state}; stack = [state]
    while stack:
        s = stack.pop()
        for t in Tback_all(s):
            if t is not None and t not in seen: seen.add(t); stack.append(t)
    return seen
def chain_len(state, Rinv):
    k = 0
    while True:
        s = Rinv(state)
        if s is None: return k
        state = s; k += 1

summary = {'seed': SEED}

# ---------------- E1: joint ancestor formula |anc| = |T-anc| * (k+1) on all states in a box
def box_states(dim, B):
    if dim == 1: return [(x,) for x in range(1, B + 1)]
    if dim == 2: return [(x, y) for x in range(1, B + 1) for y in range(1, B + 1)]
    return [(x, y, z) for x in range(1, B + 1) for y in range(1, B + 1) for z in range(1, B + 1)]
systems = {'fibonacci_type': (2, 300, Rinv_fib), 'pell_type': (2, 300, Rinv_pell), 'tribonacci_type': (3, 40, Rinv_trib),
           'double_a_to_2a': (1, 5000, Rinv_double), 'triple_a_to_3a': (1, 5000, Rinv_triple)}
e1 = {}; rows_e1 = []
for name, (dim, B, Rinv) in systems.items():
    n = ok = 0; bad = []
    for st in box_states(dim, B):
        tanc = len(T_ancestors(st)); k = chain_len(st, Rinv); anc = len(ancestors(st, Rinv)); n += 1
        if anc == tanc * (k + 1): ok += 1
        elif len(bad) < 8: bad.append((st, anc, tanc, k))
    e1[name] = dict(states=n, product_formula_holds=ok, fails=n - ok, examples=bad)
    for b in bad: rows_e1.append([name, *b[0], b[1], b[2], b[3]])
summary['E1_joint_ancestor_product_formula'] = e1
with open(OUT / 'product_formula_failures.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['system', 'state', 'ancestors', 'T_ancestors', 'chain_len']); w.writerows([[r[0], r[1:-3], r[-3], r[-2], r[-1]] for r in rows_e1])

# ---------------- E2: commutation (equivariance) tests
def commute_violations(f, box):
    tested = viol = 0
    for x in range(1, box + 1):
        for N in range(1, x + 1):
            if x % N: continue
            fx = f(x)
            if fx % N: continue                      # T_N(f(x)) not defined
            tested += 1
            if f(x * (N + 1) ** 2 // N) != fx * (N + 1) ** 2 // N: viol += 1
    return tested, viol
e2 = {}
for name, f in {'a_to_2a (linear)': lambda x: 2 * x, 'a_to_5a (linear)': lambda x: 5 * x, 'sylvester x^2-x+1': lambda x: x * x - x + 1,
                'mersenne 2x+1': lambda x: 2 * x + 1, 'squares x^2': lambda x: x * x}.items():
    t, v = commute_violations(f, 600); e2[name] = dict(tested=t, violations=v)
# two-term linear recurrences: R(x,y)=(y,x+y); T_N acts diagonally -> check exact equality on the domain
def comm_pair(R, box):
    tested = viol = 0
    for x in range(1, box + 1):
        for y in range(1, box + 1):
            g = gcd(x, y)
            for N in range(1, g + 1):
                if g % N: continue
                tested += 1
                r = (N + 1) ** 2 // N if False else None
                a = R((x * (N + 1) ** 2 // N, y * (N + 1) ** 2 // N)); b = tuple(v * (N + 1) ** 2 // N for v in R((x, y)))
                if any(v % 1 for v in a) or a != b: viol += 1
    return tested, viol
for name, R in {'fibonacci (x,y)->(y,x+y)': lambda s: (s[1], s[0] + s[1]), 'pell (x,y)->(y,x+2y)': lambda s: (s[1], s[0] + 2 * s[1])}.items():
    t, v = comm_pair(R, 120); e2[name] = dict(tested=t, violations=v)
summary['E2_equivariance'] = e2

# ---------------- E3: gcd invariance of consecutive terms + pair-level alphabet
random.seed(SEED); inv = []
for _ in range(400):
    a0, a1 = random.randint(1, 500), random.randint(1, 500); g0 = gcd(a0, a1); a, b = a0, a1; okc = True
    for _ in range(60):
        a, b = b, a + b
        if gcd(a, b) != g0: okc = False
    inv.append(okc)
summary['E3_consecutive_gcd_invariant_random_starts'] = dict(trials=len(inv), all_invariant=all(inv))

# ---------------- E4: pair-level vs single-term counts on Fibonacci / Lucas panels, h-lifts
def seq(name, N):
    a, b = (0, 1) if name == 'fibonacci' else (2, 1); s = [a, b]
    while len(s) <= N: s.append(s[-1] + s[-2])
    return s
H = [1, 2, 3, 4, 6, 8, 12, 24, 36]; rows = []; e4 = {}
for name in ('fibonacci', 'lucas'):
    s = seq(name, 84); tot = act = 0; stats = {}
    for h in H:
        pet_pos = 0; n_terms = 0; ratio = []
        for n in range(2, 85):
            c = h * s[n]; single = count(c); pair_level = count(h)       # pair (h a_{n-1}, h a_n) has gcd h
            petal = single - pair_level; pet_pos += petal > 0; n_terms += 1
            x, y = h * s[n - 1], h * s[n]
            k = chain_len((x, y), Rinv_fib) if y <= 10**7 else None
            rows.append([name, h, n, c, single, pair_level, petal, k if k is not None else ''])
        stats[h] = dict(terms=n_terms, nonempty_petal=pet_pos, frac=pet_pos / n_terms)
    e4[name] = stats
summary['E4_petal_activation_fraction'] = e4
with open(OUT / 'petal_table.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['sequence', 'h', 'n', 'h_times_a_n', 'single_term_nonempty_words', 'pair_level_nonempty_words', 'petal', 'pair_chain_len_if_small']); w.writerows(rows)

# ---------------- E5: sunflower theorem on explicit word sets (small) and counts (panels)
@lru_cache(None)
def words(x): return frozenset({()} | {w + (n,) for s, n in incoming(x) for w in words(s)})
sf = dict(triples=0, ok=0); fails = []
for h in (1, 2, 3, 4, 6, 12):
    for a in range(1, 91):
        for b in range(a, 91):
            if gcd(a, b) != 1: continue
            A, Bv, C = words(h * a), words(h * b), words(h * (a + b)); core = words(h); sf['triples'] += 1
            if A & Bv == core and A & C == core and Bv & C == core: sf['ok'] += 1
            elif len(fails) < 5: fails.append((h, a, b))
sf['failures'] = fails; summary['E5_sunflower_explicit_words'] = sf
# counts on Fibonacci / Lucas panels: |W(h a)∩W(h b)| = |W(h gcd)| is SCG-01; petals pairwise disjoint -> total size identity
cnt = dict(checked=0, ok=0)
for name in ('fibonacci', 'lucas'):
    s = seq(name, 84)
    for n in range(2, 85):
        a, b, c = s[n - 2], s[n - 1], s[n]
        if min(a, b) <= 0: continue
        for h in (1, 2, 6):
            cnt['checked'] += 1
            if gcd(a, b) == gcd(b, c) == gcd(a, c): cnt['ok'] += 1
summary['E5b_panel_pairwise_gcd_equal'] = cnt

# ---------------- E6: same-sum control (Euclid-type chain length of coprime splits of c = F_n)
def chain_pair(a, c):
    k = 0; x, y = a, c
    while y > x: x, y = y - x, x; k += 1
    return k
rows6 = []; e6 = {}
for n in range(6, 24):
    c = seq('fibonacci', n)[n]; best = (-1, None); ch = []
    for a in range(1, c):
        if gcd(a, c) == 1:
            k = chain_pair(a, c); ch.append(k)
            if k > best[0]: best = (k, a)
    fibpair = seq('fibonacci', n)[n - 1]
    e6[n] = dict(c=c, coprime_splits=len(ch), max_chain=best[0], argmax_a=best[1], fib_a=fibpair, fib_chain=chain_pair(fibpair, c), mean_chain=sum(ch) / len(ch),
                 frac_with_chain_ge_2=sum(k >= 2 for k in ch) / len(ch))
    rows6.append([n, c, len(ch), best[0], best[1], fibpair, e6[n]['fib_chain'], round(e6[n]['mean_chain'], 4)])
summary['E6_same_sum_control'] = e6
with open(OUT / 'same_sum_control.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['n', 'c=F_n', 'coprime_splits', 'max_chain', 'argmax_a', 'F_(n-1)', 'chain_of_fibonacci_split', 'mean_chain']); w.writerows(rows6)

# ---------------- E7: single-term activation of recurrence sums vs matched coprime sums (matched magnitude)
random.seed(SEED); e7 = {}
for name in ('fibonacci', 'lucas'):
    s = seq(name, 60); obs = []; ctl = []
    for n in range(4, 61):
        c = s[n]; obs.append(count(c) > 0)
        for _ in range(40):                                   # random coprime split (a, c'-a) with c' in [c/2, 2c]
            cc = random.randint(max(2, c // 2), 2 * c)
            ctl.append(count(cc) > 0)
    e7[name] = dict(n_terms=len(obs), observed_frac=sum(obs) / len(obs), matched_integer_frac=sum(ctl) / len(ctl), n_control=len(ctl))
summary['E7_activation_vs_matched_integers'] = e7
(OUT / 'summary.json').write_text(json.dumps(summary, indent=1, sort_keys=True, default=str))
print(json.dumps({k: v for k, v in summary.items() if k in ('E1_joint_ancestor_product_formula',)}, indent=1, default=str)[:2500])
print('done')
