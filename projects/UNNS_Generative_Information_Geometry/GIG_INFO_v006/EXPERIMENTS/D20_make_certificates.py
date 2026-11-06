"""D20 -- write CERTIFICATES/positives_cycle_cocycle.json: for each of the 290 positives (content, minimal source L, cycle z, edge cocycle c) for the standalone verifier."""
import json, os
import _path, nerve
import A21_motifs as M
import A23_cone_criterion as C
from A20_load_positives import load_positives
if __name__ == "__main__":
    P, F, R = load_positives(); out = []
    for p in P:
        D = nerve.dead_sets(p["mask"]); B = nerve.Bounder(D); cyc = None
        for t in M.hollow_triangles(D):
            if not B.bounds(t): cyc = list(t); break
        if cyc is None: cyc = C.shortest_nonbounding(D)
        cert = nerve.cocycle_certificate(D, cyc)
        assert cert and nerve.check_cocycle(cert[0], D, cyc)
        L = p["L"] if p["src"] == "H6" else p["L"]
        out.append({"src": p["src"], "content": list(p["content"]), "source": int(L), "cycle": cyc, "cocycle_edges": [list(e) for e in cert[0]]})
    json.dump(out, open(os.path.join(_path.ROOT, "CERTIFICATES", "positives_cycle_cocycle.json"), "w"))
    print(len(out), sum(len(o["cocycle_edges"]) for o in out))
