# SYNTHESIS_YM2.md

## UNNS Yang–Mills Gap / Vacuum Boundary Non-Crossability  
### YM-2 Stage Synthesis — Vacuum-Boundary Experiment

**Project:** `UNNS_YM_GAP`  
**Stage closed:** YM-2 — Vacuum-boundary experiment  
**Next stage:** YM-3 — Common refinement  
**Primary chamber at stage close:** CORR-I v0.1.2  
**Status:** Stage synthesis / frozen handoff record

---

## 1. Purpose of this synthesis

This document closes the first complete vacuum-boundary investigation of the UNNS Yang–Mills Gap project.

The project hypothesis was frozen at the outset as:

> **Gapless Yang–Mills continuation is structurally non-generable under refinement, whereas the massive branch is refinement-stable.**

The stronger target remains:

> **The Yang–Mills mass gap corresponds to a refinement-stable non-crossability boundary separating the vacuum from every non-vacuum admissible state.**

YM-2 was not intended to prove that statement. Its task was narrower and necessary: construct explicit massive and adversarial gapless continuations, determine whether the available UNNS machinery can discriminate them, falsify inadequate representations, and leave behind a frozen diagnostic suitable for the refinement test.

That objective has now been met.

The central stage result is:

\[
\boxed{
\text{A correlator-native UNNS diagnostic distinguishes massive-side structure from
positive-spectral gapless structure, while the corresponding refinement stability remains untested.}
}
\]

This is a chamber-level structural result. It is **not** a Yang–Mills mass-gap proof.

---

## 2. Original YM-2 question

The conventional spectral question is whether the physical Yang–Mills Hamiltonian admits arbitrarily low positive-energy excitations above the vacuum.

In the UNNS framing, the corresponding adversarial question is:

\[
V \to X_1 \to X_2 \to \cdots,
\qquad
E(X_n)-E(V)\to0^+,
\]

and whether that continuation can remain structurally admissible.

The initial operational plan was therefore to compare:

1. a **physical massive branch**, and
2. an explicitly constructed **gapless branch** approaching the vacuum,

under a frozen structural grammar.

The project protocol required four non-negotiable conditions:

- gauge-invariant observables;
- an adversarially constructed gapless continuation rather than mere absence of low-energy states;
- persistence of any obstruction under common refinement;
- eventual quantitative connection between structural separation and the physical Hamiltonian spectrum.

YM-2 addresses the first two directly. The third belongs to YM-3. The fourth remains the later bridge-theorem program.

---

## 3. Physical corpus and refinement backbone

The principal physical source for this stage is:

**A. Athenodorou and M. Teper, “The glueball spectrum of SU(3) gauge theory in 3+1 dimensions,” JHEP 11 (2020) 172, arXiv:2007.06422.**

The extracted AT20 corpus provides eight lattice refinements:

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

The normalized gap trajectory approaches the published continuum value \(M_{0^{++}}/\sqrt{\sigma}=3.405(21)\).

For YM-2, the finest lattice, β = 6.50 on \(38^4\), became the first correlator-side test case because AT20 provides its finest effective-mass resolution there and explicitly identifies the \(0^{++}\) ground state as the mass-gap state.

---

## 4. First attempt: spectral-ladder vacuum anchoring

### 4.1 YM1A ladder

The first physical representation used five glueball-state coordinates available across all eight β values:

- \(c_1\): \(A_1^{++}\) ground state — the \(0^{++}\) mass-gap state;
- \(c_2\): \(A_1^{++}\) first excited state;
- \(c_3\): \(E^{++}\) ground state;
- \(c_4\): \(T_2^{++}\) ground state;
- \(c_5\): \(A_1^{-+}\) ground state.

The explicit vacuum node was then added:

\[
L_i^{YM}=(0,x_1,x_2,x_3,x_4,x_5).
\]

This correction was essential. Without the vacuum node, a common translation of all positive masses leaves adjacent internal spacings unchanged and is therefore invisible to a gap-based structural chamber.

### 4.2 Adversarial families

