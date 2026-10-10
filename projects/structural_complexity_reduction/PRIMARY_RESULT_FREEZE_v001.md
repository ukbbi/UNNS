# PRIMARY_RESULT_FREEZE_v001 — SCR-III-B Primary Result

**Record date:** 2026-10-10
**Status:** `PRIMARY_EXECUTED / RESULT_FROZEN / HELDOUT_NOT_STARTED`
**Scope:** freezes the recorded outcome and the evidence files of the SCR-III-B primary run. It authorizes no further 3×3 computation, changes no protocol, and does not touch GitHub.

## Frozen outcome
| Axis | Result |
|---|---|
| G | **PASS** — 2,604 grammar states (constructive = scan = numpy audit); nominal contraction 99.98448%; G2 traversal independent of W |
| P | **FAIL** — at W = k_B·792 K the target has 26 states, 10 in grammar, 16 excluded |
| T | **NOT_TESTED** (by protocol) |
| C | **NOT_ELIGIBLE** (P failed; no timing run; no speed claim) |

Exclusion gap Δ_nonG = 1.0310349156e-20 J = 0.9428984 k_BT; W/Δ_nonG = 1.0606. Sensitivities: 0.5 kT preserved (2/2); 2 kT 146 of 434 in grammar (288 excluded). Nulls (1,000 N1 + 1,000 N2) are descriptive only.

## Execution record
- Authorization: `PRIMARY_AUTHORIZATION_v001.md` (with Addendum A).
- First launch killed by the host sandbox in the null phase; its artifacts and the reconstructed original driver (hash 973e4e83…, matching the pre-edit hash recorded in the authorization) are in `aborted_run_1/`, with the revision diff. The revised driver (2df16134…) adds checkpoint/resume only. The aborted run's values were not used.
- Final run: pre-execution check PASS; solver binaries `pg` 7adcc1625bd2be6e45a3fe569badd69f1deb09340f71c51dd4f51b48a51878e5, `e2` 1659fcbb00dae2a75d2460f9d4b26359a76eb5177c702b084f82082fd942358b (built from the v009 sources with `g++ -std=c++17 -O2 -Wall -Wextra`).
- The invocation log contains 4 expected BLOCKED records from the guard test at each pre-execution check (one per launch of the final driver).

## Post-run checks (additive; no verdict change)
- External audit of the workbook against the result JSON: no discrepancy.
- Erratum E1: the sentence "all five solvers returned identical target sets" was corrected to: B0, B1, E2 return the 26-state target; G1, G2 return its 10-state grammar-restricted subset.
- `PRIMARY_AUDIT_v001.md`: direct charge-position energies and geometric ice-rule check of the 26 targets reproduce the 16 exclusions and Δ_nonG to ~1e-14; driver revision verified by hash-matched reconstruction.
- Note on hashes: `PRIMARY_RESULT_v001.md` was edited once after first writing (Erratum E1 appended and one sentence corrected). Its pre-erratum hash was d323ac8d3842604c23ef911591df4e81a11e1f6e5270fc103de2488c6e4cb225; the frozen version is listed below.

## Known limitations carried with this freeze
1. Completeness of the 16,777,216-state target enumeration rests on the agreeing C++ and numpy exhaustive scans, both on the frozen v005 physical model. The direct check validates the reported targets and exclusions, not completeness.
2. Verifier and grammar share authorship; the physical model is not independently validated against the original Dryad code (the archives and PREFLIGHT zips were not on disk; verification used extracted-tree manifests).
3. The primary window was chosen knowing the public 1×1 and 2×2 gaps; blindness was low-energy-outcome blindness only.
4. The run used a Linux VM with 2 CPUs; no timing comparison was made.
5. Post hoc observation (not part of the result): in this model the exclusion gap crosses 1 kT at ≈790.4 K, 1.6 K below the reference temperature. See `SCR_III_HELDOUT_SCOPING_NOTE_v001.md` (draft, unfrozen).

