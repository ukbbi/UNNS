import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
def run(shard):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "RUN_VERIFY.py"), "--shard", shard], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-1000:]
def test_active_primes():
    from prime_geometry import active_primes, passive_primes
    assert active_primes((2, 3, 8, 9)) == [2, 3] and passive_primes((2, 3, 8, 9)) == [5]
def test_irreducible_loop():
    from dimension_tests import Content
    c = Content((2, 3, 4, 5, 6, 7)); assert tuple(c.betti_at((3, 1, 0, 0))) == (1, 1, 0, 0, 0, 0)
def test_field_map():
    from field_adapter import strand
    from fractions import Fraction
    assert strand(4, 3) == [Fraction(4), Fraction(8), Fraction(12), Fraction(16)]
def test_churn():
    from occurrence_events import history_churn
    assert history_churn(2, 4, (1,) * 7) == 0 and history_churn(2, 4, (2, 2, 3, 3, 3, 3)) == 1
def test_shards():
    for s in ("Z0", "Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7"): run(s)
