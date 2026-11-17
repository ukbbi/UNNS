"""Gate 1 -- exact representation.  n = B q + r."""
import json, math, random, sys, os
from scale_lib import to_coords, from_coords, to_mixed, from_mixed

random.seed(20261116)
res = {"gate": 1, "claims": {}}

# G1.a  exhaustive round trip and bijection on [0, B*M) for B in {10,100,1000}
exh = {}
for B, M in [(10, 100000), (100, 10000), (1000, 1000)]:
    seen = set()
    ok = True
    for n in range(B * M):
        q, r = to_coords(n, B)
        if not (0 <= q < M and 0 <= r < B) or from_coords(q, r, B) != n:
            ok = False; break
        seen.add((q, r))
    exh[str(B)] = {"range": [0, B * M], "bijection_onto_[0,M)x[0,B)": ok and len(seen) == B * M}
res["claims"]["G1a_exhaustive"] = exh

# G1.b  B = 10^6, boundaries + random over [0, 10^12]
B = 10 ** 6
bad = 0
pts = [0, 1, B - 1, B, B + 1, 10**12 - B, 10**12 - 1, 10**12, 845123456789]
pts += [random.randrange(0, 10**12 + 1) for _ in range(200000)]
for n in pts:
    q, r = to_coords(n, B)
    if from_coords(q, r, B) != n or not (0 <= r < B):
        bad += 1
res["claims"]["G1b_B1e6_points_tested"] = len(pts)
res["claims"]["G1b_B1e6_failures"] = bad
res["claims"]["G1b_worked_example"] = {"n": 845123456789, "(q,r)": list(to_coords(845123456789, B))}

# G1.c  range accounting for positive integers 1..10^12 (off-by-one record)
qs = {to_coords(n, B)[0] for n in [1, B - 1, B, 10**12 - 1, 10**12]}
res["claims"]["G1c_range_accounting"] = {
    "positions_0_to_1e12_minus_1": "outer q in [0, 1e6-1], 1e6 blocks of 1e6 positions each",
    "n=1e12": list(to_coords(10**12, B)),
    "note": "1..10^12 needs q = 10^6 for the single endpoint n = 10^12 (r = 0); 'one million outer blocks' is exact for [0,10^12) or for 0-based indexing.",
}

# G1.d  information accounting (bits)
res["claims"]["G1d_bits"] = {
    "log2(1e12)": math.log2(10**12),
    "bits(q)+bits(r) with ceil": 2 * math.ceil(math.log2(10**6)),
    "log2(1e6)": math.log2(10**6),
    "statement": "q and r together carry exactly log2(1e12) bits of information; the two-level coordinates are a change of geometry, not a reduction of information.",
}

# G1.e  mixed radix 10^12 = 10^4 x 10^4 x 10^4 and 10^6 x 10^6
mix_bad = 0
for radices in ([10**4] * 3, [10**6] * 2, [10**2] * 6, [10] * 12):
    for n in pts[:20000]:
        d = to_mixed(n, radices)
        if from_mixed(d, radices) != n:
            mix_bad += 1
        if not all(0 <= x < b for x, b in zip(d[:-1], radices)):
            mix_bad += 1
res["claims"]["G1e_mixed_radix_failures"] = mix_bad

res["PASS"] = (
    all(v["bijection_onto_[0,M)x[0,B)"] for v in exh.values()) and bad == 0 and mix_bad == 0
)
out = os.path.join(os.path.dirname(__file__), "..", "results", "gate1.json")
json.dump(res, open(out, "w"), indent=2)
print(json.dumps(res, indent=2)); sys.exit(0 if res["PASS"] else 1)
