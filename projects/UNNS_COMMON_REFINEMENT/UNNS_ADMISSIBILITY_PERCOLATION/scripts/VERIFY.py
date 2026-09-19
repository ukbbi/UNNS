#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/"outputs"/"records"/"FREEZE_RECORD.json"

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()

def main():
    rec=json.loads(REC.read_text(encoding="utf-8"))
    bad=[]
    for rel,expected in rec["files"].items():
        p=ROOT/rel
        got=sha(p) if p.exists() else None
        if got!=expected:
            bad.append({"file":rel,"expected":expected,"got":got})
    result={"status":"PASS" if not bad else "FAIL","checked":len(rec["files"]),"mismatches":bad}
    print(json.dumps(result,indent=2))
    sys.exit(0 if not bad else 1)

if __name__=="__main__":
    main()
