import sys, json, time
sys.setrecursionlimit(10000)
from hist import *
from eng3 import factor
def sig(E): return tuple(sorted((p, e // 2) for p, e in factor(E).items() if e // 2))
res = {}
t0 = time.time()
for m0 in (4,):
    groups = {}
    for E in range(4 * m0, 120001):
        if all(e < 2 for e in factor(E).values()): continue
        H = histories(m0, E)
        if not H: continue
        C = classes(m0, E)[1]
        groups.setdefault(sig(E), []).append((E, len(H), len(C)))
    coll = [(s, g) for s, g in groups.items() if len({c for (_, _, c) in g}) > 1]
    print(m0, 'groups', len(groups), 'collisions', len(coll), round(time.time() - t0, 1))
    res[m0] = [(list(map(list, s)), g) for s, g in coll[:40]]
    res['totals_%d' % m0] = {'range': [4 * m0, 120000], 'groups': len(groups), 'groups_with_several_E': sum(1 for g in groups.values() if len(g) > 1), 'collisions_diff_classes': len(coll), 'collisions_diff_histcount': sum(1 for g in groups.values() if len({h for (_, h, _) in g}) > 1)}
    for s, g in coll[:8]: print(s, g)
json.dump(res, open('../results/c1_collide.json', 'w'))
