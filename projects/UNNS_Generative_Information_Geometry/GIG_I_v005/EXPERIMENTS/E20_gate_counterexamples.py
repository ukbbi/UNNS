"""E20 -- gate-1 / gate-3 counterexamples: z survives although a gate is open. Builds the certificate files and re-verifies them with a
presence rule independent of filling.py (face F present iff m is divisible by lcm of D over Pref(F)); exact cochain phi with phi(d3)=0, phi(z)=1."""
import json, os, sys
from math import lcm
import _path
import hole_survival as H, block_factor as bf

CERT = os.path.join(_path.ROOT, "CERTIFICATES")


def verify(labels, m):
    D = bf.denominators(labels)
    present = [i for i, f in enumerate(H._FS) if m % lcm(*[D[I] for I in H._pref_sets(f)]) == 0]
    ps = set(present)
    if not all(g in ps for g in H.Z):
        return {"z_present": False}
    two = [i for i in present if H._DIM[i] == 2]
    idx = {g: k for k, g in enumerate(two)}
    rows = []
    for i in present:
        if H._DIM[i] == 3:
            r = 0
            for b in H._BND[i]:
                r |= 1 << idx[b]
            rows.append(r)
    zm = 0
    for g in H.Z:
        zm |= 1 << idx[g]
    basis = {}

    def add(v, rhs):
        while v:
            h = v.bit_length() - 1
            if h in basis:
                bv, br = basis[h]
                v ^= bv
                rhs ^= br
            else:
                basis[h] = (v, rhs)
                return True
        return rhs == 0
    consistent = all(add(r, 0) for r in rows) and add(zm, 1)
    if not consistent:
        return {"z_present": True, "z_bounds": True}
    sol = 0
    for h in sorted(basis):
        bv, br = basis[h]
        if (bin(bv & sol & ~(1 << h)).count("1") & 1) ^ br:
            sol |= 1 << h
    ok = all(bin(r & sol).count("1") % 2 == 0 for r in rows) and bin(zm & sol).count("1") % 2 == 1
    supp = [H._FS[two[k]] for k in range(len(two)) if sol >> k & 1]
    return {"z_present": True, "z_bounds": False, "phi_verified": ok, "phi_support_faces": [[list(b) for b in f] for f in supp],
            "obstructed_octahedra_present": [i for i in range(len(H.OBS)) if m % lcm(*[D[I] for I in H.PT[i]]) == 0],
            "faces_present": len(present), "three_faces_present": len(rows)}


def run():
    res = {}
    for a in (1, 3):
        d = json.load(open(os.path.join(CERT, "gate%d_counterexample.json" % a)))
        v = verify(d["labels"], d["m"])
        res[a] = {"labels": d["labels"], "m": str(d["m"]), **{k: v[k] for k in v if k != "phi_support_faces"}}
        d["verification"] = v
        json.dump(d, open(os.path.join(CERT, "gate%d_counterexample.json" % a), "w"), indent=1)
    return res


if __name__ == "__main__":
    r = run()
    json.dump(r, open(os.path.join(_path.ROOT, "RESULTS", "E20_gate_counterexamples.json"), "w"), indent=1)
    print(json.dumps(r, indent=1))
