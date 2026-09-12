#!/usr/bin/env python3
"""
generate_randomwalk_ladder.py

R3 adversarial generator:
Correlated random-walk ladders.

Purpose:
    Produce ladders with:
        - local correlation
        - smooth regional drift
        - plausible continuity
        - NO global physical constraint

This is intentionally more dangerous than:
    - uniform random
    - Pareto fragmentation

because it may partially mimic
real persistence structure.

Output:
    CLE_PILOT_I/adversarial/raw/randomwalk/randomwalk_XXXX.csv

CSV format:
    n,value
    1,...
    2,...
"""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd


def generate_randomwalk_ladder(
    length: int,
    seed: int,
    smooth_kernel: int
) -> np.ndarray:

    rng = np.random.default_rng(seed)

    # Base Gaussian increments
    increments = rng.normal(
        loc=0.0,
        scale=1.0,
        size=length - 1
    )

    # Absolute value to preserve monotonic ladder growth
    increments = np.abs(increments)

    # Optional smoothing introduces local correlation
    if smooth_kernel > 1:

        kernel = np.ones(smooth_kernel)
        kernel /= kernel.sum()

        increments = np.convolve(
            increments,
            kernel,
            mode="same"
        )

    # Numerical safety
    increments[increments <= 1e-12] = 1e-12

    # Convert increments -> cumulative ladder
    values = np.concatenate([
        [0.0],
        np.cumsum(increments)
    ])

    return values


def main():

    parser = argparse.ArgumentParser(
        description="Generate R3 correlated random-walk adversarial ladders."
    )

    parser.add_argument(
        "--out",
        default="CLE_PILOT_I/adversarial/raw",
        help="Base output directory."
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
        "--smooth-kernel",
        type=int,
        default=5,
        help="Local smoothing kernel width."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Master random seed."
    )

    args = parser.parse_args()

    out_dir = Path(args.out) / "randomwalk"
    out_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    rng = np.random.default_rng(args.seed)

    manifest = []

    for i in range(args.count):

        length = int(
            rng.integers(
                args.min_length,
                args.max_length + 1
            )
        )

        seed = int(
            rng.integers(
                0,
                2**32 - 1
            )
        )

        values = generate_randomwalk_ladder(
            length=length,
            seed=seed,
            smooth_kernel=args.smooth_kernel
        )

        name = f"randomwalk_{i:04d}_n{length}.csv"

        path = out_dir / name

        df = pd.DataFrame({
            "n": np.arange(1, length + 1),
            "value": values
        })

        df.to_csv(
            path,
            index=False
        )

        manifest.append({
            "file": name,
            "class": "R3_randomwalk",
            "length": length,
            "smooth_kernel": args.smooth_kernel,
            "seed": seed,
            "path": str(path)
        })

    manifest_path = out_dir / "randomwalk_manifest.csv"

    pd.DataFrame(manifest).to_csv(
        manifest_path,
        index=False
    )

    print(f"Generated {args.count} random-walk adversarial ladders.")
    print(f"Output folder: {out_dir}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()