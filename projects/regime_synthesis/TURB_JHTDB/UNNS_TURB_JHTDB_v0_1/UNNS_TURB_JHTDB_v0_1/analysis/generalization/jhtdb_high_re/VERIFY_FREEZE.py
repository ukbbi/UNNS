#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
here=Path(__file__).resolve().parent
freeze=here/'FREEZE_SHA256.txt'
fail=False
for line in freeze.read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    digest, rel=line.split('  ',1)
    p=here/rel
    if not p.exists():
        print('[MISSING]',rel); fail=True; continue
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    if h!=digest:
        print('[FAIL]',rel); fail=True
    else:
        print('[PASS]',rel)
if fail: raise SystemExit(1)
print('[PASS] High-Re preregistration freeze verified.')
