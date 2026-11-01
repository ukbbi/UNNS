import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
def run(shard):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "RUN_VERIFY.py"), "--shard", shard], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-1000:]
def test_benchmark_signatures():
    from history_events import rho, birth_loss
    assert rho((1, (1, 1, 2)), 2) == (0, 1, 1, 1) and rho((1, (1, 2, 1)), 2) == (0, 1, 0, 1)
    ev = birth_loss((1, (1, 1, 2)))[-1]
    assert ev["births"] == [3, 6] and ev["losses"] == [4]
def test_shard_V6(): run("V6")
def test_shard_V8(): run("V8")
