"""D1 -- exact untruncated distances d(Bn, B(n+1)) for n <= N.  Usage: run_D1_exact.py N B1 B2 ... (writes ../results/D1_B<B>_N<N>.json)
Every distance is exact (meet-in-the-middle with complete neighbourhoods, no graph truncation).
Finite maxima are CERTIFIED LOWER BOUNDS on D_B (never claimed as suprema)."""
import sys, json, time, collections, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import exact_distance
from indep_check import certify_distance

def run(B, N):
    t0 = time.time(); hist = collections.Counter(); first = {}; big = []; tot = 0
    for n in range(1, N + 1):
        d, p = exact_distance(B * n, B * (n + 1))
        hist[d] += 1; tot += d
        if d not in first: first[d] = (n, p)
        if d >= 5 and len(big) < 8: big.append((n, d, p))
    mx = max(hist)
    # independent certificate (sympy-based, disjoint balls) for the first witness of every distance value >= max-1
    certs = {}
    for dd in sorted(first):
        if dd >= max(3, mx - 1):
            n, p = first[dd]
            certs[dd] = {"n": n, "path": p, "ball_radii_sizes": certify_distance(B * n, B * (n + 1), dd, p)}
    return {"B": B, "N": N, "hist": dict(sorted(hist.items())), "mean": tot / N, "finite_max": mx,
            "status": "CERTIFIED lower bound D_B >= %d (finite maximum over n<=%d)" % (mx, N),
            "first_witness": {str(k): {"n": v[0], "path": v[1]} for k, v in first.items()},
            "d_ge_5_examples": [{"n": a, "d": b, "path": c} for a, b, c in big],
            "independent_certificates": {str(k): v for k, v in certs.items()}, "seconds": round(time.time() - t0, 1)}

if __name__ == "__main__":
    N = int(sys.argv[1]); out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
    os.makedirs(out, exist_ok=True)
    for B in map(int, sys.argv[2:]):
        r = run(B, N); json.dump(r, open(os.path.join(out, f"D1_B{B}_N{N}.json"), "w"), indent=1)
        print(B, r["hist"], round(r["mean"], 4), r["finite_max"], r["seconds"], flush=True)
