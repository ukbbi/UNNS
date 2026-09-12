from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

TOOL_NAME = "JHTDB_HIGH_RE_SCALE"
TOOL_VERSION = "0.1.2"
REBUILD_VERSION = "0.1.2"

SOURCE_BUNDLE_REL = Path("outputs/records/HIGH_RE_SCALE_LADDERS.zip")
SOURCE_BUNDLE_SHA256 = "2f33fca62b35683272d0c4f822be36973475c085618b42f15d7d2efdd7462415"
OUTPUT_DIR_REL = Path("ladders/chamber_input/jhtdb_high_re")
OUTPUT_ZIP_REL = Path("outputs/records/HIGH_RE_CHAMBER_INPUTS.zip")
EXPECTED_OUTPUT_ZIP_SHA256 = "b82e157dea0184f4d68e4ed509adee6d4a53027551e345edfb0f68eff8926b2c"

PRIMARY = (
    "i8192_s00",
    "i8192_s01",
    "i8192_s02",
    "i8192_s03",
    "i8192_s04",
    "i32768_s00",
)
CONTRAST = ("i8192_s05",)
ALL_SAMPLES = PRIMARY + CONTRAST

CHAMBER_PROTOCOL = """# HIGH-RE CHAMBER EXECUTION PROTOCOL v0.1

Status: frozen before STRUC-I / STRUC-PERC-I high-Re chamber results are observed.

## Source identity

Source bundle: `HIGH_RE_SCALE_LADDERS.zip`

SHA-256:
`2f33fca62b35683272d0c4f822be36973475c085618b42f15d7d2efdd7462415`

All ladder files rebuilt here are byte-identical copies of the frozen `P_SCALE.csv`
populations. Files are renamed only so several samples can be selected conveniently
in the browser chamber interfaces.

No jitter, smoothing, normalization, rescaling, value editing, deduplication, or
multiplicity editing is applied by the rebuild step.

## STRUC-I v1.0.4

Primary group:
- i8192_s00
- i8192_s01
- i8192_s02
- i8192_s03
- i8192_s04
- i32768_s00

Contrast:
- i8192_s05

Run each ladder under the same chamber settings used for Pilot A:
- generic single-column numeric CSV
- kappa min = 0.01
- kappa max = 1.0
- kappa steps = 40
- Monte Carlo primary = 2000

For Pilot-A parity, preserve a 10,000-MC precision validation run with the same
settings. Do not change the ladder or kappa grid between primary and precision runs.

Interpret the chamber-defined regime/state. The preregistered high-Re endpoint is
based on recurrence versus shift of the Pilot-A `P_SCALE` STRUC-I regime, not on
tuning mean A_kappa.

## STRUC-PERC-I v2.5.0

Use the canonical generic adapter with no modification.

The frozen `P_SCALE` populations are intentionally quantized (3 or 4 distinct
values). The canonical generic adapter may therefore reduce them to a very
low-dimensional support. This is not an error and must not be repaired by jittering
or altering duplicate values.

STRUC-PERC-I is secondary/descriptive for this quantized coordinate. STRUC-I is the
cross-chamber regime test used for the registered recurrence/stabilization
interpretation.

## Decision discipline

Do not change:
- the `P_SCALE` population;
- duplicate multiplicities before STRUC-I;
- chamber kappa ranges/steps;
- MC counts after seeing a favorable or unfavorable outcome;
- STRUC-PERC-I's canonical generic adapter.
"""

README = """HIGH_RE_CHAMBER_INPUTS

Purpose
-------
Deterministically rebuilt, byte-identical chamber inputs for the seven frozen
high-Re P_SCALE ladders.

Source
------
outputs/records/HIGH_RE_SCALE_LADDERS.zip
SHA-256: 2f33fca62b35683272d0c4f822be36973475c085618b42f15d7d2efdd7462415

Folders
-------
STRUC_I_PRIMARY   Five isotropic8192 primary high-Re snapshots + isotropic32768.
STRUC_I_CONTRAST  Prespecified isotropic8192 low-Re contrast.
STRUC_PERC_BATCH  All seven uniquely named inputs for STRUC-PERC-I.
RECORDS           Frozen route/ladder provenance copied from the source bundle.
CHAMBER_PROTOCOL.md
INPUT_MANIFEST.json
REBUILD_RECORD.json

No scientific values are changed by this rebuild step.
"""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def project_root() -> Path:
    # .../project/tools/derive/JHTDB_HIGH_RE_SCALE_v0_1_2/this_script.py
    return Path(__file__).resolve().parents[3]


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def deterministic_zip(tree: Path, output_zip: Path) -> str:
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    tmp = output_zip.with_suffix(output_zip.suffix + ".tmp")
    if tmp.exists():
        tmp.unlink()

    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_STORED) as zf:
        for path in sorted(p for p in tree.rglob("*") if p.is_file()):
            rel = path.relative_to(tree).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = (0o100644 & 0xFFFF) << 16
            info.flag_bits = 0
            zf.writestr(info, path.read_bytes())

    tmp.replace(output_zip)
    return sha256_file(output_zip)


