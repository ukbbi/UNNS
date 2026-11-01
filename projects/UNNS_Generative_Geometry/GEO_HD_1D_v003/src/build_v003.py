"""HD-1D v003 builder: writes results/*.json from the builder modules (swap_classes, route_topology, topo_census, occurrence_bridge).
   python build_v003.py            (about 1-2 minutes)"""
import os, sys, json, itertools, random, time
from math import gcd, prod
from collections import Counter
from itertools import permutations
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from thresholds import threshold_table, classes_at, lcm_closure, split_sources, K
from swap_classes import feeds, scc_blocks, is_acyclic, strongly_connected, block_product_classes, direct_classes
from swap_classes import has_hub, three_label_splits, K_prefix, kappa
from route_topology import betti, nerve_components
from topo_census import patterns, census
import occurrence_bridge as OB


def dump(name, obj):
    with open(os.path.join(ROOT, "results", name), "w") as f: json.dump(obj, f, indent=1, sort_keys=True)


def feeding_census():
    out = {}
    # Lemma NF at the threshold level: x does not feed y  =>  K((y,x)) | K((x,y))
    n = bad = 0
    for x in range(1, 301):
        for y in range(1, 301):
            if x == y or feeds(x, y): continue
            n += 1
            if K((x, y)) % K((y, x)): bad += 1
    out["NF_threshold_pairs"] = {"pairs": n, "violations": bad, "range": "labels 1..300"}
    # F2 product formula
    random.seed(3); tot = bad = 0; ncont = 0
    def run(contents, cap):
        nonlocal tot, bad, ncont
        for c in contents:
            thr = threshold_table(c)
            try: cl = lcm_closure(set(thr.values()), cap=200000)
            except OverflowError: continue
            if len(cl) > cap: cl = random.sample(cl, cap)
            ncont += 1
            for m in set(cl) | {x * p for x in cl[:30] for p in (2, 3, 5)}:
                tot += 1
                if direct_classes(c, m) != block_product_classes(c, m): bad += 1
    for k, rng in ((2, 30), (3, 22), (4, 13)): run(itertools.combinations(range(1, rng + 1), k), 300)
    run((c for c in itertools.combinations_with_replacement(range(1, 11), 4) if len(set(c)) < 4), 200)
    run((c for c in itertools.combinations_with_replacement(range(1, 9), 5) if len(set(c)) < 5 and len(set(c)) >= 3), 100)
    out["F2_product_formula"] = {"contents": ncont, "content_source_pairs": tot, "violations": bad,
                                 "scope": "distinct k=2 (<=30), 3 (<=22), 4 (<=13); repeated size 4 (<=10), size 5 (<=8); lcm-closure sources + multiples"}
    # F1 and 'split needs a block with >= 3 distinct labels'
    f1 = {}
    for k, rng in ((3, 30), (4, 14), (5, 10)):
        nac = maxcl = nsplit = nbad3 = ntot = 0
        for c in itertools.combinations(range(1, rng + 1), k):
            ntot += 1
            thr, cl, sp, mins = split_sources(c)
            blocks = scc_blocks(c)
            if is_acyclic(c):
                nac += 1
                maxcl = max(maxcl, max((len(classes_at(thr, m)) for m in cl), default=0))
            if sp:
                nsplit += 1
                if max(len(B) for B in blocks) < 3: nbad3 += 1
        f1[str(k)] = {"labels_le": rng, "contents": ntot, "acyclic": nac, "max_classes_acyclic": maxcl, "split": nsplit, "split_without_block_of_size_ge3": nbad3}
    out["F1_and_block_size"] = f1
    # 3-label strongly connected census and hub criterion
    sc = [c for c in itertools.combinations(range(1, 31), 3) if strongly_connected(c)]
    scs = [c for c in sc if split_sources(c)[2]]
    out["three_label_census"] = {"labels_le": 30, "contents": 4060, "split": 127, "strongly_connected": len(sc), "strongly_connected_split": len(scs),
                                 "strongly_connected_no_split": len(sc) - len(scs), "no_split_examples": [c for c in sc if c not in set(scs)][:20]}
    hub = {}
    for k, rng in ((3, 30), (4, 14)):
        a = b = c_ = d = 0
        for c in itertools.combinations(range(1, rng + 1), k):
            h = has_hub(c); sp = bool(split_sources(c)[2])
            if h and sp: a += 1
            elif h: b += 1
            elif sp: c_ += 1
            else: d += 1
        hub[str(k)] = {"labels_le": rng, "hub_and_split": a, "hub_nosplit": b, "nohub_split": c_, "nohub_nosplit": d}
    out["hub_descent"] = hub
    # {2,3,N}: SCC characterisation
    out["family_2_3_N_scc"] = {"N_range": "4..3000", "violations": sum(1 for N in range(4, 3001) if (len(scc_blocks((2, 3, N))) == 1) != (N % 6 in (2, 3)))}
    # prefix-set form and the exact 3-label criterion
    n = nsp = bad = badK = 0
    for c in itertools.combinations(range(1, 41), 3):
        n += 1; sp = bool(split_sources(c)[2]); nsp += sp
        if sp != bool(three_label_splits(c)): bad += 1
        badK += sum(1 for w, kk in threshold_table(c).items() if K_prefix(w) != kk)
    out["three_label_criterion"] = {"labels_le": 40, "contents": n, "split": nsp, "mismatch": bad, "prefix_form_violations": badK}
    dump("FEEDING_CENSUS.json", out); return out


