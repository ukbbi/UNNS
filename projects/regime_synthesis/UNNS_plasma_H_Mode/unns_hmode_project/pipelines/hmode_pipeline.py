"""
UNNS-H Mode pipeline scaffold.

Usage:
    python -m pipelines.hmode_pipeline input.csv output.csv

The input must already be canonical or close to canonical.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd

# Local imports assume this script is run from project root.
from components.edge_margin import compute_edge_margin
from components.pedestal_load import compute_pedestal_load
from components.turbulence_fragmentation import compute_turbulence_fragmentation
from components.elm_risk import compute_boundary_overload


def run(input_csv: str | Path, output_csv: str | Path) -> None:
    df = pd.read_csv(input_csv)

    df["pedestal_load"] = compute_pedestal_load(df)
    df["turbulence_fragmentation"] = compute_turbulence_fragmentation(df)
    df["m_edge"] = compute_edge_margin(df)
    df["boundary_overload_index"] = compute_boundary_overload(df)

    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python -m pipelines.hmode_pipeline input.csv output.csv")
    run(sys.argv[1], sys.argv[2])
