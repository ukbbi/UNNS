# FINAL_SYNTHESIS.md

## UNNS Yang–Mills Gap / Vacuum Boundary Non-Crossability
### Final Project Synthesis and Closure Record

**Project:** `UNNS_YM_GAP`  
**Final status:** **CLOSED**  
**Closure point:** YM-3B  
**Date closed:** 2026-09-30  
**Final chamber used:** CORR-I v0.1.2  
**Terminal measured-data verdict:** `DATA-INDETERMINATE`  
**Central project hypothesis:** **NOT ESTABLISHED**

---

## 1. Executive conclusion

The project began with the hypothesis:

> **Gapless Yang–Mills continuation is structurally non-generable under refinement, whereas the massive branch is refinement-stable.**

Its stronger formulation was:

> **The Yang–Mills mass gap corresponds to a refinement-stable non-crossability boundary separating the vacuum from every non-vacuum admissible state.**

The investigation did not establish that claim.

The project progressed through increasingly demanding representations:

1. a vacuum-anchored spectral ladder;
2. STRUC-I and STRUC-PERC-I structural tests;
3. a correlator-native chamber, CORR-I;
4. adversarial positive-spectral gapless controls;
5. eight-level Class C refinement;
6. four-level Class B published-data refinement.

The decisive result is the final Class B stage.

For the Sakai-Sasaki four-level measured-data reconstruction, the primary boundary coordinate was

\[
S_B=\log_{10}\!\left(\frac{R_{p=8}}{R_B}\right).
\]

The central sequence was

\[
\boxed{
+0.020350,\quad
+0.035867,\quad
-0.003395,\quad
+0.051851
}
\]

at

\[
\beta=6.20,\ 6.40,\ 6.71,\ 6.93.
\]

Thus the central reconstruction **crossed the proposed structural boundary at \(\beta=6.71\)**.

That negative sign survived:

- the preregistered PCHIP interpolation sensitivity;
- all three nested R3 ladder lengths, L5/L6/L7.

However, the preregistered 2,000-draw pointwise-no-covariance uncertainty ensemble for \(\beta=6.71\) yielded

\[
S_B^{2.5\%}=-0.027454,\qquad
S_B^{50\%}=-0.003285,\qquad
S_B^{97.5\%}=+0.019320,
\]

so the uncertainty distribution spans both sides of zero.

The frozen YM-3B verdict is therefore:

\[
\boxed{\textbf{DATA-INDETERMINATE}}
\]

This does **not** erase the central crossing. It means that the available published-figure precision is insufficient to classify that crossing as a statistically stable falsification.

The correct terminal project statement is:

> **The UNNS Yang–Mills Gap / Vacuum Boundary Non-Crossability project did not establish a refinement-stable non-crossable vacuum boundary. The central Class B refinement trajectory crossed the proposed boundary once, and that crossing survived interpolation and ladder-resolution checks, but the preregistered uncertainty ensemble spanned both sides of the boundary. The evidence therefore does not support the proposed universal structural non-crossability as an established property, while remaining insufficient to demonstrate conclusively that no such structural boundary exists.**

The project is intentionally closed at this point. No further tests are to be used to rescue, tune, or reformulate the original hypothesis inside this project.

At the same time, the negative result exposed a deeper UNNS-level consequence. The vacuum could not be maintained as a structurally external object separated from admissible structure by a universal non-crossable wall. Across the project's representations, admissible structures could be driven arbitrarily toward the vacuum-side construction, and in the final Class B central trajectory the proposed CORR-I boundary was crossed without the representation ceasing to be a valid Yang–Mills-derived structural object.

This motivates the project's principal positive structural interpretation:

\[
\boxed{
\textbf{The vacuum belongs to the UNNS Substrate as an internal structural regime or limit, not as an exterior beyond structure.}
}
\]

This statement is an **UNNS structural conclusion** drawn from the behavior of the tested representations. It is not a theorem about the ontology of quantum field theory, nor does it imply the absence of a physical spectral mass gap.

---


## 2. Original scientific logic

Let \(V\) denote the Yang–Mills vacuum and \(X\) a non-vacuum admissible Yang–Mills structure.

The original structural hypothesis required a strictly positive vacuum separation,

