"""General class cover (no pivot restriction) with the fast engine.  Usage: fast_cover_gen.py B K maxM budget tag [M0 r0]"""
import sys, json, time
from fractions import Fraction
sys.path.insert(0, '.')
from fast_sym import general_route
from poly_check import verify_identity
from cover2 import vp
PR = (2, 3, 5, 7)
def run(B, K, maxM, budget, tag, M0=1, r0=0, verbose=True, Kfall=None):
    t0 = time.time(); front = [(M0, r0)]; done = []; unres = []; tried = 0
    while front and time.time() - t0 < budget:
        M, r = front.pop(0); tried += 1
        st = general_route(B, M, r, K); ok = False
        if st is None and Kfall and M >= 1260: st = general_route(B, M, r, Kfall, 700_000)
        if st is not None:
            ok, info = verify_identity(B, M, r, st)
            if ok: done.append({"M": M, "r": r, "length": len(st), "t0": info, "steps": st})
        if not ok:
            p = sorted(PR, key=lambda q: (vp(M, q), q))[0]
            if M * p <= maxM: front += [(M * p, r + M * i) for i in range(p)]
            else: unres.append((M, r))
        if tried % 25 == 0:
            json.dump({"B": B, "K": K, "done": done, "unresolved": unres, "pending": front}, open(f"/tmp/fcg_{tag}.json", "w"))
        if verbose and tried % 25 == 0: print(f"tried {tried} done {len(done)} front {len(front)} unres {len(unres)} t={time.time()-t0:.0f}s", flush=True)
    dd = sum(Fraction(1, d["M"]) for d in done); du = sum(Fraction(1, M) for M, r in unres + front)
    json.dump({"B": B, "K": K, "done": done, "unresolved": unres, "pending": front}, open(f"/tmp/fcg_{tag}.json", "w"))
    print(f"B={B} K={K}: identities {len(done)}, density closed {float(dd):.8f}, open {float(du):.8f} (unres {len(unres)} pending {len(front)}) t={time.time()-t0:.0f}s")
if __name__ == "__main__":
    B, K, maxM, budget = map(int, sys.argv[1:5]); tag = sys.argv[5]
    M0 = int(sys.argv[6]) if len(sys.argv) > 6 else 1; r0 = int(sys.argv[7]) if len(sys.argv) > 7 else 0
    Kf = int(sys.argv[8]) if len(sys.argv) > 8 else None
    run(B, K, maxM, budget, tag, M0, r0, Kfall=Kf)
