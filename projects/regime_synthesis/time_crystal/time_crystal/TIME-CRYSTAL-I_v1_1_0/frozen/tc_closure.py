from __future__ import annotations

from pathlib import Path
import sys
import numpy as np


def load_phys_module(phys_root: str | Path):
    phys_root = Path(phys_root).resolve()
    src = phys_root / "src"
    if not (src / "tc_phys.py").exists():
        raise FileNotFoundError(f"Frozen physics module not found: {src / 'tc_phys.py'}")
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    import tc_phys
    return tc_phys


def reconstruct_unaligned_trajectory(tc_phys, name: str, arr: np.ndarray,
                                     W0: float = 0.15,
                                     Wf_ratio: float = 2.0/3.0):
    """
    Reuse the frozen TC_PHYS_v001 correction/mitigation layer, then restore
    the original stroboscopic sign sequence.

    TC_PHYS aligns the ideal 2T alternation only to fit the hardware-decay
    envelope. That alignment MUST NOT enter the closure search, otherwise q=2
    would be built into the data. We therefore invert it before any closure
    metric is calculated.
    """
    rec = tc_phys.prepare_record(name, arr)
    mit = tc_phys.mitigate_record(rec, W0=W0, Wf_ratio=Wf_ratio)

    corrected_targets = np.stack(
        [tc_phys.measurement_correct(arr[k]) for k in range(1, tc_phys.N_ITER)],
        axis=0,
    )
    original_corrected_mean = np.nanmean(corrected_targets, axis=0)
    s0 = np.sign(original_corrected_mean[0]).astype(float)
    s0[s0 == 0] = 1.0

    # Inverse of align_period2: aligned = original * s0 * (-1)^t.
    original_mitigated = (
        mit["aligned_mitigated"]
        * s0[None, :]
        * tc_phys.PARITY[:, None]
    )
    return rec, mit, original_mitigated


def pair_closure(x: np.ndarray, y: np.ndarray, amp0: float) -> tuple[float, float, float]:
    """
    Bounded state-recurrence score.

    similarity = 1 - ||x-y|| / (||x||+||y||)
    support    = min(RMS(x), RMS(y)) / early-time RMS reference, clipped [0,1]
    closure    = similarity * support

    The support term prevents a thermalized near-zero state from being
    misclassified as strongly closed merely because 0 ~ 0.
    """
    nx = float(np.linalg.norm(x))
    ny = float(np.linalg.norm(y))
    denom = nx + ny
    similarity = 1.0 - (float(np.linalg.norm(x-y)) / (denom + 1e-12))
    similarity = float(np.clip(similarity, 0.0, 1.0))

    n = max(1, x.size)
    support = min(nx, ny) / (np.sqrt(n) * (amp0 + 1e-12))
    support = float(np.clip(support, 0.0, 1.0))
    return similarity * support, similarity, support


def closure_spectrum(x_tq: np.ndarray, accepted: np.ndarray,
                     qmax: int = 10, early_points: int = 5):
    """
    Generic temporal closure spectrum C(q), q=1..qmax.
    No physical phase label and no published epsilon_c enter this calculation.
    """
    X = x_tq[:, accepted]
    if X.shape[1] < 2:
        raise ValueError("Too few accepted qubits for closure calculation")

    rms = np.linalg.norm(X, axis=1) / np.sqrt(X.shape[1])
    amp0 = float(np.nanmedian(rms[:early_points]))
    if not np.isfinite(amp0) or amp0 <= 1e-12:
        raise ValueError("Invalid early-time amplitude reference")

    rows = []
    ladder_rows = []
    for q in range(1, qmax+1):
        vals, sims, sups = [], [], []
        by_residue = {r: [] for r in range(q)}
        for t in range(0, X.shape[0]-q):
            c, s, a = pair_closure(X[t], X[t+q], amp0)
            vals.append(c)
            sims.append(s)
            sups.append(a)
            by_residue[t % q].append(c)

        rows.append({
            "q": q,
            "closure": float(np.nanmean(vals)),
            "similarity": float(np.nanmean(sims)),
            "support": float(np.nanmean(sups)),
            "n_pairs": len(vals),
        })
        for r in range(q):
            vv = np.asarray(by_residue[r], dtype=float)
            ladder_rows.append({
                "q": q,
                "residue": r,
                "ladder_closure": float(np.nanmean(vv)) if vv.size else np.nan,
                "n_pairs": int(vv.size),
            })

    return rows, ladder_rows, amp0


