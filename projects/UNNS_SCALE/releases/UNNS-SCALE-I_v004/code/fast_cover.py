"""Class cover with the fast engine.  Families n+1 = C*s.  Usage: fast_cover.py B C M0 r0 K4 maxM budget tag"""
import sys, json, time
from fractions import Fraction
sys.path.insert(0, '.')
from fast_sym import pivot_route
from poly_check import verify_identity
from cover2 import vp
PR = (2, 3, 5, 7)
def run(B, C, M0, r0, K4, maxM, budget, tag, verbose=True):
    t0 = time.time(); front = [(M0, r0)]; done = []; unres = []; tried = 0
    while front and time.time() - t0 < budget:
        M, r = front.pop(0); tried += 1
        res = pivot_route(B, C, M, r, K4)
        ok = False
        if res is not None:
            Mn, rn, steps = res
            ok, info = verify_identity(B, Mn, rn, [(d, list(l)) for d, l in steps])
            if ok: done.append({"M": Mn, "r": rn, "s_class": [M, r], "C": C, "t0": info, "steps": [(d, list(l)) for d, l in steps]})
        if not ok:
            p = sorted(PR, key=lambda q: (vp(M, q), q))[0]
            if M * p <= maxM: front += [(M * p, r + M * i) for i in range(p)]
            else: unres.append((M, r))
        if verbose and tried % 50 == 0: print(f"tried {tried} done {len(done)} front {len(front)} unres {len(unres)} t={time.time()-t0:.0f}s", flush=True)
    dens_done = sum(Fraction(1, d["s_class"][0]) for d in done)
    dens_un = sum(Fraction(1, M) for M, r in unres) + sum(Fraction(1, M) for M, r in front)
    out = {"B": B, "C": C, "K4": K4, "maxM": maxM, "done": done, "unresolved": unres, "pending": front,
           "density_s_closed": str(dens_done), "density_s_open": str(dens_un)}
    json.dump(out, open(f"/tmp/fc_{tag}.json", "w"))
    print(f"B={B} C={C}: closed identities {len(done)}, s-density closed {float(dens_done):.6f}, open {float(dens_un):.6f} (unres {len(unres)}, pending {len(front)}) t={time.time()-t0:.0f}s")
    return out
if __name__ == "__main__":
    B, C, M0, r0, K4, maxM, budget = map(int, sys.argv[1:8]); run(B, C, M0, r0, K4, maxM, budget, sys.argv[8])
