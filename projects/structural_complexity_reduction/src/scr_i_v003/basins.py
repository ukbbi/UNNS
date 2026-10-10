from __future__ import annotations
from collections import defaultdict, deque
from itertools import product
from typing import Any
import math

EPS=0.25
MIN_NEIGHBORS=20
FEATURE_NAMES=('gamma0/2','beta/2','d/5','kmax/6','locality_score')


def feature(m: Any) -> tuple[float,float,float,float,float]:
    return (m.gamma0/2.0, m.beta/2.0, m.d/5.0, m.kmax/6.0, m.locality_score)

def distance_x(a, b) -> float:
    return math.sqrt(sum((x-y)*(x-y) for x,y in zip(a,b)))

def centroid(xs):
    n=len(xs)
    if not n: return None
    return tuple(sum(x[j] for x in xs)/n for j in range(5))

class NeighborIndex:
    def __init__(self, xs, radius=EPS):
        self.xs=xs; self.radius=radius; self.grid=defaultdict(list); self.cache={}
        for i,x in enumerate(xs): self.grid[self.cell(x)].append(i)
    def cell(self,x): return tuple(math.floor(v/self.radius) for v in x)
    def neighbors(self,i):
        if i in self.cache: return self.cache[i]
        x=self.xs[i]; c=self.cell(x); out=[]; r2=self.radius*self.radius
        for off in product((-1,0,1), repeat=5):
            key=tuple(c[j]+off[j] for j in range(5))
            for k in self.grid.get(key,()):
                if k==i: continue
                y=self.xs[k]; d2=sum((x[j]-y[j])**2 for j in range(5))
                if d2 < r2: out.append(k)
        self.cache[i]=out
        return out
    def any_within(self,x):
        c=self.cell(x); r2=self.radius*self.radius
        for off in product((-1,0,1), repeat=5):
            key=tuple(c[j]+off[j] for j in range(5))
            for k in self.grid.get(key,()):
                y=self.xs[k]
                if sum((x[j]-y[j])**2 for j in range(5)) < r2: return True
        return False


def cluster_target_basins(mechanisms: list[Any], eps: float=EPS, min_neighbors: int=MIN_NEIGHBORS) -> dict:
    xs=[feature(m) for m in mechanisms]
    idx=NeighborIndex(xs,eps)
    visited=[False]*len(xs); labels=[-1]*len(xs); clusters=[]
    for i in range(len(xs)):
        if visited[i]: continue
        neigh=idx.neighbors(i)
        if len(neigh) < min_neighbors:
            visited[i]=True
            continue
        cid=len(clusters); members=[i]; labels[i]=cid; visited[i]=True
        q=deque(neigh)
        while q:
            k=q.popleft()
            if visited[k]: continue
            visited[k]=True; labels[k]=cid; members.append(k)
            nk=idx.neighbors(k)
            if len(nk) >= min_neighbors: q.extend(nk)
        clusters.append(members)
    clustered=sum(len(c) for c in clusters)
    return {'clusters':clusters,'labels':labels,'clustered':clustered,'unclustered':len(xs)-clustered,'xs':xs}


def phenotype_strata(mechanisms: list[Any], min_count: int=20) -> dict[tuple[str,str,str], list[int]]:
    d=defaultdict(list)
    for i,m in enumerate(mechanisms): d[(m.regime_base,m.family,m.composition)].append(i)
    return {k:v for k,v in d.items() if len(v)>=min_count}


def prepare_preservation_baseline(target_mechanisms: list[Any], *, eps:float=EPS, min_neighbors:int=MIN_NEIGHBORS, stratum_min_count:int=20) -> dict:
    """Precompute the immutable baseline geometry for one (seed, pool-size) cell.

    This is an implementation-only cache. It does not change any v003 scientific
    rule, threshold, target label, cluster definition, distance, or verdict.
    """
    base=cluster_target_basins(target_mechanisms,eps,min_neighbors)
    clusters=base['clusters']; xs=base['xs']
    basin_centroids=[centroid([xs[i] for i in members]) for members in clusters]
    strata=phenotype_strata(target_mechanisms,stratum_min_count)
    return {
        'target_count':len(target_mechanisms),
        'clusters':clusters,
        'labels':base['labels'],
        'clustered':base['clustered'],
        'unclustered':base['unclustered'],
        'xs':xs,
        'basin_centroids':basin_centroids,
        'strata':strata,
        'eps':eps,
        'min_neighbors':min_neighbors,
        'stratum_min_count':stratum_min_count,
    }


