#!/usr/bin/env python3
"""
CEA 2017 deterministic Grace/EPS extractor for UNNS VREF-I/B.

This script extracts native data points and published pointwise error bars
from E_physical_scaling_SU3.eps. It performs NO VREF-I/B scientific fit
or continuity/isolation classification.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import tarfile
from datetime import datetime, timezone
from pathlib import Path

ARCHIVE_SHA256 = "38e899b4c9d83b78e8bca70a51fc3adb3fa4e8c278ce4c392b3b08cbc3de2c44"
EPS_NAME = "E_physical_scaling_SU3.eps"
EPS_SHA256 = "bfa9e27a3d6e045e33977c277b8c473d1123067acac0c97955cd4fbee670a6fe"

X0, X1 = 0.1500, 0.8500
Y0, Y1 = 0.1500, 0.8500
X_WORLD_MAX = 1.1
Y_WORLD_MAX = 0.5
EPS_QUANT_GEV2 = 1.0e-4 * (Y_WORLD_MAX / (Y1 - Y0))

SERIES = {
    "Color1": {"refinement": "R1", "beta": 6.050, "d_over_a": 8},
    "Color2": {"refinement": "R2", "beta": 6.195, "d_over_a": 10},
}


class ExtractError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def x_to_fm(x: float) -> float:
    return (x - X0) * (X_WORLD_MAX / (X1 - X0))


def y_to_gev2(y: float) -> float:
    return (y - Y0) * (Y_WORLD_MAX / (Y1 - Y0))


EVENT_RE = re.compile(
    r"\[/DeviceRGB\]\s+SCS\s+(Color\d+)\s+SC|"
    r"n\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+0\s+360\s+EARC\s+s|"
    r"n\s+([0-9.]+)\s+([0-9.]+)\s+m\s+([0-9.]+)\s+([0-9.]+)\s+l\s+s"
)


def parse_events(text: str, end_pos: int):
    events = []
    color = None
    for m in EVENT_RE.finditer(text[:end_pos]):
        if m.group(1):
            color = m.group(1)
        elif m.group(2):
            x, y, xr, yr = map(float, m.group(2, 3, 4, 5))
            events.append(("marker", color, m.start(), x, y, xr, yr))
        elif m.group(6):
            x1, y1, x2, y2 = map(float, m.group(6, 7, 8, 9))
            events.append(("line", color, m.start(), x1, y1, x2, y2))
    return events


def validate_eps_text(text: str):
    if "%%Creator: Grace-5.1.25" not in text:
        raise ExtractError("Unexpected EPS creator")
    if "%%Title: E_physical_scaling_SU3.agr" not in text:
        raise ExtractError("Unexpected EPS title")
    for label in ("(=6.050) show", "(=6.195) show"):
        if label not in text:
            raise ExtractError(f"Missing legend label {label}")
    frame_anchor = "0.1500 0.1500 m"
    pos = text.find(frame_anchor)
    if pos < 0:
        raise ExtractError("Could not locate frozen graph-frame anchor")
    return pos


def recover_rows(events, color: str):
    markers = [
        e for e in events
        if e[0] == "marker"
        and e[1] == color
        and abs(e[5] - 0.0050) <= 1e-9
        and abs(e[6] - 0.0050) <= 1e-9
        and X0 - 1e-6 <= e[3] <= X1 + 1e-6
        and Y0 - 1e-6 <= e[4] <= Y1 + 1e-6
    ]
    if len(markers) != 11:
        raise ExtractError(f"{color}: expected 11 data markers, found {len(markers)}")

    rows = []
    for idx, mk in enumerate(markers):
        _, _, marker_pos, x, y, _, _ = mk

        candidates = []
        for e in events:
            if e[0] != "line" or e[1] != color or e[2] >= marker_pos:
                continue
            x1, yy1, x2, yy2 = e[3], e[4], e[5], e[6]
            if abs(x1 - x) > 5e-5 or abs(x2 - x) > 5e-5:
                continue
            if abs(yy1 - y) <= 5e-5 or abs(yy2 - y) <= 5e-5:
                candidates.append(e)

        if len(candidates) < 2:
            raise ExtractError(f"{color} point {idx}: could not recover both vertical error-bar halves")

        halves = candidates[-2:]
        ys = []
        for e in halves:
            ys.extend([e[4], e[6]])
        ylo, yhi = min(ys), max(ys)

        if not (ylo <= y <= yhi):
            raise ExtractError(f"{color} point {idx}: marker not bracketed by error bar")

        midpoint = 0.5 * (ylo + yhi)
        if abs(midpoint - y) > 1.5e-4:
            raise ExtractError(
                f"{color} point {idx}: error-bar midpoint mismatch "
                f"({midpoint:.7f} vs {y:.7f})"
            )

        xf = x_to_fm(x)
        ef = y_to_gev2(y)
        elo = y_to_gev2(ylo)
        ehi = y_to_gev2(yhi)
        sigma_pub = 0.5 * (ehi - elo)
        sigma_fit = math.sqrt(sigma_pub * sigma_pub + EPS_QUANT_GEV2 * EPS_QUANT_GEV2)

        rows.append({
            "color": color,
            "point_index": idx,
            "X_plot": x,
            "Y_plot": y,
            "Y_low_plot": ylo,
            "Y_high_plot": yhi,
            "x_fm": xf,
            "E_GeV2": ef,
            "published_error_GeV2": sigma_pub,
            "eps_quant_GeV2": EPS_QUANT_GEV2,
            "fit_sigma_GeV2": sigma_fit,
        })

    xs = [r["x_fm"] for r in rows]
    if any(xs[i+1] <= xs[i] for i in range(len(xs)-1)):
        raise ExtractError(f"{color}: x coordinates are not strictly increasing")
    if abs(xs[0]) > 2.0e-4:
        raise ExtractError(f"{color}: first x is not consistent with zero")

    spacings = [xs[i+1] - xs[i] for i in range(len(xs)-1)]
    mean_dx = sum(spacings) / len(spacings)
    max_dev = max(abs(dx - mean_dx) for dx in spacings)
    if max_dev > 3.5e-4:
        raise ExtractError(
            f"{color}: native spacing is not uniform enough "
            f"(mean={mean_dx:.7f}, max deviation={max_dev:.7f})"
        )

    return rows, mean_dx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", type=Path, default=Path("."))
    ap.add_argument("--validate-only", action="store_true")
    args = ap.parse_args()

    root = args.project_root.resolve()
    archive = root / "data" / "raw" / "cea_2017" / "arXiv-1702.06437v3.tar.gz"

    if not archive.exists():
        raise ExtractError(f"Missing source archive: {archive}")

    archive_hash = sha256_file(archive)
    if archive_hash != ARCHIVE_SHA256:
        raise ExtractError(
            "Source archive SHA-256 mismatch\n"
            f"expected: {ARCHIVE_SHA256}\n"
            f"actual:   {archive_hash}"
        )

    with tarfile.open(archive, "r:gz") as tf:
        eps_bytes = tf.extractfile(EPS_NAME).read()

    eps_hash = sha256_bytes(eps_bytes)
    if eps_hash != EPS_SHA256:
        raise ExtractError(
            "EPS SHA-256 mismatch\n"
            f"expected: {EPS_SHA256}\n"
            f"actual:   {eps_hash}"
        )

    text = eps_bytes.decode("latin1")
    frame_pos = validate_eps_text(text)
    events = parse_events(text, frame_pos)

    all_rows = []
    spacing = {}
    for color, meta in SERIES.items():
        rows, dx = recover_rows(events, color)
        spacing[color] = dx
        for row in rows:
            all_rows.append({
                "source_id": "CEA_2017_SU3",
                "refinement": meta["refinement"],
                "beta": meta["beta"],
                **row,
            })

    if not spacing["Color1"] > spacing["Color2"]:
        raise ExtractError("Series-spacing check failed: Color1 should be d=8a and coarser than Color2 d=10a")

    if args.validate_only:
        print("CEA_2017 VREF-I/B vector extraction validation: PASS")
        print(f"archive sha256: {archive_hash}")
        print(f"eps sha256:     {eps_hash}")
        print(f"R1 points: 11, mean dx = {spacing['Color1']:.9f} fm")
        print(f"R2 points: 11, mean dx = {spacing['Color2']:.9f} fm")
        print("No extracted CSV was written (--validate-only).")
        return 0

    out_dir = root / "data" / "derived" / "cea_2017"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "CEA17_VREF_B_POINTS.csv"
    json_path = out_dir / "CEA17_VREF_B_EXTRACT.json"

    fields = [
        "source_id", "refinement", "beta", "color", "point_index",
        "X_plot", "Y_plot", "Y_low_plot", "Y_high_plot",
        "x_fm", "E_GeV2", "published_error_GeV2",
        "eps_quant_GeV2", "fit_sigma_GeV2",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_rows)

    csv_hash = sha256_file(csv_path)
    record = {
        "schema": "CEA17_VREF_B_EXTRACT_v1",
        "status": "EXTRACTION-VALID",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_id": "CEA_2017_SU3",
        "archive": {
            "path": str(archive.relative_to(root)).replace("\\", "/"),
            "sha256": archive_hash,
        },
        "eps_asset": {
            "name": EPS_NAME,
            "sha256": eps_hash,
            "creator": "Grace-5.1.25",
            "title": "E_physical_scaling_SU3.agr",
        },
        "graph_transform": {
            "viewport": {"x": [X0, X1], "y": [Y0, Y1]},
            "world": {"x_fm": [0.0, X_WORLD_MAX], "E_GeV2": [0.0, Y_WORLD_MAX]},
        },
        "series": {
            "Color1": {"beta": 6.050, "refinement": "R1", "points": 11, "mean_dx_fm": spacing["Color1"]},
            "Color2": {"beta": 6.195, "refinement": "R2", "points": 11, "mean_dx_fm": spacing["Color2"]},
        },
        "eps_quant_GeV2": EPS_QUANT_GEV2,
        "output_csv": {
            "path": str(csv_path.relative_to(root)).replace("\\", "/"),
            "sha256": csv_hash,
            "rows": len(all_rows),
        },
        "scientific_fit_performed": False,
    }
    json_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    print("CEA_2017 VREF-I/B vector extraction: EXTRACTION-VALID")
    print(f"Wrote: {csv_path}")
    print(f"Wrote: {json_path}")
    print("No VREF-I/B asymptotic model fit was performed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ExtractError as exc:
        print(f"EXTRACTION-INVALID: {exc}")
        raise SystemExit(2)
