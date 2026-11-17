"""E1: for each divisor A of 10^6, search for n with d_A(n) >= 5 (lower bounds for D_A).  Candidate order: the two B=10 distance-6 witnesses, the 614 window-exceptional n,
then n = 1..200; time-boxed per A.  Every distance is exact (full graph).  Usage: e1_divisor_scales.py part nparts budget_per_A"""
import sys, os, json, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import exact_distance
from indep_check import check_path
part, nparts, budget = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
here = os.path.dirname(os.path.abspath(__file__)); res = os.path.join(here, "..", "results")
U = json.load(open(os.path.join(here, "..", "..", "..", "v005", "UNNS-SCALE-I_v005", "results", "A_window_uncovered_614.json")))["results"]
cand = [365759, 351359] + sorted(int(k) for k in U) + list(range(1, 201))
As = sorted(2**a * 5**b for a in range(7) for b in range(7))[part::nparts]
if len(sys.argv) > 4: As = [int(x) for x in sys.argv[4].split(",")]
out = {}
for A in As:
    t0 = time.time(); best = (0, None, None); tested = 0; hist = {}
    for n in cand:
        if time.time() - t0 > budget: break
        try: d, p = exact_distance(A * n, A * (n + 1), 6)
        except MemoryError: hist["memory"] = hist.get("memory", 0) + 1; continue
        tested += 1; hist[d] = hist.get(d, 0) + 1
        assert check_path(p) == d
        if d > best[0]: best = (d, n, p)
        if d >= 6: break
    out[str(A)] = {"A": A, "tested": tested, "hist": {str(k): v for k, v in sorted(hist.items(), key=str)}, "max_d": best[0], "witness_n": best[1], "witness_path": best[2] if best[0] >= 5 else None, "seconds": round(time.time() - t0, 1)}
    print(A, tested, best[0], best[1], hist, flush=True)
    json.dump(out, open(os.path.join(res, f"E1_divisor_scales_part{part}.json"), "w"))
