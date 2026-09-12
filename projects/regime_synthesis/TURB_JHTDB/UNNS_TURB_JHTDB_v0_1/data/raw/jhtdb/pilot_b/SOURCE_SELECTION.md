# JHTDB Pilot B — Frozen Source Selection

**Project:** `UNNS_TURB_JHTDB_v0_1`  
**Pilot:** `jhtdb_pilot_b`  
**Status:** `SELECTED / LOCKED / PENDING ACQUISITION`  
**Selection lock SHA-256:** `385cca0a0b28ac3b17f757ef3b7fcfe2c1954423ceb5376b927b67633a40875e`

## Selected physical sample

Dataset: `isotropic1024coarse`  
Field: `velocity`

Spatial cutout, 1-based inclusive JHTDB indexing:

- `x = 513:768`
- `y = 513:768`
- `z = 513:768`

Zero-based equivalent:

- `x,y,z = 512:767`

Cutout size: `256 × 256 × 256` grid points.  
Spatial stride: `1`.  
Filter width: `1`.

The cube is a half-domain translation of the Pilot-A origin along all three axes. It shares **zero spatial grid points** with Pilot A.

## Selected time window

Stored coarse-frame indices, 1-based inclusive:

- `501:510`

With `dt = 0.002` and `t(i) = (i-1) × 0.002`, the physical times are:

`1.000, 1.002, 1.004, 1.006, 1.008, 1.010, 1.012, 1.014, 1.016, 1.018`.

This shares **zero stored frames and zero physical times** with Pilot A (`1:10`, `t=0.000:0.018`). The gap from Pilot A's last time to Pilot B's first time is `0.982`.

## Why this selection

The choice was made before Pilot-B data were inspected. It preserves the same dataset, `256³` dimensions, 10 consecutive frames, spatial stride, filter width, and stored `dt` as Pilot A while strengthening physical separation in both space and time. No outcome-dependent search over cutouts is allowed after this selection.

## Acquisition

The required final source path is:

`data/raw/jhtdb/pilot_b/isotropic1024-coarse-pilot-b-velocity.h5`

Use:

`tools/acquire/JHTDB_PILOT_B_v0_1_0/ACQUIRE_PILOT_B.bat`

The acquisition tool verifies the selection lock before querying JHTDB, performs serial z-slab requests, assembles the ten frames into the Pilot-A-compatible HDF5 layout, validates the file, calculates SHA-256, and updates `SOURCE_RECORD.json`.

A registered JHTDB token is required. The public testing token cannot be used for this acquisition because its query limit is far below the selected cutout size.

**Do not run the frozen physical adapter until `SOURCE_RECORD.json` says `ACQUIRED_HASHED_READY_FOR_ADAPTER` and `adapter_may_run` is `true`.**
