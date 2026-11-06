"""E28 (S3-1) -- reconstruct the four inherited H_3 certificates: exact 3-cycle z3, cochain phi3, cellular boundary verification.
(a) combinatorial, in the full P_7: d3 z3 = 0, phi3(z3)=1, exactly 6 four-faces with odd phi3-boundary, all of the form ({a,2,4,5,6}|y|w).
(b) on the regime complex X_lambda(m) (cell_boundary): beta_3, phi3 kills the boundary of every 4-cell, boundary-squared = 0.
(c) lifted cycle: z3' = Lam(z)+first(c_B0)+last(c_B1) (E29) is homologous to the certified z3 in X_lambda(m)."""
import itertools, json, os, time
import _path
import cell_boundary as cb
import threshold_closure as tc
import hole_survival as H
import lift as Lf
from pk import PK

P6, P7 = PK(6), PK(7)
CASES = {"H3-1": ((2, 3, 4, 5, 8, 9, 14), 4032), "H3-2": ((2, 3, 4, 5, 8, 9, 15), 4320), "H3-3": ((2, 3, 6, 7, 8, 9, 14), 6048), "H3-4": ((2, 3, 6, 7, 8, 9, 15), 6480)}
V4 = _path._vpath.V004


def lifted_pair_cycle(a=0, b=1):
    z6 = P6.bits(H.Z)
    fam, _ = P6.minimal_families(z6, 2)
    P = P6.pz(z6)
    ca = Lf.filling_chain(P6, z6, P | fam[a])
    cb_ = Lf.filling_chain(P6, z6, P | fam[b])
    zf = Lf.lam_faces([P6.FS[g] for g in H.Z], 6) ^ Lf.first([P6.FS[g] for g in ca], 6) ^ Lf.last([P6.FS[g] for g in cb_], 6)
    return sorted(P7.IDX[f] for f in zf)


def run():
    out = {}
    for name, (C, L) in CASES.items():
        d = json.load(open(os.path.join(V4, "CERTIFICATES", "H3_%s.json" % name)))
        z_ids = P7.ids(d["z3_faces"])
        phi_ids = P7.ids(d["phi3_faces"])
        z, phi = P7.bits(z_ids), P7.bits(phi_ids)
        pair = [(a, b) for a, b in itertools.permutations(range(4), 2) if P7.pz(P7.bits(lifted_pair_cycle(a, b))) == P7.pz(z)]
        assert len(pair) == 1
        lift01 = lifted_pair_cycle(*pair[0])
        rec = {"content": list(C), "source": L, "z3_weight": len(z_ids), "phi3_weight": len(phi_ids), "z3_is_cycle_in_P7": P7.is_cycle(z), "phi3_of_z3": bin(z & phi).count("1") & 1}
        ob = P7.obstructed(phi, 3)
        rec["obstructed_4faces_of_P7"] = [[list(b) for b in P7.FS[i]] for i in ob]
        rec["obstructed_all_of_form_a245_6|y|w"] = all(P7.FS[i][0][1:] == (2, 4, 5, 6) or tuple(sorted(set(P7.FS[i][0]) - {0, 1, 3})) == (2, 4, 5, 6) for i in ob)
        cx = cb.Complex(tc.source_mask(C, L), 7)
        pos = {g: j for j, g in enumerate(cx.dims[3])}
        zc = sum(1 << pos[g] for g in z_ids)
        pc = sum(1 << pos[g] for g in phi_ids)
        ver = cb.verify_cocycle(cx, 3, zc, pc)
        rec["regime_complex"] = {"arrangements": cx.f()[0], "f": cx.f(), "betti": cx.betti(), "boundary_squared_ok": cx.check_boundary_squared() in (None, True, 0) or cx.check_boundary_squared(), **ver}
        zl = sum(1 << pos[g] for g in lift01)
        diff = zc ^ zl
        fc = cb.fill_chain(cx, 3, diff)
        rec["lifted_pair"] = {"pair_(a,b)_of_gate_fillings": list(pair[0]), "weight": len(lift01), "present_in_regime_complex": all(g in pos for g in lift01), "z3cert_plus_lift_is_boundary": fc is not None,
                                  "phi3_of_lift": bin(zl & pc).count("1") & 1}
        out[name] = rec
        print(name, {k: v for k, v in rec.items() if k not in ("obstructed_4faces_of_P7",)})
    return out


if __name__ == "__main__":
    t = time.time()
    r = run()
    r["seconds"] = round(time.time() - t, 1)
    json.dump(r, open(os.path.join(_path.ROOT, "RESULTS", "E28_h3_certificates.json"), "w"), indent=1)
