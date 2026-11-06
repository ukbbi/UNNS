"""C10 -- Experiment C: exact sweep of all 512 binary transition-rule sets for the six events with categories S,S,S,R,R,N (primary), and the extension to all 28 category multisets of size 6."""
import json, os, time
import numpy as np
import _path, sym, geomk
import history_complex as hc

CATS = tuple("SSSRRN")


def analyse(cats):
    sysd = sym.all_systems(cats)
    masks = list(sysd)
    F = geomk.Geom(6).features(masks) if masks else {}
    rows = []
    for i, m in enumerate(masks):
        b = hc.betti(m, 6)
        fv = hc.f_vector(m, 6)
        rows.append({"codes": sysd[m], "mask": m, "N": int(F["N"][i]), "betti": list(b), "f": list(fv), "Q": int(F["sq"][i]), "S2": int(F["Ss2"][i]), "Sds": int(F["Sds"][i]), "SB22": int(F["SB22"][i]), "Sd2": int(F["Sd2"][i]), "E": int(F["E"][i]),
                     "h1": [int(x) for x in F["hd"][i]], "h2": [int(x) for x in F["hb"][i][:40]], "hq": [int(x) for x in F["hq"][i]]})
    return rows


if __name__ == "__main__":
    t0 = time.time()
    out = {}
    prim = analyse(CATS)
    out["primary"] = {"cats": list(CATS), "rule_sets": 512, "nonempty_rule_sets": sum(len(r["codes"]) for r in prim), "distinct_systems": len(prim),
                      "betti_signatures": {str(k): v for k, v in __import__("collections").Counter(tuple(r["betti"]) for r in prim).items()}}
    out["primary"]["rows"] = prim
    print("primary", {k: v for k, v in out["primary"].items() if k != "rows"}, round(time.time() - t0), flush=True)
    ext = {}
    for cats in sym.multisets():
        rows = analyse(cats)
        ext["".join(cats)] = rows
    out["extension"] = ext
    tot = sum(len(v) for v in ext.values())
    print("extension systems", tot, round(time.time() - t0), flush=True)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "C10_symbolic_sweep.json"), "w"))
