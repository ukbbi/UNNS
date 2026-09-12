# 02 — Data Inventory: Public / Candidate Sources

This is an initial inventory. Raw data are not included in this starter archive.

## A. TCV L-H transition database — Zenodo

- Status: public dataset record.
- Use: likely first candidate for L-H threshold metadata and transition classification.
- Associated topic: L-H power threshold for neutral beam heated plasmas with Deuterium, Hydrogen, Helium and mixed ion species in TCV.
- Fit for UNNS: good for event-level transition threshold analysis; may be limited for high-frequency turbulence/pedestal dynamics unless diagnostic time series are included.
- URL: https://zenodo.org/records/14996664

## B. FAIR MAST — UKAEA

- Status: public-facing repository.
- Use: experimental diagnostic data from MAST M05-M09 campaigns.
- Access pattern: JSON API for shot metadata plus public S3 bucket with Zarr-formatted diagnostic data.
- Fit for UNNS: strong candidate for time-series pipeline because it exposes diagnostic data, not only paper-level transition tables.
- URL: https://www.ukaea.org/service/fair-mast/

## C. MAST H-mode threshold studies

- Status: open paper with described analysis and figures/tables.
- Use: L-H and H-L threshold dependencies, pedestal parameters, X-point height dependence.
- Fit for UNNS: good for defining candidate edge variables and failure tests.
- URL: https://www.mdpi.com/2571-6182/2/3/24

## D. ITPA global H-mode confinement database

- Status: important literature/database reference; public data access must be verified.
- Use: global confinement scaling, multi-machine comparison, H98-style benchmarking.
- Fit for UNNS: useful for later cross-device validation of confinement-margin ideas.
- Initial source: "The updated ITPA global H-mode confinement database: description and analysis."

## E. TCV confinement-state classification literature

- Status: literature and possible data lead.
- Use: labels for L, D, H, and ELM detection; machine-learning baselines.
- Fit for UNNS: useful baseline for comparing UNNS transition features against pure ML state classification.

## F. DIII-D / DBS / ELM forecasting literature

- Status: promising literature; data access may require collaboration or database credentials.
- Use: pre-ELM forecasting and edge-flow/turbulence signals.
- Fit for UNNS: excellent later test of boundary-overload index if data access is available.

## First acquisition priority

1. Zenodo TCV database: easy public starting point.
2. FAIR MAST: richer but requires adapter work for JSON/Zarr.
3. MAST paper tables/figures: good for formal variable selection and sanity tests.
4. ITPA database/literature: later cross-machine scaling validation.
