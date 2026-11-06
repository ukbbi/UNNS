"""B11 -- out-of-sample information: train on the census D, test on the held-out H6 (and the reverse).  Balanced test ensemble (1/2 positives, 1/2 negatives).
Recovered information = 1 - balanced cross-entropy (bits).  Models: histogram gradient boosting on exact integer features (fixed seeds) and an exact-signature lookup with back-off."""
import json, os
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import _path
from B10_information_profiles import load

FS = {"N": ["N"], "radius1 scalars": ["N", "E", "Sd2", "Sd3", "dmax", "dmin"], "radius1 + squares": ["N", "E", "Sd2", "Sd3", "dmax", "dmin", "sq", "hx"],
      "radius2 scalars": ["N", "E", "Sd2", "Sd3", "dmax", "dmin", "sq", "hx", "Sq2", "Ss2", "Sds", "Sdq", "Ssq", "SB2", "SB22", "bmax", "bmin"], "(Q,S2) only": ["sq", "Ss2"]}
EPS = 1e-6


def bal_loss(y, p):
    p = np.clip(p, EPS, 1 - EPS)
    lp = -np.log2(p[y == 1]).mean()
    ln = -np.log2(1 - p[y == 0]).mean()
    ce = 0.5 * lp + 0.5 * ln
    return ce, 0.5 * ((p[y == 1] > 0.5).mean() + (p[y == 0] <= 0.5).mean())


def lookup(tr, te, levels):
    Ytr = (tr["beta2"] > 0).astype(int); P, M = Ytr.sum(), (1 - Ytr).sum()
    tabs = []
    for names in levels:
        trk = [tuple(r) for r in np.concatenate([tr[k].reshape(len(Ytr), -1) for k in names], axis=1).tolist()]
        tek = [tuple(r) for r in np.concatenate([te[k].reshape(len(te["N"]), -1) for k in names], axis=1).tolist()]
        t = {}
        for k, y in zip(trk, Ytr):
            c = t.setdefault(k, [0, 0]); c[y] += 1
        tabs.append((t, tek))
    p = np.zeros(len(te["N"])); level = np.zeros(len(te["N"]), dtype=int)
    for i in range(len(p)):
        for li, (t, tek) in enumerate(tabs):
            c = t.get(tek[i])
            if c is not None:
                odds = ((c[1] + 0.5) / P) / ((c[0] + 0.5) / M)
                p[i] = odds / (1 + odds); level[i] = li; break
        else:
            p[i] = 0.5; level[i] = len(tabs)
    return p, level


if __name__ == "__main__":
    D, H6 = load("features_all.npz"), load("H6_features.npz")
    out = {}
    for tag, tr, te in (("train D -> test H6", D, H6), ("train H6 -> test D", H6, D)):
        ytr, yte = (tr["beta2"] > 0).astype(int), (te["beta2"] > 0).astype(int)
        rec = {"train_positives": int(ytr.sum()), "test_positives": int(yte.sum()), "test_systems": len(yte), "gradient_boosting": {}}
        for fs, names in FS.items():
            Xtr = np.stack([tr[k] for k in names], 1).astype(float); Xte = np.stack([te[k] for k in names], 1).astype(float)
            m = HistGradientBoostingClassifier(max_depth=4, max_iter=200, learning_rate=0.1, class_weight="balanced", random_state=0).fit(Xtr, ytr)
            p = m.predict_proba(Xte)[:, 1]
            ce, ba = bal_loss(yte, p)
            rec["gradient_boosting"][fs] = {"balanced_cross_entropy_bits": round(float(ce), 4), "information_recovered_bits": round(float(1 - ce), 4), "balanced_accuracy": round(float(ba), 4), "AUC": round(float(roc_auc_score(yte, p)), 4)}
            print(tag, fs, rec["gradient_boosting"][fs], flush=True)
        levels = [["N", "hd", "sq", "Ss2"], ["N", "hd", "sq"], ["N", "hd"], ["N"]]
        p, lev = lookup(tr, te, levels)
        ce, ba = bal_loss(yte, p)
        rec["exact_signature_lookup_with_backoff"] = {"balanced_cross_entropy_bits": round(float(ce), 4), "information_recovered_bits": round(float(1 - ce), 4), "balanced_accuracy": round(float(ba), 4),
                                                       "fraction_of_test_positives_whose_finest_signature_was_seen_in_training": round(float((lev[yte == 1] == 0).mean()), 4), "fraction_of_test_negatives_with_finest_signature_seen": round(float((lev[yte == 0] == 0).mean()), 4)}
        print(tag, "lookup", rec["exact_signature_lookup_with_backoff"], flush=True)
        out[tag] = rec
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "B11_out_of_sample.json"), "w"), indent=1)
