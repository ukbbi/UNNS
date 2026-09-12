# UNNS Color Confinement - First Diagnostic Report

**Report status:** Formalized first diagnostic  
**Scope:** Static spectrum + flux-tube profile + UNNS mapping  
**Boundary condition:** This report does not claim that UNNS derives QCD confinement. It formalizes a grounded structural mapping from the current data pack.

---

## Executive conclusion

Color confinement can be used as a physical benchmark for **admissibility-by-closure**: colored constituents may be internally real, but isolated colored externalization is not the admissible output. The observable route is tensioned, localized, and repaired into color-neutral composite channels.

In UNNS language, the currently supported sequence is:

```
internal colored constituent
-> attempted separation
-> localized route tension
-> threshold / repair region
-> admissible color-neutral composite
```

---

## 1. Data status

### 1.1 Static-source energy levels

- Rows: **57**
- Separation range: **0.70686 to 1.6065 fm**
- Data status: **MODEL_RECONSTRUCTION_FROM_REPORTED_PARAMETERS_NOT_RAW_DATA**
- Minimum gap V1 - V0: **0.078378 GeV**
- Minimum gap V2 - V1: **0.040918 GeV**

Interpretation boundary: these static-source levels are model-reconstructed from reported Hamiltonian parameters. They are useful for a first structural diagnostic but must not be treated as raw measured GEVP point data.

### 1.2 String-breaking thresholds

| threshold | channel | reported r [fm] | nearest reconstructed r [fm] | gap V1 - V0 [GeV] | gap V2 - V1 [GeV] |
|---|---|---:|---:|---:|---:|
| r_c | light_static_light_threshold | 1.224 +/- 0.015 | 1.22094 | 0.089700 | 0.045937 |
| r_cs | strange_static_strange_threshold | 1.293 +/- 0.016 | 1.28520 | 0.086418 | 0.046390 |


### 1.3 Flux-tube pointwise profile

- Rows: **31**
- Transverse range: **-1.107463 to 1.107463 fm**
- Static-source separation: **0.738309 fm**
- Data status: **AUTHOR_ANCILLARY_POINTWISE_DATA**
- Peak Ex FULL: **0.343135 GeV^2**
- Peak Ex nonperturbative: **0.244566 GeV^2**
- Estimated nonperturbative FWHM: **0.551469 fm**

---

## 2. Diagnostic figures

### Figure 1. Static Q-Qbar model-reconstructed energy levels

![Static energy levels](fig_static_energy_levels.png)

The static-source energy levels supply the first route-extension diagnostic. In the UNNS mapping, separation r is treated as a route-extension coordinate and the static spectrum as a boundary-pressure / route-tension spectrum.

### Figure 2. Static-source level gaps

![Static energy gaps](fig_static_energy_gaps.png)

The gap plot is the first threshold diagnostic. The relevant region is not simply where energy rises, but where competing levels approach, reorganize, and mark the onset of screened/repaired channels.

### Figure 3. Flux-tube transverse longitudinal chromoelectric profile

![Flux-tube profile](fig_flux_tube_profile.png)

The flux-tube profile supplies a direct geometry of route localization. The chromoelectric field is concentrated around the source-connecting route rather than freely dispersing in the transverse direction.

### Figure 4. UNNS confinement sequence

![UNNS confinement sequence](fig_unns_confinement_sequence.png)

---

## 3. UNNS working map

| QCD diagnostic object | UNNS interpretation |
|---|---|
| quark separation r | route-extension coordinate |
| V0(r), V1(r), V2(r) | boundary-pressure / route-tension spectrum |
| string-breaking threshold | repair-threshold marker |
| two-meson threshold / screened channel | repaired admissible composite channel |
| flux-tube transverse profile Ex(xt) | localized route geometry |
| absence of free color in ordinary external spectrum | non-externalizable internal coordinate |

---

## 4. Formal interpretation

The first diagnostic supports a bounded claim: color confinement is a strong benchmark for the UNNS distinction between internal reality and external admissibility.

A colored constituent may be valid as an internal coordinate of the physical structure, but the isolated colored object is not the admissible external output. Attempted separation is carried by a localized, tensioned route. At threshold, the system is not interpreted as revealing free color; instead, the relevant channel is repaired into color-neutral composite structure.

This is the physical pattern that matters for UNNS regime synthesis:

```
internal coordinate != external admissible object
route extension -> boundary pressure -> threshold repair -> closed observable composite
```

---

## 5. Supported now

- Static-source separation can be used as a first route-extension coordinate.
- The reconstructed static spectrum can be used as a provisional route-tension / boundary-pressure proxy.
- The reported light and strange string-breaking thresholds identify a repair-threshold window.
- The Baker pointwise flux-tube profile gives direct localized-route geometry.
- The overall diagnostic supports admissibility-by-closure as a regime-synthesis benchmark.

---

## 6. Not supported yet

- A derivation of QCD confinement from UNNS.
- Raw measured V0, V1, V2 lattice GEVP point tables.
- Full uncertainty propagation for the reconstructed static spectrum.
- A complete threshold-window analysis across all available flux-tube separations.
- A general law across QCD, H-mode, and other confinement systems.

---

## 7. Next report

The next formal report should be:

```
02_repair_threshold_analysis.md
```

It should focus only on:

```
r near r_c  ~= 1.224 fm
r near r_cs ~= 1.293 fm
gap behavior
two-meson threshold
transition from stretched route to repaired composite route
```

---

## 8. Report decision

This diagnostic is now suitable to enter the UNNS regime-synthesis track as:

**Color Confinement - Admissibility-by-Closure Benchmark I**

Its current function is not to prove QCD confinement, but to provide a grounded physical case where the distinction between internal constituent, non-externalizable route, localized boundary pressure, and admissible closed composite can be studied quantitatively.
