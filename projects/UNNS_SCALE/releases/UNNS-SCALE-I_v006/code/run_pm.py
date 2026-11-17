"""E2b: does every tested n at B=10^6 admit a (+-|+-) four-step route?  n sets: the 614 window-exceptional n, the first 400 n, a seeded random window sample, and the outside-window scan values (v005).  Time-boxed."""
import sys, os, json, time, random
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pm_meet import pm_meet
budget = int(sys.argv[1]); part = int(sys.argv[2]); nparts = int(sys.argv[3])
here = os.path.dirname(os.path.abspath(__file__)); res = os.path.join(here, "..", "results"); v5 = os.path.join(here, "..", "..", "..", "v005", "UNNS-SCALE-I_v005", "results")
U = sorted(int(k) for k in json.load(open(os.path.join(v5, "A_window_uncovered_614.json")))["results"])
S = sorted(int(k) for k in json.load(open(os.path.join(v5, "B_outside_window_scan.json")))["results"])
rnd = random.Random(11); cand = [("exceptional", n) for n in U] + [("small", n) for n in range(1, 401)] + [("random", rnd.randint(1, 999999)) for _ in range(1500)] + [("outside", n) for n in S]
rnd.shuffle(cand); cand = cand[part::nparts]; out = {}; t0 = time.time(); miss = []
for tag, n in cand:
    if time.time() - t0 > budget: break
    w = pm_meet(10**6, n); out[str(n)] = {"set": tag, "witness": list(w) if w else None}
    if w is None: miss.append(n); print("MISS", n, flush=True)
json.dump({"tested": len(out), "misses": miss, "results": out, "seconds": round(time.time() - t0, 1)}, open(os.path.join(res, f"E2b_pm_part{part}.json"), "w"))
import collections; print(len(out), collections.Counter(v["set"] for v in out.values()), "misses:", miss, round(time.time() - t0))
