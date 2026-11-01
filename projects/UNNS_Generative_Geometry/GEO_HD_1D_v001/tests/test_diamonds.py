import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
def run(shard):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "RUN_VERIFY.py"), "--shard", shard], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-1000:]
def test_criterion_pointwise():
    from diamond_criterion import diamond, diamond_direct, m_ordered, ordered_ok_direct
    for m in range(1, 150):
        for A in range(1, 20):
            for B in range(1, 20):
                assert diamond(m, A, B) == diamond_direct(m, A, B)
                assert ordered_ok_direct(m, A, B) == (m % m_ordered(A, B) == 0)
def test_shard_V2(): run("V2")
def test_shard_V7(): run("V7")
