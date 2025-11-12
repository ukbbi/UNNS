/*═══════════════════════════════════════════════════════════════════════════════
  UNNS SUBSTRATE — JSON EXPORTER MODULE
  ───────────────────────────────────────────────────────────────────────────────
  File:        json_exporter.js
  Version:     vF.0.1-pre
  Chamber:     XX  (Recursive Tensor Potential & Operator Coupling Simulator)
  Phase:       F  (Field Data Serialization)
  Author:      UNNS Research Collective
  License:     UNNS Open Computational License (UOCL-2025)

  PURPOSE:
  ─────────
  Serializes validated recursion-tensor data and derived field tensors (E,B)
  into standardized JSON format for Phase F storage, cross-chamber analysis,
  and Maxwell-bridge post-processing.

  INPUT STRUCTURE:
  ────────────────
      {
        "phase": "F",
        "fields": n,
        "grid": 256,
        "Rij": [...],
        "Phi": [...],
        "E_field": [...],
        "B_field": [...],
        "alpha_matrix": [...],
        "energy": <float>,
        "divergence_balance": <float>,
        "curl_magnitude": <float>,
        "timestamp": <ms>
      }

  CORE OPERATIONS:
  ────────────────
  • buildHeader()          → add metadata (phase, build, git_hash)
  • compressJSON()         → gzip stream for efficient storage
  • computeCRC32()         → ensure data integrity via hash signature
  • exportToDisk(path)     → write validated `.json.gz` output
  • verifyExport()         → re-parse + CRC recheck for bit-level consistency

  OUTPUT SCHEMA (vF.0.1):
  ────────────────────────
      {
        "phase": "F",
        "version": "vF.0.1",
        "build": <string>,
        "git_hash": <string>,
        "data": { ... },
        "crc32": <string>,
        "file_size": <bytes>
      }

  NUMERIC & STRUCTURAL ASSUMPTIONS:
  ─────────────────────────────────
  - All arrays are flattened Float64 (row-major order)
  - JSON indentation level = 0 (compact mode)
  - CRC computed before compression
  - Timestamp in UNIX ms precision
  - Compatibility: backward-readable by Phase E exporters

  PERFORMANCE TARGETS:
  ────────────────────
  • Export time < 300 ms @ 256² grid
  • Compression ratio ≥ 2.5×
  • CRC verification = 100 % success
  • Memory usage < 200 MB

  VALIDATION CRITERIA:
  ────────────────────
  • File write & re-parse without exception
  • CRC32(source) === CRC32(parsed)
  • Header metadata complete (phase, version, timestamp)
  • Optional SHA-256 cross-check (developer debug flag)

  ───────────────────────────────────────────────────────────────────────────────
  UNNS SUBSTRATE PROJECT — Data Integrity & Archival Layer
  “Preserve the Field, Protect the Recursion.”
═══════════════════════════════════════════════════════════════════════════════*/
