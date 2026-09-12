# Data and Object Schema

## 1. Source layer

`data/source/`

Official documentation and compact reference products supplied by JHTDB.
This layer establishes provenance and interpretation but is not the analysis
corpus.

## 2. Raw layer

`data/raw/jhtdb/isotropic1024coarse/`

Untouched retrieved JHTDB cutouts plus their metadata.

A raw cutout is authoritative for all downstream transformations.

## 3. Derived physical layer

`data/derived/fields/`
Pointwise or voxelwise derived physical fields.

`data/derived/scales/`
The same flow represented across an ordered family of filter/coarse-graining
scales.

`data/derived/objects/`
Detected connected/coherent objects and their descriptors.

## 4. Control layer

`data/controls/`

Controls are descendants of validated real data but are stored independently.
A control file must carry a reference to its real parent.

## 5. Native UNNS ladder layer

`ladders/native/`

Canonical project-level representation:

    Flow realization / time
      -> ordered scale rungs
      -> structural descriptors on each rung
      -> cross-rung relations

This is deliberately chamber-neutral.

## 6. Chamber-input layer

`ladders/struc_i/`
`ladders/struc_perc_i/`

These contain only valid inputs produced by explicit adapters from the native
ladder layer.

## 7. Chamber-output layer

`outputs/exports/struc_i/`
`outputs/exports/struc_perc_i/`

Direct chamber exports. These are never relabeled as source or raw data.

## 8. Analysis layer

`analysis/`

Derived comparisons, family assignments, transition matrices, persistence
statistics and control contrasts.

## 9. Result layer

`outputs/records/`

Machine-readable final claims. Each record must be reproducible from the stored
lineage.

## Required lineage

Every promoted result must permit reconstruction of:

JHTDB query
  -> raw checksum
  -> derived transform
  -> scale definition
  -> object/feature extraction
  -> native ladder
  -> chamber adapter
  -> chamber version and parameters
  -> chamber export
  -> statistical analysis
  -> reported result
