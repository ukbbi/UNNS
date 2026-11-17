"""E3: exact scan of d_800(n) (800 = 2^5*5^2 is the smallest divisor of 10^6 with no distance-5 case found in E1).  Candidates: the two B=10 witnesses, the 614 window-exceptional n,
then n=1,2,3,...  Time-boxed; exact in the full graph; stops at the first d>=5 (then certify with audit_cert)."""
import sys, os, json, time, collections
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import exact_distance
from indep_check import check_path
A = int(sys.argv[1]); budget = int(sys.argv[2]); here = os.path.dirname(os.path.abspath(__file__)); res = os.path.join(here, "..", "results")
U = json.load(open(os.path.join(here, "..", "..", "..", "v005", "UNNS-SCALE-I_v005", "results", "A_window_uncovered_614.json")))["results"]
cand = [365759, 351359] + sorted(int(k) for k in U); seen = set(cand); cand += [n for n in range(1, 20001) if n not in seen]
t0 = time.time(); h = collections.Counter(); best = (0, None, None); tested = 0
for n in cand:
    if time.time() - t0 > budget: break
    try: d, p = exact_distance(A * n, A * (n + 1), 6)
    except MemoryError: h['memory'] += 1; continue
    assert check_path(p) == d; tested += 1; h[d] += 1
    if d > best[0]: best = (d, n, p)
    if d >= 5: print("FOUND", A, n, d, flush=True); break
json.dump({"A": A, "tested": tested, "hist": dict(h), "max_d": best[0], "witness_n": best[1], "witness_path": best[2] if best[0] >= 5 else None, "seconds": round(time.time() - t0, 1)}, open(os.path.join(res, f"E3_scale{A}.json"), "w"))
print(A, tested, dict(h), best[0], round(time.time() - t0))
