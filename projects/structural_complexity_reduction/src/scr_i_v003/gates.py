from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


GATE_ORDER = ("G1", "G2", "G3", "G4")


@dataclass(frozen=True, slots=True)
class GateVerdict:
    G1: bool
    G2: bool
    G3: bool
    G4: bool

    @property
    def passed(self) -> bool:
        return self.G1 and self.G2 and self.G3 and self.G4

    def as_dict(self) -> dict[str, bool]:
        return {"G1": self.G1, "G2": self.G2, "G3": self.G3, "G4": self.G4}

    def first_reject(self) -> str | None:
        for g in GATE_ORDER:
            if not getattr(self, g):
                return g
        return None


def evaluate_gates(m: Any) -> GateVerdict:
    g1 = m.curvature_method == "turning_angle"
    g2 = m.delta_kappa > 0.05
    if not m.has_bifurcation:
        g3 = False
    elif m.sharpness >= 0.10:
        g3 = bool(m.temporal_signature_valid)
    elif m.sharpness < 0.08:
        g3 = False
    else:
        g3 = m.temporal_quality >= 0.70
    g4 = m.locality_score < 0.10
    return GateVerdict(g1, g2, g3, g4)


def timed_chain_count(m: Any) -> tuple[bool, str | None, int]:
    """Frozen G1→G2→G3→G4 early-termination chain.

    Returns pass, first reject, and primitive gate predicates executed.
    """
    count = 1
    if m.curvature_method != "turning_angle":
        return False, "G1", count
    count += 1
    if not (m.delta_kappa > 0.05):
        return False, "G2", count
    count += 1
    if not m.has_bifurcation:
        return False, "G3", count
    if m.sharpness >= 0.10:
        g3 = bool(m.temporal_signature_valid)
    elif m.sharpness < 0.08:
        g3 = False
    else:
        g3 = m.temporal_quality >= 0.70
    if not g3:
        return False, "G3", count
    count += 1
    if not (m.locality_score < 0.10):
        return False, "G4", count
    return True, None, count


def audit(pool: Iterable[Any]) -> tuple[list[dict], dict]:
    rows = []
    overlap = {g: {h: 0 for h in GATE_ORDER} for g in GATE_ORDER}
    unique = {g: 0 for g in GATE_ORDER}
    first = {g: 0 for g in GATE_ORDER}
    reject = {g: 0 for g in GATE_ORDER}
    survivors = 0
    primitive_timed = 0

    for m in pool:
        v = evaluate_gates(m)
        vd = v.as_dict()
        failed = [g for g in GATE_ORDER if not vd[g]]
        for g in failed:
            reject[g] += 1
            for h in failed:
                overlap[g][h] += 1
        if len(failed) == 1:
            unique[failed[0]] += 1
        passed, first_reject, n_eval = timed_chain_count(m)
        primitive_timed += n_eval
        if first_reject:
            first[first_reject] += 1
        if passed:
            survivors += 1
        rows.append({
            "candidate_id": m.candidate_id,
            **vd,
            "scr_pass": passed,
            "first_reject": first_reject or "",
            "timed_gate_evals": n_eval,
        })

    summary = {
        "n": len(rows),
        "survivors": survivors,
        "rejected": len(rows) - survivors,
        "reject": reject,
        "unique_reject": unique,
        "first_reject": first,
        "overlap": overlap,
        "timed_gate_evals": primitive_timed,
    }
    return rows, summary
