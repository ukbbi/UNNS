# UNNS Turbulence — JHTDB Pilot Scope

## Pilot objective

Test whether forced isotropic turbulence exhibits **reproducible multiscale
structural organization** that is not reducible to its one-dimensional energy
spectrum alone.

The pilot is deliberately narrower than a general "theory of turbulence".
It asks whether a useful UNNS structural description exists in a controlled,
statistically stationary DNS setting.

## Physical system

Initial source:

- Johns Hopkins Turbulence Database (JHTDB)
- forced isotropic turbulence
- canonical dataset: `isotropic1024coarse`
- 1024^3 periodic DNS
- velocity and pressure fields
- statistically stationary forced turbulence
- Taylor-scale Reynolds number approximately R_lambda ~ 433
- 5,028 stored frames over t = 0 ... 10.056

These dataset facts are provenance metadata. The actual sampling corpus is not
defined in this structure package and must be fixed before downloading data.

## Core UNNS interpretation

A turbulent snapshot is not represented by one scalar sequence. It is represented
as a scale-ordered structural object:

    L(t) = {S_l0, S_l1, ..., S_ln}

where each rung S_l describes the flow after filtering/coarse-graining at a
specified physical scale l.

Candidate rung information may include:

- local or regional velocity statistics;
- vorticity and enstrophy;
- strain;
- helicity;
- spectral/coherence descriptors;
- coherent-object connectivity;
- object volume, shape and persistence;
- branching / merging / fragmentation;
- interscale transfer descriptors.

The pilot must determine empirically which of these quantities are stable enough
to form a useful structural ladder. They are not assumed to be equally useful.

## Three-stage claim ladder

### Stage A — structural discrimination
Real turbulence differs reproducibly from matched controls.

### Stage B — structural families
Real turbulence occupies recurring multiscale families with measurable
persistence and cross-realization stability.

### Stage C — restricted transition grammar
Transitions among those families are non-uniform and predictive enough to define
a measurable route structure across scale and/or time.

Stage C is the strongest target. Failure at one stage prevents promotion to the
next.

## What this pilot does NOT claim

- It does not replace Navier-Stokes dynamics.
- It does not claim to solve turbulence from first principles.
- It does not infer significance from reproducing the -5/3 spectrum alone.
- It does not treat visual vortex patterns as evidence without quantitative tests.
- It does not modify the canonical STRUC-I or STRUC-PERC-I chambers.

## Success criterion

A useful positive result requires a reproducible structural difference between
real turbulence and matched controls, followed by evidence that the detected
organization persists across independent cutouts/times and is not an artifact of
one filtering scale, threshold or chamber encoding.
