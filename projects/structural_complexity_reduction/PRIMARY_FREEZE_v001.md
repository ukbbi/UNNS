# PRIMARY_FREEZE_v001 — SCR-III-B Primary Protocol

**Record date:** 2026-10-10  
**Status:** PRIMARY_PROTOCOL_FROZEN / PRIMARY_NOT_AUTHORIZED  
**Scope:** Protocol document content only — no primary physical experiment has been executed or authorized.

## Exact frozen deliverables

| Document | SHA-256 |
|---|---|
| `SCR_III_B_SPEC_v001_FINAL.md` | `8a7d9178aab7cc3050718d54eaaa8f4ffe7882f247d948e98540f011306e80af` |
| `SCR_III_B_PREREG_v001_FINAL.md` | `cd7e0c76bac8d0354c4790d296429f7b22a26abb4d53f7d7efc9bd541f519f88` |
| `RATIFY_v001.md` | `e07f95de65ca5004190da518f25226db25bd0171732315e40dc1ae0258beae5d` |

See `PRIMARY_MANIFEST_v001.json` for SHA-256 fingerprints, byte sizes and accessible source-archive hashes. These exact `FINAL` filenames identify the frozen document bytes; no earlier draft was overwritten.

## Scientific decisions locked

G and P are separately judged; T is **NOT_TESTED**; C is a separate, conditional computational consequence. Primary physical window `W=k_B×792 K`; operational `tau=1e-9 Σ|K|`. E2 retains **75%** strongest pairs. Deterministic master seed `20261010`; 1,000 valid N1 and 1,000 valid N2 nulls with 5,000 attempt cap per family. Z₂ disabled. H-C requires complete P PASS and all 15 paired charged B0/G2 timings, with **both median and minimum ratios ≥1.20**. B1 and E2 are sensitivity comparators. The proposed nominal-95% bootstrap is **rejected as uncalibrated**; the rule makes no 95% coverage assertion.

This record replaces neither the v005–v009 historical results nor their freeze records. The ratified values are consolidated in the two FINAL documents without conflicting earlier draft/addendum language.

## Execution barrier

**NO 3×3 W>0 experiment is authorized by this record.** Before any separate execution authorization, verify the deployed runner's exact options, compiler build, hash manifest, frozen inputs and guard status. The full target spectrum and Δ_nonG must remain withheld until that authorization. Any conformance mismatch blocks execution and requires a dated additive amendment.

## Hash and freeze limitations

The filenames and hashes certify the attached document bytes, not filesystem read-only status and not the state of the user's D: drive. The record is a standalone scientific freeze; do not silently alter any earlier frozen file or modify GitHub.

**Current state:** SPEC_FINAL_HASHED / PREREG_FINAL_HASHED / PRIMARY_NOT_AUTHORIZED.
