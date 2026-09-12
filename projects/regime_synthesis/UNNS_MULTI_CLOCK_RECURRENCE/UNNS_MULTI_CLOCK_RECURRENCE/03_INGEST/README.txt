UNNS MULTI-CLOCK RECURRENCE - NEUTRAL INGEST v0.0.1

Purpose
-------
Canonicalize source time-domain trajectories without defining a UNNS multi-clock metric.

Generated now
-------------
HUANG: limit-cycle, quasi-periodic, and chaotic time/intensity records from Figure2.
LUO: DTQC m(t), fidelity F(t), and entanglement-entropy S(t) records for low/intermediate/high driving-frequency regimes.

Explicit exclusions
-------------------
No smoothing, interpolation, normalization, target-frequency selection, thresholding, or UNNS classification.
Publisher-provided Fourier spectra are catalogued but not used in canonical time-domain records.
C003 is not used. Zhu 2026 remains a holdout. Moon 2025 remains access-restricted.

Reproduction
------------
Place source files in the project root as:
02_RAW/HUANG_2025/41467_2025_64413_MOESM3_ESM.xlsx
02_RAW/LUO_2026/18396452.zip
Then run from 03_INGEST:
  python ingest_huang.py
  python ingest_luo.py

See HUANG/HUANG_INGEST.json, LUO/LUO_INGEST.json and ../04_CORPUS/INGEST_AUDIT.json for provenance and checksums.
