"""E27 -- final accounting for the 158 census regimes against atlas_v2: covering classes per regime, PS-1 overlap, greedy minimal class cover, class-level descriptors."""
import json, os
from collections import Counter
import _path
import atlas as A
import hole_survival as H
import E23_families as E23
import E24_atlas_coverage as E24
import E25_refine as E25

regimes, classes = E24.law_classes()
prev = json.load(open(os.path.join(_path.ROOT, "RESULTS", "E24_atlas_coverage.json")))["heldout"]
fn = sorted({(tuple(c), x[0]) for c, x in prev["false_negative"]})
classes, _ = E25.add_cycles(classes, fn)
zb = 0
for g in H.Z:
    zb |= 1 << g
ps1_key = min(E23.images({"P": A.pz(zb), "fams": A.minimal_families(zb)[0]}))
ps1_idx = [i for i, c in enumerate(classes) if c["key"] == ps1_key]
Afs = [E23.adm_family(tuple(r["content"]), r["L"]) for r in regimes]
cov = [E24.predict(classes, a) for a in Afs]
left, cover = set(range(len(regimes))), []
while left:
    i = max(range(len(classes)), key=lambda i: sum(1 for j in left if i in cov[j]))
    cover.append(i)
    left -= {j for j in left if i in cov[j]}
unexpl = [j for j, r in enumerate(regimes) if not r["ps1_explained"]]
out = {"v2_classes": len(classes), "regimes": len(regimes), "covered": sum(1 for c in cov if c),
       "ps1_class_indices": ps1_idx, "ps1_class_covers": sum(1 for c in cov if set(c) & set(ps1_idx)),
       "regimes_106_unexplained": len(unexpl), "of_which_covered": sum(1 for j in unexpl if cov[j]),
       "of_which_not_covered_by_ps1_class": sum(1 for j in unexpl if not set(cov[j]) & set(ps1_idx)),
       "greedy_cover_classes": len(cover), "greedy_cover_sizes": [sum(1 for c in cov if i in c) for i in cover],
       "classes": [{"index": i, "cycles_in_class": len(c["cycles"]), "weights": c["weights"], "P_size": c["P"].bit_count(), "q": c["q"], "n_min_families": len(c["fams"]),
                    "family_sizes": sorted(f.bit_count() for f in c["fams"]), "singleton_gates": [[s for s in range(64) if f >> s & 1][0] for f in c["fams"] if f.bit_count() == 1],
                    "regimes_covered": sum(1 for x in cov if i in x)} for i, c in enumerate(classes)],
       "assignment": [{"content": r["content"], "L": r["L"], "beta2": r["beta2"], "ps1_explained": r["ps1_explained"], "classes": cov[j]} for j, r in enumerate(regimes)]}
json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E27_assignment.json"), "w"), indent=1)
print({k: v for k, v in out.items() if k not in ("classes", "assignment")})
print(Counter(len(c["singleton_gates"]) for c in out["classes"]), Counter(c["n_min_families"] for c in out["classes"]))
