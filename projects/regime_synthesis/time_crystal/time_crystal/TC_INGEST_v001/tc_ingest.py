from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import re
import numpy as np

N_ITER = 5
N_TIME = 51
N_QUBIT = 57
DTYPE = np.float32
EXPECTED_VALUES = N_ITER * N_TIME * N_QUBIT
EXPECTED_BYTES = EXPECTED_VALUES * np.dtype(DTYPE).itemsize

_EPS_RE = re.compile(r"_Eps(\d+)_")


def parse_epsilon_code(code: str) -> float:
    """Decode filename convention: 005->0.05, 01->0.1, 1->1.0."""
    return int(code) / (10 ** (len(code) - 1))


@dataclass(frozen=True)
class RecordMeta:
    filename: str
    device: str
    epsilon_code: str
    epsilon: float
    timesteps: int
    iterations: int
    qubits: int
    initial_state_tag: str
    disorder_tag: str
    special_tag: str

    def to_dict(self):
        return asdict(self)


def parse_meta(path: str | Path) -> RecordMeta:
    name = Path(path).name
    m = _EPS_RE.search(name)
    if not m:
        raise ValueError(f"Cannot parse epsilon from {name}")
    code = m.group(1)
    device = "Brooklyn" if "_Bro57_" in name else "Manhattan" if "_Man57_" in name else "unknown"

    # Conservative filename-only classification. Do not infer beyond explicit tags.
    if "_NEEL" in name:
        init = "neel"
    elif "_POL" in name or "_PolND_" in name:
        init = "polarized"
    elif "_RND_" in name:
        init = "random"
    else:
        init = "unspecified"

    if "NoDIS" in name or "PolND" in name:
        disorder = "no_disorder_tagged"
    elif "RefDis" in name:
        disorder = "reference_disorder_tagged"
    else:
        disorder = "standard_or_unspecified"

    special = ""
    for tag in ("NEEL", "POL", "NoDIS", "RND_RefDis", "PolND_RefDis"):
        if tag in name:
            special = tag
            break

    return RecordMeta(
        filename=name,
        device=device,
        epsilon_code=code,
        epsilon=parse_epsilon_code(code),
        timesteps=N_TIME - 1,
        iterations=N_ITER,
        qubits=N_QUBIT,
        initial_state_tag=init,
        disorder_tag=disorder,
        special_tag=special,
    )


def load_dat(path: str | Path) -> np.ndarray:
    """Load one binary .dat file as [iteration, time, qubit]."""
    path = Path(path)
    if path.stat().st_size != EXPECTED_BYTES:
        raise ValueError(
            f"Unexpected size for {path.name}: {path.stat().st_size} bytes; "
            f"expected {EXPECTED_BYTES}."
        )
    arr = np.fromfile(path, dtype=DTYPE)
    if arr.size != EXPECTED_VALUES:
        raise ValueError(f"Unexpected value count for {path.name}: {arr.size}")
    return arr.reshape(N_ITER, N_TIME, N_QUBIT)


def split_reference_target(arr: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Notebook generation order:
      iteration 0 -> epsilon=0 reference run
      iterations 1..4 -> target-epsilon runs
    """
    if arr.shape != (N_ITER, N_TIME, N_QUBIT):
        raise ValueError(f"Expected {(N_ITER, N_TIME, N_QUBIT)}, got {arr.shape}")
    return arr[0], arr[1:]


def initial_sign(series_tq: np.ndarray) -> np.ndarray:
    s = np.sign(series_tq[0]).astype(float)
    s[s == 0] = 1.0
    return s


def autocorrelation_from_magnetization(series_tq: np.ndarray) -> np.ndarray:
    """Use the measured t=0 sign as the local initial-state label."""
    return series_tq * initial_sign(series_tq)[None, :]


def target_autocorrelation(arr: np.ndarray) -> np.ndarray:
    """Average the four finite-epsilon target runs, then form local autocorrelation."""
    _, target = split_reference_target(arr)
    target_mean = target.mean(axis=0)
    return autocorrelation_from_magnetization(target_mean)


def reference_autocorrelation(arr: np.ndarray) -> np.ndarray:
    ref, _ = split_reference_target(arr)
    return autocorrelation_from_magnetization(ref)


def half_frequency_per_qubit(ac_tq: np.ndarray) -> np.ndarray:
    """Absolute DFT component at 0.5 cycles/Floquet period, normalized by N_time."""
    parity = ((-1.0) ** np.arange(ac_tq.shape[0]))[:, None]
    return np.abs(np.sum(ac_tq * parity, axis=0)) / ac_tq.shape[0]


def staggered(ac_tq: np.ndarray) -> np.ndarray:
    return ac_tq * ((-1.0) ** np.arange(ac_tq.shape[0]))[:, None]


def state_distance(ac_tq: np.ndarray, q: int) -> float:
    """Mean normalized Euclidean distance between site-resolved states q cycles apart."""
    if q <= 0 or q >= ac_tq.shape[0]:
        raise ValueError("q must satisfy 0 < q < number of timesteps")
    a = ac_tq[:-q]
    b = ac_tq[q:]
    num = np.linalg.norm(a - b, axis=1)
    scale = np.linalg.norm(a, axis=1) + np.linalg.norm(b, axis=1) + 1e-12
    return float(np.mean(2.0 * num / scale))
