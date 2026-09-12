from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import shutil
import tarfile
import tempfile
import zipfile
from pathlib import Path


PRIMARY_PREFIX = "4T-DTC_upload/raw data/ibm/"
PRIMARY_FILES = [
    "Z_ibmq_guadalupe.json",
    "Z_ibmq_guadalupe2.json",
    "Z_ibmq_kolkata.json",
    "Z_ibmq_mumbai.json",
    "Z_ibm_cairo.json",
    "Z_ibm_cairo2.json",
    "Z_ibm_hanoi.json",
    "Z_ibm_hanoi2.json",
]

CONTROL_FILES = [
    "Z_no_recompilationibmq_guadalupe2.json",
    "Z_no_recompilationibmq_kolkata.json",
    "Z_no_recompilationibm_cairo2.json",
    "Z_no_recompilationibm_cairot20.json",
    "Z_no_recompilation_ibmq_mumbai.json",
    "Z_no_recompilation_ibm_cairo.json",
    "Z_no_recompilation_ibm_hanoi.json",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json_array(tf: tarfile.TarFile, filename: str):
    member = PRIMARY_PREFIX + filename
    raw = tf.extractfile(member).read().decode("utf-8")
    return [float(x) for x in json.loads(raw)]


def write_bundle(bundle_dir: Path, candidate_id: str, arrays: dict[str, list[float]],
                 note: str):
    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    (bundle_dir/"temporal").mkdir(parents=True)

    min_len = min(len(v) for v in arrays.values())
    columns = list(arrays.keys())

    (bundle_dir/"manifest.json").write_text(
        json.dumps({
            "candidate_id": candidate_id,
            "label": candidate_id,
            "domain": "quantum_many_body",
            "protocol": "quantum_dtc_v1_1_0",
            "adapter_note": note,
        }, indent=2),
        encoding="utf-8"
    )

    with (bundle_dir/"temporal"/"trajectories.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f)
        w.writerow(["t"] + columns)
        for t in range(min_len):
            w.writerow([t] + [arrays[c][t] for c in columns])

    (bundle_dir/"ADAPTER_RECORD.json").write_text(
        json.dumps({
            "candidate_id": candidate_id,
            "source_members": [PRIMARY_PREFIX + x for x in columns],
            "trajectory_length": min_len,
            "coordinate_count": len(columns),
            "operation": (
                "Stack same-observable, same-cycle experimental runs as coordinates. "
                "No smoothing, sign alignment, Fourier filtering, interpolation, "
                "mitigation mixing, or phase-label input."
            ),
        }, indent=2),
        encoding="utf-8"
    )


def make_zip(folder: Path, zip_path: Path):
    if zip_path.exists():
        zip_path.unlink()
    shutil.make_archive(str(zip_path.with_suffix("")), "zip", folder.parent, folder.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archive")
    ap.add_argument("project_root")
    args = ap.parse_args()

    archive = Path(args.archive).resolve()
    root = Path(args.project_root).resolve()
    candidates = root/"candidates"
    candidates.mkdir(parents=True, exist_ok=True)

    with tarfile.open(archive, "r") as tf:
        primary = {Path(n).stem: read_json_array(tf, n) for n in PRIMARY_FILES}
        control = {Path(n).stem: read_json_array(tf, n) for n in CONTROL_FILES}

    with tempfile.TemporaryDirectory(prefix="tci_4t_") as td:
        td = Path(td)

        primary_dir = td/"TC_P01_C001"
        write_bundle(
            primary_dir,
            "TC_P01_C001",
            primary,
            "Neutral primary experimental ensemble from the recompilation-result IBM Z trajectories."
        )
        make_zip(primary_dir, candidates/"TC_P01_C001.zip")

        control_dir = td/"TC_P01_NRCTRL"
        write_bundle(
            control_dir,
            "TC_P01_NRCTRL",
            control,
            "Neutral no-recompilation hardware/control ensemble kept separate from the primary candidate."
        )
        make_zip(control_dir, candidates/"TC_P01_NRCTRL.zip")

    hashes = {
        "source_archive": {
            "path": archive.name,
            "sha256": sha256(archive),
            "bytes": archive.stat().st_size,
        },
        "candidate_zip": {
            "path": "candidates/TC_P01_C001.zip",
            "sha256": sha256(candidates/"TC_P01_C001.zip"),
        },
        "control_zip": {
            "path": "candidates/TC_P01_NRCTRL.zip",
            "sha256": sha256(candidates/"TC_P01_NRCTRL.zip"),
        },
    }
    (root/"registry"/"SOURCE_HASHES.json").write_text(
        json.dumps(hashes, indent=2), encoding="utf-8"
    )

    print("ADAPTER STATUS: COMPLETE")
    print("Primary candidate:", candidates/"TC_P01_C001.zip")
    print("No-recompilation control:", candidates/"TC_P01_NRCTRL.zip")


if __name__ == "__main__":
    main()
