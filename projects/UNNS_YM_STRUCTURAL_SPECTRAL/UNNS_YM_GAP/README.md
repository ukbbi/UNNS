# UNNS Yang–Mills Gap / Vacuum Boundary Non-Crossability

**Local project name:** `UNNS_YM_GAP`  
**Current stage:** **CLOSED at YM-3B** — central hypothesis not established; terminal Class B verdict `DATA-INDETERMINATE`
**Primary active chamber:** none — CORR-I v0.1.2 retained as the frozen final chamber
**Development mode:** local-first; GitHub is reference/publication infrastructure only until the local project is mature

## Final closure

This project is **closed**.

The original hypothesis that the Yang–Mills mass gap corresponds to a refinement-stable
non-crossable structural vacuum boundary was **not established**.

The decisive Class B Sakai-Sasaki sequence produced the central boundary coordinates

\[
+0.020350,\quad +0.035867,\quad -0.003395,\quad +0.051851,
\]

so the central reconstruction crossed the proposed structural boundary at beta = 6.71.
The negative sign survived PCHIP interpolation and the preregistered L5/L6/L7 ladder tests,
but the 2,000-draw uncertainty interval at that level spanned both signs.

The frozen YM-3B verdict is therefore:

**`DATA-INDETERMINATE`**

The project does not claim that no structural boundary exists, and it does not prove or disprove
the physical Yang–Mills mass gap. It closes because the original universal non-crossability
hypothesis did not obtain the measured-data support required by its own refinement criterion.

Authoritative terminal records:

- `FINAL_STATUS.md`
- `docs/FINAL_SYNTHESIS.md`
- `docs/STAGE0_ORIGIN.md`

No further scientific tests are active in this project.


## Research target

This project investigates whether the Yang–Mills mass-gap problem admits a structural formulation in the UNNS Substrate:

> **Gapless Yang–Mills continuation is structurally non-generable under refinement, whereas the massive branch is refinement-stable.**

The stronger target is:

> **The Yang–Mills mass gap corresponds to a refinement-stable non-crossability boundary separating the vacuum from every non-vacuum admissible physical state.**

The project does **not** assume that a UNNS structural obstruction is automatically a proof of a physical mass gap. A result becomes relevant to the mathematical Yang–Mills mass-gap problem only after a quantitative bridge is established between structural separation and the spectrum of the physical Hamiltonian.

## Core distinction

The project keeps three statements separate:

1. **Confinement** — colored objects do not occur as isolated physical asymptotic states.
2. **Dynamical scale generation** — quantum Yang–Mills dynamics generates a finite physical scale.
3. **Mass gap** — the physical spectrum contains no arbitrarily small positive-energy excitation above the vacuum.

The present project targets item 3 while using the earlier UNNS color-confinement work as structural precedent rather than as a substitute for a mass-gap argument.

## UNNS formulation

Let `V` denote the Yang–Mills vacuum and let `A_YM` denote the family of physically admissible, gauge-invariant Yang–Mills structures represented under the frozen project grammar.

A gapless continuation would require a sequence

\[
V \rightarrow X_1 \rightarrow X_2 \rightarrow \cdots,
\qquad
E(X_n)-E(V)\rightarrow 0^+,
\]

with every `X_n` remaining structurally admissible.

The central UNNS hypothesis is that a positive structural separation survives refinement:

\[
D_{\rm YM}(X,V)\ge\delta_G>0
\]

for every non-vacuum admissible state in the relevant continuum-oriented family.

The eventual bridge target is

\[
E(X)-E(V)\ge F_G(D_{\rm YM}(X,V)),
\]

with `F_G(δ_G) > 0`, which would imply a positive spectral lower bound.

## Current project status

| Phase | Purpose | Status |
|---|---|---|
| **YM-0 — Formalization** | Freeze hypotheses, admissible observables, null rules, refinement logic, and falsification criteria | **Complete for the present program** |
| **YM-1 — Gauge-invariant corpus** | Build the working lattice/glueball corpus from gauge-invariant quantities | **Sufficient for current work** |
| **YM-2 — Vacuum-boundary experiment** | Compare massive and explicitly gapless/adversarial continuations and test structural discrimination | **Closed** |
| **YM-3 — Common refinement** | Test model-level and measured-data refinement persistence | **Closed — YM-3A `MODEL-REFINEMENT PERSISTENT`; YM-3B `DATA-INDETERMINATE` with central crossing** |
| **YM-4 — Bridge theorem program** | Connect structural separation quantitatively to the physical Hamiltonian spectrum | **Not entered / cancelled at project closure** |

The original YM-0 protocol documents are retained as the preregistered foundation. The frozen scientific record of the completed YM-2 stage is:

`docs/SYNTHESIS_YM2.md`

## Primary physical source and refinement backbone

The current physical backbone is A. Athenodorou and M. Teper, **“The glueball spectrum of SU(3) gauge theory in 3+1 dimensions,”** JHEP 11 (2020) 172, arXiv:2007.06422.

