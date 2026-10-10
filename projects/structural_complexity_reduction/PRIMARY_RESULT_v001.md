# PRIMARY_RESULT_v001 — SCR-III-B Primary Generative Admissibility Experiment

**Date:** 2026-10-10 · **Driver:** `scr_iii_b/primary_exec/primary_run_v001.py` (sha256 2df16134…0c18b) · **Authorization:** `PRIMARY_AUTHORIZATION_v001.md` (+ Addendum A)
**Instance:** real 3×3, 24 spins, E0 = −9.271994751803727e-20 J, W = k_B·792 K = 1.093474008e-20 J, tau = 1e-9·Σ|K|.

## Verdict (reported independently)
| Axis | Result |
|---|---|
| **G** constructive contraction | **PASS** — grammar set = 2,604 states, equal across constructive G2, full-scan G1 and an independent numpy audit; 99.984% of the 16,777,216 nominal states never materialized (2,604 materialized, 25,786 nodes); G2 traversal identical at all three windows (target-blind) |
| **P** physical preservation | **FAIL** — at W = 1 kT the target has 26 states, 10 inside the grammar and **16 excluded** (FN = 16) |
| **T** independent transfer | **NOT_TESTED** (by protocol) |
| **C** charged computational consequence | **NOT_ELIGIBLE** (requires P PASS); no timing run |

## Exclusion gap (first disclosure)
Δ_nonG = 1.0310e-20 J = **0.9429 k_BT** (cpp nullgap and numpy audit agree). W/Δ_nonG = 1.0606 → W + tau > Δ_nonG → fail, consistent with the gap theorem. Smallest excluded target id 2726297; FN ids: [2726297, 4613734, 5400166, 5531238, 5654118, 5662326, 5727846, 7759462, 9017753, 11049369, 11114889, 11123097, 11245977, 11377049, 12163481, 14050918].

## Sensitivities (cannot rescue the primary)
| W | target states | in grammar | FN | preserved |
|---|---|---|---|---|
| 0.5 kT | 2 | 2 | 0 | yes (W/Δ = 0.530) |
| 1 kT (primary) | 26 | 10 | 16 | **no** (1.061) |
| 2 kT | 434 | 146 | 288 | no (2.121) |

B0, B1 and E2@75% returned the identical complete physical target at every window; G1 and G2 returned the identical grammar-restricted subset (target ∩ grammar), as designed (see Erratum E1); numpy audit target = B0 target; zero unresolved-boundary cases; zero numpy near-boundary states.

## Nulls (1,000 + 1,000 valid; descriptive only, no p-value or verdict)
- N1 degree-preserving: survivors min/median/max 2552/2970/7560 (1.6% of nulls have ≤ 2,604); Δ_null median 0, max 0.0077 (< real 0.0102); preservation at 1 kT: 0/1000.
- N2 free incidence (9 empty-grammar rejections, 1009 draws): survivors 256/2432/6336; Δ_null = 0 for all; preservation at 1 kT: 0/1000.
- The real grammar is the only one of 2,001 with Δ_nonG > 0.0077: most nulls exclude a ground state outright.

## Run integrity and disclosures
- Pre-execution check PASS (document hashes, v005–v009 manifests, constants, guard blocks W>0 without the flag). The check re-ran on each resume, so the audit log shows 4 expected guard BLOCKED records.
- First launch was killed by the host sandbox mid-null-phase; partial artifacts kept in `output/primary/aborted_run_1/`; driver revised for checkpoint/resume only (Addendum A). Final run used checkpoints for phase A and nulls; phase A itself ran in one pass.
- Window chosen knowing the public 1×1 (0.871) and 2×2 (0.952) gaps; blindness was low-energy-outcome only. Verifier shares authorship with the grammar code.
- No H-C timing was run, so no speed claim of any kind. Environment: Linux VM, 2 CPUs.

## Output hashes
```
5bf2766d76963b55ec7f483e68a1684a35a5cb0ec8c6e743b17837a3db416b34  PRIMARY_RESULT_v001.json
2015295ce3d03eba2d70a9d209c8d84514a9027f9a09912f588dfa2acf3f0b55  NULLS_primary_v001.csv
b52261801d593cd40735cb1a9377a0d8781f509be43fad4f4fd96ad29fa8d33e  PRECHECK_primary_v001.json
fcda76964ddce08d35011beccce7d1072264b8f74a7003266b75bce87df4ed54  TARGET_IDS_primary_v001.txt
b65f08b788395cc1afd6fab1b1397c640389c024385d90a021cc82ae7164da45  TARGET_IDS_sens_0.5kT_v001.txt
8c5f3ec002cbe72c006f3cc692a2ba6d4e27cb851631cf43a8900da075b3d5a6  TARGET_IDS_sens_2kT_v001.txt
68c279229a53adee52b42fc7d94d99fa7805bcf459499a62452515370b570c23  INVOCATION_LOG_primary_v001.jsonl.gz
```

## Erratum E1 (2026-10-10, after external audit)
The original sentence "All five solvers returned identical target sets" was misleading. Correct statement: B0, B1, E2 return the 26-state physical target at 1 kT; G1 and G2 return its 10-state grammar-restricted subset. The driver's check compared each solver with its expected set, so the verdicts are unchanged; only the wording was wrong. The gap between the two sets is the 16 false exclusions.
Further follow-up checks are recorded in `PRIMARY_AUDIT_v001.md`.
