"""HD-1D v002 builder: writes results/THRESHOLD_CENSUS.json and results/FAMILY_14Q.json.  python build_v002.py"""
import os, sys, json, itertools, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from thresholds import *
from math import gcd


def max_components(content):
    thr = threshold_table(content)
    cl = lcm_closure(set(thr.values()))
    return max(len(classes_at(thr, m)) for m in cl), len(cl)


t0 = time.time()
three = []; maxc = {}
for c in itertools.combinations(range(1, 31), 3):
    thr, cl, sp, mins = split_sources(c)
    if sp: three.append(dict(content=list(c), minimal_split_sources=mins, closure_size=len(cl)))
four = []
for c in itertools.combinations(range(1, 15), 4):
    thr, cl, sp, mins = split_sources(c)
    if sp: four.append(dict(content=list(c), minimal_split_sources=mins))
rep = []; nrep = 0
for k in (3, 4, 5):
    for c in itertools.combinations_with_replacement(range(1, 11), k):
        if len(set(c)) == k: continue
        nrep += 1
        thr, cl, sp, mins = split_sources(c)
        if sp: rep.append(dict(content=list(c), minimal_split_sources=mins))
fam = {}
for N in range(4, 401):
    thr, cl, sp, mins = split_sources((2, 3, N))
    fam[N] = dict(split=bool(sp), minimal_split_sources=mins)
mc3 = max(max_components(c)[0] for c in itertools.combinations(range(1, 13), 3))
mc4 = max(max_components(c)[0] for c in itertools.combinations(range(1, 11), 4))
json.dump(dict(
    scope=dict(three_distinct="labels<=30 (4060 contents)", four_distinct="labels<=14 (1001 contents)", repeated="size 3-5 multisets with a repeat, labels<=10 (%d contents)" % nrep, family="{2,3,N}, 4<=N<=400"),
    three_distinct_split=dict(count=len(three), contents=three), four_distinct_split=dict(count=len(four), contents=four), repeated_split=dict(count=len(rep), contents=rep),
    family_2_3_N=dict(split_N=[N for N, v in fam.items() if v["split"]], all_minimal_sources_equal_N=all(v["minimal_split_sources"] == [N] for N, v in fam.items() if v["split"]), residues_mod_6=sorted({N % 6 for N, v in fam.items() if v["split"]})),
    max_components_seen=dict(three_labels_le12=mc3, four_labels_le10=mc4), seconds=round(time.time() - t0)), open(os.path.join(ROOT, "results", "THRESHOLD_CENSUS.json"), "w"), indent=1)
thr = threshold_table((2, 3, 14))
rows = []
for q in range(1, 121):
    cl = classes_at(thr, 14 * q)
    rows.append(dict(q=q, admissible=sum(len(c) for c in cl), classes=len(cl), predicted_classes=2 if gcd(q, 6) == 1 else 1))
json.dump(dict(content=[2, 3, 14], thresholds={str(w): k for w, k in thr.items()}, connection_thresholds=connect_thresholds(thr, (14, 3, 2), (2, 3, 14)),
               rule="2 classes iff gcd(q,6)=1 else 1 (source 14q, histories from a FIXED source; complete histories need a squarefree source)", table=rows), open(os.path.join(ROOT, "results", "FAMILY_14Q.json"), "w"), indent=1)
print("done", round(time.time() - t0), len(three), len(four), len(rep), mc3, mc4)
