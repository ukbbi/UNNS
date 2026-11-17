"""Adaptive residue-class covering with prime rotation, multiprocessing, time budget."""
import json, sys, time
from multiprocessing import Pool
from sym_lib import search, certify

PR = (2, 3, 5, 7)

def vp(M, p):
    v = 0
    while M % p == 0: M //= p; v += 1
    return v

def next_split(M, max_M):
    # prime with least valuation in M that still fits
    cands = sorted(PR, key=lambda p: (vp(M, p), p))
    for p in cands:
        if M * p <= max_M: return p
    return None

def work(args):
    B, M, r, K, cap = args
    st, msg = search(B, M, r, K, node_cap=cap)
    if st is not None:
        c = certify(B, M, r, st)
        if c is not None:
            return ("ok", M, r, {"M": M, "r": r, "length": c["length"], "t0": c["t0"],
                                 "steps": [(d, str(N.as_expr())) for d, N in st]})
    return ("no", M, r, None)

def cover(B, K, max_M=2000, cap=200000, budget=150, procs=2, M0=1):
    t0 = time.time()
    todo = [(M0, r) for r in range(M0)]
    done, unresolved = [], []
    with Pool(procs) as pool:
        while todo and time.time() - t0 < budget:
            batch, todo = todo[:64], todo[64:]
            res = pool.map(work, [(B, M, r, K, cap) for M, r in batch])
            for st, M, r, d in res:
                if st == "ok": done.append(d)
                else:
                    p = next_split(M, max_M)
                    if p is None: unresolved.append((M, r))
                    else: todo += [(M * p, r + M * i) for i in range(p)]
    return done, unresolved, todo

def density(done):
    from fractions import Fraction
    return sum(Fraction(1, d["M"]) for d in done)

if __name__ == "__main__":
    B, K, max_M, budget = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
    done, unres, todo = cover(B, K, max_M=max_M, budget=budget)
    dens = density(done)
    print(f"B={B} K={K} maxM={max_M}: ok {len(done)} unresolved {len(unres)} pending {len(todo)} density covered {float(dens):.6f}")
    json.dump({"B": B, "K": K, "done": done, "unresolved": unres, "pending": todo}, open(f"/tmp/cover_{B}_{K}.json", "w"))
