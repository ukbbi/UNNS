import sys, json, time
sys.dont_write_bytecode = True
from height import shortest_paths_height
B = int(sys.argv[1]); lo, hi = int(sys.argv[2]), int(sys.argv[3]); out = sys.argv[4]
rows = []; t0 = time.time()
for n in range(lo, hi):
    d, h, path, cnt = shortest_paths_height(B * n, B * (n + 1))
    rows.append({"n": n, "d": d, "hmin": h, "ratio": h / (B * (n + 1)) if h else None, "paths": cnt, "path": path})
    if time.time() - t0 > float(sys.argv[5]): break
json.dump({"B": B, "rows": rows}, open(out, "w"))
print("done", len(rows), "n up to", rows[-1]["n"], round(time.time() - t0))
