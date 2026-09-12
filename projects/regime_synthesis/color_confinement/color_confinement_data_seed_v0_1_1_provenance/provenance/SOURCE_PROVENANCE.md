# Source Provenance and Row-Traceability

This pack is a small seed for the UNNS + color confinement investigation. It is **not** a complete raw lattice-data repository.

Every row must be traceable to a source. No future row should be accepted unless it contains:

1. `source_id`
2. `source_url` / arXiv identifier / DOI when available
3. `source_location` such as table, figure, equation, abstract, conclusion, ancillary file, or extraction target
4. `row_provenance`, one of: `reported_table_row`, `reported_in_paper`, `reported_summary_value`, `reported_setup_row_not_pointwise_profile`, `digitized_from_figure`, `author_data`, `derived_from_model`, `queued_not_data`, or `acquisition_target_not_data`
5. a clear distinction between reported data, derived values, and extraction targets

## Primary source map

| source_id | Source | Use in this pack | Status |
|---|---|---|---|
| `Bulava2019_string_breaking` | Bulava et al., *String breaking by light and strange quarks in QCD*, arXiv:1902.04006; DOI: 10.1016/j.physletb.2019.05.018 | reported string-breaking distances; static Q-Qbar spectrum extraction target | primary QCD evidence source |
| `Bulava2024_mass_dependence` | Bulava et al., *The quark-mass dependence of the potential energy between static colour sources in the QCD vacuum with light and strange quarks*, arXiv:2403.00754; DOI: 10.1016/j.physletb.2024.138754 | ensemble metadata; reported physical-point string tension; physical-point threshold extraction target | primary QCD evidence source |
| `Baker2024_flux_tube_full_QCD` | Baker et al., *Unveiling the flux tube structure in full QCD*, arXiv:2409.20168; DOI: 10.1140/epjc/s10052-024-13725-2 | flux-tube simulation setup rows; pointwise chromoelectric-field profile acquisition target | primary QCD evidence source |
| `Cardoso2013_SU3_flux_tube` | Cardoso et al., *Inside the SU(3) quark-antiquark QCD flux tube: screening versus quantum widening*, arXiv:1302.3633 | pure-gauge SU(3) flux-tube reference/control extraction target | secondary/control source |

## Strict interpretation

The CSV files in this seed pack currently contain source-indexed reported rows and extraction targets. They do **not** yet contain complete pointwise static-potential curves or complete pointwise chromoelectric field profiles.

The next required data are:

- pointwise `E0(r)`, `E1(r)`, `E2(r)` static-source energy levels;
- pointwise nonperturbative longitudinal chromoelectric field profiles;
- author data, ancillary files, or controlled digitization records for all pointwise values.
