#!/usr/bin/env python3
"""GIG-INFO v006 -- STANDALONE certificate verifier (Python >= 3.8, standard library only; imports nothing from this package).
It re-derives every finite fact used by the two self-contained theorems from definitions:
  [ADJ]   the finite hypotheses of the pairwise-adjacency theorem (k=6): Z_p acyclic in degrees 0,1 for all 30 ordered pairs; Z_pq nonempty & connected for all 435 pairs of pairs; Z_pqr nonempty for all 4060 triples.
  [3ADJ]  the triple-adjacency counterexample: beta_2(K_A)=5 for A = orderings avoiding consecutive (1,2,0) and (5,4,3), computed from the definition of K_A (faces of the permutohedron P_6 all of whose vertices are admissible).
  [NERVE] for each arithmetic certificate (content, source, cycle z, cocycle c): dead sets from the definition, nerve N[D] faces, and the check that c vanishes on every triangle boundary and c(z)=1.
          With --full also beta_2(K_A) from the definition of K_A (slow).
usage:  python standalone_verify.py [--full] [--cert PATH_TO_positives_cycle_cocycle.json]
exit status 0 iff every check passes."""
import itertools, json, os, sys, time

K = 6; FULL = 63
def rank(rows):
    piv = {}; rk = 0
    for r in rows:
        while r:
            h = r.bit_length() - 1
            if h in piv: r ^= piv[h]
            else: piv[h] = r; rk += 1; break
    return rk

# ---------------- ordered partitions as block-index tuples ----------------
OP = [b for m in range(2, K + 1) for b in itertools.product(range(1, m + 1), repeat=K) if len(set(b)) == m]
def cuts(b):
    return tuple(sum(1 << i for i in range(K) if b[i] <= t) for t in range(1, max(b)))
def merged(b, t):                     # merge blocks t and t+1 (delete the cut t)
    return tuple(x if x <= t else x - 1 for x in b)

def check_adj():
    ok = True; rep = {}
    pairs = [(x, y) for x in range(K) for y in range(K) if x != y]
    maskp = {}
    for p in pairs:
        m = 0
        for i, b in enumerate(OP):
            if (b[p[1]] - b[p[0]]) in (0, 1): m |= 1 << i
        maskp[p] = m
    idx = {b: i for i, b in enumerate(OP)}
    # closure under coarsening (simplicial complex property) for every Z_p
    for p, m in maskp.items():
        for i, b in enumerate(OP):
            if m >> i & 1 and max(b) > 2:
                for t in range(1, max(b)):
                    if not (m >> idx[merged(b, t)] & 1): ok = False
    # (a) single pieces: reduced b0, b1 = 0
    bad_single = 0
    for p, m in maskp.items():
        S = [OP[i] for i in range(len(OP)) if m >> i & 1]
        V = sorted({cuts(b)[0] for b in S if max(b) == 2}); E = [b for b in S if max(b) == 3]; Tg = [b for b in S if max(b) == 4]
        vid = {v: i for i, v in enumerate(V)}
        eid = {b: i for i, b in enumerate(E)}
        r1 = rank([(1 << vid[cuts(b)[0]]) ^ (1 << vid[cuts(b)[1]]) for b in E])
        r2 = rank([sum(1 << eid[merged(b, t)] for t in (1, 2, 3)) for b in Tg])      # d(triangle) = 3 merged faces (each a 3-block partition = an edge)
        b0 = len(V) - r1 - 1; b1 = len(E) - r1 - r2
        if b0 or b1: bad_single += 1
    rep["single_pieces_nonacyclic"] = bad_single
    # (b) pairs of pairs: nonempty and connected
    bad_pair = 0; npairs = 0
    for p, q in itertools.combinations(pairs, 2):
        npairs += 1
        m = maskp[p] & maskp[q]
        S = [OP[i] for i in range(len(OP)) if m >> i & 1]
        if not S: bad_pair += 1; continue
        par = {}
        def f(x):
            while par.setdefault(x, x) != x: par[x] = par[par[x]]; x = par[x]
            return x
        for b in S:
            if max(b) == 2: f(cuts(b)[0])
            if max(b) == 3:
                a, c = cuts(b); par[f(a)] = f(c)
        if len({f(x) for x in list(par)}) != 1: bad_pair += 1
    rep["pairs_checked"] = npairs; rep["pairs_empty_or_disconnected"] = bad_pair
    bad_tr = 0; ntr = 0
    for p, q, r in itertools.combinations(pairs, 3):
        ntr += 1
        if not (maskp[p] & maskp[q] & maskp[r]): bad_tr += 1
    rep["triples_checked"] = ntr; rep["triples_empty"] = bad_tr
    ok = ok and bad_single == 0 and bad_pair == 0 and bad_tr == 0 and npairs == 435 and ntr == 4060
    return ok, rep

# ---------------- K_A from the definition, beta_2 ----------------
def all_ordered_partitions(k):
    res = []
    def rec(rem, acc):
        if not rem: res.append(tuple(acc)); return
        rem = list(rem)
        for r in range(1, len(rem) + 1):
            for blk in itertools.combinations(rem, r):
                rec([x for x in rem if x not in blk], acc + [blk])
    rec(list(range(k)), [])
    return res
OPS = all_ordered_partitions(K)
def vertices(face):
    for choice in itertools.product(*[itertools.permutations(b) for b in face]):
        yield tuple(x for blk in choice for x in blk)