\[
D_{\rm YM}(X,V)\ge\delta_G>0,
\]

surviving refinement.

A gapless continuation would instead require a sequence

\[
V\rightarrow X_1\rightarrow X_2\rightarrow\cdots,
\qquad
E(X_n)-E(V)\rightarrow0^+,
\]

with the structures remaining admissible.

The eventual intended physical bridge was

\[
E(X)-E(V)\ge F_G(D_{\rm YM}(X,V)),
\]

with \(F_G(\delta_G)>0\).

That bridge was never reached. The project therefore remained a structural investigation throughout and never became a proof program for the physical Yang–Mills mass gap.

---

## 3. Frozen methodological requirements

The project imposed four central requirements:

1. use gauge-invariant or explicitly gauge-independent observables;
2. actively construct gapless adversaries rather than infer them from absence;
3. require the structural obstruction to survive common refinement;
4. distinguish a structural diagnostic from a Hamiltonian spectral theorem.

The refinement requirement was decisive. A fixed-resolution separation was never sufficient by itself.

---

## 4. YM-2A — vacuum-anchored spectral ladders

The first representation used five glueball-state coordinates plus an explicit vacuum node.

Four deformation families were constructed:

- `offset`;
- `upctrl`;
- `scale`;
- `gaponly`.

### STRUC-I

STRUC-I did not reject the vacuum-compressed branch.

The six-node ladder remained structurally admissible even under a factor-1024 reduction of the vacuum gap.

Therefore:

\[
\boxed{
\text{the short spectral-ladder representation did not establish vacuum-specific non-crossability}
}
\]

### STRUC-PERC-I

STRUC-PERC-I fragmented under some downward gap deformations, but the directionality test failed:

- downward displacement could fragment;
- upward displacement could also fragment;
- uniform scaling could preserve normalized connectivity;
- gap-only deformation fragmented strongly.

The operative effect was therefore not uniquely approach toward the vacuum.

This yielded an important structural distinction:

\[
\boxed{
\text{connectivity collapse is not equivalent to vacuum non-crossability}
}
\]

The initial representation/test pair was falsified.

---

## 5. YM-2B — CORR-I representation correction

A short extracted mass ladder was recognized as too compressed to retain enough information about spectral support.

The project therefore moved to Euclidean correlators,

\[
C(t)=\int_0^\infty\rho(E)e^{-Et}\,dE,
\qquad
\rho(E)\ge0.
\]

CORR-I was developed to test:

- positivity;
- monotonicity;
- discrete log-convexity;
- effective-mass evolution;
- plateau behavior;
- Hankel/Hausdorff moment consistency;
- compatibility with deliberately added low-energy spectral weight.

The frozen adversary became

\[
C_{\rm adv}(t)
=
(1-\alpha)C(t)+\alpha e^{-\mu(t-t_0)}.
\]

Rather than impose a fixed arbitrary admixture, CORR-I computes

\[
\alpha_{\max}(\mu),
\]

the maximum compatible low-energy spectral admixture.

The stage coordinate was

\[
R_{\rm contract}
=
\frac{\alpha_{\max}(\mu/m_{\rm ref}=10^{-3})}
{\alpha_{\max}(\mu/m_{\rm ref}=1)}.
\]

Smaller \(R_{\rm contract}\) means stronger contraction of the near-zero compatibility envelope.

This is a UNNS diagnostic coordinate. It is not the physical Yang–Mills gap.

---

## 6. YM-2 fixed-resolution discrimination

At the finest AT20 resolution, the massive control yielded

\[
R_{\rm massive}\approx0.007688.
\]

The positive-spectral gapless Gamma family yielded:

| Representation | \(R_{\rm contract}\) | Relative to massive |
|---|---:|---:|
| gapless \(p=0.5\) | 0.500947 | 65.2× |
| gapless \(p=1\) | 0.326916 | 42.5× |
| gapless \(p=2\) | 0.178612 | 23.2× |
| gapless \(p=4\) | 0.084534 | 11.0× |
| gapless \(p=8\) | 0.037668 | 4.90× |
| massive control | 0.007688 | 1× |

Every gapless member remained positive-spectral consistent.

Therefore positive spectral consistency alone did not force the massive-side CORR-I response.

