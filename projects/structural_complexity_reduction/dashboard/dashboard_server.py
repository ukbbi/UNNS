from __future__ import annotations

import csv
import hashlib
import json
import mimetypes
import os
import subprocess
import sys
import threading
import time
import webbrowser
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

DASHBOARD_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DASHBOARD_DIR.parent
CONFIG_PATH = DASHBOARD_DIR / "dashboard_config.json"
HTML_PATH = DASHBOARD_DIR / "SCR_I_DASHBOARD.html"

with CONFIG_PATH.open("r", encoding="utf-8") as fh:
    CONFIG = json.load(fh)

PREREG_DIR = PROJECT_ROOT / CONFIG["preregistration_dir"]
OUTPUT_DIR = PROJECT_ROOT / CONFIG["primary_output_dir"]
INPUT_DIR = PROJECT_ROOT / "inputs"

MAX_PREVIEW_BYTES = 1024 * 1024
MAX_TABLE_ROWS = 200


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = f"blob {len(data)}\0".encode("ascii") + data
    return hashlib.sha1(payload).hexdigest()


def safe_rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PROJECT_ROOT.resolve())).replace("\\", "/")
    except Exception:
        return path.name


def json_read(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def prereg_config() -> dict[str, Any] | None:
    p = PREREG_DIR / CONFIG.get("prereg_config_file", "config/scr_i_prereg_v003.json")
    if not p.is_file():
        return None
    try:
        return json_read(p)
    except Exception:
        return None


def validate_prereg() -> dict[str, Any]:
    script = PREREG_DIR / "scripts" / "validate_prereg.py"
    if not script.is_file():
        return {"ok": False, "returncode": None, "stdout": "", "stderr": "validate_prereg.py not found"}
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(PREREG_DIR),
        text=True,
        capture_output=True,
        timeout=120,
    )
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-12000:],
        "stderr": proc.stderr[-12000:],
    }


def locate_source_file(repo_path: str) -> Path | None:
    rel = Path(*repo_path.split("/"))
    env_root = os.environ.get("UNNS_REPO")
    candidates: list[Path] = []
    if env_root:
        candidates.append(Path(env_root))
    candidates.extend([
        PROJECT_ROOT,
        PROJECT_ROOT.parent,
        PROJECT_ROOT.parent.parent,
        PROJECT_ROOT.parent.parent.parent,
        PROJECT_ROOT.parent.parent.parent.parent,
    ])
    # Common optional local source-lock locations.
    local_name = rel.name
    for d in [PROJECT_ROOT / "references" / "source_lock", DASHBOARD_DIR / "source_lock"]:
        p = d / local_name
        if p.is_file():
            return p
    seen: set[str] = set()
    for root in candidates:
        try:
            key = str(root.resolve())
        except Exception:
            key = str(root)
        if key in seen:
            continue
        seen.add(key)
        p = root / rel
        if p.is_file():
            return p
    return None


def source_lock_status() -> dict[str, Any]:
    entries = []
    all_ok = True
    for item in CONFIG.get("source_lock", {}).get("files", []):
        located = locate_source_file(item["path"])
        if located is None:
            entries.append({**item, "found": False, "match": False, "local_path": None, "actual_git_blob_sha": None})
            all_ok = False
            continue
        try:
            actual = git_blob_sha(located)
            match = actual == item["git_blob_sha"]
        except Exception as exc:
            actual = f"ERROR: {exc}"
            match = False
        entries.append({
            **item,
            "found": True,
            "match": match,
            "local_path": str(located),
            "actual_git_blob_sha": actual,
        })
        all_ok = all_ok and match
    return {"ok": all_ok, "entries": entries, "commit_reference": CONFIG.get("source_lock", {}).get("commit_reference")}


