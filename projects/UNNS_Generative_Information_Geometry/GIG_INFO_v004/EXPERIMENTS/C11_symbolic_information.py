"""C11 -- information recovery on the symbolic domain: Y2=1[beta2>0] (primary), Y1=1[beta1>0] (secondary), natural and balanced ensembles, observation hierarchy."""
import json, os
from collections import Counter
import _path, ent2

OBS = {"O0=N": lambda r: (r["N"],), "(N,h1)": lambda r: (r["N"], tuple(r["h1"])), "(N,h1,h2)": lambda r: (r["N"], tuple(r["h1"]), tuple(r["h2"])), "(Q,S2)": lambda r: (r["Q"], r["S2"]), "(N,h1,Q,S2)": lambda r: (r["N"], tuple(r["h1"]), r["Q"], r["S2"]),
       "f-vector": lambda r: tuple(r["f"]), "(N,SB22)": lambda r: (r["N"], r["SB22"])}


def prof(rows, ytag):
    Y = [1 if (r["betti"][2] if ytag == "Y2" else r["betti"][1]) > 0 else 0 for r in rows]
    res = {"systems": len(rows), "positives": sum(Y)}
    for mode in ("natural", "balanced"):
        if sum(Y) in (0, len(Y)):
            res[mode] = "undefined (one class only)"
            continue
        res[mode] = {k: ent2.profile(Y, [f(r) for r in rows], mode, 20) for k, f in OBS.items()}
    return res


if __name__ == "__main__":
    S = json.load(open(os.path.join(_path.ROOT, "RESULTS", "C10_symbolic_sweep.json")))
    prim = S["primary"]["rows"]
    ext_all = [dict(r, cats=c) for c, rows in S["extension"].items() for r in rows]
    # dedupe across multisets is NOT done: different category multisets are different systems even if masks coincide
    out = {"primary_Y2": prof(prim, "Y2"), "primary_Y1": prof(prim, "Y1"), "extension_Y2": prof(ext_all, "Y2"), "extension_Y1": prof(ext_all, "Y1"),
           "extension_betti2_positive": [{"cats": r["cats"], "N": r["N"], "betti": r["betti"], "codes": r["codes"][:3]} for r in ext_all if r["betti"][2] > 0][:20],
           "extension_betti_histogram_b1_b2": {str(k): v for k, v in Counter((min(r["betti"][1], 5), min(r["betti"][2], 5)) for r in ext_all).items()}}
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "C11_symbolic_information.json"), "w"), indent=1)
    for k in ("primary_Y2", "primary_Y1", "extension_Y2", "extension_Y1"):
        v = out[k]
        print(k, v["systems"], v["positives"])
        for mode in ("natural", "balanced"):
            if isinstance(v[mode], dict):
                print("  ", mode, {o: (p["H(Y|O)"][:7], p["I(Y;O)"][:7], p["mixed_classes"]) for o, p in v[mode].items()})
    print(out["extension_betti_histogram_b1_b2"], out["extension_betti2_positive"][:5])
