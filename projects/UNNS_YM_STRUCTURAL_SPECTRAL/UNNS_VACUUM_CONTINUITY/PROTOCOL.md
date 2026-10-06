# PROTOCOL.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Protocol level:** Project-wide  
**Current stage:** Stage 2 preparation

## Non-negotiable inherited rules

1. `UNNS_YM_GAP` remains closed and historically unchanged.
2. The old terminal result remains `DATA-INDETERMINATE`; its central Class-B trajectory crossed the proposed CORR-I boundary at beta = 6.71, while the preregistered uncertainty ensemble spanned both signs.
3. Negative and indeterminate results are preserved.
4. STRUC-I remains canonical and must not be modified.
5. CORR-I cannot define the new continuity hypothesis by itself.
6. Model refinement is not promoted to measured-data refinement.
7. No threshold, distance, window, proxy, or normalization may be retuned after the target result is inspected.

## Stage-2 run order

A. Freeze `PREREG_VREF_I.md`.  
B. Freeze `SOURCE_ADMISSION.md`.  
C. Run VREF-I self-tests.  
D. Validate the operational vacuum proxy independently of CORR-I.  
E. Apply the frozen representation to the first admitted measured-data source.  
F. Run the preregistered independent representation/sensitivity checks.  
G. Only then compare with inherited CORR-I behavior.

## Primary Stage-2 representation

VREF-I uses an ordered gauge-invariant spatial profile referenced to an independently defined no-source or explicitly vacuum-subtracted baseline.

The primary finite-data vacuum proxy is zero in those vacuum-referenced coordinates:

\[
V_r^*=0.
\]

The primary distance is the fixed-width common-grid RMS profile distance frozen in `stage1/STAGE1_FREEZE.md`.

## Output rule

All Stage-2 results are written to `output/`; source material remains in `data/raw/`, deterministic derived products in `data/derived/`, and chamber implementation in `chambers/vref_i/`.
