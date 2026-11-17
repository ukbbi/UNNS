"""v009: excursion geometry.  For x=Bn, y=B(n+1): d=d(x,y)<=4. Enumerate ALL shortest paths (via radius-2 balls) and compute
  h_min(n) = min over shortest paths of max vertex  (minimal excursion height),  ratio = h_min/max(x,y).
A path is 'inside' if max vertex <= B*(n+1) (= max endpoint); excursion ratio rho(n)=h_min/(B(n+1))."""
import sys, os, itertools
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import factor
from b2_types import moves
def nbrs(x, fx):
    return [(l, y, fy) for l, _, y, fy in moves(x, fx)]
def shortest_paths_height(x, y, maxd=4):
    """returns (d, h_min, a path attaining h_min, n_paths_len_d) ; d = exact distance if <=4 else None"""
    fx, fy = factor(x), factor(y)
    # layers up to radius 2 from each side (as dict vertex-> list of parents)
    def layers(s, fs, R):
        L = [{s: [None]}]; F = {s: fs}; seen = {s}
        for r in range(R):
            nxt = {}
            for v in L[-1]:
                for l, w, fw in nbrs(v, F[v]):
                    if w in seen and w not in nxt: continue
                    nxt.setdefault(w, []).append(v); F[w] = fw
            seen |= set(nxt); L.append(nxt)
        return L
    # BFS exactness: use first meeting radius pair
    Lx = layers(x, fx, 2); Ly = layers(y, fy, 2)
    for d in range(1, maxd + 1):
        a = (d + 1) // 2; b = d - a
        best = None; cnt = 0
        for z in Lx[a]:
            if z in Ly[b]:
                # reconstruct all paths x..z (len a) and y..z (len b), minimise max
                px = paths_to(Lx, a, z); py = paths_to(Ly, b, z)
                for p1 in px:
                    for p2 in py:
                        path = p1 + p2[::-1][1:]
                        cnt += 1; h = max(path)
                        if best is None or h < best[0]: best = (h, path)
        if best: return d, best[0], best[1], cnt
    return None, None, None, 0
def paths_to(L, k, z):
    if k == 0: return [[z]]
    out = []
    for p in L[k][z]:
        for q in paths_to(L, k - 1, p): out.append(q + [z])
    return out
if __name__ == "__main__":
    B = int(sys.argv[1]); lo, hi = int(sys.argv[2]), int(sys.argv[3])
    import json
    rows = []
    for n in range(lo, hi):
        d, h, path, cnt = shortest_paths_height(B * n, B * (n + 1))
        rows.append((n, d, h / (B * (n + 1)) if h else None, cnt))
        if n % 50 == 0: print(n, d, round(rows[-1][2], 3), cnt, flush=True)
