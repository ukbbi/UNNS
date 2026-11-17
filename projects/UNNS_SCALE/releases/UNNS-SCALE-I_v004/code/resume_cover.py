"""Resume a covering run: process the pending / extra classes of a raw cover file and merge the result into it."""
import sys, json, time
from multiprocessing import Pool
from cover2 import work, next_split

def resume(rawfile, B, K, max_M, budget, extra=(), cap=300000, procs=2, move_unresolved=False):
    raw = json.load(open(rawfile)); t0 = time.time()
    todo = [tuple(x) for x in raw.get("pending", [])] + [tuple(x) for x in extra]
    if move_unresolved:
        todo += [tuple(x) for x in raw["unresolved"]]; raw["unresolved"] = []
    done, unres = raw["done"], [tuple(x) for x in raw["unresolved"]]
    with Pool(procs) as pool:
        while todo and time.time() - t0 < budget:
            batch, todo = todo[:64], todo[64:]
            for st, M, r, d in pool.map(work, [(B, M, r, K, cap) for M, r in batch]):
                if st == "ok": done.append(d)
                else:
                    p = next_split(M, max_M)
                    if p is None: unres.append((M, r))
                    else: todo += [(M * p, r + M * i) for i in range(p)]
    raw["done"], raw["unresolved"], raw["pending"] = done, unres, todo
    json.dump(raw, open(rawfile, "w"))
    from fractions import Fraction
    print(B, K, "ok", len(done), "unres", len(unres), "pending", len(todo), "covered", float(sum(Fraction(1, d["M"]) for d in done)), flush=True)

if __name__ == "__main__":
    B, K, maxM, bud = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
    resume(f"/tmp/cover_{B}_{K}.json", B, K, maxM, bud)
