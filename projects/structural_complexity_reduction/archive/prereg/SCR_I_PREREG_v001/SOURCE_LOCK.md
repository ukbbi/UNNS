# SCR-I-A Source Lock

**Repository:** `ukbbi/UNNS`  
**Reference commit observed during preregistration review:** `aa17dbc9c48f8da6daf51b0547b060558c175e7d`

The experiment must use the pinned Git blob content below or a local byte-identical copy. A later repository change must not silently alter SCR-I-A.

| Role | Repository path | Git blob SHA |
|---|---|---|
| P3 Mode-C downstream source | `canonical/chamber_lii_phase_P₃/chamber_lii_v1_3_2_CURV_RESP_ENCODING_FIXED.html` | `7985c98f09d42776ea6a099bfb0e03a95864e89f` |
| P4 generator/gate source | `canonical/chamber_liii_phase_P₄/chamber_liii_v3_1_0_modular.html` | `52607c8e3b078084906b352d934d037c3aad9dd3` |
| Axis V methodology | `canonical/axis_v_admissibility_gate/axis_v_methodology_guide.md` | `53df9d3cd73b924a3b48742ae7ad0b35cb1f3232` |
| Axis V validation supplement | `canonical/axis_v_admissibility_gate/axis_v_technical_supplement.md` | `8dcab608ff49da8d4b3349c81c48ec8af81d1d45` |
| Discovery/generative-control precedent | `canonical/chamber_xlix/README.md` | `52d120848fb6dd52335892ea8d21001e086175ab` |
| Structural-arc synthesis | `canonical/chambers_li-lv-structural-arc/README.md` | `fed78a43251b962231669c77e5cd0fa029b2253a` |

## Frozen extracted facts

P4 baseline profile:

```text
G3_s_lo = 0.08
G3_s_hi = 0.10
G3_T_min = 0.70
G4_locality_strict = 0.10
generator mix = 0.50 boundary / 0.30 pathological / 0.20 broad
```

Primary P4 predicates:

```text
G1: turning_angle
G2: delta_kappa > 0.05
G3: bifurcation + soft-band temporal coherence rule
G4: locality_score < 0.10
```

Pinned Chamber-LII emergence criterion includes:

```text
Mode-C R4 coverage threshold: coverage_abs_delta_ge_0_20 >= 0.25
baseline must remain below R4 threshold
Mode-C curvature must exceed baseline by > 0.05
```

## Local-source rule

Before execution, copy the two executable upstream HTML files into the SCR project under a source-lock directory or otherwise verify their Git blob SHAs through Git. Do not run against an unpinned live web page.
