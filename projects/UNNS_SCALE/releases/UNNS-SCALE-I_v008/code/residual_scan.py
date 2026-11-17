"""v008 E5: exact test of every n in a window left uncovered by constant-ratio shapes (v',w'<=K, rho>0 incl. rho<1)."""
import sys, os, json, time, numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from famE import coverage
from prime_scan import routes
B = 10**6
K, N, budget = map(int, sys.argv[1:4]); t0 = time.time()
h, S = coverage(B, K, N); un = (np.nonzero(~h[2:])[0] + 2).tolist()
print("K", K, "window", N, "shapes", len(S), "uncovered", len(un), round(time.time() - t0), flush=True)
res = {}; none = []
for n in un:
    if time.time() - t0 > budget: break
    R = routes(n); res[str(n)] = len(R)
    if not R: none.append(n)
print("exactly tested", len(res), "of", len(un), "; with NO (+-|+-) route:", none)
json.dump({"K": K, "window": N, "shapes": len(S), "uncovered": un, "routes": res, "none": none}, open(f'../results/R2_residual_K{K}_N{N}.json', 'w'))
