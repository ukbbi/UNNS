from __future__ import annotations

import argparse
from pathlib import Path

from jhtdb_adapter.pipeline import run_adapter


def parse_factors(text):
    if not text:
        return None
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def main():
    ap = argparse.ArgumentParser(
        description="JHTDB physical-to-STRUC-ROUTE-I adapter"
    )
    ap.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parent / "config" / "pilot_a.json")
    )
    ap.add_argument("--project-root", default=None)
    ap.add_argument("--skip-hash", action="store_true")
    ap.add_argument(
        "--frame-limit", type=int, default=None,
        help="Process only the first N frames (validation/debug only)."
    )
    ap.add_argument(
        "--factors", default=None,
        help="Override scale factors, e.g. 1,2,4 (validation/debug only)."
    )
    args = ap.parse_args()

    run_adapter(
        Path(args.config),
        project_root=Path(args.project_root) if args.project_root else None,
        skip_hash=args.skip_hash,
        frame_limit=args.frame_limit,
        factors_override=parse_factors(args.factors),
        progress=print,
    )


if __name__ == "__main__":
    main()
