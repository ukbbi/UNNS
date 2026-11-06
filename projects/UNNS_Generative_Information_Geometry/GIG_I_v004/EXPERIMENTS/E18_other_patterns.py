"""E18 -- the beta_2 > 0 regimes of the k=6 census (labels <= 16) NOT explained by the PS-1 pattern: certificates and a coarse signature.
For each unexplained regime: minimal-weight cycle z' (local search), cochain phi' (phi'(d3 c)=0, phi'(z')=1), signature = (|z'|, face types of z',
|phi'|, types of the obstructed 3-faces of P_6 with their threshold ratios K/gcd(K, L)).  Signatures are NOT canonical up to S_6 (coarse)."""
import json
import time
from collections import Counter
import math
import _path  # noqa: F401
import threshold_closure as tc
import cell_boundary as cb
import face_threshold as ft
import block_factor as bf
import history_complex as hc
import E10_h2


def certify(C, L):
    cx = cb.Complex(tc.source_mask(C, L), 6)
    reps, piv = cb.homology_representatives(cx, 2)
    out = []
    fs, vm, dim, bnd = hc._complex_data(6)
    gidx = {f: i for i, f in enumerate(fs)}
    D = bf.denominators(list(C))
    for z0 in reps[:1]:
        z = E10_h2.reduce_weight(cx, z0, piv)
        phi = cb.cocycle_certificate(cx, 2, z, piv)
        ver = cb.verify_cocycle(cx, 2, z, phi)
        L2 = cx.dims[2]
        zt = Counter(ft.TYPE_NAME[ft.face_type(cx.gfaces[L2[j]])] for j in range(len(L2)) if z >> j & 1)
        phiS = {L2[j] for j in range(len(L2)) if phi >> j & 1}
        obs = []
        for i, f in enumerate(fs):
            if dim[i] == 3 and sum(1 for b in bnd[i] if b in phiS) % 2:
                K = ft.threshold_closed_form(list(C), f, D)
                obs.append((ft.TYPE_NAME[ft.face_type(f)], K // math.gcd(K, L), L % K == 0))
        out.append({"z_weight": z.bit_count(), "z_types": dict(zt), "phi_weight": phi.bit_count(), "verified": ver["z_is_cycle"] and ver["phi_of_z"] == 1 and ver["phi_kills_all_boundaries"],
                    "obstructed": sorted(obs), "n_obstructed": len(obs)})
    return out


def run(results_json, limit=None):
    t0 = time.time()
    r = json.load(open(results_json))
    un = r["E15"]["completeness_census"]["beta2_regimes_unexplained_by_parametric_mechanism"]
    if limit:
        un = un[:limit]
    sigs = Counter()
    ex = {}
    allv = True
    for C, L, b in un:
        for c in certify(tuple(C), L):
            allv &= c["verified"]
            sig = (c["z_weight"], tuple(sorted(c["z_types"].items())), c["phi_weight"], c["n_obstructed"], tuple(sorted(Counter(t for t, _, _ in c["obstructed"]).items())))
            sigs[sig] += 1
            ex.setdefault(sig, {"content": C, "L": L, "obstructed": c["obstructed"]})
    return {"experiment": "E18", "unexplained_regimes": len(un), "all_certificates_verified": allv, "distinct_coarse_signatures": len(sigs),
            "signatures": [{"z_weight": s[0], "z_types": dict(s[1]), "phi_weight": s[2], "n_obstructed_3faces": s[3], "obstructed_types": dict(s[4]), "regimes": n, "example": ex[s]}
                           for s, n in sigs.most_common()], "seconds": round(time.time() - t0, 1)}


if __name__ == "__main__":
    import os
    out = run(os.path.join(_path.RESULTS, "results.json"))
    with open(os.path.join(_path.RESULTS, "E18_other_patterns.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(out["unexplained_regimes"], out["distinct_coarse_signatures"], out["all_certificates_verified"])
    for s in out["signatures"]: print(s["regimes"], s["z_weight"], s["z_types"], s["phi_weight"], s["n_obstructed_3faces"], s["obstructed_types"], s["example"]["content"], s["example"]["L"])
