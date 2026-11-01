"""P4-H0 finite test: for planar lattices L and boxes Q, is conv(L cap Q) (origin INCLUDED) contained in U0(L,Q) (Graver cells, origin allowed)?"""
import sys, os, json, time
from itertools import product
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import _boot  # noqa
fa = _boot.p4("free_axis"); lm = _boot.p4("lattice_model")
import exact_containment as ec
NMAX, QM = int(sys.argv[1]), int(sys.argv[2])
t = time.time(); runs = bad = 0; fails = []
for n in range(1, NMAX + 1):
    for B in lm.hnf2(n):
        inL = lm.member2(B)
        for q in product(range(1, QM + 1), repeat=2):
            pts = [v for v in product(range(q[0] + 1), range(q[1] + 1)) if inL(v)]
            if len(pts) < 3:
                continue
            try:
                hs = ec.hull_halfspaces(pts, 2)
            except Exception:
                continue
            if not hs:
                continue
            T = [ec.Target(c[0], c[1], 2) for c in fa.planar_cells0(inL, q, True)]
            w, nn = fa.decide_poly(hs, T, 2, 20000)
            runs += 1
            if w is not None:
                bad += 1; fails.append({"B": B, "q": q, "w": [str(x) for x in w]})
print(runs, bad, fails[:5], time.time() - t)
json.dump({"runs": runs, "failures": fails, "limits": {"NMAX": NMAX, "QM": QM}}, open(os.path.join(ROOT, "results/P4_H0_TEST_%d_%d.json" % (NMAX, QM)), "w"))
