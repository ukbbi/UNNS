"""write MANIFEST.json (sha256 of every v003 file + hashes of the frozen v001/v002 manifests)."""
import hashlib
import json
import os
import platform
import _path
import _v2path

ROOT = _path.ROOT
files = {}
for d, ds, fs in os.walk(ROOT):
    ds[:] = [x for x in ds if x != "__pycache__"]
    for fn in sorted(fs):
        rel = os.path.relpath(os.path.join(d, fn), ROOT).replace(os.sep, "/")
        if rel == "MANIFEST.json" or rel.endswith(".pyc") or "quick" in fn:
            continue
        with open(os.path.join(d, fn), "rb") as f:
            files[rel] = hashlib.sha256(f.read()).hexdigest()


def h(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


man = {"release": "GIG_I_v003", "date": "2026-11-05", "python": platform.python_version(),
       "parents": {"GIG_I_v001": {"MANIFEST.json_sha256": h(os.path.join(_v2path.V001, "MANIFEST.json")), "status": "FROZEN, read-only, imported unchanged"},
                   "GIG_I_v002": {"MANIFEST.json_sha256": h(os.path.join(_v2path.V002, "MANIFEST.json")), "status": "FROZEN, read-only, imported unchanged"}},
       "dependencies": "Python standard library only (>=3.10: int.bit_count)", "files": files,
       "frozen_references": "SELECT-II, GEO-HD-1 and GEO-HD-1D v004 are read-only references; no remote repository was modified.",
       "arithmetic": "exact integer/Fraction arithmetic for every divisibility, rank and homology certificate; floats only in presentation (entropies)."}
with open(os.path.join(ROOT, "MANIFEST.json"), "w") as f:
    json.dump(man, f, indent=1, sort_keys=True)
print("manifest:", len(files), "files")
