from __future__ import annotations

import math
import numpy as np
import pandas as pd
from scipy import ndimage as ndi

from .physics import interior_slices


STRUCT26 = np.ones((3, 3, 3), dtype=np.uint8)


def _labels_touching_retained_boundary(labels: np.ndarray, margin: int):
    if margin <= 0:
        planes = [
            labels[0, :, :], labels[-1, :, :],
            labels[:, 0, :], labels[:, -1, :],
            labels[:, :, 0], labels[:, :, -1],
        ]
    else:
        z0, z1 = margin, labels.shape[0] - margin - 1
        y0, y1 = margin, labels.shape[1] - margin - 1
        x0, x1 = margin, labels.shape[2] - margin - 1
        planes = [
            labels[z0, :, :], labels[z1, :, :],
            labels[:, y0, :], labels[:, y1, :],
            labels[:, :, x0], labels[:, :, x1],
        ]
    touched = set()
    for p in planes:
        touched.update(int(x) for x in np.unique(p) if x > 0)
    return touched


def segment_q_objects(
    q: np.ndarray,
    enstrophy: np.ndarray,
    helicity: np.ndarray,
    *,
    q_rms_multiplier: float,
    margin_cells: int,
    min_voxels: int,
    discard_touching: bool,
):
    """
    Segment Q-threshold objects and return compact int32 labels + threshold info.
    """
    sl = interior_slices(q.shape, margin_cells)
    q_int = q[sl]
    q_rms = float(np.sqrt(np.mean(q_int.astype(np.float64) ** 2)))
    threshold = float(q_rms_multiplier * q_rms)

    mask = np.zeros(q.shape, dtype=bool)
    if q_rms > 0:
        mask[sl] = q_int >= threshold

    labels, _ = ndi.label(mask, structure=STRUCT26)
    del mask

    counts = np.bincount(labels.ravel())
    keep = np.ones(len(counts), dtype=bool)
    keep[0] = False
    keep &= counts >= int(min_voxels)

    touching = set()
    if discard_touching and labels.max() > 0:
        touching = _labels_touching_retained_boundary(labels, margin_cells)
        if touching:
            keep[list(touching)] = False

    ids = np.flatnonzero(keep)
    lookup = np.zeros(len(counts), dtype=np.int32)
    lookup[ids] = np.arange(1, len(ids) + 1, dtype=np.int32)
    compact = lookup[labels]
    del labels, lookup

    return compact, {
        "q_rms": q_rms,
        "q_threshold": threshold,
        "raw_component_count": int(len(counts) - 1),
        "kept_component_count": int(len(ids)),
        "discarded_small_or_boundary": int((len(counts) - 1) - len(ids)),
        "touching_component_count": int(len(touching)),
    }


def object_table(
    labels: np.ndarray,
    q: np.ndarray,
    enstrophy: np.ndarray,
    helicity: np.ndarray,
    *,
    time_idx: int,
    time_value: float,
    scale_idx: int,
    factor: int,
    spacing_native: float,
    origin_xyz: tuple[float, float, float],
):
    n = int(labels.max())
    if n == 0:
        return pd.DataFrame(columns=[
            "node_id","time_idx","time_value","scale_idx","scale_value",
            "object_id","size","weight","voxel_count","physical_volume",
            "cx","cy","cz","equiv_radius","q_mean","q_max",
            "enstrophy_mean","enstrophy_integral","enstrophy_max",
            "helicity_mean","helicity_integral"
        ])

    ids = np.arange(1, n + 1, dtype=np.int32)
    counts = np.bincount(labels.ravel(), minlength=n+1)[1:].astype(np.int64)

    q_sum = ndi.sum(q, labels, ids)
    q_max = ndi.maximum(q, labels, ids)
    e_sum = ndi.sum(enstrophy, labels, ids)
    e_max = ndi.maximum(enstrophy, labels, ids)
    h_sum = ndi.sum(helicity, labels, ids)

    foreground = (labels > 0).astype(np.uint8)
    centers_zyx = ndi.center_of_mass(foreground, labels, ids)
    del foreground

    cell_spacing = spacing_native * factor
    cell_volume = cell_spacing ** 3
    offset = 0.5 * (factor - 1) * spacing_native
    x0, y0, z0 = origin_xyz

    rows = []
    for j, lab in enumerate(ids):
        zc, yc, xc = centers_zyx[j]
        physical_volume = float(counts[j] * cell_volume)
        ens_integral = float(e_sum[j] * cell_volume)
        hel_integral = float(h_sum[j] * cell_volume)
        equiv_radius = float((3.0 * physical_volume / (4.0 * math.pi)) ** (1.0/3.0))
        node_id = f"t{time_idx:02d}_s{scale_idx:02d}_o{int(lab):06d}"
        rows.append({
            "node_id": node_id,
            "time_idx": int(time_idx),
            "time_value": float(time_value),
            "scale_idx": int(scale_idx),
            "scale_value": float(cell_spacing),
            "object_id": f"o{int(lab):06d}",
            "size": physical_volume,
            "weight": ens_integral,
            "voxel_count": int(counts[j]),
            "physical_volume": physical_volume,
            "cx": float(x0 + offset + xc * cell_spacing),
            "cy": float(y0 + offset + yc * cell_spacing),
            "cz": float(z0 + offset + zc * cell_spacing),
            "equiv_radius": equiv_radius,
            "q_mean": float(q_sum[j] / counts[j]),
            "q_max": float(q_max[j]),
            "enstrophy_mean": float(e_sum[j] / counts[j]),
            "enstrophy_integral": ens_integral,
            "enstrophy_max": float(e_max[j]),
            "helicity_mean": float(h_sum[j] / counts[j]),
            "helicity_integral": hel_integral,
        })
    return pd.DataFrame(rows)
