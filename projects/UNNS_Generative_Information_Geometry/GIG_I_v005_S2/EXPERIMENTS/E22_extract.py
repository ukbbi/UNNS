"""E22 -- exact homology representatives for all 158 beta_2>0 regimes of the v004 census (labels<=16): a basis of H_2 (one cycle per basis class), reduced to
low weight, canonicalised under S_6, with cochain certificates; then group the canonical cycles.  Classes are relative to the chosen representatives."""
import json, os, random, time
from collections import Counter, defaultdict
import _path
import atlas as A
import cell_boundary as cb
import threshold_closure as tc
import _vpath

R = json.load(open(os.path.join(_vpath.V004, "RESULTS", "results.json")))["E15"]["completeness_census"]["beta2_regimes"]


def reduce_many(cx, z, tries=12, seed=1):
    rows = list(cx.rows.get(3, []))
    rnd = random.Random(seed)
    best = None
    for t in range(tries):
        r = rows[:]
        if t:
            rnd.shuffle(r)
        w = z
        imp = True
        while imp:
            imp = False
            for row in r:
                nz = w ^ row
                if nz.bit_count() < w.bit_count():
                    w, imp = nz, True
        if best is None or w.bit_count() < best.bit_count():
            best = w
    return best


def regime_record(C, L, beta2):
    cx = cb.Complex(tc.source_mask(C, L), 6)
    reps, piv = cb.homology_representatives(cx, 2)
    assert len(reps) == cx.betti()[2] == beta2, (C, L, len(reps), beta2)
    L2 = cx.dims[2]
    out = []
    for z0 in reps:
        z = reduce_many(cx, z0)
        phi = cb.cocycle_certificate(cx, 2, z, piv)
        ver = cb.verify_cocycle(cx, 2, z, phi)
        assert ver["z_is_cycle"] and ver["phi_of_z"] == 1 and ver["phi_kills_all_boundaries"]
        zb = 0
        for j in range(len(L2)):
            if z >> j & 1:
                zb |= 1 << L2[j]
        cz, sig = A.canonical(zb)
        phiL = [L2[j] for j in range(len(L2)) if phi >> j & 1]
        zl = [L2[j] for j in range(len(L2)) if z >> j & 1]
        out.append({"weight": zb.bit_count(), "canon_cycle": cz, "sigma": list(sig), "z_faces": zl, "phi_faces": phiL})
    return out


def run():
    t0 = time.time()
    recs = []
    certs = []
    classes = defaultdict(list)
    for r in R:
        C, L, b = tuple(r["content"]), r["L"], r["beta2"]
        rr = regime_record(C, L, b)
        recs.append({"content": list(C), "L": L, "beta2": b, "ps1_explained": r["explaining_bijections"] > 0, "classes": [x["canon_cycle"] for x in rr], "weights": [x["weight"] for x in rr]})
        certs.append({"content": list(C), "L": L, "beta2": b, "basis": [{"z_faces": x["z_faces"], "phi_faces": x["phi_faces"], "weight": x["weight"], "sigma_to_canonical": x["sigma"]} for x in rr]})
        for x in rr:
            classes[x["canon_cycle"]].append((C, L))
    return recs, classes, round(time.time() - t0, 1), certs


if __name__ == "__main__":
    recs, classes, sec, certs = run()
    json.dump(certs, open(os.path.join(_path.ROOT, 'CERTIFICATES', 'regime_certificates.json'), 'w'))
    out = {"regimes": len(recs), "basis_cycles": sum(len(r["classes"]) for r in recs), "distinct_canonical_cycles": len(classes), "seconds": sec,
           "weight_hist": dict(Counter(w for r in recs for w in r["weights"])),
           "beta2_hist": dict(Counter(r["beta2"] for r in recs)),
           "records": [{**r, "classes": [str(c) for c in r["classes"]]} for r in recs]}
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E22_extract.json"), "w"), indent=1)
    print({k: v for k, v in out.items() if k != "records"})
