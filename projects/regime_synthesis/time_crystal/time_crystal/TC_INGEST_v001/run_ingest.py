from __future__ import annotations
import argparse, csv, json
from pathlib import Path
import numpy as np
from tc_ingest import parse_meta, load_dat, EXPECTED_BYTES, N_ITER, N_TIME, N_QUBIT


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir")
    ap.add_argument("output_dir")
    args = ap.parse_args()
    data_dir = Path(args.data_dir)
    out = Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)

    files = sorted(data_dir.glob("*.dat"))
    manifest = []
    failures = []
    for p in files:
        try:
            meta = parse_meta(p)
            arr = load_dat(p)
            d = meta.to_dict()
            d.update({
                "bytes": p.stat().st_size,
                "shape": "5x51x57",
                "dtype": "float32",
                "finite": bool(np.isfinite(arr).all()),
                "min": float(arr.min()),
                "max": float(arr.max()),
            })
            manifest.append(d)
        except Exception as e:
            failures.append({"file": p.name, "error": str(e)})

    fields = list(manifest[0].keys()) if manifest else []
    with open(out / "manifest.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(manifest)

    eps = sorted({m["epsilon"] for m in manifest})
    devices = {}
    for m in manifest:
        devices[m["device"]] = devices.get(m["device"], 0) + 1

    validation = {
        "status": "PASS" if manifest and not failures else "FAIL",
        "dat_files": len(files),
        "validated_files": len(manifest),
        "failures": failures,
        "expected_bytes_per_file": EXPECTED_BYTES,
        "decoded_shape": [N_ITER, N_TIME, N_QUBIT],
        "dtype": "float32",
        "epsilon_values": eps,
        "epsilon_count": len(eps),
        "device_counts": devices,
        "note": "Iteration 0 is the epsilon=0 reference; iterations 1-4 are target runs, following DTC_qiskit.ipynb generation order."
    }
    (out / "validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    print(json.dumps(validation, indent=2))

if __name__ == "__main__": main()
