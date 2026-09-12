from __future__ import annotations

import math
import numpy as np
import pandas as pd


def _expand_labels(labels: np.ndarray, ratio: int):
    if ratio == 1:
        return labels
    x = np.repeat(labels, ratio, axis=0)
    x = np.repeat(x, ratio, axis=1)
    x = np.repeat(x, ratio, axis=2)
    return x


def _feature_similarity(a, b):
    x = float(a)
    y = float(b)
    if not np.isfinite(x) or not np.isfinite(y) or x <= 0 or y <= 0:
        return 0.0
    return float(min(x, y) / max(x, y))


def overlap_relations(
    src_labels: np.ndarray,
    dst_labels: np.ndarray,
    src_objects: pd.DataFrame,
    dst_objects: pd.DataFrame,
    *,
    axis: str,
    src_factor: int,
    dst_factor: int,
    spacing_native: float,
):
    """
    Exact positive-overlap route candidates.

    For scale routing, dst_factor must be an integer multiple of src_factor.
    The coarse destination labels are expanded exactly to the source block grid.
    """
    if axis not in ("scale", "time"):
        raise ValueError(axis)

    if axis == "scale":
        if dst_factor % src_factor:
            raise ValueError("Adjacent scale factors must be integer nested.")
        ratio = dst_factor // src_factor
    else:
        if dst_factor != src_factor:
            raise ValueError("Time relation requires equal scale factor.")
        ratio = 1

    dst_on_src = _expand_labels(dst_labels, ratio)
    if dst_on_src.shape != src_labels.shape:
        raise ValueError(
            f"Aligned label shapes differ: src={src_labels.shape}, dst={dst_on_src.shape}"
        )

    a = src_labels.ravel()
    b = dst_on_src.ravel()
    both = (a > 0) & (b > 0)
    if not np.any(both):
        return pd.DataFrame(columns=[
            "src_id","dst_id","axis","overlap_src","overlap_dst","iou",
            "distance_norm","feature_similarity","transfer_weight","confidence"
        ])

    aa = a[both].astype(np.int64, copy=False)
    bb = b[both].astype(np.int64, copy=False)
    base = int(dst_labels.max()) + 1
    codes = aa * base + bb
    unique, inter = np.unique(codes, return_counts=True)
    src_lab = unique // base
    dst_lab = unique % base

    src_counts = np.bincount(a, minlength=int(src_labels.max())+1)
    dst_counts_coarse = np.bincount(
        dst_labels.ravel(), minlength=int(dst_labels.max())+1
    )
    dst_counts_srcgrid = dst_counts_coarse * (ratio ** 3)

    src_map = {
        int(str(r.object_id).lstrip("o")): r
        for r in src_objects.itertuples(index=False)
    }
    dst_map = {
        int(str(r.object_id).lstrip("o")): r
        for r in dst_objects.itertuples(index=False)
    }

    src_cell_volume = (spacing_native * src_factor) ** 3
    rows = []
    for sl, dl, nint in zip(src_lab, dst_lab, inter):
        sl = int(sl); dl = int(dl); nint = int(nint)
        if sl not in src_map or dl not in dst_map:
            continue
        sc = int(src_counts[sl])
        dc = int(dst_counts_srcgrid[dl])
        union = sc + dc - nint
        osrc = nint / sc if sc else 0.0
        odst = nint / dc if dc else 0.0
        iou = nint / union if union else 0.0

        s = src_map[sl]
        d = dst_map[dl]
        dx = float(s.cx - d.cx); dy = float(s.cy - d.cy); dz = float(s.cz - d.cz)
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        denom = float(s.equiv_radius + d.equiv_radius)
        distance_norm = dist / denom if denom > 0 else math.inf

        fsim = _feature_similarity(s.enstrophy_mean, d.enstrophy_mean)

        rows.append({
            "src_id": str(s.node_id),
            "dst_id": str(d.node_id),
            "axis": axis,
            "overlap_src": float(osrc),
            "overlap_dst": float(odst),
            "iou": float(iou),
            "distance_norm": float(distance_norm),
            "feature_similarity": float(fsim),
            "transfer_weight": float(nint * src_cell_volume),
            # Outgoing route weight = fraction of source volume entering dst.
            "confidence": float(osrc),
        })
    return pd.DataFrame(rows)
