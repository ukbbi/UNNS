#!/usr/bin/env python3
"""Read-only integrity checker for the 14 frozen UNNS-SCALE releases (stdlib)."""
import hashlib
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
RELEASES = ROOT / "releases"
MANIFESTS = [RELEASES / "SHA256SUMS.txt"] + [
    RELEASES / f"UNNS-SCALE-I_v{v:03d}" / f"SHA256SUMS_v{v:03d}.txt"
    for v in range(2, 15)
]
LINE = re.compile(r"^([a-f0-9]{64})\s+\*?(.+)$")

def main():
    checked = 0
    failures = []
    for mf in MANIFESTS:
        if not mf.is_file():
            failures.append(f"missing manifest: {mf}")
            continue
        base = RELEASES if mf.name == "SHA256SUMS.txt" else mf.parent
        count = 0
        for idx, raw in enumerate(mf.read_text(encoding="utf-8-sig").splitlines(), 1):
            if not raw.strip():
                continue
            m = LINE.match(raw)
            if not m:
                failures.append(f"invalid entry {mf.name}:{idx}")
                continue
            expected, rel = m.groups()
            candidate = (base / rel).resolve()
            if not candidate.is_relative_to(RELEASES.resolve()):
                failures.append(f"unsafe manifest entry: {mf.name}:{idx}: {rel}")
                continue
            if not candidate.is_file():
                failures.append(f"missing: {candidate.relative_to(ROOT)}")
                continue
            actual = hashlib.sha256(candidate.read_bytes()).hexdigest()
            if actual != expected:
                failures.append(f"mismatch: {candidate.relative_to(ROOT)}")
            count += 1
        checked += count
        print(f"{mf.relative_to(ROOT)}: {count} files checked")
    print(f"TOTAL: {len(MANIFESTS)} manifests; {checked} checks; " + (f"FAIL ({len(failures)} errors)" if failures else "PASS"))
    if failures:
        for f in failures[:50]: print('  '+f)
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
