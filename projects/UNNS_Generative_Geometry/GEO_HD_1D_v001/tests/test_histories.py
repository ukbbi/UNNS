import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
def run(shard):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "RUN_VERIFY.py"), "--shard", shard], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-1000:]
def test_complete_histories_of_72():
    from select_history import complete_histories
    assert sorted(complete_histories(72)) == [(1, (1, 1, 2)), (1, (1, 2, 1)), (3, (3, 2)), (10, (5,))]
def test_recurrence_values():
    from predecessor_count import H
    assert [H(72 ** r) for r in (1, 2, 3, 4)] == [4, 100, 3601, 194864]
def test_shard_V0(): run("V0")
def test_shard_V1(): run("V1")
def test_shard_V9(): run("V9")
