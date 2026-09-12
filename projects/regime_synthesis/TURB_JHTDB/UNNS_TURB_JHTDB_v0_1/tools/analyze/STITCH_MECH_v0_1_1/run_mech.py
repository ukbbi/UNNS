from pathlib import Path
import argparse
from stitch_mech.pipeline import run

def main():
    ap=argparse.ArgumentParser(description="JHTDB scale-time stitching mechanism test")
    ap.add_argument("--config",default=str(Path(__file__).resolve().parent/"CONFIG.json"))
    ap.add_argument("--project-root",default=None)
    args=ap.parse_args()
    run(
        Path(args.config),
        project_root=Path(args.project_root) if args.project_root else None,
        progress=print,
    )

if __name__=="__main__":
    main()
