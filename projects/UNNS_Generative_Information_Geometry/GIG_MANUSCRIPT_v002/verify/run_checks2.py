#!/usr/bin/env python3
"""Second batch of independent checks (anchor certificate, gates, thresholds, 6-cycles, 72^r to r=10, count laws).
Reads inherited certificates from verify/inherited/ (copies of frozen files; sha256 recorded in MANIFEST)."""
import json, os, sys, random, math
from fractions import Fraction
from itertools import permutations, combinations
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gigmini import *
OUT = {}
def rec(name, **kw): OUT[name] = kw; print(name, json.dumps(kw, default=str)[:260])
INH = os.path.join(HERE, "inherited")
def tomask(b): return sum(1 << x for x in b)
def face_from(lst): return tuple(tomask(b) for b in lst)

# ---- anchor certificate (z, phi) in rank coordinates ----
cert = json.load(open(os.path.join(INH, "pattern_H2.json")))
z = {face_from(f) for f in cert["z_faces"]}
phi = {face_from(f) for f in cert["phi_faces"]}
def bd_chain(S):
    out = set()
    for F in S:
        for G in face_boundary(F): out ^= {G}
    return out
rec("ch6_certificate_basic", z_weight=len(z), z_is_cycle=(len(bd_chain(z)) == 0), phi_weight=len(phi),
    phi_of_z=len(phi & z) % 2, z_types={"square": sum(1 for F in z if max(bin(B).count("1") for B in F) == 2), "hexagon": sum(1 for F in z if max(bin(B).count("1") for B in F) == 3)},
    z_vertices=len({v for F in z for v in face_vertices(F)}))
# PS-0: phi(dF) over all 3-faces of P_6
P6 = ordered_partitions(6)
three = [F for F in P6 if 6 - len(F) == 3]
odd = [F for F in three if len(phi & set(face_boundary(F))) % 2 == 1]
rec("ch6_PS0_540_faces", n3faces=len(three), odd=[[[i for i in range(6) if B >> i & 1] for B in F] for F in odd], n_odd=len(odd))
# prefix sets, gates
Pz = set()
for F in z: Pz |= prefsets_of_face(F)
rec("ch6_Pz", n_prefix_sets=len(Pz))
gates = {}
for F in odd:
    first = [i for i in range(6) if F[0] >> i & 1]
    a = [i for i in first if i in (0, 1, 3)][0]
    gates.setdefault(a, set()).update(prefsets_of_face(F) - Pz)
rec("ch6_gates", gates={a: sorted("".join(str(i) for i in range(6) if I >> i & 1) for I in S) for a, S in gates.items()})
# thresholds for the two anchors
def Kset(lab, S):
    L = 1
    for I in S: L = lcm(L, Dmask(lab, I))
    return L
thr = {}
for nm, lab in (("A", (2, 3, 4, 5, 8, 9)), ("B", (2, 3, 6, 7, 8, 9))):
    thr[nm] = {"K_z": Kset(lab, Pz), "octahedra": [Kset(lab, prefsets_of_face(F)) for F in odd]}
rec("ch6_thresholds", **thr)
# the exact arithmetic predicate on the anchors, verified for sources up to 20000 by direct complex homology would be heavy;
# here: certificate check at selected sources (phi kills all 3-faces present; phi(z)=1)
def present_faces(lab, m):
    k = 6; fam = {I for I in range(1, 64) if m % Dmask(lab, I) == 0}
    return complex_from_prefix_family(k, fam), fam
for nm, lab, m0 in (("A", (2, 3, 4, 5, 8, 9), 288), ("B", (2, 3, 6, 7, 8, 9), 432)):
    res = {}
    for t in (1, 7, 11, 2, 3, 5, 6, 10):
        m = m0 * t
        faces, fam = present_faces(lab, m)
        fs = set(faces)
        zin = z <= fs
        okphi = all(len(phi & set(face_boundary(F))) % 2 == 0 for F in faces if 6 - len(F) == 3)
        res[t] = {"z_present": zin, "phi_kills_present_3faces": okphi, "certifies_hole": zin and okphi}
    rec("ch6_certificate_at_sources_" + nm, **{str(k): v for k, v in res.items()})
# gate 0 universal filling: solve z = d(c) using faces F with Pref(F) <= Pz u Pref(T0)
T0 = [F for F in odd if (F[0] >> 0 & 1)][0]
W0set = Pz | prefsets_of_face(T0)
W0 = [F for F in three if prefsets_of_face(F) <= W0set]
def solve_filling(cands, target):
    idx = {}
    rows = []
    # build columns = 2-faces
    cols = {}
    for F in cands:
        for G in face_boundary(F): cols.setdefault(G, len(cols))
    for G in target: cols.setdefault(G, len(cols))
    vecs = []
    for F in cands:
        v = 0
        for G in face_boundary(F): v ^= 1 << cols[G]
        vecs.append(v)
    t = 0
    for G in target: t ^= 1 << cols[G]
    # gaussian elimination with combination tracking
    piv = {}
    for i, v in enumerate(vecs):
        c = 1 << i
        while v:
            h = v.bit_length() - 1
            if h in piv: pv, pc = piv[h]; v ^= pv; c ^= pc
            else: piv[h] = (v, c); break
    c = 0
    while t:
        h = t.bit_length() - 1
        if h not in piv: return None
        pv, pc = piv[h]; t ^= pv; c ^= pc
    return [cands[i] for i in range(len(cands)) if c >> i & 1]
