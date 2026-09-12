from __future__ import annotations

import numpy as np


N_TIME = 51
N_DIM = 20
SEED = 20260819


def base_vector(n_dim: int = N_DIM) -> np.ndarray:
    x = np.linspace(0.2, 2.8, n_dim)
    a = np.sin(x) + 0.35 * np.cos(np.linspace(0.1, 4.0, n_dim))
    return a / np.sqrt(np.mean(a * a))


def perfect_period2(n_time: int = N_TIME, n_dim: int = N_DIM) -> np.ndarray:
    a = base_vector(n_dim)
    return np.stack([a if t % 2 == 0 else -a for t in range(n_time)], axis=0)


def noisy_period2(sigma: float, n_time: int = N_TIME, n_dim: int = N_DIM) -> np.ndarray:
    """
    Additive observational/state noise applied to a deterministic period-2
    trajectory. A single frozen noise realization is scaled by sigma so the
    sweep is nested and reproducible.
    """
    base = perfect_period2(n_time, n_dim)
    rng = np.random.default_rng(SEED)
    noise = rng.normal(size=base.shape)
    return base + float(sigma) * noise


def damped_period2(gamma: float, n_time: int = N_TIME, n_dim: int = N_DIM) -> np.ndarray:
    """
    Ordinary transient period doubling with an exponentially decaying
    amplitude. No stochastic term is added.
    """
    base = perfect_period2(n_time, n_dim)
    t = np.arange(n_time, dtype=float)[:, None]
    return base * np.exp(-float(gamma) * t)


def iid_random(n_time: int = N_TIME, n_dim: int = N_DIM) -> np.ndarray:
    rng = np.random.default_rng(SEED)
    return rng.normal(size=(n_time, n_dim))


def logistic_ensemble(r: float, n_time: int = N_TIME, n_dim: int = N_DIM, burn: int = 500) -> np.ndarray:
    """
    Classical logistic-map ensemble:

        x_(t+1) = r x_t (1 - x_t)

    Twenty initial conditions are evolved in parallel. The 20-dimensional
    vector is the state X_t supplied to the frozen temporal-closure metric.
    The burn-in removes transient approach to the attractor.

    r=3.2  -> stable period-2 attractor
    r=3.5  -> stable period-4 attractor
    r=4.0  -> chaotic regime
    """
    x = np.linspace(0.07, 0.93, n_dim, dtype=float)
    for _ in range(int(burn)):
        x = float(r) * x * (1.0 - x)
    out = []
    for _ in range(n_time):
        out.append(x.copy())
        x = float(r) * x * (1.0 - x)
    return np.asarray(out, dtype=float)


def selected_controls() -> dict[str, np.ndarray]:
    return {
        "perfect_2T": perfect_period2(),
        "noisy_2T_sigma_0p20": noisy_period2(0.20),
        "damped_2T_gamma_0p10": damped_period2(0.10),
        "iid_random": iid_random(),
        "logistic_period2_r3p20": logistic_ensemble(3.20),
        "logistic_period4_r3p50": logistic_ensemble(3.50),
        "logistic_chaos_r4p00": logistic_ensemble(4.00),
    }
