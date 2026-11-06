"""E30 (S3-4, S3-5) -- arithmetic survival of the 12 lifted patterns (identity role map; the new rank 6 is the largest label) over ALL 7-label contents with labels in
[2, Lmax].  By AT-2 (dimension-free: the existence argument only uses monotonicity of A(m)) a hole regime for pattern (a,b) exists iff no filling family is contained in
A(K_P), K_P = lcm_{I in P} D(I).  Also records whether the 6-label sub-content (the six smallest labels) admits the H_2 hole of Stage 1 at all, and the ratio K_P(7)/K_P(6)."""
import itertools, json, math, os, sys, time
from math import gcd, lcm
import multiprocessing as mp
import _path

LM = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 20
L = json.load(open(os.path.join(_path.ROOT, "CERTIFICATES", "lift_pairs.json")))
PAIRS = [p for p in L["pairs"] if not p["diagonal"]]
import lift  # noqa
from pk import PK
P7 = PK(7)
for p in PAIRS:
    z = P7.bits(p["z3_faces"])
    p["Pset"] = [s for s in range(1, 128) if P7.pz(z) >> s & 1]
    p["fam_masks"] = [sum(1 << s for s in f) for f in p["families"]]
import hole_survival as H
H2P = sorted(H.PZ)
H2F = [sum(1 << s for s in f) for f in L["H2_families"]]


def denominators(labels):
    k = len(labels)
    D = [1] * (1 << k)
    num = [1] * (1 << k)
    den = [1] * (1 << k)
    for I in range(1, 1 << k):
        j = (I & -I).bit_length() - 1
        J = I & (I - 1)
        num[I] = num[J] * labels[j]
        den[I] = den[J] * (labels[j] + 1) ** 2
        D[I] = num[I] // gcd(num[I], den[I])
    return D


def exists(D, Pset, fam_masks):
    K = 1
    for s in Pset:
        K = lcm(K, D[s])
    A = 0
    for s in range(1, len(D)):
        if K % D[s] == 0:
            A |= 1 << s
    return all(f & ~A for f in fam_masks), K


def job(first):
    res = []
    for rest in itertools.combinations(range(first + 1, LM + 1), 6):
        C = (first,) + rest
        D = denominators(list(C))
        hits = []
        for i, p in enumerate(PAIRS):
            ok, K = exists(D, p["Pset"], p["fam_masks"])
            if ok:
                hits.append((i, K))
        if hits:
            D6 = D[:64]
            ok6, K6 = exists(D6, H2P, H2F)
            res.append((C, hits, ok6, K6))
    return res


if __name__ == "__main__":
    t0 = time.time()
    with mp.get_context("fork").Pool(2) as pool:
        parts = pool.map(job, range(2, LM - 5), chunksize=1)
    hits = [x for p in parts for x in p]
    total = sum(math.comb(LM - f, 6) for f in range(2, LM - 5))
    out = {"Lmax": LM, "contents": total, "pairs": [(p["a"], p["b"]) for p in PAIRS], "contents_with_hole_regime": len(hits),
           "by_pair": {"%d%d" % (p["a"], p["b"]): sum(1 for h in hits for i, _ in h[1] if i == k) for k, p in enumerate(PAIRS)},
           "records": [{"content": list(C), "patterns": [("%d%d" % (PAIRS[i]["a"], PAIRS[i]["b"]), str(K)) for i, K in hs], "sub6_has_H2_hole_regime": ok6, "K6_of_sub6": str(K6)} for C, hs, ok6, K6 in sorted(hits)],
           "seconds": round(time.time() - t0, 1)}
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E30_arithmetic_census_L%d.json" % LM), "w"), indent=1)
    print({k: v for k, v in out.items() if k != "records"})
    for r in out["records"][:30]:
        print(r["content"], r["patterns"], r["sub6_has_H2_hole_regime"])
