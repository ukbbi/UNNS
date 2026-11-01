# GEO-HD-1B / E2-P4 v005

Independent proof and boundary analysis for the planar theorem P4-P1 and its three-dimensional extension. C3 is NOT claimed. Nothing here is a novelty claim.

## Results in one table
| | status |
|---|---|
| P5-P1 planar monotonicity (explicit tiling lemma, subset-sum vertices; no gap found) | PROVED |
| P5-P1.a FIELD-I corollary scope: needs Lambda_x <= Lambda_{C(x)} | PROVED (correction) |
| 3D "no free coordinate => preserved" | FALSE: 2E_3 <= 2Z^3, Q=(2,4,2); hand proof, infinite family (dilation) |
| 3D "no split coordinate => preserved" | FALSE: BCC target (finite-exact certificate) |
| 3D split targets: exact criterion via slab law | PROVED (P5-S4) |
| Which non-split targets preserve U | OPEN (P5-Q1) |
| Prior-art audit | LIMITED, not a clearance |

Same-author caveat: proofs and code come from the same author as v004; an external reviewer is still needed.

## Layout
* `theory/` THEOREMS_V005.md (proofs), THEOREM_AUDIT_V005.md, COUNTEREXAMPLES_V005.md, PRIOR_ART_AUDIT_V005.md
* `src/` engine (byte-identical v004 pinned copy), geo3.py, mini.py (stdlib brute force), tiling_lemma.py, ce_check.py, planar_audit.py, split_slab.py, scan3.py, make_results.py, run_split_criterion.py
* `results/` scans, audits, counterexample checks, P5_REPORT_V005.md
* `RUN_VERIFY.py --fast | --full | --shard Sk | --list`; `tests/test_v005.py` (pytest)
* `STATUS.json`, `CHANGELOG_V005.md`, `MANIFEST.json` are release-local; project-level STATUS/CHANGELOG/MANIFEST were not touched.

Inherited v004 verification is recorded NOT_RERUN (hash-pinned engine, v004 zip sha256 in shard S0).
