"""v009: minimal excursion height over ALL simple routes of length <= 4 (not only shortest ones)."""
import sys, os, json, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import factor
from height import nbrs
def walks(s, fs):
    W = [{s: [[s]]}]; F = {s: fs}
    for k in range(2):
        nxt = {}
        for v, ps in W[-1].items():
            for l, w, fw in nbrs(v, F[v]):
                F[w] = fw
                for p in ps:
                    if w not in p: nxt.setdefault(w, []).append(p + [w])
        W.append(nxt)
    return W
def h_le4(x, y):
    Wx = walks(x, factor(x)); Wy = walks(y, factor(y)); best = {}
    for t in range(1, 5):
        a = (t + 1) // 2; b = t - a
        for z, pa in Wx[a].items():
            if z in Wy[b]:
                for p1 in pa:
                    for p2 in Wy[b][z]:
                        path = p1 + p2[::-1][1:]
                        if len(set(path)) == len(path):
                            h = max(path)
                            if t not in best or h < best[t][0]: best[t] = (h, path)
    return best     # length -> (min height, path)
if __name__ == "__main__":
    B = int(sys.argv[1]); lo, hi = int(sys.argv[2]), int(sys.argv[3]); out = sys.argv[4]; rows = []; t0 = time.time()
    for n in range(lo, hi):
        b = h_le4(B * n, B * (n + 1)); allh = min(v[0] for v in b.values()); tb = [t for t, v in b.items() if v[0] == allh][0]
        rows.append({"n": n, "by_length": {str(t): [v[0], v[1]] for t, v in b.items()}, "hmin_le4": allh, "path": b[tb][1]})
        if time.time() - t0 > float(sys.argv[5]): break
    json.dump({"B": B, "rows": rows}, open(out, "w")); print("done", len(rows), rows[-1]["n"], round(time.time() - t0))
