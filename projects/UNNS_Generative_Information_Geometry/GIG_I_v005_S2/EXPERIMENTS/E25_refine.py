"""E25 -- refinement of the atlas with the held-out false negatives of E24 (round 2), then a FRESH held-out test (different seed, none of the E24 contents).
Rounds are reported separately: atlas_v1 (E22 census cycles), atlas_v2 (v1 + cycles of the E24 false negatives)."""
import json, os, time
import _path
import atlas as A
import E22_extract as E22
import E23_families as E23
import E24_atlas_coverage as E24


def add_cycles(classes, fn_regimes):
    keys = {c["key"] for c in classes}
    new = []
    for C, L in fn_regimes:
        for x in E22.regime_record(tuple(C), L, None if False else E22.cb.Complex(E22.tc.source_mask(tuple(C), L), 6).betti()[2]):
            zb = x["canon_cycle"]
            P = A.pz(zb)
            fams, st = A.minimal_families(zb)
            a = {"cycle": zb, "P": P, "fams": fams, "stats": st, "weight": zb.bit_count()}
            imgs = E23.images(a)
            k = min(imgs)
            if k in keys:
                continue
            keys.add(k)
            new.append({"key": k, "cycles": [zb], "weights": [a["weight"]], "imgs": imgs, "P": P, "fams": fams, "q": st["q"], "source": [C, L]})
    return classes + new, new


if __name__ == "__main__":
    t0 = time.time()
    regimes, classes = E24.law_classes()
    prev = json.load(open(os.path.join(_path.ROOT, "RESULTS", "E24_atlas_coverage.json")))["heldout"]
    fn = sorted({(tuple(c), x[0]) for c, x in prev["false_negative"]})
    classes2, new = add_cycles(classes, fn)
    # does v2 cover the E24 false negatives it was built from (resubstitution) -- sanity only
    Afs = [E23.adm_family(tuple(c), L) for c, L in fn]
    resub = sum(1 for a in Afs if E24.predict(classes2, a))
    out = {"v1_classes": len(classes), "fn_regimes_used": len(fn), "new_classes_added": len(new), "v2_classes": len(classes2), "resubstitution_covered": [resub, len(fn)],
           "new_class_summary": [{"weights": c["weights"], "P_size": c["P"].bit_count(), "family_sizes": sorted(f.bit_count() for f in c["fams"]), "q": c["q"], "source": c["source"]} for c in new]}
    for tag, cl in (("v1", classes), ("v2", classes2)):
        r = E24.heldout(cl, 300, 300, seed=25)
        out["fresh_heldout_" + tag] = {k: v for k, v in r.items() if k not in ("false_positive", "false_negative")}
        out["fresh_heldout_" + tag]["n_false_positive"] = len(r["false_positive"])
        out["fresh_heldout_" + tag]["n_false_negative"] = len(r["false_negative"])
        out["fresh_heldout_" + tag]["false_negative"] = r["false_negative"]
    out["seconds"] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E25_refine.json"), "w"), indent=1)
    json.dump([{"cycle_bits": str(c["cycles"][0]), "P": str(c["P"]), "families": [str(f) for f in c["fams"]], "source": c.get("source")} for c in classes2], open(os.path.join(_path.ROOT, "CERTIFICATES", "atlas_v2_classes.json"), "w"))
    print(json.dumps({k: v for k, v in out.items() if k != "new_class_summary"}, indent=0)[:1500])
    print(out["new_class_summary"])
