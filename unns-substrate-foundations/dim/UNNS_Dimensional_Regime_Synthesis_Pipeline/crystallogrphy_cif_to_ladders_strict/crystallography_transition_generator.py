from __future__ import annotations

import math
import zipfile
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

try:
    from pymatgen.core import Structure
except ImportError as exc:
    raise SystemExit(
        "This script requires pymatgen.\n"
        "Install it with:\n"
        "pip install pymatgen"
    ) from exc


BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "crystallography_cifs_input"
OUTPUT_LADDERS_DIR = BASE_DIR / "crystal_ladders_expanded"
OUTPUT_TRANSITIONS_DIR = BASE_DIR / "crystal_transition_data"

OUTPUT_LADDERS_DIR.mkdir(exist_ok=True)
OUTPUT_TRANSITIONS_DIR.mkdir(exist_ok=True)

B_VALUES = np.linspace(0.0, 1.0, 100)

# Expand small/asymmetric cells into a meaningful atomic cloud
SUPERCELL = (3, 3, 3)

# Distance cutoff keeps the ladder structural and avoids huge O(N^2) blowups
DISTANCE_CUTOFF_ANGSTROM = 8.0

# Need enough distances for a meaningful covariance/gap analysis
MIN_DISTANCES = 20


def iter_cif_files(folder: Path) -> Iterable[Path]:
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix.lower() == ".cif":
            yield p


def sanitize_name(name: str) -> str:
    bad = '<>:"/\\|?*'
    out = []
    for ch in name:
        out.append("_" if ch in bad else ch)
    return "".join(out)


def load_and_expand_structure(cif_path: Path) -> Structure:
    structure = Structure.from_file(str(cif_path))
    expanded = structure.copy()
    expanded.make_supercell(SUPERCELL)
    return expanded


def pairwise_distances_cartesian(cart_coords: np.ndarray, cutoff: float) -> np.ndarray:
    n = len(cart_coords)
    if n < 2:
        return np.array([], dtype=float)

    dists: list[float] = []
    for i in range(n - 1):
        delta = cart_coords[i + 1 :] - cart_coords[i]
        ds = np.linalg.norm(delta, axis=1)
        good = ds[(ds > 1e-8) & (ds <= cutoff)]
        if good.size:
            dists.extend(good.tolist())

    if not dists:
        return np.array([], dtype=float)

    return np.sort(np.array(dists, dtype=float))


def save_ladder_csv(values: np.ndarray, out_path: Path) -> None:
    pd.DataFrame({"value": values}).to_csv(out_path, index=False)


def apply_deformation(values: np.ndarray, b: float) -> np.ndarray:
    """
    Mild nonlinear deformation in ladder space.
    Keeps ordering but changes gap geometry.
    """
    idx = np.arange(len(values), dtype=float)
    scale = 1.0 + 0.15 * b + 0.05 * b * np.sin(idx / max(8.0, len(values) / 25.0))
    deformed = values * scale
    return np.sort(deformed)


def compute_gaps(values: np.ndarray) -> np.ndarray:
    gaps = np.diff(values)
    return gaps[gaps > 1e-12]


def compute_margin(gaps: np.ndarray) -> float | None:
    if len(gaps) < 3:
        return None
    med = float(np.median(gaps))
    mad = float(np.median(np.abs(gaps - med)))
    denom = med + mad
    if denom <= 0:
        return None
    return med / denom


def compute_alpha(gaps: np.ndarray) -> float | None:
    if len(gaps) < 5:
        return None
    x = np.arange(1, len(gaps) + 1, dtype=float)
    y = np.sort(np.abs(gaps)) + 1e-12
    try:
        slope, _ = np.polyfit(np.log(x), np.log(y), 1)
        return float(slope)
    except Exception:
        return None


