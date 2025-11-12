/*═══════════════════════════════════════════════════════════════════════════════
  UNNS SUBSTRATE — PHASE F VALIDATION MODULE
  ───────────────────────────────────────────────────────────────────────────────
  File:        phaseF_validator.js
  Version:     vF.0.1-pre
  Chamber:     XX  (Recursive Tensor Potential & Operator Coupling Simulator)
  Phase Link:  E → F Transition
  Author:      UNNS Research Collective
  License:     UNNS Open Computational License (UOCL-2025)

  PURPOSE:
  ─────────
  Provides post-processing and numerical integrity tests for Phase F data.
  Validates tensor antisymmetry, divergence conservation, and energy equilibrium
  of exported recursion datasets before they enter analytic pipelines.

  INPUT STRUCTURE:
  ────────────────
      {
        "Rij": [...],
        "Phi": [...],
        "E_field": [...],
        "B_field": [...],
        "grid": 256,
        "phase": "F",
        "energy_gradient": <float>,
        "timestamp": <ms>
      }

  CORE CHECKS:
  ────────────
  • validateAntisymmetry()     →  |R_ij + R_ji| < 0.005
  • validateConservation()     →  ΣΦ_ij ≈ 0  (periodic boundary)
  • validateOrthogonality()    →  ⟨E·B⟩ ≈ 0 ± 1e−3
  • validateEquilibrium()      →  |∂E/∂t| + |∂B/∂t| < 1e−6
  • reportMetrics()            →  summary JSON + console diagnostics

  OUTPUT SCHEMA:
  ──────────────
      {
        "antisymmetry_error": <float>,
        "divergence_error": <float>,
        "E_B_dot": <float>,
        "energy_gradient": <float>,
        "status": "PASS|WARN|FAIL"
      }

  NUMERIC ASSUMPTIONS:
  ────────────────────
  - Same FD stencil & periodic boundaries as phaseF_bridge.js
  - Tolerances defined globally in validator.conf
  - Precision: double (64-bit float)

  PERFORMANCE:
  ────────────
  • Executes <100 ms @ 256² grid
  • Memory footprint < 300 MB

  ───────────────────────────────────────────────────────────────────────────────
  UNNS SUBSTRATE PROJECT — Numerical Integrity Layer
  “Validation before Visualization.”
═══════════════════════════════════════════════════════════════════════════════*/
