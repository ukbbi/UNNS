"""v002-A  exact prime-factor boundary law and its asymptotic mean."""
import json, os, random, sys
import numpy as np
from math import gcd, log, isqrt
from scale_lib import factor, merge, neighbours
from boundary_lib import eps_closed, c_B, predicted_mean, tau_mean_const, s_mean_const, tau_e, sq1_e, EULER_GAMMA

random.seed(20261116)
res = {"part": "A", "claims": {}}

# ---- A1: closed form vs enumeration of non-lattice neighbours --------------------------------
Bs = [2, 6, 10, 12, 100, 360, 1000, 2**10, 7**3 * 11, 30030, 10**4, 10**6, 10**6 * 3]
a1 = {}
bad_total = 0
for B in Bs:
    fB = factor(B)
    xs = list(range(1, 1501)) + [random.randrange(1501, 10**6) for _ in range(500)]
    bad = 0
    for x in xs:
        fx = factor(x)
        nb = neighbours(merge(fB, fx))
        enum = sum(1 for (_, _, v) in nb if v % B != 0)
        if enum != eps_closed(fB, fx):
            bad += 1
    a1[str(B)] = {"vertices": len(xs), "mismatches": bad}
    bad_total += bad
res["claims"]["A1_closed_form_vs_enumeration"] = a1

# ---- A1': coprime corollary  eps_B(x) = (tau(B)-1) tau(x) + s(B) (s(x)+1)  for gcd(x,B)=1 ------
cor_bad = 0; cor_n = 0
for B in [10, 12, 360, 10**6, 30030]:
    fB = factor(B)
    for x in range(1, 4000):
        if gcd(x, B) != 1: continue
        fx = factor(x); cor_n += 1
        lhs = eps_closed(fB, fx)
        rhs = (tau_e(fB) - 1) * tau_e(fx) + (sq1_e(fB) - 1) * sq1_e(fx)
        cor_bad += lhs != rhs
res["claims"]["A1b_coprime_corollary"] = {"checked": cor_n, "mismatches": cor_bad}

# ---- A2: asymptotic mean -------------------------------------------------------------------------
from sieve_lib import tau_sieve, valuation, tau_B_sum_exact, s_sum_exact

# validate the exact s-identity against direct enumeration at small X
chk = {}
for B in (12, 360, 1000):
    fB = factor(B); X = 3000
    direct = sum((sq1_e(merge(fB, factor(x))) - sq1_e(factor(x))) for x in range(1, X + 1))
    chk[str(B)] = (direct == s_sum_exact(X, B))
res["claims"]["A2_s_identity_vs_direct"] = chk

a2 = {}
XS = [10**4, 10**5, 10**6, 4 * 10**6]
tau_full = tau_sieve(max(XS))
for B in [10, 12, 360, 1000, 10**6]:
    fB = factor(B); cB = c_B(fB); rows = []
    for X in XS:
        sT = tau_B_sum_exact(X, fB, tau_full[:X + 1]); sT0 = int(tau_full[1:X + 1].sum())
        tau_part = (sT - sT0) / X
        s_part = s_sum_exact(X, B) / X
        c, d = tau_mean_const(fB)
        tau_pred = (c - 1) * (log(X) + 2 * EULER_GAMMA - 1) - d
        K = s_mean_const(fB)
        rows.append({"X": X, "mean_eps": tau_part + s_part, "tau_part": tau_part, "tau_part_pred": tau_pred,
                     "tau_err": tau_part - tau_pred, "s_part": s_part, "K_B": K, "s_err": s_part - K,
                     "pred_total": tau_pred + K, "total_err": tau_part + s_part - tau_pred - K})
    # slope of mean vs log X between the two largest decades
    slope = (rows[-1]["mean_eps"] - rows[-2]["mean_eps"]) / (log(rows[-1]["X"]) - log(rows[-2]["X"]))
    a2[str(B)] = {"c_B": cB, "leading_coeff_c_B_minus_1": cB - 1, "observed_slope_last_two_X": slope, "rows": rows}
res["claims"]["A2_asymptotic_mean"] = a2
for B, v in a2.items():
    r = v["rows"][-1]
    print(f"B={B}: lead coeff {v['leading_coeff_c_B_minus_1']:.4f}, slope {v['observed_slope_last_two_X']:.4f}; "
          f"X={r['X']}: tau_err={r['tau_err']:+.4f} s_err={r['s_err']:+.4f} total_err={r['total_err']:+.4f}")

res["PASS"] = (bad_total == 0 and cor_bad == 0 and all(chk.values()) and
               all(abs(v["rows"][-1]["tau_err"]) < 0.05 * max(1.0, v["leading_coeff_c_B_minus_1"]) for v in a2.values()))
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "A_boundary.json"), "w"), indent=1)
print("A1 mismatches:", bad_total, " coprime:", cor_bad, " PASS", res["PASS"]); sys.exit(0 if res["PASS"] else 1)
