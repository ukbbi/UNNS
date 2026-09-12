# TokaMark Comparison Candidate Selection

## Purpose

Select the next weaker / comparison TokaMark shot to run through the same pipeline as reference shot 12063.

This follows `docs/20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md`.

## Recommended candidate

```text
reference shot:      12063
recommended shot:    11830
candidate class:     PROFILE_DALPHA_CANDIDATE
comparison role:     profile_no_softx_weaker_control
candidate score:     81.429
core required:       8/8
profile preferred:   2/2
edge activity:       0/2
supporting:          9/14
```

## Why this candidate

This is the preferred first comparison because it preserves core + Thomson profile coverage but lacks soft-X edge-activity support. It is weaker than shot 12063 without being diagnostically unusable.

## Run this pipeline

```powershell
python components\tokamark_one_shot_array_probe.py --shot-id 11830 --out-dir outputs\reports
python components\tokamark_m_edge_t_probe.py --shot-id 11830 --out-dir outputs\reports
python components\tokamark_m_edge_trace_inspector.py --input outputs\reports\tokamark_shot_11830_m_edge_t_probe.csv --shot-id 11830 --out-dir outputs\reports
python components\tokamark_cross_shot_m_edge_comparator.py --reference-shot 12063 --comparison-shot 11830 --out-dir outputs\reports
```

## Shortlist

| rank | shot_id | campaign | split_membership | candidate_score | candidate_class | comparison_role | core_required_present | profile_preferred_present | edge_activity_present | supporting_present | missing_core_required | missing_profile_preferred | missing_edge_activity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 46 | 11830 | M5 | train | 81.429 | PROFILE_DALPHA_CANDIDATE | profile_no_softx_weaker_control | 8 | 2 | 0 | 9 | nan | nan | soft_x_rays-horizontal_cam_lower;soft_x_rays-horizontal_cam_upper |
| 49 | 11798 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 50 | 11799 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 51 | 11802 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 52 | 11804 | M5 | val | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 53 | 11805 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 54 | 11806 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 55 | 11807 | M5 | val | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 56 | 11808 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 57 | 11809 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 58 | 11810 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 59 | 11811 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 60 | 11812 | M5 | val | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 61 | 11815 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 62 | 11816 | M5 | val | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 63 | 11817 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 64 | 11818 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 65 | 11819 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 66 | 11820 | M5 | val | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |
| 67 | 11821 | M5 | train | 71.429 | CORE_DALPHA_GEOMETRY_CANDIDATE | core_softx_no_profile_weaker_control | 8 | 0 | 2 | 9 | nan | thomson_scattering-t_e;thomson_scattering-n_e | nan |

## Decision rule

If the comparison shot reproduces the same coherent positive-window pattern as shot 12063, v0.1 is probably overbroad. If it lacks coherent positive windows or shows higher missingness/fragmentation dominance, shot 12063 becomes structurally more meaningful.