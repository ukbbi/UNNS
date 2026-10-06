#!/usr/bin/env python3
"""
BUILD_ANALYTICS.py  --  UNNS_VACUUM_CONTINUITY research analytics builder.

Reads the frozen result records of the two linked projects
    UNNS_YM_GAP            (closed 2026-09-30, terminal YM-3B)
    UNNS_VACUUM_CONTINUITY (closed 2026-10-06, Stage 3)
assembles one DATA object (numbers are parsed from the project's own CSV/JSON/MD
records; none are typed in), hashes every source file with SHA-256, and embeds the
result into a single self-contained HTML file (no server, no fetch, no CDN).

Usage (defaults assume the layout  <parent>/UNNS_YM_GAP  and
<parent>/UNNS_VACUUM_CONTINUITY/analytics/BUILD_ANALYTICS.py):

    python analytics/BUILD_ANALYTICS.py
    python analytics/BUILD_ANALYTICS.py --gap PATH --vc PATH --out FILE
"""
import argparse, ast, csv, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--vc", default=str(HERE.parent))
ap.add_argument("--gap", default=str(HERE.parent.parent / "UNNS_YM_GAP"))
ap.add_argument("--out", default=str(HERE.parent / "UNNS_VACUUM_CONTINUITY_ANALYTICS.html"))
ap.add_argument("--template", default=str(HERE / "analytics_template.html"))
args = ap.parse_args()
VC, GAP = Path(args.vc), Path(args.gap)

PROV = {}          # label -> {path, sha256, bytes}
MISSING = []
CHECKS = []        # integrity checks (name, ok, detail)


def _p(root, rel, tag):
    return root / rel, f"{tag}/{rel}"


