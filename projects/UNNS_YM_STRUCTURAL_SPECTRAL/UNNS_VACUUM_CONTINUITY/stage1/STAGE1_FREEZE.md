# Stage 1 Freeze — Structural Vacuum Continuity

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Project title:** *Vacuum Belongs to the Substrate — Structural Continuity Across the Yang–Mills Vacuum Regime*  
**Record:** `STAGE1_FREEZE.md`  
**Version:** v0.1  
**Status:** **FROZEN**  
**Date:** 2026-09-30  
**Inherited project:** `UNNS_YM_GAP` — **CLOSED; immutable**

---

## 1. Frozen purpose

Stage 1 defines precisely what is meant by:

> **Vacuum belongs to the UNNS Substrate.**

The statement is not that the Yang–Mills physical mass gap vanishes.

### Physical interpretation

In Yang–Mills theory, the vacuum is not an exterior absence of physical structure but the lowest-energy state of the same gauge-field system whose non-vacuum excitations are being studied. Gauge-invariant correlations and excitation channels are defined with respect to that vacuum. The UNNS proposition “vacuum belongs to the substrate” therefore means that the vacuum should be representable as an internal structural state, locus, or limiting regime of the same admissible structural domain as non-vacuum Yang–Mills configurations.

This does not imply that the Hamiltonian spectrum is continuous. A structural trajectory may approach the vacuum continuously while the lowest excited eigenstate remains separated from the vacuum by a nonzero energy gap. The project therefore distinguishes **structural continuity** from **spectral discreteness**.

The physical shorthand is frozen as:

\[
\boxed{\textbf{The mass gap separates eigenvalues, not necessarily structural neighborhoods.}}
\]

This sentence is interpretive, not a theorem connecting the Yang–Mills Hamiltonian spectrum to a particular UNNS metric.

---

## 2. Frozen Stage-1 ontology

Let \(\mathcal A_{\rm YM}\) denote the admissible Yang–Mills-derived UNNS structural domain and let \(V\) denote the vacuum structural object.

The primary Stage-1 ontology is:

\[
\boxed{
V\in\overline{\mathcal A_{\rm YM}\setminus\{V\}}
}
\]

The vacuum is therefore treated first as an **internal closure object**.

Stage 1 does **not** freeze the stronger language “basin,” “attractor,” “fixed point,” or “dynamical regime.” Those descriptions require additional evidence.

The primary hypothesis remains:

\[
\inf_{X\in\mathcal A_{\rm YM}\setminus\{V\}}
D_{\rm struct}(X,V)=0.
\]

The isolation alternative is:

\[
\exists\,\delta_V>0
\quad\text{such that}\quad
D_{\rm struct}(X,V)\ge \delta_V
\]

for every sufficiently refined admissible non-vacuum structure in the tested representation class.

---

## 3. Frozen independent structural representation

The primary representation independent of CORR-I is frozen as:

# **VREF-I — Vacuum-Referenced Profile Representation**

VREF-I is an ordered spatial representation built from a **gauge-invariant observable profile referenced to an independently defined vacuum baseline**.

The primary VREF-I input class is a gauge-invariant Yang–Mills spatial profile such as a connected action-density, energy-density, field-energy, or equivalent gauge-invariant observable profile for which the vacuum/no-source baseline is independently measurable or already removed by the published observable definition.

VREF-I is independent of CORR-I because it does **not** use:

- \(\alpha_{\max}\);
- the Gamma-family gapless adversary;
- \(R_{\rm contract}\);
- \(S_B\);
- effective-mass plateau fitting;
- Hankel/Hausdorff moment acceptance;
- the CORR-I boundary \(S_B=0\).

CORR-I may later be compared with VREF-I, but it cannot define, normalize, tune, or rescue VREF-I.

STRUC-I remains canonical and unchanged. It may be used as a **secondary grammar readout** of VREF-I profile windows, but it does not define the VREF-I vacuum proxy or primary distance.

---

## 4. Frozen operational vacuum proxy

For refinement level \(r\), observable \(O\), and physical coordinate \(x\), define the measured no-source vacuum baseline

\[
\widehat O_{\rm vac}^{(r)}(x).
\]

For a non-vacuum Yang–Mills-derived profile \(X\), define the vacuum-referenced contrast

\[
\Delta O_X^{(r)}(x)
=
\widehat O_X^{(r)}(x)
-
\widehat O_{\rm vac}^{(r)}(x).
\]

If the published observable is already a connected or explicitly vacuum-subtracted profile, the published subtraction convention is retained and

\[
\Delta O_X^{(r)}(x)=0
\]

is the operational vacuum reference.

The finite-data vacuum proxy is therefore

\[
\boxed{
V_r^* \equiv \Delta O^{(r)}(x)=0
}
\]

on the common physical grid.

The zero in this expression is **not** an assumed CORR-I boundary. It follows from the independently defined vacuum subtraction.

### Vacuum-proxy admission rule

A dataset is eligible for the primary VREF-I test only if at least one of the following is true:

