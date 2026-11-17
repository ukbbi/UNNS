"""Turn a raw cover (from cover2.py) into a verified D2 result:
 - converts step labels to integer coefficient lists
 - independent sympy-free polynomial verification of every identity (poly_check)
 - exact finite check of the t<t0 members of every class (untruncated exact engine)
 - exact density of covered / exceptional classes (Fractions)
 - finite statistics of the exceptional classes (first members, exact distances)
Usage: finalize_cover.py B K   (reads /tmp/cover_B_K.json or ../results/D2raw_B*_K*.json)"""
import sys, json, os
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from poly_check import verify_identity
from exact_lib import exact_distance

t = sp.symbols('t')
def coeffs(expr):
    return [int(c) for c in sp.Poly(sp.sympify(expr), t).all_coeffs()]

def finalize(B, K, rawfile, outdir):
    raw = json.load(open(rawfile)); ids = []; dens = Fraction(0); fin_checked = 0
    for c in raw["done"]:
        steps = [(d, coeffs(N)) for d, N in c["steps"]]
        ok, info = verify_identity(B, c["M"], c["r"], steps)
        assert ok, (B, c, info)
        t0 = info
        for tt in range(0, t0):                       # members below the validity threshold: exact check
            n = c["M"] * tt + c["r"]
            if n >= 1:
                d, _ = exact_distance(B * n, B * (n + 1)); assert d <= K, (B, n, d); fin_checked += 1
        ids.append({"M": c["M"], "r": c["r"], "length": len(steps), "t0": t0, "steps": steps})
        dens += Fraction(1, c["M"])
    exc = [tuple(x) for x in raw["unresolved"]] + [tuple(x) for x in raw.get("pending", [])]
    edens = sum(Fraction(1, M) for M, r in exc)
    assert dens + edens == 1, (dens, edens)
    exc_stats = []
    for M, r in sorted(exc):
        ds = []
        for k in range(0, 5):
            n = M * k + r
            if n >= 1:
                d, _ = exact_distance(B * n, B * (n + 1)); ds.append((n, d))
        exc_stats.append({"M": M, "r": r, "first_members_exact_d": ds})
    out = {"B": B, "K": K, "status_covered": f"PROVED: d(Bn,B(n+1)) <= {K} for every n in the {len(ids)} classes below (identities verified independently; t<t0 members checked exactly)",
           "density_covered": str(dens), "density_covered_float": float(dens), "density_exceptional": str(edens),
           "density_exceptional_float": float(edens), "n_identities": len(ids), "max_modulus": max([c["M"] for c in ids] + [1]),
           "finite_members_checked_exactly": fin_checked, "identities": ids,
           "exceptional_classes_OPEN_for_this_K": exc_stats}
    os.makedirs(outdir, exist_ok=True)
    json.dump(out, open(os.path.join(outdir, f"D2_B{B}_K{K}.json"), "w"), indent=1)
    return out

if __name__ == "__main__":
    B, K = int(sys.argv[1]), int(sys.argv[2])
    raw = sys.argv[3] if len(sys.argv) > 3 else f"/tmp/cover_{B}_{K}.json"
    r = finalize(B, K, raw, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results"))
    print(B, K, r["n_identities"], r["density_covered_float"], r["density_exceptional_float"], r["finite_members_checked_exactly"])