fill0 = solve_filling(W0, z)
rec("ch6_gate0_filling", candidate_3faces=len(W0), filling_size=None if fill0 is None else len(fill0),
    verified=(fill0 is not None and bd_chain(set(fill0)) == z))
# minimal filling families B0..B3 of the anchor cycle: test bounding with P_z u S
EXTRA = [8, 9, 10, 11, 21, 24, 25, 26, 27, 34, 38, 40, 41, 42, 43, 46, 56, 57, 58, 59, 40]
EXTRA = sorted(set(EXTRA))
def bounds(S):
    fam = Pz | set(S)
    cands = [F for F in three if prefsets_of_face(F) <= fam]
    return solve_filling(cands, z) is not None
B = {"B0": [21], "B1": [34, 38, 46], "B2": [8, 9, 10, 11, 24, 25, 26, 27, 40, 41, 43, 56, 57, 58, 59], "B3": [8, 9, 10, 11, 24, 26, 27, 34, 40, 41, 42, 43, 46, 56, 57, 58, 59]}
Bres = {}
for nm, S in B.items():
    Bres[nm] = {"bounds": bounds(S), "minimal": all(not bounds([x for x in S if x != y]) for y in S), "size": len(S)}
rec("ch6_PS5_minimal_families", **Bres)
# every prefix set of the families must lie outside Pz, within 63 sets
rec("ch6_PS5_disjoint_from_Pz", ok=all(not (set(S) & Pz) for S in B.values()))
# random sample of the 2^20 families: criterion "bounds iff contains some B_i"
rnd = random.Random(1); agree = 0; tot = 400; EX = sorted(set(EXTRA) - Pz)
rec("ch6_PS5_extra_count", n_extra=len(EX))
for _ in range(tot):
    p = rnd.choice([0.3, 0.5, 0.7, 0.85, 0.95])
    S = {x for x in EX if rnd.random() < p}
    pred = any(set(b) <= S for b in B.values())
    agree += (bounds(S) == pred)
rec("ch6_PS5_random_sample", tested=tot, agree=agree)

# ---- 6-cycles in the permutohedron graph: classification for k <= 6 ----
def adj_list(k):
    ps = list(permutations(range(k))); idx = {p: i for i, p in enumerate(ps)}
    nb = []
    for p in ps:
        L = []
        for i in range(k - 1):
            q = p[:i] + (p[i + 1], p[i]) + p[i + 2:]; L.append(idx[q])
        nb.append(L)
    return ps, idx, nb
def six_cycles(k):
    ps, idx, nb = adj_list(k); root = idx[tuple(range(k))]
    nbs = [set(x) for x in nb]
    found = set()
    def dfs(path):
        if len(path) == 6:
            if path[0] in nbs[path[-1]]:
                # canonical form
                cyc = path[:]; m = min(cyc); i = cyc.index(m)
                c1 = tuple(cyc[i:] + cyc[:i]); c2 = tuple([c1[0]] + list(c1[1:][::-1]))
                found.add(min(c1, c2))
            return
        for w in nb[path[-1]]:
            if w not in path: dfs(path + [w])
    dfs([root])
    return ps, idx, nb, nbs, found
def classify(k):
    ps, idx, nb, nbs, cycles = six_cycles(k)
    gen = lambda a, b: [i for i in range(k - 1) if ps[a][:i] + (ps[a][i + 1], ps[a][i]) + ps[a][i + 2:] == ps[b]][0]
    types = {}
    N = len(ps)
    for c in cycles:
        chords = sum(1 for a, b in combinations(range(6), 2) if (b - a) % 6 not in (1, 5) and c[b] in nbs[c[a]])
        # outside vertices adjacent to >=2 cycle vertices
        outside = 0
        cs = set(c)
        cand = set()
        for v in c: cand |= nbs[v]
        for u in cand - cs:
            if len(nbs[u] & cs) >= 2: outside += 1
        gens = [gen(c[i], c[(i + 1) % 6]) for i in range(6)]
        span = len(set(gens))
        key = (chords, outside >= 1, "braid" if (span == 2 and abs(gens[0] - gens[1]) == 1 and gens == [gens[0], gens[1]] * 3 or gens == [gens[1], gens[0]] * 3) else "other")
        types[key] = types.get(key, 0) + 1
    return {str(k_): v for k_, v in types.items()}
for k in (4, 5, 6):
    rec(f"ch5_six_cycles_through_root_k{k}", types=classify(k))

