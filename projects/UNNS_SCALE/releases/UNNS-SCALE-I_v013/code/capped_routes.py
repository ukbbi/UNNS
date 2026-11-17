"""v013: explicit confined routes (independent Python search) for the seven pairs that were capped in v012, using the scale ladder
10^6 m -> 160000 m -> 7600 m -> 361 m -> 18 m -> 4 m -> m (six backward steps) and a short middle route at scale A in G_{10^6(n+1)}."""
import sys, os, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hubpath import route
from indep_check import check_path
LADDER = [10**6, 160000, 7600, 361, 18, 4, 1]
def confined_route(n, A, B=10**6, rmax=4, cap=3000000):
    W = B * (n + 1); i = LADDER.index(A)
    mid = route(A * n, A * (n + 1), W, rmax=rmax, cap=cap)
    if mid is None: return None
    down = [s * n for s in LADDER[: i + 1]]; up = [s * (n + 1) for s in LADDER[: i + 1]][::-1]
    return down[:-1] + mid + up[1:]
if __name__ == "__main__":
    iv = json.load(open(sys.argv[1])); out = {}
    for n, d in iv.items():
        n = int(n); best = None
        for A in (18, 4, 1):
            dist = d["distances"].get(str(A))
            if not isinstance(dist, int) or dist > 5: continue
            p = confined_route(n, A)
            if p and (best is None or len(p) < len(best)): best = p
        if best:
            assert max(best) <= 10**6 * (n + 1) and check_path(best) == len(best) - 1
            out[n] = {"length": len(best) - 1, "max_vertex": max(best), "path": best}; print(n, len(best) - 1, flush=True)
    json.dump(out, open(sys.argv[2], "w"))