def summarize_file(path: Path) -> dict[str, Any]:
    stat = path.stat()
    info = {
        "name": path.name,
        "path": safe_rel(path),
        "size": stat.st_size,
        "mtime": stat.st_mtime,
        "suffix": path.suffix.lower(),
        "sha256": None,
        "rows": None,
        "columns": None,
        "json_type": None,
        "error": None,
    }
    if stat.st_size <= 64 * 1024 * 1024:
        try:
            info["sha256"] = sha256_file(path)
        except Exception as exc:
            info["error"] = str(exc)
    try:
        if path.suffix.lower() in {".csv", ".tsv"} and stat.st_size <= MAX_PREVIEW_BYTES:
            delim = "\t" if path.suffix.lower() == ".tsv" else ","
            with path.open("r", encoding="utf-8-sig", newline="") as fh:
                reader = csv.reader(fh, delimiter=delim)
                rows = list(reader)
            info["rows"] = max(0, len(rows) - 1)
            info["columns"] = rows[0] if rows else []
        elif path.suffix.lower() == ".json" and stat.st_size <= MAX_PREVIEW_BYTES:
            data = json_read(path)
            info["json_type"] = type(data).__name__
            if isinstance(data, list):
                info["rows"] = len(data)
            elif isinstance(data, dict):
                info["columns"] = list(data.keys())[:80]
    except Exception as exc:
        info["error"] = str(exc)
    return info


def inventory(root: Path) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    files = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        files.append(summarize_file(path))
    return files


def candidate_primary_results() -> list[Path]:
    found: list[Path] = []
    if OUTPUT_DIR.exists():
        found.extend(OUTPUT_DIR.rglob(CONFIG.get("primary_result_glob", "PRIMARY_RESULT_v003*.json")))
    prereg_out = PREREG_DIR / "output"
    if prereg_out.exists():
        found.extend(prereg_out.rglob(CONFIG.get("primary_result_glob", "PRIMARY_RESULT_v003*.json")))
    # De-duplicate by resolved path.
    uniq = {}
    for p in found:
        try:
            uniq[str(p.resolve())] = p
        except Exception:
            uniq[str(p)] = p
    return sorted(uniq.values(), key=lambda p: p.stat().st_mtime, reverse=True)


def load_primary_results() -> list[dict[str, Any]]:
    out = []
    for path in candidate_primary_results():
        try:
            data = json_read(path)
            records = data if isinstance(data, list) else [data]
            for rec in records:
                if not isinstance(rec, dict):
                    continue
                out.append({"path": safe_rel(path), "mtime": path.stat().st_mtime, "sha256": sha256_file(path), "record": rec})
        except Exception as exc:
            out.append({"path": safe_rel(path), "mtime": path.stat().st_mtime, "sha256": None, "error": str(exc), "record": {}})
    return out


