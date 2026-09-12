# JHTDB High-Re Spatial Generalization — Preregistered Protocol v0.1

**Project:** `UNNS_TURB_JHTDB_v0_1`  
**Branch:** `jhtdb_high_re`  
**Status:** frozen before inspection of any selected high-Re field values  
**Relation to Pilot B:** separate branch; Pilot B remains frozen and pending acquisition.

## 1. Question

Test whether the **scale-only structural regime** observed in the Pilot-A JHTDB turbulence analysis recurs when the DNS grid and Reynolds number increase dramatically.

This branch does **not** test the Pilot-A scale–time stitching defect `D_STITCH`, temporal persistence, or scale–time commutation. The `isotropic8192` and `isotropic32768` records are snapshots, not a continuous time series for this purpose.

The branch therefore asks:

> When the same native-grid multiscale object grammar is applied to high-Reynolds forced isotropic turbulence snapshots, does the scale-persistence ladder occupy the same structural regime as Pilot A, stabilize into a different regime, or become mixed across snapshots/resolutions?

## 2. Public datasets

### isotropic8192

- forced isotropic DNS;
- grid: `8192^3`;
- domain: `2π × 2π × 2π`;
- six stored snapshots;
- public JHTDB documentation identifies snapshot labels `0..4` as the high-Re set (`Re_lambda ~1200–1300`) and snapshot `5` as the lower-Re, highly resolved case (`Re_lambda ~610`).

### isotropic32768

- forced isotropic DNS;
- grid: `32768^3`;
- domain: `2π × 2π × 2π`;
- one stored snapshot;
- public JHTDB documentation gives `Re_lambda ~2500` (approximately 2556 in the dataset README statistics).

Both datasets are accessed through the user-mounted SciServer `turbulence-ceph` volume. No JHTDB authorization token is used by this branch.

## 3. Frozen spatial samples

All samples use **native-grid 256^3 cubes**. This intentionally tests recurrence in local/native-grid coordinates; it is **not** a fixed-physical-volume comparison across DNS grids.

The sample cube is the deterministic central 256^3 cube of each periodic domain.

### isotropic8192

1-based inclusive grid coordinates:

- `x = 3969:4224`
- `y = 3969:4224`
- `z = 3969:4224`

All six stored snapshots are extracted separately:

- snapshot labels `0,1,2,3,4,5`
- corresponding Zarr indices `0,1,2,3,4,5`

The six snapshots are **independent spatial samples for this analysis**. They must never be linked with time edges.

### isotropic32768

1-based inclusive grid coordinates:

- `x = 16257:16512`
- `y = 16257:16512`
- `z = 16257:16512`

Frozen snapshot:

- snapshot label `0`
- Zarr index `0`

## 4. Boundary and periodicity rule

The parent DNS domains are periodic, but every extracted 256^3 cube is treated as a **nonperiodic cutout**:

- no opposite-face wrapping;
- no FFT derivative that assumes cutout periodicity;
- boundary-safe derivatives only;
- objects touching the protected cutout boundary are discarded under the same rule used for Pilot A.

## 5. Frozen object grammar

The high-Re scale adapter must preserve the Pilot-A object grammar exactly unless a new preregistration version is created before inspecting high-Re results:

- scale block factors: `[1,2,4,8,16]`;
- multiscale method: exact non-overlapping block mean;
- native boundary margin: `16` cells;
- segmentation field: `Q`;
- threshold mode: `Q_rms`;
- threshold multiplier: `1.5`;
- connectivity: `26`;
- minimum native object volume: `64` voxels;
- minimum coarse object volume: `2` voxels;
- relation candidate: positive voxel overlap only;
- relation eligibility: `overlap_src >= 0.1 OR overlap_dst >= 0.1 OR IoU >= 0.05`;
- relation confidence: `overlap_src`.

Only adjacent **scale** transitions are constructed. No time transitions are constructed.

## 6. Primary scale statistic

For each eligible source object, `P_SCALE` is the same scale-persistence quantity used by STRUC-ROUTE-I / Pilot A. Duplicates are preserved; no jitter, smoothing, deduplication, normalization, or rescaling is permitted before chamber use.

The real mean scale persistence is compared with the same directed layer/degree-preserving endpoint-rewiring null used in Pilot A:

- null count: `100`;
- base seed: `20260904`;
- swaps per edge: `5.0`;
- minimum mean mobility fraction: `0.01`;
- minimum unique graph fraction: `0.10`;
- maximum real-match fraction: `0.90`;
- alpha: `0.05`;
- minimum usable nulls: `20`.

The null test is one-sided in the high-persistence direction.

## 7. Cross-chamber tests

Each snapshot's `P_SCALE` ladder is interrogated independently by the canonical chambers:

- `STRUC-I v1.0.4`;
- `STRUC-PERC-I v2.5.0`.

STRUC-I precision rule is unchanged from Pilot B:

- initial run: `2,000` Monte Carlo perturbations;
- if mean `A_kappa` lies within `0.01` of a regime boundary, rerun at `10,000` MC with every other setting unchanged.

A STRUC-PERC-I connectivity result is inferentially usable only when:

- gap vertices after exact-value deduplication: `>=100`.

Giant-component support is recorded when giant ratio is `>=0.95`.

## 8. Frozen interpretation matrix

Pilot-A reference for `P_SCALE` at 10,000 MC:

- mean `A_kappa = 0.535600`;
- classification: `Structural Instability`;
- state: `Random Structure`.

### `PILOT_A_SCALE_REGIME_RECURRENCE`

Requires:

1. at least `4/5` high-Re `isotropic8192` snapshots (`0..4`) return the Pilot-A STRUC-I regime (`Structural Instability` / `Random Structure`); and
2. `isotropic32768` snapshot `0` returns the same Pilot-A STRUC-I regime.

The lower-Re `isotropic8192` snapshot `5` is reported separately and does not enter the `4/5` high-Re count.

### `HIGH_RE_SCALE_STABILIZATION`

Requires:

1. at least `4/5` high-Re `isotropic8192` snapshots return `Geometric Persistence`; and
2. `isotropic32768` returns `Geometric Persistence`.

### `MIXED_HIGH_RE_SCALE_REGIME`

Assigned when neither of the preceding two labels applies and all primary samples are analyzable.

### `UNDERRESOLVED`

Used when source integrity, object count, null mobility, or chamber quality is insufficient. Underresolved results are never converted to success/failure.

## 9. Secondary outcomes

Reported without changing the primary interpretation label:

- real vs null mean `P_SCALE` and one-sided `p_favorable` for every snapshot;
- STRUC-PERC-I verdict, giant ratio, and gap-vertex count;
- scale branching and merging frequencies;
- object-count and physical-field diagnostics at each scale;
- the lower-Re `isotropic8192` snapshot `5` as a prespecified contrast.

## 10. Stopping rule

All frozen samples are analyzed exactly once under this branch:

- five high-Re `isotropic8192` snapshots;
- one lower-Re `isotropic8192` contrast snapshot;
- one `isotropic32768` snapshot.

Do not move the cube, select a more favorable snapshot, change scale factors, or retune thresholds after seeing results. Any methodological change requires `PROTOCOL_v02` (or later) and a new freeze before applying the changed method.

## 11. Claim boundary

A positive result supports **native-grid scale-regime generalization** across much larger DNS grids and higher Reynolds number. It does not establish:

- temporal persistence at high Reynolds number;
- high-Re scale–time commutation;
- replication of `D_STITCH`;
- fixed-physical-scale invariance;
- universality beyond forced isotropic turbulence.

Pilot B remains the preregistered test of independent scale–time replication in `isotropic1024coarse`.
