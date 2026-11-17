"""D4-B: exact distances at B=10^6 for adversarial n (n+1 highly smooth; B=10 exceptional-class members; n=60 family).
Usage: run_D4B_adversarial.py [tag]   -> ../results/D4B_B1e6_adversarial.json.  Exact in the full infinite graph (exact_lib), lower bounds certified by indep_check."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import exact_distance
from indep_check import certify_distance, check_path
B = 10**6
def cand():
    s = set([59, 60, 61, 119, 179, 359, 719, 1079, 1259, 1439, 2159, 2519, 5039, 7559, 10079, 12599, 25199, 27719, 50399, 55439, 83159, 110879, 166319, 332639, 360359, 720719])
    for k in range(1, 12):                                 # B=10 exceptional classes mod 2520, small members
        for r in (359, 719, 1079, 1259, 1439, 2159, 2519): s.add(2520 * k + r)
    for m in (360, 720, 840, 1260, 2520, 5040, 7560, 10080, 12600, 27720, 55440, 83160, 166320, 277200, 720720): s.add(m - 1)
    return sorted(s)
if __name__ == "__main__":
    out = {}; t0 = time.time(); ns = cand()
    for n in ns:
        t = time.time(); d, p = exact_distance(B * n, B * (n + 1), 5)
        assert check_path(p) == d and p[0] == B * n and p[-1] == B * (n + 1)
        out[n] = {"d": d, "path": p, "sec": round(time.time() - t, 1)}
        print(n, d, round(time.time() - t, 1), flush=True)
    mx = max(v["d"] for v in out.values())
    r = {"B": B, "n_tested": len(ns), "max_d": mx, "d_hist": {str(k): sum(1 for v in out.values() if v["d"] == k) for k in sorted(set(v["d"] for v in out.values()))}, "results": {str(n): v for n, v in out.items()}, "seconds": round(time.time() - t0, 1)}
    json.dump(r, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "D4B_B1e6_adversarial.json"), "w"), indent=1)
    print("max", mx, r["d_hist"], r["seconds"])
