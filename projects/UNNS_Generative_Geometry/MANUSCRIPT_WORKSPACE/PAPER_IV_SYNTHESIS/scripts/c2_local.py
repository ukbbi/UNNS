import random, json, itertools, sys
from trans3 import analyse
from eng3 import divisors, factor
random.seed(7)
pool = sorted(d for d in divisors(factor(2**3*3**2*5*7*11)) if d >= 2)
groups = {}; n = 0
for it in range(40000):
    k = random.randint(2, 5); D = random.sample(pool, k)
    rest = [d for d in pool if d not in D]; N = random.sample(rest, random.randint(1, 3))
    try: t = analyse(D, D + N)
    except Exception as e: continue
    n += 1
    key = (tuple(t['f']), tuple(t['f2']), tuple(t['dead']), tuple(t['new']))
    groups.setdefault(key, {}).setdefault(tuple(t['db']), (sorted(D), sorted(N), t['b'], t['b2']))
    if all(t['chk'].values()) is False: print('chk fail', D, N)
coll = [(k, v) for k, v in groups.items() if len(v) > 1]
print(n, len(groups), len(coll))
coll.sort(key=lambda kv: sum(kv[0][0]) + sum(kv[0][1]))
out = []
for k, v in coll[:6]:
    print(k); 
    for db, ex in v.items(): print('   ', db, ex)
    out.append({'key': k, 'ex': [{'db': list(db), 'D': ex[0], 'N': ex[1], 'b': ex[2], 'b2': ex[3]} for db, ex in v.items()]})
json.dump(out, open('../results/c2_local.json', 'w'))
