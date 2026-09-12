#!/usr/bin/env python3
"""
Optional SOURCE-LEVEL verifier for C003_FINAL_v001.

Normal reproduction does NOT need the old Phase-I workbook because the actual project
already contains the locked canonical ingest CSVs at:

  <root>/06_VALIDATION/C003_FINAL_v001/INGEST/

Use this script only if you also have the original historical `rawdata.xls` (or an
unmodified XLSX conversion) and want to prove that it regenerates those ingest CSVs.

Examples:
  python build_C003_ingest.py --source "D:\path\rawdata.xls"
  python build_C003_ingest.py --source "D:\path\rawdata.xlsx"

The output is written beside the canonical ingest, under REPRO_INGEST/.
"""
from pathlib import Path
import argparse, hashlib
import pandas as pd

def find_project_root():
    """
    Script lives at:
      <root>/06_VALIDATION/C003_FINAL_v001/<script>.py
    Therefore parents[2] is the actual UNNS_MULTI_CLOCK_RECURRENCE root.
    """
    here = Path(__file__).resolve()
    root = here.parents[2]
    required = [
        root / "05_METHODS" / "rep_study_v002.py",
        root / "05_METHODS" / "grammar_dev_v001.py",
        root / "05_METHODS" / "mc_grammar_v001.py",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise SystemExit(
            "Could not resolve UNNS_MULTI_CLOCK_RECURRENCE root from script location.\n"
            "Missing:\n  " + "\n  ".join(missing)
        )
    return root


ROOT = find_project_root()
VAL = ROOT / "06_VALIDATION" / "C003_FINAL_v001"
CANON = VAL / "INGEST"
OUT = VAL / "REPRO_INGEST"
OUT.mkdir(parents=True, exist_ok=True)

R = 1.618

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):
            h.update(chunk)
    return h.hexdigest()

ap=argparse.ArgumentParser()
ap.add_argument("--source", required=True,
                help="Historical rawdata.xls or unmodified XLSX conversion")
args=ap.parse_args()

src=Path(args.source).expanduser().resolve()
if not src.exists():
    raise SystemExit(f"Missing source workbook: {src}")

df=pd.read_excel(src, sheet_name="Fig. 1", header=None)

specs={
    "TC_P01_C003": (7,8,9),       # Fig.1d
    "TC_P01_C003_CTRL": (0,1,2),  # Fig.1b
}

for rid,(c0,c1,c2) in specs.items():
    q=df.iloc[2:,[c0,c1,c2]].copy()
    q.columns=["time_tau1","polarization","error"]
    q=q.apply(pd.to_numeric,errors="coerce")
    q=q.dropna(subset=["time_tau1","polarization"])
    q=q.sort_values("time_tau1").reset_index(drop=True)
    q["source_cycles_tau2"]=q["time_tau1"]/R

    p=OUT/f"{rid}.csv"
    q[["time_tau1","source_cycles_tau2","polarization","error"]].to_csv(p,index=False)

    canon=CANON/f"{rid}.csv"
    got=sha256(p)
    exp=sha256(canon)
    print(rid)
    print("  reproduced:",got)
    print("  canonical: ",exp)
    print("  MATCH:",got==exp)
    if got != exp:
        raise SystemExit(f"Canonical ingest mismatch for {rid}")

print("PASS: historical source workbook reproduces both canonical C003 ingest CSVs.")
