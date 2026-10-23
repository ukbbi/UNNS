# Reference baseline and preservation scope

**Edition:** Complete Reference Collection v001 (23 October 2026).  
**Mathematical theorem baseline:** FIELD-I v012, with T69–T73.  
**Purpose:** frozen reference for a coordinated, separately authored Volume I (generative reachability) and Volume II (collective dynamics).

| Program | Source of record | State |
|---|---|---|
| SELECT-I | `sources/SELECT-I/` | Retains frozen source and outputs |
| SELECT-II (base) | `sources/SELECT-II/` | Retains base reachability source and outputs |
| SELECT-II v002 snapshot | `sources/SELECT-II/v002/` | Earlier snapshot, unchanged |
| SELECT-II v002b | `sources/SELECT-II/v002b/` | Distinct continued reachability/history tests, recovered from earlier archive |
| FIELD-I base | `sources/FIELD-I/` | Preserves original program data and reports |
| FIELD-I v001–v012 | `sources/FIELD-I/v001/` … `v012/` | Full historical releases, including scripts, output, manifests, errata |
| UNNS_RELATIONAL_I | `sources/UNNS_RELATIONAL_I/` | Supporting references; no automatic theorem promotion |
| UNNS_ENTANGLE_I | `sources/UNNS_ENTANGLE_I/` | Supporting references; no automatic theorem promotion |

**Every one of the 437 files in the latest upload is included without byte changes.** The three recovered v002b files are additional and explicitly recorded. There are 440 preserved source files total.

File paths for FIELD-I directories were normalized from variants `FIELD-I v00x` / `FIELD-I_v00x` to `v00x` in order to restore references such as `..\v010\field10.py` in the Windows launchers; *no* original research text was edited. Source-to-destination mapping, original paths and hashes are in `SOURCE_MAP.tsv`.

The separate manuscript drafts are **not** stored here. All proofs remain subject to outside mathematical review. Scientific status labels in source records (PROVED / DATA / OPEN / FALSIFIED or ERRATUM) must be preserved in citation and synthesis.
