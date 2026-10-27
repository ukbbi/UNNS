#!/usr/bin/env python3
"""GEO-I v011 Programme B experiment.  python3 experiments/w2_attack.py [--k5] [--random N]
(1) brute force over ALL subsets of AG(k-1,2), k=3,4 (and k=5 with --k5): spanning, 1 in C, minimal non-embedded by the E1 criterion, W2 count;
(2) the inherited nullity-6 classification (215 classes): identities, W2, bound n_2 >= p-1 (p >= 9);
(3) random minimal boxes at nullity 7, 8 (identities + bound);
(4) exact threshold table of the W2 inequality for p <= 400;
(5) knapsack/Parseval feasibility of a W2-failing profile for k = 4..14 (supplementary, not used in the proof).
Writes output/data/v11_w2.json."""
import os, sys, json, random, itertools, time
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); sys.path.insert(0, os.path.join(ROOT, 'theory'))
import circuit_partitions as CP
DATA = os.path.join(ROOT, 'output', 'data')


def brute(k):
    m = k - 1; top = 1 << m; pts = [top | a for a in range(1 << m)]; res = []; n_sub = 0
    for mask in range(1, 1 << len(pts)):
        X = [pts[i] for i in range(len(pts)) if mask >> i & 1]
        if len(X) < k + 1 or CP.rank(X) < k: continue
        n_sub += 1; c = CP.circuits(X, k); n = len(X)
        P = CP.partitions(c, n)
        if len(P) < 2: continue                                   # F1: minimal => two partitions of the full set
        if not CP.is_minimal_E1(X, k): continue
        tb = CP.two_block_partitions(c, n)
        ok = CP.counting_identity(P, k) and CP.parseval_identity(c, P, n, k)
        res.append({'p': n, 'n_two_blocks': len(tb), 'identities': ok, 'bound_ok': (n < 9) or len(tb) >= n - 1})
    return {'k': k, 'spanning_subsets': n_sub, 'minimal_subsets': len(res), 'min_two_blocks': min(r['n_two_blocks'] for r in res), 'all_W2': all(r['n_two_blocks'] >= 2 for r in res),
            'all_identities': all(r['identities'] for r in res), 'all_bound': all(r['bound_ok'] for r in res), 'p_values': sorted({r['p'] for r in res})}


def inherited(k):
    d = json.load(open(os.path.join(DATA, 'v10_binary%d.json' % k)))['minimal']; mn = 10 ** 9; bad = 0
    for r in d:
        X = r['support']; c = CP.circuits(X, k); n = len(X); P = CP.partitions(c, n); tb = CP.two_block_partitions(c, n); mn = min(mn, len(tb))
        ok = CP.counting_identity(P, k) and CP.parseval_identity(c, P, n, k) and CP.vector_space_partition(c, P, X, k) and CP.parseval_direct(X, k) and len(tb) >= 2 and (n < 9 or len(tb) >= n - 1)
        bad += (not ok)
    return {'k': k, 'classes': len(d), 'violations': bad, 'min_two_blocks': mn}


def random_boxes(k, trials, seed):
    rng = random.Random(seed); m = k - 1; top = 1 << m; pts = [top | a for a in range(1 << m)]; tested = 0; viol = 0; mn = 10 ** 9; ps = []
    for _ in range(trials):
        n = rng.randint(k + 1, min(len(pts), 2 * k + 6)); X = rng.sample(pts, n)
        if CP.rank(X) < k: continue
        c = CP.circuits(X, k); P = CP.partitions(c, n)
        if len(P) < 2 or not CP.counting_identity(P, k): continue       # rigidity filter (heuristic prefilter; the identity is what is tested next)
        tested += 1; tb = CP.two_block_partitions(c, n); mn = min(mn, len(tb)); ps.append(n)
        if not (CP.parseval_identity(c, P, n, k) and len(tb) >= 2 and (n < 9 or len(tb) >= n - 1)): viol += 1
    return {'k': k, 'tested': tested, 'violations': viol, 'min_two_blocks': mn if tested else None, 'p_range': [min(ps), max(ps)] if ps else None}


def smin(p, m):
    q, r = divmod(p, m); return (m - r) * q * q + r * (q + 1) ** 2


def feasibility(k):
    """Parseval/counting knapsack with block sizes >= 2: is a profile with n_2 in {0,1} numerically possible?  (supplementary)"""
    bad = []
    for p in range(k + 1, (1 << (k - 1)) + 1):
        for n2 in (0, 1):
            target = (1 << k) - 2 - 2 * n2; items = []
            for m in range(3, k):
                if p < 2 * m: continue
                items.append(((1 << m) - 2, (1 << m) * smin(p, m) - 2 * p * p))
            INF = float('inf'); best = [INF] * (target + 1); best[0] = 0
            for t_ in range(1, target + 1):
                b = INF
                for w, c_ in items:
                    if w <= t_ and best[t_ - w] + c_ < b: b = best[t_ - w] + c_
                best[t_] = b
            if best[target] <= p * ((1 << k) - 2 * p): bad.append([p, n2])
    return bad


if __name__ == '__main__':
    t0 = time.time(); out = {'release': 'v011'}
    out['brute'] = [brute(3), brute(4)] + ([brute(5)] if '--k5' in sys.argv else [])
    out['inherited'] = [inherited(k) for k in (3, 4, 5, 6)]
    out['random'] = [random_boxes(7, 1500, 11), random_boxes(8, 400, 12)]
    out['threshold'] = {'p_checked': [6, 400], 'true_for_all_p_ge_9': all(CP.w2_threshold_ok(p) for p in range(9, 401)), 'false_at': [p for p in range(6, 9) if not CP.w2_threshold_ok(p)]}
    out['knapsack_feasible_profiles'] = {str(k): feasibility(k) for k in range(4, 13)}
    out['seconds'] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(DATA, 'v11_w2.json'), 'w'), indent=1); print(json.dumps({k: v for k, v in out.items() if k != 'knapsack_feasible_profiles'}, indent=1)[:3000]); print(out['knapsack_feasible_profiles'])
