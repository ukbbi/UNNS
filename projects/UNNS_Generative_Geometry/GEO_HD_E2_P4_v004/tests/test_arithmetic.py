import _path  # noqa: F401
from fractions import Fraction as Fr
af = _path._boot.p4("arithmetic_family")


def test_family_members():
    for m in range(1, 9):
        assert af.verify_member(m)["all_pass"]


def test_known_values_m1():
    r = af.field_I_step(af.x_m(1))
    assert r["G"] == 9 and r["L"] == 110 ** 2 and r["next"] == Fr(110 ** 4, 3)
    assert len(af.occurrence_exponents(1, 9)) == 5 and len(af.occurrence_exponents(1, 3)) == 13


def test_engine_agrees():
    import fibre_transport as ft
    for m in (1, 2):
        assert ft.C_step(af.x_m(m))["next"] == af.y_m(m)
