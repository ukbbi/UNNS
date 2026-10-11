# Manuscript evidence (additive records)

Two additive records supporting the manuscript "Structural Predictability in the UNNS Substrate" (v009 and later).
They were produced after the frozen SCR-III / SCR-IV research records and do not modify them.
The original scientific evidence remains anchored to commit 4e759d381875c7341e2f26cb72319b44d87aed15.

| Package | Content |
|---|---|
| SCR_MS_GRAMMAR_COUNT_4X4_v001 | Exact 4x4 ice-rule grammar count (193,662 of 2^40) from the frozen vertex table; not Lean-checked |
| SCR_MS_SUPPLEMENT_v001 | Single-island reversal analysis of the 4x4 ground state and perturbation-bound inputs; exact rational arithmetic on frozen couplings; outside the Lean certificate |

Both read frozen inputs from `scr_iii_b/GAP4_v010/` read-only. Reproduce from this directory (ROOT must be passed, because the packages sit one level deeper than their default):

    cd SCR_MS_GRAMMAR_COUNT_4X4_v001 && python3 grammar_count_4x4_v001.py ../..
    cd SCR_MS_SUPPLEMENT_v001        && python3 supplement_analysis_v001.py ../..

Each run rewrites its `*_output.json` next to the script; the recorded outputs must be byte-identical (see each package's SHA256SUMS.txt and RECORD_v001.md).
