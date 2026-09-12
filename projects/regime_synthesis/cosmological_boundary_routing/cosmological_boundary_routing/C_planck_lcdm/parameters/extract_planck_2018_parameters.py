#!/usr/bin/env python3
"""
Extract a compact canonical Planck 2018 parameter record for:

    base_plikHM_TTTEEE_lowl_lowE

Inputs expected in the same directory as this script, unless overridden:
    base_plikHM_TTTEEE_lowl_lowE.minimum
    base_plikHM_TTTEEE_lowl_lowE.margestats
    base_plikHM_TTTEEE_lowl_lowE.paramnames

Outputs:
    planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.csv
    planck_2018_base_plikHM_TTTEEE_lowl_lowE_parameters.txt

The deterministic canonical trajectory should use the best-fit values from
the .minimum file. Posterior means and 68% intervals are retained for
documentation and later uncertainty analysis.

No third-party packages are required.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


MODEL_TAG = "base_plikHM_TTTEEE_lowl_lowE"
PLANCK_RELEASE = "PR3 2018"
T_CMB_K = 2.7255
DEFAULT_N_EFF = 3.046


@dataclass
class Marginal:
    mean: float
    sddev: float
    lower68: float
    upper68: float
    limit68: str
    label: str = ""


def normalized_name(name: str) -> str:
    """Remove GetDist's derived-parameter marker."""
    return name.rstrip("*")


def parse_paramnames(path: Path) -> Dict[str, str]:
    labels: Dict[str, str] = {}
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if not parts:
                continue
            name = normalized_name(parts[0])
            label = parts[1].strip() if len(parts) > 1 else ""
            labels[name] = label
    return labels


def parse_minimum(path: Path) -> Dict[str, float]:
    """
    Parse rows of the form:
        72  0.6732178E+02   H0   H_0
    """
    values: Dict[str, float] = {}
    row_re = re.compile(
        r"^\s*\d+\s+"
        r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?)\s+"
        r"([A-Za-z0-9_]+)\b"
    )
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            match = row_re.match(raw)
            if match:
                value = float(match.group(1))
                name = normalized_name(match.group(2))
                values[name] = value
    if not values:
        raise ValueError(f"No parameter rows were parsed from {path}")
    return values


def parse_margestats(path: Path) -> Dict[str, Marginal]:
    """
    Parse GetDist margestats rows. The first eight tokens are:
      name mean sddev lower1 upper1 limit1 lower2 upper2 ...
    """
    result: Dict[str, Marginal] = {}
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("Marginalized") or line.startswith("parameter"):
                continue
            parts = line.split()
            if len(parts) < 6:
                continue
            try:
                name = normalized_name(parts[0])
                mean = float(parts[1])
                sddev = float(parts[2])
                lower68 = float(parts[3])
                upper68 = float(parts[4])
                limit68 = parts[5]
            except ValueError:
                continue
            label = " ".join(parts[15:]) if len(parts) > 15 else ""
            result[name] = Marginal(
                mean=mean,
                sddev=sddev,
                lower68=lower68,
                upper68=upper68,
                limit68=limit68,
                label=label,
            )
    if not result:
        raise ValueError(f"No marginalized rows were parsed from {path}")
    return result


def require(values: Dict[str, float], name: str, source: str) -> float:
    if name not in values:
        raise KeyError(f"Required parameter '{name}' not found in {source}")
    return values[name]


def get_marginal(marginals: Dict[str, Marginal], name: str) -> Optional[Marginal]:
    return marginals.get(name)


def radiation_density_parameter(h0: float, n_eff: float) -> tuple[float, float]:
    """
    Return (omega_r, Omega_r), where omega_r = Omega_r h^2.

    Uses:
      omega_gamma = 2.469e-5 * (T_CMB / 2.7255 K)^4
      omega_r = omega_gamma * (1 + 0.22710731766 * N_eff)

    This is the standard photons + relativistic-neutrino approximation.
    """
    h = h0 / 100.0
    omega_gamma = 2.469e-5 * (T_CMB_K / 2.7255) ** 4
    omega_r = omega_gamma * (1.0 + 0.22710731766 * n_eff)
    omega_R = omega_r / (h * h)
    return omega_r, omega_R


