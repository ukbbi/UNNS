import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
def run(shard):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "RUN_VERIFY.py"), "--shard", shard], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-1000:]
def test_six_thresholds():
    from thresholds import threshold_table
    assert sorted(threshold_table((2, 3, 14)).values()) == [14, 14, 21, 21, 28, 28]
def test_connection_thresholds():
    from thresholds import threshold_table, connect_thresholds
    assert connect_thresholds(threshold_table((2, 3, 14)), (14, 3, 2), (2, 3, 14)) == [28, 42]
def test_family_split_rule():
    from thresholds import split_sources
    for N in range(4, 80):
        assert bool(split_sources((2, 3, N))[2]) == (N % 6 in (2, 3) and N >= 8)
def test_shards():
    for s in ("W0", "W1", "W2", "W2b", "W3", "W4", "W5", "W6"): run(s)