Four frozen deformation families were constructed:

- **offset** — translate all positive states downward while holding the vacuum at zero;
- **upctrl** — translate all positive states upward by the corresponding amount;
- **scale** — uniformly multiply all positive states by \(\epsilon\);
- **gaponly** — move only the lowest state toward the vacuum.

The deformation parameter used a dyadic sequence \(\epsilon=2^{-k}\), with \(k=0,\ldots,10\).

### 4.3 STRUC-I outcome

STRUC-I did **not** produce a vacuum-boundary rejection.

Across the physical baselines and the offset family:

- all cases remained in **Geometric Persistence**;
- several Stable Structure ↔ Weak Persistence changes occurred;
- no chamber regime transition occurred.

Therefore the six-node vacuum-anchored ladder remained structurally admissible under a \(1024\times\) compression of the vacuum gap.

This falsified the expectation that STRUC-I, at this spectral resolution, would identify the desired vacuum non-crossability.

### 4.4 STRUC-PERC-I outcome

STRUC-PERC-I was more sensitive, but the directionality test failed.

Observed totals:

| Family | FULL | HARD |
|---|---:|---:|
| offset | 19 | 61 |
| upctrl | 21 | 59 |
| scale | 80 | 0 |
| gaponly | 8 | 72 |

The important facts were:

- physical baselines were connected;
- downward vacuum-gap compression often fragmented the pairwise gap graph;
- **upward** translation away from the vacuum also fragmented it;
- uniform global scaling left the normalized connectivity geometry invariant;
- gap-only deformation produced the strongest fragmentation.

The operative variable was therefore not uniquely “approach to the vacuum.” It was selective displacement of one or more gap coordinates relative to the fixed internal gap distribution, combined with the chamber’s IQR-based normalization.

The correct conclusion from the first representation was:

\[
\boxed{
\text{spectral-gap connectivity can collapse while STRUC-I admissibility survives.}
}
\]

and

\[
\boxed{
\text{the six-node spectral representation does not establish vacuum-specific non-crossability.}
}
\]

This was a successful falsification of a representation/test pair, not a failure of the wider project.

---

## 5. Representation change: why CORR-I was necessary

The spectral-ladder attempt exposed a conceptual limitation: a short ordered list of extracted masses is already a compressed product of the underlying Euclidean correlation structure.

The mass-gap question is fundamentally spectral. Euclidean two-point correlators retain more direct information about spectral support:

\[
C(t)=\int_0^\infty \rho(E)e^{-Et}\,dE,
\qquad \rho(E)\ge0.
\]

This motivated a new chamber designed specifically for correlators:

# CORR-I

CORR-I does not classify sorted mass ladders. It evaluates whether a Euclidean correlator is consistent with a positive spectral representation and how much additional low-energy spectral weight can be inserted before the observed correlator is materially altered.

The move from STRUC-I/STRUC-PERC-I to CORR-I was therefore not a relaxation of the hypothesis. It was a correction of the representation.

---

## 6. CORR-I development and freeze

### 6.1 Baseline layer

CORR-I tests:

- positivity of \(C(t)\);
- monotonic decrease;
- discrete log-convexity;
- effective-mass evolution,
  \[
  m_{\rm eff}(t)=\log\frac{C(t)}{C(t+\Delta t)};
  \]
- plateau persistence;
- Hankel/Hausdorff moment positivity on equally spaced grids.

The baseline verdict language is deliberately limited:

- `POSITIVE-SPECTRAL CONSISTENT`
- `SPECTRAL-POSITIVITY TENSION`
- `NONUNIFORM GRID — MOMENT TEST LIMITED`
- `INVALID FOR POSITIVE-SPECTRAL TEST`

### 6.2 Adversarial layer

The initial fixed-amplitude low-energy admixture was replaced after self-testing.

The frozen v0.1.1/v0.1.2 adversary is:

\[
C_{\rm adv}(t)
=
(1-\alpha)C(t)+\alpha e^{-\mu(t-t_0)}.
\]