## File hashes

### Authorization, narrative and audit records

| File | SHA-256 | Bytes |
|---|---|---|
| `PRIMARY_AUTHORIZATION_v001.md` | `109f7db466434d1beff72b9b1b6e804d05c53d9ee346c672c5dd097c1044ffda` | 3495 |
| `PRIMARY_RESULT_v001.md` | `ac662a76a6c67ab709b8a61c723ae75c69777cf19ff9689a6f55eda00a1853a6` | 4434 |
| `PRIMARY_AUDIT_v001.md` | `8d9b5294480068287d5050f09088141b1f63214b4ef0408c70ee607672734ff2` | 2832 |
| `SCR_III_B_Primary_Result_v001.xlsx` | `a793b754dc9ae2a98f747053f44663cc6e68c22bf5d9a5c8d1b5ed6869cc4c1f` | 15874 |

### Upstream frozen protocol (unchanged)

| File | SHA-256 | Bytes |
|---|---|---|
| `SCR_III_B_SPEC_v001_FINAL.md` | `8a7d9178aab7cc3050718d54eaaa8f4ffe7882f247d948e98540f011306e80af` | 9330 |
| `SCR_III_B_PREREG_v001_FINAL.md` | `cd7e0c76bac8d0354c4790d296429f7b22a26abb4d53f7d7efc9bd541f519f88` | 7803 |
| `RATIFY_v001.md` | `e07f95de65ca5004190da518f25226db25bd0171732315e40dc1ae0258beae5d` | 6286 |
| `PRIMARY_FREEZE_v001.md` | `f377c96e73ce5933e52ad56372d2934b1cd0ae9ccbadee90857a49c511ff178c` | 2445 |
| `PRIMARY_MANIFEST_v001.json` | `e137a7b02337adb265c8a6709bb8d64a99d7db649082d3a4f780de5fa76d9b3b` | 1192 |
| `FREEZE_v009.md` | `177a73443532aba1b5d883a791360795ed37cd3ba87617f558aa29cbafdbf4e5` | 8253 |

### Driver

| File | SHA-256 | Bytes |
|---|---|---|
| `scr_iii_b/primary_exec/primary_run_v001.py` | `2df1613432aa9d79e59246c239ec0b98cf5a885e4ba462c53d5d964f40d0c18b` | 18494 |

### Primary outputs (final run)

| File | SHA-256 | Bytes |
|---|---|---|
| `scr_iii_b/output/primary/.gitkeep` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `scr_iii_b/output/primary/INVOCATION_LOG_primary_v001.jsonl` | `31729d38e43b4f44f7eb6dc8ad47d281bd37f9beb409e02dcc165b7f41bbaeaa` | 1017606 |
| `scr_iii_b/output/primary/INVOCATION_LOG_primary_v001.jsonl.gz` | `68c279229a53adee52b42fc7d94d99fa7805bcf459499a62452515370b570c23` | 45691 |
| `scr_iii_b/output/primary/NULLS_primary_v001.csv` | `2015295ce3d03eba2d70a9d209c8d84514a9027f9a09912f588dfa2acf3f0b55` | 381700 |
| `scr_iii_b/output/primary/PRECHECK_primary_v001.json` | `b52261801d593cd40735cb1a9377a0d8781f509be43fad4f4fd96ad29fa8d33e` | 2711 |
| `scr_iii_b/output/primary/PRIMARY_RESULT_v001.json` | `5bf2766d76963b55ec7f483e68a1684a35a5cb0ec8c6e743b17837a3db416b34` | 23200 |
| `scr_iii_b/output/primary/TARGET_IDS_primary_v001.txt` | `fcda76964ddce08d35011beccce7d1072264b8f74a7003266b75bce87df4ed54` | 219 |
| `scr_iii_b/output/primary/TARGET_IDS_sens_0.5kT_v001.txt` | `b65f08b788395cc1afd6fab1b1397c640389c024385d90a021cc82ae7164da45` | 17 |
| `scr_iii_b/output/primary/TARGET_IDS_sens_2kT_v001.txt` | `8c5f3ec002cbe72c006f3cc692a2ba6d4e27cb851631cf43a8900da075b3d5a6` | 3645 |
| `scr_iii_b/output/primary/primary_run_v001.log` | `b749a86831a5cf5376d86865401bd1a783555a4657e68dcb6dde8f723633eb83` | 2479 |