def preservation_from_baseline(baseline: dict, survivor_mask_on_targets: list[bool], *, coverage_radius:float=EPS, min_basin_survivors:int=20, include_details:bool=True) -> dict:
    """Evaluate a survivor mask against precomputed baseline target geometry."""
    n=baseline['target_count']
    if n!=len(survivor_mask_on_targets): raise ValueError('target/survivor alignment mismatch')
    clusters=baseline['clusters']; xs=baseline['xs']; base_centroids=baseline['basin_centroids']
    details=[]; represented=0; min_cov=None; max_drift=None; min_surv=None
    for cid,members in enumerate(clusters):
        surv=[i for i in members if survivor_mask_on_targets[i]]
        if surv: represented+=1
        bx=[xs[i] for i in members]; sx=[xs[i] for i in surv]
        bc=base_centroids[cid]; sc=centroid(sx)
        drift=None if sc is None else distance_x(bc,sc)
        coverage=0.0
        if sx:
            sidx=NeighborIndex(sx,coverage_radius)
            coverage=sum(1 for x in bx if sidx.any_within(x))/len(bx)
        ns=len(surv)
        min_cov=coverage if min_cov is None else min(min_cov,coverage)
        if drift is not None: max_drift=drift if max_drift is None else max(max_drift,drift)
        min_surv=ns if min_surv is None else min(min_surv,ns)
        if include_details:
            details.append({'basin_id':cid+1,'baseline_size':len(members),'target_survivors':ns,'coverage':coverage,'centroid_drift':drift})
    basin_recall=None if not clusters else represented/len(clusters)
    if min_surv is None: min_surv=0
    unclustered_frac=(baseline['unclustered']/n) if n else None
    strata=baseline['strata']; strata_kept=0; strata_details=[]
    for key,inds in sorted(strata.items()):
        ns=sum(1 for i in inds if survivor_mask_on_targets[i])
        if ns>0: strata_kept+=1
        if include_details: strata_details.append({'key':'|'.join(key),'baseline_count':len(inds),'survivors':ns})
    stratum_recall=None if not strata else strata_kept/len(strata)
    return {
        'baseline_target_count':n,'basin_count':len(clusters),'basin_recall':basin_recall,
        'min_target_survivors_per_basin':min_surv,'min_basin_geometric_coverage':min_cov,'max_basin_centroid_drift':max_drift,
        'unclustered_target_fraction':unclustered_frac,'signature_strata_count':len(strata),'signature_stratum_recall':stratum_recall,
        'basins':details,'signature_strata':strata_details
    }


def preservation(target_mechanisms: list[Any], survivor_mask_on_targets: list[bool], *, eps:float=EPS, min_neighbors:int=MIN_NEIGHBORS, coverage_radius:float=EPS, min_basin_survivors:int=20) -> dict:
    """Reference path retained for compatibility and regression testing."""
    baseline=prepare_preservation_baseline(target_mechanisms,eps=eps,min_neighbors=min_neighbors)
    return preservation_from_baseline(baseline,survivor_mask_on_targets,coverage_radius=coverage_radius,min_basin_survivors=min_basin_survivors,include_details=True)


def passes_frozen_requirements(p: dict) -> bool:
    return bool(
        p.get('basin_count',0)>=1 and p.get('basin_recall')==1.0 and
        p.get('min_target_survivors_per_basin',0)>=20 and
        (p.get('min_basin_geometric_coverage') is not None and p['min_basin_geometric_coverage']>=0.95) and
        (p.get('max_basin_centroid_drift') is not None and p['max_basin_centroid_drift']<=0.125) and
        (p.get('unclustered_target_fraction') is not None and p['unclustered_target_fraction']<=0.05) and
        p.get('signature_stratum_recall')==1.0
    )
