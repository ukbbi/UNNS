import json
import os
from fractions import Fraction as Fr

import _path  # noqa: F401
au4 = _path._boot.p4("audit_p4")


def _c():
    return json.load(open(os.path.join(_path.ROOT, "results", "P4_CERTIFICATES.json")))


def test_forward_reverse_and_hull_m1():
    c = _c()
    q = (2, 2, 2)
    assert au4.verify_forward(c["m1_forward"], q, 9, 3)[0]
    assert au4.verify_noncontained(c["m1_reverse"], q, 3, 9)[0]
    ok, why, ng = au4.verify_hull(c["m1_target_hull_cover"], q, 3)
    assert ok and ng > 0


def test_tamper_rejected():
    import copy
    c = copy.deepcopy(_c())
    rec = c["m1_reverse"]
    w = rec["certificate"]["witness"]
    rec["certificate"]["witness"] = [w[0], w[1], str(Fr(w[2]) + 1)]
    assert not au4.verify_noncontained(rec, (2, 2, 2), 3, 9)[0]


def test_point_certificates():
    for m, rec in _c()["reverse_points"].items():
        if m == "1":
            assert au4.verify_point(rec, tuple(rec["box"]), 9)[0]
