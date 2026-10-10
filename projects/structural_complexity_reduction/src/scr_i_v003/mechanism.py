from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable

from .rng import P4LCG


CURVATURE_METHODS = ["turning_angle", "finite_diff", "smoothed", "biased", "wrong_metric"]
LOCALITY_MODES = ["local", "bounded_nonlocal", "nonlocal_global", "teleport"]
BIFURCATION_SPOOFS = ["none", "remote_step", "hysteresis_loop"]
REGIME_FLIP_INJECTORS = ["none", "seed_sensitive", "gamma_sensitive"]
FAMILIES = ["flat", "saif", "curvature_gated", "logit_sigmoid"]
COMPOSITIONS = ["utility_count", "logit_sigmoid"]

P4_BASELINE = {
    "G3_s_lo": 0.08,
    "G3_s_hi": 0.10,
    "G3_T_min": 0.70,
    "G4_locality_strict": 0.10,
    "generator_mix": {"boundary": 0.50, "pathological": 0.30, "broad": 0.20},
}


@dataclass(slots=True)
class Mechanism:
    candidate_id: str
    source_id: str
    candidate_index: int
    generator_mode: str
    seed: int
    gamma0: float
    beta: float
    d: float
    kmax: float
    curvature_method: str
    locality_mode: str
    bifurcation_spoof: str
    regime_flip_injector: str
    family: str
    composition: str
    delta_kappa_target: float
    sharpness_target: float
    locality_budget: float
    delta_kappa: float
    has_bifurcation: bool
    sharpness: float
    temporal_signature_valid: bool
    temporal_quality: float
    locality_score: float
    cov_010: float
    cov_020: float
    kappa: float
    regime_base: str
    regime: str

    def to_dict(self) -> dict:
        return asdict(self)


def _choice(values: list[str], rng: P4LCG) -> str:
    return values[int(rng.random() * len(values))]


def _compute_observables(raw: dict, rng: P4LCG) -> dict:
    # Exact Chamber LIII v3.1.0 ordering and JS `||` behavior for nonzero targets.
    delta_kappa = raw.get("delta_kappa_target") or 0.1
    if raw["curvature_method"] == "biased":
        delta_kappa *= 1.3
    if raw["curvature_method"] == "wrong_metric":
        delta_kappa *= 0.7
    if raw["curvature_method"] == "smoothed":
        delta_kappa *= 0.95
    raw["delta_kappa"] = delta_kappa

    has_bifurcation = raw["gamma0"] > 0.3 and raw["beta"] > 0.2
    if raw["bifurcation_spoof"] != "none":
        has_bifurcation = True
    raw["has_bifurcation"] = has_bifurcation

    sharpness = raw.get("sharpness_target") or (rng.random() * 0.5)
    if raw["bifurcation_spoof"] == "remote_step":
        sharpness *= 0.6
    raw["sharpness"] = sharpness

    raw["temporal_signature_valid"] = raw["bifurcation_spoof"] == "none"

    if raw["bifurcation_spoof"] == "none":
        sharp_contrib = min(1.0, raw["sharpness"] / 0.15)
        noise_floor = 0.05 * (rng.random() - 0.5)
        raw["temporal_quality"] = max(0.0, min(1.0, 0.5 + 0.5 * sharp_contrib + noise_floor))
    elif raw["bifurcation_spoof"] == "remote_step":
        raw["temporal_quality"] = 0.15 + rng.random() * 0.25
    else:
        raw["temporal_quality"] = 0.30 + rng.random() * 0.20

    locality_score = raw.get("locality_budget") or 0.0
    if raw["locality_mode"] == "local":
        locality_score = 0.02 + rng.random() * 0.03
    if raw["locality_mode"] == "bounded_nonlocal":
        locality_score = 0.08 + rng.random() * 0.1
    if raw["locality_mode"] == "nonlocal_global":
        locality_score = 0.3 + rng.random() * 0.3
    if raw["locality_mode"] == "teleport":
        locality_score = 0.7 + rng.random() * 0.3
    raw["locality_score"] = locality_score

    raw["cov_010"] = rng.random()
    raw["cov_020"] = rng.random()
    raw["kappa"] = 1.5 + rng.random() * 0.5
    raw["regime_base"] = ["R2", "R3", "R4"][int(rng.random() * 3)]
    raw["regime"] = raw["regime_base"]
    return raw


