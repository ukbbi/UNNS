"""Recomputes every exact witness quoted in Paper IV (stdlib); writes results/c6_witnesses.json; exit code 1 on any failure."""
import json, random, sys
from fractions import Fraction as Fr
from math import gcd
import eng3, hist, trans3
R = {}; ok = True
def T(m, w):
    for N in w:
        assert m % N == 0; m = m * (N + 1) ** 2 // N
    return m
# W1 endpoint equal, content different
a = (2, 2, 2, 2); b = (1, 8, 8)
R['W1'] = {'source': 32, 'w1': a, 'w2': b, 'end1': T(32, a), 'end2': T(32, b)}; ok &= R['W1']['end1'] == R['W1']['end2'] == 13122
# W2 history counts at 72
R['W2'] = {'histories_1_to_72': [list(h) for h in hist.histories(1, 72)]}; ok &= len(R['W2']['histories_1_to_72']) == 2
# W3 same D, different history count / class count (source 4)
def hc(t):
    H, cl = hist.classes(4, t); return len(H), len(cl)
R['W3'] = {'900': hc(900), '9000': hc(9000), 'D900': eng3.Dset(900), 'D9000': eng3.Dset(9000)}
ok &= R['W3']['D900'] == R['W3']['D9000'] and R['W3']['900'] == (2, 1) and R['W3']['9000'] == (4, 2)
R['W3b'] = {'288': hc(288), '4320': hc(4320), 'D288_eq': eng3.Dset(288) == eng3.Dset(4320)}
ok &= R['W3b']['D288_eq'] and R['W3b']['288'] == (3, 1) and R['W3b']['4320'] == (3, 2)
# W4 nu non-monotone in divisibility
def nu(m):
    res = {}
    for perm in __import__('itertools').permutations((2, 3, 14)):
        if hist.admissible(m, perm): res.setdefault(T(m, perm), []).append(perm)
    if not res: return 0
    t = next(iter(res)); H = [w for w in hist.histories(m, t) if sorted(w) == [2, 3, 14]]
    idx = {w: i for i, w in enumerate(H)}; par = list(range(len(H)))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for w in H:
        for i in range(2):
            w2 = w[:i] + (w[i + 1], w[i]) + w[i + 2:]
            if w2 in idx: par[f(idx[w])] = f(idx[w2])
    return len({f(i) for i in range(len(H))})
R['W4'] = {str(m): nu(m) for m in (14, 28, 42, 70, 84, 21, 7)}; ok &= (R['W4']['14'], R['W4']['28'], R['W4']['70'], R['W4']['21']) == (2, 1, 2, 1)
# W5 local-inventory insufficiency
def an(D, N):
    t = trans3.analyse(D, D + N); return {'f': t['f'], 'f2': t['f2'], 'dead': t['dead'], 'new': t['new'], 'b': t['b'], 'b2': t['b2'], 'db': t['db']}
A1 = an([385, 27720], [11, 72]); A2 = an([15, 315], [4, 21]); B1 = an([12, 35], [44, 45]); B2 = an([33, 280], [14, 20])
R['W5'] = {'pairA': [A1, A2], 'pairB': [B1, B2]}
ok &= all(A1[k] == A2[k] for k in ('f', 'f2', 'dead', 'new')) and A1['db'] != A2['db'] and all(B1[k] == B2[k] for k in ('f', 'f2', 'dead', 'new')) and B1['db'] != B2['db']
# W6 predecessor translation and fan inclusion on integers with integer image
random.seed(1); n = bad = 0
for _ in range(4000):
    x = random.randint(2, 20000); D = eng3.Dset(x)
    if not D: continue
    L, G = eng3.LG(D); y = Fr(x) + Fr(L * L, G)
    if y.denominator != 1: continue
    y = int(y); n += 1
    for d in D:
        if y % (d * d): bad += 1; continue
        if Fr(y * (d - 1), d * d) != Fr(x * (d - 1), d * d) + Fr(L * L * (d - 1), G * d * d): bad += 1
R['W6'] = {'integer_states_with_integer_image': n, 'violations': bad}; ok &= bad == 0 and n > 100
# W7 N+1 in D(T_N(m))
bad = 0
for m in range(1, 400):
    for N in range(1, m + 1):
        if m % N == 0 and (N + 1) not in eng3.Dset(m * (N + 1) ** 2 // N): bad += 1
R['W7'] = {'violations': bad}; ok &= bad == 0
# W8 tower pair
def tower(S0, k):
    S = S0 * 2 ** k; D = eng3.Dset(Fr(S * S, 5)); return eng3.LG(D), eng3.bettiD(D)
for S0 in (126, 3094):
    (LGv, b) = tower(S0, 11); R['W8_%d' % S0] = {'k': 11, 'L,G': LGv, 'betti': b}
ok &= R['W8_126']['betti'] == [1, 6, 5] and R['W8_3094']['betti'] == [1, 10, 9, 1]
# W9 set-level Betti-change witnesses (P6d), D subset D u N
def dB(D, N):
    b, b2 = list(eng3.bettiD(D)), list(eng3.bettiD(D + N)); n = max(len(b), len(b2)); b += [0]*(n-len(b)); b2 += [0]*(n-len(b2)); return b, b2
W9 = {'b0-': ([3, 10], [18], 0, -1), 'b0+': ([6, 9], [3, 5], 0, 1), 'b1+': ([8, 12], [2], 1, 1), 'b1-': ([5, 14, 33, 60, 90], [6], 1, -1)}
R['W9'] = {}
for k, (D, N, i, d) in W9.items():
    b, b2 = dB(D, N); R['W9'][k] = {'D': D, 'N': N, 'before': b, 'after': b2}; ok &= (b2[i] - b[i]) == d
# W10 fibre needs admissibility (P1b): c=(7,0,0), c'=(0,2,4) from source 1
from fractions import Fraction as _F
Rr = lambda N: _F((N+1)**2, N)
eq = Rr(1)**7 == Rr(2)**2 * Rr(3)**4 == 16384
first_ok = [N for N in (2, 3) if 1 % N == 0]      # a first letter N must divide m0 = 1
R['W10'] = {'equal_multiplier': bool(eq), 'value': 16384, 'admissible_first_letters_of_c_prime': first_ok}
ok &= eq and first_ok == []
R['ok'] = bool(ok)
json.dump(R, open('../results/c6_witnesses.json', 'w'), indent=1, default=str)
print('ok' if ok else 'FAIL', {k: v for k, v in R.items() if k in ('W1', 'W3', 'W3b', 'W4', 'W6', 'W7')}); print(R['W5'], R['W8_126'], R['W8_3094'])
sys.exit(0 if ok else 1)
