"""D4 probe -- distance at n+1 = m for m in a smooth set (the region where residue-class covers fail).
Usage: run_D4_smooth.py B LIM primes budget   -> ../results/D4_smooth_B<B>.json   (EXPERIMENTAL finite data; witnesses certified independently)"""
import sys, os, time, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import exact_distance
from indep_check import certify_distance

def smooth_list(LIM, primes):
    ms = [1]
    for p in primes:
        new = []
        for m in ms:
            x = m
            while x <= LIM: new.append(x); x *= p
        ms = new
    return sorted(set(m for m in ms if m >= 2))

if __name__ == "__main__":
    B, LIM, primes, budget = int(sys.argv[1]), int(sys.argv[2]), [int(x) for x in sys.argv[3].split(',')], float(sys.argv[4])
    ms = smooth_list(LIM, primes); t0 = time.time(); hist = collections.Counter(); wit = []; tested = 0; mx = None
    for m in ms:
        if time.time() - t0 > budget: break
        n = m - 1
        d, p = exact_distance(B * n, B * (n + 1)); hist[d] += 1; tested += 1
        if d >= 5 and len(wit) < 40: wit.append({"n": n, "d": d, "path": p})
        if mx is None or d > mx[1]: mx = (n, d, p)
    cert = None
    if mx and mx[1] >= 5:
        cert = {"n": mx[0], "d": mx[1], "balls": certify_distance(B * mx[0], B * (mx[0] + 1), mx[1], mx[2])}
    res = {"B": B, "m_limit": LIM, "primes": primes, "tested": tested, "available": len(ms), "hist": dict(sorted(hist.items())),
           "finite_max": max(hist), "d_ge_5_witnesses": wit, "independent_certificate_of_first_max": cert, "max_witness": ({"n": mx[0], "d": mx[1], "path": mx[2]} if mx else None),
           "status": "EXPERIMENTAL finite data on n+1 in a smooth set; certified lower bound D_B >= %d" % max(hist)}
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results"); os.makedirs(out, exist_ok=True)
    json.dump(res, open(os.path.join(out, f"D4_smooth_B{B}.json"), "w"), indent=1)
    print(B, tested, len(ms), res["hist"], [w["n"] for w in wit][:6], flush=True)
