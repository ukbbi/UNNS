"""E21 -- CRT construction of gate-1 / gate-3 counterexamples.
Per prime p, v_p(D(I)) = max(0, w_p(I)) with w_p(I)=sum_{j in I}(v_p(l_j) - 2 v_p(l_j+1)); A(m) is the intersection over p of {I : w_p(I) <= v_p(m)}.
Step 1: enumerate achievable single-prime masks. Step 2: for each of the 4 minimal bounding families pick a prime whose mask keeps the gate open
but excludes a member of the family. Step 3: realise the weight vectors by CRT, re-evaluate exactly. Run:  python3 E21_construct_counterexamples.py [--write]"""
import itertools, json, os, random, sys
from math import lcm
import _path
import filling as F, hole_survival as H, block_factor as bf
EX = F.EXTRA; PZ = sorted(H.PZ); bit = {s: i for i, s in enumerate(EX)}
mins = [sum(1 << bit[s] for s in f) for f in json.load(open(os.path.join(_path.ROOT, "RESULTS", "E19_bounding_lattice.json")))["minimal_bounding_families"]]
def sw(w, I): return sum(w[j] for j in range(6) if I >> j & 1)
ach = {}
for w in itertools.product([0, 1, 2, 3, 4, -2, -4], repeat=6):
    sums = {I: sw(w, I) for I in PZ + EX}
    mx = max(0, max(sums[I] for I in PZ))
    for t in range(mx, mx + 8):
        mk = sum(1 << bit[I] for I in EX if sums[I] <= t)
        ach.setdefault(mk, (w, t))
print("achievable single-prime masks:", len(ach))
gates = {1: [34, 38], 3: [8, 24, 40, 56]}
PR = [3, 5, 7, 11]
def crt(mods, res):
    x, M = 0, 1
    for m, r in zip(mods, res):
        x += M * (((r - x) * pow(M, -1, m)) % m); M *= m
    return x % M, M
def build(ws):
    mods = []; res = [[] for _ in range(6)]
    for p, w in zip(PR, ws):
        mods.append(p ** (max(abs(x) // 2 if x < 0 else x for x in w) + 1))
        for j, x in enumerate(w):
            res[j].append(p ** x if x > 0 else (p ** (-x // 2) - 1 if x < 0 else 1))
    M = 1
    for m in mods: M *= m
    out, last = [], 1
    for r in res:
        v = crt(mods, r)[0]
        while v <= last: v += M
        out.append(v); last = v
    return out
def test(labels, gate):
    D = bf.denominators(labels)
    m = lcm(*[D[j] for j in PZ + gate])
    A = sum(1 << bit[I] for I in EX if m % D[I] == 0)
    return m, F.bounds(A)
if __name__ == "__main__":
    for a, gate in gates.items():
        gm = sum(1 << bit[s] for s in gate)
        cand = [mk for mk in ach if mk & gm == gm]
        print("gate", a, "families excludable with the gate open:", [any(mk & f != f for mk in cand) for f in mins])
        ch = [[mk for mk in cand if mk & f != f] for f in mins]
        random.seed(7); best = None
        for _ in range(300):
            ws = [ach[random.choice(c)][0] for c in ch]
            labels = build(ws)
            if len(set(labels)) < 6 or (best and max(labels) >= best[0]): continue
            m, b = test(labels, gate)
            if not b: best = (max(labels), labels, m, ws)
        print(" smallest found (max label %d):" % best[0], best[1])
        if "--write" in sys.argv:
            json.dump({"gate": a, "labels": best[1], "m": best[2], "ws": best[3], "primes": PR}, open(os.path.join(_path.ROOT, "CERTIFICATES", "gate%d_counterexample.json" % a), "w"), indent=1)
