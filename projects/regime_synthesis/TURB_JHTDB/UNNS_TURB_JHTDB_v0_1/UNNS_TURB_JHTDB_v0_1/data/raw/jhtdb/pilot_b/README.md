# Pilot B JHTDB Source — Data Provenance and Acquisition

## Purpose

This directory contains the frozen **Pilot B** source used for replication in the UNNS Turbulence — Johns Hopkins Turbulence Database project.

The source was acquired directly from the **Johns Hopkins Turbulence Database (JHTDB)** after the Pilot B extraction coordinates, time window, dataset, field, and acquisition geometry had been preregistered and locked.

No Pilot B source data were inspected before the selection was frozen.

---

## Source

**Provider:** Johns Hopkins Turbulence Database (JHTDB)  
**Dataset:** `isotropic1024coarse`  
**Field:** velocity  
**Acquisition method:** authenticated JHTDB `getCutout` queries  
**Access:** registered JHTDB token issued by Johns Hopkins personnel

The registered token was supplied only to the local acquisition process through the `JHTDB_TOKEN` environment variable. The token is not stored in this directory or in the project records.

---

## Frozen Pilot B Selection

The acquisition package verified the following preregistered selection before any network access or source-data inspection:

- Dataset: `isotropic1024coarse`
- Field: velocity
- x indices: `513:768`
- y indices: `513:768`
- z indices: `513:768`
- Frames: `501:510`
- Spatial dimensions: `256 × 256 × 256`
- Number of frames: `10`
- Velocity components: `3`
- Grid stride: `1`
- Filter width: `1`
- z-slab depth per query: `30`
- Total serial queries: `90`
- Maximum points per query: `1,966,080`
- Raw float32 payload: `1.875000 GiB`
- Pilot A overlap: `spatial=0, time=0`

Frozen selection SHA-256:

`385cca0a0b28ac3b17f757ef3b7fcfe2c1954423ceb5376b927b67633a40875e`

---

## Acquisition Instrument

The data were obtained with the project-local acquisition package:

`tools/acquire/JHTDB_PILOT_B_v0_1_0/`

Principal files:

- `VERIFY_SELECTION.bat` — verifies the frozen Pilot B selection without network access
- `SETUP_ACQUIRE.bat` — installs the required Python dependencies
- `ACQUIRE_PILOT_B.bat` — launches the authenticated acquisition
- `acquire_pilot_b.py` — performs the serial JHTDB queries, writes the HDF5 source, validates it, and computes its SHA-256 hash

Before acquisition, `VERIFY_SELECTION.bat` returned:

`[PASS] Frozen selection verified. No network access or source data inspection occurred.`

The acquisition was then run with the registered JHTDB token supplied in the active Windows Command Prompt session.

The script queried the frozen volume sequentially in z-slabs for each of frames `501` through `510`. Each successful cutout was written into a resumable partial HDF5 source until all 90 requests had completed.

---

## Final Source File

**Filename:**

`isotropic1024-coarse-pilot-b-velocity.h5`

**Canonical project location:**

`data/raw/jhtdb/pilot_b/isotropic1024-coarse-pilot-b-velocity.h5`

**Final size:**

`2,015,302,728 bytes`  
approximately `1.877 GiB`

**SHA-256:**

`977e6ab3c437252395dc7f7185af1829619fe1eec754f59f5f3ceae2ca0b969f`

The acquisition instrument completed with:

`[READY] Pilot-B source acquired, validated, hashed, and recorded.`

---

## Provenance Files in This Directory

- `ACQUIRE_LOG.txt` — chronological acquisition log
- `SOURCE_RECORD.json` — machine-readable source/acquisition record
- `SOURCE_SELECTION.md` — human-readable frozen selection specification
- `SELECTION_LOCK_SHA256.txt` — hash of the frozen selection
- `SOURCE_SHA256.txt` — final HDF5 SHA-256 record
- `README.txt` — earlier directory note
- `README.md` — this provenance description

Together, these files preserve the chain from preregistered source selection through authenticated acquisition, validation, and final source hashing.

---

## Reproducibility and Handling

The HDF5 file is the canonical Pilot B raw source for the replication stage. It should not be edited in place.

Any derived ladders, chamber inputs, diagnostics, reports, or replication outputs must be written elsewhere in the project tree and must reference this source by filename and SHA-256.

If the source is copied or transferred, verify the copy against:

`977e6ab3c437252395dc7f7185af1829619fe1eec754f59f5f3ceae2ca0b969f`

before using it.

---

## Acquisition Date

Pilot B acquisition completed on **7 September 2026**.
