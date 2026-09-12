from __future__ import annotations
from pathlib import Path
import io
import json
import shutil
import tempfile
import threading
import time
import uuid
import webbrowser
import zipfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from struc_route.engine import analyze_project
from struc_route.synthetic import write_fixture

ROOT = Path(__file__).resolve().parent
UI = ROOT / "ui"
OUTPUTS = ROOT / "outputs"
WORK = ROOT / ".work"
WORK.mkdir(exist_ok=True)
OUTPUTS.mkdir(exist_ok=True)

app = FastAPI(title="STRUC-ROUTE-I", version="0.1.2")
app.mount("/static", StaticFiles(directory=UI), name="static")

jobs = {}
lock = threading.Lock()

def set_job(job_id, **kwargs):
    with lock:
        jobs.setdefault(job_id, {}).update(kwargs)

def safe_extract_zip(src: Path, dst: Path):
    with zipfile.ZipFile(src, "r") as zf:
        for member in zf.infolist():
            target = (dst / member.filename).resolve()
            if not str(target).startswith(str(dst.resolve())):
                raise ValueError("Unsafe ZIP path.")
        zf.extractall(dst)

def locate_project(folder: Path):
    if (folder / "manifest.json").exists():
        return folder
    hits = list(folder.rglob("manifest.json"))
    if len(hits) != 1:
        raise ValueError("Bundle must contain exactly one manifest.json project.")
    return hits[0].parent

def start_job(project_dir: Path):
    job_id = uuid.uuid4().hex[:12]
    set_job(job_id, status="QUEUED", progress=0.0, phase="QUEUED", message="", run_id=None)

    def worker():
        try:
            set_job(job_id, status="RUNNING")
            def prog(frac, phase, msg):
                set_job(job_id, progress=float(frac), phase=phase, message=msg)
            def publish(payload):
                stage = payload.get("stage")
                if stage == "REAL_GRAPH_COMPLETE":
                    set_job(job_id, partial_result=payload)
                elif stage == "NULL_PROGRESS":
                    set_job(job_id, null_progress=payload)
            result, run_dir = analyze_project(
                project_dir, OUTPUTS, prog, publish=publish
            )
            set_job(
                job_id,
                status="COMPLETE",
                progress=1.0,
                phase="COMPLETE",
                message=result["verdict"]["class"],
                run_id=run_dir.name,
                result=result,
            )
        except Exception as e:
            set_job(job_id, status="ERROR", phase="ERROR", message=str(e), error=str(e))
    threading.Thread(target=worker, daemon=True).start()
    return job_id

@app.get("/")
def index():
    return FileResponse(UI / "index.html")

@app.get("/api/health")
def health():
    return {"instrument":"STRUC-ROUTE-I","version":"0.1.2","status":"READY"}

@app.get("/api/status/{job_id}")
def status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(404, "Unknown job")
    return jobs[job_id]

@app.post("/api/run-files")
async def run_files(
    manifest: UploadFile = File(...),
    objects: UploadFile = File(...),
    relations: UploadFile = File(...),
    families: UploadFile | None = File(None),
):
    job_dir = WORK / uuid.uuid4().hex
    job_dir.mkdir(parents=True)
    supplied = [manifest, objects, relations] + ([families] if families else [])
    for up in supplied:
        name = Path(up.filename).name
        if up is manifest:
            name = "manifest.json"
        data = await up.read()
        (job_dir / name).write_bytes(data)
    # Canonicalize names of primary tables while preserving extension.
    for up, stem in ((objects, "objects"), (relations, "relations")):
        src = job_dir / Path(up.filename).name
        dst = job_dir / f"{stem}{Path(up.filename).suffix.lower()}"
        if src != dst:
            src.replace(dst)
    if families:
        src = job_dir / Path(families.filename).name
        dst = job_dir / f"families{Path(families.filename).suffix.lower()}"
        if src != dst:
            src.replace(dst)
    return {"job_id": start_job(job_dir)}

@app.post("/api/run-bundle")
async def run_bundle(bundle: UploadFile = File(...)):
    if not bundle.filename.lower().endswith(".zip"):
        raise HTTPException(400, "Bundle must be .zip")
    base = WORK / uuid.uuid4().hex
    base.mkdir(parents=True)
    zpath = base / "bundle.zip"
    zpath.write_bytes(await bundle.read())
    unpack = base / "project"
    unpack.mkdir()
    try:
        safe_extract_zip(zpath, unpack)
        project = locate_project(unpack)
    except Exception as e:
        raise HTTPException(400, str(e))
    return {"job_id": start_job(project)}

@app.post("/api/fixture/{name}")
def fixture(name: str):
    if name not in {"perfect_chain","binary_branch","noncommuting"}:
        raise HTTPException(404, "Unknown fixture")
    folder = WORK / f"fixture_{name}_{uuid.uuid4().hex[:8]}"
    write_fixture(folder, name)
    return {"job_id": start_job(folder)}

@app.get("/api/download/{run_id}")
def download(run_id: str):
    run_dir = OUTPUTS / Path(run_id).name
    if not run_dir.exists():
        raise HTTPException(404, "Run not found")
    zpath = WORK / f"{run_dir.name}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in run_dir.rglob("*"):
            if p.is_file():
                zf.write(p, f"{run_dir.name}/{p.relative_to(run_dir)}")
    return FileResponse(zpath, media_type="application/zip", filename=zpath.name)

def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:8765")

if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="warning")
