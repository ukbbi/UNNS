from pathlib import Path
import hashlib
root=Path(__file__).resolve().parents[1]
for p in sorted(x for x in root.rglob('*') if x.is_file() and x.name not in {'SHA256SUMS.txt'} and '__pycache__' not in x.parts):
    print(hashlib.sha256(p.read_bytes()).hexdigest(), p.relative_to(root).as_posix())
