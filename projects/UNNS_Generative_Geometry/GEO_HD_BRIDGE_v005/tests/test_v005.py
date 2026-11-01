import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(ROOT, 'src')); sys.dont_write_bytecode = True
import verify_v005 as V

def _shard(name):
    V.RESULTS.clear(); V.FAILS.clear(); V.SHARDS[name](False)
    assert not V.FAILS, V.FAILS

def test_z0_pins(): _shard('Z0')
def test_z1_sieve(): _shard('Z1')
def test_z2_first_event(): _shard('Z2')
def test_z3_divisor_complex(): _shard('Z3')
def test_z4_transitions(): _shard('Z4')
def test_z5_graph_predictor(): _shard('Z5')
def test_z7_towers(): _shard('Z7')
def test_z8_v004_events(): _shard('Z8')
def test_z9_counterexamples(): _shard('Z9')
def test_z6_reachability(): _shard('Z6')
