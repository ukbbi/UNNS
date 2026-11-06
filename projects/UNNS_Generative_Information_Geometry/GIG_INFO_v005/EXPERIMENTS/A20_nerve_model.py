"""A20 -- test of the nerve model  H~_{0,1}(Y_A) = H~_{0,1}(N[D_A])  on all 290 positives and 1000 sampled negatives from the arithmetic regimes, plus the prefix-definedness of arithmetic admissibility."""
import json, os, random, time
import numpy as np
import _path, v2, nerve
from A20_load_positives import load_positives

if __name__ == "__main__":
    t0 = time.time()
    P, F, REGS = load_positives()
    rng = random.Random(20261120)
    neg = rng.sample([i for i in range(len(REGS)) if F["beta2"][i] == 0 and REGS[i][3] != (1 << 720) - 1], 1000)
    items = [("positive_" + p["src"], p["mask"]) for p in P] + [("negative_D", REGS[i][3]) for i in neg]
    out = {"tested": 0, "prefix_defined": 0, "model_agrees_b0_b1": 0, "disagree_examples": [], "by_kind": {}}
    for kind, m in items:
        yb = nerve.y_betti(m, 1); nb = nerve.nerve_betti(nerve.dead_sets(m), 1) if nerve.dead_sets(m) else None
        pd = nerve.is_prefix_defined(m)
        ok = (nb == yb)
        out["tested"] += 1; out["prefix_defined"] += int(pd); out["model_agrees_b0_b1"] += int(ok)
        d = out["by_kind"].setdefault(kind, {"n": 0, "prefix_defined": 0, "agree": 0, "b1_pos": 0}); d["n"] += 1; d["prefix_defined"] += int(pd); d["agree"] += int(ok); d["b1_pos"] += int(yb[1] > 0)
        if not ok and len(out["disagree_examples"]) < 5:
            out["disagree_examples"].append({"kind": kind, "Y": yb, "N": nb, "prefix_defined": pd})
    out["seconds"] = round(time.time() - t0)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "A20_nerve_model.json"), "w"), indent=1)
    print(out)
