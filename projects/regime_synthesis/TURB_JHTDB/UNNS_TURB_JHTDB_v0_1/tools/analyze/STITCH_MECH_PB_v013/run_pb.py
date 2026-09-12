from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

WRAPPER = "STITCH_MECH_PB"
WRAPPER_VERSION = "0.1.2"
MECH_REL = Path("tools/analyze/STITCH_MECH_v0_1_1")
FREEZE_REL = Path("analysis/replication/jhtdb_pilot_b/FREEZE_SHA256.txt")
PRIMARY_REL = Path("outputs/route_i/pilot_b/jhtdb_pilot_b_20260907_145640")
PRIMARY_RUN_ID = "jhtdb_pilot_b_20260907_145640"
PRIMARY_HASHES = {
    "EDGES.parquet": "5fffe762df5dd160b3551c8df6c6a2e2a23af73e2ef0f5439c8a798cc7d9f6fd",
    "NODES.parquet": "2751b0e9c5b9ff26862e73419ae18fba25cb73c58f1b53fc0ee54df2d6608dac",
    "NULLS.csv": "be6ddc5af8b1696392ccdce8e2f6f8fa7b57cce2815eeb05f7860f70e8f147a4",
    "RESULT.json": "31e3c20aa24471d78b2de3eada282fc65503de74486adef8dd3eed663a1ac567",
    "RUN.json": "2efd26cf8d76d010a04dae1773aadf99ea7dbd3a2d8ff453ce2823cf89ca135d"
}

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def sha256_file(path: Path, block=16*1024*1024):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(block), b""):
            h.update(b)
    return h.hexdigest()

def find_root(start: Path):
    for p in [start.resolve()] + list(start.resolve().parents):
        if (p/"MANIFEST.json").exists() and (p/MECH_REL).exists():
            return p
    raise RuntimeError("Could not locate UNNS_TURB_JHTDB_v0_1 project root.")

def parse_freeze(path: Path):
    rows = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line:
            continue
        digest, rel = line.split(None, 1)
        rows.append((digest.lower(), Path(rel.strip().replace("\\","/"))))
    return rows

def verify_mech_freeze(root: Path):
    rows = [
        (h, rel) for h, rel in parse_freeze(root/FREEZE_REL)
        if str(rel).replace("\\","/").startswith("tools/analyze/STITCH_MECH_v0_1_1/")
    ]
    if not rows:
        raise RuntimeError("No STITCH-MECH entries found in FREEZE_SHA256.txt.")
    for exp, rel in rows:
        p = root/rel
        if not p.exists():
            raise RuntimeError(f"Frozen STITCH-MECH file missing: {rel}")
        got = sha256_file(p)
        if got.lower() != exp:
            raise RuntimeError(f"Frozen STITCH-MECH file changed: {rel}")
    return len(rows)

def verify_primary(root: Path):
    d = root/PRIMARY_REL
    if not d.is_dir():
        raise RuntimeError(f"Primary Pilot-B run directory missing: {d}")
    for name, exp in PRIMARY_HASHES.items():
        p = d/name
        if not p.is_file():
            raise RuntimeError(f"Primary Pilot-B file missing: {p}")
        got = sha256_file(p)
        if got.lower() != exp.lower():
            raise RuntimeError(
                f"Primary Pilot-B payload checksum mismatch: {name}\n"
                f"Expected: {exp}\nFound:    {got}"
            )

    result = json.loads((d/"RESULT.json").read_text(encoding="utf-8-sig"))
    runrec = json.loads((d/"RUN.json").read_text(encoding="utf-8-sig"))
    verdict = result.get("verdict", {})
    verdict_class = verdict.get("class") if isinstance(verdict, dict) else verdict
    if result.get("meta", {}).get("run_id") != PRIMARY_RUN_ID:
        raise RuntimeError("Primary Pilot-B RESULT.json run_id mismatch.")
    if result.get("meta", {}).get("version") != "0.1.2":
        raise RuntimeError("Primary Pilot-B ROUTE-I version mismatch.")
    if verdict_class != "CONSTRAINED_ROUTING":
        raise RuntimeError(f"Unexpected primary Pilot-B verdict: {verdict_class}")
    if runrec.get("run_status") != "COMPLETE":
        raise RuntimeError("Primary Pilot-B RUN.json is not COMPLETE.")
    return d

def make_transport_zip(run_dir: Path, stage: Path):
    zpath = stage/"PB.zip"
    # Rebuild transport ZIP from already verified scientific payload.
    # Container bytes are transport only; their hash is written into CONFIG_PB.json.
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in PRIMARY_HASHES:
            zf.write(run_dir/name, name)
    return zpath, sha256_file(zpath)

