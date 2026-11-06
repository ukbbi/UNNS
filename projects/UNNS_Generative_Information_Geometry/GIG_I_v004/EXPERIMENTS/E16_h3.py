"""E16 -- explicit certificates for the four k=7 beta_3 = 1 regimes found by v003/E14: a 3-cycle z3, a 3-cochain phi3 with
phi3(d4 c)=0 for every 4-face c of the complex and phi3(z3)=1, the obstructed 4-faces of the full P_7 (odd phi3-parity) with their
exact thresholds, the fate of z3 over all regimes of the content, and verified fillings."""
import json
import os
import time
from collections import Counter
import _path
import history_complex as hc
import threshold_closure as tc
import cell_boundary as cb
import face_threshold as ft
import block_factor as bf
import source_filtration as sf

CASES = {"H3-1": ((2, 3, 4, 5, 8, 9, 14), 4032), "H3-2": ((2, 3, 4, 5, 8, 9, 15), 4320),
         "H3-3": ((2, 3, 6, 7, 8, 9, 14), 6048), "H3-4": ((2, 3, 6, 7, 8, 9, 15), 6480)}


def reduce_weight(cx, z, d):
    rows = cx.rows.get(d + 1, [])
    improved = True
    while improved:
        improved = False
        for r in rows:
            nz = z ^ r
            if nz.bit_count() < z.bit_count():
                z, improved = nz, True
    return z


def case(name, C, src, write=True):
    k = 7
    mask = tc.source_mask(C, src)
    cx = cb.Complex(mask, k)
    f, rk, bt = cx.f(), cx.ranks(), cx.betti()
    reps, piv = cb.homology_representatives(cx, 3)
    z = reduce_weight(cx, reps[0], 3)
    phi = cb.cocycle_certificate(cx, 3, z, piv)
    ver = cb.verify_cocycle(cx, 3, z, phi)
    L3 = cx.dims[3]
    gf = cx.gfaces
    types = Counter(ft.TYPE_NAME[ft.face_type(gf[L3[j]])] for j in range(len(L3)) if z >> j & 1)
    # vertices of z3 and the label ranks involved
    verts = set()
    for j in range(len(L3)):
        if z >> j & 1:
            verts |= set(hc._face_vertices(gf[L3[j]]))
    # obstructed 4-faces of the full P_7
    fs, vm, dim, bnd = hc._complex_data(k)
    gidx = {g: i for i, g in enumerate(fs)}
    phiS = {gidx[gf[L3[j]]] for j in range(len(L3)) if phi >> j & 1}
    D = bf.denominators(C)
    obs = []
    for i, fc in enumerate(fs):
        if dim[i] == 4 and sum(1 for b in bnd[i] if b in phiS) % 2:
            K = ft.threshold_closed_form(C, fc, D)
            obs.append({"face": [list(B) for B in fc], "type": "x".join(map(str, ft.face_type(fc))), "K_F": K,
                        "K_F_over_gcd_with_source": K // __import__("math").gcd(K, src), "in_complex": src % K == 0})
    obs.sort(key=lambda o: (o["K_F"], o["face"]))
    # fate of z3 over all regimes of the content that contain this one
    zg = {L3[j] for j in range(len(L3)) if z >> j & 1}
    fate = []
    for r in sf.regimes(C):
        if mask & ~r["mask"]:
            continue
        cy = cb.Complex(r["mask"], k)
        zl = sum(1 << cy.local[3][g] for g in zg)
        pv = cb.image_pivots(cy.rows.get(4, []))
        bounds = cb._reduce(zl, dict(pv))[0] == 0
        rec = {"L": r["L"], "N": r["N"], "z3_bounds": bounds, "betti": cy.betti()}
        if bounds:
            c = cb.fill_chain(cy, 3, zl)
            rec["filling_4chain_size"] = c.bit_count()
            rec["filling_verified"] = cb.boundary_of_chain(cy, 4, c) == zl
        fate.append(rec)
    fate.sort(key=lambda d: (d["N"], d["L"]))
    regs_all = sf.regimes(C)
    b3_regimes = []
    res = {"case": name, "content": C, "source": src, "arrangements": mask.bit_count(), "f_vector": f, "ranks": rk, "betti": bt,
           "boundary_squared_violations": cx.check_boundary_squared(),
           "z3": {"weight": z.bit_count(), "face_types": dict(types), "vertices": len(verts), "is_cycle": ver["z_is_cycle"]},
           "phi3": {"weight": phi.bit_count(), "kills_all_4face_boundaries": ver["phi_kills_all_boundaries"], "phi_of_z": ver["phi_of_z"]},
           "obstructed_4faces_of_P7": obs, "regimes_of_content": len(regs_all),
           "z3_fate": {"regimes_above": len(fate), "bounds_in": sum(d["z3_bounds"] for d in fate),
                       "survives_in_L": [d["L"] for d in fate if not d["z3_bounds"]],
                       "killing_L": [d["L"] for d in fate if d["z3_bounds"]], "all_fillings_verified": all(d.get("filling_verified", True) for d in fate)}}
    if write:
        cert = dict(res)
        cert["z3_faces"] = [[list(B) for B in gf[L3[j]]] for j in range(len(L3)) if z >> j & 1]
        cert["phi3_faces"] = [[list(B) for B in gf[L3[j]]] for j in range(len(L3)) if phi >> j & 1]
        cert["fate"] = fate
        with open(os.path.join(_path.CERTS, "H3_%s.json" % name), "w") as fh:
            json.dump(cert, fh, indent=1, sort_keys=True)
    return res


def parametric_existence(Lmax, verify=6):
    """k=7 contents with labels <= Lmax (identity role map): which admit a 3-hole regime according to the parametric criterion for the two
    combinatorial 3-cycle classes (x=14-type: H3-1, x=15-type: H3-2)?  The first `verify` predicted contents are checked by exact homology
    (beta_3 of X(K_z3) and the cocycle)."""
    import h3_survival as H3
    from itertools import combinations
    pats = {c: H3.Pattern(c) for c in ("H3-1", "H3-2")}
    hits = {c: [] for c in pats}
    n = 0
    for C in combinations(range(1, Lmax + 1), 7):
        n += 1
        for c, P in pats.items():
            ok, Kz = P.hole_regime_exists(list(C))
            if ok:
                hits[c].append((C, Kz))
    ver = []
    for c, L_ in hits.items():
        for C, Kz in L_[:verify]:
            cx = cb.Complex(tc.source_mask(C, Kz), 7)
            ver.append({"pattern": c, "content": C, "K_z3": Kz, "betti": cx.betti(), "beta3_positive": cx.betti()[3] > 0})
    return {"labels_max": Lmax, "contents_scanned": n, "predicted_hole_contents": {c: [{"content": C, "K_z3": Kz} for C, Kz in L_] for c, L_ in hits.items()},
            "exact_verification": ver}


def run(quick=False):
    t0 = time.time()
    cases = dict(list(CASES.items())[:1]) if quick else CASES
    out = {"experiment": "E16", "cases": {n: case(n, C, s, write=not quick) for n, (C, s) in cases.items()},
           "parametric_existence": parametric_existence(12 if quick else 18, 2 if quick else 8)}
    out["seconds"] = round(time.time() - t0, 1)
    return out


if __name__ == "__main__":
    r = run()
    for n, c in r["cases"].items():
        print(n, c["betti"], c["z3"], c["phi3"], len(c["obstructed_4faces_of_P7"]), c["z3_fate"], flush=True)
        for o in c["obstructed_4faces_of_P7"][:12]:
            print("   ", o)
