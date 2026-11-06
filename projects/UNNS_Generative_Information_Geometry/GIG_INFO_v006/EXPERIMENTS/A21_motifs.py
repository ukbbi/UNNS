"""A21 -- minimal non-bounding cycles of N[D_A] across the 290 positives (and 1000 negatives): is there a hollow (non-bounding) triangle; its S6 orbit type."""
import itertools, json, os, random, time
from collections import Counter
import numpy as np
import _path, v2, nerve
from A20_load_positives import load_positives

PERMS = list(itertools.permutations(range(6)))
ACT = []
for p in PERMS:
    t = [0] * 64
    for m in range(64):
        r = 0
        for i in range(6):
            if m >> i & 1: r |= 1 << p[i]
        t[m] = r
    ACT.append(t)

def canon(tup):
    return min(tuple(sorted(t[x] for x in tup)) for t in ACT)

def hollow_triangles(D):
    """3-cycles of N[D] (pairwise non-complementary) that are not faces."""
    D = sorted(D); out = []
    for a, b, c in itertools.combinations(D, 3):
        if any(x ^ y == 63 for x, y in ((a, b), (a, c), (b, c))): continue
        if not any(all(x in nerve.COMP[z] for x in (a, b, c)) for z in nerve.SUBS):
            out.append((a, b, c))
    return out

def analyse(m):
    D = nerve.dead_sets(m)
    B = nerve.Bounder(D)
    ht = hollow_triangles(D)
    nb = [t for t in ht if not B.bounds(t)]
    return D, ht, nb

if __name__ == "__main__":
    t0 = time.time()
    P, F, REGS = load_positives()
    rng = random.Random(20261121)
    neg = rng.sample([i for i in range(len(REGS)) if F["beta2"][i] == 0 and REGS[i][3] != (1 << 720) - 1], 1000)
    res = {}
    for tag, items in (("positives", [p["mask"] for p in P]), ("negatives", [REGS[i][3] for i in neg])):
        c = Counter(); types = Counter(); nbtypes = Counter(); sizes = []
        per = []
        for m in items:
            D, ht, nb = analyse(m)
            sizes.append(len(D))
            c["systems"] += 1; c["with_hollow_triangle"] += bool(ht); c["with_nonbounding_hollow_triangle"] += bool(nb)
            for t in set(canon(x) for x in ht): types[t] += 1
            for t in set(canon(x) for x in nb): nbtypes[t] += 1
            per.append((len(D), len(ht), len(nb)))
        res[tag] = {"counts": dict(c), "mean_D": float(np.mean(sizes)), "hollow_type_systems": {str(k): v for k, v in types.most_common()}, "nonbounding_type_systems": {str(k): v for k, v in nbtypes.most_common()}}
        print(tag, res[tag]["counts"], len(types), len(nbtypes), round(time.time() - t0), flush=True)
    json.dump(res, open(os.path.join(_path.ROOT, "RESULTS", "A21_motifs.json"), "w"), indent=1)
