"""Exact d_B(n) for the first members (n, n+L, n+2L) of every open residue class (B=10, 12, 10^6).  Full infinite graph, untruncated (known_upper=6)."""
import json, sys, os, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import exact_distance
from indep_check import check_path
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
out = {}
for B, f, per in [(12, "D4C_B12_closure.json", 3), (10, "D4A_B10_closure.json", 3), (10**6, "D4B_B1e6_cover.json", 3)]:
    J = json.load(open(os.path.join(R, f))); L = J["period"]; t0 = time.time(); res = {}; mx = 0; wit = None
    for o in J["open_residues_mod_period"]:
        for k in range(per):
            n = o + k * L
            if n < 1: continue
            d, p = exact_distance(B * n, B * (n + 1), 6); assert check_path(p) == d and p[0] == B * n and p[-1] == B * (n + 1)
            res[str(n)] = {"d": d, "path": p}
            if d > mx: mx, wit = d, n
    h = collections.Counter(v["d"] for v in res.values())
    out[str(B)] = {"period": L, "members_per_class": per, "n_checked": len(res), "hist": dict(sorted(h.items())), "max": mx, "max_witness_n": wit, "results": res, "seconds": round(time.time() - t0, 1)}
    print(B, dict(h), mx, wit, round(time.time() - t0), flush=True)
json.dump(out, open(os.path.join(R, "D4_open_class_members_exact.json"), "w"))
