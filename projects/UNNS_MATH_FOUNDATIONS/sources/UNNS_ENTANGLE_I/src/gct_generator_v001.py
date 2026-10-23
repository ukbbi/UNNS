from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from itertools import product
from typing import Dict, List, Tuple

Outcome = int
JointDist = Dict[Tuple[Outcome, Outcome], float]

@dataclass(frozen=True)
class GCTLock:
    measurement_independence: bool = True
    bell_local_factorization: bool = True
    no_signalling_required: bool = True
    born_rule_import_forbidden_in_generator: bool = True
    comparator_isolated: bool = True


def _sign(x: float) -> int:
    return 1 if x >= 0 else -1


def hidden_variable_grid(num_samples: int = 360) -> List[float]:
    return [2.0 * math.pi * k / num_samples for k in range(num_samples)]


def local_outcomes(a: float, b: float, lam: float) -> Tuple[int, int]:
    A = _sign(math.cos(a - lam))
    B = -_sign(math.cos(b - lam))
    return A, B


def local_joint_distribution(a: float, b: float, num_samples: int = 360) -> JointDist:
    counts = {(+1, +1): 0, (+1, -1): 0, (-1, +1): 0, (-1, -1): 0}
    for lam in hidden_variable_grid(num_samples):
        counts[local_outcomes(a, b, lam)] += 1
    total = float(num_samples)
    return {k: v / total for k, v in counts.items()}


def singlet_distribution(a: float, b: float) -> JointDist:
    delta = a - b
    return {(A, B): 0.25 * (1.0 - A * B * math.cos(delta)) for A, B in product((+1, -1), repeat=2)}


def expectation(dist: JointDist) -> float:
    return sum(A * B * p for (A, B), p in dist.items())


def marginals(dist: JointDist):
    pa = {+1: 0.0, -1: 0.0}
    pb = {+1: 0.0, -1: 0.0}
    for (A, B), p in dist.items():
        pa[A] += p
        pb[B] += p
    return pa, pb


def chsh(distribution_fn, angles: Tuple[float, float, float, float]) -> float:
    a, ap, b, bp = angles
    return expectation(distribution_fn(a, b)) + expectation(distribution_fn(a, bp)) + expectation(distribution_fn(ap, b)) - expectation(distribution_fn(ap, bp))


def grid_search_local_max(num_angles: int = 12, num_samples: int = 360):
    vals = [2.0 * math.pi * k / num_angles for k in range(num_angles)]
    best = -1.0
    best_tuple = None
    dist_fn = lambda x, y: local_joint_distribution(x, y, num_samples)
    for a in vals:
        for ap in vals:
            for b in vals:
                for bp in vals:
                    s = abs(chsh(dist_fn, (a, ap, b, bp)))
                    if s > best:
                        best = s
                        best_tuple = (a, ap, b, bp)
    return {"max_abs_chsh": best, "best_angles": best_tuple, "num_angles": num_angles, "num_hidden_variable_samples": num_samples}


def optimal_quantum_angles() -> Tuple[float, float, float, float]:
    return (0.0, math.pi / 2.0, math.pi / 4.0, -math.pi / 4.0)


def run_gct():
    lock = GCTLock()
    q_angles = optimal_quantum_angles()
    local_dist = local_joint_distribution(q_angles[0], q_angles[2])
    singlet_dist = singlet_distribution(q_angles[0], q_angles[2])
    local_pa, local_pb = marginals(local_dist)
    singlet_pa, singlet_pb = marginals(singlet_dist)
    return {
        "program": "UNNS Entanglement — Generative Correlation Theorem",
        "version": "v001",
        "lock": asdict(lock),
        "benchmark_angles": {"a": q_angles[0], "a_prime": q_angles[1], "b": q_angles[2], "b_prime": q_angles[3]},
        "local_witness": {
            "distribution_at_a_b": {f"{k[0]},{k[1]}": v for k, v in local_dist.items()},
            "marginals_A": local_pa,
            "marginals_B": local_pb,
            "expectation_at_a_b": expectation(local_dist),
            "chsh_at_quantum_angles": chsh(local_joint_distribution, q_angles),
            "grid_search": grid_search_local_max(),
        },
        "quantum_comparator": {
            "distribution_at_a_b": {f"{k[0]},{k[1]}": v for k, v in singlet_dist.items()},
            "marginals_A": singlet_pa,
            "marginals_B": singlet_pb,
            "expectation_at_a_b": expectation(singlet_dist),
            "chsh_at_quantum_angles": chsh(singlet_distribution, q_angles),
        },
        "scientific_verdict": "NO_GO_WITH_LOCAL_FACTORIZATION",
        "summary": "The frozen v001 assumptions remain Bell-local. The local witness stays at or below the CHSH bound while the isolated singlet comparator reaches 2*sqrt(2)."
    }

if __name__ == "__main__":
    print(json.dumps(run_gct(), indent=2, sort_keys=True))
