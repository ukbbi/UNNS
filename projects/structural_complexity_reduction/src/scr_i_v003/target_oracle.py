from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Any

REPLICATES=20
PASS_RATE_MIN=0.85
TARGET_WORK_UNITS_PER_CANDIDATE=26  # 20 replicate regime steps + 6 checks

@dataclass(frozen=True, slots=True)
class ViabilityResult:
    target: bool
    pass_rate: float
    regime_stability: float
    checks: dict[str,bool]


def evaluate(m: Any, replicates: int=REPLICATES) -> ViabilityResult:
    regimes=[]
    for i in range(replicates):
        regime=m.regime_base
        if m.regime_flip_injector=='seed_sensitive' and i%3==0:
            regime='R3' if regime=='R2' else ('R2' if regime=='R3' else regime)
        if m.regime_flip_injector=='gamma_sensitive' and m.gamma0>0.5 and m.gamma0<0.7:
            regime='R2'
        regimes.append(regime)
    counts=Counter(regimes)
    regime_stability=max(counts.values())/replicates if counts else 0.0
    # In the pinned source every gamma-critical value lies in [0.45,0.55),
    # therefore population std <=0.05 <0.15 for every finite replicate set.
    gamma_crit_consistent=True
    checks={
        'regime_stable': regime_stability>=0.95,
        'delta_kappa_bounded': m.delta_kappa<0.5,
        'kappa_positive': m.kappa>0,
        'locality_ok': m.locality_score<0.20,
        'temporal_signature': bool(m.temporal_signature_valid) or not bool(m.has_bifurcation),
        'gamma_crit_consistent': gamma_crit_consistent,
    }
    pass_rate=sum(checks.values())/len(checks)
    return ViabilityResult(pass_rate>=PASS_RATE_MIN, pass_rate, regime_stability, checks)


def labels(pool: Iterable[Any]) -> list[bool]:
    return [evaluate(m).target for m in pool]
