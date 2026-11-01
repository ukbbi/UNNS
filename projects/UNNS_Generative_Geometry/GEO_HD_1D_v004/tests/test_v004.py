import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
def run(shard):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "RUN_VERIFY.py"), "--shard", shard], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-1000:]
def test_kernel():
    from integer_kernel import kernel_of_alphabet
    assert len(kernel_of_alphabet((1, 2, 3))) == 1
def test_merger():
    from fractions import Fraction as F
    assert F(4) ** 7 == F(9, 2) ** 2 * F(16, 3) ** 4
def test_rewrite_threshold():
    from block_rewrites import rewrite_threshold
    assert rewrite_threshold((1,) * 7, (2, 2, 3, 3, 3, 3)) == 4
def test_dichotomy_shard(): run("Y4")
def test_shards():
    for s in ("Y0", "Y1", "Y2", "Y3", "Y5", "Y6", "Y7"): run(s)
