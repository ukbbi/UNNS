# Context.md

# UNNS Yang–Mills Gap / Vacuum Boundary Non-Crossability

**Local project folder:** `UNNS_YM_GAP`  
**Current stage:** **CLOSED at YM-3B** — final measured-data verdict `DATA-INDETERMINATE`; original structural non-crossability hypothesis not established
**Primary active chamber:** none — CORR-I v0.1.2 is frozen as the terminal chamber
**Development mode:** local-first; GitHub is reference only until the local project is mature

---

## 1. Core project hypothesis

Frozen hypothesis:

> **Gapless Yang–Mills continuation is structurally non-generable under refinement, whereas the massive branch is refinement-stable.**

Stronger target:

> **The Yang–Mills mass gap corresponds to a refinement-stable non-crossability boundary separating the vacuum from every non-vacuum admissible state.**

Conceptual summary:

\[
\boxed{
\text{Mass gap = refinement-stable non-crossability of the vacuum boundary.}
}
\]

The project must not merely rediscover a nonzero mass scale. It must test whether a gapless route toward the vacuum becomes structurally unavailable, and whether that obstruction survives refinement.

---

## 2. Non-negotiable project tests

The investigation was frozen around four requirements:

1. use gauge-invariant observables;
2. construct the gapless branch adversarially rather than merely note its absence;
3. require any obstruction to survive common refinement;
4. eventually connect structural separation quantitatively to the physical Hamiltonian spectrum.

Until item 4 is achieved, results must be described as structural diagnostics/findings rather than a Yang–Mills mass-gap proof.

---

## 3. Project phases

### YM-0 — Formalization
Define:
- vacuum boundary;
- admissible Yang–Mills structural family;
- massive branch;
- adversarial gapless branch;
- structural distance from vacuum;
- falsification criteria.

**Status:** complete for the present program.

### YM-1 — Gauge-invariant corpus
Build the working corpus from gauge-invariant lattice quantities.

**Status:** sufficient for current work.

### YM-2 — Vacuum-boundary experiment
Construct massive and adversarial gapless continuations and determine whether the structural machinery discriminates them.

**Status:** closed by `docs/SYNTHESIS_YM2.md`.

### YM-3 — Common refinement
Test whether the massive-side CORR-I signature persists under the AT20 refinement sequence.

**Status:** closed. YM-3A ended `MODEL-REFINEMENT PERSISTENT`; YM-3B ended `DATA-INDETERMINATE` with a central crossing at beta = 6.71.

### YM-4 — Bridge theorem
Seek a relation of the form

\[
D_{\rm YM}(L,V)\ge\delta_G>0
\]

together with

\[
E(L)-E(V)\ge F_G(D_{\rm YM}),
\]

so that

\[
\Delta_G\ge F_G(\delta_G)>0.
\]

**Status:** not entered; cancelled at project closure.

---

## 4. Primary physical source

Main source:

**Andreas Athenodorou & Michael Teper,  
“The glueball spectrum of SU(3) gauge theory in 3+1 dimensions,”  
JHEP 11 (2020) 172, arXiv:2007.06422.**

Important source facts already established:

- the paper uses gauge-invariant glueball operators;
- it constructs cross-correlators and optimized correlators variationally;
- effective energy is extracted through
  \[
  aE_{\rm eff}(n_t)=-\ln[C(n_t)/C(n_t-1)];
  \]
- exact effective mass should decrease for the relevant positive-spectral correlators, with late-time increases attributed to statistical fluctuations;
- β = 6.50 on \(38^4\) is the finest lattice used for the effective-mass plots;
- the \(0^{++}\) ground state is the mass-gap state;
- published β = 6.50 mass:
  \[
  aM_{0^{++}}=0.3474(22).
  \]

AT20 does **not** tabulate the full raw correlator matrices or covariance needed for a fully statistical CORR-I analysis.

---

## 5. AT20 refinement backbone

The current eight-level refinement sequence is:

