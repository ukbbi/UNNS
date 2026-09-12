import numpy as np
import pandas as pd

from stitch_mech.route_math import jsd_norm, run_metrics
from stitch_mech.nulls import rewire_stratified
from stitch_mech.mechanism import spearman


def objects_square():
    rows=[]
    for t in (0,1):
        for s in (0,1):
            for k,x in enumerate((0.0,10.0)):
                rows.append({
                    "node_id":f"n{s}{t}{k}","scale_idx":s,"time_idx":t,
                    "cx":x,"cy":float(t),"cz":float(s),"equiv_radius":1.0,
                    "enstrophy_mean":1.0+k,"q_mean":0.1,
                    "weight":1.0,"physical_volume":1.0
                })
    return pd.DataFrame(rows)


def edge(src,dst,axis,conf=1.0):
    return {
        "src_id":src,"dst_id":dst,"axis":axis,"confidence":conf,
        "overlap_src":conf,"overlap_dst":conf,"iou":conf,
        "distance_norm":0.5,"feature_similarity":1.0
    }


def commuting_edges():
    e=[]
    for k in (0,1):
        e += [
            edge(f"n00{k}",f"n10{k}","scale"),
            edge(f"n01{k}",f"n11{k}","scale"),
            edge(f"n00{k}",f"n01{k}","time"),
            edge(f"n10{k}",f"n11{k}","time"),
        ]
    return pd.DataFrame(e)


def test_jsd_identity():
    assert abs(jsd_norm({"a":1.0},{"a":1.0})) < 1e-15


def test_commuting_square_zero():
    o=objects_square(); e=commuting_edges()
    m,_,_,_=run_metrics(o,e)
    assert abs(m["stitch_defect"]) < 1e-15


def test_stratified_rewire_preserves_degrees():
    o=objects_square()
    # Add enough alternatives in the same transition group.
    e=pd.DataFrame([
        edge("n000","n100","scale"),edge("n001","n101","scale"),
        edge("n010","n110","scale"),edge("n011","n111","scale"),
        edge("n000","n010","time"),edge("n001","n011","time"),
        edge("n100","n110","time"),edge("n101","n111","time"),
    ])
    before_out=e.groupby(["axis","src_id"]).size().sort_index()
    before_in=e.groupby(["axis","dst_id"]).size().sort_index()
    r,d=rewire_stratified(
        o,e,seed=3,swaps_per_edge=20,distance_bins=2,feature_bins=None
    )
    after_out=r.groupby(["axis","src_id"]).size().sort_index()
    after_in=r.groupby(["axis","dst_id"]).size().sort_index()
    assert before_out.equals(after_out)
    assert before_in.equals(after_in)
    assert d["attempts"] > 0


def test_spearman():
    assert spearman([1,2,3,4],[2,4,6,8]) > .999


def test_mechanism_table_source_aggregate_merge_regression():
    from stitch_mech.mechanism import build_mechanism_table

    o=objects_square()
    e=commuting_edges()

    # Add the same physical/route columns present in the real Pilot-A NODES.
    o["scale_persistence"]=0.5
    o["time_persistence"]=0.5
    o["scale_branching"]=0
    o["time_branching"]=0
    o["scale_merging"]=0
    o["time_merging"]=0
    o["stitch_defect"]=0.0
    o["q_mean"]=0.1

    table=build_mechanism_table(o,e,viscosity=0.000185)
    assert len(table)==len(o)
    assert "scale_out_edge_n" in table.columns
    assert "time_out_edge_n" in table.columns
    assert table["node_id"].is_unique
