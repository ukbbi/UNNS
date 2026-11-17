"""Builds the v004 result files from the raw cover outputs (/tmp/*.json) and runs exact checks on open-class representatives."""
import json, glob, sys, os, time, collections
from fractions import Fraction
from math import gcd
sys.path.insert(0, '.')
import numpy as np
from accounting import union_open, v003, G
from cover2 import vp
from poly_check import verify_identity
from exact_lib import exact_distance
from indep_check import check_path
R = "../results"; RAW = R + "/raw"
def load_ids(files):
    out = []; seen = set()
    for f in files:
        for c in json.load(open(f))["done"]:
            k = (c["M"], c["r"])
            if k not in seen: seen.add(k); out.append({"M": c["M"], "r": c["r"], "length": c["length"], "t0": c["t0"], "steps": [[d, list(l)] for d, l in c["steps"]]})
    return out
def opens(classes):
    L, cov = union_open(classes); o = np.nonzero(~cov)[0]
    return L, [int(x) for x in o]
def val_hist(L, o):
    c = collections.Counter(); g = 0
    for n in o:
        g = gcd(g, n + 1)
    return g
def classes_of(ids): return [(c["M"], c["r"]) for c in ids]
# ---- Theorem G
Gids = [{"M": 4, "r": 1, "length": 4, "steps": [["+", [4, 1]], ["-", [2, 0]], ["+", [1, 0]], ["-", [2, 1]]]},
        {"M": 16, "r": 7, "length": 5, "steps": [["+", [16, 7]], ["-", [2, 0]], ["+", [1, 0]], ["-", [2, 1]], ["-", [1]]]}]
for c in Gids: c["t0"] = verify_identity(1, c["M"], c["r"], [(d, l) for d, l in c["steps"]])[1]
# ---- B=10
b10 = load_ids(glob.glob(RAW + "/fcg_b10v_*.json") + [RAW + "/fcg_b10_359.json", RAW + "/fcg_b10res.json"])
b10_base = v003(10, 5) + classes_of(Gids)
L10, o10 = opens(b10_base + classes_of(b10))
L10_v3, o10_v3 = opens(v003(10, 5))
pend10 = []
json.dump({"B": 10, "K": 5, "new_identities": b10, "inherited": "v003 D2_B10_K5 identities + Theorem G classes",
           "period": L10, "open_residues_mod_period": o10, "open_density": f"{len(o10)}/{L10}", "open_density_float": len(o10) / L10,
           "v003_open_density": f"{len(o10_v3)}/{L10_v3}", "gcd_n_plus_1_over_open": val_hist(L10, o10),
           "n60_witness": "see D1_B10_N6000.json first_witness['5'] (exact d_10(60)=5)"}, open(f"{R}/D4A_B10_closure.json", "w"), indent=1)
print("B=10 open", len(o10), L10, len(o10) / L10, "gcd", val_hist(L10, o10), "new identities", len(b10))
# ---- B=12
b12 = load_ids([RAW + "/fcg_b12q.json", RAW + "/fcg_b12p.json"])
L12, o12 = opens(v003(12, 4) + classes_of(Gids) + classes_of(b12))
json.dump({"B": 12, "K": 5, "new_identities": b12, "inherited": "v003 D2_B12_K4 identities (K=4) + Theorem G classes", "period": L12, "open_residues_mod_period": o12,
           "open_density": f"{len(o12)}/{L12}", "open_density_float": len(o12) / L12, "gcd_n_plus_1_over_open": val_hist(L12, o12),
           "d12_25199": 5}, open(f"{R}/D4C_B12_closure.json", "w"), indent=1)
print("B=12 open", len(o12), L12, len(o12) / L12, "gcd", val_hist(L12, o12))
# ---- B=10^6
m6 = load_ids([RAW + "/fcg_m6run.json"]); m6k4 = [c for c in m6 if c["length"] <= 4]
divs = [(2, 5), (4, 5), (5, 5)]
inherited = b10_base + classes_of(b10) + [x for (B, K) in divs for x in v003(B, K)]
L6a, o6a = opens(inherited)                      # inherited from divisors only
L6, o6 = opens(inherited + classes_of(m6))       # + direct B=10^6 identities
json.dump({"B": 10**6, "direct_identities": m6, "n_direct": len(m6), "n_direct_len4": len(m6k4),
           "inherited_from_divisors": "B=10 identities (v003+v004), Theorem G, B=2,4,5 K=5 identities (pointwise law d_{10^6}(n)<=d_A(n), A|10^6)",
           "open_density_inherited_only": f"{len(o6a)}/{L6a}", "open_density_inherited_float": len(o6a) / L6a,
           "period": L6, "open_residues_mod_period": o6, "open_density": f"{len(o6)}/{L6}", "open_density_float": len(o6) / L6,
           "direct_cover_pending_fronts": json.load(open(RAW + "/fcg_m6run.json"))["pending"][:5], "direct_cover_open_density_float_K4_run": 0.00061602}, open(f"{R}/D4B_B1e6_cover.json", "w"), indent=1)
print("B=1e6 open inherited", len(o6a) / L6a, "combined", len(o6), L6, len(o6) / L6, "gcd", val_hist(L6, o6))
# ---- exact distances at B=10^6 for representatives of open classes (members in [1, 3*period])
t0 = time.time(); rep = {}
cands = sorted(o6)[:400]
for n in cands:
    if n < 1: n += L6
    d, p = exact_distance(10**6 * n, 10**6 * (n + 1), 5); assert check_path(p) == d
    rep[str(n)] = {"d": d, "path": p}
hist = collections.Counter(v["d"] for v in rep.values())
json.dump({"B": 10**6, "description": "exact d_B(n) for the smallest representative n of each open residue class of the combined cover", "n_checked": len(rep), "hist": dict(hist), "results": rep, "seconds": round(time.time() - t0, 1)}, open(f"{R}/D4B_B1e6_open_class_representatives.json", "w"), indent=1)
print("open-class reps at 1e6:", dict(hist), round(time.time() - t0))
