# Chamber Inputs — UNNS + Color Confinement
These files are chamber-ready ordered numeric ladders generated from QC-clean confinement diagnostics.
## Source inputs
- Trusted Baker flux profile summary: `C:\Users\igorc\Desktop\UNNS_SUBSTRATE(desktop)\TRANSFER\Bulk_2\REGIME_SYNTHESIS\Color confinement\color_confinement_data_seed_v0_1_1_provenance\reports\baker_flux_profile_trusted_summary.csv`
- Repair-window static gaps: `C:\Users\igorc\Desktop\UNNS_SUBSTRATE(desktop)\TRANSFER\Bulk_2\REGIME_SYNTHESIS\Color confinement\color_confinement_data_seed_v0_1_1_provenance\reports\repair_threshold_window_static_gaps.csv`

## Rule
Each chamber input CSV is deliberately single-column with header `value`. Do not add metadata columns to these ladder files, because STRUC-I and STRUC-PERC-I ingest numeric ladders. Provenance is kept in `chamber_input_manifest.csv`.

## Generated ladder files
- `flux_FULL_peak_trusted_ladder.csv` — FULL flux-tube central/peak route-intensity ladder (15 values; GeV^2)
- `flux_NP_peak_trusted_ladder.csv` — nonperturbative peak route-intensity ladder (15 values; GeV^2)
- `flux_FULL_width_trusted_ladder.csv` — FULL flux-tube transverse-width ladder (15 values; fm)
- `flux_NP_width_trusted_ladder.csv` — nonperturbative transverse-width ladder (15 values; fm)
- `flux_FULL_area_trusted_ladder.csv` — FULL integrated transverse route-strength ladder (15 values; GeV^2 fm)
- `flux_NP_area_trusted_ladder.csv` — nonperturbative integrated transverse route-strength ladder (15 values; GeV^2 fm)
- `static_gap01_repair_window_ladder.csv` — repair-window V1-V0 channel-competition ladder (17 values; GeV)
- `static_gap12_repair_window_ladder.csv` — repair-window V2-V1 channel-competition ladder (17 values; GeV)
- `boundary_pressure_proxy_ladder_SCHEMA.csv` — placeholder for future boundary-pressure proxy ladder; not used as chamber input yet (0 values; dimension depends on proxy)

## How to run
1. Upload up to six flux ladders into STRUC-I first.
2. Export STRUC-I JSON/CSV.
3. Run STRUC-PERC-I on the same ladder CSV files.
4. Compare STRUC-I admissibility class with STRUC-PERC-I realizability/connectivity class.

## Boundary
These files are derived chamber inputs, not raw QCD data. They use the QC-accepted FULL/NP rows only. REVIEW_SEPARATELY rows are not mixed into these ladders.
