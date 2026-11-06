"""Regenerate MANIFEST.json (file hashes + frozen-source pins).  python EXPERIMENTS/make_manifest.py"""
import hashlib, json, os, platform
import _path

FROZEN_REFERENCES = [
    {"name": "UNNS Mathematical Foundations (SELECT-II)", "path": "projects/UNNS_MATH_FOUNDATIONS/", "commit": "9a021346b2b3d964523440d2737b9d0c4ddbb3e5"},
    {"name": "UNNS Higher-Dimensional Geometry (GEO-I)", "path": "projects/UNNS_Higher-Dimensional Geometry/", "commit": "9a021346b2b3d964523440d2737b9d0c4ddbb3e5"},
    {"name": "UNNS Generative Geometry (GEO-HD-1, HD-1D v001-v004, BRIDGE v001-v005)", "path": "projects/UNNS_Generative_Geometry/", "commit": "a88f31487f3b05c9db297dcd1192d56eea2b0c7d"},
]
FROZEN_FILES_READ = {   # read-only; sha256 measured on the project owner's disk
    "GEO_HD_1D_v004/src/select_history.py": "454e7c7d159a7a69cb8a1547d9c0b4adc83efeeaee21555b76d8c09f24d5f6b7",
    "GEO_HD_1D_v004/src/thresholds.py": "091143462b8a4719ac77bfd0e76a71ed37a451a8f8bc5c965f80bdfe7b450b56",
    "GEO_HD_1D_v004/src/route_topology.py": "740d08a99f6ed45f9a809399f7f17dd9fc9b2e7804a1464f6bb93d30649f2062",
    "GEO_HD_1D_v004/src/route_complex.py": "f768df267e1001db744f3c2b918f65febbfd03053ae7e81bd56ac77798f1d817",
    "GEO_HD_1D_v004/src/swap_classes.py": "eac8acaade5161de1c804c21c8cb032059ff0b5f2f32490f67b819b80fdf172b",
    "GEO_HD_1D_v004/src/predecessor_count.py": "caa3b5f70e9d3503236e47f45a5056faaf322041e05e4c7652c1b6e2290ec340",
    "GEO_HD_1D_v003/theory/ROUTE_TOPOLOGY.md": "a0f4726a64061738c767f1156965ef7386eb0acd367a927e5c1bc58ee390bd21",
    "GEO_HD_1D_v003/results/COUNTEREXAMPLES.md": "31665a46fd618b0ef9581d495ac4f964bed65669474731332a38179c4006ed8f",
    "GEO_HD_1D_v003/results/THEOREMS.md": "bfb1cb3fd2674f14952950ec07b458dc9ce4ea739d48b49cc194568bc6d9636e",
}
FROZEN_FILES_ROOT = "UNNS_ENTANGLE_I/GEO_HD_NEXT_MILESTONE/GEO_HD_1_PROJECT/"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    files = {}
    for d, _, fs in os.walk(_path.ROOT):
        for f in sorted(fs):
            p = os.path.join(d, f)
            rel = os.path.relpath(p, _path.ROOT).replace(os.sep, "/")
            if "__pycache__" in rel or rel == "MANIFEST.json" or rel.endswith(".pyc"):
                continue
            files[rel] = sha(p)
    m = {
        "release": "GIG_I_v001", "title": "Generative Information Geometry in the UNNS Substrate: Arithmetic Ancestry, Information Loss, and History Topology",
        "date": "2026-11-05", "python_tested": platform.python_version(), "dependencies": "Python standard library only",
        "scope": "finite arithmetic history information and recombination topology (specification section 9)",
        "frozen_references": FROZEN_REFERENCES,
        "frozen_files_read_only": {"root_on_disk": FROZEN_FILES_ROOT, "sha256": FROZEN_FILES_READ,
                                   "use": "definitions of history, completeness, swap, threshold law and permutohedral complex were taken from these files and re-implemented; the engine imports none of them; the tests may cross-check against them when GIG_FROZEN_SRC is set"},
        "definitions_reused": ["SELECT-II operator T_N(m)=m(N+1)^2/N", "history / complete history (squarefree source)", "threshold law K(w)|m (D-T7)",
                               "legal adjacent swap of distinct adjacent labels", "permutohedral full-subcomplex history complex (distinct labels), GF(2) Betti numbers",
                               "inherited examples {2,3,8,9}@72 beta=(1,1,0,0) and {2,3,8,9,14}@1008 beta=(1,0,1,0,0)", "complete histories of 72 and counts |F_{72^r}|, r=1..6"],
        "no_remote_changes": "no GitHub repository or frozen release was modified",
        "files": files,
    }
    with open(os.path.join(_path.ROOT, "MANIFEST.json"), "w") as f:
        json.dump(m, f, indent=1, sort_keys=True)
    print("MANIFEST.json written,", len(files), "files")


if __name__ == "__main__":
    main()
