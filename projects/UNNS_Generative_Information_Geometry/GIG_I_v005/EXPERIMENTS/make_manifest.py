import hashlib, json, os, platform
import _path
ROOT = _path.ROOT
def h(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
files = {}
for d, ds, fs in os.walk(ROOT):
    ds[:] = [x for x in ds if x != "__pycache__"]
    for fn in sorted(fs):
        rel = os.path.relpath(os.path.join(d, fn), ROOT).replace(os.sep, "/")
        if rel != "MANIFEST.json" and not rel.endswith(".pyc"):
            files[rel] = h(os.path.join(d, fn))
parents = {}
for n in (1, 2, 3, 4):
    p = getattr(_path._v4path, "V00%d" % n)
    mp = os.path.join(p, "MANIFEST.json")
    parents["GIG_I_v00%d" % n] = {"MANIFEST.json_sha256": h(mp) if os.path.exists(mp) else None, "status": "FROZEN, read-only, imported unchanged"}
man = {"release": "GIG_I_v005 (stage 1: gate necessity and exact survival criterion)", "python": platform.python_version(), "parents": parents,
       "dependencies": "Python standard library only (>=3.10)", "files": files,
       "arithmetic": "exact integer/Fraction arithmetic and GF(2) elimination for every certificate; no floats."}
json.dump(man, open(os.path.join(ROOT, "MANIFEST.json"), "w"), indent=1, sort_keys=True)
print("manifest:", len(files), "files")