def format_number(value: Optional[float]) -> str:
    if value is None:
        return ""
    return f"{value:.12g}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract canonical Planck 2018 base_plikHM_TTTEEE_lowl_lowE parameters."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory containing the three Planck input files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory. Defaults to --input-dir.",
    )
    args = parser.parse_args()

    input_dir = args.input_dir.resolve()
    output_dir = (args.output_dir or input_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    minimum_path = input_dir / f"{MODEL_TAG}.minimum"
    margestats_path = input_dir / f"{MODEL_TAG}.margestats"
    paramnames_path = input_dir / f"{MODEL_TAG}.paramnames"

    for path in (minimum_path, margestats_path, paramnames_path):
        if not path.is_file():
            raise FileNotFoundError(f"Required input file not found: {path}")

    labels = parse_paramnames(paramnames_path)
    best = parse_minimum(minimum_path)
    marg = parse_margestats(margestats_path)

    h0 = require(best, "H0", minimum_path.name)
    n_eff = best.get("nnu", DEFAULT_N_EFF)
    omega_r, Omega_r = radiation_density_parameter(h0, n_eff)

    logA_best = require(best, "logA", minimum_path.name)
    As_best = math.exp(logA_best) * 1e-10

    logA_marg = get_marginal(marg, "logA")
    As_mean = math.exp(logA_marg.mean) * 1e-10 if logA_marg else None
    As_lower68 = math.exp(logA_marg.lower68) * 1e-10 if logA_marg else None
    As_upper68 = math.exp(logA_marg.upper68) * 1e-10 if logA_marg else None

    # Canonical rows, in the project-requested order.
    specifications = [
        ("H0", "H0", "km s^-1 Mpc^-1", "direct"),
        ("omegabh2", "omegabh2", "dimensionless", "direct"),
        ("omegach2", "omegach2", "dimensionless", "direct"),
        ("Omega_m", "omegam", "dimensionless", "direct"),
        ("Omega_Lambda", "omegal", "dimensionless", "direct"),
        ("n_s", "ns", "dimensionless", "direct"),
        ("ln_1e10_A_s", "logA", "dimensionless", "direct"),
        ("tau", "tau", "dimensionless", "direct"),
        ("sigma8", "sigma8", "dimensionless", "direct"),
        ("age", "age", "Gyr", "direct"),
    ]

    rows = []
    for output_name, source_name, unit, status in specifications:
        m = get_marginal(marg, source_name)
        rows.append(
            {
                "parameter": output_name,
                "source_parameter": source_name,
                "latex_label": labels.get(source_name, m.label if m else ""),
                "best_fit": best.get(source_name),
                "posterior_mean": m.mean if m else None,
                "sddev": m.sddev if m else None,
                "lower_68": m.lower68 if m else None,
                "upper_68": m.upper68 if m else None,
                "limit_type_68": m.limit68 if m else "",
                "unit": unit,
                "status": status,
                "derivation": "",
                "canonical_use": "best_fit",
            }
        )

    # Derived A_s.
    rows.append(
        {
            "parameter": "A_s",
            "source_parameter": "logA",
            "latex_label": "A_s",
            "best_fit": As_best,
            "posterior_mean": As_mean,
            "sddev": None,
            "lower_68": As_lower68,
            "upper_68": As_upper68,
            "limit_type_68": logA_marg.limit68 if logA_marg else "",
            "unit": "dimensionless",
            "status": "derived",
            "derivation": "A_s = exp(logA) * 1e-10",
            "canonical_use": "best_fit",
        }
    )

    # Derived radiation density.
    rows.append(
        {
            "parameter": "omega_r",
            "source_parameter": "H0,nnu",
            "latex_label": r"\Omega_r h^2",
            "best_fit": omega_r,
            "posterior_mean": None,
            "sddev": None,
            "lower_68": None,
            "upper_68": None,
            "limit_type_68": "",
            "unit": "dimensionless",
            "status": "derived",
            "derivation": (
                "omega_gamma=2.469e-5*(T_CMB/2.7255)^4; "
                "omega_r=omega_gamma*(1+0.22710731766*N_eff)"
            ),
            "canonical_use": "best_fit-derived",
        }
    )
    rows.append(
        {
            "parameter": "Omega_r",
            "source_parameter": "H0,nnu",
            "latex_label": r"\Omega_r",
            "best_fit": Omega_r,
            "posterior_mean": None,
            "sddev": None,
            "lower_68": None,
            "upper_68": None,
            "limit_type_68": "",
            "unit": "dimensionless",
            "status": "derived",
            "derivation": "Omega_r = omega_r / h^2, h = H0 / 100",
            "canonical_use": "best_fit-derived",
        }
    )

    csv_path = output_dir / f"planck_2018_{MODEL_TAG}_parameters.csv"
    txt_path = output_dir / f"planck_2018_{MODEL_TAG}_parameters.txt"

    fieldnames = [
        "parameter",
        "source_parameter",
        "latex_label",
        "best_fit",
        "posterior_mean",
        "sddev",
        "lower_68",
        "upper_68",
        "limit_type_68",
        "unit",
        "status",
        "derivation",
        "canonical_use",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            serial = row.copy()
            for key in ("best_fit", "posterior_mean", "sddev", "lower_68", "upper_68"):
                serial[key] = format_number(serial[key])
            writer.writerow(serial)

    with txt_path.open("w", encoding="utf-8") as handle:
        handle.write("PLANCK 2018 CANONICAL PARAMETER RECORD\n")
        handle.write("Cosmological Boundary Routing — Dataset C\n")
        handle.write("=" * 72 + "\n\n")
        handle.write(f"Planck release: {PLANCK_RELEASE}\n")
        handle.write(f"Model/likelihood tag: {MODEL_TAG}\n")
        handle.write("Canonical trajectory values: best-fit values from .minimum\n")
        handle.write("Uncertainty record: posterior means and 68% limits from .margestats\n")
        handle.write(f"T_CMB used for Omega_r derivation: {T_CMB_K} K\n")
        handle.write(f"N_eff used for Omega_r derivation: {n_eff}\n\n")

        for row in rows:
            handle.write(f"{row['parameter']}\n")
            handle.write(f"  source parameter : {row['source_parameter']}\n")
            handle.write(f"  best fit        : {format_number(row['best_fit'])}\n")
            handle.write(f"  posterior mean  : {format_number(row['posterior_mean'])}\n")
            handle.write(f"  sddev           : {format_number(row['sddev'])}\n")
            handle.write(
                f"  68% interval    : "
                f"[{format_number(row['lower_68'])}, {format_number(row['upper_68'])}]"
                f"{' (' + row['limit_type_68'] + ')' if row['limit_type_68'] else ''}\n"
            )
            handle.write(f"  unit            : {row['unit']}\n")
            handle.write(f"  status          : {row['status']}\n")
            if row["derivation"]:
                handle.write(f"  derivation      : {row['derivation']}\n")
            handle.write("\n")

        handle.write("NOTES\n")
        handle.write("- Direct parameters are read from official Planck GetDist outputs.\n")
        handle.write("- A_s is derived from logA = ln(10^10 A_s).\n")
        handle.write(
            "- Omega_r uses the photons + relativistic-neutrino approximation and "
            "is not a directly tabulated Planck chain parameter.\n"
        )
        handle.write(
            "- The deterministic Dataset C trajectory should read the best_fit "
            "column only.\n"
        )
        handle.write(
            "- Posterior means and intervals are retained for later robustness "
            "and Monte Carlo analysis.\n"
        )

    print(f"Created: {csv_path}")
    print(f"Created: {txt_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
