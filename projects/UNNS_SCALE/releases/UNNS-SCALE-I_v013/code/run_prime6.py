"""v013: composite prime-flip bound at B=10^6 for a deterministic sample of primes p in (10^6, 10^6+60000): every 12th prime."""
import sys, os, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from primeflip import adjacency, bfs_path, bound
from indep_check import check_path
from sympy import primerange
B = 10**6
ps = [p for p in primerange(B + 1, B + 60000)][::12]
adj = adjacency(max(ps) + 3)
out = open(sys.argv[1], "w")
for p in ps:
    p1 = bfs_path(adj, B, 1, p + 2); p2 = bfs_path(adj, p + 1, B, p + 1)
    if p1 is None or p2 is None:
        out.write("%d none %s %s\n" % (p, None if p1 is None else len(p1) - 1, None if p2 is None else len(p2) - 1)); out.flush(); continue
    path = [v * p for v in p1] + [(p + 1) ** 2] + [v * (p + 1) for v in p2[1:]]
    assert max(path) == (p + 1) ** 2 and check_path(path) == len(path) - 1
    out.write("%d %d %d %d\n" % (p, len(path) - 1, len(p1) - 1, len(p2) - 1)); out.flush()