### Checkpoints used by the final run

| File | SHA-256 | Bytes |
|---|---|---|
| `scr_iii_b/output/primary/ckpt/gen_N1.json` | `fc92738d9b7160992864ba6524af8af930f467cfc78005cca136e63fd2f0be0b` | 595908 |
| `scr_iii_b/output/primary/ckpt/gen_N2.json` | `e1bcee06e5a27b308119787a54bc33ba8306c8db9eeaeb43e959213694d92892` | 594024 |
| `scr_iii_b/output/primary/ckpt/phaseA.json` | `a6091c08d4a457ae996916482133e735c7e7e96a5c39bbb42911a86617392b6d` | 16515 |
| `scr_iii_b/output/primary/ckpt/rows_N1.jsonl` | `df5870ed7e3f7f53bf68abac0f22e385792539b7c75236f73621ac00672a91dd` | 324834 |
| `scr_iii_b/output/primary/ckpt/rows_N2.jsonl` | `d49bd2502b3c23bec863ef35cf27cd55872311bbf692fe07543a2cc57494d19c` | 318778 |

### Aborted first launch and driver provenance

| File | SHA-256 | Bytes |
|---|---|---|
| `scr_iii_b/output/primary/aborted_run_1/INVOCATION_LOG_primary_v001.jsonl` | `7a9dca928c4a7600d5c59e5a80afc5a2f3ecfc1e52c70dce788d082430a2e878` | 302349 |
| `scr_iii_b/output/primary/aborted_run_1/PRECHECK_primary_v001.json` | `09fd75ad7716ad62a65c103badd7709ff7ab068db22800f3b9a64673601db885` | 2711 |
| `scr_iii_b/output/primary/aborted_run_1/TARGET_IDS_primary_v001.txt` | `fcda76964ddce08d35011beccce7d1072264b8f74a7003266b75bce87df4ed54` | 219 |
| `scr_iii_b/output/primary/aborted_run_1/TARGET_IDS_sens_0.5kT_v001.txt` | `b65f08b788395cc1afd6fab1b1397c640389c024385d90a021cc82ae7164da45` | 17 |
| `scr_iii_b/output/primary/aborted_run_1/TARGET_IDS_sens_2kT_v001.txt` | `8c5f3ec002cbe72c006f3cc692a2ba6d4e27cb851631cf43a8900da075b3d5a6` | 3645 |
| `scr_iii_b/output/primary/aborted_run_1/driver_revision.diff` | `7f4123067691bdc3aa269e9a4e91be37c4d7f92b89293fd78417943c90d82097` | 19093 |
| `scr_iii_b/output/primary/aborted_run_1/primary_run_v001.log` | `42e3740b92debe7153949ef4e65881aaf5d24b8069e91b77e9941782b38fbc6b` | 434 |
| `scr_iii_b/output/primary/aborted_run_1/primary_run_v001.original_973e4e83.py` | `973e4e83e91342d63bfd29231f0a0d09371b9edcbe4d5d7687d41d0abf58aa48` | 16869 |

Machine-readable copy: `PRIMARY_RESULT_MANIFEST_v001.json`. This file's own hash is reported outside it (in the session record), since a file cannot contain its own hash.

**Current state:** PRIMARY_RESULT_FROZEN / G_PASS / P_FAIL / T_NOT_TESTED / C_NOT_ELIGIBLE / NO_FURTHER_3x3_EXECUTION_AUTHORIZED.
