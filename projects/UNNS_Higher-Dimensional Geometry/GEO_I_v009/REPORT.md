# GEO-I v009 — Report

## Verdicts
* **Hollow box (G9-C1/T1/T1H): OPEN (A-OPEN).** The continued-fraction boundary induction was attempted; A1 (sail directions) is standard, but A2–A5 (exact piece decomposition respecting the punctured origin, an invariance-preserving induction step, a no-additional-hole lemma, `β1 = 2`) were not obtained. Mandatory falsification: exact survey of `853` structured pairs for `d = 73..110` (composite `d`, large partial quotients up to `54`) and all units for `d = 46..50` (a gap of the inherited ranges) — no counterexample. Label: *no counterexample within the completed scope*; not a theorem.
* **Cap (G9-CAP/T2): OPEN (B-OPEN).** Survey of 10,110 boxes (`d = 21..22`) plus v008's 26,636: all covered. The proof programme B1–B5 was not completed (the cap needs the same continued-fraction data as G9-C1).
* **Consolidation (G9-T3): OPEN**, conditional on the two above.
* **Nullity five (G9-C2, G9-T4): PROVED+CHECKED.** All minimal non-embedded boxes of nullity 5 (any length, any parity matrix) are blow-ups of one of **12** reduced supports (`p = 8..16`), and each has `r_min = 3`. Orbit completeness (1371 non-empty orbits, 1326 spanning) confirmed by an independent Burnside count over `GL(5,2)`; classification cross-checked on 785 supports by the v006 code path with 0 disagreements; 12 RANK certificates accepted by the standalone checker.
* **Zero columns (G9-Z): PROVED+CHECKED.** A zero parity column never occurs in a minimal non-embedded box; the proof is self-contained (MATHEMATICS §1) and confirmed exhaustively on 6,763 matrices. The v008 census is therefore unrestricted.
* **Corollary G9-T5: PROVED+CHECKED.** Every non-embedded box of nullity `≤ 5` has `r_min = 3`; any counterexample to the universal `r_min = 3` has nullity `≥ 6`. All 212 non-embedded spanning nullity-5 orbits (not only minimal ones) have `r_min = 3`.

## What the release does not establish
The two planar proofs (the stated release-defining goals) were not obtained, so the original planar stabilization question stays open. The nullity-five classification does not decide G8-C3 (full support) or nullity `≥ 6`.

## Corrections recorded
The v008 handoff said the legacy certificate files contain 20 records; they contain 19 (the 40 new v008 certificates and their acceptance are unaffected). The hollow exact-complement data of v006–v008 left `d = 46..50` unchecked in the exact-complement sense (only the T-part check existed); v009 closes that range.

## Gates
G1 earlier releases and frozen libraries byte-identical (hash-checked); G2–G4 reported honestly as OPEN; G5 nullity-5 and zero-column done; G6 certificates verified independently; G7 clean-unzip smoke and full runs, new and inherited checks separate; G8 documentation; G9 no remote changes, no rewriting of earlier results.

## Next
(1) A cell-level induction map between consecutive Euclid levels (G9-C1); (2) the cap through the record-minimum chain; (3) nullity 6 (`GL(6,2)` orbits of `PG(5,2)` subsets are too many to list; a structural reduction such as full support/common base would be needed).
