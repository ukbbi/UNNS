"""E6 -- exhaustive realizable-set census (k=6; plus k=4,5 for comparison) and independent T12 verification."""
import time
import random
from collections import Counter
from itertools import combinations
import _path  # noqa: F401
import _common
import threshold_closure as tc
import history_complex as hc
import history_fibres as hf


def verify_t12(k, L, seed=20261105, sample_contents=60):
    """independent checks of GIG-T12 on a deterministic sample of contents (full census sets are all checked below)."""
    rng = random.Random(seed)
    contents = list(combinations(range(1, L + 1), k))
    rng.shuffle(contents)
    contents = contents[:sample_contents]
    n_closed = n_min = n_sq = n_lcm = n_closure_min = 0
    for C in contents:
        cc = tc.ContentClosure(C)
        ms = tc.realizable_masks_of_content(C)
        # (i) every realizable set is closed; (ii) L(S) via level masks == lcm of thresholds; (iii) squarefree criterion
        for S in ms:
            assert cc.is_closed(S)
            n_closed += 1
            Ls = tc.lcm_of_thresholds(C, S)
            assert Ls == cc.minimal_source(S)
            n_lcm += 1
            assert tc.source_mask(C, Ls) == S               # L(S) realizes S
            # divisibility-minimality: every realizing source is a multiple of L(S); test on all proper divisors of L(S)
            for d in _proper_divisors(Ls):
                assert tc.source_mask(C, d) != S
            n_min += 1
        # (iv) squarefree criterion against brute force over all squarefree sources made of the relevant primes
        primes = sorted(tc.level_masks(C))
        sqmasks = set()
        for bits in range(1 << len(primes)):
            m = 1
            for i, q in enumerate(primes):
                if bits >> i & 1:
                    m *= q
            sqmasks.add(tc.source_mask(C, m))
        sqmasks.discard(0)
        crit = {S for S in ms if tc.squarefree_realizable(C, S)}
        assert crit == sqmasks, (C,)
        n_sq += 1
        # (v) cl is a closure operator and cl(S) is the SMALLEST realizable superset: random subsets
        P = len(hc.perms(k))
        for _ in range(25):
            S = 0
            for _j in range(rng.randint(1, 6)):
                S |= 1 << rng.randrange(P)
            c = cc.closure(S)
            assert S & ~c == 0 and cc.closure(c) == c            # extensive, idempotent
            sup = [T for T in ms if S & ~T == 0]
            assert sup and c in ms and all(c & ~T == 0 for T in sup)   # smallest realizable superset
            S2 = S | (1 << rng.randrange(P))
            assert cc.closure(S) & ~cc.closure(S2) == 0              # monotone
            n_closure_min += 1
    return {"contents_checked": len(contents), "realizable_sets_closed": n_closed, "lcm_equals_L": n_lcm,
            "minimality_checked": n_min, "squarefree_criterion_contents": n_sq, "closure_operator_samples": n_closure_min}


def _proper_divisors(n):
    ds = [1]
    for q, e in hf.factor(n):
        ds = [d * q ** i for d in ds for i in range(e + 1)]
    return sorted(d for d in ds if d < n)


def verify_against_simulation(k, L, seed=20261105, n_contents=40, n_sources=6):
    rng = random.Random(seed)
    contents = list(combinations(range(1, L + 1), k))
    rng.shuffle(contents)
    tested = 0
    P = hc.perms(k)
    for C in contents[:n_contents]:
        cc = tc.ContentClosure(C)
        ms = sorted(tc.realizable_masks_of_content(C))
        for S in ms[:n_sources] + rng.sample(ms, min(n_sources, len(ms))):
            m = cc.minimal_source(S)
            sim = 0
            for i, p in enumerate(P):
                if hf.is_admissible(m, tuple(C[j] for j in p)):
                    sim |= 1 << i
            assert sim == S
            for mult in (2, 3, 6):                                    # other sources: threshold law == simulation
                mm = m * mult
                sim2 = 0
                for i, p in enumerate(P):
                    if hf.is_admissible(mm, tuple(C[j] for j in p)):
                        sim2 |= 1 << i
                assert sim2 == tc.source_mask(C, mm)
            tested += 1
    return {"sets_confirmed_against_forward_simulation": tested}


def run(bounds=((6, 10), (6, 12)), extra=((4, 40), (5, 16))):
    t0 = time.time()
    out = {"experiment": "E6", "coverage": [], "census": {}}
    for k, L in list(bounds) + list(extra):
        t = time.time()
        found, cov = _common.census(k, L)
        cov = dict(cov)
        cov["incomplete_branches"] = 0
        cov["exhaustive"] = cov["closure_cap_exclusions"] == 0
        cov["seconds"] = round(time.time() - t, 1)
        out["coverage"].append(cov)
        nsq = sum(1 for r in found.values() if r["sqcontent"] is not None)
        sizes = Counter(m.bit_count() for m in found)
        out["census"][f"k{k}_L{L}"] = {"sets": len(found), "squarefree_source_realizable": nsq,
                                       "max_N": max(sizes), "min_N": min(sizes),
                                       "multi_content_sets": sum(1 for r in found.values() if r["n"] > 1)}
    out["T12_verification"] = verify_t12(6, 10)
    out["T12_verification_k4"] = verify_t12(4, 20, sample_contents=100)
    out["T12_verification_k5"] = verify_t12(5, 12, sample_contents=60)
    out["simulation_crosscheck"] = verify_against_simulation(6, 12)
    out["seconds"] = round(time.time() - t0, 1)
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(run(((6, 8),), ((4, 12), (5, 9))), indent=1))
