# Preservation and alignment report

- Input: the user-supplied `UNNS_MATH_FOUNDATIONS(1).zip` (SHA-256 `e1a204297ed30cbab1096dd0edaf5bd6894386edcdcb4814a31efe5941a222b4`), 437 files.
- Supplemental preservation: three distinct SELECT-II v002b files from the earlier user-uploaded `UNNS_MATH_FOUNDATIONS.zip` (not found in the latest ZIP).
- Output: **440 individual source files**, source-byte hashes unchanged, zero omitted source files.
- The complete latest upload is embedded verbatim as `archives/ORIGINAL_USER_UPLOAD.zip`.
- FIELD-I directory names are normalized to `v001`–`v012` without editing inner files, to restore predecessor launcher paths.
- SELECT-I and SELECT-II are preserved in full; neither branch was collapsed into another.
- Support material `UNNS_RELATIONAL_I` and `UNNS_ENTANGLE_I` is retained without exclusion, including the original PDFs, outputs and compiled files.
- Root-level indexes and integrity tooling are **new publication metadata**, not changes to the historical record.
- Paths were moved; use `SOURCE_MAP.tsv` to trace exact original names. Link targets have not yet acquired permanent GitHub commit identifiers.

Local verification: run `RUN_VERIFY.bat` or `python verify_sources.py`. It checks source file hashes, the embedded original archive, original archive-to-expanded mapping, supplement provenance in the map, expected source counts, and presence of FIELD-I predecessor paths. It does **not** run research scripts or update output.
