import pandas as pd

from struc_route.nulls import rewire_degree_preserving
from struc_route.synthetic import write_fixture
from struc_route.engine import analyze_project


def test_immobile_null_is_detected(tmp_path):
    p = write_fixture(tmp_path/"p", "perfect_chain")
    r, _ = analyze_project(p, tmp_path/"out")
    q = r["null_quality"]
    assert q["swap_accepted_total"] == 0
    assert "NULL_ENSEMBLE_IMMOBILE" in q["flags"]
    assert r["verdict"]["class"] == "UNDERRESOLVED"


def test_rewire_reports_attempts_and_accepts():
    objects = pd.DataFrame([
        {"node_id":"a","time_idx":0,"time_value":0.0,"scale_idx":0,"scale_value":0.0,"object_id":"a","size":1},
        {"node_id":"b","time_idx":0,"time_value":0.0,"scale_idx":0,"scale_value":0.0,"object_id":"b","size":1},
        {"node_id":"x","time_idx":0,"time_value":0.0,"scale_idx":1,"scale_value":1.0,"object_id":"x","size":1},
        {"node_id":"y","time_idx":0,"time_value":0.0,"scale_idx":1,"scale_value":1.0,"object_id":"y","size":1},
    ])
    edges = pd.DataFrame([
        {"src_id":"a","dst_id":"x","axis":"scale","confidence":1.0},
        {"src_id":"b","dst_id":"y","axis":"scale","confidence":1.0},
    ])
    rew, d = rewire_degree_preserving(objects, edges, seed=1, swaps_per_edge=20)
    assert d["attempts"] > 0
    assert d["accepted"] > 0
    assert d["mobility_fraction"] > 0
    # Accepted swaps prove the proposal kernel is mobile. The final graph may
    # legitimately return to its starting state after later accepted swaps;
    # final-state diversity is diagnosed separately by graph_signature.
    assert d["graph_signature"]
