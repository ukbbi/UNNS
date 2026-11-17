"""E2c: larger (+-|+-) universality test at B=10^6: random window n, random n up to 10^9, and n+1 = 720 * (random 7-smooth) up to 10^10.  Time-boxed.  Usage: run_pm2.py budget part nparts"""
import sys, os, json, time, random, collections
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pm_meet import pm_meet
budget, part, nparts = map(int, sys.argv[1:4]); res = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
rnd = random.Random(97); cand = [("random window", rnd.randint(1, 999999)) for _ in range(6000)] + [("random to 1e9", rnd.randint(10**6, 10**9)) for _ in range(3000)]
for _ in range(3000):
    while True:
        m = 720
        for p in (2, 3, 5, 7):
            for _ in range(rnd.randint(0, 4)): m *= p
        if m <= 10**10: break
    cand.append(("720*smooth", m - 1))
rnd.shuffle(cand); cand = cand[part::nparts]; out = {}; miss = []; t0 = time.time()
for tag, n in cand:
    if time.time() - t0 > budget: break
    w = pm_meet(10**6, n); out[str(n)] = {"set": tag, "witness": list(w) if w else None}
    if w is None: miss.append(n); print("MISS", n, flush=True)
json.dump({"tested": len(out), "misses": miss, "results": out, "seconds": round(time.time() - t0, 1)}, open(os.path.join(res, f"E2c_pm_part{part}.json"), "w"))
print(len(out), dict(collections.Counter(v["set"] for v in out.values())), "misses:", miss, round(time.time() - t0))
