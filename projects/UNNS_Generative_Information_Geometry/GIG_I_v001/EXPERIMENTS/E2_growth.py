"""E2 -- complete-history counts of 72^r by exact dynamic programming (GIG-T5)."""
import json, sys
from math import comb, log2
import _path
from history_fibres import count_complete, count_complete_by_source, complete_histories, is_admissible, endpoint
import information as inf

REFERENCE = [4, 100, 3601, 194864, 14177856, 1258011667]


def binomial_family(r):
    """the C(2r,r) words 1^r followed by every arrangement of r labels 1 and r labels 2, from source 1."""
    from itertools import combinations
    out = []
    for twos in combinations(range(2 * r), r):
        tail = [1] * (2 * r)
        for i in twos:
            tail[i] = 2
        out.append((1, (1,) * r + tuple(tail)))
    return out


def run(rmax=7):
    rows = []
    for r in range(1, rmax + 1):
        t = 72 ** r
        n = count_complete(t)
        row = {"r": r, "count": n, "A_bits": inf.fmt(inf.hartley(n), 10),
               "lower_bound_binom": comb(2 * r, r), "log2_lower_bound": round(log2(comb(2 * r, r)), 10),
               "A_over_r": inf.fmt(inf.hartley(n) / r, 8)}
        if r <= 7:   # the by-source refinement is memory-heavy beyond r = 7
            row["n_sources"] = len(count_complete_by_source(t))
        if r > 1:
            row["increment_A_bits"] = inf.fmt(inf.hartley(n) - inf.hartley(count_complete(72 ** (r - 1))), 8)
        row["bound_holds"] = n >= comb(2 * r, r)
        if r <= 4:  # enumeration cross-check; the DP is the only method used beyond that
            row["enumerated"] = sum(1 for _ in complete_histories(t))
        if r <= 5:
            fam = binomial_family(r)
            row["family_size"] = len(fam)
            row["family_all_complete_admissible_and_end_at_72^r"] = all(is_admissible(*h) and endpoint(*h) == t for h in fam) and len(set(fam)) == len(fam)
        rows.append(row)
    ok_ref = [x["count"] for x in rows[:6]] == REFERENCE
    return {"source_convention": "complete-history fibre F_t, t = 72^r", "method": "memoised DP count(t) = sum over reverse edges (squarefree t: 1)",
            "reference_sequence": REFERENCE, "matches_reference_r1_to_6": ok_ref, "rows": rows}


if __name__ == "__main__":
    rmax = int(sys.argv[1]) if len(sys.argv) > 1 else 7   # e.g. `python E2_growth.py 10` (about 5 minutes) for the long table
    print(json.dumps(run(rmax), indent=1))
