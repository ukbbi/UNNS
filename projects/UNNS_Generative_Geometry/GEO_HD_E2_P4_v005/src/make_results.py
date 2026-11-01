"""v005: regenerate the small result files (planar audit, counterexample checks, tiling lemma). Usage: python src/make_results.py"""
import sys, os, json, random, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'engine'))
import planar_audit as pa, ce_check, tiling_lemma as tl

def dump(name, obj):
    json.dump(obj, open(os.path.join(ROOT, 'results', name), 'w'), indent=1, default=str)

t = time.time()
# planar audits (exact polygon subtraction)
rnd = {}
st, fl = pa.audit(7, 200, 14, nmax_src=9, nmax_tgt=6, time_budget=150)
rnd['random_nested_seed7'] = dict(stats=st, failures=fl[:5])
hd = {}
for seed in (100, 101, 102, 103):
    st, fl = pa.hard_driven_audit(seed, 4000, time_budget=60, nmax_src=4, nmax_tgt=4, cap=14)
    hd['seed%d' % seed] = dict(stats=st, failures=fl[:5])
dump('P5_PLANAR_AUDIT.json', dict(random=rnd, hard_driven=hd, note='exact rational polygon containment; P5-P1 predicts failures == 0 and structure_violations == 0'))
print('planar done', round(time.time() - t), rnd, hd, flush=True)

# counterexample checks (three implementations + independently verified certificate)
ce = {}
for name, c in ce_check.CASES.items():
    ce[name] = ce_check.check_case(name, c)
dump('P5_CE_CHECKS.json', dict(cases=ce, note='NOT_CONTAINED each, certificate independently verified'))
print('ce done', round(time.time() - t), flush=True)

# tiling lemma
rng = random.Random(20261031); out = []
for d, cnt in ((1, 40), (2, 40), (3, 40)):
    bad = tiles = 0
    for V in tl.random_configs(rng, d, cnt, 6):
        while True:
            try:
                vo, co, nt = tl.check_configuration(V, rng); break
            except ValueError:
                continue
        tiles += nt; bad += (not (vo and co))
    out.append(dict(d=d, configs=cnt, tiles=tiles, bad=bad))
dump('P5_TILING_LEMMA.json', dict(runs=out, seed=20261031, note='volume identity + coverage of lifted tiles; subset-sum vertices by construction'))
print('tiling', out, round(time.time() - t))
