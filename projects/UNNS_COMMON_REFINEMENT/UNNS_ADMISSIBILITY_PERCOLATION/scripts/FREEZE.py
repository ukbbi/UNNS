#!/usr/bin/env python3
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"outputs"/"records"/"FREEZE_RECORD.json"

TRACK=[
    "PROTOCOL.md",
    "adapters/ADAPTER_SPEC.md",
    "corpus/CORPUS_INDEX.csv",
    "corpus/CORPUS_AUDIT.json",
    "corpus/LADDER_INDEX.csv",
    "inputs/struc_i/ALL_SYSTEM_SPECTRA.csv",
    "chambers/STRUC-I/chamber_struc_i_v1_0_4.html",
    "chambers/STRUC-PERC-I/struc_perc_i_v2_5_0.html",
]

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()

def main():
    files={}
    for rel in TRACK:
        p=ROOT/rel
        if not p.exists():
            raise SystemExit(f"Missing tracked file: {rel}")
        files[rel]=sha(p)
    # Freeze individual PERC inputs too.
    for p in sorted((ROOT/"inputs"/"struc_perc_i").glob("*.csv")):
        rel=p.relative_to(ROOT).as_posix()
        files[rel]=sha(p)

    rec={
        "experiment":"UNNS_TRACEABILITY_PHENOTYPE",
        "freeze_version":"0.1",
        "status":"FROZEN_BEFORE_FIRST_CHAMBER_RUN",
        "primary_object":"SYSTEM_SPECTRUM",
        "N":128,
        "n_cases":30,
        "files":files
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(rec,indent=2))

if __name__=="__main__":
    main()
