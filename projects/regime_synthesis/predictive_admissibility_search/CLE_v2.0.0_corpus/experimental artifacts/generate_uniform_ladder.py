#!/usr/bin/env python3
"""
generate_uniform_ladder.py

R1 adversarial generator:
Uniform random gap ladders.

Output:
    CLE_PILOT_I/adversarial/raw/uniform_XXXX.csv

CSV format:
    n,value
    1,...
    2,...
"""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd


def generate_uniform_ladder(length: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)

    # length values require length - 1 positive gaps
    gaps = rng.uniform(0.0, 1.0, size=length - 1)

    # avoid exact zero gaps
    gaps[gaps <= 1e-12] = 1e-12

    values = np.concatenate([[0.0], np.cumsum(gaps)])
    return values


def main():
    parser = argparse.ArgumentParser(
        description="Generate R1 uniform random gap adversarial ladders."
    )

    parser.add_argument(
        "--out",
        default="CLE_PILOT_I/adversarial/raw",
        help="Output directory."
    )

    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Number of ladders to generate."
    )

    parser.add_argument(
        "--min-length",
        type=int,
        default=10,
        help="Minimum ladder length."
    )

    parser.add_argument(
        "--max-length",
        type=int,
        default=1000,
        help="Maximum ladder length."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Master random seed."
    )

    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(args.seed)
    manifest = []

    for i in range(args.count):
        length = int(rng.integers(args.min_length, args.max_length + 1))
        seed = int(rng.integers(0, 2**32 - 1))

        values = generate_uniform_ladder(length, seed)

        name = f"uniform_{i:04d}_n{length}.csv"
        path = out_dir / name

        df = pd.DataFrame({
            "n": np.arange(1, length + 1),
            "value": values
        })

        df.to_csv(path, index=False)

        manifest.append({
            "file": name,
            "class": "R1_uniform",
            "length": length,
            "seed": seed,
            "path": str(path)
        })

    manifest_path = out_dir / "uniform_manifest.csv"
    pd.DataFrame(manifest).to_csv(manifest_path, index=False)

    print(f"Generated {args.count} uniform adversarial ladders.")
    print(f"Output folder: {out_dir}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()