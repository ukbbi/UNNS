"""A15 -- do the stronger signatures (N,Q,S2), (N,h1,Q,S2) also fail on prefix families?  Selects the smallest-N mixed class of the strongest failing signature."""
import json, os
import numpy as np
import _path
from A12_scope_hierarchy import classes

if __name__ == "__main__":
    R = os.path.join(_path.ROOT, "RESULTS")
    out = {}
    for tag in ("PF", "VS"):
        d = dict(np.load(os.path.join(R, "A12_%s_features.npz" % tag)))
        out[tag] = {}
        for nm, names in {"(N,Q,S2)": ["N", "sq", "Ss2"], "(N,h1,Q,S2)": ["N", "hd", "sq", "Ss2"], "(N,h1,Q,S2,Sds)": ["N", "hd", "sq", "Ss2", "Sds"], "(N,h1,h2)": ["N", "hd", "hb"], "(N,h1,hq,h2)": ["N", "hd", "hq", "hb"]}.items():
            inv, mixed, hid, nm_ = classes(d, names)
            rec = {"mixed_classes": nm_, "positives_hidden": hid, "systems": len(d["N"]), "positives": int((d["beta2"] > 0).sum())}
            if nm_:
                best = min(((int(d["N"][np.nonzero(inv == c)[0][0]]), int(c)) for c in np.nonzero(mixed)[0]))
                ix = np.nonzero(inv == best[1])[0]
                pi = [int(i) for i in ix if d["beta2"][i] > 0][0]; ni = [int(i) for i in ix if d["beta2"][i] == 0][0]
                rec["smallest"] = {"N": best[0], "mask_pos": str(d["masks_hex"][pi]), "mask_neg": str(d["masks_hex"][ni]), "beta2_pos": int(d["beta2"][pi]), "beta2_neg": int(d["beta2"][ni])}
            out[tag][nm] = rec
            print(tag, nm, {k: v for k, v in rec.items() if k != "smallest"}, rec.get("smallest", {}).get("N"), flush=True)
    json.dump(out, open(os.path.join(R, "A15_stronger_signatures.json"), "w"), indent=1)
