"""v010 Programme C (adversarial, nullity >= 7): random and hill-climbing search over reduced supports Sigma in AG(m,2) (k = m+1), looking for MINIMAL non-embedded boxes (partition criterion + shortening)
and recording the number of two-circuit partitions of the all-ones word (W2 holds iff >= 2).  Objective of the climb: minimise that number.  A minimal box with fewer than 2 would be a candidate for r_min >= 4
(then the full cell engine must exclude every rank-3 collision).  usage: rank_attack7.py M NRANDOM NCLIMB SEED OUT.json"""
import sys,random,time,json; sys.path.insert(0,'theory')
import binary5 as B5, binary6 as B6
m=int(sys.argv[1]); NR=int(sys.argv[2]); NC=int(sys.argv[3]); rng=random.Random(int(sys.argv[4])); out=sys.argv[5]; k=m+1
top=1<<m; pts=[top|a for a in range(1<<m)]
def evaluate(sig):
    """returns None if not (spanning, non-embedded, minimal) else (#two-circuit partitions of 1, circuits)."""
    if B5.rank_of(sig)<k: return None
    C=B5.code_masks(sig); n=len(sig)
    if not B6.non_embedded(C): return None
    for i in range(n):
        if B6.non_embedded(B5.delete(C,i)): return None
    circ=B5.circuits_of_code(C); full=(1<<n)-1; cs=set(circ)
    two=sum(1 for c in circ if (full^c) in cs)//2
    return two,len(circ)
res={'m':m,'k':k,'random_tested':0,'random_minimal':0,'min_two_blocks_random':None,'climb_best':None,'counterexample':None}; t0=time.time(); hist={}
best=None
for it in range(NR):
    p=rng.randint(k+1,len(pts)); sig=sorted(rng.sample(pts,p)); res['random_tested']+=1
    e=evaluate(sig)
    if e is None: continue
    res['random_minimal']+=1; hist[e[0]]=hist.get(e[0],0)+1
    if best is None or e[0]<best[0]: best=(e[0],sig)
    if e[0]<2: res['counterexample']=sig; print('CANDIDATE',sig,flush=True)
res['two_block_hist_random']=dict(sorted(hist.items()))
if best: res['min_two_blocks_random']=best[0]
# hill climb from best/random minimal starts: single point toggle moves, accept if still minimal non-embedded and two-block count does not increase
cur=best
for it in range(NC):
    if cur is None: break
    sig=list(cur[1]); j=rng.choice(pts)
    nxt=sorted(set(sig)^{j}) if rng.random()<.6 else sorted((set(sig)-{rng.choice(sig)})|{j})
    if len(nxt)<k+1: continue
    e=evaluate(nxt)
    if e is None: continue
    if e[0]<=cur[0]: cur=(e[0],nxt)
    if e[0]<2: res['counterexample']=nxt; print('CANDIDATE',nxt,flush=True); break
if cur: res['climb_best']=[cur[0],len(cur[1]),cur[1]]
res['seconds']=round(time.time()-t0,1); json.dump(res,open(out,'w')); print(res)
