# VREF_B_SOURCE.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Branch:** VREF-I/B — Structural Vacuum Accessibility  
**Source ID:** `CEA_2017_SU3`  
**Status:** **FROZEN — PRIMARY SOURCE ADMITTED**  
**Freeze date:** 2026-10-05

## 1. Source

Paolo Cea, Leonardo Cosmai, Francesca Cuteri, Alessandro Papa,  
**“Flux tubes in the QCD vacuum,”** arXiv:1702.06437v3.

Primary local source files:

```text
data/raw/cea_2017/
├── arXiv-1702.06437v3.tar.gz
└── cea_2017.pdf
```

Expected SHA-256:

```text
arXiv-1702.06437v3.tar.gz
38e899b4c9d83b78e8bca70a51fc3adb3fa4e8c278ce4c392b3b08cbc3de2c44

cea_2017.pdf
13f9defe0fc0f30337bd52eed229ffc7175559201db66dcc31cdf4b799eda155
```

## 2. Primary vector asset

The primary empirical profile is recovered from the Grace-generated vector figure:

```text
E_physical_scaling_SU3.eps
```

inside the arXiv source archive.

Expected SHA-256:

```text
bfa9e27a3d6e045e33977c277b8c473d1123067acac0c97955cd4fbee670a6fe
```

The standalone SU(3), d=8a figure is retained only as an extraction cross-check:

```text
E_physical_SU3_dist8.eps
SHA-256: ea683fc5967d396e3d3275ccfce90848a78abba5e1e93bb95c2a3e1c87f72525
```

## 3. Physical observable

The admitted observable is the longitudinal chromoelectric field

\[
E_l(x_t)
\]

measured at the transverse distance \(x_t\) from the midpoint axis of a static quark–antiquark pair.

The connected correlator is explicitly vacuum referenced:

\[
\rho_{\rm conn}
\rightarrow
a^2g\left(
\langle F_{\mu\nu}\rangle_{q\bar q}
-
\langle F_{\mu\nu}\rangle_0
\right),
\]

with the vacuum average expected to vanish.

Thus the operational VREF vacuum coordinate is

\[
\boxed{E_l=0}.
\]

## 4. Physical geometry

The primary branch uses the pure-gauge SU(3) continuum-scaling pair at

\[
\boxed{d=0.76\ {\rm fm}}.
\]

Refinements:

```text
R1: beta = 6.050, source distance = 8a
R2: beta = 6.195, source distance = 10a
```

Both correspond to the same physical source separation according to the source analysis.

## 5. Why this source is primary

This source is admitted because it provides:

- pure-gauge SU(3) Yang–Mills;
- a gauge-invariant connected-correlator field observable;
- an explicit vacuum subtraction in the continuum interpretation;
- the same physical source separation at two lattice refinements;
- a measured transverse profile extending far beyond the flux-tube core;
- vector-recoverable plotted data and pointwise error bars;
- a published continuum-scaling comparison.

## 6. Scope limitation

The source uses HYP+APE smoothing. Therefore the VREF-I/B verdict is a statement about the **published gauge-invariant, plateau-selected, smeared connected-field representation**.

Smoothing is not silently treated as absent.

Cross-representation evidence from Battelli 2019 (unsmoothed connected correlator) and Yanagihara 2019 (vacuum-subtracted EMT) remains external validation and does not define the primary result.

## 7. Admission verdict

```text
CEA_2017_SU3
STATUS: ADMITTED
ROLE: VREF-I/B PRIMARY
```

No scientific VREF-I/B outcome is frozen in this file.
