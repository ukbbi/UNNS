"""v014 (EXPERIMENTAL observation): exception rate of 'tau^4 > 6' versus rho(n) = q(n)/(1000 sqrt(n+1)) (parity-barrier tightness: (q+1)^2 vs 10^6 (n+1))."""
import sys, os, json, math, collections
sys.dont_write_bytecode = True
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from qn import qvec
from summarize14 import sweep
def compute():
    s = sweep(); q = qvec(len(s)); bins = collections.defaultdict(collections.Counter)
    for n in range(1, len(s) + 1): bins[min(int(q[n] / (1000 * math.sqrt(n + 1)) * 10), 9)][s[n - 1] == "9"] += 1
    return {("%.1f" % (b / 10)): dict(n=sum(c.values()), exceptions=c[True], rate_percent=round(100 * c[True] / sum(c.values()), 2)) for b, c in sorted(bins.items())}
if __name__ == "__main__":
    r = compute(); json.dump(r, open(os.path.join(here, "..", "results", "OBS_rho.json"), "w"), indent=1); print(json.dumps(r))
