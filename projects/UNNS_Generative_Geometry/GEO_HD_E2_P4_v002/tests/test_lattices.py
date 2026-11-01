import _path  # noqa: F401
cl = _path._boot.p4("coupled_lattices")
P = (2, 5, 11)


def test_nonrectangular_and_relation():
    assert cl.describe(P, 9)["nonrectangular"] and cl.describe(P, 3)["nonrectangular"]
    assert cl.relation(P, 9, 3) == "ENLARGE" and cl.relation(P, 3, 9) == "SHRINK"


def test_rectangular_example():
    assert cl.is_rectangular((2, 7, 13), 3)  # target of the E2-P3 witness: a even only


def test_index():
    assert cl.index(P, 9) == 6 and cl.index(P, 3) == 2