def make_config(root: Path, stage: Path, zip_sha: str):
    original = json.loads((root/MECH_REL/"CONFIG.json").read_text(encoding="utf-8-sig"))
    cfg = copy.deepcopy(original)
    cfg["pilot"] = "jhtdb_pilot_b"
    cfg["frozen_run"]["relative_path"] = "PB.zip"
    cfg["frozen_run"]["sha256"] = zip_sha

    # Scientific settings are copied verbatim from the frozen config.
    cfg["outputs"] = {
        "analysis_relative_dir": "analysis",
        "records_relative_dir": "records",
        "tables_relative_dir": "tables",
    }

    p = stage/"CONFIG_PB.json"
    p.write_text(json.dumps(cfg, indent=2)+"\n", encoding="utf-8")
    return p, original, cfg

def verify_config_diff(original, pb):
    # Allowed changes: pilot identity, transport source identity/path, output locations.
    a = copy.deepcopy(original)
    b = copy.deepcopy(pb)
    for x in (a,b):
        pass
    a["pilot"] = b["pilot"]
    a["frozen_run"]["relative_path"] = b["frozen_run"]["relative_path"]
    a["frozen_run"]["sha256"] = b["frozen_run"]["sha256"]
    a["outputs"] = b["outputs"]
    if a != b:
        raise RuntimeError("Pilot-B STITCH-MECH config changes frozen scientific settings.")

