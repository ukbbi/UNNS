#!/usr/bin/env python3
"""Verify preserved UNNS source files without requiring a duplicate ZIP archive.

Checks the 440 source files directly against their original SHA-256 ledger
and source map. Does not edit any project file or run scientific experiments.

Line endings: the original hashes were taken on the author's files. Text files are
stored with LF endings on GitHub, and a checkout may convert them (git autocrlf).
NEWLINE_LEDGER.tsv records, for each file, the newline form of the ORIGINAL bytes
(lf, crlf or binary). A file passes if its hash matches either exactly, or after
converting ONLY its line endings to the recorded original form. Binary files are
never normalised; any other difference fails.
"""

import csv
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
EXPECTED_COUNTS = {
    "SELECT-I": 8,
    "SELECT-II": 14,
    "FIELD-I": 152,
    "UNNS_RELATIONAL_I": 44,
    "UNNS_ENTANGLE_I": 222,
}
EXPECTED_TOTAL = sum(EXPECTED_COUNTS.values())


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalized_digest(path, form):
    """SHA-256 after converting only line endings to the recorded original form."""
    data = path.read_bytes()
    if form == "lf":
        data = data.replace(b"\r\n", b"\n")
    elif form == "crlf":
        data = re.sub(rb"\r?\n", b"\r\n", data)
    else:
        raise VerificationError(f"No newline normalisation allowed for form {form!r}")
    return hashlib.sha256(data).hexdigest()


def safe_source_path(raw):
    parts = PurePosixPath(raw).parts
    require(raw.startswith("sources/") and len(parts) >= 3,
            f"Invalid source path: {raw}")
    require(".." not in parts and "\\" not in raw and not raw.startswith("/"),
            f"Unsafe source path: {raw}")
    return ROOT.joinpath(*parts)


def verify():
    map_file = ROOT / "SOURCE_MAP.tsv"
    ledger_file = ROOT / "SHA256_SOURCES.sha256"
    require(map_file.is_file(), "Missing SOURCE_MAP.tsv")
    require(ledger_file.is_file(), "Missing SHA256_SOURCES.sha256")

    with map_file.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required = {"original_path_in_source_zip", "repository_path", "sha256", "provenance"}
        require(required.issubset(set(reader.fieldnames or [])),
                "SOURCE_MAP.tsv has missing columns")
        rows = list(reader)
    require(len(rows) == EXPECTED_TOTAL,
            f"SOURCE_MAP.tsv: expected {EXPECTED_TOTAL} files, found {len(rows)}")

    paths = [r["repository_path"] for r in rows]
    require(len(set(paths)) == EXPECTED_TOTAL, "Duplicate paths in SOURCE_MAP.tsv")
    counts = Counter(PurePosixPath(path).parts[1] for path in paths)
    require(counts == EXPECTED_COUNTS,
            f"Unexpected collection totals: {dict(counts)}")
    provenance = Counter(r["provenance"] for r in rows)
    require(provenance == {"user-current-upload": 437, "earlier-user-source-archive": 3},
            f"Unexpected provenance counts: {dict(provenance)}")

    supplement = {PurePosixPath(r["repository_path"]).name for r in rows
                  if r["provenance"] == "earlier-user-source-archive"}
    require(supplement == {"select2b.py", "SELECT2B_note.md", "select2b_output.txt"},
            "Expected separate SELECT-II v002b materials are missing")

    with ledger_file.open(encoding="utf-8-sig") as handle:
        ledger = handle.read().splitlines()
    require(len(ledger) == EXPECTED_TOTAL,
            f"SHA256 ledger: expected {EXPECTED_TOTAL} entries, found {len(ledger)}")

    nl_file = ROOT / "NEWLINE_LEDGER.tsv"
    require(nl_file.is_file(), "Missing NEWLINE_LEDGER.tsv")
    with nl_file.open(encoding="utf-8", newline="") as handle:
        nl_reader = csv.DictReader(handle, delimiter="\t")
        require(set(nl_reader.fieldnames or []) == {"repository_path", "original_newline_form", "sha256_of_original_bytes"},
                "NEWLINE_LEDGER.tsv has unexpected columns")
        nl_rows = list(nl_reader)
    require(len(nl_rows) == EXPECTED_TOTAL, "NEWLINE_LEDGER.tsv: wrong number of entries")
    nl = {r["repository_path"]: r for r in nl_rows}
    require(set(nl) == set(paths), "NEWLINE_LEDGER.tsv paths differ from SOURCE_MAP.tsv")
    n_exact = n_norm = 0

    for idx, (row, entry) in enumerate(zip(rows, ledger), 1):
        relative = row["repository_path"]
        expected_sha = row["sha256"].lower()
        require(re.fullmatch(r"[0-9a-f]{64}", expected_sha) is not None,
                f"Invalid SHA-256 at SOURCE_MAP.tsv entry {idx}")
        require(entry == f"{expected_sha}  {relative}",
                f"Hash ledger and source map disagree: {relative}")
        path = safe_source_path(relative)
        require(path.is_file(), f"Missing source file: {relative}")
        form = nl[relative]["original_newline_form"]
        require(form in ("lf", "crlf", "binary"), f"Bad newline form for {relative}: {form}")
        require(nl[relative]["sha256_of_original_bytes"].lower() == expected_sha,
                f"NEWLINE_LEDGER hash differs from source map: {relative}")
        if digest(path) == expected_sha:
            n_exact += 1
        else:
            require(form != "binary", f"SHA-256 mismatch (binary file, no normalisation allowed): {relative}")
            require(normalized_digest(path, form) == expected_sha, f"SHA-256 mismatch: {relative}")
            n_norm += 1

    # Check that the original FIELD-I launchers still point to existing releases.
    field_root = ROOT / "sources" / "FIELD-I"
    for i in range(2, 13):
        require((field_root / f"v{i:03d}" / f"field{i}.py").is_file(),
                f"Missing FIELD-I release v{i:03d}")
    for launcher in field_root.rglob("RUN_TESTS.bat"):
        text = launcher.read_text(encoding="utf-8", errors="replace")
        for version in re.findall(r"\.\.\\v(\d{3})\\field\d+\.py", text, flags=re.I):
            require((launcher.parent.parent / f"v{version}").is_dir(),
                    f"Broken predecessor directory in {launcher.relative_to(ROOT)}")

    print(f"Files checked: {EXPECTED_TOTAL}")
    print("SELECT-I: 8; SELECT-II: 14 (v002 and distinct v002b)")
    print("FIELD-I: 152; UNNS_RELATIONAL_I: 44; UNNS_ENTANGLE_I: 222")
    print("Current upload: 437 files; restored historical complement: 3 files")
    print(f"Source SHA-256 verified: {n_exact} byte-exact, {n_norm} after documented newline normalisation only")
    print("FIELD-I predecessor paths verified")
    print("ZIP archive: not required")
    print("Integrity/path errors: 0")
    print("PASS")


if __name__ == "__main__":
    try:
        verify()
    except (VerificationError, OSError, ValueError, csv.Error) as exc:
        print("FAIL:", exc)
        sys.exit(1)
