# CLAIM_EVIDENCE — GIG_MANUSCRIPT_v002 (carried over from v001; statement labels are mapped in THEOREM_CROSSWALK_v002.md and V001_TO_V002_MAP.md)
Each headline claim, its evidence class, and where the evidence lives.

| Claim | Evidence class | Location |
|---|---|---|
| Histories of 72, decomposition | exact re-derivation | verify/results.json ch3_* |
| 72^r counts, r ≤ 7 | exact re-derivation | results2.json ch3_72r_counts_to_7 |
| 72^r, r = 8..10 | inherited NOT_RERUN | GIG-INFO v001 |
| Anchor certificate (z: 96 faces, φ: 6 hexagons; 540 three-faces) | exact + certificate | results2.json ch6_*, verify/inherited/H2_anchor_A.json, app:certs |
| Thresholds 288 / 432; octahedra | exact | results2.json ch6_thresholds |
| Exact survival criterion B0..B3 | exact, minimality checked; 400/400 random agree | results2.json ch6_PS5_* |
| Gate-1/3 necessity refuted | exact counterexamples | results3.json |
| Lift identities, J-1/J-2 | exact | results4.json, results.json ch8_* |
| Radius-2 identity | proof + exact check | results.json ch9_radius2_identity |
| Witnesses W1, W2, W5, W6 | exact | results.json ch10_witnesses |
| Anchor windows | exact | results.json ch10_anchor_* |
| Nerve theorem, Alexander duality | proof + exact instances | results.json ch12_*, results5.json |
| 290 positives certified, cores | exact | results5.json, standalone_verify_manuscript_run.txt |
| Tamper test | exact | tamper_test.txt |
| F1 (30), F2 (435), F3 (4060); triple N = 674 | exact | results.json ch14_* |
| Census (346,859 regimes; 158 hole regimes, 52/59 explained) | inherited NOT_RERUN | GIG-I v005/v006 |
| Atlas 32 classes, held-out prediction | inherited NOT_RERUN | GIG-I v005 S3, v006 |
| D21 table (219,145 / 151) | inherited NOT_RERUN | GIG-INFO v005 |
| Pre-registered H6 outcomes | inherited NOT_RERUN | GIG-INFO v004/v005 |
| Figures 4(b), 6 | registered inherited data, not recomputed | figures/make_figures.py |
| Figures 5, 7, 8 | recomputed from exact data | figures/*_data.json |

No claim relies on floating-point computation.

Note (final closure): the claim "the uncoloured graph does not determine beta_2" is NOT made; see FINAL_CLOSURE_v002.md item 5.
