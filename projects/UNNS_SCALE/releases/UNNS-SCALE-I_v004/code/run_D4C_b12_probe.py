"""D4-C: exact d_12(n) for n+1 = 12600 s and 25200 s (s<=40, s in {127,509,1021}).  Writes ../results/D4C_B12_pole_probe.json"""
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import exact_distance
from indep_check import check_path
t0 = time.time(); res = {}; h = collections.Counter()
for s in list(range(1, 41)) + [127, 509, 1021]:
    for C in (12600, 25200):
        n = C * s - 1; d, p = exact_distance(12 * n, 12 * (n + 1), 6); assert check_path(p) == d
        res[str(n)] = {"C": C, "s": s, "d": d, "path": p}; h[(C, d)] += 1
json.dump({"B": 12, "hist_by_C_d": {f"{C},{d}": c for (C, d), c in sorted(h.items())}, "max": max(v["d"] for v in res.values()), "results": res, "seconds": round(time.time() - t0, 1)},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "D4C_B12_pole_probe.json"), "w"))
print(sorted(h.items()))
