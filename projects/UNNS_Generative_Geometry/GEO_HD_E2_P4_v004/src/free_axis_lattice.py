"""v003: P4-S2 decision on every lattice-level (pair, box) of the v002 spatial scan whose target has a free coordinate; compare with the 36 stored failures."""
import sys, os, json, time, math
from itertools import product
from collections import Counter
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import _boot  # noqa
fa = _boot.p4("free_axis"); lm = _boot.p4("lattice_model")
import exact_containment as ec
boxes = [q for q in product((1, 2), repeat=3)] + [(2, 2, 3), (2, 3, 2), (3, 2, 2)]
def orders(B):
    f = lm.member3(B); res = []
    for i in range(3):
        k = 1
        while not f(tuple(k if j == i else 0 for j in range(3))): k += 1
        res.append(k)
    return res
def work(a):
    B, Bp = a
    inS, inT = lm.member3(B), lm.member3(Bp)
    free = lm.free_coordinates3(inT); out = []
    for q in boxes:
        F, cs = lm.cells_of_member(inS, q)
        if not F: continue
        S = ec.geometric_maximal(cs, 3)
        r = fa.decide_free_axis(S, inT, q, free[0])
        out.append([list(q), r["verdict"], r.get("part")])
    return [B, Bp, out]
if __name__ == "__main__":
    t = time.time()
    lat = {n: lm.hnf3(n) for n in range(1, 13)}
    nr = [(n, B) for n in range(2, 7) for B in lat[n] if math.prod(orders(B)) != n and lm.free_coordinates3(lm.member3(B))]
    tasks = []
    for n2, Bp in nr:
        fp = lm.member3(Bp)
        for n in range(2 * n2, 13, n2):
            for B in lat[n]:
                if all(fp(r) for r in B): tasks.append((B, Bp))
    with Pool(2) as p: R = p.map(work, tasks, chunksize=4)
    runs = [(B, Bp, x) for B, Bp, o in R for x in o]
    fails = {(json.dumps(B), json.dumps(Bp), tuple(x[0])) for B, Bp, x in runs if x[1] == "NOT_CONTAINED"}
    old = json.load(open(os.path.join(ROOT, "..", "GEO_HD_E2_P4_v002/results/P4_LATTICE3.json")))["failures"]
    oldset = {(json.dumps(f["B"]), json.dumps(f["Bp"]), tuple(f["q"])) for f in old}
    parts = Counter(x[2] for B, Bp, x in runs if x[1] == "NOT_CONTAINED")
    res = {"n_targets_free_nonrect": len(nr), "n_pairs": len(tasks), "n_runs": len(runs), "n_fail_free_axis": len(fails), "n_fail_stored_v002": len(oldset),
           "same_set": fails == oldset, "extra_vs_stored": [list(x) for x in fails - oldset][:10], "missing_vs_stored": [list(x) for x in oldset - fails][:10], "parts": dict((str(k), v) for k, v in parts.items())}
    json.dump(res, open(os.path.join(ROOT, "results/P4_FREE_AXIS_LATTICE.json"), "w"), indent=1)
    print(res, time.time() - t)
