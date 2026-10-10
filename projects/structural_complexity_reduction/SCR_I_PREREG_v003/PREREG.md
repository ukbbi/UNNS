# SCR-I-A v003 — Frozen Preregistration

## Primary question
Can a frozen UNNS structural gate chain reduce mechanism-candidate space while preserving the independently identified viable **mechanism-basin structure**?

The primary unit is a basin/class, not an individual candidate identity.

## Frozen separation of roles
1. **Generator:** pinned Chamber LIII P4 adversarial generator.
2. **Structural filter:** G1→G2→G3→G4, unchanged from v002.
3. **Independent target oracle:** pinned LIII empirical-viability criterion, unchanged from v002.
4. **Basin identifier:** pinned LIII normalized five-coordinate density clustering, applied only to target-positive candidates.
5. **Primary seeds:** `2026101001`–`2026101005`; never used for design calibration.

## Primary preservation criteria
For every seed × pool-size cell:

- basin recall = 1.000;
- each baseline target basin retains at least 20 target-positive SCR survivors;
- at least 95% of each baseline basin lies within normalized distance 0.25 of a surviving target-positive representative from that same basin;
- normalized survivor-centroid drift from the baseline basin centroid ≤ 0.125;
- unclustered target fraction ≤ 0.05;
- all adequately populated target phenotype strata `(regime_base, family, composition)` remain represented.

Candidate-level target recall is retained as a diagnostic but is **not** a success criterion.

## Interpretation discipline
Preserving one basin while discarding many redundant candidate identities establishes structural compression only if the frozen criteria above pass. It does not establish a complexity-class result. A matched-random null tests whether the same preservation is generic at the observed pruning rate.
