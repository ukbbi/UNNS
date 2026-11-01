"""v004: structure of robustly flagged ('hard') planar cells, as predicted by the proof of P4-P1 (CP3-A):
   corners A=(0,y0), B=(x0,0) opposite; the other corners D,E have all coordinates >= (k',l'); all corners satisfy x/k'+y/l' >= 2."""
import sys, os, json, time
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import _boot  # noqa
lm = _boot.p4("lattice_model"); ze = _boot.p4("zv_explicit")
import exact_containment as ec
from itertools import product
NMAX, QM = int(sys.argv[1]), int(sys.argv[2])
tot = bad = 0; contained_checked = 0; failures = []
t = time.time()
lats = [(n, B) for n in range(1, NMAX + 1) for B in lm.hnf2(n)]
for n, B in lats:
    inL = lm.member2(B)
    for n2, Bp in lats:
        if not (n2 < n and n % n2 == 0 and all(lm.member2(Bp)(r) for r in B)):
            continue
        inT = lm.member2(Bp)
        kp = next(k for k in range(1, 10**4) if inT((k, 0))); lp = next(l for l in range(1, 10**4) if inT((0, l)))
        for q in product(range(2, QM + 1), repeat=2):
            F, cs = lm.cells_of_member(inL, q)
            if not F: continue
            for b, g in ec.geometric_maximal(cs, 2):
                if len(g) != 2 or not ze.robustly_flagged(b, g, inT): continue
                tot += 1
                V = ec.cell_vertices(b, g)
                ok = all(v[0] * 1 >= 0 for v in V)
                A = [v for v in V if v[0] == 0 and v[1] > 0]; Bc = [v for v in V if v[1] == 0 and v[0] > 0]
                good = bool(A) and bool(Bc)
                if good:
                    A, Bc = A[0], Bc[0]
                    others = [v for v in V if v not in (A, Bc)]
                    opposite = (len(others) == 2 and tuple(A[i] + Bc[i] for i in range(2)) == tuple(others[0][i] + others[1][i] for i in range(2)))
                    good = opposite and all(v[0] >= kp and v[1] >= lp for v in others) and all(Fr(v[0], kp) + Fr(v[1], lp) >= 2 for v in V)
                if not good:
                    bad += 1; failures.append((B, Bp, q, b, g))
print("robustly flagged planar cells:", tot, "structure violations:", bad, time.time() - t)
json.dump({"n_cells": tot, "violations": len(failures), "limits": {"NMAX": NMAX, "QM": QM}}, open(os.path.join(ROOT, "results/P4_HARD_CELLS_%d_%d.json" % (NMAX, QM)), "w"))
