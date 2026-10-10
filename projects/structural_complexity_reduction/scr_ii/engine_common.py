from __future__ import annotations
import hashlib, json, os, time
from pathlib import Path
from typing import Any

ENGINE_VERSION = "SCR_II_ENGINE_v001"
BENCHMARK = "ROUTE_CSP_I"
PREREG = "SCR_II_PREREG_v001"

def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha256_obj(obj: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(obj)).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def safe_write_json(path: Path, obj: Any, retries: int = 12, delay: float = 0.15) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(obj, indent=2, sort_keys=True) + "\n"
    tmp = path.with_name(path.name + f".{os.getpid()}.{time.time_ns()}.tmp")
    tmp.write_text(payload, encoding="utf-8")
    last = None
    for i in range(retries):
        try:
            os.replace(tmp, path)
            return
        except PermissionError as e:
            last = e
            time.sleep(delay * (i + 1))
    recovery = path.with_name(path.name + f".recovery.{int(time.time())}.json")
    recovery.write_text(payload, encoding="utf-8")
    try:
        tmp.unlink(missing_ok=True)
    except Exception:
        pass
    raise RuntimeError(f"Could not replace {path} after retries; recovery saved to {recovery}") from last

def find_scr_ii_root(start: Path | None = None) -> Path:
    p = (start or Path(__file__)).resolve()
    if p.is_file():
        p = p.parent
    for candidate in [p, *p.parents]:
        if (candidate / "SCR_II_PREREG_v001").is_dir() and (candidate / "generator").is_dir():
            return candidate
    raise RuntimeError("Could not locate scr_ii root containing SCR_II_PREREG_v001/")
