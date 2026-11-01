import sys, json, os, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import _boot  # noqa
fa = _boot.p4("free_axis"); lm = _boot.p4("lattice_model"); sl = _boot.p4("slab_law")
import exact_containment as ec
V2 = os.path.join(os.path.dirname(ROOT), "GEO_HD_E2_P4_v002")
d = json.load(open(os.path.join(V2, "results/P4_FIELDI3.json")))
out, cmp_ = [], Counter()
t = time.time()
for r in d["rows"]:
    P, b, b2, q = r["primes"], r["b"], r["b_next"], r["box"]
    inT = sl.mem_chi(P, b2)
    free = lm.free_coordinates3(inT)
    if not free:
        continue
    if r["verdict"] == "PROVED_BY_P4Z1" and "--all" not in sys.argv:
        continue
    inS = sl.mem_chi(P, b)
    F, cs = lm.cells_of_member(inS, tuple(q)); S = ec.geometric_maximal(cs, 3)
    res = fa.decide_free_axis(S, inT, q, free[0])
    cmp_[(r["verdict"], res["verdict"], res.get("part"))] += 1
    out.append({"primes": P, "b": b, "b_next": b2, "box": q, "stored": r["verdict"], "free_axis": res["verdict"], "part": res.get("part"), "witness": res.get("witness"), "cell": res.get("cell"), "nodes": res["nodes"]})
json.dump({"comparison": {"%s|%s|%s" % k: v for k, v in cmp_.items()}, "rows": out}, open(os.path.join(ROOT, "results/P4_FREE_AXIS_ROWS.json"), "w"), indent=1)
print(dict(cmp_), time.time() - t)
