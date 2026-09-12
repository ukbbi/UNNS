# TCV Fragment-Isolate Mapping Report

## Purpose

This report maps STRUC-PERC-I hard-fragmenting scalar variables back to the TCV event rows and shots adjacent to isolated or non-giant gap components.

## Method

For each target variable and each subset (`all_events`, `lh_only`), the script sorts unique scalar values, constructs the gap vector Δ, rebuilds the full pairwise gap graph at κ = 1 using ε = IQR(Δ), identifies giant and non-giant components, and maps each gap back to the lower/upper source rows.

## Hard-fragmenting target variables

No hard-fragmenting target variables were found in the supplied STRUC-PERC-I result files.

## Non-giant components requiring inspection

| subset     | variable                  |   component_id | component_role    |   component_size_gaps |   involved_row_count |   involved_shot_count | involved_shots                      |   event_time_min |   event_time_max |
|:-----------|:--------------------------|---------------:|:------------------|----------------------:|---------------------:|----------------------:|:------------------------------------|-----------------:|-----------------:|
| all_events | P_loss_candidate_MW       |              1 | minor_component   |                     2 |                    4 |                     4 | 67992;68001;68206;68207             |            1.91  |            2.03  |
| all_events | P_loss_candidate_MW       |              2 | singleton_isolate |                     1 |                    2 |                     2 | 68206;69807                         |            1.47  |            1.91  |
| all_events | P_total_aux_candidate_MW  |              1 | singleton_isolate |                     1 |                    2 |                     2 | 68001;69807                         |            1.47  |            2.03  |
| all_events | P_total_candidate_MW      |              1 | singleton_isolate |                     1 |                    2 |                     2 | 68001;68002                         |            1.93  |            2.03  |
| all_events | chi_eff_candidate         |              1 | minor_component   |                     2 |                    3 |                     3 | 67992;68001;69668                   |            1.58  |            2.03  |
| all_events | chi_eff_candidate         |              2 | singleton_isolate |                     1 |                    2 |                     2 | 69668;69807                         |            1.47  |            1.58  |
| all_events | divertor_signal_candidate |              1 | minor_component   |                     3 |                    6 |                     6 | 67990;68000;68003;68632;69891;69892 |            1.838 |            1.96  |
| all_events | divertor_signal_candidate |              2 | minor_component   |                     2 |                    4 |                     4 | 66445;68006;68719;69892             |            1.112 |            1.948 |
| all_events | divertor_signal_candidate |              3 | singleton_isolate |                     1 |                    2 |                     2 | 66445;68207                         |            1.948 |            1.99  |
| all_events | divertor_signal_candidate |              4 | singleton_isolate |                     1 |                    2 |                     2 | 68719;68728                         |            1.669 |            1.917 |
| all_events | event_time                |              1 | minor_component   |                     2 |                    4 |                     4 | 66452;69668;69807;69913             |            1.394 |            1.651 |
| all_events | event_time                |              2 | singleton_isolate |                     1 |                    2 |                     2 | 69913;73917                         |            1.22  |            1.394 |
| all_events | event_time                |              3 | singleton_isolate |                     1 |                    2 |                     2 | 69668;69807                         |            1.47  |            1.58  |
| lh_only    | P_loss_candidate_MW       |              1 | minor_component   |                     2 |                    4 |                     4 | 67992;68007;68206;69895             |            1.117 |            1.93  |
| lh_only    | P_loss_candidate_MW       |              2 | singleton_isolate |                     1 |                    2 |                     2 | 68200;68422                         |            1.757 |            1.763 |
| lh_only    | divertor_signal_candidate |              1 | minor_component   |                     2 |                    4 |                     4 | 66445;68006;68719;69892             |            1.112 |            1.948 |
| lh_only    | divertor_signal_candidate |              2 | minor_component   |                     2 |                    4 |                     4 | 68000;68003;68632;69892             |            1.838 |            1.931 |
| lh_only    | divertor_signal_candidate |              3 | singleton_isolate |                     1 |                    2 |                     2 | 66445;67990                         |            1.909 |            1.948 |
| lh_only    | divertor_signal_candidate |              4 | singleton_isolate |                     1 |                    2 |                     2 | 68719;68728                         |            1.669 |            1.917 |
| lh_only    | event_time                |              1 | singleton_isolate |                     1 |                    2 |                     2 | 67986;69913                         |            1.21  |            1.394 |
| lh_only    | event_time                |              2 | singleton_isolate |                     1 |                    2 |                     2 | 66452;69913                         |            1.394 |            1.651 |

## Interpretation

Rows adjacent to non-giant components are the first candidates for transition-family inspection. They are not automatically errors or outliers; in UNNS terms they are candidate branch points or isolated admissibility corridors in the transition corpus.

## Generated outputs

- `tcv_fragment_component_summary.csv`
- `tcv_fragment_gap_map.csv`
- `tcv_suspect_transition_families.csv`
- `tcv_fragment_isolate_mapping_summary.json`