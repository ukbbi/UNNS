from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd


def build_one(source: Path, candidate_id: str, output_zip: Path):
    df = pd.read_csv(source)
    idx = df.columns[0]

    for c in ("x", "y", "z"):
        if c not in df.columns:
            raise RuntimeError(f"{source}: missing required column {c}")

    strobe = df[df[idx].astype(int) % 300 == 0][[idx, "x", "y", "z"]].copy()
    strobe.columns = ["t", "x", "y", "z"]

    expected = np.arange(0, 300001, 300)
    observed = strobe["t"].to_numpy(dtype=int)
    if not np.array_equal(observed, expected):
        raise RuntimeError("Stored N=300 stroboscopic sequence is incomplete")

    with tempfile.TemporaryDirectory(prefix="tc_p01_c002_") as td:
        td = Path(td)
        root = td / candidate_id
        (root / "temporal").mkdir(parents=True)

        (root / "manifest.json").write_text(json.dumps({
            "candidate_id": candidate_id,
            "label": candidate_id,
            "domain": "quantum_many_body",
            "protocol": "quantum_dtc_v1_1_0"
        }, indent=2), encoding="utf-8")

        strobe.to_csv(root / "temporal" / "trajectories.csv", index=False)

        (root / "ADAPTER_RECORD.json").write_text(json.dumps({
            "candidate_id": candidate_id,
            "stroboscopic_step": 300,
            "source_rows_used": len(strobe),
            "operation": (
                "Select stored rows at source index divisible by 300; preserve signed "
                "x,y,z exactly; no sign alignment, target-period input, smoothing, "
                "Fourier filtering, interpolation, or chamber tuning."
            )
        }, indent=2), encoding="utf-8")

        if output_zip.exists():
            output_zip.unlink()
        shutil.make_archive(str(output_zip.with_suffix("")), "zip", root.parent, root.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate_source")
    ap.add_argument("control_source")
    ap.add_argument("project_root")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    cands = root / "candidates"
    cands.mkdir(parents=True, exist_ok=True)

    build_one(Path(args.candidate_source).resolve(), "TC_P01_C002",
              cands / "TC_P01_C002.zip")
    build_one(Path(args.control_source).resolve(), "TC_P01_C002_CTRL",
              cands / "TC_P01_C002_CTRL.zip")

    print("C002 ADAPTER STATUS: COMPLETE")
    print("Candidate:", cands / "TC_P01_C002.zip")
    print("Control:", cands / "TC_P01_C002_CTRL.zip")


if __name__ == "__main__":
    main()