Instead of choosing an arbitrary \(\alpha\), the chamber determines

\[
\boxed{\alpha_{\max}(\mu)}
\]

— the largest added spectral weight compatible with the active deviation limits.

This produces a compatibility envelope as the trial energy approaches zero.

An explicit identity control is always included:

\[
\alpha=0,
\]

which must reproduce the baseline exactly.

### 6.3 Stage metric

For the current no-covariance tests, a compact descriptive metric is

\[
R_{\rm contract}
=
\frac{\alpha_{\max}(\mu/m_{\rm ref}=10^{-3})}
{\alpha_{\max}(\mu/m_{\rm ref}=1)}.
\]

Small \(R_{\rm contract}\) means strong suppression of additional spectral weight as the trial scale approaches \(0^+\).

It is a chamber diagnostic, not a physical mass-gap observable.

### 6.4 Version freeze

- **v0.1.1** introduced the \(\alpha_{\max}(\mu)\) envelope and identity null.
- **v0.1.2** added genuine multi-file/multi-channel batch execution and ZIP export.
- The v0.1.2 batch upgrade did **not** change the baseline or envelope mathematics.

---

## 7. CORR-I self-test

The analytic self-test used a positive two-exponential correlator.

It passed:

- positivity;
- monotonicity;
- log-convexity;
- effective-mass plateau detection;
- Hankel/Hausdorff checks;
- exact \(\alpha=0\) identity control.

The self-test also showed why the fixed-\(\alpha\) design was inadequate: a 5% admixture was already in tension at the top of the scan. This directly motivated the compatibility-envelope formulation.

After the redesign, the self-test produced a smooth contraction of \(\alpha_{\max}\) toward \(0^+\), with the identity null preserved exactly.

CORR-I v0.1.1 was therefore frozen before physical use.

---

## 8. First physical-side correlator representation

AT20 does not tabulate the original correlator matrix \(C_{ij}(t)\). It presents effective-mass plots and resulting mass estimates.

The first physical-side input was therefore reconstructed from the β = 6.50 \(0^{++}\) ground-state effective-mass series in Figure 7.

Using

\[
C(0)=1,
\qquad
C(n+1)=C(n)e^{-aM_{\rm eff}(n+1/2)},
\]

a normalized published-figure proxy was built.

This representation was explicitly labelled:

> **published-figure reconstruction; not the authors’ raw lattice correlator.**

### 8.1 Figure-7 proxy result

The reconstructed baseline contained:

- 11 positive correlator points;
- zero monotonicity violations;
- four log-convexity violations;
- no plateau under the frozen threshold;
- failed higher-rank Hankel tests.

CORR-I therefore classified it:

`SPECTRAL-POSITIVITY TENSION`.

This was not interpreted as a failure of Yang–Mills spectral positivity. AT20 itself discusses the late-time rise of the \(0^{++}\) effective mass as a statistical fluctuation. The exact moment tests are sufficiently strict that the digitized/noisy proxy is not expected to behave like the unavailable raw correlator.

Despite the baseline tension, its descriptive near-zero envelope showed strong contraction:

\[
R_{\rm raw}\approx0.007163,
\]

with deepest

\[
\alpha_{\max}\approx0.003581.
\]

---

## 9. Published-mass plateau control

To separate physical scale from Figure-7 noise, a second controlled representation was constructed from the published β = 6.50 mass estimate:

\[
aM=0.3474(22).
\]

The central control was:

\[
C_{\rm massive}(t)=e^{-0.3474t},
\qquad t/a=0,\ldots,10.
\]

The published ±0.0022 mass uncertainty was retained as a correlated mass-model band and was **not** converted into independent pointwise correlator uncertainties.

### 9.1 Baseline result

The control passed exactly:

- 11/11 positive points;
- zero monotonicity violations;
- zero log-convexity violations;
- immediate stable plateau;
- \(m_{\rm ref}=0.3474\);
- all Hankel/Hausdorff checks passed;
- `POSITIVE-SPECTRAL CONSISTENT`.

### 9.2 Near-zero envelope

