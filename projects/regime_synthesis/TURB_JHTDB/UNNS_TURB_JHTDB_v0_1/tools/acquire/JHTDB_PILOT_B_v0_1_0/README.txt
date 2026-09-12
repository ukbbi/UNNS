JHTDB PILOT B ACQUISITION v0.1.0
====================================

Purpose
-------
Acquire exactly the already-frozen Pilot-B source. This tool does NOT choose a
cutout and does NOT inspect Pilot-B results before acquisition.

Frozen selection
----------------
Dataset: isotropic1024coarse
Field: velocity
x = 513:768, y = 513:768, z = 513:768  (1-based inclusive)
frames = 501:510
physical time = 1.000..1.018, dt = 0.002
selection SHA-256 = 385cca0a0b28ac3b17f757ef3b7fcfe2c1954423ceb5376b927b67633a40875e

Required output
---------------
data\raw\jhtdb\pilot_b\isotropic1024-coarse-pilot-b-velocity.h5

Before acquisition
------------------
1. Run VERIFY_SELECTION.bat. It must report PASS.
2. Run SETUP_ACQUIRE.bat once to install givernylocal and dependencies.
3. Obtain a registered JHTDB token if you do not already have one.
4. In the SAME Command Prompt window, set the token only as an environment variable:

   set JHTDB_TOKEN=<your registered token>

Do not paste the token into SOURCE_RECORD.json or any project file.

Acquire
-------
Run:

   ACQUIRE_PILOT_B.bat

The default acquisition is serial and uses z slabs of depth 30. This gives
90 sequential JHTDB requests, each below 2 million spatial grid points.
No simultaneous requests are made.

Resume
------
If network access is interrupted, run ACQUIRE_PILOT_B.bat again. The .partial.h5
file is preserved and acquisition resumes from the last fully written z slab.
Use --force-restart only if you explicitly want to discard that partial file.

Completion gate
---------------
Do NOT run the physical adapter until:

- SOURCE_RECORD.json status = ACQUIRED_HASHED_READY_FOR_ADAPTER
- readiness.adapter_may_run = true
- SOURCE_SHA256.txt exists

The acquisition script sets those only after HDF5 validation and SHA-256 hashing.

Why a registered token is required
----------------------------------
The public JHTDB testing token is limited to 4096 points per query. It is
therefore deliberately rejected by this tool for the 256^3 Pilot-B source.
