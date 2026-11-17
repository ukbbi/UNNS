import sys, json
sys.dont_write_bytecode = True
from classes import all_classes
from cover import cover
B = 10**6; res = {}
for K, bud in ((4, 40), (8, 100), (12, 100)):
    C = [c for c in all_classes(B, K) if c[2] <= 10**6]
    o = cover([(r, m) for r, m, n0, sh in C], bud)
    res[K] = {"classes": len(C), "max_n0": max(c[2] for c in C), "finished": o["finished"], "dead": len(o["dead"]), "nodes": o["nodes"], "frontier": o["frontier"], "uncovered_upper_bound": float(o["uncovered_upper_bound"]), "seconds": round(o["seconds"])}
    print(K, res[K], flush=True)
json.dump(res, open("../results/C2_covering_search.json", "w"), indent=1)
