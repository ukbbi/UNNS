# E2-P4 v002 focused theorem audit (P4-E5, partial)
| Claim | Status | Basis | Novelty |
|---|---|---|---|
| P4-A, P4-L, P4-T1, P4-T2 (v001) | PROVED (unchanged) | v001 audit; T2 uses only the inclusion chain | elementary |
| P4-C1 inclusion part | PROVED | U subset conv F subset conv F(E_3) = U(E_3) | elementary |
| P4-C1 equality clause | WITHDRAWN (false) | 2Z^3 counterexample, exact, independently replayed (S8) | -- |
| P4-Z1 zero-vertex sufficient condition | PROVED | Graver conformal decomposition + fine zonotopal tiling; tile vertices are subset sums; checked: independent brute-force re-screen of 846 + 1,443 planar and 3,845 spatial rows reproduces all cell and flag counts (S12-S14); 0 P4-Z1 violations among the exact-validated zero-vertex-free runs (2,214 lattice-level and the sampled spatial rows; the remaining ZV-free runs are proved, not re-run) | elementary; one-sided screen |
| P4-Z1.a edges never obstruct | PROVED | Graver minimality of g in Lambda | elementary |
| P4-S1 slab lemma | PROVED | product Graver structure; finite replay for E2+Z box (2,2,2) (243 points, S11) | elementary |
| P4-S1.a obstruction criterion | PROVED (sufficient condition) | immediate from S1 | elementary |
| 57 noncontainment witnesses (36 lattice-level, 21 FIELD-I) | FINITE-EXACT | exact witness in source cell, outside independently derived target cells (S9, S10) | -- |
| Slab witness <=> NOT_CONTAINED on the 1,418 free-coordinate FIELD-I rows in scope | FINITE-EXACT (scoped; 21 rows UNAVAILABLE) | S11 | empirical; no proof of the converse |
| No failure with targets lacking a free coordinate (2,427 rows) | FINITE-EXACT (scoped) | 2,374 by P4-Z1, 53 exact | no theorem |
| CP3-A (general planar) | OPEN | 42,287 + 846 + 1,443 evaluations, 0 failures; no proof | -- |
| P4-F1 | FALSIFIED in general | CE-2 | -- |
| P4-T3 / P4-T4 | NOT PROVED | -- | -- |

**Novelty audit (honest).**  No literature or prior-art search was performed in this release; the proved statements are elementary and are to be regarded as lemmas about the GEO-I realized-geometry
construction, not as discoveries.  Any claim that the slab obstruction is "new" is unverified.  The slab mechanism is the E2-P3 rectangular corner-cube witness mechanism lifted to a nonrectangular
target with a free coordinate; it is not an independent genuinely three-dimensional coupling law.
**Predictive-law verdict.**  Within the recorded scope the slab criterion predicts the exact verdict on every decided free-coordinate row, and no row without a free coordinate fails.  This is a *scoped empirical
predictor with a proved sufficient direction*; it is not a proved complete law, and C3 is NOT claimed.
**Independence caveat.**  Builder and verifier were written by the same author; the verifier shares no code with the builder modules but is not external verification.