The massive control produced:

\[
\alpha_{\max}(1)=0.5,
\]

\[
\alpha_{\max}(10^{-3})\approx0.0038438,
\]

and

\[
\boxed{
R_{\rm massive}\approx0.00768765.
}
\]

The raw Figure-7 proxy and the clean published-mass control therefore agreed at the level relevant to the adversarial envelope:

\[
R_{\rm raw}\approx0.00716,
\qquad
R_{\rm massive}\approx0.00769.
\]

The late-time digitization/statistical fluctuations strongly affected exact positivity tests, but they did **not** create the strong near-zero envelope contraction.

This was the first robustness result of CORR-I.

---

## 10. Genuine gapless positive-spectral control

A single gapless control was then constructed with

\[
\rho(E)=\frac{1}{\theta}e^{-E/\theta},
\qquad E\ge0,
\]

so that the spectral support extends continuously to \(E=0\).

Its correlator is

\[
C(t)=\frac{1}{1+\theta t}.
\]

The parameter

\[
\theta=e^{0.3474}-1
\]

was chosen so that the first effective-mass interval exactly matches the massive control:

\[
m_{\rm eff}(0.5)=0.3474.
\]

Thus the comparison does not merely contrast different initial scales.

### 10.1 Gapless-control result

The control was:

- positive;
- monotone;
- log-convex;
- Hankel/Hausdorff consistent;
- `POSITIVE-SPECTRAL CONSISTENT`;
- without a constant effective-mass plateau.

Its envelope gave:

\[
\alpha_{\max}(1)\approx0.062299,
\]

\[
\alpha_{\max}(10^{-3})\approx0.020367,
\]

and

\[
\boxed{
R_{p=1}\approx0.326916.
}
\]

This is roughly \(42.5\times\) the massive contraction ratio.

Therefore CORR-I does **not** generically force every positive-spectral correlator into the same strong near-zero contraction.

---

## 11. Gapless Gamma-family falsification

One gapless control was not enough. A wider positive-spectral family was constructed:

\[
C_p(t)=(1+\theta_p t)^{-p},
\]

with

\[
\theta_p=e^{0.3474/p}-1.
\]

This is the Laplace transform of the Gamma spectral density

\[
\rho_p(E)
=
\frac{E^{p-1}e^{-E/\theta_p}}
{\Gamma(p)\theta_p^p},
\qquad E\ge0.
\]

Every member is exactly gapless because its spectral support reaches \(E=0\).

Every member is also matched to:

\[
m_{\rm eff}(0.5)=0.3474
\]

and uses the same finite interval \(t/a=0,\ldots,10\).

The family deliberately varies shape while holding the initial mass scale fixed.

### 11.1 Batch results

CORR-I v0.1.2 produced:

| Representation | Baseline | Plateau | \(\alpha_{\max}^{high}\) | \(\alpha_{\max}^{deep}\) | \(R_{\rm contract}\) | \(R/R_{\rm massive}\) |
|---|---|---:|---:|---:|---:|---:|
| gapless \(p=0.5\) | POSITIVE-SPECTRAL CONSISTENT | no | 0.065539 | 0.032831 | **0.500947** | **65.2×** |
| gapless \(p=1\) | POSITIVE-SPECTRAL CONSISTENT | no | 0.062299 | 0.020367 | **0.326916** | **42.5×** |
| gapless \(p=2\) | POSITIVE-SPECTRAL CONSISTENT | no | 0.071142 | 0.012707 | **0.178612** | **23.2×** |
| gapless \(p=4\) | POSITIVE-SPECTRAL CONSISTENT | no | 0.099413 | 0.008404 | **0.084534** | **11.0×** |
| gapless \(p=8\) | POSITIVE-SPECTRAL CONSISTENT | no | 0.162982 | 0.006139 | **0.037668** | **4.90×** |
| massive plateau control | POSITIVE-SPECTRAL CONSISTENT | yes | 0.500000 | 0.003844 | **0.007688** | **1×** |

The entire gapless family passed the positive-spectral baseline tests.

