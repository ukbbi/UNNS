#!/usr/bin/env python3
"""
Generate Dataset A: matched classical Friedmann contraction toward the
small-a singular boundary.

This is the classical comparison branch for Cosmological Boundary Routing.

Shared anchor:
    ../C_planck_lcdm/parameters/extracted/
    planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv

Default output:
    A_classical_friedmann/generated_trajectory/raw/
    classical_friedmann_approach_raw.csv

The trajectory uses the same Planck-anchored density parameters and the same
logarithmic scale-factor grid as Dataset C, but orders the evolution from
a = 1 down to a = 1e-8 and assigns the contracting branch H < 0.

No third-party packages are required.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path
from typing import Dict, List


MODEL_TAG = "base_plikHM_TTTEEE_lowl_lowE"

HERE = Path(__file__).resolve().parent
DATASET_ROOT = HERE.parent

DEFAULT_INPUT = (
    DATASET_ROOT.parent
    / "C_planck_lcdm"
    / "parameters"
    / "extracted"
    / f"planck_2018_{MODEL_TAG}_parameters.csv"
)

DEFAULT_OUTPUT = (
    DATASET_ROOT
    / "generated_trajectory"
    / "raw"
    / "classical_friedmann_approach_raw.csv"
)

DEFAULT_DIAGNOSTICS = (
    DATASET_ROOT
    / "generated_trajectory"
    / "diagnostics"
    / "classical_friedmann_approach_diagnostics.txt"
)

MPC_IN_KM = 3.0856775814913673e19
SECONDS_PER_GYR = 3.15576e16


def load_best_fit_parameters(path: Path) -> Dict[str, float]:
    values: Dict[str, float] = {}

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        if not {"parameter", "best_fit"}.issubset(fields):
            raise ValueError(
                f"{path} must contain 'parameter' and 'best_fit' columns."
            )

        for row in reader:
            name = (row.get("parameter") or "").strip()
            raw = (row.get("best_fit") or "").strip()
            if not name or not raw:
                continue
            try:
                value = float(raw)
            except ValueError as exc:
                raise ValueError(
                    f"Invalid best_fit value for {name!r}: {raw!r}"
                ) from exc
            if not math.isfinite(value):
                raise ValueError(
                    f"Non-finite best_fit value for {name!r}."
                )
            values[name] = value

    required = {
        "H0",
        "Omega_m",
        "Omega_Lambda",
        "Omega_r",
        "age",
    }
    missing = sorted(required - values.keys())
    if missing:
        raise KeyError(
            "Missing required parameter(s): " + ", ".join(missing)
        )

    return values


def logarithmic_grid_descending(
    a_min: float,
    a_max: float,
    samples: int,
) -> List[float]:
    if not (0.0 < a_min < a_max):
        raise ValueError("Require 0 < a_min < a_max.")
    if samples < 3:
        raise ValueError("samples must be at least 3.")

    log_min = math.log(a_min)
    log_max = math.log(a_max)
    step = (log_max - log_min) / (samples - 1)

    ascending = [
        math.exp(log_min + index * step)
        for index in range(samples)
    ]
    return list(reversed(ascending))


def e2_of_a(
    a: float,
    omega_r: float,
    omega_m: float,
    omega_lambda_dynamic: float,
) -> float:
    return (
        omega_r / a**4
        + omega_m / a**3
        + omega_lambda_dynamic
    )


def integrate_contraction_time_gyr(
    scale_factors_desc: List[float],
    e_values: List[float],
    h0_gyr_inv: float,
) -> List[float]:
    """
    Integrate positive elapsed contraction time using:
        dt = -d(ln a) / (H0 E(a))
    because d(ln a) < 0 on the descending grid.
    """
    elapsed = [0.0]

    for index in range(1, len(scale_factors_desc)):
        ln_a0 = math.log(scale_factors_desc[index - 1])
        ln_a1 = math.log(scale_factors_desc[index])

        f0 = 1.0 / (h0_gyr_inv * e_values[index - 1])
        f1 = 1.0 / (h0_gyr_inv * e_values[index])

        delta_ln_a = ln_a1 - ln_a0
        dt = -0.5 * (f0 + f1) * delta_ln_a
        elapsed.append(elapsed[-1] + dt)

    return elapsed


def write_trajectory(
    path: Path,
    parameters: Dict[str, float],
    a_min: float,
    a_max: float,
    samples: int,
) -> Dict[str, float]:
    h0 = parameters["H0"]
    omega_m = parameters["Omega_m"]
    omega_r = parameters["Omega_r"]
    omega_lambda_planck = parameters["Omega_Lambda"]
    omega_lambda_dynamic = 1.0 - omega_m - omega_r

    if omega_lambda_dynamic <= 0.0:
        raise ValueError(
            "Computed Omega_Lambda_dynamic is non-positive."
        )

    h0_s_inv = h0 / MPC_IN_KM
    h0_gyr_inv = h0_s_inv * SECONDS_PER_GYR

    a_values = logarithmic_grid_descending(
        a_min=a_min,
        a_max=a_max,
        samples=samples,
    )

    e2_values = [
        e2_of_a(
            a,
            omega_r,
            omega_m,
            omega_lambda_dynamic,
        )
        for a in a_values
    ]

    if any(
        value <= 0.0 or not math.isfinite(value)
        for value in e2_values
    ):
        raise ValueError("Invalid E(a)^2 encountered.")

    e_values = [math.sqrt(value) for value in e2_values]
    elapsed_values = integrate_contraction_time_gyr(
        a_values,
        e_values,
        h0_gyr_inv,
    )

    closure_planck = (
        omega_m + omega_r + omega_lambda_planck
    )
    closure_dynamic = (
        omega_m + omega_r + omega_lambda_dynamic
    )

    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "sample_index",
        "trajectory_role",
        "evolution_direction",
        "redshift",
        "scale_factor",
        "ln_scale_factor",
        "contraction_elapsed_time_Gyr",
        "time_to_numerical_cutoff_Gyr",
        "H_signed_km_s_Mpc",
        "H_magnitude_km_s_Mpc",
        "E_of_a",
        "E2_of_a",
        "Omega_m_planck",
        "Omega_r_effective",
        "Omega_Lambda_planck",
        "Omega_Lambda_dynamic",
        "present_closure_planck_plus_radiation",
        "present_closure_dynamic",
        "rho_m_relative_to_rho_crit0",
        "rho_r_relative_to_rho_crit0",
        "rho_lambda_relative_to_rho_crit0",
        "rho_total_relative_to_rho_crit0",
        "fraction_matter_at_a",
        "fraction_radiation_at_a",
        "fraction_lambda_at_a",
        "ricci_scalar_over_6H0sq",
        "scale_factor_margin_component",
        "density_margin_component",
        "curvature_margin_component",
        "boundary_margin_candidate",
        "distance_to_cutoff_log_a",
    ]

    total_elapsed = elapsed_values[-1]

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()

        for index, (
            a,
            e2,
            e,
            elapsed,
        ) in enumerate(
            zip(
                a_values,
                e2_values,
                e_values,
                elapsed_values,
            )
        ):
            redshift = 1.0 / a - 1.0

            rho_m = omega_m / a**3
            rho_r = omega_r / a**4
            rho_lambda = omega_lambda_dynamic
            rho_total = rho_m + rho_r + rho_lambda

            fraction_m = rho_m / rho_total
            fraction_r = rho_r / rho_total
            fraction_lambda = rho_lambda / rho_total

            ricci_proxy = (
                0.5 * omega_m / a**3
                + 2.0 * omega_lambda_dynamic
            )

            scale_margin = min(max(a / a_max, 0.0), 1.0)
            density_margin = 1.0 / (1.0 + rho_total)
            curvature_margin = 1.0 / (
                1.0 + abs(ricci_proxy)
            )
            boundary_margin = min(
                scale_margin,
                density_margin,
                curvature_margin,
            )

            distance_to_cutoff = (
                math.log(a) - math.log(a_min)
            )

            writer.writerow(
                {
                    "sample_index": index,
                    "trajectory_role": "classical_singular_approach",
                    "evolution_direction": "contraction",
                    "redshift": f"{redshift:.12g}",
                    "scale_factor": f"{a:.12g}",
                    "ln_scale_factor": f"{math.log(a):.12g}",
                    "contraction_elapsed_time_Gyr": (
                        f"{elapsed:.12g}"
                    ),
                    "time_to_numerical_cutoff_Gyr": (
                        f"{total_elapsed - elapsed:.12g}"
                    ),
                    "H_signed_km_s_Mpc": f"{-h0 * e:.12g}",
                    "H_magnitude_km_s_Mpc": f"{h0 * e:.12g}",
                    "E_of_a": f"{e:.12g}",
                    "E2_of_a": f"{e2:.12g}",
                    "Omega_m_planck": f"{omega_m:.12g}",
                    "Omega_r_effective": f"{omega_r:.12g}",
                    "Omega_Lambda_planck": (
                        f"{omega_lambda_planck:.12g}"
                    ),
                    "Omega_Lambda_dynamic": (
                        f"{omega_lambda_dynamic:.12g}"
                    ),
                    "present_closure_planck_plus_radiation": (
                        f"{closure_planck:.12g}"
                    ),
                    "present_closure_dynamic": (
                        f"{closure_dynamic:.12g}"
                    ),
                    "rho_m_relative_to_rho_crit0": (
                        f"{rho_m:.12g}"
                    ),
                    "rho_r_relative_to_rho_crit0": (
                        f"{rho_r:.12g}"
                    ),
                    "rho_lambda_relative_to_rho_crit0": (
                        f"{rho_lambda:.12g}"
                    ),
                    "rho_total_relative_to_rho_crit0": (
                        f"{rho_total:.12g}"
                    ),
                    "fraction_matter_at_a": (
                        f"{fraction_m:.12g}"
                    ),
                    "fraction_radiation_at_a": (
                        f"{fraction_r:.12g}"
                    ),
                    "fraction_lambda_at_a": (
                        f"{fraction_lambda:.12g}"
                    ),
                    "ricci_scalar_over_6H0sq": (
                        f"{ricci_proxy:.12g}"
                    ),
                    "scale_factor_margin_component": (
                        f"{scale_margin:.12g}"
                    ),
                    "density_margin_component": (
                        f"{density_margin:.12g}"
                    ),
                    "curvature_margin_component": (
                        f"{curvature_margin:.12g}"
                    ),
                    "boundary_margin_candidate": (
                        f"{boundary_margin:.12g}"
                    ),
                    "distance_to_cutoff_log_a": (
                        f"{distance_to_cutoff:.12g}"
                    ),
                }
            )

    return {
        "H0": h0,
        "Omega_m": omega_m,
        "Omega_r": omega_r,
        "Omega_Lambda_planck": omega_lambda_planck,
        "Omega_Lambda_dynamic": omega_lambda_dynamic,
        "closure_planck_plus_radiation": closure_planck,
        "closure_dynamic": closure_dynamic,
        "a_min": a_min,
        "a_max": a_max,
        "samples": float(samples),
        "contraction_elapsed_Gyr": total_elapsed,
        "initial_H_signed": -h0 * e_values[0],
        "terminal_H_signed": -h0 * e_values[-1],
        "initial_margin": min(
            1.0,
            1.0 / (
                1.0
                + omega_m
                + omega_r
                + omega_lambda_dynamic
            ),
            1.0 / (
                1.0
                + abs(
                    0.5 * omega_m
                    + 2.0 * omega_lambda_dynamic
                )
            ),
        ),
        "terminal_margin": min(
            a_min / a_max,
            1.0 / (
                1.0
                + omega_m / a_min**3
                + omega_r / a_min**4
                + omega_lambda_dynamic
            ),
            1.0 / (
                1.0
                + abs(
                    0.5 * omega_m / a_min**3
                    + 2.0 * omega_lambda_dynamic
                )
            ),
        ),
    }


def write_diagnostics(
    path: Path,
    source: Path,
    output: Path,
    summary: Dict[str, float],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        handle.write(
            "DATASET A — CLASSICAL FRIEDMANN APPROACH DIAGNOSTICS\n"
        )
        handle.write("=" * 72 + "\n\n")

        handle.write(f"Parameter source: {source}\n")
        handle.write(f"Trajectory output: {output}\n\n")

        handle.write("ROLE\n")
        handle.write(
            "Matched classical contracting branch approaching the "
            "small-a numerical singular cutoff.\n\n"
        )

        handle.write("PARAMETERS\n")
        handle.write(
            f"H0 = {summary['H0']:.12g} km s^-1 Mpc^-1\n"
        )
        handle.write(
            f"Omega_m = {summary['Omega_m']:.12g}\n"
        )
        handle.write(
            f"Omega_r_effective = "
            f"{summary['Omega_r']:.12g}\n"
        )
        handle.write(
            f"Omega_Lambda_planck = "
            f"{summary['Omega_Lambda_planck']:.12g}\n"
        )
        handle.write(
            f"Omega_Lambda_dynamic = "
            f"{summary['Omega_Lambda_dynamic']:.12g}\n\n"
        )

        handle.write("CLOSURE\n")
        handle.write(
            "Planck Lambda plus explicit radiation = "
            f"{summary['closure_planck_plus_radiation']:.15g}\n"
        )
        handle.write(
            "Dynamic flat closure = "
            f"{summary['closure_dynamic']:.15g}\n"
        )
        handle.write(
            "Dynamic closure residual = "
            f"{summary['closure_dynamic'] - 1.0:.6e}\n\n"
        )

        handle.write("SAMPLING\n")
        handle.write(
            f"a_start = {summary['a_max']:.12g}\n"
        )
        handle.write(
            f"a_cutoff = {summary['a_min']:.12g}\n"
        )
        handle.write(
            f"samples = {int(summary['samples'])}\n"
        )
        handle.write(
            "grid = logarithmic in scale factor, descending\n\n"
        )

        handle.write("CONTRACTION CHECK\n")
        handle.write(
            f"elapsed contraction time to cutoff = "
            f"{summary['contraction_elapsed_Gyr']:.12g} Gyr\n"
        )
        handle.write(
            f"initial H_signed = "
            f"{summary['initial_H_signed']:.12g} "
            "km s^-1 Mpc^-1\n"
        )
        handle.write(
            f"terminal H_signed = "
            f"{summary['terminal_H_signed']:.12g} "
            "km s^-1 Mpc^-1\n"
        )
        handle.write(
            f"initial provisional margin = "
            f"{summary['initial_margin']:.12g}\n"
        )
        handle.write(
            f"terminal provisional margin = "
            f"{summary['terminal_margin']:.12g}\n\n"
        )

        handle.write("EXPECTED MONOTONICITY\n")
        handle.write("- scale factor: decreasing\n")
        handle.write("- contraction elapsed time: increasing\n")
        handle.write("- |H|: increasing\n")
        handle.write("- total density: increasing\n")
        handle.write("- curvature proxy: increasing\n")
        handle.write("- provisional boundary margin: decreasing\n\n")

        handle.write("METHOD NOTES\n")
        handle.write(
            "- H is negative to identify the contracting branch.\n"
        )
        handle.write(
            "- The trajectory stops at a = a_min and does not numerically "
            "evaluate a = 0.\n"
        )
        handle.write(
            "- Omega_r remains an effective relativistic radiation density.\n"
        )
        handle.write(
            "- boundary_margin_candidate remains provisional and is not "
            "the frozen shared A/B/C margin.\n"
        )
        handle.write(
            "- Dataset A and Dataset C share the same background "
            "Friedmann magnitude E(a); their research roles and trajectory "
            "orientations differ.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate Dataset A classical Friedmann contraction toward "
            "the small-a singular cutoff."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
    )
    parser.add_argument(
        "--diagnostics",
        type=Path,
        default=DEFAULT_DIAGNOSTICS,
    )
    parser.add_argument(
        "--a-min",
        type=float,
        default=1.0e-8,
    )
    parser.add_argument(
        "--a-max",
        type=float,
        default=1.0,
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=4001,
    )
    args = parser.parse_args()

    source = args.input.resolve()
    output = args.output.resolve()
    diagnostics = args.diagnostics.resolve()

    if not source.is_file():
        raise FileNotFoundError(
            f"Compact Planck parameter CSV not found: {source}"
        )

    parameters = load_best_fit_parameters(source)
    summary = write_trajectory(
        output,
        parameters,
        a_min=args.a_min,
        a_max=args.a_max,
        samples=args.samples,
    )
    write_diagnostics(
        diagnostics,
        source,
        output,
        summary,
    )

    print(f"Created trajectory: {output}")
    print(f"Created diagnostics: {diagnostics}")
    print(
        "Dynamic closure residual = "
        f"{summary['closure_dynamic'] - 1.0:.6e}"
    )
    print(
        "Initial H_signed = "
        f"{summary['initial_H_signed']:.12g}"
    )
    print(
        "Terminal H_signed = "
        f"{summary['terminal_H_signed']:.12g}"
    )
    print(
        "Terminal provisional margin = "
        f"{summary['terminal_margin']:.12g}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
