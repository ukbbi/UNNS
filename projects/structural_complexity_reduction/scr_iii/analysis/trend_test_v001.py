from __future__ import annotations
import random
from typing import Iterable, Mapping, Sequence


def block_stat(rows):
    by_seed = {}
    for r in rows:
        by_seed.setdefault(int(r["seed"]), []).append((float(r["q"]), float(r["solution_recall"])))
    total = 0.0
    for seed, vals in by_seed.items():
        if len(vals) < 2:
            continue
        qs = [x[0] for x in vals]; rs = [x[1] for x in vals]
        mq = sum(qs)/len(qs); mr = sum(rs)/len(rs)
        total += sum((q-mq)*(r-mr) for q,r in vals)
    return total


def blocked_permutation_trend(rows, permutations: int, seed: int):
    rows = list(rows)
    observed = block_stat(rows)
    by_seed = {}
    for r in rows:
        by_seed.setdefault(int(r["seed"]), []).append(dict(r))
    rng = random.Random(int(seed))
    extreme = 0
    for _ in range(int(permutations)):
        perm_rows = []
        for _, vals in by_seed.items():
            qvals = [float(v["q"]) for v in vals]
            rng.shuffle(qvals)
            for v, q in zip(vals, qvals):
                x = dict(v); x["q"] = q; perm_rows.append(x)
        if block_stat(perm_rows) >= observed - 1e-15:
            extreme += 1
    p = (extreme + 1) / (int(permutations) + 1)
    return {"statistic_T": observed, "permutations": int(permutations), "extreme": extreme, "p_one_sided": p}