The noisy AT20 Figure-7 reconstruction and the clean published-mass control also produced similar near-zero contraction:

\[
R_{\rm raw}\approx0.00716,
\qquad
R_{\rm massive}\approx0.00769.
\]

This supported the conclusion that the observed contraction was not created solely by the late-time fluctuation in the digitized figure.

YM-2 therefore closed with:

> **VACUUM-BOUNDARY DIAGNOSTIC ESTABLISHED; REFINEMENT TEST REQUIRED**

That statement was explicitly provisional.

---

## 7. YM-3A — eight-level Class C model refinement

YM-3A used exact mass-anchored exponential controls built from the eight-level AT20 refinement sequence.

Evidence class:

**Class C — mass-anchored model controls, not measured correlators.**

The frozen result was:

\[
\boxed{\textbf{MODEL-REFINEMENT PERSISTENT}}
\]

Across all eight levels:

- the massive controls remained on the massive side of the fixed hardest gapless reference;
- the beta-matched Gamma controls preserved the required ordering;
- the qualitative separation did not reverse under the native-grid diagnostic.

The matched structural separation increased overall toward the finest lattice, reaching

\[
S_{\rm match}(6.50)\approx1.589194.
\]

This was a genuine positive result, but only for the model family.

The project explicitly prohibited promotion of this result into a measured-data or continuum claim.

---

## 8. Why YM-3A was not decisive

A Class C correlator is constructed from a published fitted mass as an exact exponential.

Such a control is useful because it tests whether the CORR-I signature itself survives a prescribed refinement of the mass scale.

But it does not preserve:

- measured effective-mass fluctuations;
- non-single-exponential contamination;
- finite-sample correlator structure;
- the actual covariance of the lattice measurement.

Therefore YM-3A established:

> **model-refinement persistence**

but not:

> **measured Yang–Mills correlator refinement persistence.**

This distinction became decisive in YM-3B.

---

## 9. YM-3B — Class B measured-data refinement

The primary Class B source was Sakai & Sasaki (2023), with four ordered pure-SU(3) ensembles:

\[
\beta=6.20,\ 6.40,\ 6.71,\ 6.93.
\]

The \(A_1^{++}/0^{++}\) ground-state effective-mass trajectories from Figures 9–12 were digitized and reconstructed into normalized variational-eigenvalue proxies.

The common physical-time grid was

\[
u=
0.31,\ 0.36,\ 0.41,\ 0.46,\ 0.51,\ 0.56,\ 0.61.
\]

The primary interpolation, PCHIP sensitivity, matched Gamma adversaries, R3 nested ladders and uncertainty procedure were frozen before the scientific batch.

All four levels passed the input-admission procedure.

---

## 10. YM-3B primary result

The central result was:

| \(\beta\) | \(R_B\) | \(R_{p=8}\) | \(S_B\) | PCHIP \(S_B\) |
|---:|---:|---:|---:|---:|
| 6.20 | 0.088575860 | 0.092825100 | +0.020350 | +0.019648 |
| 6.40 | 0.082775197 | 0.089901538 | +0.035867 | +0.036198 |
| **6.71** | **0.092699571** | **0.091977820** | **−0.003395** | **−0.003948** |
| 6.93 | 0.082333274 | 0.092774114 | +0.051851 | +0.052060 |

The complete matched ordering

\[
R_{0.5}>R_1>R_2>R_4>R_8>R_B
\]

failed at \(\beta=6.71\), precisely because

\[
R_B>R_8.
\]

This is the central crossing.

---

## 11. The crossing was structurally persistent under representation checks

For \(\beta=6.71\):

\[
S_B^{L5}=-0.007663,
\]

\[
S_B^{L6}=-0.006666,
\]

\[
S_B^{L7}=-0.003395.
\]

Thus the sign did not depend on choosing five, six, or seven common-grid points.

The PCHIP result was likewise negative:

\[
S_B^{\rm PCHIP}=-0.003948.
\]

Therefore the crossing cannot be dismissed as an artifact of the primary interpolation rule or the chosen nested ladder length.

This is the strongest adverse result obtained by the project.

---

## 12. Why the project does not claim definitive falsification

The preregistered 2,000-draw pointwise-no-covariance sensitivity ensemble produced:

| \(\beta\) | 2.5% | median \(S_B\) | 97.5% | \(P(S_B>0)\) |
|---:|---:|---:|---:|---:|
| 6.20 | +0.004053 | +0.020325 | +0.035659 | 0.9955 |
| 6.40 | +0.017167 | +0.035606 | +0.053094 | 1.0000 |
| **6.71** | **−0.027454** | **−0.003285** | **+0.019320** | **0.3935** |
| 6.93 | +0.024726 | +0.052621 | +0.081194 | 1.0000 |

At \(\beta=6.71\), approximately 60.65% of the draws were negative and 39.35% positive.

The uncertainty therefore dominates the sign of the only central crossing.

Under the frozen preregistration this forces:

\[
\boxed{\textbf{DATA-INDETERMINATE}}
\]

rather than `DATA-REFINEMENT CROSSED`.

The project does not weaken or hide the central crossing, but it also does not promote it beyond the precision of the source.

---

## 13. Additional Class B limitations

The four reconstructed SS23 common-grid baselines were classified as `SPECTRAL-POSITIVITY TENSION` under CORR-I's strict moment checks.

This is consistent with their provenance as digitized published effective-mass trajectories rather than raw covariance-preserving correlators.

The \(\beta=6.93\) common-grid reconstruction also did not satisfy the frozen plateau detector even though its boundary coordinate remained positive.

These facts reinforce the final decision not to claim a continuum structural theorem from the Class B reconstruction.

---

## 14. Integrated scientific interpretation

The project produced three experimentally distinct outcomes and one deeper structural consequence.

### A. Representation falsification

The first short spectral-ladder representation failed to produce vacuum-specific non-crossability.

This was already significant. When the vacuum gap was compressed, STRUC-I continued to admit the resulting structures rather than treating approach toward the vacuum as approach toward an exterior non-structural domain.

### B. Controlled diagnostic success

CORR-I successfully distinguished massive-side and gapless positive-spectral controls at fixed resolution and under Class C model refinement.

This showed that a useful structural coordinate could be built, but it did not show that the coordinate defined an ontological wall.

### C. Measured-data non-confirmation

When the test moved to a Class B sequence preserving published effective-mass structure, the universal separation was no longer maintained in the central values.

A refinement-stable non-crossable boundary must not rely on replacing measured correlator structure by exact mass-anchored exponentials.

The central Class B crossing therefore provides evidence **against treating the proposed CORR-I boundary as an established universal structural boundary**.

Because its uncertainty spans zero, the project stops short of claiming that the boundary has been conclusively disproved.

### D. Ontological consequence inside the UNNS framework

The failed boundary hypothesis changes how the vacuum should be positioned inside UNNS.

The original working picture implicitly suggested

\[
\text{admissible structure}
\quad\Big|\quad
\text{structurally forbidden region}
\quad\Big|\quad
V.
\]

The experiments did not support that geometry.

A more faithful UNNS interpretation of the observed behavior is

\[
\text{admissible structure}
\longrightarrow
\text{increasingly vacuum-like structure}
\longrightarrow
V,
\]

all within a common structural domain.

Thus the vacuum should no longer be treated as an ontological exterior to the substrate. Operationally, the project supports

\[
\boxed{
V\in\mathcal S_{\rm UNNS}
}
\]

rather than a picture in which \(V\) lies outside the structural space.

In this sense:

> **Vacuum is not the absence of UNNS structure. It is a distinguished internal structural regime, limit, or locus of the substrate.**

This is the principal positive conceptual gain of the project.

It also exposes a previously implicit assumption:

\[
\text{physical spectral gap}
\Longrightarrow
\text{positive structural separation from vacuum}.
\]

The project did not establish that implication. On the contrary, its results make the alternative structurally natural:

\[
\boxed{
\text{spectral separation need not imply structural separation}
}
\]

and therefore:

\[
\boxed{
\textbf{structural continuity can coexist with spectral discreteness.}
}
\]

The latter statement is not claimed here as a completed cross-domain law. It is the new principle suggested by the closed project and the natural starting point for any successor investigation.

The important distinction is therefore no longer simply “massive structure versus vacuum.” It is between:

- **spectral distinction**, which concerns the physical energy spectrum; and
- **structural location**, which concerns where the vacuum and non-vacuum configurations sit inside UNNS admissibility space.

