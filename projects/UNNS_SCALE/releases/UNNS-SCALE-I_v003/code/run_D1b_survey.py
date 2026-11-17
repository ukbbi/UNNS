"""D1b -- wide survey: exact d(Bn,B(n+1)) for every B <= Bmax and n <= N; stores the full per-n distance lists
(used for the pointwise divisibility-monotonicity check d_A(n) >= d_B(n) for A | B).  Usage: run_D1b_survey.py Bmax N"""
import sys, os, json, time
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import exact_distance

def row(args):
    B, N = args
    return B, [exact_distance(B * n, B * (n + 1))[0] for n in range(1, N + 1)]

if __name__ == "__main__":
    Bmax, N = int(sys.argv[1]), int(sys.argv[2]); t0 = time.time()
    with Pool(2) as p: rows = p.map(row, [(B, N) for B in range(1, Bmax + 1)], chunksize=1)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results"); os.makedirs(out, exist_ok=True)
    data = {"Bmax": Bmax, "N": N, "d": {str(B): ds for B, ds in rows}, "seconds": round(time.time() - t0, 1),
            "status": "EXACT finite data (untruncated distances); maxima are certified lower bounds on D_B, not suprema"}
    json.dump(data, open(os.path.join(out, f"D1b_survey_B{Bmax}_N{N}.json"), "w"))
    print("done", round(time.time() - t0, 1))