def generate_pool(count: int, seed: int, strategy: str = "adversarial") -> list[Mechanism]:
    if strategy != "adversarial":
        raise ValueError("SCR-I-A freezes strategy='adversarial'")
    rng = P4LCG(seed)
    out: list[Mechanism] = []
    mix = P4_BASELINE["generator_mix"]

    for idx in range(count):
        u = rng.random()
        mode = "boundary" if u < mix["boundary"] else ("pathological" if u < mix["boundary"] + mix["pathological"] else "broad")

        source_suffix = int(rng.random() * 10000)
        raw = {
            "source_id": f"M_0_{source_suffix}",
            "candidate_id": f"S{seed}_I{idx:06d}_{source_suffix:04d}",
            "candidate_index": idx,
            "generator_mode": mode,
            "seed": int(seed),
            "gamma0": 0.0,
            "beta": 0.0,
            "d": 0.0,
            "kmax": 0.0,
            "curvature_method": "",
            "locality_mode": "",
            "bifurcation_spoof": "",
            "regime_flip_injector": "",
            "family": "",
            "composition": "",
            "delta_kappa_target": 0.0,
            "sharpness_target": 0.0,
            "locality_budget": 0.0,
        }

        if mode == "boundary":
            raw["gamma0"] = rng.random() * 2.0
            raw["beta"] = rng.random() * 2.0
            raw["d"] = rng.random() * 5.0
            raw["kmax"] = rng.random() * 6.0
            raw["delta_kappa_target"] = 0.05 + (rng.random() - 0.5) * 0.04
            g3_lo, g3_hi = 0.08, 0.10
            g3_mid = (g3_lo + g3_hi) / 2.0
            g3_span = (g3_hi - g3_lo) / 2.0 + 0.02
            raw["sharpness_target"] = g3_mid + (rng.random() - 0.5) * 2.0 * g3_span
            raw["locality_budget"] = (0.10 - 0.05) + (rng.random() - 0.5) * 0.1
            raw["curvature_method"] = "turning_angle" if rng.random() < 0.8 else "finite_diff"
            raw["locality_mode"] = "local" if rng.random() < 0.7 else "bounded_nonlocal"
            raw["bifurcation_spoof"] = "none"
            raw["regime_flip_injector"] = "none"
        elif mode == "pathological":
            raw["gamma0"] = rng.random() * 2.0
            raw["beta"] = rng.random() * 2.0
            raw["d"] = rng.random() * 5.0
            raw["kmax"] = rng.random() * 6.0
            raw["curvature_method"] = ["biased", "wrong_metric", "smoothed"][int(rng.random() * 3)]
            raw["locality_mode"] = "nonlocal_global" if rng.random() < 0.5 else "teleport"
            raw["locality_budget"] = 0.3 + rng.random() * 0.5
            raw["bifurcation_spoof"] = "remote_step" if rng.random() < 0.5 else "hysteresis_loop"
            raw["regime_flip_injector"] = "seed_sensitive" if rng.random() < 0.5 else "gamma_sensitive"
            raw["delta_kappa_target"] = rng.random() * 0.3
            raw["sharpness_target"] = rng.random() * 0.5
        else:
            raw["gamma0"] = rng.random() * 2.0
            raw["beta"] = rng.random() * 2.0
            raw["d"] = rng.random() * 5.0
            raw["kmax"] = rng.random() * 6.0
            raw["curvature_method"] = _choice(CURVATURE_METHODS, rng)
            raw["locality_mode"] = _choice(LOCALITY_MODES, rng)
            raw["bifurcation_spoof"] = _choice(BIFURCATION_SPOOFS, rng)
            raw["regime_flip_injector"] = _choice(REGIME_FLIP_INJECTORS, rng)
            raw["delta_kappa_target"] = rng.random() * 0.3
            raw["sharpness_target"] = rng.random() * 0.5
            raw["locality_budget"] = rng.random() * 0.8

        raw["family"] = _choice(FAMILIES, rng)
        raw["composition"] = _choice(COMPOSITIONS, rng)
        raw = _compute_observables(raw, rng)
        out.append(Mechanism(**raw))

    return out


def pool_as_dicts(pool: Iterable[Mechanism]) -> list[dict]:
    return [m.to_dict() for m in pool]
