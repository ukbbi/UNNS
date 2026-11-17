"""v014: aggregate statistics from stored data (sweep digits + exception tables)."""
import sys, os, glob, json, collections
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); res = os.path.join(here, "..", "results")
def rd(f):
    d = {}
    for l in open(f):
        n, v = map(int, l.split()); d[n] = v
    return d
def sweep(res=res):
    parts = sorted(glob.glob(os.path.join(res, "sweep_A4", "A4_*.txt"))); s = "".join(open(f).read() for f in parts)
    return s
def compute(res=res):
    s = sweep(res); N = len(s); cnt = collections.Counter(s); exc = [i + 1 for i, c in enumerate(s) if c == "9"]
    el = [int(x) for x in open(os.path.join(res, "EXC_A4_gt6.txt")).read().split()]
    a4 = rd(os.path.join(res, "exc", "EXC_A4_R4.txt")); a1 = rd(os.path.join(res, "exc", "EXC_A1_R4.txt")); a18 = rd(os.path.join(res, "exc", "EXC_A18_R4_on_eq8.txt"))
    a361 = rd(os.path.join(res, "exc", "EXC_A361_R3.txt")); a7600 = rd(os.path.join(res, "exc", "EXC_A7600_R3.txt")); a160 = rd(os.path.join(res, "exc", "EXC_A160000_R3.txt"))
    best = {}; who = collections.Counter()
    for n in el:
        c = [(10 + a4[n], 4), (12 + a1[n], 1)]
        for A, d, i in ((18, a18, 4), (361, a361, 3), (7600, a7600, 2), (160000, a160, 1)):
            if n in d and d[n] < 9999: c.append((2 * i + d[n], A))
        best[n] = min(c); who[best[n][1]] += 1
    allb = collections.Counter({10 + int(k): v for k, v in cnt.items() if k != "9"}); allb.update(collections.Counter(b[0] for b in best.values()))
    fm = lambda d: dict(sorted(collections.Counter(d.values()).items()))
    return dict(N=N, tau4_counts={k: cnt[k] for k in sorted(cnt)}, n_exceptions=len(exc), exc_min=exc[0], exc_max=exc[-1], exc_list_matches=(exc == el), exc_by_100k=[sum(1 for e in exc if lo <= e < lo + 100000) for lo in range(0, 1000000, 100000)],
        tau4_on_exceptions=fm(a4), tau1_on_exceptions=fm(a1), tau18_on_eq8=fm(a18), tau361_on_exceptions=fm(a361), tau7600_on_exceptions=fm(a7600), tau160000_on_exceptions=fm(a160),
        best_bound_on_exceptions=dict(sorted(collections.Counter(b[0] for b in best.values()).items())), best_scale_on_exceptions=dict(sorted(who.items())),
        bound_histogram_all_n=dict(sorted(allb.items())), max_bound=max(allb), n_bound_le16=sum(v for k, v in allb.items() if k <= 16), n_bound_17=allb.get(17, 0), n_bound_18=allb.get(18, 0))
if __name__ == "__main__":
    S = compute(); json.dump(S, open(os.path.join(res, "SUMMARY_v014.json"), "w"), indent=1); print(json.dumps(S, indent=1))