| β | \(a\sqrt{\sigma}\) | \(aM_G\) |
|---:|---:|---:|
| 5.6924 | 0.3999 | 0.987 |
| 5.80 | 0.31666 | 0.908 |
| 5.8941 | 0.26118 | 0.7991 |
| 5.99 | 0.21982 | 0.7045 |
| 6.0625 | 0.19472 | 0.6365 |
| 6.235 | 0.15003 | 0.4969 |
| 6.3380 | 0.12928 | 0.4276 |
| 6.50 | 0.10383 | 0.3474 |

Known detail:
- at β = 5.8941, Table 1 gives mass gap `0.7991(92)` while Table 8 gives A1++ ground `0.799(10)`;
- both values were preserved in the extracted corpus rather than silently reconciled.

---

## 6. Existing AT20 project corpus

Current extracted/derived AT20 material includes:

- `data/raw/at20.zip`
- `data/raw/at20/`
- `at_lat.csv`
- `at_aux.csv`
- `at_mass.csv`
- `at_cont.csv`
- `at_flux.csv`
- `at_cov.csv`

Scale of extracted corpus:

- 443 lattice glueball masses;
- 59 continuum ratios;
- 8 flux-tube energies;
- 8 refinement levels.

---

## 7. First YM-2 representation: vacuum-anchored spectral ladders

Five state identities were used across all eight β values:

- `c1` — A1++ ground state;
- `c2` — A1++ first excited state;
- `c3` — E++ ground state;
- `c4` — T2++ ground state;
- `c5` — A1-+ ground state.

The vacuum node was explicitly added:

\[
L_i^{YM}=(0,x_1,x_2,x_3,x_4,x_5).
\]

Four adversarial families were constructed:

- `offset`
- `upctrl`
- `scale`
- `gaponly`

with \(k=0,\ldots,10\).

### STRUC-I result

No vacuum-specific rejection was found.

Across baselines and offset cases:
- all 88 remained **Geometric Persistence**;
- only Stable/Weak state changes occurred;
- no regime transition occurred.

The six-node vacuum-anchored representation remained admissible even under a factor-1024 vacuum-gap compression.

### STRUC-PERC-I result

Observed totals:

| Family | FULL | HARD |
|---|---:|---:|
| offset | 19 | 61 |
| upctrl | 21 | 59 |
| scale | 80 | 0 |
| gaponly | 8 | 72 |

Interpretation:

- downward vacuum-gap compression can fragment the gap graph;
- upward translation can do so too;
- uniform scaling remains invariant;
- selective displacement is the dominant driver;
- fragmentation is therefore not uniquely tied to approach toward the vacuum.

Frozen conclusion:

\[
\boxed{
\text{spectral-gap connectivity can collapse while structural admissibility survives}
}
\]

and

\[
\boxed{
\text{the short spectral-ladder representation does not establish vacuum-specific non-crossability.}
}
\]

This was treated as a successful falsification of the representation/test pair.

---

## 8. Why CORR-I was created

The short mass ladder is already a compressed output of a deeper Euclidean spectral object.

CORR-I was therefore introduced to operate directly on

\[
C(t)=\int_0^\infty \rho(E)e^{-Et}\,dE,
\qquad \rho(E)\ge0.
\]

The chamber tests correlator-side spectral structure rather than only sorted mass coordinates.

### CORR-I baseline checks

- positivity;
- monotonicity;
- discrete log-convexity;
- effective mass;
- plateau behavior;
- Hankel/Hausdorff positive-moment consistency.

### CORR-I adversary

Frozen form:

\[
C_{\rm adv}(t)
=
(1-\alpha)C(t)+\alpha e^{-\mu(t-t_0)}.
\]

Rather than use a fixed arbitrary \(\alpha\), CORR-I computes

\[
\alpha_{\max}(\mu),
\]

the largest compatible low-energy spectral admixture under the active limits.

Identity null:

\[
\alpha=0
\]

