"""D4-B: exact (untruncated) distances d(B n, B(n+1)) at B = 10^6.  Usage: run_D4B_million.py N  [extra n list file]
Every distance is exact in the full infinite graph; lower bounds by disjoint balls, certified by indep_check (sympy)."""
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import exact_distance
from indep_check import certify_distance
B = 10**6
def run(ns, label):
    out = {}
    for n in ns:
        d, p = exact_distance(B * n, B * (n + 1)); out[n] = (d, p)
    return out
if __name__ == "__main__":
    N = int(sys.argv[1]); t0 = time.time()
    ns = list(range(1, N + 1)); res = run(ns, "scan")
    hist = collections.Counter(d for d, p in res.values())
    mx = max(hist); wit = [n for n, (d, p) in res.items() if d == mx][:5]
    cert = {}
    for n in wit[:2]:
        d, p = res[n]; cert[n] = {"d": d, "path": p, "balls": certify_distance(B * n, B * (n + 1), d, p)}
    r = {"B": B, "N": N, "hist": dict(sorted(hist.items())), "mean": sum(d for d, _ in res.values()) / N, "finite_max": mx,
         "max_witness_n": wit, "certificates": {str(k): v for k, v in cert.items()}, "first_of_each": {str(d): [n, res[n][1]] for d in hist for n in [min(k for k, (dd, _) in res.items() if dd == d)]},
         "per_n": {str(n): d for n, (d, _) in res.items()}, "seconds": round(time.time() - t0, 1)}
    json.dump(r, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", f"D4B_B1e6_N{N}.json"), "w"), indent=1)
    print(r["hist"], r["mean"], mx, r["seconds"])
