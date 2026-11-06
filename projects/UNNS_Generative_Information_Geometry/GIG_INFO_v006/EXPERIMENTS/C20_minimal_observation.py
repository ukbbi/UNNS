"""C20 -- how little of the forbidden-history data suffices?  Over ALL 346,859 census regimes: dead set D_A (62-bit pattern), exact H1 of N[D_A] via strong-collapse core, and cheap nerve statistics.
Writes RESULTS/C20_dead_patterns.npz (one row per distinct dead-set pattern) -- no sampling."""
import itertools, os, sys, time
import numpy as np
from multiprocessing import Pool
import _path, v2, nerve

SUBS = nerve.SUBS; POS = {s: i for i, s in enumerate(SUBS)}
def fm(S): return any(all(x in nerve.COMP[z] for x in S) for z in SUBS)
PAIR = np.array([(a, b) for a, b in itertools.combinations(range(62), 2)])
PEDGE = np.array([(SUBS[a] ^ SUBS[b]) != 63 for a, b in PAIR])
TRI = np.array(list(itertools.combinations(range(62), 3)))
TFACE = np.array([fm([SUBS[a], SUBS[b], SUBS[c]]) for a, b, c in TRI])
TPE = PEDGE  # reuse
_pid = {(a, b): i for i, (a, b) in enumerate(PAIR)}
TALLE = np.array([PEDGE[_pid[(a, b)]] and PEDGE[_pid[(a, c)]] and PEDGE[_pid[(b, c)]] for a, b, c in TRI])

def work(code):
    D = frozenset(SUBS[i] for i in range(62) if code >> i & 1)
    sel = np.zeros(62, bool)
    for i in range(62):
        if code >> i & 1: sel[i] = True
    V = int(sel.sum()); pe = sel[PAIR[:, 0]] & sel[PAIR[:, 1]]
    E = int((pe & PEDGE).sum()); comp = int((pe & ~PEDGE).sum())
    ts = sel[TRI[:, 0]] & sel[TRI[:, 1]] & sel[TRI[:, 2]]
    Tr = int((ts & TFACE).sum()); Hol = int((ts & TALLE & ~TFACE).sum())
    v, f = nerve.strong_core(D)
    b = nerve.complex_betti_from_facets(v, f)
    return (code, V, E, comp, Tr, Hol, len(v), b[0], b[1])

if __name__ == "__main__":
    t0 = time.time()
    R = v2.census.enumerate_regimes(); mult = {}
    for r in R:
        if r[3] == (1 << 720) - 1: continue
        D = nerve.dead_sets(r[3]); code = sum(1 << POS[s] for s in D)
        mult[code] = mult.get(code, 0) + 1
    codes = [c for c in mult if c]       # empty D <=> full mask only (excluded)
    print("patterns", len(codes), "zero-pattern regimes", mult.get(0, 0), round(time.time() - t0), flush=True)
    with Pool(2) as p:
        rows = []
        for k, r in enumerate(p.imap(work, codes, chunksize=200)):
            rows.append(r)
            if k % 20000 == 0: print(k, round(time.time() - t0), flush=True)
    A = np.array(rows, dtype=np.int64)
    # codes up to 2^62 fit in int64
    np.savez_compressed(os.path.join(_path.ROOT, "RESULTS", "C20_dead_patterns.npz"), code=A[:, 0], V=A[:, 1], E=A[:, 2], comp=A[:, 3], Tr=A[:, 4], Hol=A[:, 5], core=A[:, 6], b0=A[:, 7], b1=A[:, 8], mult=np.array([mult[int(c)] for c in A[:, 0]]))
    print("done", round(time.time() - t0), "positive patterns", int((A[:, 8] > 0).sum()), flush=True)
