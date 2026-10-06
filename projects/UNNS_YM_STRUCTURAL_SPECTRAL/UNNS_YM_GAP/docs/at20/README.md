# AT2020 SU(3) glueball tables for UNNS_YM_GAP

Extraction of Tables 1, 7-13 and 14 of A. Athenodorou and M. Teper,
*The glueball spectrum of SU(3) gauge theory in 3+1 dimensions*,
JHEP 11 (2020) 172, DOI https://doi.org/10.1007/JHEP11(2020)172.

**Source limitation:** the PDFs attached to the earlier chat were not available
in this workspace. This package uses the public author manuscript
https://arxiv.org/pdf/2007.06422v2 (20 October 2020), downloaded on
2026-09-29. It has not been compared with the missing uploads or with the
publisher's typeset PDF. The exact PDF bytes are included and pinned by SHA-256.
The extraction is complete for the requested tables in that manuscript.

## Install in the project

Extract `at20.zip` to a staging folder. Merge its `data/raw` and `data/derived`
folders into `UNNS_YM_GAP/data/raw` and `UNNS_YM_GAP/data/derived`. Keep the
`at20` folder intact if you want to run the supplied reproduction commands;
the script locates data relative to its parent folder. Keep this README,
`source.json`, `notes.json`, `schema.json`, `counts.json`, `qa.json` and
`manifest.json` with the package as its provenance record. No synced files
under `sources/` were changed.

All basenames are short ASCII Windows-safe names. CSVs use UTF-8 without a BOM,
commas, decimal points and LF line endings. JSON metadata is UTF-8. Numeric
fields are unquoted numeric text where possible; import `beta`, identifiers,
`raw` and lattice notation as text to retain trailing zeros. Uncertainties
have their own columns, so no Excel-specific formulas are required.

## Files

| File | Rows | Meaning |
| --- | ---: | --- |
| `data/raw/at20.pdf` | 75 pages | Exact public arXiv v2 source |
| `data/raw/at_t01.csv` | 8 | Table 1 original numerical tokens and lattice text |
| `data/raw/at_t07_13.csv` | 564 | Tables 7-13 printed cells, including 113 blank cells and 8 flux energies |
| `data/raw/at_t14.csv` | 76 | Table 14 printed cells, including 17 blank cells |
| `data/derived/at_lat.csv` | 8 | Main ensembles, plaquette, scale and Table 1 mass gap |
| `data/derived/at_aux.csv` | 10 | Auxiliary Table 1 lattices, one row per lattice |
| `data/derived/at_mass.csv` | 443 | Reported lattice glueball masses `aM` |
| `data/derived/at_cont.csv` | 59 | Reported continuum ratios `M/sqrt(sigma)` |
| `data/derived/at_flux.csv` | 8 | Winding-flux-tube energies `aE_l` |
| `data/derived/at_cov.csv` | 160 | Eight ensembles x twenty cubic/parity/charge channels, including absent channels |

The mass counts by beta are 5, 10, 40, 62, 71, 80, 85, 90 in increasing beta
order. Counts exclude winding-flux energies. The continuum table has four
starred poor-fit results. `manifest.json` records sizes, hashes and CSV row
counts for all package files except the manifest itself; the ZIP has no
self-referential checksum.

## Data interpretation

- `R` is a cubic/octahedral irrep, not continuum spin J. `P` and `C` are separate
  signs; e.g. `channel=A1++`. No speculative spin assignment is added.
  `irrep_dim` is 1 for A1/A2, 2 for E and 3 for T1/T2. Do not expand a listed
  mass into independent observations using this degeneracy.
- `slot` is the one-based printed row within the channel block; `state_index`
  is `slot-1`. Preserve this ordering. Values are not sorted by magnitude;
  a higher printed row can have a lower central value. Matching slot numbers
  at different beta, or between lattice and continuum tables, does not prove
  an unambiguous state correspondence.
