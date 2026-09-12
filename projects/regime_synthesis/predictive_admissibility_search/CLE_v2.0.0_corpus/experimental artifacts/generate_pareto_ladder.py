#!/usr/bin/env python3
"""
generate_pareto_ladder.py

R2 adversarial generator:
Heavy-tailed Pareto gap ladders.

Purpose:
    Produce ladders with:
        - extreme discontinuities
        - large rare jumps
        - irregular stitching structure
        - heavy-tail fragmentation pressure

Output:
    CLE_PILOT_I/adversarial/raw/pareto_XXXX.csv

CSV format:
    n,value
    1,...
    2,...
"""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd


def generate_pareto_ladder(
    length: int,
    seed: int,
    alpha: float,
    xmin: float
) -> np.ndarray:

    rng = np.random.default_rng(seed)

    # Pareto distributed positive gaps
    gaps = xmin * (1.0 + rng.pareto(alpha, size=length - 1))

    # Numerical safety
    gaps[gaps <= 1e-12] = 1e-12

    # Convert gaps -> cumulative ladder
    values = np.concatenate([[0.0], np.cumsum(gaps)])

    return values


def main():

    parser = argparse.ArgumentParser(
        description="Generate R2 Pareto heavy-tailed adversarial ladders."
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
        "--alpha",
        type=float,
        default=1.2,
        help="Pareto tail exponent."
    )

    parser.add_argument(
        "--xmin",
        type=float,
        default=0.1,
        help="Minimum Pareto gap scale."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Master random seed."
    )

    args = parser.parse_args()

    out_dir = Path(args.out) / "pareto"
    out_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(args.seed)

    manifest = []

    for i in range(args.count):

        length = int(
            rng.integers(args.min_length, args.max_length + 1)
        )

        seed = int(
            rng.integers(0, 2**32 - 1)
        )

        values = generate_pareto_ladder(
            length=length,
            seed=seed,
            alpha=args.alpha,
            xmin=args.xmin
        )

        name = f"pareto_{i:04d}_n{length}.csv"

        path = out_dir / name

        df = pd.DataFrame({
            "n": np.arange(1, length + 1),
            "value": values
        })

        df.to_csv(path, index=False)

        manifest.append({
            "file": name,
            "class": "R2_pareto",
            "length": length,
            "alpha": args.alpha,
            "xmin": args.xmin,
            "seed": seed,
            "path": str(path)
        })

    manifest_path = out_dir / "pareto_manifest.csv"

    pd.DataFrame(manifest).to_csv(
        manifest_path,
        index=False
    )

    print(f"Generated {args.count} Pareto adversarial ladders.")
    print(f"Output folder: {out_dir}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()