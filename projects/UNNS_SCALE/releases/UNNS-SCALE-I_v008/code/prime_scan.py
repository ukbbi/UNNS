"""v008 E3: prime n (hardest absorption case).  For prime n=l (l not dividing B) every route must absorb l in N, M+1 or r-1 (Absorption Lemma).
Exact full route enumeration at B=10^6; records which absorption cases occur and the minimal label."""
import sys, os, json, random, time, collections
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from midpoint_lib import all_pairs
from exact_lib import _is_prime as is_prime
B = 10**6
def routes(n):
    a = collections.defaultdict(list); b = collections.defaultdict(list)
    x = B * n; y = B * (n + 1)
    for N, q in all_pairs(B, n): a[x // N * (N + 1) ** 2 // (q * q) * (q - 1)].append((N, q))
    for M, r in all_pairs(B, n + 1): b[y // M * (M + 1) ** 2 // (r * r) * (r - 1)].append((M, r))
    return [(N, q, M, r) for z in a.keys() & b.keys() for (N, q) in a[z] for (M, r) in b[z]]
if __name__ == "__main__":
    budget = int(sys.argv[1]); rnd = random.Random(21); t0 = time.time(); out = {}
    ps = []
    while len(ps) < 400:
        p = rnd.randint(1000, 10**6)
        if is_prime(p): ps.append(p)
    while len(ps) < 560:
        p = rnd.randint(10**9, 10**10)
        if is_prime(p): ps.append(p)
    for p in ps:
        if time.time() - t0 > budget: break
        R = routes(p); cases = collections.Counter()
        for N, q, M, r in R:
            c = tuple(name for name, val in (("N", N), ("M+1", M + 1), ("r-1", r - 1)) if val % p == 0)
            assert c, (p, N, q, M, r)
            for name in c: cases[name] += 1
        T = min((max(N, q, M, r) for N, q, M, r in R), default=None)
        out[str(p)] = {"routes": len(R), "cases": dict(cases), "Tmin": T}
    json.dump(out, open('../results/P1_prime_scan.json', 'w'))
    no = [k for k, v in out.items() if v["routes"] == 0]
    print("primes tested", len(out), "with no (+-|+-) route:", no)
    agg = collections.Counter()
    for v in out.values():
        for c in v["cases"]: agg[c] += 1
    print("number of primes having at least one route in absorption case:", dict(agg))
    ratio = sorted(v["Tmin"] / int(k) for k, v in out.items() if v["Tmin"])
    print("Tmin/p: min %.3f median %.3f max %.3f   (Lemma: Tmin >= p-1)" % (ratio[0], ratio[len(ratio) // 2], ratio[-1]))
    print("lemma violations:", [k for k, v in out.items() if v["Tmin"] and v["Tmin"] < int(k) - 1])
