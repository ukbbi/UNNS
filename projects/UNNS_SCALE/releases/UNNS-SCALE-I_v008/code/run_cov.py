"""v008 C1: coverage table including rho<1 shapes (window n<=2e6) and the list of Delta<0 shapes' effect."""
import sys, os, json, time, numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from famE import coverage
B = 10**6; N = 2_000_000; rows = []
for K in (1, 2, 3, 4, 6, 8, 12, 20, 40):
    h, S = coverage(B, K, N); h0, S0 = coverage(B, K, N, False); n720 = np.arange(719, N + 1, 720)
    neg = sum(1 for s in S if s[3] * s[0] > s[2] * s[1])
    rows.append({"K": K, "shapes_pos": len(S0), "unc_pos": int((~h0[2:]).sum()), "shapes_all": len(S), "shapes_neg": neg, "unc_all": int((~h[2:]).sum()), "cov720": float(h[n720].mean()),
                 "uncovered_list": (np.nonzero(~h[2:])[0] + 2).tolist() if int((~h[2:]).sum()) < 50 else None})
    print(rows[-1]["K"], rows[-1]["unc_pos"], rows[-1]["unc_all"], flush=True)
json.dump({"window": N, "rows": rows}, open('../results/C1_coverage_with_rho_lt1.json', 'w'))
