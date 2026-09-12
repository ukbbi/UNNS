# Baker Flux-Tube Extension QC

Fourth diagnostic for the UNNS + color confinement investigation.

This is a quality-control report, not a final physics interpretation. Its purpose is to separate usable separation-dependent flux-tube profiles from summary rows, paper-defined aggregate rows, and outlier-like profiles before a formal flux-tube extension report is written.

## 1. Input status

- Summary source used: `extension_report_table:/mnt/data/cc_qc_full_work/color_confinement_data_seed_v0_1_3_pointwise_started/reports/03_flux_tube_separation_extension.md`
- Profile-summary rows inspected: 41
- Long pointwise rows available locally: 62
- Components represented: `{"NP": 17, "FULL": 16, "PAPER_DEFINED": 8}`
- QC decision counts: `{"ACCEPT_FOR_TREND": 30, "REVIEW_SEPARATELY": 9, "EXCLUDE_FROM_TREND": 2}`

## 2. QC rules

The QC pass applies conservative rules:

```
ACCEPT_FOR_TREND:
  FULL or NP component; n_points >= 5; valid peak; finite FWHM <= 1.5 fm; no strong local peak outlier.

REVIEW_SEPARATELY:
  PAPER_DEFINED component, unusually wide FWHM, missing FWHM, or peak outlier versus same component/group.

EXCLUDE_FROM_TREND:
  single-point summary row, invalid field/width values, unknown component, or too few data points.
```

The review threshold `FWHM > 1.5 fm` is deliberately permissive: it flags extreme width estimates without removing ordinary broadened profiles.

## 3. QC summary

Trusted trend separation range: **0.723–1.060 fm**.

The trusted rows are suitable for cautious trend plotting only. They are not yet a fitted UNNS law.

## 4. Accepted trend rows

| source_file | component | source_separation_fm | n_points | peak_field_GeV2 | fwhm_estimate_fm | area_trapz_GeV2_fm | qc_decision |
|---|---|---|---|---|---|---|---|
| Ex_FULL_d0.7fm_scaling_normfact.agr | FULL | 0.723 | 21 | 0.386605 | 0.53008 | 0.230694 | ACCEPT_FOR_TREND |
| Ex_FULL_d0.7fm_scaling_normfact.agr | FULL | 0.738 | 31 | 0.343135 | 0.544917 | 0.219357 | ACCEPT_FOR_TREND |
| Ex_FULL-NP_beta7.158d10a.agr | FULL | 0.74 | 31 | 0.343135 | 0.544917 | 0.219357 | ACCEPT_FOR_TREND |
| Ex_FULL_d0.7fm_scaling_normfact.agr | FULL | 0.76 | 29 | 0.35795 | 0.552803 | 0.220812 | ACCEPT_FOR_TREND |
| Ex_FULL_d0.7fm_scaling_normfact.agr | FULL | 0.76 | 29 | 0.365073 | 0.542314 | 0.223304 | ACCEPT_FOR_TREND |
| Ex_FULL_d0.7fm_scaling_normfact.agr | FULL | 0.76 | 21 | 0.342995 | 0.543463 | 0.215645 | ACCEPT_FOR_TREND |
| Ex_FULL_d0.9fm_scaling_normfact.agr | FULL | 0.855 | 29 | 0.272548 | 0.607597 | 0.192042 | ACCEPT_FOR_TREND |
| Ex_FULL_d0.9fm_scaling_normfact.agr | FULL | 0.887 | 29 | 0.278237 | 0.607586 | 0.187296 | ACCEPT_FOR_TREND |
| Ex_FULL_d0.9fm_scaling_normfact.agr | FULL | 0.912 | 29 | 0.296637 | 0.592638 | 0.195319 | ACCEPT_FOR_TREND |
| Ex_FULL_d0.9fm_scaling_normfact.agr | FULL | 0.95 | 21 | 0.242573 | 0.632543 | 0.176965 | ACCEPT_FOR_TREND |
| Ex_FULL_d0.9fm_scaling_normfact.agr | FULL | 0.959 | 31 | 0.226776 | 0.645401 | 0.169512 | ACCEPT_FOR_TREND |
| Ex_FULL_d1.0fm_scaling_normfact.agr | FULL | 1.013 | 21 | 0.229091 | 0.662059 | 0.17374 | ACCEPT_FOR_TREND |
| Ex_FULL_d1.0fm_scaling_normfact.agr | FULL | 1.013 | 29 | 0.236928 | 0.630087 | 0.178546 | ACCEPT_FOR_TREND |
| Ex_FULL_d1.0fm_scaling_normfact.agr | FULL | 1.045 | 29 | 0.195287 | 0.637244 | 0.158899 | ACCEPT_FOR_TREND |
| Ex_FULL_d1.0fm_scaling_normfact.agr | FULL | 1.06 | 29 | 0.214339 | 0.663369 | 0.165928 | ACCEPT_FOR_TREND |
| Ex_NP_d0.7fm_scaling_normfact.agr | NP | 0.723 | 21 | 0.27402 | 0.544289 | 0.170973 | ACCEPT_FOR_TREND |
| Ex_NP_d0.7fm_scaling_normfact.agr | NP | 0.738 | 31 | 0.244566 | 0.551469 | 0.160806 | ACCEPT_FOR_TREND |
| Ex_FULL-NP_beta7.158d10a.agr | NP | 0.74 | 31 | 0.244566 | 0.551469 | 0.160806 | ACCEPT_FOR_TREND |
| Ex_NP_d0.7fm_scaling_normfact.agr | NP | 0.76 | 29 | 0.214398 | 0.617581 | 0.150063 | ACCEPT_FOR_TREND |
| Ex_NP_d0.7fm_scaling_normfact.agr | NP | 0.76 | 29 | 0.244402 | 0.582336 | 0.160543 | ACCEPT_FOR_TREND |
| Ex_NP_d0.7fm_scaling_normfact.agr | NP | 0.76 | 21 | 0.252381 | 0.549384 | 0.161232 | ACCEPT_FOR_TREND |
| Ex_NP_d0.9fm_scaling_normfact.agr | NP | 0.855 | 29 | 0.192298 | 0.651003 | 0.151778 | ACCEPT_FOR_TREND |
| Ex_NP_d0.9fm_scaling_normfact.agr | NP | 0.887 | 29 | 0.21382 | 0.640631 | 0.159606 | ACCEPT_FOR_TREND |
| Ex_NP_d0.9fm_scaling_normfact.agr | NP | 0.912 | 29 | 0.214398 | 0.617581 | 0.150063 | ACCEPT_FOR_TREND |
| Ex_NP_d0.9fm_scaling_normfact.agr | NP | 0.95 | 21 | 0.200931 | 0.656989 | 0.154115 | ACCEPT_FOR_TREND |
| Ex_NP_d0.9fm_scaling_normfact.agr | NP | 0.959 | 31 | 0.198812 | 0.635626 | 0.158066 | ACCEPT_FOR_TREND |
| Ex_NP_d1.0fm_scaling_normfact.agr | NP | 1.013 | 21 | 0.170863 | 0.647646 | 0.106577 | ACCEPT_FOR_TREND |
| Ex_NP_d1.0fm_scaling_normfact.agr | NP | 1.013 | 29 | 0.191971 | 0.673198 | 0.153579 | ACCEPT_FOR_TREND |
| Ex_NP_d1.0fm_scaling_normfact.agr | NP | 1.045 | 29 | 0.125975 | 0.722692 | 0.131811 | ACCEPT_FOR_TREND |
| Ex_NP_d1.0fm_scaling_normfact.agr | NP | 1.06 | 29 | 0.170636 | 0.675694 | 0.143059 | ACCEPT_FOR_TREND |

