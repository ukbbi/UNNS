# UNNS Mathematical Foundations — Complete Reference Collection

**Purpose:** A stable, complete GitHub reference base for *The Mathematical Foundations of the UNNS Substrate*, Volumes I and II. This is **not** the manuscript-writing workspace and **not** a new experimental-development branch.

**Baseline:** FIELD-I v012 (23 October 2026); the existing SELECT results and supporting research records retain their original status. No research source file has been edited or discarded.

## Reference directories

| Source | GitHub path | Preserved files | Coverage |
|---|---|---:|---|
| SELECT-I | [`sources/SELECT-I/`](sources/SELECT-I/) | 8 | Freeze note, program, outputs, manifest, replay, launcher |
| SELECT-II | [`sources/SELECT-II/`](sources/SELECT-II/) | 14 | Original development plus **both** distinct v002 branches |
| FIELD-I | [`sources/FIELD-I/`](sources/FIELD-I/) | 152 | Complete base and releases `v001`–`v012`, including code, proofs, logs, manifests and launchers |
| UNNS_RELATIONAL_I | [`sources/UNNS_RELATIONAL_I/`](sources/UNNS_RELATIONAL_I/) | 44 | Supporting research and manuscript source records |
| UNNS_ENTANGLE_I | [`sources/UNNS_ENTANGLE_I/`](sources/UNNS_ENTANGLE_I/) | 222 | Supporting exploratory research and recorded tests |
| **Total** | [`sources/`](sources/) | **440** | All source files retained: 401 byte-identical to the original files; 39 text files stored with LF line endings (see [`NEWLINE_LEDGER.tsv`](NEWLINE_LEDGER.tsv)) |

**Important SELECT-II distinction:** [`sources/SELECT-II/v002/`](sources/SELECT-II/v002/) is the earlier `select2.py` snapshot; [`sources/SELECT-II/v002b/`](sources/SELECT-II/v002b/) contains the separate `select2b.py` extension and its note/output. These three v002b files were present in the user's earlier source archive but absent from the latest 437-file upload. Both are preserved, **not silently merged or substituted**.

## Quick mathematical reference links

- [SELECT-I: freeze and nonselection record](sources/SELECT-I/FREEZE.md)
- [SELECT-II: research results](sources/SELECT-II/RESULTS.md) and [v002 note](sources/SELECT-II/v002/SELECT2_note.md)
- [SELECT-II: v002b complete histories and no-shortcut results](sources/SELECT-II/v002b/SELECT2B_note.md)
- [FIELD-I v002: grammar and theorems](sources/FIELD-I/v002/THEOREMS.md)
- [FIELD-I v009: eventual scaling and event dynamics](sources/FIELD-I/v009/THEOREMS.md)
- [FIELD-I v010: prime-carry exclusion](sources/FIELD-I/v010/THEOREMS.md)
- [FIELD-I v011: static survivor selection and certificates](sources/FIELD-I/v011/THEOREMS.md)
- [FIELD-I v012: transient bounds and T73 correction](sources/FIELD-I/v012/THEOREMS.md)

For complete background, see [REFERENCE_INDEX.md](REFERENCE_INDEX.md), [BASELINE.md](BASELINE.md) and [CORRECTIONS.md](CORRECTIONS.md).

## Preservation and audit

- **440 individual source files** have unchanged content. Their original SHA-256 hashes are reproduced exactly for 401 files, and for 39 text files after restoring the original CRLF line endings (GitHub stores text with LF; see [`NEWLINE_LEDGER.tsv`](NEWLINE_LEDGER.tsv)). Only the parent directory paths are normalized for clean internal navigation and working version-relative paths.
- The original **437-file upload ZIP** (SHA-256 `e1a204297ed30cbab1096dd0edaf5bd6894386edcdcb4814a31efe5941a222b4`) is **not included** in this repository; its hash is kept in [`SHA256_ARCHIVES.sha256`](SHA256_ARCHIVES.sha256) as a historical record only.
- The three recovered historical files are explicitly identified in [`SOURCE_MAP.tsv`](SOURCE_MAP.tsv).
- [`SHA256_SOURCES.sha256`](SHA256_SOURCES.sha256) checks each research file; [`NEWLINE_LEDGER.tsv`](NEWLINE_LEDGER.tsv) records the newline form of each original file so that the check is independent of the git line-ending setting.
- [`RUN_VERIFY.bat`](RUN_VERIFY.bat) performs a **read-only integrity/path check**. It does *not* run or modify research experiments.

Existing research launchers inside `sources/` are retained *as historical research evidence*. This repository copy is for mathematical references, not for ongoing computations. If you choose to run a historical script, do so in a separate working copy because its output may overwrite recorded files.

## Citation policy

Cite exact GitHub commit URLs, not an unfrozen `main` branch. Reference Collection v001 is commit `bb8b12d753c600c597feb00df17fe139c7cc65fa`. See [CITATION.md](CITATION.md). All mathematical conclusions are model-specific; the SELECT-II successor graph and FIELD-I collective map are **explicitly chosen rules**, not uniquely forced by original nest arithmetic. Existing errata take precedence over superseded interpretations.
