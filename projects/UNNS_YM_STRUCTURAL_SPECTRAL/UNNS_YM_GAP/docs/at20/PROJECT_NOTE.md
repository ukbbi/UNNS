# AT20 placement note

This directory documents the Athenodorou–Teper 2020 corpus used as the first
primary Yang–Mills spectral dataset (`YM-1A`) in `UNNS_YM_GAP`.

## Placement

- Immutable received archive: `data/raw/at20.zip`
- ArXiv source PDF and raw extracted tables: `data/raw/at20/`
- Publisher JHEP PDF: `data/raw/at20/at20_jhep.pdf`
- Normalized/derived tables: `data/derived/at20/`
- Metadata and QA: `docs/at20/`
- Reproducibility scripts: `scripts/at20/`

## Source identity check

The project copy `data/raw/at20/at20.pdf` is byte-identical to the user-uploaded
`2007.06422v2.pdf`.

SHA-256:

`f0eb6406bf49a00d376c0be25917173426c826050046a1bf0f32987895de23d0`

The publisher PDF is preserved separately and has SHA-256:

`af40f084cf4f4624224af726d0bb4822e449b161b03ce38972077023cbd0ca7c`

The original Work-produced package remains untouched as `data/raw/at20.zip`.
Its original manifest is preserved as `docs/at20/manifest_source.json`.

## Important data note

The published discrepancy at beta = 5.8941 is intentionally preserved:
Table 1 reports `0.7991(92)` while the corresponding Table 8 A1++ ground-state
entry reports `0.799(10)`. Neither value is silently overwritten.

The derived corpus contains 443 lattice glueball masses, 59 continuum mass
ratios, 8 flux-tube energies, and 8 principal lattice refinement levels.
