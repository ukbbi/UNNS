from __future__ import annotations
import argparse
from pathlib import Path
from struc_route.engine import analyze_project

def main():
    ap = argparse.ArgumentParser(description="STRUC-ROUTE-I command line runner")
    ap.add_argument("project", help="Input project folder")
    ap.add_argument("--outputs", default="outputs", help="Output root")
    args = ap.parse_args()

    def progress(frac, phase, msg):
        print(f"[{frac*100:6.2f}%] {phase:16s} {msg}")

    result, run_dir = analyze_project(args.project, args.outputs, progress)
    print()
    print("Verdict:", result["verdict"]["class"])
    print("Run:", run_dir)

if __name__ == "__main__":
    main()
