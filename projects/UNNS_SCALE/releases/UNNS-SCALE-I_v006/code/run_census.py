"""Census of meeting word pairs at B = 10^6: for each n, the set of (word_x, word_y) with minimal total length (exact radius-2 balls).
n set: the 614 window-exceptional n, plus a seeded random sample of window n.  Time-boxed; incremental JSON.  Usage: run_census.py budget_seconds nrandom"""
import sys, os, json, time, random
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from b2_types import meetings
budget, nrand = int(sys.argv[1]), int(sys.argv[2])
here = os.path.dirname(os.path.abspath(__file__)); res = os.path.join(here, "..", "results")
U = json.load(open(os.path.join(here, "..", "..", "..", "v005", "UNNS-SCALE-I_v005", "results", "A_window_uncovered_614.json")))["results"]
rnd = random.Random(2026); ns = [("exceptional", int(k)) for k in sorted(U, key=int)] + [("random", rnd.randint(1, 999999)) for _ in range(nrand)]
rnd.shuffle(ns); out = {}; t0 = time.time()
for tag, n in ns:
    if time.time() - t0 > budget: break
    B = 10**6; d, pairs = meetings(B * n, B * (n + 1))
    out[str(n)] = {"set": tag, "min_total": d, "pairs": sorted(f"{a}|{b}" for a, b in pairs)}
    if len(out) % 50 == 0: json.dump(out, open(os.path.join(res, "E2_census.json"), "w")); print(len(out), round(time.time() - t0), flush=True)
json.dump(out, open(os.path.join(res, "E2_census.json"), "w")); print("done", len(out), round(time.time() - t0))
