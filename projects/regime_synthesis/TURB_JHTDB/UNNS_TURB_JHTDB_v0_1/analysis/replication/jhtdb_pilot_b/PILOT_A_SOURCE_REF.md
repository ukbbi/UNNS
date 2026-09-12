# Pilot A Source Reference for Pilot-B Replication

**Project:** `UNNS_TURB_JHTDB_v0_1`  
**Record:** `JHTDB_PILOT_A_SOURCE_REFERENCE v0.1`  
**Purpose:** Freeze the recovered Pilot-A extraction coordinates and time window before selecting Pilot B.

## Pilot A source

Dataset:

`isotropic1024coarse`

Local frozen HDF5:

`data/raw/jhtdb/isotropic1024coarse/cutouts/isotropic1024-coarse-velocity.h5`

SHA-256:

`e32c9225af656a2f0fa0a704be7dcd78fa12efc1a01b880af23eb45e02108a46`

Public source reference:

[ArielLubonja/johns-hopkins-turbulence-database — Hugging Face](https://huggingface.co/datasets/ArielLubonja/johns-hopkins-turbulence-database/tree/main)

## Exact spatial extraction

Full DNS grid:

\[
1024^3.
\]

Pilot-A cutout:

\[
256\times256\times256.
\]

HDF5/JHTDB 1-based inclusive indices:

\[
x=1{:}256,\qquad
y=1{:}256,\qquad
z=1{:}256.
\]

Zero-based array equivalent:

\[
x,y,z=0{:}255.
\]

Spatial stride:

\[
1.
\]

Filter width:

\[
1.
\]

With:

\[
\Delta x=\frac{2\pi}{1024}
\approx0.00613592315154,
\]

the sampled coordinate interval on each axis is:

\[
0
\le x,y,z \le
255\frac{2\pi}{1024}
\approx1.56466040364.
\]

## Exact temporal extraction

Stored frame indices:

\[
1{:}10.
\]

Stored frame count:

\[
10.
\]

Stored frame spacing:

\[
\Delta t=0.002.
\]

Time-index origin:

\[
1.
\]

Therefore:

\[
t_i=(i-1)\times0.002.
\]

Pilot-A physical times are:

\[
0,\ 0.002,\ 0.004,\ 0.006,\ 0.008,\ 0.010,\ 0.012,\ 0.014,\ 0.016,\ 0.018.
\]

Physical time window:

\[
\boxed{0\le t\le0.018}.
\]

## Replication consequence

A genuine Pilot B must not reuse any Pilot-A spatial grid point.

Therefore Pilot B must have:

\[
\boxed{\text{spatial overlap with Pilot A}=0}
\]

if it is to retain the `jhtdb_pilot_b` label.

A different time subset of the same Pilot-A spatial cube is an internal robustness test, not Pilot B.

A spatial subdivision of the Pilot-A cube is also an internal robustness test, not Pilot B.

## Example only

A possible same-size non-overlapping spatial candidate would be:

\[
x=257{:}512,\qquad
y=1{:}256,\qquad
z=1{:}256.
\]

This is **not yet the selected Pilot-B source**. It is recorded only as an example of a spatially disjoint cube.

## Protocol status

This provenance record is added after the Pilot-B protocol freeze.

It does not modify any frozen Pilot-B setting, chamber, null definition, threshold, or replication criterion.
