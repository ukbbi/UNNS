from __future__ import annotations
import argparse
from pathlib import Path
from struc_route.postrun import analyze_run_zip

def main():
    ap=argparse.ArgumentParser(
        description="STRUC-ROUTE-I post-run high-D_square physics analysis"
    )
    ap.add_argument("run_zip")
    ap.add_argument("--out", default=None)
    ap.add_argument("--viscosity", type=float, default=None)
    ap.add_argument("--permutations", type=int, default=2000)
    args=ap.parse_args()

    run=Path(args.run_zip).resolve()
    out=Path(args.out).resolve() if args.out else run.with_name(run.stem+"_STITCH_PHYSICS")
    report=analyze_run_zip(
        run,out,viscosity=args.viscosity,permutations=args.permutations
    )
    print("Complete:", out)
    print(json.dumps(report["correlations"], indent=2))
if __name__=="__main__":
    import json
    main()
