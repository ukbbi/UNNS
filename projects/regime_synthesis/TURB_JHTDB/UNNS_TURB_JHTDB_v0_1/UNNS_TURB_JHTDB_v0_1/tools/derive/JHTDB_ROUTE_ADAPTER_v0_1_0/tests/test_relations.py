import numpy as np
import pandas as pd

from jhtdb_adapter.relations import overlap_relations


def _obj(node, oid, cx=0, vol=8, r=1):
    return {
        "node_id":node,"object_id":oid,"cx":cx,"cy":0.0,"cz":0.0,
        "equiv_radius":r,"enstrophy_mean":1.0
    }


def test_scale_overlap_exact_nested_blocks():
    src = np.zeros((4,4,4), dtype=np.int32)
    src[:2,:2,:2] = 1
    dst = np.zeros((2,2,2), dtype=np.int32)
    dst[0,0,0] = 1

    so = pd.DataFrame([_obj("s","o000001")])
    do = pd.DataFrame([_obj("d","o000001")])

    r = overlap_relations(
        src,dst,so,do,axis="scale",
        src_factor=1,dst_factor=2,spacing_native=1.0
    )
    assert len(r) == 1
    assert np.isclose(r.iloc[0].overlap_src, 1.0)
    assert np.isclose(r.iloc[0].overlap_dst, 1.0)
    assert np.isclose(r.iloc[0].iou, 1.0)
