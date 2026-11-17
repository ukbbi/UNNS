"""v013: recompute all headline statistics from the stored result files (compared with SUMMARY_v013.json by the verifier)."""
import sys, os, json, collections, statistics as S
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frontier_io import read_frontier
from primeflip import adjacency, bound, bfs_path
def tau_of(pts, C):
    for l, h in pts:
        if h <= C: return l
def lattice(res):
    R = os.path.join(res, "lattice"); divs = sorted(2**a * 5**b for a in range(7) for b in range(7))
    F = {D: read_frontier(os.path.join(R, "F_%d.txt" % D)) for D in divs}; cm = lambda D: 10**8 if D == 10**6 else max(100 * D, 10000)
    pairs = checks = skipped = viol = 0
    for D in divs:
        for D2 in divs:
            if D2 > D and D2 % D == 0:
                M = D2 // D; pairs += 1
                for n in range(1, 100):
                    for l, h in F[D][n][0]:
                        if h * M > cm(D2): skipped += 1; continue
                        checks += 1; t = tau_of(F[D2][n][0], h * M); viol += (t is None or t > l)
    tab = {}
    for D in divs:
        t = [F[D][n][0][-1][0] for n in range(1, 100) if F[D][n][1] == "*"]
        tab[str(D)] = {"connected_at_kappa": len(t), "mean_tau": round(S.mean(t), 2) if t else None, "max_tau": max(t) if t else None}
    return {"divisor_pairs": pairs, "checks": checks, "skipped_beyond_Cmax": skipped, "violations": viol, "per_scale": tab}
def descent(res):
    R = os.path.join(res, "descent"); tot = viol = 0; sl = collections.Counter(); combos = 0
    for line in open(os.path.join(R, "index.txt")):
        B, s, A = map(int, line.split()); combos += 1
        FB = read_frontier(os.path.join(R, "FB_%d.txt" % B)); FA = read_frontier(os.path.join(R, "FA_%d_s%d.txt" % (B, s)))
        for n in range(1, 100):
            for l, h in FA[n][0]:
                tb = tau_of(FB[n][0], max(h, B * (n + 1))); tot += 1
                if tb is None or tb > l + 2: viol += 1
                else: sl[l + 2 - tb] += 1
    return {"combinations": combos, "checks": tot, "violations": viol, "slack_distribution": sorted(sl.items())}
def chain(res):
    R = os.path.join(res, "chain"); B = 10**6; LAD = [160000, 7600, 361, 18, 4, 1]
    FB = read_frontier(os.path.join(R, "FB_1000000.txt")); per = {}; tot = viol = 0; best = {}
    for i, A in enumerate(LAD, 1):
        FA = read_frontier(os.path.join(R, "FC_%d.txt" % A)); v = c = 0
        for n in range(1, 100):
            for l, h in FA[n][0]:
                tb = tau_of(FB[n][0], max(h, B * (n + 1))); c += 1
                v += (tb is None or tb > l + 2 * i)
            t = tau_of(FA[n][0], B * (n + 1))
            if t is not None: best[n] = min(best.get(n, 99), 2 * i + t)
        per[str(A)] = {"level": i, "checks": c, "violations": v}; tot += c; viol += v
    ex = {n: FB[n][0][-1][0] for n in range(1, 100)}
    gap = collections.Counter(best[n] - ex[n] for n in range(1, 100) if n in best)
    return {"per_scale": per, "checks": tot, "violations": viol, "best_chain_bound_minus_exact": sorted(gap.items()), "pairs_with_bound": len(best), "max_best_bound": max(best.values()), "mean_best_bound": round(S.mean(best.values()), 2)}
def primes(res):
    out = {}
    for B, hi in ((100, 3005), (1000, 3005)):
        F = read_frontier(os.path.join(res, "FP_%d.txt" % B)); adj = adjacency(hi); ex = []; app = 0; viol = 0; sl = []; kap = 0
        for p, (pts, fl) in sorted(F.items()):
            l, h = pts[-1]; kap += h == (p + 1) ** 2; ex.append(l)
            r = bound(p, B, adj)
            if r: app += 1; viol += r[0] < l; sl.append(r[0] - l)
        out["B=%d" % B] = {"primes": len(F), "kappa_equals_(p+1)^2": kap, "exact_mean": round(S.mean(ex), 2), "exact_max": max(ex), "exact_distribution": sorted(collections.Counter(ex).items()),
                           "composite_applicable": app, "composite_below_exact": viol, "slack_mean": round(S.mean(sl), 2), "slack_max": max(sl)}
    L = [l.split() for l in open(os.path.join(res, "PF_B6.txt"))]; ok = [l for l in L if l[1] != "none"]
    out["B=10^6 sample"] = {"primes": len(L), "composite_applicable": len(ok), "length_distribution": sorted(collections.Counter(int(l[1]) for l in ok).items()), "first_leg_lengths": sorted(collections.Counter(int(l[2]) for l in L if l[2] != "None").items())}
    return out
def compute(res):
    return {"lattice": lattice(res), "descent": descent(res), "chain": chain(res), "primes": primes(res)}
if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); res = os.path.join(here, "..", "results"); S_ = compute(res)
    json.dump(S_, open(os.path.join(res, "SUMMARY_v013.json"), "w"), indent=1)
    print(json.dumps({k: (v if k != "lattice" else {x: y for x, y in v.items() if x != "per_scale"}) for k, v in S_.items()}, indent=1))
