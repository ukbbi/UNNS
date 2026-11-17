"""v011: explicit in-domain routes (all vertices <= B(n+1)) for sampled window pairs whose endpoints are hub-direct: B n -> 999 n ~~> 1 ~~> 999(n+1) -> B(n+1)."""
import sys, os, json, random, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hubpath import route
from indep_check import check_path
B = 10**6
def hub_route(m):
    p = route(999 * m, 1, 10**9, rmax=80, cap=3000000)
    return p
def pair_route(n):
    a = hub_route(n); b = hub_route(n + 1)
    if a is None or b is None: return None
    return [B * n] + a + b[::-1][1:] + [B * (n + 1)]
if __name__ == "__main__":
    res = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
    listed = set(int(l.split()[0]) for l in open(os.path.join(res, "CN1_vertex_links.txt")))
    rnd = random.Random(11); out = {}; t0 = time.time()
    while len(out) < int(sys.argv[1]):
        n = rnd.randint(1000, 999998)
        if n in listed or (n + 1) in listed or str(n) in out: continue
        p = pair_route(n)
        if p is None: continue
        assert check_path(p) and max(p) <= B * (n + 1), n
        out[str(n)] = p
    json.dump(out, open(os.path.join(res, "E1_explicit_routes.json"), "w"))
    print({n: (len(p) - 1, max(p) // 10**6) for n, p in out.items()}, round(time.time() - t0), "s")