## 5. Rows requiring review or exclusion

| source_file | component | source_separation_fm | n_points | peak_field_GeV2 | fwhm_estimate_fm | qc_decision | qc_reason |
|---|---|---|---|---|---|---|---|
| Ex_FULL-NP_beta7.158d10a.agr | FULL | 0.738309 | 1 | 0.343135 |  | EXCLUDE_FROM_TREND | summary_or_single_point_row; missing_fwhm |
| Ex_FULL-NP_beta7.158d10a.agr | NP | 0.738309 | 1 | 0.244566 |  | EXCLUDE_FROM_TREND | summary_or_single_point_row; missing_fwhm |
| Ex_NP_d1.0fm_scaling_normfact.agr | NP | 1.033 | 37 | 0.439904 | 2.45802 | REVIEW_SEPARATELY | wide_fwhm>1.5fm; peak_outlier_vs_group_median |
| beta7.158dist13.agr | PAPER_DEFINED | 0.96 | 31 | 0.292766 | 0.645401 | REVIEW_SEPARATELY | paper_defined_profile_class_keep_separate |
| beta6.3942dist789.agr | PAPER_DEFINED | 1.064 | 29 | 0.27671 | 0.663369 | REVIEW_SEPARATELY | paper_defined_profile_class_keep_separate |
| QCD_large_distances.agr | PAPER_DEFINED | 1.216 | 29 | 0.140815 | 0.708268 | REVIEW_SEPARATELY | paper_defined_profile_class_keep_separate |
| beta6.3942dist789.agr | PAPER_DEFINED | 1.216 | 29 | 0.181792 | 0.708268 | REVIEW_SEPARATELY | paper_defined_profile_class_keep_separate |
| QCD_large_distances.agr | PAPER_DEFINED | 1.235 | 28 | 0.562076 | 0.538481 | REVIEW_SEPARATELY | paper_defined_profile_class_keep_separate |
| QCD_large_distances.agr | PAPER_DEFINED | 1.267 | 29 | 0.441594 | 1.27198 | REVIEW_SEPARATELY | paper_defined_profile_class_keep_separate |
| QCD_large_distances.agr | PAPER_DEFINED | 1.368 | 29 | 0.196347 | 4.17106 | REVIEW_SEPARATELY | paper_defined_profile_class_keep_separate; wide_fwhm>1.5fm |
| beta6.3942dist789.agr | PAPER_DEFINED | 1.368 | 29 | 0.253483 | 4.17106 | REVIEW_SEPARATELY | paper_defined_profile_class_keep_separate; wide_fwhm>1.5fm |

## 6. Figures produced

- `fig_baker_qc_peak_trusted.png`
- `fig_baker_qc_width_trusted.png`

## 7. UNNS interpretation boundary

This QC pass does not yet establish route broadening, route weakening, or threshold approach. It only establishes which Baker profiles may be used in the next formal interpretation.

The provisional UNNS reading after QC is:

```
trusted FULL / NP profiles
-> usable localized-route geometry samples

PAPER_DEFINED and wide/outlier profiles
-> keep separate until source conventions and normalization are inspected

single-point summary rows
-> exclude from shape/width/peak trend plots
```

## 8. Next action

Use the accepted FULL and NP rows to write the formal flux-tube extension report only after inspecting the rows marked `REVIEW_SEPARATELY`, especially large-distance and paper-defined profiles.
