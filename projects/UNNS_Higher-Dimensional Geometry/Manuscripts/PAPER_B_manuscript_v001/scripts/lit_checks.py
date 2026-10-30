#!/usr/bin/env python3
"""Consistency checks supporting Section 20 (literature comparison). Not proofs.
 (1) Heden tail bound as quoted in Kurz (arXiv:1708.01113): n2 >= 2^d - 1 on all classified classes (d+1 = least m>=3).
 (2) Cooper-Okur (arXiv:2504.08083) translation: E1 non-embeddedness of a graph's cycle code  <=>  some connected Eulerian
     subgraph contains two cycles sharing an edge (random multigraphs, <=5 vertices, <=9 edges)."""
import json, random, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geo2
here = os.path.dirname(os.path.abspath(__file__))
recs = []
c = json.load(open(os.path.join(here, '../logs/classify.json')))
for k in ('k3', 'k4', 'k5'):
    for i in c[k]['info']: recs.append((k, i['p'], i['m']))
for r in json.load(open(os.path.join(here, '../logs/k6_records.json')))['k6']: recs.append(('k6', r[1], r[2]))
viol = 0; mixed = 0
for k, p, m in recs:
    big = [x for x in m if x >= 3]
    if not big: continue
    mixed += 1
    d = min(big) - 1; n2 = m.count(2)
    if not (n2 > 0 and n2 >= 2 ** d - 1): viol += 1
print('heden_tail', {'classes': len(recs), 'with_part_dim>=2': mixed, 'violations': viol})
assert viol == 0 and len(recs) == 231

def cycle_code(edges, n):
    W = set()
    for mask in range(1 << len(edges)):
        deg = [0] * n
        for i, (u, v) in enumerate(edges):
            if mask >> i & 1: deg[u] ^= 1; deg[v] ^= 1
        if not any(deg): W.add(mask)
    return W
def connected(edges, mask, n):
    es = [edges[i] for i in range(len(edges)) if mask >> i & 1]
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for u, v in es: par[f(u)] = f(v)
    return len({f(u) for u, v in es}) == 1
random.seed(2); mism = 0; N = 2000
for _ in range(N):
    nv = random.randint(2, 5); m = random.randint(3, 9)
    edges = [tuple(random.sample(range(nv), 2)) for _ in range(m)]
    W = cycle_code(edges, nv); circs = geo2.circuits_of(W)
    e1 = geo2.is_nonembedded_E1(circs)
    nc = any(w and connected(edges, w, nv) and any(a & b for i, a in enumerate([x for x in circs if x & w == x]) for b in [x for x in circs if x & w == x][i + 1:]) for w in W)
    mism += (e1 != nc)
print('cooper_okur', {'tested': N, 'mismatch': mism})
assert mism == 0
