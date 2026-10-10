from __future__ import annotations
import gzip, hashlib, json, os, time
from pathlib import Path
from typing import Any

ENGINE_VERSION = "SCR_III_ENGINE_v001"
BENCHMARK = "ROUTE_CSP_C"
BENCHMARK_VERSION = "v001"
PREREG = "SCR_III_PREREG_v001"


def scr_iii_root() -> Path:
    return Path(__file__).resolve().parent


def project_root() -> Path:
    return scr_iii_root().parent


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
    raise RuntimeError(f"Could not replace {path}; recovery saved to {recovery}") from last


def write_json_gz(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(obj, f, sort_keys=True, separators=(",", ":"))


def read_json_gz(path: Path) -> Any:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def stable_int(*parts: object, bits: int = 63) -> int:
    raw = "|".join(str(x) for x in parts).encode("utf-8")
    value = int.from_bytes(hashlib.sha256(raw).digest()[:8], "big")
    return value & ((1 << bits) - 1)


def q_key(q: float) -> str:
    return f"{float(q):.1f}"


def sigma_key(sigma: float) -> str:
    return f"{float(sigma):.1f}"


def cell_id(depth: int, seed: int, sigma: float, q: float) -> str:
    return f"d{int(depth)}_s{int(seed)}_sig{float(sigma):.1f}_q{float(q):.1f}"
