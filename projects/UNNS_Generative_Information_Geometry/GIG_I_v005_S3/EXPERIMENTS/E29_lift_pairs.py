"""E29 (S3-2, S3-3) -- the two-sided suspension lift L_{c_a,c_b}(z) = Lam(z) + first(c_a) + last(c_b) of the distinguished H_2 cycle z (96 faces, 4 minimal fillings
B0..B3 of Stage 1) for all 12 ordered pairs a != b and the 4 diagonal pairs: cycle test, cochain pairing, obstructed 4-faces, P_z3, exact minimal filling families
(P_7, 4-cell boundaries) with an independently checkable completeness certificate."""
import itertools, json, os, time
import _path
import hole_survival as H
import lift as Lf
from pk import PK, verify_family_certificate

P6, P7 = PK(6), PK(7)


def run():
    z6 = P6.bits(H.Z)
    f6, _ = P6.minimal_families(z6, 2)
    P = P6.pz(z6)
    chains = [Lf.filling_chain(P6, z6, P | F) for F in f6]
    phi2 = [P6.FS[g] for g in H.PHI]
    phi3 = P7.bits([P7.IDX[Lf.ins(f, 0, 6)] for f in phi2])
    obs = P7.obstructed(phi3, 3)
    S = lambda f: [s for s in range(128) if f >> s & 1]
    out = {"H2_families": [S(f) for f in f6], "chain_sizes": [len(c) for c in chains], "phi3_obstructed_4faces": [[list(b) for b in P7.FS[i]] for i in obs], "pairs": []}
    for a, b in itertools.product(range(len(f6)), repeat=2):
        t = time.time()
        zf = Lf.lam_faces([P6.FS[g] for g in H.Z], 6) ^ Lf.first([P6.FS[g] for g in chains[a]], 6) ^ Lf.last([P6.FS[g] for g in chains[b]], 6)
        ids = sorted(P7.IDX[f] for f in zf)
        z3 = P7.bits(ids)
        fams, st = P7.minimal_families(z3, 3, certificate=True)
        ok, msg = verify_family_certificate(P7, z3, 3, fams, st["maximal_false_sets"])
        out["pairs"].append({"a": a, "b": b, "diagonal": a == b, "weight": len(ids), "is_cycle": P7.is_cycle(z3), "phi3_of_z3": bin(z3 & phi3).count("1") & 1,
                             "P_size": P7.pz(z3).bit_count(), "q": st["q"], "families": [S(f) for f in fams], "family_sizes": sorted(f.bit_count() for f in fams),
                             "degenerate_(empty_family)": 0 in fams, "completeness_certified": ok, "completeness_msg": msg, "n_maximal_false": len(st["maximal_false_sets"]),
                             "maximal_false_sets": [S(n) for n in st["maximal_false_sets"]], "z3_faces": ids, "seconds": round(time.time() - t, 1)})
        print(a, b, out["pairs"][-1]["family_sizes"], ok, out["pairs"][-1]["seconds"])
    return out


if __name__ == "__main__":
    r = run()
    json.dump(r, open(os.path.join(_path.ROOT, "CERTIFICATES", "lift_pairs.json"), "w"))
    json.dump({"H2_families": r["H2_families"], "pairs": [{k: v for k, v in p.items() if k not in ("z3_faces", "maximal_false_sets", "families")} | {"families": p["families"]} for p in r["pairs"]]},
              open(os.path.join(_path.ROOT, "RESULTS", "E29_lift_pairs.json"), "w"), indent=1)