must reproduce the baseline exactly.

### Current descriptive metric

\[
R_{\rm contract}
=
\frac{\alpha_{\max}(\mu/m_{\rm ref}=10^{-3})}
{\alpha_{\max}(\mu/m_{\rm ref}=1)}.
\]

Smaller \(R_{\rm contract}\) means stronger suppression of added near-zero spectral weight.

This is a chamber coordinate, not the physical mass gap.

---

## 9. CORR-I versions

### v0.1.0
Initial prototype.

Problem discovered:
- fixed \(\alpha=0.05\) adversary was already too strong near \(\mu/m_{\rm ref}=1\).

This version was superseded.

### v0.1.1
Frozen mathematical redesign.

Added:
- \(\alpha_{\max}(\mu)\) compatibility envelope;
- \(\alpha=0\) identity null.

Self-test passed.

### v0.1.2
Operational batch upgrade.

Added:
- multiple CSV selection;
- wide multi-channel CSV support;
- `RUN BATCH + ZIP`;
- automatic per-channel JSON + envelope CSV exports;
- `batch_summary.csv`;
- `batch_record.json`;
- visible batch result table.

Important:

> **The v0.1.2 batch upgrade did not alter the v0.1.1 baseline or envelope mathematics.**

Current active chamber package:

`CORR_I_v012.zip`

---

## 10. CORR-I self-test

Analytic self-test:

\[
C(t)=0.78e^{-0.52t}+0.22e^{-1.35t}.
\]

v0.1.1 results:

- positivity passed;
- monotonicity passed;
- log-convexity passed;
- plateau found;
- \(m_{\rm ref}\approx0.5200002\);
- all Hankel tests passed;
- classification:
  `POSITIVE-SPECTRAL CONSISTENT`;
- identity null passed exactly;
- deepest \(\alpha_{\max}\approx2.67\times10^{-6}\);
- strong contraction toward \(0^+\).

This validated the redesigned chamber before physical-side use.

---

## 11. First physical-side correlator proxy

AT20 does not publish raw \(C(t)\), so Figure 7 at β = 6.50 was digitized for the \(0^{++}\) ground state.

Approximate effective masses:

```text
0.3588
0.3480
0.3450
0.3443
0.3511
0.3611
0.3553
0.3511
0.3606
0.3910
```

Using

\[
C(0)=1,
\qquad
C(n+1)=C(n)e^{-m_{\rm eff}(n+1/2)},
\]

a normalized correlator proxy was reconstructed.

Important provenance:

> This is a published-figure reconstruction, not the raw AT20 correlator.

### Result

Baseline:
- 11 positive points;
- monotonicity violations: 0;
- log-convexity violations: 4;
- plateau not found;
- higher-rank Hankel tests fail;
- classification:
  `SPECTRAL-POSITIVITY TENSION`.

Interpretation:
- this does not mean the actual Yang–Mills correlator violates positivity;
- the proxy contains digitization/statistical fluctuations;
- AT20 explicitly notes late-time statistical rise in the effective mass.

Adversarial envelope:
- deepest \(\alpha_{\max}\approx0.00358145\);
- contraction ratio:
  \[
  R_{\rm raw}\approx0.007163.
  \]

---

## 12. Published-mass massive control

A clean control was built from the published β = 6.50 value:

\[
aM=0.3474.
\]

Control:

\[
C_{\rm massive}(t)=e^{-0.3474t},
\qquad t=0,\ldots,10.
\]

The quoted ±0.0022 mass uncertainty is retained as a correlated mass-model band only, not as independent pointwise correlator error bars.

### Result

Baseline:
- positive;
- monotone;
- zero log-convexity violations;
- plateau found immediately;
- \(m_{\rm ref}=0.3474\);
- all Hankel tests pass;
- classification:
  `POSITIVE-SPECTRAL CONSISTENT`.

