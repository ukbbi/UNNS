MC_REP_STUDY_v002

Purpose:
  Full cross-corpus comparison of four temporal representations.

Core representations:
  1. vector-depth recurrence family
  2. joint-phase-conditioned recurrence
  3. source-defined frequency lattice
  4. fractional-cover decomposition

Important:
  - C003 is never loaded.
  - Huang and integer DTC controls do not receive fabricated second clocks.
  - no threshold, verdict, or grammar freeze is defined.
  - quantitative outputs are hashed before interpretation.

Run:
  python 05_METHODS/rep_study_v002.py --root <UNNS_MULTI_CLOCK_RECURRENCE>
