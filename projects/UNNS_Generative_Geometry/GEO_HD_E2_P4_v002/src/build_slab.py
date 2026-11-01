"""v002: slab-criterion records for every recorded 3D failure + negative sample on the UNAVAILABLE_COST rows + free-coordinate cross-tab."""
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import _boot  # noqa: E402

sl = _boot.p4("slab_law")
lm = _boot.p4("lattice_model")

L3 = json.load(open(os.path.join(ROOT, "results/P4_LATTICE3.json")))
F3 = json.load(open(os.path.join(ROOT, "results/P4_FIELDI3.json")))

lat = []
for f in L3["failures"]:
    r = sl.slab_record(f["Bp"], f["q"], f["witness"])
    lat.append({"Bp": f["Bp"], "B": f["B"], "q": f["q"], "witness": f["witness"], "decomposable": r["decomposable"], "free": r["free"],
                "slab_witness": bool(r["slab"] and r["slab"]["slab_witness"]), "slab": r["slab"]})
fi = []
for n in F3["noncontained"]:
    r = sl.slab_record_chi(n["primes"], n["b_next"], n["box"], n["witness"])
    fi.append({"primes": n["primes"], "b": n["b"], "b_next": n["b_next"], "box": n["box"], "witness": n["witness"], "free": r["free"],
               "slab_witness": bool(r["slab"] and r["slab"]["slab_witness"]), "slab": r["slab"], "essential_3d": n.get("essential_3d")})
un = []
for r in F3["rows"]:
    if r["verdict"] == "UNAVAILABLE_COST":
        w = sl.slab_sample_witness(r["primes"], r["b"], r["b_next"], r["box"])
        un.append({"primes": r["primes"], "b": r["b"], "b_next": r["b_next"], "box": r["box"], "slab_sample_witness": w})
# free-coordinate cross-tab over ALL nonrectangular-target FIELD-I rows
tab = Counter()
for r in F3["rows"]:
    free = any((p % r["b_next"]) == 1 % r["b_next"] for p in r["primes"])
    tab[("free_coordinate" if free else "no_free_coordinate", r["verdict"])] += 1
planar = Counter((tuple(x["slab"]["planar_box"]), x["slab"]["planar_target_F"]) for x in fi + lat if x["slab"])
out = {"statement": "SLAB: for target Lambda' = Lambda'_2 (+) Z e_i and 0<c<1, (x',c) in U(Lambda',Q) iff x' in U(Lambda'_2,Q')",
       "lattice_level": {"n": len(lat), "n_slab_witness": sum(x["slab_witness"] for x in lat), "n_decomposable": sum(x["decomposable"] for x in lat),
                         "n_free_coordinate": sum(bool(x["free"]) for x in lat), "records": lat},
       "fieldI": {"n": len(fi), "n_slab_witness": sum(x["slab_witness"] for x in fi), "n_free_coordinate": sum(bool(x["free"]) for x in fi), "records": fi},
       "unavailable_cost_rows": {"n": len(un), "n_with_slab_sample_witness": sum(bool(x["slab_sample_witness"]) for x in un), "records": un,
                                 "status": "UNAVAILABLE_COST retained: exact 3D decision not completed at box (3,3,3); the slab sample finds no witness (not a proof of containment)"},
       "free_coordinate_crosstab_fieldI_nonrect_target": {"%s|%s" % k: v for k, v in sorted(tab.items())},
       "planar_gap_profile_of_failures": {"%s|F=%d" % (k[0], k[1]): v for k, v in planar.items()}}
json.dump(out, open(os.path.join(ROOT, "results/P4_SLAB.json"), "w"), indent=1)
print(out["lattice_level"]["n_slab_witness"], out["fieldI"]["n_slab_witness"], out["unavailable_cost_rows"], out["free_coordinate_crosstab_fieldI_nonrect_target"], out["planar_gap_profile_of_failures"])