1. an explicit no-source vacuum expectation is available under the same ensemble and observable definition; or
2. the published observable is explicitly connected/vacuum-subtracted and the subtraction convention is documented.

If neither condition holds, the dataset may be exploratory but cannot support the primary Stage-2 VREF-I verdict.

Vacuum-baseline uncertainty must be propagated whenever it is available. A published zero baseline is never treated as error-free merely because the plotted central value is zero.

---

## 5. Frozen dimensionless profile coordinate

Let \(O\) have canonical mass dimension \(d_O\). Let \(\ell_{\rm ref}\) be a physical scale declared before the target VREF-I result is inspected and held fixed across the refinement branch.

Define

\[
z_X^{(r)}(u)
=
\ell_{\rm ref}^{d_O}
\Delta O_X^{(r)}(x),
\qquad
u\equiv\frac{x}{\ell_{\rm ref}}.
\]

The coordinate \(u\) is the common dimensionless spatial coordinate.

The profile is **not** normalized to its own peak, norm, integral, or first data point. Such self-normalization would erase precisely the amplitude information required for an operational approach to the vacuum.

If more than one observable channel is available, each channel is first tested separately. No cross-channel weighted average is permitted in the primary Stage-2 test unless its weights are preregistered independently of the target result.

---

## 6. Frozen structural object: fixed-width profile windows

Choose a fixed dimensionless window width \(W\) and fixed offsets

\[
0=\xi_1<\xi_2<\cdots<\xi_m\le W
\]

before the target result is inspected.

At position \(s\), define the ordered VREF-I structural window

\[
L_r(s)
=
\big(
 z_X^{(r)}(s+\xi_1),
 z_X^{(r)}(s+\xi_2),
 \ldots,
 z_X^{(r)}(s+\xi_m)
\big).
\]

The vacuum proxy on the same window is

\[
V_r^*=(0,0,\ldots,0).
\]

The fixed-width rule prevents an artificial decrease of distance merely because fewer data points remain at larger radius or transverse distance.

The spatial ordering is preserved. The ladder is not sorted by amplitude.

---

## 7. Frozen primary VREF-I distance

The primary representation-native vacuum distance is

\[
\boxed{
D_{\rm VREF}^{(r)}(s)
=
\left[
\frac{1}{m}
\sum_{j=1}^{m}
\left(z_X^{(r)}(s+\xi_j)\right)^2
\right]^{1/2}
}
\]

for the single primary observable channel.

Properties:

\[
D_{\rm VREF}^{(r)}(s)\ge0,
\]

and

\[
D_{\rm VREF}^{(r)}(s)=0
\iff
L_r(s)=V_r^*
\]

at the measured resolution.

Measurement uncertainty is propagated around this distance but is not used to redefine the metric itself. This prevents a noisier refinement level from appearing artificially closer to the vacuum merely because its error bars are larger.

An \(L_\infty\) window distance may be used only as a preregistered sensitivity check:

\[
D_{\infty}^{(r)}(s)
=
\max_j |z_X^{(r)}(s+\xi_j)|.
\]

It is not the primary metric.

---

## 8. Frozen physical path

The primary VREF-I structural path is **spatial**, not an artificial global amplitude scaling.

For a localized gauge-invariant non-vacuum structure, the path is

\[
L_r(s_1),
L_r(s_2),
\ldots,
L_r(s_n)
\]

with increasing physical distance from the non-vacuum structural core toward a region independently identified as vacuum/asymptotic baseline support.

The continuity question is therefore:

\[
D_{\rm VREF}^{(r)}(s)
\longrightarrow 0
\]

as the structural window moves from the non-vacuum region into the vacuum-like region, while the representation remains valid and the behavior survives refinement.

### Non-triviality rule

The following do **not** count as primary evidence for structural vacuum continuity:

- multiplying one fixed profile by an imposed sequence \(\lambda\to0\);
- renormalizing every profile to force its tail toward zero;
- deleting nonzero points as the vacuum is approached;
- shrinking the comparison window with \(s\);
- choosing the vacuum baseline from the same tail because it minimizes \(D_{\rm VREF}\);
- tuning \(W\), \(m\), \(\ell_{\rm ref}\), interpolation, or acceptance thresholds after viewing the target outcome.

This clause prevents the hypothesis from becoming a tautology under arbitrary amplitude attenuation.

---

## 9. Frozen refinement requirement

A primary Stage-2 VREF-I refinement verdict requires at least **three ordered refinement levels** to survive admission.

All admitted levels must be mapped onto a common physical/dimensionless coordinate support before comparison.

The primary refinement statement is not that one level reaches a small value. It is that the vacuum-directed profile behavior is compatible across refinement levels and does not reveal a stable positive structural exclusion scale.

A two-level sequence may be used as an independent replication or sensitivity branch but not as the sole primary refinement verdict.

---

## 10. Frozen common-refinement principle

For refinement levels \(r_1,r_2,\ldots\), comparison is performed only on the intersection of physically supported coordinate ranges.

The common grid, interpolation rule, fixed window width, and minimum number of supported points must be frozen before the primary batch.

No extrapolation beyond measured support is permitted in the primary test.

