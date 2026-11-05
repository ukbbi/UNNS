"""Search: same local key AND same Delta beta_0, different Delta beta_1 (needs 2-cells for Euler consistency)"""
import random, json
from trans3 import analyse
from eng3 import divisors, factor
random.seed(11)
pool = sorted(d for d in divisors(factor(2**3*3**2*5*7*11)) if d >= 2)
groups = {}; n = 0
for it in range(60000):
    k = random.randint(3, 6); D = random.sample(pool, k)
    rest = [d for d in pool if d not in D]; N = random.sample(rest, random.randint(1, 3))
    try: t = analyse(D, D + N)
    except Exception: continue
    if t['f'][2] == 0 and t['f2'][2] == 0: continue
    key = (tuple(t['f']), tuple(t['f2']), tuple(t['dead']), tuple(t['new']), t['db'][0])
    groups.setdefault(key, {}).setdefault(tuple(t['db']), (sorted(D), sorted(N), t['b'], t['b2']))
coll = [(k, v) for k, v in groups.items() if len(v) > 1]
coll.sort(key=lambda kv: sum(kv[0][1]) + sum(kv[0][3]))
print(len(groups), len(coll))
out = []
for k, v in coll[:5]:
    print(k)
    for db, ex in v.items(): print('  ', db, ex)
    out.append({'key': k, 'ex': [{'db': list(db), 'D': ex[0], 'N': ex[1], 'b': ex[2], 'b2': ex[3]} for db, ex in v.items()]})
json.dump(out, open('../results/c7_dim2.json', 'w'))
