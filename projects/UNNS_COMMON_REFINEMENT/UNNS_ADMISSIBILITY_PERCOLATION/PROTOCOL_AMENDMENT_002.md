# PROTOCOL AMENDMENT 002

## Status

**SEPARATE PERCOLATION AUDIT INSTRUMENT CREATED — v2.5.0 REMAINS FROZEN**

Date: 2026-09-19

## Trigger

The frozen STRUC-PERC-I v2.5.0 batch produced five non-full cases while STRUC-I had already classified all 30 ladders as fully admissible.

`CROSS_CHAMBER_AUDIT_001.md` reproduced the v2.5.0 batch and identified two implementation-sensitive mechanisms plus the need for exact connectivity-threshold reporting.

## New instrument

A separate chamber has been created:

`chambers/STRUC-PERC-I_AUDIT_v2_5_1/struc_perc_i_audit_v2_5_1.html`

Parent SHA-256:

`844b84e4f1d681a4363207974061bbee62fdc69904990a9387bdaa2bb8b71200`

v2.5.1 SHA-256:

`bc3daa66c3281f1e2679d5d42c153123b49e78b9bdfeb856d93eb18e4c1d5b7c`

## Scoped changes

Only three logical changes are allowed in v2.5.1:

1. effective-zero IQR fallback tolerance;
2. nonterminal adaptive plateau before exact-threshold probing;
3. exact graph-connectivity-threshold reporting.

No source corpus, frozen input, STRUC-I result, or parent STRUC-PERC-I v2.5.0 artifact is changed.

## Next run

Run v2.5.1 on the same 30 frozen files in:

`inputs/struc_perc_i/`

Export:

`struc_perc_audit_v2_5_1_batch_results.csv`

`struc_perc_audit_v2_5_1_batch_results.json`

These outputs must be stored separately from the v2.5.0 batch before final synthesis.
