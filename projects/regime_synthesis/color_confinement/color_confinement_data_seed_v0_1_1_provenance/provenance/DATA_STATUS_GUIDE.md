# Data Status Guide

Use these tags consistently in all CSV files.

| tag | Meaning |
|---|---|
| `reported_table_row` | A row copied from a table or table-like data in the source. |
| `reported_in_paper` | A numerical value explicitly reported in the source text/equation/result. |
| `reported_summary_value` | A summary value stated in the abstract, conclusion, or summary paragraph. |
| `reported_setup_row_not_pointwise_profile` | Simulation setup metadata only; not the measured profile/curve itself. |
| `digitized_from_figure` | Value extracted from a plot by controlled digitization; needs digitization log. |
| `author_data` | Value taken from author-provided tables, repository, or ancillary files. |
| `derived_from_model` | Value calculated from a model/equation; must cite equation and calculation script. |
| `queued_not_data` | Placeholder row marking a value to obtain; not a data row. |
| `acquisition_target_not_data` | Queue item specifying what to collect next. |

Do not mix `queued_not_data` rows with actual measurement rows during analysis.
