import _path  # noqa: F401
x4 = _path._boot.p4("exact_containment")
tg = _path._boot.p4("target_gap")
P = (2, 5, 11)


def test_m1_classification():
    r = x4.compare(P, 9, 3, (2, 2, 2))
    assert r["classification"] == "SOURCE_CONTAINED"
    assert r["census_source"]["f_vector"] == [5, 7, 2, 0] and r["census_target"]["f_vector"] == [13, 45, 36, 3]


def test_cube_tiling_and_hull():
    for n in (2, 4, 6):
        assert tg.cube_tiling_lemma(n)[0] and tg.hull_check_e3(n)[0]


def test_cell_monotone_small():
    assert tg.cell_vertex_sets(2) <= tg.cell_vertex_sets(4)
