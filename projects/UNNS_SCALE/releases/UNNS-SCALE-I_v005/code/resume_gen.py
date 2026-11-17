"""Resume a general class cover from stored pending fronts.  Usage: resume_gen.py B K budget tag Kfall file1 [file2 ...]"""
import sys, json, time
sys.path.insert(0, '.')
from fractions import Fraction
from fast_sym import general_route
from poly_check import verify_identity
from cover2 import vp
PR = (2, 3, 5, 7)
B, K, budget, tag, Kf = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5])
front = []; done = []
for f in sys.argv[6:]:
    d = json.load(open(f)); front += [tuple(x) for x in d["pending"]] + [tuple(x) for x in d["unresolved"]]; done += d["done"]
front.sort(key=lambda x: x[0]); t0 = time.time(); tried = 0; unres = []
while front and time.time() - t0 < budget:
    M, r = front.pop(0); tried += 1
    st = general_route(B, M, r, K); ok = False
    if st is None and Kf and M >= 1260: st = general_route(B, M, r, Kf, 700_000)
    if st is not None:
        ok, info = verify_identity(B, M, r, st)
        if ok: done.append({"M": M, "r": r, "length": len(st), "t0": info, "steps": st})
    if not ok:
        p = sorted(PR, key=lambda q: (vp(M, q), q))[0]; front += [(M * p, r + M * i) for i in range(p)]
    if tried % 25 == 0: json.dump({"B": B, "K": K, "done": done, "unresolved": unres, "pending": front}, open(f"/tmp/fcg_{tag}.json", "w"))
json.dump({"B": B, "K": K, "done": done, "unresolved": unres, "pending": front}, open(f"/tmp/fcg_{tag}.json", "w"))
print(f"resume {tag}: tried {tried} identities {len(done)} pending {len(front)} t={time.time()-t0:.0f}s")
