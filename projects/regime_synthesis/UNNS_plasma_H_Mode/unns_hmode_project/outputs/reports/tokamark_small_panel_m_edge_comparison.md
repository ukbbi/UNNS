# TokaMark Small-Panel m_edge(t) Comparison

## Purpose

Run and summarize a small multi-shot TokaMark/MAST panel using the same pipeline as the reference shot 12063.

This is the next step after `docs/21_TOKAMARK_CROSS_SHOT_M_EDGE_COMPARISON.md`.

## Panel decision

```text
decision: reference_structurally_strong_but_not_unique
- reference_has_top_panel_structural_score
- reference_has_highest_or_tied_interpretable_positive_count
- reference_result_not_explained_by_lower_missingness
reference shot: 12063
panel size: 5
reference panel rank: 1
```

## Panel summary

|   panel_rank | panel_role   |   shot_id | candidate_class                |   candidate_score |   panel_structural_score |   positive_boundary_margin_fraction |   negative_leakage_margin_fraction |   m_edge_median |   m_edge_max |   interpretable_positive_count |   interpretable_negative_count |   fragile_positive_count |   fragile_negative_count |   missingness_pressure_median |
|-------------:|:-------------|----------:|:-------------------------------|------------------:|-------------------------:|------------------------------------:|-----------------------------------:|----------------:|-------------:|-------------------------------:|-------------------------------:|-------------------------:|-------------------------:|------------------------------:|
|            1 | reference    |     12063 | FULL_PROFILE_EDGE_CANDIDATE    |            97.143 |                 20.8439  |                            0.258216 |                           0.112676 |       0.087961  |     0.475695 |                              8 |                              3 |                        0 |                        0 |                      0.222222 |
|            2 | comparison   |     11876 | CORE_DALPHA_GEOMETRY_CANDIDATE |            72.143 |                 13.1648  |                            0.216015 |                           0.165736 |       0.0156955 |     0.568895 |                              5 |                              7 |                        0 |                        0 |                      0.222222 |
|            3 | comparison   |     11776 | LOW_PRIORITY                   |            58.929 |                  9.91819 |                            0.659656 |                           0.156788 |       0.486177  |     0.727017 |                              4 |                              0 |                        0 |                        3 |                      0.444444 |
|            4 | comparison   |     11768 | PARTIAL_DALPHA_CANDIDATE       |            65.179 |                  4.33617 |                            0.533654 |                           0.230769 |       0.372648  |     0.622713 |                              2 |                              0 |                        0 |                        3 |                      0.333333 |
|            5 | comparison   |     11830 | PROFILE_DALPHA_CANDIDATE       |            81.429 |                  1.78583 |                            0.226064 |                           0.228723 |      -0.0366668 |     0.387901 |                              2 |                              0 |                        2 |                        2 |                      0.222222 |

## Metadata roles

|   shot_id | candidate_class                |   core_required_present |   profile_preferred_present |   edge_activity_present |   supporting_present | missing_core_required                                                     | missing_profile_preferred                     | missing_edge_activity                                             |
|----------:|:-------------------------------|------------------------:|----------------------------:|------------------------:|---------------------:|:--------------------------------------------------------------------------|:----------------------------------------------|:------------------------------------------------------------------|
|     11768 | PARTIAL_DALPHA_CANDIDATE       |                       7 |                           0 |                       2 |                    9 | summary-power_nbi                                                         | thomson_scattering-t_e;thomson_scattering-n_e | nan                                                               |
|     11776 | LOW_PRIORITY                   |                       6 |                           0 |                       2 |                    9 | summary-power_nbi;spectrometer_visible-filter_spectrometer_dalpha_voltage | thomson_scattering-t_e;thomson_scattering-n_e | nan                                                               |
|     11830 | PROFILE_DALPHA_CANDIDATE       |                       8 |                           2 |                       0 |                    9 | nan                                                                       | nan                                           | soft_x_rays-horizontal_cam_lower;soft_x_rays-horizontal_cam_upper |
|     11876 | CORE_DALPHA_GEOMETRY_CANDIDATE |                       8 |                           0 |                       2 |                   10 | nan                                                                       | thomson_scattering-t_e;thomson_scattering-n_e | nan                                                               |
|     12063 | FULL_PROFILE_EDGE_CANDIDATE    |                       8 |                           2 |                       2 |                   10 | nan                                                                       | nan                                           | nan                                                               |

## Pipeline stage status

|   shot_id | stage                | status           |   return_code |
|----------:|:---------------------|:-----------------|--------------:|
|     12063 | one_shot_array_probe | skipped_existing |             0 |
|     12063 | m_edge_t_probe       | skipped_existing |             0 |
|     12063 | trace_inspection     | skipped_existing |             0 |
|     11830 | one_shot_array_probe | skipped_existing |             0 |
|     11830 | m_edge_t_probe       | skipped_existing |             0 |
|     11830 | trace_inspection     | skipped_existing |             0 |
|     11876 | one_shot_array_probe | ok               |             0 |
|     11876 | m_edge_t_probe       | ok               |             0 |
|     11876 | trace_inspection     | ok               |             0 |
|     11768 | one_shot_array_probe | ok               |             0 |
|     11768 | m_edge_t_probe       | ok               |             0 |
|     11768 | trace_inspection     | ok               |             0 |
|     11776 | one_shot_array_probe | ok               |             0 |
|     11776 | m_edge_t_probe       | ok               |             0 |
|     11776 | trace_inspection     | ok               |             0 |

## Interpretation

If the reference shot remains top-ranked or structurally stronger across this small panel, v0.1 passes a stronger specificity test. If weaker shots reproduce the same coherent positive-window structure, v0.1 is probably overbroad and should be revised.

## Bounded claim

This panel comparison is still not physical H-mode validation. It tests whether the normalized UNNS-H Mode margin distinguishes the reference shot from several weaker public TokaMark candidates.

## Next document

```text
docs/
  22_TOKAMARK_SMALL_PANEL_M_EDGE_COMPARISON.md
```