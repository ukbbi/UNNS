"""v008 E1: minimal over all (+-|+-) routes of max(N,M,q,r) for each n, at B=10^6 (exact, complete enumeration)."""
import sys, os, json, math, random, time, collections
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from midpoint_lib import all_pairs
B = 10**6
def zmap(m):
    x = B * m; out = collections.defaultdict(list)
    for N, q in all_pairs(B, m):
        out[x // N * (N + 1) ** 2 // (q * q) * (q - 1)].append((N, q))
    return out
def minT(n):
    a = zmap(n); b = zmap(n + 1); best = None
    for z in a.keys() & b.keys():
        for (N, q) in a[z]:
            for (M, r) in b[z]:
                T = max(N, q, M, r)
                if best is None or T < best[0]: best = (T, N, q, M, r)
    return best
if __name__ == "__main__":
    budget = int(sys.argv[1]); rnd = random.Random(11); t0 = time.time()
    exc = sorted(int(k) for k in json.load(open('/home/claude/v005/UNNS-SCALE-I_v005/results/A_window_uncovered_614.json'))['results'])
    cand = [("random", rnd.randint(3, 10**6)) for _ in range(1500)] + [("exceptional", n) for n in rnd.sample(exc, 200)] + [("smallprime", p) for p in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53)]
    rnd.shuffle(cand); out = {}
    for tag, n in cand:
        if time.time() - t0 > budget: break
        r = minT(n); out[str(n)] = {"set": tag, "min": list(r) if r else None}
    json.dump(out, open('../results/G1_min_label.json', 'w'))
    rows = [(v["set"], math.log(v["min"][0]) / math.log(int(k)), v["min"][0], int(k)) for k, v in out.items() if v["min"] and int(k) > 100]
    print("tested", len(out), "no route:", [k for k, v in out.items() if v["min"] is None])
    for s in ("random", "exceptional"):
        e = sorted(x[1] for x in rows if x[0] == s)
        print(s, len(e), "exponent log Tmin/log n: min %.3f  q10 %.3f  median %.3f  q90 %.3f  max %.3f" % (e[0], e[len(e)//10], e[len(e)//2], e[9*len(e)//10], e[-1]))
    print("global min exponent", min(rows)[1:], " bound n^(1/6) exponent = 0.1667")
