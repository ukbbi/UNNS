"""E35 (v006-3) -- full-complex verification of the arithmetic filling-dependence examples of E34 (GF(2)).  For each hit (content, a, a', b) and m = K: A(m) = {I : D(I) | m};
the cycles L_{a,b}, L_{a',b} and their sum first(c_a+c_a') are tested against boundaries of ALL 4-faces of P_7 whose prefix sets lie in A(m) (not only the family-based test).
Also records the dimension of the span {[L],[L']} in H_3 (2 iff all three of [L],[L'],[L+L'] are nonzero)."""
import json, os
import _path
import hole_survival as H, lift as Lf, fi
from pk import PK
from E30_arith import denominators
import E34_filling_dependence as E34

P6, P7 = PK(6), PK(7)
z6 = P6.bits(H.Z)
f6, _ = P6.minimal_families(z6, 2)
P = P6.pz(z6)
ch = [set(Lf.filling_chain(P6, z6, P | F)) for F in f6]


def L(a, b):
    zf = Lf.lam_faces([P6.FS[g] for g in H.Z], 6) ^ Lf.first([P6.FS[g] for g in ch[a]], 6) ^ Lf.last([P6.FS[g] for g in ch[b]], 6)
    return P7.bits([P7.IDX[f] for f in zf])


if __name__ == "__main__":
    res = json.load(open(os.path.join(_path.ROOT, "RESULTS", "E34_filling_dependence.json")))
    out = []
    for h in res["hits"]:
        C, a, a2, b, K = h["content"], h["a"], h["a2"], h["b"], int(h["K"])
        D = denominators(C)
        A = sum(1 << s for s in range(1, 128) if K % D[s] == 0)
        l1, l2 = L(a, b), L(a2, b)
        B = fi.Bounder(P7, A, 3)
        inA = lambda z: not P7.pz(z) & ~A
        rec = {"content": C, "a": a, "a2": a2, "b": b, "m": K, "cells_in_complex": inA(l1) and inA(l2), "both_cycles": P7.is_cycle(l1) and P7.is_cycle(l2),
               "L_bounds": B.contains(l1), "Lp_bounds": B.contains(l2), "sum_bounds": B.contains(l1 ^ l2)}
        rec["independent_classes_in_H3"] = rec["cells_in_complex"] and rec["both_cycles"] and not (rec["L_bounds"] or rec["Lp_bounds"] or rec["sum_bounds"])
        out.append(rec)
        print(rec)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E35_verify_dependence.json"), "w"), indent=1)
