#!/usr/bin/env python3
"""GEO-I v012 experiment.  python3 experiments/cap_attack12.py [FULL_DMAX STRUCT_DMAX N_RANDOM]
Exact evidence (NOT the proof) for G12-T3..T8: the explicit cell family of theory/cap_cover.py covers H_Q minus H_0
 (1) every small box d<=FULL_DMAX;  (2) the structural lemmas S1..S6 on every small box d<=STRUCT_DMAX;
 (3) targeted adversarial boxes: Fibonacci / golden-ratio moduli, extreme residues s in {2,3,d-3,d-2, near d/2, d/k}, thin and strongly unequal enlargements (u or v in {0,1,2,d-2,d-1,..}), d up to 400;
 (4) N_RANDOM random boxes with 31<=d<=250.   Writes output/data/v12_cap.json."""
import os, sys, json, random, time
from math import gcd
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); sys.path.insert(0, os.path.join(ROOT, 'theory'))
import cap_cover as C
FD, SD, NR = ([int(x) for x in sys.argv[1:4]] + [20, 16, 3000][len(sys.argv[1:4]):])
t0 = time.time(); out = {'release': 'v012', 'params': {'full_dmax': FD, 'struct_dmax': SD, 'random': NR}}
n, bad = C.sweep(5, FD); out['full_sweep'] = {'dmax': FD, 'boxes': n, 'failures': bad}
n, bad = C.structure_sweep(5, SD); out['structure_sweep'] = {'dmax': SD, 'boxes': n, 'failures': [list(map(str, b)) for b in bad]}
def units(d): return [s for s in range(2, d - 1) if gcd(s, d) == 1]
fib = [5, 8, 13, 21, 34, 55, 89, 144, 233, 377]; tg = []
for i in range(len(fib) - 2):
    d, s = fib[i + 2], fib[i + 1]                      # consecutive Fibonacci: all partial quotients 1 (golden-ratio type)
    for (dd, ss) in ((d, s), (d, d - s), (d, fib[i]), (d, d - fib[i])):
        if 2 <= ss <= dd - 2 and gcd(ss, dd) == 1: tg.append((dd, ss))
for d in (7, 11, 13, 31, 64 + 1, 101, 128 + 1, 257, 399):
    us = units(d); sel = {2, 3, d - 3, d - 2, 4, d - 4}
    for k in (2, 3, 4, 5, 7, 11): sel |= {d // k, d // k + 1, d // k - 1}
    tg += [(d, s) for s in sorted(sel) if 2 <= s <= d - 2 and gcd(s, d) == 1]
tg = sorted(set(tg)); nt = 0; badt = []
for (d, s) in tg:
    ex = sorted({0, 1, 2, 3, d - 1, d - 2, d - 3, d // 2, d // 3, (2 * d) // 3, (d * 618) // 1000, (d * 382) // 1000})
    ex = [x for x in ex if 0 <= x < d]
    for u in ex:
        for v in ex:
            if u == v == 0: continue
            nt += 1; ok, info = C.verify(d, s, u, v)
            if not ok: badt.append((d, s, u, v, str(info)))
out['targeted'] = {'pairs': len(tg), 'boxes': nt, 'dmax': max(d for d, s in tg), 'failures': badt}
rng = random.Random(12); nr = 0; badr = []
while nr < NR:
    d = rng.randint(31, 250); s = rng.choice(units(d)); u = rng.randrange(d); v = rng.randrange(d)
    if u == v == 0: continue
    nr += 1; ok, info = C.verify(d, s, u, v)
    if not ok: badr.append((d, s, u, v, str(info)))
out['random'] = {'boxes': nr, 'failures': badr}
out['seconds'] = round(time.time() - t0, 1)
json.dump(out, open(os.path.join(ROOT, 'output', 'data', 'v12_cap.json'), 'w'), indent=1)
print({k: (v if not isinstance(v, dict) else {a: (b if a != 'failures' else len(b)) for a, b in v.items()}) for k, v in out.items()})