The closed project provides no basis for identifying these two notions.

---

## 15. Final status of the original hypothesis

### Not established

The project did not establish:

\[
D_{\rm YM}(X,V)\ge\delta_G>0
\]

for all admissible non-vacuum Yang–Mills structures under refinement.

### Challenged by the measured-data central trajectory

The Class B central reconstruction contains a boundary crossing:

\[
S_B(6.71)<0.
\]

That crossing is stable to interpolation and R3 ladder length.

### Not conclusively falsified

The preregistered uncertainty ensemble crosses \(S_B=0\), preventing a definitive empirical falsification claim from the published figures alone.

Therefore the terminal status is:

\[
\boxed{
\textbf{UNIVERSAL STRUCTURAL VACUUM NON-CROSSABILITY: NOT ESTABLISHED}
}
\]

with the stronger note:

\[
\boxed{
\textbf{THE CENTRAL CLASS B TRAJECTORY IS COMPATIBLE WITH STRUCTURAL CROSSABILITY}
}
\]

---

## 16. What the project did establish

The project leaves several positive results that remain valid independently of the failed central hypothesis.

1. **Connectivity is not admissibility.**  
   STRUC-PERC-I fragmentation alone cannot be used as a Yang–Mills vacuum-gap diagnostic.

2. **Representation depth matters.**  
   A short sorted mass ladder can erase distinctions retained by the Euclidean correlator structure.

3. **Positive spectral consistency is not sufficient to determine the CORR-I near-zero response.**  
   Legitimate gapless positive-spectral controls can differ systematically from an exponential massive control.

4. **Finite-window gapless spectra can approach massive-looking correlator behavior continuously.**  
   The Gamma family exposed this explicitly.

5. **Model-level persistence does not imply measured-data persistence.**  
   YM-3A and YM-3B together demonstrate why evidence classes must remain separated.

6. **A structural discriminator need not be equivalent to a physical spectral gap.**  
   No bridge theorem was established, and the measured-data behavior provides no basis for assuming such equivalence.

7. **The vacuum need not be structurally exterior to the UNNS domain.**  
   The project did not find a universal forbidden structural interval isolating the vacuum. In the operational UNNS representation used here, admissible structures remain definable while approaching the vacuum-side regime, and the final central Class B trajectory crosses the proposed boundary without leaving the structural representation. This supports the UNNS interpretation

   \[
   \boxed{
   \text{vacuum is an internal regime of the substrate}
   }
   \]

   rather than an external absence of structure.

8. **Spectral discreteness and structural continuity are logically distinct.**  
   A nonzero physical energy gap does not, by itself, imply a nonzero UNNS structural distance from the vacuum. The missing YM-4 bridge is therefore not a technical afterthought; it marks a genuinely nontrivial logical step that the project never established.

These are durable methodological and conceptual gains of the project.

The seventh and eighth points are statements about the **UNNS structural interpretation of the evidence**, not independent theorems about continuum Yang–Mills theory.

---

## 17. Claims explicitly rejected at closure

The project does **not** claim:

- proof of the Yang–Mills mass gap;
- disproof of the Yang–Mills mass gap;
- a theorem that no mathematical or physical vacuum boundary of any kind exists;
- a theorem that every possible UNNS representation must be structurally crossable;
- a Hamiltonian interpretation of \(R_{\rm contract}\) or \(S_B\);
- a continuum theorem derived from digitized published figures;
- equivalence between CORR-I structural separation and spectral discreteness.

The project **does** adopt the following internal UNNS interpretation of its completed evidence:

> **The Yang–Mills vacuum should be represented as belonging to the UNNS structural domain rather than as an exterior beyond it.**

This follows from the failure to establish a universal forbidden structural interval, together with the persistence of admissible/meaningful structural representations arbitrarily close to—and centrally across—the proposed boundary.

The distinction is essential: **internal structural inclusion of the vacuum is not the same claim as absence of a physical spectral mass gap.**

---

## 18. Reason for closure

The project is closed by decision after the first preregistered Class B measured-data refinement experiment.

The reason is methodological, not logistical:

> **The stronger structural non-crossability hypothesis did not receive the measured-data support required by its own refinement criterion.**

