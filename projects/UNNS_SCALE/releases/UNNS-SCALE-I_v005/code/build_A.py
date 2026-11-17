"""Part A builder: assemble the finite-window theorem record for B = 10^6, 1 <= n <= 999999."""
import json, os, sys, time
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.join(here, ".."); res = os.path.join(root, "results")
V4 = os.path.join(root, "..", "..", "v004", "UNNS-SCALE-I_v004") if not os.path.exists(os.path.join(root, "..", "UNNS-SCALE-I_v004")) else os.path.join(root, "..", "UNNS-SCALE-I_v004")
sys.path.insert(0, here)
from exact_lib import exact_distance
from indep_check import check_path
B = 10**6; N = 999999
D = json.load(open(os.path.join(V4, "results", "D4B_B1e6_cover.json")))
ids = [{"M": c["M"], "r": c["r"], "t0": c["t0"], "steps": c["steps"]} for c in D["direct_identities"] if len(c["steps"]) <= 4]
d1, p1 = exact_distance(B, 2 * B, 6); assert check_path(p1) == d1
json.dump({"B": B, "range": [1, N], "identities": ids, "n1_exact": {"d": d1, "path": p1},
           "note": "identities valid for n = M t + r, t >= t0; members below t0 (only n=1 in the window) are handled by n1_exact; the 614 remaining n are in A_window_uncovered_614.json"},
          open(os.path.join(res, "A_window_identities_and_n1.json"), "w"))
print(len(ids), "identities; n=1 exact distance", d1)
