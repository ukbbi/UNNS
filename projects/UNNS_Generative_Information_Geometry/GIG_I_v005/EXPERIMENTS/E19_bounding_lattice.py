"""E19 -- exact bounding lattice of the common 2-cycle z over all 2^20 families of extra prefix sets (finite-exact, GF(2))."""
import json, os, time
import _path
import filling as F
N = len(F.EXTRA)
b = bytearray(1 << N)
mins = []
t = time.time()
for S in range(1 << N):
    x, hit = S, False
    while x:
        l = x & -x
        if b[S ^ l]:
            hit = True
            break
        x ^= l
    if hit:
        b[S] = 1
    elif F.bounds(S):
        b[S] = 1
        mins.append(S)
out = {"extra_prefix_sets": F.EXTRA, "families_total": 1 << N, "families_bounding": sum(b),
       "minimal_bounding_families": [[F.EXTRA[i] for i in range(N) if S >> i & 1] for S in mins],
       "seconds": round(time.time() - t, 1)}
with open(os.path.join(_path.ROOT, "RESULTS", "E19_bounding_lattice.json"), "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "extra_prefix_sets"}, indent=1))
