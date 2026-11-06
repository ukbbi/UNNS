"""E24 -- law classes (canonical (P_z, minimal families) under S_6), coverage accounting of the 158 census regimes, and held-out prediction.
Held-out set: contents NOT among the labels<=16 census (>=1 label > 16): (i) census hole contents with 1-2 labels replaced by labels in 17..40,
(ii) uniformly random contents with labels <= 40.  For every regime of every such content the exact beta_2 is computed (full homology) and compared with the atlas."""
import json, os, random, sys, time
from collections import Counter
import _path
import atlas as A
import E22_extract as E22
import E23_families as E23
import cell_boundary as cb
import source_filtration as sf
import threshold_closure as tc


def law_classes():
    regimes, atlas, _ = E23.build()
    keys = {}
    for i, a in enumerate(atlas):
        keys.setdefault(min(E23.images(a)), []).append(i)
    classes = []
    for k, idxs in sorted(keys.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        classes.append({"key": k, "cycles": [atlas[i]["cycle"] for i in idxs], "weights": sorted({atlas[i]["weight"] for i in idxs}), "imgs": E23.images(atlas[idxs[0]]),
                        "P": atlas[idxs[0]]["P"], "fams": atlas[idxs[0]]["fams"], "q": atlas[idxs[0]]["stats"]["q"]})
    return regimes, classes


def predict(classes, Afam):
    return [c for c, cl in enumerate(classes) if E23.covers(cl["imgs"], Afam)]


def census_accounting(regimes, classes):
    Afs = [E23.adm_family(tuple(r["content"]), r["L"]) for r in regimes]
    cov = [predict(classes, a) for a in Afs]
    return {"regimes": len(regimes), "covered": sum(1 for c in cov if c), "uncovered": sum(1 for c in cov if not c),
            "covered_by_exactly_one_class": sum(1 for c in cov if len(c) == 1), "covered_by_several": sum(1 for c in cov if len(c) > 1),
            "ps1_explained_regimes": sum(r["ps1_explained"] for r in regimes), "ps1_explained_and_covered": sum(1 for r, c in zip(regimes, cov) if r["ps1_explained"] and c),
            "regimes_per_class": dict(Counter(i for c in cov for i in c)), "unique_regimes_per_class": dict(Counter(c[0] for c in cov if len(c) == 1)),
            "overlap_size_hist": dict(Counter(len(c) for c in cov))}


def _job(C):
    out = {"content": list(C), "regimes": 0, "tp": 0, "fp": [], "fn": []}
    for r in sf.regimes(C):
        out["regimes"] += 1
        cx = cb.Complex(r["mask"], 6)
        b2 = cx.betti()[2]
        Af = E23.adm_family(C, r["L"])
        pred = bool(predict(_CLASSES, Af))
        if b2 and pred:
            out["tp"] += 1
        elif pred and not b2:
            out["fp"].append([r["L"], b2])
        elif b2 and not pred:
            out["fn"].append([r["L"], b2])
    return out


_CLASSES = None


def heldout(classes, n_mut=300, n_rand=300, seed=24, procs=2):
    global _CLASSES
    _CLASSES = classes
    rnd = random.Random(seed)
    base = sorted({tuple(r["content"]) for r in E22.json.load(open(os.path.join(_path.ROOT, "RESULTS", "E22_extract.json")))["records"]})
    conts = set()
    while len(conts) < n_mut:
        C = list(rnd.choice(base))
        for _ in range(rnd.choice((1, 2))):
            C[rnd.randrange(6)] = rnd.randint(17, 40)
        if len(set(C)) == 6:
            conts.add(tuple(sorted(C)))
    while len(conts) < n_mut + n_rand:
        C = tuple(sorted(rnd.sample(range(1, 41), 6)))
        if max(C) > 16:
            conts.add(C)
    import multiprocessing as mp
    with mp.get_context("fork").Pool(procs) as pool:
        res = pool.map(_job, sorted(conts), chunksize=4)
    return {"contents": len(res), "regimes": sum(r["regimes"] for r in res), "beta2_positive_predicted": sum(r["tp"] for r in res),
            "false_positive": [(r["content"], x) for r in res for x in r["fp"]], "false_negative": [(r["content"], x) for r in res for x in r["fn"]]}


if __name__ == "__main__":
    t0 = time.time()
    regimes, classes = law_classes()
    out = {"law_classes": len(classes), "class_summary": [{"cycles": len(c["cycles"]), "weights": c["weights"], "P_size": c["P"].bit_count(), "family_sizes": sorted(f.bit_count() for f in c["fams"]), "q": c["q"]} for c in classes],
           "census": census_accounting(regimes, classes)}
    print(out["census"])
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    out["heldout"] = heldout(classes, n, n)
    out["heldout"]["n_false_positive"] = len(out["heldout"]["false_positive"])
    out["heldout"]["n_false_negative"] = len(out["heldout"]["false_negative"])
    out["seconds"] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E24_atlas_coverage.json"), "w"), indent=1)
    print({k: v for k, v in out["heldout"].items() if k not in ("false_positive", "false_negative")})
    print("FN sample", out["heldout"]["false_negative"][:6])
