from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

REPO = "ukbbi/UNNS"
COMMIT = "aa17dbc9c48f8da6daf51b0547b060558c175e7d"
SOURCES = [
    {
        "role": "P4 generator/gates/viability source",
        "path": "canonical/chamber_liii_phase_P₄/chamber_liii_v3_1_0_modular.html",
        "git_blob_sha": "52607c8e3b078084906b352d934d037c3aad9dd3",
        "local_name": "chamber_liii_v3_1_0_modular.html",
    },
    {
        "role": "Axis V methodology",
        "path": "canonical/axis_v_admissibility_gate/axis_v_methodology_guide.md",
        "git_blob_sha": "53df9d3cd73b924a3b48742ae7ad0b35cb1f3232",
        "local_name": "axis_v_methodology_guide.md",
    },
    {
        "role": "Axis V validation supplement",
        "path": "canonical/axis_v_admissibility_gate/axis_v_technical_supplement.md",
        "git_blob_sha": "8dcab608ff49da8d4b3349c81c48ec8af81d1d45",
        "local_name": "axis_v_technical_supplement.md",
    },
]


def blob(data: bytes) -> str:
    """Return the canonical Git blob SHA-1 for *data*.

    Git hashes a blob as: b"blob " + decimal_length + b"\\0" + data.
    The v002-prep v001 build accidentally used the two printable bytes "\\0"
    instead of a NUL byte. That made every otherwise-correct pinned source fail
    verification. This implementation uses the canonical NUL separator.
    """
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def roots(project: Path) -> list[Path]:
    out: list[Path] = []
    env = os.environ.get("UNNS_REPO")
    if env:
        out.append(Path(env))
    p = project
    for _ in range(7):
        out.append(p)
        if p.parent == p:
            break
        p = p.parent
    # Stable de-duplication.
    seen: set[str] = set()
    unique: list[Path] = []
    for r in out:
        try:
            key = str(r.resolve())
        except Exception:
            key = str(r)
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


def install(project: Path, allow_download: bool = True) -> dict:
    d = project / "references" / "source_lock"
    d.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    all_ok = True

    for s in SOURCES:
        target = d / s["local_name"]
        data = target.read_bytes() if target.is_file() else None
        origin = "existing"

        if data is None or blob(data) != s["git_blob_sha"]:
            data = None
            rel = Path(*s["path"].split("/"))
            for r in roots(project):
                p = r / rel
                if p.is_file():
                    candidate = p.read_bytes()
                    if blob(candidate) == s["git_blob_sha"]:
                        data = candidate
                        origin = "local_repo"
                        break

        download_error = None
        if data is None and allow_download:
            try:
                url = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/{quote(s['path'], safe='/')}"
                with urlopen(Request(url, headers={"User-Agent": "SCR-I-v003"}), timeout=60) as resp:
                    data = resp.read()
                    origin = "pinned_download"
            except Exception as exc:
                download_error = str(exc)

        actual = blob(data) if data is not None else None
        good = data is not None and actual == s["git_blob_sha"]
        if good:
            target.write_bytes(data)

        row = {
            **s,
            "ok": good,
            "origin": origin if data is not None else "not_found",
            "actual_git_blob_sha": actual,
            "local_path": str(target),
        }
        if download_error:
            row["error"] = download_error
        elif data is not None and not good:
            row["error"] = "git blob SHA mismatch"
        elif data is None:
            row["error"] = "source not found"
        rows.append(row)
        all_ok = all_ok and good

    rec = {"repository": REPO, "commit": COMMIT, "ok": all_ok, "sources": rows}
    (d / "SOURCE_HASHES_v003.json").write_text(
        json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return rec


def verify(project: Path) -> dict:
    return install(project, allow_download=False)
