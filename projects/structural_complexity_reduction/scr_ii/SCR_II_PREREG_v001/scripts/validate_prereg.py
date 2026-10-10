from pathlib import Path
import json, hashlib, sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "PREREG.md","BENCHMARK.md","GRAMMAR_FREEZE.md","SOLVER.md","NULLS.md",
    "METRICS.md","SCALING.md","DECISION_RULES.md","SEEDS.json",
    "config/prereg_v001.json","schema/result.schema.json","MANIFEST.md","SHA256SUMS.txt"
]

def sha(p):
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

def main():
    missing=[x for x in REQUIRED if not (ROOT/x).exists()]
    if missing:
        print("FAIL missing:", ", ".join(missing)); return 1

    cfg=json.loads((ROOT/"config/prereg_v001.json").read_text(encoding="utf-8"))
    seeds=json.loads((ROOT/"SEEDS.json").read_text(encoding="utf-8"))

    if cfg["status"]!="FROZEN_BEFORE_PRIMARY":
        print("FAIL status"); return 1
    if cfg["primary_depths"] != [14,16,18]:
        print("FAIL primary depths"); return 1
    if cfg["gate_order"] != ["G1","G2","G3","G4"]:
        print("FAIL gate order"); return 1

    cal=set(sum(seeds["calibration"].values(), []))
    design=set(seeds["design_audit"])
    prim=set(sum(seeds["primary"].values(), []))
    if cal & design or cal & prim or design & prim:
        print("FAIL seed overlap"); return 1
    if len(prim)!=30:
        print("FAIL primary grid"); return 1

    sums={}
    for line in (ROOT/"SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        digest, rel = line.split("  ",1)
        sums[rel]=digest
    # SHA256SUMS and MANIFEST intentionally not self-hashed.
    for rel,digest in sums.items():
        p=ROOT/rel
        if not p.exists() or sha(p)!=digest:
            print("FAIL hash:",rel); return 1

    print("SCR-II v001 preregistration: PASS")
    print("Primary depths:", cfg["primary_depths"])
    print("Primary instances:", len(prim))
    print("Primary seeds are disjoint from calibration/design seeds: PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
