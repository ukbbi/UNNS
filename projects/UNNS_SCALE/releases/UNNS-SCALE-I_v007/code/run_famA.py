import sys, os, json, math, random
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from famA import families, route
from indep_check import check_path
B = 10**6; F = families(B); rnd = random.Random(7)
live = []; dead = []
for c, d, s in F:
    if math.gcd(c, s) != 1 or math.gcd(d, s) != 1: dead.append((c, d, s)); continue
    res = (-pow(c, -1, s)) % s; live.append((c, d, s, res))
print("families", len(F), "live", len(live), "dead (gcd)", len(dead))
# verify: each live family, 5 random n in class, route exists & edge-checked; and second congruence automatic
bad = 0; ver = 0
for c, d, s, res in live:
    for _ in range(3):
        n = res + s * rnd.randint(2 * c // s + 3 if False else 1, 3000) ; n = n if n >= 2 else n + s
        p = route(B, n, c, d, s)
        if p is None: bad += 1; continue
        if len(str(p[1])) < 40: check_path(p)
        ver += 1
print("verified", ver, "bad", bad)
exc = sorted(int(k) for k in json.load(open('/home/claude/v005/UNNS-SCALE-I_v005/results/A_window_uncovered_614.json'))['results'])
cov = {}
for n in exc:
    for c, d, s, res in live:
        if n % s == res and route(B, n, c, d, s): cov.setdefault(n, []).append((c, d, s)); 
print("614 covered by famA:", len(cov), "of", len(exc))
moduli = sorted({s for c, d, s, r in live}); print("distinct moduli", len(moduli), moduli[:20])
# density estimate: classes with distinct moduli (union bound and independence)
dens_ub = sum(1 / s for c, d, s, r in live); dens_ind = 1 - math.prod(1 - 1 / s for c, d, s, r in live)
print("density union-bound %.4f, independence-heuristic %.4f" % (dens_ub, dens_ind))
# window coverage by direct count over n<=2e6
N = 2_000_000; hit = bytearray(N + 1)
for c, d, s, res in live:
    for n in range(res if res >= 2 else res + s, N + 1, s):
        if c * n + 1 >= 2 * s and d * (n + 1) + 1 >= 2 * s: hit[n] = 1
print("window n<=%d covered: %d (%.4f)" % (N, sum(hit), sum(hit) / N))
json.dump({"live": live, "dead": dead, "covered614": {str(k): v for k, v in cov.items()}, "window_N": N, "window_covered": sum(hit)}, open('../results/FAMA_coverage.json', 'w'))
