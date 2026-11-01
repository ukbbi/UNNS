"""v005: exact verification of the 3D containment FAILURES (counterexamples to 'no free coordinate => preservation').
Three independent routes: (A) mini.py brute force from the definitions; (B) the pinned E2-P3 engine through lattice_model.compare_lattices
+ its independent certificate checker; (C) geo3.py (numpy complex).  Lattices are given by row-HNF bases of Z^3 sublattices."""
import sys, os
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mini
import geo3

# name -> (Lambda basis, Lambda' basis, box, source cell (base, gens), witness)
CASES = {
    # primitive failure: E3 inside Z^3 (free coordinates), box (1,2,1)
    "CE0_E3_in_Z3": dict(B=[[1, 0, 1], [0, 1, 1], [0, 0, 2]], Bp=[[1, 0, 0], [0, 1, 0], [0, 0, 1]], Q=(1, 2, 1),
                         base=(0, 1, 1), gens=((0, 1, -1), (1, -1, 0)), w=(Fr(1, 3), Fr(5, 6), Fr(5, 6))),
    # dilation by 2: 2*E3 inside 2*Z^3 -- NO free coordinate (axis orders (2,2,2))
    "CE1_2E3_in_2Z3": dict(B=[[2, 0, 2], [0, 2, 2], [0, 0, 4]], Bp=[[2, 0, 0], [0, 2, 0], [0, 0, 2]], Q=(2, 4, 2),
                           base=(0, 2, 2), gens=((0, 2, -2), (2, -2, 0)), w=(Fr(2, 3), Fr(5, 3), Fr(5, 3))),
    # dilation by 3
    "CE2_3E3_in_3Z3": dict(B=[[3, 0, 3], [0, 3, 3], [0, 0, 6]], Bp=[[3, 0, 0], [0, 3, 0], [0, 0, 3]], Q=(3, 6, 3),
                           base=(0, 3, 3), gens=((0, 3, -3), (3, -3, 0)), w=(Fr(1), Fr(5, 2), Fr(5, 2))),
    # same source, split target E_2 x 2Z (coordinate 2 split with period 2)
    "CE3_2E3_in_E2x2Z": dict(B=[[2, 0, 2], [0, 2, 2], [0, 0, 4]], Bp=[[1, 0, 1], [0, 2, 0], [0, 0, 2]], Q=(2, 4, 2),
                             base=(0, 2, 2), gens=((0, 2, -2), (2, -2, 0)), w=(Fr(2, 3), Fr(5, 3), Fr(5, 3))),
    # same source, NON-SPLIT target: all coordinates of the same parity (body-centred)
    "CE4_2E3_in_BCC": dict(B=[[2, 0, 2], [0, 2, 2], [0, 0, 4]], Bp=[[1, 1, 1], [0, 2, 0], [0, 0, 2]], Q=(2, 4, 2),
                           base=(0, 2, 2), gens=((0, 2, -2), (2, -2, 0)), w=(Fr(5, 6), Fr(5, 3), Fr(3, 2))),
}
# contrast: the same source cell IS contained in the non-split face-centred target E_3 (finite exact)
CONTRAST = {"K0_2E3_in_E3": dict(B=[[2, 0, 2], [0, 2, 2], [0, 0, 4]], Bp=[[1, 0, 1], [0, 1, 1], [0, 0, 2]], Q=(2, 4, 2))}


def check_case(name, c, with_engine=True):
    B = tuple(map(tuple, c["B"])); Bp = tuple(map(tuple, c["Bp"]))
    mB = lambda v: geo3.member(B, v); mBp = lambda v: geo3.member(Bp, v)
    Q = c["Q"]; res = {"name": name, "Lambda": B, "Lambda_prime": Bp, "box": Q, "axis_orders_target": geo3.axis_orders(Bp),
                       "split_coordinates_target": geo3.split_coordinates(Bp)}
    assert geo3.contains_lattice(Bp, B)
    # (A) from the definitions
    ok, why = mini.is_cell_of(mB, Q, c["base"], c["gens"]); res["A_source_is_cell"] = ok
    w = tuple(c["w"]); res["A_witness_in_source_cell"] = mini.in_cell(c["base"], c["gens"], w)
    tcells, F, G = mini.cells(mBp, Q)
    res["A_n_target_cells"] = len(tcells); res["A_witness_in_target_union"] = mini.in_union(tcells, w)
    # (C) numpy
    C = geo3.Complex(Bp, Q)
    res["C_witness_covered_float"] = bool(C.covers([float(x) for x in w], __import__("numpy").array(Q)))
    # (B) pinned engine
    if with_engine:
        import _boot
        lm = _boot.p4("lattice_model")
        import certificate_check as cc
        r = lm.compare_lattices(lm.member3(B), lm.member3(Bp), Q)
        res["B_engine_verdict"] = r["verdict"]
        if r["verdict"] == "NOT_CONTAINED":
            okc, whyc = cc.verify_noncontainment(r["certificate"], r["target_maximal"], 3)
            res["B_certificate_independently_verified"] = okc
            res["B_engine_witness"] = r["certificate"]["witness"]
    res["FAILURE_CONFIRMED_A"] = bool(res["A_source_is_cell"] and res["A_witness_in_source_cell"] and not res["A_witness_in_target_union"])
    return res


if __name__ == "__main__":
    import json
    out = [check_case(k, v) for k, v in CASES.items()]
    for r in out:
        print(json.dumps(r, default=str))
