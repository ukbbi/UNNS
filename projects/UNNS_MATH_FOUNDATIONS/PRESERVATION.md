# Preservation and alignment report

- Input: the user-supplied `UNNS_MATH_FOUNDATIONS(1).zip` (SHA-256 `e1a204297ed30cbab1096dd0edaf5bd6894386edcdcb4814a31efe5941a222b4`), 437 files.
- Supplemental preservation: three distinct SELECT-II v002b files from the earlier user-uploaded `UNNS_MATH_FOUNDATIONS.zip` (not found in the latest ZIP).
- Output: **440 individual source files**, content unchanged, zero omitted source files. Original SHA-256 hashes are reproduced byte-for-byte for 401 files and, for 39 text files, after restoring original CRLF line endings (GitHub stores text with LF; see `NEWLINE_LEDGER.tsv`).
- The original upload ZIP is **not included** in this repository; its hash is kept in `SHA256_ARCHIVES.sha256` as a historical record only.
- FIELD-I directory names are normalized to `v001`–`v012` without editing inner files, to restore predecessor launcher paths.
- SELECT-I and SELECT-II are preserved in full; neither branch was collapsed into another.
- Support material `UNNS_RELATIONAL_I` and `UNNS_ENTANGLE_I` is retained without exclusion, including the original PDFs, outputs and compiled files.
- Root-level indexes and integrity tooling are **new publication metadata**, not changes to the historical record.
- Paths were moved; use `SOURCE_MAP.tsv` to trace exact original names. Reference Collection v001 is GitHub commit `bb8b12d753c600c597feb00df17fe139c7cc65fa`; later documentation revisions are separate commits (see `REVISIONS.md`).

Local verification: run `RUN_VERIFY.bat` or `python verify_sources.py`. It checks source file hashes (byte-exact, or after documented newline normalisation only, as recorded in `NEWLINE_LEDGER.tsv`), the source map and ledgers, supplement provenance in the map, expected source counts, and presence of FIELD-I predecessor paths. No ZIP archive is required. It does **not** run research scripts or update output.