def local_contrasts(spec_rows: list[dict]) -> dict[int, float]:
    c = {r["q"]: r["closure"] for r in spec_rows}
    out = {}
    for q in range(2, max(c)):
        out[q] = float(c[q] - 0.5 * (c[q-1] + c[q+1]))
    return out


def detect_fundamental_q(aggregate_spec: list[dict]) -> dict:
    """
    Fundamental recurrence depth is selected without hard-coding q=2:
    choose q in 2..qmax-1 with the largest local spectral contrast.
    """
    contrasts = local_contrasts(aggregate_spec)
    q0 = max(contrasts, key=contrasts.get)
    return {
        "q0": int(q0),
        "local_contrast": float(contrasts[q0]),
        "all_local_contrasts": {str(k): float(v) for k, v in contrasts.items()},
    }


def family_contrast(spec_rows: list[dict], q0: int) -> dict:
    """
    Once q0 is detected, compare its recurrence family (multiples of q0)
    with non-family depths. This generalizes the even-vs-odd contrast.
    """
    fam = [r["closure"] for r in spec_rows if r["q"] % q0 == 0]
    non = [r["closure"] for r in spec_rows if r["q"] % q0 != 0]
    return {
        "family_mean": float(np.nanmean(fam)),
        "nonfamily_mean": float(np.nanmean(non)),
        "family_contrast": float(np.nanmean(fam) - np.nanmean(non)),
    }


def plateau_exit_boundary(scan_rows: list[dict], key: str = "family_contrast",
                          seed_n: int = 5, sigma_mult: float = 3.0,
                          consecutive: int = 2) -> dict:
    """
    Exploratory basin-edge rule fixed in TC_CLOSURE_v001:
    - use the first `seed_n` epsilon points as the low-perturbation seed basin;
    - robust center = median;
    - robust sigma = 1.4826*MAD;
    - lower edge = center - sigma_mult*robust_sigma;
    - boundary = first epsilon at which `consecutive` values lie below the edge.

    This rule does not receive the published physical transition as input.
    """
    rows = sorted(scan_rows, key=lambda r: r["epsilon"])
    x = np.asarray([r["epsilon"] for r in rows], dtype=float)
    y = np.asarray([r[key] for r in rows], dtype=float)

    if len(y) < seed_n + consecutive:
        raise ValueError("Too few epsilon points for plateau-exit detector")

    base = y[:seed_n]
    center = float(np.nanmedian(base))
    mad = float(np.nanmedian(np.abs(base-center)))
    robust_sigma = 1.4826 * mad
    threshold = center - sigma_mult * robust_sigma

    boundary = np.nan
    boundary_index = None
    below = y < threshold
    for i in range(seed_n, len(y)-consecutive+1):
        if np.all(below[i:i+consecutive]):
            boundary = float(x[i])
            boundary_index = int(i)
            break

    return {
        "key": key,
        "seed_n": seed_n,
        "sigma_mult": sigma_mult,
        "consecutive": consecutive,
        "baseline_median": center,
        "baseline_MAD": mad,
        "baseline_robust_sigma": robust_sigma,
        "lower_threshold": float(threshold),
        "boundary_epsilon": boundary,
        "boundary_index": boundary_index,
    }


def shuffle_null(x_tq: np.ndarray, accepted: np.ndarray, q: int,
                 n_surrogates: int = 200, seed: int = 20260819) -> dict:
    """
    Time-order permutation null. It preserves the set of state vectors and
    amplitudes but destroys their temporal order.
    """
    observed = closure_spectrum(x_tq, accepted, qmax=q)[0][q-1]["closure"]
    rng = np.random.default_rng(seed)
    null = []
    for _ in range(n_surrogates):
        perm = rng.permutation(x_tq.shape[0])
        c = closure_spectrum(x_tq[perm], accepted, qmax=q)[0][q-1]["closure"]
        null.append(c)
    null = np.asarray(null, dtype=float)
    p = (1 + int(np.sum(null >= observed))) / (n_surrogates + 1)
    return {
        "q": q,
        "observed": float(observed),
        "null_mean": float(np.mean(null)),
        "null_std": float(np.std(null, ddof=1)),
        "null_q95": float(np.quantile(null, 0.95)),
        "null_q99": float(np.quantile(null, 0.99)),
        "empirical_p_ge": float(p),
        "n_surrogates": int(n_surrogates),
        "seed": int(seed),
    }
