# Dataset 001 — TCV L-H Transition Database, Zenodo 14996664

## Acquisition status

Raw files were downloaded into:

```text
unns_hmode_project/data/raw/tcv_zenodo_14996664/
```

Expected raw files:

```text
LH_analysis.ipynb
LH_DATA.h5
lhdatabase.h5
README_1.md or README.md
requirements.txt
```

Raw files must remain unchanged. Derived CSV/JSON outputs belong in `data/processed/` and `outputs/reports/`.

## Inspected files

### `lhdatabase.h5`

This is the first file to use for the event-level UNNS pilot.

Observed structure:

- Flat HDF5 file.
- 80 top-level datasets.
- Every dataset is a row vector with 92 entries.
- Interpretable as an event-level table: one row per transition/threshold record.
- 92 rows across 66 unique TCV shots.
- Shot range: 66444 to 73917.
- Shot years represented: 2020, 2021, 2022.
- `ILH` contains 84 entries equal to 1 and 8 entries equal to 0.
- `COND` is always 1 in this extracted table.

Important columns for first UNNS mapping:

| Source column | Initial role in UNNS-H Mode project |
|---|---|
| `SHOT` | discharge / shot identifier |
| `TIME` | transition/event time candidate |
| `THL` | additional transition timing or interval field; confirm against README/notebook |
| `ILH` | L-H event indicator / quality indicator candidate; confirm against README/notebook |
| `PLH` | L-H threshold power candidate |
| `PLMW`, `PTOTMW`, `PTOTMW_A` | loss/total power candidates |
| `PNBI`, `PECH`, `POHMSMOOTH` | heating components |
| `PRAD`, `PRADCORE` | radiated/core radiated power candidates |
| `DWMHDMW`, `WMHD`, `WMHD_A` | stored-energy / derivative candidates |
| `NEL`, `NEL20` | line-averaged density candidates |
| `IP`, `BT`, `Q95`, `KAPPA`, `DELTA` | magnetic/equilibrium geometry fields |
| `cH`, `cHe`, `A`, `Z`, `ZEFF` | species/composition/effective charge candidates |
| `nRyter`, `PRyter` | Ryter-normalized density/power candidates |
| `PDIV`, `PDIV150`, `PDHEII` | divertor/edge signal candidates |
| `CHIEFF` | effective transport coefficient candidate |

Important missingness:

- `NEUTRATE` is sparse: 17 non-null values, 75 missing.
- `PLMW`, `PTOTMW_A`, `PLMWSTD`, `PTOTMW_ASTD`, `HDR`, `HDRSTD`, `CHIEFF` have 3 missing values each.
- Several other columns have 1–2 missing values.
- No infinities were detected in numeric fields.

### `LH_DATA.h5`

This is not the first canonical table. It appears to be MATLAB-exported supporting data organized by figure groups:

```text
data/fig1
data/fig2
data/fig5
data/fig6
data/fig8
```

Observed roles:

| Group | Observed content | First-use priority |
|---|---|---|
| `data/fig1` | time-series-like arrays for heating, stored energy, density, photodiode data, times | second |
| `data/fig2` | loss-power / neutral / radiated-power related arrays | second |
| `data/fig5` | helium/composition/profile-support arrays | second |
| `data/fig6` | compact arrays: `NEL20`, `P1`, `PLMW`, `PLMWSTD`, `ci2`, `cond1` | first cross-check |
| `data/fig8` | Thomson-scattering/profile-related structures and profile arrays | later pedestal/profile work |

`LH_DATA.h5` should be used after `lhdatabase.h5` is ingested, because it contains diagnostic support arrays and figure-level structures rather than one obvious canonical event table.

## Immediate UNNS interpretation

The dataset is suitable for the first UNNS-H Mode pilot because it provides a compact event-level L-H threshold table with power, density, composition, magnetic geometry, and energy terms.

For the initial project, treat it as:

```text
L-H threshold/event table → boundary-admissibility transition dataset
```

Do not yet claim it contains enough information for full turbulence-suppression or ELM precursor analysis. That requires richer time-series diagnostics, likely from `LH_DATA.h5` or later MAST/FAIR data.

## First canonical outputs

Create these derived files:

```text
data/processed/tcv_lh_events_raw_flat.csv
data/processed/tcv_lh_events_canonical.csv
outputs/reports/tcv_lh_h5_inspection_summary.json
outputs/reports/tcv_lh_columns_summary.csv
```

## First pilot question

Use this dataset to answer the first limited question:

> Do L-H threshold/event records occupy a coherent region in a UNNS boundary-admissibility feature space defined from density, loss power, heating components, magnetic geometry, species composition, and stored-energy response?

This is not yet the full H-mode-origin question. It is the necessary first step.

## Required confirmation before formal modeling

Read the downloaded README and notebook to confirm the precise meanings and units of:

```text
TIME
THL
ILH
PLH
PLMW
PTOTMW_A
DWMHDMW
nRyter
PRyter
COND
```

Until that is done, the adapter should label these as candidate semantic mappings rather than final physics definitions.