def boundary(face):
    out = []
    for i, blk in enumerate(face):
        if len(blk) < 2: continue
        for r in range(1, len(blk)):
            for first in itertools.combinations(blk, r):
                rest = tuple(x for x in blk if x not in first)
                out.append(face[:i] + (first, rest) + face[i + 1:])
    return out
def canon(face): return tuple(tuple(sorted(b)) for b in face)
def beta2_of(A):
    A = set(A); by = {}
    for f in OPS:
        f = canon(f)
        if len(f) in (3, 4, 5) and all(v in A for v in vertices(f)):
            by.setdefault(len(f), set()).add(f)
    # note: set removes duplicates caused by canon
    f2, f3, f1 = sorted(by.get(4, ())), sorted(by.get(3, ())), sorted(by.get(5, ()))
    i1 = {f: i for i, f in enumerate(f1)}; i2 = {f: i for i, f in enumerate(f2)}
    def rows(src, tgt_idx):
        out = []
        for f in src:
            r = 0
            for g in boundary(f): r ^= 1 << tgt_idx[canon(g)]
            out.append(r)
        return out
    return len(f2) - rank(rows(f2, i1)) - rank(rows(f3, i2))
PERMS = list(itertools.permutations(range(K)))
def arithmetic_A(content, m0):
    labs = sorted(content); A = []
    for p in PERMS:
        m, ok = m0, True
        for r in p:
            if m % labs[r]: ok = False; break
            m = m // labs[r] * (labs[r] + 1) ** 2
        if ok: A.append(p)
    return A

def check_3adj():
    bad = {(1, 2, 0), (5, 4, 3)}
    A = [p for p in PERMS if not any(p[j:j + 3] in bad for j in range(4))]
    b2 = beta2_of(A)
    return b2 == 5 and len(A) == 674, {"N": len(A), "beta2": b2}

# ---------------- dead sets and nerve certificates ----------------
def dead_sets(A):
    through = set()
    for p in A:
        m = 0
        for x in p[:-1]:
            m |= 1 << x; through.add(m)
    return sorted(I for I in range(1, FULL) if I not in through)
def comparable(a, b): return (a & b) == a or (a & b) == b
def is_face(T): return any(all(comparable(x, z) for x in T) for z in range(1, FULL))
def nerve_h1(D):
    edges = [e for e in itertools.combinations(D, 2) if is_face(e)]
    tris = [t for t in itertools.combinations(D, 3) if is_face(t)]
    vid = {v: i for i, v in enumerate(D)}; eid = {e: i for i, e in enumerate(edges)}
    r1 = rank([(1 << vid[a]) ^ (1 << vid[b]) for a, b in edges])
    r2 = rank([(1 << eid[(a, b)]) ^ (1 << eid[(a, c)]) ^ (1 << eid[(b, c)]) for a, b, c in tris])
    return len(edges) - r1 - r2, edges, tris
def check_certificate(rec, full=False):
    A = arithmetic_A(rec["content"], rec["source"]); D = dead_sets(A)
    b1, edges, tris = nerve_h1(D)
    es = {tuple(e) for e in rec["cocycle_edges"]}
    z = rec["cycle"]; n = len(z)
    if not all(((min(z[i], z[(i + 1) % n]), max(z[i], z[(i + 1) % n])) in set(edges)) for i in range(n)): return False, "cycle edge not in nerve"
    for a, b, c in tris:
        if ((a, b) in es) ^ ((a, c) in es) ^ ((b, c) in es): return False, "cocycle fails on a triangle"
    val = 0
    for i in range(n): val ^= int((min(z[i], z[(i + 1) % n]), max(z[i], z[(i + 1) % n])) in es)
    if val != 1: return False, "c(z) != 1"
    if full and beta2_of(A) <= 0: return False, "beta2 by definition is 0"
    return b1 > 0, {"H1_rank": b1, "dead": len(D)}

def main():
    full = "--full" in sys.argv; t0 = time.time(); allok = True
    certp = sys.argv[sys.argv.index("--cert") + 1] if "--cert" in sys.argv else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "CERTIFICATES", "positives_cycle_cocycle.json")
    ok, rep = check_adj(); print("[ADJ]", "PASS" if ok else "FAIL", rep, round(time.time() - t0)); allok &= ok
    ok, rep = check_3adj(); print("[3ADJ]", "PASS" if ok else "FAIL", rep, round(time.time() - t0)); allok &= ok
    pairs = [((2, 3, 4, 5, 8, 15), 480, 1), ((2, 3, 4, 5, 8, 15), 800, 0), ((2, 4, 5, 9, 14, 15), 2520, 1), ((2, 4, 5, 9, 14, 15), 3780, 0)]
    for C, s, want in pairs:
        A = arithmetic_A(C, s); b2 = beta2_of(A); b1 = nerve_h1(dead_sets(A))[0]
        good = (b2, b1) == (want, want); allok &= good
        print("[NERVE-PAIR]", C, s, "beta2 by definition =", b2, " H1(N[D]) =", b1, "PASS" if good else "FAIL")
    if os.path.exists(certp):
        recs = json.load(open(certp)); bad = 0
        for r in recs:
            good, info = check_certificate(r, full)
            if not good: bad += 1; print("  certificate FAIL", r["content"], r["source"], info)
        print("[NERVE-CERT]", len(recs), "certificates,", "all PASS" if bad == 0 else f"{bad} FAIL", round(time.time() - t0)); allok &= (bad == 0)
    else:
        print("[NERVE-CERT] certificate file not found:", certp); allok = False
    print("ALL PASS" if allok else "FAILURES"); sys.exit(0 if allok else 1)
if __name__ == "__main__": main()
