"""write MANIFEST.json (sha256 of every v002 file + the frozen v001 manifest hash)."""
import hashlib
import json
import os
import platform
import _path
import _v1path

ROOT = _path.ROOT
skip_dirs = {"__pycache__"}
files = {}
for d, ds, fs in os.walk(ROOT):
    ds[:] = [x for x in ds if x not in skip_dirs]
    for fn in sorted(fs):
        rel = os.path.relpath(os.path.join(d, fn), ROOT).replace(os.sep, "/")
        if rel == "MANIFEST.json" or rel.endswith(".pyc") or "quick" in fn:
            continue
        with open(os.path.join(d, fn), "rb") as f:
            files[rel] = hashlib.sha256(f.read()).hexdigest()
v1 = os.path.join(_v1path.V001, "MANIFEST.json")
with open(v1, "rb") as f:
    v1hash = hashlib.sha256(f.read()).hexdigest()
man = {"release": "GIG_I_v002", "date": "2026-11-05", "python": platform.python_version(),
       "parent": {"release": "GIG_I_v001", "MANIFEST.json_sha256": v1hash, "status": "FROZEN, read-only, imported unchanged"},
       "dependencies": "Python standard library only (>=3.10: int.bit_count)", "files": files,
       "frozen_references": "SELECT-II, GEO-HD-1 and GEO-HD-1D v004 are read-only references; no remote repository was modified."}
with open(os.path.join(ROOT, "MANIFEST.json"), "w") as f:
    json.dump(man, f, indent=1, sort_keys=True)
print("manifest:", len(files), "files")
