#!/usr/bin/env python3
"""
Generate Dataset B: an effective loop-quantum-cosmology bounce trajectory.

The generator uses the Planck-anchored radiation-matter-Lambda density model
already adopted for Datasets A and C, together with the effective LQC equation

    H^2 = H0^2 * rho_rel(a) * [1 - rho_rel(a) / rho_c_rel]

where rho_rel is measured relative to today's critical density.

The trajectory contains both branches:

    contraction -> finite bounce -> expansion

At the bounce:

    rho_rel = rho_c_rel
    H = 0
    a = a_bounce > 0

The default critical density is

    rho_c = 0.41 * rho_Planck

converted to units of today's critical density using the extracted Planck H0.
This convention is configurable from the command line.

Input:
    ../../C_planck_lcdm/parameters/extracted/
    planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv

Outputs:
    ../generated_trajectory/raw/lqc_bounce_trajectory_raw.csv
    ../generated_trajectory/diagnostics/lqc_bounce_trajectory_diagnostics.txt

No third-party packages are required.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path
from typing import Dict, List, Tuple


HERE = Path(__file__).resolve().parent
DATASET_ROOT = HERE.parent

MODEL_TAG = "base_plikHM_TTTEEE_lowl_lowE"

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
    / "lqc_bounce_trajectory_raw.csv"
)

DEFAULT_DIAGNOSTICS = (
    DATASET_ROOT
    / "generated_trajectory"
    / "diagnostics"
    / "lqc_bounce_trajectory_diagnostics.txt"
)

# SI constants
G_SI = 6.67430e-11
C_SI = 299792458.0
HBAR_SI = 1.054571817e-34
MPC_IN_M = 3.0856775814913673e22
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


def present_critical_mass_density(H0_km_s_Mpc: float) -> float:
    H0_s = H0_km_s_Mpc * 1000.0 / MPC_IN_M
    return 3.0 * H0_s**2 / (8.0 * math.pi * G_SI)


def planck_mass_density() -> float:
    return C_SI**5 / (HBAR_SI * G_SI**2)


def default_rho_c_relative(
    H0_km_s_Mpc: float,
    lqc_planck_fraction: float,
) -> Tuple[float, float, float]:
    rho_crit0 = present_critical_mass_density(H0_km_s_Mpc)
    rho_planck = planck_mass_density()
    rho_c = lqc_planck_fraction * rho_planck
    return rho_c / rho_crit0, rho_c, rho_crit0


def rho_relative(
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


def drho_da(
    a: float,
    omega_r: float,
    omega_m: float,
) -> float:
    return (
        -4.0 * omega_r / a**5
        -3.0 * omega_m / a**4
    )


def find_bounce_scale_factor(
    rho_c_rel: float,
    omega_r: float,
    omega_m: float,
    omega_lambda_dynamic: float,
) -> float:
    """
    Solve rho_relative(a) = rho_c_rel by bisection.

    rho_relative decreases monotonically with a for a > 0.
    """
    if rho_c_rel <= rho_relative(
        1.0, omega_r, omega_m, omega_lambda_dynamic
    ):
        raise ValueError(
            "rho_c_rel must exceed the present total relative density."
        )

    # Radiation-dominated estimate supplies a useful starting scale.
    estimate = (omega_r / rho_c_rel) ** 0.25
    low = max(estimate * 1.0e-6, 1.0e-300)
    high = min(max(estimate * 1.0e6, 1.0e-20), 1.0)

    while rho_relative(
        low, omega_r, omega_m, omega_lambda_dynamic
    ) < rho_c_rel:
        low *= 0.1
        if low <= 1.0e-300:
            raise ValueError("Could not bracket the bounce from below.")

    while rho_relative(
        high, omega_r, omega_m, omega_lambda_dynamic
    ) > rho_c_rel:
        high *= 10.0
        if high >= 1.0:
            high = 1.0
            break

    if rho_relative(
        high, omega_r, omega_m, omega_lambda_dynamic
    ) > rho_c_rel:
        raise ValueError("Could not bracket the bounce from above.")

    for _ in range(300):
        mid = math.sqrt(low * high)
        value = rho_relative(
            mid, omega_r, omega_m, omega_lambda_dynamic
        )
        if value > rho_c_rel:
            low = mid
        else:
            high = mid

        if abs(math.log(high / low)) < 1.0e-14:
            break

    return math.sqrt(low * high)


def lqc_y(
    a: float,
    rho_c_rel: float,
    omega_r: float,
    omega_m: float,
    omega_lambda_dynamic: float,
) -> Tuple[float, float, float]:
    """
    Return rho_rel, correction factor, and Y = (H/H0)^2.
    """
    rho = rho_relative(
        a, omega_r, omega_m, omega_lambda_dynamic
    )
    ratio = min(max(rho / rho_c_rel, 0.0), 1.0)
    correction = max(1.0 - ratio, 0.0)
    y = rho * correction
    return rho, correction, y


def quadratic_scale_grid(
    a_bounce: float,
    a_outer: float,
    points_per_branch: int,
) -> List[float]:
    """
    Grid from the exact bounce to a_outer using:
        a(x) = a_bounce + (a_outer - a_bounce) x^2

    The quadratic coordinate regularizes the integrable dt/da divergence
    at the bounce.
    """
    if points_per_branch < 2:
        raise ValueError("points_per_branch must be at least 2.")
    if not (0.0 < a_bounce < a_outer):
        raise ValueError("Require 0 < a_bounce < a_outer.")

    return [
        a_bounce
        + (a_outer - a_bounce)
        * (index / (points_per_branch - 1)) ** 2
        for index in range(points_per_branch)
    ]


def time_integrand_dx(
    x: float,
    a: float,
    a_bounce: float,
    a_outer: float,
    H0_gyr_inv: float,
    rho_c_rel: float,
    omega_r: float,
    omega_m: float,
    omega_lambda_dynamic: float,
) -> float:
    """
    Compute dt/dx for the quadratic bounce coordinate.

    The x=0 limit is evaluated analytically.
    """
    span = a_outer - a_bounce

    if x == 0.0:
        derivative_at_bounce = drho_da(
            a_bounce, omega_r, omega_m
        )
        denominator = (
            a_bounce
            * H0_gyr_inv
            * math.sqrt(max(-derivative_at_bounce * span, 1.0e-300))
        )
        return 2.0 * span / denominator

    _, _, y = lqc_y(
        a,
        rho_c_rel,
        omega_r,
        omega_m,
        omega_lambda_dynamic,
    )
    if y <= 0.0:
        raise ValueError(
            "Non-positive effective H^2 away from the exact bounce."
        )

    da_dx = 2.0 * span * x
    return da_dx / (a * H0_gyr_inv * math.sqrt(y))


def integrate_time_from_bounce(
    a_values: List[float],
    a_bounce: float,
    a_outer: float,
    H0_gyr_inv: float,
    rho_c_rel: float,
    omega_r: float,
    omega_m: float,
    omega_lambda_dynamic: float,
) -> List[float]:
    count = len(a_values)
    x_values = [
        index / (count - 1)
        for index in range(count)
    ]

    integrands = [
        time_integrand_dx(
            x,
            a,
            a_bounce,
            a_outer,
            H0_gyr_inv,
            rho_c_rel,
            omega_r,
            omega_m,
            omega_lambda_dynamic,
        )
        for x, a in zip(x_values, a_values)
    ]

    times = [0.0]
    for index in range(1, count):
        dx = x_values[index] - x_values[index - 1]
        dt = 0.5 * (
            integrands[index - 1] + integrands[index]
        ) * dx
        times.append(times[-1] + dt)

    return times


def effective_curvature_proxy(
    a: float,
    rho: float,
    rho_c_rel: float,
    omega_r: float,
    omega_m: float,
) -> float:
    """
    R / (6 H0^2) for the effective background:

        Y(a) = (H/H0)^2 = rho * (1 - rho/rho_c)
        R/(6H0^2) = 0.5*a*dY/da + 2Y
    """
    rho_prime = drho_da(a, omega_r, omega_m)
    dY_da = rho_prime * (1.0 - 2.0 * rho / rho_c_rel)
    y = rho * max(1.0 - rho / rho_c_rel, 0.0)
    return 0.5 * a * dY_da + 2.0 * y


def build_branch_rows(
    branch: str,
    sign: float,
    a_values_from_bounce: List[float],
    time_from_bounce: List[float],
    parameters: Dict[str, float],
    rho_c_rel: float,
    a_bounce: float,
) -> List[Dict[str, object]]:
    h0 = parameters["H0"]
    omega_m = parameters["Omega_m"]
    omega_r = parameters["Omega_r"]
    omega_lambda_planck = parameters["Omega_Lambda"]
    omega_lambda_dynamic = 1.0 - omega_m - omega_r

    if branch == "contraction":
        paired = list(
            zip(
                reversed(a_values_from_bounce),
                reversed(time_from_bounce),
            )
        )
    elif branch == "expansion":
        paired = list(
            zip(a_values_from_bounce, time_from_bounce)
        )
    else:
        raise ValueError(f"Unknown branch: {branch}")

    rows: List[Dict[str, object]] = []

    for local_index, (a, positive_time) in enumerate(paired):
        rho, correction, y = lqc_y(
            a,
            rho_c_rel,
            omega_r,
            omega_m,
            omega_lambda_dynamic,
        )
        h_magnitude = h0 * math.sqrt(max(y, 0.0))
        h_signed = sign * h_magnitude

        rho_m = omega_m / a**3
        rho_r = omega_r / a**4
        rho_lambda = omega_lambda_dynamic

        fraction_m = rho_m / rho
        fraction_r = rho_r / rho
        fraction_lambda = rho_lambda / rho

        curvature = effective_curvature_proxy(
            a,
            rho,
            rho_c_rel,
            omega_r,
            omega_m,
        )

        scale_margin = a
        density_margin = max(1.0 - rho / rho_c_rel, 0.0)
        curvature_margin = 1.0 / (1.0 + abs(curvature))
        boundary_margin = min(
            scale_margin,
            density_margin,
            curvature_margin,
        )

        if branch == "contraction":
            time_relative = -positive_time
            distance_to_bounce = positive_time
        else:
            time_relative = positive_time
            distance_to_bounce = positive_time

        rows.append(
            {
                "branch_local_index": local_index,
                "branch": branch,
                "time_relative_to_bounce_Gyr": time_relative,
                "distance_to_bounce_Gyr": distance_to_bounce,
                "scale_factor": a,
                "ln_scale_factor": math.log(a),
                "redshift_equivalent": 1.0 / a - 1.0,
                "H_signed_km_s_Mpc": h_signed,
                "H_magnitude_km_s_Mpc": h_magnitude,
                "E_classical_of_a": math.sqrt(rho),
                "E_lqc_of_a": math.sqrt(max(y, 0.0)),
                "E2_lqc_of_a": y,
                "rho_total_relative_to_rho_crit0": rho,
                "rho_over_rho_c": rho / rho_c_rel,
                "rho_c_relative_to_rho_crit0": rho_c_rel,
                "lqc_correction_factor": correction,
                "rho_m_relative_to_rho_crit0": rho_m,
                "rho_r_relative_to_rho_crit0": rho_r,
                "rho_lambda_relative_to_rho_crit0": rho_lambda,
                "fraction_matter_at_a": fraction_m,
                "fraction_radiation_at_a": fraction_r,
                "fraction_lambda_at_a": fraction_lambda,
                "Omega_m_planck": omega_m,
                "Omega_r_effective": omega_r,
                "Omega_Lambda_planck": omega_lambda_planck,
                "Omega_Lambda_dynamic": omega_lambda_dynamic,
                "effective_ricci_over_6H0sq": curvature,
                "scale_factor_margin_component": scale_margin,
                "density_to_bounce_margin_component": density_margin,
                "curvature_margin_component": curvature_margin,
                "boundary_margin_candidate": boundary_margin,
                "distance_from_bounce_log_a": math.log(a / a_bounce),
            }
        )

    return rows


def write_trajectory(
    path: Path,
    parameters: Dict[str, float],
    rho_c_rel: float,
    rho_c_si: float,
    rho_crit0_si: float,
    a_outer: float,
    points_per_branch: int,
) -> Dict[str, float]:
    h0 = parameters["H0"]
    omega_m = parameters["Omega_m"]
    omega_r = parameters["Omega_r"]
    omega_lambda_dynamic = 1.0 - omega_m - omega_r

    a_bounce = find_bounce_scale_factor(
        rho_c_rel,
        omega_r,
        omega_m,
        omega_lambda_dynamic,
    )

    h0_s_inv = h0 * 1000.0 / MPC_IN_M
    h0_gyr_inv = h0_s_inv * SECONDS_PER_GYR

    a_values = quadratic_scale_grid(
        a_bounce,
        a_outer,
        points_per_branch,
    )
    time_values = integrate_time_from_bounce(
        a_values,
        a_bounce,
        a_outer,
        h0_gyr_inv,
        rho_c_rel,
        omega_r,
        omega_m,
        omega_lambda_dynamic,
    )

    contraction_rows = build_branch_rows(
        "contraction",
        -1.0,
        a_values,
        time_values,
        parameters,
        rho_c_rel,
        a_bounce,
    )
    expansion_rows = build_branch_rows(
        "expansion",
        1.0,
        a_values,
        time_values,
        parameters,
        rho_c_rel,
        a_bounce,
    )

    # Keep exactly one bounce row.
    all_rows = contraction_rows[:-1] + expansion_rows

    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "sample_index",
        "branch_local_index",
        "branch",
        "time_relative_to_bounce_Gyr",
        "distance_to_bounce_Gyr",
        "scale_factor",
        "ln_scale_factor",
        "redshift_equivalent",
        "H_signed_km_s_Mpc",
        "H_magnitude_km_s_Mpc",
        "E_classical_of_a",
        "E_lqc_of_a",
        "E2_lqc_of_a",
        "rho_total_relative_to_rho_crit0",
        "rho_over_rho_c",
        "rho_c_relative_to_rho_crit0",
        "lqc_correction_factor",
        "rho_m_relative_to_rho_crit0",
        "rho_r_relative_to_rho_crit0",
        "rho_lambda_relative_to_rho_crit0",
        "fraction_matter_at_a",
        "fraction_radiation_at_a",
        "fraction_lambda_at_a",
        "Omega_m_planck",
        "Omega_r_effective",
        "Omega_Lambda_planck",
        "Omega_Lambda_dynamic",
        "effective_ricci_over_6H0sq",
        "scale_factor_margin_component",
        "density_to_bounce_margin_component",
        "curvature_margin_component",
        "boundary_margin_candidate",
        "distance_from_bounce_log_a",
    ]

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()

        for sample_index, row in enumerate(all_rows):
            serial = {"sample_index": sample_index}
            for key, value in row.items():
                if isinstance(value, float):
                    serial[key] = f"{value:.17g}"
                else:
                    serial[key] = value
            writer.writerow(serial)

    bounce_row = all_rows[len(contraction_rows) - 1]
    outer_time = time_values[-1]

    return {
        "H0": h0,
        "Omega_m": omega_m,
        "Omega_r": omega_r,
        "Omega_Lambda_dynamic": omega_lambda_dynamic,
        "rho_c_rel": rho_c_rel,
        "rho_c_si": rho_c_si,
        "rho_crit0_si": rho_crit0_si,
        "a_bounce": a_bounce,
        "a_outer": a_outer,
        "points_per_branch": float(points_per_branch),
        "total_rows": float(len(all_rows)),
        "outer_time_Gyr": outer_time,
        "bounce_H": float(bounce_row["H_signed_km_s_Mpc"]),
        "bounce_rho_ratio": float(bounce_row["rho_over_rho_c"]),
        "bounce_margin": float(
            bounce_row["boundary_margin_candidate"]
        ),
        "bounce_curvature": float(
            bounce_row["effective_ricci_over_6H0sq"]
        ),
        "minimum_scale_factor": min(
            float(row["scale_factor"]) for row in all_rows
        ),
        "maximum_density_ratio": max(
            float(row["rho_over_rho_c"]) for row in all_rows
        ),
        "maximum_H_magnitude": max(
            float(row["H_magnitude_km_s_Mpc"])
            for row in all_rows
        ),
    }


def write_diagnostics(
    path: Path,
    source: Path,
    output: Path,
    summary: Dict[str, float],
    lqc_planck_fraction: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        handle.write(
            "DATASET B — EFFECTIVE LQC BOUNCE DIAGNOSTICS\n"
        )
        handle.write("=" * 72 + "\n\n")

        handle.write(f"Parameter source: {source}\n")
        handle.write(f"Trajectory output: {output}\n\n")

        handle.write("MODEL\n")
        handle.write(
            "H^2 = H0^2 * rho_rel * (1 - rho_rel/rho_c_rel)\n"
        )
        handle.write(
            f"rho_c = {lqc_planck_fraction:.12g} * rho_Planck\n\n"
        )

        handle.write("PARAMETERS\n")
        handle.write(
            f"H0 = {summary['H0']:.12g} km s^-1 Mpc^-1\n"
        )
        handle.write(
            f"Omega_m = {summary['Omega_m']:.12g}\n"
        )
        handle.write(
            f"Omega_r_effective = {summary['Omega_r']:.12g}\n"
        )
        handle.write(
            f"Omega_Lambda_dynamic = "
            f"{summary['Omega_Lambda_dynamic']:.12g}\n\n"
        )

        handle.write("CRITICAL DENSITY\n")
        handle.write(
            f"rho_crit0 = {summary['rho_crit0_si']:.12g} kg m^-3\n"
        )
        handle.write(
            f"rho_c = {summary['rho_c_si']:.12g} kg m^-3\n"
        )
        handle.write(
            f"rho_c/rho_crit0 = {summary['rho_c_rel']:.12g}\n\n"
        )

        handle.write("BOUNCE\n")
        handle.write(
            f"a_bounce = {summary['a_bounce']:.12g}\n"
        )
        handle.write(
            f"H_at_bounce = {summary['bounce_H']:.12g} "
            "km s^-1 Mpc^-1\n"
        )
        handle.write(
            f"rho/rho_c at bounce = "
            f"{summary['bounce_rho_ratio']:.12g}\n"
        )
        handle.write(
            f"effective Ricci proxy at bounce = "
            f"{summary['bounce_curvature']:.12g}\n"
        )
        handle.write(
            f"provisional margin at bounce = "
            f"{summary['bounce_margin']:.12g}\n\n"
        )

        handle.write("SAMPLING\n")
        handle.write(
            f"outer scale factor = {summary['a_outer']:.12g}\n"
        )
        handle.write(
            f"points per branch = "
            f"{int(summary['points_per_branch'])}\n"
        )
        handle.write(
            f"total rows = {int(summary['total_rows'])}\n"
        )
        handle.write(
            f"|time| from bounce to outer endpoint = "
            f"{summary['outer_time_Gyr']:.12g} Gyr\n\n"
        )

        handle.write("BOUND CHECKS\n")
        handle.write(
            f"minimum scale factor = "
            f"{summary['minimum_scale_factor']:.12g}\n"
        )
        handle.write(
            f"maximum rho/rho_c = "
            f"{summary['maximum_density_ratio']:.12g}\n"
        )
        handle.write(
            f"maximum |H| = "
            f"{summary['maximum_H_magnitude']:.12g} "
            "km s^-1 Mpc^-1\n\n"
        )

        handle.write("EXPECTED STRUCTURE\n")
        handle.write(
            "- contraction branch: H < 0 and a decreases toward the bounce\n"
        )
        handle.write(
            "- bounce row: H = 0, rho/rho_c = 1, a = a_bounce > 0\n"
        )
        handle.write(
            "- expansion branch: H > 0 and a increases away from the bounce\n"
        )
        handle.write(
            "- density remains bounded by rho_c\n"
        )
        handle.write(
            "- effective curvature remains finite\n\n"
        )

        handle.write("METHOD NOTES\n")
        handle.write(
            "- The background matter mixture is the same Planck-anchored "
            "radiation-matter-Lambda model used for Datasets A and C.\n"
        )
        handle.write(
            "- The effective LQC correction is a model trajectory, not a "
            "direct Planck observation.\n"
        )
        handle.write(
            "- The default rho_c convention is configurable and must be "
            "preserved in provenance.\n"
        )
        handle.write(
            "- boundary_margin_candidate remains provisional.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate Dataset B effective LQC contraction-bounce-expansion "
            "trajectory."
        )
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
        help="Raw Dataset B trajectory CSV.",
    )
    parser.add_argument(
        "--diagnostics",
        type=Path,
        default=DEFAULT_DIAGNOSTICS,
        help="Diagnostics text output.",
    )
    parser.add_argument(
        "--lqc-planck-fraction",
        type=float,
        default=0.41,
        help="Critical density as a fraction of Planck mass density.",
    )
    parser.add_argument(
        "--rho-c-relative",
        type=float,
        default=None,
        help=(
            "Optional explicit rho_c/rho_crit0 override. "
            "When supplied, this overrides --lqc-planck-fraction."
        ),
    )
    parser.add_argument(
        "--a-outer",
        type=float,
        default=1.0,
        help="Outer scale factor reached on both branches.",
    )
    parser.add_argument(
        "--points-per-branch",
        type=int,
        default=2001,
        help=(
            "Samples from bounce to outer endpoint on each branch, "
            "including both endpoints. Total rows are 2*N-1."
        ),
    )
    args = parser.parse_args()

    source = args.input.resolve()
    output = args.output.resolve()
    diagnostics = args.diagnostics.resolve()

    if not source.is_file():
        raise FileNotFoundError(
            f"Compact Planck parameter CSV not found: {source}"
        )

    if args.lqc_planck_fraction <= 0.0:
        raise ValueError("lqc-planck-fraction must be positive.")

    parameters = load_best_fit_parameters(source)

    default_rel, rho_c_si_default, rho_crit0_si = (
        default_rho_c_relative(
            parameters["H0"],
            args.lqc_planck_fraction,
        )
    )

    if args.rho_c_relative is None:
        rho_c_rel = default_rel
        rho_c_si = rho_c_si_default
    else:
        if args.rho_c_relative <= 1.0:
            raise ValueError(
                "rho-c-relative must exceed the present density."
            )
        rho_c_rel = args.rho_c_relative
        rho_c_si = rho_c_rel * rho_crit0_si

    summary = write_trajectory(
        output,
        parameters,
        rho_c_rel,
        rho_c_si,
        rho_crit0_si,
        a_outer=args.a_outer,
        points_per_branch=args.points_per_branch,
    )

    write_diagnostics(
        diagnostics,
        source,
        output,
        summary,
        args.lqc_planck_fraction,
    )

    print(f"Created trajectory: {output}")
    print(f"Created diagnostics: {diagnostics}")
    print(f"Bounce scale factor: {summary['a_bounce']:.12g}")
    print(f"rho_c/rho_crit0: {summary['rho_c_rel']:.12g}")
    print(f"Rows: {int(summary['total_rows'])}")
    print(f"H at bounce: {summary['bounce_H']:.6e}")
    print(
        "Maximum rho/rho_c: "
        f"{summary['maximum_density_ratio']:.12g}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