def rd(root, rel, tag, binary=False):
    path, label = _p(root, rel, tag)
    if not path.exists():
        MISSING.append(label)
        raise FileNotFoundError(label)
    b = path.read_bytes()
    PROV[label] = {"path": label, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    return b if binary else b.decode("utf-8").replace("\r\n", "\n")


def csv_rows(root, rel, tag):
    return list(csv.DictReader(rd(root, rel, tag).splitlines()))


def jload(root, rel, tag):
    return json.loads(rd(root, rel, tag))


def num(x):
    if x in ("True", "False"):
        return x == "True"
    try:
        return float(x)
    except (TypeError, ValueError):
        return x


def numrow(r):
    return {k: num(v) for k, v in r.items()}


def must_contain(name, text, needle):
    ok = needle in text
    CHECKS.append({"name": name, "ok": ok, "needle": needle})
    return ok


G, V = "UNNS_YM_GAP", "UNNS_VACUUM_CONTINUITY"

# ------------------------------------------------------------------ YM_GAP
closure = jload(GAP, "docs/CLOSURE_RECORD.json", G)
final_status = rd(GAP, "FINAL_STATUS.md", G)
readme_gap = rd(GAP, "README.md", G)
ym3_txt = rd(GAP, "docs/YM3_RESULT.md", G)
ym3b_txt = rd(GAP, "docs/YM3B_RESULT.md", G)
ym3 = [numrow(r) for r in csv_rows(GAP, "output/ym3/YM3_SUMMARY.csv", G)]
ym3b = [numrow(r) for r in csv_rows(GAP, "output/ym3b/YM3B_SUMMARY.csv", G)]
ym3b_unc = [numrow(r) for r in csv_rows(GAP, "output/ym3b/YM3B_UNCERTAINTY_SUMMARY.csv", G)]
ym3b_r3 = [numrow(r) for r in csv_rows(GAP, "output/ym3b/YM3B_R3.csv", G)]
gap_ladder = [numrow(r) for r in csv_rows(GAP, "ladders/ym1a_gap.csv", G)]
continuum = [numrow(r) for r in csv_rows(GAP, "ladders/ym1a_continuum.csv", G)]

must_contain("YM-3A verdict string", ym3_txt, "MODEL-REFINEMENT PERSISTENT")
must_contain("YM-3B verdict string", ym3b_txt, "DATA-INDETERMINATE")
must_contain("YM_GAP central hypothesis", final_status, "NOT ESTABLISHED")
must_contain("YM-2 stage verdict", readme_gap, "VACUUM-BOUNDARY DIAGNOSTIC ESTABLISHED; REFINEMENT TEST REQUIRED")
must_contain("CLOSURE_RECORD ym3a", json.dumps(closure), "MODEL-REFINEMENT PERSISTENT")
must_contain("CLOSURE_RECORD ym3b", json.dumps(closure), "DATA-INDETERMINATE")

# ------------------------------------------------------------------ VACUUM_CONTINUITY
s1 = rd(VC, "stage1/STAGE1_FREEZE.md", V)
s2_syn = rd(VC, "stage2/STAGE2_SYNTHESIS.md", V)
s2_status = rd(VC, "stage2/STAGE2_STATUS.md", V)
s2_freeze = jload(VC, "stage2/STAGE2_FREEZE.json", V)
emt_lock = rd(VC, "stage2/EMT_PRIMARY_RESULT_LOCK.md", V)
emt_geom_res = rd(VC, "stage2/EMT_GEOM_RESULT.md", V)
bat_res = rd(VC, "stage2/BATTELLI_CTRL_RESULT.md", V)
vref_a_rep = rd(VC, "output/reports/VREF_A_REPORT.md", V)
vref_b_rep = rd(VC, "output/reports/VREF_B_REPORT.md", V)
emt_rep = rd(VC, "output/yanagihara_emt/reports/EMT_I_REPORT.md", V)
emt_geom_rep = rd(VC, "output/yanagihara_emt/geometry/reports/EMT_GEOM_REPORT.md", V)
vref_a = [numrow(r) for r in csv_rows(VC, "output/tables/VREF_A_REFINEMENT.csv", V)]
vref_b = [numrow(r) for r in csv_rows(VC, "output/tables/VREF_B_REFINEMENT.csv", V)]
emt_fits = [numrow(r) for r in csv_rows(VC, "output/yanagihara_emt/tables/EMT_I_FITS.csv", V)]
emt_geom_fits = [numrow(r) for r in csv_rows(VC, "output/yanagihara_emt/geometry/tables/EMT_GEOM_FITS.csv", V)]
spec_a_txt = rd(VC, "output/spec_i_a/SPEC_I_A_RESULT.md", V)
spec_b_txt = rd(VC, "output/spec_i_b/SPEC_I_B_RESULT.md", V)
spec_a = jload(VC, "data/derived/at20/SPEC_I_A_EXTRACT.json", V)
spec_b = jload(VC, "data/derived/chen06/SPEC_I_B_EXTRACT.json", V)
bridge_txt = rd(VC, "output/bridge_iii/BRIDGE_III_RESULT.md", V)
bridge = jload(VC, "output/bridge_iii/BRIDGE_III_RUN.json", V)
lock = rd(VC, "stage3/BRIDGE_III_LOCK.md", V)
closure_vc = rd(VC, "stage3/PROJECT_CLOSURE.md", V)
s3_syn = rd(VC, "stage3/STAGE3_SYNTHESIS.md", V)
s3_manifest = jload(VC, "stage3/STAGE3_CLOSE_MANIFEST.json", V)

# ---- verdict strings verified against their source records
VERDICTS = [
    ("Baker 2022 · VREF-I/A", "CALIBRATION-SENSITIVE", vref_a_rep),
    ("CEA 2017 · VREF-I/B", "REFINEMENT-INDETERMINATE", vref_b_rep),
    ("CEA 2017 · STRUC bridge", "ARCHITECTURE-PRESERVED", s2_status),
    ("Battelli 2019 · unsmoothed control", "UNSMOOTHED-ARCHITECTURE-CONSISTENT", bat_res),
    ("Yanagihara 2019 · EMT-I R=0.69", "EMT-UNCERTAINTY-LIMITED", emt_rep),
    ("Yanagihara 2019 · geometry", "GEOMETRY-ROBUST-NO-FLOOR", emt_geom_rep),
    ("Stage 2 synthesis", "NO-UNIVERSAL-STRUCTURAL-EXCLUSION-DETECTED", s2_status),
    ("Stage 2 interpretation", "STRUCTURAL-VACUUM-ACCESSIBILITY-SUPPORTED", s2_status),
    ("SPEC-I/A", "SPECTRAL-SCALE-POSITIVE", spec_a_txt),
    ("SPEC-I/B", "SPECTRAL-SCALE-POSITIVE", spec_b_txt),
    ("BRIDGE-III", "COEXISTENCE-SUPPORTED", bridge_txt),
    ("Stage 3 / project", "STRUCTURAL-SPECTRAL-COEXISTENCE-SUPPORTED", closure_vc),
]
for name, needle, text in VERDICTS:
    must_contain(f"{name}: {needle}", text, needle)
must_contain("BRIDGE_III_RUN outcome", json.dumps(bridge), "COEXISTENCE-SUPPORTED")
must_contain("Stage-1 sentence", s1, "The mass gap separates eigenvalues, not necessarily structural neighborhoods.")

# ---- parsed values from markdown reports
def parse_aicc_table(text):
    rows = []
    for m in re.finditer(r"\|\s*(PRIMARY|DROP-FIRST)\s*\|\s*(\w+)\s*\|\s*([-\d.]+)\s*\|\s*(\w+)\s*\|", text):
        rows.append({"tail": m.group(1), "family": m.group(2), "dAICc": float(m.group(3)), "cls": m.group(4)})
    return rows

cea_aicc = parse_aicc_table(vref_b_rep)
chi2_ref = float(re.search(r"chi2_ref / N_tail:\s*([\d.]+)", vref_b_rep).group(1))
n_tail = int(re.search(r"tail common-grid points:\s*(\d+)", vref_b_rep).group(1))
cea_rows = int(re.search(r"rows:\s*(\d+)", vref_b_rep).group(1))
cea_support = re.search(r"common support:\s*([^\n]+)", vref_b_rep).group(1).strip()
cea_cut = re.search(r"primary tail cut:\s*([^\n]+)", vref_b_rep).group(1).strip()

bat = []
for m in re.finditer(r"\|\s*(B\d)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|", bat_res):
    bat.append({"ladder": m.group(1), "regime": m.group(2), "state": m.group(3),
                "mean_Ak": float(m.group(4)), "min_Ak": float(m.group(5)), "max_rho": float(m.group(6))})
bat_n = {m.group(1): int(m.group(2)) for m in re.finditer(r"^(B\d)\s+n=(\d+)", bat_res, re.M)}
bat_kappa = {m.group(1): float(m.group(2)) for m in re.finditer(r"^(B\d)\s+kappa_connect = ([\d.]+)", bat_res, re.M)}
for b in bat:
    b["n"] = bat_n.get(b["ladder"])
    b["kappa_connect"] = bat_kappa.get(b["ladder"])
must_contain("Battelli: 3 ladders parsed", str(len(bat)), "3")

emt_components = {}
m = re.findall(r"- `(\w+)`: \*\*([A-Z-]+)\*\*", emt_rep)
emt_components["R069"] = dict(m)
for geo in ("R046", "R092"):
    blk = re.search(rf"## {geo}[^\n]*\n(?:.*\n)*?- components: (\{{[^\n]*\}})", emt_geom_rep)
    emt_components[geo] = ast.literal_eval(blk.group(1))
emt_norm = {}
emt_norm["R069"] = "VACUUM-DIRECTED" if re.search(r"four-component norm path: VACUUM-DIRECTED", emt_rep) else "?"
for geo in ("R046", "R092"):
    blk = re.search(rf"## {geo}[^\n]*\n- outcome: \*\*([A-Z-]+)\*\*\n- four-component norm path: ([A-Z-]+)\n- tail points: (\d+)", emt_geom_rep)
    emt_norm[geo] = {"outcome": blk.group(1), "path": blk.group(2), "tail": int(blk.group(3))}
emt_norm["R069"] = {"outcome": "EMT-UNCERTAINTY-LIMITED", "path": "VACUUM-DIRECTED",
                    "tail": int(re.search(r"tail coordinates:\s*(\d+)", emt_rep).group(1))}

# EMT dAICc (floor - zero), one value per geometry x tail x family
emt_daicc = []
seen = set()
for r in emt_fits:
    key = ("R069", 0.69, "PRIMARY" if "PRIMARY" in r["tail_cut"] else "DROP-FIRST", r["family"])
    if key in seen:
        continue
    seen.add(key)
    emt_daicc.append({"geom": "R069", "R_fm": 0.69, "tail": key[2],
                      "family": "K0" if "K0" in r["family"] else "exp",
                      "dAICc": r["delta_AICc_floor_minus_zero"], "n": r["n"], "cls": r["classification"]})
seen = set()
for r in emt_geom_fits:
    tail = "PRIMARY" if r["tail_cut"] == "PRIMARY" else "DROP-FIRST"
    key = (r["geometry"], r["R_fm"], tail, r["family"])
    if key in seen:
        continue
    seen.add(key)
    emt_daicc.append({"geom": r["geometry"], "R_fm": r["R_fm"], "tail": tail,
                      "family": "K0" if "K0" in r["family"] else "exp",
                      "dAICc": r["delta_AICc_floor_minus_zero"], "n": r["n"], "cls": r["classification"]})
emt_daicc.sort(key=lambda d: (d["R_fm"], d["tail"] != "PRIMARY", d["family"]))

# ---- manifest hash audit: recorded sha256 vs the file actually present
hash_audit = []
for man_name, man in (("STAGE2_FREEZE.json", s2_freeze), ("STAGE3_CLOSE_MANIFEST.json", s3_manifest)):
    for f in man["files"]:
        fp = VC / f["path"]
        if fp.exists():
            actual = hashlib.sha256(fp.read_bytes()).hexdigest()
            hash_audit.append({"manifest": man_name, "path": f["path"], "recorded": f["sha256"],
                               "actual": actual, "match": actual == f["sha256"]})
            PROV.setdefault(f"{V}/{f['path']}", {"path": f"{V}/{f['path']}", "sha256": actual, "bytes": fp.stat().st_size})
        else:
            hash_audit.append({"manifest": man_name, "path": f["path"], "recorded": f["sha256"],
                               "actual": None, "match": None})

# bridge input hash audit (BRIDGE_III_RUN.json records the sha256 of its three inputs)
bridge_inputs = []
for k, v in bridge["inputs"].items():
    fp = VC / v["path"]
    actual = hashlib.sha256(fp.read_bytes()).hexdigest() if fp.exists() else None
    bridge_inputs.append({"input": k, "path": v["path"], "recorded": v["sha256"], "actual": actual,
                          "match": (actual == v["sha256"]) if actual else None})

DATA = {
    "meta": {
        "title": "UNNS Vacuum Continuity — Research Analytics",
        "subtitle": "Non-Crossability Program · Structural Vacuum Accessibility · Spectral Scale · BRIDGE-III Coexistence",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "projects": [
            {"id": G, "status": "CLOSED", "date": closure["closed_date"], "terminal": "YM-3B · DATA-INDETERMINATE"},
            {"id": V, "status": "CLOSED — PRIMARY PROGRAM COMPLETE", "date": "2026-10-06",
             "terminal": "STRUCTURAL-SPECTRAL-COEXISTENCE-SUPPORTED"},
        ],
    },
    "gap": {
        "closure": closure,
        "ym3": ym3, "ym3b": ym3b, "ym3b_unc": ym3b_unc, "ym3b_r3": ym3b_r3,
        "gap_ladder": gap_ladder, "continuum": continuum,
    },
    "vc": {
        "verdicts": [{"branch": n, "verdict": v, "verified": True} for n, v, _ in VERDICTS],
        "vref_a": vref_a, "vref_b": vref_b, "cea_aicc": cea_aicc,
        "cea": {"chi2_ref_per_N": chi2_ref, "n_tail": n_tail, "rows": cea_rows,
                "support": cea_support, "tail_cut": cea_cut},
        "battelli": bat, "emt_daicc": emt_daicc,
        "emt_components": emt_components, "emt_norm": emt_norm,
        "spec_a": spec_a, "spec_b": spec_b,
        "bridge": {"outcome": bridge["outcome"], "checks": bridge["checks"],
                   "run_utc": bridge["run_utc"],
                   "earlier_verdicts_modified": bridge["earlier_verdicts_modified"],
                   "mass_gap_theorem_claimed": bridge["mass_gap_theorem_claimed"],
                   "closure_theorem_claimed": bridge["closure_theorem_claimed"]},
        "bridge_inputs": bridge_inputs,
    },
    "reproducibility": {
        "provenance": sorted(PROV.values(), key=lambda p: p["path"]),
        "missing_sources": MISSING,
        "checks": CHECKS,
        "hash_audit": hash_audit,
        "build_timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
}

for _f, _lab in ((Path(__file__).resolve(), "analytics/BUILD_ANALYTICS.py"), (Path(args.template), "analytics/analytics_template.html")):
    _b = _f.read_bytes()
    PROV[_lab] = {"path": _lab, "sha256": hashlib.sha256(_b).hexdigest(), "bytes": len(_b)}
DATA["reproducibility"]["provenance"] = sorted(PROV.values(), key=lambda p: p["path"])

tpl = Path(args.template).read_text(encoding="utf-8")
assert "/*__DATA__*/null" in tpl, "template placeholder missing"
html = tpl.replace("/*__DATA__*/null", json.dumps(DATA, ensure_ascii=True, separators=(",", ":")))
Path(args.out).write_text(html, encoding="utf-8")

bad = [c for c in CHECKS if not c["ok"]]
print(f"wrote {args.out}  ({len(html):,} bytes)")
print(f"sources hashed: {len(PROV)} | verdict/string checks: {len(CHECKS)-len(bad)}/{len(CHECKS)} | missing: {len(MISSING)}")
print("manifest hash audit:", sum(1 for h in hash_audit if h['match']), "match,",
      sum(1 for h in hash_audit if h['match'] is False), "MISMATCH,",
      sum(1 for h in hash_audit if h['match'] is None), "not present")
print("bridge input hashes:", [b["match"] for b in bridge_inputs])
if bad:
    print("FAILED CHECKS:", bad)
    sys.exit(1)
