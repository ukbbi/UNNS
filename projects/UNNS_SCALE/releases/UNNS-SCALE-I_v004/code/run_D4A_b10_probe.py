"""D4-A: exact d_10(n) for n+1 = 720 * 2^a * p (p prime, a = 0..5): probe of the pole family.  Writes ../results/D4A_B10_pole_probe.json"""
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import exact_distance
from indep_check import check_path
from sympy import primerange
t0 = time.time(); res = {}; h = collections.Counter()
for a in range(0, 6):
    for p in primerange(7, 140):
        m = 720 * 2**a * p; n = m - 1
        d, path = exact_distance(10 * n, 10 * (n + 1), 6); assert check_path(path) == d
        res[str(n)] = {"a": a, "p": p, "d": d, "path": path if d == 6 else None}; h[(a, d)] += 1
    if time.time() - t0 > 480: print("time stop after a =", a); break
sixes = sorted((v["a"], v["p"]) for v in res.values() if v["d"] == 6)
json.dump({"B": 10, "family": "n+1 = 720*2^a*p, p prime in [7,139]", "hist_by_a_d": {f"{a},{d}": c for (a, d), c in sorted(h.items())}, "six_witnesses_a_p": sixes, "results": res, "seconds": round(time.time() - t0, 1)},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "D4A_B10_pole_probe.json"), "w"))
print(sorted(h.items()), sixes, round(time.time() - t0))
