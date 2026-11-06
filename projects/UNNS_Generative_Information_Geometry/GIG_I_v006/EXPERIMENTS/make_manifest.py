import hashlib, json, os, platform
import _path
ROOT = _path.ROOT
def h(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
files = {}
for d, ds, fs in os.walk(ROOT):
    ds[:] = [x for x in ds if x != "__pycache__"]
    for fn in sorted(fs):
        rel = os.path.relpath(os.path.join(d, fn), ROOT).replace(os.sep, "/")
        if rel != "MANIFEST.json" and not rel.endswith(".pyc"):
            files[rel] = h(os.path.join(d, fn))
parents = {}
for n, p in [("GIG_I_v00%d" % i, getattr(_path._vpath, "V00%d" % i)) for i in range(1, 6)] + [("GIG_I_v005_S2", _path._vpath.V005S2), ("GIG_I_v005_S3", _path._vpath.V005S3)]:
    mp = os.path.join(p, "MANIFEST.json")
    parents[n] = {"MANIFEST.json_sha256": h(mp) if os.path.exists(mp) else None, "status": "FROZEN, read-only"}
man = {"release": "GIG_I_v006 (Iterated Obstruction Lifting and Generative Homology)", "python": platform.python_version(), "parents": parents, "files": files,
       "dependencies": "Python standard library only (>=3.10)", "arithmetic": "exact integers and GF(2) elimination; no floats in any certificate"}
json.dump(man, open(os.path.join(ROOT, "MANIFEST.json"), "w"), indent=1, sort_keys=True)
print("manifest:", len(files), "files")
