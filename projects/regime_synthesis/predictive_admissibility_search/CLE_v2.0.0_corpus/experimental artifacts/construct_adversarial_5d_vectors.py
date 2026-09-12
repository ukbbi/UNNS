#!/usr/bin/env python3
"""
construct_adversarial_5d_vectors.py

Constructs a STRUC-PERC-level 5D proxy vector table from batch output ZIP files.

IMPORTANT:
This is a proxy construction from STRUC-PERC-I batch summaries only.
The true manuscript vector

    v(L) = (P_depth, sigma2_GR, frag_rate, adm_persist, aniso_persist)

requires the full deformation grid output for sigma2_GR and anisotropic persistence.
This script uses explicit proxy definitions so Step 5 can be tested preliminarily.

Proxy definitions:
    P_depth        = log10(1 + kappa_connect), with missing kappa_connect -> 0
    sigma2_GR      = (1 - giantRatio)^2
    frag_rate      = clip((1 - giantRatio) + isolatedFraction, 0, 1)
    adm_persist    = giantRatio
    aniso_persist  = tailDominance

Inputs expected in the current folder or supplied by --zip-dir:
    uniform_STRUC-PERC-I_output.zip
    pareto_STRUC-PERC-I_output.zip
    randomwalk_STRUC-PERC-I_output.zip
    shuffle_STRUC-PERC-I_output.zip
"""

from pathlib import Path
import argparse
import json
import zipfile
import numpy as np
import pandas as pd


ZIP_NAMES = {
    "uniform": "uniform_STRUC-PERC-I_output.zip",
    "pareto": "pareto_STRUC-PERC-I_output.zip",
    "randomwalk": "randomwalk_STRUC-PERC-I_output.zip",
    "shuffle": "shuffle_STRUC-PERC-I_output.zip",
}


def read_zip_batch(zip_path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(zip_path) as z:
        csvs = [n for n in z.namelist() if n.lower().endswith(".csv")]
        jsons = [n for n in z.namelist() if n.lower().endswith(".json")]

        if csvs:
            name = max(csvs, key=lambda n: z.getinfo(n).file_size)
            return pd.read_csv(z.open(name))

        if jsons:
            name = max(jsons, key=lambda n: z.getinfo(n).file_size)
            data = json.load(z.open(name))
            return pd.DataFrame(data)

    raise RuntimeError(f"No CSV/JSON batch result found in {zip_path}")


def construct_vectors(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    for col in [
        "n",
        "giantRatio",
        "kappa_connect",
        "isolated",
        "isolatedFraction",
        "tailDominance",
    ]:
        out[col] = pd.to_numeric(out.get(col), errors="coerce")

    out["P_depth"] = np.log10(1 + out["kappa_connect"].fillna(0))
    out["sigma2_GR"] = (1 - out["giantRatio"].fillna(0)) ** 2
    out["frag_rate"] = np.clip(
        (1 - out["giantRatio"].fillna(0)) + out["isolatedFraction"].fillna(0),
        0,
        1,
    )
    out["adm_persist"] = out["giantRatio"].fillna(0)
    out["aniso_persist"] = out["tailDominance"].fillna(0)

    return out[
        [
            "name",
            "class",
            "n",
            "verdict",
            "P_depth",
            "sigma2_GR",
            "frag_rate",
            "adm_persist",
            "aniso_persist",
            "kappa_connect",
            "giantRatio",
            "isolatedFraction",
            "tailDominance",
            "runStatus",
        ]
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip-dir", default=".", help="Folder containing STRUC-PERC output ZIPs.")
    parser.add_argument("--out", default="adversarial_STRUC_5D_proxy_vectors.csv")
    parser.add_argument("--summary", default="adversarial_STRUC_5D_proxy_summary.csv")
    args = parser.parse_args()

    zip_dir = Path(args.zip_dir)
    frames = []

    for cls, name in ZIP_NAMES.items():
        path = zip_dir / name
        if not path.exists():
            raise FileNotFoundError(path)

        df = read_zip_batch(path)
        df["class"] = cls
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    vectors = construct_vectors(combined)
    vectors.to_csv(args.out, index=False)

    summary = vectors.groupby("class").agg(
        count=("name", "count"),
        full=("verdict", lambda s: (s == "FULL_PERCOLATION").sum()),
        giant=("verdict", lambda s: (s == "GIANT_COMPONENT_PERCOLATION").sum()),
        tail=("verdict", lambda s: (s == "TAIL_FRAGMENTATION").sum()),
        hard=("verdict", lambda s: (s == "HARD_FRAGMENTATION").sum()),
        median_P_depth=("P_depth", "median"),
        median_frag_rate=("frag_rate", "median"),
        median_adm_persist=("adm_persist", "median"),
        median_aniso_persist=("aniso_persist", "median"),
        median_kappa=("kappa_connect", "median"),
        median_tail=("tailDominance", "median"),
    ).reset_index()

    summary.to_csv(args.summary, index=False)

    print(f"Wrote vectors: {args.out}")
    print(f"Wrote summary: {args.summary}")
    print(f"Rows: {len(vectors)}")


if __name__ == "__main__":
    main()
