import fibparam as fp, sys, json
from math import isqrt
res = {}
for P in (24, 72, 120):
    found = {}
    for r in range(P):
        for K in (6, 7):
            out = fp.search(P, r, K, J=3)
            if out[0] is not None: found[r] = (out[0], out[1], out[2]); break
    res[P] = found
    print(P, len(found), "of", P, sorted(found)[:40], flush=True)
json.dump({str(P): {str(r): v for r, v in f.items()} for P, f in res.items()}, open("/tmp/fibcover.json", "w"))