def aggregate_results(items: list[dict[str, Any]]) -> dict[str, Any]:
    records=[x["record"] for x in items if isinstance(x.get("record"),dict) and x.get("record")]
    if not records:return {"available":False}
    def nums(k):
        return [float(r[k]) for r in records if isinstance(r.get(k),(int,float)) and not isinstance(r.get(k),bool)]
    def med(v):
        if not v:return None
        s=sorted(v);n=len(s);return s[n//2] if n%2 else (s[n//2-1]+s[n//2])/2
    target_base=sum(int(r.get("target_count_base",0) or 0) for r in records)
    target_scr=sum(round(float(r.get("candidate_target_recall",0) or 0)*int(r.get("target_count_base",0) or 0)) for r in records)
    by_size={}
    for size in sorted({int(r.get("pool_size",0)) for r in records if r.get("pool_size")}):
        rr=[r for r in records if int(r.get("pool_size",0))==size]
        by_size[str(size)]={
            "records":len(rr),
            "preserved":sum(1 for r in rr if r.get("verdict")=="STRUCTURAL_COMPRESSION_PRESERVED"),
            "representation_loss":sum(1 for r in rr if r.get("verdict")=="REPRESENTATION_LOSS"),
            "median_r_candidate":med([float(r["r_candidate"]) for r in rr if isinstance(r.get("r_candidate"),(int,float))]),
            "median_basin_coverage":med([float(r["min_basin_geometric_coverage"]) for r in rr if isinstance(r.get("min_basin_geometric_coverage"),(int,float))]),
        }
    return {
      "available":True,"records":len(records),"n0":sum(int(r.get("n0",0) or 0) for r in records),"n1":sum(int(r.get("n1",0) or 0) for r in records),
      "target_count_base":target_base,"target_count_scr":target_scr,
      "minimum_basin_recall":min(nums("basin_recall")) if nums("basin_recall") else None,
      "minimum_basin_coverage":min(nums("min_basin_geometric_coverage")) if nums("min_basin_geometric_coverage") else None,
      "maximum_centroid_drift":max(nums("max_basin_centroid_drift")) if nums("max_basin_centroid_drift") else None,
      "minimum_signature_recall":min(nums("signature_stratum_recall")) if nums("signature_stratum_recall") else None,
      "median_candidate_target_recall":med(nums("candidate_target_recall")),"median_r_candidate":med(nums("r_candidate")),"median_r_eval":med(nums("r_eval")),"median_g_time":med(nums("g_time")),"median_g_ops":med(nums("g_ops")),
      "verdicts":sorted({str(r.get("verdict")) for r in records if r.get("verdict")}),"by_size":by_size
    }


def run_readiness() -> dict[str, Any]:
    sources=source_lock_status(); runner=None
    for rel in CONFIG["execution"]["primary_runner_candidates"]:
        p=PROJECT_ROOT/rel
        if p.is_file():runner=p;break
    prereg_ok=validate_prereg()["ok"] if PREREG_DIR.exists() else False
    audit_marker=PROJECT_ROOT/CONFIG["execution"].get("design_preservation_audit_marker","output/v003_phase1/DESIGN_PRESERVATION_AUDIT_PASS.json")
    def marker_ok(path):
        try:return path.is_file() and bool(json_read(path).get("ok"))
        except Exception:return False
    design_ok=marker_ok(audit_marker)
    progress_path=PROJECT_ROOT/"output"/"RUN_PROGRESS_v003.json"
    result_path=PROJECT_ROOT/"output"/"PRIMARY_RESULT_v003.json"
    try:
        progress=json_read(progress_path) if progress_path.is_file() else {}
        primary_complete=bool(result_path.is_file() and progress.get("status")=="COMPLETE" and int(progress.get("completed_cells",0))==int(progress.get("total_cells",-1))==15)
    except Exception:
        primary_complete=False
    primary_enabled=bool(prereg_ok and sources["ok"] and design_ok and runner is not None and not primary_complete)
    return {"prereg_ok":prereg_ok,"source_lock_ok":sources["ok"],"adapter_regression_pass":design_ok,"adapter_regression_marker":safe_rel(audit_marker),"design_preservation_audit_pass":design_ok,"design_preservation_audit_marker":safe_rel(audit_marker),"runner_found":runner is not None,"runner":safe_rel(runner) if runner else None,"primary_complete":primary_complete,"primary_enabled":primary_enabled}


def project_status(run_validation: bool = False) -> dict[str, Any]:
    pconfig = prereg_config()
    validation = validate_prereg() if run_validation and PREREG_DIR.exists() else None
    results = load_primary_results()
    return {
        "dashboard": CONFIG["dashboard_version"],
        "project_root": str(PROJECT_ROOT),
        "prereg_dir": str(PREREG_DIR),
        "prereg_exists": PREREG_DIR.is_dir(),
        "prereg_config": pconfig,
        "validation": validation,
        "source_lock": source_lock_status(),
        "readiness": run_readiness(),
        "inputs": inventory(INPUT_DIR),
        "outputs": inventory(OUTPUT_DIR),
        "prereg_outputs": inventory(PREREG_DIR / "output"),
        "primary_results": results,
        "aggregate": aggregate_results(results),
        "expected_primary_files": CONFIG.get("expected_primary_files", []),
        "historical_v001_feasibility": (json_read(PROJECT_ROOT / CONFIG["historical_v001_feasibility"]) if CONFIG.get("historical_v001_feasibility") and (PROJECT_ROOT / CONFIG["historical_v001_feasibility"]).is_file() else None),
        "server_time": time.time(),
    }


def read_doc(name: str) -> dict[str, Any]:
    allowed = {
        "README.md", "PREREG.md", "BASIN_ORACLE.md", "DESIGN_AUDIT.md", "V002_TRANSITION.md", "BENCH_A.md", "GATES.md", "METRICS.md",
        "NULLS.md", "DECISION_RULES.md", "RUN_PLAN.md", "SOURCE_LOCK.md", "UPI_BLIND.md", "MANIFEST.md"
    }
    if name not in allowed:
        raise ValueError("Document not allowed")
    path = PREREG_DIR / name
    if not path.is_file():
        raise FileNotFoundError(name)
    return {"name": name, "text": path.read_text(encoding="utf-8-sig"), "sha256": sha256_file(path)}


def execute_primary_runner() -> dict[str, Any]:
    ready = run_readiness()
    if not ready["primary_enabled"]:
        return {"ok": False, "blocked": True, "readiness": ready, "message": "Primary execution remains locked by preregistration readiness requirements."}
    runner = PROJECT_ROOT / ready["runner"]
    if runner.suffix.lower() == ".py":
        cmd = [sys.executable, str(runner)]
    elif os.name == "nt" and runner.suffix.lower() == ".bat":
        cmd = ["cmd", "/c", str(runner)]
    else:
        return {"ok": False, "blocked": True, "message": "Runner type is not executable on this platform."}
    proc = subprocess.run(cmd, cwd=str(PROJECT_ROOT), text=True, capture_output=True, timeout=24 * 3600)
    return {"ok": proc.returncode == 0, "returncode": proc.returncode, "stdout": proc.stdout[-20000:], "stderr": proc.stderr[-20000:]}


def freeze_primary() -> dict[str, Any]:
    results = candidate_primary_results()
    if not results:
        return {"ok": False, "message": "No PRIMARY_RESULT JSON exists."}
    # Freeze the newest result only. Never mutate result content.
    path = results[0]
    digest = sha256_file(path)
    marker = path.with_suffix(path.suffix + ".sha256")
    if marker.exists():
        existing = marker.read_text(encoding="utf-8").strip().split()[0]
        if existing != digest:
            return {"ok": False, "message": "Existing freeze hash does not match current result bytes; refusing to overwrite.", "path": safe_rel(path)}
        return {"ok": True, "already_frozen": True, "sha256": digest, "path": safe_rel(path), "marker": safe_rel(marker)}
    marker.write_text(f"{digest}  {path.name}\n", encoding="utf-8")
    return {"ok": True, "already_frozen": False, "sha256": digest, "path": safe_rel(path), "marker": safe_rel(marker)}


def open_output_folder() -> dict[str, Any]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        if os.name == "nt":
            os.startfile(str(OUTPUT_DIR))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(OUTPUT_DIR)])
        else:
            subprocess.Popen(["xdg-open", str(OUTPUT_DIR)])
        return {"ok": True, "path": str(OUTPUT_DIR)}
    except Exception as exc:
        return {"ok": False, "path": str(OUTPUT_DIR), "message": str(exc)}