Envelope:
- \(\alpha_{\max}(1)=0.5\);
- deepest \(\alpha_{\max}\approx0.0038438247\);
- contraction ratio:
  \[
  \boxed{R_{\rm massive}\approx0.00768765}.
  \]

Important robustness observation:

\[
R_{\rm raw}\approx0.00716
\]

versus

\[
R_{\rm massive}\approx0.00769.
\]

Therefore the strong near-zero contraction is not created solely by the noisy Figure-7 reconstruction.

---

## 13. First genuinely gapless control

Positive spectral density:

\[
\rho(E)=\frac{1}{\theta}e^{-E/\theta},
\qquad E\ge0.
\]

Correlator:

\[
C(t)=\frac{1}{1+\theta t}.
\]

With

\[
\theta=e^{0.3474}-1,
\]

the first effective-mass interval matches the massive control exactly:

\[
m_{\rm eff}(0.5)=0.3474.
\]

Because the spectral support reaches \(E=0\), this control has no positive mass gap.

### Result

- `POSITIVE-SPECTRAL CONSISTENT`;
- no plateau;
- deepest \(\alpha_{\max}\approx0.0203665\);
- contraction ratio:
  \[
  R_{p=1}\approx0.326916.
  \]

This is about \(42.5\times\) the massive contraction ratio.

---

## 14. Gapless Gamma-family controls

Family:

\[
C_p(t)=(1+\theta_p t)^{-p},
\]

with

\[
\theta_p=e^{0.3474/p}-1.
\]

Corresponding spectral density:

\[
\rho_p(E)
=
\frac{E^{p-1}e^{-E/\theta_p}}
{\Gamma(p)\theta_p^p},
\qquad E\ge0.
\]

Every member:
- is positive spectral;
- has support down to \(E=0\);
- is exactly gapless;
- satisfies
  \[
  m_{\rm eff}(0.5)=0.3474;
  \]
- uses \(t=0,\ldots,10\).

Batch family tested:

\[
p=0.5,\;1,\;2,\;4,\;8.
\]

### Frozen results

| Representation | \(R_{\rm contract}\) | Relative to massive |
|---|---:|---:|
| gapless \(p=0.5\) | 0.500947 | 65.2× |
| gapless \(p=1\) | 0.326916 | 42.5× |
| gapless \(p=2\) | 0.178612 | 23.2× |
| gapless \(p=4\) | 0.084534 | 11.0× |
| gapless \(p=8\) | 0.037668 | 4.90× |
| massive control | 0.007688 | 1× |

All gapless family members were:
- positive;
- monotone;
- log-convex;
- Hankel/Hausdorff consistent;
- `POSITIVE-SPECTRAL CONSISTENT`;
- without a stable constant-mass plateau.

Frozen ordering:

\[
R_{0.5}>R_1>R_2>R_4>R_8>R_{\rm massive}.
\]

This means the CORR-I response moves continuously toward the massive result as a gapless correlator becomes increasingly exponential-like on the finite observation window, but even the difficult \(p=8\) case remains separated from the massive control.

---

## 15. YM-2 scientific conclusion

The correct stage conclusion is:

\[
\boxed{
\textbf{VACUUM-BOUNDARY DIAGNOSTIC ESTABLISHED; REFINEMENT TEST REQUIRED}
}
\]

More explicitly:

> A short vacuum-anchored mass ladder did not establish vacuum-specific non-crossability. A correlator-native chamber was therefore developed and frozen. CORR-I distinguishes the AT20 massive-side representation from multiple legitimate positive-spectral gapless controls. The separation is systematic across a controlled gapless Gamma family and is robust to replacement of the noisy Figure-7 reconstruction by a clean published-mass plateau control. This establishes a viable structural discriminator for YM-3, but not yet refinement-stable Yang–Mills non-crossability.

---

## 16. Claims that must NOT be made yet

Do not claim that:

- CORR-I proves the Yang–Mills mass gap;
- the digitized Figure-7 proxy is raw lattice correlator data;
- \(R_{\rm contract}\) is the physical mass gap;
- the current fixed-resolution separation is already refinement-stable;
- the massive control is an independent physical measurement;
- the structural diagnostic already implies a Hamiltonian spectral theorem.

The project remains deliberately stricter than that.

---

## 17. Current project structure

Recommended local placement:

```text
UNNS_YM_GAP/
│
├── README.md
├── PROTOCOL.md
├── HYPOTHESES.md
├── DATA_PLAN.md
├── REFINEMENT_PLAN.md
├── FALSIFICATION.md
├── Context.md
│
├── data/
│   ├── raw/
│   └── derived/
│       └── corr_i/
│           ├── at20_0pp_b650/
│           ├── at20_0pp_b650_control/
│           ├── gapless_control/
│           └── gapless_family/
│
├── chambers/
│   └── corr_i/
│       └── CORR_I_v012/
│
├── ladders/
├── nulls/
├── scripts/
├── output/
│
└── docs/
    └── SYNTHESIS_YM2.md
```

### Exact requested placement

Put:

```text
SYNTHESIS_YM2.md
```

here:

```text
UNNS_YM_GAP/docs/SYNTHESIS_YM2.md
```

Put this context file:

```text
Context.md
```

at the project root:

```text
UNNS_YM_GAP/Context.md
```

The root placement is intentional: `Context.md` is the handoff document for a new conversation, while `docs/SYNTHESIS_YM2.md` is a permanent scientific stage record.

---

## 18. Active artifacts at the handoff point

Important local artifacts to preserve:

### Project framing
- `project_UNNS_Yang–Mills_ Gap.pdf`

### YM-2 synthesis
- `docs/SYNTHESIS_YM2.md`

### YM-3 preregistration
- `docs/PREREG_YM3.md`
- `docs/PREREG_YM3.json`
- `docs/YM3_INPUT_MATRIX.csv`

### CORR-I
- `CORR_I_v012.zip`
- `corr_i_v012.html`

### Physical-side correlator inputs
- `CORR_I_AT20_0PP_v001.zip`
- `CORR_I_AT20_0PP_CONTROL_v001.zip`

### Gapless controls
- `CORR_I_GAPLESS_CTRL_v001.zip`
- `CORR_I_GAPLESS_FAM_v001.zip`

### Batch result
- `corr_i_batch_4_csv_files.zip`

### Primary source
- AT20 PDF / arXiv PDF

### Earlier project corpus
- AT20 extracted data package
- YM1A spectral ladders
- G0.1 vacuum-anchored families
- STRUC-I outputs
- STRUC-PERC-I outputs

---

## 19. What to upload in the next chat

For efficient continuation from the completed YM-3A result, upload at minimum:

1. `Context.md`
2. `docs/SYNTHESIS_YM2.md`
3. `docs/PREREG_YM3.md`
4. `docs/YM3_RESULT.md`
5. `docs/YM3_RESULT.json`
6. `docs/YM3_BUILD_RECORD.md`
7. `docs/YM3_INPUT_MATRIX.csv`
8. `output/ym3/YM3_SUMMARY.csv`
9. `project_UNNS_Yang–Mills_ Gap.pdf`

For reproducibility of the completed Class C experiment, also keep available:

10. `chambers/corr_i/corr_i_v012.html`;
11. `scripts/ym3/run_corr_i.py`;
12. the current AT20 extracted-data package;
13. the AT20 source PDF.

If the complete synchronized project ZIP is available, it subsumes these individual uploads.

There is no need to rerun YM-2 or YM-3A controls unless a scientific reason requires it.

---

## 20. Immediate next task in the new chat

Continue **YM-3 — Common Refinement** from the completed YM-3A result.

The preregistered Class C batch is finished and recorded in:

- `docs/YM3_RESULT.md`
- `docs/YM3_RESULT.json`
- `output/ym3/YM3_SUMMARY.csv`
- `output/ym3/YM3_RUN_RECORD.json`

