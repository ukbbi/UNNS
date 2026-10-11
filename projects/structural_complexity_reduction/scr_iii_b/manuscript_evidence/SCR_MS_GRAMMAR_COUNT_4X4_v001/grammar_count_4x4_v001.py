#!/usr/bin/env python3
"""SCR manuscript-completion record: exact ice-rule grammar count |S_G(L)| for L = 1..4.

Read-only with respect to every frozen file. Uses only the frozen vertex table (mask, plusIn) and the frozen geometry module.
No Hamiltonian, no coupling, no energy is read or computed. Pure standard library.

Convention (frozen; same as solver_v010 / SCR_IV_Grammar.lean): vertex = (mask, plusIn); island i incident iff mask bit i;
island i points INTO the vertex iff (s_i = +1) == (plusIn bit i); vertex satisfied iff exactly 2 incident islands point in.
State id: bit i = 1 <-> s_i = +1.

Usage:  python3 grammar_count_4x4_v001.py [path/to/scr_iii_b]   (default: parent directory of this record's folder)
Method A  variable-elimination DP over the frozen real_4x4.txt vertex table (also public_1.txt, public_2.txt).
Method B  pruned depth-first enumeration of all solutions over the same table (checks witnesses).
Method C  vertex table rebuilt from geometry (physical_energy_v005.source_geometry / incident_islands) for L=1..4, counted with Method A,
          compared with the file table, and spot-checked against ice_ok_geometric.
"""
import sys, os, json, hashlib, random
from collections import defaultdict

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
G = os.path.join(ROOT, "GAP4_v010")
sys.path.insert(0, G)

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def load(path):
    L = open(path).read().split("\n")
    n, nv = map(int, L[0].split())
    nc = n * (n - 1) // 2
    rest = [l for l in L[1:] if l.strip() != ""]
    assert len(rest) == nc + nv, (len(rest), nc, nv)
    return n, [tuple(map(int, l.split())) for l in rest[nc:]]      # coupling lines are skipped, never parsed

def idxs(m, n): return [i for i in range(n) if m >> i & 1]

def count_dp(n, vs):
    hi = [max(idxs(m, n)) for m, _ in vs]
    last = [-1] * n
    for (m, _), h in zip(vs, hi):
        for i in idxs(m, n): last[i] = max(last[i], h)
    tab = {(): 1}; act = []
    for d in range(n):
        new = defaultdict(int)
        for a, c in tab.items():
            for v in (1, -1):
                full = dict(zip(act, a)); full[d] = v
                if all(sum(1 for i in idxs(m, n) if (full[i] > 0) == bool(p >> i & 1)) == 2
                       for (m, p), h in zip(vs, hi) if h == d):
                    new[tuple(sorted(full.items()))] += c
        keep = [i for i in sorted(set(act) | {d}) if last[i] > d]
        tab = defaultdict(int)
        for fa, c in new.items():
            f = dict(fa); tab[tuple(f[i] for i in keep)] += c
        act = keep
    return sum(tab.values())

def enumerate_bt(n, vs):
    byhi = [[] for _ in range(n)]
    for m, p in vs: byhi[max(idxs(m, n))].append((m, p))
    sols = []; nodes = [0]
    def rec(d, bits):
        nodes[0] += 1
        if d == n: sols.append(bits); return
        for b in (0, 1):
            x = bits | (b << d)
            if all(bin(~(x ^ p) & m).count("1") == 2 for m, p in byhi[d]): rec(d + 1, x)
    rec(0, 0); return sols, nodes[0]

def main():
    import physical_energy_v005 as P
    out = {"record": "SCR_MS_GRAMMAR_COUNT_4X4_v001", "inputs": {}, "counts": {}, "checks": {}}
    real = os.path.join(G, "output", "real_4x4.txt")
    out["inputs"]["real_4x4.txt sha256"] = sha(real)
    out["inputs"]["INSTANCE_SHA256.txt"] = open(os.path.join(G, "output", "INSTANCE_SHA256.txt")).read().split()[0]
    out["inputs"]["physical_energy_v005.py sha256"] = sha(os.path.join(G, "physical_energy_v005.py"))
    out["checks"]["instance hash matches frozen record"] = out["inputs"]["real_4x4.txt sha256"] == out["inputs"]["INSTANCE_SHA256.txt"]
    for name in ("public_1.txt", "public_2.txt"):
        n, vs = load(os.path.join(G, name)); out["counts"][f"A: {name} (n={n})"] = count_dp(n, vs)
    n, fvs = load(real)
    cA = count_dp(n, fvs); out["counts"]["A: real_4x4.txt DP"] = cA
    sols, nodes = enumerate_bt(n, fvs)
    out["counts"]["B: real_4x4.txt pruned enumeration"] = len(sols); out["checks"]["B nodes visited"] = nodes
    S = set(sols)
    for nm, i in (("ground witness 711243241830", 711243241830), ("true excluded minimum 711243241766", 711243241766),
                  ("frozen excluded value 161487427942", 161487427942)):
        out["checks"][f"in grammar: {nm}"] = i in S
    out["checks"]["witness convention"] = "ground in S_G; both excluded-state ids not in S_G (as recorded)"
    geo = {}
    for L in (1, 2, 3, 4):
        isl = P.source_geometry(L); vp = P.vertex_positions(L); inc = P.incident_islands(isl, vp)
        vs = []
        for v, idx in zip(vp, inc):
            assert len(idx) == 4
            m = p = 0
            for i in idx:
                q = isl[i]; m |= 1 << i
                if (v[0] - q.x) * q.ux + (v[1] - q.y) * q.uy > 0: p |= 1 << i
            vs.append((m, p))
        nn = len(isl); geo[L] = (nn, vs)
        out["counts"][f"C: geometry L={L} (n={nn}) DP"] = count_dp(nn, vs)
    out["checks"]["geometry vertex table == file vertex table (L=4, same order)"] = (geo[4][1] == fvs)
    isl = P.source_geometry(4); vp = P.vertex_positions(4)
    ok = lambda x: all(bin(~(x ^ p) & m).count("1") == 2 for m, p in fvs)
    random.seed(1); agree = tot = 0
    probe = [random.getrandbits(40) for _ in range(100000)] + [711243241830 ^ (1 << i) for i in range(40)]
    for x in probe:
        agree += (P.ice_ok_geometric(P.decode(x, 40), isl, vp) == ok(x)); tot += 1
    out["checks"]["geometric ice rule vs vertex-table rule on 100,040 probe states (agree/total)"] = [agree, tot]
    N = 2 ** 40
    out["result"] = {"|S_G(4)|": cA, "nominal": N, "contraction": 1 - cA / N, "one_in": N / cA, "excluded": N - cA}
    assert cA == len(sols) == out["counts"]["C: geometry L=4 (n=40) DP"]
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "grammar_count_4x4_v001_output.json"), "w"), indent=2)
    print(json.dumps(out, indent=2))

main()