def compute_gamma(values: np.ndarray) -> float | None:
    if len(values) < 5:
        return None
    x = np.arange(1, len(values) + 1, dtype=float)
    y = np.sort(np.abs(values)) + 1e-12
    try:
        slope, _ = np.polyfit(np.log(x), np.log(y), 1)
        return float(slope)
    except Exception:
        return None


def compute_dim(gaps: np.ndarray) -> int | None:
    if len(gaps) < 6:
        return None

    # same spirit as your extractor: covariance of local gap triplets
    X = np.array([[gaps[i], gaps[i + 1], gaps[i + 2]] for i in range(len(gaps) - 2)], dtype=float)
    std = X.std(axis=0)
    std[std == 0] = 1.0
    X = (X - X.mean(axis=0)) / std

    cov = np.cov(X, rowvar=False)
    eig = np.linalg.eigvalsh(cov)
    eig = np.sort(eig)[::-1]

    total = eig.sum()
    if total <= 0:
        return 1

    return int(np.sum((eig / total) > 0.10))


def process_cif(cif_path: Path) -> tuple[bool, str]:
    try:
        structure = load_and_expand_structure(cif_path)
    except Exception as e:
        return False, f"[FAIL] {cif_path.name}: could not parse/expand ({e})"

    cart = np.array(structure.cart_coords, dtype=float)
    dists = pairwise_distances_cartesian(cart, DISTANCE_CUTOFF_ANGSTROM)

    if len(dists) < MIN_DISTANCES:
        return False, f"[FAIL] {cif_path.name}: not enough distances ({len(dists)})"

    stem = sanitize_name(cif_path.stem)

    ladder_path = OUTPUT_LADDERS_DIR / f"{stem}_ladder.csv"
    save_ladder_csv(dists, ladder_path)

    rows = []
    for b in B_VALUES:
        deformed = apply_deformation(dists, float(b))
        gaps = compute_gaps(deformed)

        rows.append(
            {
                "file": ladder_path.name,
                "B": float(b),
                "alpha": compute_alpha(gaps),
                "gamma": compute_gamma(deformed),
                "m": compute_margin(gaps),
                "dim": compute_dim(gaps),
            }
        )

    transition_path = OUTPUT_TRANSITIONS_DIR / f"{stem}_transition.csv"
    pd.DataFrame(rows).to_csv(transition_path, index=False)

    return True, (
        f"[OK] {cif_path.name} -> "
        f"{ladder_path.name} ({len(dists)} distances), "
        f"{transition_path.name}"
    )


def zip_outputs() -> None:
    ladder_zip = BASE_DIR / "crystal_ladders_expanded.zip"
    with zipfile.ZipFile(ladder_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(OUTPUT_LADDERS_DIR.glob("*.csv")):
            zf.write(p, arcname=p.name)

    transition_zip = BASE_DIR / "crystal_transition_data.zip"
    with zipfile.ZipFile(transition_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(OUTPUT_TRANSITIONS_DIR.glob("*.csv")):
            zf.write(p, arcname=p.name)


def main() -> None:
    if not INPUT_DIR.exists():
        raise SystemExit(
            f"Input folder not found:\n{INPUT_DIR}\n\n"
            "Create it and put your CIF files there."
        )

    cifs = list(iter_cif_files(INPUT_DIR))
    if not cifs:
        raise SystemExit(f"No CIF files found in:\n{INPUT_DIR}")

    ok = 0
    fail = 0

    for cif in cifs:
        success, message = process_cif(cif)
        print(message)
        if success:
            ok += 1
        else:
            fail += 1

    zip_outputs()

    print("\n=== SUMMARY ===")
    print(f"Valid structures: {ok}")
    print(f"Rejected structures: {fail}")
    print(f"Ladders: {OUTPUT_LADDERS_DIR}")
    print(f"Transitions: {OUTPUT_TRANSITIONS_DIR}")
    print(f"Zips: {BASE_DIR / 'crystal_ladders_expanded.zip'}")
    print(f"      {BASE_DIR / 'crystal_transition_data.zip'}")


if __name__ == "__main__":
    main()