If a finer level loses the physical region required for the frozen comparison, that level fails admission; the grid is not moved merely to retain it.

---

## 11. Frozen admissibility separation

VREF-I distance is **not** itself an admissibility test.

A profile/window enters \(\mathcal A_{\rm YM}\) only if it independently satisfies the preregistered provenance and representation rules:

- Yang–Mills-derived provenance;
- gauge-invariant observable status for the primary branch;
- valid vacuum reference;
- known coordinate ordering and scale mapping;
- finite, reproducible derived values;
- frozen common-refinement support;
- no target-dependent rescue transformation.

A small \(D_{\rm VREF}\) cannot make an otherwise invalid object admissible.

---

## 12. Frozen role of STRUC-I

STRUC-I remains canonical and is not modified.

For VREF-I, STRUC-I may be run on the ordered non-vacuum profile windows as a secondary structural readout to ask whether canonical grammar signatures persist, change, or collapse as the primary VREF-I distance decreases.

STRUC-I does not define:

- \(V_r^*\);
- \(D_{\rm VREF}\);
- the physical common grid;
- the vacuum baseline;
- Stage-2 continuity by itself.

No STRUC-I thresholds are changed to accommodate the new project.

---

## 13. Frozen role of CORR-I

CORR-I remains scientifically useful as a separate temporal/spectral structural coordinate inherited from Stage 0.

Its role in the new project is comparative only.

The project may later ask whether a CORR-I coordinate and VREF-I spatial distance move coherently or differently near the vacuum-like regime.

No CORR-I quantity participates in the definition of VREF-I.

Thus an eventual agreement between CORR-I and VREF-I would be cross-representation evidence rather than self-confirmation.

---

## 14. Frozen Stage-2 positive-evidence requirement

Within the VREF-I representation class, evidence for structural vacuum continuity requires all of the following:

1. at least three admitted refinement levels;
2. a documented independent vacuum baseline or explicit connected/vacuum subtraction;
3. common physical support;
4. fixed-width ordered profile windows;
5. decreasing or vacuum-compatible \(D_{\rm VREF}\) toward the independently identified asymptotic region;
6. no refinement-stable positive lower bound resolved above uncertainty;
7. persistence under the preregistered metric/interpolation sensitivities;
8. no loss of representation admissibility;
9. no dependence on CORR-I in constructing the result.

A finite dataset can support structural continuity over its tested domain. It cannot by itself prove the mathematical infinite-resolution limit

\[
D_{\rm struct}\to0.
\]

---

## 15. Frozen Stage-2 falsification condition

Within the tested VREF-I representation class, the structural-continuity hypothesis is contradicted if sufficiently refined admitted data establish a stable nonzero exclusion scale

\[
\boxed{
D_{\rm VREF}^{(r)}(s)\ge\delta_V>0
}
\]

through the full independently defined vacuum-directed region, with the bound surviving:

- common refinement;
- uncertainty propagation;
- the frozen secondary metric;
- independent observable/profile construction where available.

If the vacuum reference is inadequate, the common grid fails, or uncertainties dominate the putative lower bound, the verdict is **indeterminate**, not isolation-supported.

---

## 16. Frozen separation from spectral discreteness

VREF-I measures structural proximity in a spatial gauge-invariant observable representation.

It does not measure the Hamiltonian mass gap.

The following quantities remain distinct:

\[
D_{\rm VREF}
\qquad\text{structural profile distance,}
\]

\[
\Delta_{\rm spec}
\qquad\text{measured/reconstructed positive spectral scale,}
\]

\[
\Delta_{\rm YM}
\qquad\text{the physical continuum Yang--Mills mass gap.}
\]

Stage 2 addresses the first quantity.

Stage 3 may test whether VREF-I structural approach to the vacuum coexists, in the same theory and preferably matched ensembles/operator sectors, with independently established positive spectral scales.

Such coexistence would support the UNNS proposition

\[
\boxed{
\textbf{structural continuity with spectral discreteness}
}
\]

but would not constitute a proof of the continuum Yang–Mills mass gap.

---

## 17. Frozen Stage-1 outcome

Stage 1 is now frozen around three commitments:

\[
\boxed{
V\in\overline{\mathcal A_{\rm YM}\setminus\{V\}}
}
\]

as the hypothesis to test,

\[
\boxed{
\text{VREF-I: gauge-invariant vacuum-referenced spatial profile representation}
}
\]

as the primary CORR-I-independent representation, and

\[
\boxed{
V_r^*=0
\text{ in independently vacuum-subtracted profile coordinates}
}
\]

as the operational finite-data vacuum proxy.

The project is therefore no longer waiting for a definition of the independent representation or the vacuum proxy.

The next scientific task is **Stage 2 preregistration and source admission for VREF-I**. No target data are to be analyzed before that protocol is frozen.

---

## 18. Immutability rule

This Stage-1 freeze may be superseded only by an explicitly versioned record that states why a frozen assumption proved unusable before the primary Stage-2 result was inspected.

It may not be silently edited in response to an adverse empirical result.
