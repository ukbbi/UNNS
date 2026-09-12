#!/usr/bin/env python3
"""
generate_lqc_bounce_trajectory_v2_2.py

Generate Dataset B: a resolved effective loop-quantum-cosmology bounce
trajectory using a hybrid sampling grid.

Model:
    H^2 = H0^2 * rho_rel(a) * [1 - rho_rel(a) / rho_c_rel]

Hybrid branch sampling:
    1. Near-bounce region:
       x = sqrt(1 - rho/rho_c), logarithmically sampled.
    2. Intermediate/classical region:
       scale factor a, logarithmically sampled.

The regions meet at a configurable density ratio, default:

    rho/rho_c = 0.01

Version 2.2 guarantees:
    - exactly one bounce row;
    - H = 0 at the bounce;
    - rho/rho_c = 1 at the bounce;
    - bounded density;
    - dense quantum-region resolution;
    - resolved outer cosmological history;
    - continuous time integration across the hybrid-grid junction.

Input:
    ../../C_planck_lcdm/parameters/extracted/
    planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv

Outputs:
    ../generated_trajectory/raw/lqc_bounce_trajectory_raw_v2_2.csv
    ../generated_trajectory/diagnostics/lqc_bounce_trajectory_diagnostics_v2_2.txt

No third-party packages are required.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path
from typing import Dict, List, Tuple


SCRIPT_VERSION = "2.2.0"
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
    / "lqc_bounce_trajectory_raw_v2_2.csv"
)

DEFAULT_DIAGNOSTICS = (
    DATASET_ROOT
    / "generated_trajectory"
    / "diagnostics"
    / "lqc_bounce_trajectory_diagnostics_v2_2.txt"
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
                raise ValueError(f"Non-finite value for {name!r}.")
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
    h0_s = H0_km_s_Mpc * 1000.0 / MPC_IN_M
    return 3.0 * h0_s**2 / (8.0 * math.pi * G_SI)


def planck_mass_density() -> float:
    return C_SI**5 / (HBAR_SI * G_SI**2)


def critical_density_values(
    H0_km_s_Mpc: float,
    lqc_planck_fraction: float,
) -> Tuple[float, float, float]:
    rho_crit0 = present_critical_mass_density(H0_km_s_Mpc)
    rho_planck = planck_mass_density()
    rho_c_si = lqc_planck_fraction * rho_planck
    rho_c_rel = rho_c_si / rho_crit0
    return rho_c_rel, rho_c_si, rho_crit0


def rho_relative(
    a: float,
    omega_r: float,
    omega_m: float,
    omega_lambda: float,
) -> float:
    return (
        omega_r / a**4
        + omega_m / a**3
        + omega_lambda
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
    omega_lambda: float,
) -> float:
    if rho_c_rel <= rho_relative(
        1.0, omega_r, omega_m, omega_lambda
    ):
        raise ValueError(
            "rho_c_rel must exceed the present total density."
        )

    estimate = (omega_r / rho_c_rel) ** 0.25
    low = max(estimate * 1.0e-8, 1.0e-300)
    high = min(max(estimate * 1.0e8, 1.0e-20), 1.0)

    while rho_relative(
        low, omega_r, omega_m, omega_lambda
    ) < rho_c_rel:
        low *= 0.1

    while rho_relative(
        high, omega_r, omega_m, omega_lambda
    ) > rho_c_rel:
        high *= 10.0
        if high >= 1.0:
            high = 1.0
            break

    for _ in range(320):
        mid = math.sqrt(low * high)
        value = rho_relative(
            mid, omega_r, omega_m, omega_lambda
        )
        if value > rho_c_rel:
            low = mid
        else:
            high = mid

        if abs(math.log(high / low)) < 1.0e-15:
            break

    return math.sqrt(low * high)


def solve_a_for_density(
    target_rho: float,
    a_low: float,
    a_high: float,
    omega_r: float,
    omega_m: float,
    omega_lambda: float,
) -> float:
    rho_low = rho_relative(
        a_low, omega_r, omega_m, omega_lambda
    )
    rho_high = rho_relative(
        a_high, omega_r, omega_m, omega_lambda
    )

    if target_rho >= rho_low:
        return a_low
    if target_rho <= rho_high:
        return a_high

    low = a_low
    high = a_high

    for _ in range(260):
        mid = math.sqrt(low * high)
        value = rho_relative(
            mid, omega_r, omega_m, omega_lambda
        )

        if value > target_rho:
            low = mid
        else:
            high = mid

        if abs(math.log(high / low)) < 1.0e-14:
            break

    return math.sqrt(low * high)


def logarithmic_values(
    minimum: float,
    maximum: float,
    count: int,
) -> List[float]:
    if count < 2:
        raise ValueError("Logarithmic grid requires at least 2 values.")
    if not (0.0 < minimum < maximum):
        raise ValueError("Require 0 < minimum < maximum.")

    log_min = math.log(minimum)
    log_max = math.log(maximum)

    values = [
        math.exp(
            log_min
            + index * (log_max - log_min) / (count - 1)
        )
        for index in range(count)
    ]
    values[0] = minimum
    values[-1] = maximum
    return values


def build_hybrid_branch(
    parameters: Dict[str, float],
    rho_c_rel: float,
    a_outer: float,
    near_points: int,
    outer_points: int,
    transition_ratio: float,
    x_min: float,
) -> Tuple[List[Dict[str, float]], float, float]:
    if near_points < 3:
        raise ValueError("near_points must be at least 3.")
    if outer_points < 2:
        raise ValueError("outer_points must be at least 2.")
    if not (0.0 < transition_ratio < 1.0):
        raise ValueError("transition_ratio must lie in (0,1).")

    omega_m = parameters["Omega_m"]
    omega_r = parameters["Omega_r"]
    omega_lambda = 1.0 - omega_m - omega_r

    a_bounce = find_bounce_scale_factor(
        rho_c_rel,
        omega_r,
        omega_m,
        omega_lambda,
    )

    transition_rho = transition_ratio * rho_c_rel
    a_transition = solve_a_for_density(
        transition_rho,
        a_bounce,
        a_outer,
        omega_r,
        omega_m,
        omega_lambda,
    )

    x_transition = math.sqrt(1.0 - transition_ratio)
    if not (0.0 < x_min < x_transition):
        raise ValueError(
            "x_min must be positive and below the transition x."
        )

    # Near-bounce section includes exact bounce and transition.
    x_nonzero = logarithmic_values(
        x_min,
        x_transition,
        near_points - 1,
    )

    near_rows: List[Dict[str, float]] = [
        {
            "grid_region": 0.0,
            "grid_coordinate": 0.0,
            "x_bounce_distance": 0.0,
            "rho_over_rho_c": 1.0,
            "rho_total_relative_to_rho_crit0": rho_c_rel,
            "scale_factor": a_bounce,
            "lqc_correction_factor": 0.0,
            "E2_lqc_of_a": 0.0,
            "E_lqc_of_a": 0.0,
        }
    ]

    for x in x_nonzero:
        correction = x * x
        ratio = 1.0 - correction
        if ratio <= 0.0:
            ratio = transition_ratio
            correction = 1.0 - ratio

        target_rho = ratio * rho_c_rel
        a = solve_a_for_density(
            target_rho,
            a_bounce,
            a_transition,
            omega_r,
            omega_m,
            omega_lambda,
        )
        y = target_rho * correction

        near_rows.append(
            {
                "grid_region": 0.0,
                "grid_coordinate": x,
                "x_bounce_distance": x,
                "rho_over_rho_c": ratio,
                "rho_total_relative_to_rho_crit0": target_rho,
                "scale_factor": a,
                "lqc_correction_factor": correction,
                "E2_lqc_of_a": y,
                "E_lqc_of_a": math.sqrt(max(y, 0.0)),
            }
        )

    # Force exact transition values.
    near_rows[-1].update(
        {
            "x_bounce_distance": x_transition,
            "rho_over_rho_c": transition_ratio,
            "rho_total_relative_to_rho_crit0": transition_rho,
            "scale_factor": a_transition,
            "lqc_correction_factor": 1.0 - transition_ratio,
            "E2_lqc_of_a": (
                transition_rho * (1.0 - transition_ratio)
            ),
            "E_lqc_of_a": math.sqrt(
                transition_rho * (1.0 - transition_ratio)
            ),
        }
    )

    # Outer section includes transition and a_outer.
    outer_a = logarithmic_values(
        a_transition,
        a_outer,
        outer_points,
    )

    outer_rows: List[Dict[str, float]] = []
    for a in outer_a:
        rho = rho_relative(
            a, omega_r, omega_m, omega_lambda
        )
        ratio = min(max(rho / rho_c_rel, 0.0), 1.0)
        correction = max(1.0 - ratio, 0.0)
        y = rho * correction

        outer_rows.append(
            {
                "grid_region": 1.0,
                "grid_coordinate": math.log(a),
                "x_bounce_distance": math.sqrt(correction),
                "rho_over_rho_c": ratio,
                "rho_total_relative_to_rho_crit0": rho,
                "scale_factor": a,
                "lqc_correction_factor": correction,
                "E2_lqc_of_a": y,
                "E_lqc_of_a": math.sqrt(max(y, 0.0)),
            }
        )

    # Remove duplicate transition row from outer section.
    hybrid_rows = near_rows + outer_rows[1:]

    expected = near_points + outer_points - 1
    if len(hybrid_rows) != expected:
        raise ValueError(
            f"Hybrid-grid count mismatch: {len(hybrid_rows)} != {expected}"
        )

    return hybrid_rows, a_bounce, a_transition


def near_dt_dx(
    row: Dict[str, float],
    a_bounce: float,
    H0_gyr_inv: float,
    rho_c_rel: float,
    omega_r: float,
    omega_m: float,
) -> float:
    x = row["x_bounce_distance"]
    a = row["scale_factor"]
    rho_prime = drho_da(a, omega_r, omega_m)

    if rho_prime >= 0.0:
        raise ValueError("Expected drho/da < 0.")

    if x == 0.0:
        return (
            2.0
            * math.sqrt(rho_c_rel)
            / (a_bounce * H0_gyr_inv * abs(rho_prime))
        )

    da_dx = (-2.0 * x * rho_c_rel) / rho_prime
    e_lqc = row["E_lqc_of_a"]
    if e_lqc <= 0.0:
        raise ValueError("Expected E_lqc > 0 away from bounce.")

    return da_dx / (a * H0_gyr_inv * e_lqc)


def integrate_hybrid_time(
    rows: List[Dict[str, float]],
    near_points: int,
    a_bounce: float,
    H0_gyr_inv: float,
    rho_c_rel: float,
    omega_r: float,
    omega_m: float,
) -> List[float]:
    """
    Integrate from bounce outward.

    Near region:
        trapezoid in x.

    Outer region:
        trapezoid in u = ln(a), with dt/du = 1/(H0 E_lqc).
    """
    if len(rows) < near_points:
        raise ValueError("Hybrid rows shorter than near section.")

    times = [0.0]

    # Near section, indices 0..near_points-1.
    near_integrands = [
        near_dt_dx(
            rows[index],
            a_bounce,
            H0_gyr_inv,
            rho_c_rel,
            omega_r,
            omega_m,
        )
        for index in range(near_points)
    ]

    for index in range(1, near_points):
        x0 = rows[index - 1]["x_bounce_distance"]
        x1 = rows[index]["x_bounce_distance"]
        dx = x1 - x0
        dt = 0.5 * (
            near_integrands[index - 1]
            + near_integrands[index]
        ) * dx
        times.append(times[-1] + dt)

    # Outer section starts at transition index near_points-1.
    for index in range(near_points, len(rows)):
        previous = rows[index - 1]
        current = rows[index]

        u0 = math.log(previous["scale_factor"])
        u1 = math.log(current["scale_factor"])

        e0 = previous["E_lqc_of_a"]
        e1 = current["E_lqc_of_a"]
        if e0 <= 0.0 or e1 <= 0.0:
            raise ValueError(
                "Outer integration encountered non-positive E_lqc."
            )

        f0 = 1.0 / (H0_gyr_inv * e0)
        f1 = 1.0 / (H0_gyr_inv * e1)
        dt = 0.5 * (f0 + f1) * (u1 - u0)
        times.append(times[-1] + dt)

    if len(times) != len(rows):
        raise ValueError("Time-grid length mismatch.")

    return times


def effective_curvature_proxy(
    a: float,
    rho: float,
    rho_c_rel: float,
    omega_r: float,
    omega_m: float,
) -> float:
    rho_prime = drho_da(a, omega_r, omega_m)
    dY_da = rho_prime * (1.0 - 2.0 * rho / rho_c_rel)
    y = rho * max(1.0 - rho / rho_c_rel, 0.0)
    return 0.5 * a * dY_da + 2.0 * y


def decorate_branch(
    branch: str,
    sign: float,
    base_rows: List[Dict[str, float]],
    time_from_bounce: List[float],
    parameters: Dict[str, float],
    rho_c_rel: float,
    a_bounce: float,
    near_points: int,
) -> List[Dict[str, object]]:
    omega_m = parameters["Omega_m"]
    omega_r = parameters["Omega_r"]
    omega_lambda_planck = parameters["Omega_Lambda"]
    omega_lambda = 1.0 - omega_m - omega_r
    h0 = parameters["H0"]

    if branch == "contraction":
        pairs = list(
            zip(
                reversed(base_rows),
                reversed(time_from_bounce),
            )
        )
    elif branch == "expansion":
        pairs = list(zip(base_rows, time_from_bounce))
    else:
        raise ValueError(f"Unknown branch: {branch}")

    output: List[Dict[str, object]] = []

    for local_index, (base, t_abs) in enumerate(pairs):
        a = base["scale_factor"]
        ratio = base["rho_over_rho_c"]
        rho = base["rho_total_relative_to_rho_crit0"]
        correction = base["lqc_correction_factor"]
        e_lqc = base["E_lqc_of_a"]
        e2_lqc = base["E2_lqc_of_a"]
        is_bounce = base["x_bounce_distance"] == 0.0

        if is_bounce:
            a = a_bounce
            ratio = 1.0
            rho = rho_c_rel
            correction = 0.0
            e_lqc = 0.0
            e2_lqc = 0.0
            h_magnitude = 0.0
            h_signed = 0.0
        else:
            h_magnitude = h0 * e_lqc
            h_signed = sign * h_magnitude

        rho_m = omega_m / a**3
        rho_r = omega_r / a**4
        rho_lambda = omega_lambda

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
        density_margin = max(1.0 - ratio, 0.0)
        curvature_margin = 1.0 / (1.0 + abs(curvature))
        boundary_margin = min(
            scale_margin,
            density_margin,
            curvature_margin,
        )

        grid_region = (
            "near_bounce"
            if base["grid_region"] == 0.0
            else "outer_log_a"
        )

        output.append(
            {
                "branch_local_index": local_index,
                "branch": branch,
                "time_relative_to_bounce_Gyr": (
                    -t_abs if branch == "contraction" else t_abs
                ),
                "distance_to_bounce_Gyr": t_abs,
                "sampling_region": grid_region,
                "x_bounce_distance": base["x_bounce_distance"],
                "scale_factor": a,
                "ln_scale_factor": math.log(a),
                "redshift_equivalent": 1.0 / a - 1.0,
                "H_signed_km_s_Mpc": h_signed,
                "H_magnitude_km_s_Mpc": h_magnitude,
                "E_classical_of_a": math.sqrt(rho),
                "E_lqc_of_a": e_lqc,
                "E2_lqc_of_a": e2_lqc,
                "rho_total_relative_to_rho_crit0": rho,
                "rho_over_rho_c": ratio,
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
                "Omega_Lambda_dynamic": omega_lambda,
                "effective_ricci_over_6H0sq": curvature,
                "scale_factor_margin_component": scale_margin,
                "density_to_bounce_margin_component": density_margin,
                "curvature_margin_component": curvature_margin,
                "boundary_margin_candidate": boundary_margin,
                "distance_from_bounce_log_a": math.log(a / a_bounce),
                "is_exact_bounce": "yes" if is_bounce else "no",
            }
        )

    return output


def write_trajectory(
    path: Path,
    parameters: Dict[str, float],
    rho_c_rel: float,
    rho_c_si: float,
    rho_crit0_si: float,
    a_outer: float,
    near_points: int,
    outer_points: int,
    transition_ratio: float,
    x_min: float,
) -> Dict[str, float]:
    h0 = parameters["H0"]
    omega_m = parameters["Omega_m"]
    omega_r = parameters["Omega_r"]

    base_rows, a_bounce, a_transition = build_hybrid_branch(
        parameters,
        rho_c_rel,
        a_outer,
        near_points,
        outer_points,
        transition_ratio,
        x_min,
    )

    h0_s_inv = h0 * 1000.0 / MPC_IN_M
    h0_gyr_inv = h0_s_inv * SECONDS_PER_GYR

    times = integrate_hybrid_time(
        base_rows,
        near_points,
        a_bounce,
        h0_gyr_inv,
        rho_c_rel,
        omega_r,
        omega_m,
    )

    contraction = decorate_branch(
        "contraction",
        -1.0,
        base_rows,
        times,
        parameters,
        rho_c_rel,
        a_bounce,
        near_points,
    )
    expansion = decorate_branch(
        "expansion",
        1.0,
        base_rows,
        times,
        parameters,
        rho_c_rel,
        a_bounce,
        near_points,
    )

    # Keep one exact bounce row.
    all_rows = contraction[:-1] + expansion

    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "sample_index",
        "branch_local_index",
        "branch",
        "time_relative_to_bounce_Gyr",
        "distance_to_bounce_Gyr",
        "sampling_region",
        "x_bounce_distance",
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
        "is_exact_bounce",
    ]

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()

        for sample_index, row in enumerate(all_rows):
            serial = {"sample_index": sample_index}
            for key, value in row.items():
                serial[key] = (
                    f"{value:.17g}"
                    if isinstance(value, float)
                    else value
                )
            writer.writerow(serial)

    bounce_rows = [
        row for row in all_rows
        if row["is_exact_bounce"] == "yes"
    ]
    if len(bounce_rows) != 1:
        raise ValueError(
            f"Expected exactly one bounce row, found {len(bounce_rows)}."
        )

    bounce = bounce_rows[0]
    quantum_rows = [
        row for row in all_rows
        if float(row["rho_over_rho_c"]) >= transition_ratio
    ]
    outer_rows = [
        row for row in all_rows
        if row["sampling_region"] == "outer_log_a"
    ]

    return {
        "H0": h0,
        "Omega_m": omega_m,
        "Omega_r": omega_r,
        "Omega_Lambda_dynamic": (
            1.0 - omega_m - omega_r
        ),
        "rho_c_rel": rho_c_rel,
        "rho_c_si": rho_c_si,
        "rho_crit0_si": rho_crit0_si,
        "a_bounce": a_bounce,
        "a_transition": a_transition,
        "a_outer": a_outer,
        "near_points": float(near_points),
        "outer_points": float(outer_points),
        "points_per_branch": float(
            near_points + outer_points - 1
        ),
        "total_rows": float(len(all_rows)),
        "outer_time_Gyr": times[-1],
        "bounce_H": float(bounce["H_signed_km_s_Mpc"]),
        "bounce_ratio": float(bounce["rho_over_rho_c"]),
        "bounce_correction": float(
            bounce["lqc_correction_factor"]
        ),
        "bounce_E": float(bounce["E_lqc_of_a"]),
        "bounce_margin": float(
            bounce["boundary_margin_candidate"]
        ),
        "bounce_curvature": float(
            bounce["effective_ricci_over_6H0sq"]
        ),
        "quantum_region_rows": float(len(quantum_rows)),
        "outer_region_rows": float(len(outer_rows)),
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
        "transition_ratio": transition_ratio,
    }


def write_diagnostics(
    path: Path,
    source: Path,
    output: Path,
    summary: Dict[str, float],
    lqc_planck_fraction: float,
    x_min: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    exact_pass = (
        summary["bounce_H"] == 0.0
        and summary["bounce_ratio"] == 1.0
        and summary["bounce_correction"] == 0.0
        and summary["bounce_E"] == 0.0
    )
    density_pass = summary["maximum_density_ratio"] <= 1.0
    positive_a_pass = summary["minimum_scale_factor"] > 0.0
    time_reasonable = 0.0 < summary["outer_time_Gyr"] < 100.0
    outer_resolved = summary["outer_region_rows"] >= 1000.0

    with path.open("w", encoding="utf-8") as handle:
        handle.write(
            "DATASET B — EFFECTIVE LQC BOUNCE DIAGNOSTICS V2.2\n"
        )
        handle.write("=" * 72 + "\n\n")

        handle.write(f"Script version: {SCRIPT_VERSION}\n")
        handle.write(f"Parameter source: {source}\n")
        handle.write(f"Trajectory output: {output}\n\n")

        handle.write("MODEL\n")
        handle.write(
            "H^2 = H0^2 * rho_rel * (1 - rho_rel/rho_c_rel)\n"
        )
        handle.write(
            f"rho_c = {lqc_planck_fraction:.12g} * rho_Planck\n\n"
        )

        handle.write("HYBRID SAMPLING\n")
        handle.write(
            "near bounce: logarithmic in x = sqrt(1-rho/rho_c)\n"
        )
        handle.write(
            "outer branch: logarithmic in scale factor a\n"
        )
        handle.write(
            f"transition rho/rho_c = "
            f"{summary['transition_ratio']:.12g}\n"
        )
        handle.write(
            f"x_min = {x_min:.12g}\n"
        )
        handle.write(
            f"near points = {int(summary['near_points'])}\n"
        )
        handle.write(
            f"outer points = {int(summary['outer_points'])}\n"
        )
        handle.write(
            f"points per branch after overlap removal = "
            f"{int(summary['points_per_branch'])}\n\n"
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

        handle.write("EXACT BOUNCE CHECK\n")
        handle.write(
            f"a_bounce = {summary['a_bounce']:.12g}\n"
        )
        handle.write(
            f"H_at_bounce = {summary['bounce_H']:.12g}\n"
        )
        handle.write(
            f"rho/rho_c at bounce = "
            f"{summary['bounce_ratio']:.12g}\n"
        )
        handle.write(
            f"correction at bounce = "
            f"{summary['bounce_correction']:.12g}\n"
        )
        handle.write(
            f"E_lqc at bounce = {summary['bounce_E']:.12g}\n"
        )
        handle.write(
            f"curvature proxy at bounce = "
            f"{summary['bounce_curvature']:.12g}\n"
        )
        handle.write(
            f"provisional margin at bounce = "
            f"{summary['bounce_margin']:.12g}\n\n"
        )

        handle.write("JUNCTION AND RESOLUTION\n")
        handle.write(
            f"a_transition = {summary['a_transition']:.12g}\n"
        )
        handle.write(
            f"rows with rho/rho_c >= transition = "
            f"{int(summary['quantum_region_rows'])}\n"
        )
        handle.write(
            f"outer-region rows across both branches = "
            f"{int(summary['outer_region_rows'])}\n"
        )
        handle.write(
            f"total rows = {int(summary['total_rows'])}\n\n"
        )

        handle.write("TIME CHECK\n")
        handle.write(
            f"|time| from bounce to a={summary['a_outer']:.12g} = "
            f"{summary['outer_time_Gyr']:.12g} Gyr\n"
        )
        handle.write(
            f"Planck extracted age reference = "
            f"{summary.get('planck_age_Gyr', float('nan')):.12g} Gyr\n\n"
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

        handle.write("VALIDATION STATUS\n")
        handle.write(
            f"exact bounce condition = "
            f"{'PASS' if exact_pass else 'FAIL'}\n"
        )
        handle.write(
            f"near-bounce quantum-region resolution = "
            f"{'PASS' if summary['quantum_region_rows'] >= 100 else 'REVIEW'}\n"
        )
        handle.write(
            f"outer cosmological-region resolution = "
            f"{'PASS' if outer_resolved else 'REVIEW'}\n"
        )
        handle.write(
            f"density bound rho/rho_c <= 1 = "
            f"{'PASS' if density_pass else 'FAIL'}\n"
        )
        handle.write(
            f"positive minimum scale factor = "
            f"{'PASS' if positive_a_pass else 'FAIL'}\n"
        )
        handle.write(
            f"finite reasonable branch time = "
            f"{'PASS' if time_reasonable else 'FAIL'}\n\n"
        )

        handle.write("METHOD NOTES\n")
        handle.write(
            "- The exact bounce row is identified only by x=0 and forced "
            "to H=0.\n"
        )
        handle.write(
            "- The hybrid grid resolves both the quantum region and the "
            "late classical branch.\n"
        )
        handle.write(
            "- Dataset B is a model-generated effective LQC trajectory.\n"
        )
        handle.write(
            "- boundary_margin_candidate remains provisional.\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate Dataset B effective LQC bounce trajectory "
            "with hybrid near-bounce and logarithmic-a sampling."
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
        "--lqc-planck-fraction",
        type=float,
        default=0.41,
    )
    parser.add_argument(
        "--rho-c-relative",
        type=float,
        default=None,
    )
    parser.add_argument(
        "--a-outer",
        type=float,
        default=1.0,
    )
    parser.add_argument(
        "--near-points",
        type=int,
        default=801,
        help=(
            "Near-bounce points including exact bounce and transition."
        ),
    )
    parser.add_argument(
        "--outer-points",
        type=int,
        default=1201,
        help=(
            "Log-a points including transition and outer endpoint."
        ),
    )
    parser.add_argument(
        "--transition-ratio",
        type=float,
        default=0.01,
        help="Hybrid junction value of rho/rho_c.",
    )
    parser.add_argument(
        "--x-min",
        type=float,
        default=1.0e-7,
        help="Smallest nonzero x=sqrt(1-rho/rho_c).",
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

    rho_c_rel_default, rho_c_si_default, rho_crit0_si = (
        critical_density_values(
            parameters["H0"],
            args.lqc_planck_fraction,
        )
    )

    if args.rho_c_relative is None:
        rho_c_rel = rho_c_rel_default
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
        near_points=args.near_points,
        outer_points=args.outer_points,
        transition_ratio=args.transition_ratio,
        x_min=args.x_min,
    )
    summary["planck_age_Gyr"] = parameters["age"]

    write_diagnostics(
        diagnostics,
        source,
        output,
        summary,
        args.lqc_planck_fraction,
        args.x_min,
    )

    print(f"Script version: {SCRIPT_VERSION}")
    print(f"Created trajectory: {output}")
    print(f"Created diagnostics: {diagnostics}")
    print(f"Bounce scale factor: {summary['a_bounce']:.12g}")
    print(f"Transition scale factor: {summary['a_transition']:.12g}")
    print(f"H at bounce: {summary['bounce_H']:.6e}")
    print(
        f"Rows with rho/rho_c >= {summary['transition_ratio']:.6g}: "
        f"{int(summary['quantum_region_rows'])}"
    )
    print(
        f"Outer branch time: {summary['outer_time_Gyr']:.12g} Gyr"
    )
    print(
        f"Maximum rho/rho_c: "
        f"{summary['maximum_density_ratio']:.12g}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
