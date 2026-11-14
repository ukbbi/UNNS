#!/usr/bin/env python3
"""Fourth batch: dead-set nerve theorem and strong-collapse cores on random arithmetic regimes."""
import json, os, sys, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); 
from gigmini import *
from nerve_tools import dead_sets, nerve_facets, simplices_upto2, strong_collapse
OUT = {}
def rec(name, **kw): OUT[name] = kw; print(name, json.dumps(kw, default=str)[:300])
def h1_of(facets):
    S = simplices_upto2(facets)
    V = sorted(s[0] for s in S if len(s) == 1); E = sorted(s for s in S if len(s) == 2); T = sorted(s for s in S if len(s) == 3)
    vi = {v: i for i, v in enumerate(V)}; ei = {e: i for i, e in enumerate(E)}
    d1 = [(1 << vi[e[0]]) | (1 << vi[e[1]]) for e in E]
    d2 = [(1 << ei[(t[0], t[1])]) | (1 << ei[(t[0], t[2])]) | (1 << ei[(t[1], t[2])]) for t in T]
    return len(E) - rank_gf2(d1) - rank_gf2(d2)
rnd = random.Random(20261106)
tested = 0; ok_nerve = 0; ok_core = 0; pos = 0; maxcore = 0; mism = []
while tested < 160:
    lab = tuple(sorted(rnd.sample(range(1, 23), 6)))
    m = rnd.choice([rnd.randint(1, 4000), 2 ** rnd.randint(0, 6) * 3 ** rnd.randint(0, 4) * rnd.choice([1, 5, 7, 11, 13])])
    A = admissible_perms(lab, m)
    if not A or len(A) == 720: continue
    f, b = betti(6, complex_from_vertex_set(6, A)); b2 = b[2] if len(b) > 2 else 0
    D = dead_sets(6, A); fac = nerve_facets(6, D)
    h1 = h1_of(fac)
    core = strong_collapse(fac)
    h1c = h1_of(core) if core else 0
    tested += 1; pos += (b2 > 0); maxcore = max(maxcore, len(set().union(*core)) if core else 0)
    ok_nerve += (b2 == h1); ok_core += (b2 == h1c)
    if b2 != h1 or b2 != h1c: mism.append((lab, m, b2, h1, h1c))
rec("ch12_13_nerve_and_core_random", tested=tested, beta2_positive=pos, beta2_eq_H1_nerve=ok_nerve, beta2_eq_H1_core=ok_core, max_core_vertices=maxcore, mismatches=mism[:5])
# the four named systems: core sizes
named = {}
for lab, ms in (((2, 4, 5, 9, 14, 15), (2520, 3780)), ((2, 3, 4, 5, 8, 15), (480, 800))):
    for m in ms:
        A = admissible_perms(lab, m); D = dead_sets(6, A); fac = nerve_facets(6, D); core = strong_collapse(fac)
        f, b = betti(6, complex_from_vertex_set(6, A))
        named[f"{lab}@{m}"] = dict(N=len(A), dead=len(D), core_vertices=len(set().union(*core)) if core else 0, beta2=b[2], H1_nerve=h1_of(fac))
rec("ch13_named_systems_cores", **named)

# all 290 known positives: beta_2 from the definition vs H_1 of the nerve vs H_1 of the collapse core
cert = json.load(open(os.path.join(HERE, "inherited", "positives_cycle_cocycle.json")))
from collections import Counter
ok = 0; coresizes = Counter(); bad = []
for r in cert:
    lab = tuple(r["content"]); m = r["source"]
    A = admissible_perms(lab, m)
    f, b = betti(6, complex_from_vertex_set(6, A)); b2 = b[2] if len(b) > 2 else 0
    D = dead_sets(6, A); fac = nerve_facets(6, D); core = strong_collapse(fac)
    h1 = h1_of(fac); h1c = h1_of(core) if core else 0
    coresizes[len(set().union(*core)) if core else 0] += 1
    if b2 > 0 and b2 == h1 == h1c: ok += 1
    else: bad.append((lab, m, b2, h1, h1c))
rec("ch12_13_all_290_positives", n=len(cert), all_equal_and_positive=ok, core_size_distribution=dict(sorted(coresizes.items())), bad=bad[:5])

# the 151 distinct rank-indexed dead-set patterns of the 158 census positives and their strong-collapse core sizes
seen_pat = set(); cs = Counter()
for r in cert:
    if r["src"] != "D": continue
    lab = tuple(r["content"]); m = r["source"]
    A = admissible_perms(lab, m); D = dead_sets(6, A)
    if tuple(D) in seen_pat: continue
    seen_pat.add(tuple(D))
    core = strong_collapse(nerve_facets(6, D)); cs[len(set().union(*core))] += 1
rec("ch13_census_positive_patterns_core_sizes", n_patterns=len(seen_pat), sizes=dict(sorted(cs.items())))
json.dump(OUT, open(os.path.join(HERE, "results5.json"), "w"), indent=1, default=str)
print("DONE")
