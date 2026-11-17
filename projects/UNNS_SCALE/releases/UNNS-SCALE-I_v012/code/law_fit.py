"""v012: least-squares fits of the confined shortest-route length tau_n(kappa) against ln q(n) (EXPERIMENTAL law) and summary statistics."""
import sys, os, json, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from frontier_io import read_frontier, read_ladder, qn
def fit(pts):
    X = np.array([[1.0, math.log(qn(n))] for n, _ in pts]); Y = np.array([t for _, t in pts], float)
    c = np.linalg.lstsq(X, Y, rcond=None)[0]; pred = X @ c
    return {"points": len(pts), "intercept": round(float(c[0]), 3), "slope_ln_q": round(float(c[1]), 3), "R2": round(float(1 - ((Y - pred) ** 2).sum() / ((Y - Y.mean()) ** 2).sum()), 3), "max_tau": int(Y.max()), "mean_tau": round(float(Y.mean()), 3)}
def compute(res):
    S = {}
    def tk(F): return [(n, p[0][-1][0]) for n, p in F.items() if p[1] == "*"]
    for name, f in (("B=100 (n=1..99)", "F100.txt"), ("B=1000 (n=1..999)", "F1000.txt"), ("B=10^4 (50 sampled n)", "F10000.txt")):
        S[name] = fit(tk(read_frontier(os.path.join(res, f))))
    F6 = {}
    for f in ("F1e6_n1_99.txt", "F1e6_n100_199.txt"):
        p = os.path.join(res, f)
        if os.path.exists(p): F6.update(read_frontier(p))
    L = read_ladder(os.path.join(res, "LAD_B6_a.txt"), os.path.join(res, "LAD_B6_b.txt"))
    pts6 = tk(F6) + [(n, v) for (n, W), v in L.items() if isinstance(v, int) and W == 10**6 * (n + 1)]
    S["B=10^6 (exact DP n<=199 + ladder n up to 10^6)"] = fit(sorted(set(pts6)))
    cens = [(n, v) for (n, W), v in L.items() if isinstance(v, tuple) and W == 10**6 * (n + 1)]
    S["B=10^6 censored kappa-distance lower bounds (ladder)"] = [{"n": n, "tau_gt": v[1]} for n, v in sorted(cens)]
    return S
if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); res = os.path.join(here, "..", "results"); S = compute(res)
    json.dump(S, open(os.path.join(res, "FIT_summary.json"), "w"), indent=1); print(json.dumps(S, indent=1))
