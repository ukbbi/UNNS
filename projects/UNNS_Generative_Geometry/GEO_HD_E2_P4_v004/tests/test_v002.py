import json
import os
from fractions import Fraction as Fr

import _path  # noqa: F401
au2 = _path._boot.p4("audit_v002")
sl = _path._boot.p4("slab_law")
zv = _path._boot.p4("zero_vertex")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(rel):
    return json.load(open(os.path.join(ROOT, rel)))


def test_c1_equality_false_small_box():
    # n=4 is slow; the same obstruction at the level of cells: 2Z^3 has Graver +-2e_i, so cube [0,2]^3 (corner 0) is never a cell
    F, S = au2.cells_from_member(lambda v: all(x % 2 == 0 for x in v), (2, 2, 2))
    assert not au2.in_cells(S, (Fr(1), Fr(1), Fr(1)))


def test_edges_never_obstruct():
    inL = lambda v: True  # noqa: E731
    # source E2 (even sum): g=(-1,1) is Graver, edge (1,1)->(0,2) has corners in F; target Z^2
    assert zv.zero_vertex_decomposition((1, 1), [(-1, 1)], inL) is None


def test_zv_flag_example():
    d = load("results/P4_LATTICE3.json")["failures"][0]
    ex = d["zv_example"]
    inT = lambda v: au2.in_hnf(d["Bp"], v)  # noqa: E731
    assert au2.zv_decomposition_ok(inT, ex)


def test_slab_lemma_finite():
    tot, bad = au2.slab_lemma_check(2)
    assert tot == 243 and bad == 0


def test_all_slab_witnesses_recorded():
    s = load("results/P4_SLAB.json")
    assert s["lattice_level"]["n_slab_witness"] == 36 and s["fieldI"]["n_slab_witness"] == 21


def test_smallest_fieldI_counterexample():
    r = min(load("results/P4_FIELDI3.json")["noncontained"], key=lambda r: Fr(r["x"]))
    assert r["x"] == "2352980000/9" and r["x_next"] == "1176490000/3" and r["primes"] == [2, 5, 7] and r["box"] == [2, 2, 3]
    inS, inT = au2.chi_member(r["primes"], 9), au2.chi_member(r["primes"], 3)
    ok, why = au2.noncontained_ok(inS, inT, tuple(r["box"]), r["witness_cell"], r["witness"])
    assert ok, why


def test_independent_rescreen_matches_stored_planar_sample():
    rows = load("results/P4_PLANAR_CORE.json")["rows"][:100]
    for r in rows:
        assert au2.zv_rescreen(r["primes"], r["b"], r["b_next"], r["box"]) == (r["n_src_max"], r["n_zv"])


def test_z2_explicit_matches_bruteforce_on_small_pair():
    ze = _path._boot.p4("zv_explicit")
    lm = _path._boot.p4("lattice_model")
    import exact_containment as ec
    inS, inT = lm.member2(((1, 1), (0, 3))), lm.member2(((1, 0), (0, 1)))
    F, cs = lm.cells_of_member(inS, (3, 3))
    for b, g in ec.geometric_maximal(cs, 2):
        if g:
            assert (zv.zero_vertex_decomposition(b, g, inT) is not None) == ze.zv_explicit(b, g, inT)


def test_k1_counterexample_cell_is_contained():
    ok = au2.counterexample_K1()
    assert all(ok)
