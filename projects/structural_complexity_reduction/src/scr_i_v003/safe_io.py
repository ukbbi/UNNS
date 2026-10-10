from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

_LOCK_ERRORS = {5, 32, 33}  # access denied, sharing violation, lock violation


def _is_transient_lock(exc: BaseException) -> bool:
    if isinstance(exc, PermissionError):
        return True
    winerror = getattr(exc, "winerror", None)
    return winerror in _LOCK_ERRORS


def _write_tmp(path: Path, payload: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{time.time_ns()}.tmp")
    with tmp.open("x", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)
        fh.flush()
        os.fsync(fh.fileno())
    return tmp


def safe_dump(path: Path | str, obj: Any, *, retries: int = 80, base_delay: float = 0.05) -> None:
    """Windows-safe JSON checkpoint writer.

    The v003 primary runner is often used from folders watched by sync/indexing/AV
    software. Such software can briefly hold the destination checkpoint open,
    causing os.replace/Path.replace to raise WinError 5 or 32.

    This implementation preserves atomic replacement semantics but retries the
    replace long enough for a transient lock to clear. If the destination stays
    locked, it writes a recovery copy and stops rather than silently continuing
    with a stale checkpoint.
    """
    p = Path(path)
    payload = json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, default=str) + "\n"
    tmp = _write_tmp(p, payload)

    last_exc: BaseException | None = None
    try:
        for attempt in range(1, retries + 1):
            try:
                os.replace(tmp, p)
                return
            except OSError as exc:
                last_exc = exc
                if not _is_transient_lock(exc):
                    raise
                if attempt in {5, 20, 40, 60}:
                    print(
                        f"[SCR-I v003] checkpoint/output file temporarily locked: {p.name}; "
                        f"retry {attempt}/{retries}",
                        flush=True,
                    )
                time.sleep(min(0.75, base_delay * (1.0 + attempt / 8.0)))

        recovery = p.with_name(f"{p.name}.recovery.{time.time_ns()}.json")
        # Do not rename: a rename can hit the same lock. Create an independent copy.
        with recovery.open("x", encoding="utf-8", newline="\n") as fh:
            fh.write(payload)
            fh.flush()
            os.fsync(fh.fileno())
        raise RuntimeError(
            f"Could not replace {p} after {retries} retries because Windows kept the "
            f"destination locked. A complete recovery checkpoint was written to {recovery}. "
            "Close/suspend the process locking the checkpoint and rerun; completed cells remain recoverable."
        ) from last_exc
    finally:
        try:
            if tmp.exists():
                tmp.unlink()
        except OSError:
            pass
