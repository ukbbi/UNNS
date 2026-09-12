JHTDB_HIGH_RE_SCALE v0.1.2 — WINDOWS PATH-LENGTH FIX

This is a transport-only bug fix over v0.1.1.

Observed failure:
  STRUC-ROUTE-I completed the 100-null ensemble for i8192_s00, then pandas/pyarrow
  failed to write NODES.parquet because the full Windows path was exactly 260
  characters (legacy MAX_PATH boundary).

Fix:
  ROUTE-I run output root shortened from
    outputs/exports/struc_route_i/jhtdb_high_re/<sample_id>
  to
    outputs/r/hr/<sample_id>

No scientific change:
  - same seven frozen HDF5 sources
  - same source hashes and archive identity
  - same scale factors [1,2,4,8,16]
  - same Q threshold 1.5*RMS(Q)
  - same 26-connectivity and object rules
  - same relation eligibility
  - same canonical STRUC-ROUTE-I v0.1.2 code hashes
  - same 100-null ensemble, seed, and swaps
  - no retuning after field inspection

The incomplete v0.1.1 output directory may remain as provenance. Do not use it as a result.
Run RUN_ROUTE_AND_EXTRACT_WINDOWS.bat from this v0_1_2 folder. The existing v0.1.1
virtual environment is intentionally reused because dependencies are unchanged.

JHTDB_HIGH_RE_SCALE v0.1.1

BUGFIX: source-integrity verification now correctly treats the already SHA-256-locked HIGH_RE_EXPORT.tar as the primary source identity and cross-checks extracted HDF5 files against EXPORT_MANIFEST.json contained in that exact archive. The duplicated per-file hashes in config/high_re.json are retained for audit but are not an independent rejection gate. This changes no source, sample, coordinate, threshold, scale factor, adapter, chamber, or scientific criterion.

JHTDB HIGH-RE SCALE STAGE v0.1.0
================================

PURPOSE
-------
Process the seven preregistered high-Re HDF5 samples already acquired from
SciServer into scale-only structural route projects, run the canonical
STRUC-ROUTE-I v0.1.2 null ensemble for each sample, and extract one frozen
P_SCALE ladder per sample for later STRUC-I and STRUC-PERC-I interrogation.

THIS STAGE DOES NOT
-------------------
- treat the six isotropic8192 snapshots as a time series;
- create time edges;
- compute or interpret D_STITCH;
- run STRUC-I or STRUC-PERC-I;
- move the frozen cube or tune thresholds.

SOURCE LOCATION
---------------
Expected project location:

  data\raw\jhtdb\high_re\
      HIGH_RE_EXPORT.tar
      HIGH_RE_EXPORT.tar.sha256
      HIGH_RE_EXPORT\
          EXPORT_MANIFEST.json
          isotropic8192\...
          isotropic32768\...

The archive SHA-256 is frozen as:

  bbda6ab3fe3b22679a0bccdaad4287cca7f0f0f06e28caa1f9692d92298c105f

CANONICAL GRAMMAR REUSE
-----------------------
The stage imports, without modifying, the Pilot-A physical adapter modules from:

  tools\derive\JHTDB_ROUTE_ADAPTER_v0_1_0\jhtdb_adapter\

and the canonical routing engine from:

  chambers\STRUC_ROUTE_I_v0_1_2\struc_route\

Frozen spatial grammar:
  block factors        [1,2,4,8,16]
  block method         exact non-overlapping block mean
  boundary margin      16 native cells
  segmentation         Q >= 1.5 * RMS(Q)
  connectivity         26
  min native voxels    64
  min coarse voxels    2
  relation candidate   positive overlap only
  eligibility          overlap_src>=0.10 OR overlap_dst>=0.10 OR IoU>=0.05
  confidence           overlap_src

RUN
---
Recommended staged workflow:

  1. VERIFY_SOURCE_WINDOWS.bat
  2. RUN_ADAPTER_WINDOWS.bat
  3. RUN_ROUTE_AND_EXTRACT_WINDOWS.bat

Or run everything in sequence with:

  RUN_ALL_WINDOWS.bat

The launchers create/reuse a short-path environment at:

  %LOCALAPPDATA%\UNNS\JHTDB_HIGH_RE_SCALE_v010