The contraction ratios obeyed the preregistered ordering:

\[
R_{0.5}>R_1>R_2>R_4>R_8>R_{\rm massive}.
\]

As \(p\) increases, the gapless correlator becomes progressively more exponential-like over the finite observation window, and its CORR-I response moves progressively toward the massive result.

Crucially, even the deliberately difficult \(p=8\) control remains separated:

\[
R_{p=8}\approx4.90\,R_{\rm massive}.
\]

At the deepest near-zero scan point it also allows approximately \(1.60\times\) more added spectral weight than the massive control.

---

## 12. What YM-2 has established

YM-2 has established the following.

### 12.1 The original short spectral-ladder representation is insufficient

The vacuum-anchored five-state spectrum does not provide the desired vacuum-specific obstruction under STRUC-I/STRUC-PERC-I.

The negative result is structurally informative:

- connectivity is not admissibility;
- fragmentation alone is not a mass-gap diagnostic;
- a representation can be too compressed to preserve the distinction under investigation.

### 12.2 CORR-I is a discriminating spectral-structure chamber

CORR-I distinguishes:

- a stable exponential massive-side representation;
- a genuinely gapless positive-spectral continuum;
- a controlled family of gapless spectra approaching exponential behavior.

The chamber does not reject gapless controls as spectrally invalid. Instead, it reads their low-energy compatibility envelopes differently.

### 12.3 Strong near-zero contraction is not a trivial consequence of positivity

All gapless controls are positive-spectral consistent.

Yet their \(R_{\rm contract}\) values remain substantially above the massive value.

Therefore:

\[
\boxed{
\text{positive spectral consistency alone does not force the massive-side CORR-I signature.}
}
\]

### 12.4 The massive-side signature is robust to the first representation perturbation

The noisy Figure-7 reconstruction and the clean published-mass plateau control give nearly the same strong near-zero contraction despite very different exact positivity behavior.

Therefore:

\[
\boxed{
\text{the observed envelope contraction is not an artifact of the late-time Figure-7 fluctuation alone.}
}
\]

### 12.5 A finite-window limitation has been exposed rather than hidden

The Gamma family shows a continuous approach toward the massive response as \(p\) increases.

This is important. A sufficiently exponential-looking gapless correlator can imitate aspects of massive behavior over a finite Euclidean-time window.

CORR-I therefore does not provide a binary theorem from one short correlator.

Instead, YM-2 has identified a measurable structural separation whose persistence must now be tested under refinement and, eventually, under longer/independent correlator information.

---

## 13. What YM-2 has not established

The following claims are **not** made.

1. CORR-I has not proved the Yang–Mills mass gap.
2. The AT20 Figure-7 reconstruction is not the authors’ raw \(C(t)\) dataset.
3. The current physical-side envelope uses descriptive relative limits because full pointwise covariance information is unavailable.
4. The massive control is a controlled representation anchored to the published mass, not an independent measurement.
5. The current result has not yet been shown to survive the lattice-refinement sequence.
6. No structural-distance-to-Hamiltonian-energy bridge theorem has yet been proved.
7. The current chamber metric \(R_{\rm contract}\) is a UNNS diagnostic coordinate, not itself the physical gap \(\Delta\).

These limits do not negate the YM-2 result. They define exactly what must be tested next.

---

## 14. Stage verdict

### YM-2 verdict

\[
\boxed{\textbf{VACUUM-BOUNDARY DIAGNOSTIC ESTABLISHED; REFINEMENT TEST REQUIRED}}
\]

More explicitly:

> The first spectral-ladder representation failed the preregistered vacuum-specific criterion. A correlator-native chamber was therefore developed and frozen. CORR-I distinguishes the AT20 massive-side representation from multiple legitimate positive-spectral gapless controls. The separation is systematic across a controlled Gamma-family and is robust to replacement of the noisy Figure-7 reconstruction by a published-mass plateau control. This establishes a viable structural discriminator for the next phase, but not yet refinement-stable Yang–Mills non-crossability.

