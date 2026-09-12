# Color Confinement Data Seed v0.1.1 — Provenance Fixed

This is a small, source-indexed seed data pack for the UNNS + color confinement investigation.

It is **not** a full raw lattice-data repository yet. It contains:

- directly reported ensemble/table rows,
- directly reported string-breaking threshold rows,
- directly reported string-tension summary,
- flux-tube simulation setup rows,
- a strict queue for the actual pointwise data still needed.

Core UNNS target:

```
internal colored constituent -> forbidden external isolation -> route tension -> threshold repair -> admissible color-neutral composite
```

## Files

- `source_registry.csv` — canonical source table with URL, arXiv ID, DOI, publication URL, and intended use.
- `SOURCE_PROVENANCE.md` — human-readable source map and row-traceability rule.
- `DATA_STATUS_GUIDE.md` — allowed provenance/status tags.
- `static_QQbar_ensemble_metadata_seed.csv` — source-indexed ensemble metadata seed rows.
- `string_breaking_thresholds_seed.csv` — reported string-breaking thresholds plus explicit queued rows for missing physical-point thresholds.
- `string_tension_seed.csv` — reported physical-point string-tension seed row.
- `flux_tube_simulation_summary_seed.csv` — simulation setup rows only; not pointwise field profiles.
- `next_data_acquisition_queue.csv` — next missing data, explicitly marked as acquisition targets.
- `manifest.json` — package metadata.

## Source provenance

Every data/queue row now carries, directly or through `source_registry.csv`:

```
source_id
source_url
arxiv_id
doi
publication_url
source_location
row_provenance
```

Primary sources:

1. `Bulava2019_string_breaking` — Bulava et al. 2019, *String breaking by light and strange quarks in QCD*, arXiv:1902.04006, DOI: 10.1016/j.physletb.2019.05.018.
2. `Bulava2024_mass_dependence` — Bulava et al. 2024, *The quark-mass dependence of the potential energy between static colour sources in the QCD vacuum with light and strange quarks*, arXiv:2403.00754, DOI: 10.1016/j.physletb.2024.138754.
3. `Baker2024_flux_tube_full_QCD` — Baker et al. 2024/2025, *Unveiling the flux tube structure in full QCD*, arXiv:2409.20168, DOI: 10.1140/epjc/s10052-024-13725-2.
4. `Cardoso2013_SU3_flux_tube` — Cardoso et al. 2013, *Inside the SU(3) quark-antiquark QCD flux tube: screening versus quantum widening*, arXiv:1302.3633.

## Strict interpretation

Do not treat this as completed raw data. The next required data are pointwise `V_n(r)` / `E_n(r)` and pointwise chromoelectric field profiles.

Current seed content is suitable for:

```
source mapping
reported-threshold tracking
ensemble setup tracking
planning pointwise extraction
```

Current seed content is **not** sufficient for:

```
fitting a new potential curve
claiming a new string-breaking distance
computing a UNNS boundary-pressure proxy
publishing a quantitative confinement result
```