def run_subprocess(cmd, cwd: Path, log: Path):
    log.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # Force UTF-8 for the frozen instrument's progress output. On the user's
    # Windows locale, the default cp1251 stdout encoding cannot represent
    # characters used by STITCH-MECH progress text (for example U+2248 "≈").
    # This changes console I/O encoding only; no scientific computation.
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    with log.open("a", encoding="utf-8", newline="\n") as f:
        f.write("\n=== "+utc_now()+" ===\n")
        f.write("COMMAND: "+" ".join(str(x) for x in cmd)+"\n")
        f.flush()
        p = subprocess.Popen(
            [str(x) for x in cmd],
            cwd=str(cwd),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
        assert p.stdout is not None
        for line in p.stdout:
            print(line, end="")
            f.write(line)
            f.flush()
        return p.wait()

def copy_outputs(root: Path, stage: Path, transport_sha: str, freeze_n: int):
    analysis_src = stage/"analysis"
    records_src = stage/"records"
    tables_src = stage/"tables"

    required = [
        analysis_src/"REPORT.json",
        analysis_src/"REPORT.html",
        records_src/"STITCH_MECH_REPORT.json",
        records_src/"STITCH_MECH_RESULT.zip",
        tables_src/"STITCH_MECH_OBJECTS.csv",
        tables_src/"STITCH_NULL_HIERARCHY.csv",
        tables_src/"STITCH_N1_NULLS.csv",
        tables_src/"STITCH_N2_NULLS.csv",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("STITCH-MECH completed without expected outputs:\n  "+"\n  ".join(missing))

    report = json.loads((analysis_src/"REPORT.json").read_text(encoding="utf-8-sig"))
    if report.get("tool", {}).get("version") != "0.1.1":
        raise RuntimeError("Unexpected STITCH-MECH report version.")
    if report.get("pilot") != "jhtdb_pilot_b":
        raise RuntimeError("STITCH-MECH report is not labelled jhtdb_pilot_b.")

    analysis_dst = root/"analysis/mechanism/jhtdb_pilot_b/stitch_mech_v01"
    tables_dst = root/"outputs/tables/pilot_b"
    records_dst = root/"outputs/records/pilot_b"
    for d in (analysis_dst, tables_dst, records_dst):
        d.mkdir(parents=True, exist_ok=True)

    shutil.copy2(analysis_src/"REPORT.json", analysis_dst/"REPORT.json")
    shutil.copy2(analysis_src/"REPORT.html", analysis_dst/"REPORT_RAW.html")

    # Frozen HTML writer hardcodes "Pilot A" in its heading only.
    # Correct that presentation label after preserving the raw HTML.
    html = (analysis_src/"REPORT.html").read_text(encoding="utf-8")
    html = html.replace("JHTDB Pilot A", "JHTDB Pilot B")
    (analysis_dst/"REPORT.html").write_text(html, encoding="utf-8")

    for name in ("STITCH_MECH_OBJECTS.csv","STITCH_NULL_HIERARCHY.csv",
                 "STITCH_N1_NULLS.csv","STITCH_N2_NULLS.csv"):
        shutil.copy2(tables_src/name, tables_dst/name)

    shutil.copy2(records_src/"STITCH_MECH_REPORT.json", records_dst/"STITCH_MECH_REPORT.json")
    shutil.copy2(records_src/"STITCH_MECH_RESULT.zip", records_dst/"STITCH_MECH_RESULT_RAW.zip")

    # Build canonical bundle with corrected HTML plus unchanged scientific tables/report.
    canonical_zip = records_dst/"STITCH_MECH_RESULT.zip"
    with zipfile.ZipFile(canonical_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in [
            analysis_dst/"REPORT.json",
            analysis_dst/"REPORT.html",
            tables_dst/"STITCH_NULL_HIERARCHY.csv",
            tables_dst/"STITCH_MECH_OBJECTS.csv",
            tables_dst/"STITCH_N1_NULLS.csv",
            tables_dst/"STITCH_N2_NULLS.csv",
        ]:
            zf.write(p, p.name)

    run_record = {
        "record": "STITCH_MECH_PILOT_B_RUN",
        "wrapper_version": WRAPPER_VERSION,
        "status": "COMPLETE",
        "created_utc": utc_now(),
        "frozen_instrument": {
            "path": str(MECH_REL).replace("\\\\","/"),
            "version": "0.1.1",
            "files_verified": freeze_n,
            "modified": False,
        },
        "source": {
            "primary_run": str(PRIMARY_REL).replace("\\\\","/"),
            "file_level_sha256_verified": PRIMARY_HASHES,
            "transport_zip_sha256": transport_sha,
        },
        "scientific_config_changed": False,
        "metadata_postprocess": {
            "raw_html_preserved": "REPORT_RAW.html",
            "canonical_html_change": "heading label Pilot A -> Pilot B only",
            "scientific_values_modified": False,
        },
        "mechanistic_verdict": report.get("mechanistic_verdict"),
        "outputs": {
            "analysis": str(analysis_dst.relative_to(root)).replace("\\\\","/"),
            "tables": str(tables_dst.relative_to(root)).replace("\\\\","/"),
            "records": str(records_dst.relative_to(root)).replace("\\\\","/"),
        },
        "hashes": {
            "report_json": sha256_file(analysis_dst/"REPORT.json"),
            "null_hierarchy": sha256_file(tables_dst/"STITCH_NULL_HIERARCHY.csv"),
            "n1_nulls": sha256_file(tables_dst/"STITCH_N1_NULLS.csv"),
            "n2_nulls": sha256_file(tables_dst/"STITCH_N2_NULLS.csv"),
            "canonical_bundle": sha256_file(canonical_zip),
        },
    }
    (records_dst/"MECH_PB_RUN.json").write_text(
        json.dumps(run_record, indent=2)+"\n", encoding="utf-8"
    )
    return report, run_record

def preflight(root: Path):
    print("STITCH-MECH PILOT B — PREFLIGHT")
    freeze_n = verify_mech_freeze(root)
    print(f"[PASS] frozen STITCH-MECH files: {freeze_n}")
    run_dir = verify_primary(root)
    print("[PASS] primary Pilot-B ROUTE-I scientific payload")
    print("[PASS] primary verdict: CONSTRAINED_ROUTING")
    return freeze_n, run_dir

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    root = find_root(here)
    freeze_n, run_dir = preflight(root)
    if args.check:
        print("\n[PREFLIGHT PASS] No STITCH-MECH Pilot-B nulls were generated.")
        return 0

    local = Path(os.environ.get("LOCALAPPDATA", str(here)))
    stage = local/"UNNS"/"PBM"
    stage.mkdir(parents=True, exist_ok=True)
    (stage/"analysis").mkdir(exist_ok=True)
    (stage/"records").mkdir(exist_ok=True)
    (stage/"tables").mkdir(exist_ok=True)

    zpath, zsha = make_transport_zip(run_dir, stage)
    cfg_path, original, cfg = make_config(root, stage, zsha)
    verify_config_diff(original, cfg)
    print(f"[PASS] Pilot-B config preserves all frozen scientific settings")
    print(f"[STAGE] {stage}")
    print("[RUN] N0 import + N1(100) + N2(100); run is resumable.")

    mech_dir = root/MECH_REL
    log = root/"outputs/records/pilot_b/MECH_PB_LOG.txt"
    cmd = [
        sys.executable,
        str(mech_dir/"run_mech.py"),
        "--config", str(cfg_path),
        "--project-root", str(stage),
    ]
    rc = run_subprocess(cmd, mech_dir, log)
    if rc != 0:
        print(f"\n[FAILED] STITCH-MECH returned exit code {rc}.")
        print("The short stage is preserved and the run can be resumed.")
        return rc

    report, rec = copy_outputs(root, stage, zsha, freeze_n)
    print("\n[READY] Pilot-B STITCH-MECH complete and canonical.")
    print(f"Verdict: {report.get('mechanistic_verdict')}")
    print("Report : analysis\\\\mechanism\\\\jhtdb_pilot_b\\\\stitch_mech_v01\\\\REPORT.html")
    print("Bundle : outputs\\\\records\\\\pilot_b\\\\STITCH_MECH_RESULT.zip")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
