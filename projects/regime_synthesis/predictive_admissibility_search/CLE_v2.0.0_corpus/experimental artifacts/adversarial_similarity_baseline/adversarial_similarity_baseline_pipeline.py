#!/usr/bin/env python3
"""
adversarial_similarity_baseline_pipeline.py

Purpose
-------
Adversarial baseline test for the R_sim similarity metric used in
"Structural Universality Across Physical Systems".

This script is designed to answer one question:

    Does the cross-domain similarity metric distinguish real physical
    rigidity manifolds from random or adversarial synthetic ladders?

It supports four adversarial classes:

    R1: Uniform random gaps
    R2: Heavy-tailed Pareto gaps
    R3: Correlated random-walk ladder
    R4: Shuffled-real-gap controls

The script has two intended modes:

1. Generation mode:
   Generate adversarial ladders as CSV files for CLE / STRUC-PERC evaluation.

2. Analysis mode:
   Load real and synthetic CLE summary vectors, compute R_sim distributions,
   bootstrap confidence intervals, overlap fractions, and pass/fail diagnostics.

The script deliberately does NOT claim to replace CLE v2.0.0 or STRUC-PERC-I.
It is a wrapper and adversarial-baseline controller around their outputs.

Author: UNNS Substrate Research Program workflow helper
Python: 3.10+
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

SUMMARY_COLUMNS = [
    "P_depth",
    "sigma2_GR",
    "frag_rate",
    "adm_persist",
    "aniso_persist",
]

REAL_DOMAIN_MIN_BASELINE = 0.882   # Current minimum real-real similarity: neutrino-cosmology
STRICT_REAL_REAL_BASELINE = 0.901  # Helium-neutrino, used for stronger overlap check
FAIL_MEDIAN_THRESHOLD = 0.85
PASS_MEDIAN_TARGET = 0.80


# ---------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------

@dataclass
class LadderRecord:
    ladder_id: str
    class_name: str
    n: int
    seed: int
    path: str
    notes: str = ""


@dataclass
class SimilarityResult:
    group_a: str
    group_b: str
    n_pairs: int
    median: float
    mean: float
    std: float
    ci95_low: float
    ci95_high: float
    min_value: float
    max_value: float
    overlap_gt_0901: float
    overlap_gt_0882: float
    verdict: str


# ---------------------------------------------------------------------
# Ladder generation utilities
# ---------------------------------------------------------------------

def normalize_positive_gaps(gaps: np.ndarray) -> np.ndarray:
    """Ensure gaps are strictly positive and numerically safe."""
    gaps = np.asarray(gaps, dtype=float)
    gaps = np.abs(gaps)
    gaps[gaps <= 1e-12] = 1e-12
    return gaps


def gaps_to_ladder(gaps: np.ndarray, start: float = 0.0) -> np.ndarray:
    """Convert positive gaps into a strictly increasing ladder."""
    gaps = normalize_positive_gaps(gaps)
    return start + np.concatenate([[0.0], np.cumsum(gaps)])


def generate_uniform_gaps(n_points: int, rng: np.random.Generator) -> np.ndarray:
    """
    R1: Uniform random gaps.
    Produces a flat, structure-poor gap field.
    """
    gaps = rng.uniform(0.0, 1.0, size=max(n_points - 1, 1))
    return gaps_to_ladder(gaps)


def generate_pareto_gaps(
    n_points: int,
    rng: np.random.Generator,
    xm: float = 0.1,
    alpha: float = 1.2,
) -> np.ndarray:
    """
    R2: Heavy-tailed Pareto gaps.
    Produces extreme gaps and random stitching-like discontinuities.
    """
    gaps = xm * (1.0 + rng.pareto(alpha, size=max(n_points - 1, 1)))
    return gaps_to_ladder(gaps)


def generate_random_walk_ladder(n_points: int, rng: np.random.Generator) -> np.ndarray:
    """
    R3: Correlated random-walk-like ladder.
    Generates increments from N(0,1), takes absolute values, then cumulatively sums.
    This creates local correlation but no physical constraint.
    """
    increments = np.abs(rng.normal(0.0, 1.0, size=max(n_points - 1, 1)))
    # Smooth slightly to introduce local correlation.
    if len(increments) >= 5:
        kernel = np.array([0.15, 0.2, 0.3, 0.2, 0.15])
        increments = np.convolve(increments, kernel, mode="same")
    return gaps_to_ladder(increments)


def load_ladder_csv(path: Path) -> np.ndarray:
    """
    Load a ladder from CSV.
    Accepts either:
    - one unnamed numeric column
    - a column named value, level, ladder, x, or L
    """
    df = pd.read_csv(path)
    if df.shape[1] == 1:
        values = df.iloc[:, 0].to_numpy(dtype=float)
    else:
        candidates = ["value", "level", "ladder", "x", "L"]
        col = next((c for c in candidates if c in df.columns), None)
        if col is None:
            numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
            if not numeric_cols:
                raise ValueError(f"No numeric ladder column found in {path}")
            col = numeric_cols[0]
        values = df[col].to_numpy(dtype=float)

    values = values[np.isfinite(values)]
    values = np.unique(np.sort(values))
    if len(values) < 3:
        raise ValueError(f"Ladder too short after cleanup: {path}")
    return values


def generate_shuffled_gap_controls(
    real_ladder_paths: Sequence[Path],
    output_dir: Path,
    n_shuffles_per_ladder: int,
    rng: np.random.Generator,
) -> List[LadderRecord]:
    """
    R4: Shuffled-real-gap controls.
    Preserve gap multiset but destroy sequential gap ordering.

    Important:
    If downstream metrics depend only on sorted gap distribution and not sequential gap order,
    these controls may remain too similar. That is precisely why R4 is a high-value adversarial test.
    """
    records: List[LadderRecord] = []
    output_dir.mkdir(parents=True, exist_ok=True)

    for path in real_ladder_paths:
        real = load_ladder_csv(path)
        gaps = np.diff(real)
        stem = path.stem

        for j in range(n_shuffles_per_ladder):
            seed = int(rng.integers(0, 2**32 - 1))
            local_rng = np.random.default_rng(seed)
            shuffled = np.array(gaps, copy=True)
            local_rng.shuffle(shuffled)
            ladder = gaps_to_ladder(shuffled)

            ladder_id = f"R4_{stem}_shuffle_{j:03d}"
            out = output_dir / f"{ladder_id}.csv"
            pd.DataFrame({"value": ladder}).to_csv(out, index=False)
            records.append(
                LadderRecord(
                    ladder_id=ladder_id,
                    class_name="R4_shuffled_real_gaps",
                    n=len(ladder),
                    seed=seed,
                    path=str(out),
                    notes=f"Gap multiset shuffled from {path.name}",
                )
            )
    return records


def generate_adversarial_corpus(
    output_dir: Path,
    n_ladders_per_class: int = 100,
    n_points_range: Tuple[int, int] = (10, 1000),
    seed: int = 42,
    real_ladder_dir: Optional[Path] = None,
    n_shuffles_per_ladder: int = 5,
) -> pd.DataFrame:
    """
    Generate R1, R2, R3, and optional R4 ladders.
    """
    rng = np.random.default_rng(seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    records: List[LadderRecord] = []

    generators = {
        "R1_uniform_random_gaps": generate_uniform_gaps,
        "R2_pareto_heavy_tailed_gaps": generate_pareto_gaps,
        "R3_correlated_random_walk": generate_random_walk_ladder,
    }

    lo, hi = n_points_range
    if lo < 3 or hi < lo:
        raise ValueError("n_points_range must satisfy 3 <= low <= high")

    for class_name, generator in generators.items():
        class_dir = output_dir / class_name
        class_dir.mkdir(parents=True, exist_ok=True)

        for i in range(n_ladders_per_class):
            n_points = int(rng.integers(lo, hi + 1))
            local_seed = int(rng.integers(0, 2**32 - 1))
            local_rng = np.random.default_rng(local_seed)
            ladder = generator(n_points, local_rng)

            ladder_id = f"{class_name}_{i:04d}_n{n_points}"
            out = class_dir / f"{ladder_id}.csv"
            pd.DataFrame({"value": ladder}).to_csv(out, index=False)

            records.append(
                LadderRecord(
                    ladder_id=ladder_id,
                    class_name=class_name,
                    n=len(ladder),
                    seed=local_seed,
                    path=str(out),
                    notes="Synthetic adversarial ladder",
                )
            )

    if real_ladder_dir is not None and real_ladder_dir.exists():
        real_paths = sorted(real_ladder_dir.glob("*.csv"))
        if real_paths:
            r4_records = generate_shuffled_gap_controls(
                real_ladder_paths=real_paths,
                output_dir=output_dir / "R4_shuffled_real_gaps",
                n_shuffles_per_ladder=n_shuffles_per_ladder,
                rng=rng,
            )
            records.extend(r4_records)

    manifest = pd.DataFrame([asdict(r) for r in records])
    manifest_path = output_dir / "adversarial_ladder_manifest.csv"
    manifest.to_csv(manifest_path, index=False)

    return manifest


# ---------------------------------------------------------------------
# Similarity metric utilities
# ---------------------------------------------------------------------

def validate_summary_frame(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """
    Expected columns:
        item_id, group, P_depth, sigma2_GR, frag_rate, adm_persist, aniso_persist

    item_id may be absent; it will be generated.
    group may be absent; source_name will be used.
    """
    missing = [c for c in SUMMARY_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"{source_name} missing required summary columns: {missing}")

    df = df.copy()
    if "item_id" not in df.columns:
        df["item_id"] = [f"{source_name}_{i:04d}" for i in range(len(df))]
    if "group" not in df.columns:
        df["group"] = source_name

    for c in SUMMARY_COLUMNS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=SUMMARY_COLUMNS)
    if df.empty:
        raise ValueError(f"{source_name} has no valid summary vectors after cleanup")
    return df


def load_summary_vectors(paths: Sequence[Path], source_prefix: str) -> pd.DataFrame:
    frames = []
    for path in paths:
        if path.suffix.lower() == ".json":
            obj = json.loads(path.read_text())
            if isinstance(obj, list):
                df = pd.DataFrame(obj)
            elif isinstance(obj, dict) and "records" in obj:
                df = pd.DataFrame(obj["records"])
            else:
                df = pd.DataFrame([obj])
        else:
            df = pd.read_csv(path)
        frames.append(validate_summary_frame(df, source_name=f"{source_prefix}_{path.stem}"))
    return pd.concat(frames, ignore_index=True)


def compute_normalization_denominator(vectors: np.ndarray) -> float:
    """
    Denominator used in R_sim:
        max pairwise Euclidean distance across the comparison set.

    If all vectors are identical, returns 1.0 to avoid division by zero.
    """
    n = len(vectors)
    if n < 2:
        return 1.0

    max_dist = 0.0
    for i in range(n):
        diffs = vectors[i + 1:] - vectors[i]
        if len(diffs) == 0:
            continue
        dists = np.linalg.norm(diffs, axis=1)
        local_max = float(np.max(dists)) if len(dists) else 0.0
        max_dist = max(max_dist, local_max)

    return max(max_dist, 1e-12)


def r_sim(vec_a: np.ndarray, vec_b: np.ndarray, denom: float) -> float:
    """
    R_sim = 1 - ||a - b|| / max_pairwise_distance
    Clipped to [0, 1] for robust reporting.
    """
    dist = float(np.linalg.norm(vec_a - vec_b))
    return float(np.clip(1.0 - dist / denom, 0.0, 1.0))


def bootstrap_ci(
    values: Sequence[float],
    statistic=np.median,
    n_boot: int = 2000,
    seed: int = 123,
    alpha: float = 0.05,
) -> Tuple[float, float]:
    if len(values) == 0:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    arr = np.asarray(values, dtype=float)
    boot = []
    for _ in range(n_boot):
        sample = rng.choice(arr, size=len(arr), replace=True)
        boot.append(float(statistic(sample)))
    return (
        float(np.quantile(boot, alpha / 2)),
        float(np.quantile(boot, 1 - alpha / 2)),
    )


def pairwise_group_similarity(
    df: pd.DataFrame,
    group_a: str,
    group_b: str,
    denom: float,
    n_boot: int = 2000,
) -> SimilarityResult:
    a = df[df["group"] == group_a]
    b = df[df["group"] == group_b]
    if a.empty or b.empty:
        raise ValueError(f"Empty group comparison: {group_a} vs {group_b}")

    values = []
    for _, row_a in a.iterrows():
        va = row_a[SUMMARY_COLUMNS].to_numpy(dtype=float)
        for _, row_b in b.iterrows():
            if group_a == group_b and row_a["item_id"] == row_b["item_id"]:
                continue
            vb = row_b[SUMMARY_COLUMNS].to_numpy(dtype=float)
            values.append(r_sim(va, vb, denom))

    if not values:
        values = [1.0]

    values_arr = np.asarray(values, dtype=float)
    ci_low, ci_high = bootstrap_ci(values_arr, n_boot=n_boot)

    median = float(np.median(values_arr))
    if group_a.startswith("R") or group_b.startswith("R"):
        if median > FAIL_MEDIAN_THRESHOLD:
            verdict = "FAIL: random-real median exceeds 0.85"
        elif median < PASS_MEDIAN_TARGET:
            verdict = "PASS: random-real median below 0.80"
        else:
            verdict = "BORDERLINE: random-real median between 0.80 and 0.85"
    else:
        verdict = "REFERENCE: real-real or non-random comparison"

    return SimilarityResult(
        group_a=group_a,
        group_b=group_b,
        n_pairs=len(values_arr),
        median=median,
        mean=float(np.mean(values_arr)),
        std=float(np.std(values_arr, ddof=1)) if len(values_arr) > 1 else 0.0,
        ci95_low=ci_low,
        ci95_high=ci_high,
        min_value=float(np.min(values_arr)),
        max_value=float(np.max(values_arr)),
        overlap_gt_0901=float(np.mean(values_arr > STRICT_REAL_REAL_BASELINE)),
        overlap_gt_0882=float(np.mean(values_arr > REAL_DOMAIN_MIN_BASELINE)),
        verdict=verdict,
    )


def analyze_similarity(
    real_summary_paths: Sequence[Path],
    synthetic_summary_paths: Sequence[Path],
    output_dir: Path,
    n_boot: int = 2000,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load real and synthetic summary vectors and compute group-level R_sim diagnostics.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    real_df = load_summary_vectors(real_summary_paths, "real")
    synth_df = load_summary_vectors(synthetic_summary_paths, "synthetic")
    df = pd.concat([real_df, synth_df], ignore_index=True)

    vectors = df[SUMMARY_COLUMNS].to_numpy(dtype=float)
    denom = compute_normalization_denominator(vectors)

    groups = sorted(df["group"].unique())
    results: List[SimilarityResult] = []

    for i, ga in enumerate(groups):
        for gb in groups[i:]:
            results.append(pairwise_group_similarity(df, ga, gb, denom=denom, n_boot=n_boot))

    results_df = pd.DataFrame([asdict(r) for r in results])
    all_vectors_path = output_dir / "all_summary_vectors_used.csv"
    results_path = output_dir / "similarity_baseline_results.csv"

    df.to_csv(all_vectors_path, index=False)
    results_df.to_csv(results_path, index=False)

    # Additional global diagnostic: separation margin
    real_groups = [g for g in groups if not g.startswith("R")]
    random_groups = [g for g in groups if g.startswith("R")]

    diagnostics = {
        "normalization_denominator": denom,
        "real_groups": real_groups,
        "random_groups": random_groups,
        "min_real_real_reference": REAL_DOMAIN_MIN_BASELINE,
        "strict_real_real_reference": STRICT_REAL_REAL_BASELINE,
    }

    # Compute max random-real median and min real-real median from results
    real_real = results_df[
        results_df["group_a"].isin(real_groups)
        & results_df["group_b"].isin(real_groups)
        & (results_df["group_a"] != results_df["group_b"])
    ]
    random_real = results_df[
        (
            results_df["group_a"].isin(random_groups)
            & results_df["group_b"].isin(real_groups)
        )
        | (
            results_df["group_a"].isin(real_groups)
            & results_df["group_b"].isin(random_groups)
        )
    ]

    diagnostics["min_observed_real_real_median"] = (
        float(real_real["median"].min()) if not real_real.empty else None
    )
    diagnostics["max_observed_random_real_median"] = (
        float(random_real["median"].max()) if not random_real.empty else None
    )
    if diagnostics["min_observed_real_real_median"] is not None and diagnostics["max_observed_random_real_median"] is not None:
        diagnostics["separation_margin_delta"] = (
            diagnostics["min_observed_real_real_median"]
            - diagnostics["max_observed_random_real_median"]
        )
    else:
        diagnostics["separation_margin_delta"] = None

    (output_dir / "similarity_baseline_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2)
    )

    return df, results_df


# ---------------------------------------------------------------------
# Template helper
# ---------------------------------------------------------------------

def write_summary_template(output_path: Path) -> None:
    """
    Create a blank summary-vector CSV template.

    Fill one row per evaluated ladder or one row per domain aggregate.
    """
    rows = [
        {
            "item_id": "helium_domain",
            "group": "helium",
            "P_depth": 0.0,
            "sigma2_GR": 0.0,
            "frag_rate": 0.0,
            "adm_persist": 0.0,
            "aniso_persist": 0.0,
        },
        {
            "item_id": "cosmology_domain",
            "group": "cosmology",
            "P_depth": 0.0,
            "sigma2_GR": 0.0,
            "frag_rate": 0.0,
            "adm_persist": 0.0,
            "aniso_persist": 0.0,
        },
        {
            "item_id": "neutrino_domain",
            "group": "neutrino",
            "P_depth": 0.0,
            "sigma2_GR": 0.0,
            "frag_rate": 0.0,
            "adm_persist": 0.0,
            "aniso_persist": 0.0,
        },
    ]
    pd.DataFrame(rows).to_csv(output_path, index=False)


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Adversarial baseline pipeline for R_sim structural universality tests."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_gen = sub.add_parser("generate", help="Generate R1/R2/R3 and optional R4 adversarial ladders.")
    p_gen.add_argument("--output-dir", type=Path, required=True)
    p_gen.add_argument("--n-ladders-per-class", type=int, default=100)
    p_gen.add_argument("--n-min", type=int, default=10)
    p_gen.add_argument("--n-max", type=int, default=1000)
    p_gen.add_argument("--seed", type=int, default=42)
    p_gen.add_argument("--real-ladder-dir", type=Path, default=None, help="Optional directory of real ladder CSVs for R4 shuffled-gap controls.")
    p_gen.add_argument("--n-shuffles-per-ladder", type=int, default=5)

    p_template = sub.add_parser("template", help="Write a summary-vector CSV template.")
    p_template.add_argument("--output", type=Path, required=True)

    p_analyze = sub.add_parser("analyze", help="Analyze real and synthetic CLE summary vectors.")
    p_analyze.add_argument("--real-summary", type=Path, nargs="+", required=True)
    p_analyze.add_argument("--synthetic-summary", type=Path, nargs="+", required=True)
    p_analyze.add_argument("--output-dir", type=Path, required=True)
    p_analyze.add_argument("--n-boot", type=int, default=2000)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "generate":
        manifest = generate_adversarial_corpus(
            output_dir=args.output_dir,
            n_ladders_per_class=args.n_ladders_per_class,
            n_points_range=(args.n_min, args.n_max),
            seed=args.seed,
            real_ladder_dir=args.real_ladder_dir,
            n_shuffles_per_ladder=args.n_shuffles_per_ladder,
        )
        print(f"Wrote {len(manifest)} adversarial ladders.")
        print(f"Manifest: {args.output_dir / 'adversarial_ladder_manifest.csv'}")

    elif args.command == "template":
        write_summary_template(args.output)
        print(f"Wrote template: {args.output}")

    elif args.command == "analyze":
        _, results = analyze_similarity(
            real_summary_paths=args.real_summary,
            synthetic_summary_paths=args.synthetic_summary,
            output_dir=args.output_dir,
            n_boot=args.n_boot,
        )
        print(f"Wrote results: {args.output_dir / 'similarity_baseline_results.csv'}")
        print(results[["group_a", "group_b", "median", "ci95_low", "ci95_high", "verdict"]].to_string(index=False))


if __name__ == "__main__":
    main()
