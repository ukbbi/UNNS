import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
def run(shard):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "RUN_VERIFY.py"), "--shard", shard], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-1000:]
def test_feeding_basics():
    from swap_classes import feeds, scc_blocks
    assert feeds(2, 3) and feeds(3, 2) and not feeds(2, 5)
    assert [sorted(B) for B in scc_blocks((2, 3, 8))] == [[2, 3, 8]]
    assert len(scc_blocks((2, 3, 10))) == 2
def test_three_label_criterion():
    from swap_classes import three_label_splits
    assert three_label_splits((2, 3, 14)) and not three_label_splits((2, 3, 10))
    assert min(L for *_, L in three_label_splits((2, 3, 14))) == 14
def test_loop_and_void():
    from thresholds import threshold_table
    from route_topology import betti
    def b(c, m):
        rank = {x: i for i, x in enumerate(sorted(c))}
        return tuple(betti(frozenset(tuple(rank[x] for x in w) for w, K in threshold_table(c).items() if m % K == 0), len(c))[0])
    assert b((2, 3, 8, 9), 72) == (1, 1, 0, 0)
    assert b((2, 3, 8, 9, 14), 1008) == (1, 0, 1, 0, 0)
def test_restricted_counts_r2():
    from occurrence_bridge import restricted_counts
    out, _, _ = restricted_counts(72 ** 2, [2])
    assert out["classes_unrestricted"] == 22 and out[(2, "preserve")] == 36 and out[(2, "after")] == 32
def test_shards():
    for s in ("X0", "X1", "X2", "X3", "X4", "X5", "X6", "X7"): run(s)
