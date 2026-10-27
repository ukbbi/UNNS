"""GEO-I v004: arithmetic criteria for embedding / essential dimensionality (exact, finite-group arithmetic only).

(C1) k=2:  K_abs(Lambda,q) is embedded for ALL boxes q  <=>  |H| = o1*o2   (v003 T2, re-proved/used here).
(C2) any k: |H| = o_1...o_k  (direct product)  ==> embedded for all boxes   (v003 T2a).
(C3) templates:  embedded(q)  <=>  q >= no minimal box of a forbidden template (theory/obstruction_templates.py, T-FIN).
(C4) essential dimensionality (G4-T6).  A prime with residue 1 mod b contributes the unit axis e_i to Lambda
     (Lambda = Lambda' + Z e_i, an orthogonal direct summand, order o_i = 1).  Theorem E: adjoining it does not change whether the
     complex is embedded; it is therefore NOT an essential dimension.  The essential dimension of (res,b) is the number of
     distinct non-1 residues, further reduced by exact repeats (equal residues give the diagonal move g=e_i-e_j, order 1 direction,
     which IS essential for embedding: Proposition D) - see essential_dimension()."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry',): sys.path.insert(0, os.path.join(HERE, '..', d_))
from math import prod
from arith import order_mod, group_order


def invariants(res, b):
    o = [order_mod(r, b) for r in res]
    H = group_order(res, b)
    return {'orders': o, 'H': H, 'prod_orders': prod(o), 'direct_product': H == prod(o), 'k': len(res)}


def embedded_for_all_boxes_sufficient(res, b):
    """True if the direct-product condition guarantees embedding for every box (C2)."""
    return invariants(res, b)['direct_product']


def k2_embedded_for_all_boxes(res, b):
    assert len(res) == 2
    return invariants(res, b)['direct_product']


def drop_unit_residues(res):
    """remove primes with residue 1 (unit axes).  returns (reduced residues, dropped indices)."""
    keep = [i for i, r in enumerate(res) if r != 1]
    return tuple(res[i] for i in keep), [i for i in range(len(res)) if i not in keep]


def essential_dimension(res, b):
    """number of directions that can participate in an obstruction: non-unit residues (a residue-1 prime is not essential)."""
    return len(drop_unit_residues([r % b for r in res])[0])


def klein_four(res, b):
    """True when H = <res> is isomorphic to Z/2 x Z/2 and the residues have orders (2,2,2) (the G4-T4 family)."""
    from arith import order_mod as om
    return sorted(om(r, b) for r in res) == [2, 2, 2] and group_order(res, b) == 4