Frozen YM-3A verdict:

\[
\boxed{
\textbf{MODEL-REFINEMENT PERSISTENT}
}
\]

All eight massive Class C inputs remained positive-spectral consistent with stable plateaus and passing identity nulls. Both preregistered hard margins remained positive at every refinement level, the full matched Gamma ordering remained intact, and the native-grid diagnostic did not reverse the separation.

The allowed stage statement is:

> **The massive-side CORR-I signature is persistent across the AT20 mass-anchored Class C refinement sequence.**

The next practical task is **YM-3B data acquisition and admission**. Seek additional non-Class-C information sufficient for a genuine measured-data refinement comparison, respecting the frozen admission rule: at least three ordered levels on a primary refinement axis when available, a second independent refinement axis, matched physical/adversarial processing, a frozen chamber, and explicit boundary tracking.

Any interpolation, resampling, covariance handling, or uncertainty model for newly acquired Class A/B data must be preregistered in a supplementary YM-3B protocol **before** inspecting the resulting refinement behavior.

Do not rerun YM-3A unless a scientific reason requires it.

Do not jump directly to a continuum theorem.

---

## 21. Important methodological caution for YM-3

The evidence-class distinction is now frozen in `docs/PREREG_YM3.md` and `docs/YM3_INPUT_MATRIX.csv`.

### Class A — raw or published correlator-level data
Best available evidence. None is currently available across the eight-level AT20 backbone in the local package.

### Class B — published effective-mass trajectories
The present physical-side Class B anchor is the β = 6.50 Figure-7 `0++` reconstruction already frozen in YM-2.

### Class C — exact single-exponential controls anchored only to published fitted masses
Available across all eight β values and used for the executable YM-3A mass-anchored model-refinement sequence.

The project therefore explicitly separates:

- **YM-3A:** eight-level Class C model refinement, **complete — `MODEL-REFINEMENT PERSISTENT`**;
- **YM-3B:** measured correlator/effective-mass refinement, **next — requires additional Class A/B data**.

For the seven coarser β values, evaluating exact exponentials on the preregistered common physical-time grid remains a model construction. It must never be described as interpolated raw lattice correlator data.

A positive YM-3A result may show that the frozen CORR-I massive-side signature is refinement-persistent in the AT20 mass-anchored model family. It does not by itself establish refinement stability of measured Yang–Mills correlators.

The original minimum refinement standard and the later Hamiltonian bridge requirement remain unchanged.

---

## 22. Research style and workflow preferences

Keep the following project conventions:

- local-first development;
- GitHub remains reference-only until the local research is mature;
- use short Windows-safe filenames;
- do not create needless deep folder hierarchies;
- preserve meaningful words such as `output`, `RUN_EXAMPLE`, `Context`;
- no placeholders;
- do not modify canonical STRUC-I;
- reproducibility matters: README, manifest, scripts, batch files where appropriate;
- do not repeat completed runs unless a scientific reason requires it;
- distinguish positive findings from limitations without weakening valid results;
- preserve the difference between:
  - structural admissibility,
  - connectivity,
  - mass generation,
  - confinement,
  - mass gap.

---

## 23. One-line continuation instruction

When opening the next chat, the working instruction is:

> **Continue `UNNS_YM_GAP` in active YM-3 from the completed YM-3A result. Treat `SYNTHESIS_YM2.md`, `docs/PREREG_YM3.md`, and `docs/YM3_RESULT.md` as frozen stage records, keep CORR-I v0.1.2 mathematically unchanged, do not rerun YM-3A without scientific cause, and proceed to YM-3B Class A/B data acquisition plus a supplementary preregistration before any measured-data refinement run.**

---

## YM-3B source-admission update — 2026-09-30

YM-3A remains frozen as `MODEL-REFINEMENT PERSISTENT`.

The primary YM-3B Class B source has now been admitted and preregistered:

