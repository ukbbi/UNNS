import sys, os, json, math, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from famD import shapes, route, coverage
from propB import propB, check
B = 10**6; N = 2_000_000; res = {}
exc = sorted(int(k) for k in json.load(open('/home/claude/v005/UNNS-SCALE-I_v005/results/A_window_uncovered_614.json'))['results'])
table = []
for K in (1, 2, 3, 4, 6, 8, 12):
    h1, S1 = coverage(B, K, N, True); h, S = coverage(B, K, N); n720 = np.arange(719, N + 1, 720)
    table.append({"K": K, "shapes_Q1": len(S1), "cov_Q1": float(h1[2:].mean()), "shapes": len(S), "cov": float(h[2:].mean()), "cov_720": float(h[n720].mean()), "uncovered": int((~h[2:]).sum())})
    print(table[-1], flush=True)
res["coverage_table"] = table; res["window"] = N
c614 = {}
for K in (3, 12, 40):
    S = shapes(B, K); cov = {}
    for n in exc:
        for sh in S:
            if route(B, n, sh): cov[n] = list(sh); break
    c614[K] = {"shapes": len(S), "covered": len(cov), "witness": {str(k): v for k, v in cov.items()} if K == 40 else None}
    print("614 covered, K=%d: %d/%d" % (K, len(cov), len(exc)), flush=True)
res["exceptional614"] = c614
t = time.time(); pb = {}; miss = []
for n in exc:
    w = propB(B, n)
    if w and check(B, n, w): pb[str(n)] = list(w)
    else: miss.append(n)
res["propB_614"] = {"covered": len(pb), "miss": miss, "witness": pb}
json.dump(res, open('../results/V7_coverage.json', 'w'))
