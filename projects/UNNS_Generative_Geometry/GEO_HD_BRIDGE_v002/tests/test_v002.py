import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(ROOT, "src")); sys.dont_write_bytecode = True
import geo_snapshots as G, field_regimes as F, event_correspondence as E

def test_closed_form():
    r = G.closed_form(2**4 * 3**2)
    assert r["chi"] == 1 and r["nF"] == (2 + 1) * (1 + 1) - 1

def test_rigid_tower():
    for k in range(1, 6):
        x = 4 ** k
        assert F.direct_orbit(x, 3)[-1] == 4 * x

def test_scaling_obstruction():
    assert [N for N in range(1, 2000) if (N + 1) ** 2 % N == 0] == [1]

def test_shards():
    for s in ("Z0", "Z2", "Z4"):
        assert subprocess.run([sys.executable, os.path.join(ROOT, "RUN_VERIFY.py"), "--shard", s], capture_output=True).returncode == 0
