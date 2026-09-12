from pathlib import Path
import json

from struc_route.synthetic import write_fixture
from struc_route.engine import analyze_project


def test_entropy_is_descriptive_only(tmp_path):
    p=write_fixture(tmp_path/"p","perfect_chain")
    r,_=analyze_project(p,tmp_path/"out")
    assert "scale_entropy" not in r["evidence"]["tests"]
    assert "time_entropy" not in r["evidence"]["tests"]
    assert r["evidence"]["descriptive_only"]["scale_entropy"]["role"]=="DESCRIPTIVE_ONLY"


def test_publish_real_before_nulls(tmp_path):
    p=write_fixture(tmp_path/"p","perfect_chain")
    events=[]
    analyze_project(p,tmp_path/"out",publish=lambda x:events.append(x))
    stages=[x["stage"] for x in events]
    assert "REAL_GRAPH_COMPLETE" in stages
    assert "NULL_PROGRESS" in stages
    assert stages.index("REAL_GRAPH_COMPLETE") < stages.index("NULL_PROGRESS")


def test_analysis_filter_scale(tmp_path):
    p=write_fixture(tmp_path/"p","perfect_chain")
    m=json.loads((p/"manifest.json").read_text())
    m["analysis_filter"]={"max_scale_idx":1,"label":"test"}
    (p/"manifest.json").write_text(json.dumps(m))
    r,_=analyze_project(p,tmp_path/"out")
    assert r["input"]["scale_layers"]==2
    assert r["input"]["analysis_filter"]["applied"] is True