OUTPUTS
-------
Per sample route input:

  ladders\native\jhtdb_high_re\<sample_id>\route_project\
      manifest.json
      objects.parquet
      relations.parquet
      ADAPTER_REPORT.json
      PHYS_STATS.csv

Canonical P_SCALE ladder:

  ladders\route_i\jhtdb_high_re\<sample_id>\P_SCALE.csv

Byte-identical chamber-facing copies:

  ladders\struc_i\jhtdb_high_re\<sample_id>\P_SCALE.csv
  ladders\struc_perc_i\jhtdb_high_re\<sample_id>\P_SCALE.csv

Aggregate records:

  outputs\records\HIGH_RE_ADAPTER_REPORT.json
  outputs\records\HIGH_RE_SCALE_STAGE_REPORT.json
  outputs\records\HIGH_RE_SCALE_LADDERS.zip
  outputs\tables\high_re_scale\HIGH_RE_SCALE_SUMMARY.csv

IMPORTANT
---------
The canonical STRUC-ROUTE-I global verdict will normally be UNDERRESOLVED for
this branch because only the scale axis is intentionally supplied. That global
verdict is not the branch endpoint. The preregistered quantities used here are
scale persistence, its matched null, null mobility, branching/merging, and the
extracted P_SCALE ladder.

CHAMBER INPUT REPLICATION
-------------------------
After HIGH_RE_SCALE_LADDERS.zip has been produced, chamber-facing inputs can be
rebuilt deterministically from that frozen bundle with:

  REBUILD_CHAMBER_INPUTS_WINDOWS.bat

or:

  python REBUILD_CHAMBER_INPUTS.py

The rebuild verifies the frozen source bundle SHA-256 and every P_SCALE.csv hash,
then creates:

  ladders\chamber_input\jhtdb_high_re\
  outputs\records\HIGH_RE_CHAMBER_INPUTS.zip

No scientific values are changed. P_SCALE files are copied byte-for-byte and only
renamed for browser-chamber convenience.

The output ZIP is deterministic: sorted paths, ZIP_STORED, fixed 1980-01-01
timestamps, and fixed file modes. Expected rebuilt archive SHA-256:

  3864a027b70f87ef541706ba4965a7cb1b2dab89b22dbca4a91b653340334f4f

Frozen replication record:

  analysis\generalization\jhtdb_high_re\CHAMBER_INPUT_REPLICATION.json


REBUILD v0.1.1 WINDOWS FIX
--------------------------
v0.1.0 attempted to delete the existing `ladders\chamber_input\jhtdb_high_re`
directory before replacement. On Windows this can fail with WinError 5 when
Explorer or another process holds a directory handle (observed on `RECORDS`).

v0.1.1 is non-destructive:
- constructs the full rebuild in a staging directory;
- creates and verifies the deterministic archive from staging;
- overwrites only the expected chamber-input files byte-for-byte;
- does not delete the existing chamber-input directory;
- verifies every synchronized file against staging;
- strictly enforces the deterministic archive SHA-256.

Expected deterministic rebuilt archive SHA-256 (v0.1.1):
  3864a027b70f87ef541706ba4965a7cb1b2dab89b22dbca4a91b653340334f4f

Scientific inputs and chamber protocol are unchanged.


REBUILD v0.1.2 WINDOWS STAGING FIX
----------------------------------
A second Windows-specific failure was observed when a previously used project-local
staging directory (`jhtdb_high_re.rebuild_tmp`) was itself held open by Explorer or
another process, causing WinError 5 before the rebuild began.

v0.1.2 removes project-local staging entirely:
- every run creates a fresh staging directory under the system temporary directory;
- no existing staging directory is deleted at startup;
- deterministic ZIP construction is still performed from the complete staging tree;
- output files are synchronized non-destructively into the chamber-input directory;
- temporary cleanup is best-effort and cannot invalidate a successful rebuild.

Scientific inputs, sample membership, ladder bytes, and chamber protocol are unchanged.

Expected deterministic rebuilt archive SHA-256 (v0.1.2):
  b82e157dea0184f4d68e4ed509adee6d4a53027551e345edfb0f68eff8926b2c
