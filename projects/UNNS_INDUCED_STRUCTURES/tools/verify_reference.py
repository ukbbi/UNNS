#!/usr/bin/env python3
"""Verify byte-level integrity of this curated reference collection (stdlib only).

From the collection root: python3 tools/verify_reference.py
This verifies the curated checksums; it does NOT rerun all scientific experiments.
"""
import hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
DIGESTS=ROOT/'CHECKSUMS.sha256'
lines=[s for s in DIGESTS.read_text(encoding='utf-8').splitlines() if s and not s.startswith('#')]
bad=[]
for row in lines:
    expected,path=row.split('  ',1)
    f=ROOT/path
    if not f.is_file(): bad.append(('MISSING',path)); continue
    found=hashlib.sha256(f.read_bytes()).hexdigest()
    if found!=expected: bad.append(('MISMATCH',path))
tracked={row.split('  ',1)[1] for row in lines}
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
        if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.pyo'}}-{'CHECKSUMS.sha256'}
extra=sorted(actual-tracked)
if extra: bad.extend(('UNLISTED',p) for p in extra)
for kind,path in bad[:40]: print(kind,path)
print(f'CURATED REFERENCE: {"PASS" if not bad else "FAIL"}; entries={len(lines)}, errors={len(bad)}')
raise SystemExit(1 if bad else 0)
