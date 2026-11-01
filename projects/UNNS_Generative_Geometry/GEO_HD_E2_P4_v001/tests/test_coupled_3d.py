import _path  # noqa: F401
c3 = _path._boot.p4("coupled_3d")


def test_admissible():
    assert c3.admissible_for_census((2, 5, 11), 9, 3)
    assert not c3.admissible_for_census((2, 7, 13), 9, 3)  # rectangular target (E2-P3 witness) is only a control


def test_status_honest():
    assert c3.STATUS == "NOT_STARTED"