The eight-level refinement sequence currently used by the project is:

| β | `a√σ` | `aM_G` |
|---:|---:|---:|
| 5.6924 | 0.3999 | 0.987 |
| 5.80 | 0.31666 | 0.908 |
| 5.8941 | 0.26118 | 0.7991 |
| 5.99 | 0.21982 | 0.7045 |
| 6.0625 | 0.19472 | 0.6365 |
| 6.235 | 0.15003 | 0.4969 |
| 6.3380 | 0.12928 | 0.4276 |
| 6.50 | 0.10383 | 0.3474 |

AT20 provides gauge-invariant glueball observables and fitted masses, but it does **not** tabulate the full raw correlator matrices and covariance required for a fully statistical CORR-I refinement study. Provenance therefore remains an explicit part of YM-3.

## YM-2 result

### First representation: vacuum-anchored spectral ladders

The first YM-2 representation used five glueball-state coordinates plus an explicit vacuum node and four adversarial deformation families (`offset`, `upctrl`, `scale`, `gaponly`).

The result was deliberately negative:

- STRUC-I produced no vacuum-specific rejection;
- the six-node representation remained admissible even under a factor-1024 vacuum-gap compression;
- STRUC-PERC-I fragmentation was not directional, because upward translation could fragment the gap graph as well;
- therefore connectivity collapse was not equivalent to vacuum non-crossability.

The frozen conclusion is:

> **The short spectral-ladder representation does not establish vacuum-specific non-crossability.**

This is treated as a successful falsification of that representation/test pair, not as a failure of the wider project.

### Representation correction: CORR-I

Because a short mass ladder is already a compressed output of a deeper Euclidean spectral object, YM-2 moved to a correlator-native chamber:

\[
C(t)=\int_0^\infty \rho(E)e^{-Et}\,dE,
\qquad \rho(E)\ge0.
\]

CORR-I tests:

- positivity;
- monotonicity;
- discrete log-convexity;
- effective-mass evolution;
- plateau behavior;
- Hankel/Hausdorff positive-moment consistency;
- compatibility with added low-energy spectral weight.

The frozen adversary is

\[
C_{\rm adv}(t)
=
(1-\alpha)C(t)+\alpha e^{-\mu(t-t_0)},
\]

and the chamber computes the compatibility envelope `α_max(μ)` rather than imposing a fixed arbitrary admixture.

The descriptive stage coordinate is

\[
R_{\rm contract}
=
\frac{\alpha_{\max}(\mu/m_{\rm ref}=10^{-3})}
{\alpha_{\max}(\mu/m_{\rm ref}=1)}.
\]

Smaller `R_contract` means stronger suppression of added near-zero spectral weight. It is a **UNNS chamber coordinate, not the physical mass gap**.

### Frozen YM-2 comparison

| Representation | `R_contract` | Relative to massive |
|---|---:|---:|
| gapless `p=0.5` | 0.500947 | 65.2× |
| gapless `p=1` | 0.326916 | 42.5× |
| gapless `p=2` | 0.178612 | 23.2× |
| gapless `p=4` | 0.084534 | 11.0× |
| gapless `p=8` | 0.037668 | 4.90× |
| massive plateau control | 0.007688 | 1× |

All tested gapless Gamma-family controls are positive-spectral consistent and genuinely gapless. Their CORR-I response moves continuously toward the massive response as the finite-window correlator becomes more exponential-like, but even the difficult `p=8` case remains separated at the YM-2 resolution.

The β = 6.50 digitized Figure-7 proxy gives `R_raw ≈ 0.00716`, close to the clean mass-anchored massive control `R_massive ≈ 0.00769`, showing that the strong near-zero envelope contraction is not produced solely by the late-time Figure-7 fluctuation.

### YM-2 stage verdict

> **VACUUM-BOUNDARY DIAGNOSTIC ESTABLISHED; REFINEMENT TEST REQUIRED**

CORR-I now provides a viable structural discriminator for YM-3. The project has **not** yet established refinement-stable Yang–Mills non-crossability.

## Claims that are not made

The project does **not** currently claim that:

- CORR-I proves the Yang–Mills mass gap;
- the digitized Figure-7 proxy is the authors’ raw lattice correlator;
- `R_contract` is the physical mass gap;
- the fixed-resolution YM-2 separation is already refinement-stable;
- the exact exponential massive control is an independent physical measurement;
- the structural diagnostic already implies a Hamiltonian spectral theorem.

## Non-negotiable rules

- Primary inputs must be **gauge-invariant or explicitly gauge-independent physical observables**.
- The gapless branch must be **actively constructed and stress-tested**, not merely absent from the real corpus.
- The decisive structural effect must survive **common refinement**.
- The canonical `STRUC-I` chamber is not modified for this project.
- CORR-I v0.1.2 remains mathematically frozen for the YM-3 comparison unless a separately documented scientific reason requires a new version.
- A structural result is not called a mass-gap proof unless the energy-spectrum bridge is established.
- Nulls and adversarial families are defined before target outcomes are inspected whenever practicable.
- No conclusion may depend on a single discretization, one operator basis, or one numerical ensemble.
- Completed YM-2 controls are not rerun without a scientific reason.

