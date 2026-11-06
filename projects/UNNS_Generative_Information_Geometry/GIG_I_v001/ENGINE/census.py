"""GIG-I v001 -- census of arithmetically realizable admissible sets and their information/topology data.

For a content C of k distinct labels, the set of admissible arrangements at source m is
  A_C(m) = { w in S_k : K(w) | m }     (frozen law D-T7; here K is computed by history_fibres.threshold),
and it only changes when m crosses the lcm-closure of the thresholds.  So every realizable A_C(m) equals A_C(c)
for some c in that closure.  The census enumerates them and attaches (N, components, ball data, Betti).
"""
from itertools import combinations, permutations
from math import lcm
from collections import Counter
from history_fibres import threshold, is_squarefree
import history_complex as hc
import swap_graph as sg


def lcm_closure(values, cap):
    S = set(values)
    fr = set(values)
    while fr:
        new = set()
        for a in fr:
            for b in S:
                c = lcm(a, b)
                if c not in S:
                    new.add(c)
        S |= new
        fr = new
        if len(S) > cap:
            return None
    return S


def realizable_masks(k, L, cap=30000):
    """dict mask -> {'ex': (content, source), 'sq': bool, 'exsq': (content, source) or None}.
    Contents: k-subsets of {1..L}.  Sources: lcm-closure of thresholds.  Contents with closure > cap are counted in 'skipped'."""
    P = hc.perms(k)
    found, skipped = {}, 0
    for C in combinations(range(1, L + 1), k):
        thr = [threshold(tuple(C[i] for i in p)) for p in P]
        S = lcm_closure(set(thr), cap)
        if S is None:
            skipped += 1
            continue
        for m in S:
            mask = 0
            for i, K in enumerate(thr):
                if m % K == 0:
                    mask |= 1 << i
            if not mask:
                continue
            sq = is_squarefree(m)
            e = found.get(mask)
            if e is None:
                found[mask] = {"ex": (C, m), "sq": sq, "exsq": (C, m) if sq else None}
            elif sq and e["exsq"] is None:
                e["exsq"] = (C, m)
                e["sq"] = True
    return found, skipped


def mask_data(mask, k):
    """information + topology data of the induced swap graph / permutohedral complex on the arrangement set `mask`."""
    P = hc.perms(k)
    A = [P[i] for i in range(len(P)) if mask >> i & 1]
    order, adj = hc.induced_adjacency(set(A), k)
    comps = sg.components(adj)
    prof = sg.ball_profile(adj)
    D = max(len(p) - 1 for p in prof)
    return {
        "N": len(A), "E": sum(len(a) for a in adj) // 2, "sizes": tuple(sorted(len(c) for c in comps)),
        "D": D, "Pr": tuple(sg.ball_product(prof, r) for r in range(D + 1)), "prof": prof,
        "deg": tuple(sorted(len(a) for a in adj)), "betti": hc.betti(mask, k), "cubical": hc.betti(mask, k, True),
    }


def truncated_signature(d, r):
    """fine accessibility signature up to swap-radius r: (class sizes, multiset of per-vertex ball-size vectors (|B_0|..|B_r|))."""
    vecs = Counter(tuple(sg.ball_size(p, j) for j in range(r + 1)) for p in d["prof"])
    return (d["sizes"], tuple(sorted(vecs.items())))


def scalar_signature(d, r):
    """scalar information signature up to radius r: (N, class sizes, P_0..P_r) -- equivalent to (N, sizes, I_0..I_r)."""
    return (d["N"], d["sizes"], tuple(d["Pr"][min(j, d["D"])] for j in range(r + 1)))


def detection_table(datas, rmax=4):
    """for r = 0..rmax: number of signature groups and number of groups containing >1 distinct Betti vector."""
    out = []
    for r in range(rmax + 1):
        for name, f in (("fine", truncated_signature), ("scalar", scalar_signature)):
            g = {}
            for d in datas:
                g.setdefault(f(d, r), set()).add(d["betti"])
            out.append({"r": r, "kind": name, "groups": len(g), "ambiguous_groups": sum(1 for s in g.values() if len(s) > 1)})
    return out


def symmetry_group(k):
    """index maps of the symmetry group S_k x Z_2 of the permutohedron acting on arrangement sets (relabel values; reverse)."""
    P = hc.perms(k)
    pidx = hc.perm_index(k)
    G = []
    for g in permutations(range(k)):
        for rev in (0, 1):
            mp = []
            for p in P:
                q = tuple(g[x] for x in p)
                if rev:
                    q = q[::-1]
                mp.append(pidx[q])
            G.append(mp)
    return G


def canonical_mask(mask, G):
    bits = [i for i in range(mask.bit_length()) if mask >> i & 1]
    best = None
    for mp in G:
        m = 0
        for i in bits:
            m |= 1 << mp[i]
        if best is None or m < best:
            best = m
    return best
