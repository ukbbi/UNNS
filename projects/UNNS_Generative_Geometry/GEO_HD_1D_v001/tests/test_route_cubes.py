import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
def run(shard):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "RUN_VERIFY.py"), "--shard", shard], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-1000:]
def test_cube_family_builder():
    from route_complex import route_cube_family, verify_cube, binomial_family
    from select_history import endpoint
    for r in range(1, 7):
        b, pos = route_cube_family(r)
        assert verify_cube(b, pos) and endpoint(*b) == 72 ** r and len(pos) == r
        assert len(binomial_family(r)) > 0
def test_swap_split_minimal():
    from merge_obstructions import split_contents
    assert (14, (2, 3, 14)) in split_contents(5400)
def test_shard_V3(): run("V3")
def test_shard_V4(): run("V4")
def test_shard_V5(): run("V5")
