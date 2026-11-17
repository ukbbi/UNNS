"""Part B (exploratory): exact d(10^6 n, 10^6(n+1)) outside the window, on arithmetic families where B=10 has distance 6 or the K<=4 cover fails.
Time-budgeted; every distance exact in the full graph; any d>=5 would be stored with its path and certified.  Usage: partB_scan.py budget_seconds seed"""
import sys, os, json, time, random, collections
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import exact_distance
from indep_check import check_path
from sympy import primerange
budget = int(sys.argv[1]); rnd = random.Random(int(sys.argv[2])); B = 10**6; out = {}; t0 = time.time()
fam = []
for a in range(0, 6):
    for p in primerange(7, 140): fam.append(("720*2^a*p", 720 * 2**a * p - 1))
for _ in range(150):
    while True:
        m = 720
        for p in (2, 3, 5, 7):
            for _ in range(rnd.randint(0, 3)): m *= p
        if 10**6 <= m <= 10**10: break
    fam.append(("smooth 720|m", m - 1))
for _ in range(150): fam.append(("random 180|m", 180 * rnd.randint(5600, 5 * 10**6) - 1))
rnd.shuffle(fam); fam = fam[:]
for tag, n in fam:
    if time.time() - t0 > budget: break
    d, p = exact_distance(B * n, B * (n + 1), 6); assert check_path(p) == d and p[0] == B * n and p[-1] == B * (n + 1)
    out[str(n)] = {"family": tag, "d": d, "path": p if d >= 5 else None}
    if d >= 5: print("FOUND d>=5 at n =", n, d, flush=True)
h = collections.Counter((v["family"], v["d"]) for v in out.values())
json.dump({"B": B, "tested": len(out), "hist": {f"{a}|{d}": c for (a, d), c in sorted(h.items())}, "max_d": max(v["d"] for v in out.values()), "results": out, "seconds": round(time.time() - t0, 1)}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "B_outside_window_scan.json"), "w"))
print(sorted(h.items()), len(out), round(time.time() - t0))