# ---- Petrie vs braid hexagon: isomorphic graphs, different complexes (k=6) ----
def perm_apply(base, swaps):
    p = list(base)
    for i in swaps: p[i], p[i + 1] = p[i + 1], p[i]
    return tuple(p)
base = tuple(range(6))
cube = [perm_apply(base, [i for i, b in zip((0, 2, 4), bits) if b]) for bits in __import__("itertools").product([0, 1], repeat=3)]
cube_bits = {tuple(bits): perm_apply(base, [i for i, b in zip((0, 2, 4), bits) if b]) for bits in __import__("itertools").product([0, 1], repeat=3)}
petrie = {cube_bits[b] for b in cube_bits if b not in ((0, 0, 0), (1, 1, 1))}
hexa = {perm_apply(base, w) for w in ([], [0], [1], [0, 1], [1, 0], [0, 1, 0])}
fP, bP = betti(6, complex_from_vertex_set(6, petrie)); fH, bH = betti(6, complex_from_vertex_set(6, hexa))
rec("ch5_petrie_vs_braid", petrie={"N": len(petrie), "f": fP, "beta": bP}, braid={"N": len(hexa), "f": fH, "beta": bH})
# six-vertex slice of a commuting cube is not realisable by prefix-defined sets (cube-product property), checked on random prefix families
rnd = random.Random(5); viol = 0; tests = 0
cubes = []
for bits in [(0, 2, 4)]: cubes.append(bits)
for _ in range(300):
    fam = {I for I in range(1, 63) if rnd.random() < rnd.choice([0.4, 0.6, 0.8])}
    A = {p for p in permutations(range(6)) if all(I in fam for I in prefix_sets(p))}
    for v in permutations(range(6)):
        pass
    # test all commuting cubes with swap positions (0,2,4) at a few bases
    for _b in range(20):
        bp = list(range(6)); rnd.shuffle(bp); bp = tuple(bp)
        slice_ = [bp for bits in __import__("itertools").product([0, 1], repeat=3)]
        S = [perm_apply(bp, [i for i, b in zip((0, 2, 4), bits) if b]) for bits in __import__("itertools").product([0, 1], repeat=3)]
        cnt = sum(1 for s in S if s in A); tests += 1
        if cnt not in (0, 1, 2, 4, 8): viol += 1
rec("ch5_cube_product_property_prefix_defined", tests=tests, violations=viol)

# ---- 72^r counts up to r = 10 with exponent bookkeeping ----
def fac_small(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def key(fd): return tuple(sorted(fd.items()))
memo = {}
def count_f(fd):
    k = key(fd)
    if k in memo: return memo[k]
    s = 1
    for p, e in fd.items(): s *= p ** (e // 2)
    # divisors of s from exponents
    ds = [(1, {})]
    for p, e in fd.items():
        h = e // 2; new = []
        for d, dd in ds:
            for i in range(h + 1):
                d2 = dict(dd)
                if i: d2[p] = i
                new.append((d * p ** i, d2))
        ds = new
    tot = 0; any_ = False
    for d, dd in ds:
        if d < 2: continue
        any_ = True
        N = d - 1; # predecessor m = N t/(N+1)^2
        g = dict(fd)
        for p, e in dd.items():
            g[p] = g.get(p, 0) - 2 * e
        for p, e in fac_small(N).items(): g[p] = g.get(p, 0) + e
        g = {p: e for p, e in g.items() if e > 0}
        tot += count_f(g)
    memo[k] = tot if any_ else 1
    return memo[k]
reg = [4, 100, 3601, 194864, 14177856, 1258011667, 127958272791, 14628387999697, 1831257259071051, 247547117576968617]
RMAX = 7
got = [count_f({2: 3 * r, 3: 2 * r}) for r in range(1, RMAX + 1)]
rec("ch3_72r_counts_to_7", computed=got, registered=reg[:RMAX], match=got == reg[:RMAX], note="r=8..10 registered in GIG-I v001 (e2_long_table.json) and recorded NOT_RERUN here")

# ---- counting laws N(288 t) and N(432 t) ----
def Ncount(lab, m): return len(admissible_perms(lab, m))
lawA = all(Ncount((2, 3, 4, 5, 8, 9), 288 * t) == 372 + 36 * (t % 2 == 0) + 72 * (t % 3 == 0) + 240 * (t % 5 == 0) for t in range(1, 61))
labB = (2, 3, 6, 7, 8, 9)
addB = [Ncount(labB, 432 * t) == 276 + 36 * (t % 2 == 0) + 48 * (t % 3 == 0) + 336 * (t % 7 == 0) for t in range(1, 61)]
bad = [t for t, ok in zip(range(1, 61), addB) if not ok]
rec("ch4_count_laws", A_additive_all_t=lawA, B_additive_fails_at=bad, B_N_at_21=Ncount(labB, 432 * 21), B_additive_prediction_21=276 + 48 + 336)
json.dump(OUT, open(os.path.join(HERE, "results2.json"), "w"), indent=1, default=str)
print("DONE2")
