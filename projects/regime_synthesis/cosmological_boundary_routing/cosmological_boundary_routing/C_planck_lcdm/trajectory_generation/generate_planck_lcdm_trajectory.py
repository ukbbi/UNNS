#!/usr/bin/env python3
"""
Generate the Planck-anchored flat Lambda-CDM trajectory for Dataset C.

Input:
    ../parameters/extracted/
    planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv

Outputs:
    ../generated_trajectory/raw/planck_lcdm_trajectory_raw.csv
    ../generated_trajectory/diagnostics/planck_lcdm_trajectory_diagnostics.txt

Important:
- Omega_Lambda_planck is preserved exactly as extracted.
- Omega_Lambda_dynamic is computed explicitly as:
      1 - Omega_m - Omega_r
  and is used in the Friedmann trajectory.
- Omega_r is treated as an effective relativistic radiation density.
- boundary_margin_candidate is provisional and is not the frozen UNNS
  canonical margin definition.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path
from typing import Dict, List


MODEL_TAG = "base_plikHM_TTTEEE_lowl_lowE"
DEFAULT_INPUT = (
    Path(__file__).resolve().parent
    / ".."
    / "parameters"
    / "extracted"
    / f"planck_2018_{MODEL_TAG}_parameters.csv"
)
DEFAULT_OUTPUT = (
    Path(__file__).resolve().parent
    / ".."
    / "generated_trajectory"
    / "raw"
    / "planck_lcdm_trajectory_raw.csv"
)
DEFAULT_DIAGNOSTICS = (
    Path(__file__).resolve().parent
    / ".."
    / "generated_trajectory"
    / "diagnostics"
    / "planck_lcdm_trajectory_diagnostics.txt"
)

MPC_IN_KM = 3.0856775814913673e19
SECONDS_PER_GYR = 3.15576e16


def load_best_fit_parameters(path: Path) -> Dict[str, float]:
    values: Dict[str, float] = {}

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required_columns = {"parameter", "best_fit"}
        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                f"{path} must contain columns: "
                + ", ".join(sorted(required_columns))
            )

        for row in reader:
            name = (row.get("parameter") or "").strip()
            raw_value = (row.get("best_fit") or "").strip()
            if not name or not raw_value:
                continue
            try:
                values[name] = float(raw_value)
            except ValueError as exc:
                raise ValueError(
                    f"Invalid best_fit value for parameter {name!r}: {raw_value!r}"
                ) from exc

    required = {
        "H0",
        "Omega_m",
        "Omega_Lambda",
        "Omega_r",
        "omegabh2",
        "omegach2",
        "n_s",
        "ln_1e10_A_s",
        "tau",
        "sigma8",
        "age",
    }
    missing = sorted(required - values.keys())
    if missing:
        raise KeyError(
            "Missing required parameter(s) in compact Planck record: "
            + ", ".join(missing)
        )

    return values


def logarithmic_grid(a_min: float, a_max: float, samples: int) -> List[float]:
    if not (0.0 < a_min < a_max):
        raise ValueError("Require 0 < a_min < a_max.")
    if samples < 3:
        raise ValueError("samples must be at least 3.")

    log_min = math.log(a_min)
    log_max = math.log(a_max)
    step = (log_max - log_min) / (samples - 1)
    return [math.exp(log_min + i * step) for i in range(samples)]


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


def integrate_cosmic_time_gyr(
    scale_factors: List[float],
    e_values: List[float],
    h0_gyr_inv: float,
) -> List[float]:
    """
    Integrate dt = d(ln a) / H(a) with the trapezoid rule.

    The first value is time elapsed from a_min, not from a = 0.
    """
    times = [0.0]

    for i in range(1, len(scale_factors)):
        ln_a0 = math.log(scale_factors[i - 1])
        ln_a1 = math.log(scale_factors[i])
        f0 = 1.0 / (h0_gyr_inv * e_values[i - 1])
        f1 = 1.0 / (h0_gyr_inv * e_values[i])
        dt = 0.5 * (f0 + f1) * (ln_a1 - ln_a0)
        times.append(times[-1] + dt)

    return times


def write_trajectory(
    path: Path,
    parameters: Dict[str, float],
    a_min: float,
    a_max: float,
    samples: int,
) -> Dict[str, float]:
    h0 = parameters["H0"]
    omega_m = parameters["Omega_m"]
    omega_lambda_planck = parameters["Omega_Lambda"]
    omega_r = parameters["Omega_r"]

    omega_lambda_dynamic = 1.0 - omega_m - omega_r
    if omega_lambda_dynamic <= 0.0:
        raise ValueError(
            "Computed Omega_Lambda_dynamic is non-positive; "
            "check the input parameter record."
        )

    h0_s_inv = h0 / MPC_IN_KM
    h0_gyr_inv = h0_s_inv * SECONDS_PER_GYR

    a_values = logarithmic_grid(a_min, a_max, samples)
    e2_values = [
        e2_of_a(a, omega_r, omega_m, omega_lambda_dynamic)
        for a in a_values
    ]

    if any(value <= 0.0 or not math.isfinite(value) for value in e2_values):
        raise ValueError("Non-positive or non-finite E(a)^2 encountered.")

    e_values = [math.sqrt(value) for value in e2_values]
    time_values = integrate_cosmic_time_gyr(a_values, e_values, h0_gyr_inv)
    integrated_age = time_values[-1]

    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "sample_index",
        "redshift",
        "scale_factor",
        "ln_scale_factor",
        "cosmic_time_from_a_min_Gyr",
        "lookback_from_present_Gyr",
        "H_km_s_Mpc",
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
    ]

    closure_planck = omega_m + omega_r + omega_lambda_planck
    closure_dynamic = omega_m + omega_r + omega_lambda_dynamic

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()

        for index, (a, e2, e, cosmic_time) in enumerate(
            zip(a_values, e2_values, e_values, time_values)
        ):
            redshift = 1.0 / a - 1.0
            rho_m = omega_m / a**3
            rho_r = omega_r / a**4
            rho_lambda = omega_lambda_dynamic
            rho_total = rho_m + rho_r + rho_lambda

            fraction_m = rho_m / rho_total
            fraction_r = rho_r / rho_total
            fraction_lambda = rho_lambda / rho_total

            # For flat FLRW:
            # R/(6 H0^2) = a E dE/da + 2E^2
            # Radiation cancels from the Ricci scalar:
            # R/(6 H0^2) = 0.5*Omega_m/a^3 + 2*Omega_Lambda.
            ricci_proxy = (
                0.5 * omega_m / a**3
                + 2.0 * omega_lambda_dynamic
            )

            # Provisional UNNS margin components.
            scale_margin = min(max(a / a_max, 0.0), 1.0)
            density_margin = 1.0 / (1.0 + rho_total)
            curvature_margin = 1.0 / (1.0 + abs(ricci_proxy))
            boundary_margin = min(
                scale_margin,
                density_margin,
                curvature_margin,
            )

            writer.writerow(
                {
                    "sample_index": index,
                    "redshift": f"{redshift:.12g}",
                    "scale_factor": f"{a:.12g}",
                    "ln_scale_factor": f"{math.log(a):.12g}",
                    "cosmic_time_from_a_min_Gyr": f"{cosmic_time:.12g}",
                    "lookback_from_present_Gyr": f"{integrated_age - cosmic_time:.12g}",
                    "H_km_s_Mpc": f"{h0 * e:.12g}",
                    "E_of_a": f"{e:.12g}",
                    "E2_of_a": f"{e2:.12g}",
                    "Omega_m_planck": f"{omega_m:.12g}",
                    "Omega_r_effective": f"{omega_r:.12g}",
                    "Omega_Lambda_planck": f"{omega_lambda_planck:.12g}",
                    "Omega_Lambda_dynamic": f"{omega_lambda_dynamic:.12g}",
                    "present_closure_planck_plus_radiation": f"{closure_planck:.12g}",
                    "present_closure_dynamic": f"{closure_dynamic:.12g}",
                    "rho_m_relative_to_rho_crit0": f"{rho_m:.12g}",
                    "rho_r_relative_to_rho_crit0": f"{rho_r:.12g}",
                    "rho_lambda_relative_to_rho_crit0": f"{rho_lambda:.12g}",
                    "rho_total_relative_to_rho_crit0": f"{rho_total:.12g}",
                    "fraction_matter_at_a": f"{fraction_m:.12g}",
                    "fraction_radiation_at_a": f"{fraction_r:.12g}",
                    "fraction_lambda_at_a": f"{fraction_lambda:.12g}",
                    "ricci_scalar_over_6H0sq": f"{ricci_proxy:.12g}",
                    "scale_factor_margin_component": f"{scale_margin:.12g}",
                    "density_margin_component": f"{density_margin:.12g}",
                    "curvature_margin_component": f"{curvature_margin:.12g}",
                    "boundary_margin_candidate": f"{boundary_margin:.12g}",
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
        "integrated_age_Gyr": integrated_age,
        "planck_age_Gyr": parameters["age"],
        "age_difference_Gyr": integrated_age - parameters["age"],
        "a_min": a_min,
        "a_max": a_max,
        "samples": float(samples),
    }


def write_diagnostics(path: Path, summary: Dict[str, float], source: Path, output: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        handle.write("PLANCK LCDM TRAJECTORY GENERATION DIAGNOSTICS\n")
        handle.write("=" * 72 + "\n\n")
        handle.write(f"Input parameter record: {source}\n")
        handle.write(f"Trajectory output: {output}\n\n")

        handle.write("PARAMETER HANDLING\n")
        handle.write(f"H0 = {summary['H0']:.12g} km s^-1 Mpc^-1\n")
        handle.write(f"Omega_m = {summary['Omega_m']:.12g}\n")
        handle.write(
            f"Omega_r_effective = {summary['Omega_r']:.12g}\n"
        )
        handle.write(
            f"Omega_Lambda_planck = "
            f"{summary['Omega_Lambda_planck']:.12g}\n"
        )
        handle.write(
            f"Omega_Lambda_dynamic = "
            f"{summary['Omega_Lambda_dynamic']:.12g}\n"
        )
        handle.write(
            "Omega_Lambda_dynamic formula = 1 - Omega_m - Omega_r\n\n"
        )

        handle.write("CLOSURE CHECKS\n")
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
        handle.write(f"a_min = {summary['a_min']:.12g}\n")
        handle.write(f"a_max = {summary['a_max']:.12g}\n")
        handle.write(f"samples = {int(summary['samples'])}\n")
        handle.write("grid = logarithmic in scale factor\n\n")

        handle.write("AGE CHECK\n")
        handle.write(
            f"Integrated age from a_min = "
            f"{summary['integrated_age_Gyr']:.12g} Gyr\n"
        )
        handle.write(
            f"Planck extracted age = "
            f"{summary['planck_age_Gyr']:.12g} Gyr\n"
        )
        handle.write(
            f"Difference = {summary['age_difference_Gyr']:.12g} Gyr\n\n"
        )

        handle.write("METHOD NOTES\n")
        handle.write(
            "- Omega_Lambda_planck is retained unchanged for provenance.\n"
        )
        handle.write(
            "- Omega_Lambda_dynamic is used in E(a)^2 to enforce exact flat "
            "closure after adding the separately derived Omega_r.\n"
        )
        handle.write(
            "- Omega_r is an effective relativistic radiation density; this "
            "trajectory does not model the massive-neutrino transition in "
            "precision detail.\n"
        )
        handle.write(
            "- cosmic_time_from_a_min_Gyr begins at the chosen numerical "
            "a_min, not exactly at a = 0.\n"
        )
        handle.write(
            "- boundary_margin_candidate is provisional and must not be "
            "treated as the frozen canonical UNNS margin.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Dataset C Planck-anchored Lambda-CDM trajectory."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Compact Planck parameter CSV.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Raw trajectory CSV output.",
    )
    parser.add_argument(
        "--diagnostics",
        type=Path,
        default=DEFAULT_DIAGNOSTICS,
        help="Diagnostics text output.",
    )
    parser.add_argument(
        "--a-min",
        type=float,
        default=1.0e-8,
        help="Minimum scale factor.",
    )
    parser.add_argument(
        "--a-max",
        type=float,
        default=1.0,
        help="Maximum scale factor.",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=4001,
        help="Number of logarithmically spaced samples.",
    )
    args = parser.parse_args()

    source = args.input.resolve()
    output = args.output.resolve()
    diagnostics = args.diagnostics.resolve()

    if not source.is_file():
        raise FileNotFoundError(f"Input parameter CSV not found: {source}")

    parameters = load_best_fit_parameters(source)
    summary = write_trajectory(
        output,
        parameters,
        a_min=args.a_min,
        a_max=args.a_max,
        samples=args.samples,
    )
    write_diagnostics(diagnostics, summary, source, output)

    print(f"Created trajectory: {output}")
    print(f"Created diagnostics: {diagnostics}")
    print(
        "Omega_Lambda_planck = "
        f"{summary['Omega_Lambda_planck']:.12g}"
    )
    print(
        "Omega_Lambda_dynamic = "
        f"{summary['Omega_Lambda_dynamic']:.12g}"
    )
    print(
        "Dynamic closure residual = "
        f"{summary['closure_dynamic'] - 1.0:.6e}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
