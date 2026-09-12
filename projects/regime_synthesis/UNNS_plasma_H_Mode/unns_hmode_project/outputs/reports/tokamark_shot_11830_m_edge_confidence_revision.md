# TokaMark m_edge Diagnostic-Confidence Revision — Shot 11830

## Purpose

Preserve raw `m_edge(t)` while adding diagnostic confidence and a conservative confidence-weighted margin.

## Summary

|   shot_id | candidate_class          |   candidate_score |   rows |   raw_positive_fraction |   conf_positive_fraction |   raw_negative_fraction |   conf_negative_fraction |   conf_low_confidence_fraction |   m_edge_raw_median |   m_edge_conf_median |   m_edge_raw_max |   m_edge_conf_max |   Q_diag_median |   P_missing_critical_median |   confidence_structural_score |
|----------:|:-------------------------|------------------:|-------:|------------------------:|-------------------------:|------------------------:|-------------------------:|-------------------------------:|--------------------:|---------------------:|-----------------:|------------------:|----------------:|----------------------------:|------------------------------:|
|     11830 | PROFILE_DALPHA_CANDIDATE |            81.429 |    376 |                0.226064 |                        0 |                0.228723 |                 0.510638 |                       0.154255 |          -0.0366668 |            -0.322615 |         0.387901 |          0.175543 |        0.863889 |                    0.111111 |                       -6.4816 |

## Global diagnostic availability

|   has_nbi_global |   has_ip_global |   has_density_global |   has_dalpha_global |   has_softx_lower_global |   has_softx_upper_global |   has_te_global |   has_ne_global |
|-----------------:|----------------:|---------------------:|--------------------:|-------------------------:|-------------------------:|----------------:|----------------:|
|                1 |               1 |                    1 |                   1 |                        0 |                        0 |               1 |               1 |

## Bounded interpretation

This output is not physical H-mode validation. It tests whether the raw structural margin remains interpretable after missing and incomplete diagnostics are penalized.