This is the correct close of YM-2.

---

## 15. Frozen handoff to YM-3

YM-3 must now test the actual project hypothesis under refinement.

The next question is:

\[
\boxed{
\text{Does the massive-side CORR-I signature persist across the AT20 refinement sequence?}
}
\]

The available β sequence is:

\[
5.6924,\;
5.80,\;
5.8941,\;
5.99,\;
6.0625,\;
6.235,\;
6.3380,\;
6.50.
\]

The required YM-3 logic is:

\[
\text{coarse YM}
\rightarrow
\text{fine YM}
\rightarrow
a\to0,
\]

while tracking whether the same correlator-side separation from the gapless controls is preserved.

A positive YM-3 outcome would require more than the persistence of a nonzero fitted mass. It would require the **structural diagnostic itself** to remain on the massive side under refinement.

A negative YM-3 outcome would be equally decisive: if the CORR-I separation collapses, reverses, or is shown to be an artifact of finite resolution, the present YM-2 signature must not be promoted into a Yang–Mills structural law.

---

## 16. Frozen research statement after YM-2

The project can now state the following, and no more:

> **At fixed finest AT20 resolution, a correlator-native UNNS chamber identifies a strong near-zero compatibility-envelope contraction for the massive \(0^{++}\) representation. The same chamber accepts multiple exactly gapless positive-spectral controls but assigns them systematically weaker contraction. This establishes a discriminating vacuum-boundary diagnostic. Whether that diagnostic represents Yang–Mills vacuum non-crossability depends on its survival under common refinement.**

This statement is the starting point for YM-3.

---

## 17. Key artifacts at stage close

### Physical/source corpus
- AT20 arXiv/JHEP source PDFs
- `at20.zip`
- extracted lattice, mass, continuum, flux and covariance tables

### Spectral-ladder phase
- YM1A refinement ladders
- G0.1 vacuum-anchored deformation inputs
- STRUC-I output
- STRUC-PERC-I physical, offset and control outputs

### CORR-I chamber
- `CORR_I_v011.zip`
- `CORR_I_v012.zip`
- `corr_i_v012.html`

### Physical-side correlator representations
- `CORR_I_AT20_0PP_v001.zip`
- `CORR_I_AT20_0PP_CONTROL_v001.zip`

### Gapless controls
- `CORR_I_GAPLESS_CTRL_v001.zip`
- `CORR_I_GAPLESS_FAM_v001.zip`

### Batch result
- `corr_i_batch_4_csv_files.zip`

---

## 18. Final stage transition

**YM-0:** formalization — complete for current purposes.  
**YM-1:** gauge-invariant corpus — sufficient for current program.  
**YM-2:** vacuum-boundary experiment — **closed by this synthesis**.  
**YM-3:** common refinement — **next active stage**.  
**YM-4:** bridge theorem — not yet entered.

The project therefore advances with the original hypothesis unchanged:

\[
\boxed{
\text{Gapless Yang–Mills continuation is structurally non-generable under refinement,
whereas the massive branch is refinement-stable.}
}
\]

YM-2 has supplied the diagnostic needed to test the second half of that statement.

YM-3 must now determine whether the result survives refinement.

---

## Sources and provenance

This synthesis is based on the local `UNNS_YM_GAP` research record and the following primary/derived materials:

- Athenodorou & Teper (2020), JHEP 11 (2020) 172 / arXiv:2007.06422.
- Original project framing: `project_UNNS_Yang–Mills_ Gap.pdf`.
- Canonical STRUC-I v1.0.4 and STRUC-PERC-I v2.5.0 chamber definitions used during the first representation.
- YM1A/G0.1 physical and adversarial ladder outputs.
- CORR-I v0.1.1 and v0.1.2 self-tests and protocol records.
- β = 6.50 \(0^{++}\) Figure-7 correlator proxy and published-mass plateau control.
- Positive-spectral gapless control and Gamma-family batch results.

No claim in this synthesis depends on treating the digitized Figure-7 proxy as raw lattice correlator data.
