"""v002-C  information content of the inner coordinate under the universally admissible move n -> 4n."""
import json, os, sys, math
res = {"part": "C", "claims": {}}

def outer_after(t, q, r, B):
    return (4 ** t * (B * q + r)) // B          # = floor(4^t n / B), n = Bq + r

# C1: formula q_t = 4^t q + floor(4^t r / B)
f_bad = 0
for B in (12, 1000, 10**6):
    for q in (0, 1, 7, 12345):
        for r in range(0, B, max(1, B // 997)):
            for t in range(0, 14):
                if outer_after(t, q, r, B) != 4 ** t * q + (4 ** t * r) // B:
                    f_bad += 1
res["claims"]["C1_formula_mismatches"] = f_bad

# C2: number of resolvable classes of r after t steps = min(4^t, B); injective iff 4^t >= B
rows = {}; ok = True
for B in (12, 1000, 4**5, 10**6, 3 * 10**6 + 1):
    tmin = next(t for t in range(0, 64) if 4 ** t >= B)
    per_t = []
    for t in range(0, tmin + 2):
        classes = len({(4 ** t * r) // B for r in range(B)})
        per_t.append({"t": t, "classes": classes, "min(4^t,B)": min(4 ** t, B)})
        ok &= classes == min(4 ** t, B)
    # injectivity threshold exactly at t = ceil(log_4 B)
    inj = {t["t"]: t["classes"] == B for t in per_t}
    ok &= all(inj[t] == (4 ** t >= B) for t in inj)
    rows[str(B)] = {"threshold_t=ceil(log4 B)": tmin, "bits_B": math.log2(B), "per_t": per_t}
res["claims"]["C2_resolution_by_horizon"] = rows

# C3: block independence (same class counts in every outer block q) for a small B
B = 360; ref = len({tuple(outer_after(t, 0, r, B) for t in range(0, 8)) for r in range(B)})
indep = all(len({tuple(outer_after(t, q, r, B) - 4 ** t * q for t in range(0, 8)) for r in range(B)}) == ref
            for q in (0, 1, 5, 99))
res["claims"]["C3_block_independence"] = {"B": B, "classes": ref, "independent_of_q": indep}

res["claims"]["C4_B=10^6"] = {"t_needed": next(t for t in range(64) if 4 ** t >= 10**6),
                             "4^9": 4 ** 9, "4^10": 4 ** 10, "9_steps_injective": len({(4 ** 9 * r) // 10**6 for r in range(10**6)}) == 10**6,
                             "10_steps_injective": len({(4 ** 10 * r) // 10**6 for r in range(10**6)}) == 10**6}
res["PASS"] = (f_bad == 0 and ok and indep and ref == B and res["claims"]["C4_B=10^6"]["t_needed"] == 10
               and not res["claims"]["C4_B=10^6"]["9_steps_injective"] and res["claims"]["C4_B=10^6"]["10_steps_injective"])
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "C_information.json"), "w"), indent=1)
print(json.dumps(res["claims"]["C4_B=10^6"]), " formula mismatches", f_bad, " PASS", res["PASS"]); sys.exit(0 if res["PASS"] else 1)
