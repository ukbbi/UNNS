from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
for p in sorted(x for x in ROOT.rglob('*') if x.is_file() and x.name!='SHA256SUMS.txt'):
    print(hashlib.sha256(p.read_bytes()).hexdigest(),' ',p.relative_to(ROOT).as_posix())