def main() -> int:
    root = project_root()
    source = root / SOURCE_BUNDLE_REL
    output_dir = root / OUTPUT_DIR_REL
    output_zip = root / OUTPUT_ZIP_REL

    print(f"{TOOL_NAME} {TOOL_VERSION} - deterministic chamber-input rebuild v{REBUILD_VERSION}")
    print(f"Project root: {root}")

    if not source.is_file():
        raise FileNotFoundError(f"missing frozen source bundle: {source}")

    source_sha = sha256_file(source)
    print(f"Source bundle SHA-256: {source_sha}")
    if source_sha != SOURCE_BUNDLE_SHA256:
        raise ValueError("HIGH_RE_SCALE_LADDERS.zip does not match the frozen source hash")

    with zipfile.ZipFile(source, "r") as zf:
        stage_report = json.loads(zf.read("HIGH_RE_SCALE_STAGE_REPORT.json"))
        stage_map = {x["sample"]["sample_id"]: x for x in stage_report["samples"]}
        if set(stage_map) != set(ALL_SAMPLES):
            raise ValueError("source bundle sample set differs from frozen seven-sample plan")

        # Use a fresh system-temporary staging directory on every run.
        # Do not reuse/delete a project-local staging directory: on Windows,
        # Explorer, antivirus, or sync software may hold a directory handle and
        # cause WinError 5 even when file contents are otherwise writable.
        staging = Path(tempfile.mkdtemp(prefix="unns_high_re_chamber_"))

        records = staging / "RECORDS"
        manifest_samples = []
        output_hashes = {}

        for sid in ALL_SAMPLES:
            src_name = f"{sid}/P_SCALE.csv"
            rec_name = f"{sid}/P_SCALE_RECORD.json"
            data = zf.read(src_name)
            expected = stage_map[sid]["P_SCALE"]["sha256"]
            actual = sha256_bytes(data)
            if actual != expected:
                raise ValueError(f"P_SCALE hash mismatch for {sid}: {actual} != {expected}")

            renamed = f"{sid}_P_SCALE.csv"
            targets = []
            if sid in PRIMARY:
                targets.append(staging / "STRUC_I_PRIMARY" / renamed)
            else:
                targets.append(staging / "STRUC_I_CONTRAST" / renamed)
            targets.append(staging / "STRUC_PERC_BATCH" / renamed)

            for target in targets:
                write_bytes(target, data)
                rel = target.relative_to(staging).as_posix()
                output_hashes[rel] = actual

            rec_data = zf.read(rec_name)
            rec_target = records / f"{sid}_P_SCALE_RECORD.json"
            write_bytes(rec_target, rec_data)
            output_hashes[rec_target.relative_to(staging).as_posix()] = sha256_bytes(rec_data)

            manifest_samples.append({
                "sample_id": sid,
                "role": stage_map[sid]["sample"]["role"],
                "source_entry": src_name,
                "source_p_scale_sha256": expected,
                "count": stage_map[sid]["P_SCALE"]["count"],
                "distinct_values": stage_map[sid]["P_SCALE"]["distinct_values"],
                "struc_i_group": "PRIMARY" if sid in PRIMARY else "CONTRAST",
            })

        for name in ("HIGH_RE_SCALE_STAGE_REPORT.json", "HIGH_RE_SCALE_SUMMARY.csv"):
            data = zf.read(name)
            target = records / name
            write_bytes(target, data)
            output_hashes[target.relative_to(staging).as_posix()] = sha256_bytes(data)

        input_manifest = {
            "schema": "UNNS_HIGH_RE_CHAMBER_INPUT_MANIFEST_v0.1",
            "source_bundle": SOURCE_BUNDLE_REL.as_posix(),
            "source_bundle_sha256": SOURCE_BUNDLE_SHA256,
            "scientific_transform": "NONE",
            "copy_policy": "byte-identical P_SCALE.csv copies; filename-only renaming",
            "primary_samples": list(PRIMARY),
            "contrast_samples": list(CONTRAST),
            "samples": manifest_samples,
        }
        write_text(staging / "INPUT_MANIFEST.json", json.dumps(input_manifest, indent=2, sort_keys=True) + "\n")
        write_text(staging / "CHAMBER_PROTOCOL.md", CHAMBER_PROTOCOL)
        write_text(staging / "README.txt", README)

        # Hash generated metadata before writing the final deterministic rebuild record.
        for name in ("INPUT_MANIFEST.json", "CHAMBER_PROTOCOL.md", "README.txt"):
            p = staging / name
            output_hashes[name] = sha256_file(p)

        rebuild_record = {
            "schema": "UNNS_HIGH_RE_CHAMBER_REBUILD_RECORD_v0.1",
            "status": "REBUILT_AND_VERIFIED",
            "tool": {"name": TOOL_NAME, "version": TOOL_VERSION, "rebuild_version": REBUILD_VERSION},
            "source_bundle": SOURCE_BUNDLE_REL.as_posix(),
            "source_bundle_sha256": source_sha,
            "output_directory": OUTPUT_DIR_REL.as_posix(),
            "output_archive": OUTPUT_ZIP_REL.as_posix(),
            "scientific_transform": "NONE",
            "determinism": {
                "archive_entry_order": "lexicographic POSIX relative path",
                "archive_compression": "ZIP_STORED",
                "archive_timestamp": "1980-01-01T00:00:00",
                "archive_file_mode": "100644",
                "json_keys": "sorted where generated by this rebuild script",
                "text_newlines": "LF",
            },
            "samples": manifest_samples,
            "output_file_sha256": dict(sorted(output_hashes.items())),
        }
        write_text(staging / "REBUILD_RECORD.json", json.dumps(rebuild_record, indent=2, sort_keys=True) + "\n")

        # Build and verify the deterministic archive FROM STAGING first.
        # This avoids deleting the existing chamber-input directory, which can be
        # held open by Windows Explorer / sync software even when its files are writable.
        archive_sha = deterministic_zip(staging, output_zip)
        print(f"Rebuilt archive SHA-256: {archive_sha}")
        if archive_sha != EXPECTED_OUTPUT_ZIP_SHA256:
            raise ValueError(
                "deterministic rebuilt archive hash differs from the registered expected hash: "
                f"{archive_sha} != {EXPECTED_OUTPUT_ZIP_SHA256}"
            )

        # Non-destructive in-place synchronization of the known rebuilt files.
        # Existing directories are retained; expected files are overwritten byte-for-byte.
        output_dir.mkdir(parents=True, exist_ok=True)
        expected_relpaths = []
        for p in sorted(x for x in staging.rglob("*") if x.is_file()):
            rel = p.relative_to(staging)
            expected_relpaths.append(rel.as_posix())
            dest = output_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, dest)

        # Verify the synchronized files exactly match staging.
        for rel in expected_relpaths:
            a = staging / Path(rel)
            b = output_dir / Path(rel)
            if sha256_file(a) != sha256_file(b):
                raise ValueError(f"post-sync hash mismatch: {rel}")

        # Extra pre-existing files do not enter the deterministic archive.
        present = {
            p.relative_to(output_dir).as_posix()
            for p in output_dir.rglob("*") if p.is_file()
        }
        extras = sorted(present - set(expected_relpaths))
        if extras:
            print(f"NOTE: {len(extras)} pre-existing extra file(s) remain in chamber_input;")
            print("      they are excluded from the deterministic rebuilt archive.")

        shutil.rmtree(staging, ignore_errors=True)

    print("[PASS] Seven frozen P_SCALE ladders rebuilt for STRUC-I / STRUC-PERC-I with no scientific transformation.")
    print(f"Folder:  {output_dir}")
    print(f"Archive: {output_zip}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        raise
