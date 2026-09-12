# Regime Synthesis

**UNNS Substrate Research Program**  
**Project role:** Cross-domain synthesis and development of Structural Regime Theory  
**Status of foundation document:** Intermediate-stage foundation document  
**Primary instrument:** STRUC-I v1.0.4  
**Year:** 2026

## Overview

`regime_synthesis/` collects the UNNS work in which previously separate admissibility, deformation, persistence, and boundary results are assembled into a common **structural-regime framework**.

The central document in this project is:

- `Foundations of the UNNS Substrate.pdf`

Its full title is **Foundations of the UNNS Substrate: From Universal Admissibility to Structural Regime Theory**.

The document synthesizes a cross-domain corpus reported as exceeding 1,500 ladders and 150,000 structural assessments across atomic, molecular, nuclear, hadronic, geoid, seismological, cosmological, condensed-matter, and biological systems.

The project does not replace the earlier domain investigations from which that corpus was built. Its purpose is to identify the larger structure that becomes visible when those results are read together.

## Core synthesis

The foundation document organizes the accumulated evidence around three interlocking claims:

1. **Universal admissibility** — the UNNS admissibility inequality is reported to hold at physical constant values throughout the tested corpus, with no hard physical-parameter violations in the studied domain families.
2. **Stratified occupation** — physical systems do not populate the admissible region uniformly; they occupy characteristic structural regimes with differing pressure, persistence, and boundary proximity.
3. **Operator-selective activation** — structural response is anisotropic: some constant/domain deformation directions produce genuine reorganization, while others remain metrically neutral.

Together these motivate **Structural Regime Theory**, in which the main object is no longer only a universal inequality but an operational geometry of admissible structure.

The synthesis introduces or consolidates the following ideas:

- the Universal Structural Law (USL);
- structural admissibility as a pre-dynamical restriction;
- a selection operator over admissible configurations;
- an admissibility manifold;
- structural coordinates and regime maps;
- operator-induced trajectories through structural space;
- flat and curved directions in operator space;
- the admissibility boundary as a structural phase interface;
- boundary amplification and boundary information;
- structural sensitivity and constant anchoring;
- substrate-independence across tested physical and non-physical sequence domains.

## Scientific status

The foundation document explicitly presents itself as an **intermediate-stage foundation document**, not as a mathematically closed final theory.

Within its own stated scope, it reports established corpus-level results including:

- admissibility across more than 1,500 ladders and 150,000+ assessments;
- structural stratification across domain families;
- directional sensitivity under fundamental-constant deformation;
- phase-interface behavior near admissibility boundaries;
- structural invariance across a wide range of physical scales and governing equations.

It also states open mathematical problems, including the absence of a complete global topology or intrinsic metric for the admissibility manifold.

Those open problems motivate the developed research branch contained in `local_geometry/`.

## Current developed material

The current project package includes the `local_geometry/` research branch, which develops the local geometry of realizability boundaries, structural margins, chart structure, and associated validation studies.

See:

- [`local_geometry/README.md`](local_geometry/README.md)

for the detailed research sequence and contents.

Additional branches and supporting material may be added to `regime_synthesis/` as the project archive is completed.

## Directory structure

```text
regime_synthesis/
├── README.md
├── Foundations of the UNNS Substrate.pdf
└── local_geometry/
    ├── README.md
    ├── Local Geometry of Realizability Boundaries in the UNNS Substrate.pdf
    ├── local_geometry_dashboard.html
    ├── Helium Multi-Chart Validation.pdf
    ├── helium_multichart_v3.html
    ├── Si Local Geometry Validation.pdf
    ├── si28_local_geometry_validation.html
    ├── Atomic Structural Phase Landscape in the UNNS Substrate.pdf
    ├── atomic_phase_landscape_v1.html
    ├── atoms_input.zip
    ├── atoms_output..zip
    ├── image1d.png
    ├── image2d.png
    └── image3d.png
```

## Suggested reading order

For a reader entering this project for the first time:

1. **Foundations of the UNNS Substrate** — the cross-domain synthesis and statement of Structural Regime Theory.
2. **Local Geometry of Realizability Boundaries in the UNNS Substrate** — the formal local-geometric development.
3. **²⁸Si Local Geometry Validation** — nuclear-corpus test of the local theory.
4. **Helium Multi-Chart Validation** — representation-dependent and multi-chart validation.
5. **Atomic Structural Phase Landscape in the UNNS Substrate** — extension from a single-system chart to a cross-element regime landscape.

The HTML dashboards provide browser-readable companion views of the corresponding local-geometry studies.

## Relationship to the wider UNNS repository

This project is part of the structured `projects/` archive.

Earlier UNNS material elsewhere in the repository remains part of the same research program. Its existing paths are not reorganized here because those paths may already be externally referenced.

`regime_synthesis/` therefore serves as the structured home of this particular synthesis program and its developed local-geometry branch, while preserving continuity with the earlier UNNS corpus on which the synthesis depends.
