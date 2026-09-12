# TCV Suspect Shot Review

## Purpose

This report creates a focused one-row-per-shot review table for the recurrent TCV shots identified by the fragment/isolate mapping stage. It does not run another chamber. It maps previously detected fragmentation back to physical shot variables.

## Reviewed shots

69807, 68001, 69668, 69892, 66445, 68719, 69913, 67992, 68206

## Fragment-variable recurrence

| Fragment variable | Shot count |
|---|---:|
| `P_loss_candidate_MW` | 4 |
| `chi_eff_candidate` | 4 |
| `divertor_signal_candidate` | 3 |
| `event_time` | 3 |
| `P_total_aux_candidate_MW` | 2 |
| `P_total_candidate_MW` | 1 |

## Preliminary branch tags

| Branch tag | Shot count |
|---|---:|
| `power_balance_branch` | 4 |
| `transport_branch` | 4 |
| `edge_divertor_response_branch` | 3 |
| `timing_branch` | 3 |

## Focused shot table

|   SHOT | TIME        |   canonical_event_rows |   fragment_count | fragment_variables                                                                  | fragment_tags                                       |   P_LH_candidate_MW |   P_total_candidate_MW |   P_loss_candidate_MW |   n_e_1e20_m3 |   helium_fraction_candidate |   chi_eff_candidate |   divertor_signal_candidate |
|-------:|:------------|-----------------------:|-----------------:|:------------------------------------------------------------------------------------|:----------------------------------------------------|--------------------:|-----------------------:|----------------------:|--------------:|----------------------------:|--------------------:|----------------------------:|
|  69807 | 1.470;1.940 |                      2 |                5 | P_loss_candidate_MW;P_total_aux_candidate_MW;chi_eff_candidate;event_time           | power_balance_branch;transport_branch;timing_branch |            0.218104 |               0.950818 |              0.777786 |      0.267367 |                   0.024961  |            2.61934  |                   0.0186899 |
|  68001 | 1.159;2.030 |                      2 |                4 | P_loss_candidate_MW;P_total_aux_candidate_MW;P_total_candidate_MW;chi_eff_candidate | power_balance_branch;transport_branch               |            0.345337 |               1.10961  |              0.868754 |      0.506799 |                   0.106772  |            2.2335   |                   0.0888251 |
|  69668 | 1.580       |                      1 |                4 | chi_eff_candidate;event_time                                                        | transport_branch;timing_branch                      |            0.216071 |               0.744312 |              0.779358 |      0.265899 |                   0.0251548 |            3.04184  |                   0.0187466 |
|  69892 | 1.206;1.838 |                      2 |                4 | divertor_signal_candidate                                                           | edge_divertor_response_branch                       |            0.373524 |               0.963662 |              0.719128 |      0.565601 |                   0.0402663 |            1.62383  |                   0.0894552 |
|  66445 | 1.071;1.948 |                      2 |                4 | divertor_signal_candidate                                                           | edge_divertor_response_branch                       |            0.381468 |               0.913125 |              0.594634 |      0.571467 |                   0.0251698 |            1.37635  |                   0.0945756 |
|  68719 | 1.669       |                      1 |                4 | divertor_signal_candidate                                                           | edge_divertor_response_branch                       |            0.47704  |               0.671406 |                       |      0.797745 |                   0.0254265 |                     |                   0.138759  |
|  69913 | 1.394       |                      1 |                4 | event_time                                                                          | timing_branch                                       |            0.272318 |               0.575489 |              0.392938 |      0.362429 |                   0.0250545 |            0.930461 |                   0.0142754 |
|  67992 | 1.112;1.930 |                      2 |                3 | P_loss_candidate_MW;chi_eff_candidate                                               | power_balance_branch;transport_branch               |            0.339726 |               1.01611  |              0.80207  |      0.493965 |                   0.0254658 |            2.08833  |                   0.0741081 |
|  68206 | 1.004;1.910 |                      2 |                3 | P_loss_candidate_MW                                                                 | power_balance_branch                                |            0.420383 |               0.923097 |              0.739229 |      0.672398 |                   0.0715177 |            1.76527  |                   0.0510742 |

## Interpretation

The reviewed shots form a concentrated candidate set. Most are not isolated through geometry alone; they are recurrently linked to power-balance, transport, timing, and edge/divertor-response variables. This is consistent with the working UNNS-H Mode hypothesis that H-mode access is a boundary-route organization problem rather than a single total-power threshold problem.

## Caution

This table identifies candidate transition families. It does not prove that these shots are faulty, anomalous, or physically causal. The next step is manual physical review of the rows and, if needed, dataset-specific diagnostics from the source notebook/README.
