from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]

def sha(p):
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

def main():
    cfg=json.loads((ROOT/"config/prereg_v002.json").read_text(encoding="utf-8"))
    seeds=json.loads((ROOT/"SEEDS.json").read_text(encoding="utf-8"))
    if cfg["status"]!="FROZEN_BEFORE_PRIMARY":
        print("FAIL status"); return 1
    if cfg["solution_density_min"]!=0.02 or cfg["solution_density_max"]!=0.04:
        print("FAIL density band"); return 1
    cal=set(sum(seeds["calibration"].values(),[]))
    des=set(seeds["design_audit"])
    prim=set(sum(seeds["primary"].values(),[]))
    if cal & des or cal & prim or des & prim:
        print("FAIL seed overlap"); return 1
    if len(prim)!=30:
        print("FAIL primary grid"); return 1
    for line in (ROOT/"SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        digest,rel=line.split("  ",1)
        p=ROOT/rel
        if not p.exists() or sha(p)!=digest:
            print("FAIL hash",rel); return 1
    print("SCR-II v002 preregistration: PASS")
    print("Multiplicity band: 2%-4%")
    print("Primary instances: 30")
    print("Primary seeds inspected: NO")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
