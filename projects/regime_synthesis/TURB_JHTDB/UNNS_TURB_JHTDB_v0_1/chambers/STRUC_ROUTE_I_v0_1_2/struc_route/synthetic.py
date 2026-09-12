from __future__ import annotations
from pathlib import Path
import json
import pandas as pd

def _node(node_id, t, s, weight=1.0, family=None):
    return {
        "node_id": node_id,
        "time_idx": t,
        "time_value": float(t),
        "scale_idx": s,
        "scale_value": float(s),
        "object_id": node_id,
        "size": weight,
        "weight": weight,
        "cx": float(s),
        "cy": float(t),
        "cz": 0.0,
        "family_id": family,
    }

def perfect_chain():
    # 3x3 commuting lattice, one object in every cell.
    objects = []
    edges = []
    for t in range(3):
        for s in range(3):
            nid = f"n_s{s}_t{t}"
            objects.append(_node(nid, t, s, 1.0, "A"))
    for t in range(3):
        for s in range(2):
            edges.append({"src_id":f"n_s{s}_t{t}","dst_id":f"n_s{s+1}_t{t}","axis":"scale","confidence":1.0})
    for s in range(3):
        for t in range(2):
            edges.append({"src_id":f"n_s{s}_t{t}","dst_id":f"n_s{s}_t{t+1}","axis":"time","confidence":1.0})
    return pd.DataFrame(objects), pd.DataFrame(edges)

def binary_branch():
    # Scale branching repeated through time with consistent temporal identity.
    objects, edges = [], []
    for t in range(3):
        objects.append(_node(f"r_t{t}", t, 0, 2.0, "R"))
        objects.append(_node(f"a_t{t}", t, 1, 1.0, "A"))
        objects.append(_node(f"b_t{t}", t, 1, 1.0, "B"))
        objects.append(_node(f"a2_t{t}", t, 2, 1.0, "A"))
        objects.append(_node(f"b2_t{t}", t, 2, 1.0, "B"))
        edges += [
            {"src_id":f"r_t{t}","dst_id":f"a_t{t}","axis":"scale","confidence":0.5},
            {"src_id":f"r_t{t}","dst_id":f"b_t{t}","axis":"scale","confidence":0.5},
            {"src_id":f"a_t{t}","dst_id":f"a2_t{t}","axis":"scale","confidence":1.0},
            {"src_id":f"b_t{t}","dst_id":f"b2_t{t}","axis":"scale","confidence":1.0},
        ]
    for base in ("r","a","b","a2","b2"):
        for t in range(2):
            edges.append({"src_id":f"{base}_t{t}","dst_id":f"{base}_t{t+1}","axis":"time","confidence":1.0})
    return pd.DataFrame(objects), pd.DataFrame(edges)

def noncommuting():
    # A designed 2x2 route square where ST and TS lead to different terminal descendants.
    objects = [
        _node("root",0,0,1,"R"),
        _node("sA",0,1,1,"A"), _node("sB",0,1,1,"B"),
        _node("tA",1,0,1,"A"), _node("tB",1,0,1,"B"),
        _node("zA",1,1,1,"A"), _node("zB",1,1,1,"B"),
    ]
    edges = [
        {"src_id":"root","dst_id":"sA","axis":"scale","confidence":0.9},
        {"src_id":"root","dst_id":"sB","axis":"scale","confidence":0.1},
        {"src_id":"root","dst_id":"tA","axis":"time","confidence":0.1},
        {"src_id":"root","dst_id":"tB","axis":"time","confidence":0.9},
        {"src_id":"sA","dst_id":"zA","axis":"time","confidence":1.0},
        {"src_id":"sB","dst_id":"zB","axis":"time","confidence":1.0},
        {"src_id":"tA","dst_id":"zA","axis":"scale","confidence":1.0},
        {"src_id":"tB","dst_id":"zB","axis":"scale","confidence":1.0},
    ]
    return pd.DataFrame(objects), pd.DataFrame(edges)

def default_manifest(name):
    return {
        "project_name": name,
        "run_id": name,
        "domain": "SYNTHETIC_VALIDATION",
        "strict_adjacent": True,
        "relation_rule": {"mode":"all","conditions":[
            {"column":"confidence","op":">=","value":0.0}
        ]},
        "edge_weight_column": "confidence",
        "object_weight_column": "weight",
        "nulls": {"count": 25, "seed": 20260904, "swaps_per_edge": 8},
        "inference": {"alpha": 0.05, "min_nulls": 20}
    }

FIXTURES = {
    "perfect_chain": perfect_chain,
    "binary_branch": binary_branch,
    "noncommuting": noncommuting,
}

def write_fixture(folder: str | Path, name: str):
    if name not in FIXTURES:
        raise KeyError(name)
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    objects, relations = FIXTURES[name]()
    (folder / "manifest.json").write_text(
        json.dumps(default_manifest(name), indent=2) + "\n", encoding="utf-8"
    )
    objects.to_csv(folder / "objects.csv", index=False)
    relations.to_csv(folder / "relations.csv", index=False)
    return folder
