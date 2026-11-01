"""v005: replay of the P5-S4 criterion against the pinned exact engine over many split targets (writes results/P5_SPLIT_SLAB.json)."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'engine'))
import split_slab as ss, planar_audit as pa
out = sys.argv[1]
budget = float(sys.argv[2]) if len(sys.argv) > 2 else 40
t = time.time(); st = dict(hard=0, agree=0, disagree=0, noncontained=0); bad = []; per = []
L2s = [L for n in (1, 2, 3) for L in pa.hnf2_all(n)]
for L2 in L2s:
    for k in (1, 2, 3):
        s0 = dict(st)
        s, b = ss.check_criterion(L2, k, m_list=(2,), stats=st, time_budget=budget); bad += b
        per.append(dict(L2=L2, k=k, hard=st['hard'] - s0['hard'], noncontained=st['noncontained'] - s0['noncontained'], disagree=st['disagree'] - s0['disagree']))
        print(L2, k, st, round(time.time() - t), flush=True)
        json.dump(dict(stats=st, bad=bad[:10], per=per, complete=False), open(out, 'w'), default=str)
json.dump(dict(stats=st, bad=bad[:10], per=per, complete=True, description="P5-S4 criterion vs pinned engine; split targets Lambda'_2 (+) kZ, Lambda'_2 of index<=3 in Z^2, k=1,2,3; sources of index 2 in Lambda'; every hard cell with bounding box <= min(3 k_c, cap); per-combination time budget %s s" % budget), open(out, 'w'), default=str)
print('DONE', st)
