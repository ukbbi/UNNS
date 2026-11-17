"""v008 E4: adversarial n = k L_S, L_S = lcm(v' P) over all constant-ratio shapes (v',w'<=12, P<=S) at B=10^6.
By Theorem A'' such n lie in no class of those shapes.  Do they still have a (+-|+-) route (exact full enumeration)?"""
import sys, os, json, math, time, collections
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from famD import shapes
from prime_scan import routes
from midpoint_lib import coords
B = 10**6
def L_of(S, K=12):
    L = 1
    for vp, wp, c, d, P, Q in shapes(B, K):
        if P <= S: L = L * (vp * P) // math.gcd(L, vp * P)
    return L
if __name__ == "__main__":
    budget = int(sys.argv[1]); t0 = time.time(); out = {}
    for S in (5, 10, 20, 30):
        L = L_of(S)
        for k in (1, 2, 3, 4, 5, 6, 7):
            if time.time() - t0 > budget: break
            n = L * k
            t1 = time.time(); R = routes(n)
            best = min(R, key=lambda t: (max(t), t)) if R else None
            info = None
            if best:
                N, q, M, r = best; d, v, vp, P, Q = coords(B, n, N, q); e, w, wp, P2, Q2 = coords(B, n + 1, M, r)
                info = {"N": N, "q": q, "M": M, "r": r, "v'": vp, "w'": wp, "rho": [P, Q], "rho'": [P2, Q2]}
            out[f"{S}:{k}"] = {"S": S, "n": n, "routes": len(R), "best": info, "sec": round(time.time() - t1, 1)}
            print(S, k, n, "routes", len(R), info and (info["rho"], info["rho'"], info["v'"], info["w'"]), round(time.time() - t1), flush=True)
    json.dump(out, open('../results/A1_adversarial.json', 'w'))
