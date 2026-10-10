from __future__ import annotations
import random


def coverage_block_stat(rows):
    by_seed = {}
    for r in rows:
        c = r.get("coverage_C")
        if c is None:
            continue
        by_seed.setdefault(int(r["seed"]), []).append((float(c), float(r["solution_recall"])))
    total = 0.0
    for vals in by_seed.values():
        if len(vals) < 2:
            continue
        cs = [x[0] for x in vals]
        rs = [x[1] for x in vals]
        mc = sum(cs) / len(cs)
        mr = sum(rs) / len(rs)
        total += sum((c - mc) * (r - mr) for c, r in vals)
    return total


def blocked_permutation_coverage_trend(rows, permutations: int, seed: int):
    """One-sided within-family permutation test of recall against realized coverage C."""
    rows = [dict(r) for r in rows if r.get("coverage_C") is not None]
    observed = coverage_block_stat(rows)
    by_seed = {}
    for r in rows:
        by_seed.setdefault(int(r["seed"]), []).append(dict(r))
    rng = random.Random(int(seed))
    extreme = 0
    for _ in range(int(permutations)):
        perm_rows = []
        for vals in by_seed.values():
            cvals = [float(v["coverage_C"]) for v in vals]
            rng.shuffle(cvals)
            for v, c in zip(vals, cvals):
                x = dict(v)
                x["coverage_C"] = c
                perm_rows.append(x)
        if coverage_block_stat(perm_rows) >= observed - 1e-15:
            extreme += 1
    p = (extreme + 1) / (int(permutations) + 1)
    return {
        "statistic_T_C": observed,
        "permutations": int(permutations),
        "extreme": int(extreme),
        "p_one_sided": p,
    }
