# PROOF_AUDIT — GIG_MANUSCRIPT_v002 (carried over from v001; statement labels are mapped in THEOREM_CROSSWALK_v002.md and V001_TO_V002_MAP.md)
Status vocabulary: analytic (complete proof in text) / computer-assisted / finite-exact / bounded / conjectural / falsified. "M" = independently re-derived by this manuscript's verifier (verify/gigmini.py + run_checks*.py). "NOT_RERUN" = inherited, certificate named.

| Result | Status | Hand proof? | Re-derived (M)? | Gap |
|---|---|---|---|---|
| Lemma F (valuation criterion) | analytic | yes | M | — |
| thm:closure, thm:block, cor:CP | analytic | yes | M (cube property) | — |
| thm:face-threshold | analytic | yes | M | — |
| thm:swap-reconstruction | analytic | yes | — | — |
| thm:skeleton (T15) | analytic modulo enumeration | partial | M (6-cycles k=4,5,6) | 6-cycle classification only enumerated, k ≤ 8; no uniform proof |
| thm:face-recognition | T20a analytic; T20b computer-assisted k≤7; T20d open | partial | — | T20b NOT_RERUN; T20d unproved |
| thm:hole-survival, anchor (z, φ) | analytic / finite-exact | yes | M | — |
| thm:exact-survival (PS-5) | finite-exact | no (finite statement) | M (B0..B3 minimal; 400/400 random agree) | count 589,839 not recounted |
| prop:gate-nec (PS-3′) | finite-exact refutation | — | M (results3.json) | strong gate necessity is FALSIFIED |
| prop:CRT | analytic | yes | — | — |
| thm:AT1 | analytic | yes | M (instances) | — |
| Atlas (32 classes), held-out record | bounded / finite-exact | no | NOT_RERUN | closure open |
| LT-0, LT-1, LT-2, FI-1, FI-3, J-1, J-2, J-6 | analytic | yes | M | — |
| LT-3 (obstructed 4-faces), FI-5/6, J-3..5 | finite-exact | no | partly M | — |
| LT-6 / ND-1 (general non-degeneracy) | open | no | — | 554 pairs finite-exact only |
| J-7 | open | no | — | — |
| HL-3 | bounded | no | NOT_RERUN | — |
| thm:obs-ladder, thm:profile | analytic (ladder restricted to prefix-defined, k ≤ 8) | yes | partly M | scope narrowed |
| thm:radius2 + moments | analytic | yes | M | — |
| W1–W6 witnesses | finite-exact | — | M (W1,W2,W5,W6) | W3, W4 inherited |
| Anchored window counts | finite-exact | — | M | GI-8 (injectivity in general) unproved |
| Plug-in/out-of-sample, H6 test | bounded | — | NOT_RERUN | S_A falsified; (Q,S2) general principle falsified |
| thm:AD | analytic given Alexander duality | yes | M (random) | — |
| thm:nerve | analytic given nerve theorem | yes | M (instances; all 290 positives) | — |
| thm:barmak, cor:core-suffices | classical + analytic | yes | M (cores of all 290 positives) | D21 table NOT_RERUN |
| thm:pairwise (k = 6) | computer-assisted | partial | M (F1 30, F2 435, F3 4060) | F1, F2 connectedness: no human proof |
| prop:triple (sharpness) | finite-exact | — | M (N = 674, β = (1,2,5,0,0,0)) | — |

## Discharge of "unproved" items listed in THEOREM_CROSSWALK
T20d, T21c, PS-3 (universal), LT-6 (all cycles), J-7, GI-8 — none proved; each is stated in the text as open or as finite-exact only. Nothing is claimed beyond its status.

## NOT_RERUN
Six-label census (346,859 source regimes), seven-label scan of 1,560,780 contents, HL-3 search, D21 table, held-out round R5, atlas rounds, 72^r for r = 8..10. Certificates named in app:sources.

## Corrections carried
18,980-regime gate claim refuted as a general statement (rem:gate-correction); (Q,S2) principle falsified; S_A falsified; ladder β1 claim narrowed.
