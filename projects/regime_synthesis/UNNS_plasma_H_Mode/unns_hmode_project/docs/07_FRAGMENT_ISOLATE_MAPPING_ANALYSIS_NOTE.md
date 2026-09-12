# Fragment-Isolate Mapping — Immediate Analysis Note

## Generated candidate branches

| subset     | variable                  |   component_id | component_role    |   component_size_gaps |   involved_row_count |   involved_shot_count | involved_shots                      |   event_time_min |   event_time_max |
|:-----------|:--------------------------|---------------:|:------------------|----------------------:|---------------------:|----------------------:|:------------------------------------|-----------------:|-----------------:|
| all_events | P_total_aux_candidate_MW  |              1 | singleton_isolate |                     1 |                    2 |                     2 | 68001;69807                         |            1.47  |            2.03  |
| all_events | P_total_candidate_MW      |              1 | singleton_isolate |                     1 |                    2 |                     2 | 68001;68002                         |            1.93  |            2.03  |
| all_events | chi_eff_candidate         |              1 | minor_component   |                     2 |                    3 |                     3 | 67992;68001;69668                   |            1.58  |            2.03  |
| all_events | chi_eff_candidate         |              2 | singleton_isolate |                     1 |                    2 |                     2 | 69668;69807                         |            1.47  |            1.58  |
| all_events | divertor_signal_candidate |              1 | minor_component   |                     3 |                    6 |                     6 | 67990;68000;68003;68632;69891;69892 |            1.838 |            1.96  |
| all_events | divertor_signal_candidate |              2 | minor_component   |                     2 |                    4 |                     4 | 66445;68006;68719;69892             |            1.112 |            1.948 |
| all_events | divertor_signal_candidate |              3 | singleton_isolate |                     1 |                    2 |                     2 | 66445;68207                         |            1.948 |            1.99  |
| all_events | divertor_signal_candidate |              4 | singleton_isolate |                     1 |                    2 |                     2 | 68719;68728                         |            1.669 |            1.917 |
| lh_only    | P_loss_candidate_MW       |              1 | minor_component   |                     2 |                    4 |                     4 | 67992;68007;68206;69895             |            1.117 |            1.93  |
| lh_only    | P_loss_candidate_MW       |              2 | singleton_isolate |                     1 |                    2 |                     2 | 68200;68422                         |            1.757 |            1.763 |
| lh_only    | event_time                |              1 | singleton_isolate |                     1 |                    2 |                     2 | 67986;69913                         |            1.21  |            1.394 |
| lh_only    | event_time                |              2 | singleton_isolate |                     1 |                    2 |                     2 | 66452;69913                         |            1.394 |            1.651 |

## Next analytical use

Open `tcv_suspect_transition_families.csv` and inspect the HIGH-priority rows first. Those rows identify the first candidate TCV transition families behind the STRUC-PERC-I fragmentation signal.