- `value` and `uncertainty` preserve the printed precision. For example,
  `0.3474(22)` becomes `0.3474` and `0.0022`, while `7.38(11)` becomes `7.38`
  and `0.11`. Errors are the authors' quoted errors; no confidence interval,
  covariance matrix, systematic-error completion or statistical independence
  is inferred. `raw` keeps the original numeric token, including stars/typos.
- Main Table 1 lattice dimensions describe the spectrum/string-tension
  ensembles. Auxiliary lattices are listed separately and are not additional
  mass measurements. Their use is collectively finite-volume and/or topology;
  Table 1 alone does not assign an exact purpose to every auxiliary lattice.
- All tabulated quantities here are dimensionless. Table 1 `a_sqrt_sigma`
  means `a*sqrt(sigma)`, not `a*sigma`. Table 14 is `M/sqrt(sigma)`, not a
  ratio to the scalar glueball. The lattice values `aM` tend to shrink under
  refinement even when a physical mass stays finite; do not interpret that
  shrinkage alone as closing the physical mass gap.
- A raw `status=blank` means the printed cell is empty, not zero. Such cells
  are excluded from normalized measurement CSVs. `at_cov.csv` also makes
  wholly unlisted channels explicit. It does not invent missing excitations.
- `poor_fit=1` retains Table 14's star: chi-squared per degree of freedom
  greater than 2.5. Zero means no such mark, not proof of a good fit. The
  table does not supply exact fit statistics, fit ranges or cross-correlations.
- These are published spectral estimates, not raw correlators or correlation
  matrices. No reconstructed correlator, continuum refit, propagated ratio
  uncertainty or UNNS boundary claim is part of this extraction.

## Source issues retained

`notes.json` lists the precise affected cells and source context.

1. Table 11 T2++, slot 2 prints `1,0247(52)`. The normalized central value is
   `1.0247`, uncertainty `0.0052`; the printed comma is retained in `raw`.
2. Table 8 A2--, slot 1 prints `2.10(12`, and Table 12 T2++, slot 5 prints
   `0.974(12`. Missing closing parentheses are interpreted only in the
   numeric fields: `2.10 +/- 0.12` and `0.974 +/- 0.012`. These are editorial
   normalizations, not author-confirmed errata.
3. At beta 5.8941 Table 1 has `0.7991(92)` whereas Table 8 A1++, slot 1 has
   `0.799(10)`. Both are retained as separate source values. Neither replaces
   the other. All other Table 1 ground-state tokens agree with Tables 7-13.
4. The paper discusses possible finite-volume ditorelon contamination in
   excited A1++/E++ levels. No lattice rows are removed or relabeled here.
   In Section 5.1 the authors limit Table 14 to four A1++ and E++ levels.

## Reproduce and verify (Windows PowerShell)

From the extracted `at20` folder, with Python available:

```powershell
py -m pip install -r requirements.txt
py scripts/extract.py
py scripts/verify.py
```

`python` can replace `py`. Extraction does not access the network and rejects
PDF bytes whose SHA-256 differs from the pinned source. It uses pdfplumber
word coordinates to assign columns, numeric tokens to recover central values
and quoted errors, and a visually reviewed mapping for Table 7's split
superscripts/subscripts. The main lattice size grammar was checked against
the rendered PDF. Existing raw CSV snapshots and derived CSVs are regenerated;
the source PDF is never edited. No files outside the package are written.

Verification checks the manifest, exact counts, unique measurement keys,
positive uncertainties, ensemble joins, raw-to-normalized identity, correction
locations, four poor-fit marks and all eight scalar ground-state entries.
An independent pypdf reader checks the complete ordered numeric token stream
of each requested table against the raw CSVs. This second-reader test checks
numbers and ordering; channel/column identities were also reviewed against
all nine rendered table pages. `qa.json` records the completed checks.

`schema.json` defines every CSV column, primary key, type and quantity/unit.
`source_table`, `pdf_page` (one-based) and `printed_page` locate the source.
Mass/continuum raw CSVs additionally retain `bbox_pt` in PDF points, measured
from the top-left corner, for each nonblank numeric token.
