"""Gate 3 (first slice) -- distance behaviour of the scale copy.

Exact fact (T2):  d_G(Bu,Bv) <= d_G(u,v).
Experiment: how often is the inequality strict, i.e. does the full graph offer
a shortcut through off-lattice vertices?

Distances come from exact bidirectional BFS inside finite truncations G[1..L].
A truncated distance is the length of a real path, hence an UPPER bound for the
true distance.  The scaled graph is truncated at B*L_base4 so that it contains
the scaled copy of the base graph exactly (T2); therefore  d_scaled <= d_base4
must hold in every run, and a violation would falsify T2.
Strictness is reported only for pairs whose base distance is finite and
unchanged under 4x truncation ("stable"); this is evidence, not a certificate,
of the true base distance.  See reports for the exact status of each claim.
"""
import json, os, sys, time
from scale_lib import build_csr, csr_distance

INF = 10 ** 9
res = {"gate": 3, "slice": "distance comparison, successor and doubling pairs", "runs": {}}
t0 = time.time()

def run(B, L1, xmax):
    c1, c4, cs = build_csr(L1), build_csr(4 * L1), build_csr(B * 4 * L1)
    rows = []
    for kind, pair in (("succ", lambda x: (x, x + 1)), ("double", lambda x: (x, 2 * x))):
        for x in range(1, xmax + 1):
            a, b = pair(x)
            d1 = csr_distance(c1, a, b); d4 = csr_distance(c4, a, b); dB = csr_distance(cs, B * a, B * b)
            rows.append([kind, x, a, b, INF if d1 is None else d1, INF if d4 is None else d4,
                         INF if dB is None else dB])
    stable = [r for r in rows if r[4] == r[5] and r[5] < INF]
    viol = [r for r in rows if r[6] > r[5]]
    strict = [r for r in stable if r[6] < r[5]]
    return {"B": B, "base_L": L1, "base4_L": 4 * L1, "scaled_L": B * 4 * L1,
            "pairs": len(rows), "stable_pairs": len(stable),
            "violations_of_T2 (scaled > base4)": len(viol),
            "stable_strict (scaled < base)": len(strict),
            "stable_equal": sum(1 for r in stable if r[6] == r[5]),
            "max_base_stable": max(r[5] for r in stable), "max_scaled_all": max(r[6] for r in rows),
            "scaled_gap_histogram_stable": {str(g): sum(1 for r in stable if r[5] - r[6] == g)
                                            for g in sorted({r[5] - r[6] for r in stable})},
            "examples_strict": strict[:15], "rows": rows}

for B, L1, xmax in [(2, 200000, 200), (3, 200000, 200), (6, 200000, 150), (10, 100000, 150), (100, 10000, 80)]:
    res["runs"][str(B)] = r = run(B, L1, xmax)
    print(f"B={B}: pairs={r['pairs']} stable={r['stable_pairs']} strict={r['stable_strict (scaled < base)']} "
          f"equal={r['stable_equal']} T2-violations={r['violations_of_T2 (scaled > base4)']} "
          f"gaps={r['scaled_gap_histogram_stable']} t={time.time()-t0:.0f}s", flush=True)

c = build_csr(12_000_000)
res["sanity_d_163_164_trunc1.2e7"] = csr_distance(c, 163, 164)
res["large_truncation_recheck_L=1.2e7"] = []
for Bk in ("2", "10"):
    for kind, x, a, b, d1, d4, dB in res["runs"][Bk]["examples_strict"][:8]:
        dl = csr_distance(c, a, b)
        res["large_truncation_recheck_L=1.2e7"].append({"B": int(Bk), "pair": [a, b], "base4": d4, "base_1.2e7": dl, "scaled": dB, "unchanged": dl == d4})
res["PASS"] = all(r["violations_of_T2 (scaled > base4)"] == 0 for r in res["runs"].values()) and all(e["unchanged"] for e in res["large_truncation_recheck_L=1.2e7"])
json.dump(res, open(os.path.join(os.path.dirname(__file__), "..", "results", "gate3_distance.json"), "w"))
print("d(163,164) =", res["sanity_d_163_164_trunc1.2e7"], " PASS", res["PASS"]); sys.exit(0 if res["PASS"] else 1)