class Handler(BaseHTTPRequestHandler):
    server_version = "SCRDashboard/0.0.3"

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stdout.write("[dashboard] " + (fmt % args) + "\n")

    def _json(self, data: Any, status: int = 200) -> None:
        payload = json.dumps(data, ensure_ascii=False, indent=None).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def _bytes(self, data: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        try:
            if path in {"/", "/index.html", "/SCR_I_DASHBOARD.html"}:
                self._bytes(HTML_PATH.read_bytes(), "text/html; charset=utf-8")
                return
            if path == "/api/status":
                self._json(project_status(run_validation=False))
                return
            if path == "/api/validate":
                self._json(validate_prereg())
                return
            if path == "/api/readiness":
                self._json(run_readiness())
                return
            if path == "/api/doc":
                qs = parse_qs(parsed.query)
                name = qs.get("name", [""])[0]
                self._json(read_doc(name))
                return
            if path == "/api/results":
                items = load_primary_results()
                self._json({"items": items, "aggregate": aggregate_results(items)})
                return
            if path == "/api/health":
                self._json({"ok": True, "dashboard": CONFIG["dashboard_version"]})
                return
            self._json({"error": "not found"}, status=404)
        except FileNotFoundError as exc:
            self._json({"error": f"file not found: {exc}"}, status=404)
        except Exception as exc:
            self._json({"error": str(exc)}, status=500)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        try:
            if path == "/api/actions/validate_prereg":
                self._json(validate_prereg())
                return
            if path == "/api/actions/run_primary":
                self._json(execute_primary_runner())
                return
            if path == "/api/actions/freeze_primary":
                self._json(freeze_primary())
                return
            if path == "/api/actions/open_output":
                self._json(open_output_folder())
                return
            self._json({"error": "not found"}, status=404)
        except subprocess.TimeoutExpired:
            self._json({"error": "operation timed out"}, status=504)
        except Exception as exc:
            self._json({"error": str(exc)}, status=500)


def choose_port(start: int = 8765, attempts: int = 20) -> int:
    import socket
    for port in range(start, start + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No local dashboard port available")


def main() -> int:
    if not HTML_PATH.is_file():
        print(f"Missing dashboard HTML: {HTML_PATH}", file=sys.stderr)
        return 2
    port = choose_port()
    url = f"http://127.0.0.1:{port}/"
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("SCR-I Dashboard")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"URL: {url}")
    print("Press Ctrl+C in this window to stop the dashboard server.")
    if "--no-browser" not in sys.argv:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