## YM-3 evidence classes

Before the eight-level refinement experiment is run, every input must be assigned an explicit provenance class:

- **Class A — raw or published correlator-level data:** preferred evidence;
- **Class B — published effective-mass trajectories:** may support reconstructed correlator proxies when provenance is explicit;
- **Class C — exact single-exponential controls anchored only to published fitted masses:** valid controlled representations, but not independent correlator measurements.

A refinement study based only on Class C inputs would test the refinement behavior of a **mass-anchored model family**, not the measured Yang–Mills correlators themselves.

## Current directory structure

```text
UNNS_YM_GAP/
│
├── README.md
├── PROTOCOL.md
├── HYPOTHESES.md
├── DATA_PLAN.md
├── REFINEMENT_PLAN.md
├── FALSIFICATION.md
│
├── chambers/
│   ├── corr_i/
│   ├── struc_i_v104.html
│   └── struc_perc_i_v250.html
│
├── data/
│   ├── raw/
│   └── derived/
│       ├── at20/
│       └── corr_i/
│           ├── at20_0pp_b650/
│           ├── at20_0pp_b650_control/
│           ├── gapless_control/
│           ├── gapless_family/
│           └── ym3/
│
├── ladders/
├── nulls/
├── inputs/
├── scripts/
│   └── ym3/
├── output/
│   └── ym3/
│
└── docs/
    ├── SYNTHESIS_YM2.md
    ├── PREREG_YM3.md
    ├── PREREG_YM3.json
    ├── YM3_INPUT_MATRIX.csv
    ├── YM3_BUILD_RECORD.md
    ├── YM3_BUILD_MANIFEST.json
    ├── YM3_RESULT.md
    ├── YM3_RESULT.json
    ├── at20/
    └── ym1a/
```

Root-level `Context.md` is the conversation/project handoff document and is included with the local project package.

## Local workflow

This project is developed locally first. GitHub is reference/publication infrastructure only and is not modified during exploratory development. Project updates should be exchanged as compact ZIP packages or individual files until the local project is mature.

## YM-3A result and immediate next milestone — YM-3B data acquisition

The preregistered YM-3A Class C experiment is complete. The frozen result record is:

`docs/YM3_RESULT.md`

with machine-readable companion:

`docs/YM3_RESULT.json`

The assigned frozen-rule verdict is:

> **MODEL-REFINEMENT PERSISTENT**

Across all eight AT20 refinement levels:

- all massive Class C baselines are `POSITIVE-SPECTRAL CONSISTENT`;
- the massive plateau is retained;
- the α = 0 identity null passes;
- `S_fixed > 0` at every β;
- `S_match > 0` at every β;
- the full matched ordering `R0.5 > R1 > R2 > R4 > R8 > Rmassive` is preserved;
- the native-lattice diagnostic does not reverse the separation.

The permitted conclusion is therefore restricted to the preregistered model family:

> **The massive-side CORR-I signature is persistent across the AT20 mass-anchored Class C refinement sequence.**

This is **not** an eight-level measured-correlator refinement result. The next scientific milestone is **YM-3B data acquisition**: identify at least three ordered non-Class-C refinement levels, preferably Class A raw/published correlators or Class B published effective-mass trajectories, freeze their resampling/uncertainty protocol before inspection, and then run the measured-data refinement comparison.

Do not jump from YM-3A directly to a continuum theorem. YM-3B and the later YM-4 bridge-theorem program remain separate.


## YM-3B current status

The first executable measured-data refinement source is now frozen:

`Sakai & Sasaki 2023 (SS23)` — four Class B `0++` effective-mass trajectories at beta
6.20, 6.40, 6.71, and 6.93.

Protocol: `docs/PREREG_YM3B.md`

Current next step: digitize all four trajectories and construct the preregistered Class B inputs.
No YM-3B CORR-I result has been inspected yet.


## YM-3B SS23 input build

The primary `SS23_B4` Class B inputs are now built and admitted at all four beta levels
(6.20, 6.40, 6.71, 6.93). The CORR-I scientific batch has not yet been run.

See:

- `docs/YM3B_BUILD_RECORD.md`
- `output/ym3b/admission/YM3B_INPUT_ADMISSION.csv`
- `data/derived/corr_i/ym3b/ss23/`

Next: matched Gamma controls + frozen four-beta CORR-I batch.


## YM-3B result

Primary SS23 Class B refinement batch complete.

**Verdict:** `DATA-INDETERMINATE`

See:

- `docs/YM3B_RESULT.md`
- `output/ym3b/YM3B_SUMMARY.csv`
- `output/ym3b/YM3B_UNCERTAINTY_SUMMARY.csv`

Next: Liang14 independent Class B replication, followed by Chen06 extension audit.
