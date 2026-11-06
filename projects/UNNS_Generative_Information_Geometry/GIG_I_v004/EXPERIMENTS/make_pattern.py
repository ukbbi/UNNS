"""write CERTIFICATES/pattern_H2.json: the content-independent combinatorial data of the Parametric Hole-Survival Theorem (k=6)."""
import json
import os
import _path
import hole_survival as H


def sets(masks):
    return ["".join(str(r) for r in range(6) if I >> r & 1) for I in masks]


chk = H.check_cycle_and_cochain()
gs = H.gate_sets()
pair_equal = all(set(H.PT[H.GATES[a][0]]) - set(H.PZ) == set(H.PT[H.GATES[a][1]]) - set(H.PZ) for a in H.GATES)
fill0 = H.universal_filling(0)
doc = {"description": "content-independent data of the Parametric Hole-Survival Theorem (rank coordinates 0..5)",
       "z_faces": [[list(B) for B in H._FS[g]] for g in H.Z], "phi_faces": [[list(B) for B in H._FS[g]] for g in H.PHI],
       "z_is_cycle": chk["z_is_cycle"], "phi_of_z": chk["phi_of_z"],
       "obstructed_3faces_of_P6": [[list(B) for B in t] for t in chk["obstructed_3faces"]],
       "P_z_prefix_sets": sets(H.PZ), "gate_sets": {str(a): sets(S) for a, S in gs.items()},
       "two_orderings_give_same_gate_sets": pair_equal,
       "gate0_universal_filling": {"faces": [[list(B) for B in H._FS[i]] for i in fill0], "count": len(fill0)}}
with open(os.path.join(_path.CERTS, "pattern_H2.json"), "w") as f:
    json.dump(doc, f, indent=1)
print(len(H.Z), len(H.PHI), chk["z_is_cycle"], chk["phi_of_z"], pair_equal, len(fill0), {a: sets(S) for a, S in gs.items()})
