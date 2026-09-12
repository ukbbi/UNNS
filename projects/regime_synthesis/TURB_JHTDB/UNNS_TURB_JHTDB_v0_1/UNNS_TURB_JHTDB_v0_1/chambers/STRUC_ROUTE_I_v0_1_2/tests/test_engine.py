from pathlib import Path
import math
from struc_route.synthetic import write_fixture
from struc_route.engine import analyze_project

def test_perfect_chain(tmp_path):
    p = write_fixture(tmp_path/"p", "perfect_chain")
    r, out = analyze_project(p, tmp_path/"out")
    assert r["structure"]["scale"]["persistence_max"] == 1.0
    assert r["structure"]["time"]["persistence_max"] == 1.0
    assert r["structure"]["scale"]["branch_fraction_all"] == 0.0
    assert r["structure"]["time"]["branch_fraction_all"] == 0.0
    assert r["structure"]["stitch"]["mean_defect"] == 0.0
    assert (out/"RESULT.json").exists()
    assert (out/"LADDERS.zip").exists()
    assert (out/"NODES.parquet").exists() or (out/"NODES.csv").exists()

def test_binary_branching(tmp_path):
    p = write_fixture(tmp_path/"p", "binary_branch")
    r, _ = analyze_project(p, tmp_path/"out")
    assert r["structure"]["scale"]["branch_fraction_all"] > 0
    assert r["structure"]["scale"]["conservation_mean"] is not None

def test_noncommuting_has_stitch_defect(tmp_path):
    p = write_fixture(tmp_path/"p", "noncommuting")
    r, _ = analyze_project(p, tmp_path/"out")
    d = r["structure"]["stitch"]["mean_defect"]
    assert d is not None
    assert d > 0.4
