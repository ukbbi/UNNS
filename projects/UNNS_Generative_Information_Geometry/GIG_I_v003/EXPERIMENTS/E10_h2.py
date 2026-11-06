"""E10 -- the two inherited beta_2=1 anchors: f-vector, boundary ranks, chain-complex checks, an explicit nonzero 2-cycle z,
a 2-cochain phi vanishing on every 3-cell boundary with phi(z)=1, and the actual 3-cells / incidences around z."""
import json
import os
from collections import Counter
import _path
import history_complex as hc
import threshold_closure as tc
import cell_boundary as cb
import face_threshold as ft

ANCHORS = {"A": ((2, 3, 4, 5, 8, 9), 288, 372), "B": ((2, 3, 6, 7, 8, 9), 432, 276)}


def reduce_weight(cx, z, piv):
    """local search: add 3-cell boundaries while weight decreases (z stays in the same homology class)."""
    rows = cx.rows.get(3, [])
    improved = True
    while improved:
        improved = False
        for r in rows:
            nz = z ^ r
            if nz.bit_count() < z.bit_count():
                z, improved = nz, True
    return z


def anchor(name, C, src, n_expected, write=True):
    k = 6
    mask = tc.source_mask(C, src)
    cx = cb.Complex(mask, k)
    f, rk = cx.f(), cx.ranks()
    betti = cx.betti()
    reps, piv = cb.homology_representatives(cx, 2)
    z = reduce_weight(cx, reps[0], piv)
    phi = cb.cocycle_certificate(cx, 2, z, piv)
    ver = cb.verify_cocycle(cx, 2, z, phi)
    gfaces = cx.gfaces
    L2 = cx.dims[2]
    supp = [j for j in range(len(L2)) if z >> j & 1]
    types2 = Counter(ft.TYPE_NAME[ft.face_type(gfaces[L2[j]])] for j in supp)
    # 3-cells of the complex and their incidences with supp(z)
    L3 = cx.dims.get(3, [])
    cells = []
    meet = 0
    for j, g in enumerate(L3):
        row = cx.rows[3][j]
        inter = (row & z).bit_count()
        if inter:
            meet += 1
        cells.append({"face": [list(B) for B in gfaces[g]], "type": ft.TYPE_NAME[ft.face_type(gfaces[g])],
                      "facets_in_complex": row.bit_count(), "facets_in_support_of_z": inter})
    # incidence count: how many complex 3-cells contain each support 2-face
    inc = Counter()
    for r in cx.rows.get(3, []):
        x = r & z
        while x:
            b = x & -x
            inc[b.bit_length() - 1] += 1
            x ^= b
    inc_hist = Counter(inc.get(j, 0) for j in supp)
    # full inventory of 3-cells by type
    inv = Counter(c["type"] for c in cells)
    # the 3-faces of the FULL P_6 whose boundary has odd phi-parity: phi is a cocycle on X(m') iff none of them lies in X(m')
    import math
    import block_factor as bf
    Dn = bf.denominators(C)
    gidx = {f: i for i, f in enumerate(cx.gfaces)}
    phi_faces = {gidx[tuple(tuple(b) for b in gfaces[L2[j]])] for j in range(len(L2)) if phi >> j & 1}
    obstructed = []
    fs_, vm_, dim_, bnd_ = hc._complex_data(k)
    for i, fc in enumerate(fs_):
        if dim_[i] == 3 and sum(1 for b in bnd_[i] if b in phi_faces) % 2:
            K = ft.threshold_closed_form(C, fc, Dn)
            obstructed.append({"face": [list(B) for B in fc], "type": ft.TYPE_NAME[ft.face_type(fc)], "threshold_K_F": K,
                               "K_F_over_gcd_with_source": K // math.gcd(K, src), "present_in_anchor_complex": K != 0 and src % K == 0})
    res = {"anchor": name, "content": C, "source": src, "arrangements": mask.bit_count(), "arrangements_expected": n_expected,
           "f_vector": f, "rank_d1_d2_d3_d4_d5": rk, "betti": betti,
           "boundary_squared_violations": cx.check_boundary_squared(),
           "accounting_beta2_equals_f2_minus_rk2_minus_rk3": betti[2] == f[2] - rk[1] - rk[2],
           "three_cells_by_type": dict(inv),
           "z": {"weight": z.bit_count(), "face_types": dict(types2), "is_cycle": ver["z_is_cycle"]},
           "phi": {"weight": phi.bit_count(), "kills_all_3cell_boundaries": ver["phi_kills_all_boundaries"], "phi_of_z": ver["phi_of_z"]},
           "obstructed_3faces_of_P6": obstructed,
           "incidences": {"three_cells_total": len(L3), "three_cells_meeting_supp_z": meet,
                          "histogram_#3cells_containing_each_supp_face": {str(a): b for a, b in sorted(inc_hist.items())},
                          "supp_faces_in_no_3cell": inc_hist.get(0, 0)}}
    if write:
        cert = dict(res)
        cert["z_faces"] = [[list(B) for B in gfaces[L2[j]]] for j in supp]
        cert["phi_support_faces"] = [[list(B) for B in gfaces[L2[j]]] for j in range(len(L2)) if phi >> j & 1]
        cert["three_cells"] = cells
        os.makedirs(_path.CERTS, exist_ok=True)
        with open(os.path.join(_path.CERTS, "H2_anchor_%s.json" % name), "w") as fh:
            json.dump(cert, fh, indent=1, sort_keys=True)
    return res


def run(quick=False):
    return {"experiment": "E10", "anchors": {n: anchor(n, *v, write=not quick) for n, v in ANCHORS.items()}}


if __name__ == "__main__":
    print(json.dumps(run(), indent=1))
