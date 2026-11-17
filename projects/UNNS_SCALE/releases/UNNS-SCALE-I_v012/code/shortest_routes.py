"""v012: independent exact shortest confined routes (Python bidirectional layered BFS in G_C; implementation shares no code with the C++ engines).
route(a,b,C) returns a shortest path (first layer-intersection) with all vertices <= C. usage: python shortest_routes.py out.json n1 n2 ..."""
import sys, os, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hubpath import route
from indep_check import check_path
B = 10**6
if __name__ == "__main__":
    out = {}
    for n in map(int, sys.argv[2:]):
        a, b = B*n, B*(n+1)
        p = route(a, b, b, rmax=6, cap=1500000)
        if p is None: print(n, "not found within radius 6/side & cap"); continue
        assert max(p) == b and check_path(p) == len(p)-1
        out[n] = {"length": len(p)-1, "path": p, "min_vertex": min(p)}
        print(n, len(p)-1, "min vertex", min(p), flush=True)
    json.dump(out, open(sys.argv[1], "w"))