No further datasets, chamber modifications, alternative thresholds, or reformulations will be introduced inside `UNNS_YM_GAP` to seek a favorable outcome.

Specifically cancelled as continuations of this project:

- Liang14 Class B replication;
- Chen06 extension;
- additional source hunting;
- CORR-I redesign intended to restore separation;
- YM-4 bridge-theorem development under the original non-crossability premise.

The source files already collected may remain in the archive for provenance, but no additional test belongs to the closed project.

---

## 19. Relation to any future project

The closure of `UNNS_YM_GAP` does more than motivate an arbitrary opposite hypothesis. It exposes a new structural question that did not exist in the original formulation.

The old project asked:

> **Is the vacuum structurally isolated by a refinement-stable non-crossable boundary?**

Its answer was:

> **That universal structural isolation was not established.**

The deeper UNNS consequence is that the vacuum can no longer be treated naturally as something outside the substrate. The completed evidence instead motivates the structural picture

\[
V\in\mathcal S_{\rm UNNS}.
\]

A successor project may therefore begin from:

\[
\boxed{
\textbf{Vacuum belongs to the substrate.}
}
\]

and test the stronger dynamical proposition:

\[
\boxed{
\textbf{Structural continuity can coexist with spectral discreteness.}
}
\]

Such a future investigation would ask whether structural crossability itself is refinement-stable and whether massive spectral organization can persist while structural trajectories enter, approach, or traverse vacuum-like regimes.

This is **not** a retroactive reinterpretation of the closed experiment. The frozen empirical result remains:

> **The proposed refinement-stable structural vacuum boundary was not established; the central Class B trajectory crossed the proposed boundary once, while uncertainty prevented definitive falsification.**

The new project would use that result as **Stage 0 / origin evidence** and would explicitly identify the positive conceptual inheritance:

> **The vacuum is treated as an internal UNNS structural regime rather than as an ontological exterior.**

See:

`docs/STAGE0_ORIGIN.md`

---

## 20. Final phase record

| Stage | Purpose | Terminal status |
|---|---|---|
| YM-0 | formalization and falsification rules | **COMPLETE** |
| YM-1 | gauge-invariant working corpus | **COMPLETE / SUFFICIENT** |
| YM-2A | spectral-ladder vacuum-boundary test | **REPRESENTATION/TEST PAIR FALSIFIED** |
| YM-2B | CORR-I fixed-resolution diagnostic | **DIAGNOSTIC ESTABLISHED** |
| YM-3A | eight-level Class C common refinement | **MODEL-REFINEMENT PERSISTENT** |
| YM-3B | four-level Class B measured-data refinement | **DATA-INDETERMINATE; CENTRAL CROSSING PRESENT** |
| YM-4 | structural-to-Hamiltonian bridge theorem | **NOT ENTERED / CANCELLED** |

Final project status:

\[
\boxed{\textbf{CLOSED}}
\]

Final central-hypothesis status:

\[
\boxed{\textbf{NOT ESTABLISHED}}
\]

Principal positive conceptual gain:

\[
\boxed{
\textbf{VACUUM BELONGS TO THE UNNS STRUCTURAL DOMAIN}
}
\]

with the explicit qualification that this is an UNNS structural interpretation of the completed evidence, not a theorem about the physical Yang–Mills spectrum.

---

## 21. Canonical terminal records

The authoritative final records are:

- `docs/FINAL_SYNTHESIS.md` — complete scientific synthesis;
- `FINAL_STATUS.md` — concise closure status;
- `docs/STAGE0_ORIGIN.md` — immutable handoff for any future project;
- `docs/SYNTHESIS_YM2.md` — frozen YM-2 record;
- `docs/YM3_RESULT.md` — frozen YM-3A Class C record;
- `docs/YM3B_RESULT.md` — frozen YM-3B Class B record;
- `output/ym3b/YM3B_SUMMARY.csv` — central Class B results;
- `output/ym3b/YM3B_R3.csv` — nested-ladder sensitivity;
- `output/ym3b/YM3B_UNCERTAINTY_SUMMARY.csv` — uncertainty summary;
- `docs/FINAL_MANIFEST.json` — closure manifest and hashes.

No later scientific result belongs to this project unless the project is explicitly reopened as a new version, which is not part of the present closure.
