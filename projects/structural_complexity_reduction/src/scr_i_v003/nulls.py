from __future__ import annotations
import hashlib, random
from .basins import preservation, preservation_from_baseline

def seed_for(primary_seed:int,replicate:int)->int:
    return int.from_bytes(hashlib.sha256(f'{primary_seed}|{replicate}|v003-N1'.encode()).digest()[:8],'big')

def selection_mask(n:int,n_survivors:int,primary_seed:int,replicate:int)->list[bool]:
    rng=random.Random(seed_for(primary_seed,replicate)); ids=set(rng.sample(range(n),n_survivors)) if n_survivors else set()
    return [i in ids for i in range(n)]

def rate_matched_random(pool,target_labels,n_survivors,primary_seed,replicate):
    """Reference compatibility path; recomputes baseline clustering."""
    ids=selection_mask(len(pool),n_survivors,primary_seed,replicate)
    target_mechs=[]; target_surv=[]
    for i,(m,t) in enumerate(zip(pool,target_labels)):
        if t: target_mechs.append(m); target_surv.append(ids[i])
    p=preservation(target_mechs,target_surv)
    p['n_survivors']=n_survivors
    p['candidate_target_recall']=(sum(target_surv)/len(target_surv)) if target_surv else None
    return p

def rate_matched_random_cached(pool,target_labels,n_survivors,primary_seed,replicate,baseline):
    """Mathematically identical N1 null evaluation using cached baseline geometry."""
    ids=selection_mask(len(pool),n_survivors,primary_seed,replicate)
    target_surv=[ids[i] for i,t in enumerate(target_labels) if t]
    p=preservation_from_baseline(baseline,target_surv,include_details=False)
    p['n_survivors']=n_survivors
    p['candidate_target_recall']=(sum(target_surv)/len(target_surv)) if target_surv else None
    return p
