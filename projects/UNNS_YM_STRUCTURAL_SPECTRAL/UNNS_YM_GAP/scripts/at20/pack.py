"""Refresh the relocated AT20 manifest and create output/at20_project.zip."""
from pathlib import Path
import hashlib, json, zipfile

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "at20"
TARGET = ROOT / "output" / "at20_project.zip"

INCLUDE = [
    ROOT / "data" / "raw" / "at20",
    ROOT / "data" / "derived" / "at20",
    ROOT / "docs" / "at20",
    ROOT / "scripts" / "at20",
]
EXTRA = [ROOT / "data" / "raw" / "at20.zip"]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def corpus_files():
    out = []
    for folder in INCLUDE:
        out.extend(p for p in folder.rglob("*") if p.is_file())
    out.extend(p for p in EXTRA if p.is_file())
    return sorted(set(out))

def main():
    files = [p for p in corpus_files()
             if p != DOCS / "manifest.json"
             and "__pycache__" not in p.parts
             and p.suffix != ".pyc"]
    entries = [{
        "path": p.relative_to(ROOT).as_posix(),
        "bytes": p.stat().st_size,
        "sha256": sha(p)
    } for p in files]
    manifest = {
        "package": "UNNS_YM_GAP/at20",
        "version": "2.0-project-layout",
        "algorithm": "SHA-256",
        "paths_relative_to": "UNNS_YM_GAP project root",
        "excluded": ["docs/at20/manifest.json itself", "Python bytecode/cache"],
        "files": entries
    }
    (DOCS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(TARGET, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(files + [DOCS / "manifest.json"]):
            z.write(p, p.relative_to(ROOT).as_posix())
    print(f"Created {TARGET} with {len(entries)+1} files.")

if __name__ == "__main__":
    main()
