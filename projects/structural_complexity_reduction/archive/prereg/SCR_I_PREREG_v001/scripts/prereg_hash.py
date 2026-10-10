from __future__ import annotations
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "SHA256SUMS.txt"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    paths = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if p == OUT or p.name.endswith(".pyc") or "__pycache__" in p.parts:
            continue
        paths.append(p)
    lines = [f"{digest(p)}  {p.relative_to(ROOT).as_posix()}" for p in sorted(paths)]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} hashes to {OUT.name}")


if __name__ == "__main__":
    main()
