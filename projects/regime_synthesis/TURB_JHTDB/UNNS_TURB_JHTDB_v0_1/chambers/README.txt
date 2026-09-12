CANONICAL CHAMBERS
==================

This directory intentionally contains no modified chamber implementation.

STRUC-I and STRUC-PERC-I are treated as canonical external instruments.
The turbulence project adapts its native ladder data TO the chambers.

Rules:
- do not edit a canonical chamber to make turbulence data fit;
- place adapter code under tools/ladders/;
- place chamber-ready inputs under ladders/struc_i/ and ladders/struc_perc_i/;
- place direct chamber outputs under outputs/exports/struc_i/ and
  outputs/exports/struc_perc_i/;
- record chamber version/hash in every promoted run record.
