# UNNS_U4_STAGE2_v001 (no manuscript)
Author: UNNS Research Collective. Contents: docs/PROOFS.md (proofs, hypotheses, falsification, non-claims), data/registry_stage2.{json,csv} (53 claims, separate `proof_closure` field), data/stage2_config.json + stage2_registration.json (SHA-256 of config and code, written BEFORE the experiments), code/ (independent engine `indep_graph.py`, checks, survey, selectors, verifier), reports/ (machine-readable), SHA256SUMS.
Run: `python3 code/verify_stage2.py` (~8 min; `--quick` skips the 340 s survey). Paths are relative.

## Status (proved / falsified / conditional / open)
* Proved (author-level, external review pending): U4.3-T2, U4.3-T3 (memory one only), U4.3-T4 (radius one, k>=3), U4.2-T4 (needs a loop), lemma M1-P2, U4-M2 items 1-6 (Y_NB).
* Falsified: nothing in this release. Negative result retained: golden mean and directed 3-cycle with loops not found at memory 1 or 2 (golden mean excluded by T2; 3-cycle open).
* Conditional: U4.3-X1 (rests on T2-T4); everything inherited from frozen U3/U3-COR (triangle-free, N(1)={4}, scaling homomorphism).
* Open: entropy of infinite Y_NB; U4.3-Cj1/Cj2; U4.5-S2c; U4.1-C1; G2.
* Not closed, NOT upgraded: U4.1-T2, T4, T5; U4.4-T1, T2; U4.5-S2d (still sketches).
* Observations (not theorems): survey 2C (memory 2: 94,352 rules; 68,364 non-real; 6,422 nonempty with no period<=2 point; 0 fixed-point violations; 42,615 signatures; signature matches are necessary conditions only) and selector experiment 2D (432 runs; all neighbourhoods certified; state-only val_asc/deg_asc give period-2 cycles from all 18 starts, NB memory changes behaviour: val_asc rank1 -> 9 cycles of period 21 + 9 STUCK; deg_asc rank1 -> 4 cycles (period 21), 10 escapes, 4 STUCK; descending keys escape in both; ranks 2,3 mostly coincide. Prime visits are finite observations; a history constraint is not an autonomous generator).

## Gates
S2-G1 PASS (verifier reruns four independent checks; proofs written, not externally refereed). S2-G2 PASS (certificates + proof of Y_NB items). S2-G3 PASS (no imported source constraints: rules metric-only; survey reproduces). S2-G4 PASS (selector rows reproduce). S2-G5 PASS (exact distance/neighbour computations; independent engine cross-checked). S2-G6 PASS (every claim carries explicit status and proof_closure). S2-G7 PASS (hashes, relative paths, frozen releases untouched).

## Disclosures and limitations
1. A development dry run of the selector code on start 30 preceded registration and is unrecorded.
2. Amendments A1, A2 (in stage2_config.json): the survey's non-real-spectrum classifier was first floating-point on whole matrices (unsound), then floating-point on recurrent blocks (12/400 audit disagreements), finally exact (sympy) for all rules. Run 2 counts differ partly because an audit hook consumed the shared RNG; superseded. Final counts are those above.
3. Survey covers 10 windows; 'not found' is not 'impossible'.
4. Inherited verifications (U1-U4 SPEC) NOT_RERUN; frozen sources hashed in data/u3_v001_registration.json.
5. Proofs depend on frozen results I1-I4 (triangle-free etc.), not re-derived here.
6. Entropy of Y_NB open; Hashimoto lower bounds are exploratory.
