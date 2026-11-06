"""A26 -- for every one of the 290 positives: an explicit non-bounding 1-cycle z of N[D_A] and an edge cocycle c with c(boundary of every triangle)=0 and c(z)=1 (checked by independent code).
By T-NERVE + T-AD this certifies beta_2(K_A)>0 from forbidden-history data alone."""
import json, os
from collections import Counter
import _path, nerve
import A21_motifs as M
import A23_cone_criterion as C
from A20_load_positives import load_positives

if __name__ == "__main__":
    P, F, R = load_positives()
    cnt = Counter(); lens = Counter(); rows = []
    for p in P:
        D = nerve.dead_sets(p["mask"]); B = nerve.Bounder(D)
        cyc = None
        for t in M.hollow_triangles(D):
            if not B.bounds(t): cyc = list(t); break
        if cyc is None: cyc = C.shortest_nonbounding(D)
        cert = nerve.cocycle_certificate(D, cyc)
        ok = cert is not None and nerve.check_cocycle(cert[0], D, cyc)
        cnt["systems"] += 1; cnt["certified"] += bool(ok); lens[len(cyc)] += 1
        rows.append({"src": p["src"], "idx": p["idx"], "cycle_len": len(cyc), "cocycle_edges": len(cert[0]) if cert else None, "verified": bool(ok)})
    res = {"counts": dict(cnt), "cycle_length_distribution": dict(lens), "rows": rows}
    json.dump(res, open(os.path.join(_path.ROOT, "RESULTS", "A26_cocycle_certificates.json"), "w"), indent=1); print(res["counts"], res["cycle_length_distribution"])