- Sakai & Sasaki (2023), Phys. Rev. D 107, 034510;
- pure SU(3) Yang-Mills, standard Wilson plaquette action;
- `A1++` / `0++` ground-state effective-mass trajectories;
- beta = 6.20, 6.40, 6.71, 6.93;
- Figures 9–12;
- evidence class B.

Frozen supplementary protocol:

`docs/PREREG_YM3B.md`

Source audit:

`docs/YM3B_SOURCE_AUDIT.md`

Admission matrix:

`docs/YM3B_ADMISSION.csv`

The next action is digitization and Class B input construction under the frozen YM-3B protocol.
No YM-3B CORR-I scientific result has yet been produced.

---

## YM-3B SS23 input-build update - 2026-09-30

The primary four-level Sakai-Sasaki Class B sequence has now been digitized and reconstructed under
the frozen `docs/PREREG_YM3B.md` protocol.

Status:

- beta 6.20, 6.40, 6.71, 6.93 digitized from Figures 9-12;
- four normalized native variational-eigenvalue proxies reconstructed;
- frozen seven-point common physical-time inputs built;
- preregistered PCHIP sensitivity inputs built;
- all four levels pass the pre-CORR-I admission checks;
- no YM-3B CORR-I scientific batch has yet been run.

Permanent build record:

`docs/YM3B_BUILD_RECORD.md`

Admission record:

`output/ym3b/admission/YM3B_INPUT_ADMISSION.csv`

Next action:

construct the beta-matched Gamma controls, verify the frozen CORR-I v0.1.2 hash, and execute the
complete four-beta YM-3B batch without inspecting partial beta results.

---

## YM-3B execution update - 2026-09-30

The full preregistered Sakai-Sasaki four-beta Class B CORR-I batch has been executed.

- frozen CORR-I v0.1.2 hash: PASS;
- 4 measured Class B inputs completed;
- 20 beta-matched Gamma controls completed;
- PCHIP interpolation sensitivity completed;
- R3 L5/L6/L7 sensitivity completed;
- 2,000 no-covariance draws per beta completed last.

Frozen-rule verdict:

**DATA-INDETERMINATE**

The central beta=6.71 result crosses slightly to `S_B < 0`, but the preregistered uncertainty
ensemble spans both signs there. Therefore the available published-figure precision does not
support a stable crossed/persistent classification.

Permanent record:

`docs/YM3B_RESULT.md`

Next scientific move:

freeze and execute the independent Liang14 two-level Class B replication, then audit Chen06 for
a possible five-level Class B extension.

---

## FINAL PROJECT CLOSURE — 2026-09-30

`UNNS_YM_GAP` is closed.

The original hypothesis of a refinement-stable, non-crossable Yang-Mills vacuum boundary in UNNS
structural space was **not established**.

The decisive Class B Sakai-Sasaki central sequence was:

\[
S_B =
(+0.020350,\ +0.035867,\ -0.003395,\ +0.051851)
\]

for beta = 6.20, 6.40, 6.71, 6.93.

The beta = 6.71 crossing survived the frozen interpolation and R3 ladder-length checks, but its
2,000-draw no-covariance uncertainty interval crossed zero. The frozen terminal verdict is therefore:

**`DATA-INDETERMINATE`**

No additional Liang14, Chen06, source-acquisition, CORR-I redesign, or YM-4 test will be performed
inside this project.

Canonical terminal records:

- `FINAL_STATUS.md`
- `docs/FINAL_SYNTHESIS.md`
- `docs/STAGE0_ORIGIN.md`
- `docs/YM3B_RESULT.md`
- `docs/YM3_RESULT.md`
- `docs/SYNTHESIS_YM2.md`

A future project may use this investigation as Stage 0 / origin evidence, but the present project
must not be retrospectively reinterpreted. Its frozen conclusion is:

> The proposed refinement-stable structural vacuum boundary was not established; the central Class B
> trajectory crossed the proposed boundary once, while uncertainty prevented definitive falsification.
