# HD-0 verdict — Source-Locked Generative Atlas Preflight

Date: 2026-10-30. Spec: GEO_HD_1_SPEC_v003.

| Gate | Criterion | Result |
|---|---|---|
| SOURCE | overlap matrix complete (theorem, release, hypotheses, status, local path, GitHub path, immutable commit) | **SOURCE_PASS** — 27 rows / 20 claims; 19 GitHub-hosted sources byte-identical to local; v002b present only on GitHub, snapshotted with hashes |
| SOURCE | every candidate theorem checked for prior duplication | done; see matrix statuses (7 INHERITED, 5 REPLICATION, 3 REFORMULATION, 6 NEW_CANDIDATE [elementary], 1 COUNTEREXAMPLE [remark], 5 OPEN rows) |
| ATLAS | benchmark incidence data reproduce frozen results | **ATLAS_PASS** — FR-1…FR-11 (6: 24/27/32/49; 72: 3 occurrences, 3 incoming edges, 4 histories; GEO-I v002 cell counts for 3600, 44100) |
| ATLAS | connecting maps have explicit domains/codomains | `HD0_CONNECTING_MAPS.md` |
| ATLAS | independent verification | `verify_atlas.py` 36/36 checks, 5/5 mutation tests detected (builder and verifier share no code) |

**Verdict: SOURCE_PASS + ATLAS_PASS.** Meaning: the atlas is well-defined and its obligations are identified; it does not mean any new theorem was found. The expensive inherited verifications (Vol. I/II registry reruns, GEO-I v002–v012 exhaustive audits, SELECT-II enumeration to 20,000) are NOT_RERUN.

Not authorized by this verdict: GEO-HD-1B transport experiments. They begin only on the user's instruction.

Items needing the user's attention:
1. Vol. I/II first appear on GitHub at fefa7910…, one commit after the reference-collection commit bb8b12d7…; Paper A/B manuscripts and `registry.csv` are local-only (hashes recorded).
2. GEO-I v004 §1.5 already proves the planar origin-deletion non-coverage, so the "higher-dimensional obstruction" in GEO_HD_1.pdf is a k-dimensional restatement, not new.
3. Bounded observation: minimal common successors of 96 and 27 up to 5000 are {432, 784, 3750}; the frozen C7 lists {432, 784} (≤ 784). Not a theorem.
4. Identifier choice not specified by the spec: the 13-point k = 3 parity specimen is `PARITY_TERNARY_K3`.
5. Existing STATUS.md, CHANGELOG.md, MANIFEST.json were not modified; HD-0 additions are recorded in `BASELINE/` only.
