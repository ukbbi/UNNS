#!/usr/bin/env python3
"""SCR-III held-out seed registry v001 (target-blind; derives labels and fingerprints only; no instance is built, no energy computed).
label = "<master>|<family>|<idx>" (same convention as seeds_v009); rng = random.Random(label); seed_sha256 = SHA-256(label)."""
import csv, hashlib, json, sys, pathlib
MASTER = 20261010
rows = []
for fam in ("S", "P"):
    for n in (24, 28, 32, 36, 40):
        for idx in range(20):
            f = "FEAS_%s_n%d" % (fam, n)
            lab = "%d|%s|%d" % (MASTER, f, idx)
            rows.append(dict(study="GAP_4X4_FEASIBILITY", family=f, n=n, idx=idx, label=lab, seed_sha256=hashlib.sha256(lab.encode()).hexdigest()))
T_GRID = (300, 500, 600, 650, 700, 725, 750, 775, 790, 792, 810)
for L in (2, 3):
    for T in T_GRID:
        for M in ("M0", "M1", "M2"):
            f = "DISC_SIM_L%d_T%d_%s" % (L, T, M)
            lab = "%d|%s|0" % (MASTER, f)
            rows.append(dict(study="T_DISCRIMINATION", family=f, n=2 * L * (L + 1), idx=0, label=lab, seed_sha256=hashlib.sha256(lab.encode()).hexdigest()))
out = pathlib.Path(sys.argv[1])
with open(out / "SCR_III_SEED_REGISTRY_v001.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
assert len({r["label"] for r in rows}) == len(rows) == 200 + 66
print(len(rows), hashlib.sha256(json.dumps([r["seed_sha256"] for r in rows]).encode()).hexdigest())