def topology_census():
    out = {}; cache5 = {}
    for k, rng in ((3, 30), (4, 18), (5, 11)):
        cache, hist, ex, nc, ns = census(k, rng)
        S = set(permutations(range(k))); viol = 0; ndual = 0
        for A, (b, chi) in cache.items():
            R = S - set(A)
            if not R or not A: continue
            red = list(b); red[0] -= 1; ndual += 1
            if red[k - 3] != nerve_components(R, k) - 1 or red[k - 2] != 0: viol += 1
        out["k%d" % k] = {"labels_le": rng, "contents": nc, "content_source_pairs": ns, "distinct_admissible_sets": len(cache),
                          "betti_histogram": {str(key): v for key, v in sorted(hist.items())},
                          "duality_top_degree_checked": ndual, "duality_violations": viol,
                          "first_noncontractible_examples": {str(key): [list(e[0]), e[1], e[2]] for key, e in ex.items()}}
    # acyclic => contractible
    ac = {}
    for k, rng in ((3, 30), (4, 18), (5, 12)):
        n = badn = 0
        for c in itertools.combinations(range(1, rng + 1), k):
            if not is_acyclic(c): continue
            try: pats = patterns(c)
            except OverflowError: continue
            for A, m in pats.items():
                n += 1
                b = betti(A, k)[0]
                if A and b != (1,) + (0,) * (k - 1): badn += 1
        ac[str(k)] = {"labels_le": rng, "acyclic_content_source_pairs": n, "noncontractible": badn}
    out["acyclic_contractible"] = ac
    # two-facet (parity-separation) family: C = {2,3} u X, X in {n>=8, n = 2,3 mod 6}, m = prod X
    F = [n for n in range(8, 62) if n % 6 in (2, 3)]; fam = {"contents": 0, "mismatch": 0, "betti": Counter()}
    for r in (1, 2, 3, 4):
        for X in itertools.combinations(F, r):
            if r == 4 and max(X) > 44: continue
            C = (2, 3) + X; m = prod(X); thr = threshold_table(C)
            E = {x for x in C if x % 6 == 2}; O = {x for x in C if x % 6 == 3}
            R = {w for w, kk in thr.items() if m % kk}
            Rp = {w for w in thr if set(w[:len(E)]) == E or set(w[:len(O)]) == O}
            fam["contents"] += 1
            if R != Rp: fam["mismatch"] += 1
            if len(C) <= 5:
                rank = {x: i for i, x in enumerate(sorted(C))}
                A = frozenset(tuple(rank[x] for x in w) for w in thr if w not in R)
                fam["betti"][str(betti(A, len(C))[0])] += 1
    fam["betti"] = dict(fam["betti"]); out["two_facet_family"] = fam
    # converse for {2,3,N,M}
    mism = 0; n = 0
    for N, M in itertools.combinations(range(4, 61), 2):
        c = (2, 3, N, M)
        try: pats = patterns(c)
        except OverflowError: continue
        hit = any(betti(A, 4)[0][1] > 0 for A in pats); n += 1
        if hit != (N >= 8 and M >= 8 and N % 6 in (2, 3) and M % 6 in (2, 3)): mism += 1
    out["converse_2_3_N_M"] = {"pairs": n, "range": "4<=N<M<=60", "mismatch": mism}
    # cubical vs permutohedral for the full hexagon / k=4
    S3 = list(permutations(range(3))); S4 = list(permutations(range(4)))
    out["cubical_vs_permutohedral"] = {"k3_full": {"perm": list(betti(S3, 3)[0]), "cubical": list(betti(S3, 3, True)[0])},
                                       "k4_full": {"perm": list(betti(S4, 4)[0]), "cubical": list(betti(S4, 4, True)[0])}}
    dump("TOPOLOGY_CENSUS.json", out); return out


def occurrence_bridge():
    out = {}; ds = [2, 3, 4, 6, 8, 9, 12, 18, 24, 36]
    for r in (1, 2, 3):
        res, hists, cache = OB.restricted_counts(72 ** r, ds)
        out["72^%d" % r] = {"n_histories": res["n_histories"], "classes_unrestricted": res["classes_unrestricted"],
                            "preserve": {str(d): res[(d, "preserve")] for d in ds}, "after": {str(d): res[(d, "after")] for d in ds}}
    dump("OCCURRENCE_BRIDGE.json", out); return out


if __name__ == "__main__":
    t = time.time(); os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    f = feeding_census(); print("feeding %.0fs" % (time.time() - t), flush=True)
    tp = topology_census(); print("topology %.0fs" % (time.time() - t), flush=True)
    ob = occurrence_bridge(); print("occurrence %.0fs" % (time.time() - t), flush=True)
