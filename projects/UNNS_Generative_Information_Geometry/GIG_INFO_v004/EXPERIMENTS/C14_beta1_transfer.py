"""C14 -- like-for-like transfer on the secondary target Y1=1[beta1>0]: observation hierarchy in the symbolic domain (SYM-6 stress sample, 508,680 distinct systems) and in the arithmetic census D (346,859 regimes)."""
import csv, gzip, json, os
import numpy as np
import _path
from A12_scope_hierarchy import classes
from A13_collision_concordance import stats

R4 = os.path.join(_path.ROOT, "RESULTS")
R3 = os.path.join(_path._vpath.PATHS["INFO003"], "RESULTS")
W = {"hd": 8, "hq": 16, "hb": 60}


def pad(d):
    for k, w in W.items():
        x = d[k]; d[k] = x[:, :w] if x.shape[1] >= w else np.pad(x, ((0, 0), (0, w - x.shape[1])))
    return d


if __name__ == "__main__":
    S = pad(dict(np.load(os.path.join(R4, "SYM6_stress_features.npz"))))
    S["Y"] = S["beta1"]
    A = pad(dict(np.load(os.path.join(R3, "features_all.npz"))))
    b1 = []
    with gzip.open(os.path.join(_path._vpath.PATHS["INFO002"], "RESULTS", "census_regimes.csv.gz"), "rt") as f:
        for r in csv.DictReader(f):
            b1.append(int(r["betti1"]))
    A["Y"] = np.array(b1)
    out = {}
    SIGS = {"N": ["N"], "(N,h1)": ["N", "hd"], "(N,h1,Q)": ["N", "hd", "sq"], "(Q,S2)": ["sq", "Ss2"], "(N,h1,Q,S2)": ["N", "hd", "sq", "Ss2"], "(N,h1,h2)": ["N", "hd", "hb"]}
    for tag, F in (("symbolic SYM-6 stress", S), ("arithmetic census D", A)):
        F2 = dict(F); F2["beta2"] = F["Y"]  # reuse the Y=beta2 helpers with Y replaced
        rec = {"systems": len(F["N"]), "positives_beta1": int((F["Y"] > 0).sum())}
        for nm, names in SIGS.items():
            inv, mixed, hid, nm_ = classes(F2, names)
            st = stats(F2, names, tag)
            rec[nm] = {"mixed_classes": nm_, "positives_hidden": hid, "partner_positive_rate": st["partner_positive_rate"], "positives_with_partner": st["positive_systems_with_a_partner"], "base_rate": st["base_rate"]}
        out[tag] = rec
        print(tag, rec["systems"], rec["positives_beta1"], {k: (v["mixed_classes"], v["positives_hidden"], None if v["partner_positive_rate"] is None else round(v["partner_positive_rate"], 3)) for k, v in rec.items() if isinstance(v, dict)}, flush=True)
    json.dump(out, open(os.path.join(R4, "C14_beta1_transfer.json"), "w"), indent=1)
